"""
Parallel Agent Execution with Rate Limiting

Description: Pattern for executing multiple async agents in parallel with semaphore-based
rate limiting, timeout handling, and retry logic. Ensures controlled concurrency while
maximizing throughput for multi-agent systems.

Use Cases:
- Executing multiple LLM API calls in parallel without exceeding rate limits
- Coordinating parallel research tasks across specialized agents
- Managing concurrent database or external API operations
- Any scenario requiring controlled parallel async execution
- Load balancing across multiple service instances

Dependencies:
- asyncio (for parallel execution and semaphores)
- typing (for type hints)
- time (for timing measurements)

Notes:
- Semaphores prevent overwhelming APIs with too many concurrent requests
- Individual timeouts prevent single slow agents from blocking the swarm
- Return exceptions pattern allows partial failures without stopping execution
- Retry logic handles transient failures gracefully
- Progress callbacks enable real-time UI updates
- Works with any async callable, not just agents

Related Snippets:
- hierarchical_agent_coordination.py - Full hierarchical agent system
- agent_lifecycle_management.py - Agent state tracking
- task_routing_and_delegation.py - Intelligent task assignment

Source Attribution:
- Extracted from: /home/coolhand/projects/beltalowda/src/beltalowda/orchestrator.py
- Method: _execute_belters_parallel() (lines 498-636)
- Original author: Luke Steuber
- Project: Beltalowda Multi-Agent Orchestration Platform
"""

import asyncio
import time
from typing import List, Optional, Any, Callable, TypeVar, Generic
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# TYPE DEFINITIONS
# ============================================================================

T = TypeVar('T')  # Generic type for task results


class ExecutionStatus(str, Enum):
    """Status of individual task execution"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    RETRYING = "retrying"


@dataclass
class ExecutionResult(Generic[T]):
    """Result of a single task execution"""
    task_id: str
    status: ExecutionStatus
    result: Optional[T] = None
    error: Optional[str] = None
    execution_time: float = 0.0
    retry_count: int = 0


@dataclass
class ParallelExecutionConfig:
    """Configuration for parallel execution"""
    max_concurrent: int = 10
    timeout_seconds: float = 60.0
    enable_retries: bool = True
    max_retries: int = 2
    retry_delay: float = 1.0


# ============================================================================
# PARALLEL EXECUTOR
# ============================================================================

class ParallelExecutor:
    """
    Executes async tasks in parallel with rate limiting and error handling.

    Features:
    - Semaphore-based concurrency control
    - Per-task timeout handling
    - Automatic retry for failed tasks
    - Progress callbacks for real-time updates
    - Graceful degradation on partial failures
    """

    def __init__(self, config: Optional[ParallelExecutionConfig] = None):
        """Initialize executor with configuration"""
        self.config = config or ParallelExecutionConfig()
        self.semaphore = asyncio.Semaphore(self.config.max_concurrent)

    async def execute_parallel(
        self,
        tasks: List[Callable],
        task_args: Optional[List[tuple]] = None,
        progress_callback: Optional[Callable] = None
    ) -> List[ExecutionResult]:
        """
        Execute multiple async tasks in parallel.

        Args:
            tasks: List of async callables to execute
            task_args: Optional list of argument tuples for each task
            progress_callback: Optional callback(task_id, status, data)

        Returns:
            List of ExecutionResult objects
        """
        # Prepare task arguments
        if task_args is None:
            task_args = [()] * len(tasks)

        # Execute all tasks
        execution_tasks = [
            self._execute_with_limit_and_timeout(
                task_id=f"task_{i}",
                task=task,
                args=args,
                progress_callback=progress_callback
            )
            for i, (task, args) in enumerate(zip(tasks, task_args))
        ]

        results = await asyncio.gather(*execution_tasks, return_exceptions=True)

        # Process results and handle retries
        processed_results = []
        retry_tasks = []

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                # Convert exception to ExecutionResult
                error_result = ExecutionResult(
                    task_id=f"task_{i}",
                    status=ExecutionStatus.FAILED,
                    error=str(result)
                )
                processed_results.append(error_result)

                # Queue for retry if enabled
                if self.config.enable_retries:
                    retry_tasks.append((i, tasks[i], task_args[i]))
            else:
                processed_results.append(result)

        # Execute retries
        if retry_tasks:
            await self._execute_retries(retry_tasks, processed_results, progress_callback)

        return processed_results

    async def _execute_with_limit_and_timeout(
        self,
        task_id: str,
        task: Callable,
        args: tuple,
        progress_callback: Optional[Callable]
    ) -> ExecutionResult:
        """Execute single task with semaphore limiting and timeout"""
        async with self.semaphore:
            start_time = time.time()

            # Notify start
            if progress_callback:
                await progress_callback(task_id, ExecutionStatus.RUNNING, None)

            try:
                # Execute with timeout
                result = await asyncio.wait_for(
                    task(*args),
                    timeout=self.config.timeout_seconds
                )

                execution_time = time.time() - start_time

                # Notify completion
                if progress_callback:
                    await progress_callback(task_id, ExecutionStatus.COMPLETED, result)

                return ExecutionResult(
                    task_id=task_id,
                    status=ExecutionStatus.COMPLETED,
                    result=result,
                    execution_time=execution_time
                )

            except asyncio.TimeoutError:
                execution_time = time.time() - start_time

                # Notify timeout
                if progress_callback:
                    await progress_callback(task_id, ExecutionStatus.TIMEOUT, None)

                return ExecutionResult(
                    task_id=task_id,
                    status=ExecutionStatus.TIMEOUT,
                    error=f"Timeout after {self.config.timeout_seconds}s",
                    execution_time=execution_time
                )

            except Exception as e:
                execution_time = time.time() - start_time

                # Notify failure
                if progress_callback:
                    await progress_callback(task_id, ExecutionStatus.FAILED, str(e))

                return ExecutionResult(
                    task_id=task_id,
                    status=ExecutionStatus.FAILED,
                    error=str(e),
                    execution_time=execution_time
                )

    async def _execute_retries(
        self,
        retry_tasks: List[tuple],
        results: List[ExecutionResult],
        progress_callback: Optional[Callable]
    ):
        """Execute retries for failed tasks"""
        for retry_count in range(self.config.max_retries):
            if not retry_tasks:
                break

            # Wait before retry
            await asyncio.sleep(self.config.retry_delay)

            next_retry_tasks = []

            for idx, task, args in retry_tasks:
                task_id = f"task_{idx}_retry_{retry_count + 1}"

                # Notify retry
                if progress_callback:
                    await progress_callback(task_id, ExecutionStatus.RETRYING, None)

                retry_result = await self._execute_with_limit_and_timeout(
                    task_id=task_id,
                    task=task,
                    args=args,
                    progress_callback=progress_callback
                )

                retry_result.retry_count = retry_count + 1

                # Update result if retry succeeded
                if retry_result.status == ExecutionStatus.COMPLETED:
                    results[idx] = retry_result
                else:
                    # Queue for another retry if still failing
                    if retry_count < self.config.max_retries - 1:
                        next_retry_tasks.append((idx, task, args))
                    else:
                        # Update with final failed result
                        results[idx] = retry_result

            retry_tasks = next_retry_tasks


# ============================================================================
# AGENT-SPECIFIC PARALLEL EXECUTOR
# ============================================================================

class AgentSwarmExecutor:
    """
    Specialized executor for agent swarm execution with progress tracking.

    Extends ParallelExecutor with agent-specific features like progress
    simulation and detailed status reporting.
    """

    def __init__(self, config: Optional[ParallelExecutionConfig] = None):
        """Initialize agent swarm executor"""
        self.executor = ParallelExecutor(config)
        self.config = config or ParallelExecutionConfig()

    async def execute_agent_swarm(
        self,
        agents: List[Any],
        tasks: List[str],
        progress_callback: Optional[Callable] = None
    ) -> List[ExecutionResult]:
        """
        Execute multiple agents in parallel with progress tracking.

        Args:
            agents: List of agent instances
            tasks: List of task prompts/descriptions
            progress_callback: Callback for progress updates

        Returns:
            List of ExecutionResult objects
        """
        # Create wrapped tasks with progress simulation
        wrapped_tasks = [
            self._create_agent_task_with_progress(agent, task, i, progress_callback)
            for i, (agent, task) in enumerate(zip(agents, tasks))
        ]

        # Execute in parallel
        results = await self.executor.execute_parallel(
            tasks=wrapped_tasks,
            progress_callback=progress_callback
        )

        return results

    async def _create_agent_task_with_progress(
        self,
        agent: Any,
        task: str,
        index: int,
        progress_callback: Optional[Callable]
    ) -> Callable:
        """Create agent task wrapper with progress simulation"""
        async def wrapped_task():
            # Simulate progress stages
            stages = [
                (10, "Initializing agent..."),
                (25, "Analyzing task..."),
                (50, "Processing..."),
                (75, "Generating response..."),
                (95, "Finalizing...")
            ]

            # Start execution in background
            execution_future = asyncio.create_task(
                agent.execute_task(task)
            )

            # Progress simulation
            progress_task = asyncio.create_task(
                self._simulate_progress(index, stages, progress_callback)
            )

            try:
                # Wait for execution to complete
                done, pending = await asyncio.wait(
                    [execution_future, progress_task],
                    return_when=asyncio.FIRST_COMPLETED
                )

                # Cancel progress simulation
                for p in pending:
                    p.cancel()
                    try:
                        await p
                    except asyncio.CancelledError:
                        pass

                # Get result
                if execution_future in done:
                    result = await execution_future
                    if progress_callback:
                        await progress_callback(
                            f"agent_{index}",
                            ExecutionStatus.COMPLETED,
                            {"progress": 100, "description": "Complete"}
                        )
                    return result
                else:
                    return await execution_future

            except Exception as e:
                # Cancel any pending tasks
                for task_obj in [execution_future, progress_task]:
                    if not task_obj.done():
                        task_obj.cancel()
                raise e

        return wrapped_task

    async def _simulate_progress(
        self,
        agent_index: int,
        stages: List[tuple],
        callback: Optional[Callable]
    ):
        """Simulate realistic progress updates"""
        if not callback:
            return

        try:
            for progress, description in stages:
                await callback(
                    f"agent_{agent_index}",
                    ExecutionStatus.RUNNING,
                    {"progress": progress, "description": description}
                )
                await asyncio.sleep(0.5)
        except asyncio.CancelledError:
            pass


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    # Example 1: Basic parallel execution
    async def example_basic():
        """Basic parallel execution with rate limiting"""
        print("Example 1: Basic Parallel Execution")
        print("=" * 60)

        # Define some async tasks
        async def slow_task(task_id: str, delay: float):
            await asyncio.sleep(delay)
            return f"Task {task_id} completed after {delay}s"

        # Create executor with max 3 concurrent tasks
        config = ParallelExecutionConfig(
            max_concurrent=3,
            timeout_seconds=5.0,
            enable_retries=True,
            max_retries=2
        )
        executor = ParallelExecutor(config)

        # Create tasks
        tasks = [
            lambda: slow_task("A", 1.0),
            lambda: slow_task("B", 2.0),
            lambda: slow_task("C", 1.5),
            lambda: slow_task("D", 0.5),
            lambda: slow_task("E", 3.0),
        ]

        # Execute in parallel
        start_time = time.time()
        results = await executor.execute_parallel(tasks)
        total_time = time.time() - start_time

        # Display results
        print(f"\nCompleted {len(results)} tasks in {total_time:.2f}s")
        for result in results:
            print(f"  {result.task_id}: {result.status.value} - {result.result or result.error}")

    # Example 2: Agent swarm execution with progress
    async def example_agent_swarm():
        """Agent swarm execution with progress tracking"""
        print("\n\nExample 2: Agent Swarm Execution")
        print("=" * 60)

        # Mock agent class
        class MockAgent:
            def __init__(self, agent_id: str):
                self.agent_id = agent_id

            async def execute_task(self, task: str):
                await asyncio.sleep(1.5)
                return f"Agent {self.agent_id} completed: {task}"

        # Progress callback
        async def progress_callback(task_id: str, status: ExecutionStatus, data: Any):
            if data and isinstance(data, dict):
                progress = data.get('progress', 0)
                desc = data.get('description', '')
                print(f"  [{task_id}] {progress}% - {desc}")
            else:
                print(f"  [{task_id}] {status.value}")

        # Create agents
        agents = [MockAgent(f"agent_{i}") for i in range(5)]
        tasks = [f"Task {i}" for i in range(5)]

        # Execute swarm
        config = ParallelExecutionConfig(max_concurrent=3, timeout_seconds=10.0)
        swarm_executor = AgentSwarmExecutor(config)

        start_time = time.time()
        results = await swarm_executor.execute_agent_swarm(
            agents=agents,
            tasks=tasks,
            progress_callback=progress_callback
        )
        total_time = time.time() - start_time

        # Display results
        print(f"\nSwarm execution completed in {total_time:.2f}s")
        successful = len([r for r in results if r.status == ExecutionStatus.COMPLETED])
        print(f"  Successful: {successful}/{len(results)}")

    # Example 3: Handling timeouts and retries
    async def example_timeouts():
        """Demonstrate timeout and retry handling"""
        print("\n\nExample 3: Timeout and Retry Handling")
        print("=" * 60)

        # Create some tasks that might timeout
        async def unreliable_task(task_id: str, fail_probability: float):
            import random
            delay = random.uniform(0.5, 3.0)
            await asyncio.sleep(delay)

            if random.random() < fail_probability:
                raise Exception(f"Task {task_id} failed randomly")

            return f"Task {task_id} succeeded after {delay:.2f}s"

        config = ParallelExecutionConfig(
            max_concurrent=3,
            timeout_seconds=2.0,  # Short timeout
            enable_retries=True,
            max_retries=2,
            retry_delay=0.5
        )
        executor = ParallelExecutor(config)

        tasks = [
            lambda: unreliable_task("A", 0.3),
            lambda: unreliable_task("B", 0.3),
            lambda: unreliable_task("C", 0.3),
            lambda: unreliable_task("D", 0.3),
        ]

        # Execute with retries
        results = await executor.execute_parallel(tasks)

        # Display results
        print("\nResults:")
        for result in results:
            status_symbol = "✓" if result.status == ExecutionStatus.COMPLETED else "✗"
            retry_info = f" (retries: {result.retry_count})" if result.retry_count > 0 else ""
            print(f"  {status_symbol} {result.task_id}: {result.status.value}{retry_info}")
            if result.error:
                print(f"     Error: {result.error}")

    # Run all examples
    async def main():
        await example_basic()
        await example_agent_swarm()
        await example_timeouts()

    asyncio.run(main())

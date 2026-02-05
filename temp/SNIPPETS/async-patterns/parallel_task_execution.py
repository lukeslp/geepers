"""
Parallel Task Execution Pattern

Description: Pattern for executing multiple async tasks concurrently with proper
error handling, progress tracking, and result aggregation. Demonstrates how to
orchestrate parallel workflows with asyncio.gather, task grouping, and streaming
updates.

Use Cases:
- Multi-agent AI workflows with parallel processing
- Batch processing with concurrent workers
- Coordinating multiple API calls in parallel
- Swarm-based task decomposition and execution
- Real-time progress tracking for long-running operations

Dependencies:
- asyncio (built-in)
- typing (built-in)
- logging (built-in)
- dataclasses (built-in)

Notes:
- Use asyncio.gather() for parallel execution with return_exceptions=True
- Implement progress callbacks for streaming updates
- Handle partial failures gracefully
- Track execution metrics per task
- Consider using semaphores for rate limiting
- Clean up resources in finally blocks

Related Snippets:
- /home/coolhand/SNIPPETS/async-patterns/async_llm_operations.py
- /home/coolhand/SNIPPETS/streaming-patterns/sse_streaming_responses.py

Source Attribution:
- Extracted from: /home/coolhand/enterprise_orchestration/core/coordinator.py
- Related: /home/coolhand/html/beltalowda/task-swarm/src/beltalowda/orchestrator.py
- Related: /home/coolhand/projects/xai_swarm/core/swarm_orchestrator.py
"""

import asyncio
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, TypeVar, Generic
from enum import Enum

logger = logging.getLogger(__name__)

T = TypeVar('T')


# ============================================================================
# STATUS AND RESULT TRACKING
# ============================================================================

class TaskStatus(Enum):
    """Task execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class TaskResult(Generic[T]):
    """Result container for individual task."""
    task_id: str
    status: TaskStatus
    result: Optional[T] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    execution_time: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'task_id': self.task_id,
            'status': self.status.value,
            'result': self.result,
            'error': self.error,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'execution_time': self.execution_time,
            'metadata': self.metadata
        }


@dataclass
class ParallelExecutionResult(Generic[T]):
    """Aggregate result from parallel execution."""
    results: List[TaskResult[T]]
    total_time: float
    successful_count: int
    failed_count: int
    cancelled_count: int
    total_tasks: int

    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.total_tasks == 0:
            return 0.0
        return self.successful_count / self.total_tasks

    @property
    def all_successful(self) -> bool:
        """Check if all tasks succeeded."""
        return self.successful_count == self.total_tasks

    def get_successful_results(self) -> List[T]:
        """Get all successful results."""
        return [
            r.result for r in self.results
            if r.status == TaskStatus.COMPLETED and r.result is not None
        ]

    def get_failed_tasks(self) -> List[TaskResult[T]]:
        """Get all failed task results."""
        return [r for r in self.results if r.status == TaskStatus.FAILED]


# ============================================================================
# BASIC PARALLEL EXECUTION
# ============================================================================

async def execute_tasks_parallel(
    tasks: List[Callable[..., Any]],
    task_ids: Optional[List[str]] = None,
    return_exceptions: bool = True
) -> ParallelExecutionResult:
    """
    Execute multiple async tasks in parallel.

    Args:
        tasks: List of coroutine functions or coroutines to execute
        task_ids: Optional list of task identifiers
        return_exceptions: If True, exceptions are returned as results

    Returns:
        ParallelExecutionResult with all task outcomes
    """
    start_time = time.time()

    # Generate task IDs if not provided
    if task_ids is None:
        task_ids = [f"task_{i+1}" for i in range(len(tasks))]

    # Initialize result containers
    task_results: List[TaskResult] = []

    # Create task result objects
    for task_id in task_ids:
        task_results.append(TaskResult(
            task_id=task_id,
            status=TaskStatus.PENDING
        ))

    # Execute all tasks in parallel
    try:
        # Ensure we have coroutines
        coros = [
            task() if callable(task) and not asyncio.iscoroutine(task) else task
            for task in tasks
        ]

        # Execute with gather
        results = await asyncio.gather(*coros, return_exceptions=return_exceptions)

        # Process results
        for i, (result, task_result) in enumerate(zip(results, task_results)):
            if isinstance(result, Exception):
                task_result.status = TaskStatus.FAILED
                task_result.error = str(result)
            else:
                task_result.status = TaskStatus.COMPLETED
                task_result.result = result

    except Exception as e:
        logger.error(f"Parallel execution failed: {e}")
        # Mark all remaining tasks as failed
        for task_result in task_results:
            if task_result.status == TaskStatus.PENDING:
                task_result.status = TaskStatus.FAILED
                task_result.error = str(e)

    # Calculate statistics
    total_time = time.time() - start_time
    successful_count = sum(1 for r in task_results if r.status == TaskStatus.COMPLETED)
    failed_count = sum(1 for r in task_results if r.status == TaskStatus.FAILED)
    cancelled_count = sum(1 for r in task_results if r.status == TaskStatus.CANCELLED)

    return ParallelExecutionResult(
        results=task_results,
        total_time=total_time,
        successful_count=successful_count,
        failed_count=failed_count,
        cancelled_count=cancelled_count,
        total_tasks=len(task_results)
    )


# ============================================================================
# PARALLEL EXECUTION WITH PROGRESS TRACKING
# ============================================================================

async def execute_with_progress(
    tasks: List[Callable[..., Any]],
    task_names: Optional[List[str]] = None,
    progress_callback: Optional[Callable] = None
) -> ParallelExecutionResult:
    """
    Execute tasks in parallel with progress tracking and callbacks.

    Args:
        tasks: List of async functions to execute
        task_names: Optional descriptive names for tasks
        progress_callback: Optional callback for progress updates
            Signature: async def callback(event_type: str, data: Dict)

    Returns:
        ParallelExecutionResult with all outcomes
    """
    start_time = time.time()

    if task_names is None:
        task_names = [f"Task {i+1}" for i in range(len(tasks))]

    # Initialize result tracking
    task_results = [
        TaskResult(
            task_id=f"task_{i+1}",
            status=TaskStatus.PENDING,
            metadata={'name': name}
        )
        for i, name in enumerate(task_names)
    ]

    async def execute_with_tracking(index: int, task: Callable) -> Any:
        """Execute single task with progress tracking."""
        task_result = task_results[index]
        task_result.status = TaskStatus.RUNNING
        task_result.started_at = datetime.now()

        # Notify start
        if progress_callback:
            await progress_callback('task_start', {
                'task_id': task_result.task_id,
                'name': task_names[index],
                'index': index,
                'total': len(tasks)
            })

        try:
            # Execute the task
            result = await task()

            task_result.status = TaskStatus.COMPLETED
            task_result.result = result
            task_result.completed_at = datetime.now()
            task_result.execution_time = (
                task_result.completed_at - task_result.started_at
            ).total_seconds()

            # Notify completion
            if progress_callback:
                await progress_callback('task_complete', {
                    'task_id': task_result.task_id,
                    'name': task_names[index],
                    'index': index,
                    'status': 'success',
                    'execution_time': task_result.execution_time
                })

            return result

        except Exception as e:
            task_result.status = TaskStatus.FAILED
            task_result.error = str(e)
            task_result.completed_at = datetime.now()

            if task_result.started_at:
                task_result.execution_time = (
                    task_result.completed_at - task_result.started_at
                ).total_seconds()

            # Notify failure
            if progress_callback:
                await progress_callback('task_error', {
                    'task_id': task_result.task_id,
                    'name': task_names[index],
                    'index': index,
                    'error': str(e)
                })

            return e  # Return exception for gather

    # Notify overall start
    if progress_callback:
        await progress_callback('execution_start', {
            'total_tasks': len(tasks),
            'task_names': task_names
        })

    # Execute all tasks in parallel
    await asyncio.gather(
        *[execute_with_tracking(i, task) for i, task in enumerate(tasks)],
        return_exceptions=True
    )

    # Calculate final statistics
    total_time = time.time() - start_time
    successful_count = sum(1 for r in task_results if r.status == TaskStatus.COMPLETED)
    failed_count = sum(1 for r in task_results if r.status == TaskStatus.FAILED)

    result = ParallelExecutionResult(
        results=task_results,
        total_time=total_time,
        successful_count=successful_count,
        failed_count=failed_count,
        cancelled_count=0,
        total_tasks=len(task_results)
    )

    # Notify overall completion
    if progress_callback:
        await progress_callback('execution_complete', {
            'total_tasks': len(tasks),
            'successful': successful_count,
            'failed': failed_count,
            'total_time': total_time,
            'success_rate': result.success_rate
        })

    return result


# ============================================================================
# GROUPED PARALLEL EXECUTION (BATCHES)
# ============================================================================

async def execute_in_batches(
    tasks: List[Callable[..., Any]],
    batch_size: int = 5,
    delay_between_batches: float = 0.0,
    progress_callback: Optional[Callable] = None
) -> ParallelExecutionResult:
    """
    Execute tasks in batches with configurable concurrency.

    Useful for rate limiting or controlling resource usage.

    Args:
        tasks: List of async functions to execute
        batch_size: Number of tasks to run concurrently per batch
        delay_between_batches: Seconds to wait between batches
        progress_callback: Optional callback for progress updates

    Returns:
        ParallelExecutionResult with all outcomes
    """
    all_results: List[TaskResult] = []
    start_time = time.time()

    # Split tasks into batches
    batches = [
        tasks[i:i + batch_size]
        for i in range(0, len(tasks), batch_size)
    ]

    if progress_callback:
        await progress_callback('batch_execution_start', {
            'total_tasks': len(tasks),
            'num_batches': len(batches),
            'batch_size': batch_size
        })

    for batch_num, batch in enumerate(batches):
        if progress_callback:
            await progress_callback('batch_start', {
                'batch_num': batch_num + 1,
                'total_batches': len(batches),
                'batch_size': len(batch)
            })

        # Execute batch
        batch_result = await execute_tasks_parallel(
            batch,
            task_ids=[
                f"batch_{batch_num+1}_task_{i+1}"
                for i in range(len(batch))
            ]
        )

        all_results.extend(batch_result.results)

        if progress_callback:
            await progress_callback('batch_complete', {
                'batch_num': batch_num + 1,
                'successful': batch_result.successful_count,
                'failed': batch_result.failed_count
            })

        # Delay between batches (except after last batch)
        if delay_between_batches > 0 and batch_num < len(batches) - 1:
            await asyncio.sleep(delay_between_batches)

    # Calculate aggregate statistics
    total_time = time.time() - start_time
    successful_count = sum(1 for r in all_results if r.status == TaskStatus.COMPLETED)
    failed_count = sum(1 for r in all_results if r.status == TaskStatus.FAILED)

    return ParallelExecutionResult(
        results=all_results,
        total_time=total_time,
        successful_count=successful_count,
        failed_count=failed_count,
        cancelled_count=0,
        total_tasks=len(all_results)
    )


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

async def example_basic_parallel():
    """Example: Basic parallel execution."""
    print("=== Basic Parallel Execution ===\n")

    async def task(n: int, delay: float) -> str:
        """Simulated async task."""
        await asyncio.sleep(delay)
        return f"Task {n} completed after {delay}s"

    tasks = [
        task(1, 0.5),
        task(2, 0.3),
        task(3, 0.7),
        task(4, 0.2),
        task(5, 0.6),
    ]

    result = await execute_tasks_parallel(tasks)

    print(f"Total time: {result.total_time:.2f}s")
    print(f"Success rate: {result.success_rate:.1%}")
    print(f"Successful: {result.successful_count}/{result.total_tasks}")
    print()

    for task_result in result.results:
        print(f"  {task_result.task_id}: {task_result.result}")


async def example_with_progress():
    """Example: Parallel execution with progress tracking."""
    print("\n=== Parallel Execution with Progress Tracking ===\n")

    async def progress_callback(event_type: str, data: Dict):
        """Handle progress updates."""
        if event_type == 'task_start':
            print(f"▶ Starting: {data['name']} ({data['index']+1}/{data['total']})")
        elif event_type == 'task_complete':
            print(f"✓ Completed: {data['name']} in {data['execution_time']:.2f}s")
        elif event_type == 'task_error':
            print(f"✗ Failed: {data['name']} - {data['error']}")
        elif event_type == 'execution_complete':
            print(f"\n✅ All tasks complete: {data['successful']}/{data['total_tasks']} "
                  f"successful in {data['total_time']:.2f}s")

    async def simulated_work(name: str, duration: float) -> str:
        """Simulated work."""
        await asyncio.sleep(duration)
        if name == "Agent 3":  # Simulate one failure
            raise Exception("Simulated failure")
        return f"{name} result"

    tasks = [
        lambda: simulated_work("Agent 1", 0.5),
        lambda: simulated_work("Agent 2", 0.3),
        lambda: simulated_work("Agent 3", 0.4),  # This will fail
        lambda: simulated_work("Agent 4", 0.6),
        lambda: simulated_work("Agent 5", 0.2),
    ]

    task_names = [f"Agent {i+1}" for i in range(5)]

    result = await execute_with_progress(tasks, task_names, progress_callback)

    print(f"\nFinal success rate: {result.success_rate:.1%}")


async def example_batched():
    """Example: Batched execution for rate limiting."""
    print("\n=== Batched Parallel Execution ===\n")

    async def api_call(n: int) -> str:
        """Simulated API call."""
        await asyncio.sleep(0.1)
        return f"API call {n} result"

    async def progress_callback(event_type: str, data: Dict):
        """Handle batch progress."""
        if event_type == 'batch_start':
            print(f"Processing batch {data['batch_num']}/{data['total_batches']}")
        elif event_type == 'batch_complete':
            print(f"  ✓ Batch complete: {data['successful']} successful, "
                  f"{data['failed']} failed")

    tasks = [lambda n=i: api_call(n) for i in range(15)]

    result = await execute_in_batches(
        tasks,
        batch_size=5,
        delay_between_batches=0.5,
        progress_callback=progress_callback
    )

    print(f"\nTotal execution time: {result.total_time:.2f}s")
    print(f"All tasks completed: {result.all_successful}")


async def main():
    """Run all examples."""
    await example_basic_parallel()
    await example_with_progress()
    await example_batched()


if __name__ == "__main__":
    asyncio.run(main())

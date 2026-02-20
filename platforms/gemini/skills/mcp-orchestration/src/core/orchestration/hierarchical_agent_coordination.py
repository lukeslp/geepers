"""
Hierarchical Agent Coordination Pattern

Description: Three-tier hierarchical agent architecture for coordinating multi-agent swarms
with parallel execution, synthesis layers, and executive consolidation. This pattern enables
scalable coordination of 1-30+ agents with automatic synthesis at mid and executive levels.

Use Cases:
- Large-scale research tasks requiring multiple perspectives
- Complex analysis that benefits from parallel investigation
- Tasks that need synthesis across multiple specialized domains
- Executive-level strategic planning with comprehensive research
- Any problem requiring hierarchical aggregation of insights

Dependencies:
- asyncio (for parallel agent execution)
- pydantic (for data models)
- enum (for status and role definitions)
- typing (for type hints)

Notes:
- Belter agents (workers) execute in parallel with semaphore-based rate limiting
- Drummer agents (synthesizers) aggregate every 5 Belter responses
- Camina agent (executive) provides final synthesis when 2+ Drummers exist
- Each tier uses progressively lower temperature for consistency
- System automatically scales synthesis layers based on agent count
- Supports timeout handling and retry logic for failed agents

Related Snippets:
- parallel_agent_execution.py - Parallel execution with rate limiting
- agent_lifecycle_management.py - Agent state management
- task_decomposition_pattern.py - Breaking tasks into subtasks
- multi_agent_communication.py - Inter-agent message passing

Source Attribution:
- Extracted from: /home/coolhand/projects/beltalowda/src/beltalowda/
- Core files: orchestrator.py, agents/base.py, agents/belter.py, agents/drummer.py, agents/camina.py
- Original author: Luke Steuber
- Project: Beltalowda Multi-Agent Orchestration Platform
"""

import asyncio
import time
import uuid
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Optional, Any, Callable
from pydantic import BaseModel
from datetime import datetime
from dataclasses import dataclass, field


# ============================================================================
# DATA MODELS
# ============================================================================

class AgentRole(str, Enum):
    """Agent role types in the hierarchical system"""
    BELTER = "belter"           # Level 1: Individual task workers
    DRUMMER = "drummer"         # Level 2: Synthesize 5 Belters
    CAMINA = "camina"           # Level 3: Final executive synthesis
    CITATION_MONITOR = "citation_monitor"
    DECOMPOSER = "decomposer"


class TaskStatus(str, Enum):
    """Task execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentTask(BaseModel):
    """Individual agent task specification"""
    id: str = None
    prompt: str
    context: Optional[Dict[str, Any]] = None
    agent_type: Optional[str] = None
    priority: int = 1
    timeout_seconds: int = 300
    created_at: datetime = None

    def __init__(self, **data):
        if data.get('id') is None:
            data['id'] = str(uuid.uuid4())
        if data.get('created_at') is None:
            data['created_at'] = datetime.utcnow()
        super().__init__(**data)


class AgentResponse(BaseModel):
    """Agent execution response"""
    task_id: str
    agent_id: str
    status: TaskStatus
    content: str
    citations: List[str] = []
    artifacts: List[Dict[str, Any]] = []
    metadata: Optional[Dict[str, Any]] = None
    execution_time_seconds: Optional[float] = None
    cost_estimate: Optional[float] = None
    error_message: Optional[str] = None


@dataclass
class OrchestratorConfig:
    """Configuration for hierarchical orchestration"""
    num_agents: int = 5
    enable_drummer: bool = True
    enable_camina: bool = True
    parallel_execution: bool = True
    max_concurrent_agents: int = 10
    timeout_seconds: int = 300
    belter_timeout: int = 180
    drummer_timeout: int = 240
    camina_timeout: int = 300
    retry_failed_tasks: bool = True
    max_retries: int = 2


# ============================================================================
# ABSTRACT BASE AGENT
# ============================================================================

class BaseAgent(ABC):
    """
    Abstract base class for all agents in the hierarchical system.

    Provides common functionality for task execution, status tracking,
    and communication with the orchestration layer.
    """

    def __init__(
        self,
        agent_id: str,
        role: AgentRole,
        **config
    ):
        """Initialize base agent with configuration"""
        self.agent_id = agent_id
        self.role = role
        self.config = config
        self.status = TaskStatus.PENDING
        self.current_task = None

    @abstractmethod
    async def execute_task(self, task: AgentTask) -> AgentResponse:
        """Execute a single task and return response"""
        pass

    def _create_response(
        self,
        task: AgentTask,
        content: str,
        status: TaskStatus = TaskStatus.COMPLETED,
        **kwargs
    ) -> AgentResponse:
        """Helper to create standardized agent response"""
        return AgentResponse(
            task_id=task.id,
            agent_id=self.agent_id,
            status=status,
            content=content,
            **kwargs
        )


# ============================================================================
# TIER 1: BELTER AGENTS (WORKERS)
# ============================================================================

class BelterAgent(BaseAgent):
    """
    Individual task execution agent (Tier 1).

    Belters are the atomic workers that execute specific subtasks with
    potential specializations for different domains.
    """

    def __init__(
        self,
        agent_id: str,
        specialization: Optional[str] = None,
        **config
    ):
        """Initialize Belter with optional specialization"""
        super().__init__(agent_id, AgentRole.BELTER, **config)
        self.specialization = specialization or "general"

    async def execute_task(self, task: AgentTask) -> AgentResponse:
        """Execute individual task with specialized processing"""
        self.current_task = task
        self.status = TaskStatus.RUNNING
        start_time = time.time()

        try:
            print(f"🎯 Belter {self.agent_id} ({self.specialization}) executing: {task.prompt}")

            # Simulate work (in real implementation, this would call an LLM)
            await asyncio.sleep(1)  # Placeholder for actual LLM call

            response_content = f"Belter {self.agent_id} completed task: {task.prompt}"
            citations = []  # Would extract from LLM response
            artifacts = []

            execution_time = time.time() - start_time
            self.status = TaskStatus.COMPLETED

            return self._create_response(
                task=task,
                content=response_content,
                status=TaskStatus.COMPLETED,
                citations=citations,
                artifacts=artifacts,
                execution_time_seconds=execution_time,
                metadata={
                    "specialization": self.specialization,
                    "tier": "belter"
                }
            )

        except Exception as e:
            execution_time = time.time() - start_time
            self.status = TaskStatus.FAILED

            return self._create_response(
                task=task,
                content="",
                status=TaskStatus.FAILED,
                execution_time_seconds=execution_time,
                error_message=str(e)
            )
        finally:
            self.current_task = None


# ============================================================================
# TIER 2: DRUMMER AGENTS (SYNTHESIZERS)
# ============================================================================

class DrummerAgent(BaseAgent):
    """
    Synthesis agent that aggregates multiple Belter responses (Tier 2).

    Drummers take output from 5 Belter agents and create coherent,
    synthesized reports that combine their insights.
    """

    def __init__(self, agent_id: str, **config):
        """Initialize Drummer agent"""
        super().__init__(agent_id, AgentRole.DRUMMER, **config)

    async def synthesize_belter_results(
        self,
        belter_responses: List[AgentResponse],
        original_query: Optional[str] = None
    ) -> AgentResponse:
        """Synthesize multiple Belter agent results"""
        task = AgentTask(
            prompt=original_query or "Synthesize research findings",
            context={
                "belter_responses": belter_responses,
                "original_query": original_query,
                "task_type": "synthesis"
            }
        )

        return await self.execute_task(task)

    async def execute_task(self, task: AgentTask) -> AgentResponse:
        """Execute synthesis task using multiple Belter responses"""
        self.current_task = task
        self.status = TaskStatus.RUNNING
        start_time = time.time()

        try:
            belter_responses = task.context.get('belter_responses', []) if task.context else []

            if not belter_responses:
                raise ValueError("No Belter responses provided for synthesis")

            print(f"🥁 Drummer {self.agent_id} synthesizing {len(belter_responses)} Belter responses")

            # Simulate synthesis (in real implementation, this would call an LLM)
            await asyncio.sleep(1.5)

            # Aggregate citations
            all_citations = []
            for response in belter_responses:
                if response.status == TaskStatus.COMPLETED:
                    all_citations.extend(response.citations)
            unique_citations = list(set(all_citations))

            synthesis_content = f"Drummer synthesis of {len(belter_responses)} Belter responses"

            execution_time = time.time() - start_time
            self.status = TaskStatus.COMPLETED

            return self._create_response(
                task=task,
                content=synthesis_content,
                status=TaskStatus.COMPLETED,
                citations=unique_citations,
                execution_time_seconds=execution_time,
                metadata={
                    "belter_count": len(belter_responses),
                    "synthesis_type": "drummer",
                    "tier": "drummer"
                }
            )

        except Exception as e:
            execution_time = time.time() - start_time
            self.status = TaskStatus.FAILED

            return self._create_response(
                task=task,
                content="",
                status=TaskStatus.FAILED,
                execution_time_seconds=execution_time,
                error_message=str(e)
            )
        finally:
            self.current_task = None


# ============================================================================
# TIER 3: CAMINA AGENT (EXECUTIVE)
# ============================================================================

class CaminaAgent(BaseAgent):
    """
    Final synthesis agent for large multi-agent operations (Tier 3).

    Camina provides executive-level synthesis when dealing with large
    swarms (2+ Drummers). Creates comprehensive strategic reports.
    """

    def __init__(self, agent_id: str, **config):
        """Initialize Camina agent"""
        super().__init__(agent_id, AgentRole.CAMINA, **config)

    async def final_synthesis(
        self,
        belter_responses: List[AgentResponse],
        drummer_responses: List[AgentResponse],
        original_query: Optional[str] = None
    ) -> AgentResponse:
        """Perform final synthesis of all agent outputs"""
        task = AgentTask(
            prompt=original_query or "Create executive-level synthesis",
            context={
                "drummer_responses": drummer_responses,
                "total_belter_count": len(belter_responses),
                "original_query": original_query,
                "task_type": "executive_synthesis"
            }
        )

        return await self.execute_task(task)

    async def execute_task(self, task: AgentTask) -> AgentResponse:
        """Execute final synthesis using multiple Drummer responses"""
        self.current_task = task
        self.status = TaskStatus.RUNNING
        start_time = time.time()

        try:
            drummer_responses = task.context.get('drummer_responses', []) if task.context else []
            belter_count = task.context.get('total_belter_count', 0) if task.context else 0

            if not drummer_responses:
                raise ValueError("No Drummer responses provided for final synthesis")

            print(f"👑 Camina {self.agent_id} creating executive synthesis from {len(drummer_responses)} Drummers")

            # Simulate executive synthesis (in real implementation, this would call an LLM)
            await asyncio.sleep(2)

            # Aggregate all citations
            all_citations = []
            for response in drummer_responses:
                if response.status == TaskStatus.COMPLETED:
                    all_citations.extend(response.citations)
            unique_citations = list(set(all_citations))

            executive_content = f"Executive synthesis: {len(drummer_responses)} Drummer units, {belter_count} total Belters"

            execution_time = time.time() - start_time
            self.status = TaskStatus.COMPLETED

            return self._create_response(
                task=task,
                content=executive_content,
                status=TaskStatus.COMPLETED,
                citations=unique_citations,
                execution_time_seconds=execution_time,
                metadata={
                    "drummer_count": len(drummer_responses),
                    "total_belter_count": belter_count,
                    "synthesis_type": "camina_executive",
                    "tier": "camina"
                }
            )

        except Exception as e:
            execution_time = time.time() - start_time
            self.status = TaskStatus.FAILED

            return self._create_response(
                task=task,
                content="",
                status=TaskStatus.FAILED,
                execution_time_seconds=execution_time,
                error_message=str(e)
            )
        finally:
            self.current_task = None


# ============================================================================
# HIERARCHICAL ORCHESTRATOR
# ============================================================================

class HierarchicalOrchestrator:
    """
    Main orchestrator for coordinating hierarchical agent swarms.

    Manages task decomposition, parallel agent execution, and hierarchical
    synthesis through Belter → Drummer → Camina tiers.
    """

    def __init__(self, config: Optional[OrchestratorConfig] = None):
        """Initialize orchestrator with configuration"""
        self.config = config or OrchestratorConfig()
        self.agents: Dict[str, BaseAgent] = {}

    async def execute_task(
        self,
        task: str,
        stream_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Execute a task using hierarchical agent swarm.

        Args:
            task: The main task to execute
            stream_callback: Optional callback for streaming updates

        Returns:
            Dictionary with all agent responses and metadata
        """
        start_time = time.time()

        try:
            # Step 1: Create agent swarm
            agents = await self._create_agent_swarm(self.config.num_agents)

            # Step 2: Execute Belters in parallel
            if stream_callback:
                await stream_callback('status', f'Deploying {self.config.num_agents} Belter agents...')

            belter_results = await self._execute_belters_parallel(
                agents['belters'],
                task,
                stream_callback
            )

            # Step 3: Execute Drummers (every 5 Belters)
            drummer_results = []
            if self.config.enable_drummer and len(belter_results) >= 5:
                if stream_callback:
                    await stream_callback('status', 'Initializing Drummer synthesis...')

                drummer_results = await self._execute_drummers_parallel(
                    agents['drummers'],
                    belter_results,
                    task,
                    stream_callback
                )

            # Step 4: Execute Camina (when 2+ Drummers)
            camina_result = None
            if self.config.enable_camina and len(drummer_results) >= 2:
                if stream_callback:
                    await stream_callback('status', 'Launching Camina executive synthesis...')

                camina_result = await agents['camina'].final_synthesis(
                    belter_results,
                    drummer_results,
                    task
                )

            execution_time = time.time() - start_time

            return {
                "task": task,
                "belter_responses": belter_results,
                "drummer_responses": drummer_results,
                "camina_response": camina_result,
                "execution_time": execution_time,
                "total_agents": len(belter_results) + len(drummer_results) + (1 if camina_result else 0)
            }

        except Exception as e:
            print(f"Orchestration failed: {str(e)}")
            raise

    async def _create_agent_swarm(self, num_subtasks: int) -> Dict[str, Any]:
        """Create and initialize all required agents"""
        agents = {
            'belters': [],
            'drummers': [],
            'camina': None
        }

        # Create Belter agents with specializations
        specializations = ['research', 'analysis', 'coding', 'financial', 'general']

        for i in range(num_subtasks):
            specialization = specializations[i % len(specializations)]
            agent = BelterAgent(
                agent_id=f"belter_{i+1}",
                specialization=specialization
            )
            agents['belters'].append(agent)
            self.agents[agent.agent_id] = agent

        # Create Drummer agents (1 per 5 Belters)
        if self.config.enable_drummer:
            num_drummers = (num_subtasks + 4) // 5
            for i in range(num_drummers):
                agent = DrummerAgent(agent_id=f"drummer_{i+1}")
                agents['drummers'].append(agent)
                self.agents[agent.agent_id] = agent

        # Create Camina agent if needed (when 2+ drummers)
        num_drummers = (num_subtasks + 4) // 5 if self.config.enable_drummer else 0
        if self.config.enable_camina and num_drummers >= 2:
            agent = CaminaAgent(agent_id="camina_1")
            agents['camina'] = agent
            self.agents[agent.agent_id] = agent

        return agents

    async def _execute_belters_parallel(
        self,
        belters: List[BelterAgent],
        task: str,
        stream_callback: Optional[Callable]
    ) -> List[AgentResponse]:
        """Execute Belter agents in parallel with rate limiting"""
        semaphore = asyncio.Semaphore(self.config.max_concurrent_agents)

        async def execute_with_limit(agent: BelterAgent, idx: int):
            async with semaphore:
                agent_task = AgentTask(
                    prompt=f"Subtask {idx+1}: {task}",
                    timeout_seconds=self.config.belter_timeout
                )

                try:
                    response = await asyncio.wait_for(
                        agent.execute_task(agent_task),
                        timeout=self.config.belter_timeout
                    )
                    return response
                except asyncio.TimeoutError:
                    return agent._create_response(
                        agent_task,
                        "",
                        status=TaskStatus.FAILED,
                        error_message=f"Timeout after {self.config.belter_timeout}s"
                    )

        # Execute all Belters in parallel
        tasks = [execute_with_limit(agent, idx) for idx, agent in enumerate(belters)]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        processed_results = []
        for result in results:
            if isinstance(result, Exception):
                print(f"Belter failed: {result}")
            else:
                processed_results.append(result)

        return processed_results

    async def _execute_drummers_parallel(
        self,
        drummers: List[DrummerAgent],
        belter_results: List[AgentResponse],
        original_task: str,
        stream_callback: Optional[Callable]
    ) -> List[AgentResponse]:
        """Execute Drummer agents in parallel to synthesize Belter results"""
        # Group Belter results by 5
        belter_groups = [
            belter_results[i:i+5]
            for i in range(0, len(belter_results), 5)
        ]

        async def execute_drummer(drummer: DrummerAgent, belter_group: List[AgentResponse]):
            return await drummer.synthesize_belter_results(belter_group, original_task)

        # Execute all Drummers in parallel
        tasks = [
            execute_drummer(drummer, group)
            for drummer, group in zip(drummers, belter_groups) if group
        ]

        return await asyncio.gather(*tasks) if tasks else []


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    async def main():
        """Example usage of hierarchical agent coordination"""

        # Create orchestrator with configuration
        config = OrchestratorConfig(
            num_agents=12,  # Will create 12 Belters, 3 Drummers, 1 Camina
            enable_drummer=True,
            enable_camina=True,
            max_concurrent_agents=5,
            belter_timeout=60,
            drummer_timeout=90,
            camina_timeout=120
        )

        orchestrator = HierarchicalOrchestrator(config)

        # Define callback for streaming updates
        async def progress_callback(event_type: str, data: Any):
            print(f"[{event_type}] {data}")

        # Execute task with hierarchical coordination
        result = await orchestrator.execute_task(
            task="Analyze the impact of artificial intelligence on healthcare",
            stream_callback=progress_callback
        )

        # Display results
        print(f"\n{'='*60}")
        print(f"Task: {result['task']}")
        print(f"Total Execution Time: {result['execution_time']:.2f}s")
        print(f"Total Agents: {result['total_agents']}")
        print(f"\nBelter Responses: {len(result['belter_responses'])}")
        print(f"Drummer Syntheses: {len(result['drummer_responses'])}")
        print(f"Camina Executive: {'Yes' if result['camina_response'] else 'No'}")

        # Show hierarchy
        print(f"\n{'='*60}")
        print("HIERARCHICAL STRUCTURE:")
        print(f"Tier 1 (Belters): {len(result['belter_responses'])} agents")
        print(f"Tier 2 (Drummers): {len(result['drummer_responses'])} agents")
        print(f"Tier 3 (Camina): {1 if result['camina_response'] else 0} agent")

        if result['camina_response']:
            print(f"\nFinal Executive Synthesis:")
            print(f"  Status: {result['camina_response'].status}")
            print(f"  Content: {result['camina_response'].content}")
            print(f"  Citations: {len(result['camina_response'].citations)}")

    # Run the example
    asyncio.run(main())

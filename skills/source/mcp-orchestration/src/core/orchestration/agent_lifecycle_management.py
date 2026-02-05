"""
Agent Lifecycle Management Pattern

Description: Comprehensive pattern for managing agent lifecycle from initialization through
execution to cleanup. Includes state tracking, validation, cost estimation, and metadata
management for multi-agent systems.

Use Cases:
- Managing agent pools in orchestration systems
- Tracking agent status and health across distributed systems
- Resource management and cleanup for long-running agents
- Cost tracking and budget management for LLM-based agents
- Debugging and monitoring agent behavior

Dependencies:
- abc (for abstract base classes)
- typing (for type hints)
- enum (for status enums)
- pydantic (for data models)

Notes:
- Agents transition through PENDING → RUNNING → COMPLETED/FAILED states
- Validation ensures agents are properly configured before execution
- Metadata tracking enables debugging and performance analysis
- Cost estimation helps manage API usage and budgets
- Clean separation between agent logic and orchestration concerns

Related Snippets:
- hierarchical_agent_coordination.py - Uses this pattern for agent management
- parallel_agent_execution.py - Tracks agent execution status
- provider_abstraction_pattern.py - Provider layer for agents

Source Attribution:
- Extracted from: /home/coolhand/projects/beltalowda/src/beltalowda/agents/base.py
- Additional context from: orchestrator.py, agents/belter.py
- Original author: Luke Steuber
- Project: Beltalowda Multi-Agent Orchestration Platform
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
from datetime import datetime
import uuid


# ============================================================================
# ENUMS AND STATUS DEFINITIONS
# ============================================================================

class AgentRole(str, Enum):
    """Agent role types in the system"""
    WORKER = "worker"           # Individual task executor
    SYNTHESIZER = "synthesizer" # Aggregates multiple workers
    EXECUTIVE = "executive"     # Final consolidation
    MONITOR = "monitor"         # Validation and verification
    DECOMPOSER = "decomposer"   # Task breakdown


class TaskStatus(str, Enum):
    """Task execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentHealth(str, Enum):
    """Agent health status"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


# ============================================================================
# DATA MODELS
# ============================================================================

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


class AgentMetrics(BaseModel):
    """Performance metrics for an agent"""
    total_tasks: int = 0
    successful_tasks: int = 0
    failed_tasks: int = 0
    total_execution_time: float = 0.0
    total_cost: float = 0.0
    average_execution_time: float = 0.0
    success_rate: float = 0.0


# ============================================================================
# ABSTRACT BASE AGENT
# ============================================================================

class BaseAgent(ABC):
    """
    Abstract base class for all agents in the system.

    Provides common functionality for task execution, status tracking,
    lifecycle management, and communication with the orchestration layer.
    """

    def __init__(
        self,
        agent_id: str,
        role: AgentRole,
        provider_adapter: Optional[Any] = None,
        model: Optional[str] = None,
        **config
    ):
        """
        Initialize base agent with configuration.

        Args:
            agent_id: Unique identifier for this agent
            role: Role type from AgentRole enum
            provider_adapter: LLM provider adapter instance
            model: Model name to use
            **config: Additional configuration parameters
        """
        self.agent_id = agent_id
        self.role = role
        self.provider = provider_adapter
        self.model = model
        self.config = config

        # Lifecycle state
        self.status = TaskStatus.PENDING
        self.health = AgentHealth.UNKNOWN
        self.current_task: Optional[AgentTask] = None
        self.created_at = datetime.utcnow()

        # Metrics tracking
        self.metrics = AgentMetrics()
        self.task_history: List[AgentResponse] = []

    @abstractmethod
    async def execute_task(self, task: AgentTask) -> AgentResponse:
        """
        Execute a single task and return response.

        This method must be implemented by all agent subclasses.

        Args:
            task: The task to execute

        Returns:
            AgentResponse with execution results
        """
        pass

    async def initialize(self) -> bool:
        """
        Initialize agent and validate configuration.

        Returns:
            True if initialization successful, False otherwise
        """
        try:
            # Validate provider if present
            if self.provider:
                is_valid = await self.validate_setup()
                if not is_valid:
                    self.health = AgentHealth.UNHEALTHY
                    return False

            self.health = AgentHealth.HEALTHY
            return True

        except Exception as e:
            print(f"Agent {self.agent_id} initialization failed: {e}")
            self.health = AgentHealth.UNHEALTHY
            return False

    async def validate_setup(self) -> bool:
        """
        Validate agent configuration and provider connectivity.

        Returns:
            True if setup is valid, False otherwise
        """
        try:
            if self.provider:
                return await self.provider.validate_api_key()
            return True
        except Exception:
            return False

    def get_agent_info(self) -> Dict[str, Any]:
        """
        Get comprehensive agent metadata and status.

        Returns:
            Dictionary with agent information
        """
        return {
            "agent_id": self.agent_id,
            "role": self.role.value,
            "model": self.model,
            "provider": self.provider.get_provider_name() if self.provider else None,
            "status": self.status.value,
            "health": self.health.value,
            "current_task": self.current_task.id if self.current_task else None,
            "created_at": self.created_at.isoformat(),
            "config": self.config,
            "metrics": self.metrics.dict()
        }

    async def estimate_task_cost(self, task: AgentTask) -> float:
        """
        Estimate cost for executing a task.

        Args:
            task: The task to estimate

        Returns:
            Estimated cost in USD
        """
        if not self.provider:
            return 0.0

        try:
            # Create mock messages for cost estimation
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": task.prompt}
            ]

            return await self.provider.estimate_cost(
                messages=messages,
                model=self.model,
                max_tokens=self.config.get('max_tokens', 2048)
            )
        except Exception:
            return 0.0

    def _create_response(
        self,
        task: AgentTask,
        content: str,
        status: TaskStatus = TaskStatus.COMPLETED,
        **kwargs
    ) -> AgentResponse:
        """
        Helper to create standardized agent response.

        Args:
            task: The task that was executed
            content: Response content
            status: Execution status
            **kwargs: Additional response fields

        Returns:
            AgentResponse object
        """
        return AgentResponse(
            task_id=task.id,
            agent_id=self.agent_id,
            status=status,
            content=content,
            **kwargs
        )

    def _update_metrics(self, response: AgentResponse):
        """
        Update agent metrics after task execution.

        Args:
            response: The task response to record
        """
        self.metrics.total_tasks += 1

        if response.status == TaskStatus.COMPLETED:
            self.metrics.successful_tasks += 1
        elif response.status == TaskStatus.FAILED:
            self.metrics.failed_tasks += 1

        if response.execution_time_seconds:
            self.metrics.total_execution_time += response.execution_time_seconds

        if response.cost_estimate:
            self.metrics.total_cost += response.cost_estimate

        # Calculate derived metrics
        if self.metrics.total_tasks > 0:
            self.metrics.average_execution_time = (
                self.metrics.total_execution_time / self.metrics.total_tasks
            )
            self.metrics.success_rate = (
                self.metrics.successful_tasks / self.metrics.total_tasks
            )

        # Add to history (limit to last 100 tasks)
        self.task_history.append(response)
        if len(self.task_history) > 100:
            self.task_history.pop(0)

    async def shutdown(self):
        """
        Gracefully shutdown agent and cleanup resources.
        """
        # Cancel current task if running
        if self.current_task:
            self.status = TaskStatus.CANCELLED

        # Cleanup provider resources if needed
        if self.provider and hasattr(self.provider, 'close'):
            await self.provider.close()

        self.health = AgentHealth.UNHEALTHY


# ============================================================================
# AGENT POOL MANAGER
# ============================================================================

class AgentPoolManager:
    """
    Manages a pool of agents with lifecycle tracking.

    Provides centralized management for creating, monitoring, and
    cleaning up agent instances.
    """

    def __init__(self):
        """Initialize agent pool manager"""
        self.agents: Dict[str, BaseAgent] = {}
        self.agent_groups: Dict[str, List[str]] = {}

    def register_agent(self, agent: BaseAgent, group: Optional[str] = None):
        """
        Register an agent with the pool.

        Args:
            agent: Agent instance to register
            group: Optional group name for organization
        """
        self.agents[agent.agent_id] = agent

        if group:
            if group not in self.agent_groups:
                self.agent_groups[group] = []
            self.agent_groups[group].append(agent.agent_id)

    def unregister_agent(self, agent_id: str):
        """
        Unregister an agent from the pool.

        Args:
            agent_id: ID of agent to unregister
        """
        if agent_id in self.agents:
            # Remove from groups
            for group_agents in self.agent_groups.values():
                if agent_id in group_agents:
                    group_agents.remove(agent_id)

            # Remove from agents dict
            del self.agents[agent_id]

    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        """
        Get agent by ID.

        Args:
            agent_id: Agent identifier

        Returns:
            Agent instance or None if not found
        """
        return self.agents.get(agent_id)

    def get_agents_by_group(self, group: str) -> List[BaseAgent]:
        """
        Get all agents in a group.

        Args:
            group: Group name

        Returns:
            List of agent instances
        """
        agent_ids = self.agent_groups.get(group, [])
        return [self.agents[aid] for aid in agent_ids if aid in self.agents]

    def get_agents_by_role(self, role: AgentRole) -> List[BaseAgent]:
        """
        Get all agents with a specific role.

        Args:
            role: Agent role to filter by

        Returns:
            List of matching agent instances
        """
        return [agent for agent in self.agents.values() if agent.role == role]

    def get_agents_by_status(self, status: TaskStatus) -> List[BaseAgent]:
        """
        Get all agents with a specific status.

        Args:
            status: Task status to filter by

        Returns:
            List of matching agent instances
        """
        return [agent for agent in self.agents.values() if agent.status == status]

    def get_healthy_agents(self) -> List[BaseAgent]:
        """
        Get all healthy agents.

        Returns:
            List of healthy agent instances
        """
        return [
            agent for agent in self.agents.values()
            if agent.health == AgentHealth.HEALTHY
        ]

    def get_pool_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive pool statistics.

        Returns:
            Dictionary with pool metrics
        """
        total_agents = len(self.agents)
        if total_agents == 0:
            return {"total_agents": 0}

        # Aggregate metrics
        total_tasks = sum(agent.metrics.total_tasks for agent in self.agents.values())
        total_successful = sum(agent.metrics.successful_tasks for agent in self.agents.values())
        total_failed = sum(agent.metrics.failed_tasks for agent in self.agents.values())
        total_cost = sum(agent.metrics.total_cost for agent in self.agents.values())

        # Status distribution
        status_distribution = {}
        for status in TaskStatus:
            count = len(self.get_agents_by_status(status))
            if count > 0:
                status_distribution[status.value] = count

        # Health distribution
        health_distribution = {}
        for health in AgentHealth:
            count = len([a for a in self.agents.values() if a.health == health])
            if count > 0:
                health_distribution[health.value] = count

        return {
            "total_agents": total_agents,
            "total_tasks_executed": total_tasks,
            "total_successful": total_successful,
            "total_failed": total_failed,
            "total_cost": round(total_cost, 4),
            "average_success_rate": round(total_successful / total_tasks, 3) if total_tasks > 0 else 0,
            "status_distribution": status_distribution,
            "health_distribution": health_distribution,
            "groups": {name: len(agents) for name, agents in self.agent_groups.items()}
        }

    async def shutdown_all(self):
        """Shutdown all agents in the pool"""
        for agent in self.agents.values():
            await agent.shutdown()


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    import asyncio

    # Example agent implementation
    class ExampleAgent(BaseAgent):
        """Example agent for demonstration"""

        async def execute_task(self, task: AgentTask) -> AgentResponse:
            """Execute task with lifecycle tracking"""
            self.current_task = task
            self.status = TaskStatus.RUNNING

            import time
            start_time = time.time()

            try:
                # Simulate work
                await asyncio.sleep(0.5)

                response = self._create_response(
                    task=task,
                    content=f"Agent {self.agent_id} completed: {task.prompt}",
                    status=TaskStatus.COMPLETED,
                    execution_time_seconds=time.time() - start_time,
                    cost_estimate=0.001
                )

                self.status = TaskStatus.COMPLETED
                self._update_metrics(response)

                return response

            except Exception as e:
                response = self._create_response(
                    task=task,
                    content="",
                    status=TaskStatus.FAILED,
                    execution_time_seconds=time.time() - start_time,
                    error_message=str(e)
                )

                self.status = TaskStatus.FAILED
                self._update_metrics(response)

                return response

            finally:
                self.current_task = None

    async def main():
        """Demonstrate agent lifecycle management"""
        print("Agent Lifecycle Management Demo")
        print("=" * 60)

        # Create agent pool manager
        pool = AgentPoolManager()

        # Create and register agents
        for i in range(5):
            agent = ExampleAgent(
                agent_id=f"worker_{i}",
                role=AgentRole.WORKER
            )
            await agent.initialize()
            pool.register_agent(agent, group="workers")

        # Execute some tasks
        tasks = [
            AgentTask(prompt=f"Task {i}")
            for i in range(10)
        ]

        print(f"\nExecuting {len(tasks)} tasks across {len(pool.agents)} agents...\n")

        for i, task in enumerate(tasks):
            agent_id = f"worker_{i % 5}"
            agent = pool.get_agent(agent_id)

            if agent:
                response = await agent.execute_task(task)
                print(f"  {agent_id}: {response.status.value}")

        # Display statistics
        print(f"\n{'='*60}")
        print("Pool Statistics:")
        stats = pool.get_pool_statistics()
        for key, value in stats.items():
            print(f"  {key}: {value}")

        # Display individual agent info
        print(f"\n{'='*60}")
        print("Agent Details:")
        for agent in pool.agents.values():
            info = agent.get_agent_info()
            print(f"\n  {info['agent_id']}:")
            print(f"    Role: {info['role']}")
            print(f"    Status: {info['status']}")
            print(f"    Health: {info['health']}")
            print(f"    Tasks: {info['metrics']['total_tasks']}")
            print(f"    Success Rate: {info['metrics']['success_rate']:.1%}")
            print(f"    Avg Time: {info['metrics']['average_execution_time']:.2f}s")

        # Shutdown
        print(f"\n{'='*60}")
        print("Shutting down all agents...")
        await pool.shutdown_all()

    asyncio.run(main())

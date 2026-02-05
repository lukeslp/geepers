"""
Multi-Agent Orchestration Data Models

Description: Structured data classes for multi-agent workflows. Provides type-safe
containers for tasks, agent results, synthesis operations, and streaming events.
Based on Beltalowda and Swarm orchestration patterns.

Use Cases:
- Multi-agent research workflows (Beltalowda pattern)
- Specialized agent swarms (Swarm pattern)
- Hierarchical task decomposition systems
- Real-time orchestration dashboards
- Cost tracking across agent executions
- Citation and provenance tracking

Dependencies:
- dataclasses (Python 3.7+)
- typing hints
- datetime for timestamps
- enum for status types

Notes:
- Immutable by default (use replace() or to_dict()/from_dict() for updates)
- JSON-serializable via to_dict() methods
- Supports dependency tracking between subtasks
- Extensible metadata fields for custom orchestrators
- Built-in progress tracking for streaming UIs

Related Snippets:
- /agent-orchestration/beltalowda_hierarchical_orchestrator.py
- /agent-orchestration/swarm_specialized_orchestrator.py
- /streaming-patterns/sse_event_stream.py
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    """Status of a task or workflow."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentType(Enum):
    """Types of agents in orchestrator patterns."""
    WORKER = "worker"              # Parallel execution agents (Belters)
    SYNTHESIZER = "synthesizer"    # Mid-level synthesis (Drummers)
    EXECUTIVE = "executive"        # Final synthesis (Camina)
    MONITOR = "monitor"            # Verification/monitoring (Citation Monitor)
    SPECIALIZED = "specialized"    # Domain-specific agents (Swarm)


@dataclass
class SubTask:
    """
    A single subtask within a larger workflow.

    Attributes:
        id: Unique subtask identifier
        description: Task description
        context: Additional context for execution
        agent_type: Type of agent to handle this task
        specialization: Optional specialization (research, analysis, etc.)
        priority: Task priority (higher = more important)
        dependencies: List of subtask IDs that must complete first
        metadata: Additional metadata
    """
    id: str
    description: str
    context: Dict[str, Any] = field(default_factory=dict)
    agent_type: AgentType = AgentType.WORKER
    specialization: Optional[str] = None
    priority: int = 0
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "description": self.description,
            "context": self.context,
            "agent_type": self.agent_type.value,
            "specialization": self.specialization,
            "priority": self.priority,
            "dependencies": self.dependencies,
            "metadata": self.metadata
        }


@dataclass
class AgentResult:
    """
    Result from a single agent execution.

    Attributes:
        agent_id: Unique agent identifier
        agent_type: Type of agent
        subtask_id: ID of subtask this agent executed
        content: Main result content
        status: Execution status
        execution_time: Time taken (seconds)
        cost: API cost (if applicable)
        metadata: Additional result metadata
        error: Error message if failed
        citations: List of citations/sources
    """
    agent_id: str
    agent_type: AgentType
    subtask_id: str
    content: str
    status: TaskStatus = TaskStatus.COMPLETED
    execution_time: float = 0.0
    cost: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    citations: List[Dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type.value,
            "subtask_id": self.subtask_id,
            "content": self.content,
            "status": self.status.value,
            "execution_time": self.execution_time,
            "cost": self.cost,
            "metadata": self.metadata,
            "error": self.error,
            "citations": self.citations
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentResult":
        """Create AgentResult from dictionary data."""
        if data is None:
            raise ValueError("AgentResult.from_dict requires data")

        agent_type_value = data.get("agent_type", AgentType.WORKER.value)
        if isinstance(agent_type_value, AgentType):
            agent_type_enum = agent_type_value
        else:
            try:
                agent_type_enum = AgentType(agent_type_value)
            except ValueError:
                agent_type_enum = AgentType.WORKER

        status_value = data.get("status", TaskStatus.COMPLETED.value)
        if isinstance(status_value, TaskStatus):
            status_enum = status_value
        else:
            try:
                status_enum = TaskStatus(status_value)
            except ValueError:
                status_enum = TaskStatus.COMPLETED

        return cls(
            agent_id=data.get("agent_id", ""),
            agent_type=agent_type_enum,
            subtask_id=data.get("subtask_id", ""),
            content=data.get("content", ""),
            status=status_enum,
            execution_time=float(data.get("execution_time", 0.0)),
            cost=float(data.get("cost", 0.0)),
            metadata=data.get("metadata", {}) or {},
            error=data.get("error"),
            citations=data.get("citations", []) or []
        )


@dataclass
class SynthesisResult:
    """
    Result from a synthesis operation.

    Attributes:
        synthesis_id: Unique synthesis identifier
        synthesis_level: Level of synthesis (mid-level, executive, etc.)
        content: Synthesized content
        source_agent_ids: IDs of agents whose results were synthesized
        execution_time: Time taken
        cost: API cost
        metadata: Additional metadata
    """
    synthesis_id: str
    synthesis_level: str
    content: str
    source_agent_ids: List[str]
    execution_time: float = 0.0
    cost: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "synthesis_id": self.synthesis_id,
            "synthesis_level": self.synthesis_level,
            "content": self.content,
            "source_agent_ids": self.source_agent_ids,
            "execution_time": self.execution_time,
            "cost": self.cost,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SynthesisResult":
        """Create SynthesisResult from dictionary data."""
        if data is None:
            raise ValueError("SynthesisResult.from_dict requires data")

        return cls(
            synthesis_id=data.get("synthesis_id", ""),
            synthesis_level=data.get("synthesis_level", ""),
            content=data.get("content", ""),
            source_agent_ids=data.get("source_agent_ids", []) or [],
            execution_time=float(data.get("execution_time", 0.0)),
            cost=float(data.get("cost", 0.0)),
            metadata=data.get("metadata", {}) or {}
        )


@dataclass
class OrchestratorResult:
    """
    Complete result from an orchestrator workflow.

    Attributes:
        task_id: Unique workflow task identifier
        title: Workflow title
        status: Overall workflow status
        agent_results: List of all agent results
        synthesis_results: List of synthesis results
        final_synthesis: Final synthesized content
        execution_time: Total execution time
        total_cost: Total API cost
        metadata: Workflow metadata
        generated_documents: List of generated document files
        artifacts: List of artifact files
        error: Error message if workflow failed
        completed_at: ISO timestamp of completion
    """
    task_id: str
    title: str
    status: TaskStatus
    agent_results: List[AgentResult] = field(default_factory=list)
    synthesis_results: List[SynthesisResult] = field(default_factory=list)
    final_synthesis: Optional[str] = None
    execution_time: float = 0.0
    total_cost: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    generated_documents: List[Dict[str, Any]] = field(default_factory=list)
    artifacts: List[str] = field(default_factory=list)
    error: Optional[str] = None
    completed_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "status": self.status.value,
            "agent_results": [r.to_dict() for r in self.agent_results],
            "synthesis_results": [s.to_dict() for s in self.synthesis_results],
            "final_synthesis": self.final_synthesis,
            "execution_time": self.execution_time,
            "total_cost": self.total_cost,
            "metadata": self.metadata,
            "generated_documents": self.generated_documents,
            "artifacts": self.artifacts,
            "error": self.error,
            "completed_at": self.completed_at
        }

    def get_content_sections(self) -> List[Dict[str, Any]]:
        """
        Get content sections for document generation.

        Returns list of sections suitable for document generators.

        Example:
            result = OrchestratorResult(...)
            sections = result.get_content_sections()
            for section in sections:
                print(f"{section['title']}: {section['content'][:100]}...")
        """
        sections = []

        # Add agent results as sections
        for result in self.agent_results:
            sections.append({
                "title": f"{result.agent_type.value.title()}: {result.agent_id}",
                "content": result.content,
                "type": result.agent_type.value
            })

        # Add synthesis results
        for synthesis in self.synthesis_results:
            sections.append({
                "title": f"{synthesis.synthesis_level.title()} Synthesis",
                "content": synthesis.content,
                "type": "synthesis"
            })

        # Add final synthesis
        if self.final_synthesis:
            sections.append({
                "title": "Final Synthesis",
                "content": self.final_synthesis,
                "type": "final"
            })

        return sections

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OrchestratorResult":
        """Create OrchestratorResult from dictionary data."""
        if data is None:
            raise ValueError("OrchestratorResult.from_dict requires data")

        status_value = data.get("status", TaskStatus.COMPLETED.value)
        if isinstance(status_value, TaskStatus):
            status_enum = status_value
        else:
            try:
                status_enum = TaskStatus(status_value)
            except ValueError:
                status_enum = TaskStatus.COMPLETED

        agent_results = [
            AgentResult.from_dict(item)
            for item in data.get("agent_results", []) or []
        ]
        synthesis_results = [
            SynthesisResult.from_dict(item)
            for item in data.get("synthesis_results", []) or []
        ]

        return cls(
            task_id=data.get("task_id", ""),
            title=data.get("title", ""),
            status=status_enum,
            agent_results=agent_results,
            synthesis_results=synthesis_results,
            final_synthesis=data.get("final_synthesis"),
            execution_time=float(data.get("execution_time", 0.0)),
            total_cost=float(data.get("total_cost", 0.0)),
            metadata=data.get("metadata", {}) or {},
            generated_documents=data.get("generated_documents", []) or [],
            artifacts=data.get("artifacts", []) or [],
            error=data.get("error"),
            completed_at=data.get("completed_at")
        )


@dataclass
class StreamEvent:
    """
    Streaming event for real-time progress updates.

    Attributes:
        event_type: Type of event (see EventType constants)
        task_id: Workflow task ID
        timestamp: Event timestamp
        data: Event data
        agent_id: Optional agent ID for agent-specific events
        progress: Optional progress percentage (0-100)
    """
    event_type: str
    task_id: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    data: Dict[str, Any] = field(default_factory=dict)
    agent_id: Optional[str] = None
    progress: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "event_type": self.event_type,
            "task_id": self.task_id,
            "timestamp": self.timestamp.isoformat(),
            "data": self.data,
            "agent_id": self.agent_id,
            "progress": self.progress
        }

    def to_json_string(self) -> str:
        """Convert to JSON string for SSE."""
        import json
        return json.dumps(self.to_dict())


class EventType:
    """Standard event types for streaming."""
    WORKFLOW_START = "workflow_start"
    DECOMPOSITION_START = "decomposition_start"
    DECOMPOSITION_COMPLETE = "decomposition_complete"
    ITERATION_START = "iteration_start"
    ITERATION_COMPLETE = "iteration_complete"
    AGENT_START = "agent_start"
    AGENT_PROGRESS = "agent_progress"
    AGENT_COMPLETE = "agent_complete"
    AGENT_ERROR = "agent_error"
    SYNTHESIS_START = "synthesis_start"
    SYNTHESIS_COMPLETE = "synthesis_complete"
    DOCUMENT_GENERATION_START = "document_generation_start"
    DOCUMENT_GENERATION_COMPLETE = "document_generation_complete"
    WORKFLOW_COMPLETE = "workflow_complete"
    WORKFLOW_ERROR = "workflow_error"
    WORKFLOW_CANCELLED = "workflow_cancelled"


if __name__ == "__main__":
    # Usage examples
    import json

    # Example 1: Create subtasks
    tasks = [
        SubTask(
            id="task-1",
            description="Research quantum computing basics",
            agent_type=AgentType.WORKER,
            priority=1
        ),
        SubTask(
            id="task-2",
            description="Analyze quantum algorithms",
            agent_type=AgentType.WORKER,
            priority=2,
            dependencies=["task-1"]
        )
    ]

    # Example 2: Create agent result
    result = AgentResult(
        agent_id="belter-1",
        agent_type=AgentType.WORKER,
        subtask_id="task-1",
        content="Quantum computing is...",
        execution_time=5.2,
        cost=0.003,
        citations=[
            {"title": "Quantum Computing 101", "url": "https://..."}
        ]
    )

    # Example 3: Serialize to JSON
    print("Agent Result JSON:")
    print(json.dumps(result.to_dict(), indent=2))

    # Example 4: Create streaming event
    event = StreamEvent(
        event_type=EventType.AGENT_COMPLETE,
        task_id="workflow-123",
        agent_id="belter-1",
        progress=33.3,
        data={"message": "Completed research task"}
    )
    print("\nStream Event:")
    print(event.to_json_string())

    # Example 5: Complete workflow result
    workflow = OrchestratorResult(
        task_id="workflow-123",
        title="Quantum Computing Research",
        status=TaskStatus.COMPLETED,
        agent_results=[result],
        execution_time=30.5,
        total_cost=0.15,
        completed_at=datetime.utcnow().isoformat()
    )
    print("\nWorkflow sections:")
    for section in workflow.get_content_sections():
        print(f"- {section['title']} ({section['type']})")

# ================================================
# Phased Workflow Orchestrator Pattern
# ================================================
# Language: python
# Tags: orchestration, workflow, phases, agents, async
# Source: geepers-orchestrators/orchestrators/base_geepers.py
# Last Updated: 2025-12-12
# Author: Luke Steuber
# ================================================
# Description:
# Abstract base class for orchestrating multi-phase workflows with
# sequential and parallel execution modes. Supports task tracking,
# phase-level error handling, automatic report generation, and
# structured result serialization.
#
# Differs from hierarchical_agent_coordination.py in that this uses
# explicit workflow phases defined declaratively rather than automatic
# tier-based scaling. Better for deterministic workflows where phase
# order matters.
#
# Use Cases:
# - Multi-step data pipelines with dependencies
# - Code analysis workflows (scan → fix → test → report)
# - Deployment orchestration (validate → build → deploy → verify)
# - Research workflows with defined methodology phases
# - Any workflow where phase ordering is critical
#
# Dependencies:
# - asyncio (built-in)
# - dataclasses (built-in)
# - datetime (built-in)
# - pathlib (built-in)
# - typing (built-in)
# - json (built-in)
# - abc (built-in)
#
# Notes:
# - Phases can run sequentially or in parallel
# - Context flows from phase to phase
# - Failed phases can stop or continue workflow
# - Automatic tracking of duration and artifacts
# - Reports generated to date-organized directories
#
# Related Snippets:
# - /home/coolhand/SNIPPETS/agent-orchestration/hierarchical_agent_coordination.py
# - /home/coolhand/SNIPPETS/agent-orchestration/parallel_agent_execution.py
# - /home/coolhand/SNIPPETS/async-patterns/concurrent_task_execution.py
# ================================================

import asyncio
import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Awaitable, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class WorkflowPhase:
    """Definition of a single workflow phase."""
    name: str
    dispatch_to: str  # Agent or function to execute
    purpose: str = ""
    wait_for_completion: bool = True
    can_run_parallel: bool = False


@dataclass
class PhaseResult:
    """Result from executing a workflow phase."""
    phase_name: str
    agent_name: str
    status: str  # success, partial, failed, skipped
    findings: Dict[str, Any] = field(default_factory=dict)
    artifacts: List[Path] = field(default_factory=list)
    duration_seconds: float = 0.0
    error: Optional[str] = None


@dataclass
class OrchestratorResult:
    """Complete result from orchestrator execution."""
    orchestrator_name: str
    task_id: str
    project: str
    status: str  # success, partial, failed
    phase_results: List[PhaseResult] = field(default_factory=list)
    summary: str = ""
    artifacts: List[Path] = field(default_factory=list)
    started_at: str = ""
    completed_at: str = ""
    total_duration_seconds: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "orchestrator_name": self.orchestrator_name,
            "task_id": self.task_id,
            "project": self.project,
            "status": self.status,
            "phase_results": [
                {
                    "phase_name": pr.phase_name,
                    "agent_name": pr.agent_name,
                    "status": pr.status,
                    "findings": pr.findings,
                    "duration_seconds": pr.duration_seconds,
                    "error": pr.error,
                }
                for pr in self.phase_results
            ],
            "summary": self.summary,
            "artifacts": [str(a) for a in self.artifacts],
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "total_duration_seconds": self.total_duration_seconds,
        }


# Type for agent execution callbacks
AgentExecutor = Callable[[str, Dict[str, Any]], Awaitable[Dict[str, Any]]]


# ============================================================================
# BASE ORCHESTRATOR
# ============================================================================

class BaseWorkflowOrchestrator(ABC):
    """
    Abstract base class for phased workflow orchestrators.

    Subclasses define workflow phases and implement agent execution logic.
    This base class handles:
    - Phase execution (sequential and parallel)
    - Context passing between phases
    - Error handling and status tracking
    - Report generation
    - Task lifecycle management
    """

    def __init__(
        self,
        name: str,
        output_dir: Path,
        agent_executor: Optional[AgentExecutor] = None,
    ):
        """
        Initialize the orchestrator.

        Args:
            name: Orchestrator name for reporting
            output_dir: Base directory for outputs
            agent_executor: Callback to execute individual agents
        """
        self.name = name
        self.output_dir = Path(output_dir)
        self.agent_executor = agent_executor or self._default_agent_executor

        # Active task tracking
        self._active_tasks: Dict[str, OrchestratorResult] = {}

    @abstractmethod
    def get_workflow_phases(self, mode: str = "full") -> List[WorkflowPhase]:
        """
        Return workflow phases for given mode.

        Args:
            mode: Workflow mode (e.g., "quick", "full")

        Returns:
            List of workflow phases to execute
        """
        pass

    async def _default_agent_executor(
        self, agent_name: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Default agent executor that returns a placeholder result.

        Override this or provide custom executor in constructor.
        """
        logger.info(f"Default executor: would invoke {agent_name}")
        return {
            "status": "simulated",
            "message": f"Simulated execution of {agent_name}",
            "context": context,
        }

    async def execute_agent(
        self, agent_name: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a single agent with given context.

        Args:
            agent_name: Name of agent to execute
            context: Context dict with project info, previous results, etc.

        Returns:
            Agent execution result
        """
        start_time = datetime.now()
        try:
            result = await self.agent_executor(agent_name, context)
            result["duration_seconds"] = (datetime.now() - start_time).total_seconds()
            return result
        except Exception as e:
            logger.error(f"Agent {agent_name} failed: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "duration_seconds": (datetime.now() - start_time).total_seconds(),
            }

    async def _execute_phase(
        self, phase: WorkflowPhase, context: Dict[str, Any]
    ) -> PhaseResult:
        """Execute a single workflow phase."""
        start_time = datetime.now()

        try:
            result = await self.execute_agent(phase.dispatch_to, context)
            status = result.get("status", "success")
            if status == "failed":
                status = "failed"
            elif status == "partial":
                status = "partial"
            else:
                status = "success"

            return PhaseResult(
                phase_name=phase.name,
                agent_name=phase.dispatch_to,
                status=status,
                findings=result.get("findings", {}),
                duration_seconds=(datetime.now() - start_time).total_seconds(),
                error=result.get("error"),
            )
        except Exception as e:
            return PhaseResult(
                phase_name=phase.name,
                agent_name=phase.dispatch_to,
                status="failed",
                error=str(e),
                duration_seconds=(datetime.now() - start_time).total_seconds(),
            )

    async def _execute_sequential(
        self, phases: List[WorkflowPhase], context: Dict[str, Any]
    ) -> List[PhaseResult]:
        """Execute phases sequentially, passing results to next phase."""
        results = []
        running_context = context.copy()

        for phase in phases:
            logger.info(f"Executing phase: {phase.name}")
            result = await self._execute_phase(phase, running_context)
            results.append(result)

            # Add this phase's findings to context for next phase
            running_context[f"{phase.name}_result"] = result.findings

            # Stop on failure if wait_for_completion is True
            if result.status == "failed" and phase.wait_for_completion:
                logger.warning(f"Phase {phase.name} failed, stopping sequence")
                break

        return results

    async def _execute_parallel(
        self, phases: List[WorkflowPhase], context: Dict[str, Any]
    ) -> List[PhaseResult]:
        """Execute phases in parallel."""
        logger.info(f"Executing {len(phases)} phases in parallel")
        tasks = [self._execute_phase(phase, context) for phase in phases]
        return await asyncio.gather(*tasks)

    async def run(
        self,
        project: str,
        mode: str = "full",
        agents: Optional[List[str]] = None,
    ) -> OrchestratorResult:
        """
        Execute the orchestrator workflow.

        Args:
            project: Project path or identifier
            mode: Workflow mode ("quick" or "full")
            agents: Optional list of specific agents to run

        Returns:
            OrchestratorResult with all phase results
        """
        task_id = f"{self.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        started_at = datetime.now()

        # Initialize result
        result = OrchestratorResult(
            orchestrator_name=self.name,
            task_id=task_id,
            project=project,
            status="running",
            started_at=started_at.isoformat(),
        )
        self._active_tasks[task_id] = result

        try:
            # Get workflow phases
            all_phases = self.get_workflow_phases(mode)

            # Filter to specific agents if requested
            if agents:
                all_phases = [p for p in all_phases if p.dispatch_to in agents]

            # Separate sequential and parallel phases
            sequential = [p for p in all_phases if not p.can_run_parallel]
            parallel = [p for p in all_phases if p.can_run_parallel]

            # Base context
            context = {
                "project": project,
                "mode": mode,
                "orchestrator": self.name,
                "task_id": task_id,
            }

            # Execute sequential phases first
            if sequential:
                seq_results = await self._execute_sequential(sequential, context)
                result.phase_results.extend(seq_results)

                # Update context with sequential results
                for pr in seq_results:
                    context[f"{pr.agent_name}_result"] = pr.findings

            # Execute parallel phases
            if parallel:
                par_results = await self._execute_parallel(parallel, context)
                result.phase_results.extend(par_results)

            # Determine overall status
            statuses = [pr.status for pr in result.phase_results]
            if all(s == "success" for s in statuses):
                result.status = "success"
            elif any(s == "failed" for s in statuses):
                result.status = "partial" if any(s == "success" for s in statuses) else "failed"
            else:
                result.status = "partial"

            # Generate summary
            result.summary = self._generate_summary(result)

            # Generate artifacts (reports)
            result.artifacts = self._generate_reports(project, result)

        except Exception as e:
            logger.error(f"Orchestrator {self.name} failed: {e}")
            result.status = "failed"
            result.summary = f"Orchestrator failed: {e}"

        finally:
            result.completed_at = datetime.now().isoformat()
            result.total_duration_seconds = (datetime.now() - started_at).total_seconds()

        return result

    def _generate_summary(self, result: OrchestratorResult) -> str:
        """Generate human-readable summary of execution."""
        lines = [
            f"# {self.name} Summary",
            "",
            f"**Project**: {result.project}",
            f"**Status**: {result.status}",
            f"**Duration**: {result.total_duration_seconds:.1f}s",
            "",
            "## Phase Results",
        ]

        for pr in result.phase_results:
            emoji_map = {
                "success": "✓",
                "partial": "⚠",
                "failed": "✗",
                "skipped": "○"
            }
            emoji = emoji_map.get(pr.status, "?")
            lines.append(f"- [{emoji}] {pr.phase_name} ({pr.agent_name}): {pr.status}")
            if pr.error:
                lines.append(f"  - Error: {pr.error}")

        return "\n".join(lines)

    def _generate_reports(self, project: str, result: OrchestratorResult) -> List[Path]:
        """Generate report files for the execution."""
        artifacts = []

        try:
            # Ensure output directories exist
            date_str = datetime.now().strftime('%Y-%m-%d')
            report_dir = self.output_dir / 'reports' / 'by-date' / date_str
            report_dir.mkdir(parents=True, exist_ok=True)

            # Write summary report
            project_name = Path(project).name
            report_path = report_dir / f"{self.name}-{project_name}.md"
            report_path.write_text(result.summary)
            artifacts.append(report_path)

            # Write JSON result
            json_path = report_dir / f"{self.name}-{project_name}.json"
            json_path.write_text(json.dumps(result.to_dict(), indent=2))
            artifacts.append(json_path)

            # Update log
            log_dir = self.output_dir / 'logs'
            log_dir.mkdir(parents=True, exist_ok=True)
            log_path = log_dir / f"{self.name}-{date_str}.log"
            with open(log_path, 'a') as f:
                f.write(f"[{datetime.now().isoformat()}] {result.task_id} status={result.status}\n")
            artifacts.append(log_path)

        except Exception as e:
            logger.error(f"Failed to generate reports: {e}")

        return artifacts

    def get_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a running or completed task."""
        if task_id in self._active_tasks:
            return self._active_tasks[task_id].to_dict()
        return None


# ============================================================================
# EXAMPLE IMPLEMENTATION
# ============================================================================

class CodeAnalysisOrchestrator(BaseWorkflowOrchestrator):
    """Example: Code analysis workflow orchestrator."""

    def __init__(self, output_dir: Path):
        super().__init__(
            name="code_analysis",
            output_dir=output_dir,
        )

    def get_workflow_phases(self, mode: str = "full") -> List[WorkflowPhase]:
        """Define code analysis workflow phases."""
        if mode == "quick":
            return [
                WorkflowPhase(
                    name="Quick Scan",
                    dispatch_to="scanner",
                    purpose="Fast code quality scan",
                ),
            ]

        # Full workflow
        return [
            WorkflowPhase(
                name="Discovery",
                dispatch_to="scout",
                purpose="Scan project structure",
                wait_for_completion=True,
                can_run_parallel=False,
            ),
            WorkflowPhase(
                name="Static Analysis",
                dispatch_to="linter",
                purpose="Run linters and type checkers",
                wait_for_completion=True,
                can_run_parallel=False,
            ),
            WorkflowPhase(
                name="Security Scan",
                dispatch_to="security",
                purpose="Check for vulnerabilities",
                wait_for_completion=False,
                can_run_parallel=True,
            ),
            WorkflowPhase(
                name="Dependency Audit",
                dispatch_to="deps",
                purpose="Audit dependencies",
                wait_for_completion=False,
                can_run_parallel=True,
            ),
            WorkflowPhase(
                name="Report Generation",
                dispatch_to="reporter",
                purpose="Generate final report",
                wait_for_completion=True,
                can_run_parallel=False,
            ),
        ]


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

async def main():
    """Example usage of phased workflow orchestrator."""

    # Create orchestrator
    output_dir = Path("/tmp/workflow_output")
    orchestrator = CodeAnalysisOrchestrator(output_dir)

    # Define custom agent executor
    async def custom_executor(agent_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate agent execution."""
        print(f"  → Executing {agent_name}...")
        await asyncio.sleep(1)  # Simulate work
        return {
            "status": "success",
            "findings": {
                "agent": agent_name,
                "items_found": 5,
            },
        }

    orchestrator.agent_executor = custom_executor

    # Run workflow
    print("Starting workflow...")
    result = await orchestrator.run(
        project="/path/to/project",
        mode="full"
    )

    # Display results
    print("\n" + "=" * 60)
    print(result.summary)
    print("=" * 60)
    print(f"\nArtifacts generated:")
    for artifact in result.artifacts:
        print(f"  - {artifact}")

    print(f"\nJSON output:")
    print(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    asyncio.run(main())

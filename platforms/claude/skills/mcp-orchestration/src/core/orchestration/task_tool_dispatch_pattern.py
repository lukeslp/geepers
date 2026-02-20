# ================================================
# Task Tool Dispatch Pattern
# ================================================
# Language: python
# Tags: claude-code, task-tool, mcp, orchestration, dispatch
# Source: geepers-orchestrators/orchestrators/agent_dispatch.py
# Last Updated: 2025-12-12
# Author: Luke Steuber
# ================================================
# Description:
# Pattern for MCP servers to dispatch work to Claude Code's Task tool.
# Since MCP servers run as separate processes, they can't directly invoke
# Task - instead they return structured instructions that Claude Code can
# execute. This bridges the gap between MCP protocol and Task tool.
#
# Use Cases:
# - MCP servers that need to delegate work to specialized agents
# - Orchestrators coordinating multiple Claude Code subagents
# - Building multi-step workflows where each step is a Task
# - Creating dispatch systems for agent routing
#
# Dependencies:
# - dataclasses (built-in)
# - enum (built-in)
# - typing (built-in)
# - datetime (built-in)
# - pathlib (built-in)
#
# Notes:
# - Returns instructions, not direct execution
# - Claude Code reads the response and calls Task itself
# - Supports sequential and parallel execution plans
# - Includes prompt templates for common agent types
# - Maps agent names to Task subagent_type values
#
# Related Snippets:
# - /home/coolhand/SNIPPETS/tool-registration/mcp_stdio_server_pattern.py
# - /home/coolhand/SNIPPETS/agent-orchestration/phased_workflow_orchestrator.py
# ================================================

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


# ============================================================================
# DISPATCH MODES
# ============================================================================

class DispatchMode(str, Enum):
    """How to dispatch agent execution."""
    INSTRUCTIONS = "instructions"  # Return prompts for Claude Code to execute
    HUB = "hub"                    # Execute via shared/mcp hub (port 5060)
    SIMULATE = "simulate"          # Simulate execution (testing)


# ============================================================================
# AGENT DISPATCH DATA MODEL
# ============================================================================

@dataclass
class AgentDispatch:
    """
    Instructions for dispatching an agent via Claude Code's Task tool.

    This gets returned by the MCP server so Claude Code knows
    exactly how to invoke each agent.
    """
    agent_name: str
    subagent_type: str
    prompt: str
    context: Dict[str, Any] = field(default_factory=dict)
    model: str = "sonnet"
    description: str = ""

    def to_task_call(self) -> Dict[str, Any]:
        """
        Return parameters for Claude Code's Task tool.

        This can be used directly in a Task tool invocation.

        Returns:
            Dict with Task tool parameters
        """
        return {
            "subagent_type": self.subagent_type,
            "prompt": self.prompt,
            "description": self.description or f"Run {self.agent_name}",
            "model": self.model,
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "agent_name": self.agent_name,
            "subagent_type": self.subagent_type,
            "prompt": self.prompt,
            "context": self.context,
            "model": self.model,
            "description": self.description,
            "task_call": self.to_task_call(),
        }


# ============================================================================
# WORKFLOW DISPATCH PLAN
# ============================================================================

@dataclass
class WorkflowDispatch:
    """
    Complete workflow dispatch plan for an orchestrator.

    Contains all agent dispatches organized by phase,
    so Claude Code knows the execution order.
    """
    orchestrator_name: str
    task_id: str
    project: str
    mode: str
    phases: List[Dict[str, Any]] = field(default_factory=list)

    def add_phase(
        self,
        phase_name: str,
        dispatches: List[AgentDispatch],
        parallel: bool = False,
    ):
        """Add a phase with its agent dispatches."""
        self.phases.append({
            "phase_name": phase_name,
            "parallel": parallel,
            "dispatches": [d.to_dict() for d in dispatches],
        })

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "orchestrator_name": self.orchestrator_name,
            "task_id": self.task_id,
            "project": self.project,
            "mode": self.mode,
            "phases": self.phases,
            "execution_instructions": self._get_instructions(),
        }

    def _get_instructions(self) -> str:
        """Generate human-readable execution instructions."""
        lines = [
            f"# {self.orchestrator_name} Workflow",
            f"Project: {self.project}",
            f"Mode: {self.mode}",
            "",
            "Execute the following phases in order:",
            "",
        ]

        for i, phase in enumerate(self.phases, 1):
            phase_name = phase["phase_name"]
            parallel = phase["parallel"]
            dispatches = phase["dispatches"]

            if parallel:
                lines.append(f"## Phase {i}: {phase_name} (PARALLEL)")
                lines.append("Run these agents in parallel:")
            else:
                lines.append(f"## Phase {i}: {phase_name} (SEQUENTIAL)")
                lines.append("Run these agents in sequence:")

            for dispatch in dispatches:
                lines.append(f"  - {dispatch['agent_name']} ({dispatch['subagent_type']})")
            lines.append("")

        return "\n".join(lines)


# ============================================================================
# AGENT NAME MAPPING
# ============================================================================

# Map agent names to Task subagent_type values
AGENT_SUBAGENT_MAP = {
    # Checkpoint agents
    "geepers_scout": "geepers_scout",
    "geepers_repo": "geepers_repo",
    "geepers_status": "geepers_status",
    "geepers_snippets": "geepers_snippets",

    # Deploy agents
    "geepers_validator": "geepers_validator",
    "geepers_caddy": "geepers_caddy",
    "geepers_services": "geepers_services",
    "geepers_canary": "geepers_canary",

    # Quality agents
    "geepers_a11y": "geepers_a11y",
    "geepers_perf": "geepers_perf",
    "geepers_api": "geepers_api",
    "geepers_deps": "geepers_deps",
    "geepers_critic": "geepers_critic",

    # Research agents
    "geepers_data": "geepers_data",
    "geepers_links": "geepers_links",
    "geepers_diag": "geepers_diag",
    "geepers_citations": "geepers_citations",

    # Fullstack agents
    "geepers_db": "geepers_db",
    "geepers_design": "geepers_design",
    "geepers_react": "geepers_react",
    "geepers_flask": "geepers_flask",

    # Domain agents
    "geepers_corpus": "geepers_corpus",
    "geepers_gamedev": "geepers_gamedev",
    "geepers_pycli": "geepers_pycli",

    # System agents
    "geepers_janitor": "geepers_janitor",
    "geepers_scalpel": "geepers_scalpel",
    "geepers_dashboard": "geepers_dashboard",
}


# ============================================================================
# PROMPT TEMPLATES
# ============================================================================

AGENT_PROMPTS = {
    "geepers_scout": """
Execute reconnaissance on project: {project}

Tasks:
1. Scan for code quality issues
2. Apply quick fixes where safe
3. Generate improvement recommendations
4. Update ~/geepers/recommendations/by-project/{project_name}.md

{context}

Report to: ~/geepers/reports/by-date/{date}/scout-{project_name}.md
""",

    "geepers_repo": """
Perform git hygiene on project: {project}

Tasks:
1. Review uncommitted changes
2. Clean up temp files and artifacts
3. Organize staged changes
4. Create meaningful commits
5. Archive old branches if needed

{context}

Report to: ~/geepers/reports/by-date/{date}/repo-{project_name}.md
""",

    "geepers_status": """
Update status dashboard for project: {project}

Tasks:
1. Log work completed this session
2. Update ~/geepers/status/current-session.json
3. Generate session summary

{context}

Report to: ~/geepers/status/
""",

    "geepers_snippets": """
Harvest reusable patterns from project: {project}

Tasks:
1. Identify reusable code patterns in recently modified files
2. Extract and document useful snippets
3. Add to ~/geepers/snippets/ or ~/SNIPPETS/
4. Avoid duplicating existing snippets

{context}

Focus on files modified in this session.
""",
}


# ============================================================================
# DISPATCH FACTORY
# ============================================================================

def create_agent_dispatch(
    agent_name: str,
    project: str,
    context: Optional[Dict[str, Any]] = None,
    previous_results: Optional[Dict[str, Any]] = None,
) -> AgentDispatch:
    """
    Create dispatch instructions for an agent.

    Args:
        agent_name: Name of the agent (e.g., "geepers_scout")
        project: Project path or identifier
        context: Additional context for the agent
        previous_results: Results from previous phases

    Returns:
        AgentDispatch with Task tool parameters
    """
    subagent_type = AGENT_SUBAGENT_MAP.get(agent_name, agent_name)

    # Build the prompt for the agent
    prompt = get_agent_prompt(agent_name, project, context)

    if previous_results:
        prompt += "\n\nPrevious phase results:\n"
        for phase, result in previous_results.items():
            prompt += f"  - {phase}: {result.get('status', 'unknown')}\n"

    return AgentDispatch(
        agent_name=agent_name,
        subagent_type=subagent_type,
        prompt=prompt,
        context=context or {},
        description=f"Run {agent_name} on {project}",
    )


def get_agent_prompt(
    agent_name: str,
    project: str,
    context: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Get the full prompt for an agent.

    Uses templates when available, falls back to generic prompt.

    Args:
        agent_name: Name of agent
        project: Project path
        context: Additional context

    Returns:
        Formatted prompt string
    """
    project_name = Path(project).name
    date = datetime.now().strftime("%Y-%m-%d")

    context_str = ""
    if context:
        context_str = "Additional context:\n" + "\n".join(
            f"  - {k}: {v}" for k, v in context.items()
        )

    template = AGENT_PROMPTS.get(agent_name)
    if template:
        return template.format(
            project=project,
            project_name=project_name,
            date=date,
            context=context_str,
        ).strip()

    # Generic prompt
    return f"""
Execute {agent_name} for project: {project}

{context_str}

Generate appropriate output to ~/geepers/
""".strip()


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    import json

    # Example 1: Create a single agent dispatch
    print("=" * 60)
    print("EXAMPLE 1: Single agent dispatch")
    print("=" * 60)

    dispatch = create_agent_dispatch(
        agent_name="geepers_scout",
        project="/home/user/my-project",
        context={"quick": True, "focus": "python"},
    )

    print("\nAgent dispatch:")
    print(json.dumps(dispatch.to_dict(), indent=2))

    print("\nTask tool call parameters:")
    print(json.dumps(dispatch.to_task_call(), indent=2))

    # Example 2: Create a workflow dispatch plan
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Multi-phase workflow")
    print("=" * 60)

    workflow = WorkflowDispatch(
        orchestrator_name="checkpoint",
        task_id="checkpoint_20251212_120000",
        project="/home/user/my-project",
        mode="full",
    )

    # Phase 1: Sequential analysis
    phase1_dispatches = [
        create_agent_dispatch("geepers_scout", "/home/user/my-project"),
        create_agent_dispatch("geepers_repo", "/home/user/my-project"),
    ]
    workflow.add_phase("Analysis", phase1_dispatches, parallel=False)

    # Phase 2: Parallel cleanup
    phase2_dispatches = [
        create_agent_dispatch("geepers_status", "/home/user/my-project"),
        create_agent_dispatch("geepers_snippets", "/home/user/my-project"),
    ]
    workflow.add_phase("Cleanup", phase2_dispatches, parallel=True)

    print("\nWorkflow dispatch plan:")
    print(json.dumps(workflow.to_dict(), indent=2))

    print("\n" + "=" * 60)
    print("EXECUTION INSTRUCTIONS")
    print("=" * 60)
    print(workflow._get_instructions())

    # Example 3: How an MCP server would use this
    print("\n" + "=" * 60)
    print("EXAMPLE 3: MCP server integration")
    print("=" * 60)

    print("""
In an MCP server's handle_tool_call method:

async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]):
    if tool_name == "orchestrator_run":
        project = arguments["project"]

        # Create workflow dispatch plan
        workflow = WorkflowDispatch(
            orchestrator_name="checkpoint",
            task_id=f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            project=project,
            mode=arguments.get("mode", "full"),
        )

        # Add phases with dispatches
        dispatches = [
            create_agent_dispatch("geepers_scout", project),
            create_agent_dispatch("geepers_repo", project),
        ]
        workflow.add_phase("Analysis", dispatches, parallel=False)

        # Return to Claude Code for execution
        return {
            "content": [
                {
                    "type": "text",
                    "text": workflow._get_instructions(),
                }
            ],
            "workflow": workflow.to_dict(),
        }

Claude Code then reads this response and executes each Task in order.
""")

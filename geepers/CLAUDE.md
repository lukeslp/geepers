# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working in this directory.

## What's Here

The `geepers` Python package — published to PyPI as `geepers-llm` v1.1.0. Provides orchestration infrastructure, config management, naming registry, and MCP server bridges.

## Module Map

| Module | Purpose |
|--------|---------|
| `config.py` | `ConfigManager` — multi-source config with provider key auto-discovery |
| `orchestrators/` | `BaseOrchestrator` + 7 concrete types + 7 pattern modules + enterprise subpackage |
| `naming/` | Registry mapping roles to identifiers across 4 scopes (internal/package/cli/mcp) |
| `utils/` | Async helpers, rate limiting, retry decorators, caching, parallel execution |
| `parser/` | Markdown agent definition parser (stub — not yet implemented) |
| `mcp/` | **Symlink** to `~/shared/mcp/` — the actual MCP server code lives there |

## Orchestrator Pattern

All orchestrators inherit from `BaseOrchestrator` (`orchestrators/base_orchestrator.py`) and implement:

```python
async def decompose_task(self, task, context=None) -> List[SubTask]
async def execute_subtask(self, subtask, context=None) -> AgentResult
async def synthesize_results(self, agent_results, context=None) -> str
```

The base class runs the full lifecycle: decompose → parallel/sequential execution (semaphore, timeout, retry) → synthesis → optional document generation. Streaming events emit via callbacks throughout.

**Concrete orchestrators** (in `orchestrators/`):

| Class | File | Purpose |
|-------|------|---------|
| `DreamCascadeOrchestrator` | `dream_cascade_orchestrator.py` | Hierarchical 3-tier research |
| `DreamSwarmOrchestrator` | `dream_swarm_orchestrator.py` | Parallel multi-domain search |
| `SequentialOrchestrator` | `sequential_orchestrator.py` | Sequential task execution |
| `ConditionalOrchestrator` | `conditional_orchestrator.py` | Branching logic |
| `IterativeOrchestrator` | `iterative_orchestrator.py` | Iterative refinement |
| `AccessibilityOrchestrator` | `accessibility_orchestrator.py` | A11y-focused workflow |
| `PhasedWorkflowOrchestrator` | `phased_workflow_orchestrator.py` | Phased execution |

**Legacy aliases** (in `orchestrators/__init__.py` for backward compat):
- `BeltalowdaOrchestrator` → `DreamCascadeOrchestrator`
- `SwarmOrchestrator` → `DreamSwarmOrchestrator`

**Pattern modules** (reusable building blocks, not standalone orchestrators):
`agent_lifecycle_management`, `hierarchical_agent_coordination`, `multi_agent_data_models`, `parallel_agent_execution`, `provider_abstraction_pattern`, `task_decomposition_pattern`, `task_tool_dispatch_pattern`

## Data Models (`orchestrators/models.py`)

`SubTask`, `AgentResult`, `SynthesisResult`, `OrchestratorResult`, `StreamEvent`, `EventType` — all have `to_dict()`/`from_dict()`.

## Config Management

```python
from geepers import ConfigManager

config = ConfigManager(app_name="myapp")
api_key = config.get_api_key("anthropic")
```

**Load precedence** (later overrides earlier):
1. Defaults passed at init
2. Custom config file (`.{app_name}`)
3. `.env` file
4. Environment variables
5. CLI arguments

16 LLM providers in `KNOWN_PROVIDERS` are auto-discovered from env vars.

## Naming Registry (`naming/core.py`)

Maps roles (`conductor`, `orchestrator`, `agent`, `utility`) to identifiers across four scopes:

| Scope | Pattern | Example |
|-------|---------|---------|
| internal | `{role}_{slug}` | `orchestrator_beltalowda` |
| package | `geepers-{role}-{slug}` | `geepers-orchestrator-beltalowda` |
| cli | `{role}-{slug}` | `orchestrator-beltalowda` |
| mcp | `{role}.{slug}` | `orchestrator.beltalowda` |

`LEGACY_MAP` translates old class names to canonical `NamingEntry`.

## Enterprise Subpackage (`orchestrators/enterprise/`)

Lower-level building blocks:
- `SwarmModuleBase` — Base class with status tracking
- `CaminaCoordinator` — Executive synthesis coordinator
- `BelterAgent` — Worker agent implementation
- `TaskRequest`/`TaskResult` — Priority-aware request/response models

## Streaming (`orchestrators/streaming.py`)

- `create_progress_bar_callback()` — Terminal progress bars
- `create_websocket_callback()` — WebSocket streaming
- `create_sse_callback()` — Server-Sent Events streaming

## MCP Symlink

`geepers/mcp/` → `~/shared/mcp/` — edit the target, not this symlink. Entry points registered in `pyproject.toml`:
- `geepers-unified`, `geepers-providers`, `geepers-data`, `geepers-cache`, `geepers-utility`, `geepers-websearch`

## Version Note

`__init__.py` reports `__version__ = "1.0.0"` — update this when bumping `pyproject.toml` version.

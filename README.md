# Geepers

Multi-agent orchestration for LLM workflows. Two ways to use it:
- **Claude Code plugin** - 60+ specialized agents for development tasks
- **Python package** - Orchestrators, config management, MCP server bridges

## Install

```bash
# Python package
pip install geepers-llm

# With specific LLM providers
pip install "geepers-llm[anthropic]"
pip install "geepers-llm[openai]"
pip install "geepers-llm[all]"      # everything

# As Claude Code plugin (agents only)
/plugin add lukeslp/geepers
```

## Python Package

Orchestration infrastructure for building multi-agent LLM systems:

```python
from geepers import ConfigManager
from geepers.orchestrators import (
    DreamCascadeOrchestrator,   # Hierarchical 3-tier research
    DreamSwarmOrchestrator,     # Parallel multi-domain search
    SequentialOrchestrator,
    ConditionalOrchestrator,
    IterativeOrchestrator,
)
```

### Orchestrators

All orchestrators share the same interface:

```python
async def decompose_task(task, context=None) -> List[SubTask]
async def execute_subtask(subtask, context=None) -> AgentResult
async def synthesize_results(results, context=None) -> str
```

The base class handles parallel execution with semaphores, timeouts, retries, and streaming progress events.

**Dream Cascade** - Three-tier hierarchical research. Decomposes tasks into subtasks, fans out to worker agents, synthesizes through a mid-level coordinator, then produces a final executive summary.

**Dream Swarm** - Parallel multi-domain search. Dispatches specialized agents (web search, academic, data analysis) simultaneously and merges results.

### Config Management

```python
from geepers import ConfigManager

config = ConfigManager(app_name="myapp")
# Loads: defaults < config file < .env < env vars < CLI args
api_key = config.get_api_key("anthropic")
```

Auto-discovers keys for 16 LLM providers from environment variables.

### MCP Server Bridges

Entry points for STDIO-based MCP servers:

- `geepers-unified` - All tools in one server
- `geepers-providers` - LLM provider access
- `geepers-data` - Data source clients
- `geepers-cache` - Caching layer
- `geepers-utility` - File and text utilities
- `geepers-websearch` - Web search tools

### Naming Registry

```python
from geepers.naming import get_identifier, resolve_legacy

get_identifier("orchestrator", "cascade")  # Returns scoped identifier
resolve_legacy("BeltalowdaOrchestrator")   # Maps to canonical name
```

## Claude Code Agents

60+ markdown-defined agents organized into 15 domains:

| Domain | Orchestrator | Specialists |
|--------|-------------|-------------|
| **Master** | conductor_geepers | Routes to all domains |
| **Checkpoint** | orchestrator_checkpoint | scout, repo, status, snippets |
| **Deploy** | orchestrator_deploy | caddy, services, validator |
| **Quality** | orchestrator_quality | a11y, perf, deps, critic, security, testing |
| **Frontend** | orchestrator_frontend | css, design, motion, typescript, uxpert, webperf |
| **Fullstack** | orchestrator_fullstack | db, react |
| **Hive** | orchestrator_hive | builder, planner, integrator, quickwin, refactor |
| **Research** | orchestrator_research | data, links, diag, citations, fetcher, searcher |
| **Web** | orchestrator_web | flask, express |
| **Python** | orchestrator_python | pycli |
| **Games** | orchestrator_games | game, gamedev, godot |
| **Corpus** | orchestrator_corpus | corpus, corpus_ux |
| **Datavis** | orchestrator_datavis | viz, color, story, math, data |
| **System** | (standalone) | help, onboard, diag |
| **Standalone** | (standalone) | api, scalpel, janitor, canary, dashboard, git, docs |

Agents follow a strict routing hierarchy: **Conductor -> Orchestrators -> Specialists**.

```
# Usage in Claude Code (via Task tool)
Task with subagent_type="geepers_scout"
Task with subagent_type="geepers_orchestrator_frontend"
Task with subagent_type="conductor_geepers"
```

## Related

- [dr-eamer-ai-shared](https://pypi.org/project/dr-eamer-ai-shared/) - Core shared library (LLM providers, data clients)
- [geepers-orchestrators](https://pypi.org/project/geepers-orchestrators/) - Standalone orchestration patterns
- [MCP-Dreamwalker](https://github.com/lukeslp/mcp-dreamwalker) - MCP server for multi-agent workflows

## License

MIT - Luke Steuber

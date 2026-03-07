# Geepers

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/geepers-llm.svg)](https://pypi.org/project/geepers-llm/)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://pypi.org/project/geepers-llm/)
[![Live](https://img.shields.io/badge/live-dr.eamer.dev-cyan.svg)](https://dr.eamer.dev/geepers/)

Multi-agent orchestration for LLM workflows. Ships as a Python package for building orchestrated pipelines and as a Claude Code plugin that puts 72 specialized agents a task invocation away.

## Features

- Run hierarchical research workflows with Dream Cascade — tasks decompose into subtasks, flow through a mid-level coordinator, and arrive at an executive summary
- Dispatch parallel agents across domains with Dream Swarm — web, academic, and data searches run simultaneously and merge into a unified result
- Load config from any combination of defaults, `.env`, env vars, and CLI args; later sources always win
- Auto-discover API keys for 16 LLM providers from the environment with no extra setup
- Stream real-time progress via callbacks — terminal progress bars, WebSocket, or SSE
- Install as a Claude Code plugin and invoke 72 specialized agents across 15 domains from any session

## Ecosystem

| | |
|---|---|
| **PyPI** | [`geepers-llm`](https://pypi.org/project/geepers-llm/) · [`geepers-kernel`](https://pypi.org/project/geepers-kernel/) |
| **Claude Code** | [`/plugin add lukeslp/geepers`](https://github.com/lukeslp/geepers-skills) |
| **Codex CLI** | [`geepers-gpt`](https://github.com/lukeslp/geepers-gpt) |
| **Gemini** | [`geepers-gemini`](https://github.com/lukeslp/geepers-gemini) |
| **ClawHub** | [`geepers-api-skills`](https://github.com/lukeslp/geepers-api-skills) |
| **MCP servers** | [`geepers-unified` · `geepers-providers` · `geepers-data` · `geepers-websearch`](https://github.com/lukeslp/geepers-kernel) |
| **Orchestration** | [`beltalowda`](https://github.com/lukeslp/beltalowda) · [`multi-agent-orchestration`](https://github.com/lukeslp/multi-agent-orchestration) |
| **Data clients** | [`research-data-clients`](https://github.com/lukeslp/research-data-clients) — 17+ structured APIs |

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

## Quick Start

```python
from geepers import ConfigManager
from geepers.orchestrators import DreamCascadeOrchestrator

config = ConfigManager(app_name="myapp")

orchestrator = DreamCascadeOrchestrator(config=config)
result = await orchestrator.run("Summarize recent research on transformer efficiency")
print(result.summary)
```

## Python Package

Orchestration infrastructure for LLM workflows:

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

Every orchestrator subclasses `BaseOrchestrator` and implements three abstract methods:

```python
async def decompose_task(self, task, context=None) -> List[SubTask]:
    ...  # Break the task into subtasks

async def execute_subtask(self, subtask, context=None) -> AgentResult:
    ...  # Run a single subtask

async def synthesize_results(self, results, context=None) -> str:
    ...  # Merge all results into a final output
```

The base class handles parallel execution, timeouts, retries, and streaming events automatically.

**Dream Cascade** — Hierarchical research workflow. Breaks a task into subtasks, farms them to worker agents, synthesizes through a mid-level coordinator, and produces an executive summary.

**Dream Swarm** — Parallel search across domains. Dispatches specialized agents (web search, academic, data analysis) simultaneously and merges the results.

### Config Management

```python
from geepers import ConfigManager

config = ConfigManager(app_name="myapp")
# Loads: defaults < config file < .env < env vars < CLI args
api_key = config.get_api_key("anthropic")
```

Auto-discovers keys for 16 LLM providers from environment variables.

### MCP Server Bridges

Six STDIO-based MCP servers ship with the package, covering the most common tool categories:

- `geepers-unified` — All tools in one server
- `geepers-providers` — LLM provider access
- `geepers-data` — Data source clients
- `geepers-cache` — Caching layer
- `geepers-utility` — File and text utilities
- `geepers-websearch` — Web search tools

### Naming Registry

Maps roles to consistent identifiers across four scopes (internal, package, CLI, MCP) and resolves legacy class names to their canonical equivalents:

```python
from geepers.naming import get_identifier, resolve_legacy

get_identifier("orchestrator", "cascade")  # Returns scoped identifier
resolve_legacy("BeltalowdaOrchestrator")   # Maps to canonical name
```

## Claude Code Agents

Markdown-defined agents organized into 15 domains. Each domain has an orchestrator that coordinates its specialists; the top-level conductor routes across all domains.

| Domain | Orchestrator | Specialists |
|--------|-------------|-------------|
| Master | conductor_geepers | Routes to all domains |
| Checkpoint | orchestrator_checkpoint | scout, repo, status, snippets |
| Deploy | orchestrator_deploy | caddy, services, validator |
| Quality | orchestrator_quality | a11y, perf, deps, critic, security, testing |
| Frontend | orchestrator_frontend | css, design, motion, typescript, uxpert, webperf |
| Fullstack | orchestrator_fullstack | db, react |
| Hive | orchestrator_hive | builder, planner, integrator, quickwin, refactor |
| Research | orchestrator_research | data, links, diag, citations, fetcher, searcher, doublecheck |
| Web | orchestrator_web | flask, express |
| Python | orchestrator_python | pycli |
| Games | orchestrator_games | game, gamedev, godot |
| Corpus | orchestrator_corpus | corpus, corpus_ux |
| Datavis | orchestrator_datavis | viz, color, story, math, data |
| System | (standalone) | help, onboard, diag |
| Standalone | (standalone) | api, scalpel, janitor, canary, dashboard, git, docs |

Routing: Conductor → Orchestrators → Specialists.

To invoke an agent in Claude Code, use the `Task` tool with the agent's `subagent_type`:

```
conductor_geepers               # top-level router — when in doubt, start here
geepers_orchestrator_frontend   # coordinates all frontend specialists
geepers_scout                   # fast project reconnaissance
geepers_orchestrator_research   # coordinates research and data agents
```

## Cross-Platform Skills

38 skill packs in `skills/source/` packaged for Claude Desktop, Codex CLI, Gemini, and ClawHub. The canonical registry lives in `manifests/skills-manifest.yaml`.

Skills fall into three categories: **Claude Desktop skills** for local workflows (datavis, engineering, finance, server-deploy, and others), **API skills** that wrap the public `dr.eamer.dev` REST API (geepers-llm, geepers-orchestrate, geepers-data, and related), and **platform adapters** that export the same skill definitions in the format each platform expects.

## Author

**Luke Steuber** · [lukesteuber.com](https://lukesteuber.com) · [@lukesteuber.com](https://bsky.app/profile/lukesteuber.com)

## License

MIT — see [LICENSE](LICENSE)

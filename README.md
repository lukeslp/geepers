# Geepers

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/geepers-llm.svg)](https://pypi.org/project/geepers-llm/)

Multi-agent orchestration for LLM workflows — 73 Claude Code agents and a Python package for building orchestrated workflows.

## Ecosystem

| | |
|---|---|
| **PyPI** | [`geepers-llm`](https://pypi.org/project/geepers-llm/) · [`geepers-kernel`](https://pypi.org/project/geepers-kernel/) |
| **Claude Code** | [`/plugin add lukeslp/geepers`](https://github.com/lukeslp/geepers-skills) |
| **Codex CLI** | [`geepers-gpt`](https://github.com/lukeslp/geepers-gpt) |
| **Gemini** | [`geepers-gemini`](https://github.com/lukeslp/geepers-gemini) |
| **Manus** | [`geepers-manus`](https://github.com/lukeslp/geepers-manus) |
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

Every orchestrator implements three methods:

```python
async def decompose_task(task, context=None) -> List[SubTask]
async def execute_subtask(subtask, context=None) -> AgentResult
async def synthesize_results(results, context=None) -> str
```

Base class handles the grunt work: parallel execution, timeouts, retries, and streaming events.

Dream Cascade - Hierarchical research workflow. Breaks tasks into subtasks, farms them out to worker agents, synthesizes through a mid-level coordinator, produces executive summary.

Dream Swarm - Parallel search across domains. Dispatches specialized agents (web search, academic, data analysis) simultaneously and merges results.

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

73 markdown-defined agents organized into 15 domains:

| Domain | Orchestrator | Specialists |
|--------|-------------|-------------|
| Master | conductor_geepers | Routes to all domains |
| Checkpoint | orchestrator_checkpoint | scout, repo, status, snippets |
| Deploy | orchestrator_deploy | caddy, services, validator |
| Quality | orchestrator_quality | a11y, perf, deps, critic, security, testing |
| Frontend | orchestrator_frontend | css, design, motion, typescript, uxpert, webperf |
| Fullstack | orchestrator_fullstack | db, react |
| Hive | orchestrator_hive | builder, planner, integrator, quickwin, refactor |
| Research | orchestrator_research | data, links, diag, citations, fetcher, searcher |
| Web | orchestrator_web | flask, express |
| Python | orchestrator_python | pycli |
| Games | orchestrator_games | game, gamedev, godot |
| Corpus | orchestrator_corpus | corpus, corpus_ux |
| Datavis | orchestrator_datavis | viz, color, story, math, data |
| System | (standalone) | help, onboard, diag |
| Standalone | (standalone) | api, scalpel, janitor, canary, dashboard, git, docs |

Routing hierarchy: Conductor -> Orchestrators -> Specialists.

```
# Usage in Claude Code (via Task tool)
Task with subagent_type="geepers_scout"
Task with subagent_type="geepers_orchestrator_frontend"
Task with subagent_type="conductor_geepers"
```

## License

MIT - Luke Steuber

## Cross-Platform Skill Packaging

Skills live in `skills/source/` and get built and synced to each platform mirror repo.

```bash
# 1) Validate skill manifests and SKILL.md frontmatter
python3 scripts/validate-skills.py --strict

# 2) Build packages for Claude, Codex, Gemini, Manus, and ClawHub
python3 scripts/build-platform-packages.py --platform all --clean

# 3) Check drift between built packages and mirror repos
bash scripts/report-drift.sh --strict --skip-missing

# 4) Push built packages to mirror repos
bash scripts/sync-mirrors.sh --delete
```

Key files:
- `manifests/skills-manifest.yaml`
- `manifests/platforms.yaml`
- `manifests/aliases.yaml`
- `docs/UNIFICATION_ARCHITECTURE.md`
- `docs/MIGRATION_MAP.md`

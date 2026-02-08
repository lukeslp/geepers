# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

Geepers is a multi-agent orchestration system that ships as a **Claude Code plugin** (`/plugin add lukeslp/geepers`). It has two distinct layers:

1. **Agent definitions** (`agents/`) - 62 markdown-defined specialists organized into 14 domains, invoked via Claude Code's `Task` tool with `subagent_type`
2. **Python package** (`geepers/`) - Orchestration framework, config management, naming registry, and utilities. Published to PyPI as `geepers`. The `geepers/mcp/` directory is a symlink to `~/shared/mcp/` (the actual MCP server code).

## Commands

```bash
# Install package in dev mode
pip install -e .

# Test imports
python -c "from geepers import ConfigManager"

# Run MCP server (what Claude Code connects to)
~/start-mcp-server

# Publish to PyPI
python -m build && twine upload dist/*

# Rebuild Claude Desktop skill zips after editing source
cd ~/geepers/skills && bash rebuild-zips.sh
```

## Architecture

### Agent Hierarchy

Agents follow a strict routing hierarchy: **Conductor -> Orchestrators -> Specialists**

- `conductor_geepers` (master/) - Top-level router, dispatches to orchestrators
- 12 orchestrators (one per domain) - Coordinate groups of specialists
- 50 specialists - Do the actual work

Each agent is a markdown file with YAML frontmatter (`name`, `description`, `model`, `color`) and structured sections (Mission, Workflow, Coordination Protocol). The plugin manifest at `.claude-plugin/plugin.json` maps agent IDs to their markdown source paths.

### Python Package Modules

| Module | Purpose |
|--------|---------|
| `geepers/orchestrators/` | Abstract `BaseOrchestrator` + 5 concrete implementations (DreamCascade, DreamSwarm, Sequential, Conditional, Iterative) |
| `geepers/config.py` | `ConfigManager` - multi-source config loading with precedence: defaults < config file < .env < env vars < CLI args |
| `geepers/naming/` | Naming registry mapping roles (conductor/orchestrator/agent/utility) to identifiers across scopes (internal/package/cli/mcp) |
| `geepers/utils/` | Async patterns, rate limiting, retry decorators, caching |
| `geepers/parser/` | Markdown agent definition parser (stub) |

### Orchestrator Pattern

All orchestrators inherit from `BaseOrchestrator` and implement three abstract methods:

```python
async def decompose_task(self, task, context=None) -> List[SubTask]
async def execute_subtask(self, subtask, context=None) -> AgentResult
async def synthesize_results(self, agent_results, context=None) -> str
```

The base class handles the workflow lifecycle: decompose -> parallel/sequential execution (with semaphore, timeout, retry) -> synthesis -> optional document generation. Streaming events are emitted via callbacks throughout.

Legacy class names (`BeltalowdaOrchestrator`, `SwarmOrchestrator`) are aliased for backward compatibility in `orchestrators/__init__.py`.

### MCP Server

`geepers/mcp/` symlinks to `~/shared/mcp/`. The actual server code lives there. Entry points for STDIO bridges are registered in `pyproject.toml` under `[project.scripts]`:
- `geepers-unified`, `geepers-providers`, `geepers-data`, `geepers-cache`, `geepers-utility`, `geepers-websearch`

Claude Code connects via `~/.mcp.json` -> `~/start-mcp-server` -> `~/shared/mcp/UnifiedMCPServer`.

### Skills

`skills/source/` contains Claude Desktop skills (SKILL.md + scripts). Each skill is zipped into `skills/zips/` for upload. Skills are separate from agents - skills run in Claude Desktop, agents run in Claude Code.

### Output Directories

Agents write reports, recommendations, and status files to:
- `reports/` - Organized by date and project
- `recommendations/by-project/` - Per-project improvement suggestions
- `status/` - Session and project status tracking
- `temp/SNIPPETS/` - Harvested reusable code patterns

These directories are excluded from the PyPI package via `pyproject.toml`.

## Agent Domain Reference

| Domain | Directory | Orchestrator | Specialist Count |
|--------|-----------|-------------|-----------------|
| Master | `agents/master/` | `conductor_geepers` | 0 |
| Checkpoint | `agents/checkpoint/` | `geepers_orchestrator_checkpoint` | 4 (scout, repo, status, snippets) |
| Deploy | `agents/deploy/` | `geepers_orchestrator_deploy` | 4 (caddy, services, validator, canary) |
| Quality | `agents/quality/` | `geepers_orchestrator_quality` | 7 (a11y, perf, api, deps, critic, testing, security) |
| Frontend | `agents/frontend/` | `geepers_orchestrator_frontend` | 7 (css, typescript, motion, webperf, design, uxpert, react) |
| Fullstack | `agents/fullstack/` | `geepers_orchestrator_fullstack` | 3 (db, design, react) |
| Web | `agents/web/` | `geepers_orchestrator_web` | 2 (flask, express) |
| Hive | `agents/hive/` | `geepers_orchestrator_hive` | 5 (planner, builder, quickwin, integrator, refactor) |
| Research | `agents/research/` | `geepers_orchestrator_research` | 6 (data, links, diag, citations, fetcher, searcher) |
| Python | `agents/python/` | `geepers_orchestrator_python` | 1 (pycli) |
| Games | `agents/games/` | `geepers_orchestrator_games` | 3 (gamedev, game, godot) |
| Corpus | `agents/corpus/` | `geepers_orchestrator_corpus` | 2 (corpus, corpus_ux) |
| Datavis | `agents/datavis/` | `geepers_orchestrator_datavis` | 5 (viz, color, story, math, data) |
| System | `agents/system/` | (none) | 3 (help, onboard, diag) |
| Standalone | `agents/standalone/` | (none) | 8 (api, scalpel, janitor, canary, dashboard, git, todoist, docs) |

Full routing guide: `agents/AGENT_DOMAINS.md`

## Key Symlinks

| Symlink | Target | Purpose |
|---------|--------|---------|
| `~/geepers_agents` | `~/geepers/agents/` | Backward compat for agent references |
| `~/geepers/geepers/mcp/` | `~/shared/mcp/` | MCP server code lives in shared library |

## Adding a New Agent

1. Create `agents/<domain>/geepers_<name>.md` with YAML frontmatter and structured sections
2. Add entry to `.claude-plugin/plugin.json` in the `agents` array
3. If it belongs to an orchestrator, update that orchestrator's markdown to reference it
4. Update `agents/AGENT_DOMAINS.md`

## Adding a New Orchestrator Type

Subclass `BaseOrchestrator` in `geepers/orchestrators/`:
1. Implement `decompose_task()`, `execute_subtask()`, `synthesize_results()`
2. Create config dataclass in `orchestrators/config.py`
3. Export from `orchestrators/__init__.py`

## ConfigManager Precedence

Config values are loaded in this order (later overrides earlier):
1. Defaults passed at init
2. Custom config file (`.{app_name}`)
3. `.env` file
4. Environment variables
5. CLI arguments

Known provider API keys are auto-discovered from environment even if not in defaults.

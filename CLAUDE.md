# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

Geepers is a multi-agent orchestration system that ships in two ways:
- **Claude Code plugin** (`/plugin add lukeslp/geepers`) - Installs ~52 registered agent definitions
- **Python package** (`pip install geepers-llm`) - Provides orchestrators, config, utilities

It has four distinct layers:

1. **Agent definitions** (`agents/`) - Markdown-defined specialists organized into 15 domains, invoked via Claude Code's `Task` tool with `subagent_type`
2. **Python package** (`geepers/`) - Orchestration framework, config management, naming registry, and utilities. Published to PyPI as **`geepers-llm`** v1.1.0. The `geepers/mcp/` directory is a symlink to `~/shared/mcp/` (the actual MCP server code).
3. **Skills** (`skills/source/`) - 38 skill packs (Claude Desktop skills + geepers-* API skills) zipped for upload
4. **Platform manifests** (`platforms/`) - Generated manifests and skill packages for 5 platforms: `claude`, `clawhub`, `codex`, `gemini`, `manus`. Each contains `manifest.generated.json`, `aliases.json`, `SYNC_INFO.md`, `README.md`, and a `skills/` directory with platform-specific skill exports.

## Commands

```bash
# Install from PyPI (regular usage)
pip install geepers-llm                 # Core package
pip install "geepers-llm[anthropic]"    # With Anthropic provider
pip install "geepers-llm[all]"          # Everything

# Install in dev mode (for development)
pip install -e .
pip install -e ".[all]"

# Verify installation
python -c "from geepers import ConfigManager"
python -c "from geepers.orchestrators import DreamCascadeOrchestrator"
python -c "from geepers.naming import get_identifier"

# Run MCP server (what Claude Code connects to)
~/start-mcp-server

# Build and publish to PyPI
python -m build
twine upload dist/*

# Rebuild skill zips after editing source
cd ~/geepers/skills && bash rebuild-zips.sh

# System cleanup (removes logs, backups, temp files)
bash scripts/system-cleanup.sh
```

**Testing**: No formal test suite exists. Verify changes by:
1. Testing imports (see above)
2. Running the MCP server and checking Claude Code connection
3. Testing orchestrator execution with a simple task
4. Checking agent invocation via Claude Code Task tool

## Dependencies

**Core dependency**: `geepers-kernel>=1.2.0` - Foundation library providing LLM providers, orchestration primitives, and data fetching. Geepers builds on top of this.

**Optional dependency groups** (defined in `pyproject.toml`):
- LLM providers: `anthropic`, `openai`, `xai`, `mistral`, `cohere`, `gemini`, `perplexity`, `groq`, `huggingface`
- Data sources: `arxiv`, `wikipedia`, `youtube`
- Utilities: `tts`, `citations`, `redis`, `documents`, `telemetry`
- Install specific groups: `pip install "geepers-llm[anthropic,redis]"`

## Architecture

### Agent Hierarchy

Agents follow a strict routing hierarchy: **Conductor -> Orchestrators -> Specialists**

- `conductor_geepers` (`agents/master/`) - Top-level router, dispatches to orchestrators
- 13 orchestrators (one per domain) - Coordinate groups of specialists
- ~40 specialists - Do the actual work

52 agents are registered in `.claude-plugin/plugin.json`. More `.md` files exist on disk that are not yet registered.

Each agent is a markdown file with YAML frontmatter (`name`, `description`, `model`, `color`) and structured sections (Mission, Workflow, Coordination Protocol). The plugin manifest at `.claude-plugin/plugin.json` maps agent IDs to their markdown source paths.

Shared workflow requirements that all agents must follow live in `agents/shared/WORKFLOW_REQUIREMENTS.md`.

### Python Package Modules

| Module | Purpose |
|--------|---------|
| `geepers/orchestrators/` | Abstract `BaseOrchestrator` + concrete orchestrators + 7 pattern modules + enterprise subpackage |
| `geepers/config.py` | `ConfigManager` - multi-source config loading with precedence: defaults < config file < .env < env vars < CLI args |
| `geepers/naming/` | Naming registry mapping roles (conductor/orchestrator/agent/utility) to identifiers across scopes (internal/package/cli/mcp) |
| `geepers/utils/` | Async patterns, rate limiting, retry decorators, caching, parallel task execution |
| `geepers/parser/` | Markdown agent definition parser (stub) |

### Orchestrator Pattern

All orchestrators inherit from `BaseOrchestrator` and implement three abstract methods:

```python
async def decompose_task(self, task, context=None) -> List[SubTask]
async def execute_subtask(self, subtask, context=None) -> AgentResult
async def synthesize_results(self, agent_results, context=None) -> str
```

The base class handles the workflow lifecycle: decompose -> parallel/sequential execution (with semaphore, timeout, retry) -> synthesis -> optional document generation. Streaming events are emitted via callbacks throughout.

**Concrete orchestrators**: `DreamCascadeOrchestrator` (hierarchical 3-tier), `DreamSwarmOrchestrator` (parallel multi-domain search), `SequentialOrchestrator`, `ConditionalOrchestrator`, `IterativeOrchestrator`, `AccessibilityOrchestrator`, `PhasedWorkflowOrchestrator`.

**Pattern modules** (reusable orchestration building blocks): `agent_lifecycle_management`, `hierarchical_agent_coordination`, `multi_agent_data_models`, `parallel_agent_execution`, `provider_abstraction_pattern`, `task_decomposition_pattern`, `task_tool_dispatch_pattern`.

**Config hierarchy**: `OrchestratorConfig` (base) -> `DreamCascadeConfig`, `DreamSwarmConfig`, `LessonPlanConfig`.

**Data models** (`orchestrators/models.py`): `SubTask`, `AgentResult`, `SynthesisResult`, `OrchestratorResult`, `StreamEvent`, `EventType`. All have `to_dict()`/`from_dict()` methods.

**Legacy aliases** (backward compat in `orchestrators/__init__.py`): `BeltalowdaOrchestrator` = `DreamCascadeOrchestrator`, `SwarmOrchestrator` = `DreamSwarmOrchestrator`, `BeltalowdaConfig` = `DreamCascadeConfig`, `SwarmConfig` = `DreamSwarmConfig`.

### Enterprise Subpackage

`geepers/orchestrators/enterprise/` provides lower-level building blocks for multi-agent workflows:
- `SwarmModuleBase` - Base class for swarm modules with status tracking
- `CaminaCoordinator` - Executive synthesis coordinator
- `BelterAgent` - Worker agent implementation
- `TaskRequest`/`TaskResult` - Request/response models with priority

### Streaming

`orchestrators/streaming.py` provides callback wrappers for real-time progress:
- `StreamingCallbackWrapper` - Generic callback wrapper
- `create_progress_bar_callback()` - Terminal progress bars
- `create_websocket_callback()` - WebSocket streaming
- `create_sse_callback()` - Server-Sent Events streaming

### MCP Server

`geepers/mcp/` symlinks to `~/shared/mcp/`. The actual server code lives there. Entry points for STDIO bridges are registered in `pyproject.toml` under `[project.scripts]`:
- `geepers-unified`, `geepers-providers`, `geepers-data`, `geepers-cache`, `geepers-utility`, `geepers-websearch`

Claude Code connects via `~/.mcp.json` -> `~/start-mcp-server` -> `~/shared/mcp/UnifiedMCPServer`.

### Skills

`skills/source/` contains 38 skill packs, each with SKILL.md + scripts. Zipped into `skills/zips/` for upload.

| Category | Skill Packs |
|----------|-------------|
| **Claude Desktop** | `bluesky-cli`, `data-fetch`, `datavis`, `dream-swarm`, `engineering`, `executive`, `finance`, `git-hygiene-guardian`, `mcp-orchestration`, `porkbun-cli`, `product`, `server-deploy`, `vision` |
| **Geepers workflow** | `geepers-builder`, `geepers-planner`, `geepers-quality`, `geepers-scout`, `geepers-swarm`, `geepers-team`, `geepers-testing`, `geepers-validate` |
| **API skills** (dr.eamer.dev API) | `geepers-corpus`, `geepers-data`, `geepers-datavis`, `geepers-deploy`, `geepers-dream-swarm`, `geepers-engineering`, `geepers-etymology`, `geepers-executive`, `geepers-fetch`, `geepers-finance`, `geepers-git`, `geepers-llm`, `geepers-mcp`, `geepers-orchestrate`, `geepers-porkbun`, `geepers-product`, `geepers-vision` |

Skills run in Claude Desktop; agents run in Claude Code. API skills wrap the public dr.eamer.dev REST API (`/code/api/`). Rebuild zips after editing source: `cd ~/geepers/skills && bash rebuild-zips.sh`

### Output Directories

Agents write reports, recommendations, and status files to:
- `reports/` - Organized by date and project
- `recommendations/by-project/` - Per-project improvement suggestions
- `status/` - Session and project status tracking
- `temp/SNIPPETS/` - Harvested reusable code patterns
- `hive/` - Hive orchestrator workspace: queue files, quickwins lists, planner summaries, cross-project work documents. **Do not delete these** — they represent in-progress work plans.
- `todos/` - Per-project backend todo lists

These directories are excluded from the PyPI package via `pyproject.toml`.

## Agent Domain Reference

| Domain | Directory | Orchestrator | Key Specialists |
|--------|-----------|-------------|-----------------|
| Master | `agents/master/` | `conductor_geepers` | (routes to all) |
| Checkpoint | `agents/checkpoint/` | `geepers_orchestrator_checkpoint` | scout, repo, status, snippets |
| Deploy | `agents/deploy/` | `geepers_orchestrator_deploy` | caddy, services, validator |
| Quality | `agents/quality/` | `geepers_orchestrator_quality` | a11y, perf, deps, critic, testing, security |
| Frontend | `agents/frontend/` | `geepers_orchestrator_frontend` | css, typescript, motion, webperf, design, uxpert |
| Fullstack | `agents/fullstack/` | `geepers_orchestrator_fullstack` | db, react |
| Web | `agents/web/` | `geepers_orchestrator_web` | flask, express |
| Hive | `agents/hive/` | `geepers_orchestrator_hive` | planner, builder, quickwin, integrator, refactor |
| Research | `agents/research/` | `geepers_orchestrator_research` | data, links, diag, citations, fetcher, searcher, doublecheck |
| Python | `agents/python/` | `geepers_orchestrator_python` | pycli |
| Games | `agents/games/` | `geepers_orchestrator_games` | gamedev, game, godot |
| Corpus | `agents/corpus/` | `geepers_orchestrator_corpus` | corpus, corpus_ux |
| Datavis | `agents/datavis/` | `geepers_orchestrator_datavis` | viz, color, story, math, data, poet |
| System | `agents/system/` | (none) | help, onboard, diag |
| Standalone | `agents/standalone/` | (none) | api, scalpel, janitor, canary, dashboard, git, todoist, docs, humanizer, readme |

Full routing guide: `agents/AGENT_DOMAINS.md`

## Directory Structure

```
~/geepers/
├── agents/              # Markdown agent definitions (15 domains)
├── geepers/             # Python package source
│   ├── orchestrators/   # BaseOrchestrator + concrete orchestrators + patterns
│   ├── mcp/            # Symlink to ~/shared/mcp/ (actual MCP server code)
│   ├── config.py       # ConfigManager (multi-source loading)
│   ├── naming/         # Naming registry (4 scopes)
│   ├── parser/         # Agent markdown parser (stub)
│   └── utils/          # Async, retry, cache, parallel execution
├── skills/             # Skill packs
│   ├── source/         # Editable SKILL.md + scripts (38 packs)
│   └── zips/           # Built archives for upload
├── platforms/          # Generated manifests for 5 platforms (claude, codex, gemini, manus, clawhub)
├── manifests/          # Canonical skills-manifest.yaml and aliases.yaml
├── .claude-plugin/     # Plugin manifest (plugin.json) and marketplace.json
├── hive/               # Hive orchestrator workspace (queue, quickwins, plans)
├── todos/              # Per-project todo lists
├── reports/            # Agent output (excluded from package)
├── recommendations/    # Per-project suggestions (excluded from package)
├── status/             # Session tracking (excluded from package)
├── temp/SNIPPETS/      # Reusable code patterns (excluded from package)
└── scripts/            # Utility scripts (system-cleanup.sh)
```

## Key Symlinks

| Symlink | Target | Purpose |
|---------|--------|---------|
| `~/geepers_agents` | `~/geepers/agents/` | Backward compat for agent references |
| `~/geepers/geepers/mcp/` | `~/shared/mcp/` | MCP server code lives in shared library |

## Adding a New Agent

1. Create `agents/<domain>/geepers_<name>.md` with YAML frontmatter (`name`, `description`, `model`, `color`) and structured sections (Mission, Workflow, Coordination Protocol)
2. Add entry to `.claude-plugin/plugin.json` in the `agents` array
3. If it belongs to an orchestrator, update that orchestrator's markdown to reference it
4. Update `agents/AGENT_DOMAINS.md`

## Adding a New Orchestrator Type

Subclass `BaseOrchestrator` in `geepers/orchestrators/`:
1. Implement `decompose_task()`, `execute_subtask()`, `synthesize_results()`
2. Create config dataclass extending `OrchestratorConfig` in `orchestrators/config.py`
3. Export from `orchestrators/__init__.py`

## Naming Convention

The naming registry (`geepers/naming/core.py`) maps roles to identifiers across four scopes:

| Scope | Pattern | Example |
|-------|---------|---------|
| internal | `{role}_{slug}` | `orchestrator_beltalowda` |
| package | `geepers-{role}-{slug}` | `geepers-orchestrator-beltalowda` |
| cli | `{role}-{slug}` | `orchestrator-beltalowda` |
| mcp | `{role}.{slug}` | `orchestrator.beltalowda` |

`LEGACY_MAP` in `naming/core.py` translates old class names (e.g. `BeltalowdaOrchestrator`) to their canonical `NamingEntry`.

## ConfigManager Precedence

Config values are loaded in this order (later overrides earlier):
1. Defaults passed at init
2. Custom config file (`.{app_name}`)
3. `.env` file
4. Environment variables
5. CLI arguments

Known provider API keys (16 providers in `KNOWN_PROVIDERS`) are auto-discovered from environment even if not in defaults.

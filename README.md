# Geepers

Multi-agent orchestration for LLM workflows. Ships as a Python package for building orchestrated pipelines and as a Claude Code plugin with 73 specialized agents across 15 domains.

## Features

- Run hierarchical research workflows with Dream Cascade — tasks decompose into subtasks, flow through a mid-level coordinator, and arrive at an executive summary
- Dispatch parallel agents across domains with Dream Swarm — web, academic, and data searches run simultaneously and merge into a unified result
- Load config from any combination of defaults, `.env`, env vars, and CLI args; later sources always win
- Auto-discover API keys for 16 LLM providers from the environment with no extra setup
- Stream real-time progress via callbacks — terminal progress bars, WebSocket, or SSE
- Install as a Claude Code plugin and invoke 73 specialized agents across 15 domains from any session

## Ecosystem

| | |
|---|---|
| **PyPI** | [`geepers-llm`](https://pypi.org/project/geepers-llm/) · [`geepers-kernel`](https://pypi.org/project/geepers-kernel/) |
| **Claude Code** | `/plugin add lukeslp/geepers` |
| **Manus** | `manus-skills.json` in this repo |
| **Codex** | `codex-package.json` in this repo |
| **Clawhub** | `clawhub-package.json` in this repo |
| **MCP servers** | [`geepers-mcp`](https://github.com/lukeslp/geepers-mcp) — `pip install geepers-mcp[all]` |
| **Orchestration** | [`beltalowda`](https://github.com/lukeslp/beltalowda) · [`multi-agent-orchestration`](https://github.com/lukeslp/multi-agent-orchestration) |
| **Data clients** | [`research-data-clients`](https://github.com/lukeslp/research-data-clients) — 17+ structured APIs |

## Install

### As Claude Code Plugin (recommended)

In Claude Code CLI:
```bash
/plugin add lukeslp/geepers
```

### Manual Installation (skills only)
```bash
git clone https://github.com/lukeslp/geepers.git ~/geepers
mkdir -p ~/.claude/skills
for zip in ~/geepers/skills/zips/*.zip; do
  name=$(basename "$zip" .zip)
  mkdir -p ~/.claude/skills/$name
  unzip -o "$zip" -d ~/.claude/skills/$name
done
```

## Quick Start

### 73 Specialized Agents

config = ConfigManager(app_name="myapp")

| Category | Agents | Purpose |
|----------|--------|---------|
| **Master** | geepers_conductor | Intelligent routing to specialists |
| **Checkpoint** | scout, repo, status, snippets, orchestrator | Session maintenance |
| **Deploy** | caddy, services, validator, orchestrator | Infrastructure |
| **Quality** | a11y, perf, api, deps, critic, security, testing, orchestrator | Code audits |
| **Frontend** | css, design, motion, typescript, uxpert, webperf, orchestrator | UI/UX development |
| **Fullstack** | db, react, orchestrator | End-to-end features |
| **Hive** | builder, planner, integrator, quickwin, refactor, orchestrator | Task execution |
| **Research** | data, links, diag, citations, fetcher, searcher, orchestrator | Data gathering |
| **Datavis** | color, data, math, story, viz, orchestrator | Data visualization |
| **Games** | game, gamedev, godot, orchestrator | Game development |
| **Corpus** | corpus, corpus_ux, orchestrator | Linguistics/NLP |
| **Web** | flask, express, orchestrator | Web applications |
| **Python** | pycli, orchestrator | Python projects |
| **Standalone** | api, scalpel, dashboard, canary, janitor, docs, git, todoist, humanizer | Specialized tasks |
| **System** | help, onboard, diag | System utilities |

### Packaged Skills

All agents are packaged as Claude Code skills in `skills/zips/` (39 zips):

| Skill | Type | Description |
|-------|------|-------------|
| **conductor** | Master | Top-level orchestrator routing to all agents |
| **checkpoint** | Orchestrator | Session boundaries, routine maintenance |
| **deploy** | Orchestrator | Deployment, infrastructure, Caddy |
| **quality** | Orchestrator | Code audits, a11y, perf, security, testing |
| **frontend** | Orchestrator | CSS, TypeScript, motion, design, UX |
| **fullstack** | Orchestrator | Backend + frontend end-to-end |
| **hive** | Orchestrator | Build from plans, execute backlogs |
| **research** | Orchestrator | Information gathering, API data |
| **datavis** | Orchestrator | D3.js, Chart.js, data visualization |
| **datavis-agents** | Orchestrator | Individual datavis specialist agents |
| **games** | Orchestrator | Game dev, Godot, gamification |
| **corpus** | Orchestrator | Linguistics, NLP, corpus work |
| **web-dev** | Orchestrator | Flask + Express web applications |
| **python-dev** | Orchestrator | Python projects, CLI tools |
| **server-deploy** | Standalone | dr.eamer.dev service management |
| **engineering** | Standalone | System architecture, full-stack code |
| **executive** | Standalone | Strategic planning, cross-team coordination |
| **finance** | Standalone | Monetization, financial modeling |
| **product** | Standalone | Product strategy, PRDs |
| **api-design** | Standalone | REST API design review |
| **canary** | Standalone | Quick health checks |
| **dashboard** | Standalone | System monitoring dashboard |
| **docs** | Standalone | Documentation generation |
| **git-ops** | Standalone | Git operations, conflict resolution |
| **git-hygiene-guardian** | Standalone | Git hygiene enforcement |
| **janitor** | Standalone | Project cleanup |
| **scalpel** | Standalone | Surgical code edits |
| **todoist** | Standalone | Todoist task management |
| **humanize** | Standalone | Clean up docs — fix terminology, tone, formatting |
| **system-diag** | Standalone | Full system diagnostics |
| **system-help** | Standalone | Agent discovery and help |
| **system-onboard** | Standalone | Project onboarding |
| **swarm** | Research | Parallel multi-domain search |
| **geepers-cascade** | Research | Hierarchical deep research |
| **geepers-publish** | Workflow | Publishing and release workflow |
| **geepers-team** | Workflow | Team coordination workflow |
| **data-fetch** | MCP | Universal data fetching server |
| **mcp-orchestration** | MCP | Multi-agent orchestration server |
| **vision** | MCP | Alt text and image analysis |

## Skill Structure

```
skills/
├── source/           # Skill source directories
│   ├── conductor/
│   │   └── SKILL.md
│   ├── quality/
│   │   ├── SKILL.md
│   │   └── agents/   # Sub-agent definitions
│   │       ├── geepers_a11y.md
│   │       ├── geepers_critic.md
│   │       └── ...
│   └── ...
├── zips/             # Packaged skill zips
├── rebuild-zips.sh   # Rebuild all zips from source
└── package_all_skills.py  # Generate skills from agents
```

### Orchestrators

Agents are available via Claude Code's Task tool with `subagent_type`:

```
# Quick reconnaissance
Task with subagent_type="geepers_scout"

# Infrastructure changes
Task with subagent_type="geepers_caddy"

# End-of-session cleanup
Task with subagent_type="geepers_orchestrator_checkpoint"

# Full-stack development
Task with subagent_type="geepers_orchestrator_fullstack"

# Frontend work
Task with subagent_type="geepers_orchestrator_frontend"
```

## Agent Categories

See [AGENT_DOMAINS.md](agents/shared/AGENT_DOMAINS.md) for the full routing guide.

**Orchestrators** coordinate multiple specialists:
- `geepers_conductor` - Master router
- `geepers_orchestrator_frontend` - CSS, React, design, motion
- `geepers_orchestrator_fullstack` - Backend + frontend
- `geepers_orchestrator_hive` - Build from plans and TODOs
- `geepers_orchestrator_quality` - Audits and reviews
- `geepers_orchestrator_deploy` - Infrastructure changes
- `geepers_orchestrator_checkpoint` - Session maintenance
- `geepers_orchestrator_research` - Data gathering
- `geepers_orchestrator_datavis` - Visualization
- `geepers_orchestrator_games` - Game development
- `geepers_orchestrator_corpus` - Linguistics/NLP
- `geepers_orchestrator_web` - Web applications
- `geepers_orchestrator_python` - Python projects

## Related: MCP-Dreamwalker

For programmatic orchestration with LLM providers and data clients, see [MCP-Dreamwalker](https://github.com/lukeslp/mcp-dreamwalker):

- **Dream Cascade** - Hierarchical 3-tier research orchestration
- **Dream Swarm** - Multi-domain parallel search
- **12 LLM Providers** - Anthropic, OpenAI, xAI, Gemini, Mistral, Cohere, etc.
- **17 Data Clients** - Census, arXiv, GitHub, NASA, Wikipedia, etc.

## Building Skills

```bash
# Regenerate all SKILL.md files from agent definitions
python3 skills/package_all_skills.py

# Rebuild all zip files
bash skills/rebuild-zips.sh

# Install to Claude Code
for zip in skills/zips/*.zip; do
  name=$(basename "$zip" .zip)
  mkdir -p ~/.claude/skills/$name
  unzip -o "$zip" -d ~/.claude/skills/$name
done
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
| Master | geepers_conductor | Routes to all domains |
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
geepers_conductor               # top-level router — when in doubt, start here
geepers_orchestrator_frontend   # coordinates all frontend specialists
geepers_scout                   # fast project reconnaissance
geepers_orchestrator_research   # coordinates research and data agents
```

## Cross-Platform Skills

22 skills in `skills/` shared across all platforms. One repo, multiple manifests — each platform gets its own manifest file generated from the same skill directories:

| Platform | Manifest | Install |
|----------|----------|---------|
| **Claude Code** | `.claude-plugin/plugin.json` | `/plugin add lukeslp/geepers` |
| **Manus** | `manus-skills.json` | Copy skills/ and manus-skills.json |
| **Codex** | `codex-package.json` | Copy skills/ and codex-package.json |
| **Clawhub** | `clawhub-package.json` | `bash scripts/publish-clawhub.sh` |

Regenerate all manifests after adding/removing skills:
```bash
python3 scripts/build-manifests.py
```

## Author

**Luke Steuber** · [lukesteuber.com](https://lukesteuber.com) · [@lukesteuber.com](https://bsky.app/profile/lukesteuber.com)

## License

MIT — see [LICENSE](LICENSE)

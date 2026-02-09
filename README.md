# Geepers

Multi-agent orchestration system with specialized Claude Code plugin agents and skills.

## Installation

### As Claude Code Plugin (recommended)

In Claude Code CLI:
```bash
# 1. Add the marketplace (one-time)
/plugin marketplace add lukeslp/geepers

# 2. Install the plugin
/plugin install geepers@geepers-marketplace
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

## What's Included

### 70 Specialized Agents

Markdown-defined agents for Claude Code that provide specialized workflows:

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
| **humanize** | Standalone | Remove AI writing indicators from documentation |
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

## Usage

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

See [AGENT_DOMAINS.md](agents/AGENT_DOMAINS.md) for the full routing guide.

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

## License

MIT License - Luke Steuber

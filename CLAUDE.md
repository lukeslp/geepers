# Geepers Package

Multi-agent orchestration system combining MCP tools, Claude Code plugin agents, and packaged skills.

## Consolidated Structure

```
~/geepers/                     # THE canonical geepers location
├── agents/                    # 73 markdown agent definitions
│   ├── master/                # conductor_geepers (top-level orchestrator)
│   ├── checkpoint/            # scout, repo, status, snippets + orchestrator
│   ├── deploy/                # caddy, services, validator + orchestrator
│   ├── quality/               # a11y, perf, api, deps, critic, security, testing + orchestrator
│   ├── frontend/              # css, design, motion, typescript, uxpert, webperf + orchestrator
│   ├── fullstack/             # db, react + orchestrator
│   ├── hive/                  # builder, planner, integrator, quickwin, refactor + orchestrator
│   ├── research/              # data, links, diag, citations, fetcher, searcher + orchestrator
│   ├── datavis/               # color, data, math, story, viz + orchestrator
│   ├── games/                 # game, gamedev, godot + orchestrator
│   ├── corpus/                # corpus, corpus_ux + orchestrator
│   ├── web/                   # flask, express + orchestrator
│   ├── python/                # pycli + orchestrator
│   ├── standalone/            # api, scalpel, dashboard, canary, janitor, docs, git, todoist
│   ├── system/                # help, onboard, diag
│   └── shared/                # Workflow requirements, parallel patterns
├── skills/                    # 37 packaged Claude Code skills
│   ├── source/                # Skill source directories
│   ├── zips/                  # Built skill zip files
│   ├── package_all_skills.py  # Generate SKILL.md from agent definitions
│   └── rebuild-zips.sh        # Rebuild all zips from source
├── geepers/                   # Python package
│   ├── mcp/ → ~/shared/mcp/  # Symlink to shared MCP server
│   ├── orchestrators/         # Workflow orchestration
│   └── parser/                # Agent markdown parser
├── .claude-plugin/            # Claude marketplace manifest
├── pyproject.toml             # PyPI package config
└── README.md
```

## Key Symlinks

| Symlink | Target | Purpose |
|---------|--------|---------|
| `~/geepers_agents` | `~/geepers/agents/` | Backward compatibility |
| `~/geepers/geepers/mcp/` | `~/shared/mcp/` | Avoid MCP code duplication |

## Key Commands

```bash
# Install in dev mode
pip install -e .

# Test imports
python -c "from geepers import ConfigManager"

# Run MCP server (what Claude Code uses)
~/start-mcp-server

# Regenerate skills from agent definitions
python3 skills/package_all_skills.py

# Rebuild skill zips
bash skills/rebuild-zips.sh

# Install skills to Claude Code
for zip in skills/zips/*.zip; do
  name=$(basename "$zip" .zip)
  mkdir -p ~/.claude/skills/$name
  unzip -o "$zip" -d ~/.claude/skills/$name
done
```

## Agent Categories (73 agents)

| Category | Orchestrator | Agents |
|----------|--------------|--------|
| **master/** | conductor_geepers | Routes to all other agents |
| **checkpoint/** | orchestrator_checkpoint | scout, repo, status, snippets |
| **deploy/** | orchestrator_deploy | caddy, services, validator |
| **quality/** | orchestrator_quality | a11y, perf, api, deps, critic, security, testing |
| **frontend/** | orchestrator_frontend | css, design, motion, typescript, uxpert, webperf |
| **fullstack/** | orchestrator_fullstack | db, react |
| **hive/** | orchestrator_hive | builder, planner, integrator, quickwin, refactor |
| **research/** | orchestrator_research | data, links, diag, citations, fetcher, searcher |
| **datavis/** | orchestrator_datavis | color, data, math, story, viz |
| **games/** | orchestrator_games | game, gamedev, godot |
| **corpus/** | orchestrator_corpus | corpus, corpus_ux |
| **web/** | orchestrator_web | flask, express |
| **python/** | orchestrator_python | pycli |
| **standalone/** | (none) | api, scalpel, dashboard, canary, janitor, docs, git, todoist |
| **system/** | (none) | help, onboard, diag |

## Packaged Skills (37)

Skills are built from agent definitions and installed to `~/.claude/skills/`.

**Orchestrator skills** include the orchestrator SKILL.md plus individual agent .md files in an `agents/` subdirectory.

**Standalone skills** contain a single SKILL.md derived from the agent definition.

Run `python3 skills/package_all_skills.py && bash skills/rebuild-zips.sh` to rebuild after editing agents.

## Publishing

### To PyPI
```bash
python -m build
twine upload dist/*
```

### To Claude Marketplace
Push to GitHub - plugins are auto-discovered from `.claude-plugin/plugin.json`.

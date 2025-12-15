# Geepers Package

Multi-agent orchestration system combining MCP tools and Claude Code plugin agents.

## Consolidated Structure

```
~/geepers/                     # THE canonical geepers location
├── agents/                    # 50+ markdown agent definitions
│   ├── master/                # conductor_geepers (top-level orchestrator)
│   ├── product/               # business_plan, prd, fullstack_dev, intern_pool, code_checker, docs
│   ├── checkpoint/            # scout, repo, status, snippets, janitor
│   ├── deploy/                # caddy, services, validator, canary
│   ├── quality/               # a11y, perf, api, deps, critic
│   ├── research/              # data, links, diag, citations, swarm_research
│   ├── fullstack/             # db, design, react
│   ├── games/                 # game, gamedev, godot
│   ├── corpus/                # corpus, corpus_ux
│   ├── web/                   # flask
│   ├── python/                # pycli
│   ├── standalone/            # scalpel, dashboard, canary, janitor
│   └── system/                # help, onboard, diag
├── geepers/                   # Python package
│   ├── mcp/ → ~/shared/mcp/   # Symlink to shared MCP server
│   ├── orchestrators/         # Workflow orchestration
│   └── parser/                # Agent markdown parser
├── .claude-plugin/            # Claude marketplace manifest
├── pyproject.toml             # PyPI package config
└── README.md

~/geepers_agents → ~/geepers/agents/   # Symlink for compatibility
~/.mcp.json                            # Points to ~/start-mcp-server
~/start-mcp-server                     # STDIO bridge → ~/shared/mcp/UnifiedMCPServer
~/shared/mcp/                          # Actual MCP server code
```

## Key Symlinks

| Symlink | Target | Purpose |
|---------|--------|---------|
| `~/geepers_agents` | `~/geepers/agents/` | Backward compatibility |
| `~/geepers/geepers/mcp/` | `~/shared/mcp/` | Avoid MCP code duplication |

## Archived (in ~/archive/)

- `dreamwalker-mcp/` - Original MCP project (superseded)
- `geepers-orchestrators/` - Old agent repo (merged into geepers)
- `orchestrator_snippets/` - Old orchestrator code

## Key Commands

```bash
# Install in dev mode
pip install -e .

# Test imports
python -c "from geepers import ConfigManager"

# Run MCP server (what Claude Code uses)
~/start-mcp-server
```

## Agent Categories (50+ agents)

| Category | Orchestrator | Agents |
|----------|--------------|--------|
| **master/** | conductor_geepers | Routes to all other agents |
| **product/** | orchestrator_product | business_plan, prd, fullstack_dev, intern_pool, code_checker, docs |
| **checkpoint/** | orchestrator_checkpoint | scout, repo, status, snippets, janitor |
| **deploy/** | orchestrator_deploy | caddy, services, validator, canary |
| **quality/** | orchestrator_quality | a11y, perf, api, deps, critic |
| **research/** | orchestrator_research | data, links, diag, citations, swarm_research |
| **fullstack/** | orchestrator_fullstack | db, design, react |
| **games/** | orchestrator_games | game, gamedev, godot |
| **corpus/** | orchestrator_corpus | corpus, corpus_ux |
| **web/** | orchestrator_web | flask |
| **python/** | orchestrator_python | pycli |

## Publishing

### To PyPI
```bash
python -m build
twine upload dist/*
```

### To Claude Marketplace
Push to GitHub - plugins are auto-discovered from `.claude-plugin/plugin.json`.

# Geepers

Multi-agent orchestration system with specialized Claude Code plugin agents.

## Installation

### As Claude Code Plugin (agents)
```bash
/plugin add lukeslp/geepers
```

## What's Included

### 63 Specialized Agents

Markdown-defined agents for Claude Code that provide specialized workflows:

| Category | Agents | Purpose |
|----------|--------|---------|
| **Master** | conductor_geepers | Intelligent routing to specialists |
| **Checkpoint** | scout, repo, status, snippets, orchestrator | Session maintenance |
| **Deploy** | caddy, services, validator, orchestrator | Infrastructure |
| **Quality** | a11y, perf, api, deps, critic, security, testing, orchestrator | Code audits |
| **Frontend** | css, design, motion, typescript, uxpert, webperf, orchestrator | UI/UX development |
| **Fullstack** | db, react, orchestrator | End-to-end features |
| **Hive** | builder, planner, integrator, quickwin, refactor, orchestrator | Task execution |
| **Research** | data, links, diag, citations, fetcher, searcher, orchestrator | Data gathering |
| **Games** | game, gamedev, godot, orchestrator | Game development |
| **Corpus** | corpus, corpus_ux, orchestrator | Linguistics/NLP |
| **Web** | flask, express, orchestrator | Web applications |
| **Python** | pycli, orchestrator | Python projects |
| **Standalone** | api, scalpel, dashboard, canary, janitor, docs, git | Specialized tasks |
| **System** | help, onboard, diag | System utilities |

## Related: MCP-Dreamwalker

For programmatic orchestration with LLM providers and data clients, see [MCP-Dreamwalker](https://github.com/lukeslp/mcp-dreamwalker):

- **Dream Cascade** - Hierarchical 3-tier research orchestration
- **Dream Swarm** - Multi-domain parallel search
- **12 LLM Providers** - Anthropic, OpenAI, xAI, Gemini, Mistral, Cohere, etc.
- **17 Data Clients** - Census, arXiv, GitHub, NASA, Wikipedia, etc.

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
- `conductor_geepers` - Master router
- `geepers_orchestrator_frontend` - CSS, React, design, motion
- `geepers_orchestrator_fullstack` - Backend + frontend
- `geepers_orchestrator_hive` - Build from plans and TODOs
- `geepers_orchestrator_quality` - Audits and reviews
- `geepers_orchestrator_deploy` - Infrastructure changes
- `geepers_orchestrator_checkpoint` - Session maintenance

## License

MIT License - Luke Steuber

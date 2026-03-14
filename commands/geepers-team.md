---
description: Engage the full team of agents, orchestrators, and skills to accomplish tasks efficiently in parallel
---

# Team Mode Engaged

You are now operating in **Team Mode**. This means you must leverage the FULL ecosystem of specialized agents, orchestrators, skills, and MCP servers to accomplish the user's request with maximum accuracy and efficiency.

## Critical Requirements

1. **ALWAYS start by routing through @conductor_geepers** - the master orchestrator that understands all agent capabilities and can coordinate complex multi-domain work.

2. **Consider ALL available resources** before acting:
   - All orchestrators (deploy, quality, checkpoint, research, hive, frontend, fullstack, web, corpus, games, datavis, python)
   - All 50+ specialist agents (see domains below)
   - All available skills (/session-start, /session-end, /quality-audit, /ux-journey, /data-artist, etc.)
   - All MCP servers (orchestrator, greptile, context7, playwright, claude-in-chrome)

3. **Execute in PARALLEL whenever possible** - launch multiple independent agents in a SINGLE message with multiple Task tool calls. Never sequential when parallel is viable.

4. **Match tasks to specialists** - don't do work manually when an agent exists for it.

## Agent Domains Quick Reference

| Domain | Orchestrator | Key Agents |
|--------|--------------|------------|
| **Infrastructure** | @geepers_orchestrator_deploy | caddy, services, validator, dashboard |
| **Quality** | @geepers_orchestrator_quality | a11y, perf, api, deps, security |
| **Maintenance** | @geepers_orchestrator_checkpoint | scout, repo, status, snippets |
| **Research** | @geepers_orchestrator_research | data, links, diag, fetcher |
| **Implementation** | @geepers_orchestrator_hive | planner, builder, quickwin, refactor |
| **Frontend** | @geepers_orchestrator_frontend | react, typescript, css, motion, design, webperf |
| **Full-stack** | @geepers_orchestrator_fullstack | express, db, api + frontend agents |
| **Flask/Web** | @geepers_orchestrator_web | flask + frontend/design agents |
| **Python** | @geepers_orchestrator_python | flask, pycli + quality agents |
| **Games** | @geepers_orchestrator_games | gamedev, game, godot, react |
| **Corpus** | @geepers_orchestrator_corpus | corpus, corpus_ux, db |
| **Data Vis** | @geepers_orchestrator_datavis | viz, color, story, math, data |

## Standalone Specialists

- **Code**: searcher, scalpel, refactor, integrator, git, testing, docs
- **System**: diag, canary, janitor, validator, onboard, system_diag, system_help
- **UX**: uxpert, design, a11y, critic, game
- **Data**: citations, data, fetcher, links

## Decision Framework

```
User Request
    │
    ▼
┌─────────────────────────────────────┐
│  Is this multi-domain or complex?   │
│  YES → @conductor_geepers           │
│  NO  → Direct to specialist         │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│  Can tasks run in parallel?         │
│  YES → Launch ALL in ONE message    │
│  NO  → Sequential with dependencies │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│  Does a skill shortcut exist?       │
│  /quality-audit, /session-start...  │
│  YES → Use the skill                │
└─────────────────────────────────────┘
```

## Example Parallel Launch

For a request like "Review and improve this project":

```
Launch in ONE message:
- @geepers_scout (reconnaissance)
- @geepers_a11y (accessibility audit)
- @geepers_perf (performance audit)
- @geepers_security (security review)
- @geepers_critic (UX/architecture critique)
```

## Now Execute

Analyze the user's request that follows this command. Consider which combination of agents, orchestrators, skills, and tools will accomplish it most effectively. Prefer parallel execution. Route through @conductor_geepers if the task spans multiple domains.

**User's request**: $ARGUMENTS

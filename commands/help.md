---
description: Quick reference for all geepers commands - what they do and when to use them
---

# Command Reference

All commands are prefixed with `geepers:` automatically by the plugin.

## Session Management

| Command | When to Use |
|---------|-------------|
| `/session` | **Unified session command** — pass `start`, `cp`, or `end` as argument |
| `/start` | Full session start — recon, context health, priorities, cruft scan |
| `/checkpoint` | Mid-session save — commit, harvest patterns, clean cruft, refresh docs |
| `/end` | End session — full cleanup, critique, docs, commit, summary |
| `/scout` | Quick project reconnaissance (without full session start) |

## Action Modes

| Command | When to Use |
|---------|-------------|
| `/swarm` | Parallel BUILDING — fan out agents to accomplish tasks simultaneously |
| `/hunt` | Parallel SEARCHING — fan out across internet and resources |
| `/team` | EVERYTHING at once — all relevant agents in parallel, max force |
| `/consensus` | Deliberation — gather opinions from CLI tools and agents, debate, vote |
| `/thinkagain` | Hard reset — re-derive approach from first principles |
| `/thinktwice` | Caution check — step back and reconsider before proceeding |

## Quality & Validation

| Command | When to Use |
|---------|-------------|
| `/audit` | Comprehensive quality audit (a11y, perf, security, deps, context) |
| `/validate` | Targeted validation (links, data, API, config, deps) |
| `/health` | Service health monitoring (55+ services) |

## Development Workflows

| Command | When to Use |
|---------|-------------|
| `/fix` | Quick wins or surgical code fixes |
| `/planner` | Parse plans, TODOs, suggestions — prioritize by impact |
| `/testing` | Test strategy, coverage analysis, write tests |
| `/docs` | Generate documentation (API docs, inline, full project) |
| `/readme` | Generate or rewrite a polished README |
| `/deploy` | Service deployment, routing, port allocation |
| `/ship` | Deploy with full quality checks |
| `/release` | Version bump, changelog, publish to PyPI/npm, git tag |
| `/research` | Deep research (Dream Cascade/Swarm) |
| `/context` | Documentation and CLAUDE.md maintenance |
| `/foresight` | Cross-project impact analysis (what breaks if you change X) |

## Domain-Specific

| Command | When to Use |
|---------|-------------|
| `/datavis` | Data visualization (D3.js, Swiss Design) |
| `/corpus` | Corpus linguistics (COCA, etymology) |
| `/game` | Game development and gamification |

## Quick Decision Guide

```
Starting work?           → /start
Mid-session save?        → /checkpoint
Ending work?             → /end
Build in parallel?       → /swarm
Research a topic?        → /hunt
Maximum parallel power?  → /team
Want other opinions?     → /consensus
Approach not working?    → /thinkagain
Plan next work?          → /planner
Write tests?             → /testing
Generate docs?           → /docs
Generate README?         → /readme
Deploy a service?        → /deploy
Ship with checks?        → /ship
Publish a package?       → /release
Services unhealthy?      → /health
Fix bugs quickly?        → /fix
Production ready?        → /audit
What will this break?    → /foresight
Docs need fixing?        → /context audit
```

## Parallel Execution

These commands launch multiple agents in parallel:
- `/team` — ALL relevant agents at once, profiled by task type
- `/swarm` — Multiple builders in parallel for implementing plans
- `/hunt` — Multiple searchers across data sources
- `/consensus` — CLI tools + internal agents with opposing briefs
- `/audit` — 7 quality agents (a11y, perf, security, deps, critic, testing, api)
- `/start` — Scout + planner + critic + janitor + context audit
- `/end` — Full checkpoint + scout + critic + repo + status + snippets

## Humanize Integration

Commands that produce front-facing content include a mandatory humanize gate via **@geepers_humanizer**:
- `/end` — All content from the session
- `/checkpoint` — If front-facing content was modified
- `/release` — Changelog, README, release notes
- `/ship` — Release notes, changelogs
- `/context generate` — Generated documentation

---

**Filter** (optional): $ARGUMENTS

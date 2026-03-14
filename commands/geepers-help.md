---
description: Quick reference for all geepers commands - what they do and when to use them
---

# Geepers Command Reference

## Session Management

| Command | When to Use |
|---------|-------------|
| `/geepers-session` | **Unified session command** — pass `start`, `cp`, or `end` as argument |
| `/geepers-start` | Full session start — recon, context health, priorities, cruft scan |
| `/geepers-checkpoint` | Mid-session save — commit, harvest patterns, clean cruft, refresh docs |
| `/geepers-end` | End session — full cleanup, critique, docs, commit, summary |
| `/geepers-scout` | Quick project reconnaissance (without full session start) |

## Action Modes

| Command | When to Use |
|---------|-------------|
| `/geepers-swarm` | Parallel BUILDING — fan out agents to accomplish tasks simultaneously |
| `/geepers-hunt` | Parallel SEARCHING — fan out across internet and resources |
| `/geepers-team` | EVERYTHING at once — all relevant agents in parallel, max force |
| `/geepers-consensus` | Deliberation — gather opinions from CLI tools and agents, debate, vote |
| `/geepers-thinkagain` | Hard reset — re-derive approach from first principles |
| `/geepers-thinktwice` | Caution check — step back and reconsider before proceeding |

## Quality & Validation

| Command | When to Use |
|---------|-------------|
| `/geepers-audit` | Comprehensive quality audit (a11y, perf, security, deps, context) |
| `/geepers-validate` | Targeted validation (links, data, API, config, deps) |
| `/geepers-health` | Service health monitoring (55+ services) |

## Development Workflows

| Command | When to Use |
|---------|-------------|
| `/geepers-fix` | Quick wins or surgical code fixes |
| `/geepers-ship` | Deploy with safety checks |
| `/geepers-release` | Version bump, changelog, publish to PyPI/npm, git tag |
| `/geepers-research` | Deep research (Dream Cascade/Swarm) |
| `/geepers-context` | Documentation and CLAUDE.md maintenance |
| `/geepers-foresight` | Cross-project impact analysis (what breaks if you change X) |

## Domain-Specific

| Command | When to Use |
|---------|-------------|
| `/geepers-datavis` | Data visualization (D3.js, Swiss Design) |
| `/geepers-corpus` | Corpus linguistics (COCA, etymology) |
| `/geepers-game` | Game development and gamification |

## Quick Decision Guide

```
Starting work?           → /geepers-start
Mid-session save?        → /geepers-checkpoint
Ending work?             → /geepers-end
Build in parallel?       → /geepers-swarm
Research a topic?        → /geepers-hunt
Maximum parallel power?  → /geepers-team
Want other opinions?     → /geepers-consensus
Approach not working?    → /geepers-thinkagain
Deploy something?        → /geepers-ship
Publish a package?       → /geepers-release
Services unhealthy?      → /geepers-health
Fix bugs quickly?        → /geepers-fix
Production ready?        → /geepers-audit
What will this break?    → /geepers-foresight
Docs need fixing?        → /geepers-context audit
```

## Parallel Execution

These commands launch multiple agents in parallel:
- `/geepers-team` — ALL relevant agents at once, profiled by task type
- `/geepers-swarm` — Multiple builders in parallel for implementing plans
- `/geepers-hunt` — Multiple searchers across data sources
- `/geepers-consensus` — CLI tools + internal agents with opposing briefs
- `/geepers-audit` — 7 quality agents (a11y, perf, security, deps, critic, testing, api)
- `/geepers-start` — Scout + planner + critic + janitor + context audit
- `/geepers-end` — Full checkpoint + scout + critic + repo + status + snippets

## Humanize Integration

Commands that produce front-facing content include a mandatory humanize gate via **@geepers_humanizer**:
- `/geepers-end` — All content from the session
- `/geepers-checkpoint` — If front-facing content was modified
- `/geepers-release` — Changelog, README, release notes
- `/geepers-ship` — Release notes, changelogs
- `/geepers-context generate` — Generated documentation

---

**Filter** (optional): $ARGUMENTS

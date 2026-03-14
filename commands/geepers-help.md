---
description: Quick reference for all geepers commands - what they do and when to use them
---

# Geepers Command Reference

## Session Management

| Command | When to Use |
|---------|-------------|
| `/geepers-session` | **Unified session command** — pass `start`, `cp`, or `end` as argument |
| `/geepers-scout` | Quick project reconnaissance |
| `/geepers-todo` | Todoist integration, task capture |

## Full Swarm & Multi-LLM

| Command | When to Use |
|---------|-------------|
| `/swarm` | Launch ALL relevant agents in parallel - maximum force |
| `/second-opinion` | Get Codex + Gemini + Grok perspectives on a task |

## Quality & Validation

| Command | When to Use |
|---------|-------------|
| `/geepers-audit` | Comprehensive quality audit (a11y, perf, security, deps, context) |
| `/geepers-validate` | Targeted validation (links, data, API, config, deps) |
| `/geepers-health` | Service health monitoring (55+ services) |

## Development Workflows

| Command | When to Use |
|---------|-------------|
| `/geepers-team` | Complex multi-domain tasks (full ecosystem) |
| `/geepers-fix` | Quick wins or surgical code fixes |
| `/geepers-ship` | Deploy with safety checks |
| `/geepers-release` | Version bump, changelog, publish to PyPI/npm, git tag |
| `/geepers-reuse` | Check for existing code before building |
| `/geepers-research` | Deep research (Dream Cascade/Swarm) |
| `/geepers-context` | Documentation and CLAUDE.md maintenance |
| `/geepers-foresight` | Cross-project impact analysis (what breaks if you change X) |
| `/geepers-thinktwice` | Step back and reconsider your approach |

## Domain-Specific

| Command | When to Use |
|---------|-------------|
| `/geepers-bluesky` | Bluesky ecosystem (firehose, skymarshal, etc.) |
| `/geepers-datavis` | Data visualization (D3.js, Swiss Design) |
| `/geepers-corpus` | Corpus linguistics (COCA, etymology) |
| `/geepers-game` | Game development and gamification |

## Quick Decision Guide

```
Starting work?           → /geepers-session start
Mid-session save?        → /geepers-session cp
Ending work?             → /geepers-session end
What should I work on?   → /geepers-scout
Complex task?            → /geepers-team OR /swarm
Maximum parallel power?  → /swarm
Want other LLM opinions? → /second-opinion
Deploy something?        → /geepers-ship
Publish a package?       → /geepers-release
Services unhealthy?      → /geepers-health
Check if code exists?    → /geepers-reuse
Fix bugs quickly?        → /geepers-fix
Production ready?        → /geepers-audit
Research a topic?        → /geepers-research
What will this break?    → /geepers-foresight
Approach not working?    → /geepers-thinktwice
Docs need fixing?        → /geepers-context audit
```

## Parallel Execution

These commands launch multiple agents in parallel:
- `/swarm` - Maximum parallel deployment - ALL relevant agents at once
- `/second-opinion` - Codex + Gemini + Grok CLIs simultaneously
- `/geepers-team` - Routes through conductor
- `/geepers-audit` - 7 quality agents (including context audit)
- `/geepers-session start` - Scout + planner + git + context audit
- `/geepers-session end` - Checkpoint orchestrator (scout + repo + status + snippets)
- `/geepers-validate all` - All validators
- `/geepers-health audit` - Health + diag + canary
- `/geepers-release` - Validator + testing + deps + security
- `/geepers-foresight` - Parallel dependency scans across projects

## Humanize Integration

Commands that produce front-facing content include a mandatory humanize gate:
- `/geepers-session end` - All content from the session
- `/geepers-session cp` - If front-facing content was modified
- `/geepers-release` - Changelog, README, release notes
- `/geepers-ship` - Release notes, changelogs
- `/geepers-context generate` - Generated documentation

---

**Filter** (optional): $ARGUMENTS

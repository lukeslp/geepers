# Geepers Agent Quick Reference

**Fast lookup table**: Task Type → Agent(s) to launch

Use this table BEFORE calling `geepers_conductor`. If your task is in here, launch the agent directly.

---

## Planning & Prioritization

| Task | Primary Agent | Secondary | When to Use |
|------|---|---|---|
| "What should I work on?" | **geepers_planner** | geepers_scout | >10 tasks exist; session planning |
| "What's wrong here?" | **geepers_scout** | geepers_critic | Quick code health scan |
| "Is this architecture good?" | **geepers_critic** | — | UX/design/tech debt assessment |

---

## Implementation

| Task | Primary Agent | Secondary | When to Use |
|------|---|---|---|
| "Build this feature" | **geepers_builder** | geepers_planner | After tasks are prioritized |
| "Quick win/easy fix" | **geepers_quickwin** | geepers_scout | Typos, dead code, missing attrs |
| "Refactor this code" | **geepers_refactor** | geepers_scalpel | <500 lines; complex → use Scalpel |
| "Edit complex file" | **geepers_scalpel** | — | Files >200 lines; intricate dependencies |
| "Bulk change (20+ files)" | **geepers_scalpel** | — | Regex ops across multiple files |

---

## Quality & Testing

| Task | Primary Agent | Secondary | When to Use |
|------|---|---|---|
| "Check accessibility" | **geepers_a11y** | geepers_scout | WCAG compliance, missing alt/aria |
| "Optimize performance" | **geepers_perf** | geepers_diag | Profiling, bottleneck detection |
| "Security audit" | **geepers_security** | geepers_deps | OWASP, vulnerability scan |
| "Test coverage" | **geepers_testing** | geepers_critic | Coverage analysis, test design |
| "Full code review" | **geepers_orchestrator_quality** | — | Comprehensive quality sweep |

---

## Debugging & Diagnostics

| Task | Primary Agent | Secondary | When to Use |
|------|---|---|---|
| "Service is down" | **geepers_diag** | geepers_services | Root cause analysis + repair |
| "Performance degraded" | **geepers_diag** | geepers_perf | System logs, resource check |
| "Weird error happening" | **geepers_diag** | geepers_scalpel | Log analysis → surgical fix |
| "Quick health check" | **geepers_canary** | geepers_diag | Fast status; deep dive if issues |

---

## Infrastructure & Deployment

| Task | Primary Agent | Secondary | When to Use |
|------|---|---|---|
| "Deploy code" | **geepers_orchestrator_deploy** | geepers_validator | Infrastructure changes |
| "Update Caddy routing" | **geepers_caddy** | geepers_validator | Reverse proxy configuration |
| "Manage services" | **geepers_services** | geepers_canary | Start/stop/restart services |
| "System diagnostics" | **geepers_system_diag** | geepers_diag | Full system health check |

---

## By Project Type

| Tech Stack | Primary Orchestrator | Use When |
|---|---|---|
| **Flask web app** | **geepers_orchestrator_web** | Python backend + React/HTML frontend |
| **Node.js / Express** | **geepers_orchestrator_fullstack** | JavaScript backend + frontend |
| **Frontend only (no backend)** | **geepers_orchestrator_frontend** | React, Vue, pure JavaScript |
| **Python project (CLI/tool)** | **geepers_orchestrator_python** | Click, typer, argparse apps |
| **Game development** | **geepers_orchestrator_games** | Godot, game logic, gamification |
| **Linguistics / NLP** | **geepers_orchestrator_corpus** | Corpus analysis, KWIC, concordance |

---

## Session Management

| Task | Primary Agent | Secondary | When to Use |
|---|---|---|---|
| **Session start** | **geepers_scout** + **geepers_planner** (parallel) | — | Always start sessions this way |
| **Session end** | **geepers_orchestrator_checkpoint** | — | Wrap up, document, save state |
| **Clean up old files** | **geepers_janitor** | geepers_scout | Aggressive cleanup |
| **Git hygiene** | **geepers_repo** | — | Merge conflicts, branch cleanup |

---

## Special Purpose

| Task | Primary Agent | Secondary | When to Use |
|---|---|---|---|
| "Verify no regressions" | **geepers_integrator** | — | After multi-file implementation |
| "Extract reusable patterns" | **geepers_snippets** | — | After major features complete |
| "Document code" | **geepers_docs** | geepers_snippets | README, API docs, guides |
| "Generate insights/report" | **geepers_scout** | geepers_snippets | After significant work |

---

## When to Use geepers_conductor

| Situation | Action |
|---|---|
| **Task clearly maps to table above** | Skip conductor, call agent directly |
| **Task crosses multiple domains** | Use conductor for routing |
| **Unsure which orchestrator** | Use conductor to figure it out |
| **Starting major session** | Consider using conductor for full assessment |

**Recommendation**: 80% of tasks should skip conductor and go direct.

---

## Anti-Patterns

### ❌ DON'T do these

```
"Check accessibility" → geepers_conductor → geepers_a11y
(Skip conductor, go direct to geepers_a11y)

"Quick fixes" → geepers_conductor → geepers_quickwin
(Skip conductor, go direct to geepers_quickwin)

"Performance problem" → geepers_conductor → geepers_diag
(Skip conductor, go direct to geepers_diag)
```

### ✅ DO this instead

```
"Check accessibility" → geepers_a11y
"Quick fixes" → geepers_quickwin
"Performance problem" → geepers_diag
```

---

## Quick Decision Tree

```
What do I need?

├─ To decide WHAT to work on
│  └─ geepers_planner
│
├─ To implement something
│  ├─ Quick fix (<30 min)
│  │  └─ geepers_quickwin
│  ├─ Feature (multi-file)
│  │  └─ geepers_builder (after geepers_planner)
│  └─ Complex code edit
│     └─ geepers_scalpel
│
├─ To check code quality
│  ├─ Quick scan
│  │  └─ geepers_scout
│  ├─ Accessibility issues
│  │  └─ geepers_a11y
│  ├─ Performance problems
│  │  └─ geepers_perf
│  └─ Full audit
│     └─ geepers_orchestrator_quality
│
├─ To debug something
│  ├─ Service is broken
│  │  └─ geepers_diag
│  ├─ Error in logs
│  │  └─ geepers_diag
│  └─ Quick health check
│     └─ geepers_canary
│
├─ To deploy/configure
│  ├─ Deploy code
│  │  └─ geepers_orchestrator_deploy
│  ├─ Update Caddy
│  │  └─ geepers_caddy
│  └─ Service management
│     └─ geepers_services
│
├─ Starting/ending session
│  ├─ Session start
│  │  └─ geepers_scout + geepers_planner (parallel)
│  └─ Session end
│     └─ geepers_orchestrator_checkpoint
│
└─ Still unsure?
   └─ geepers_conductor
```

---

## Pro Tips

### Tip 1: Plan Before You Code
Always run planner first if you have multiple tasks:
```
geepers_planner → geepers_builder → geepers_integrator
```

### Tip 2: Diagnose Before Guessing
When something breaks, diagnose first:
```
geepers_diag → [identify root cause] → geepers_scalpel
```

### Tip 3: Use Scalpel for Large Files
Always use scalpel for files >200 lines:
```
geepers_scalpel (instead of manual edits)
```

### Tip 4: Parallel Agents at Session Start
Get faster context with parallel initial scan:
```
geepers_scout + geepers_planner (run together)
```

### Tip 5: Verify After Multi-File Changes
Always check for integration issues after large changes:
```
geepers_builder → geepers_integrator → [commit]
```

---

## Last Updated

2026-01-05 (based on comprehensive agent system audit)

For full analysis, see: `/home/coolhand/geepers/reports/agent-optimization-analysis.md`

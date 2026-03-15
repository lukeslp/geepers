---
description: Parse plans, TODOs, and suggestions - prioritize tasks by impact and effort
---

# Planner Mode

Analyze existing plans, TODOs, and suggestions to identify the highest-value work.

## Execute

Launch **@geepers_planner** to:

1. Parse `PROJECT_PLAN.md`, `SUGGESTIONS.md`, `TODO.md`, and inline TODOs/FIXMEs
2. Read `~/geepers/recommendations/by-project/<project>.md` for prior recommendations
3. Prioritize tasks by impact vs effort
4. Produce a ranked task queue

## What It Scans

- `PROJECT_PLAN.md`, `IMPLEMENTATION_PLAN.md` — structured plans
- `SUGGESTIONS.md`, `RECOMMENDATIONS.md` — improvement ideas
- `TODO.md`, `TODO` — task lists
- Inline `TODO`, `FIXME`, `HACK`, `XXX` comments in code
- `CLAUDE.md` — project-specific guidance and known issues
- `~/geepers/recommendations/by-project/` — agent-generated recommendations

## Output

A prioritized task queue with:
- Task description
- Impact estimate (high/medium/low)
- Effort estimate (quick/moderate/large)
- Suggested agent to handle it
- Dependencies on other tasks

## Follow-up

After planning, execute with:
- `/fix` — quick wins from the queue
- `/swarm` — parallel execution of independent tasks
- **@geepers_builder** — work through tasks sequentially
- **@geepers_orchestrator_hive** — coordinate building from the plan

## Cross-References

- Quick reconnaissance: `/scout` (includes planner)
- Session start: `/start` (includes planner)
- Implementation: `/swarm` (parallel execution)

**Focus area** (optional): $ARGUMENTS

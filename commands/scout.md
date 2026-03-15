---
description: Quick project reconnaissance - understand current state, find issues, identify quick wins
---

# Scout Mode

Run a fast reconnaissance sweep of the current project to understand its state and identify opportunities.

## Execute in PARALLEL

Launch these agents simultaneously:

1. **@geepers_scout** - Primary reconnaissance:
   - Analyze project structure and architecture
   - Identify code quality issues and quick fixes
   - Check for uncommitted changes and git hygiene
   - Find TODOs, FIXMEs, and technical debt
   - Generate an actionable report

2. **@geepers_planner** - Task planning:
   - Parse existing PROJECT_PLAN.md, SUGGESTIONS.md, TODO files
   - Prioritize tasks by impact and effort
   - Identify highest-value work

## Also Check

- `~/geepers/recommendations/by-project/<project>.md` - Existing recommendations
- Project's CLAUDE.md - Project-specific guidance
- Recent git commits - Context on recent work

## Cross-References

- Session lifecycle: `/session` (start, cp, end)
- Deeper audit: `/audit`
- Quick fixes: `/fix`

**Focus area** (optional): $ARGUMENTS

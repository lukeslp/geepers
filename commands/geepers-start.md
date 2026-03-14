---
description: Start a full work session - reconnaissance agents, recommendations, context audit, task prioritization
---

# Session Start

Full session initialization with parallel reconnaissance agents, recommendations loading, context health check, and conversation naming.

This is a self-contained version of `/geepers-session start`. Either command produces the same workflow.

## Execute ALL of These in PARALLEL

### 1. Check Recommendations
```
~/geepers/recommendations/by-project/<project-name>.md
```
Load any existing recommendations from previous sessions. Derive `<project-name>` from the current working directory basename.

### 2. Reconnaissance Agents (PARALLEL — launch in the SAME message)
- **@geepers_scout** - Project state, quick wins, code quality issues, technical debt, TODOs/FIXMEs
- **@geepers_planner** - Parse existing plans (PROJECT_PLAN.md, TODO files, SUGGESTIONS.md), prioritize tasks by impact and effort

### 3. Git State
- `git status` — check for uncommitted changes (warn if significant)
- `git log --oneline -5` — review recent commits for context
- `git diff --stat` — see what's changed since last commit

### 4. Project Context
- Load project CLAUDE.md if present
- Check for PROJECT_PLAN.md, TODO.md, SUGGESTIONS.md
- Note key files: requirements.txt, package.json, pyproject.toml, Makefile, start.sh
- Check for venv/node_modules presence

### 5. Context Audit (BACKGROUND agent)
Launch `/geepers-context audit` as a **background** agent:
- Runs `~/scripts/validate-claude-nav.sh` (nav headers + parent refs)
- Checks for missing CLAUDE.md in new directories
- Flags stale references and cruft files (SUGGESTIONS.md, CRITIC.md, ONBOARD.md, *_STATUS.md, temp_*)
- Creates CLAUDE.md from template if missing

## Output

After all parallel agents complete, present a concise session briefing:

```
Session Start: <project>
---
Git: <branch> | <uncommitted count> uncommitted changes
Recent: <last 3 commits summary>
Recommendations: <count> pending items
Quick Wins: <from scout>
Priority Tasks: <from planner>
CLAUDE.md: <healthy | needs update | missing>
```

## Name This Conversation

Run `/rename` with format: `<project>: <topic>` based on top priority task identified by planner/scout.

## When to Use

- Starting a dedicated work session on a project
- Picking up a project after time away
- When you need full awareness of project health, priorities, and opportunities

For a faster start without agents, use `/init` instead.

## Cross-References

- Quick init (no agents): `/init`
- Canonical lifecycle: `/geepers-session` (start, cp, end — all three modes)
- Mid-session save: `/geepers-checkpoint` or `/geepers-session cp`
- End session: `/geepers-end` or `/geepers-session end`
- Context health: `/geepers-context`
- Quick recon only: `/geepers-scout`
- Deeper audit: `/geepers-audit`
- Deploy after session: `/geepers-ship`
- Impact analysis: `/geepers-foresight`
- Capture tasks to Todoist: `/geepers-todo wrap`
- Full reference: `~/admin/workflow.html`

## Target

**Project/directory**: $ARGUMENTS

If no arguments, use current working directory.

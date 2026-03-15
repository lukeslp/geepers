---
description: Start a work session - full recon, context health, priorities, cruft scan
---

# Session Start

Full session initialization with parallel reconnaissance, context health check, and cruft scan.

## Execute ALL Steps

### 1. Git State

Run in parallel:
```bash
git status
git log --oneline -5
git diff --stat
git remote show origin 2>/dev/null | head -5
```

Check for uncommitted changes (warn if significant). Note if local is ahead/behind remote.

### 2. Load Context

- Read project CLAUDE.md if present
- Check for PROJECT_PLAN.md, TODO.md, SUGGESTIONS.md
- Load recommendations: `~/geepers/recommendations/by-project/<project-name>.md`

### 3. Parallel Recon (launch ALL in the SAME message)

- **@geepers_scout** — Project state, quick wins, TODOs/FIXMEs, tech debt, code quality
- **@geepers_planner** — Parse existing plans (PROJECT_PLAN.md, TODO files), prioritize tasks by impact and effort
- **@geepers_critic** — Architectural critique, identify friction points and design concerns early

### 4. Context Health (background)

Launch `/context audit` as a **background** agent:
- Validate CLAUDE.md navigation headers and parent refs
- Check for missing CLAUDE.md in new directories
- Flag stale references and cruft files

### 5. Cruft Scan

Launch **@geepers_janitor** in report-only mode:
- Identify temp files, agent artifacts (SUGGESTIONS.md, CRITIC.md, ONBOARD.md, *_STATUS.md, temp_*)
- Dead code, unused imports
- Do NOT delete yet — just report findings

### 6. Present Briefing

After all agents complete, present:
```
Session Start: <project>
---
Git: <branch> | <uncommitted count> uncommitted | <ahead/behind remote>
Recent: <last 3 commits summary>

Recommendations: <count> pending items
Quick Wins: <from scout>
Priority Tasks: <from planner>
Design Concerns: <from critic>
Cruft Found: <from janitor>
CLAUDE.md: <healthy | needs update | missing>
```

## Cross-References

- Mid-session save: `/checkpoint`
- End session: `/end`
- Unified lifecycle: `/session`
- Context health: `/context`
- Quick recon only: `/scout`
- Full audit: `/audit`

## Target

**Project/directory**: $ARGUMENTS

If no arguments, use current working directory.

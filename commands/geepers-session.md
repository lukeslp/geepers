---
description: Start, checkpoint, or end a work session - checks recommendations, git status, launches scout + planner
---

# Session Management

Unified session lifecycle command. Replaces `/geepers-start`, `/geepers-checkpoint`, `/geepers-end`.

## Session Start

Execute ALL of these in PARALLEL:

### 1. Check Recommendations
```
~/geepers/recommendations/by-project/<project-name>.md
```
Load any existing recommendations from previous sessions.

### 2. Reconnaissance Agents (parallel)
- **@geepers_scout** - Project state, quick wins, issues
- **@geepers_planner** - Parse existing plans, prioritize tasks

### 3. Git State
- Check for uncommitted changes (warn if significant)
- Review recent commits for context
- `git log --oneline -5` for recent activity

### 4. Project Context
- Load project CLAUDE.md if present
- Check for PROJECT_PLAN.md, TODO files

### 5. Context Audit (background agent)
Launch `/geepers-context audit` as a background agent:
- Runs `~/scripts/validate-claude-nav.sh` (nav headers + parent refs)
- Checks for missing CLAUDE.md in new directories
- Flags stale references and cruft files
- Creates CLAUDE.md from template if missing

### 6. Output
Present a concise session briefing:
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

### 7. Name This Conversation
Run `/rename` with format: `<project>: <topic>` based on top priority task.

---

## Checkpoint

Lightweight mid-session save point. Use when switching tasks, after completing a feature, or every 1-1.5 hours.

### 1. Commit Current Work
- `git status` + `git diff --stat` to review changes
- `git log --oneline -3` to verify latest commit is expected (no surprise agent commits)
- Stage and commit with descriptive message (prefix: `checkpoint:`)

### 2. Context Audit (if structural changes)
If files/dirs were added or removed since last checkpoint:
- Run `/geepers-context audit` as background agent (nav validation + staleness check)
- Skip if no structural changes

### 3. Log Progress
Brief note:
- What was completed since last checkpoint
- What's next

### 4. Pattern Harvest (optional)
If a reusable pattern was implemented this checkpoint:
- Launch **@geepers_snippets** to harvest it before context is lost

### 5. Humanize Gate
If any front-facing content was modified (docs, READMEs, public comments):
- Run `/humanize` on changed files

### 6. Context Update (if needed)
If context audit flagged issues, run `/geepers-context update` to fix them.

### 7. Name This Conversation
Run `/rename` with format: `<project>: <what's been done / what's in progress>`.

---

## Session End

Wrap up a work session cleanly. Commits work, documents progress, harvests reusable patterns.

### 1. Checkpoint Orchestrator
Launch **@geepers_orchestrator_checkpoint** which coordinates:
- **@geepers_scout** - Final sweep for loose ends
- **@geepers_repo** - Git hygiene, ensure all work committed
- **@geepers_status** - Log accomplishments
- **@geepers_snippets** - Harvest reusable patterns from this session

### 2. Context Audit
Launch `/geepers-context audit` as a background agent:
- Runs `~/scripts/validate-claude-nav.sh` (nav headers + parent refs)
- Checks for missing CLAUDE.md in new directories
- Flags stale references and cruft files
- If issues found, run `/geepers-context update` to fix them

### 3. Session Summary
Create a concise summary:
```
Session End: <project>
---
Accomplished:
- <what was done>

Commits: <count> new commits
Files changed: <count>

Open Items:
- <what's left>

Blockers:
- <any blockers for next session>
```

### 4. Humanize Gate (MANDATORY)
Run `/humanize` on any front-facing content created or modified during this session:
- READMEs, documentation, changelogs
- Public-facing code comments
- Any content that will be seen by humans outside the dev environment

### 5. Name This Conversation
Run `/rename` with format: `<project>: <what was done>`.

---

## Execute

**Mode**: $ARGUMENTS

If no arguments or "start": Run session start workflow
If "checkpoint" or "save" or "cp": Run checkpoint workflow
If "end" or "wrap": Run session end workflow
If "status": Show current session state without full workflow

## Cross-References

- Context health: `/geepers-context`
- Quick recon only: `/geepers-scout`
- Deploy after session: `/geepers-ship`
- Impact analysis: `/geepers-foresight`
- Capture tasks to Todoist: `/geepers-todo wrap`
- Full reference: `~/admin/workflow.html`

## Target

**Project/directory**: $ARGUMENTS

If no arguments, use current working directory.

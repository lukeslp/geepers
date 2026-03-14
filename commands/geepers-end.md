---
description: End a work session - commit, checkpoint orchestrator, context audit, humanize gate, session summary
---

# Session End

Wrap up a work session cleanly. Commits work, documents progress, harvests reusable patterns, ensures context health.

Self-contained version of `/geepers-session end`. Either command produces the same workflow.

## Execute

### 1. Checkpoint Orchestrator
Launch **@geepers_orchestrator_checkpoint** which coordinates these agents in parallel:
- **@geepers_scout** - Final sweep for loose ends
- **@geepers_repo** - Git hygiene, ensure all work committed
- **@geepers_status** - Log accomplishments
- **@geepers_snippets** - Harvest reusable patterns from this session

### 2. Context Audit
Launch `/geepers-context audit` as a **background** agent:
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

## Cross-References

- Full session start: `/geepers-start` or `/geepers-session start`
- Quick init: `/init`
- Mid-session save: `/geepers-checkpoint` or `/geepers-session cp`
- Context health: `/geepers-context`
- Deploy after session: `/geepers-ship`
- Capture tasks to Todoist: `/geepers-todo wrap`
- Full reference: `~/admin/workflow.html`

## Target

**Project/directory**: $ARGUMENTS

If no arguments, use current working directory.

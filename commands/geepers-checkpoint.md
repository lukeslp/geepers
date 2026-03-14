---
description: Mid-session save point - commit work, log progress, harvest patterns, humanize gate
---

# Checkpoint

Lightweight mid-session save point. Use when switching tasks, after completing a feature, or every 1-1.5 hours.

Self-contained version of `/geepers-session cp`. Either command produces the same workflow.

## Execute

### 1. Commit Current Work
Run these in parallel first:
```bash
git status
git diff --stat
git log --oneline -3
```
- Verify latest commit is what you expect (no surprise agent commits)
- Verify only your intended changes are present
- Stage and commit with descriptive message (prefix: `checkpoint:`)
- Follow git safety protocol: never `git add -A` when agents are running in parallel

### 2. Context Audit (if structural changes)
If files/dirs were added or removed since last checkpoint:
- Run `/geepers-context audit` as a **background** agent (nav validation + staleness check)
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

## Cross-References

- Full session start: `/geepers-start` or `/geepers-session start`
- Quick init: `/init`
- End session: `/geepers-end` or `/geepers-session end`
- Context health: `/geepers-context`

## Target

**Project/directory**: $ARGUMENTS

If no arguments, use current working directory.

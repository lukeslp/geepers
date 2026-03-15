---
description: Mid-session save - commit, harvest patterns, clean cruft, refresh docs
---

# Checkpoint

Mid-session save point. Commits work, harvests patterns, cleans cruft, refreshes documentation.

Use when switching tasks, after completing a feature, or every 1-1.5 hours.

## Execute ALL Steps

### 1. Git Review

Run in parallel:
```bash
git status
git diff --stat
git log --oneline -3
```
- Verify latest commit is what you expect (no surprise agent commits)
- Verify only your intended changes are present

### 2. Stage and Commit

- Stage relevant files (never `git add -A` when agents are running in parallel)
- Commit with descriptive message, prefix: `checkpoint:`
- Follow git safety protocol

### 3. Parallel Maintenance (launch ALL in the SAME message)

- **@geepers_snippets** — Harvest any reusable patterns from this chunk of work before context is lost
- **@geepers_janitor** — Remove cruft: temp files, dead code, agent artifacts (SUGGESTIONS.md, CRITIC.md, ONBOARD.md, *_STATUS.md, temp_*)

### 4. Context Audit (if structural changes)

If files or directories were added or removed since last checkpoint:
- Run `/context audit` as a **background** agent
- Validates CLAUDE.md nav headers and parent refs
- Skip if no structural changes

### 5. Documentation Gate

If any front-facing content was modified (docs, READMEs, public comments):
- Launch **@geepers_humanizer** on changed files
- Removes AI writing patterns, restores human voice

### 6. CLAUDE.md Refresh

If project state changed meaningfully (new files added, features removed, architecture changed):
- Update the project CLAUDE.md to reflect current state
- Keep it factual and current — stale context is worse than no context

### 7. Progress Note

Brief summary:
- What was completed since last checkpoint
- What's next

## Cross-References

- Session start: `/start`
- End session: `/end`
- Unified lifecycle: `/session`
- Context health: `/context`

## Target

**Project/directory**: $ARGUMENTS

If no arguments, use current working directory.

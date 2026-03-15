---
description: Session lifecycle router - start, checkpoint, or end a work session
---

# Session

Unified session lifecycle command. Routes to the appropriate workflow.

## Execute

**Mode**: $ARGUMENTS

| Input | Action |
|-------|--------|
| (empty) or `start` | Run `/geepers-start` workflow |
| `checkpoint` or `cp` or `save` | Run `/geepers-checkpoint` workflow |
| `end` or `wrap` or `done` | Run `/geepers-end` workflow |
| `status` | Show current session state: git status, uncommitted changes, time since last commit |

## Quick Reference

- **Start** — Full recon, context health, priorities, cruft scan
- **Checkpoint** — Commit, harvest patterns, clean cruft, refresh docs
- **End** — Full cleanup, critique, docs, commit, session summary

## Cross-References

- `/geepers-start` — Full session start workflow
- `/geepers-checkpoint` — Mid-session save
- `/geepers-end` — End session workflow
- `/geepers-context` — Context health separately
- `/geepers-scout` — Quick recon without full session

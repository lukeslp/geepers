---
description: End session - full cleanup, critique, docs, commit, summary
---

# Session End

Button up for the night. Everything committed, documented, critiqued, and clean.

## Execute ALL Steps

### Phase 1: Full Checkpoint

Run the complete `/geepers-checkpoint` workflow first:
1. Git review (status, diff, log)
2. Stage and commit (prefix `checkpoint:`)
3. Parallel maintenance: @geepers_snippets + @geepers_janitor
4. Context audit if structural changes
5. Documentation gate via @geepers_humanizer
6. CLAUDE.md refresh if needed
7. Progress note

### Phase 2: Parallel Final Sweep (launch ALL in the SAME message)

- **@geepers_scout** — Final loose ends scan, anything missed
- **@geepers_critic** — Full architectural and UX critique of today's work
- **@geepers_repo** — Git hygiene, verify ALL work is committed, no orphaned branches
- **@geepers_status** — Log accomplishments to `~/geepers/logs/`
- **@geepers_snippets** — Final pattern harvest from the full session

### Phase 3: Mandatory Cleanup

1. **CLAUDE.md mandatory refresh** — Update project CLAUDE.md to reflect current state regardless of whether it "seems" changed. End-of-session state must be accurate.

2. **@geepers_humanizer (mandatory)** — Run on ALL front-facing content created or modified during this session:
   - READMEs, documentation, changelogs
   - Public-facing code comments
   - Any content that will be seen by humans outside the dev environment

3. **Context audit** — Full `/geepers-context audit`:
   - Validate all CLAUDE.md nav headers and parent refs
   - If issues found, fix them immediately

### Phase 4: Final Commit and Sync

1. **Final commit** — If any cleanup or documentation changes were made in Phase 3
2. **Remote sync check** — Warn if local is ahead of remote (unpushed commits)

### Phase 5: Session Summary

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

Recommendations saved: ~/geepers/recommendations/by-project/<project>.md
```

## Cross-References

- Session start: `/geepers-start`
- Mid-session save: `/geepers-checkpoint`
- Unified lifecycle: `/geepers-session`
- Context health: `/geepers-context`
- Deploy after session: `/geepers-ship`

## Target

**Project/directory**: $ARGUMENTS

If no arguments, use current working directory.

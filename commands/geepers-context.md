---
description: Maintain and sculpt project context - audit CLAUDE.md files, cross-link documentation, track open questions
---

# Context Mode

Maintain coherent project context across documentation, CLAUDE.md files, and recommendations.

Facts live in ONE place, cross-link elsewhere, track open questions explicitly.

## Context Architecture

```
~/CLAUDE.md                    # System-wide — architecture, conventions
~/CLAUDE_MAP.md                # Relationship graph — ports, deps, nested repos
~/[dir]/CLAUDE.md              # Each has nav headers:
                               #   <!-- Navigation: ~/[path]/CLAUDE.md -->
                               #   <!-- Parent: ~/[parent]/CLAUDE.md -->
                               #   <!-- Map: ~/CLAUDE_MAP.md -->

~/geepers/recommendations/by-project/<project>.md  # Agent findings
~/.claude/CLAUDE.md                                # Global instructions
```

## Workflows

### Audit Context (Default)

Check context health — run this at session start/end or standalone:

1. **Run nav validation**
   ```bash
   ~/scripts/validate-claude-nav.sh
   ```
   Checks all CLAUDE.md files have navigation headers and parent refs resolve.

2. **Check CLAUDE.md hierarchy**
   - Root `~/CLAUDE.md` + `~/CLAUDE_MAP.md`
   - Project/directory CLAUDE.md files
   - Verify nav headers present (Navigation, Parent, Map)

3. **Verify cross-references**
   - Do parent links point to files that exist?
   - Does CLAUDE_MAP.md port registry match `sm status`?
   - Are new directories missing CLAUDE.md files?

4. **Find open questions**
   - TODOs, FIXMEs, questions in docs
   - Unknowns that need resolution

5. **Check for staleness**
   - CLAUDE.md referencing dirs/files that no longer exist
   - Port numbers that don't match service_manager.py
   - Information contradicting code

6. **Clean cruft**
   - Delete any SUGGESTIONS.md, CRITIC.md, ONBOARD.md, *_STATUS.md, temp_* files found
   - These are agent artifacts, not permanent documentation

### Update Context

When structural changes were made (new dirs, removed files, new services):

1. **Run nav validation** — `~/scripts/validate-claude-nav.sh`
2. **Add nav headers** to any new CLAUDE.md files using template from `~/documentation/resources/development-patterns/claude-md-templates/`
3. **Update CLAUDE_MAP.md** if ports, services, or directory structure changed
4. **Update parent CLAUDE.md** if children were added/removed
5. **Run `claude-md-management:revise-claude-md`** for deeper content updates

### Generate Context

Bootstrap context for a new project:

1. **Create CLAUDE.md** from appropriate template (standard, server, project, or html)
2. **Add nav headers** — Navigation, Parent, Map
3. **@geepers_docs** - Generate missing documentation
4. **@geepers_scout** - Identify recommendations

## Principles

| Principle | Implementation |
|-----------|----------------|
| **One source of truth** | Each fact in ONE place; link elsewhere |
| **Nav headers everywhere** | Every CLAUDE.md links to parent and map |
| **Progressive disclosure** | Root → directory → project CLAUDE.md |
| **No orphans** | Every doc linked from somewhere |
| **Keep current** | Stale context worse than no context |

## Humanize Gate

If "generate" mode was used (creating public-facing documentation):
- Run `/humanize` on all generated docs

## Cross-References

- Session lifecycle: `/geepers-session` (start/cp/end — all trigger context audit)
- Quality audit: `/geepers-audit`
- Nav validation: `~/scripts/validate-claude-nav.sh`
- Templates: `~/documentation/resources/development-patterns/claude-md-templates/`
- System map: `~/CLAUDE_MAP.md`

## Execute

**Mode**: $ARGUMENTS

If no arguments or "audit":
- Run full context audit (nav validation + hierarchy + staleness + cruft)

If "update":
- Guide through updating context after structural changes

If "generate" or "bootstrap":
- Generate initial context for a new project

If "sync":
- Sync recommendations from ~/geepers/recommendations/ into project docs

If "validate" or "check":
- Just run ~/scripts/validate-claude-nav.sh (quick check)

## Supporting Agents

- **@geepers_validator** - Verify paths and configurations
- **@geepers_docs** - Documentation generation
- **@geepers_scout** - Project reconnaissance
- **@geepers_janitor** - Cruft cleanup

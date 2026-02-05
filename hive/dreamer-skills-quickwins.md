# Quick Wins: Dreamer-Skills Plugin

**Scan Date**: 2026-01-12
**Plugin Version**: 1.1.0
**Total Issues Found**: 10
**Quick Wins Identified**: 8
**Remaining Improvements**: 2

---

## Completed Quick Wins

*(Record completed wins as they are fixed)*

---

## Quick Wins Available (Priority Order)

### [Content] 1. Add missing related skills cross-references to session-start
**File**: `/home/coolhand/.claude/plugins/marketplaces/dreamer-skills/skills/session-start/SKILL.md`
**Line**: End of file (after Anti-Patterns section)
**Effort**: 3 minutes
**Priority**: HIGH (UX - helps users navigate)
**Impact**: Immediate visibility
**Current State**: No "Related Skills" section
**Fix**: Add section after anti-patterns listing `/session-end`, `/scout`, `/quality-audit`

```markdown
## Related Skills

- `/session-end` - Run at end of session to commit and checkpoint
- `/scout` - Quick mid-session health checks
- `/quality-audit` - Comprehensive quality review before major changes
```

---

### [Content] 2. Fix scout vs session-start comparison table terminology
**File**: `/home/coolhand/.claude/plugins/marketplaces/dreamer-skills/skills/scout/SKILL.md`
**Line**: 78-91 (comparison table)
**Effort**: 5 minutes
**Priority**: HIGH (Clarity - users often pick wrong tool)
**Impact**: Prevents confusion
**Current State**: Table shows checkmarks (✅) and X marks (❌) but description is unclear
**Fix**: Enhance table with clear guidance in caption

- Line 78: Change caption from `## Scout vs. Full Session Start` to `## When to Use Scout vs. Session Start`
- Add note: **Scout** = quick diagnosis mid-session, **Session Start** = comprehensive setup ritual at beginning
- Replace the `❌` entries in Health check row with contextual text like "(basic)" vs "(detailed)"
- Example fix at line 83:

```markdown
| Health check | Basic status | Full inventory |
```

---

### [Content] 3. Missing example usage commands for quality-audit
**File**: `/home/coolhand/.claude/plugins/marketplaces/dreamer-skills/skills/quality-audit/SKILL.md`
**Line**: After line 156 (end of document)
**Effort**: 7 minutes
**Priority**: MEDIUM (Usability - helps new users)
**Impact**: Clearer invocation patterns
**Current State**: No usage examples at end
**Fix**: Add common workflows section

```markdown
## Common Workflows

```
# Full pre-release audit
/quality-audit

# Quick accessibility check only
@geepers_a11y

# Performance-focused audit
@geepers_perf

# Security review before deployment
@geepers_security

# Dependency verification
@geepers_deps
```
```

---

### [Content] 4. Add "When NOT to use" section to data-fetch
**File**: `/home/coolhand/.claude/plugins/marketplaces/dreamer-skills/skills/data-fetch/SKILL.md`
**Line**: After line 145 (before Related Skills)
**Effort**: 5 minutes
**Priority**: MEDIUM (Clarity - prevents misuse)
**Impact**: Sets expectations
**Current State**: Only shows when to use, not when not to
**Fix**: Add anti-patterns section

```markdown
## When NOT to Use Data-Fetch

- **Real-time data only** - These sources have delays; not suitable for live dashboards
- **Proprietary APIs** - Only public/authorized APIs supported
- **Local files** - Use local file system, not this skill
- **Private databases** - Only public datasets
- **Ultra-low latency needs** - API calls have inherent delays

Use direct API clients or database queries for these cases.
```

---

### [Content] 5. Fix incomplete agent reference in ux-journey
**File**: `/home/coolhand/.claude/plugins/marketplaces/dreamer-skills/skills/ux-journey/SKILL.md`
**Line**: 61
**Effort**: 2 minutes
**Priority**: HIGH (Correctness - agent reference missing)
**Impact**: Clear agent coordination
**Current State**: `@geepers_uxpert` referenced but not defined in domain section
**Fix**: Extract and define before execution strategy (after line 60):

Add before line 61:
```markdown
### 4. Interaction Patterns & Interaction Design (@geepers_uxpert)

**Interaction Quality:**
- Navigation clarity and mental model alignment
- Form interactions and error recovery
- Loading states and feedback patterns
- Touch targets and mobile responsiveness
- State management and visual feedback
```

---

### [Content] 6. Add version compatibility notes to README
**File**: `/home/coolhand/.claude/plugins/marketplaces/dreamer-skills/README.md`
**Line**: After line 5 (Installation section)
**Effort**: 4 minutes
**Priority**: MEDIUM (Documentation - prevents issues)
**Impact**: Clarity on compatibility
**Current State**: No version info
**Fix**: Add compatibility note after installation

```markdown

## Compatibility

- **Claude Code**: v1.0+
- **dr.eamer.dev**: Required (skills reference shared library, service manager, geepers agents)
- **Geepers Agents**: 50+ agents needed for full functionality
```

---

### [Content] 7. Missing "Success Criteria" in quality-audit thresholds
**File**: `/home/coolhand/.claude/plugins/marketplaces/dreamer-skills/skills/quality-audit/SKILL.md`
**Line**: 126-133 (Quality Thresholds table)
**Effort**: 6 minutes
**Priority**: MEDIUM (Clarity - helps interpret results)
**Impact**: Clear pass/fail guidance
**Current State**: Thresholds exist but not clear what "pass" means for deployment
**Fix**: Add pre-table explanation (before line 126):

```markdown
## Quality Thresholds & Deployment Readiness

Use these thresholds to determine if code is ready for production:
- **All PASS** = Ready to deploy immediately
- **WARN in non-critical** = Deploy with monitoring; add to sprint backlog
- **FAIL in any domain** = Block deployment, fix before release
- **Critical issues** = Always blocks deployment

Thresholds:

| Domain | Pass | Warn | Fail |
...
```

---

### [Hook] 8. Add example output to pre-compact hook
**File**: `/home/coolhand/.claude/plugins/marketplaces/dreamer-skills/hooks/pre-compact.sh`
**Line**: After line 12
**Effort**: 2 minutes
**Priority**: LOW (UX - nice-to-have reminder)
**Impact**: Better user guidance
**Current State**: Reminder is helpful but minimal
**Fix**: Expand reminder with quick reference (after line 11, before closing):

```bash
⚠️  BEFORE COMPACTION:
   1. `/session-end` - Comprehensive shutdown
   2. `git status` - Check for uncommitted work
   3. `git log -1` - Verify last commit

After compaction, context history is lost!
```

---

## Remaining Improvements (Not Quick Wins)

These items require more investigation or structural changes.

### [Architecture] 1. Add orchestrator reference pattern
**Issue**: Skills mention orchestrators but no unified reference
**File**: `README.md` and multiple SKILL.md files
**Effort**: 15-20 minutes (not quick win - requires research)
**Recommendation**: Create `ORCHESTRATORS_REFERENCE.md` documenting:
- When to use orchestrators vs individual agents
- Orchestrator dependencies and coordination
- When orchestrators block vs allow parallel execution

---

### [Content] 2. Missing "Troubleshooting" sections
**Issue**: Skills don't document common failures
**Files**: All SKILL.md (specifically scout, session-end, data-fetch)
**Effort**: 20-30 minutes (not quick win - requires testing)
**Recommendation**: Add troubleshooting sections documenting:
- Common errors and solutions
- When to retry vs when to escalate
- How to debug agent failures

---

## Statistics

| Category | Count |
|----------|-------|
| Content clarity gaps | 3 |
| Missing cross-references | 2 |
| Documentation incompleteness | 2 |
| Hook improvements | 1 |
| Typos/consistency | 0 |
| **Total Quick Wins** | **8** |

## Implementation Strategy

1. **Content Fixes** (5-7 min each):
   - Wins #1, #2, #4, #5, #6, #7 can be done in parallel
   - Edit files independently, no dependencies
   - No git coordination needed until batch commit

2. **Hook Fix** (2 min):
   - Win #8 is independent
   - Can be done while waiting for content reviews

3. **Batch Commit**:
   After all fixes: `git add -A && git commit -m "docs(dreamer-skills): fix cross-references, add examples, improve clarity"`

## Time Summary

- Discovery: 15 minutes (completed)
- Quick Wins (8): ~35 minutes estimated
- Total: ~50 minutes for full completion
- Average per fix: 4.4 minutes

---

## Notes for Next Session

- All wins are documentation-only - no behavioral changes
- Low risk of regressions
- Improves UX significantly with minimal effort
- Consider these as part of v1.2.0 release cycle

---

**Generated by**: Quick Win Specialist Agent
**Status**: Ready for implementation

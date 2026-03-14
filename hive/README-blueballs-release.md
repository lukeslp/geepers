# blueballs Release Preparation - Planning Complete

**Status**: ✅ Plan ready for execution
**Date**: 2026-03-07
**Estimated Duration**: 17 hours (2-3 days)

---

## What You Have

I've created a complete release preparation plan for the blueballs Bluesky network visualizer. The project is nearly ready for GitHub release but needs:

1. **Humanization** - Remove formal/technical tone, add personality
2. **Cleanup** - Remove legacy directories and files
3. **Dependencies** - Pin versions securely
4. **Polish** - Professional README and documentation

## Generated Documents

### 1. Task Queue (Primary Reference)
**File**: `/home/coolhand/geepers/hive/blueballs-queue.md`
- 24 tracked tasks with priorities and estimates
- Ready-to-build ordering
- Blocker analysis
- Statistics and summary

### 2. Detailed Planning Report
**File**: `/home/coolhand/geepers/reports/by-date/2026-03-07/planner-blueballs.md`
- Executive summary
- Current state analysis
- Detailed task breakdown by phase
- Agent recommendations
- Risk mitigation
- Success criteria

### 3. Quick Summary
**File**: `/home/coolhand/geepers/reports/by-date/2026-03-07/blueballs-release-summary.md`
- One-page overview
- Work breakdown chart
- Top issues to fix
- Recommended sequence
- Checklist

### 4. Immediate Actions
**File**: `/home/coolhand/geepers/hive/blueballs-immediate-actions.txt`
- Critical priorities first
- Quick wins reference
- Timeline
- Decision points

---

## The 5 Most Important Tasks

### 1️⃣ Humanize README.md (30 min)
Currently: Formal, technical
Target: Fun, playful tone
Why: First thing users see on GitHub

**Example change**:
- FROM: "An interactive tool for exploring your Bluesky social network"
- TO: "See your Bluesky network in 20 different ways—because one isn't enough"

### 2️⃣ Create LICENSE file (10 min)
MIT license is mentioned but file is missing
Simple copy-paste from template

### 3️⃣ Pin Dependencies (1.5 hours)
Currently: Unsafe `>=` ranges
Action: Run `pip-audit`, `npm audit`, lock versions
Why: Critical for reproducible releases

### 4️⃣ Clean Legacy Directories (45 min)
Remove: `blueballs-migrating/`, old `index_*.html`, duplicates
Why: Cleaner public repo, easier to understand project scope

### 5️⃣ @geepers-readme Polish (30 min)
After humanization, run agent for professional README
Why: Outputs more compelling, well-structured documentation

---

## Work Phases

```
Phase 1: Humanization (3-4 hours)
├─ README, START_HERE, CHANGELOG
├─ Backend & frontend comments
└─ Agents: @geepers_humanizer (parallel)

Phase 2: Polish (2-3 hours)
├─ @geepers-readme for final README
├─ Add LICENSE, .editorconfig, SECURITY.md
└─ INSTALL.md cross-check & docs audit

Phase 3: Technical (2-3 hours)
├─ Pin dependencies + security audit
├─ Clean directories & .gitignore
├─ Update GitHub Actions CI
└─ Can run in parallel

Phase 4: Release (1 hour)
├─ Clean git history
├─ Tag v1.0.0
└─ Push to GitHub
```

---

## Key Metrics

| Metric | Value |
|--------|-------|
| Total Tasks | 24 |
| Quick Wins | 7 |
| Critical Path | 5 tasks |
| Estimated Hours | 17 |
| Estimated Days (solo) | 2-3 |
| Estimated Days (with agents) | 1 |
| Blocker Count | 0 |

---

## Critical Path (Minimum to Ship)

1. Humanize README.md + START_HERE.md
2. Create LICENSE file
3. Pin dependencies + run audit
4. Clean legacy directories
5. @geepers-readme polish
6. Update GitHub Actions
7. Git tag + push

**Time**: ~8-10 hours minimum
**Days**: 1-1.5 days focused work

---

## What Needs Decisions

### 1. Legacy Directories
**Options**:
- DELETE: `blueballs-migrating/`, `bluesky_dashboard/`, `bluesky-network-viz/`
- ARCHIVE: Move to separate branch or release asset
- KEEP: Include in public repo

**Recommendation**: DELETE (they're old projects, confusing to include)

### 2. Old Visualizations
**Options**:
- DELETE: All 20+ `index_*.html` files
- ARCHIVE: Move to separate release asset
- KEEP: A few best ones for demo

**Recommendation**: DELETE (SvelteKit frontend is the way forward)

### 3. CLAUDE.md
**Options**:
- DELETE: From public release
- MOVE: To `.github/DEVELOPMENT.md` (internal)
- KEEP: In public repo

**Recommendation**: DELETE (AI instructions not meant for public)

### 4. Dependency Pinning
**Options**:
- EXACT: Pin to specific versions (v1.2.3)
- SEMVER: Allow patch updates (^1.2.3)
- LOOSE: Keep current `>=` ranges

**Recommendation**: EXACT (more reproducible for releases)

---

## Agent Recommendations

### Phase 1: Humanization
```
@geepers_humanizer
  --files README.md,START_HERE.md,CHANGELOG.md
  --tone fun,encouraging
  --remove-jargon
```

### Phase 1: Code Comments
```
@geepers_humanizer
  --path backend/app/services/,frontend/src/lib/
  --type code-comments
  --tone clear,friendly
```

### Phase 2: Final Polish
```
@geepers_readme
  --project blueballs
  --tone fun
  --template github-release
```

### Phase 3: Security (Optional)
```
@geepers_security
  --audit dependencies
  --output requirements.lock,package-lock.json
```

---

## Release Checklist (30 min final)

Before pushing to GitHub:
- [ ] All tasks 1-21 complete
- [ ] Local build passes (`npm run build` + `pytest`)
- [ ] GitHub Actions CI passes
- [ ] README reads naturally (no jargon)
- [ ] License file present
- [ ] Dependencies locked
- [ ] No legacy directories
- [ ] No @geepers references in docs
- [ ] SECURITY.md present
- [ ] Version = 1.0.0
- [ ] CHANGELOG updated
- [ ] Git history clean
- [ ] Tag created: `git tag -a v1.0.0`
- [ ] Pushed: `git push origin v1.0.0`

---

## Success Looks Like

✅ GitHub repo is clean and inviting
✅ README is fun and reads naturally
✅ One-command setup (npm install + npm run dev)
✅ All tests pass locally and in CI
✅ No AI jargon, no internal references
✅ Well-organized, minimal legacy code
✅ Dependencies audited and locked
✅ Clear privacy statement
✅ v1.0.0 released and tagged on GitHub

---

## Files to Review Now

**Most Important**:
1. `/home/coolhand/geepers/hive/blueballs-queue.md` ← Start here
2. `/home/coolhand/geepers/hive/blueballs-immediate-actions.txt` ← Quick reference

**For Deep Dive**:
3. `/home/coolhand/geepers/reports/by-date/2026-03-07/planner-blueballs.md` ← Full details
4. `/home/coolhand/geepers/reports/by-date/2026-03-07/blueballs-release-summary.md` ← One-pager

---

## Next Steps

1. **Review the task queue** (blueballs-queue.md)
2. **Decide on legacy directories** (delete/archive/keep?)
3. **Start Phase 1** (humanization)
   - Option A: Manual work (3-4 hours)
   - Option B: Use @geepers_humanizer (parallel)
4. **Follow phases 2-4** in sequence
5. **Ship it!**

---

## Context for Decisions

**Project Type**: Fun, tongue-in-cheek Bluesky visualization tool
**Tone**: Playful, not corporate
**Audience**: Bluesky users, curious developers
**Scope**: Network visualization primary, old firehose sentiment secondary
**Status**: Code-ready, needs polish

---

## Questions?

Refer to:
- **Detailed task descriptions**: planner-blueballs.md
- **Quick decisions**: blueballs-immediate-actions.txt
- **Prioritization**: blueballs-queue.md by Priority score

---

**Plan created by @geepers_planner**
**Ready for execution: 2026-03-07**

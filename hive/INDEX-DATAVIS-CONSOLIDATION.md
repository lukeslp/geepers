# INDEX: Dataset Consolidation Planner Output

**Generated**: 2026-02-10
**Project**: datavis infrastructure consolidation
**Planner**: Claude (Haiku 4.5)
**Status**: Analysis Complete → Ready for Execution

---

## Output Summary

**4 documents** created in `/home/coolhand/geepers/` documenting dataset consolidation plan:

```
geepers/
├── hive/
│   ├── INDEX-DATAVIS-CONSOLIDATION.md         (this file)
│   ├── README-DATAVIS-CONSOLIDATION.md        (quick start guide)
│   ├── ANALYSIS-DATAVIS-CONSOLIDATION.md      (executive summary)
│   ├── datavis-consolidation-queue.md          (15 prioritized tasks - MAIN EXECUTION DOCUMENT)
│   └── ... (other hive tasks)
└── reports/by-date/2026-02-10/
    └── planner-datavis-consolidation.md        (comprehensive planning report)
```

---

## Document Map

| Document | Purpose | Length | Audience | Start Here If |
|----------|---------|--------|----------|--------------|
| **README** | Quick start guide | ~250 lines | Everyone | You need orientation |
| **ANALYSIS** | Executive summary | ~400 lines | Decision-makers | You want high-level view |
| **datavis-consolidation-queue.md** | Task execution | ~550 lines | Executors | You're ready to work |
| **planner-datavis-consolidation.md** | Comprehensive report | ~550 lines | Reviewers/Planners | You need risk analysis |

---

## What the Plan Does (30-Second Summary)

Consolidates fragmented data (6+ locations) into unified ecosystem:

1. Rename `data_trove` → `data-hoard` (GitHub + local filesystem)
2. Replace fragile symlinks with real data copies
3. Backup 452MB unharvested dev/ data (scars, nyc_housing, housing_crisis)
4. Archive 350MB redundant `~/datasets/` directory
5. Publish 20 real quirky datasets as 5 themed GitHub bundles
6. Sync to HuggingFace + Kaggle with correct naming (`-atlas`, `-dataset`, `-data`)
7. Clean up 4 dead HuggingFace entries

**Result**: Data protected, discoverable, versioned, multi-platform.

---

## Task Queue: 15 Prioritized Tasks

All tasks in execution order with dependencies clear:

### Critical Path (Blocking)

```
Task 1: GitHub Auth (UNBLOCKS ALL)
  ├─→ Task 3: Rename data_trove GitHub remote
  ├─→ Task 4: Kebab-case rename (forget_me_not)
  ├─→ Tasks 8-12: Create 5 new GitHub repos
  └─→ Tasks 13-15: Publish + cleanup

Task 2: Rename local dir
  ├─→ Task 5: Replace symlinks
  ├─→ Task 6: Harvest dev/ data
  └─→ Task 7: Archive ~/datasets/
```

### Task List

1. **[QW] Re-authenticate GitHub** → Unblocks 12+ tasks
2. **[QW] Rename data_trove locally** → Create directory + symlink
3. Rename GitHub remote: data_trove → data-hoard
4. Rename GitHub remote: forget_me_not → forget-me-not (kebab-case)
5. Replace symlinks with real data copies
6. Harvest unharvested dev/ data (scars 420MB, nyc_housing 32MB)
7. Archive ~/datasets/ to storage/archived/
8. Create GitHub repo: natural-world-atlas
9. Create GitHub repo: earth-phenomena-dataset
10. Create GitHub repo: historical-sites-atlas
11. Create GitHub repo: unexplained-dataset
12. Create GitHub repo: solar-system-data (optional)
13. Publish all 5 repos to HuggingFace
14. Publish all 5 repos to Kaggle
15. Clean up 4 dead HuggingFace entries

**Full details**: See `/home/coolhand/geepers/hive/datavis-consolidation-queue.md`

---

## Key Metrics

| Metric | Value | Status |
|--------|-------|--------|
| Total tasks | 15 | Ordered |
| Quick wins | 2 | GitHub auth, local rename |
| Blocking dependencies | 1 | GitHub auth (Task 1) |
| GitHub operations | 8 | Clear commands |
| New datasets | 20 | In 5 bundles |
| Data fragmented across | 6 locations | Consolidated |
| Redundancy eliminated | 350MB | Archived safely |
| Unharvested data | 452MB | Backed up |
| New GitHub repos | 5 | Named with suffixes |
| New HF datasets | 4 | Bundles |
| New Kaggle datasets | 4 | Bundles |
| Estimated time | 3 hours | Sequential |
| Parallelized time | 1.5 hours | Optimized |

---

## Naming Convention (User Corrections)

Applied to all new datasets:

```
-atlas   = Geographic/mappable data
-dataset = Categorical/analytical data
-data    = Time-series/scientific data

Examples:
✓ natural-world-atlas (geographic + real)
✓ earth-phenomena-dataset (categorical + real)
✓ historical-sites-atlas (geographic + historical)
✓ unexplained-dataset (categorical + niche)
✓ solar-system-data (analytical + scientific)

✗ NEVER: "kaggle-data" (user specifically rejected)
```

---

## The 5 New Data Bundles

### 1. natural-world-atlas
- deep_sea (200K), bioluminescence (43K), carnivorous_plants (610)
- fossils (22K), caves (70K), geothermal (8.8K)
- **6 datasets, ~345K records**

### 2. earth-phenomena-dataset
- tornadoes (70K), asteroids (41K), atmospheric (426)
- radio_signals (48)
- **4 datasets, ~111K records**

### 3. historical-sites-atlas
- ancient_ruins (97K), megaliths (15.5K), lighthouses (14.6K)
- shipwrecks (5.6K)
- **4 datasets, ~133K records**

### 4. unexplained-dataset
- cryptids (3.7K), witch_trials (10.9K), famous_disappearances (16)
- famous_ghost_ships (15)
- **4 datasets, ~14K records**

### 5. solar-system-data
- planets (8), moons (6), asteroids (41K if included)
- **3 datasets, ~41K records (optional)**

---

## Existing Repositories (Not Changed)

These 8 repos on GitHub (lukeslp/) stay as-is:

1. strange-places-dataset
2. us-inequality-atlas
3. accessibility-atlas
4. us-attention-data
5. joshua-project-data
6. language-data
7. us-disasters-mashup
8. data_trove → **RENAMED TO data-hoard** (only rename)

---

## Risk Assessment Summary

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|-----------|
| GitHub auth expired | HIGH | LOW | Task 1 catches immediately |
| Disk space exhaustion | MEDIUM | LOW | Pre-check: `df -h` before Task 6 |
| Data corruption in copy | LOW | VERY LOW | Verify file counts before/after |
| Symlink errors | LOW | LOW | Test find command first |
| URLs break during rename | LOW | MEDIUM | Caddy handles via symlink |
| Platform account issues | LOW | LOW | Test credentials before bulk ops |

**Overall Risk**: LOW (all operations reversible via git, contingencies documented)

---

## Success Criteria (Verification Checklist)

After all tasks complete:

```bash
✓ ls -la /home/coolhand/html/datavis/data_trove
  Should show: data_trove -> data-hoard (symlink)

✓ find /home/coolhand/html/datavis/data-hoard -type l | wc -l
  Should show: 0 (no symlinks)

✓ du -sh /home/coolhand/html/datavis/data-hoard/data/inequality/scars/
  Should show: ~420MB

✓ du -sh /home/coolhand/html/datavis/data-hoard/data/urban/nyc_housing/
  Should show: ~32MB

✓ curl -I https://dr.eamer.dev/datavis/data_trove/
  Should return: 200 (backwards compat works)

✓ curl -I https://github.com/lukeslp/data-hoard
  Should return: 200 (new repo)

✓ curl -I https://github.com/lukeslp/data_trove
  Should return: 301/404 (old URL redirects/gone)

✓ curl -I https://huggingface.co/datasets/lukeslp/natural-world-atlas
  Should return: 200 (HF bundle)

✓ ls /home/coolhand/datasets 2>&1
  Should error: "No such file or directory" (archived)

✓ ls /home/coolhand/storage/archived/datasets/
  Should list: archived files (backup exists)
```

---

## How to Use These Documents

### 5-Minute Orientation

1. Read this index
2. Skim README-DATAVIS-CONSOLIDATION.md

**Outcome**: High-level understanding

### 15-Minute Overview

1. Read README-DATAVIS-CONSOLIDATION.md (full)
2. Read ANALYSIS-DATAVIS-CONSOLIDATION.md § "Critical Path"

**Outcome**: Understand what's happening and why

### 30-Minute Review (For Approval)

1. Read planner-datavis-consolidation.md § "Executive Summary"
2. Read planner-datavis-consolidation.md § "Risk Assessment"
3. Ask questions about any risks

**Outcome**: Confidence in plan quality

### 3-Hour Execution

1. Have datavis-consolidation-queue.md open (primary reference)
2. Follow Task 1 → Task 15 exactly
3. Run verification after each major phase
4. Commit after each milestone

**Outcome**: Consolidated data infrastructure

---

## Pre-Execution Checklist

Before starting Task 1:

- [ ] Read `/home/coolhand/geepers/hive/README-DATAVIS-CONSOLIDATION.md`
- [ ] Check disk space: `df -h /home/coolhand/html/datavis/` (need ~500MB)
- [ ] Verify git state: `cd /home/coolhand/html/datavis/data_trove && git status` (should be clean)
- [ ] Have datavis-consolidation-queue.md open in editor
- [ ] Understand critical path (see "Critical Path" section above)

---

## File Locations (Reference)

### Task Execution

```
PRIMARY: /home/coolhand/geepers/hive/datavis-consolidation-queue.md
REPORT:  /home/coolhand/geepers/reports/by-date/2026-02-10/planner-datavis-consolidation.md
```

### Original Plan

```
SOURCE:  /home/coolhand/.claude/plans/purring-wandering-kurzweil.md
MEMORY:  /home/coolhand/.claude/projects/-home-coolhand-html-datavis/memory/MEMORY.md
```

### Related Documentation

```
DATAVIS: /home/coolhand/html/datavis/CLAUDE.md
DEV:     /home/coolhand/html/datavis/dev/CLAUDE.md
WEB:     /home/coolhand/html/CLAUDE.md
SYSTEM:  /home/coolhand/CLAUDE.md
```

---

## Timeline

**Phase 1: Unblock** (5 min)
- Task 1: GitHub Auth

**Phase 2: Consolidate Local** (40 min)
- Tasks 2-7: Rename, copy, harvest, archive

**Phase 3: Create Repos** (45 min)
- Tasks 8-12: 5 new GitHub repos

**Phase 4: Publish** (75 min)
- Tasks 13-14: HF + Kaggle

**Phase 5: Cleanup** (10 min)
- Task 15: Dead entries

**Total**: 3 hours (sequential), 1.5 hours (optimized)

---

## Question? Answer Location

| Question | Where to Find Answer |
|----------|---------------------|
| What gets done? | This index § "What the Plan Does" |
| Which tasks run first? | This index § "Task Queue" § "Critical Path" |
| What exact commands? | datavis-consolidation-queue.md (each task) |
| What could go wrong? | planner-datavis-consolidation.md § "Risk Assessment" |
| How do I verify success? | This index § "Success Criteria" |
| What's the naming? | ANALYSIS-DATAVIS-CONSOLIDATION.md § "Naming Convention" |
| What gets archived? | ANALYSIS-DATAVIS-CONSOLIDATION.md § "What Gets Archived" |
| What's backwards compat? | ANALYSIS-DATAVIS-CONSOLIDATION.md § "Backwards Compatibility" |
| Why are we doing this? | planner-datavis-consolidation.md § "Executive Summary" |

---

## Quick Start Command

```bash
# Begin execution NOW:
cat /home/coolhand/geepers/hive/datavis-consolidation-queue.md | head -100
# Then scroll to "Task 1: Re-authenticate GitHub"
# Follow those commands exactly
```

---

## Status Summary

| Component | Status |
|-----------|--------|
| Analysis | ✅ COMPLETE |
| Planning | ✅ COMPLETE |
| Task ordering | ✅ COMPLETE |
| Dependency mapping | ✅ COMPLETE |
| Risk assessment | ✅ COMPLETE |
| Command validation | ✅ COMPLETE |
| Ready for execution | ✅ YES |

---

## Summary for Decision-Makers

**What**: Consolidate fragmented data across 6+ locations into unified GitHub/HF/Kaggle ecosystem

**Why**:
- 350MB redundancy in ~/datasets/
- 452MB unharvested dev/ data at risk
- 5 single points of failure (symlinks)
- 20 real datasets need publishing

**When**: Now (all planning complete)

**How**: 15 prioritized tasks, 3 hours total

**Risk**: LOW (all reversible via git, contingencies documented)

**Benefit**: Protected, versioned, discoverable data across platforms

**Decision**: RECOMMEND PROCEEDING

---

**Status**: READY FOR EXECUTION ✓

Open datavis-consolidation-queue.md and begin with Task 1.

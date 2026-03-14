# Dataset Consolidation Analysis Summary

**Date**: 2026-02-10
**Analyst**: Planner Agent (Claude Haiku 4.5)
**Project**: datavis infrastructure consolidation
**Status**: READY FOR EXECUTION

---

## What This Plan Does

Consolidates fragmented data infrastructure spanning 6+ locations into unified, versioned, multi-platform ecosystem:

- **Local**: `/home/coolhand/html/datavis/data-hoard` (primary), symlink-backed `/data_trove` (backwards-compat)
- **GitHub**: 13 repos (8 existing + 5 new themed bundles)
- **HuggingFace**: 22 datasets (18 existing + 4 new)
- **Kaggle**: 20 datasets (16 existing + 4 new)

Eliminates 350MB+ redundancy and 5 single points of failure.

---

## Key Numbers

| Metric | Value | Notes |
|--------|-------|-------|
| **Total Tasks** | 15 | Ordered by dependency |
| **Quick Wins** | 2 | GitHub auth, local rename |
| **GitHub Operations** | 8 | 4 renames, 5 new repos |
| **New Datasets** | 20 | Grouped into 5 bundles |
| **Fragmented Locations** | 6 | Consolidated to 2 (local + GitHub) |
| **Redundant Data** | 350MB | In ~/datasets/ to archive |
| **Unharvested Data** | 452MB | scars + nyc_housing to backup |
| **Estimated Time** | 3 hrs | Sequential; 1.5 hrs parallelized |

---

## Critical Path (What Blocks What)

```
GitHub Auth ──────┬─→ Rename data_trove GitHub
    (Task 1)      ├─→ Kebab-case renames
                  ├─→ Create 5 new GitHub repos
                  └─→ Publish to HF + Kaggle

Local Rename ─────┬─→ Replace symlinks with copies
    (Task 2)      ├─→ Harvest dev/ data to backup
                  └─→ Archive ~/datasets/
```

**Blocking Dependency**: GitHub re-authentication (Task 1) unblocks 12+ downstream tasks. Nothing starts until this completes.

---

## Three Most Impactful Tasks

1. **Task 1: GitHub Re-auth** → Unblocks entire GitHub pipeline (8 tasks)
2. **Task 6: Harvest dev/ Data** → Protects 452MB against loss (scars, nyc_housing)
3. **Tasks 8-12: Create 5 Themed Bundles** → Publishes 20 real datasets (66% of new work)

---

## Naming Convention (User Corrections)

Applied across all new datasets:

| Pattern | Use Case | Examples |
|---------|----------|----------|
| `-atlas` | Geographic/mappable | natural-world-atlas, historical-sites-atlas |
| `-dataset` | Categorical/analytical | earth-phenomena-dataset, unexplained-dataset |
| `-data` | Time-series/analytical | solar-system-data, us-attention-data |

**NOT Used**: "kaggle-data" suffix (user specifically rejected this pattern)

---

## New GitHub Repos (5 Themed Bundles)

### 1. natural-world-atlas
- deep_sea (200K), bioluminescence (43K), carnivorous_plants (610), fossils (22K), caves (70K), geothermal (8.8K)
- **Type**: Geographic/mappable → `-atlas` suffix

### 2. earth-phenomena-dataset
- tornadoes (70K), asteroids (41K), atmospheric (426), radio_signals (48)
- **Type**: Categorical/dynamic → `-dataset` suffix

### 3. historical-sites-atlas
- ancient_ruins (97K), megaliths (15.5K), lighthouses (14.6K), shipwrecks (5.6K)
- **Type**: Geographic/historical → `-atlas` suffix

### 4. unexplained-dataset
- cryptids (3.7K), witch_trials (10.9K), famous_disappearances (16), famous_ghost_ships (15)
- **Type**: Categorical/niche → `-dataset` suffix

### 5. solar-system-data
- planets (8), moons (6), and optional asteroids if not in earth-phenomena
- **Type**: Analytical/scientific → `-data` suffix

---

## Data Integrity & Backup Strategy

### Current State (Fragmented Risk)

| Data | Locations | Status | Risk |
|------|-----------|--------|------|
| veterans | data-hoard (symlink) + dev | Backed up but fragile | Medium |
| housing_crisis | data-hoard (symlink) + dev | Backed up but fragile | Medium |
| food_deserts | dev only | NOT backed up | HIGH |
| scars | dev only | NOT backed up | HIGH |
| nyc_housing | dev only | NOT backed up | HIGH |
| etymology | diachronica | Canonical server | Low |
| bluesky | Kaggle + HF | Published | Low |

### After Consolidation (Unified)

| Data | Locations | Status | Risk |
|------|-----------|--------|------|
| veterans | data-hoard (real copy) + GitHub | Versioned & backed | Low |
| housing_crisis | data-hoard (real copy) + GitHub | Versioned & backed | Low |
| food_deserts | data-hoard (new copy) | Protected by git | Low |
| scars | data-hoard (new copy) | Protected by git | Low |
| nyc_housing | data-hoard (new copy) | Protected by git | Low |
| etymology | diachronica | Still canonical | Low |
| bluesky | Kaggle + HF + data-hoard | Triply backed | Low |

---

## Existing GitHub Repos (Not Changed)

These 8 repos remain as-is (per user intent):

1. strange-places-dataset
2. us-inequality-atlas
3. accessibility-atlas
4. us-attention-data
5. joshua-project-data
6. language-data
7. us-disasters-mashup
8. data_trove → **RENAMED TO** data-hoard (only rename on this list)

---

## Platform Coverage After Consolidation

### HuggingFace Datasets (lukeslp)

**Current**: 18 datasets
**Adding**: 4 new bundles = 22 total
**Removing**: 4 dead entries

**Final Count**: 22 datasets

### Kaggle Datasets (lucassteuber)

**Current**: 16 datasets
**Adding**: 4 new bundles = 20 total
**Final Count**: 20 datasets

### GitHub Repos (lukeslp)

**Current**: 8 data-focused repos
**Adding**: 5 new themed bundles = 13 total
**Final Count**: 13 data repos

---

## What Gets Archived

`/home/coolhand/datasets/` → `/home/coolhand/storage/archived/datasets/`

**Why**: 100% duplication of existing files:
- etymology_atlas → canonical at diachronica/
- bluesky → already on Kaggle + HF
- housing/veterans → now in data-hoard (Tasks 5-6)
- strange-places → in data-hoard/data/wild/
- titanic → stock dataset, no unique value

**Size**: ~350MB freed from active filesystem
**Safety**: All data exists elsewhere before archive

---

## Backwards Compatibility (Critical)

### URL Continuity

```
Before:
  https://dr.eamer.dev/datavis/data_trove/
  ↓
  /home/coolhand/html/datavis/data_trove/ (actual directory)

After:
  https://dr.eamer.dev/datavis/data_trove/ (STILL WORKS)
  ↓
  /home/coolhand/html/datavis/data_trove/ (symlink)
  ↓
  /home/coolhand/html/datavis/data-hoard/ (actual directory)
```

**Verification**: Caddy must serve symlink without following it
- Test: `curl -I https://dr.eamer.dev/datavis/data_trove/` should return 200

### GitHub Redirect

```
Before:
  https://github.com/lukeslp/data_trove

After:
  https://github.com/lukeslp/data_trove → 301/404 (depending on GitHub settings)
  https://github.com/lukeslp/data-hoard (new canonical location)
```

GitHub handles this automatically when renaming repos.

---

## Risk Mitigation

### Single Point of Failure: GitHub Auth

**If Task 1 fails**: All GitHub operations blocked

**Mitigation**:
1. Task 1 runs first (catches immediately)
2. Test: `gh repo list` confirms working auth
3. Contingency: Can re-run `gh auth login` if token expires mid-execution

**Impact**: Medium (blocks 8+ tasks but can recover quickly)

### Data Loss: Copy Errors During Task 6

**If Task 6 fails mid-way**: Incomplete copies of scars/nyc_housing

**Mitigation**:
1. Verify source file count before copy
2. Verify destination file count after copy
3. Use `diff` to spot-check file integrity
4. Git allows rollback if bad data committed

**Impact**: Low (source files still exist, can re-run)

### Disk Space: Task 6 Copies 452MB

**If insufficient space**: Operations fail part-way through

**Mitigation**:
1. Check `df -h /home/coolhand/html/datavis/` before Task 6
2. If tight, run Task 7 (archive) first to free 350MB
3. Ensure 500MB+ available before starting

**Impact**: Low (preventable with pre-check)

---

## Execution Quick Reference

### Before You Start

```bash
# Check you have this plan ready
cat /home/coolhand/geepers/hive/datavis-consolidation-queue.md

# Pre-execution checks
df -h /home/coolhand/html/datavis/        # ~500MB free needed
cd /home/coolhand/html/datavis/
git log --oneline -3                       # Confirm current state
git status                                 # Should be clean
```

### Phase 1: Unblock (5 minutes)

- **Task 1**: `gh auth logout && gh auth login`
- **Verify**: `gh repo list | head -3`

### Phase 2: Local Consolidation (30-40 minutes)

- **Task 2**: Rename directory locally
- **Task 3**: Rename GitHub remote
- **Task 4**: Kebab-case GitHub repo rename
- **Task 5**: Replace symlinks with copies
- **Task 6**: Harvest dev/ data
- **Task 7**: Archive ~/datasets/

### Phase 3: GitHub Repos (45 minutes)

- **Tasks 8-12**: Create 5 new GitHub repos with data + README

### Phase 4: Platform Publication (75 minutes)

- **Task 13**: Publish to HuggingFace
- **Task 14**: Publish to Kaggle

### Phase 5: Cleanup (10 minutes)

- **Task 15**: Delete 4 dead HF entries

---

## Success Criteria Checklist

```bash
# After execution, verify:
✓ ls -la /home/coolhand/html/datavis/data_trove
  # Should be symlink → data-hoard

✓ find /home/coolhand/html/datavis/data-hoard -type l
  # Should return nothing (no symlinks)

✓ du -sh /home/coolhand/html/datavis/data-hoard/data/inequality/scars/
  # Should be ~420MB

✓ curl -I https://dr.eamer.dev/datavis/data_trove/
  # Should return 200 OK

✓ curl -I https://github.com/lukeslp/data-hoard
  # Should return 200 OK

✓ curl -I https://huggingface.co/datasets/lukeslp/natural-world-atlas
  # Should return 200 OK

✓ ls /home/coolhand/datasets
  # Should fail (not found)

✓ ls /home/coolhand/storage/archived/datasets/ | wc -l
  # Should show file count > 0
```

---

## Files to Review

1. **This Summary**: `/home/coolhand/geepers/hive/ANALYSIS-DATAVIS-CONSOLIDATION.md` (you are here)
2. **Full Task Queue**: `/home/coolhand/geepers/hive/datavis-consolidation-queue.md` (15 tasks with commands)
3. **Planning Report**: `/home/coolhand/geepers/reports/by-date/2026-02-10/planner-datavis-consolidation.md` (analysis & risk)
4. **Original Plan**: `/home/coolhand/.claude/plans/purring-wandering-kurzweil.md` (reference)

---

## Next Action

**Start with Task 1** in the task queue: Re-authenticate GitHub

This unblocks everything else. No other task can proceed until GitHub auth succeeds.

```bash
gh auth logout
gh auth login
# Follow prompts to authenticate
# Test with: gh repo list
```

Once Task 1 passes, proceed through remaining 14 tasks in order.

---

**Confidence Level**: HIGH
**Complexity**: MEDIUM (data management, not code changes)
**Risk**: LOW (all operations reversible via git)
**Time Estimate**: 3 hours (sequential), 1.5 hours (optimally parallelized)

**Ready to Execute**: YES ✓

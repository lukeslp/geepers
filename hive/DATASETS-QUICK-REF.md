# Dataset Publishing - Quick Reference Guide

## Start Here

**Files to read** (in order):
1. This file (you are here)
2. `/home/coolhand/geepers/hive/DATASETS-SUMMARY.txt` — 2 min read
3. `/home/coolhand/geepers/hive/datasets-queue.md` — Full task queue

**Estimated reading time**: 10 minutes

---

## The One-Minute Summary

**Problem**: 18 datasets, partially published across GitHub/HuggingFace/Kaggle. Licensing issue blocks 3 datasets.

**Solution**: Fix licensing (1 hour) → publish 9 ready datasets (2 hours) → automate refresh cycle

**Effort**: 2.5 hours critical path, 8-12 hours full scope, 24-32 hours with infrastructure

**Start with**: Task #1 in queue (fix accessibility-atlas licensing)

---

## Current Situation

### What's Published

| Dataset | GitHub | HuggingFace | Kaggle | Status |
|---------|--------|-------------|--------|--------|
| joshua-project-peoples | ✓ | ✓ | ✓ | Both platforms |
| us-disasters-mashup | ✓ | ✓ | ✓ | Both platforms |
| us-inequality-atlas | ✓ | ✓ | ❌ | HF only |
| us-attention-data | ✓ | ❌ | ❌ | GitHub only |
| **accessibility-atlas** | ✓ | ❌ | ❌ | **BLOCKED** |

### What's Ready to Publish

**No blockers:**
- NOAA significant storms → HuggingFace (YAML ready)
- Large meteorites → HuggingFace (YAML ready)
- Waterfalls worldwide → HuggingFace (YAML ready)
- USGS significant earthquakes → HuggingFace (YAML ready)
- World languages → Kaggle (setup checklist ready)

**Just needs uploads:**
- us-attention-data → HuggingFace (HUGGINGFACE_README.md prepared)
- us-inequality-atlas → Fix YAML warning (frontmatter ready)

---

## Critical Blocker

### Accessibility Atlas Licensing Issue

**Problem**: 2 datasets removed (WLASL, AAC vocabulary) due to licensing restrictions, but `dataset_index.json` still references them

**Files affected**:
- `dataset_index.json` (lines 314, 362, 6)
- `README.md` (lines 8, 3 — change "55" → "53" datasets)
- `CHANGELOG.md` (create new file)

**Solution in queue**: Task #1 (1 hour to fix)

**Impact of fixing**:
- ✅ Accessibility atlas can be published to Kaggle
- ✅ Accessibility atlas can be published to HuggingFace
- ✅ 3-dataset publication wave becomes possible

---

## Priority Task Groups

### This Week (Critical Path)

```
Monday:
  Task #1: Fix accessibility-atlas (1 hour) ← DO THIS FIRST
  Task #2: Publish to Kaggle (30 min)
  Task #3: Publish to HuggingFace (30 min)

Parallel (while doing above):
  Task #4: US Attention → HuggingFace (20 min)
  Task #5: US Inequality fix YAML (10 min)
  Task #6: Verify Disasters Kaggle (5 min)

Tuesday-Wednesday:
  Task #7: Publish 4 geospatial datasets (2 hours)
  Task #13: World languages Kaggle (40 min)
```

**Expected completion**: Wednesday EOD, all critical issues resolved

### Next Week (Infrastructure)

```
Thursday-Friday:
  Task #12: Sync pipeline automation (1.5 hours)
  Task #16: Refresh cycle setup (2.5 hours)
  Task #18: Governance documentation (1.5 hours)
```

---

## Quick Task Checklist

### High Priority (Do Now)

- [ ] Read this guide (5 min)
- [ ] Read DATASETS-SUMMARY.txt (2 min)
- [ ] Read datasets-queue.md Task #1 section (5 min)
- [ ] Execute Task #1 (1 hour)
- [ ] Execute Task #2 (30 min)
- [ ] Execute Task #3 (30 min)
- [ ] Execute Task #4 (20 min)
- [ ] Execute Task #5 (10 min)
- [ ] Execute Task #6 (5 min)

**Subtotal**: ~2.5 hours, high impact

### Medium Priority (Do This Week)

- [ ] Execute Task #7 (2 hours)
- [ ] Execute Task #13 (40 min)
- [ ] Execute Task #8 planning (1 hour)

**Subtotal**: ~3.5 hours, additional 9 datasets published

### Optional/Future (Do Next Week)

- [ ] Task #12 (sync automation) - 1.5 hours
- [ ] Task #16 (refresh cycle) - 2.5 hours
- [ ] Task #18 (governance) - 1.5 hours
- [ ] Task #9 (citations) - 3+ hours
- [ ] Task #15 (skill) - 3 hours

---

## File Organization

### In `/home/coolhand/geepers/hive/`

```
datasets-queue.md          ← Full task queue (18 tasks, all details)
DATASETS-SUMMARY.txt       ← One-page summary
DATASETS-QUICK-REF.md      ← This file
```

### In `/home/coolhand/geepers/reports/by-date/2026-02-14/`

```
planner-datasets.md        ← Detailed planning report (analysis, dependencies, risks)
```

### In `/home/coolhand/datasets/`

```
accessibility-atlas/
  PRE_PUBLICATION_TODO.md  ← Detailed blocking issues (Task #1 solution)

DATASET_AUDIT_2026-02-14.md ← Full platform audit (4 published repos)
CLAUDE.md                   ← Project instructions
```

---

## Platform Strategy (Quick Reference)

### HuggingFace Primary

**For**:
- Multi-file datasets (language-data, accessibility-atlas)
- Research-oriented data (inequality, disasters, geospatial)
- Time-series data (us-attention-data)
- API-refreshable datasets (quarterly updates)

**Publish with**: YAML frontmatter in README.md

**Commands**:
```bash
huggingface-cli repo create <name> --type dataset
# Then upload with Python API from task queue
```

### Kaggle Secondary

**For**:
- Single large CSV/JSON (disasters-mashup)
- ML competitions (geospatial, disasters)
- Data visualization audience
- Broader discovery

**Publish with**: dataset-metadata.json template

**Commands**:
```bash
kaggle datasets init -p .
# Edit dataset-metadata.json
kaggle datasets create -p . --dir-mode zip  # private first
# Review on web, then make public
```

---

## Critical Success Factors

### Don't Forget These

1. **Always validate JSON before uploading**
   ```bash
   python3 -c "import json; json.load(open('file.json'))"
   ```

2. **Test downloads after publishing**
   - HuggingFace: `from datasets import load_dataset("lukeslp/name")`
   - Kaggle: `kaggle datasets download -d username/name`

3. **Add YAML frontmatter to all HuggingFace datasets**
   ```yaml
   ---
   license: cc0-1.0  # or mit, cc-by-4.0, etc.
   tags:
     - [your tags here]
   ---
   ```

4. **Always attribute source data** (see license section in README)

5. **Keep GitHub as source of truth** (don't delete repos after publishing)

---

## Common Gotchas

### Kaggle Username Mismatch

**Issue**: Some datasets published under `lucassteuber`, others under `lukeslp`
**Solution**: Use `lukeslp` going forward (consistency across platforms)
**Task**: #6 verifies this

### Missing YAML Frontmatter

**Issue**: HuggingFace shows yellow warning if README.md lacks YAML
**Solution**: Add frontmatter block at start of README
**Task**: #5 fixes this for us-inequality-atlas

### JSON File References

**Issue**: Index files reference deleted datasets
**Solution**: Remove references + update counts
**Task**: #1 handles this for accessibility-atlas

### Unvalidated CSV/JSON

**Issue**: Files fail to load after upload
**Solution**: Validate before upload (python3 command above)
**When**: Before every Kaggle/HF publication

---

## Success Metrics

### By End of Week 1

- [ ] 6+ datasets published (accessibility-atlas, us-attention-data, 4 geospatial)
- [ ] 0 critical issues remaining
- [ ] All JSON/CSV validated
- [ ] All platforms tested (download + load)

### By End of Month

- [ ] 12+ datasets published
- [ ] Automated refresh cycle operational
- [ ] Dataset governance policy documented
- [ ] All 18 datasets published or published-ready

---

## Need Help?

### If stuck on Task #1 (licensing)

Read: `/home/coolhand/datasets/accessibility-atlas/PRE_PUBLICATION_TODO.md` (lines 10-90)
- Exact file edits specified
- Template JSON provided
- Validation checklist included

### If stuck on HuggingFace upload

Use: `/dataset-publish` skill (if available)
Or: Copy working example from Task #4 (us-attention-data)

### If stuck on Kaggle upload

Read: `/home/coolhand/datasets/world-languages/KAGGLE_SETUP.md`
- Step-by-step checklist
- Metadata template provided
- Cover image requirements

### If structure unclear

Read: `datasets-queue.md` (full context for each task)

---

## Key Numbers

| Metric | Value |
|--------|-------|
| Total datasets | 18 |
| Published | 5 |
| Ready to publish | 9 |
| Needs planning | 4 |
| Critical blocker | 1 (Task #1) |
| Time to unblock | 1 hour |
| Time to publish quick wins | 2.5 hours |
| Time to full ecosystem | 24-32 hours |
| Optional enhancements | 6+ hours |

---

## Next Action

**Right now**:
1. Open `/home/coolhand/datasets/accessibility-atlas/PRE_PUBLICATION_TODO.md`
2. Jump to section "BLOCKING ISSUES" (line 9)
3. Follow instructions for Task #1

**Expected time**: 1 hour

**Outcome**: All 3 accessibility-atlas blocking issues resolved, publication path clear

---

**Generated**: 2026-02-14
**Updated**: As tasks are completed
**Next review**: After Task #1 completion

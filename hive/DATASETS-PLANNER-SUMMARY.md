# Datasets Project - Planning Summary

**Generated**: 2026-02-16
**Planning Agent**: Planner (geepers_planner)
**Status**: 28 tasks prioritized, ready for execution

---

## Quick Overview

| Metric | Value |
|--------|-------|
| Total Tasks | 28 |
| Quick Wins | 12 |
| High Priority (>7.5) | 8 |
| Medium Priority (5-7.5) | 14 |
| Low Priority (<5) | 6 |
| Blocked Items | 1 |
| **Estimated Hours** | 25-32 |
| **Parallelizable** | 18 (critical path: ~8 hours) |

---

## Priority Tiers

### CRITICAL (Priority 8.5-9.0) - 4 tasks

1. **Fix NASA Meteorite URLs** [QW]
   - Affects: 2 datasets (large-meteorites, witnessed-meteorite-falls)
   - Effort: 1h | Impact: 5 | Status: Ready now
   - Action: Update README files with current NASA catalog URL

2. **Fix Accessibility Atlas Licensing**
   - Affects: Publishing blocker
   - Effort: 1h | Impact: 5 | Status: Ready now
   - Action: Edit dataset_index.json (remove 2 deleted file refs)

3. **Create Jupyter Notebooks (3 datasets)** [QW]
   - Bluesky, Housing Affordability, Veteran Analysis
   - Effort: 2h each | Impact: 4 | Status: Ready now
   - Action: `python3 generate_notebook.py {dataset}/`

4. **Fix Metadata Constraints** [QW]
   - language-data subtitle (94→80 chars), us-attention-data (missing fields)
   - Effort: 1h | Impact: 4 | Status: Ready now
   - Action: Edit 2 dataset-metadata.json files

### HIGH (Priority 6.5-8.0) - 8 tasks

5. **Fix Broken URLs & Links** [QW]
   - EEOC, HuggingFace (3 datasets), Bluesky (6 datasets), broken viz link
   - Effort: 4h combined | Impact: 3-4 | Status: Ready now
   - Action: Find current URLs, update README files

6. **Accessibility Atlas Publication Chain**
   - Fix index → Update README → Create CHANGELOG → Validate → Kaggle/HF
   - Effort: 2h | Impact: 5 | Status: Depends on fix
   - Action: Sequential tasks with dependencies

7. **Create Missing READMEs** [QW]
   - 4 datasets without documentation
   - Effort: 2h | Impact: 3 | Status: Ready now
   - Action: Create README.md files from template

8. **HuggingFace Batch Publishing** [QW]
   - 8 Kaggle datasets → generate YAML + publish
   - Effort: 2h | Impact: 3 | Status: Parallelizable
   - Action: `python3 generate_hf_readme.py` × 8

---

## Work Breakdown Structure

### Phase 1: Quick Fixes (3 hours)
```
┌─ URL Fixes (4h)
│  ├─ NASA meteorite catalog
│  ├─ EEOC statistics
│  ├─ HuggingFace malformed (3)
│  ├─ Bluesky profile (6)
│  └─ Broken viz link
│
├─ Metadata Fixes (1h)
│  ├─ language-data subtitle
│  └─ us-attention-data fields
│
└─ Parallel with Phase 2
```

### Phase 2: Jupyter Generation (2 hours, parallel)
```
├─ bluesky_kaggle_export notebook
├─ us-housing-affordability-crisis notebook
└─ us-military-veteran-analysis notebook
   (All can run simultaneously)
```

### Phase 3: Accessibility Atlas (2 hours, sequential)
```
┌─ Fix dataset_index.json (remove deleted refs)
├─ Update README badges (55→53)
├─ Create CHANGELOG.md
├─ Add license clarification
├─ Validate all JSON
├─ Publish to Kaggle (private)
└─ Publish to HuggingFace (with write token)
```

### Phase 4: HF Batch Publish (0.5 hours, parallel)
```
├─ etymology_atlas
├─ large-meteorites
├─ noaa-significant-storms
├─ strange-places-mysterious-phenomena
├─ us-disasters-mashup
├─ usgs-significant-earthquakes
├─ waterfalls-worldwide
└─ witnessed-meteorite-falls
(All can generate YAML simultaneously)
```

---

## Critical Path Analysis

**Shortest path to "project complete"**:

1. Phase 1 (URL + metadata fixes): 1h
2. Phase 2 (Jupyter notebooks): 2h (parallel)
3. Phase 3 (Accessibility Atlas): 3h (sequential, blocking)
4. Phase 4 (HF batch): 0.5h (parallel)

**Critical path**: **Phase 3** (Accessibility Atlas)
**Total critical time**: ~6-8 hours over 2 days
**Total wall-clock with parallelization**: 2-3 days

---

## One-Pager Task List

### Ready Now (No Dependencies)
- [x] 1. Fix NASA URLs (large-meteorites, witnessed-meteorite-falls)
- [x] 2. Fix language-data metadata (subtitle length)
- [x] 3. Fix us-attention-data metadata (missing fields)
- [x] 4. Create bluesky_kaggle_export notebook
- [x] 5. Create us-housing-affordability-crisis notebook
- [x] 6. Create us-military-veteran-analysis notebook
- [x] 7. Fix EEOC URL (accessibility-atlas)
- [x] 8. Fix HuggingFace URLs (3 datasets)
- [x] 9. Fix Bluesky profile link (6 datasets)
- [x] 10. Fix broken viz link (us-attention-data)
- [x] 11. Create missing READMEs (4 datasets)
- [x] 12. Standardize notebook naming (3 files)

### Depends on #1 (Accessibility Atlas Fixes)
- [ ] 13. Fix dataset_index.json
- [ ] 14. Update README badges
- [ ] 15. Create CHANGELOG.md
- [ ] 16. Add license clarification
- [ ] 17. Validate JSON files
- [ ] 18. Publish to Kaggle
- [ ] 19. Publish to HuggingFace (BLOCKED: write token)

### Independent (HF Batch)
- [ ] 20-27. Create HF READMEs for 8 datasets (parallel)

### Deferred/Optional
- [ ] 28. Decide on titanic-dataset fate
- [ ] Refresh Census 2022→2023 data (5-6h)
- [ ] Update UN CRPD data (1h)

---

## Key Blockers & Solutions

| Blocker | Severity | Solution | Timeline |
|---------|----------|----------|----------|
| HF token read-only | HIGH | Generate write-scoped token manually | 5 min before #19 |
| NASA URL 404 | HIGH | Research current catalog URL | 15 min |
| EEOC URL 404 | MEDIUM | Find current statistics page | 15 min |
| Metadata constraints | MEDIUM | Edit 2 files to fix format | 30 min |

---

## Agent Delegation Recommendations

### Use `/dataset-publish` Skill
- Tasks #18-19 (Kaggle/HF publication)
- Tasks #20-27 (HF batch README generation)
- **Efficiency gain**: Reduces per-dataset time from 30 min → 10 min

### Use `/humanize` Skill
- All README changes (before commit)
- All CHANGELOG creation (remove AI terminology)
- **Critical**: MANDATORY pre-commit for documentation

### Manual + Script
- Tasks #3-6: `python3 generate_notebook.py`
- Parallel execution possible (run all 3 notebooks simultaneously)

### Parallel Agents (Dream Swarm)
- All independent URL fixes: Launch together
- All notebook generation: Launch together
- All HF README generation: Launch together
- **Estimated speedup**: 4× faster vs sequential

---

## Reporting Locations

- **Full task queue**: `/home/coolhand/geepers/hive/datasets-queue.md`
- **Detailed planning report**: `/home/coolhand/geepers/reports/by-date/2026-02-16/planner-datasets.md`
- **Recommendations source**: `/home/coolhand/geepers/recommendations/by-project/datasets.md`
- **Accessibility Atlas TODO**: `/home/coolhand/datasets/accessibility-atlas/PRE_PUBLICATION_TODO.md`

---

## Success Metrics

Upon completion:

✅ All 28 datasets have valid metadata (Kaggle/HF compliant)
✅ No broken URLs in any dataset documentation
✅ 3 new Jupyter notebooks generated and tested
✅ Accessibility Atlas published (Kaggle + HuggingFace)
✅ 8 additional datasets on HuggingFace
✅ All changes committed with proper attribution
✅ Zero "AI" terminology in public docs (`/humanize` verified)

---

**Status**: READY FOR EXECUTION
**Recommended Start**: Phase 1 (3h quick wins)
**Expected Completion**: 2-3 days for critical path, 1 week for full queue

See `/home/coolhand/geepers/hive/datasets-queue.md` for detailed task descriptions with file paths and effort estimates.

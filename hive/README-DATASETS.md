# Dataset Publishing Workflow - Complete Guide

**Generated**: 2026-02-14 04:20 UTC
**Status**: Planning complete, ready for execution
**Effort**: 24-32 hours total (2.5 hours critical path)

---

## Start Here

### 1. Read These First (10 minutes)

1. **This file** (you are here) — Overview and navigation
2. `/home/coolhand/geepers/hive/DATASETS-SUMMARY.txt` — One-page executive summary
3. `/home/coolhand/geepers/hive/DATASETS-QUICK-REF.md` — Quick reference (gotchas, success metrics)

### 2. Full Task Queue (30 minutes)

- **File**: `/home/coolhand/geepers/hive/datasets-queue.md`
- **Length**: 21 KB (comprehensive)
- **Contains**: 18 prioritized tasks, dependencies, time estimates, validation checklists

### 3. Detailed Planning Report (30 minutes)

- **File**: `/home/coolhand/geepers/reports/by-date/2026-02-14/planner-datasets.md`
- **Length**: 15 KB (analysis-focused)
- **Contains**: Risk assessment, platform strategy, dependency mapping, success criteria

### 4. Original Sources (reference)

- **Blocking TODO**: `/home/coolhand/datasets/accessibility-atlas/PRE_PUBLICATION_TODO.md`
- **Audit Report**: `/home/coolhand/datasets/DATASET_AUDIT_2026-02-14.md`
- **Setup Checklist**: `/home/coolhand/datasets/world-languages/KAGGLE_SETUP.md`

---

## At a Glance

### What You'll Find

**In geepers/hive/**:
```
datasets-queue.md           ← 18 prioritized tasks (do this)
DATASETS-SUMMARY.txt        ← 1-page summary
DATASETS-QUICK-REF.md       ← Quick reference + gotchas
README-DATASETS.md          ← This file
```

**In geepers/reports/by-date/2026-02-14/**:
```
planner-datasets.md         ← Detailed planning report
```

**Source files** (in datasets directory):
```
accessibility-atlas/
  PRE_PUBLICATION_TODO.md   ← Specific blocking issues + fixes
DATASET_AUDIT_2026-02-14.md ← Full audit of 4 published repos
CLAUDE.md                   ← Project instructions
```

---

## The Problem

### Current State

- **18 datasets** across GitHub, HuggingFace, Kaggle
- **5 published** (2 on Kaggle, 3 on HuggingFace, 4 on GitHub)
- **9 ready to publish** (just need uploads)
- **4 need planning** (multi-file structures, consolidation decisions)

### Critical Blocker

**Accessibility Atlas licensing issue** (FIXED in queue):
- 2 datasets removed (WLASL, AAC vocabulary) due to licensing
- `dataset_index.json` still references deleted files
- Prevents publication to Kaggle + HuggingFace
- **Solution**: Task #1 in queue (1 hour to fix)

### Missing Metadata

Several datasets have HuggingFace YAML frontmatter but not all:
- US Inequality Atlas has warning on HF (Task #5)
- Language data needs dataset card (Task #8)
- Several geospatial datasets ready but not published (Task #7)

### No Refresh Automation

Datasets with API-driven updates (Census, Joshua Project, GDELT) lack:
- Automated quarterly refresh schedule
- Version bumping strategy
- HuggingFace + Kaggle sync workflows

---

## The Solution

### Phase 1: Unblock (2.5 hours)

**Monday morning** (critical path):

1. **Task #1** - Fix accessibility-atlas licensing (1 hour)
   - Edit 3 files, create 1 new file
   - Unblocks 2-3 dependent tasks
   - Fully specified in PRE_PUBLICATION_TODO.md

2. **Task #2** - Publish accessibility-atlas to Kaggle (30 min)
   - Use metadata template
   - Upload private, review, make public

3. **Task #3** - Publish accessibility-atlas to HuggingFace (30 min)
   - HUGGINGFACE_README.md exists (ready to use)
   - Add tags + test

4. **In parallel**:
   - Task #4: US Attention Data → HF (20 min)
   - Task #5: US Inequality fix YAML (10 min)
   - Task #6: Verify Disasters Kaggle (5 min)

**Result**: 6 quick wins completed, 3 critical issues resolved

### Phase 2: Expand (3.5 hours)

**Tuesday-Wednesday**:

5. **Task #7** - Publish 4 geospatial datasets (2 hours)
   - NOAA storms, meteorites, waterfalls, earthquakes
   - All have YAML frontmatter ready

6. **Task #13** - Complete world-languages Kaggle (40 min)
   - Setup checklist provided in KAGGLE_SETUP.md

7. **Task #8** - Plan language-data consolidation (1 hour)
   - Decision: single dataset or 2-3 focused?
   - Estimate publication time

**Result**: 9 total datasets published, ecosystem largely complete

### Phase 3: Hardening (5.5 hours)

**Thursday-Friday**:

8. **Task #12** - Sync automation (1.5 hours)
   - strange-places pipeline (HF → ~/datasets → data_trove)

9. **Task #16** - Refresh automation (2.5 hours)
   - Quarterly schedule for Census, Joshua Project
   - Version bumping workflow

10. **Task #18** - Governance docs (1.5 hours)
    - Formalize dataset lifecycle
    - Attribution + licensing policies

**Result**: Infrastructure ready for long-term maintenance

### Optional (Later)

- Task #9: DOI/citation metadata (3 hours)
- Task #10-11: Stale data refresh (5-7 hours)
- Task #15: `/dataset-publish` skill (3 hours)
- Task #14-17: Optional Kaggle publications (4 hours)

---

## Task Overview

### Quick Wins (High Priority)

| Task | Platform | Effort | Ready? | Status |
|------|----------|--------|--------|--------|
| #1: accessibility-atlas licensing | N/A | 1h | 🟡 Blocked | Fix dataset_index.json |
| #2: accessibility-atlas Kaggle | Kaggle | 30m | After #1 | Create metadata |
| #3: accessibility-atlas HF | HF | 30m | After #1 | Upload files |
| #4: us-attention-data HF | HF | 20m | ✅ | Use prepared README |
| #5: us-inequality YAML | HF | 10m | ✅ | Fix frontmatter |
| #6: disasters-mashup verify | Kaggle | 5m | ✅ | Check username |

### Medium Priority

| Task | Platform | Effort | Ready? | Status |
|------|----------|--------|--------|--------|
| #7: 4 geospatial HF | HF | 2h | ✅ | YAML ready |
| #8: language-data plan | Both | 1h | 🟡 Planning | Consolidation strategy |
| #9: citations/DOI | Both | 3h | ⚠️ Optional | Zenodo integration |
| #13: world-languages Kaggle | Kaggle | 40m | ✅ | Setup checklist |

### Infrastructure & Future

| Task | Type | Effort | Priority | Status |
|------|------|--------|----------|--------|
| #10: refresh automation | Build | 2.5h | Medium | Schedule + versioning |
| #11: strange-places sync | Build | 1.5h | Medium | 3-way pipeline |
| #12: stale data refresh | Update | 5-7h | Low | Census 2022→2023 |
| #15: `/dataset-publish` skill | Tool | 3h | Low | Batch publication |
| #16: governance docs | Docs | 1.5h | Low | Lifecycle policies |

---

## Platform Strategy

### HuggingFace (Primary)

**Best for**:
- Multi-file datasets (language-data, accessibility-atlas)
- Research-oriented collections (inequality, disasters)
- Time-series data (us-attention-data)
- API-refreshable datasets (quarterly updates)

**How to publish**:
1. Prepare README.md with YAML frontmatter
2. Create HF repo: `huggingface-cli repo create <name> --type dataset`
3. Upload files (Python API or Git)
4. Add tags + task categories via web UI
5. Test with `datasets.load_dataset()`

**Datasets (11 total)**:
- 3 published (inequality, disasters-mashup, joshua-project)
- 8 ready (attention-data, geospatial ×4, accessibility-atlas, world-languages, language-data)

### Kaggle (Secondary)

**Best for**:
- Single large CSV/JSON (disasters-mashup)
- ML competitions + data viz (geospatial)
- Broader discovery
- Kaggle Kernels community

**How to publish**:
1. Generate metadata: `kaggle datasets init -p .`
2. Edit dataset-metadata.json (template provided)
3. Upload private: `kaggle datasets create -p . --dir-mode zip`
4. Review on web UI
5. Make public
6. Test download: `kaggle datasets download -d username/name`

**Datasets (4 total)**:
- 2 published (joshua-project, disasters-mashup)
- 2 optional (attention-data, inequality-atlas)

### GitHub (Source of Truth)

**All datasets**:
- 4 published repos (separate .git remotes)
- 14 local datasets (in ~/datasets/)
- Source for data pipelines + scripts
- Version control for schemas
- Issue tracking for quality

---

## Critical Success Factors

### Before Publishing

1. **Validate JSON/CSV**
   ```bash
   python3 -c "import json; json.load(open('file.json'))"
   ```

2. **Check licensing**
   - Source data public domain or properly licensed
   - Attribution clear in README
   - License matches platform terms

3. **Verify record counts**
   - Match documentation
   - Validate with `wc -l` or pandas

4. **Add YAML frontmatter** (HuggingFace)
   ```yaml
   ---
   license: cc0-1.0
   tags: [your, tags, here]
   ---
   ```

### After Publishing

1. **Test downloads**
   - HuggingFace: `from datasets import load_dataset("lukeslp/name")`
   - Kaggle: `kaggle datasets download -d username/name`

2. **Verify on web**
   - Check metadata displays correctly
   - Verify file counts match
   - Confirm tags appear

3. **Document in git**
   - Update PUBLISH_STATUS.md or similar
   - Tag releases if applicable

---

## Success Metrics

### Week 1 (Critical Path)

- [ ] Accessibility atlas licensing fixed
- [ ] 6 quick wins published
- [ ] 3 critical issues resolved
- [ ] All JSON/CSV validated
- [ ] All platforms tested

### End of Month

- [ ] 12+ datasets published
- [ ] 0 critical blockers
- [ ] Refresh automation operational
- [ ] All publications documented

### Q1 2026

- [ ] 18/18 datasets published or published-ready
- [ ] Governance policy documented
- [ ] `/dataset-publish` skill available
- [ ] Quarterly refresh cycle established

---

## Quick Reference

### File Locations

**Task queue**: `/home/coolhand/geepers/hive/datasets-queue.md` (21 KB)
**This guide**: `/home/coolhand/geepers/hive/README-DATASETS.md`
**Summary**: `/home/coolhand/geepers/hive/DATASETS-SUMMARY.txt`
**Quick ref**: `/home/coolhand/geepers/hive/DATASETS-QUICK-REF.md`
**Report**: `/home/coolhand/geepers/reports/by-date/2026-02-14/planner-datasets.md`

**Source files**:
- Blocking TODO: `/home/coolhand/datasets/accessibility-atlas/PRE_PUBLICATION_TODO.md`
- Audit: `/home/coolhand/datasets/DATASET_AUDIT_2026-02-14.md`
- Setup: `/home/coolhand/datasets/world-languages/KAGGLE_SETUP.md`

### Commands

**Validate JSON**:
```bash
python3 -c "import json; json.load(open('file.json'))"
```

**Create HF repo**:
```bash
huggingface-cli repo create <name> --type dataset
```

**Create Kaggle metadata**:
```bash
kaggle datasets init -p .
```

**Upload to Kaggle (private)**:
```bash
kaggle datasets create -p . --dir-mode zip
```

**Test HF download**:
```bash
from datasets import load_dataset
ds = load_dataset("lukeslp/dataset-name")
```

---

## Frequently Asked Questions

### How long will this take?

- **Critical blocker only**: 1 hour (Task #1)
- **Critical + quick wins**: 2.5 hours (Tasks 1-6)
- **Full ecosystem**: 8-12 hours (Tasks 1-9)
- **With infrastructure**: 24-32 hours (all tasks)

### Do I need to publish to both HuggingFace and Kaggle?

No. Use this matrix:
- **HuggingFace primary** for research, multi-file, API-driven
- **Kaggle secondary** for ML, single-file, broader audience
- **Both** only for public domain, broad impact datasets

### What if I'm missing YAML frontmatter?

HuggingFace shows a yellow warning but still works. Add YAML block to README:
```yaml
---
license: cc0-1.0
tags: [tags, here]
---
```

See Task #5 for example (us-inequality-atlas).

### How do I set up automated refreshes?

See Task #16 (refresh automation, 2.5 hours).
Includes cron job templates for Census, Joshua Project, GDELT.

### Can I publish to Kaggle without HuggingFace?

Yes, but not recommended. HuggingFace better for multi-file + research.
Use Kaggle as secondary for broader reach.

### What if a dataset is already published?

Check the platform-specific status in task queue.
- If already on both: verify consistency (Task #6 does this)
- If on one platform: publish to other (Tasks #2-3, #4, #7)

---

## Next Steps

### Right Now (5 minutes)

1. Read DATASETS-SUMMARY.txt (2 min)
2. Read DATASETS-QUICK-REF.md (3 min)

### Today (1-2 hours)

3. Read full task queue (/home/coolhand/geepers/hive/datasets-queue.md)
4. Execute Task #1 (fix accessibility-atlas licensing)

### This Week (8-12 hours)

5. Execute Tasks #2-7 (publish 6 quick wins + 4 geospatial)
6. Complete Task #8 (language-data planning)

### Next Week (5+ hours)

7. Execute Tasks #12, #16, #18 (infrastructure)
8. Optional: Tasks #9-11 (citations, refresh, governance)

---

## Support

### If you get stuck

1. Check DATASETS-QUICK-REF.md (gotchas section)
2. Read task details in datasets-queue.md
3. Read original source file (linked in each task)
4. Follow exact steps in PRE_PUBLICATION_TODO.md (Task #1)

### If you have questions

- **Why this order?**: See "Dependency Analysis" in planner report
- **How long per task?**: See "Effort Estimation" in task queue
- **What about X dataset?**: Check platform strategy matrix above
- **Which platform?**: See DATASET_AUDIT_2026-02-14.md (platform comparison)

---

## Timeline Summary

```
📅 Monday:  Task #1 (1h) + Tasks #2-6 parallel (1.5h) = 2.5h total
📅 Tuesday: Task #7 (2h) + Task #13 (40m) = 2.5-3h total
📅 Wednesday: Task #8 planning (1h) = done by EOD
📅 Thursday-Friday: Tasks #12, #16, #18 (5.5h) = infrastructure ready
📅 Later: Optional Tasks #9-11, #15 = enhancements
```

**Critical path completion**: Wednesday EOD
**Full ecosystem**: End of month

---

## Handoff Checklist

When passing to another person:

- [ ] They've read DATASETS-SUMMARY.txt
- [ ] They've read DATASETS-QUICK-REF.md
- [ ] They have access to all source files
- [ ] They understand Task #1 (critical blocker)
- [ ] They know platform strategy (HF primary, Kaggle secondary)
- [ ] They can run validation commands
- [ ] They know where to find help

---

**Planning completed**: 2026-02-14 04:20 UTC
**Ready for execution**: Now
**Next review**: After Task #1 completion

---

## Document Hierarchy

```
README-DATASETS.md (this file)
├── DATASETS-SUMMARY.txt (2 min read)
├── DATASETS-QUICK-REF.md (5 min read)
├── datasets-queue.md (30 min read, full details)
└── planner-datasets.md (analysis + risk assessment)

Source files (for reference):
├── /home/coolhand/datasets/accessibility-atlas/PRE_PUBLICATION_TODO.md
├── /home/coolhand/datasets/DATASET_AUDIT_2026-02-14.md
└── /home/coolhand/datasets/CLAUDE.md
```

**Start with this file, then pick your level**: summary (2 min), quick ref (5 min), full queue (30 min), or report (analysis).

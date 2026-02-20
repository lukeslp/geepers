# Task Queue: Dataset Publishing Workflow

**Generated**: 2026-02-14 08:45
**Total Tasks**: 18
**Quick Wins**: 6
**Blocked**: 0
**Estimated Total Effort**: 24-32 hours

---

## Executive Summary

The dataset ecosystem consists of **18 datasets** across three categories:
- **4 GitHub-primary repos** (with separate .git remotes): external distribution on HuggingFace, Kaggle
- **14 local datasets** in `/home/coolhand/datasets/`: unpublished or publishing-ready
- **Issues**: Incomplete publications, missing metadata, stale data, licensing gaps

**Minimum viable action**: Fix accessibility-atlas licensing issues + publish us-attention-data to HuggingFace = **2 hours**

**Recommended action**: Complete all blocking issues + publish remaining ready datasets = **8-12 hours**

---

## Ready to Build (Priority Order)

### 1. [QW] Fix Accessibility Atlas Licensing Issues

- **Source**: `/home/coolhand/datasets/accessibility-atlas/PRE_PUBLICATION_TODO.md:1-160`
- **Impact**: 5 | **Effort**: 1 | **Priority**: 9.0
- **Status**: BLOCKING - prevents publication
- **Description**: Edit 4 files to remove references to 2 deleted datasets (WLASL, AAC vocabulary) and update counts from 55→53

**Changes required**:
1. **dataset_index.json**: Remove `local_file` refs to deleted files, add `access: "Public download"` notes (3 edits, ~10 min)
2. **README.md**: Change badge from "55" to "53" datasets (1 line, 1 min)
3. **Create CHANGELOG.md**: Document removed files with rationale (new file, 10 min)
4. **Add license clarification section to README** (optional but recommended, 5 min)

**Files affected**:
- `/home/coolhand/datasets/accessibility-atlas/dataset_index.json` (lines 314, 362, 6)
- `/home/coolhand/datasets/accessibility-atlas/README.md` (lines 8, 3)
- `/home/coolhand/datasets/accessibility-atlas/CHANGELOG.md` (new file)

**Validation checklist**:
- [ ] `dataset_index.json` validates with `python3 -c "import json; json.load(open('dataset_index.json'))"`
- [ ] No `local_file` references to wlasl_index.csv or aac_vocabulary_data.json
- [ ] Badge shows "53" not "55"
- [ ] Removed files confirmed deleted: `ls /home/coolhand/datasets/accessibility-atlas/wlasl_index.csv` should fail

**Next steps**: After this, can proceed with Kaggle/HuggingFace publication (Task #2)

---

### 2. [QW] Publish Accessibility Atlas to Kaggle

- **Source**: `/home/coolhand/datasets/accessibility-atlas/PRE_PUBLICATION_TODO.md:205-232`
- **Impact**: 4 | **Effort**: 2 | **Priority**: 8.0
- **Depends on**: Task #1 (licensing fixes)
- **Status**: READY after Task #1
- **Description**: Create Kaggle metadata, upload as private, review, then make public

**Steps**:
1. Generate Kaggle metadata: `kaggle datasets init -p /home/coolhand/datasets/accessibility-atlas`
2. Edit dataset-metadata.json (5 fields, templated in PRE_PUBLICATION_TODO.md)
3. Upload private: `kaggle datasets create -p . --dir-mode zip`
4. Review on https://www.kaggle.com/settings/datasets (verify files + metadata)
5. Make public via web UI
6. Test download and load

**Files to create**:
- `/home/coolhand/datasets/accessibility-atlas/dataset-metadata.json`

**Validation**:
- [ ] Kaggle dataset page loads at https://www.kaggle.com/datasets/lucassteuber/accessibility-atlas
- [ ] All 41 files present
- [ ] Metadata displays correctly
- [ ] Public badge appears

**Time estimate**: 10 min generation + 5 min review + 5 min testing = 20 min

---

### 3. [QW] Publish Accessibility Atlas to HuggingFace

- **Source**: `/home/coolhand/datasets/accessibility-atlas/PRE_PUBLICATION_TODO.md:234-257`
- **Impact**: 4 | **Effort**: 2 | **Priority**: 7.8
- **Depends on**: Task #1 (licensing fixes)
- **Status**: READY after Task #1
- **Description**: Create HF repo, upload files, add tags

**Steps**:
1. Create HF dataset repo: `huggingface-cli repo create accessibility-atlas --type dataset`
2. Upload folder using Python API (templated in PRE_PUBLICATION_TODO.md)
3. Add tags via web UI: disability, accessibility, census, employment, web-accessibility, wcag, ada, healthcare, education, international
4. Test dataset loading with `datasets` library

**Files involved**:
- `/home/coolhand/datasets/accessibility-atlas/HUGGINGFACE_README.md` (already prepared)
- All 41 data files

**Validation**:
- [ ] HF dataset page: https://huggingface.co/datasets/lukeslp/accessibility-atlas
- [ ] README displays properly
- [ ] Download works: `from datasets import load_dataset; ds = load_dataset("lukeslp/accessibility-atlas")`

**Time estimate**: 15 min creation + 10 min tagging + 5 min testing = 30 min

---

### 4. [QW] Publish US Attention Data to HuggingFace

- **Source**: `/home/coolhand/datasets/DATASET_AUDIT_2026-02-14.md:83-145`
- **Impact**: 4 | **Effort**: 1 | **Priority**: 8.0
- **Status**: READY NOW (HUGGINGFACE_README.md already prepared)
- **Description**: Use existing HUGGINGFACE_README.md to publish 4.3 MB attention dataset

**Steps**:
1. Create HF repo: `huggingface-cli repo create us-attention-data --type dataset`
2. Upload using Python API with existing HUGGINGFACE_README.md
3. Add YAML frontmatter: `attention`, `wikipedia`, `google-trends`, `gdelt`, `time-series`, `media-analysis`
4. Add task categories: `time-series-forecasting`, `feature-extraction`
5. Test loading with `datasets` library

**Files involved**:
- `/home/coolhand/datasets/us-attention-data/HUGGINGFACE_README.md` (existing)
- 10 JSON files + metadata

**Why this is quick**: HUGGINGFACE_README.md already written, just needs upload

**Validation**:
- [ ] HF dataset: https://huggingface.co/datasets/lukeslp/us-attention-data
- [ ] Download works: `datasets.load_dataset("lukeslp/us-attention-data")`
- [ ] Tags appear on dataset page

**Time estimate**: 10 min upload + 5 min tagging + 5 min testing = 20 min

---

### 5. [QW] Fix US Inequality Atlas HuggingFace YAML

- **Source**: `/home/coolhand/datasets/DATASET_AUDIT_2026-02-14.md:27-79`
- **Impact**: 3 | **Effort**: 1 | **Priority**: 7.0
- **Status**: READY NOW (already published, just needs YAML fix)
- **Description**: Add proper YAML frontmatter to existing HF dataset README to clear validation warning

**Changes**:
1. Add YAML block to `/home/coolhand/datasets/us-inequality-atlas/README.md` (at line 1):
   ```yaml
   ---
   license: mit
   task_categories:
     - feature-extraction
   tags:
     - inequality
     - census
     - counties
     - healthcare
     - food-deserts
     - fips
     - united-states
   size_categories:
     - 1K<n<10K
   ---
   ```
2. Update HuggingFace repo with new README

**Files**:
- `/home/coolhand/datasets/us-inequality-atlas/README.md`

**Validation**:
- [ ] No YAML warning on https://huggingface.co/datasets/lukeslp/us-inequality-atlas
- [ ] Tags appear: inequality, census, counties, healthcare, food-deserts, fips

**Time estimate**: 5 min edit + 5 min HF sync = 10 min

---

### 6. [QW] Verify US Disasters Mashup Kaggle Username

- **Source**: `/home/coolhand/datasets/DATASET_AUDIT_2026-02-14.md:207-267`
- **Impact**: 3 | **Effort**: 1 | **Priority**: 6.5
- **Status**: READY NOW
- **Description**: Check username inconsistency (lucassteuber vs lukeslp) on Kaggle

**Action**:
1. Visit https://www.kaggle.com/datasets/lucassteuber/us-disasters-mashup
2. Check if account is unified with lukeslp
3. If inconsistent: Either update to lukeslp or create redirect

**Validation**:
- [ ] Kaggle dataset accessible and matches GitHub version
- [ ] Dataset description matches /home/coolhand/datasets/us-disasters-mashup/README.md

**Time estimate**: 5 min investigation

---

## Medium Priority (High Impact, Medium Effort)

### 7. Publish Remaining Unpublished Geospatial Datasets

- **Source**: Local dataset audit
- **Impact**: 4 | **Effort**: 3 | **Priority**: 6.5
- **Status**: READY (docs prepared, data exists)
- **Description**: Publish 4 geospatial datasets with HuggingFace YAML frontmatter already in place

**Datasets**:
- `noaa-significant-storms/` - 14,770 records, CC0, YAML ready
- `large-meteorites/` - 4,871 records, CC0, YAML ready
- `waterfalls-worldwide/` - 80,000+ records, CC0, YAML ready
- `usgs-significant-earthquakes/` - ~3,700 records, CC0, YAML ready (similar to disasters-mashup)

**Platform strategy**:
- **Primary**: HuggingFace (YAML frontmatter already in README.md files)
- **Secondary**: Kaggle (optional, but good for ML audience)

**Steps per dataset** (~30 min each):
1. Create HF repo: `huggingface-cli repo create <name> --type dataset`
2. Upload with existing README.md
3. Add task category + tags via web UI
4. Test loading

**Estimated time**: 2 hours total (4 datasets × 30 min)

**Validation per dataset**:
- [ ] HF dataset loads: `datasets.load_dataset("lukeslp/<name>")`
- [ ] Tags visible on dataset page
- [ ] Record count matches README

**Next action**: Use `/dataset-publish` skill for batch publication

---

### 8. Consolidate Language Data Datasets

- **Source**: `/home/coolhand/datasets/language-data/`
- **Impact**: 4 | **Effort**: 3 | **Priority**: 6.0
- **Status**: NEEDS PLANNING
- **Description**: Publish multi-source linguistic data collection (23,740 languages across 7 core files)

**Current state**:
- ✅ Multiple curated CSVs (Glottolog, WALS, PHOIBLE)
- ✅ Integration work (world_languages_integrated.json)
- ✅ Subdirectories (language-families/, historical-corpora/, reference-corpora/)
- ❌ Not published to HuggingFace
- ❌ No YAML frontmatter
- ❌ No dataset card

**Challenges**:
- Multi-file structure (complex for single dataset)
- Could be 3 separate datasets: core linguistic, language families, historical corpora
- OR single multi-table dataset with subdirectories

**Approach**:
1. **Decision**: Split into 2-3 focused datasets or keep as single large collection?
2. Create YAML frontmatter (tags: linguistics, nlp, language-families, glottolog, wals, phoible)
3. Create dataset card with loading examples
4. Publish to HuggingFace

**Time estimate**: 1 hour planning + 2 hours publication = 3 hours

---

### 9. Create Citation/DOI Metadata for Published Datasets

- **Source**: Audit findings
- **Impact**: 4 | **Effort**: 2 | **Priority**: 5.5
- **Status**: OPTIONAL but recommended
- **Description**: Generate DOI/citation metadata for datasets published on HuggingFace and Kaggle

**Datasets that need citations**:
- accessibility-atlas
- us-attention-data
- us-disasters-mashup (already has CC0)
- geospatial datasets (storm, meteorite, waterfalls, earthquakes)

**Tools**:
- Zenodo integration (free DOI for research data)
- HuggingFace BibTeX citations (automatic)
- Kaggle citations (automatic)

**Time estimate**: 30 min per dataset = 3+ hours total

**Lower priority**: Can do after initial publications

---

## Stale Data (Quality Enhancement)

### 10. Refresh Accessibility Atlas Census Data (Optional)

- **Source**: `/home/coolhand/datasets/accessibility-atlas/PRE_PUBLICATION_TODO.md:164-177`
- **Impact**: 3 | **Effort**: 4 | **Priority**: 3.0
- **Status**: DEFERRED (nice-to-have before publication)
- **Description**: Update 4 Census Bureau files from 2022 → 2023 data

**Files to update**:
- `census_disability_by_age_sex_2022.json` → 2023
- `census_disability_by_race_2022.json` → 2023
- `census_disability_characteristics_2022.json` → 2023
- `census_disability_national_trends.json` → 2023

**Source**: https://data.census.gov/table/ACSST1Y2023.S1810

**Time estimate**: 4-6 hours (API calls, data processing, testing)

**Recommendation**: Publish v1.0 with 2022 data, then release v1.1 with 2023 refresh after 2-3 months

---

### 11. Update UN CRPD Ratification Data

- **Source**: `/home/coolhand/datasets/accessibility-atlas/PRE_PUBLICATION_TODO.md:179-184`
- **Impact**: 2 | **Effort**: 2 | **Priority**: 2.5
- **Status**: DEFERRED (very stale, 14 years old)
- **Description**: Refresh UN CRPD dataset from 2012 baseline

**File**: `un_crpd_ratification.json`

**Source**: https://treaties.un.org/Pages/ViewDetails.aspx?src=TREATY&mtdsg_no=IV-15

**Time estimate**: 1 hour research + 1 hour data processing

**Recommendation**: Defer to v1.1 release cycle (low user impact, high effort)

---

## Discovery & Syncing

### 12. Sync Strange Places Mysterious Phenomena

- **Source**: `/home/coolhand/datasets/strange-places-mysterious-phenomena/SYNC_NOTES.md`
- **Impact**: 3 | **Effort**: 2 | **Priority**: 5.0
- **Status**: OPERATIONAL (but needs documentation)
- **Description**: Maintain 3-way sync: HF repo → ~/datasets/ → data_trove → interactive viz

**Locations**:
1. **HuggingFace** (master): https://huggingface.co/datasets/lukeslp/strange-places-mysterious-phenomena
2. **Local master**: `/home/coolhand/datasets/strange-places-mysterious-phenomena/` (clone from HF)
3. **Data trove**: `/home/coolhand/html/datavis/data_trove/published/hf/strange-places-mysterious-phenomena/`
4. **Interactive viz**: `/home/coolhand/html/datavis/interactive/strange-places/data/phenomena.json` (27MB processed)

**Sync workflow**:
- When HF updates → `git pull` in ~/datasets/
- When ~/datasets updates → copy to data_trove/
- When viz needs refresh → process dataset → update phenomena.json

**Action items**:
1. Create sync script (automated pull from HF) - 30 min
2. Document quarterly refresh schedule - 15 min
3. Set up data_trove copy automation - 30 min

**Time estimate**: 1.5 hours

---

### 13. Document World Languages Dataset Strategy

- **Source**: `/home/coolhand/datasets/world-languages/KAGGLE_SETUP.md`
- **Impact**: 2 | **Effort**: 1 | **Priority**: 4.0
- **Status**: READY (KAGGLE_SETUP.md exists but incomplete)
- **Description**: Complete Kaggle setup for world-languages dataset

**Action items**:
1. Upload cover image (1200x630px) - 10 min
2. Fill remaining Kaggle metadata fields per KAGGLE_SETUP.md - 10 min
3. Create/update HuggingFace dataset card - 20 min
4. Delete KAGGLE_SETUP.md after completion (per instructions in file)

**Files**:
- `/home/coolhand/datasets/world-languages/KAGGLE_SETUP.md` (to delete after)

**Time estimate**: 40 min total

---

## Blocked / Deferred

### 14. Consider Kaggle for US Attention Data (Optional)

- **Source**: `/home/coolhand/datasets/DATASET_AUDIT_2026-02-14.md:316-321`
- **Impact**: 3 | **Effort**: 2 | **Priority**: 3.5
- **Status**: OPTIONAL
- **Decision needed**: Does JSON format + attention analysis appeal to Kaggle's ML audience?

**Rationale for publishing**:
- Broader ML/data science reach
- Kaggle Kernels community
- Competition opportunities (time-series forecasting)

**Rationale against**:
- JSON not ideal for Kaggle's CSV preview
- HuggingFace better suited for time-series research

**Recommendation**: Publish to HuggingFace first (Task #4), then gauge interest before Kaggle

---

### 15. Consider Kaggle for US Inequality Atlas (Optional)

- **Source**: `/home/coolhand/datasets/DATASET_AUDIT_2026-02-14.md:323-327`
- **Impact**: 3 | **Effort**: 2 | **Priority**: 3.0
- **Status**: OPTIONAL
- **Decision needed**: Multi-file structure (5 subdirs) less convenient for Kaggle; better on HuggingFace

**Rationale for Kaggle**:
- Data visualization community
- Tableau/PowerBI users
- County-level data good for mapping competitions

**Rationale against**:
- Multi-file structure awkward in Kaggle's interface
- HuggingFace file browser better for navigation
- Already on HuggingFace with good engagement

**Recommendation**: Stay HuggingFace-primary; Kaggle secondary only if resources available

---

## Infrastructure

### 16. Set Up Automated Dataset Refresh Cycle

- **Source**: `/home/coolhand/datasets/DATASET_AUDIT_2026-02-14.md:328-334`
- **Impact**: 4 | **Effort**: 3 | **Priority**: 4.5
- **Status**: PLANNING ONLY
- **Description**: Establish quarterly refresh schedule for API-driven datasets

**Datasets with update potential**:
- joshua-project-data: Quarterly (Python script exists: `fetch_all_datasets.py`)
- us-inequality-atlas: Annually (Census ACS releases March)
- us-attention-data: Weekly (API sources continual; already implemented?)
- us-disasters-mashup: Quarterly (NTSB, NOAA, USGS releases)

**Actions**:
1. Create cron/scheduler entry per dataset - 30 min
2. Test refresh pipeline - 1 hour
3. Document version bumping process (HF + Kaggle) - 30 min
4. Create notification system for new versions - 30 min

**Time estimate**: 2.5 hours

**Lower priority**: Can implement after initial publications

---

### 17. Create Dataset Publishing Checklist Skill

- **Source**: Cross-cutting concern
- **Impact**: 4 | **Effort**: 2 | **Priority**: 4.0
- **Status**: PLANNING ONLY
- **Description**: Build `/dataset-publish` skill (Claude skill) to automate publication workflow

**Features**:
- Interactive checklist for licensing verification
- Automated metadata generation (YAML frontmatter)
- Batch upload to HuggingFace + Kaggle
- Citation/DOI generation
- Post-publication testing script

**Time estimate**: 2-3 hours to build skill

**Value**: Reduces per-dataset publication time from 1 hour → 15 min

**Note**: Referenced in CLAUDE.md but not yet built

---

## Ongoing Maintenance

### 18. Establish Dataset Governance

- **Source**: Architecture observation
- **Impact**: 5 | **Effort**: 2 | **Priority**: 3.5
- **Status**: PLANNING ONLY
- **Description**: Formalize dataset lifecycle: creation → publication → versioning → maintenance

**Policies to document**:
1. **Creation**: Data sources must be public domain or clearly licensed
2. **Publication**: Minimum standards (README, metadata, validation)
3. **Versioning**: Semantic versioning for dataset updates
4. **Maintenance**: 6-month review cycle per published dataset
5. **Attribution**: Always credit source data + Luke Steuber

**Locations**:
- `/home/coolhand/datasets/GOVERNANCE.md` (new file)
- Update `/home/coolhand/datasets/CLAUDE.md` with standards

**Time estimate**: 1-1.5 hours

---

## Statistics

| Category | Count | Hours |
|----------|-------|-------|
| **Quick Wins (1-2 hour tasks)** | 6 | 8 |
| **Medium (2-4 hours)** | 4 | 12 |
| **Large (4+ hours)** | 2 | 10 |
| **Optional/Deferred** | 6 | 12+ |
| **Total Actionable** | 12 | 24-32 |

### Priority Breakdown

| Priority Range | Tasks | Est. Hours | Notes |
|---|---|---|---|
| 8.0-9.0 (Critical) | 3 | 1.5 | License fixes, HF publication |
| 6.5-7.8 (High) | 3 | 1.5 | Secondary HF publications |
| 5.0-6.0 (Medium) | 4 | 8-10 | Geospatial datasets, infrastructure |
| 3.0-4.5 (Low) | 2 | 4-6 | Stale data, optional Kaggle |

---

## Recommended Execution Plan

### Week 1: Launch (High Priority)

**Day 1 - Monday (4 hours)**:
1. Task #1: Fix accessibility-atlas licensing (1 hour) ✓ QW
2. Task #2: Publish accessibility-atlas to Kaggle (30 min) ✓ QW
3. Task #3: Publish accessibility-atlas to HuggingFace (30 min) ✓ QW
4. Task #4: Publish us-attention-data to HuggingFace (20 min) ✓ QW
5. Task #5: Fix us-inequality-atlas YAML (10 min) ✓ QW
6. Task #6: Verify us-disasters-mashup Kaggle username (5 min) ✓ QW

**Subtotal**: 2+ hours, all critical issues resolved ✅

**Day 2-3 - Tuesday-Wednesday (4 hours)**:
7. Task #7: Publish 4 geospatial datasets to HuggingFace (2 hours)
8. Task #13: Complete world-languages Kaggle setup (30 min)
9. Task #8: Plan language-data consolidation strategy (1 hour)

**Subtotal**: 3.5 hours, ecosystem largely published ✅

### Week 2: Hardening (Medium Priority)

10. Task #12: Sync strange-places data pipeline (1.5 hours)
11. Task #16: Set up automated refresh cycle (2.5 hours)
12. Task #18: Establish governance documentation (1.5 hours)

**Subtotal**: 5.5 hours

### Later: Optional Enhancements

- Task #9: Create DOI citations (3+ hours)
- Task #10-11: Refresh stale data (5-7 hours, defer to v1.1)
- Task #14-15: Optional Kaggle publications (4 hours)
- Task #17: Build `/dataset-publish` skill (3 hours)

---

## Completion Checklist

When this queue is complete:

- [ ] Accessibility atlas published (Kaggle + HuggingFace)
- [ ] US attention data published to HuggingFace
- [ ] US inequality atlas YAML fixed
- [ ] US disasters mashup username verified
- [ ] 4 geospatial datasets published (storms, meteorites, waterfalls, earthquakes)
- [ ] World languages Kaggle setup complete
- [ ] Strange places sync pipeline documented
- [ ] Automated refresh cycle configured
- [ ] Dataset governance policies documented
- [ ] All JSON files validated
- [ ] All publications tested (download + load)
- [ ] GitHub repos cleaned and committed

---

## Key References

- **Accessibility Atlas TODO**: `/home/coolhand/datasets/accessibility-atlas/PRE_PUBLICATION_TODO.md`
- **Audit Report**: `/home/coolhand/datasets/DATASET_AUDIT_2026-02-14.md`
- **Publishing Skill**: `/dataset-publish` (not yet implemented)
- **Project CLAUDE.md**: `/home/coolhand/datasets/CLAUDE.md`

---

**Next action**: Execute Task #1 (licensing fixes) to unblock publication tasks

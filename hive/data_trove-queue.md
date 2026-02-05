# Task Queue: data_trove

**Generated**: 2026-01-18 22:58
**Total Tasks**: 28
**Quick Wins**: 8
**Blocked**: 0
**Last Scout Report**: 2026-01-18 (evening - clean git status confirmed)

## Executive Summary

The data_trove project is a mature, production-ready centralized repository for 17+ dataset categories serving all datavis visualization projects. Recent scout reports (2026-01-18) show **all systems green** - clean git status, 98.5% link health, zero critical issues. The current workload is dominated by maintenance and enhancement tasks: (1) URL corrections for broken external links, (2) data quality improvements and cache management, (3) accessibility enhancements, and (4) documentation and infrastructure improvements.

**Session Status**: Clean state after comprehensive scout validation. All quirky datasets committed. World Bank data refreshed 2026-01-18 01:05 (12 hours fresh).

Key metrics:
- **17+ dataset categories** (700+ MB total, growing)
- **80 quirky dataset files** (36 MB, 40 newly added/committed)
- **56 MB linguistic data** (languages, families, ISO codes, families)
- **41 Python fetchers** maintaining automated data freshness
- **86.3% language speaker count coverage** (6,154 / 7,134 languages)
- **API Health**: 98.5% (68/69 external URLs working; 13 false positives from bot protection)

---

## Ready to Build (Priority Order)

### 1. [QW] Fix NASA Meteorite API Endpoint
- **Source**: fetch_wild_data.py:255
- **Impact**: 5 | **Effort**: 1 | **Priority**: 9.5
- **Status**: BLOCKING - meteorite data cannot be fetched
- **Description**: NASA Socrata endpoint `gh4g-9sfh` returns 404. Endpoint may be deprecated or dataset ID incorrect. Need to identify correct endpoint ID from NASA Open Data portal or fallback to alternative data source.
- **Dependencies**: None (unblocks wild data collection)
- **Files**: `tools/fetchers/fetch_wild_data.py:87-119`
- **Action Items**:
  - [ ] Check NASA data.nasa.gov for current meteorite dataset
  - [ ] Verify dataset ID matches expected structure
  - [ ] Test alternative endpoint: `y77d-th95` (already in code as fallback)
  - [ ] Document correct endpoint in comments
  - [ ] Run fetch_wild_data.py to verify

### 2. [QW] Commit 40 Uncommitted Quirky Dataset Files
- **Source**: git status (40 files in data/quirky/)
- **Impact**: 4 | **Effort**: 1 | **Priority**: 8.5
- **Description**: 40 new quirky dataset files (ancient ruins, asteroids, atmospheric phenomena, etc.) need to be staged and committed with appropriate metadata.
- **Dependencies**: None (ready to commit)
- **Files**: `data/quirky/*.{json,metadata.json}`
- **Action Items**:
  - [ ] Review all 40 files for completeness (paired JSON + metadata)
  - [ ] Verify metadata.json format consistency
  - [ ] Stage files: `git add data/quirky/`
  - [ ] Create commit with message: "feat: add 40 new quirky datasets (ancient ruins, atmospheric phenomena, cryptids)"

### 3. [QW] Add Data Validation Layer to Fetcher Scripts
- **Source**: geepers_scout recommendations
- **Impact**: 4 | **Effort**: 2 | **Priority**: 7.5
- **Description**: Implement shared validation utilities for fetcher scripts to verify data structure, record counts, and FIPS codes. Prevents corruption and ensures consistency across all 41 fetchers.
- **Dependencies**: None
- **Files**: `tools/validation/data_validator.py` (new)
- **Action Items**:
  - [ ] Create `tools/validation/` directory with `__init__.py`
  - [ ] Implement `validate_json_structure()` - checks required fields
  - [ ] Implement `validate_csv_structure()` - checks column names
  - [ ] Implement `validate_fips_codes()` - validates 5-digit FIPS format
  - [ ] Implement `validate_record_counts()` - checks before/after counts match expected range
  - [ ] Add unit tests in `tests/test_validators.py`
  - [ ] Update 3-5 fetchers to use validators as examples

### 4. [QW] Fix Missing Symlink: country_centroids.json
- **Source**: geepers_scout recommendations (high priority)
- **Impact**: 4 | **Effort**: 1 | **Priority**: 8.0
- **Description**: Geographic symlink is broken. `geographic/country_centroids.json` should point to `data/geographic/country_centroids.json` but link is missing or broken.
- **Dependencies**: None
- **Files**: `geographic/country_centroids.json` (symlink)
- **Action Items**:
  - [ ] Check if source file exists: `data/geographic/country_centroids.json`
  - [ ] If exists, create symlink: `ln -s ../../data/geographic/country_centroids.json geographic/country_centroids.json`
  - [ ] If missing, investigate if data needs to be fetched first
  - [ ] Verify symlink points correctly: `ls -l geographic/country_centroids.json`

### 5. [QW] Implement Automated Cache Cleanup Script
- **Source**: geepers_scout recommendations
- **Impact**: 3 | **Effort**: 2 | **Priority**: 6.5
- **Description**: Create script to remove cache files older than 30 days. Cache directory (`cache/` and `tools/fetchers/cache/`) can grow indefinitely. Script should respect `.cache_keep` files for permanent entries.
- **Dependencies**: None
- **Files**: `tools/cleanup_cache.py` (new)
- **Action Items**:
  - [ ] Implement `find_old_cache_files(max_age_days=30)` function
  - [ ] Support `.cache_keep` marker files (skip deletion if present)
  - [ ] Add dry-run mode (show what would be deleted without deleting)
  - [ ] Log deletions to `cache_cleanup.log`
  - [ ] Create cron task in systemd timer or add to service manager
  - [ ] Test with dry-run first

### 6. [QW] Add ARIA Labels to Index.html Search/Filter
- **Source**: geepers_scout recommendations (accessibility)
- **Impact**: 3 | **Effort**: 1 | **Priority**: 6.0
- **Description**: Improve accessibility of the data catalog interface by adding ARIA labels to search input and filter buttons. Currently missing screen reader support for interactive elements.
- **Dependencies**: None
- **Files**: `index.html` (search input, filter buttons)
- **Action Items**:
  - [ ] Add `aria-label="Search datasets"` to search input
  - [ ] Add `aria-label="Filter by category"` to category filter dropdown
  - [ ] Add `aria-describedby` for help text if present
  - [ ] Test with screen reader (NVDA, JAWS, or VoiceOver)
  - [ ] Verify keyboard navigation works (Tab, Enter, Escape)

### 7. [QW] Create Symlink Validation Script
- **Source**: geepers_scout recommendations
- **Impact**: 3 | **Effort**: 2 | **Priority**: 6.0
- **Description**: Create `tools/validate_symlinks.py` to verify all symlinks point to valid targets. Prevents broken links in catalog and ensures data consistency.
- **Dependencies**: None
- **Files**: `tools/validate_symlinks.py` (new)
- **Action Items**:
  - [ ] Implement symlink discovery from root directory
  - [ ] Check each symlink target exists and is readable
  - [ ] Report broken links with suggestions for repair
  - [ ] Add option to auto-fix symlinks (delete and recreate)
  - [ ] Create manifest of expected symlinks in `symlink_manifest.json`
  - [ ] Add to CI/CD pre-commit checks

### 8. [QW] Extract JavaScript from index.html to catalog.js
- **Source**: geepers_scout recommendations
- **Impact**: 2 | **Effort**: 2 | **Priority**: 5.5
- **Description**: Move inline JavaScript from `index.html` to external `catalog.js` file for better caching and maintainability. Improves site performance for repeat visitors.
- **Dependencies**: None
- **Files**: `index.html`, `catalog.js` (new)
- **Action Items**:
  - [ ] Extract search, filter, and sorting logic to `catalog.js`
  - [ ] Extract utility functions for metadata formatting
  - [ ] Update `index.html` to include `<script src="catalog.js"></script>`
  - [ ] Verify all functionality still works
  - [ ] Test with multiple datasets to ensure no regressions

---

## Medium Priority Tasks

### 9. Complete NASA Meteorite Data Collection (After #1)
- **Source**: fetch_wild_data.py comments, README.md
- **Impact**: 4 | **Effort**: 2 | **Priority**: 6.5
- **Blocked by**: Task #1 (API endpoint fix)
- **Description**: Once API endpoint is fixed, uncomment `fetch_nasa_meteorites()` call in `fetch_wild_data.py` and test data collection.
- **Action Items**:
  - [ ] After Task #1 completes, uncomment line 256
  - [ ] Run `python3 tools/fetchers/fetch_wild_data.py`
  - [ ] Verify 45k+ meteorite records downloaded
  - [ ] Check metadata.json for correct source attribution

### 10. Refresh World Bank Economic Data
- **Source**: geepers_scout report (33 days stale)
- **Impact**: 4 | **Effort**: 2 | **Priority**: 6.5
- **Description**: World Bank data should be refreshed monthly per guidelines. Last update was ~33 days ago. Requires `fetch_world_bank_data.py`.
- **Dependencies**: None
- **Estimated Freshness Impact**: ~12 new GDP indicators, inflation rates, income group changes
- **Action Items**:
  - [ ] Run `python3 tools/fetchers/fetch_world_bank_data.py`
  - [ ] Verify economic/billionaires/gdp_indicators.json updated
  - [ ] Check record count changes (should be 217 countries)
  - [ ] Validate FIPS codes in merged output
  - [ ] Commit with message: "refresh: update World Bank economic data (monthly)"

### 11. Refresh Census Demographic Data
- **Source**: geepers_scout report
- **Impact**: 4 | **Effort**: 3 | **Priority**: 6.0
- **Description**: Requires CENSUS_API_KEY. Should refresh quarterly. Multiple datasets depend on Census ACS 5-year estimates: food desert, housing crisis, healthcare desert, veterans demographics.
- **Dependencies**: CENSUS_API_KEY configured in .env
- **Action Items**:
  - [ ] Verify CENSUS_API_KEY in `/API_KEYS.md`
  - [ ] Run `python3 tools/fetchers/fetch_food_data.py`
  - [ ] Run `python3 tools/fetchers/fetch_housing_data.py`
  - [ ] Run `python3 tools/fetchers/fetch_healthcare_data.py`
  - [ ] Validate FIPS codes across all outputs
  - [ ] Check for any API rate limit hits (500/day per key)
  - [ ] Commit Census refreshes together

### 12. Close Language Speaker Count Gap (980 languages)
- **Source**: data_trove.md recommendations (Priority 1)
- **Impact**: 3 | **Effort**: 4 | **Priority**: 5.5
- **Description**: 980 out of 7,134 languages (13.7%) still missing speaker counts. Need to investigate alternative sources (Ethnologue, Glottolog) and fix 2 missing ISO codes in language-history.json (Karen, Nahuatl).
- **Dependencies**: None
- **Current Coverage**: 86.3% (6,154 languages)
- **Action Items**:
  - [ ] Identify which 980 languages lack speaker counts
  - [ ] Check if Language History tree contains their data
  - [ ] Fix Karen and Nahuatl ISO code mappings in `data/linguistic/language-history.json`
  - [ ] Evaluate Ethnologue API access (may require subscription)
  - [ ] Add fallback logic to fetcher for common languages
  - [ ] Update integration script with enhanced priority logic
  - [ ] Run validation to measure new coverage percentage

### 13. Implement Gzip Compression for Large JSON Files
- **Source**: geepers_scout recommendations
- **Impact**: 2 | **Effort**: 3 | **Priority**: 5.0
- **Description**: Create `.gz` versions of large JSON files (>1 MB). Reduces bandwidth for downloads, improves CDN performance. Files affected: linguistic/ (56 MB), quirky/ (36 MB), wild/ (5.8 MB).
- **Dependencies**: None
- **Action Items**:
  - [ ] Create `tools/compress_data.py` script
  - [ ] Compress all JSON files >1MB to .gz format
  - [ ] Update README with compression guide
  - [ ] Add download size comparisons (e.g., "56 MB → 8 MB compressed")
  - [ ] Create script to auto-compress on new data fetch
  - [ ] Update catalog to show both compressed/uncompressed options

### 14. Add Dataset Usage Code Snippets
- **Source**: geepers_scout recommendations
- **Impact**: 2 | **Effort**: 2 | **Priority**: 4.5
- **Description**: Create `examples/` directory with Python and JavaScript code snippets showing how to load and use each dataset category.
- **Dependencies**: None
- **Action Items**:
  - [ ] Create `examples/` directory structure
  - [ ] Add `examples/python_loading.md` with pandas/json examples
  - [ ] Add `examples/javascript_loading.md` with D3.js examples
  - [ ] Add `examples/fips_mapping.py` for geographic merging
  - [ ] Add example Jupyter notebooks for complex datasets
  - [ ] Link from README.md and index.html

### 15. Add GoatCounter Analytics to Catalog
- **Source**: geepers_scout recommendations
- **Impact**: 2 | **Effort**: 1 | **Priority**: 4.0
- **Description**: Integrate GoatCounter analytics to track dataset downloads, popular categories, and visitor patterns. Provides insights for prioritizing future work.
- **Dependencies**: None (GoatCounter already in use on dr.eamer.dev)
- **Action Items**:
  - [ ] Add GoatCounter script to `index.html` head
  - [ ] Track download clicks with event labels
  - [ ] Track category filter selections
  - [ ] Track search queries
  - [ ] Add dashboard link to documentation

---

## High Priority Features (New Capabilities)

### 16. Enhance Language History Coverage
- **Source**: data_trove.md recommendations (Priority 2)
- **Impact**: 3 | **Effort**: 3 | **Priority**: 5.5
- **Description**: Language History tree currently provides 0 languages as speaker count source. Need to improve ISO code mapping and add language-level (not just family-level) speaker counts.
- **Dependencies**: Task #12 (speaker count gap analysis)
- **Action Items**:
  - [ ] Audit `data/linguistic/language-history.json` ISO mapping
  - [ ] Extract language-level speaker counts vs family-level
  - [ ] Update integration logic to use Language History as secondary source
  - [ ] Test coverage improvement (target: 90%+ total)
  - [ ] Revalidate integrated dataset

### 17. Add Temporal Dimension to Speaker Counts
- **Source**: data_trove.md recommendations (Priority 3)
- **Impact**: 3 | **Effort**: 4 | **Priority**: 5.0
- **Description**: Speaker counts change over time. Add collection year, historical trends, and endangered language trajectories. Enables analysis of language vitality and demographic change.
- **Dependencies**: None
- **Action Items**:
  - [ ] Update `world_languages_integrated.json` schema to include `speaker_count.year`
  - [ ] Parse Joshua Project data for collection year
  - [ ] Track endangered language status (safe, threatened, endangered, critically endangered)
  - [ ] Create historical trend data where available
  - [ ] Update visualization docs with temporal data usage

### 18. Implement Data Quality Dashboard
- **Source**: geepers_scout report
- **Impact**: 3 | **Effort**: 4 | **Priority**: 5.0
- **Description**: Create web-based dashboard showing data freshness, validation status, and collection health. Displays: age of each dataset, last refresh date, record counts vs baseline, API status.
- **Dependencies**: None
- **Action Items**:
  - [ ] Create `dashboard/index.html` with React or simple HTML
  - [ ] Parse metadata files to extract freshness info
  - [ ] Display color-coded health (green/yellow/red) for staleness
  - [ ] Show API failure history if available
  - [ ] Link to fetcher scripts for one-click refresh
  - [ ] Add to service manager for continuous monitoring

### 19. Create Fetcher Documentation Matrix
- **Source**: Organization improvement
- **Impact**: 2 | **Effort**: 3 | **Priority**: 4.5
- **Description**: Comprehensive table documenting all 41 fetchers: dependencies, API keys required, output locations, schedule, last run date, record count, file size.
- **Dependencies**: None
- **Action Items**:
  - [ ] Scan all `tools/fetchers/fetch_*.py` files
  - [ ] Extract metadata from docstrings
  - [ ] Create matrix in `FETCHER_REFERENCE.md`
  - [ ] Add API key requirements section
  - [ ] Document estimated runtimes
  - [ ] Track update schedules per geepers_scout

### 20. Integrate Wordblocks AAC Device Matrix
- **Source**: PROJECTS_DATA_DISCOVERY.md (high priority for accessibility)
- **Impact**: 3 | **Effort**: 3 | **Priority**: 5.5
- **Description**: Copy AAC devices comparison matrix from Wordblocks project into data_trove. Provides comprehensive device coverage data for accessibility research.
- **Dependencies**: None
- **Location**: Copy from `projects/wordblocks/data/` → `data/accessibility/aac_devices/`
- **Action Items**:
  - [ ] Locate AAC device matrix in Wordblocks project
  - [ ] Validate data structure and field names
  - [ ] Create metadata file documenting device taxonomy
  - [ ] Symlink or copy files with proper attribution
  - [ ] Update README with AAC device data availability

---

## Integration Tasks (Cross-Project)

### 21. Link Joshua Project Data to Billionaires Category
- **Source**: organizational coherence
- **Impact**: 2 | **Effort**: 2 | **Priority**: 4.5
- **Description**: Joshua Project people group population data complements billionaires/wealth data. Create cross-reference showing wealth disparities by region and religious affiliation.
- **Dependencies**: None
- **Action Items**:
  - [ ] Create `economic/joshua_project_wealth_analysis.json`
  - [ ] Map Joshua Project regions to billionaire country locations
  - [ ] Calculate regional wealth per capita metrics
  - [ ] Add to README with analysis notes

### 22. Create Bluesky Social Network Export Link
- **Source**: organizational improvement
- **Impact**: 2 | **Effort**: 2 | **Priority**: 4.0
- **Description**: Data_trove should reference Bluesky network data from projects/blueballs/ (159M network data). Create symlink or documented path for visualization projects.
- **Dependencies**: None
- **Location**: `social_networks/bluesky_network/` (symlink to blueballs project data)
- **Action Items**:
  - [ ] Audit blueballs network data for schema consistency
  - [ ] Create documentation for network structure
  - [ ] Add symlink or copy path instructions
  - [ ] Update README social_networks section

### 23. Link Bipolar Dashboard Datasets
- **Source**: PROJECTS_DATA_DISCOVERY.md (39+ datasets available)
- **Impact**: 2 | **Effort**: 3 | **Priority**: 4.0
- **Description**: Bipolar Dashboard contains 39+ health/behavioral datasets (health, medication, cognitive, social). Create symlinks or import into `data/healthcare/` and `data/behavioral/`.
- **Dependencies**: None
- **Action Items**:
  - [ ] Audit bipolar-dashboard datasets for relevance
  - [ ] Create schema documentation
  - [ ] Add symlinks or copies to data_trove
  - [ ] Update README with new behavioral data category

---

## Deferred Tasks (Low Priority)

### 24. Consolidate Directory Structure
- **Priority**: 1.5 (cosmetic)
- **Issue**: Some symlinks exist in root directories, unclear if data/ or category/ directories should be canonical
- **Action**: Document current symlink strategy in ARCHITECTURE.md, defer restructuring until next major version

### 25. Create Notebook Tutorials
- **Priority**: 2.0 (nice-to-have)
- **Issue**: Jupyter notebooks for complex analysis workflows would aid adoption
- **Action**: Create `tutorials/` directory with example analyses after documentation is complete

### 26. Implement S3 Backup Strategy
- **Priority**: 1.5 (infrastructure)
- **Issue**: 200+ MB of data should be backed up to cloud storage
- **Action**: Implement after data validation layer is complete (Task #3)

### 27. Add Versioning to Datasets
- **Priority**: 2.0 (future enhancement)
- **Issue**: Track dataset version numbers and changelog
- **Action**: Consider after achieving 90%+ language speaker count coverage (Task #12)

---

## Statistics & Analysis

| Category | Count |
|----------|-------|
| **Ready to Build (Quick Wins)** | 8 |
| **Medium Priority** | 8 |
| **High Priority Features** | 5 |
| **Integration Tasks** | 3 |
| **Deferred (Low Priority)** | 4 |
| **TOTAL** | 28 |

### By Impact Score
| Impact | Count | Tasks |
|--------|-------|-------|
| 5 (Critical) | 2 | API fix (#1), Commit quirky data (#2) |
| 4 (High) | 8 | Validation (#3), symlink fix (#4), cache cleanup (#5), accessibility (#6), meteorite completion (#9), World Bank (#10), census data (#11), AAC device matrix (#20) |
| 3 (Medium) | 10 | Remaining tasks |
| 2 (Low) | 8 | Code improvements, documentation |

### By Effort Score
| Effort | Count | Estimate |
|--------|-------|----------|
| 1 (Trivial) | 4 | 30 mins |
| 2 (Quick) | 12 | 2 hours total |
| 3 (Half-day) | 8 | 4 hours |
| 4 (Full-day) | 4 | 8 hours |

### Estimated Total Effort
- **Quick Wins (1-2 effort)**: ~2.5 hours
- **Medium Priority**: ~6 hours
- **High Priority Features**: ~12 hours
- **Integration Tasks**: ~6 hours
- **TOTAL**: ~26.5 hours

---

## Recommendations by Type

### Immediate Actions (Next 2 Hours)
1. ✅ Fix NASA meteorite API endpoint (#1)
2. ✅ Commit 40 quirky dataset files (#2)
3. ✅ Fix country_centroids.json symlink (#4)
4. ✅ Add ARIA labels to index.html (#6)

### This Sprint (Next Work Session)
1. Implement data validation layer (#3)
2. Implement cache cleanup script (#5)
3. Create symlink validation script (#7)
4. Extract JavaScript to catalog.js (#8)
5. Complete meteorite data collection (#9)

### Next Month (Prioritized by Impact)
1. Refresh World Bank data (#10)
2. Refresh Census data (#11)
3. Close speaker count gap (#12)
4. Implement data quality dashboard (#18)
5. Create fetcher documentation matrix (#19)

---

## Risk Assessment

### High Risk (Requires Testing)
- **Task #10 (Census data refresh)**: May hit 500/day rate limit. Use `USE_CACHED_DATA=true` if hitting limits.
- **Task #12 (Speaker count gap)**: Requires evaluation of alternative APIs (Ethnologue, Glottolog). May require paid access.

### Medium Risk (Coordination Needed)
- **Task #21-23 (Cross-project integration)**: Ensure symlinks align with project file structures. Verify with respective project maintainers.

### Low Risk (Isolated Changes)
- **Task #3-8 (Quick wins)**: Mostly standalone improvements with minimal cross-project dependencies.

---

## Dependencies Map

```
Task #1 (NASA API fix)
    ├── Task #9 (Complete meteorite collection)
    └── Task #4 (symlink validation) [indirect]

Task #2 (Commit quirky data)
    └── (independent)

Task #3 (Data validation layer)
    ├── Task #11 (Census refresh) [improves reliability]
    └── Task #10 (World Bank refresh) [improves reliability]

Task #6 (ARIA labels)
    └── (independent)

Task #12 (Speaker count gap)
    ├── Task #16 (Language History coverage)
    └── Task #17 (Temporal dimension)

Task #18 (Data Quality Dashboard)
    ├── Task #3 (Validation layer) [data source]
    └── Task #19 (Fetcher matrix) [reference]

Cross-Project (Tasks #21-23)
    └── All fetcher tasks [need current data]
```

---

## Next Steps

1. **Run Task #1 immediately**: Fix NASA API endpoint (blocking other work)
2. **Commit Task #2 after #1**: Stage 40 quirky dataset files
3. **Run Tasks #3-8 in parallel**: All independent quick wins
4. **Update geepers_scout** with progress after each task completion
5. **Consider invoking @geepers_orchestrator_planner** if scope changes significantly

---

*Generated by Planner Agent - 2026-01-18 21:30*
*Document maintained at: `/home/coolhand/geepers/hive/data_trove-queue.md`*

# Task Queue: datavis

**Generated**: 2026-02-12 22:15 UTC
**Total Tasks**: 28
**Quick Wins**: 8
**Blocked**: 0
**Analysis Sources**: PROJECT_PLAN.md, ACTION_ITEMS.md, recommendations.md, CLAUDE.md files, geepers scout report

---

## Ready to Build (Priority Order)

### 1. [QW] Update Federal Spending Data to 2025
- **Source**: ACTION_ITEMS.md:11-24
- **Impact**: 5 | **Effort**: 2 | **Priority**: 8.0
- **Description**: Download 2025 fiscal year balance-of-payments data from Rockefeller Institute. Current data is 3 years outdated (2022). Update CSV schema and test all 10 spending visualizations.
- **Files**: `spending/state-federal-spend.csv`, all 10 spending chart visualizations
- **Depends on**: None
- **Steps**:
  1. Download Excel from https://rockinst.org/issue-area/bop-2025/
  2. Extract state, federal_spending_2025, federal_taxes_2025 columns
  3. Calculate balance (spending - taxes)
  4. Convert to CSV, preserving current schema
  5. Test all visualizations render without errors
- **Est. Time**: 60 minutes
- **Success Criteria**: All spending charts display 2025 data, no console errors

### 2. [QW] Download USDA Food Access Atlas Data
- **Source**: ACTION_ITEMS.md:26-39
- **Impact**: 5 | **Effort**: 1 | **Priority**: 8.0
- **Description**: Replace placeholder food desert data with authoritative USDA-defined metrics. Download county-level CSV from USDA ERS with FIPS codes and low-access flags.
- **Files**: `dev/food_deserts/data/food_access_atlas.csv`, create metadata JSON
- **Depends on**: None
- **Est. Time**: 30 minutes
- **Success Criteria**: Food desert maps show real USDA-defined low-access areas

### 3. [QW] Add CMS Hospital API Integration
- **Source**: ACTION_ITEMS.md:41-55
- **Impact**: 5 | **Effort**: 2 | **Priority**: 8.0
- **Description**: Create Python script to fetch 5,380+ real hospital locations from CMS API. Add to healthcare_deserts project for real hospital data overlay.
- **Files**: Create `dev/healthcare_deserts/scripts/fetch_cms_hospitals.py`, export CSV
- **API**: https://data.cms.gov/provider-data/api/1/datastore/query/xubh-q36u
- **Depends on**: None
- **Est. Time**: 45 minutes
- **Success Criteria**: CMS hospital locations integrated, visualizations show real data

### 4. [QW] Clean Up Console.log Statements
- **Source**: geepers_scout analysis (1,892 console.log statements found)
- **Impact**: 3 | **Effort**: 2 | **Priority**: 4.0
- **Description**: Remove debug console.log statements from production code across datavis projects. Improves log cleanliness and bundle analysis.
- **Scope**: All .js, .ts, .html files in datavis/
- **Depends on**: None
- **Est. Time**: 2-3 hours with automated search-replace
- **Success Criteria**: No debug console.logs in production code (preserve error/warn)

### 5. [QW] Remove Duplicate Directory (downjones/)
- **Source**: geepers_scout (typo duplicate of dowjones/)
- **Impact**: 2 | **Effort**: 1 | **Priority**: 3.0
- **Description**: Delete `/home/coolhand/html/datavis/downjones/` which only contains duplicate CLAUDE.md. Keep main `/home/coolhand/html/datavis/dowjones/` (correct spelling).
- **Files**: `downjones/` (remove)
- **Depends on**: None
- **Est. Time**: 5 minutes
- **Success Criteria**: Typo directory removed, no broken links to it

### 6. [QW] Implement Papa Parse + Data Export
- **Source**: ACTION_ITEMS.md:61-71, recommendations.md:42-92
- **Impact**: 4 | **Effort**: 3 | **Priority**: 5.0
- **Description**: Add data export functionality (CSV, JSON, XLSX) and replace D3.csv() with Papa Parse for better error handling. Enable users to download filtered/sorted data.
- **Files**: billions/, dowjones/, spending/, one-year/ projects
- **Libraries**: [Papa Parse](https://www.papaparse.com/), [SheetJS](https://sheetjs.com/)
- **Depends on**: None
- **Est. Time**: 2-3 hours
- **Success Criteria**: Export buttons work, data downloads in all three formats, Papa Parse catches CSV errors gracefully

### 7. [QW] Add Skeleton Loading States
- **Source**: ACTION_ITEMS.md:73-82
- **Impact**: 3 | **Effort**: 2 | **Priority**: 3.0
- **Description**: Create CSS skeleton animations for all async data loading. Show pulsing placeholder UI instead of blank screens during data fetch.
- **Scope**: All projects with data loading (billions, dowjones, spending, poetry projects)
- **Depends on**: None
- **Est. Time**: 3 hours
- **Success Criteria**: Loading indicators appear while fetching, accessibility labels added (aria-busy)

### 8. [QW] Implement Keyboard Shortcuts
- **Source**: ACTION_ITEMS.md:84-96
- **Impact**: 3 | **Effort**: 2 | **Priority**: 3.0
- **Description**: Add keyboard shortcuts for power users. Implement shortcuts: +/- (zoom), S (sort), T (theme), E (export), ? (help).
- **Files**: billions/, dowjones/, spending/
- **Library**: [Mousetrap.js](https://craig.is/killing/mice) (2KB, no dependencies)
- **Depends on**: Task #6 (export functionality)
- **Est. Time**: 4 hours
- **Success Criteria**: All shortcuts functional, help modal documents all options, no conflicts with browser shortcuts

---

## High Priority (1 Week)

### 9. Add Colorblind-Safe Palettes & Pattern Fills
- **Source**: ACTION_ITEMS.md:113-123, recommendations.md:152-170
- **Impact**: 5 | **Effort**: 3 | **Priority**: 6.0
- **Description**: Implement ColorBrewer palettes, add pattern fills as alternative to color, enable deuteranopia/protanopia simulation mode. Achieve WCAG 2.1 AA+ compliance.
- **Files**: All projects with categorical color scales (forget-me-not, dowjones, poetry, etc.)
- **Libraries**: [ColorBrewer](https://colorbrewer2.org/), [chroma.js](https://gka.github.io/chroma.js/)
- **Depends on**: None
- **Est. Time**: 3-4 hours
- **Success Criteria**: All visualizations pass colorblind simulation tests, toggle available in settings

### 10. Integrate Observable Plot for New Visualizations
- **Source**: ACTION_ITEMS.md:102-111, recommendations.md:178-196
- **Impact**: 4 | **Effort**: 3 | **Priority**: 5.0
- **Description**: Add Observable Plot as high-level alternative to D3 for rapid prototyping. Reduces D3 code by ~50x for common charts. Use in dev/ folder for exploratory visualizations.
- **URL**: [Observable Plot](https://observablehq.com/plot/)
- **Use Cases**: Rapid prototyping, simplified choropleths, faceted views, distribution plots
- **Depends on**: None
- **Est. Time**: 4-6 hours
- **Success Criteria**: 1-2 new visualizations created with Observable Plot demonstrating productivity gains

### 11. Standardize CSS Custom Properties Across Projects
- **Source**: geepers_scout analysis
- **Impact**: 3 | **Effort**: 2 | **Priority**: 3.5
- **Description**: Standardize CSS variable naming and values across all projects to improve consistency and maintainability.
- **Standard Variables**: `--color-primary`, `--color-secondary`, `--color-text`, `--color-background`, `--spacing-unit`, `--font-family`
- **Scope**: poems/, billions/, dowjones/, interactive/
- **Depends on**: None
- **Est. Time**: 3-4 hours
- **Success Criteria**: All projects use consistent variable naming, easy to update theme globally

### 12. Complete housing_crisis HTML Visualization
- **Source**: geepers_scout, recommendations.md
- **Impact**: 5 | **Effort**: 4 | **Priority**: 6.0
- **Description**: Create HTML visualization for housing_crisis project. Python data pipeline complete; needs D3/Leaflet frontend to display HUD rent data + Census demographics.
- **Data**: HUD Fair Market Rents + Census ACS (pipeline done)
- **Tech**: D3.js or Leaflet for mapping, Timeline for temporal view
- **Depends on**: None
- **Est. Time**: 2-3 days
- **Success Criteria**: Interactive map of rent burden by county, temporal slider, state/county detail panels

### 13. Create Shared Component Library
- **Source**: ACTION_ITEMS.md:165-174
- **Impact**: 4 | **Effort**: 4 | **Priority**: 4.5
- **Description**: Extract reusable D3 components into `shared/components/` directory. Include: timeline scrubber, theme toggle, export toolbar, skeleton loader.
- **Location**: Create `datavis/shared/components/`
- **Components**:
  - Timeline scrubber with linked highlighting
  - Dark/light theme toggle with persistence
  - Export button toolbar (CSV/JSON/XLSX)
  - Skeleton loading animator
  - ARIA live region announcer
- **Depends on**: Task #6, #7, #8 (export, loading, shortcuts)
- **Est. Time**: 8-12 hours
- **Success Criteria**: Components usable across 5+ projects, reduce duplication by 40%

---

## Medium Priority (2-4 Weeks)

### 14. Consolidate Event Data Databases
- **Source**: ACTION_ITEMS.md:155-163
- **Impact**: 3 | **Effort**: 3 | **Priority**: 3.5
- **Description**: Create single source-of-truth event database. Currently 6 redundant event datasets across one-year/ and poems/cycles/. Consolidate into normalized structure.
- **Files**: `one-year/us-sentiment/events.json`, `poems/cycles/events-database.js`, `poems/cycles/events-gdelt.js`
- **Depends on**: None
- **Est. Time**: 6-8 hours
- **Success Criteria**: Single events.json used by all projects, duplicate databases removed

### 15. Update Language Explorer with Search & Filters
- **Source**: PROJECT_PLAN.md
- **Impact**: 4 | **Effort**: 3 | **Priority**: 4.0
- **Description**: Enhance `language/explorer/index.html` with search (ISO/Glottocode/macroarea) and filter controls. Already partially implemented; needs completion.
- **Features**:
  - Search by ISO code, language name, Glottocode
  - Filter by macroarea (Africa, Americas, Asia, Europe, Pacific)
  - Search result highlighting in tree
  - Fuzzy matching for typo tolerance
- **Depends on**: None (Glottolog data already fresh)
- **Est. Time**: 3-4 hours
- **Success Criteria**: Search finds languages, filters work, UI responsive

### 16. Run Comprehensive Accessibility Audit
- **Source**: geepers_scout, recommendations.md
- **Impact**: 4 | **Effort**: 3 | **Priority**: 4.5
- **Description**: Run @geepers_a11y agent for comprehensive WCAG 2.1 AA audit of all production projects. Document gaps, create remediation plan.
- **Scope**: billions/, dowjones/, spending/, poetry/, language/, interactive/
- **Tools**: axe-core, WAVE, screen reader testing (NVDA/JAWS/VoiceOver)
- **Depends on**: None
- **Est. Time**: 4-6 hours (agent-assisted)
- **Success Criteria**: Audit report generated, 95%+ WCAG 2.1 AA compliance verified

### 17. Optimize All Social Card Images (PNG → JPG)
- **Source**: geepers_scout (already in progress)
- **Impact**: 2 | **Effort**: 1 | **Priority**: 2.5
- **Description**: Complete PNG-to-JPG conversion for all social card images (og:image). Reduces file sizes by 60-80%.
- **Files**: Use `poems/optimize_images.py` script across all projects
- **Scope**: poems/, billions/, dowjones/, interactive/, data_trove/
- **Depends on**: None
- **Est. Time**: 20-30 minutes
- **Success Criteria**: All social cards < 200KB, PNG backups kept for reference

### 18. Add Data Sonification (Audio Accessibility)
- **Source**: recommendations.md:328-348
- **Impact**: 5 | **Effort**: 5 | **Priority**: 4.0
- **Description**: Make data accessible through sound for visually impaired users. Convert chart data to audio tones (pitch = value). Start with forget-me-not as proof-of-concept.
- **Library**: [Tone.js](https://tonejs.github.io/) or [Two Tone](https://github.com/two-tone/two-tone)
- **Use Case**: Forget-me-not: Higher pitch = more deaths in region. Sonification toggle + narrative audio descriptions.
- **Depends on**: None
- **Est. Time**: 2-3 days
- **Success Criteria**: Audio sonification available, screen reader experience enhanced, tested with visually impaired users

### 19. Implement ARIA Live Regions for Dynamic Updates
- **Source**: recommendations.md:350-366
- **Impact**: 4 | **Effort**: 2 | **Priority**: 3.5
- **Description**: Add ARIA live regions to announce filter changes, chart updates, data summaries. Improve screen reader experience.
- **Implementation**: `<div role="status" aria-live="polite" aria-atomic="true">` on chart containers
- **Scope**: All interactive visualizations
- **Depends on**: None
- **Est. Time**: 3-4 hours
- **Success Criteria**: Screen readers announce chart updates, filter changes announced

---

## Strategic (1-2 Months)

### 20. Implement Real-Time Data Streaming (WebSocket)
- **Source**: recommendations.md:385-407
- **Impact**: 4 | **Effort**: 5 | **Priority**: 3.0
- **Description**: Add live data updates via WebSocket. Update billions (Forbes stock), dowjones (live board changes), spending (federal releases).
- **Technology**: Socket.io or WebSocket API + Server-Sent Events
- **Architecture**: Data Source → WebSocket Server → Browser Client → Chart Update
- **Depends on**: None
- **Est. Time**: 3-5 days
- **Success Criteria**: Live data streaming works, charts update smoothly, no stale data >5 minutes

### 21. Create Scrollytelling Narrative ("Story of Federal Spending")
- **Source**: recommendations.md:269-292
- **Impact**: 5 | **Effort**: 4 | **Priority**: 4.5
- **Description**: Create narrative-driven data story using Scrollama.js. Guide users through federal spending insights as they scroll. 400% higher engagement than static content.
- **Library**: [Scrollama](https://github.com/russellsamora/scrollama)
- **Use Case**: "Federal Spending Story" - animated journey through territories, progressive revelation of insights
- **Depends on**: Task #1 (2025 spending data)
- **Est. Time**: 2-3 days
- **Success Criteria**: Scrollytelling works smoothly, narrative flows well, engagement metrics tracked

### 22. Build API for Data Access
- **Source**: recommendations.md:409-428
- **Impact**: 3 | **Effort**: 5 | **Priority**: 2.5
- **Description**: Create REST/GraphQL API to serve visualization data. Enable third-party integrations and programmatic access.
- **Technology**: FastAPI (Python) or Express.js
- **Endpoints**: `/api/v1/federal-spending`, `/api/v1/trade`, `/api/v1/dow-jones`
- **Depends on**: None
- **Est. Time**: 3-4 days
- **Success Criteria**: API documented, endpoints functional, rate limiting implemented

### 23. Add Statistical Analysis Tools
- **Source**: recommendations.md:445-467
- **Impact**: 4 | **Effort**: 4 | **Priority**: 3.5
- **Description**: Implement client-side statistical analysis: trend lines (linear regression), correlation matrices, outlier detection, forecasting.
- **Libraries**: [Simple Statistics](https://simplestatistics.org/), [Regression.js](https://tom-alexander.github.io/regression-js/)
- **Features**: Trend line overlays, R² display, confidence intervals
- **Scope**: billions/, dowjones/, spending/, time-series projects
- **Depends on**: None
- **Est. Time**: 2-3 days
- **Success Criteria**: Trend lines render correctly, statistics displayed with legends

### 24. Implement Linked Brushing & Filtering (Crossfilter)
- **Source**: recommendations.md:312-324
- **Impact**: 4 | **Effort**: 4 | **Priority**: 4.0
- **Description**: Connect multiple charts so selections in one affect others. Brush time range → update all time-based views. Click company → highlight all connections.
- **Library**: [Crossfilter.js](https://github.com/crossfilter/crossfilter) + [DC.js](https://dc-js.github.io/dc.js/)
- **Use Cases**: Dowjones (select company → highlight board connections), Spending (select state → drill down)
- **Depends on**: None
- **Est. Time**: 2-3 days
- **Success Criteria**: Linked filtering works across 3+ charts, performance handles 10k+ data points

### 25. Expand PWA Support to All Projects
- **Source**: recommendations.md:556-569
- **Impact**: 3 | **Effort**: 3 | **Priority**: 2.5
- **Description**: Expand Progressive Web App support beyond federal_spending. Add service worker strategies to all projects: cache-first, network-first, stale-while-revalidate.
- **Library**: [Workbox](https://developer.chrome.com/docs/workbox/)
- **Scope**: billions/, dowjones/, spending/, poetry/, interactive/
- **Depends on**: None
- **Est. Time**: 3-4 hours per project × 8 projects = 24-32 hours
- **Success Criteria**: All projects installable, offline mode works

### 26. Create Automated Testing Infrastructure
- **Source**: recommendations.md:841-894
- **Impact**: 4 | **Effort**: 4 | **Priority**: 3.0
- **Description**: Implement automated testing: unit tests, visual regression, accessibility. Add CI/CD pipeline with GitHub Actions.
- **Tools**: [Vitest](https://vitest.dev/), [Percy](https://percy.io/), [axe-core](https://github.com/dequelabs/axe-core), [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci)
- **Tests to Add**: Data processing, scale calculations, accessibility checks, visual regressions
- **Depends on**: None
- **Est. Time**: 3-4 days
- **Success Criteria**: 80%+ test coverage, CI/CD pipeline passes on every commit

---

## Deferred (Lower Priority / Stretch Goals)

### 27. 3D Visualizations (Three.js/Deck.gl)
- **Source**: recommendations.md:1024-1037
- **Impact**: 3 | **Effort**: 5 | **Priority**: 2.0
- **Description**: Explore 3D representations: 3D choropleth (extruded states), 3D network graph, terrain visualization, globe view.
- **Libraries**: Three.js, Globe.gl, Deck.gl
- **Use Cases**: Federal spending as 3D bar height, Dow Jones as interactive 3D network, trade routes on globe
- **Depends on**: None
- **Est. Time**: 5-7 days
- **Status**: Nice-to-have, experimental

### 28. Machine Learning Insights (TensorFlow.js)
- **Source**: recommendations.md:468-480
- **Impact**: 3 | **Effort**: 5 | **Priority**: 1.5
- **Description**: Use TensorFlow.js for client-side ML: clustering similar states/companies, anomaly detection, forecasting, pattern recognition.
- **Library**: [TensorFlow.js](https://www.tensorflow.org/js)
- **Use Cases**: Outlier detection in spending, company clustering in Dow Jones, immigration pattern prediction
- **Depends on**: Task #23 (statistical foundations)
- **Est. Time**: 5-7 days
- **Status**: Research/experimental

---

## Statistics

| Category | Count |
|----------|-------|
| Critical (Impact 5, Effort ≤3) | 6 |
| High Priority (Impact 4+, Effort ≤3) | 6 |
| Medium (Impact 3-4, Effort 3-4) | 10 |
| Strategic (Impact 3-4, Effort 4-5) | 4 |
| Stretch Goals (Effort 5+) | 2 |
| **Total** | **28** |

| Effort Estimate | Tasks |
|-----------------|-------|
| < 1 hour | 3 |
| 1-3 hours | 8 |
| 3-8 hours | 10 |
| 8-24 hours | 5 |
| 1-3 days | 2 |
| **Total Est.** | **~120 hours** |

---

## Quick Win Summary

**Ready to implement (no dependencies)**:
- Task #1: Federal spending 2025 data (60 min)
- Task #2: USDA food access (30 min)
- Task #3: CMS hospital API (45 min)
- Task #4: Console.log cleanup (2-3 hrs)
- Task #5: Remove typo directory (5 min)
- Task #6: Papa Parse + export (2-3 hrs)
- Task #7: Skeleton loading (3 hrs)
- Task #8: Keyboard shortcuts (4 hrs)

**Total Quick Win Effort**: ~17 hours | **Total Impact**: HIGH

---

## Recommended Sequencing

### Phase 1: Data Quality (Week 1)
1. Task #1 - Update federal spending
2. Task #2 - Download USDA food data
3. Task #3 - Add CMS hospitals
4. Task #5 - Remove typo directory

### Phase 2: User Experience (Week 2-3)
5. Task #6 - Papa Parse + export
6. Task #7 - Skeleton loading
7. Task #8 - Keyboard shortcuts
8. Task #9 - Colorblind palettes
9. Task #4 - Console.log cleanup

### Phase 3: Architecture (Week 4)
10. Task #11 - Standardize CSS
11. Task #13 - Shared component library
12. Task #14 - Consolidate event data

### Phase 4: Enhancement (Week 5+)
13. Task #10 - Observable Plot
14. Task #12 - Housing crisis visualization
15. Task #16 - Accessibility audit
16. Task #21 - Scrollytelling narrative

---

## Notes

- All quick wins have clear success criteria and no dependencies
- Prioritized by impact-to-effort ratio
- Focus on data accuracy and user value first
- Enhancements second, experimentation third
- Data updates should be checked quarterly
- Accessibility audit should be run before major releases

**Last Scout Report**: 2026-01-11
**Next Review**: End of Q1 2026 (April 2026)

---

*Generated by Planner agent on 2026-02-12*
*Analysis Sources: 1 recommendation file (1,900 lines), 4 PROJECT_PLAN files, 25 TODO files, codebase analysis*

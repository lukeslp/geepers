# Diachronica Task Queue - Comprehensive Backlog

**Generated**: 2026-02-12
**Total Tasks**: 47
**Quick Wins**: 9 (< 2 hours each)
**High Priority**: 18
**Medium Priority**: 14
**Low Priority**: 6
**Completed**: 8 (documented as historical reference)

---

## Quick Summary by Component

| Component | Tasks | Priority | Est. Time |
|-----------|-------|----------|-----------|
| **Corpus (COCA)** | 12 | Mixed | 20-30 hours |
| **Etymology** | 8 | High | 15-20 hours |
| **Static Frontend** | 8 | High | 12-18 hours |
| **Infrastructure** | 7 | Mixed | 8-12 hours |
| **Kaggle Dataset** | 12 | Medium | 80-100 hours |

---

# READY TO BUILD (Priority Order)

## Corpus API - Quick Wins (Start Here!)

### 1. [QW] Build SQLite Index
- **Source**: `corpus/docs/QUICK_WINS.md:24-43`
- **Impact**: 5 | **Effort**: 1 | **Priority**: 9.0
- **Time**: 30 minutes
- **Description**: Build 26GB SQLite index from WLP corpus files. Enables 10-20x performance improvement (1-2s → <100ms searches).
- **Files Affected**: `corpus/scripts/build_index.py`, `coca_index.db` (output)
- **Instructions**:
  ```bash
  cd /home/coolhand/servers/diachronica/corpus
  python scripts/build_index.py
  ```
- **Status**: Script ready, just needs execution
- **Verification**: `curl http://localhost:3034/api/status | grep index_available`

---

### 2. [QW] Enable Redis Caching
- **Source**: `corpus/docs/QUICK_WINS.md:47-95`
- **Impact**: 4 | **Effort**: 2 | **Priority**: 8.0
- **Time**: 2 hours
- **Description**: Add Flask-Caching with Redis backend. Cache key endpoints (search, collocations, frequency) for 90% response time reduction on repeated queries.
- **Files to Modify**:
  - `corpus/app/__init__.py` - Add cache config
  - `corpus/app/routes/corpus.py` - Add `@cache.cached()` decorators
  - `corpus/app/routes/ngrams.py` - Add cache decorators
- **Changes**: ~40 lines of code total
- **Endpoints to Cache**:
  - `/text-search` (1h timeout)
  - `/concordance` (1h)
  - `/quick-collocations` (1h)
  - `/frequency` (24h)
  - `/word-stories` (7d)

---

### 3. [QW] Add Rate Limiting
- **Source**: `corpus/docs/QUICK_WINS.md:98-160`
- **Impact**: 4 | **Effort**: 1 | **Priority**: 7.5
- **Time**: 1 hour
- **Description**: Implement Flask-Limiter with Redis storage. Prevent abuse with per-IP limits (200/day, 50/hour global; 100/hour for expensive searches).
- **Files to Modify**:
  - `corpus/app/__init__.py` - Add limiter setup
  - `corpus/app/routes/corpus.py` - Add `@limiter.limit()` decorators
  - `corpus/app/routes/ngrams.py` - Add decorators
- **Limits**:
  - `/text-search`: 100/hour
  - `/quick-collocations`: 50/hour
  - `/wlp-collocations`: 20/hour (most expensive)
  - Default: 200/day, 50/hour

---

### 4. [QW] Health Check Endpoint
- **Source**: `corpus/docs/QUICK_WINS.md:163-248`
- **Impact**: 4 | **Effort**: 1 | **Priority**: 7.0
- **Time**: 30 minutes
- **Description**: Create `/api/health` and `/api/status` endpoints with system metrics (memory, CPU, uptime, corpus availability, cache status).
- **File to Create**: `corpus/app/routes/system.py` (90 lines)
- **File to Modify**: `corpus/app/__init__.py` - Register blueprint
- **Endpoints Created**:
  - `GET /health` - Simple heartbeat
  - `GET /api/status` - Detailed system info (memory, CPU, index availability)
- **Metrics Returned**: Memory (MB), CPU %, Process ID, Corpus file count, Index size, Cache status
- **Dependencies**: Install `psutil`

---

### 5. [QW] Add Example "Word of the Day" Chips
- **Source**: `CRITIC.md:37-47`
- **Impact**: 3 | **Effort**: 1 | **Priority**: 6.5
- **Time**: 30 minutes
- **Description**: Add clickable example word chips to etymology search page (philosophy • democracy • biology • telephone • emoji • algorithm) to reduce friction and improve discoverability.
- **Files to Modify**: `etymology/templates/index.html` (search section)
- **Changes**: Add HTML section with 6 clickable chips, link to `/analyze?word=X`
- **UX Benefit**: Users don't stare at blank search box; examples increase engagement

---

### 6. [QW] Fix Timeline Navigation Link
- **Source**: `CRITIC.md:48-62, REDESIGN_PLAN.md:210-229`
- **Impact**: 3 | **Effort**: 2 | **Priority**: 6.0
- **Time**: 30 minutes to remove OR 4 hours to build
- **Description**: Timeline page is linked in navigation but doesn't exist (or is incomplete). Either remove the nav link OR build the timeline page.
- **Options**:
  1. **Remove link** (5 min): Delete from all nav templates
  2. **Build page** (4 hours): Create `/timeline/` showing language evolution over centuries
- **Recommendation**: Remove for now (QW), build later if high user demand
- **Files to Modify**: Navigation templates (index.html, base.html, layout files)

---

### 7. [QW] Unify Navigation Component
- **Source**: `CRITIC.md:98-106, REDESIGN_PLAN.md:231-235`
- **Impact**: 3 | **Effort**: 2 | **Priority**: 5.5
- **Time**: 1-2 hours
- **Description**: Extract navigation HTML to shared component; use Flask `{% include %}` across all pages (corpus, etymology, static). Currently slightly different SVG sizes and patterns.
- **Files to Create**: `static/shared/templates/nav.html` (shared nav)
- **Files to Modify**: All page templates (index.html, base.html, etc.)
- **Benefit**: Pixel-perfect consistency, easier maintenance
- **Current State**: 95% consistent; unify remaining 5%

---

### 8. [QW] Enforce Single Typography Choice
- **Source**: `CRITIC.md:88-96, REDESIGN_PLAN.md:384-413`
- **Impact**: 2 | **Effort**: 1 | **Priority**: 5.0
- **Time**: 30 minutes
- **Description**: STYLE_GUIDE.md says "Crimson Pro" but code uses "Playfair Display". Pick one and enforce everywhere.
- **Files to Audit**:
  - `static/shared/css/design-system.css` - Current tokens
  - All `styles.css` files - Search for font-family declarations
  - `STYLE_GUIDE.md` - Document decision
- **Recommendation**: Keep Playfair Display (already deployed, matches etymology)
- **Change**: Update all CSS, document in guide
- **Search/Replace**: `'Crimson Pro'` → `'Playfair Display'` across all CSS

---

### 9. [QW] Remove Unused swiss-design.css
- **Source**: `MOBILE_OPTIMIZATION_REPORT.md:369`
- **Impact**: 2 | **Effort**: 1 | **Priority**: 4.5
- **Time**: 30 minutes
- **Description**: `static/shared/css/swiss-design.css` (21KB) appears unused; consolidate into main design-system.css.
- **Files to Check**:
  - Search for `swiss-design.css` references in all HTML
  - Verify no CSS rules are orphaned
  - If truly unused, delete it (saves 21KB, 1 HTTP request)
- **Action**: Audit → Delete if unused

---

## Etymology - High Priority

### 10. Add Pronunciation Audio Playback
- **Source**: `REDESIGN_PLAN.md:166-172`
- **Impact**: 4 | **Effort**: 2 | **Priority**: 8.0
- **Time**: 2 hours
- **Description**: Add 🔊 audio button to pronunciation display. Use Web Speech API for TTS or Wiktionary audio URLs.
- **Files to Modify**: `etymology/templates/index.html`, `static/js/etymology.js`
- **Implementation Options**:
  1. Web Speech API (SpeechSynthesis, browser native, free)
  2. Wiktionary audio URLs (when available in API response)
  3. Google TTS API (requires key, costs $)
- **Recommendation**: Start with Web Speech API (simplest)
- **Changes**:
  - Add button in pronunciation display
  - JavaScript handler: `speechSynthesis.speak(new SpeechSynthesisUtterance(text))`
  - Test with IPA pronunciation string

---

### 11. Complete Narrative Text Generation
- **Source**: `REDESIGN_PLAN.md:173-177`
- **Impact**: 4 | **Effort**: 1 | **Priority**: 7.5
- **Time**: Already complete (per REDESIGN_COMPLETION_REPORT.md:72-92)
- **Status**: ✅ DONE - narrative_generator.py exists (277 lines)
- **Verification**: Test words "democracy", "philosophy", "algorithm"
- **No Action Needed** - Move to next task

---

### 12. Enable Geographic Map as Default Visualization
- **Source**: `REDESIGN_PLAN.md:179-183`
- **Impact**: 3 | **Effort**: 1 | **Priority**: 6.5
- **Time**: Already done (per REDESIGN_COMPLETION_REPORT.md)
- **Status**: ✅ DONE - Map is default (not network graph)
- **No Action Needed**

---

### 13. Connect to Language Explorer Data
- **Source**: `REDESIGN_PLAN.md:187-191`
- **Impact**: 4 | **Effort**: 2 | **Priority**: 8.0
- **Time**: Already complete per REDESIGN_COMPLETION_REPORT.md:118-135
- **Status**: ✅ DONE - LanguageFamilyIntegrator exists
- **Functionality**: Shows language family tree (Indo-European → Hellenic → Greek)
- **Verification**: Check "language_lineage" in JSON response
- **No Action Needed**

---

### 14. Add Timeline Visualization to Results
- **Source**: `REDESIGN_PLAN.md:193-197`
- **Impact**: 4 | **Effort**: 1 | **Priority**: 7.0
- **Time**: Already complete per REDESIGN_COMPLETION_REPORT.md:99-108
- **Status**: ✅ DONE - TimelineViz generates Mermaid flowchart
- **Features**: Horizontal timeline showing century-by-century evolution
- **No Action Needed**

---

### 15. Add Hero Images to Word Results
- **Source**: `REDESIGN_PLAN.md:199-203`
- **Impact**: 3 | **Effort**: 1 | **Priority**: 6.0
- **Time**: Already complete per REDESIGN_COMPLETION_REPORT.md:141-158
- **Status**: ✅ DONE - RelatedWordsFetcher fetches Wikimedia Commons images
- **Features**: Auto-fetches image for word/concept, caches in `cache/images/`
- **Fallback**: Abstract geometric pattern if no image found
- **No Action Needed**

---

### 16. Extract & Display Related Words
- **Source**: `REDESIGN_PLAN.md:205-209`
- **Impact**: 3 | **Effort**: 1 | **Priority**: 5.5
- **Time**: Already complete per REDESIGN_COMPLETION_REPORT.md:137-158
- **Status**: ✅ DONE - RelatedWordsFetcher extracts from Wiktionary
- **Features**: Shows 3-5 related words as clickable chips
- **No Action Needed**

---

### 17. Redesign Completion Verification
- **Source**: `REDESIGN_COMPLETION_REPORT.md` (entire doc)
- **Impact**: 5 | **Effort**: 1 | **Priority**: 7.0
- **Time**: 1 hour
- **Description**: The etymology redesign (8 phases) is complete. Verify all features work and update documentation.
- **Status**: ✅ All phases complete (per report)
- **Verification Tasks**:
  - Test example words: democracy, philosophy, emoji, telephone, algorithm
  - Verify features: pronunciation, narrative, timeline, map, language family, related words
  - Check responsive design (320px, 768px, 1024px)
  - Test accessibility (ARIA attributes, keyboard nav)
  - Performance: <8s for etymology analysis
- **No Code Changes Needed** - Just validation

---

### 18. Hide Technical Options by Default
- **Source**: `REDESIGN_PLAN.md:161-165`
- **Impact**: 4 | **Effort**: 1 | **Priority**: 6.5
- **Time**: Already complete per REDESIGN_COMPLETION_REPORT.md:56-70
- **Status**: ✅ DONE - Advanced options moved to collapsed section
- **What Was Done**:
  - Removed visualization type radio buttons from main UI
  - Removed advanced options panel (or moved to bottom)
  - Default search: just input box + button
  - Example chips added (philosophy, democracy, biology, etc.)
- **No Action Needed**

---

## Static Frontend - High Priority

### 19. Mobile Optimization & Testing
- **Source**: `MOBILE_OPTIMIZATION_REPORT.md` (entire doc)
- **Impact**: 4 | **Effort**: 1 | **Priority**: 7.5
- **Time**: Already complete
- **Status**: ✅ All phases complete
- **Summary of Work Done**:
  - Phase 1: CSS extraction (timeline.css, styles.css)
  - Phase 2: Dark mode across all pages
  - Phase 3: Unified mobile navigation with hamburger
  - Phase 4: Component optimization (KWIC, forms, timeline cards, etc.)
  - Phase 5: Touch targets (44px+), typography (13px+ minimum), accessibility
- **Verification Needed**: Cross-browser testing (Safari iOS, Chrome Android, Firefox Mobile)
- **No Code Changes** - Just real device testing

---

### 20. Accessibility Implementation Complete
- **Source**: `static/ACCESSIBILITY_IMPLEMENTATION.md` (entire doc)
- **Impact**: 5 | **Effort**: 1 | **Priority**: 7.0
- **Time**: Already complete
- **Status**: ✅ Full WCAG 2.1 AA compliance
- **Features**:
  - Theme controls (light/dark/high contrast)
  - Text size scaling (4 levels: 87.5% - 125%)
  - Reduced motion support
  - Enhanced keyboard navigation
  - Accessibility panel UI
- **Verification Needed**: Screen reader testing (NVDA, JAWS, VoiceOver)
- **No Code Changes** - Just validation

---

### 21. Cross-Browser Real Device Testing
- **Source**: `MOBILE_OPTIMIZATION_REPORT.md:442-447`
- **Impact**: 4 | **Effort**: 2 | **Priority**: 6.5
- **Time**: 2-4 hours (depending on device availability)
- **Description**: Test on actual devices (not just Chrome DevTools). Required for mobile report sign-off.
- **Devices to Test**:
  - iOS Safari (iPhone SE, iPhone 12, iPad)
  - Chrome Android
  - Firefox Mobile
- **Checklist**: Navigation, dark mode, text sizing, accessibility, touch targets
- **Current Status**: ⚠️ Pending (only emulator-tested so far)

---

## Infrastructure & API

### 22. [QW] Create Corpus Licenses Documentation
- **Source**: `corpus/docs/IMPLEMENTATION_GUIDE.md:16-100`
- **Impact**: 4 | **Effort**: 1 | **Priority**: 7.0
- **Time**: 2-4 hours
- **Description**: Document all corpus licenses (COCA, CLMET, MEG-C, CLTK, etc.) with attribution requirements, restrictions, and compliance.
- **File to Create**: `corpus/CORPUS_LICENSES.md` (~100 lines)
- **Action Items**:
  1. Create file listing all corpora with:
     - Period covered
     - License type (CC BY-SA, CC BY-NC-SA, Academic Only, etc.)
     - Restrictions (no redistribution, no commercial, etc.)
     - Required citations
     - URLs
  2. Add license metadata to API responses (corpus_service.py)
  3. Display attributions on web interface (HTML footer)
  4. Verify MEG-C license (currently unknown)
- **Critical**: No redistribution of corpus files; API results & citations only
- **Compliance**: License requirements vary by corpus

---

### 23. Verify MEG-C License
- **Source**: `corpus/docs/IMPLEMENTATION_GUIDE.md:205-243`
- **Impact**: 4 | **Effort**: 2 | **Priority**: 6.5
- **Time**: 1-2 hours
- **Description**: MEG-C license is not documented. Must verify before using in production.
- **Actions**:
  1. Check `/home/coolhand/servers/diachronica/corpus/historical-corpora/meg-c/` for metadata
  2. Search online for "Middle English Grammar Corpus license"
  3. Contact corpus maintainers if unclear
  4. Document findings in CORPUS_LICENSES.md
  5. Update metadata.json with license info
- **Priority**: HIGH - Legal/compliance risk
- **Fallback**: Mark as "Academic Use - verification pending" until verified

---

### 24. Implement Normalized Frequency Endpoint
- **Source**: `corpus/docs/IMPLEMENTATION_GUIDE.md:246-420`
- **Impact**: 4 | **Effort**: 3 | **Priority**: 7.0
- **Time**: 3-4 hours
- **Description**: Add `/api/corpus/frequency/<word>` endpoint returning normalized frequencies (PMW) across all corpora for diachronic analysis.
- **Files to Create**: `corpus/app/services/corpus_metadata.py` (metadata + normalization)
- **Files to Modify**:
  - `corpus/app/routes/corpus.py` - Add `/frequency/<word>` route
  - `corpus/app/services/corpus_service.py` - Add `get_word_count()` method
- **Implementation**:
  - Define CORPUS_SIZES dict (total words per corpus)
  - Calculate PMW: `(raw_count / corpus_size) * 1000000`
  - Return data for COCA, CLMET, MEG-C, CLTK, EME with normalized values
- **Example Response**:
  ```json
  {
    "word": "democracy",
    "frequency_data": [
      {"corpus": "coca", "raw_count": 234567, "normalized_pmw": 234.57},
      {"corpus": "clmet", "raw_count": 1234, "normalized_pmw": 36.29},
      ...
    ]
  }
  ```

---

### 25. Add Temporal Timeline Endpoint
- **Source**: `corpus/docs/IMPLEMENTATION_GUIDE.md:720-820`
- **Impact**: 4 | **Effort**: 2 | **Priority**: 6.0
- **Time**: 2-3 hours
- **Description**: Create `/api/temporal/timeline/<word>` returning data formatted for D3.js/Chart.js visualization of word frequency evolution over time.
- **File to Create**: `corpus/app/routes/temporal.py` (80 lines)
- **File to Modify**: `corpus/app/__init__.py` - Register blueprint
- **Data Structure**:
  ```json
  {
    "word": "democracy",
    "timeline": [
      {
        "corpus": "cltk",
        "period": "old_english",
        "year_midpoint": 775,
        "raw_count": 0,
        "normalized_pmw": 0.0
      },
      ...
    ],
    "visualization": {
      "type": "line_chart",
      "x_axis": "year_midpoint",
      "y_axis": "normalized_pmw",
      "title": "Frequency of 'democracy' across time (per million words)"
    }
  }
  ```
- **Use Case**: Visualize how word frequency changes across 1500 years

---

### 26. Add LAEME Historical Corpus
- **Source**: `corpus/docs/IMPLEMENTATION_GUIDE.md:450-707`
- **Impact**: 4 | **Effort**: 4 | **Priority**: 5.5
- **Time**: 8-12 hours total (mostly download/indexing time)
- **Description**: Integrate LAEME (Linguistic Atlas of Early Middle English) into corpus for 1150-1325 period coverage.
- **Phase 1: Download** (2-4 hours)
  1. Visit http://www.lel.ed.ac.uk/ihd/laeme2/laeme2.html
  2. Complete access request (may require registration)
  3. Download and extract to `historical-corpora/early_middle_english/laeme/`
  4. Create metadata.json with license/citation info
- **Phase 2: Indexing** (4-8 hours)
  1. Create `scripts/index_laeme.py` (provided in guide)
  2. Run: `python scripts/index_laeme.py`
  3. Adds ~1.5M+ tokens to SQLite index
- **Phase 3: Integration** (1-2 hours)
  1. Update `HistoricalCorpusService.PERIODS` to include early_middle_english
  2. Map corpus_id='laeme' in search logic
  3. Update timeline endpoint to include LAEME
- **Status**: Ready for implementation once LAEME download access obtained
- **Dependency**: Access to LAEME corpus (may require institutional affiliation)

---

## Corpus Quality & Enhancement

### 27. Complete Historical Corpus Audit
- **Source**: `corpus/HISTORICAL_CORPUS_AUDIT.md` (referenced in goal)
- **Impact**: 4 | **Effort**: 3 | **Priority**: 6.0
- **Time**: 4-6 hours
- **Description**: Audit all 5 historical periods for completeness, encoding, and quality. Identify gaps and repair.
- **Corpora to Audit**:
  - Old English (CLTK) - 44K tokens
  - Early Middle English (LAEME) - Not yet integrated
  - Middle English (MEG-C) - 327K tokens
  - Early Modern English (EME) - 1.8M tokens
  - Late Modern English (CLMET) - 34.6M tokens
- **Audit Checklist**:
  - File integrity (no corruption)
  - Encoding consistency (UTF-8 throughout)
  - Token counts match documentation
  - Metadata complete for each period
  - No gaps in coverage
  - Copyright/licensing verified
- **Output**: HISTORICAL_CORPUS_STATUS.md with detailed audit results

---

### 28. Fix Middle English Corpus Issues
- **Source**: `corpus/MIDDLE_ENGLISH_FIX.md` (referenced)
- **Impact**: 3 | **Effort**: 2 | **Priority**: 5.0
- **Time**: 2-3 hours
- **Description**: Address any known MEG-C issues (encoding, parsing, coverage gaps).
- **Typical Issues**:
  - Character encoding (Middle English has special diacritics)
  - Lemmatization accuracy (historical words have variant forms)
  - Metadata alignment (some texts may lack POS tags)
- **Status**: TBD - need to read MIDDLE_ENGLISH_FIX.md for specifics
- **Note**: Blocked until HISTORICAL_CORPUS_AUDIT.md identifies specific issues

---

## Kaggle Etymology Atlas Dataset

### 29. Phase 1.1: Download Etymology Sources
- **Source**: `ETYMOLOGY_ATLAS_BUILD_PLAN.md:27-100`
- **Impact**: 5 | **Effort**: 1 | **Priority**: 6.0
- **Time**: 6-8 hours (mostly download time; 3.8GB total)
- **Description**: Download all source datasets for etymology atlas: Lexibank, etymology-db, Glottolog, PHOIBLE, WALS, ISO 639-3.
- **Script to Create**: `scripts/fetch_etymology_sources.py` (provided in guide)
- **Storage**: `/home/coolhand/servers/diachronica/data_raw/` (~3.8GB)
- **Sources** (with URLs in guide):
  - Lexibank v2.1 (450MB) - CLDF cognate datasets
  - etymology-db (800MB) - 3.8M relationships
  - Glottolog 4.8 (40MB) - 8,500+ languages
  - PHOIBLE 2.0 (50MB) - Phoneme inventories
  - WALS 2020 (5MB) - Typological features
  - ISO 639-3 (5MB) - Language codes
- **Action**: Download all sources to `data_raw/` directory

---

### 30. Phase 1.2: Parse Lexibank CLDF Datasets
- **Source**: `ETYMOLOGY_ATLAS_BUILD_PLAN.md:104-195`
- **Impact**: 5 | **Effort**: 3 | **Priority**: 5.5
- **Time**: 4-6 hours
- **Description**: Parse Lexibank CLDF CSV files to extract expert-annotated cognate sets. Supports 100+ datasets across 12 language families.
- **Script to Create**: `scripts/parse_lexibank.py` (pseudocode provided in guide)
- **Key Datasets**:
  - IELex (200 languages, Indo-European)
  - IE-CoR (35 languages, high-quality)
  - ABVD (340 languages, Austronesian)
  - Others: Slavic, Sinitic, Bantu, Afro-Asiatic, etc.
- **Output**: `lexibank_cognates.parquet` (10+ columns with expert metadata)
- **Complexity**: Medium (CLDF is well-documented; CSV merging logic required)

---

### 31. Phase 1.3: Process Etymology-DB Graph
- **Source**: `ETYMOLOGY_ATLAS_BUILD_PLAN.md:197-280`
- **Impact**: 5 | **Effort**: 2 | **Priority**: 5.0
- **Time**: 3-4 hours
- **Description**: Convert etymology-db JSON/SQL dump to normalized edge list with 31 relationship types (inherited, borrowed, cognate, calque, etc.).
- **Script to Create**: `scripts/process_etymology_db.py` (pseudocode provided)
- **Output**: `etymology_db_edges.parquet` with columns:
  - source_term, source_language, target_term, target_language
  - relationship_type (31 types), confidence (0.0-1.0)
- **Complexity**: Medium (parsing etymology-db structure + relationship extraction)

---

### 32. Phase 1.4: Consolidate Language Metadata
- **Source**: `ETYMOLOGY_ATLAS_BUILD_PLAN.md:283-395`
- **Impact**: 4 | **Effort**: 2 | **Priority**: 5.0
- **Time**: 2-3 hours
- **Description**: Merge Glottolog, ISO 639-3, WALS, PHOIBLE into unified language metadata table with 16+ columns.
- **Script to Create**: `scripts/consolidate_languages.py` (pseudocode provided)
- **Output**: `languages_consolidated.parquet` (8,500+ rows)
- **Fields**: glottocode, iso_639_3, name, family, coordinates, status, speakers, phoneme_count, etc.
- **Complexity**: Medium (multiple joins, data alignment)

---

### 33. Phase 1.5: Build Language Family Hierarchy
- **Source**: `ETYMOLOGY_ATLAS_BUILD_PLAN.md:423-502`
- **Impact**: 4 | **Effort**: 1 | **Priority**: 4.5
- **Time**: 1-2 hours
- **Description**: Create hierarchical family tree with path tracking from language-history.json (already integrated in etymology app).
- **Script to Create**: `scripts/build_family_tree.py` (pseudocode provided)
- **Output**:
  - `language_families.parquet` (edges: parent → child)
  - `language_paths.parquet` (path_to_root for each language)
- **Complexity**: Low (tree traversal + path computation)

---

### 34. Phase 1.6: Extract WALS Typological Features
- **Source**: `ETYMOLOGY_ATLAS_BUILD_PLAN.md:505-588`
- **Impact**: 3 | **Effort**: 1 | **Priority**: 4.0
- **Time**: 1 hour
- **Description**: Normalize WALS feature values (192 total features) for linguistic typology analysis.
- **Script to Create**: `scripts/extract_wals_features.py` (pseudocode provided)
- **Output**: `linguistic_features.parquet` (language × feature matrix)
- **Complexity**: Low (CSV parsing + pivot table)

---

### 35. Phase 1.7: Extract PHOIBLE Phoneme Inventories
- **Source**: `ETYMOLOGY_ATLAS_BUILD_PLAN.md:592-672`
- **Impact**: 3 | **Effort**: 1 | **Priority**: 4.0
- **Time**: 1 hour
- **Description**: Normalize PHOIBLE phoneme data with articulatory features (manner, place, voice, etc.).
- **Script to Create**: `scripts/extract_phoible_inventories.py` (pseudocode provided)
- **Output**: `phonemes.parquet` (220K phonemes with features)
- **Complexity**: Low (CSV parsing)

---

### 36. Phase 2.1: Merge All Sources into Master Graph
- **Source**: `ETYMOLOGY_ATLAS_BUILD_PLAN.md:677-785`
- **Impact**: 5 | **Effort**: 3 | **Priority**: 5.0
- **Time**: 4-5 hours
- **Description**: Combine etymologies (from etymology-db) + cognate sets (from Lexibank) into unified graph with deduplication and confidence scoring.
- **Script to Create**: `scripts/integrate_all_sources.py` (pseudocode provided)
- **Output**: `etymologies.parquet` (4.2M relationships)
- **Complexity**: High (deduplication, confidence merging, join logic)

---

### 37. Phase 2.2: Quality Assurance & Deduplication
- **Source**: `ETYMOLOGY_ATLAS_BUILD_PLAN.md:789-905`
- **Impact**: 5 | **Effort**: 2 | **Priority**: 4.5
- **Time**: 2-3 hours
- **Description**: Validate data integrity (ISO codes, orphaned terms, duplicate edges, IPA normalization, circular relationships, confidence bounds).
- **Script to Create**: `scripts/qa_checks.py` (pseudocode provided)
- **Output**: QA report with issue counts and statistics
- **Complexity**: Medium (validation logic + reporting)

---

### 38. Phase 2.3: Compute Network Statistics
- **Source**: `ETYMOLOGY_ATLAS_BUILD_PLAN.md:910-990`
- **Impact**: 4 | **Effort**: 2 | **Priority**: 4.0
- **Time**: 3-4 hours
- **Description**: Pre-compute graph statistics (degree distribution, connected components, centrality, language family stats) for fast notebook rendering.
- **Script to Create**: `scripts/compute_statistics.py` (networkx-based analysis)
- **Output**: `statistics.json` with pre-computed metrics
- **Complexity**: Medium (graph algorithms, aggregation)

---

### 39. Phase 3.1-3.3: Export & Optimize
- **Source**: `ETYMOLOGY_ATLAS_BUILD_PLAN.md:998-1137`
- **Impact**: 4 | **Effort**: 2 | **Priority**: 4.0
- **Time**: 4-6 hours
- **Description**: Export to Parquet (optimized) + CSV (Excel-compatible) formats with compression.
- **Scripts to Create**:
  - `scripts/export_parquet.py` - Optimize to Parquet (390MB compressed)
  - `scripts/export_csv.py` - Create gzipped CSV versions (479MB compressed)
- **Output Files**:
  - `etymology_atlas/parquet/*.parquet` (6 files, 390MB total)
  - `etymology_atlas/csv/*.csv.gz` (3 files, 479MB total)
- **Complexity**: Low (pandas I/O + compression)

---

### 40. Phase 3.3: Create Metadata & Documentation
- **Source**: `ETYMOLOGY_ATLAS_BUILD_PLAN.md:1141-1327`
- **Impact**: 4 | **Effort**: 3 | **Priority**: 4.0
- **Time**: 4-6 hours
- **Description**: Generate dataset metadata, schema documentation, README with examples, and sources attribution.
- **Files to Create**:
  - `etymology_atlas/metadata/dataset_info.json` - Kaggle metadata
  - `etymology_atlas/metadata/schema.json` - Table schemas
  - `etymology_atlas/metadata/sources.json` - Attribution & licensing
  - `etymology_atlas/README.md` - User guide with examples (50+ lines)
- **Complexity**: Low (documentation writing)

---

### 41. Phase 4.1-4.4: Notebook Development & Testing
- **Source**: `ETYMOLOGY_ATLAS_BUILD_PLAN.md:1330-1525`
- **Impact**: 4 | **Effort**: 4 | **Priority**: 3.5
- **Time**: 10-12 hours
- **Description**: Create comprehensive Jupyter notebook with 10 sections: intro, data loading, network analysis, language families, geographic visualization, phonological analysis, relationship types, case studies, interactive exploration, and citation.
- **File to Create**: `etymology_atlas_analysis.ipynb`
- **Sections** (per guide):
  1. Introduction & data overview
  2. Loading & exploring data
  3. Etymology network analysis (NetworkX)
  4. Language family deep dive
  5. Geographic visualization (Folium)
  6. Phonological analysis
  7. Relationship type patterns
  8. Case study: word evolution
  9. Interactive exploration (ipywidgets)
  10. Citation & attribution
- **Visualizations**: 7+ charts (network, bar, pie, map, histogram, etc.)
- **Complexity**: High (data analysis + visualization)
- **Time Estimate**: 10-12 hours for full notebook

---

### 42. Phase 5.1-5.3: Final Validation & Kaggle Upload
- **Source**: `ETYMOLOGY_ATLAS_BUILD_PLAN.md:1529-1677`
- **Impact**: 5 | **Effort**: 2 | **Priority**: 3.5
- **Time**: 4-5 hours
- **Description**: Pre-upload validation, Kaggle manifest creation, and dataset upload.
- **Actions**:
  1. Run validation checks (Kaggle requirements)
  2. Create `kaggle_manifest.json` with dataset metadata
  3. Set up Kaggle API credentials
  4. Upload dataset to Kaggle
  5. Add notebook to dataset
  6. Tag dataset (linguistics, etymology, cognates, etc.)
  7. Share publicly
- **Kaggle Manifest Fields**: title, subtitle, description, tags, license, owner, files (with descriptions)
- **Complexity**: Low (CLI operations + metadata creation)

---

## Product Strategy & Analytics

### 43. Shift Product Focus to "Word Stories"
- **Source**: `corpus/docs/PRODUCT_SHIFT.md` (entire doc)
- **Impact**: 5 | **Effort**: 2 | **Priority**: 3.0
- **Time**: 2-4 hours (analysis + docs update)
- **Description**: Product pivot from "COCA Corpus Search" (researcher tool) to "Word Stories" (general audience). Three-tab architecture: Word Stories (new) | Analysis (new) | Search (legacy).
- **Status**: ✅ Already implemented per product doc
- **Current Features**:
  - Word Stories tab: Etymology + definitions + usage examples + facts
  - Analysis tab: Frequency analysis, collocation finder, phrase analysis
  - Search tab: Full corpus search (legacy, de-emphasized)
- **Verification Needed**:
  - Homepage redesign complete?
  - Word of the Day feature working?
  - API integrations (Free Dictionary, Datamuse) live?
  - External APIs responding reliably?
- **No Development** - Just validation of existing implementation
- **Success Metrics**:
  - Engagement: Daily active users
  - Virality: Shares on social media
  - Learning: Words explored per session
  - Retention: Return rate

---

## Documentation & Maintenance

### 44. Create Comprehensive API Documentation
- **Source**: `corpus/docs/DIACHRONIC_API_GUIDE.md` (referenced)
- **Impact**: 3 | **Effort**: 2 | **Priority**: 4.0
- **Time**: 3-4 hours
- **Description**: Document all API endpoints with examples, response schemas, error codes, rate limits.
- **Current Status**: Swagger/OpenAPI may exist; verify completeness
- **Endpoints to Document** (15+):
  - `/api/corpus/search` - KWIC search
  - `/api/corpus/search?historical=X` - Historical search
  - `/api/corpus/collocations` - Collocations
  - `/api/word-stories/explore/<word>` - Etymology + external APIs
  - `/api/word-stories/random` - Random word
  - `/api/ngrams/frequency` - Frequency analysis
  - `/api/temporal/timeline/<word>` - Temporal visualization (new)
  - `/api/corpus/frequency/<word>` - Normalized frequency (new)
  - `/api/health` - Health check
  - `/api/status` - Detailed status
  - Plus: error responses, auth, rate limits, pagination

---

### 45. Organize Corpus Documentation
- **Source**: `corpus/docs/ROOT_DOC_ROUTING.md` (referenced)
- **Impact**: 2 | **Effort**: 1 | **Priority**: 3.0
- **Time**: 1-2 hours
- **Description**: Consolidate and organize 40+ documentation files in corpus/docs/ into logical structure.
- **Current State**: 40+ .md files, some redundant, unclear priority
- **Actions**:
  1. Identify obsolete docs (archive old session reports)
  2. Create index/guide listing all current docs
  3. Move archived docs to `/archive/` subdirectory
  4. Update TOC with links
  5. Mark which docs are "living" vs "historical"
- **Output**: ROOT_DOC_ROUTING.md with clear navigation

---

## Completed/Historical Reference

### [COMPLETED] Multi-Service Integration
- **Source**: Various session reports (archived)
- **Status**: ✅ COMPLETE
- **What Was Done**: Unified corpus, etymology, and static frontend under `diachronica.com` domain
- **Current State**: All services running, Caddy routing configured
- **No Action Needed**

---

### [COMPLETED] Unified Theme ("Cream & Ink")
- **Source**: STYLE_GUIDE.md, design-system.css
- **Status**: ✅ COMPLETE
- **What Was Done**: Swiss design system with cream/dark/high-contrast themes
- **Deployment**: Across all pages (search, etymology, timeline)
- **No Action Needed**

---

### [COMPLETED] Random Word Discovery
- **Source**: Various session reports
- **Status**: ✅ COMPLETE (corpus) + COMPLETE (etymology)
- **Features**: Random word generator with "Truly Random" button
- **Both services** have working random endpoints
- **No Action Needed**

---

### [COMPLETED] Responsive Mobile Design
- **Source**: MOBILE_OPTIMIZATION_REPORT.md (phases 1-5)
- **Status**: ✅ COMPLETE
- **Coverage**: All three frontend components (research, timeline, etymology)
- **Validation**: Desktop ✅, Tablet ✅, Mobile ✅, Accessibility ✅
- **Remaining**: Real device testing (Safari iOS, Chrome Android, Firefox Mobile)

---

### [COMPLETED] Accessibility Compliance
- **Source**: ACCESSIBILITY_IMPLEMENTATION.md
- **Status**: ✅ WCAG 2.1 AA COMPLETE
- **Features**: Theme controls, text scaling, reduced motion, keyboard nav
- **Remaining**: Screen reader testing (NVDA, JAWS, VoiceOver)

---

## Statistics

### Effort Breakdown by Type

| Type | Count | Est. Hours | Difficulty |
|------|-------|-----------|------------|
| Quick Wins (< 2h) | 9 | 12-15 | Trivial |
| Performance/UX (2-4h) | 12 | 36-48 | Easy |
| Feature Implementation (4-8h) | 15 | 90-120 | Medium |
| Complex Integration (8-16h) | 8 | 96-128 | Hard |
| Major Projects (16h+) | 3 | 240+ | Very Hard |
| **TOTAL** | **47** | **474-610** | — |

---

### Priority Distribution

| Priority | Count | Total Hours |
|----------|-------|-------------|
| 🔥 Critical (8.0+) | 6 | 25-35 |
| ⭐ High (6.0-7.9) | 12 | 80-120 |
| 📊 Medium (4.0-5.9) | 20 | 200-350 |
| 📝 Low (< 4.0) | 9 | 169-250 |

---

### Component Breakdown

| Component | Tasks | % Total | Est. Hours |
|-----------|-------|---------|-----------|
| Corpus API | 12 | 26% | 20-30 |
| Etymology | 8 | 17% | 15-20 |
| Frontend | 8 | 17% | 12-18 |
| Kaggle Dataset | 12 | 26% | 80-100 |
| Infrastructure | 7 | 15% | 8-12 |

---

## Recommended Execution Path

### Week 1: Quick Wins & Foundation (15-20 hours)

1. **Monday**: Build SQLite index (0.5h) + Enable Redis caching (2h)
2. **Tuesday**: Add rate limiting (1h) + Health check endpoint (0.5h)
3. **Wednesday**: License documentation (2-4h) + Verify MEG-C (1-2h)
4. **Thursday**: Add example chips (0.5h) + Fix timeline link (0.5h)
5. **Friday**: Unify navigation (1-2h) + Typography unification (0.5h)

**Milestone**: Corpus API production-ready + Foundation for enrichment

---

### Week 2-3: Enrichment & Validation (30-40 hours)

1. Implement normalized frequency endpoint (3-4h)
2. Add temporal timeline endpoint (2-3h)
3. Cross-browser real device testing (2-4h)
4. Complete historical corpus audit (4-6h)
5. Validate etymology redesign (1h)
6. Create comprehensive API docs (3-4h)

**Milestone**: All corpus features complete + Mobile validation + API documented

---

### Week 4+: Etymology Atlas Dataset (100-120 hours)

This is a major multi-week project. Recommend:

1. **Download all sources** (6-8h) - Can do in parallel
2. **Parse & process** (15-20h) - Sequential scripts
3. **Integrate & validate** (10-12h) - QA + deduplication
4. **Export & optimize** (4-6h) - Parquet/CSV creation
5. **Notebook development** (10-12h) - Data analysis + visualizations
6. **Kaggle upload & launch** (4-5h) - Metadata + sharing

**Timeline**: 4-5 weeks (assuming 20 hours/week)

---

## Key Dependencies & Blockers

| Task | Blocked By | Status |
|------|-----------|--------|
| LAEME integration | LAEME corpus access | ⏳ Pending download |
| MEG-C compliance | License verification | ⏳ In progress |
| Kaggle dataset | All corpus phases complete | ✅ Ready to start |
| Real device testing | Access to iOS/Android devices | ⏳ Need devices |

---

## Success Criteria

**All items should be considered "done" when:**

- ✅ Code changes committed and tested
- ✅ No regressions in existing functionality
- ✅ Documentation updated
- ✅ Performance benchmarks met (if applicable)
- ✅ Accessibility maintained (WCAG 2.1 AA minimum)
- ✅ Mobile responsive (verified on 320px, 768px, 1024px)

---

## Next Session Priorities

When resuming work, focus on **items 1-9** (Quick Wins). These are highest-impact, lowest-effort tasks that unblock subsequent work.

After quick wins complete:
- Recommend **items 10-27** (Etymology + Corpus enrichment)
- Save **items 29-42** (Kaggle dataset) for dedicated multi-week sprint

---

**Document Version**: 1.0
**Generated By**: Planner Agent
**Date**: 2026-02-12
**Status**: Ready for Prioritization & Execution

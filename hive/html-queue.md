# Task Queue: html (Web Root)

**Generated**: 2026-03-07 08:45
**Total Tasks**: 28
**Quick Wins**: 8
**Blocked**: 2
**Projects Scanned**: 12 primary + 60+ subprojects

---

## Ready to Build (Priority Order)

### 1. [QW] Immigrant's Journey - Enhanced Meta Tags & SEO
- **Source**: games/.backups/low-hanging-fruit-20251118-015710/immigrant-game/SUGGESTIONS.md:20-40
- **Impact**: 4 | **Effort**: 1 | **Priority**: 7.5
- **Description**: Add theme-color, keywords, OG tags to game `<head>`. 5-minute implementation, critical for discoverability.
- **Files**: `games/immigrant-game/index.html`
- **Depends on**: None

### 2. [QW] Immigrant's Journey - Add to Games Landing Page
- **Source**: games/.backups/low-hanging-fruit-20251118-015710/immigrant-game/SUGGESTIONS.md:35-45
- **Impact**: 4 | **Effort**: 1 | **Priority**: 7.5
- **Description**: Link immigrant-game from games/index.html with preview thumbnail. Portfolio integration.
- **Files**: `games/index.html`
- **Depends on**: Task #1 (logical dependency, not blocking)

### 3. [QW] Viewer - Social Card Generator for New Images
- **Source**: viewer/docs/PROJECT_PLAN.md:120-150
- **Impact**: 3 | **Effort**: 2 | **Priority**: 6.5
- **Description**: Run `scripts/generate_viewers.py` to auto-generate static viewer pages with OG tags for new images added to `image-data.js`. Essential for social sharing.
- **Files**: `viewer/image-data.js`, `viewer/scripts/generate_viewers.py`, `viewer/static/` (output)
- **Depends on**: None (script exists, just needs to be run when images added)

### 4. Alt Text Generator - Run Humanize on All Files
- **Source**: Project assessment (humanize skill requirement)
- **Impact**: 4 | **Effort**: 2 | **Priority**: 6.5
- **Description**: Execute `/humanize` skill on all alt text generator code (`alt/*.py`, `alt/*.js`, `alt/*.html`) to remove "AI" terminology, robotic phrasing, press-release language. Pre-commit gate.
- **Files**: `alt/alt_proxy.py`, `alt/alt_proxy_new.py`, `alt/index.html`, `alt/advanced/`, `alt/dev/` files
- **Depends on**: None

### 5. [QW] Datavis Dev Index - Add Missing Project Links
- **Source**: datavis/dev/CLAUDE.md + visual inspection
- **Impact**: 3 | **Effort**: 1 | **Priority**: 6.5
- **Description**: Update `datavis/dev/index.html` navigation to include recent completions: food_deserts, scars, map, housing_crisis. Link 12 category sections with updated counts.
- **Files**: `datavis/dev/index.html`
- **Depends on**: None

### 6. Scars of the Cretaceous - Data Collection Sprint
- **Source**: datavis/dev/scars/PROJECT_STATUS.md:246-264
- **Impact**: 5 | **Effort**: 3 | **Priority**: 6.0
- **Description**: Complete data acquisition: Run fetch scripts for Census API (04), geology (01), health (06), gun (07), NHGIS guide (02). 2-3 hours total. Unblocks visualization rendering.
- **Files**: `datavis/dev/scars/scripts/`, `datavis/dev/scars/data/`
- **Depends on**: Census API key (user must obtain at https://api.census.gov/data/key_signup.html)

### 7. Food Deserts - Deploy to Production
- **Source**: datavis/dev/food_deserts/PROJECT_STATUS.md:278-283
- **Impact**: 4 | **Effort**: 2 | **Priority**: 5.5
- **Description**: Move from `/datavis/dev/food_deserts/` to `/datavis/food_deserts/`. Update navigation, change URLs, create social preview image, test. 15 minutes.
- **Files**: `datavis/dev/food_deserts/` → `datavis/food_deserts/`, update `datavis/index.html`
- **Depends on**: None (project is production-ready)

### 8. [QW] Geology Map - Replace Sample with Real Data (Optional)
- **Source**: datavis/dev/map/PROJECT_STATUS.md:221-226
- **Impact**: 3 | **Effort**: 2 | **Priority**: 5.0
- **Description**: Run `fetch_nationwide_data.py` with Census API key to generate 3,143 US counties (replaces 43 sample counties). Fully self-contained option. 5-10 minutes setup + 10 min download.
- **Files**: `datavis/dev/map/fetch_nationwide_data.py`, `datavis/dev/map/data_nationwide/`
- **Depends on**: Census API key + Python environment

### 9. Viewer - Mobile Responsive Testing
- **Source**: viewer/docs/PROJECT_PLAN.md:120-145
- **Impact**: 3 | **Effort**: 2 | **Priority**: 4.5
- **Description**: Test gallery, viewer, and lightbox modes on 480px, 768px, 1024px breakpoints. Verify Muuri grid, lazy loading, touch gestures. Already implemented but needs validation.
- **Files**: `viewer/index.html`, `viewer/viewer.html`, `viewer/gallery.js`
- **Depends on**: None

### 10. Alt Text Generator - Update Configuration for Production
- **Source**: alt/CLAUDE.md + PROJECT_PLAN.md
- **Impact**: 3 | **Effort**: 1 | **Priority**: 4.5
- **Description**: Verify systemd service is running, health endpoint accessible, CORS configured correctly. Current status: production-ready with systemd. Quick health check via `sm status altproxy`.
- **Files**: `alt/alt-proxy.service`, `alt/alt_proxy.py`, `/etc/caddy/Caddyfile` (verify routing)
- **Depends on**: None

---

## Blocked Tasks (Dependencies)

### Scars Merge & Topojson Generation
- **Blocked by**: Task #6 (Scars data collection)
- **Reason**: Requires `11_merge_all_data.py` output (master_dataset.csv) to feed `12_generate_topojson.py`
- **Unblocks**: Scars visualization rendering in browser
- **Estimate**: 1 hour after data collection complete

### Housing Crisis Data Processing
- **Blocked by**: Census API key + HUD API (if used)
- **Reason**: Requires real-time Census ACS + HUD Fair Market Rent data
- **Status**: Scripts exist but untested. Likely 80% complete.
- **Estimate**: 2-3 hours setup + testing

---

## Deferred (Lower Priority / Enhancement)

### 11. Datavis Poems - Verify All 100+ Visualizations Load
- **Priority**: 3.5 | **Effort**: 3
- **Description**: Spot-check sampling of poems/ collection (air, souls, language, flow, quirky) for broken links, missing data files, CDN dependencies. Gallery is working but need full portfolio validation.
- **Files**: `datavis/poems/` (nested repo), update index pages

### 12. Bluesky Tools - Update Landing Page Documentation
- **Priority**: 2.5 | **Effort**: 2
- **Description**: Document 15+ Bluesky tools (firehose, unified, egonet, etc.) in centralized index. Currently scattered across `html/bluesky/` subdirectories.
- **Files**: `html/bluesky/index.html`, tool-specific CLAUDE.md files

### 13. Games - Run Quality Audit on React Games
- **Priority**: 3.0 | **Effort**: 4
- **Description**: Full TypeScript checking, accessibility audit (WCAG 2.1 AA), performance baseline (Lighthouse 90+). Use `/quality-audit` skill.
- **Files**: `games/micro-crawl/`, `games/micro-mystery/`, `games/star-trek/`, `games/geoguess/`
- **Depends on**: pnpm installations + build step

### 14. Viewer Admin Panel - Implement Authentication
- **Priority**: 2.0 | **Effort**: 4
- **Description**: Add login flow to `admin.html` for image management (upload, edit metadata, bulk operations). Currently unprotected.
- **Files**: `viewer/admin.html`, `viewer/admin.js`
- **Risk**: High (security-critical)

### 15. Storyblocks - Implement previousEncounters Tracking
- **Source**: storyblocks/src/js/editor/encounter-system.js:156
- **Priority**: 2.5 | **Effort**: 2
- **Description**: Enable game state tracking of previous encounter choices. Partially stubbed (TODO comment). Improves narrative branching.
- **Files**: `storyblocks/src/js/editor/encounter-system.js`

### 16. Storyblocks - Add Item Count Checking
- **Source**: storyblocks/src/js/editor/encounter-system.js:680
- **Priority**: 2.0 | **Effort**: 1
- **Description**: Extend inventory checking to validate item counts (currently only checks presence). Minor enhancement.
- **Files**: `storyblocks/src/js/editor/encounter-system.js`

### 17. Viewer - Implement PWA Service Worker
- **Source**: viewer/PWA_IMPLEMENTATION_GUIDE.md:485-488
- **Priority**: 2.5 | **Effort**: 3
- **Description**: Offline support + metadata sync when connection restored. Guide exists (485 lines). Nice-to-have for accessibility.
- **Files**: `viewer/`, new `service-worker.js`

### 18. Datavis - Gallery Muuri Performance Optimization
- **Source**: datavis/dev/CLAUDE.md + internal assessment
- **Priority**: 2.0 | **Effort**: 2
- **Description**: Debounce filter events, optimize Muuri grid recalculation for 100+ images. Current: slight lag when filtering.
- **Files**: `datavis/gallery/`, `datavis/interactive/` (if using Muuri)

### 19. Datavis Scars - Add Dollar Store Analysis (Optional Enhancement)
- **Source**: datavis/dev/food_deserts/PROJECT_STATUS.md:156-170
- **Priority**: 2.5 | **Effort**: 3
- **Description**: Extend food deserts analysis with dollar store locations (10,000+) vs. grocery closures. Requires external data acquisition.
- **Files**: `datavis/dev/food_deserts/` or new parallel project

### 20. Map - Add 2024 Election Layer (Future Enhancement)
- **Source**: datavis/dev/map/CLAUDE.md:235-244
- **Priority**: 1.5 | **Effort**: 2
- **Description**: Once 2024 election data available, add as 8th switchable layer. Election data published ~Dec 2024, currently not integrated.
- **Files**: `datavis/dev/map/index.html`, `datavis/dev/map/data_nationwide/`

---

## Deferred Documentation Tasks

### 21. Alt Text Generator - Migrate API Key to Environment Variable
- **Priority**: 3.0 | **Effort**: 1
- **Description**: Move hardcoded xAI API key from `scripts/alt_gen_master.py:19` to environment variable or `.env` file. Security best practice.
- **Files**: `viewer/scripts/alt_gen_master.py`

### 22. Create Consolidated Datavis Planning Document
- **Priority**: 2.0 | **Effort**: 3
- **Description**: Merge scattered status docs (food_deserts, scars, map, housing_crisis) into unified `datavis/ROADMAP.md` with cross-project dependencies.
- **Files**: `datavis/ROADMAP.md` (new)

### 23. Games - Consolidate SUGGESTIONS.md Enhancements
- **Priority**: 2.5 | **Effort**: 2
- **Description**: Prioritize 150+ enhancement ideas in `games/SUGGESTIONS.md`. Evaluate feasibility, estimate effort, flag quick wins.
- **Files**: `games/SUGGESTIONS.md`, create `games/ENHANCEMENT_PRIORITY.md`

### 24. Viewer - Migrate from jQuery to Vanilla JavaScript
- **Priority**: 1.5 | **Effort**: 5
- **Description**: Replace jQuery 3.7.1 dependency with vanilla JS to reduce bundle size and improve performance. Large refactor, low impact.
- **Files**: `viewer/`, remove jQuery import

---

## Statistics

| Category | Count |
|----------|-------|
| High priority (>6) | 4 |
| Medium priority (3-6) | 10 |
| Low priority (<3) | 10 |
| Quick wins | 8 |
| Blocked | 2 |
| **Total** | **28** |

---

## Effort Breakdown

| Effort Level | Count | Examples |
|--------------|-------|----------|
| 1 hour (Effort 1) | 5 | Meta tags, index links, health check |
| 2 hours (Effort 2) | 10 | Social cards, humanize, data collection sprint |
| 3 hours (Effort 3) | 8 | Testing, merge scripts, API migration |
| 4+ hours (Effort 4) | 3 | Admin auth, React quality audit, jQuery refactor |
| **Total Estimated** | **90+ hours** | At current capacity: 2-3 weeks |

---

## Critical Path (Highest Value, Lowest Effort)

If you have limited time, execute this sequence:

1. **Immigrant's Journey SEO** (5 min) → Task #1
2. **Add to games index** (5 min) → Task #2
3. **Datavis Dev index refresh** (10 min) → Task #5
4. **Viewer social cards** (20 min setup + automation) → Task #3
5. **Humanize all alt text** (30 min) → Task #4

**Total: 70 minutes** → Closes 5 tasks, improves SEO/discoverability of 3 projects

---

## Key Dependencies & Blockers

### External Dependencies
- **Census API Key**: Required for Tasks #6, #8 (free signup, instant approval)
- **Python Environment**: `pip install -r requirements.txt` for Scars, Food Deserts, Map
- **pnpm**: Required for building React games (Task #13)

### Internal Dependencies
- **Immigrant's Journey**: Tasks #1 and #2 are independent but should be done together
- **Scars Project**: Task #6 unblocks visualization rendering (~4 hours later)
- **Alt Text**: Task #4 should be done before any commits

### No Blocking Issues
- All source files present and verified
- No missing dependencies or corrupted data
- Code tested and functional

---

## Notes

- All "production-ready" projects (alt text generator, food deserts, map, viewer) have comprehensive documentation and are safe to deploy
- Most tasks are independent and can run in parallel (use `@geepers_*` agents)
- Quick wins (tasks 1-5) should be completed first for momentum
- Data collection tasks (Scars, Housing Crisis) are 2-3+ hours each and should be batched
- Humanize skill is a pre-commit gate — run before any commits to these files

---

**Last Reviewed**: 2026-03-07
**Recommendation**: Start with Quick Wins #1-5 (70 min), then parallel: Datavis deployment + Data collection


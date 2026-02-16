# Task Queue: steam-network

**Generated**: 2026-02-14 16:00
**Project**: Interactive Multi-View Steam Games Visualization (82,000+ games)
**Live URL**: https://dr.eamer.dev/datavis/interactive/steam-network/
**Status**: Core visualization complete. Data pipeline operational. Seven specialized views (scatter, force graph, chord, sankey, treemap, tree, calendar) implemented.

---

## Summary

| Metric | Value |
|--------|-------|
| **Total Tasks Identified** | 12 |
| **Quick Wins (High Impact, Low Effort)** | 4 |
| **High Priority (Impact >= 4)** | 6 |
| **Blocked Tasks** | 1 |
| **Deferred (Low Priority)** | 1 |

---

## Ready to Build (Priority Order)

### 1. [QW] Reduce JSON File Sizes via Gzip Compression
- **Source**: CLAUDE.md (data pipeline review)
- **Impact**: 5 | **Effort**: 1 | **Priority**: 9.0
- **Description**: steam_network.json (41 MB) and steam_all_2005.json (6.2 MB) are uncompressed. Apply gzip compression during build and serve with Content-Encoding header. Browser automatically decompresses.
- **Files**: `build_network_v2.py`, `enrich_data.py` (add gzip output), Caddy config (add gzip middleware)
- **Dependencies**: None
- **Success Criteria**: Initial load time < 2s (currently ~4-5s), files compressed 85-90%
- **Estimate**: 20 minutes

### 2. [QW] Pin Cache-Buster Version for Latest Data
- **Source**: CLAUDE.md (line 194: "Bump the cache-buster version `const _v = 'v=3'`")
- **Impact**: 4 | **Effort**: 1 | **Priority**: 8.0
- **Description**: Last data rebuild used fronkongames dataset from Jan 2026. Update version string in index.html to force cache refresh when deployed.
- **Files**: `index.html` (search for `const _v = 'v=`)
- **Dependencies**: None
- **Success Criteria**: Browser fetches fresh JSON on next visit
- **Estimate**: 3 minutes

### 3. [QW] Add Social Card / OG Image Meta Tags
- **Source**: HTML best practices (~/html/CLAUDE.md mentions og:title, og:image, og:url required on all public pages)
- **Impact**: 3 | **Effort**: 1 | **Priority**: 6.0
- **Description**: Add Open Graph meta tags to `index.html` for social sharing. Use existing `steam-universe-4k.png` (4.3 MB) or resize to optimal social card size (1200x630px).
- **Files**: `index.html` (head section), `steam-universe-4k.png` (already present)
- **Dependencies**: None
- **Success Criteria**: Twitter/Facebook/Discord previews show title, description, image when link shared
- **Estimate**: 15 minutes

### 4. [QW] Document Data Pipeline (README for Ops)
- **Source**: Code review (build_network_v2.py, enrich_data.py, compute_layout.py not documented)
- **Impact**: 3 | **Effort**: 1 | **Priority**: 5.0
- **Description**: Create `DATA_PIPELINE.md` documenting: source datasets, script dependencies, execution order, memory requirements, expected output sizes, cache strategies. Include version history of fronkongames CSV.
- **Files**: Create `DATA_PIPELINE.md` in project root
- **Dependencies**: None
- **Success Criteria**: Someone unfamiliar with project can rebuild data end-to-end from README
- **Estimate**: 25 minutes

---

## High Priority Tasks

### 5. Implement View-Specific Keyboard Shortcuts
- **Source**: ~/html/datavis/ACTION_ITEMS.md (Item #6: "Implement Keyboard Shortcuts", effort 4h)
- **Impact**: 4 | **Effort**: 3 | **Priority**: 5.33
- **Description**: Add keyboard shortcuts for power users: `1-7` = switch views, `+/-` = zoom, `S` = sort/search, `T` = toggle dark/light theme, `?` = help modal. Persist across view changes.
- **Files**: `index.html` (add KeyboardHandler class)
- **Dependencies**: None
- **Success Criteria**: All shortcuts work, help modal documents them, no conflicts with browser shortcuts
- **Estimate**: 2.5 hours

### 6. Implement Data Export (CSV, JSON, PNG)
- **Source**: ~/html/datavis/ACTION_ITEMS.md (Item #4: "Papa Parse + Data Export", effort 2-3h)
- **Impact**: 4 | **Effort**: 3 | **Priority**: 5.33
- **Description**: Add "Export" buttons per-view to download filtered/searched results. Formats: CSV (table views), JSON (network data), PNG (canvas renders). Use Papa Parse for CSV generation.
- **Files**: `index.html` (add ExportManager class)
- **Dependencies**: Papa Parse CDN (lightweight)
- **Success Criteria**: Users can download any visualization state as data or image
- **Estimate**: 2.5 hours

### 7. Add Colorblind-Safe Palette + Pattern Fills
- **Source**: ~/html/datavis/ACTION_ITEMS.md (Item #8: "Colorblind-Safe Palettes", effort 3-4h)
- **Impact**: 4 | **Effort**: 3 | **Priority**: 5.33
- **Description**: Implement deuteranopia/protanopia safe color palettes (ColorBrewer) for rating categories. Add pattern fills (stripes, dots) as alternative to color encoding for accessibility.
- **Files**: `index.html` (color scales + pattern SVG patterns)
- **Dependencies**: None
- **Success Criteria**: All visualizations pass WCAG 2.1 AA color contrast (4.5:1 text, 3:1 UI)
- **Estimate**: 3 hours

### 8. Implement Skeleton Loading States
- **Source**: ~/html/datavis/ACTION_ITEMS.md (Item #5: "Skeleton Loading States", effort 3h)
- **Impact**: 3 | **Effort**: 2 | **Priority**: 4.5
- **Description**: Show pulsing skeleton UI while loading 41 MB network JSON and 6.2 MB game catalog. Add progress bar showing bytes loaded.
- **Files**: `index.html` (add SkeletonLoader + progress UI)
- **Dependencies**: None
- **Success Criteria**: Users see loading feedback instead of blank screen during initial data load
- **Estimate**: 1.5 hours

### 9. Add Breadcrumb Navigation Between Views
- **Source**: UX best practice (7 views, users need clear navigation)
- **Impact**: 3 | **Effort**: 2 | **Priority**: 4.5
- **Description**: Add persistent breadcrumb or tab bar showing current view + quick links to others. Include "Back to Scatter" links in modal panels.
- **Files**: `index.html` (add navigation component)
- **Dependencies**: None
- **Success Criteria**: Users can navigate between views without losing search/filter state
- **Estimate**: 1.5 hours

---

## Medium Priority Tasks

### 10. Optimize Force Graph Physics for Large Networks
- **Source**: Code review (force.js uses D3 force simulation on 9.5K nodes)
- **Impact**: 3 | **Effort**: 4 | **Priority**: 3.5
- **Description**: Current force layout computation takes 5-13s per settlement cycle. Implement: many-body approximation (Barnes-Hut), spatial partitioning, GPU acceleration candidates. Document performance trade-offs.
- **Files**: `force.js` (refactor simulation), `index.html` (timing instrumentation)
- **Dependencies**: Potentially WebGL (optional optimization)
- **Success Criteria**: Force layout settles in < 3s, no UI freeze during computation
- **Estimate**: 4 hours

### 11. Add Dark/Light Theme Toggle (Persistent)
- **Source**: Design best practice (current: dark-only)
- **Impact**: 2 | **Effort**: 2 | **Priority**: 3.0
- **Description**: Implement theme toggle button in header. Persist choice to localStorage. Support CSS variables for dynamic theme switching.
- **Files**: `index.html` (add CSS variables + toggle UI + storage)
- **Dependencies**: None
- **Success Criteria**: Light theme readable at all zoom levels, theme persists across sessions
- **Estimate**: 1.5 hours

---

## Deferred (Low Priority)

### 12. Integrate Observable Plot for Alt Chart Views
- **Source**: ~/html/datavis/ACTION_ITEMS.md (Item #7: "Observable Plot", effort 4-6h, use for exploratory)
- **Impact**: 2 | **Effort**: 4 | **Priority**: 1.0
- **Description**: Research Observable Plot as alternative to D3 for rapid prototyping new visualizations (scatter variants, small multiples). Defer until new chart types are needed.
- **Files**: New experimental view
- **Dependencies**: Observable Plot CDN
- **Success Criteria**: Create 1 proof-of-concept chart using Plot library
- **Estimate**: 4 hours (future sprint)

---

## Blocked Tasks

### Blocked: Performance Audit + WebGL Renderer
- **Blocked by**: Task #10 (Force graph optimization completed first)
- **Reason**: Performance bottleneck analysis needed before WebGL acceleration considered
- **Unblocks**: GPU-accelerated network layout experiments
- **Impact**: 2 | **Effort**: 5+ | **Priority**: Blocked

---

## Statistics

| Category | Count |
|----------|-------|
| High priority (>5.0) | 4 |
| Medium priority (3.0-5.0) | 5 |
| Low priority (<3.0) | 2 |
| Quick wins (Impact >= 3, Effort <= 2) | 4 |
| Blocked | 1 |

---

## Dependency Graph

```
Independent (Ready Now):
  ├─ Task 1 (Cache-buster)
  ├─ Task 2 (OG meta tags)
  ├─ Task 3 (Data pipeline docs)
  ├─ Task 5 (Keyboard shortcuts)
  ├─ Task 6 (Export)
  └─ Task 7 (Colorblind palette)

Sequential:
  Task 8 (Skeleton loading) → Task 5/6 (better UX during load)
  Task 10 (Force optimization) → Task 12 (perf audit)

Independent:
  ├─ Task 9 (Breadcrumbs)
  ├─ Task 11 (Theme toggle)
  └─ Task 4 (Gzip compression) [optional, server-side]
```

---

## Implementation Sequence Recommendation

**Phase 1 (Today - Quick Wins)**: Tasks 1, 2, 3, 4 (< 1 hour total)
**Phase 2 (This Sprint)**: Tasks 5, 6, 7, 8 (8-10 hours, parallelizable)
**Phase 3 (Next Sprint)**: Tasks 9, 10, 11 (6-7 hours)
**Phase 4 (Future)**: Task 12 (exploratory, low priority)

---

## Notes

- Steam-network is in **maintenance mode** post-launch. All core views functional (7 visualization types across scatter, network, hierarchy, temporal).
- Data pipeline is stable with documented input datasets (fronkongames Jan 2026, recommendations.csv 2024).
- Main opportunities: performance optimization (force graph), accessibility (colorblind + theme), and UX polish (export, shortcuts).
- No breaking issues identified. All tasks are enhancements or operational improvements.
- Cache-buster version should be bumped with each data rebuild to ensure users see latest games.

**Next checkpoint**: After Tasks 1-4 complete, validate load times and user engagement metrics.

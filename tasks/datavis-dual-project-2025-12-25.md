# Data Visualization Dual Project Orchestration

**Date**: 2025-12-25
**Orchestrator**: geepers_orchestrator_datavis
**Project Type**: Full Pipeline + Enhancement (Mode 1 + hybrid)

## Project Overview

Two interconnected data visualization projects that demonstrate the spectrum from concrete/analytical ("Strange Places") to enhanced analytical ("Inequality Atlas Layers").

### Project 1: "Strange Places" - Geographic Overlay
**Type**: New D3.js visualization (concrete/analytical with ethereal aesthetic)
**Location**: `/home/coolhand/html/datavis/strange-places/`
**Aesthetic**: X-Files inspired dark mode, mysterious but data-driven

**Data Sources** (all exist):
- UFO Sightings: Hugging Face NUFORC dataset (~80K reports)
- NASA Meteorites: JSON dataset (~45K landings)
- USGS Earthquakes: Real-time GeoJSON feed
- Ghost Sightings: To be fetched by geepers_datavis_data

**Visualization Requirements**:
1. D3.js choropleth US map (or world if data supports)
2. Toggle layers: UFOs, Meteorites, Earthquakes, Ghosts
3. Heatmap overlays showing phenomenon concentration
4. Click county/region for detail panel
5. Time slider for date range filtering
6. Category filters (UFO shapes, meteorite classes, earthquake magnitude, ghost types)

**Color Palette** (proposed):
- UFOs: Blue (#4169E1, Royal Blue)
- Meteorites: Orange/Red gradient (#FF6347, Tomato → #DC143C, Crimson)
- Earthquakes: Yellow (#FFD700, Gold → #FFA500, Orange)
- Ghosts: Purple/Lavender (#9370DB, Medium Purple → #E6E6FA, Lavender)
- Background: Dark (#1a1a2e)
- Text: Off-white (#E0E0E0)

**Technical Stack**:
- D3.js v7 (mapping, interactions)
- TopoJSON (geographic boundaries)
- Vanilla JavaScript (no build step)
- Responsive mobile design

### Project 2: Inequality Atlas - Supplemental Layers
**Type**: Enhancement to existing static D3.js visualization
**Location**: `/home/coolhand/html/datavis/interactive/inequality-atlas/`
**Aesthetic**: Analytical, Swiss design influence, high contrast

**New Data Layers** (optional overlays):
1. **Veterans Layer**: Military service, firearm ownership, PTSD, suicide
   - Data: `/home/coolhand/html/datavis/dev/veterans/data/*.csv` (11 CSVs)
   - Color: Olive/military greens (#556B2F, Dark Olive Green)

2. **Scars (Geology) Layer**: Cretaceous geology correlation with inequality
   - Data: `/home/coolhand/html/datavis/dev/scars/data/modern/*.csv`
   - Color: Earth tones (browns, ochres #8B4513, Saddle Brown)

3. **Food Deserts Layer**: SNAP participation, food access (supplemental to existing)
   - Data: `/home/coolhand/html/datavis/dev/food_deserts/data/*.csv`
   - Color: Orange/red gradient (#FF8C00, Dark Orange)

4. **Housing Crisis Layer**: Evictions, rent burden (adds eviction data to existing)
   - Data: `/home/coolhand/html/datavis/dev/housing_crisis/data/*.csv`
   - Color: Blue/teal (#008B8B, Dark Cyan)

**Implementation Strategy**:
- Add layer toggle UI (checkboxes in control panel)
- Keep existing ICI as primary choropleth
- Layers overlay as semi-transparent choropleth (30-50% opacity)
- Clicking county shows all active layers' data in detail panel
- Lazy-load layer data (not bundled in initial load)
- Update `inequality-atlas/app.js` and `index.html`

**Data Integration Pipeline**:
- Create `scripts/05_add_supplemental_layers.py`
- Merge dev/ CSVs with FIPS-keyed data
- Output: `data/supplemental_layers.csv` with metadata JSON
- Document data sources and merge methodology

## Agent Coordination Plan

### Phase 1: Data Preparation (geepers_datavis_data)
**Responsible Agent**: geepers_datavis_data

**Tasks**:
1. **Audit existing data sources**:
   - Verify UFO data access (Hugging Face cache)
   - Verify NASA meteorite JSON structure
   - Test USGS earthquake GeoJSON endpoint
   - Fetch ghost sightings data (identify source)

2. **Create Strange Places data pipeline**:
   - Script: `strange-places/scripts/01_fetch_phenomena.py`
   - Normalize all datasets to common schema (lat, lon, date, type, metadata)
   - Output: `strange-places/data/phenomena_merged.json`
   - Generate metadata JSON

3. **Create Inequality Atlas supplemental layers pipeline**:
   - Script: `inequality-atlas/scripts/05_add_supplemental_layers.py`
   - Merge veterans, scars, food_deserts, housing_crisis CSVs by FIPS
   - Ensure FIPS standardization (5-digit zero-padded)
   - Output: `inequality-atlas/data/supplemental_layers.csv`
   - Generate metadata JSON

**Deliverables**:
- `~/geepers/reports/by-date/2025-12-25/datavis-data-strange-places.md`
- `~/geepers/reports/by-date/2025-12-25/datavis-data-inequality-layers.md`
- Data validation report (record counts, coverage, missing values)

### Phase 2: Narrative & Story Design (geepers_datavis_story)
**Responsible Agent**: geepers_datavis_story

**Tasks**:
1. **Strange Places narrative framing**:
   - Entry point: "What makes a place strange?"
   - Story arc: Discovery → Investigation → Revelation
   - User journey: Browse map → Filter phenomenon → Discover patterns
   - Emotional tone: Curious, mysterious, inviting (not sensational)
   - Copy: Tooltip text, intro paragraph, category descriptions

2. **Inequality Atlas layer integration narrative**:
   - Framing: "Supplemental Perspectives on Structural Inequality"
   - Explain how layers add depth to ICI
   - Veterans: Military culture & economic stress
   - Scars: Deep time → modern outcomes
   - Food/Housing: Tangible hardship metrics
   - Guide users on combining layers for insights

**Deliverables**:
- `~/geepers/reports/by-date/2025-12-25/datavis-story-strange-places.md`
- `~/geepers/reports/by-date/2025-12-25/datavis-story-inequality-layers.md`
- UX flow diagrams
- Copy deck (all user-facing text)

### Phase 3: Color Palette Design (geepers_datavis_color)
**Responsible Agent**: geepers_datavis_color

**Tasks**:
1. **Strange Places palette**:
   - Dark mode palette (background #1a1a2e)
   - 4 phenomenon colors (UFO blue, meteorite orange/red, earthquake yellow, ghost purple)
   - Ensure colorblind-safe (test with Coblis simulator)
   - Perceptually uniform gradients for heatmaps
   - Hover/active states
   - Export as CSS custom properties

2. **Inequality Atlas layer palette**:
   - 4 layer colors (veterans olive, scars brown, food orange, housing teal)
   - Semi-transparent overlay colors (30-50% opacity)
   - Ensure layers don't obscure existing ICI choropleth
   - Test combinations (which layers work well together visually)
   - Colorblind-safe palette
   - Export as CSS custom properties

**Deliverables**:
- `~/geepers/reports/by-date/2025-12-25/datavis-color-strange-places.md`
- `~/geepers/reports/by-date/2025-12-25/datavis-color-inequality-layers.md`
- CSS files with custom properties
- Accessibility audit (contrast ratios, colorblind simulation)

### Phase 4: Mathematical Encoding (geepers_datavis_math)
**Responsible Agent**: geepers_datavis_math

**Tasks**:
1. **Strange Places scales & encodings**:
   - Heatmap density calculation (kernel density estimation)
   - Time slider scale (linear vs log for long tails)
   - Map projection choice (Albers USA or Mercator for world)
   - Zoom/pan constraints
   - Binning strategy for concentration overlays

2. **Inequality Atlas layer scales**:
   - Normalization strategy for supplemental metrics
   - Opacity mapping for overlay intensity
   - Diverging vs sequential color scales
   - Percentile breaks for layer choropleth

**Deliverables**:
- `~/geepers/reports/by-date/2025-12-25/datavis-math-strange-places.md`
- `~/geepers/reports/by-date/2025-12-25/datavis-math-inequality-layers.md`
- Scale documentation and justification
- Edge case handling (missing data, outliers)

### Phase 5: Visualization Implementation (geepers_datavis_viz)
**Responsible Agent**: geepers_datavis_viz

**Tasks**:
1. **Strange Places D3.js implementation**:
   - File structure: `strange-places/index.html`, `app.js`, `styles.css`
   - D3.js map with TopoJSON boundaries
   - Layer toggle UI (checkboxes)
   - Heatmap overlays (D3 contours)
   - Time slider (D3 brush)
   - Detail panel (county/region click)
   - Category filters (dropdowns)
   - Responsive breakpoints (mobile, tablet, desktop)

2. **Inequality Atlas layer UI**:
   - Add layer controls to existing control panel
   - Implement layer toggle (show/hide)
   - Lazy-load layer data (fetch on first activation)
   - Overlay rendering (semi-transparent choropleth)
   - Update detail panel to show active layer metrics
   - Ensure backwards compatibility (existing ICI functionality)

**Deliverables**:
- `~/geepers/reports/by-date/2025-12-25/datavis-viz-strange-places.md`
- `~/geepers/reports/by-date/2025-12-25/datavis-viz-inequality-layers.md`
- Production-ready code files
- Code documentation and comments

### Phase 6: Design & Accessibility Review
**Collaborating Agents**: geepers_design, geepers_a11y

**Tasks**:
1. **Design review** (geepers_design):
   - Responsive layout validation
   - Swiss design principles application (Inequality Atlas)
   - X-Files aesthetic validation (Strange Places)
   - Touch target size (44px minimum)
   - Typography hierarchy

2. **Accessibility review** (geepers_a11y):
   - WCAG 2.1 AA compliance
   - Keyboard navigation (Tab, Enter, Space, Arrow keys)
   - Screen reader support (ARIA labels, live regions)
   - Contrast ratios (4.5:1 for normal text, 3:1 for large text)
   - Color-blind accessibility
   - Focus indicators

**Deliverables**:
- `~/geepers/reports/by-date/2025-12-25/datavis-design-review.md`
- `~/geepers/reports/by-date/2025-12-25/datavis-a11y-review.md`
- Accessibility remediation checklist

## Integration & Documentation

### Datavis Index Integration
**Tasks**:
1. Add Strange Places to `/home/coolhand/html/datavis/index.html`
2. Add Inequality Atlas layers announcement to index
3. Create social cards for both projects
4. Update navigation menus

### Documentation
**Create for each project**:
- `CLAUDE.md` - Claude Code guidance
- `README.md` - User-facing documentation
- `SESSION_SUMMARY.md` - Development session notes

### Deployment
**Tasks**:
1. Test Strange Places locally (python3 -m http.server)
2. Test Inequality Atlas layers (verify backwards compatibility)
3. Validate all links and assets
4. GoatCounter analytics integration
5. Generate social media cards (Swedish social card generator)

## Success Criteria

### Strange Places
- [ ] All 4 phenomenon types visible on map
- [ ] Layer toggles functional (show/hide)
- [ ] Heatmap overlays show concentration patterns
- [ ] Time slider filters data correctly
- [ ] County/region click shows detail panel
- [ ] Category filters work (UFO shapes, etc.)
- [ ] Responsive on mobile (320px+)
- [ ] Keyboard navigable
- [ ] Screen reader accessible
- [ ] Colorblind-safe palette

### Inequality Atlas Layers
- [ ] 4 supplemental layers available (Veterans, Scars, Food, Housing)
- [ ] Layer data merges correctly with FIPS
- [ ] Layer toggle UI integrated into control panel
- [ ] Lazy-loading works (no initial performance hit)
- [ ] Overlay rendering preserves ICI visibility
- [ ] Detail panel shows active layer metrics
- [ ] Backwards compatible (existing functionality intact)
- [ ] Documentation updated

## Timeline Estimate

**Total Estimated Time**: 8-12 hours across all agents

| Phase | Agent | Estimated Time |
|-------|-------|----------------|
| Data Preparation | geepers_datavis_data | 2-3 hours |
| Narrative Design | geepers_datavis_story | 1-2 hours |
| Color Design | geepers_datavis_color | 1-2 hours |
| Mathematical Encoding | geepers_datavis_math | 1-2 hours |
| Visualization Implementation | geepers_datavis_viz | 3-4 hours |
| Design & A11y Review | geepers_design, geepers_a11y | 1-2 hours |
| Integration & Documentation | Manual | 1 hour |

## Output Summary

**Files Created** (~30+ files):
- Strange Places: index.html, app.js, styles.css, data files, scripts, docs
- Inequality Atlas: updated app.js, updated index.html, new script, new data files, updated docs
- Geepers Reports: 10+ markdown reports in ~/geepers/reports/
- Documentation: 6+ CLAUDE.md/README.md files

**Data Artifacts**:
- `strange-places/data/phenomena_merged.json` (~100MB estimated)
- `inequality-atlas/data/supplemental_layers.csv` (~2MB estimated)
- Metadata JSON files for both projects

**Recommendations**:
- `~/geepers/recommendations/by-project/strange-places.md`
- `~/geepers/recommendations/by-project/inequality-atlas.md`

## Notes

- **Data Quality**: All source datasets already exist; focus on integration and normalization
- **Backwards Compatibility**: Inequality Atlas changes must not break existing functionality
- **Performance**: Strange Places may have large dataset (~100MB JSON); consider pagination or spatial indexing
- **Aesthetic Balance**: Strange Places should be mysterious but not sensational; data-driven, not tabloid
- **Narrative Coherence**: Both projects demonstrate different aspects of data storytelling (discovery vs analysis)

---

**Orchestrator Notes**:
This dual project demonstrates the breadth of data visualization work: building new (Strange Places) and enhancing existing (Inequality Atlas). The coordination requires careful sequencing: data first, then design, then implementation, then review. The agents should collaborate through shared artifacts in ~/geepers/ rather than direct communication.

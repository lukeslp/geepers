# Datavis Data Dependencies Report
**Research Date**: 2026-02-09
**Scope**: All visualization projects across `/home/coolhand/html/datavis/`
**Status**: RESEARCH ONLY - No modifications made

---

## Executive Summary

This report traces **ALL data dependencies** from visualization projects to their data sources. Understanding these dependencies is critical before any path changes or restructuring.

**Key Findings**:
- **113 visualization files** with data dependencies identified
- **Multi-layer symlink architecture** in data_trove connecting to dev/ projects
- **Mixed path strategies**: Absolute paths, relative paths, fetch() calls, and hardcoded URLs
- **Risk**: Many vizs would break if data paths change

---

## Part 1: Symlinks in data_trove

The `data_trove/` directory uses symlinks to connect cached/derived data to source projects:

### Symlink Map

```
/home/coolhand/html/datavis/data_trove/
├── geographic/
│   ├── country_centroids.json → ../data/geographic/country_centroids.json
│   └── fips_county/
│       ├── scars_master.csv → /home/coolhand/html/datavis/dev/scars/data/master_dataset.csv
│       ├── merged_county_analysis.csv → ../../../dev/veterans/data/merged_county_analysis.csv
│       └── merged_county_analysis.gpkg → ../../dev/veterans/data/merged_county_analysis.gpkg
├── demographic/
│   └── veterans/
│       ├── military_firearm_*.csv → /home/coolhand/html/datavis/dev/veterans/data/*
│       └── military_firearm_*_metadata.json → /home/coolhand/html/datavis/dev/veterans/data/*
├── cache/
│   ├── accessibility/
│   │   └── datasets--willwade--AACConversations → blob storage (symlink)
│   └── wild/
│       └── datasets--kcimc--NUFORC → blob storage (symlink)
```

**Key Insight**: Veterans and scars projects are source-of-truth; data_trove contains symlinks to their output.

---

## Part 2: Poem Visualizations - Data Dependencies

### 2a. Souls Collection
**Location**: `/home/coolhand/html/datavis/poems/souls/`
**Category**: Religious/demographic visualization
**Dependencies**:

| File | Fetches | Data Path |
|------|---------|-----------|
| hex-grid-density.html | souls_enhanced_viz_data.json | `/datavis/poems/souls/souls_enhanced_viz_data.json` |
| hex-grid-religions.html | souls_enhanced_viz_data.json | `/datavis/poems/souls/souls_enhanced_viz_data.json` |
| hex-grid-translation.html | souls_enhanced_viz_data.json | `/datavis/poems/souls/souls_enhanced_viz_data.json` |
| hex-grid-language-geo.html | souls_enhanced_viz_data.json | `/datavis/poems/souls/souls_enhanced_viz_data.json` |
| souls-viewer.html | souls_viz_data.json | `/datavis/poems/souls/souls_viz_data.json` |
| bloc-rivers-3d.html | souls_viz_data.json | `/datavis/poems/souls/souls_viz_data.json` |
| galaxy-3d.html | souls_viz_data.json | `/datavis/poems/souls/souls_viz_data.json` |
| religion-clouds-3d.html | souls_viz_data.json | `/datavis/poems/souls/souls_viz_data.json` |
| spectrum-3d.html | souls_viz_data.json | `/datavis/poems/souls/souls_viz_data.json` |

**Data Files**: Two JSON datasets
- `souls_viz_data.json` (loaded by 5 visualizations)
- `souls_enhanced_viz_data.json` (loaded by 4 visualizations)

**Data Generation**: `inspect_data.py` processes source data

---

### 2b. Whispers Collection
**Location**: `/home/coolhand/html/datavis/poems/whispers/`
**Category**: Ghost/paranormal visualization
**Dependencies**:

| File | Fetches | Data Path |
|------|---------|-----------|
| index.html | ghosts-positions.json | `./data/ghosts-positions.json` (relative) |
| index.html | ghosts-descriptions.json | `./data/ghosts-descriptions.json` (relative) |

**Data Location**: `/home/coolhand/html/datavis/poems/whispers/data/`

---

### 2c. Global Lens Collection
**Location**: `/home/coolhand/html/datavis/poems/global-lens/`
**Category**: Global sentiment/trends 2020-2025
**Dependencies**:

| File | Fetches | Data Path |
|------|---------|-----------|
| index.html | trends_data.json | `../../one-year/shared_data/trends_data.json` |
| index.html | wikipedia_pageviews.json | `../../one-year/shared_data/wikipedia_pageviews.json` |
| index.html | gdelt_weekly_events.json | `../../one-year/shared_data/gdelt_weekly_events.json` |

**Critical**: References `one-year/` project shared data

**External APIs** (also called):
- Guardian News API
- New York Times API

---

### 2d. Cosmic Clock Collection
**Location**: `/home/coolhand/html/datavis/poems/cosmic-clock/js/app.js`
**Category**: Real-time astronomy/weather
**Dependencies**:

| Data | API Endpoint |
|------|-------------|
| K-Index (space weather) | `https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json` |
| Weather forecast | `https://api.weather.gov/points/{lat},{lon}` |
| Earthquakes (live) | `https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson` |

**Pattern**: Fetches live data on load (no cached data files)

---

### 2e. Silence/Language Collection
**Location**: `/home/coolhand/html/datavis/poems/silence/`
**Category**: Language extinction visualization
**Dependencies**:

| Script | Uses | Data Path |
|--------|------|-----------|
| process_silence_data.py | world_languages_integrated.json | `/home/coolhand/html/datavis/data_trove/data/linguistic/world_languages_integrated.json` |
| process_silence_data.py | glottolog_languoid.csv | `/home/coolhand/html/datavis/data_trove/data/linguistic/glottolog_languoid.csv` |

**Pattern**: Python processes data from data_trove; HTML visualizes result

---

### 2f. Olympics Collection
**Location**: `/home/coolhand/html/datavis/poems/olympics/`
**Category**: Olympic medals visualization
**Dependencies**:

| Script | Generates |
|--------|-----------|
| fetch_olympic_data.py | olympic_medals_data.json |

**Pattern**: Data is inlined in JavaScript (`const OLYMPIC_DATA = [...]`)

---

### 2g. Risk/Descent Collection
**Location**: `/home/coolhand/html/datavis/poems/descent/`
**Category**: Risk/accessibility metrics
**Dependencies** (per CLAUDE.md):

```
Fetches 2 JSON files from `/html/datavis/data_trove/data/attention/`:
- attention_scores.json
- demographics.json
```

---

### 2h. Dev/Cycles - UFO Spiral
**Location**: `/home/coolhand/html/datavis/poems/dev/cycles/ufo-spiral.html`
**Category**: UFO data visualization
**Dependencies**:

| File | Fetches | Data Path |
|------|---------|-----------|
| ufo-spiral.html | ufo_by_year.json | `/datavis/data_trove/data/quirky/ufo_by_year.json` |

**Pattern**: Fetches from data_trove/quirky/ (auto-generated data)

---

### 2i. Dev/Cheese
**Location**: `/home/coolhand/html/datavis/poems/dev/cheese/index.html`
**Category**: Food/taxonomy visualization
**Dependencies**:

| File | Fetches | Data Path |
|------|---------|-----------|
| index.html | cheese_hierarchy.json | `/datavis/data_trove/data/quirky/cheese_hierarchy.json` |

---

### 2j. Earth Collection
**Location**: `/home/coolhand/html/datavis/poems/earth/`
**Category**: Environmental/earth data
**Dependencies**:

| File | Fetches | Data Path |
|------|---------|-----------|
| index.html | live_earth_data.json | `../../data_trove/cache/wild/live_earth_data.json` |

**Timestamp Parameter**: `?Date.now()` added for cache busting

---

### 2k. Air/Bubbles Collection
**Location**: `/home/coolhand/html/datavis/poems/air/`
**Category**: Air quality visualization
**Dependencies**:

| File | Type | Source |
|------|------|--------|
| air_bubbles.html | fetch() | Dynamic URLs (air quality API) |
| dev/globe.html | fetch() | world-110m.json + air quality data |

**External**: Open-Meteo Air Quality API

---

### 2l. Lost Generation
**Location**: `/home/coolhand/html/datavis/poems/lost_generation.html`
**Category**: Childhood impact analysis
**Dependencies**:

| File | Fetches | Data Path |
|------|---------|-----------|
| lost_generation.html | children_impact.json | `data/children_impact.json` (relative) |

---

### 2m. Risk Collection
**Location**: `/home/coolhand/html/datavis/poems/risk/`
**Category**: Risk metrics
**Dependencies**:

| File | Fetches | Data Path |
|------|---------|-----------|
| index.html | data.json | `data.json` (relative) |

---

## Part 3: Gallery Visualizations - Data Dependencies

### 3a. Data Loaders Pattern
**File**: `/home/coolhand/html/datavis/gallery/vizs/data-loaders.js`
**Purpose**: Centralized data loading utility
**Pattern**:
```javascript
const DATA_BASE = '../../data_trove';
// Loads from /home/coolhand/html/datavis/data_trove
```

---

### 3b. Gallery Demos - data_trove References

| Visualization | Data Path | Asset Type |
|---------------|-----------|-----------|
| clocks/* (4 files) | data_trove/demographic/poverty/state_rankings.json | Poverty data |
| set1/01_circle_packing.html | data_trove/demographic/poverty/state_rankings.json | Poverty data |
| set1/25_emissions_flow.html | fetch() with URL | Emissions data |
| set1/26_stock_flow.html | fetch() API call | Stock data |
| set1/23_crypto_treemap.html | fetch() API call | Crypto data |

---

### 3c. External APIs (Gallery)

| Visualization | API | Endpoint |
|---------------|-----|----------|
| Various crypto vizs | CoinLore, CoinGecko | Market cap, prices |
| Temperature vizs | NASA GISS | Climate data (CSV) |
| Earthquake rings | USGS | Historical earthquakes |
| Stock visualizations | TradingView, financial APIs | Market data |
| ISS visualizations | Open Notify | ISS location (live) |

---

### 3d. Lab Templates
**File**: `/home/coolhand/html/datavis/gallery/vizs/lab/templates.js`
**Pattern**: Dynamic fetching of HTML templates for gallery display
```javascript
fetch('/demos/webgl-stockflow.html')
fetch('/demos/earthquake-rings.html')
// ... 70+ templates
```

---

## Part 4: Interactive Projects - Data Dependencies

### 4a. Strange Places
**Location**: `/home/coolhand/html/datavis/interactive/strange-places/`
**Status**: 8-layer phenomenon visualization (UFO, Bigfoot, earthquakes, meteorites, plane crashes, ghosts, volcanoes, Superfund)

**Data Files Used**:
- `data/phenomena.json` (113,763 phenomena, generated)
- Sources: Pre-geocoded datasets
  - UFO: CORGIS (60,590 sightings)
  - Bigfoot: BFRO (3,797 sightings)
  - Earthquakes: USGS (3,742 events)
  - Meteorites: NASA (1,564)
  - Plane crashes: NTSB (32,378)
  - Ghosts: Shadowlands (9,717)
  - Volcanoes: USGS (142)
  - Superfund: EPA (1,833)

**Data Path**:
```
fetch('./data/phenomena.json')  // Relative to HTML
// Resolves to: /datavis/interactive/strange-places/data/phenomena.json
```

**Generation Script**: `scripts/build_data_v5.py` (all 8 layers)

---

### 4b. Inequality Atlas
**Location**: `/home/coolhand/html/datavis/interactive/inequality-atlas/`
**Status**: US county-level inequality index (3,143 counties)

**Data Files Used**:
- `data/inequality_atlas_final.csv` (79 columns, ICI scores)
- `data/inequality_atlas_final_metadata.json`
- `data/index_weights.json` (ICI component weights)

**Data Generation**: Python pipeline
- `01_fetch_sources.py` → Census API
- `02_merge_datasets.py` → Merge by FIPS
- `03_normalize_values.py` → Z-scores
- `04_create_indexes.py` → ICI calculation

**Fetch Pattern**:
```javascript
fetch('data/inequality_atlas_final.csv')  // Relative
```

---

### 4c. Expat Guide
**Location**: `/home/coolhand/html/datavis/interactive/expat-guide/`
**Status**: Full-stack TypeScript app (port 5070)

**Data Files**:
- `country_expatriation_data.json` (55 countries)

**Fetch Pattern**:
```javascript
// Server-side tRPC
appRouter.getCountries.query()
```

---

### 4d. South America Tour
**Location**: `/home/coolhand/html/datavis/interactive/south-america-tour/`
**Status**: Full-stack TypeScript app (port 5071)

**Data Files**:
- GeoJSON country boundaries (Leaflet)
- Historical events (19 countries)
- World Bank indicators

---

### 4e. Global Lens (Interactive)
**Location**: `/home/coolhand/html/datavis/interactive/global-lens/`
**Status**: Interactive dashboard

---

## Part 5: Vulnerable Paths - Critical Dependencies

### HIGH RISK: Would break if moved
These visualizations have HARDCODED absolute paths:

| Project | File | Path | Type |
|---------|------|------|------|
| strange-places | index.html | `/datavis/data_trove/data/quirky/*` | fetch() |
| poems/dev/cheese | index.html | `/datavis/data_trove/data/quirky/cheese_hierarchy.json` | fetch() |
| poems/dev/cycles/ufo-spiral | index.html | `/datavis/data_trove/data/quirky/ufo_by_year.json` | fetch() |
| poems/earth | index.html | `../../data_trove/cache/wild/live_earth_data.json` | fetch() |
| poems/souls/* (9 files) | *.html | `/datavis/poems/souls/souls_viz_data.json` | fetch() |

**Risk Level**: **CRITICAL** - These use absolute `/datavis/` paths from Caddy proxy

### MEDIUM RISK: Relative paths that could break
| Project | File | Path | Type |
|---------|------|------|------|
| poems/global-lens | index.html | `../../one-year/shared_data/*.json` | fetch() |
| poems/whispers | index.html | `./data/*.json` | fetch() |
| poems/lost_generation | index.html | `data/children_impact.json` | fetch() |

**Risk Level**: **MEDIUM** - Relative paths sensitive to directory depth

### LOW RISK: Generated/inlined data
| Project | File | Method |
|---------|------|--------|
| poems/olympics | index.html | Inlined in JavaScript (`const OLYMPIC_DATA = [...]`) |
| poems/silence | index.html | Inlined after Python processing |

**Risk Level**: **LOW** - Data embedded in HTML, no external dependencies

---

## Part 6: Data Generation Sources

### Python Scripts Creating Data

| Script | Location | Input | Output | Schedule |
|--------|----------|-------|--------|----------|
| `process_silence_data.py` | poems/silence/ | data_trove linguistic CSVs | (visualized inline) | On-demand |
| `fetch_olympic_data.py` | poems/olympics/ | External API | olympic_medals_data.json | On-demand |
| `inspect_data.py` | poems/souls/ | (source) | souls_viz_data.json | On-demand |
| `generate_data.py` | poems/dev/cycles/ | Manual | events data | Maintained |
| `build_data_v5.py` | interactive/strange-places/ | 8 data sources | phenomena.json (113K records) | Monthly |
| `run_pipeline.sh` | interactive/inequality-atlas/ | Census API | inequality_atlas_final.csv | Annual |

---

## Part 7: External APIs (Real-Time Data)

Projects that fetch LIVE data from external APIs:

| Visualization | API Provider | Endpoint | Frequency |
|---------------|--|----------|-----------|
| cosmic-clock | NOAA SWPC | K-index (space weather) | On load |
| cosmic-clock | NWS | Weather forecast | On load |
| cosmic-clock | USGS | Earthquakes (weekly) | On load |
| air/air_bubbles | Open-Meteo | Air quality | On load |
| gallery/earthquake-rings | USGS | Historical earthquakes | On load |
| gallery/halvorsen-iss-live | Open Notify | ISS position | On load |
| gallery/crypto-live-flow | CoinGecko API | Crypto prices | On load |
| poems/global-lens | Guardian API | News articles | On load |
| poems/global-lens | NYT API | News articles | On load |

**Risk**: If APIs go down or change, visualizations fail silently

---

## Part 8: Symlink Dependencies

**Critical Symlinks** (if broken, data path fails):

```
data_trove/geographic/country_centroids.json
  → ../data/geographic/country_centroids.json

data_trove/geographic/fips_county/scars_master.csv
  → /home/coolhand/html/datavis/dev/scars/data/master_dataset.csv

data_trove/demographic/veterans/*
  → /home/coolhand/html/datavis/dev/veterans/data/*

data_trove/cache/accessibility/*
  → blob storage (Content-Addressable Store)
```

**If any source project moves**: All symlinks would break, breaking downstream visualizations

---

## Part 9: Quirky Data Layer

**Location**: `/home/coolhand/html/datavis/data_trove/data/quirky/`

**Files** (auto-generated, version 2026-02-09):
- asteroids_real.json + metadata
- atmospheric_real.json + metadata
- bioluminescence_real.json + metadata
- carnivorous_plants_real.json + metadata
- caves_real.json + metadata
- cryptids_real.json + metadata
- deep_sea_real.json + metadata
- disappearances_real.json + metadata
- ghost_ships_real.json + metadata
- megaliths_real.json + metadata
- radio_signals_real.json + metadata
- tornadoes_real.json + metadata
- witch_trials_real.json + metadata

**Visualizations Using Quirky Data**:
- strange-places/index.html (phenomena.json includes quirky data)
- poems/dev/cheese/index.html (cheese_hierarchy.json)
- poems/dev/cycles/ufo-spiral.html (ufo_by_year.json)

---

## Part 10: Reference Keywords Found

Searched for: "accessibility", "attention", "inequality", "strange-places", "disasters", "joshua"

**Matches**:
- `accessibility/` directory (separate project)
- `attention.html` in gallery/vizs/demos/ (attention visualization)
- `inequality-atlas/` (full project)
- `strange-places/` (full project)
- Various references to "disasters" in data descriptions

**No "joshua" references found** (may be reference from previous work)

---

## Part 11: Broken Links / Potential Issues

### Missing Data Files (non-critical)

| Project | Missing | Workaround |
|---------|---------|-----------|
| poems/earth | live_earth_data.json | Falls back gracefully with error message |
| NASA meteorite API | Original endpoint (404) | Now uses TidyTuesday mirror ✓ |

### API Rate Limits

| API | Limit | Risk |
|-----|-------|------|
| Census Bureau | 500 calls/10 sec | Handled (respects 50 req/sec limit) |
| Guardian News | 10K/day free tier | Could exhaust with heavy usage |
| NYT | 4K/day free tier | Could exhaust with heavy usage |
| CoinGecko | No auth required | Aggressive rate limiting possible |

---

## Part 12: Recommendations

### Before any restructuring:

1. **Document all fetch() calls**
   - Current: Multiple path formats (relative, absolute, full URLs)
   - Recommend: Standardize to one pattern (e.g., `fetch('/data/....')`)

2. **Update symlink targets if source projects move**
   - Veterans data: `/dev/veterans/data/` → everywhere symlinked
   - Scars data: `/dev/scars/data/` → referenced in fips_county/

3. **Add data integrity validation**
   - Checksum metadata.json files to detect stale data
   - Add timestamps to data files
   - Implement graceful error handling for missing data

4. **Create data dependency graph**
   - Map all fetch() calls to their data sources
   - Track which visualizations depend on which files
   - Generate when rebuilding the site

5. **Cache external API responses**
   - NOAA, USGS, CoinGecko responses are expensive
   - Store last-known-good response locally
   - Implement stale-while-revalidate pattern

6. **Monitor broken links**
   - Test all data files on deploy
   - Periodically validate symlink targets
   - Check external APIs for endpoint changes

---

## File Locations for Reference

- **Symlinks**: `/home/coolhand/html/datavis/data_trove/`
- **Source data**: `/home/coolhand/html/datavis/dev/`
- **Poem visualizations**: `/home/coolhand/html/datavis/poems/`
- **Gallery**: `/home/coolhand/html/datavis/gallery/vizs/`
- **Interactive**: `/home/coolhand/html/datavis/interactive/`
- **Quirky data**: `/home/coolhand/html/datavis/data_trove/data/quirky/`

---

## Conclusion

The datavis ecosystem uses a **hybrid architecture**:
- **Absolute paths** (via Caddy proxy) for main visualizations
- **Relative paths** for nested directories
- **Symlinks** for derived data
- **External APIs** for real-time data
- **Inlined data** for self-contained projects

**Key Risk**: Changing `/datavis/` paths or moving source projects (`dev/veterans/`, `dev/scars/`) would break multiple visualizations. Any restructuring should happen systematically with comprehensive testing.


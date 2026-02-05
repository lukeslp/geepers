# Language & Linguistic UIs - Discovery Report

## Executive Summary

Found **3 major language/linguistic visualization projects** with existing web UIs and APIs:

1. **Language History Explorer** - D3.js phylogenetic tree, map, and timeline visualizations
2. **Diachronica Etymology Visualizer** - Flask-based etymology network and heatmap generator
3. **blissAPI Symbol Studio** - AAC symbol search API with interactive web UI

All are production-ready with working infrastructure. No new builds needed - integration and enhancement are the priority.

---

## 1. Language History Explorer

### Location
- **Source**: `/home/coolhand/html/datavis/language/`
- **Production URL**: https://dr.eamer.dev/datavis/language/explorer/
- **Single-file App**: `/home/coolhand/html/datavis/language/explorer/index.html` (78KB, vanilla JS)

### What It Does
Visualizes **360 languages** from linguistic families with three synchronized views:

1. **Tree View (Default)**
   - Phylogenetic tree of language relationships
   - Interactive D3.js force-directed graph
   - Hover to highlight ancestral paths
   - Click for detail drawer

2. **Map View**
   - Geographic distribution of languages
   - Circle size = speaker count
   - Color-coded by language family
   - Okabe-Ito color palette (color-blind safe)

3. **Timeline View**
   - Temporal evolution from 100,000 BCE to present
   - Swimlanes per language family
   - Status indicators: living (green), extinct (gray), proto (amber)
   - Horizontal bar chart with temporal span per language

### Features
- **360 languages** with metadata (ISO-639-3, Glottocode, Wikidata)
- **Filtering**: By status (living/extinct/proto), by macroarea (geographic region)
- **Search**: Full-text across language names, codes, macroarea
- **Detail Drawer**: Family, region, speakers, sources, breadcrumb lineage
- **Responsive**: Desktop-optimized, mobile needs work
- **Accessibility**: WCAG 2.1 AA compliant
- **Performance**: Renders 360 languages in <1 second

### Technologies
- **Frontend**: D3.js v7, TopoJSON v3, vanilla JavaScript
- **Data Format**: JSON (`language-history.json`, 360 nodes)
- **Design**: Swiss Style + Okabe-Ito palette

### Data Schema
```json
{
  "nodes": [
    {
      "id": "english",
      "name": "English",
      "status": "living",
      "family": "Indo-European",
      "iso_639_3": "eng",
      "glottocode": "stan1293",
      "speakers": 1500000000,
      "period_parsed": { "start": -500, "end": null },
      "macroarea": "Eurasia",
      "coordinates": [0, 52]
    }
  ],
  "links": [
    { "source": "proto-indo-european", "target": "english", "type": "parent" }
  ]
}
```

### How to Access
**Local Dev**:
```bash
cd /home/coolhand/html/datavis/language/explorer
python3 -m http.server 8000
# Open http://localhost:8000/index.html
```

**Production**: Direct access at https://dr.eamer.dev/datavis/language/explorer/

### Documentation
- Quick Start: `/home/coolhand/html/datavis/language/explorer/QUICKSTART.md`
- Code Review: `/home/coolhand/html/datavis/language/CODE_REVIEW_REPORT.md`
- Architecture: `/home/coolhand/html/datavis/language/EXPLORER_V3_ARCHITECTURE.md`
- Audit: `/home/coolhand/html/datavis/language/COMPREHENSIVE-AUDIT-2025-12-25.md`

### Known Limitations
1. Mobile optimization needed
2. No export (SVG/PNG download)
3. Timeline zoom uses equal spacing (not temporal)
4. No map clustering for overlapping points
5. Tree uses visual spacing, not temporal branch lengths

---

## 2. Diachronica Etymology Visualizer

### Location
- **Server**: `/home/coolhand/servers/diachronica/etymology/`
- **Production URL**: https://diachronica.com/etymology/ (via Caddy proxy)
- **Symlink**: `/home/coolhand/html/etymology/` (points to server directory)

### What It Does
Real-time **word origin visualization engine** - generates interactive network graphs and temporal heatmaps for any English word.

### Flask API Endpoints

**Core Endpoints**:
- `POST /analyze` - Generate visualization data for a word
  - Input: `{"word": "democracy", "depth": 5}`
  - Output: Network edges, timeline data, narrative
- `GET /health` - Service health check
- `GET /api/word/<word>` - Etymology data for single word

**Visualization Routes** (pre-generated):
- `/view/network/<word>` - Pyvis network graph (HTML)
- `/view/timeline/<word>` - Plotly timeline (HTML)
- `/view/heatmap/<word>` - Matrix visualization (HTML)
- `/view/narrative/<word>` - Text narrative with references

### Pre-Generated Visualizations
Located in `/home/coolhand/servers/diachronica/etymology/static/output/`:

**Available Words**:
- democracy (network, map, timeline)
- philosophy (network, map, timeline)
- algorithm (network, map, timeline)
- biology (network, map, timeline)
- telephone (network, map, timeline)
- emoji (network, map, timeline)

**Visualization Types**:
1. **Network Graph** - Word origin graph with Wiktionary connections
2. **Timeline** - Temporal evolution of word meanings
3. **Map** - Geographic origins and spread
4. **Narrative** - Human-readable etymology story

### Core Models
- `EtymologyFetcher` - Queries Wiktionary API
- `EtymologyGraphBuilder` - Builds origin networks
- `TimelineVisualizer` - Temporal evolution
- `NarrativeGenerator` - Human-readable explanations
- `LanguageFamilyIntegrator` - Connects to language families

### Key Middleware
- **ProxyFix**: Handles X-Forwarded-Prefix from Caddy
- **CORS**: Cross-origin requests allowed
- **Compression**: gzip response compression
- **Rate Limiting**: 1000/day, 100/hour per IP
- **Caching**: Flask-Caching with configurable TTL

### Technologies
- **Framework**: Flask + Flask-CORS + Flask-Compress
- **Visualization**: Pyvis (networks), Plotly (heatmaps), D3 (Sankey)
- **Graph Processing**: NetworkX
- **Data Source**: Wiktionary API (real-time + caching)
- **Logging**: RotatingFileHandler to `/logs/etymology.log`

### Architecture Files
- Main: `app.py` (18KB, fully configured)
- Config: `config.py` (environment-based)
- Models: `/models/` (6 specialized modules)
- Visualization: `/visualization/` (3 specialized modules)
- Templates: `/templates/` (Jinja2)
- Static: `/static/` (CSS, JS, cached outputs)

### Requirements
```
Flask==2.3.0
Flask-CORS==4.0.0
Flask-Compress==1.13
Flask-Limiter==3.3.0
Flask-Caching==2.0.2
requests==2.31.0
networkx==3.1
plotly==5.13.0
pyvis==0.3.0
```

### How to Access
**Local Dev**:
```bash
cd /home/coolhand/servers/diachronica/etymology
source venv/bin/activate
python app.py
# http://localhost:5000/analyze (Flask default)
```

**Production**: Via Caddy reverse proxy at https://diachronica.com/etymology/

### Documentation
- README: `/home/coolhand/servers/diachronica/etymology/README.md`
- Design Report: `/REDESIGN_COMPLETION_REPORT.md`
- Test Suite: `test_linguistics.py`

---

## 3. blissAPI - AAC Symbol Search

### Location
- **Project**: `/home/coolhand/projects/blissAPI/`
- **OpenAPI Spec**: `/home/coolhand/projects/blissAPI/openapi.yaml` (Full REST spec)
- **Web UI**: `/home/coolhand/projects/blissAPI/index.html` (10KB)
- **API Endpoint HTML**: `/home/coolhand/projects/blissAPI/api.html`

### What It Does
**AAC (Augmentative & Alternative Communication) symbol search API** - queries Blissymbolics, SymbolStix, and ARASAAC symbol libraries.

### OpenAPI 3.0 REST API

**Search Endpoints**:
- `GET /api/search?q=<query>` - Search all sources (limit: 1-20)
- `GET /api/search/local?q=<query>` - Search local Bliss/SymbolStix (limit: 1-50)
- `GET /api/search/arasaac?q=<query>` - Search ARASAAC only (limit: 1-50)
- `POST /api/search/batch` - Batch search multiple queries

**Metadata Endpoints**:
- `GET /api/health` - Service health check
- `GET /api/metadata` - Source info and counts
- `GET /api/licenses` - License and attribution details
- `GET /api/cache` - Cache stats and optional clear
- `GET /api/openapi.yaml` - OpenAPI specification

**Asset Endpoints**:
- `GET /symbols/{filename}` - Fetch symbol SVG/image

### Search Response Schema
```json
{
  "query": "happy",
  "results": [
    {
      "keyword": "happy",
      "icon_url": "local:happy.svg",
      "score": 0.95,
      "source": "local",
      "license": "CC0",
      "attribution": "Blissymbolics Community"
    }
  ],
  "total": 3
}
```

### Web UI Features
- **Symbol Search Panel**: Multi-source search with filtering
- **Search History**: Persisted with localStorage
- **Sentence Builder**: Tokenize sentences and map words to symbols
- **Symbol Preview Modal**: Large preview with metadata
- **Export Tools**: Download strips as PNG, SVG, or JSON
- **API Diagnostics**: Health checks, metadata viewer
- **Keyboard Shortcuts**: ? for help, / for search focus, Ctrl+Enter for generate
- **WCAG 2.1 AA Accessibility**: Full screen reader support with ARIA live regions

### Key Files
- **UI**: `/home/coolhand/projects/blissAPI/index.html` (main interface)
- **API Spec**: `openapi.yaml` (3.0.3 compliant)
- **API (v2)**: `api_v2.py` (current backend)
- **Data**: `gloss-map.json` (278KB symbol index)

### Technologies
- **Frontend**: Vanilla JavaScript (no framework), HTML5, CSS3
- **Backend**: Python (api_v2.py)
- **Data Format**: JSON gloss map
- **Symbol Libraries**:
  - Blissymbolics (local SVG)
  - SymbolStix (local SVG)
  - ARASAAC (API integration)

### Documentation
- OpenAPI Spec: Full REST documentation with examples
- HTML UI: Full inline documentation in `index.html`
- Comments: Comprehensive inline comments on all functions

---

## API Comparison Matrix

| Feature | Language Explorer | Etymology Visualizer | blissAPI |
|---------|-------------------|----------------------|----------|
| **Type** | D3 Data Viz | Flask Network API | REST Search API |
| **Data** | 360 languages | Any word (Wiktionary) | 3 symbol libraries |
| **Views** | Tree, Map, Timeline | Network, Timeline, Heatmap | Search results, Detail drawer |
| **Technology** | D3.js v7, vanilla JS | Flask, Pyvis, Plotly | Python + OpenAPI |
| **Caching** | Static JSON | Flask-Caching | Filesystem (gloss-map.json) |
| **Rate Limit** | None | 1000/day, 100/hour | Depends on backend |
| **Mobile** | Desktop-only | Responsive | Mobile-ready |
| **Accessibility** | WCAG 2.1 AA | Not specified | WCAG 2.1 AA |
| **Export** | None | HTML (pre-rendered) | PNG, SVG, JSON |
| **Live Data** | Static snapshot | Wiktionary real-time | Static library |
| **URL** | dr.eamer.dev/datavis/language/explorer/ | diachronica.com/etymology/ | localhost:7777 (dev) |

---

## Integration Opportunities

### 1. Unified Linguistic Dashboard
**Combine all three** into a single "linguistic intelligence platform":
- Central search for words → etymology network + language origins
- From language page → related words etymology → symbol representations

### 2. Cross-Reference Links
- Language Explorer → click language → show etymology of language name
- Etymology pages → click family → link to Language Explorer family tree
- Symbol Studio → click symbol → show languages that use it

### 3. Data Enrichment
- Language Explorer missing: word examples, etymology of language names
- Etymology Visualizer missing: language family classification for origin languages
- blissAPI missing: multilingual symbol names

### 4. New Visualizations Possible
- **Language-Word Network**: Show which languages use which words
- **Symbol-Etymology Timeline**: Trace symbol designs through language evolution
- **Geographic Etymology**: Combine geography + word origins

---

## Recommendations: Build vs. Integrate

### Don't Build (Already Exists)
1. Language phylogenetic tree - ALREADY EXISTS (Language Explorer)
2. Word etymology visualizations - ALREADY EXISTS (Etymology Visualizer)
3. Symbol search API - ALREADY EXISTS (blissAPI)

### Integration (Low-Hanging Fruit)
1. Add cross-links between all three systems
2. Create unified search that hits all three APIs
3. Add language family context to etymology pages
4. Show example sentences using symbols for languages

### Enhancement (Medium Effort)
1. Mobile optimization for Language Explorer
2. Export functionality (SVG/PNG) for Language Explorer
3. Accessibility audit for Etymology Visualizer
4. Real-time symbol variations across languages

### New Development (High Value)
1. Language-Etymology-Symbol unified search
2. Interactive "trace a word's journey" visualization
3. Comparative linguistics tool
4. Educational module pairing language families with symbol innovations

---

## File Locations Summary

### Language History Explorer
```
/home/coolhand/html/datavis/language/
├── explorer/
│   ├── index.html (78KB - full app)
│   ├── data/
│   │   └── countries-110m.json (TopoJSON)
│   ├── QUICKSTART.md
│   └── ENHANCEMENTS.md
├── data/
│   └── language-history.json (360 languages)
├── EXPLORER_V3_ARCHITECTURE.md
├── CODE_REVIEW_REPORT.md
└── COMPREHENSIVE-AUDIT-2025-12-25.md
```

### Diachronica Etymology Visualizer
```
/home/coolhand/servers/diachronica/etymology/
├── app.py (18KB - Flask main)
├── config.py
├── models/
│   ├── etymology_fetcher.py
│   ├── graph_builder.py
│   ├── narrative_generator.py
│   └── ... (6 total)
├── visualization/
│   ├── mermaid_viz.py
│   ├── matrix_viz.py
│   └── timeline_viz.py
├── templates/
├── static/
│   ├── output/ (pre-generated HTML visualizations)
│   └── ... (CSS, JS, cached)
├── tree/ (visualization tree views)
├── requirements.txt
└── REDESIGN_COMPLETION_REPORT.md
```

### blissAPI
```
/home/coolhand/projects/blissAPI/
├── openapi.yaml (Full REST spec, 3.0.3)
├── index.html (Web UI, 10KB)
├── api_v2.py (Current backend)
├── gloss-map.json (278KB symbol index)
├── api.html (API endpoint HTML)
└── bliss_svg/ (Symbol SVGs)
```

---

## Next Steps

1. **Immediate**: Review existing documentation in each project
2. **Short-term**: Create unified search interface hitting all three APIs
3. **Medium-term**: Add cross-links and context enrichment
4. **Long-term**: Build higher-level linguistic intelligence platform

All three are **production-ready and actively maintained**. No rebuilds needed - focus on integration and enhancement.

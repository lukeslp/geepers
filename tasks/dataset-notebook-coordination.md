# Dataset Notebook Creation - Coordination Plan

**Date**: 2026-02-14
**Orchestrator**: geepers_datavis
**Status**: Planning

## Mission

Create Jupyter notebooks for datasets in `/home/coolhand/datasets/` that:
1. Connect datasets to live visualizations in `~/html/datavis/`
2. Demonstrate mathematical elegance and "data is beautiful" aesthetic
3. Meet Kaggle publication requirements
4. Provide discovery pathways for each dataset

## Dataset → Visualization Mapping

### Tier 1: Datasets WITH Notebooks, NEED Visualization Links

| Dataset | Has Notebook | Related Visualizations | Priority |
|---------|--------------|------------------------|----------|
| `accessibility-atlas/` | ✓ (10+ notebooks) | `poems/dev/invisible-populations/` | High - add viz links |
| `us-disasters-mashup/` | ✓ | `poems/quirky/earthquake-pulse.html`, `poems/quirky/tremors.html` | High |
| `strange-places-mysterious-phenomena/` | ✓ | `interactive/strange-places/`, `poems/quirky/phenomena-*.html` | High |
| `world-languages/` | ✓ (2 notebooks) | `poems/language/*` (constellation, tree, pie, network) | High |
| `large-meteorites/` | ✓ | None identified | Medium |
| `noaa-significant-storms/` | ✓ | `poems/quirky/earthquake-pulse.html` (storms) | Medium |
| `usgs-significant-earthquakes/` | ✓ | `poems/quirky/earthquake-pulse.html` | Medium |
| `waterfalls-worldwide/` | ✓ | None identified | Low |
| `witnessed-meteorite-falls/` | ✓ | None identified | Low |

### Tier 2: Datasets WITHOUT Notebooks, WITH Visualizations

| Dataset | Related Visualizations | Priority |
|---------|------------------------|----------|
| `bluesky_kaggle_export/` | `poems/quirky/social-flow.html`, `poems/quirky/social-spiral.html` | **CRITICAL** |
| `etymology_atlas/` | `poems/language/` (all variants) | **CRITICAL** |
| `us-housing-affordability-crisis/` | `poems/dev/weight_of_rent.html` | **CRITICAL** |
| `us-military-veteran-analysis/` | None identified | Medium |
| `titanic-dataset/` | None identified | Low |

### Tier 3: Datasets WITH Visualizations, NEED Complete Integration

| Dataset | Visualization Portfolio | Notes |
|---------|-------------------------|-------|
| `language-data/` | `poems/language/*` (7+ visualizations) | Glottolog, WALS, PHOIBLE data |
| `us-inequality-atlas/` | `interactive/atlas/` (composite index choropleth) | Major project |
| `us-attention-data/` | None identified yet | Wikipedia, Google Trends, GDELT |

## Notebook Design Pattern

Each notebook should follow this structure:

### 1. Header (Markdown)
- Dataset title and one-sentence description
- Credits: Luke Steuber (data collection/curation)
- Links to:
  - Live visualizations (where applicable)
  - GitHub repo (if separate repo)
  - HuggingFace/Kaggle pages

### 2. Data Loading (Code)
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set aesthetic defaults (Swiss design-inspired)
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("muted")
```

### 3. Dataset Overview (Code + Markdown)
- Load data
- Display shape, columns, dtypes
- First/last rows preview
- Missing data summary

### 4. Summary Statistics (Code)
- Descriptive statistics
- Value counts for categorical variables
- Distribution visualizations (elegant histograms, KDE plots)

### 5. Exploratory Visualizations (Code)
- 2-4 mathematically elegant visualizations:
  - Choropleth maps (for geographic data)
  - Time series (for temporal data)
  - Network graphs (for relational data)
  - Scatter plots with perceptually uniform color scales
- Use color palettes from `geepers_datavis_color` principles

### 6. Sample Queries / Use Cases (Code + Markdown)
- 3-5 example questions the dataset can answer
- Show the code to answer each question
- Format results clearly

### 7. Links to Live Visualizations (Markdown)
- If visualization exists, embed screenshot and link
- Explain what the visualization shows
- Technical details (D3.js version, libraries used, etc.)

### 8. Next Steps / Ideas (Markdown)
- Suggest further analysis directions
- Link to related datasets
- Invite contributions

## Visualization Categories

### Abstract/Poetic
- `poems/language/*` - Language evolution as constellations, trees, networks
- `poems/forget-me-not/` - War casualties as forget-me-nots
- `poems/quirky/*` - Data poetry with emotional resonance

### Interactive/Analytical
- `interactive/atlas/` - US inequality composite index
- `interactive/strange-places/` - Unexplained phenomena mapping
- `interactive/expat-guide/` - Expatriation data

### Dashboard/Live Data
- `dashboard/live-earth/` - Real-time earth data

## Agent Dispatch Plan

### Phase 1: Add Visualization Links to Existing Notebooks
**Agent**: `@geepers_datavis_story`
- Update accessibility-atlas notebooks with links to `poems/dev/invisible-populations/`
- Update us-disasters-mashup with links to earthquake/storm visualizations
- Update world-languages notebooks with links to language visualizations
- Add screenshots of visualizations where appropriate

### Phase 2: Create Missing Notebooks (Critical Tier)
**Agent**: `@geepers_datavis_data` + `@geepers_datavis_viz`
- `bluesky_kaggle_export/` → Link to social flow/spiral visualizations
- `etymology_atlas/` → Link to language constellation/tree/pie
- `us-housing-affordability-crisis/` → Link to "weight of rent" visualization

### Phase 3: Mathematical Elegance Review
**Agent**: `@geepers_datavis_math`
- Review all visualizations in notebooks
- Ensure perceptually uniform color scales
- Add scale/transform documentation
- Validate statistical representations

### Phase 4: Color Palette Consistency
**Agent**: `@geepers_datavis_color`
- Ensure notebook visualizations use accessible color palettes
- Match color schemes to live visualizations where applicable
- Document color choices

### Phase 5: Narrative Layer
**Agent**: `@geepers_datavis_story`
- Add emotional hooks to notebook introductions
- Write compelling "next steps" sections
- Ensure each notebook tells a story (not just analysis)

## Success Criteria

- [ ] All Tier 1 datasets have visualization links added
- [ ] All Tier 2 datasets have new notebooks created
- [ ] All notebooks follow consistent design pattern
- [ ] Color accessibility validated (WCAG AA)
- [ ] Mathematical elegance reviewed
- [ ] Each notebook includes 3+ high-quality visualizations
- [ ] Screenshots of live visualizations embedded where applicable
- [ ] All notebooks executable without errors

## Technical Requirements

### Dependencies (include in all notebooks)
```python
# Standard data science stack
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Optional: for maps
import geopandas as gpd
import folium

# Optional: for networks
import networkx as nx

# Optional: for interactive plots
import plotly.express as px
import plotly.graph_objects as go
```

### File Naming
- Main notebook: `demo_notebook.ipynb` (Kaggle standard)
- Specialized notebooks: `{topic}_analysis.ipynb`

### Output Format
- Save figures as PNG with 300 DPI
- Include alt text in markdown cells
- Use descriptive variable names
- Comment complex operations

## Notes

- Kaggle REQUIRES notebooks for featured datasets
- HuggingFace recommends notebooks but doesn't require them
- Notebooks increase discoverability and citation rates
- Live visualization links create a "data storytelling ecosystem"
- Swiss design aesthetic: minimal, geometric, clear typography

## Next Actions

1. Create this task file ✓
2. Dispatch `@geepers_datavis_story` for Phase 1 (add viz links)
3. Dispatch `@geepers_datavis_data` + `@geepers_datavis_viz` for Phase 2 (new notebooks)
4. Review and iterate with math/color agents
5. Final quality check with `@geepers_doublecheck`

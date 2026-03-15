---
description: Data visualization workflow - D3.js, color palettes, narrative design, mathematical elegance
---

# Datavis Mode

Create beautiful, mathematically elegant data visualizations with the "Life is Beautiful" aesthetic.

## Datavis Orchestrator

Launch @geepers_orchestrator_datavis to coordinate:

| Agent | Focus |
|-------|-------|
| @geepers_datavis_viz | D3.js, Chart.js, SVG, force layouts |
| @geepers_datavis_color | Perceptual uniformity, colorblind-safe palettes |
| @geepers_datavis_story | Narrative design, emotional resonance |
| @geepers_datavis_math | Scales, encodings, mathematical elegance |
| @geepers_datavis_data | Data pipelines, Census/SEC/Wikipedia APIs |

## Your Datavis Projects

```
~/html/datavis/
├── billions/        # Wealth visualization
├── dowjones/        # Corporate board interlocks
├── forget_me_not/   # War casualties as flowers
├── language/        # Linguistic visualizations
├── one-year/        # Temporal data
├── stories/         # Narrative visualizations
├── zen/             # Minimalist designs
└── ...
```

## Design Principles

**Swiss Design Aesthetic:**
- 8px grid system
- Helvetica/Inter typography
- Limited color palette (3-5 colors)
- Geometric precision
- White space as design element

**Mathematical Elegance:**
- Perceptually linear scales (sqrt for area)
- Proper aspect ratios
- Golden ratio compositions
- Meaningful visual encodings

**Emotional Resonance:**
- Data reveals human stories
- Metaphors that connect (flowers for lives, etc.)
- Progressive disclosure of complexity
- Viewer journey from curiosity to insight

## Workflows

### New Visualization
1. @geepers_datavis_story - Define narrative and emotional arc
2. @geepers_datavis_data - Gather and validate data
3. @geepers_datavis_math - Choose scales and encodings
4. @geepers_datavis_color - Design palette
5. @geepers_datavis_viz - Implement in D3.js

### Review Existing Viz
Launch in PARALLEL:
- @geepers_datavis_color - Palette review
- @geepers_datavis_math - Encoding accuracy
- @geepers_a11y - Accessibility check

### Data Pipeline
1. @geepers_datavis_data - Fetch from APIs (Census, SEC, etc.)
2. @geepers_data - Validate and enrich
3. @geepers_citations - Verify sources

## Quick Reference

**Color scales:** d3-scale-chromatic, ColorBrewer
**Perceptual:** Lab/LCH color space for uniformity
**Accessibility:** 4.5:1 contrast, colorblind simulation

## Execute

**Mode**: $ARGUMENTS

If no arguments:
- Launch @geepers_orchestrator_datavis for guidance

If "new" or project name:
- Start new visualization workflow

If "review":
- Review existing visualization

If "data":
- Focus on data pipeline

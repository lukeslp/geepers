---
description: Corpus linguistics workflow - COCA, Diachronica, etymology, concordance, and language data
---

# Corpus Mode

Work with corpus linguistics projects - COCA API, Diachronica, etymology visualization.

## Corpus Orchestrator

Launch @geepers_orchestrator_corpus to coordinate:

| Agent | Focus |
|-------|-------|
| @geepers_corpus | Corpus data, NLP resources, linguistic datasets |
| @geepers_corpus_ux | KWIC displays, concordance viewers, research UIs |
| @geepers_db | Query optimization, index tuning |

## Your Corpus Projects

| Project | Port | Location |
|---------|------|----------|
| COCA API | 3034 | ~/servers/coca/ (diachronica) |
| Etymology Viz | 5013 | ~/servers/etymology/ |
| Diachronica Bluesky | 5074 | Historical linguistics bot |

## COCA API

The Corpus of Contemporary American English API:

```
https://dr.eamer.dev/coca/
```

**Key endpoints:**
- `/api/search` - Concordance search
- `/api/collocates` - Collocation analysis
- `/api/frequency` - Word frequency data

**Database:** SQLite corpus with word forms, lemmas, POS tags

## Workflows

### Improve COCA Search
1. @geepers_corpus_ux - Review KWIC interface
2. @geepers_db - Optimize slow queries
3. @geepers_perf - Profile bottlenecks
4. @geepers_a11y - Ensure accessible to researchers

### Add Linguistic Feature
1. @geepers_corpus - Validate linguistic accuracy
2. @geepers_flask - Backend implementation
3. @geepers_corpus_ux - Research-friendly UI
4. @geepers_testing - Test with real queries

### Etymology Visualization
1. @geepers_datavis_story - Narrative design for word histories
2. @geepers_corpus - Ensure etymological accuracy
3. @geepers_datavis_viz - D3.js implementation

## Linguistic Considerations

**KWIC (Key Word In Context):**
- Center alignment on search term
- Consistent column widths
- Sortable by left/right context

**Concordance Best Practices:**
- Show POS tags when relevant
- Link to full sentence context
- Export to research formats (CSV, TSV)

**Collocation Analysis:**
- MI (Mutual Information) scores
- T-scores for significance
- Frequency thresholds

## Related Data Sources

Via @geepers_datavis_data and data_fetching:
- Wikipedia for definitions
- Wiktionary for etymologies
- Academic APIs for citations

## Execute

**Mode**: $ARGUMENTS

If no arguments:
- Show corpus project status and guidance

If "coca":
- Focus on COCA API development

If "etymology":
- Focus on etymology visualization

If "search" or "query":
- Help with concordance/search features

If "ux":
- Focus on research interface design

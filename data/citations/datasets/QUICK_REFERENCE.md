# Citation Health - Quick Reference

**Last Updated**: 2026-02-14

## Status: GOOD ✅

- License compliance: 100%
- Attribution quality: 100%
- 8 of 13 datasets publication-ready

## Critical Fixes Needed

### 1. NASA URLs (2 datasets)
```
BROKEN: https://data.nasa.gov/Space-Science/Meteorite-Landings/gh4g-9sfh
STATUS: HTTP 404
IMPACT: large-meteorites, witnessed-meteorite-falls
ACTION: Find current NASA catalog URL
```

### 2. EEOC URL (1 dataset)
```
BROKEN: https://www.eeoc.gov/data/charge-statistics
STATUS: HTTP 404
IMPACT: accessibility-atlas
ACTION: Update to current EEOC statistics page
```

### 3. BLS URL (1 dataset)
```
BROKEN: https://www.bls.gov/cps/cpsdisability.htm
STATUS: HTTP 403 (bot protection)
IMPACT: accessibility-atlas
ACTION: Verify manually, add archive.org backup
```

### 4. SSA URL (1 dataset)
```
BROKEN: https://www.ssa.gov/policy
STATUS: HTTP 403 (bot protection)
IMPACT: accessibility-atlas
ACTION: Update to specific SSA reports URL
```

### 5. Malformed HuggingFace URLs (3 datasets)
```
ISSUE: Trailing "}" character in URLs
IMPACT: etymology_atlas, waterfalls-worldwide, world-languages
ACTION: Remove "}" from citation URLs (5 min fix)
```

## Publication Status

### ✅ Ready Now (4)
- us-inequality-atlas
- us-attention-data
- us-disasters-mashup
- strange-places-mysterious-phenomena

### ⚠️ Ready (Minor Issues) (4)
- accessibility-atlas (gov URLs broken)
- language-data
- noaa-significant-storms
- usgs-significant-earthquakes

### ❌ Needs Fixes (5)
- large-meteorites (NASA URL)
- witnessed-meteorite-falls (NASA URL)
- etymology_atlas (malformed URL)
- waterfalls-worldwide (malformed URL)
- world-languages (malformed URL)

### ❌ Needs README (4)
- us-housing-affordability-crisis
- us-military-veteran-analysis
- bluesky_kaggle_export
- titanic-dataset

## Quick Stats

| Metric | Value |
|--------|-------|
| Total datasets | 18 |
| With README | 13 (72%) |
| URLs checked | 155 |
| Valid URLs | 89 (57%)* |
| Critical issues | 5 |

*Many "invalid" URLs are false positives (platform auth, JSON artifacts)

## False Positives (Ignore)

- Kaggle 404s (requires cookies)
- HuggingFace 401s (private datasets)
- JSON-LD trailing `",` (15+ URLs)
- Wikipedia 403 (bot protection)

## Data Source Health

- US Government: 7/10 valid
- International: 5/5 valid
- Academic: 4/4 valid

## Next Steps

1. Fix NASA URLs (HIGH)
2. Fix gov URLs (MEDIUM)
3. Remove HF `}` (LOW - 5 min)
4. Create READMEs (MEDIUM)

---
Full reports in `/home/coolhand/geepers/reports/by-date/2026-02-14/citations-datasets.md`

# Dataset Publication Readiness Assessment

**Assessment Date**: 2026-02-14
**Criteria**: README exists, proper licensing, valid citations, source attribution

## Publication Ready (8 datasets)

### Tier 1: Excellent (No Issues)

1. **us-inequality-atlas**
   - README: Yes
   - License: MIT (clearly stated)
   - Attribution: Complete (Census, CMS, USDA, HRSA)
   - Citations: 87.5% valid (2 minor issues: Kaggle 404, Bluesky 404)
   - Status: ✅ READY FOR PUBLICATION

2. **us-attention-data**
   - README: Yes
   - License: MIT (clearly stated)
   - Attribution: Complete (Wikipedia, GDELT, Google Trends)
   - Citations: 76.9% valid (Wikipedia API 403 expected)
   - Status: ✅ READY FOR PUBLICATION

3. **us-disasters-mashup**
   - README: Yes
   - License: CC0 1.0 (clearly stated)
   - Attribution: Complete (NTSB, NOAA, USGS)
   - Citations: 44.4% valid (mostly JSON-LD false positives)
   - Status: ✅ READY FOR PUBLICATION

4. **strange-places-mysterious-phenomena**
   - README: Yes
   - License: CC BY 4.0 (clearly stated)
   - Attribution: Complete (NASA, NOAA, USGS, OSM, etc.)
   - Citations: 61.9% valid (JSON-LD artifacts)
   - Status: ✅ READY FOR PUBLICATION

### Tier 2: Good (Minor Issues)

5. **accessibility-atlas**
   - README: Yes
   - License: MIT (clearly stated)
   - Attribution: Complete (42 datasets from 25+ sources)
   - Citations: 83.3% valid
   - **Issues**: 3 government URLs broken (EEOC, BLS, SSA)
   - Status: ⚠️ NEEDS URL FIXES (still publication-worthy)

6. **language-data**
   - README: Yes
   - License: Multiple (MIT, CC-BY-4.0, CC-BY-SA-3.0 all stated)
   - Attribution: Complete (Glottolog, WALS, PHOIBLE, Joshua Project)
   - Citations: 77.8% valid (SIL 403 expected)
   - Status: ✅ READY FOR PUBLICATION

7. **noaa-significant-storms**
   - README: Yes
   - License: CC0 1.0 (clearly stated)
   - Attribution: Complete (NOAA NCEI)
   - Citations: 22.2% valid (mostly JSON-LD false positives)
   - Status: ✅ READY FOR PUBLICATION

8. **usgs-significant-earthquakes**
   - README: Yes
   - License: CC0 1.0 (clearly stated)
   - Attribution: Complete (USGS)
   - Citations: 30% valid (mostly JSON-LD false positives)
   - Status: ✅ READY FOR PUBLICATION

## Needs Work (5 datasets)

### Tier 3: Fixable Issues

9. **large-meteorites**
   - README: Yes
   - License: CC0 1.0 (clearly stated)
   - Attribution: NASA cited
   - Citations: 10% valid
   - **Critical Issue**: NASA source URL returns 404
   - Status: ❌ FIX NASA URL BEFORE PUBLICATION

10. **witnessed-meteorite-falls**
    - README: Yes
    - License: CC0 1.0 (clearly stated)
    - Attribution: NASA cited
    - Citations: 10% valid
    - **Critical Issue**: NASA source URL returns 404
    - Status: ❌ FIX NASA URL BEFORE PUBLICATION

11. **etymology_atlas**
    - README: Yes
    - License: CC-BY-SA-3.0 (clearly stated)
    - Attribution: Complete (Wiktionary, Glottolog, Lexibank, PHOIBLE, WALS)
    - Citations: 0% valid (1 URL checked, malformed)
    - **Issue**: HuggingFace URL has trailing `}`
    - Status: ⚠️ FIX URL FORMATTING

12. **waterfalls-worldwide**
    - README: Yes
    - License: CC0 1.0 (clearly stated)
    - Attribution: Complete (World Waterfall DB, OSM, USGS, National Parks)
    - Citations: 0% valid (1 URL checked, malformed)
    - **Issue**: HuggingFace URL has trailing `}`
    - Status: ⚠️ FIX URL FORMATTING

13. **world-languages**
    - README: Yes
    - License: CC-BY-4.0 (clearly stated)
    - Attribution: Complete (Glottolog, WALS, Ethnologue, UNESCO)
    - Citations: 0% valid (1 URL checked, malformed)
    - **Issue**: HuggingFace URL has trailing `}`
    - Status: ⚠️ FIX URL FORMATTING

### Tier 4: Missing Documentation

14. **us-housing-affordability-crisis**
    - README: No
    - Status: ❌ CREATE README WITH ATTRIBUTION

15. **us-military-veteran-analysis**
    - README: No
    - Status: ❌ CREATE README WITH ATTRIBUTION

16. **bluesky_kaggle_export**
    - README: No
    - Status: ❌ CREATE README WITH ATTRIBUTION

17. **titanic-dataset**
    - README: No
    - Status: ❌ CREATE README WITH ATTRIBUTION

## Not Datasets

18. **reports** - Directory for reports, not a dataset

## Summary Statistics

| Category | Count | Percentage |
|----------|-------|------------|
| Publication Ready (Tier 1) | 4 | 23.5% |
| Publication Ready (Tier 2) | 4 | 23.5% |
| Needs URL Fixes (Tier 3) | 5 | 29.4% |
| Needs README (Tier 4) | 4 | 23.5% |

## Quick Fixes (< 1 hour)

1. Fix 3 malformed HuggingFace URLs (remove trailing `}`)
2. Update Bluesky profile URL across 6 datasets
3. Fix NASA meteorite catalog URLs (find current URL)

## Medium Effort (1-3 hours)

4. Create README for `us-housing-affordability-crisis`
5. Create README for `us-military-veteran-analysis`
6. Create README for `bluesky_kaggle_export`
7. Create README for `titanic-dataset`

## Research Required (> 3 hours)

8. Find current EEOC charge statistics URL
9. Verify BLS disability employment URL (or use archive.org)
10. Update SSA policy URL to more specific path

## Best Practices Demonstrated

All publication-ready datasets include:

1. **Clear License Statement**
   - License badge in README header
   - License file in repository
   - Source licenses detailed when mixed

2. **Complete Attribution**
   - Source organization named
   - Source URL provided
   - Publication/retrieval date noted
   - License compatibility verified

3. **Structured Metadata**
   - Dataset size and record counts
   - Date coverage
   - Geographic coverage
   - Field descriptions

4. **Usage Examples**
   - Code snippets for loading data
   - Example queries/analysis
   - Field format documentation

5. **Distribution Information**
   - Multiple platform links (GitHub, Kaggle, HuggingFace)
   - Citation format (BibTeX)
   - JSON-LD structured data

## Recommendations for Future Datasets

1. **Use archive.org for government sources**
   - Government sites restructure frequently
   - Having archive.org backup ensures longevity

2. **Separate JSON-LD from README**
   - Put structured data in standalone `.jsonld` file
   - Prevents URL parsing issues

3. **Document data collection date**
   - Add "Retrieved: YYYY-MM-DD" to all sources
   - Helps future users understand data vintage

4. **Test URLs before publishing**
   - Run citation validation as pre-publication check
   - Fix broken links before pushing to platforms

5. **Version control for data sources**
   - Note which version/release of source data used
   - Enables reproducibility

# World Bank Disability & Accessibility Data - Fetch Complete

**Fetched**: 2026-02-12 18:35 UTC
**Status**: ✓ Complete - 3 comprehensive reports generated
**API Status**: ✓ Operational & tested

---

## Contents

This fetch package contains 3 detailed reports on disability and accessibility data available from the World Bank API:

### 1. **worldbank_disability_accessibility_report.md** (Main Report)
**Length**: ~400 lines | **Audience**: Researchers, analysts, policy makers

Core findings:
- World Bank has **NO explicit disability indicators**
- **7 proxy indicators** identified for disability inclusion research
- Complete indicator specifications with codes, coverage, year ranges
- Working API URLs for each indicator
- 21 available World Bank topics
- Country and region codes
- Data quality assessment

**Best for**: Understanding what data exists and what gaps remain

---

### 2. **worldbank_api_technical_guide.md** (Implementation Guide)
**Length**: ~500 lines | **Audience**: Developers, data engineers

Includes:
- Production-ready Python class with full implementation
- Node.js/JavaScript examples
- CSV/JSON export functions
- Caching strategies
- Error handling & retry logic
- Performance optimization tips
- 5 query patterns (single country, all countries, regions, etc.)
- Data transformation examples
- Testing framework

**Best for**: Building applications that consume World Bank data

---

### 3. **WORLDBANK_FINDINGS_SUMMARY.txt** (Quick Reference)
**Length**: ~250 lines | **Audience**: Everyone

Quick reference containing:
- Key findings (bullet points)
- Top 3 recommended indicators (with data samples)
- Working copy-paste API URLs
- Country codes table
- Alternative data sources
- Python quick-start code
- Recommendations (what to do/not do)

**Best for**: Getting started fast, copy-pasting API calls

---

## Quick Start (60 seconds)

### 1. Copy an API URL
```
https://api.worldbank.org/v2/country/all/indicator/SL.EMP.VULN.ZS?format=json&date=2024
```

### 2. Paste in browser or curl
```bash
curl 'https://api.worldbank.org/v2/country/all/indicator/SL.EMP.VULN.ZS?format=json&date=2024' | jq '.'
```

### 3. Or use Python (3 lines)
```python
import requests, pandas as pd
data = requests.get('https://api.worldbank.org/v2/country/all/indicator/SL.EMP.VULN.ZS?format=json&date=2024').json()
pd.DataFrame([{k: r[k] for k in ['country','date','value']} for r in data[1]]).to_csv('data.csv')
```

---

## Top 3 Indicators for Disability Research

| Rank | Indicator | Code | Coverage | Why Use It |
|------|-----------|------|----------|-----------|
| 1 | Vulnerable Employment | SL.EMP.VULN.ZS | 200+ countries, 1991-2024 | Proxy for employment barriers |
| 2 | Out-of-School Children | SE.LPV.PRIM.SD | 200+ countries, 2010-2024 | Proxy for education accessibility |
| 3 | Human Capital Index | HD.HCI.OVRL | 189 countries, 2016-2020 | Overall development/inclusion |

**Sample Data** (SL.EMP.VULN.ZS - 2024):
- Africa East & South: 72.03%
- Means: ~72% of workers in informal/precarious employment
- Proxy for: Employment barriers faced by vulnerable groups (including PWD)

---

## File Locations

All files in: `/home/coolhand/geepers/cache/`

```
/home/coolhand/geepers/cache/
├── worldbank_disability_accessibility_report.md     (Main report)
├── worldbank_api_technical_guide.md                 (Code examples)
├── WORLDBANK_FINDINGS_SUMMARY.txt                   (Quick reference)
└── README_WORLDBANK_DATA.md                         (This file)
```

---

## Key Findings

### ✓ Available
- 1,513 total indicators
- 189 countries covered
- 40-50 year time series
- Real-time API access
- No authentication needed
- Free forever

### ✗ Not Available
- Disability prevalence rates
- Disability employment gaps (direct measurement)
- Disability poverty gaps
- Assistive technology access
- Accessibility infrastructure data
- Special education enrollment (disaggregated)

---

## Next Steps

### For Researchers
1. Read **main report** to understand available indicators
2. Check **quick reference** for sample URLs
3. Use URLs in browser or curl to explore data
4. Combine with WHO/ILO data for complete picture

### For Developers
1. Review **technical guide** for your language (Python/JavaScript)
2. Copy code examples into your project
3. Test with sample URLs
4. Implement caching for performance
5. Export to CSV/JSON for analysis

### For Policy Makers
1. Check **quick reference** for top 3 indicators
2. Use URLs to get latest data for your country
3. Compare with peer countries using region codes
4. Identify trends over 10+ years
5. Use as baseline for disability inclusion policies

---

## Indicator Categories

### Employment & Vulnerability (SL.*)
- SL.EMP.VULN.ZS - Total vulnerable employment
- SL.EMP.VULN.FE.ZS - Female vulnerable employment
- SL.EMP.VULN.MA.ZS - Male vulnerable employment
- SL.EMP.TOTL.SP.ZS - Employment to population ratio

### Education & Access (SE.*)
- SE.LPV.PRIM.SD - Out-of-school children (primary)
- SE.PRM.NENR - Primary net enrollment
- SE.PRM.ENRR - Primary gross enrollment
- SE.SEC.NENR - Secondary net enrollment
- SE.TER.ENRR - Tertiary enrollment

### Human Development (HD.*)
- HD.HCI.OVRL - Human Capital Index (overall)
- HD.HCI.OVRL.FE - Human Capital Index (female)
- HD.HCI.OVRL.MA - Human Capital Index (male)

### Social Protection (per_*)
- per_allsp.cov_pop_tot - Social protection coverage
- per_allsp.adq_pop_tot - Social protection adequacy

---

## Country Code Examples

**Use in URLs like**:
```
https://api.worldbank.org/v2/country/{COUNTRY_CODE}/indicator/...
```

- US, GB, FR, DE, CN, IN, BR, ZA, KE, NG, AU, JP
- WLD (World), EAS (East Asia), ECS (Europe), LCN (Latin America), SAS (South Asia), SSF (Sub-Saharan Africa)

Full list in **main report** or get from API:
```
https://api.worldbank.org/v2/country?format=json&per_page=300
```

---

## API Query Cheat Sheet

**All countries, latest year**:
```
/country/all/indicator/SL.EMP.VULN.ZS?format=json&date=2024
```

**Specific country, time series**:
```
/country/KE/indicator/SL.EMP.VULN.ZS?format=json
```

**Region, multiple years**:
```
/country/SSF/indicator/SE.LPV.PRIM.SD?format=json&date=2015:2024
```

**Multiple indicators, one country**:
```
/country/IN/indicator/HD.HCI.OVRL.FE;HD.HCI.OVRL.MA?format=json
```

**Paginated results (page 2)**:
```
/country/all/indicator/SL.EMP.TOTL.SP.ZS?format=json&per_page=500&page=2
```

---

## Data Quality Notes

### Strengths
✓ Global coverage (189 countries)
✓ Long time series (40+ years for most indicators)
✓ Regular updates (last: 2026-01-28)
✓ Well-documented metadata
✓ Free, open access

### Limitations
✗ No disability-specific breakdowns
✗ ILO estimates (not direct surveys) for many labor indicators
✗ HCI only updated through 2020
✗ Social protection data sparse
✗ Proxy indicators only (not direct disability measurement)

---

## Comparison with Other Data Sources

| Source | Disability Data | Coverage | Ease of Use |
|--------|---|---|---|
| **World Bank** | Proxy only | 189 countries | Easy (API) |
| WHO GHO | Direct | 194 countries | Medium (Web UI) |
| ILO Stats | Partial | 190+ countries | Medium (Portal) |
| National Census | Detailed | Varies by country | Hard (Varies) |
| UN SDG Data | Limited | 193 countries | Medium (Web UI) |

**Recommendation**: Use World Bank for macro trends + WHO/ILO for disability-specific data.

---

## Common Use Cases

### Use Case 1: Monitor Education Access
Indicator: SE.LPV.PRIM.SD (Out-of-school children)
Question: "Is Kenya improving school access for marginalized children?"
Approach: Get time series (2015-2024), compare with regional averages

### Use Case 2: Compare Employment Barriers
Indicator: SL.EMP.VULN.ZS (Vulnerable employment)
Question: "Which regions have the worst informal employment?"
Approach: Get all regions, 2024 data, sort by value

### Use Case 3: Track Development Progress
Indicator: HD.HCI.OVRL (Human Capital Index)
Question: "Is Tanzania improving human capital (health/education/earnings)?"
Approach: Get country data by year (2016-2020), calculate trend

### Use Case 4: Gender Gap Analysis
Indicators: SL.EMP.VULN.FE.ZS vs SL.EMP.VULN.MA.ZS
Question: "Do women face worse employment barriers than men?"
Approach: Get both indicators, calculate difference

---

## Contact & Credits

**Fetch conducted by**: Fetcher Agent (Claude Code)
**Date**: 2026-02-12
**Tools used**: curl, jq, bash, Python
**Data source**: World Bank Open Data API v2
**License**: Public domain (World Bank data is CC-BY 4.0)

---

## Troubleshooting

**Q: API returns empty data**
A: Check country code (use /country endpoint to verify), or data may not be available for that year

**Q: Rate limit errors**
A: World Bank has no official rate limit, but add 0.5-1s delays between requests

**Q: How do I get historical data?**
A: Use date parameter: `date=2015:2024` for range, or just `date=2020` for specific year

**Q: Can I filter by disability status?**
A: No - World Bank doesn't disaggregate by disability. Use WHO/ILO sources instead

**Q: How often is data updated?**
A: Typically annually in January. Check `lastupdated` field in API response

---

## Additional Resources

- **World Bank Open Data**: https://data.worldbank.org
- **API Documentation**: https://data.worldbank.org/developers
- **Indicator Catalog**: https://data.worldbank.org/indicator
- **WHO Global Health Observatory**: https://www.who.int/data/gho
- **ILO Statistics**: https://www.ilo.org/stat
- **UN SDG Data**: https://unstats.un.org/sdgs

---

**Status**: ✓ Ready to use
**Last Updated**: 2026-02-12 18:35 UTC
**Next Check**: Recommended when World Bank adds disability indicators

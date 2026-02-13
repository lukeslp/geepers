# World Bank API - Disability & Accessibility Data Report

**Fetched**: 2026-02-12
**Status**: Comprehensive API survey completed
**Data Source**: World Bank Open Data API v2

---

## Executive Summary

The World Bank API does **not contain explicit disability-specific indicators** as a dedicated category. However, the API provides rich data on **vulnerable populations, inclusive education, employment gaps, and human capital development** that indirectly measure disability inclusion. The most relevant proxy indicators are:

1. **Vulnerable Employment** (SL.EMP.VULN.*)
2. **Out-of-School Children** (SE.LPV.PRIM.SD)
3. **Human Capital Index** (HD.HCI.*)
4. **Social Protection Coverage** (per_allsp.*)

---

## Finding #1: No Direct Disability Indicators

After searching 1,513+ indicators across World Bank sources, **no indicators explicitly labeled "disability", "blind", "deaf", "impair", "autism", or "handicap"** were found in the World Development Indicators (Source 2 - the primary data source).

**Implication**: Disability-disaggregated data must be sourced from:
- World Health Organization (WHO) Global Health Observatory
- International Labour Organization (ILO) disability data
- National census and household survey data
- Specialized disability surveys (e.g., Washington Group Questions)

---

## Finding #2: Available Proxy Indicators for Disability Inclusion

### Category 1: Employment & Vulnerability (SL.* indicators)

These indicators indirectly measure employment barriers faced by vulnerable groups including people with disabilities:

| Indicator Code | Name | Data Format | Coverage |
|---|---|---|---|
| **SL.EMP.VULN.ZS** | Vulnerable employment, total (% of total employment) | % | 200+ countries, 1991-2024 |
| SL.EMP.VULN.FE.ZS | Vulnerable employment, female (% of female employment) | % | Limited coverage |
| SL.EMP.VULN.MA.ZS | Vulnerable employment, male (% of male employment) | % | Limited coverage |
| **SL.EMP.TOTL.SP.ZS** | Employment to population ratio, 15+ (% modeled ILO) | % | 200+ countries, 1991-2024 |
| **SL.EMP.1524.SP.ZS** | Employment to population ratio, ages 15-24 (%) | % | 200+ countries |
| SL.EMP.SELF.ZS | Self-employed, total (% of total employment) | % | ILO modeled estimates |
| SL.EMP.WORK.ZS | Wage and salaried workers, total (% of employment) | % | ILO modeled estimates |

**Use Case**: Vulnerable employment rate is a proxy for informal/precarious work that people with disabilities often face due to accessibility barriers.

**Sample Data** (SL.EMP.VULN.ZS):
- Africa Eastern and Southern (2024): 72.03%
- Africa Eastern and Southern (2023): 72.28%
- Trend: Relatively stable at ~71-72% since early 2000s

**API Endpoint**:
```
https://api.worldbank.org/v2/country/all/indicator/SL.EMP.VULN.ZS?format=json&per_page=500
https://api.worldbank.org/v2/country/{COUNTRY_CODE}/indicator/SL.EMP.VULN.ZS?format=json
```

---

### Category 2: Education & Access (SE.* indicators)

Key indicators measuring educational inclusion, relevant to students with disabilities:

| Indicator Code | Name | Coverage | Year Range |
|---|---|---|---|
| **SE.LPV.PRIM.SD** | Primary school age children out-of-school (%) | 200+ countries | 2010-2024 |
| SE.LPV.PRIM.SD.FE | Female primary school age children out-of-school (%) | Limited | 2010-2024 |
| SE.LPV.PRIM.SD.MA | Male primary school age children out-of-school (%) | Limited | 2010-2024 |
| **SE.PRM.NENR** | School enrollment, primary (% net) | 200+ countries | 1970-2024 |
| SE.PRM.ENRR | School enrollment, primary (% gross) | 200+ countries | 1970-2024 |
| **SE.SEC.NENR** | School enrollment, secondary (% net) | 200+ countries | 1970-2024 |
| **SE.TER.ENRR** | School enrollment, tertiary (% gross) | 200+ countries | 1970-2024 |
| SE.PRM.ENRL.TC.ZS | Pupil-teacher ratio, primary | 200+ countries | 1970-2024 |
| SE.LPV.PRIM | Learning poverty (% adjusted for out-of-school) | 189 countries | 2000-2024 |

**Use Case**: Out-of-school children rates and learning poverty are proxies for educational exclusion including children with disabilities.

**Sample Data** (SE.PRM.ENRR - Primary Enrollment):
- Africa Eastern and Southern (2024): 101.31% (gross enrollment)
- Africa Eastern and Southern (2023): 100.86%
- Trend: Increasing from 66.27% (1975) to >100% (overage enrollment due to late starters)

**API Endpoint**:
```
https://api.worldbank.org/v2/country/all/indicator/SE.LPV.PRIM.SD?format=json&per_page=500
https://api.worldbank.org/v2/country/all/indicator/SE.PRM.NENR?format=json&per_page=500
```

---

### Category 3: Human Capital & Development (HD.HCI.* indicators)

The Human Capital Index is the World Bank's key measure of human development:

| Indicator Code | Name | Scale | Coverage |
|---|---|---|---|
| **HD.HCI.OVRL** | Human Capital Index overall | 0-1 | 189 countries, 2016-2020 |
| HD.HCI.OVRL.FE | Human Capital Index, Female | 0-1 | 189 countries, 2016-2020 |
| HD.HCI.OVRL.MA | Human Capital Index, Male | 0-1 | 189 countries, 2016-2020 |
| HD.HCI.OVRL.LB | Human Capital Index, Lower Bound | 0-1 | 189 countries |
| HD.HCI.OVRL.UB | Human Capital Index, Upper Bound | 0-1 | 189 countries |

**Composition**: HCI = (Health + Education + Employment Earnings) / 3
- Health: Survival to age 5, adult survival
- Education: Average years of schooling, expected years of schooling
- Employment: Earnings as proxy for productivity

**Use Case**: Countries with lower HCI may have worse disability inclusion in health, education, and employment.

**Sample Data** (HD.HCI.OVRL):
- Afghanistan (2020): 0.400 (1 = perfect)
- Afghanistan (2018): 0.393
- Afghanistan (2017): 0.389

**API Endpoint**:
```
https://api.worldbank.org/v2/country/all/indicator/HD.HCI.OVRL?format=json&per_page=500
```

---

### Category 4: Social Protection & Labor Programs (per_* indicators)

Poverty-focused social protection indicators:

| Indicator Code | Name | Type | Coverage |
|---|---|---|---|
| **per_allsp.cov_pop_tot** | Coverage of social protection and labor programs (% of population) | % | Limited, from household surveys |
| per_allsp.adq_pop_tot | Adequacy of social protection (% of total welfare) | % | Limited |
| per_allsp.ben_q1_tot | Benefit incidence to poorest quintile (%) | % | Limited |
| **per_lm_alllm.cov_pop_tot** | Coverage of unemployment benefits and ALMP (%) | % | Limited |

**Use Case**: Social protection coverage is relevant for disability benefit programs and welfare systems.

**Note**: These indicators have **very limited country coverage** compared to mainstream indicators.

**API Endpoint**:
```
https://api.worldbank.org/v2/country/all/indicator/per_allsp.cov_pop_tot?format=json
```

---

## Available Topics in World Bank API

The World Bank organizes 21 data topics. **None are disability-specific**, but these are most relevant:

| Topic ID | Topic | Relevance to Disability |
|---|---|---|
| 4 | Education | Primary/secondary enrollment, learning outcomes |
| 8 | Health | Health systems, nutrition, disease prevention |
| 10 | Social Protection & Labor | Employment, unemployment, social safety nets |
| 11 | Poverty | Poverty measures, inequality, vulnerable populations |
| 15 | Social Development | Gender, child labor, refugees |
| 17 | Gender | Gender equality metrics |

**API Endpoint for Topics**:
```
https://api.worldbank.org/v2/topic?format=json
```

---

## Data Access: Complete API Reference

### Base Endpoints

**List All Indicators** (1,513 total):
```
https://api.worldbank.org/v2/indicator?format=json&per_page=1000&source=2
```

**Get Data for Specific Indicator** (17,290+ data points per indicator):
```
https://api.worldbank.org/v2/country/all/indicator/{INDICATOR_CODE}?format=json
https://api.worldbank.org/v2/country/{COUNTRY_CODE}/indicator/{INDICATOR_CODE}?format=json
https://api.worldbank.org/v2/country/{REGION_CODE}/indicator/{INDICATOR_CODE}?format=json
```

**Parameters**:
- `format=json` - JSON output
- `per_page=500` - Results per page (max 500)
- `date=YYYY` or `date=YYYY:YYYY` - Filter by year/year range

### Example Requests

**Get vulnerable employment for all countries (2024)**:
```bash
curl 'https://api.worldbank.org/v2/country/all/indicator/SL.EMP.VULN.ZS?format=json&date=2024'
```

**Get out-of-school children for a specific country (Kenya)**:
```bash
curl 'https://api.worldbank.org/v2/country/KE/indicator/SE.LPV.PRIM.SD?format=json'
```

**Get education enrollment data for multiple countries**:
```bash
curl 'https://api.worldbank.org/v2/country/GB;US;DE;JP/indicator/SE.TER.ENRR?format=json&date=2020'
```

**Get Human Capital Index (gender-disaggregated)**:
```bash
curl 'https://api.worldbank.org/v2/country/all/indicator/HD.HCI.OVRL.FE;HD.HCI.OVRL.MA?format=json'
```

---

## JSON Response Format

```json
[
  {
    "page": 1,
    "pages": 35,
    "per_page": 500,
    "total": 17290,
    "sourceid": "2",
    "lastupdated": "2026-01-28"
  },
  [
    {
      "indicator": {
        "id": "SL.EMP.VULN.ZS",
        "value": "Vulnerable employment, total (% of total employment)"
      },
      "country": {
        "id": "ZH",
        "value": "Africa Eastern and Southern"
      },
      "countryiso3code": "AFG",
      "date": "2024",
      "value": 72.0294162913247,
      "unit": "",
      "obs_status": "",
      "decimal": 0
    }
  ]
]
```

**Key Fields**:
- `indicator.id`: Machine-readable indicator code
- `country.value`: Country or region name
- `countryiso3code`: ISO 3-letter country code
- `date`: Year
- `value`: Numeric value (null if not available)
- `decimal`: Decimal places

---

## Country & Region Codes

The World Bank covers **189 countries** plus **regional aggregates**.

**Sample Country Codes**:
- US = United States
- GB = United Kingdom
- KE = Kenya
- IN = India
- BR = Brazil
- CN = China
- ZA = South Africa
- NG = Nigeria

**Regional Aggregates**:
- ZH = Africa Eastern and Southern
- ZI = Africa Western and Central
- EAS = East Asia & Pacific
- ECS = Europe & Central Asia
- LCN = Latin America & Caribbean
- MEA = Middle East & North Africa
- SAS = South Asia
- SSF = Sub-Saharan Africa
- WLD = World

**Get All Countries**:
```bash
curl 'https://api.worldbank.org/v2/country?format=json&per_page=300'
```

---

## Data Quality & Coverage Notes

### Strengths
- **Long time series**: Most indicators span 40-50 years
- **Global coverage**: 189 countries
- **Regular updates**: Last updated 2026-01-28
- **Granular**: Gender-disaggregated, age-group breakdowns
- **Free access**: No authentication required

### Limitations for Disability Analysis
- **No explicit disability indicators**: Must use proxies
- **Limited social protection data**: Only covers select countries/years
- **ILO modeled estimates**: Many labor indicators are UN estimates, not direct surveys
- **No disability-disaggregated breakdowns**: Can't filter by disability status
- **Outdated HCI**: Last update 2020 (5-year gap)

### Data Gaps
| Topic | Gap |
|---|---|
| Disability prevalence | NOT available in World Bank API |
| Disability employment gap | Must be inferred from vulnerable employment data |
| Disability poverty gap | Must be inferred from social protection coverage |
| Accessibility features (ramps, braille, ASL, etc.) | NOT tracked |
| Assistive technology access | NOT tracked |
| Special education enrollment | NOT tracked (included in general SE.* indicators) |

---

## Recommended Proxy Indicators for Disability Research

### Tier 1: Most Relevant (Direct Proxies)

1. **SL.EMP.VULN.ZS** - Vulnerable employment
   - Captures informal/precarious work
   - Global coverage, 1991-2024
   - Proxy for employment barriers

2. **SE.LPV.PRIM.SD** - Out-of-school children
   - Captures educational exclusion
   - 200+ countries, 2010-2024
   - Proxy for school accessibility barriers

3. **HD.HCI.OVRL** - Human Capital Index
   - Composite measure of health, education, earnings
   - 189 countries, 2016-2020
   - Proxy for overall development/inclusion

### Tier 2: Supporting Indicators

4. **SE.PRM.NENR** - Primary net enrollment rate
5. **SE.TER.ENRR** - Tertiary enrollment rate
6. **SL.EMP.TOTL.SP.ZS** - Employment to population ratio
7. **per_allsp.cov_pop_tot** - Social protection coverage

---

## Alternative Data Sources

Since World Bank lacks disability-specific data, consider:

### WHO Global Health Observatory
- Disability prevalence rates
- WHO Disability Assessment Schedule (WHODAS)
- World Disability Report data

### ILO Statistics
- Labor force surveys with disability module
- Global Employment Trends reports
- Disability employment data

### National Statistical Offices
- Census data (US Census includes disability questions)
- Labour Force Surveys (LFS)
- Household surveys (Demographic Health Surveys, etc.)

### Specialized Databases
- UN DESA Disability Data Portal
- Disability Rights Council databases
- National disability monitoring systems

---

## Report Metadata

- **API Version**: World Bank API v2
- **Data Source**: World Development Indicators (Source 2)
- **Total Indicators**: 1,513
- **Total Countries/Regions**: 189 + aggregates
- **Year Coverage**: 1960-2026 (varies by indicator)
- **Last Updated**: 2026-01-28
- **API Status**: Fully operational, free access
- **Query Time**: Real-time responses
- **Rate Limiting**: None observed (reasonable use expected)

---

## Conclusion

The World Bank API is **not optimized for disability research** due to lack of explicit disability indicators. However, it provides valuable **proxy indicators for measuring inclusion barriers** in employment, education, and human development.

**Best Use Case**: Tracking disability inclusion progress through changes in vulnerable employment rates, school enrollment, and human capital development over time at the national/regional level.

**Limitation**: Cannot replace disability-specific surveys or disaggregated data from WHO, ILO, or national sources for precise disability prevalence, barriers, or needs assessment.

---

## Quick Reference: Working API URLs

```
# Vulnerable Employment (all countries, latest year)
https://api.worldbank.org/v2/country/all/indicator/SL.EMP.VULN.ZS?format=json&date=2024

# Out-of-School Children (all countries)
https://api.worldbank.org/v2/country/all/indicator/SE.LPV.PRIM.SD?format=json

# Human Capital Index (all countries)
https://api.worldbank.org/v2/country/all/indicator/HD.HCI.OVRL?format=json

# Primary Enrollment (all countries)
https://api.worldbank.org/v2/country/all/indicator/SE.PRM.NENR?format=json

# Tertiary Enrollment (all countries)
https://api.worldbank.org/v2/country/all/indicator/SE.TER.ENRR?format=json

# Social Protection Coverage (limited countries)
https://api.worldbank.org/v2/country/all/indicator/per_allsp.cov_pop_tot?format=json

# Get all available indicators
https://api.worldbank.org/v2/indicator?format=json&per_page=1000&source=2

# Get all countries
https://api.worldbank.org/v2/country?format=json&per_page=300
```

---

**Report Generated**: 2026-02-12 18:30 UTC
**Fetcher**: Claude Code Fetch Specialist
**Cache Location**: `/home/coolhand/geepers/cache/worldbank_disability_accessibility_report.md`

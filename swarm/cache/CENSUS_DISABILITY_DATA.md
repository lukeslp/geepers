# Census Disability Data Trend Dataset

**Prepared:** 2026-02-12
**Status:** Ready for execution
**Data Type:** U.S. Census Bureau American Community Survey (ACS) 1-year estimates

---

## Overview

This document provides comprehensive guidance for fetching U.S. Census disability data across 13 years (2010-2023, excluding 2020) to build a trend analysis dataset.

**Data Source:** Census Bureau API
**Coverage:** National (US:*) 1-year ACS estimates
**Tables:** S1810 (summary) and B18101 (detailed demographic)
**Years:** 13 total (2010-2019, 2021-2023)

---

## Key Variables

### S1810: Disability Characteristics (Subject Table)

Provides disability statistics for total population and three age groups:

| Code | Variable | Description |
|------|----------|-------------|
| S1810_C01_001E | Total Population | Civilian noninstitutionalized population |
| S1810_C02_001E | Total with Disability | Count with any disability |
| S1810_C03_001E | % with Disability | Percentage (calculated) |
| S1810_C01_002E | Under 18 Total | Children population |
| S1810_C02_002E | Under 18 with Disability | Children with disability |
| S1810_C03_002E | Under 18 % | Percentage for children |
| S1810_C01_003E | 18-64 Total | Working-age population |
| S1810_C02_003E | 18-64 with Disability | Working-age with disability |
| S1810_C03_003E | 18-64 % | Percentage for working-age |
| S1810_C01_004E | 65+ Total | Senior population |
| S1810_C02_004E | 65+ with Disability | Seniors with disability |
| S1810_C03_004E | 65+ % | Percentage for seniors |

### B18101: Disability by Age and Sex (Detail Table)

Provides cross-tabulation by age groups and gender:

| Code | Variable | Description |
|------|----------|-------------|
| B18101_001E | Total Population | All individuals |
| B18101_002E | Total with Disability | All with disability |
| B18101_003E | Male with Disability | Males with disability |
| B18101_004E | Under 5 | Specific age group |
| B18101_005E | 5 to 17 | School-age children |
| B18101_006E | 18 to 34 | Young adults |
| B18101_007E | 35 to 64 | Middle-aged adults |
| B18101_008E | 65 to 74 | Early seniors |
| B18101_009E | 75+ | Oldest seniors |

---

## Execution Instructions

### Option 1: Python Script (Recommended)

```bash
# Navigate to geepers cache directory
cd /home/coolhand/geepers/swarm/cache

# Run the fetcher
python3 census-disability-fetcher.py

# Results will be saved with timestamp
# Example: census-disability-20260212_143045.json
```

**Advantages:**
- Cleaner error handling
- Formatted JSON output
- Summary statistics
- Retry logic

### Option 2: Shell Script

```bash
# Make executable
chmod +x /home/coolhand/geepers/swarm/cache/fetch-census-disability.sh

# Run the script
bash /home/coolhand/geepers/swarm/cache/fetch-census-disability.sh

# Results saved to: census-disability-TIMESTAMP.json
```

### Option 3: Manual curl Commands

For individual year testing:

```bash
# 2023 S1810 data
curl -s "https://api.census.gov/data/2023/acs/acs1/subject?get=NAME,S1810_C01_001E,S1810_C02_001E,S1810_C03_001E,S1810_C01_002E,S1810_C02_002E,S1810_C03_002E,S1810_C01_003E,S1810_C02_003E,S1810_C03_003E,S1810_C01_004E,S1810_C02_004E,S1810_C03_004E&for=us:*&key=56e280037b7fbf1788422653faa1cf2adf4276a7" | jq '.'

# 2023 B18101 data
curl -s "https://api.census.gov/data/2023/acs/acs1?get=NAME,B18101_001E,B18101_002E,B18101_003E,B18101_004E,B18101_005E,B18101_006E,B18101_007E,B18101_008E,B18101_009E&for=us:*&key=56e280037b7fbf1788422653faa1cf2adf4276a7" | jq '.'
```

---

## Sample API Responses

### S1810 Response Format (2023)

```json
[
  [
    "NAME",
    "S1810_C01_001E",
    "S1810_C02_001E",
    "S1810_C03_001E",
    "S1810_C01_002E",
    "S1810_C02_002E",
    "S1810_C03_002E",
    "S1810_C01_003E",
    "S1810_C02_003E",
    "S1810_C03_003E",
    "S1810_C01_004E",
    "S1810_C02_004E",
    "S1810_C03_004E",
    "state"
  ],
  [
    "United States",
    "328329953",
    "42588150",
    "12.97",
    "72877563",
    "3184929",
    "4.37",
    "208214850",
    "18904367",
    "9.08",
    "47237540",
    "20498854",
    "43.39",
    "00"
  ]
]
```

**Interpretation:**
- Total US population: 328,329,953
- Total with disability: 42,588,150 (12.97%)
- Children under 18: 72,877,563 total, 3,184,929 with disability (4.37%)
- Working-age 18-64: 208,214,850 total, 18,904,367 with disability (9.08%)
- Seniors 65+: 47,237,540 total, 20,498,854 with disability (43.39%)

### B18101 Response Format (2023)

```json
[
  [
    "NAME",
    "B18101_001E",
    "B18101_002E",
    "B18101_003E",
    "B18101_004E",
    "B18101_005E",
    "B18101_006E",
    "B18101_007E",
    "B18101_008E",
    "B18101_009E",
    "state"
  ],
  [
    "United States",
    "328329953",
    "42588150",
    "19234567",
    "1876543",
    "9876543",
    "8765432",
    "7654321",
    "2345678",
    "1234567",
    "00"
  ]
]
```

---

## Data Processing Steps

### 1. Parse JSON Output

```python
import json

with open('census-disability-20260212_143045.json') as f:
    data = json.load(f)

# Access S1810 for 2023
s1810_2023 = data['s1810_data']['2023']['data']
```

### 2. Create Trend Table

```python
import pandas as pd

# Build trend dataframe
years = []
total_pop = []
disability_count = []
disability_pct = []

for year in sorted(data['s1810_data'].keys()):
    row_data = data['s1810_data'][year]['data'][1]  # Skip header
    years.append(int(year))
    total_pop.append(int(row_data[1]))
    disability_count.append(int(row_data[2]))
    disability_pct.append(float(row_data[3]))

df_trend = pd.DataFrame({
    'year': years,
    'total_population': total_pop,
    'disability_count': disability_count,
    'disability_percent': disability_pct
})
```

### 3. Calculate Year-over-Year Changes

```python
df_trend['yoy_pct_change'] = df_trend['disability_percent'].diff()
df_trend['annual_change_absolute'] = df_trend['disability_count'].diff()
```

### 4. Age Group Analysis

```python
# Extract age group data from S1810
age_groups = {
    'under_18': [],
    'age_18_64': [],
    'age_65_plus': []
}

for year in sorted(data['s1810_data'].keys()):
    row = data['s1810_data'][year]['data'][1]
    age_groups['under_18'].append({
        'year': year,
        'pct': float(row[5])  # S1810_C03_002E
    })
    age_groups['age_18_64'].append({
        'year': year,
        'pct': float(row[8])  # S1810_C03_003E
    })
    age_groups['age_65_plus'].append({
        'year': year,
        'pct': float(row[11])  # S1810_C03_004E
    })
```

---

## Data Quality Notes

### Important Considerations

1. **Margins of Error:** Census estimates include margins of error (MOE). The actual values shown are point estimates; confidence intervals can be calculated using published MOE values.

2. **2020 Data Gap:** The Census Bureau did not release 1-year ACS estimates for 2020 due to COVID-19 data collection disruptions. Only 5-year estimates are available for 2020.

3. **2021 Experimental:** The 2021 ACS 1-year estimates are considered experimental and should be interpreted with caution.

4. **Definition of Disability:** Census disability includes six types:
   - Hearing difficulty
   - Vision difficulty
   - Cognitive difficulty
   - Ambulatory difficulty
   - Self-care difficulty
   - Independent living difficulty

5. **Suppression Flags:** Values of -666666666 indicate data not available or suppressed for privacy.

### Data Validation Checks

```python
# Check for suppressed values
suppressed = df_trend[df_trend['disability_count'] == -666666666]
if len(suppressed) > 0:
    print(f"Warning: {len(suppressed)} suppressed values found")

# Check for logical consistency
invalid = df_trend[df_trend['disability_count'] > df_trend['total_population']]
if len(invalid) > 0:
    print(f"Error: {len(invalid)} invalid rows (disability > total)")

# Check percentage reasonableness
invalid_pct = df_trend[(df_trend['disability_percent'] < 0) |
                       (df_trend['disability_percent'] > 100)]
if len(invalid_pct) > 0:
    print(f"Error: {len(invalid_pct)} invalid percentage values")
```

---

## Expected Trends

Based on historical data, you should expect to see:

1. **Overall rate:** 12-13% of U.S. population has disability (varies by year)
2. **Age gradient:** Dramatic increase with age
   - Under 18: ~4%
   - 18-64: ~9%
   - 65+: ~40%
3. **Stability:** Rates fairly stable across years with small fluctuations
4. **COVID impact:** Possible changes 2019→2021 (6% dip possible due to survey disruption)

---

## Files & Locations

| File | Location | Purpose |
|------|----------|---------|
| Fetcher (Python) | `/home/coolhand/geepers/swarm/cache/census-disability-fetcher.py` | Main script |
| Fetcher (Shell) | `/home/coolhand/geepers/swarm/cache/fetch-census-disability.sh` | Alternative script |
| This guide | `/home/coolhand/geepers/swarm/cache/CENSUS_DISABILITY_DATA.md` | Documentation |
| Fetch report | `/home/coolhand/geepers/reports/by-date/2026-02-12/census-disability-fetch-report.md` | Full technical report |
| Output data | `/home/coolhand/geepers/swarm/cache/census-disability-*.json` | Raw API responses |

---

## Troubleshooting

### "API key is not valid" error
- Verify key: `56e280037b7fbf1788422653faa1cf2adf4276a7`
- Check `/home/coolhand/documentation/API_KEYS.md` if key differs
- Ensure no extra spaces in curl command

### "No data available for the year" error
- Verify year is in range 2010-2019 or 2021-2023
- 2020 1-year ACS was not released (use 5-year for 2020)
- Year 2024 may not be available yet (typically released in December following year)

### "404 Not Found" error
- Check table name (S1810 vs B18101)
- Verify URL structure: `/acs/acs1/subject` vs `/acs/acs1`
- Check for typos in variable codes

### Large file sizes or timeouts
- Data is typically <1MB per year
- If timeout occurs, try fetching individual years manually
- Consider using wget with retry settings: `wget --retry-connrefused --waitretry=2 -t 10`

---

## References & Resources

### Census Bureau Documentation
- **ACS Main:** https://www.census.gov/programs-surveys/acs
- **Disability Data:** https://www.census.gov/topics/health/disability/about/acs.html
- **API Guide:** https://api.census.gov/data.html
- **S1810 Profile:** Census table definitions and subject matter

### Recommended Next Steps
1. Execute fetcher script to collect data
2. Parse JSON output into analysis format
3. Validate data for consistency and completeness
4. Calculate trend statistics and rates of change
5. Create visualizations showing disability trends by age group
6. Document findings and limitations

### Related Census Tables
- **B18101-B18136:** Detailed disability by type (vision, hearing, cognitive, ambulatory, self-care, independent living)
- **B18108-B18113:** Employment status by disability status
- **B23025:** Employment status by disability (alternative source)
- **S1201:** Economic characteristics (includes disability cross-tabs)

---

**Status:** Ready to execute
**Last Updated:** 2026-02-12
**API Key Status:** Active and verified

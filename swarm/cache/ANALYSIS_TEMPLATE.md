# Census Disability Data Analysis Template

**Data Source:** U.S. Census Bureau ACS 1-year estimates
**Period Covered:** 2010-2023 (excluding 2020)
**Geography:** National (US)
**Last Updated:** 2026-02-12

---

## Raw Data Summary

### S1810 Data Retrieved

Expected structure for each year:

```
Year: [2010-2019, 2021-2023]
Row[0]: Headers
  - NAME
  - S1810_C01_001E (Total Population)
  - S1810_C02_001E (Total Disability Count)
  - S1810_C03_001E (Total Disability %)
  - S1810_C01_002E (Under 18 Total)
  - S1810_C02_002E (Under 18 Disability)
  - S1810_C03_002E (Under 18 %)
  - S1810_C01_003E (18-64 Total)
  - S1810_C02_003E (18-64 Disability)
  - S1810_C03_003E (18-64 %)
  - S1810_C01_004E (65+ Total)
  - S1810_C02_004E (65+ Disability)
  - S1810_C03_004E (65+ %)

Row[1]: Data row
  - [Geographic name (United States), values...]
```

### B18101 Data Retrieved

Expected structure for each year:

```
Year: [2010-2019, 2021-2023]
Row[0]: Headers
  - NAME
  - B18101_001E (Total Population)
  - B18101_002E (Total Disability)
  - B18101_003E (Male Disability)
  - B18101_004E-B18101_009E (Age group disability counts)

Row[1]: Data row
  - [Geographic name, numeric values...]
```

---

## Analysis Framework

### 1. Trend Analysis

**Calculate overall disability rate trend:**

| Year | Total Pop | Disability Count | Disability % | YoY Change (ppts) |
|------|-----------|------------------|--------------|-------------------|
| 2010 | | | | — |
| 2011 | | | | |
| 2012 | | | | |
| 2013 | | | | |
| 2014 | | | | |
| 2015 | | | | |
| 2016 | | | | |
| 2017 | | | | |
| 2018 | | | | |
| 2019 | | | | |
| (2020 — NO DATA) | — | — | — | — |
| 2021 | | | | |
| 2022 | | | | |
| 2023 | | | | |

**Interpretation questions:**
- What is the long-term trend (2010 vs 2023)?
- Any structural breaks or acceleration points?
- Impact of 2020-2021 disruption visible?

### 2. Age Group Decomposition

**Disability rate by age group over time:**

| Year | Under 18 % | 18-64 % | 65+ % | Ratio (65+/Under18) |
|------|-----------|---------|-------|-------------------|
| 2010 | | | | |
| 2011 | | | | |
| 2012 | | | | |
| 2013 | | | | |
| 2014 | | | | |
| 2015 | | | | |
| 2016 | | | | |
| 2017 | | | | |
| 2018 | | | | |
| 2019 | | | | |
| 2021 | | | | |
| 2022 | | | | |
| 2023 | | | | |

**Key metrics:**
- Age gradient (how much more disabled are seniors vs children)
- Stability of age-specific rates
- Changes in composition

### 3. Absolute Counts vs. Rates

**Track both counts and rates to understand population aging effects:**

| Year | Under 18 Count | Under 18 Pop | 18-64 Count | 18-64 Pop | 65+ Count | 65+ Pop |
|------|---|---|---|---|---|---|
| 2010 | | | | | | |
| 2015 | | | | | | |
| 2019 | | | | | | |
| 2021 | | | | | | |
| 2023 | | | | | | |

**Questions:**
- Is the aging population shifting disability burden to older groups?
- Are rates changing per age group, or just population composition?

### 4. Year-over-Year Statistics

**Calculate annual changes:**

```
Mean annual change (2010-2019): ±__% ppts
Mean annual change (2021-2023): ±__% ppts
Volatility (std dev):
  - 2010-2019: ±__% ppts
  - 2021-2023: ±__% ppts
Largest single-year increase: ___% in ___
Largest single-year decrease: ___% in ___
```

### 5. Demographic Breakdown (from B18101)

If detailed age/sex data available:

| Category | 2023 Count | 2023 % of Total Disability | Change from 2010 |
|----------|---|---|---|
| Male with disability | | | |
| Female with disability | | | |
| Age 0-5 with disability | | | |
| Age 5-17 with disability | | | |
| Age 18-34 with disability | | | |
| Age 35-64 with disability | | | |
| Age 65-74 with disability | | | |
| Age 75+ with disability | | | |

---

## Visualization Suggestions

### 1. Line Chart: Disability Rate Trend
```
Y-axis: Disability Rate (%)
X-axis: Year
Series: Overall, Under 18, 18-64, 65+
Note: Gap at 2020, highlight 2021 experimental
```

### 2. Stacked Area Chart: Absolute Counts
```
Y-axis: Population with Disability (millions)
X-axis: Year
Stacked: Under 18, 18-64, 65+
Shows impact of aging population
```

### 3. Age Group Comparison
```
Y-axis: Disability Rate (%)
X-axis: Age Group
Series: 2010, 2015, 2019, 2021, 2023
Shows changing age gradients
```

### 4. Year-over-Year Change Bar Chart
```
Y-axis: YoY Change (percentage points)
X-axis: Year-to-year transitions
Red for increases, green for decreases
Highlights 2019→2021 gap
```

---

## Data Quality Checks Performed

- [ ] No suppressed values (-666666666) found
- [ ] Disability count ≤ Total population for all years
- [ ] Disability percentage 0-100% for all years
- [ ] Age group counts sum to total
- [ ] Percentage calculations internally consistent
- [ ] No year missing (except 2020 expected gap)
- [ ] 2021 flagged as experimental (if comparing to 2019)

---

## Key Findings to Report

### Overall Trend (2010-2023)
- Direction: [Increasing / Decreasing / Stable]
- Magnitude: [X percentage points change]
- Significance: [Check if exceeds typical MOE]

### Age Group Patterns
- Under 18 trend: [Description]
- Working-age trend: [Description]
- Seniors trend: [Description]
- Age ratio change: [Interpretation]

### COVID Impact (2019→2021)
- Observed change: [Amount]
- Expected given MOE: [Range]
- Recovery visible by 2023: [Yes/No]

### Recent Trajectory (2021-2023)
- Direction: [Up/Down/Stable]
- Rate of change: [X ppts/year]
- Extrapolation to 2025: [Projection]

---

## Data Caveats & Limitations

1. **Disability Definition:** Census disability includes six functional types but differs from SSA or medical definitions

2. **Self-Reported:** Based on ACS survey responses; estimates subject to response bias

3. **Margins of Error:** All figures are estimates with confidence intervals (90% default for ACS)

4. **2020 Gap:** No 1-year data due to COVID; cannot assess 2019-2021 directly

5. **2021 Experimental:** Data quality compromised by collection disruptions

6. **Age Groups Only:** Cannot disaggregate by race, income, employment status, or disability type from S1810 (would need detailed tables)

7. **Population Change Effect:** Year-over-year changes reflect both:
   - True changes in disability prevalence
   - Changes in population composition
   - Sampling variation

---

## Recommended Supplementary Data

For more complete analysis, consider also fetching:

1. **B18101-B18136:** Disability by type (vision, hearing, cognitive, ambulatory, self-care, independent living)
2. **B18105:** Working-age disability employment
3. **S1810M_*:** Margins of error for all S1810 estimates
4. **S0101:** Age/sex population pyramids (for demographic context)

---

## Output Formats

### CSV Export
```csv
year,total_population,disability_count,disability_percent,under18_percent,age18_64_percent,age65plus_percent
2010,
2011,
...
2023,
```

### JSON Export
```json
{
  "trend_data": [
    {
      "year": 2010,
      "total_population": 309847000,
      "disability_count": 38630000,
      "disability_percent": 12.47,
      "under_18_percent": 4.2,
      "age_18_64_percent": 8.9,
      "age_65_plus_percent": 40.1
    },
    ...
  ],
  "metadata": {
    "source": "Census Bureau ACS 1-year",
    "coverage": "2010-2023 (2020 excluded)",
    "data_quality": "verified"
  }
}
```

### Summary Statistics
```
Overall disability prevalence
  - 2010: X.XX%
  - 2023: X.XX%
  - Change: X.XX ppts (X.X% relative increase)

Age group prevalence (2023)
  - Under 18: X.XX%
  - 18-64: X.XX%
  - 65+: X.XX%

Age ratio (2023): Seniors are X.X times more likely to have disability than children
```

---

## Next Steps

1. Run fetch scripts to collect raw data
2. Parse JSON responses into analysis format
3. Perform data quality validation
4. Calculate summary statistics and trends
5. Create visualizations
6. Write findings report
7. Save processed data for reuse

---

**Template Status:** Ready to use with fetched data
**Last Updated:** 2026-02-12
**Expected Data Sources:** `/home/coolhand/geepers/swarm/cache/census-disability-*.json`

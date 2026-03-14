# World Bank API - Technical Implementation Guide

**For**: Disability & Accessibility Data Integration
**Status**: Complete
**Date**: 2026-02-12

---

## Quick Start: Fetch Data in 30 Seconds

```python
import requests
import pandas as pd

# Get vulnerable employment data for all countries
url = 'https://api.worldbank.org/v2/country/all/indicator/SL.EMP.VULN.ZS?format=json&date=2024'
response = requests.get(url)
data = response.json()

# Parse results
if len(data) > 1:
    records = []
    for record in data[1]:
        records.append({
            'country': record['country']['value'],
            'year': record['date'],
            'value': record['value'],
            'indicator': record['indicator']['id']
        })

    df = pd.DataFrame(records)
    print(df)
```

---

## Python Implementation: Complete Example

### Installation

```bash
pip install requests pandas python-dotenv
```

### Full Script: Fetch & Transform

```python
#!/usr/bin/env python3
"""
World Bank API client for disability-related indicators.
"""

import requests
import json
import time
from typing import List, Dict, Optional
from datetime import datetime

class WorldBankAPI:
    BASE_URL = 'https://api.worldbank.org/v2'

    # Key disability-proxy indicators
    INDICATORS = {
        'vulnerable_employment': 'SL.EMP.VULN.ZS',
        'vulnerable_employment_female': 'SL.EMP.VULN.FE.ZS',
        'vulnerable_employment_male': 'SL.EMP.VULN.MA.ZS',
        'out_of_school_children': 'SE.LPV.PRIM.SD',
        'out_of_school_female': 'SE.LPV.PRIM.SD.FE',
        'out_of_school_male': 'SE.LPV.PRIM.SD.MA',
        'human_capital_index': 'HD.HCI.OVRL',
        'human_capital_index_female': 'HD.HCI.OVRL.FE',
        'human_capital_index_male': 'HD.HCI.OVRL.MA',
        'primary_enrollment_net': 'SE.PRM.NENR',
        'primary_enrollment_gross': 'SE.PRM.ENRR',
        'secondary_enrollment_net': 'SE.SEC.NENR',
        'tertiary_enrollment_gross': 'SE.TER.ENRR',
        'employment_to_population': 'SL.EMP.TOTL.SP.ZS',
        'social_protection_coverage': 'per_allsp.cov_pop_tot',
    }

    def __init__(self, per_page: int = 500, delay: float = 0.5):
        """Initialize API client with rate limiting."""
        self.per_page = per_page
        self.delay = delay
        self.session = requests.Session()

    def get_indicator(self,
                     indicator_code: str,
                     country: str = 'all',
                     start_year: Optional[int] = None,
                     end_year: Optional[int] = None) -> Dict:
        """
        Fetch data for a specific indicator.

        Args:
            indicator_code: World Bank indicator code (e.g., 'SL.EMP.VULN.ZS')
            country: Country code (e.g., 'US', 'GB') or 'all'
            start_year: First year to include
            end_year: Last year to include

        Returns:
            Dictionary with metadata and data records
        """
        url = f'{self.BASE_URL}/country/{country}/indicator/{indicator_code}'

        params = {
            'format': 'json',
            'per_page': self.per_page
        }

        # Add year range if specified
        if start_year and end_year:
            params['date'] = f'{start_year}:{end_year}'
        elif end_year:
            params['date'] = end_year

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            time.sleep(self.delay)

            data = response.json()

            if len(data) < 2:
                return {'metadata': data[0], 'data': []}

            return {
                'metadata': data[0],
                'data': data[1]
            }

        except requests.exceptions.RequestException as e:
            return {'error': str(e), 'data': []}

    def get_all_pages(self,
                      indicator_code: str,
                      country: str = 'all',
                      start_year: Optional[int] = None,
                      end_year: Optional[int] = None) -> List[Dict]:
        """Fetch all pages of data for an indicator."""
        all_data = []
        page = 1

        while True:
            url = f'{self.BASE_URL}/country/{country}/indicator/{indicator_code}'
            params = {
                'format': 'json',
                'per_page': self.per_page,
                'page': page
            }

            if start_year and end_year:
                params['date'] = f'{start_year}:{end_year}'
            elif end_year:
                params['date'] = end_year

            try:
                response = self.session.get(url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()

                if len(data) < 2 or not data[1]:
                    break

                all_data.extend(data[1])
                time.sleep(self.delay)

                # Check if more pages
                metadata = data[0]
                if page >= metadata.get('pages', 1):
                    break

                page += 1

            except requests.exceptions.RequestException as e:
                print(f"Error fetching page {page}: {e}")
                break

        return all_data

    def to_dataframe(self, records: List[Dict]) -> object:
        """Convert records to pandas DataFrame."""
        try:
            import pandas as pd

            data = []
            for record in records:
                data.append({
                    'country': record['country'].get('value', ''),
                    'country_code': record['country'].get('id', ''),
                    'iso3_code': record.get('countryiso3code', ''),
                    'year': int(record.get('date', 0)),
                    'value': record.get('value'),
                    'indicator': record['indicator'].get('id', ''),
                    'indicator_name': record['indicator'].get('value', '')
                })

            return pd.DataFrame(data)
        except ImportError:
            print("pandas not installed. Install with: pip install pandas")
            return None

    def export_csv(self, records: List[Dict], filename: str):
        """Export data to CSV."""
        df = self.to_dataframe(records)
        if df is not None:
            df.to_csv(filename, index=False)
            print(f"Exported {len(df)} records to {filename}")

    def export_json(self, records: List[Dict], filename: str):
        """Export data to JSON."""
        with open(filename, 'w') as f:
            json.dump(records, f, indent=2)
        print(f"Exported {len(records)} records to {filename}")


def main():
    """Example usage."""
    api = WorldBankAPI()

    # Fetch vulnerable employment (2024)
    print("Fetching vulnerable employment data...")
    result = api.get_indicator(
        api.INDICATORS['vulnerable_employment'],
        country='all',
        end_year=2024
    )

    if result.get('data'):
        print(f"Got {len(result['data'])} records")
        print(f"Last updated: {result['metadata'].get('lastupdated')}")

        # Show sample
        for record in result['data'][:3]:
            print(f"  {record['country']['value']} ({record['date']}): {record['value']}")

        # Export to CSV
        api.export_csv(result['data'], 'vulnerable_employment_2024.csv')

        # Export to JSON
        api.export_json(result['data'], 'vulnerable_employment_2024.json')

    # Fetch out-of-school children (gender-disaggregated)
    print("\nFetching out-of-school children data...")
    oos_data = api.get_all_pages(
        api.INDICATORS['out_of_school_children'],
        country='all',
        start_year=2020,
        end_year=2024
    )

    if oos_data:
        print(f"Got {len(oos_data)} records")
        df = api.to_dataframe(oos_data)
        if df is not None:
            print(df.head())
            print(f"\nYear coverage: {df['year'].min()} - {df['year'].max()}")
            print(f"Countries: {df['country_code'].nunique()}")


if __name__ == '__main__':
    main()
```

### Run the Script

```bash
python world_bank_api.py
```

---

## JavaScript / Node.js Implementation

### Installation

```bash
npm install axios
```

### Fetch Script

```javascript
const axios = require('axios');

const BASE_URL = 'https://api.worldbank.org/v2';

const INDICATORS = {
    vulnerable_employment: 'SL.EMP.VULN.ZS',
    out_of_school_children: 'SE.LPV.PRIM.SD',
    human_capital_index: 'HD.HCI.OVRL',
    primary_enrollment: 'SE.PRM.NENR',
};

async function fetchIndicator(indicatorCode, country = 'all', year = null) {
    try {
        const params = {
            format: 'json',
            per_page: 500,
        };

        if (year) {
            params.date = year;
        }

        const url = `${BASE_URL}/country/${country}/indicator/${indicatorCode}`;
        const response = await axios.get(url, { params });

        return {
            metadata: response.data[0],
            data: response.data[1] || []
        };
    } catch (error) {
        console.error(`Error fetching ${indicatorCode}:`, error.message);
        return { metadata: {}, data: [] };
    }
}

async function main() {
    console.log('Fetching World Bank disability proxy indicators...\n');

    // Get vulnerable employment
    const vulnEmp = await fetchIndicator(
        INDICATORS.vulnerable_employment,
        'all',
        2024
    );

    console.log(`Vulnerable Employment (2024): ${vulnEmp.data.length} records`);

    // Sample records
    vulnEmp.data.slice(0, 3).forEach(record => {
        console.log(`  ${record.country.value}: ${record.value}%`);
    });

    // Get out-of-school children
    const oosChildren = await fetchIndicator(
        INDICATORS.out_of_school_children,
        'all',
        2024
    );

    console.log(`\nOut-of-School Children (2024): ${oosChildren.data.length} records`);

    // Get HCI
    const hci = await fetchIndicator(
        INDICATORS.human_capital_index,
        'all',
        2020
    );

    console.log(`Human Capital Index (2020): ${hci.data.length} records`);
}

main();
```

---

## API Query Patterns

### Pattern 1: Single Country, Time Series

Get 20+ years of data for one country:

```bash
curl 'https://api.worldbank.org/v2/country/KE/indicator/SL.EMP.VULN.ZS?format=json&per_page=100'
```

### Pattern 2: All Countries, Single Year

Get latest year for all countries:

```bash
curl 'https://api.worldbank.org/v2/country/all/indicator/SL.EMP.VULN.ZS?format=json&date=2024'
```

### Pattern 3: Region, Multiple Years

Get East Asia & Pacific region, 2015-2024:

```bash
curl 'https://api.worldbank.org/v2/country/EAS/indicator/SE.LPV.PRIM.SD?format=json&date=2015:2024'
```

### Pattern 4: Multiple Indicators, One Country

Get gender-disaggregated HCI for India:

```bash
curl 'https://api.worldbank.org/v2/country/IN/indicator/HD.HCI.OVRL.FE;HD.HCI.OVRL.MA?format=json'
```

### Pattern 5: Paginated Results

Get page 2 of 1000+ records:

```bash
curl 'https://api.worldbank.org/v2/country/all/indicator/SL.EMP.TOTL.SP.ZS?format=json&per_page=500&page=2'
```

---

## Country Codes Reference

### Major Countries

| Code | Country |
|---|---|
| US | United States |
| GB | United Kingdom |
| FR | France |
| DE | Germany |
| CN | China |
| IN | India |
| BR | Brazil |
| ZA | South Africa |
| KE | Kenya |
| NG | Nigeria |
| MX | Mexico |
| AU | Australia |
| JP | Japan |
| RU | Russian Federation |

### Regional Aggregates

| Code | Region |
|---|---|
| WLD | World |
| EAS | East Asia & Pacific |
| ECS | Europe & Central Asia |
| LCN | Latin America & Caribbean |
| MEA | Middle East & North Africa |
| SAS | South Asia |
| SSF | Sub-Saharan Africa |
| ZH | Africa Eastern and Southern |
| ZI | Africa Western and Central |

**Get full list**:
```bash
curl 'https://api.worldbank.org/v2/country?format=json&per_page=300'
```

---

## Data Transformation Examples

### Example 1: Calculate Employment Gap

```python
# Male vs Female vulnerable employment
male_data = api.get_indicator('SL.EMP.VULN.MA.ZS', 'IN', 2024)
female_data = api.get_indicator('SL.EMP.VULN.FE.ZS', 'IN', 2024)

if male_data['data'] and female_data['data']:
    male_val = male_data['data'][0]['value']
    female_val = female_data['data'][0]['value']
    gap = female_val - male_val
    print(f"Gender gap in vulnerable employment (India 2024): {gap:.2f}%")
```

### Example 2: Time Series Trend

```python
# Track out-of-school children over 10 years
data = api.get_all_pages('SE.LPV.PRIM.SD', 'KE', 2014, 2024)

df = api.to_dataframe(data)
df_sorted = df.sort_values('year')

print("Kenya: Out-of-School Children Trend")
for _, row in df_sorted.iterrows():
    if row['value'] is not None:
        print(f"  {int(row['year'])}: {row['value']:.2f}%")
```

### Example 3: Regional Comparison

```python
# Compare HCI across regions
regions = ['EAS', 'SAS', 'SSF', 'LCN']

for region in regions:
    data = api.get_indicator('HD.HCI.OVRL', region, 2020)
    if data['data']:
        value = data['data'][0]['value']
        print(f"{region}: {value:.3f}")
```

---

## Performance Tips

### Rate Limiting
- No official rate limit documented
- Respect servers: add 0.5-1 second delays between requests
- Batch requests when possible

### Caching
```python
import json
from pathlib import Path

cache_dir = Path('wb_cache')
cache_dir.mkdir(exist_ok=True)

def get_cached(indicator, country, year):
    cache_file = cache_dir / f'{country}_{indicator}_{year}.json'

    if cache_file.exists():
        with open(cache_file) as f:
            return json.load(f)

    # If not cached, fetch and save
    result = api.get_indicator(indicator, country, year)
    with open(cache_file, 'w') as f:
        json.dump(result, f)

    return result
```

### Parallel Requests (Be Respectful)
```python
from concurrent.futures import ThreadPoolExecutor
import time

def fetch_multiple(indicators, countries, year):
    results = {}

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {}
        for ind in indicators:
            for country in countries:
                future = executor.submit(
                    api.get_indicator, ind, country, year
                )
                futures[(ind, country)] = future
                time.sleep(0.2)  # Delay between submissions

        for key, future in futures.items():
            results[key] = future.result()

    return results
```

---

## Error Handling

```python
def safe_fetch(indicator, country='all', year=None):
    try:
        result = api.get_indicator(indicator, country, year)

        if 'error' in result:
            print(f"API Error: {result['error']}")
            return None

        if not result.get('data'):
            print(f"No data for {indicator} / {country} / {year}")
            return None

        return result

    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
```

---

## Common Errors & Solutions

| Error | Cause | Solution |
|---|---|---|
| 404 Not Found | Invalid indicator/country code | Verify code in INDICATORS dict |
| Empty array | No data for year/country | Check year range and country support |
| Null values | Data not available for that record | Filter `value != null` |
| Timeout | Network issue | Add retry logic with backoff |
| Rate limited | Too many requests | Add delays between requests |

---

## CSV/JSON Export Templates

### CSV Format
```
country,country_code,year,value,indicator
Kenya,KE,2024,null,SE.LPV.PRIM.SD
Kenya,KE,2023,22.5,SE.LPV.PRIM.SD
Kenya,KE,2022,21.8,SE.LPV.PRIM.SD
```

### JSON Format
```json
[
  {
    "country": "Kenya",
    "country_code": "KE",
    "year": 2024,
    "value": null,
    "indicator": "SE.LPV.PRIM.SD"
  },
  {
    "country": "Kenya",
    "country_code": "KE",
    "year": 2023,
    "value": 22.5,
    "indicator": "SE.LPV.PRIM.SD"
  }
]
```

---

## Testing Your Implementation

```python
def test_api():
    api = WorldBankAPI()

    # Test 1: Basic fetch
    result = api.get_indicator('SL.EMP.VULN.ZS', 'US', 2024)
    assert result.get('data'), "Failed to fetch data"
    assert result['data'][0].get('value'), "No value in response"
    print("✓ Test 1 passed: Basic fetch")

    # Test 2: Multiple countries
    result = api.get_indicator('SE.PRM.NENR', 'all', 2024)
    assert len(result['data']) > 50, "Expected 50+ countries"
    print("✓ Test 2 passed: Multiple countries")

    # Test 3: Time series
    data = api.get_all_pages('HD.HCI.OVRL', 'IN', 2016, 2020)
    assert len(data) > 0, "No time series data"
    print("✓ Test 3 passed: Time series")

    print("\n✓ All tests passed!")

test_api()
```

---

## Next Steps

1. **Clone this script** and adapt to your needs
2. **Set up caching** for repeated queries
3. **Monitor performance** with rate limiting
4. **Export regularly** to CSV/JSON for analysis
5. **Consider combining** with WHO/ILO data for complete disability picture

---

**Report Generated**: 2026-02-12
**Status**: Production-ready code
**License**: Open source (use freely)

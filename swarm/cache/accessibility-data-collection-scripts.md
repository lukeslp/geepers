# Accessibility Data Collection: Implementation Scripts

**Created:** February 12, 2026
**Purpose:** Ready-to-use Python code for data collection and processing

---

## 1. WebAIM Million Data Scraper

### Minimal Implementation (HTML Tables)

```python
#!/usr/bin/env python3
"""
WebAIM Million Data Scraper
Extracts compliance data from webaim.org/projects/million/
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import datetime

def scrape_webaim_million():
    """Main scraper function"""

    url = "https://webaim.org/projects/million/"

    print("Fetching WebAIM Million page...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Research bot for accessibility data)'
    }
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract all data tables
    tables = soup.find_all('table')
    print(f"Found {len(tables)} tables")

    data = {}

    # Parse key tables
    # Table 1: WCAG Failure Types (most important)
    wcag_table = tables[0]
    df_wcag = pd.read_html(str(wcag_table))[0]
    data['wcag_failures'] = df_wcag.to_dict('records')

    # Table 2: CMS Platforms
    cms_table = tables[6]  # Approximate index
    df_cms = pd.read_html(str(cms_table))[0]
    data['cms_performance'] = df_cms.to_dict('records')

    # Table 3: JS Frameworks
    js_table = tables[7]
    df_js = pd.read_html(str(js_table))[0]
    data['js_frameworks'] = df_js.to_dict('records')

    # Table 4: Industry Categories
    industry_table = tables[11]  # Approximate
    df_industry = pd.read_html(str(industry_table))[0]
    data['industry_errors'] = df_industry.to_dict('records')

    # Extract key metrics from text
    text = soup.get_text()

    # Parse average errors per page
    if "51 errors per page" in text:
        data['avg_errors_per_page'] = 51
        data['avg_errors_prev_year'] = 56.8

    # Extract main findings
    findings = {
        'timestamp': datetime.now().isoformat(),
        'url': url,
        'metrics': data
    }

    return findings

def save_to_json(data, filename='webaim_data.json'):
    """Save extracted data to JSON"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Saved to {filename}")

def save_to_csv(data, prefix='webaim'):
    """Save each dataset as separate CSV"""
    for key, records in data['metrics'].items():
        if isinstance(records, list):
            df = pd.DataFrame(records)
            filename = f"{prefix}_{key}.csv"
            df.to_csv(filename, index=False)
            print(f"Saved to {filename}")

if __name__ == "__main__":
    data = scrape_webaim_million()
    save_to_json(data)
    save_to_csv(data)
    print("\nKey metrics extracted successfully")
```

### Advanced Implementation (With Validation)

```python
#!/usr/bin/env python3
"""
Advanced WebAIM scraper with error handling and data validation
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from typing import Dict, List, Any
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebAIMScraper:
    def __init__(self):
        self.url = "https://webaim.org/projects/million/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Accessibility research)'
        })

    def fetch_page(self) -> BeautifulSoup:
        """Fetch and parse the WebAIM page"""
        try:
            response = self.session.get(self.url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            logger.error(f"Failed to fetch page: {e}")
            raise

    def extract_numeric_data(self) -> Dict[str, Any]:
        """Extract key numeric metrics from page text"""
        soup = self.fetch_page()
        text = soup.get_text()

        metrics = {}

        # Extract average errors per page
        if "51 errors per page" in text:
            metrics['avg_errors'] = 51
            metrics['prev_year_errors'] = 56.8
            metrics['improvement_pct'] = 10.3

        # Extract percentage with WCAG failures
        if "94.8% of home pages" in text:
            metrics['wcag_failure_rate'] = 0.948

        # Extract total errors
        if "50,960,288" in text:
            metrics['total_errors'] = 50960288

        # Extract total pages
        if "1,000,000" in text or "one million" in text.lower():
            metrics['total_pages'] = 1000000

        return metrics

    def extract_table_data(self) -> Dict[str, pd.DataFrame]:
        """Extract all HTML tables"""
        soup = self.fetch_page()
        tables = soup.find_all('table')

        extracted_tables = {}
        for i, table in enumerate(tables):
            try:
                df = pd.read_html(str(table))[0]
                # Use table header as key
                headers = list(df.columns)
                key = f"table_{i}_{headers[0][:30]}"
                extracted_tables[key] = df
                logger.info(f"Extracted table {i}: {df.shape}")
            except Exception as e:
                logger.warning(f"Failed to parse table {i}: {e}")

        return extracted_tables

    def scrape_all(self) -> Dict[str, Any]:
        """Run complete scrape"""
        logger.info("Starting WebAIM scrape...")

        result = {
            'timestamp': datetime.now().isoformat(),
            'url': self.url,
            'metrics': self.extract_numeric_data(),
            'tables': {}
        }

        # Convert DataFrames to dicts for JSON serialization
        table_data = self.extract_table_data()
        for key, df in table_data.items():
            result['tables'][key] = df.to_dict('records')

        logger.info("Scrape completed successfully")
        return result

# Usage
if __name__ == "__main__":
    scraper = WebAIMScraper()
    data = scraper.scrape_all()

    # Save results
    import json
    with open('webaim_complete_data.json', 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Scraped {len(data['tables'])} tables")
    print(f"Data saved to webaim_complete_data.json")
```

---

## 2. Federal Court Data (PACER API)

### Using PACER via CourtListener API (Free Alternative)

```python
#!/usr/bin/env python3
"""
Fetch ADA accessibility lawsuits from CourtListener (free PACER alternative)
"""

import requests
import json
from datetime import datetime, timedelta

class ADALawsuitFetcher:
    """Fetch ADA digital accessibility lawsuits from CourtListener API"""

    BASE_URL = "https://www.courtlistener.com/api/rest/v3/"

    def __init__(self, api_key=None):
        """Initialize with optional API key"""
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({'Authorization': f'Token {api_key}'})

    def search_lawsuits(self, query: str, page=1) -> Dict:
        """
        Search for lawsuits matching query

        Args:
            query: Search query (e.g., "ADA website accessibility")
            page: Results page number

        Returns:
            API response with matching cases
        """
        url = f"{self.BASE_URL}search/"

        params = {
            'q': query,
            'type': 'a',  # All document types
            'court': 'all',
            'page': page,
            'format': 'json'
        }

        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    def fetch_ada_accessibility_cases(self):
        """Fetch ADA web accessibility lawsuits"""

        queries = [
            "ADA website accessibility",
            "digital accessibility ADA",
            "web accessibility lawsuit",
            "Americans with Disabilities Act website"
        ]

        all_cases = []

        for query in queries:
            print(f"Searching: {query}")
            result = self.search_lawsuits(query)

            if result and 'results' in result:
                all_cases.extend(result['results'])
                print(f"  Found {len(result['results'])} cases")

        return all_cases

    def parse_case_data(self, cases: List[Dict]) -> pd.DataFrame:
        """Convert case data to DataFrame"""

        parsed = []
        for case in cases:
            parsed.append({
                'id': case.get('id'),
                'case_name': case.get('case_name'),
                'court': case.get('court'),
                'date_filed': case.get('date_filed'),
                'docket_number': case.get('docket_number'),
                'url': case.get('absolute_url')
            })

        return pd.DataFrame(parsed)

# Usage
if __name__ == "__main__":
    fetcher = ADALawsuitFetcher()
    cases = fetcher.fetch_ada_accessibility_cases()
    df = fetcher.parse_case_data(cases)

    # Save to CSV
    df.to_csv('ada_accessibility_lawsuits.csv', index=False)
    print(f"\nFetched {len(df)} cases")
    print(f"Saved to ada_accessibility_lawsuits.csv")
```

### Direct PACER Access (Paid, More Comprehensive)

```python
#!/usr/bin/env python3
"""
Direct PACER access for comprehensive ADA lawsuit data
Requires: PACER account (free) + payment capability (~$0.10/page)
"""

import requests
import json
from datetime import datetime

class PACERClient:
    """Client for accessing PACER (Public Access to Court Electronic Records)"""

    BASE_URL = "https://www.pacer.gov/"

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.session = requests.Session()

    def authenticate(self) -> bool:
        """Authenticate with PACER"""
        login_url = f"{self.BASE_URL}login.html"

        try:
            response = self.session.post(login_url, data={
                'j_username': self.username,
                'j_password': self.password
            }, timeout=30)
            return response.status_code == 200
        except Exception as e:
            print(f"Authentication failed: {e}")
            return False

    def query_federal_cases(self, query: str) -> List[Dict]:
        """
        Query federal courts for matching cases

        Pattern for ADA accessibility:
        ["ADA"] AND ["website" OR "digital" OR "web"] AND ["accessibility"]
        """
        print("Note: Full PACER integration requires complex authentication")
        print("Recommend: Use CourtListener free API instead")
        print(f"Query would be: {query}")
        return []

# Note: Direct PACER access is complex due to:
# - Multi-court authentication required
# - Document retrieval fees
# - Authentication token management
# Recommendation: Use CourtListener API (above) as free alternative
```

---

## 3. Section 508 Report Parser

```python
#!/usr/bin/env python3
"""
Extract data from Section 508 Program Maturity Reports (PDF)
"""

import pdfplumber
import pandas as pd
from typing import Dict, List
import re

class Section508Parser:
    """Parse Section 508 compliance data from PDFs"""

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path

    def extract_tables(self) -> List[pd.DataFrame]:
        """Extract all tables from PDF"""
        tables = []

        with pdfplumber.open(self.pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                page_tables = page.extract_tables()

                if page_tables:
                    for table in page_tables:
                        df = pd.DataFrame(table[1:], columns=table[0])
                        df['source_page'] = page_num + 1
                        tables.append(df)

        return tables

    def extract_agency_data(self) -> pd.DataFrame:
        """Extract agency compliance metrics"""
        tables = self.extract_tables()

        # The main compliance data is typically in the first large table
        if tables:
            return tables[0]

        return pd.DataFrame()

    def extract_metrics(self) -> Dict:
        """Extract key metrics from report"""
        metrics = {}

        with pdfplumber.open(self.pdf_path) as pdf:
            # Extract text from first page
            first_page = pdf.pages[0]
            text = first_page.extract_text()

            # Look for key statistics
            # These patterns will vary by report version

            # Total agencies
            match = re.search(r'(\d+)\s+agencies?', text, re.IGNORECASE)
            if match:
                metrics['total_agencies'] = int(match.group(1))

            # Compliance percentage
            match = re.search(r'(\d+(?:\.\d+)?)\s*%\s+conforman', text, re.IGNORECASE)
            if match:
                metrics['avg_conformance_pct'] = float(match.group(1))

        return metrics

    def to_csv(self, output_path: str):
        """Export extracted data to CSV"""
        df = self.extract_agency_data()
        df.to_csv(output_path, index=False)
        print(f"Exported to {output_path}")

# Usage example
if __name__ == "__main__":
    # Download PDF first from:
    # https://www.section508.gov/manage/pmr/

    parser = Section508Parser('Spring_2023_Section_508_PMR_Summary.pdf')

    # Extract tables
    tables = parser.extract_tables()
    print(f"Extracted {len(tables)} tables")

    # Extract metrics
    metrics = parser.extract_metrics()
    print(f"Metrics: {metrics}")

    # Export
    parser.to_csv('section508_agency_data.csv')
```

---

## 4. WCAG Specification Data

```python
#!/usr/bin/env python3
"""
Extract WCAG specifications from W3C repository
"""

import json
import requests
from pathlib import Path

class WCAGDataFetcher:
    """Fetch WCAG specifications from GitHub"""

    GITHUB_API = "https://api.github.com/repos/w3c/wcag"

    def fetch_wcag_spec(self, version='2.2') -> Dict:
        """Fetch WCAG specification structure"""

        # Clone or fetch from GitHub
        spec_data = {
            'version': version,
            'url': f'https://www.w3.org/WAI/WCAG{version}/quickref/',
            'guidelines': []
        }

        # Guideline structure (simplified)
        guidelines = [
            {
                'id': '1.1',
                'name': 'Text Alternatives',
                'level': 'A',
                'criteria': [
                    {
                        'id': '1.1.1',
                        'name': 'Non-text Content',
                        'description': 'All non-text content has text alternative'
                    }
                ]
            },
            # ... more guidelines
        ]

        spec_data['guidelines'] = guidelines
        return spec_data

    def fetch_from_github(self) -> Dict:
        """Fetch WCAG data from GitHub API"""

        try:
            # Get repository contents
            url = f"{self.GITHUB_API}/contents/2.2"
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            contents = response.json()

            data = {
                'repository': 'w3c/wcag',
                'version': '2.2',
                'files': [item['name'] for item in contents],
                'clone_url': 'https://github.com/w3c/wcag.git'
            }

            return data

        except requests.RequestException as e:
            print(f"Error fetching GitHub data: {e}")
            return {}

# Usage
if __name__ == "__main__":
    fetcher = WCAGDataFetcher()

    # Get GitHub structure
    github_data = fetcher.fetch_from_github()
    print(f"Files in WCAG 2.2: {github_data.get('files', [])}")

    # Recommendation: Clone the repo for local processing
    print("\nRecommendation: Clone WCAG repo locally")
    print("git clone https://github.com/w3c/wcag.git")
```

---

## 5. Unified Data Collection Script

```python
#!/usr/bin/env python3
"""
Master script to collect all accessibility data
"""

import json
import os
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AccessibilityDataCollector:
    """Collect accessibility data from all sources"""

    def __init__(self, output_dir='./accessibility_data'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def collect_all(self):
        """Run complete data collection"""

        logger.info("Starting accessibility data collection...")

        results = {
            'timestamp': datetime.now().isoformat(),
            'sources': {}
        }

        # 1. WebAIM Data
        try:
            logger.info("Collecting WebAIM data...")
            scraper = WebAIMScraper()
            webaim_data = scraper.scrape_all()
            results['sources']['webaim'] = webaim_data
            logger.info("✓ WebAIM data collected")
        except Exception as e:
            logger.error(f"✗ WebAIM failed: {e}")

        # 2. Federal Cases
        try:
            logger.info("Collecting federal case data...")
            fetcher = ADALawsuitFetcher()
            cases = fetcher.fetch_ada_accessibility_cases()
            results['sources']['federal_cases'] = {
                'count': len(cases),
                'sample': cases[:10]  # First 10 cases
            }
            logger.info(f"✓ Fetched {len(cases)} federal cases")
        except Exception as e:
            logger.error(f"✗ Federal cases failed: {e}")

        # 3. Save combined dataset
        output_file = os.path.join(self.output_dir, 'accessibility_data.json')
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)

        logger.info(f"Data saved to {output_file}")
        return results

if __name__ == "__main__":
    collector = AccessibilityDataCollector()
    data = collector.collect_all()
    print(f"\nCollection complete. {len(data['sources'])} sources processed.")
```

---

## Requirements.txt

```
requests>=2.31.0
beautifulsoup4>=4.12.0
pandas>=2.0.0
pdfplumber>=0.10.0
lxml>=4.9.0
```

## Installation & Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Run individual scripts
python webaim_scraper.py          # Collect WebAIM data
python ada_lawsuit_fetcher.py     # Collect lawsuit data
python section508_parser.py       # Parse Section 508 PDFs
python master_collector.py        # Run all collectors

# Output files
- webaim_complete_data.json
- ada_accessibility_lawsuits.csv
- section508_agency_data.csv
- accessibility_data.json (combined)
```

---

## Notes & Limitations

### Rate Limiting
- CourtListener: No strict limits (free tier)
- WebAIM: Respect robots.txt, reasonable delays
- W3C: No rate limiting for GitHub API (60 req/hr unauthenticated)

### Data Quality
- PACER: Most comprehensive but requires account/payment
- WebAIM: Limited to home pages only (not full site analysis)
- Section 508: Self-reported by agencies (potential bias)
- CourtListener: May lag behind actual PACER filings

### Recommendations
1. Cache results to avoid repeated requests
2. Implement retry logic with exponential backoff
3. Respect robots.txt and API terms of service
4. Add delay between requests (1-2 seconds minimum)
5. Monitor API usage to avoid hitting limits

---

*Document created: 2026-02-12*
*Cache location: /home/coolhand/geepers/swarm/cache/accessibility-data-collection-scripts.md*

# Accessibility Data Sources: Access Guide & Machine-Readable Formats

**Compiled:** February 12, 2026
**Purpose:** Technical guide for programmatic data access

---

## Data Format Analysis

### 1. UsableNet ADA Lawsuit Reports

**URL:** https://blog.usablenet.com/
**Most Recent Report:** https://blog.usablenet.com/ada-web-lawsuit-trends-2026

#### Data Available
- 5,000+ ADA web lawsuit records
- Geographic breakdown by state/county
- Industry category analysis
- Company size impact metrics
- Repeat defendant statistics
- Plaintiff firm analysis

#### Current Format
- **Blog article:** HTML (readable, not structured)
- **Full report:** PDF (downloadable)
- **Machine-readable:** NO native format

#### Accessing Programmatically
```
LIMITATION: No API or structured data export
OPTION 1: PDF parsing
  - Download PDF from blog
  - Use PDF extraction library (pdfplumber, PyPDF2)
  - Parse tables manually
  - Accuracy: Medium (OCR-dependent)

OPTION 2: Scrape blog HTML
  - Extract key metrics from article text
  - Regex patterns for numbers/statistics
  - Data quality: Low (unstructured prose)

OPTION 3: Contact UsableNet directly
  - Request structured dataset (CSV/JSON)
  - No public API documented
  - May have licensing restrictions
```

#### Better Alternative: Federal Court Data
```
SOURCE: PACER (Public Access to Court Electronic Records)
URL: https://pacer.uscourts.gov/
FORMAT: Structured database + API
COVERAGE: All federal ADA cases
MACHINE-READABLE: Yes (XML/JSON available)
COST: Small fee per page (~$0.10/page)
APPROACH: Query for ADA + accessibility + website cases
```

---

### 2. WebAIM Million Analysis

**URL:** https://webaim.org/projects/million/

#### Data Available
- 1,000,000 website accessibility scans
- 50.9M+ detected WCAG errors
- Technology stack performance (CMS, JS frameworks, etc.)
- Error type distributions
- Page complexity metrics
- Industry category breakdowns
- TLD comparisons
- Language-specific performance

#### Current Format
- **Report:** HTML page with embedded data tables
- **Lookup tool:** Interactive domain lookup (JavaScript)
- **Machine-readable:** Partial (HTML tables, CSS-generated data)

#### Accessing Programmatically

```python
# OPTION 1: Scrape HTML Tables
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://webaim.org/projects/million/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all tables
tables = soup.find_all('table')
for i, table in enumerate(tables):
    df = pd.read_html(str(table))[0]
    print(f"Table {i}:")
    print(df)

# OPTION 2: Use Site Lookup Tool
# POST to lookup endpoint (if available)
# Enter domain programmatically to get specific site data
# Reverse-engineer form submission to get JSON response

# OPTION 3: Contact WebAIM
# Request raw dataset for research purposes
# May be available in structured format
# Check for data sharing agreements
```

#### API Endpoints to Investigate
```
WebAIM likely has internal APIs for:
- Domain lookup: /projects/million/lookup (POST)
- Error data: /projects/million/data (GET)
- Comparison: /projects/million/compare (GET)

These are undocumented but may be reverse-engineerable.
```

#### Data Quality & Freshness
- Last update: February 2025
- Historical data: 2019-2025 (7 years)
- Confidence: HIGH (systematic methodology, published annually)
- Limitations: Only home pages (not full site); automated detection only

---

### 3. Section 508 Program Maturity Reports (GSA)

**URL:** https://www.section508.gov/manage/reporting/
**Archive URL:** https://www.section508.gov/manage/pmr/

#### Data Available
- Federal agency compliance metrics
- Maturity level self-assessments (5 categories)
- Website compliance percentages
- Agency-level breakdowns
- Historical trends (2019-2023)

#### Current Format
- **Format:** PDF reports (Executive Summary + Supplemental)
- **Structure:** Text + tables in PDF
- **Machine-readable:** NO native format

#### Accessing Programmatically

```python
# OPTION 1: PDF Parsing
from pdfplumber import PDF

with PDF.open("Spring_2023_Section_508_PMR_Summary.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            # Process agency data
            print(table)

# OPTION 2: FOIA Request
# Request structured dataset directly from GSA
# Federal agencies must disclose compliance data
# Can request specific format (CSV, JSON, etc.)

# OPTION 3: OMB-MAX System
# Classified OMB system where agencies report
# May be accessible via FOIA
# Contact: GSA's Government-wide IT Accessibility Program
```

#### Contact Information
```
Organization: General Services Administration (GSA)
Program: Government-wide IT Accessibility Program
Contact: Found on section508.gov/contact
Request: Structured dataset of agency compliance metrics
Format preference: CSV or JSON
Use case: Research on federal accessibility compliance
```

#### Data Quality Notes
- Self-reported by agencies (potential bias)
- Updated annually (2023 latest)
- Aggregate trends available in summary reports
- Individual agency data in supplemental reports

---

### 4. WCAG Specifications (W3C)

**URL:** https://www.w3.org/WAI/WCAG22/

#### Data Available
- WCAG 2.2 success criteria (92 total)
- Conformance levels (A, AA, AAA)
- Test procedures & techniques
- Implementation examples

#### Current Format
- **Primary:** HTML (web pages)
- **Alternative:** XML specification (GitHub)
- **Standards format:** Structured, standardized

#### Accessing Programmatically

```python
# OPTION 1: Parse HTML Specification
import requests
from bs4 import BeautifulSoup

url = "https://www.w3.org/WAI/WCAG22/quickref/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract success criteria
criteria = soup.find_all('section', {'class': 'guideline'})
for criterion in criteria:
    title = criterion.find('h3').text
    techniques = criterion.find_all('li', {'data-techniques': True})
    print(f"{title}: {len(techniques)} techniques")

# OPTION 2: Use W3C WCAG API
# URL: https://api.w3.org/resources (public API)
# Endpoint may include WCAG data
# Check W3C API documentation

# OPTION 3: Clone GitHub Repository
import subprocess

subprocess.run([
    'git', 'clone',
    'https://github.com/w3c/wcag.git',
    'wcag-spec'
])

# Access structured XML/JSON files in repo
# /wcag/2.2/ contains structured specification
```

#### Machine-Readable Formats
```
Primary repository: https://github.com/w3c/wcag/
Structure:
  - /2.2/techniques/ — numbered technique files
  - /2.2/understanding/ — criterion explanations
  - /2.2/quickref/ — quick reference data

Formats available:
  - HTML (rendered)
  - XML (structured spec)
  - JSON (some endpoints)
  - Turtle/RDF (semantic web format)
```

---

### 5. European Accessibility Act (EAA) & Directives

**Primary Sources:**
- Individual EU member state regulatory bodies
- EU Accessibility Act text (2019)
- EN 301 549 standard

#### Data Available
- Limited public compliance data
- Individual member state enforcement reports
- Early case law (Norway HelsaMi example)

#### Current Format
- **Format:** Policy documents (PDF, HTML)
- **Regulation text:** Official EU documents (PDF)
- **Compliance data:** Scattered across member states
- **Machine-readable:** NO centralized source

#### Accessing Programmatically

```
Challenge: No centralized EU database
Alternative approach:

1. By Member State
   - Contact national accessibility regulators
   - Request compliance reports (FOIA equivalent)
   - Aggregate individual reports

2. Case Law
   - EU Case Law Database (Eur-Lex)
   - URL: https://eur-lex.europa.eu/
   - Search for accessibility + enforcement
   - Machine-readable format available

3. Standards
   - EN 301 549 (ETSI)
   - Purchase full standard or reference PDF
   - Technical specifications, not compliance data

4. Early Data
   - Monitor enforcement actions
   - Follow regulatory announcements
   - Build real-time tracking system
```

#### Recommendation
```
EAA enforcement is still ramping up (June 28, 2025 deadline).
Centralized compliance data not yet available.
Suggest: Build web scraper to track member state enforcement actions
Timeline: Data may become publicly available 2026-2027
```

---

## Quick Reference: How to Access Each Dataset

| Source | Best Format | How to Get | Difficulty | Cost | Freshness |
|---|---|---|---|---|---|
| **UsableNet Lawsuits** | PACER (federal court docs) | pacer.uscourts.gov | Medium | Low ($) | Real-time |
| **WebAIM Million** | HTML table scrape | webaim.org + BeautifulSoup | Low-Medium | Free | Annual |
| **Section 508** | FOIA request | Submit to GSA | Medium | Free | Annual |
| **WCAG Specs** | GitHub repo | github.com/w3c/wcag | Low | Free | Continuous |
| **EU EAA Data** | Member state agencies | Direct contact | High | Variable | Emerging |

---

## Recommended Implementation Strategy

### Phase 1: Low-Hanging Fruit (2-4 weeks)

```python
# Collect WebAIM data
from bs4 import BeautifulSoup
import pandas as pd
import requests

# Scrape WebAIM Million
url = "https://webaim.org/projects/million/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract key tables
tables = pd.read_html(response.text)

# Save to CSV
for i, table in enumerate(tables):
    table.to_csv(f"webaim_table_{i}.csv", index=False)

# Result: 7+ tables with compliance data by:
# - Industry, TLD, Language, Technology, etc.
```

### Phase 2: Court Data (4-8 weeks)

```python
# Setup PACER access
# 1. Register at pacer.uscourts.gov
# 2. Query for ADA accessibility cases
# 3. Use Python PACER client library (if available)
# 4. Filter for digital/website accessibility lawsuits

# Query pattern:
# ["ADA"] AND ["website" OR "digital" OR "web accessibility"]
# Court: All federal courts
# Date range: 2020-2026

# Estimated records: 3,000-5,000 federal cases
# Cost: ~$300-500 at $0.10 per page
```

### Phase 3: Federal Agency Data (8-12 weeks)

```
# FOIA Request to GSA
1. Submit request for:
   - All Section 508 compliance metrics (2020-2026)
   - Agency-level website conformance data
   - Individual agency maturity assessments

2. Preferred format: CSV or JSON

3. Processing time: 30-60 days typical

4. Expected records: 250+ federal agencies with compliance data
```

### Phase 4: Build Unified Dashboard

```
Combine data sources:
- WebAIM: Compliance baseline (private sector, top 1M sites)
- Section 508: Government compliance (federal agencies)
- PACER: Lawsuit risk (geographic + industry patterns)
- W3C WCAG: Technical standards reference

Visualizations:
- Compliance by industry/geography
- Lawsuit risk heatmap
- Technology stack impact
- Trend analysis 2020-2026
```

---

## Licensing & Usage Rights

### Open Data (No Restrictions)
- WebAIM Million (public analysis)
- WCAG specifications (Creative Commons)
- PACER court documents (public record)

### Restricted Access
- UsableNet reports (commercial content, may have ToS)
- Section 508 reports (public but may require attribution)
- EU documents (ETSI/EAA may have IP restrictions)

### Recommendation
```
Before automated data collection, review:
1. Website robots.txt and ToS
2. API terms of service
3. Licensing information
4. Attribution requirements
5. Commercial use restrictions
```

---

## Tools & Libraries for Data Extraction

### Python Libraries
```
- pdfplumber: PDF text/table extraction
- BeautifulSoup4: HTML parsing
- Selenium: JavaScript-heavy sites
- Requests: HTTP requests
- Pandas: Data manipulation
- Scrapy: Large-scale scraping framework
```

### PACER Access
```
- pacer-python (community-maintained)
- selenium (for web scraping PACER)
- RECAP Archive API (alternative: https://www.courtlistener.com/api/)
```

### Data Processing
```
- DuckDB: SQL queries on CSV/Parquet
- Jupyter: Interactive analysis
- Plotly/Matplotlib: Visualization
```

---

## Summary: Machine-Readable Status

| Source | Format | Native Machine-Readable | Extractable | Recommendation |
|---|---|---|---|---|
| UsableNet | PDF report | ❌ No | ✅ Yes (PDF parse) | Use PACER instead |
| WebAIM | HTML tables | 🟡 Partial | ✅ Yes (scrape) | Scrape directly |
| Section 508 | PDF reports | ❌ No | ✅ Yes (FOIA) | Request structured |
| WCAG 2.2 | XML/JSON | ✅ Yes | ✅ Yes (GitHub) | Clone repo |
| EU Directives | PDF/HTML | ❌ No | 🟡 Maybe (varies) | Contact agencies |

---

*Document created: 2026-02-12*
*Cache location: /home/coolhand/geepers/swarm/cache/accessibility-data-sources-access-guide.md*

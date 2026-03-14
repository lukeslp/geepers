# ADA Digital Accessibility Lawsuits & Web Accessibility Compliance Data

**Compiled:** February 12, 2026
**Status:** Comprehensive research from 5 major sources
**Last Updated:** 2026-02-12

---

## Executive Summary

This research compiles data on digital accessibility lawsuits and compliance metrics from multiple authoritative sources. Key findings show that over 5,000 ADA web lawsuits have been filed, with concentrated geographic risk in New York and California. Meanwhile, WCAG compliance remains abysmal: 94.8% of top 1 million websites have detectable WCAG failures.

---

## 1. UsableNet ADA Lawsuit Reports

### Source Information
- **URL:** https://blog.usablenet.com/ada-web-lawsuit-trends-2026
- **Publisher:** UsableNet, Inc.
- **Data Type:** Annual lawsuit analysis report (blog post + PDF download)
- **Frequency:** Annual (2025 data released January 2026)
- **Format:** PDF report available for download
- **Machine-Readable:** PDF (not natively machine-readable, requires parsing)
- **Access:** Free to download

### Key 2025 Findings

#### Lawsuit Volume & Trends
- **Total lawsuits filed through 2025:** 5,000+ digital accessibility lawsuits
- **10.3% decrease in error density** from 2024 (51.0 errors per page in 2025 vs. 56.8 in 2024)
- **Monthly filing rates:** Consistently 150+ new cases per month throughout 2025

#### Geographic Concentration
- **New York:** Well over one-third of all state-level ADA website lawsuits
- **New York + California combined:** Nearly 2,000 cases filed in state courts
- **Federal filings:** 3,100+ additional cases (many tied to user activity in New York)
- **Florida:** Reemerged as high-volume jurisdiction (80-110 filings/month)
- **Emerging states:** Pennsylvania, Minnesota, Missouri show increasing activity
- **Key finding:** Physical presence NOT required; if users in these states can access your site, cases proceed

#### Repeat Defendants (CRITICAL)
- **1,427 companies** out of 5,000+ lawsuits (29%) were repeat defendants
- **In federal court:** 46% of cases involved repeat defendants
- **Pattern:** Settlement → limited remediation → new plaintiff → refiling within months
- **Risk escalation:** One lawsuit materially increases likelihood of another

#### Industry Concentration
- **E-commerce:** ~70% of all ADA web lawsuits
- **Food & service businesses:** ~21%
- **Healthcare:** 2-3%
- **All others:** Comparatively small share (education, travel, entertainment, finance)

#### Company Size Effect
- **36% of sued companies** report annual revenue exceeding $25 million
- **Top 500 e-commerce retailers:** 35.8% received at least one ADA lawsuit
- **Large retailers:** Disproportionate exposure due to brand recognition, high traffic, visibility

#### Accessibility Widgets (IMPORTANT)
- Widgets explicitly referenced in complaints—not as protection
- **Widget users** saw NO meaningful reduction in lawsuits
- Monthly filing data shows constant ~150+ cases/month regardless of widget use
- **Legal conclusion:** Widgets do not materially reduce legal risk

#### Plaintiff Bar Characteristics
- Small number of firms account for majority of 2025 filings
- Standardized, sophisticated complaints with fluent accessibility references
- Systematic, deliberate litigation model (not reactive enforcement)
- File at scale across federal and state courts
- Adapt quickly to jurisdiction-specific requirements

### Data Access
- **How to get:** Download 2025 ADA Web Lawsuit Report (PDF) from blog post
- **Historical reports:** Available on UsableNet website
- **No API:** Access is manual download only
- **Recommendation:** Parse lawsuit complaint text from federal courts directly for machine-readable data

---

## 2. WebAIM Million Analysis

### Source Information
- **URL:** https://webaim.org/projects/million/
- **Publisher:** WebAIM (Web Accessibility In Mind)
- **Data Type:** Automated WCAG accessibility scan of top 1M websites
- **Frequency:** Annual (conducted February 2025, 7th consecutive year)
- **Format:** HTML report with embedded tables
- **Machine-Readable:** HTML tables (scrapeable); no JSON/CSV export noted
- **Access:** Free, public data
- **Methodology:** WAVE accessibility engine (automated detection)

### Key 2025 Findings

#### Overall Compliance
- **50,960,288 total accessibility errors** detected across 1 million pages
- **Average:** 51 errors per page (10.3% improvement from 56.8 in 2024)
- **94.8% of pages** had detected WCAG 2 failures (slight improvement from 95.9%)
- **Only 5.2% of pages** had zero detected WCAG failures

#### Most Common WCAG Failures (96% of all errors)
| Failure Type | % of Pages | Count |
|---|---|---|
| Low contrast text | 79.1% | 29.6 errors/page avg |
| Missing alt text for images | 55.5% | 11/page missing on avg |
| Missing form input labels | 48.2% | 34.2% unlabeled |
| Empty links | 45.4% | High impact |
| Empty buttons | 29.6% | High impact |
| Missing document language | 15.8% | Declining |

#### Page Complexity Growth
- **1.2 billion total page elements** across 1M pages
- **Average 1,257 elements per page** (Feb 2025)
- **7.1% increase** from 1,173 in Feb 2024
- **61% growth** over last 6 years
- **Error density:** 4.1% of all elements have detected errors (1 error per 24 elements)
- **Correlation:** Top 100K pages average 1,465 elements (45% more than bottom 100K)

#### Image & Alt Text
- **58.6 million images** across 1M pages (58.6 per page avg)
- **5.4% increase** from 2024
- **18.5% missing alt text** (11 per page avg)
- **44% of images without alt** are linked images (broken links)
- **13.4% have questionable/repetitive alt** (e.g., "image", "graphic", filename)
- **Expected:** ~1 in 3 images have missing, questionable, or repetitive alt text

#### Form Accessibility
- **6.3 form inputs per page** on average
- **34.2% not properly labeled** (missing label, aria-label, aria-labelledby, or title)

#### Heading Structure
- **24.8 million headings** detected (25 per page avg)
- **16.3% of pages** have multiple h1 tags (down from 16.8%)
- **39% of pages** have skipped heading levels (e.g., h2→h4)
- **9.8% of pages** have no headings at all (down from 11.3%)

#### ARIA Usage (Concerning)
- **105.5 million ARIA attributes** (106 per page!)
- **18.5% increase** in one year alone
- **5x higher** than 2019 levels
- **79.4% of pages** use ARIA (up from 74.6%)
- **Pages WITH ARIA:** 57 errors avg
- **Pages WITHOUT ARIA:** 27 errors avg
- **Key finding:** ARIA presence correlated with DOUBLED error rates
- **ARIA menus:** 4.5% of pages; 35% introduce accessibility barriers

#### Technology Impact (ERROR RATES)

**Best Performing CMS:**
- Divi: 27.6 errors/page (−45.9% vs avg)
- Webflow: 28.4 errors/page (−44.3%)
- Adobe Experience Manager: 30.7 (−39.8%)
- Drupal: 41.9 (−17.7%)
- WordPress: 50.0 (−1.9%, relatively neutral)

**Worst Performing CMS:**
- 1C-Bitrix: 97.0 errors/page (+90.3%)
- wpBakery: 63.5 (+24.6%)
- Joomla: 47.1 (−7.5%)

**Best JS Frameworks:**
- AngularJS: 37.7 (−26.0%)
- Next.js: 38.6 (−24.2%)
- React: 42.4 (−16.8%)
- Alpine.js: 44.1 (−13.4%)

**Worst JS Frameworks:**
- Mustache: 89.1 (+74.9%)
- Firebase: 74.6 (+46.5%)
- Redux: 78.2 (+53.4%)
- Angular: 70.7 (+38.8%)

**Worst JS Libraries:**
- Clipboard.js: 101.8 (+99.9%)
- SweetAlert2: 87.4 (+71.6%)
- crypto-js: 86.2 (+69.1%)
- FancyBox: 82.9 (+62.7%)
- OWL Carousel: 81.3 (+59.6%)

**Ad Networks (Increasing Errors):**
- theTradeDesk: 39.1 (−23.3%, best)
- Yandex: 89.5 (+75.6%, worst)
- Twitter Ads: 67.6 (+32.6%)
- Criteo: 80.7 (+58.4%)

#### By Industry Category
| Category | Avg Errors | vs Average |
|---|---|---|
| Government | 37.2 | −27.0% |
| Personal Finance | 37.7 | −26.0% |
| Non-Profit | 40.0 | −21.6% |
| **Shopping** | **71.2** | **+39.8%** (worst) |
| Sports | 66.3 | +30.1% |
| News/Weather | 59.8 | +17.4% |

#### By Top-Level Domain (TLD)
| TLD | # Pages | Avg Errors | vs Average |
|---|---|---|---|
| .gov | 1,967 | 19.6 | −61.6% (best) |
| .edu | 3,325 | 23.6 | −53.7% |
| .org | 48,191 | 37.3 | −26.9% |
| .com | 435,998 | 49.8 | −2.2% |
| .ru | 44,981 | 72.4 | +42.1% (worst) |
| .ua | 5,668 | 89.1 | +74.8% |
| .cz | 5,311 | 74.7 | +46.6% |

#### By Language
English-language pages performed best (39.8 errors, −22% vs avg)
Russian and Korean pages worst (84.6+ errors, +66-69%)

#### Other Findings
- **Tables:** 972,746 tables on 142,976 pages; only 16.6% had valid data table markup
- **Skip links:** 13.7% of pages; 10% of those were broken
- **ReCAPTCHA:** 14% of pages; +12.1 additional errors on avg
- **PWAs:** 13.9% of pages; +7.6 additional errors
- **OneTrust (cookie compliance):** 36.8 errors (better than average)
- **FingerprintJS (tracking):** 80.7 errors (worse than average)

### Data Access & Format
- **Primary:** HTML report at webaim.org/projects/million/
- **Lookup tool:** Enter domain to see specific site data
- **Historical data:** Available for 2019-2025 (7 years)
- **Machine-readable:** HTML tables (need parsing); no CSV/JSON export
- **API:** No public API mentioned
- **Recommendation:** Scrape HTML tables or contact WebAIM for data access

---

## 3. Section 508 Compliance Data (GSA)

### Source Information
- **URL:** https://www.section508.gov/manage/pmr/ (Program Maturity Reports archived)
- **URL:** https://www.section508.gov/manage/reporting/ (updated assessment framework)
- **Publisher:** General Services Administration (GSA)
- **Data Type:** Federal agency IT accessibility compliance reporting
- **Frequency:** Previously semi-annual; now annual (via Government-wide Section 508 Assessment)
- **Format:** PDF reports (Executive Summary + Supplemental)
- **Machine-Readable:** PDFs only (not structured data)
- **Access:** Free, public download

### Reporting Framework

**Replaced:** Semi-annual Program Maturity Reports (2013-2023)
**New Framework:** Government-wide Section 508 Assessment (starting 2023)

#### CFO Act Agency Reporting Requirements

**Part 1: Agency Information**
- Agency name
- Submitter name
- # Federal employees supporting Section 508
- # Contractors supporting Section 508

**Part 2: Program Maturity Metrics** (5 categories)
1. **Acquisition:** Section 508 contract language in procurement
2. **Technology Lifecycle Activities:** 508 in enterprise architecture, design, dev, testing, deployment
3. **Testing & Validation:** Section 508 conformance testing
4. **Complaints Process:** Track & resolve 508 complaints
5. **Training:** Stakeholder training on 508 roles/responsibilities

**Maturity Levels:**
- Ad Hoc: No formal policies/processes
- Planned: Policies/procedures defined & communicated
- Resourced: Resources committed; staff trained
- Measured: Validation performed; results tracked

**Part 3: Website Compliance Metrics**
- # Internet web pages evaluated + % conformant
- # Intranet web pages evaluated + % conformant

### Available Reports

**2023 (Latest):**
- Spring 2023 Executive Summary (PDF)
- Spring 2023 Executive Supplemental (PDF)

**2022:**
- Autumn & Spring reports (Executive + Supplemental PDFs)

**2021, 2020, 2019:**
- Archive of Executive Summary PDFs

### Key Context
- OMB Strategic Plan issued January 23, 2013 to improve federal IT accessibility management
- Section 752 of Consolidated Appropriations Act 2023 requires updated criteria
- Agencies report to: OMB, U.S. Access Board, CIO Council Accessibility Community of Practice (ACOP)
- Reports requested by Senate committees (Special Committee on Aging, DHS, HEP)

### Data Access
- **Download:** PDF reports from section508.gov
- **Machine-readable:** No—PDFs must be manually analyzed
- **Public dataset:** No API or structured database
- **Recommendation:** Federal agencies' internal data may be available via FOIA request

---

## 4. W3C Web Accessibility Initiative (WAI)

### Source Information
- **URL:** https://www.w3.org/WAI/
- **Publisher:** World Wide Web Consortium (W3C)
- **Data Type:** Web accessibility research, standards, and guidelines
- **Frequency:** Continuous updates; research modules released periodically
- **Format:** Primarily HTML documentation; some PDFs
- **Machine-Readable:** Limited; WCAG available in structured formats
- **Access:** Free, public

### Key Resources & Current Work

#### Active Research (February 2026)
**Cognitive Accessibility Research Modules (First Draft):**
- Voice systems & conversational interfaces
- Technology-assisted indoor navigation/wayfinding
- Online safety & wellbeing (algorithms & data)
- Supported decision-making online

#### Standards & Specifications
- **WCAG 2.2** (Web Content Accessibility Guidelines) — primary global standard
- **ATAG** (Authoring Tool Accessibility Guidelines)
- **UAAG** (User Agent Accessibility Guidelines)
- **WAI-ARIA** (Accessible Rich Internet Applications)
- **EN 301 549** (European harmonized standard)

#### Key Publications
- W3C WCAG documentation & implementation guides
- Testing & evaluation resources
- Case studies and best practices
- Accessibility evaluation reports

### Data Access
- **WCAG specifications:** Available in HTML, structured XML/JSON on GitHub
- **Implementation guides:** HTML format (scrapeable)
- **No centralized dataset:** WAI publishes guidance, not compliance statistics
- **Git repository:** https://github.com/w3c/wcag/ (machine-readable spec files)

### Limitations for Research
- W3C publishes standards/guidance, **not compliance data**
- No aggregate statistics on global WCAG compliance
- No direct lawsuit tracking
- Primary resource: Technical guidance rather than quantitative metrics

---

## 5. EU Web Accessibility Directive & European Accessibility Act

### Data Found (from UsableNet Blog)
- **European Accessibility Act (EAA):** June 28 deadline mentioned for compliance
- **Early enforcement:** Norway's HelsaMi case showing daily accessibility fines
- **Sweden:** Post regulatory evaluation of retail accessibility
- **Monitoring:** EU member states conducting assessments

### Limited Public Data
- Individual member state reports available
- No centralized EU accessibility compliance database found in this research
- EAA enforcement increasing but aggregated data sparse

---

## 6. Overlay Widget Effectiveness Data

### Key Finding (from UsableNet + WebAIM data)
- **UsableNet 2025:** Widgets explicitly appear in lawsuits as UNRESOLVED
- **WebAIM 2025:** No differentiation between widget-protected and unprotected sites in error counts
- **Lawsuit trend:** NO meaningful reduction in filing rates for widget users
- **Legal consensus:** Widgets do NOT materially reduce accessibility barriers or legal risk

**Sources:** Monthly filing data (150+ cases/month regardless of widget use)

---

## Data Sources Summary Table

| Source | URL | Format | Machine-Readable | Update Frequency | Lawsuit Data | Compliance Data | Coverage |
|---|---|---|---|---|---|---|---|
| **UsableNet** | blog.usablenet.com | PDF report | No (parse-able) | Annual | Yes (5000+) | No | Legal trends |
| **WebAIM Million** | webaim.org/projects/million/ | HTML + tables | Partial (scrape) | Annual | No | Yes (51 errors/page avg) | Top 1M websites |
| **Section 508** | section508.gov | PDF reports | No | Annual | No | Yes (agency-level) | US Federal agencies |
| **W3C WAI** | w3.org/WAI/ | HTML specs | Yes (GitHub) | Continuous | No | No (guidance only) | Standards |
| **EU Directives** | Various | Policy docs | Limited | Variable | No | Emerging data | EU member states |

---

## Recommendations for Programmatic Access

### For Lawsuit Data
1. **Direct approach:** Scrape PACER (Public Access to Court Electronic Records) at pacer.uscourts.gov
2. **Parse-based:** Download UsableNet PDF reports; extract tables via PDF parser
3. **Real-time:** Set up Google Scholar alerts for ADA accessibility lawsuits

### For WCAG Compliance Data
1. **WebAIM:** Scrape HTML tables from webaim.org/projects/million/ (note robot.txt)
2. **Build custom scan:** Use WAVE API or Axe DevTools API for your own scans
3. **Historical:** Request archived WebAIM data for 2019-2024 comparison

### For Federal Section 508 Data
1. **Contact GSA:** Request structured dataset via Section 508 Program office
2. **FOIA request:** Federal agencies must disclose compliance metrics
3. **OMB reporting portal:** OMB-MAX may have aggregated data (classified)

### For Standards & Guidance
1. **W3C GitHub:** Clone wcag repository for structured WCAG 2.2 spec
2. **Subscribe:** W3C WAI mailing lists for research updates

---

## Key Takeaways

1. **Lawsuit volume growing:** 5,000+ ADA web lawsuits filed; repeat defendants at 29%
2. **Geographic risk concentrated:** New York = 1/3 of state lawsuits; physical presence not required
3. **Industry risk varied:** E-commerce = 70% of lawsuits; government sites most compliant
4. **Compliance poor:** 94.8% of top 1M websites have WCAG failures; only 5.2% perfect
5. **Widget strategy ineffective:** No evidence of reduced lawsuit risk from overlay widgets
6. **Technology matters:** CMS choice, JS framework selection significantly impacts compliance
7. **ARIA misuse increasing:** 79.4% use ARIA; pages with ARIA have 2x more errors
8. **Federal government better:** Section 508-reporting agencies generally more compliant than private sector
9. **Standards clear but complex:** W3C publishes comprehensive WCAG guidelines; implementation remains challenging

---

## Files & Further Resources

- **UsableNet:** Full 2025 report downloadable from blog.usablenet.com/ada-web-lawsuit-trends-2026
- **WebAIM:** Site lookup tool at webaim.org/projects/million/ (enter any domain)
- **Section 508:** PMR archive at section508.gov/manage/pmr/
- **WCAG Spec:** https://www.w3.org/WAI/WCAG22/quickref/
- **PACER:** pacer.uscourts.gov (federal court documents)

---

*Research compiled by Claude Code
Cache file: /home/coolhand/geepers/swarm/cache/ada-accessibility-lawsuit-research-2026.md*

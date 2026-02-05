# Data Visualization Patterns

Comprehensive collection of battle-tested data visualization patterns extracted from production datavis projects. These snippets cover interactive charts, maps, timelines, and animation patterns using D3.js, Chart.js, Leaflet, and vanilla JavaScript.

**Last Updated:** 2025-11-09
**Total Snippets:** 5
**Primary Libraries:** D3.js v7, Chart.js v3, Leaflet.js
**Focus:** Interactive data storytelling, geographic visualization, temporal analysis

---

## Table of Contents

- [Quick Start](#quick-start)
- [Snippet Overview](#snippet-overview)
- [Common Patterns](#common-patterns)
- [Integration Guide](#integration-guide)
- [Best Practices](#best-practices)

---

## Quick Start

### Installation

Most snippets are self-contained JavaScript files. Install required libraries via CDN or npm:

```html
<!-- D3.js (for network graphs, choropleths) -->
<script src="https://d3js.org/d3.v7.min.js"></script>

<!-- Chart.js (for dashboards, statistical charts) -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@3"></script>

<!-- Leaflet (for interactive maps) -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9/dist/leaflet.js"></script>
```

Or via npm:
```bash
npm install d3 chart.js leaflet
```

### Basic Usage

```javascript
// Import pattern
import { loadCSV, formatNumber } from './data-transformation-utils.js';
import { createBarChart } from './chart-js-responsive-dashboards.js';

// Load data
const data = await loadCSV('/data/spending.csv');

// Create visualization
const chart = createBarChart(canvas, labels, values, {
  formatValue: formatNumber,
  horizontal: true
});
```

---

## Snippet Overview

### 1. D3 Force-Directed Network Visualization

**File:** `d3-force-network-visualization.js`

**Description:** Complete pattern for creating interactive force-directed graphs with mobile support, filtering, tooltips, and pinned node layouts.

**Key Features:**
- Mobile touch handling (pinch-to-zoom, drag, tap)
- "Dream catcher" layout with pinned peripheral nodes
- Connection type indicators (line styling, colors, dashing)
- Dynamic filtering and re-rendering
- Keyboard accessible navigation
- Performance optimized for 50-200 nodes

**Use Cases:**
- Corporate board interlocks and relationship mapping
- Social network visualization
- Organization charts with cross-functional relationships
- Knowledge graphs and entity relationships

**Dependencies:** D3.js v7+

**Example:**
```javascript
const nodes = [
  { id: "AAPL", name: "Apple Inc.", type: "company", connections: 3 },
  { id: "GOV1", name: "Military Service", type: "category", pinned: true }
];

const links = [
  { source: "AAPL", target: "MSFT", type: "board", sharedDirectors: ["John Doe"] }
];

const { simulation, node, link } = renderNetwork(nodes, links);
```

**Source:** Extracted from `/home/coolhand/html/datavis/dowjones/script.js`

---

### 2. Interactive Timeline Animation

**File:** `timeline-animation-interactive.js`

**Description:** Animated timeline showing historical progression with future projections. Perfect for before/after advocacy journalism and temporal data storytelling.

**Key Features:**
- Historical + projection modes with visual distinction
- Playback controls (play, pause, reset, speed adjustment)
- Keyboard shortcuts (Space, Arrow keys, R)
- Scrolling event feed
- Animated number counters with easing
- Narrative text system tied to specific years

**Use Cases:**
- Crisis timeline visualization (hospital closures, climate events)
- Before/after policy impact projection
- Temporal progression with narrative context
- Educational timelines with automated playback

**Dependencies:** Vanilla JavaScript (no framework)

**Example:**
```javascript
// Configure timeline
const config = {
  startYear: 2010,
  endYear: 2028,
  projectionStartYear: 2025,
  speed: 1000 // ms per year
};

// Generate data
const historicalData = generateHistoricalData();
const projectionData = generateProjectionData();

// Initialize
init();
```

**Source:** Extracted from `/home/coolhand/html/datavis/healthcare_deserts/UX-TEST/layout-crisis-timeline/script.js`

---

### 3. Data Transformation Utilities

**File:** `data-transformation-utils.js`

**Description:** Comprehensive collection of utility functions for data loading, parsing, formatting, filtering, and state management. Pure vanilla JavaScript.

**Key Functions:**

**Data Loading:**
- `loadCSV(url)` - Load and parse CSV with error handling
- `loadJSON(url)` - Load JSON with error handling
- `parseCSV(text)` - Parse CSV text handling quoted fields

**Formatting:**
- `formatNumber(num)` - Format with commas: `1234567 → "1,234,567"`
- `formatPercent(num, decimals)` - Format as percentage: `0.758 → "76%"`
- `formatCurrency(num, compact)` - Format currency: `25000000 → "$25.0M"`
- `formatDate(date, format)` - Format dates (short, long, ISO)

**Data Operations:**
- `filterBySearch(items, term, fields)` - Search across multiple fields
- `groupBy(items, field)` - Group array by field value
- `sortBy(items, field, descending)` - Sort by field
- `aggregate(items, field)` - Calculate sum, avg, min, max, count

**State Management:**
- `AppState` class - Lightweight pub/sub pattern

**Performance:**
- `debounce(func, wait)` - Debounce function calls
- `throttle(func, limit)` - Throttle execution rate

**Animation:**
- `animateValue(element, start, end, duration)` - Number counting animation
- `isInViewport(element)` - Check element visibility
- `observeElements(selector, callback, options)` - Intersection Observer helper

**Use Cases:**
- CSV/JSON data loading with error handling
- Number and percentage formatting for display
- Data filtering and grouping operations
- Simple state management without frameworks
- UI performance optimization

**Dependencies:** None (pure JavaScript)

**Example:**
```javascript
// Load and format data
const data = await loadCSV('/data/hospitals.csv');
const formatted = data.map(row => ({
  ...row,
  displayBudget: formatCurrency(row.budget, true),
  displayPercent: formatPercent(row.uninsured)
}));

// Filter and aggregate
const california = filterBySearch(data, 'california', ['state']);
const stats = aggregate(california, 'population');
console.log(`Average population: ${formatNumber(stats.avg)}`);

// State management
const state = new AppState({ currentYear: 2024 });
state.subscribe((newState, changes) => updateUI(changes));
state.set('currentYear', 2025);
```

**Source:** Extracted from `/home/coolhand/html/datavis/healthcare_deserts/UX-TEST/shared/utils.js`

---

### 4. Leaflet Choropleth Map

**File:** `leaflet-choropleth-map.js`

**Description:** Create interactive choropleth maps with Leaflet showing data density by geographic regions. Includes hover effects, popups, info control, and legend.

**Key Features:**
- Color scale based on data density
- Hover highlighting with visual feedback
- Information control showing details on hover
- Legend with color scale reference
- Fully customizable color scheme
- GeoJSON boundary support

**Use Cases:**
- Geographic data visualization (population, statistics, counts)
- Regional analysis and comparison
- Data-driven storytelling with maps
- County/state/country-level visualizations

**Dependencies:** Leaflet.js, GeoJSON data

**Example:**
```javascript
// Initialize map
const map = L.map('map').setView([20, 0], 2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Color scale
function getColor(value) {
  return value > 10 ? '#800026' :
         value > 5  ? '#BD0026' :
         value > 2  ? '#E31A1C' :
                      '#FD8D3C';
}

// Load and style GeoJSON
fetch('countries.geo.json')
  .then(response => response.json())
  .then(data => {
    L.geoJson(data, {
      style: (feature) => ({
        fillColor: getColor(dataByRegion[feature.properties.ADMIN]),
        fillOpacity: 0.7,
        color: 'white',
        weight: 1
      }),
      onEachFeature: (feature, layer) => {
        layer.on({
          mouseover: highlightFeature,
          mouseout: resetHighlight
        });
      }
    }).addTo(map);
  });
```

**Source:** Previously existing in `/home/coolhand/SNIPPETS/data-visualization/leaflet-choropleth-map.js`

---

### 5. Chart.js Responsive Dashboards

**File:** `chart-js-responsive-dashboards.js`

**Description:** Complete patterns for creating interactive, themeable dashboards using Chart.js. Includes bar charts, radar charts, bubble charts, line charts, and theme switching.

**Key Features:**
- Multiple chart types with consistent API
- Dark/light theme support with CSS custom properties
- Charts auto-update on theme change
- Fully responsive with proper cleanup
- Chart registry for lifecycle management
- Color palette generator for multi-series charts

**Chart Types:**
- `createBarChart()` - Horizontal/vertical bar charts
- `createBubbleChart()` - Multi-dimensional bubble visualization
- `createRadarChart()` - Spider/radar charts for multi-metric comparison
- `createLineChart()` - Temporal/sequential line charts

**Use Cases:**
- Multi-metric comparison dashboards
- Financial data visualization (spending, revenue, budgets)
- Statistical analysis displays
- KPI monitoring and reporting
- Before/after comparison views

**Dependencies:** Chart.js v3+, optional chartjs-plugin-datalabels

**Example:**
```javascript
// Create bar chart
const states = ['California', 'Texas', 'New York'];
const spending = [450000, 380000, 420000];

const barChart = createBarChart(canvas, states, spending, {
  horizontal: true,
  label: 'Federal Spending',
  formatValue: (value) => `$${(value / 1000).toFixed(1)}B`
});
registerChart('barChart', barChart);

// Create radar chart for comparisons
const metrics = ['Education', 'Healthcare', 'Infrastructure'];
const radarData = [
  { label: 'California', data: [85, 90, 70] },
  { label: 'Texas', data: [75, 70, 80] }
];
const radarChart = createRadarChart(canvas, metrics, radarData, {
  max: 100,
  formatValue: (val) => `${val}%`
});

// Theme toggle
document.getElementById('themeToggle').addEventListener('click', () => {
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', newTheme);

  updateChartsTheme(() => {
    // Recreate all charts with new theme
  });
});
```

**Source:** Extracted from `/home/coolhand/html/datavis/spending/federal_spending_chart_modern.html`

---

## Common Patterns

### Responsive Design

All snippets follow mobile-first responsive patterns:

```javascript
const isMobile = window.innerWidth <= 768;
const isSmallMobile = window.innerWidth <= 480;

// Adjust parameters based on screen size
const nodeRadius = baseRadius * (isMobile ? 0.8 : 1);
const linkDistance = baseLinkDistance * (isMobile ? 0.85 : 1);
```

### Theme Support

CSS custom properties enable seamless theme switching:

```css
:root {
  --text-primary: #1f2937;
  --bg-primary: #ffffff;
  --chart-primary: #0ea5e9;
}

[data-theme="dark"] {
  --text-primary: #f3f4f6;
  --bg-primary: #111827;
  --chart-primary: #38bdf8;
}
```

```javascript
const colors = {
  textPrimary: getComputedStyle(document.documentElement)
    .getPropertyValue('--text-primary').trim()
};
```

### Data Loading

Consistent async data loading with error handling:

```javascript
async function loadCSV(url) {
  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return parseCSV(await response.text());
  } catch (error) {
    console.error('Error loading CSV:', error);
    return [];
  }
}
```

### Accessibility

All visualizations include WCAG 2.1 AA compliance:

```javascript
// ARIA labels
node.attr('aria-label', d => `${d.name}: ${d.connections} connections`);

// Keyboard navigation
document.addEventListener('keydown', (event) => {
  if (event.code === 'Space') togglePlayback();
  if (event.code === 'ArrowRight') stepForward();
});

// Screen reader announcements
const liveRegion = document.getElementById('sr-announcements');
liveRegion.textContent = `Now viewing: ${selectedNode.name}`;
```

---

## Integration Guide

### Building a Complete Dashboard

Combine multiple snippets for full-featured data visualizations:

```javascript
// 1. Load utilities
import { loadCSV, formatNumber, formatCurrency } from './data-transformation-utils.js';
import { createBarChart, createRadarChart } from './chart-js-responsive-dashboards.js';

// 2. Load data
const data = await loadCSV('/data/spending.csv');

// 3. Create visualizations
const barChart = createBarChart(
  document.getElementById('barChart'),
  data.map(d => d.state),
  data.map(d => d.spending),
  {
    horizontal: true,
    formatValue: formatCurrency
  }
);

// 4. Add interactivity
data.forEach((row, i) => {
  const element = document.querySelectorAll('.data-row')[i];
  element.addEventListener('click', () => {
    highlightChartSegment(barChart, i);
  });
});

// 5. Handle theme changes
document.getElementById('themeToggle').addEventListener('click', () => {
  toggleTheme();
  updateChartsTheme(() => recreateAllCharts());
});
```

### Network Graph + Map Integration

Combine D3 network with Leaflet choropleth:

```javascript
import { renderNetwork } from './d3-force-network-visualization.js';

// Create network
const network = renderNetwork(nodes, links);

// Sync with map
network.node.on('click', (event, d) => {
  const mapFeature = findMapFeature(d.id);
  map.fitBounds(mapFeature.getBounds());
  highlightMapRegion(mapFeature);
});
```

---

## Best Practices

### Performance

1. **Debounce resize events:**
   ```javascript
   window.addEventListener('resize', debounce(() => {
     chart.resize();
   }, 250));
   ```

2. **Limit force simulation iterations:**
   ```javascript
   setTimeout(() => simulation.stop(), 5000);
   ```

3. **Use viewport detection for lazy loading:**
   ```javascript
   observeElements('.chart-container', (element) => {
     loadChart(element);
   }, { once: true });
   ```

### Data Management

1. **Always handle loading errors:**
   ```javascript
   const data = await loadCSV(url);
   if (data.length === 0) {
     showErrorMessage('Failed to load data');
     return;
   }
   ```

2. **Validate data before visualization:**
   ```javascript
   const validData = data.filter(row =>
     row.value !== null && !isNaN(row.value)
   );
   ```

3. **Use consistent data formats:**
   ```javascript
   const normalized = data.map(row => ({
     label: row.name,
     value: parseFloat(row.amount),
     formatted: formatCurrency(row.amount)
   }));
   ```

### Accessibility

1. **Provide text alternatives:**
   ```html
   <canvas id="chart" role="img" aria-label="Bar chart showing federal spending by state"></canvas>
   ```

2. **Support keyboard navigation:**
   ```javascript
   element.addEventListener('keydown', (e) => {
     if (e.key === 'Enter' || e.key === ' ') {
       handleSelection(e.target);
     }
   });
   ```

3. **Use semantic HTML:**
   ```html
   <section aria-labelledby="chart-title">
     <h2 id="chart-title">Federal Spending Analysis</h2>
     <div class="chart-container">...</div>
   </section>
   ```

---

## Browser Compatibility

- **Chrome/Edge (Chromium):** 90+
- **Firefox:** 88+
- **Safari:** 14+
- **Mobile:** iOS Safari 13+, Chrome Android (latest)

**Required Features:**
- ES6 modules (`import`/`export`)
- Fetch API
- CSS custom properties
- IntersectionObserver (for scroll animations)
- ResizeObserver (for responsive charts)

---

## Additional Resources

### Official Documentation
- [D3.js Documentation](https://d3js.org/)
- [Chart.js Documentation](https://www.chartjs.org/)
- [Leaflet Documentation](https://leafletjs.com/)

### Related Snippets
- See `/home/coolhand/SNIPPETS/api-clients/` for data fetching patterns
- See `/home/coolhand/SNIPPETS/web-frameworks/` for Flask/FastAPI integration
- See `/home/coolhand/SNIPPETS/testing/` for visualization unit tests

### Example Projects
- **Source Projects:** `/home/coolhand/html/datavis/dowjones/`, `healthcare_deserts/`, `spending/`
- **Live Demos:** https://dr.eamer.dev/datavis/

---

## Support

For questions or issues with these snippets:

1. Check the snippet's inline documentation and usage examples
2. Review the source files for additional context
3. Consult library documentation for API details
4. Refer to `/home/coolhand/html/datavis/CLAUDE.md` for project-specific guidance

---

**Maintained By:** Luke Steuber
**License:** Open source, use freely with attribution appreciated
**Last Harvest:** 2025-11-09 from datavis projects

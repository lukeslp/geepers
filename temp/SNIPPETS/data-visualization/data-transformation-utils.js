/**
 * Data Transformation and Utility Functions for Visualizations
 *
 * Description: Comprehensive collection of utility functions for data loading,
 * parsing, formatting, filtering, and state management in data visualization projects.
 * Pure vanilla JavaScript with no dependencies.
 *
 * Use Cases:
 * - CSV/JSON data loading with error handling
 * - Number and percentage formatting for display
 * - Data filtering and grouping operations
 * - Simple pub/sub state management
 * - UI performance optimization (debounce, viewport detection)
 * - Animation utilities (number counting, scroll-triggered reveals)
 *
 * Dependencies:
 * - None (pure JavaScript)
 *
 * Notes:
 * - All functions are framework-agnostic
 * - Includes both sync and async utilities
 * - Error handling built into data loading functions
 * - Lightweight state management pattern for simple apps
 * - Performance optimized with debouncing and lazy loading
 *
 * Related Snippets:
 * - See d3-force-network-visualization.js for D3-specific data transforms
 * - See timeline-animation-interactive.js for temporal data handling
 * - See chart-js-dashboards.js for chart data formatting
 *
 * Source Attribution:
 * - Extracted from: /home/coolhand/html/datavis/healthcare_deserts/UX-TEST/shared/utils.js
 * - Pattern used across: Multiple datavis projects (dowjones, healthcare_deserts, veterans)
 * - Related: Lodash utilities, D3 data loaders
 */

// ==================== DATA LOADING ====================

/**
 * Load and parse CSV file with error handling
 * @param {string} url - URL or path to CSV file
 * @returns {Promise<Array>} Parsed data as array of objects
 */
export async function loadCSV(url) {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    const text = await response.text();
    return parseCSV(text);
  } catch (error) {
    console.error('Error loading CSV:', error);
    return [];
  }
}

/**
 * Load JSON file with error handling
 * @param {string} url - URL or path to JSON file
 * @returns {Promise<Object|Array>} Parsed JSON data
 */
export async function loadJSON(url) {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error loading JSON:', error);
    return null;
  }
}

/**
 * Simple CSV parser handling quoted fields
 * Supports comma-separated values with quoted strings
 * @param {string} text - Raw CSV text
 * @returns {Array<Object>} Parsed rows as objects with header keys
 */
function parseCSV(text) {
  const lines = text.trim().split('\n');
  const headers = lines[0].split(',').map(h => h.trim().replace(/"/g, ''));

  return lines.slice(1).map(line => {
    const values = [];
    let current = '';
    let inQuotes = false;

    for (let i = 0; i < line.length; i++) {
      const char = line[i];
      if (char === '"') {
        inQuotes = !inQuotes;
      } else if (char === ',' && !inQuotes) {
        values.push(current.trim());
        current = '';
      } else {
        current += char;
      }
    }
    values.push(current.trim());

    const obj = {};
    headers.forEach((header, i) => {
      const value = values[i] ? values[i].replace(/"/g, '') : '';
      // Try to parse as number
      obj[header] = isNaN(value) ? value : parseFloat(value);
    });
    return obj;
  });
}

// ==================== DATA FORMATTING ====================

/**
 * Format large numbers with commas (US locale)
 * @param {number} num - Number to format
 * @returns {string} Formatted number or em dash if invalid
 */
export function formatNumber(num) {
  if (num === null || num === undefined || isNaN(num)) return '—';
  return Math.round(num).toLocaleString('en-US');
}

/**
 * Format decimal as percentage
 * @param {number} num - Decimal number (0.75 = 75%)
 * @param {number} decimals - Number of decimal places (default 0)
 * @returns {string} Formatted percentage
 */
export function formatPercent(num, decimals = 0) {
  if (num === null || num === undefined || isNaN(num)) return '—';
  return `${(num * 100).toFixed(decimals)}%`;
}

/**
 * Format currency (US dollars)
 * @param {number} num - Dollar amount
 * @param {boolean} compact - Use compact notation for large numbers
 * @returns {string} Formatted currency
 */
export function formatCurrency(num, compact = false) {
  if (num === null || num === undefined || isNaN(num)) return '—';

  if (compact) {
    if (num >= 1e12) return `$${(num / 1e12).toFixed(1)}T`;
    if (num >= 1e9) return `$${(num / 1e9).toFixed(1)}B`;
    if (num >= 1e6) return `$${(num / 1e6).toFixed(1)}M`;
    if (num >= 1e3) return `$${(num / 1e3).toFixed(1)}K`;
  }

  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(num);
}

/**
 * Format date from various input types
 * @param {Date|string|number} date - Date to format
 * @param {string} format - Output format ('short', 'long', 'iso')
 * @returns {string} Formatted date
 */
export function formatDate(date, format = 'short') {
  const d = new Date(date);
  if (isNaN(d.getTime())) return '—';

  const formats = {
    short: { month: 'short', day: 'numeric', year: 'numeric' },
    long: { month: 'long', day: 'numeric', year: 'numeric' },
    iso: null  // Returns ISO string
  };

  if (format === 'iso') return d.toISOString().split('T')[0];

  return d.toLocaleDateString('en-US', formats[format] || formats.short);
}

// ==================== DATA FILTERING & GROUPING ====================

/**
 * Filter array by search term across multiple fields
 * @param {Array} items - Array of objects to filter
 * @param {string} searchTerm - Search query
 * @param {Array<string>} fields - Fields to search in
 * @returns {Array} Filtered items
 */
export function filterBySearch(items, searchTerm, fields) {
  if (!searchTerm) return items;

  const term = searchTerm.toLowerCase();
  return items.filter(item =>
    fields.some(field => {
      const value = item[field];
      return value && value.toString().toLowerCase().includes(term);
    })
  );
}

/**
 * Group array by field value
 * @param {Array} items - Array of objects to group
 * @param {string} field - Field to group by
 * @returns {Object} Object with field values as keys, arrays as values
 */
export function groupBy(items, field) {
  return items.reduce((groups, item) => {
    const key = item[field];
    if (!groups[key]) groups[key] = [];
    groups[key].push(item);
    return groups;
  }, {});
}

/**
 * Sort array by field (ascending or descending)
 * @param {Array} items - Array of objects to sort
 * @param {string} field - Field to sort by
 * @param {boolean} descending - Sort descending (default false)
 * @returns {Array} Sorted array (mutates original)
 */
export function sortBy(items, field, descending = false) {
  return items.sort((a, b) => {
    const aVal = a[field];
    const bVal = b[field];

    if (aVal === bVal) return 0;

    const comparison = aVal > bVal ? 1 : -1;
    return descending ? -comparison : comparison;
  });
}

/**
 * Calculate statistical aggregates
 * @param {Array} items - Array of objects
 * @param {string} field - Numeric field to aggregate
 * @returns {Object} Statistics (sum, avg, min, max, count)
 */
export function aggregate(items, field) {
  const values = items.map(item => item[field]).filter(v => typeof v === 'number');

  if (values.length === 0) {
    return { sum: 0, avg: 0, min: 0, max: 0, count: 0 };
  }

  const sum = values.reduce((acc, val) => acc + val, 0);
  return {
    sum,
    avg: sum / values.length,
    min: Math.min(...values),
    max: Math.max(...values),
    count: values.length
  };
}

// ==================== STATE MANAGEMENT ====================

/**
 * Simple pub/sub state management pattern
 * Lightweight alternative to Redux for simple visualization apps
 */
export class AppState {
  constructor(initialState = {}) {
    this.state = { ...initialState };
    this.listeners = [];
  }

  get(key) {
    return this.state[key];
  }

  set(key, value) {
    const oldValue = this.state[key];
    this.state[key] = value;
    this.notify({ [key]: value }, oldValue);
  }

  update(updates) {
    const oldState = { ...this.state };
    Object.assign(this.state, updates);
    this.notify(updates, oldState);
  }

  subscribe(listener) {
    this.listeners.push(listener);
    // Return unsubscribe function
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener);
    };
  }

  notify(changes, oldValue) {
    this.listeners.forEach(listener => listener(this.state, changes, oldValue));
  }

  reset() {
    this.state = {};
    this.notify({}, null);
  }
}

// ==================== PERFORMANCE UTILITIES ====================

/**
 * Debounce function calls (prevents excessive execution)
 * @param {Function} func - Function to debounce
 * @param {number} wait - Milliseconds to wait
 * @returns {Function} Debounced function
 */
export function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

/**
 * Throttle function calls (limits execution rate)
 * @param {Function} func - Function to throttle
 * @param {number} limit - Minimum milliseconds between executions
 * @returns {Function} Throttled function
 */
export function throttle(func, limit) {
  let inThrottle;
  return function(...args) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

// ==================== ANIMATION UTILITIES ====================

/**
 * Animate number counting up with easing
 * @param {HTMLElement} element - Element to update
 * @param {number} start - Starting value
 * @param {number} end - Target value
 * @param {number} duration - Animation duration in ms
 */
export function animateValue(element, start, end, duration) {
  const startTime = performance.now();
  const diff = end - start;

  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);

    // Easing function (ease-out cubic)
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = start + (diff * eased);

    element.textContent = formatNumber(current);

    if (progress < 1) {
      requestAnimationFrame(update);
    }
  }

  requestAnimationFrame(update);
}

/**
 * Check if element is in viewport
 * @param {HTMLElement} element - Element to check
 * @returns {boolean} True if in viewport
 */
export function isInViewport(element) {
  const rect = element.getBoundingClientRect();
  return (
    rect.top >= 0 &&
    rect.left >= 0 &&
    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
  );
}

/**
 * Intersection Observer helper for scroll animations
 * @param {string} selector - CSS selector for elements to observe
 * @param {Function} callback - Function to call when element enters viewport
 * @param {Object} options - Observer options
 * @returns {IntersectionObserver} Observer instance
 */
export function observeElements(selector, callback, options = {}) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        callback(entry.target);
        if (options.once) observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: options.threshold || 0.1,
    rootMargin: options.rootMargin || '0px'
  });

  document.querySelectorAll(selector).forEach(el => observer.observe(el));
  return observer;
}

// ==================== COLOR UTILITIES ====================

/**
 * Generate color scale for choropleth/heatmaps
 * @param {number} value - Value to map to color
 * @param {Array<number>} domain - [min, max] value range
 * @param {Array<string>} colors - Color range (hex or rgb)
 * @returns {string} Interpolated color
 */
export function getColorScale(value, domain, colors = ['#ffeda0', '#f03b20']) {
  const normalized = (value - domain[0]) / (domain[1] - domain[0]);
  const clamped = Math.max(0, Math.min(1, normalized));

  // Simple linear interpolation (for more complex scales, use D3)
  if (colors.length === 2) {
    // Convert hex to RGB
    const start = hexToRgb(colors[0]);
    const end = hexToRgb(colors[1]);

    const r = Math.round(start.r + (end.r - start.r) * clamped);
    const g = Math.round(start.g + (end.g - start.g) * clamped);
    const b = Math.round(start.b + (end.b - start.b) * clamped);

    return `rgb(${r}, ${g}, ${b})`;
  }

  // Multi-stop gradient
  const index = clamped * (colors.length - 1);
  const lowerIndex = Math.floor(index);
  const upperIndex = Math.ceil(index);
  const fraction = index - lowerIndex;

  const start = hexToRgb(colors[lowerIndex]);
  const end = hexToRgb(colors[upperIndex]);

  const r = Math.round(start.r + (end.r - start.r) * fraction);
  const g = Math.round(start.g + (end.g - start.g) * fraction);
  const b = Math.round(start.b + (end.b - start.b) * fraction);

  return `rgb(${r}, ${g}, ${b})`;
}

function hexToRgb(hex) {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16)
  } : { r: 0, g: 0, b: 0 };
}

// ==================== USAGE EXAMPLES ====================

/*
// Data loading
const data = await loadCSV('/data/hospitals.csv');
const geoData = await loadJSON('/data/counties.geojson');

// Formatting
formatNumber(1234567);        // "1,234,567"
formatPercent(0.758);          // "76%"
formatCurrency(25000000, true); // "$25.0M"

// Filtering and grouping
const filtered = filterBySearch(data, 'california', ['state', 'county']);
const grouped = groupBy(data, 'state');
const sorted = sortBy(data, 'population', true); // descending

// Statistics
const stats = aggregate(data, 'population');
console.log(stats.avg, stats.max);

// State management
const state = new AppState({ currentYear: 2024 });
state.subscribe((newState, changes) => {
  console.log('State changed:', changes);
});
state.set('currentYear', 2025);

// Performance
const debouncedSearch = debounce(performSearch, 300);
input.addEventListener('input', debouncedSearch);

// Animations
observeElements('.stat-box', (element) => {
  element.classList.add('visible');
}, { once: true, threshold: 0.5 });

// Color scales
const color = getColorScale(75, [0, 100], ['#green', '#yellow', '#red']);
*/

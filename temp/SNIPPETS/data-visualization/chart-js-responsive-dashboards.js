/**
 * Chart.js Responsive Dashboard Patterns with Theme Support
 *
 * Description: Complete patterns for creating interactive, themeable dashboards
 * using Chart.js. Includes bar charts, radar charts, bubble charts, and theme
 * switching functionality. All charts are fully responsive with proper cleanup.
 *
 * Use Cases:
 * - Multi-metric comparison dashboards
 * - Financial data visualization (spending, revenue, budgets)
 * - Statistical analysis displays
 * - KPI monitoring and reporting
 * - Before/after comparison views
 *
 * Dependencies:
 * - Chart.js v3+ (https://www.chartjs.org/)
 * - chartjs-plugin-datalabels (optional, for value labels)
 *
 * Notes:
 * - Charts must be destroyed and recreated on theme change
 * - Responsive by default with maintainAspectRatio: false
 * - Theme colors extracted from CSS custom properties
 * - Supports dark/light modes seamlessly
 * - All chart types follow consistent configuration pattern
 *
 * Related Snippets:
 * - See data-transformation-utils.js for formatCurrency(), formatNumber()
 * - See d3-force-network-visualization.js for network overlays
 * - See timeline-animation-interactive.js for temporal updates
 *
 * Source Attribution:
 * - Extracted from: /home/coolhand/html/datavis/spending/federal_spending_chart_modern.html
 * - Pattern used in: Federal spending visualizations, economic dashboards
 * - Related: Chart.js official examples, Dashboard UI patterns
 */

// ==================== THEME MANAGEMENT ====================

/**
 * Get current theme colors from CSS custom properties
 * Ensures charts match the application theme
 */
function getThemeColors() {
  const root = getComputedStyle(document.documentElement);

  return {
    primary: root.getPropertyValue('--chart-primary')?.trim() || '#0ea5e9',
    secondary: root.getPropertyValue('--chart-secondary')?.trim() || '#8b5cf6',
    success: root.getPropertyValue('--chart-success')?.trim() || '#10b981',
    danger: root.getPropertyValue('--chart-danger')?.trim() || '#ef4444',
    warning: root.getPropertyValue('--chart-warning')?.trim() || '#f59e0b',
    info: root.getPropertyValue('--chart-info')?.trim() || '#06b6d4',

    textPrimary: root.getPropertyValue('--text-primary')?.trim() || '#1f2937',
    textSecondary: root.getPropertyValue('--text-secondary')?.trim() || '#6b7280',
    gridLines: root.getPropertyValue('--grid-lines')?.trim() || '#e5e7eb',
    background: root.getPropertyValue('--bg-primary')?.trim() || '#ffffff'
  };
}

/**
 * Color palette generator for multi-series charts
 * @param {number} count - Number of colors needed
 * @returns {Array<string>} Array of hex colors
 */
function generateColorPalette(count) {
  const baseColors = [
    '#0ea5e9', '#8b5cf6', '#10b981', '#ef4444', '#f59e0b',
    '#06b6d4', '#ec4899', '#6366f1', '#14b8a6', '#f97316'
  ];

  if (count <= baseColors.length) {
    return baseColors.slice(0, count);
  }

  // Generate additional colors if needed
  const additional = [];
  for (let i = baseColors.length; i < count; i++) {
    const hue = (i * 137.5) % 360; // Golden angle
    additional.push(`hsl(${hue}, 65%, 55%)`);
  }

  return [...baseColors, ...additional];
}

// ==================== CHART CONFIGURATIONS ====================

/**
 * Base configuration shared across all chart types
 */
const baseChartConfig = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    mode: 'index',
    intersect: false
  },
  animation: {
    duration: 750,
    easing: 'easeInOutQuart'
  }
};

/**
 * Create horizontal bar chart for rankings/comparisons
 * @param {HTMLCanvasElement} canvas - Canvas element
 * @param {Array} labels - Y-axis labels
 * @param {Array} data - Data values
 * @param {Object} options - Additional options
 */
function createBarChart(canvas, labels, data, options = {}) {
  const colors = getThemeColors();

  const config = {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: options.label || 'Values',
        data: data,
        backgroundColor: options.colors || colors.primary,
        borderColor: options.borderColors || colors.primary,
        borderWidth: 1,
        barThickness: options.barThickness || 'flex',
        maxBarThickness: options.maxBarThickness || 40
      }]
    },
    options: {
      ...baseChartConfig,
      indexAxis: options.horizontal ? 'y' : 'x',
      plugins: {
        legend: {
          display: options.showLegend !== false,
          labels: {
            color: colors.textPrimary,
            font: {
              size: 12,
              family: "'Inter', sans-serif"
            }
          }
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          titleColor: '#fff',
          bodyColor: '#fff',
          borderColor: colors.primary,
          borderWidth: 1,
          padding: 12,
          displayColors: true,
          callbacks: {
            label: function(context) {
              let label = context.dataset.label || '';
              if (label) {
                label += ': ';
              }
              if (options.formatValue) {
                label += options.formatValue(context.parsed.y || context.parsed.x);
              } else {
                label += context.parsed.y || context.parsed.x;
              }
              return label;
            }
          }
        }
      },
      scales: {
        x: {
          grid: {
            color: colors.gridLines,
            drawBorder: false
          },
          ticks: {
            color: colors.textSecondary,
            font: {
              size: 11
            },
            callback: options.xAxisFormat || null
          }
        },
        y: {
          grid: {
            color: colors.gridLines,
            drawBorder: false
          },
          ticks: {
            color: colors.textSecondary,
            font: {
              size: 11
            },
            callback: options.yAxisFormat || null
          }
        }
      }
    }
  };

  return new Chart(canvas, config);
}

/**
 * Create multi-dimensional bubble chart
 * @param {HTMLCanvasElement} canvas - Canvas element
 * @param {Array} datasets - Array of {x, y, r, label} objects
 * @param {Object} options - Additional options
 */
function createBubbleChart(canvas, datasets, options = {}) {
  const colors = getThemeColors();
  const palette = generateColorPalette(datasets.length);

  const config = {
    type: 'bubble',
    data: {
      datasets: datasets.map((dataset, i) => ({
        label: dataset.label,
        data: dataset.data,
        backgroundColor: palette[i] + '60', // 60 = ~37% opacity in hex
        borderColor: palette[i],
        borderWidth: 2
      }))
    },
    options: {
      ...baseChartConfig,
      plugins: {
        legend: {
          display: true,
          position: 'top',
          labels: {
            color: colors.textPrimary,
            usePointStyle: true
          }
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          callbacks: {
            label: function(context) {
              const point = context.raw;
              return [
                `${context.dataset.label}`,
                `${options.xLabel || 'X'}: ${options.formatX ? options.formatX(point.x) : point.x}`,
                `${options.yLabel || 'Y'}: ${options.formatY ? options.formatY(point.y) : point.y}`,
                `${options.rLabel || 'Size'}: ${options.formatR ? options.formatR(point.r) : point.r}`
              ];
            }
          }
        }
      },
      scales: {
        x: {
          title: {
            display: !!options.xLabel,
            text: options.xLabel,
            color: colors.textPrimary
          },
          grid: {
            color: colors.gridLines
          },
          ticks: {
            color: colors.textSecondary,
            callback: options.xAxisFormat || null
          }
        },
        y: {
          title: {
            display: !!options.yLabel,
            text: options.yLabel,
            color: colors.textPrimary
          },
          grid: {
            color: colors.gridLines
          },
          ticks: {
            color: colors.textSecondary,
            callback: options.yAxisFormat || null
          }
        }
      }
    }
  };

  return new Chart(canvas, config);
}

/**
 * Create radar/spider chart for multi-metric comparison
 * @param {HTMLCanvasElement} canvas - Canvas element
 * @param {Array} labels - Metric names (axes)
 * @param {Array} datasets - Array of {label, data} objects
 * @param {Object} options - Additional options
 */
function createRadarChart(canvas, labels, datasets, options = {}) {
  const colors = getThemeColors();
  const palette = generateColorPalette(datasets.length);

  const config = {
    type: 'radar',
    data: {
      labels: labels,
      datasets: datasets.map((dataset, i) => ({
        label: dataset.label,
        data: dataset.data,
        backgroundColor: palette[i] + '40', // 40 = ~25% opacity
        borderColor: palette[i],
        borderWidth: 2,
        pointBackgroundColor: palette[i],
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: palette[i],
        pointRadius: 4,
        pointHoverRadius: 6
      }))
    },
    options: {
      ...baseChartConfig,
      plugins: {
        legend: {
          display: true,
          position: 'top',
          labels: {
            color: colors.textPrimary,
            padding: 15,
            font: {
              size: 12
            }
          }
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          callbacks: {
            label: function(context) {
              let label = context.dataset.label || '';
              if (label) {
                label += ': ';
              }
              if (options.formatValue) {
                label += options.formatValue(context.parsed.r);
              } else {
                label += context.parsed.r;
              }
              return label;
            }
          }
        }
      },
      scales: {
        r: {
          beginAtZero: true,
          min: options.min || 0,
          max: options.max || undefined,
          ticks: {
            color: colors.textSecondary,
            backdropColor: 'transparent',
            callback: options.tickFormat || null,
            stepSize: options.stepSize || undefined
          },
          grid: {
            color: colors.gridLines
          },
          pointLabels: {
            color: colors.textPrimary,
            font: {
              size: 12,
              weight: '500'
            }
          }
        }
      }
    }
  };

  return new Chart(canvas, config);
}

/**
 * Create line chart for temporal/sequential data
 * @param {HTMLCanvasElement} canvas - Canvas element
 * @param {Array} labels - X-axis labels (typically years/dates)
 * @param {Array} datasets - Array of {label, data} objects
 * @param {Object} options - Additional options
 */
function createLineChart(canvas, labels, datasets, options = {}) {
  const colors = getThemeColors();
  const palette = generateColorPalette(datasets.length);

  const config = {
    type: 'line',
    data: {
      labels: labels,
      datasets: datasets.map((dataset, i) => ({
        label: dataset.label,
        data: dataset.data,
        borderColor: palette[i],
        backgroundColor: palette[i] + '20',
        borderWidth: 2,
        tension: 0.4, // Smooth curves
        fill: options.fill !== false,
        pointRadius: 4,
        pointHoverRadius: 6,
        pointBackgroundColor: palette[i],
        pointBorderColor: '#fff',
        pointBorderWidth: 2
      }))
    },
    options: {
      ...baseChartConfig,
      plugins: {
        legend: {
          display: true,
          position: 'top',
          labels: {
            color: colors.textPrimary,
            usePointStyle: true,
            padding: 15
          }
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          mode: 'index',
          intersect: false,
          callbacks: {
            label: function(context) {
              let label = context.dataset.label || '';
              if (label) {
                label += ': ';
              }
              if (options.formatValue) {
                label += options.formatValue(context.parsed.y);
              } else {
                label += context.parsed.y;
              }
              return label;
            }
          }
        }
      },
      scales: {
        x: {
          grid: {
            color: colors.gridLines,
            display: options.showXGrid !== false
          },
          ticks: {
            color: colors.textSecondary
          }
        },
        y: {
          beginAtZero: options.beginAtZero !== false,
          grid: {
            color: colors.gridLines
          },
          ticks: {
            color: colors.textSecondary,
            callback: options.yAxisFormat || null
          }
        }
      }
    }
  };

  return new Chart(canvas, config);
}

// ==================== CHART LIFECYCLE MANAGEMENT ====================

/**
 * Chart registry to track all active charts
 * Necessary for proper cleanup and theme updates
 */
const chartRegistry = new Map();

/**
 * Register a chart instance
 * @param {string} id - Unique identifier
 * @param {Chart} chart - Chart.js instance
 */
function registerChart(id, chart) {
  chartRegistry.set(id, chart);
}

/**
 * Destroy and remove a chart
 * @param {string} id - Chart identifier
 */
function destroyChart(id) {
  const chart = chartRegistry.get(id);
  if (chart) {
    chart.destroy();
    chartRegistry.delete(id);
  }
}

/**
 * Destroy all registered charts
 * Call before theme switch or page navigation
 */
function destroyAllCharts() {
  chartRegistry.forEach(chart => chart.destroy());
  chartRegistry.clear();
}

/**
 * Update all charts with new theme colors
 * Requires recreation of all chart instances
 * @param {Function} recreateFunction - Function to recreate all charts
 */
function updateChartsTheme(recreateFunction) {
  destroyAllCharts();
  recreateFunction();
}

// ==================== USAGE EXAMPLES ====================

/*
// Sample data
const states = ['California', 'Texas', 'New York', 'Florida', 'Illinois'];
const spending = [450000, 380000, 420000, 340000, 290000];

// 1. Create a horizontal bar chart
const barCanvas = document.getElementById('barChart');
const barChart = createBarChart(barCanvas, states, spending, {
  horizontal: true,
  label: 'Federal Spending (millions)',
  formatValue: (value) => `$${(value / 1000).toFixed(1)}B`,
  yAxisFormat: (value, index) => states[index],
  showLegend: false
});
registerChart('barChart', barChart);

// 2. Create bubble chart
const bubbleCanvas = document.getElementById('bubbleChart');
const bubbleData = [
  {
    label: 'High Income States',
    data: [
      { x: 50000, y: 120, r: 30 },  // x: income, y: spending ratio, r: population
      { x: 60000, y: 150, r: 25 }
    ]
  },
  {
    label: 'Low Income States',
    data: [
      { x: 35000, y: 180, r: 15 },
      { x: 40000, y: 160, r: 20 }
    ]
  }
];
const bubbleChart = createBubbleChart(bubbleCanvas, bubbleData, {
  xLabel: 'Median Income',
  yLabel: 'Spending Ratio',
  rLabel: 'Population (millions)',
  formatX: (val) => `$${(val / 1000).toFixed(0)}K`,
  formatY: (val) => `${val}%`,
  formatR: (val) => `${val}M`
});
registerChart('bubbleChart', bubbleChart);

// 3. Create radar chart
const radarCanvas = document.getElementById('radarChart');
const metrics = ['Education', 'Healthcare', 'Infrastructure', 'Defense', 'Social Services'];
const radarData = [
  { label: 'California', data: [85, 90, 70, 60, 95] },
  { label: 'Texas', data: [75, 70, 80, 90, 60] }
];
const radarChart = createRadarChart(radarCanvas, metrics, radarData, {
  max: 100,
  formatValue: (val) => `${val}%`
});
registerChart('radarChart', radarChart);

// 4. Theme toggle
document.getElementById('themeToggle').addEventListener('click', () => {
  const currentTheme = document.documentElement.getAttribute('data-theme');
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

  document.documentElement.setAttribute('data-theme', newTheme);
  localStorage.setItem('theme', newTheme);

  // Recreate all charts with new theme
  updateChartsTheme(() => {
    // Re-run all chart creation code
    // ...
  });
});

// 5. Responsive resize handling
window.addEventListener('resize', debounce(() => {
  chartRegistry.forEach(chart => chart.resize());
}, 250));

// 6. Cleanup on page unload
window.addEventListener('beforeunload', destroyAllCharts);
*/

// ==================== REQUIRED CSS ====================

/*
:root {
  --chart-primary: #0ea5e9;
  --chart-secondary: #8b5cf6;
  --chart-success: #10b981;
  --chart-danger: #ef4444;
  --chart-warning: #f59e0b;
  --chart-info: #06b6d4;
  --text-primary: #1f2937;
  --text-secondary: #6b7280;
  --grid-lines: #e5e7eb;
  --bg-primary: #ffffff;
}

[data-theme="dark"] {
  --chart-primary: #38bdf8;
  --chart-secondary: #a78bfa;
  --chart-success: #34d399;
  --chart-danger: #f87171;
  --chart-warning: #fbbf24;
  --chart-info: #22d3ee;
  --text-primary: #f3f4f6;
  --text-secondary: #9ca3af;
  --grid-lines: #374151;
  --bg-primary: #111827;
}

.chart-container {
  position: relative;
  height: 400px;
  width: 100%;
}

canvas {
  max-width: 100%;
}

@media (max-width: 768px) {
  .chart-container {
    height: 300px;
  }
}
*/

// Export functions for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    createBarChart,
    createBubbleChart,
    createRadarChart,
    createLineChart,
    getThemeColors,
    generateColorPalette,
    registerChart,
    destroyChart,
    destroyAllCharts,
    updateChartsTheme
  };
}

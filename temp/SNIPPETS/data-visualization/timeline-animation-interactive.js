/**
 * Interactive Timeline Animation with Projection Capability
 *
 * Description: Complete pattern for creating animated timelines showing historical
 * progression with future projections. Includes playback controls, speed adjustment,
 * and narrative text that updates as timeline progresses. Perfect for before/after
 * advocacy journalism and temporal data storytelling.
 *
 * Use Cases:
 * - Crisis timeline visualization (hospital closures, climate events)
 * - Before/after policy impact projection
 * - Temporal progression with narrative context
 * - Interactive data-driven storytelling
 * - Educational timelines with automated playback
 *
 * Dependencies:
 * - Vanilla JavaScript (no framework required)
 * - ES6 modules support
 * - CSS3 animations
 *
 * Notes:
 * - Supports historical + projection modes with visual distinction
 * - Keyboard shortcuts (Space: play/pause, Arrow keys: step, R: reset)
 * - Configurable playback speed
 * - Scrolling event feed showing timeline progression
 * - Animated number counters with easing
 * - Fully accessible with ARIA labels and keyboard nav
 *
 * Related Snippets:
 * - See d3-force-network-visualization.js for network timeline evolution
 * - See data-transformation-utils.js for formatNumber(), debounce()
 * - See chart-js-dashboards.js for complementary data displays
 *
 * Source Attribution:
 * - Extracted from: /home/coolhand/html/datavis/healthcare_deserts/UX-TEST/layout-crisis-timeline/script.js
 * - Pattern used in: Healthcare crisis before/after projection
 * - Related: D3 temporal visualizations, scrollytelling patterns
 */

// ==================== CONFIGURATION ====================

const config = {
  // Timeline range
  startYear: 2010,
  endYear: 2028,
  currentYear: 2010,
  projectionStartYear: 2025, // Historical vs projection boundary

  // Playback settings
  speed: 1000,  // milliseconds per year
  isPlaying: false,

  // Visual theming
  colors: {
    historical: '#0ea5e9',  // Blue
    projection: '#a855f7',  // Purple
    critical: '#dc2626',    // Red
    success: '#10b981'      // Green
  },

  // Animation settings
  numberCountDuration: 800,  // ms for number animation
  eventFeedMaxItems: 10
};

// ==================== STATE MANAGEMENT ====================

class TimelineState {
  constructor(initialState = {}) {
    this.state = { ...config, ...initialState };
    this.listeners = [];
    this.animationInterval = null;
  }

  get(key) {
    return this.state[key];
  }

  set(key, value) {
    const oldValue = this.state[key];
    this.state[key] = value;
    this.notify({ [key]: value }, oldValue);
  }

  subscribe(listener) {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener);
    };
  }

  notify(changes, oldValue) {
    this.listeners.forEach(listener => listener(this.state, changes, oldValue));
  }
}

const state = new TimelineState();

// ==================== DOM ELEMENTS ====================

const elements = {
  yearSlider: document.getElementById('yearSlider'),
  currentYearDisplay: document.getElementById('currentYear'),
  playBtn: document.getElementById('playBtn'),
  resetBtn: document.getElementById('resetBtn'),
  speedSelect: document.getElementById('speedSelect'),
  skipToProjectionBtn: document.getElementById('skipToProjectionBtn'),

  timelineTitle: document.getElementById('timelineTitle'),
  timelineDescription: document.getElementById('timelineDescription'),
  timelineProgress: document.getElementById('timelineProgress'),

  statsContainer: document.getElementById('statsContainer'),
  eventsList: document.getElementById('eventsList')
};

// ==================== DATA GENERATION ====================

/**
 * Generate historical data
 * In production, replace with actual data loading from CSV/JSON
 */
function generateHistoricalData() {
  const data = {};

  // Sample historical closure rates (replace with real data)
  const closuresPerYear = {
    2010: 6, 2011: 8, 2012: 13, 2013: 18, 2014: 12,
    2015: 8, 2016: 15, 2017: 19, 2018: 14, 2019: 18,
    2020: 19, 2021: 19, 2022: 7, 2023: 5, 2024: 0
  };

  let cumulative = 0;
  for (let year = config.startYear; year <= config.projectionStartYear - 1; year++) {
    cumulative += closuresPerYear[year] || 0;
    data[year] = {
      closures: closuresPerYear[year] || 0,
      cumulative: cumulative,
      population: cumulative * 40000  // Estimated impact
    };
  }

  return data;
}

/**
 * Generate projection data for future years
 * Models accelerated crisis scenario
 */
function generateProjectionData() {
  const data = {};

  const projectedClosuresPerYear = {
    2025: 80,   // First wave
    2026: 120,  // Peak impact
    2027: 80,   // Cascade effect
    2028: 70    // Continued instability
  };

  let baselineCumulative = 181; // Historical total

  for (let year = config.projectionStartYear; year <= config.endYear; year++) {
    baselineCumulative += projectedClosuresPerYear[year];
    data[year] = {
      closures: projectedClosuresPerYear[year],
      cumulative: baselineCumulative,
      population: baselineCumulative * 40000
    };
  }

  return data;
}

const historicalData = generateHistoricalData();
const projectionData = generateProjectionData();

// ==================== NARRATIVE SYSTEM ====================

/**
 * Define narrative moments with custom titles and descriptions
 * Provides emotional context and key insights at specific years
 */
const narratives = {
  2010: {
    title: 'Crisis Begins: 2010',
    desc: 'First wave of rural hospital closures signals systemic financial distress.'
  },
  2013: {
    title: 'Acceleration: 2013',
    desc: '18 closures this year. Medicaid non-expansion states see higher rates.'
  },
  2017: {
    title: 'Peak Historical Crisis: 2017',
    desc: '19 hospitals close in one year. Communities lose emergency care and local jobs.'
  },
  2020: {
    title: 'Pandemic Stress: 2020',
    desc: '19 more closures despite COVID-19. Rural hospitals strained beyond capacity.'
  },
  2024: {
    title: 'Current State: 2024',
    desc: '181 rural hospitals closed since 2010. 600+ more at immediate risk. This is where we are today.'
  },
  2025: {
    title: 'PROJECTION: First Wave (2025)',
    desc: 'IF MEDICAID CUTS PASS: 80 hospitals close in first year. Margins collapse, closures accelerate.'
  },
  2026: {
    title: 'PROJECTION: Peak Impact (2026)',
    desc: 'IF CUTS PASS: 120 closures this year. Death spiral intensifies as neighboring hospitals fail.'
  },
  2028: {
    title: 'PROJECTION: Infrastructure Collapse (2028)',
    desc: 'IF CUTS PASS: 350+ additional closures total. Rural healthcare access collapses. Mortality rises.'
  }
};

function getNarrative(year, data, isHistorical) {
  const custom = narratives[year];

  if (custom) return custom;

  // Default narrative
  return {
    title: `${isHistorical ? 'Historical' : 'PROJECTION'}: ${year}`,
    desc: isHistorical
      ? `${data.cumulative} hospitals closed since 2010. ${data.closures} closures this year.`
      : `PROJECTED: ${data.cumulative} total closures if cuts pass. ${data.closures} this year.`
  };
}

// ==================== VISUALIZATION UPDATE ====================

function updateVisualization(year) {
  const isHistorical = year < config.projectionStartYear;
  const data = isHistorical ? historicalData : projectionData;
  const yearData = data[year];

  if (!yearData) return;

  // Update year display
  elements.currentYearDisplay.textContent = year;
  elements.yearSlider.setAttribute('aria-valuenow', year);

  // Update narrative
  const narrative = getNarrative(year, yearData, isHistorical);
  elements.timelineTitle.textContent = narrative.title;
  elements.timelineDescription.textContent = narrative.desc;

  // Update progress bar
  const progressPercent = ((year - config.startYear) / (config.endYear - config.startYear)) * 100;
  elements.timelineProgress.style.width = `${progressPercent}%`;
  elements.timelineProgress.style.background = isHistorical ? config.colors.historical : config.colors.projection;

  // Update statistics with animation
  updateStatistics(yearData, isHistorical);

  // Add event to feed if there's activity
  if (yearData.closures > 0) {
    addEvent(year, yearData.closures, isHistorical);
  }
}

// ==================== STATISTICS DISPLAY ====================

function updateStatistics(yearData, isHistorical) {
  const stats = [
    {
      id: 'historicalClosures',
      value: isHistorical ? yearData.cumulative : 181,
      label: 'Historical Closures'
    },
    {
      id: 'avgPerYear',
      value: isHistorical ? Math.round(yearData.cumulative / (state.get('currentYear') - config.startYear + 1)) : Math.round(181 / 15),
      label: 'Average Per Year'
    },
    {
      id: 'projectedClosures',
      value: isHistorical ? null : yearData.cumulative - 181,
      label: 'Additional Projected'
    },
    {
      id: 'populationImpact',
      value: yearData.population,
      label: 'Population Affected'
    }
  ];

  stats.forEach(stat => {
    const element = document.getElementById(stat.id);
    if (!element) return;

    if (stat.value === null) {
      element.textContent = '—';
    } else {
      animateNumber(element, 0, stat.value, config.numberCountDuration);
    }
  });
}

/**
 * Animate number counting up with easing
 */
function animateNumber(element, start, end, duration) {
  const startTime = performance.now();
  const diff = end - start;

  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);

    // Ease-out cubic
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = start + (diff * eased);

    element.textContent = formatNumber(current);

    if (progress < 1) {
      requestAnimationFrame(update);
    }
  }

  requestAnimationFrame(update);
}

// ==================== EVENT FEED ====================

function addEvent(year, closures, isHistorical) {
  const event = document.createElement('div');
  event.className = 'event-item';

  const yearSpan = document.createElement('span');
  yearSpan.className = 'event-year';
  yearSpan.textContent = year;

  const desc = document.createElement('p');
  desc.className = 'event-desc';

  if (isHistorical) {
    desc.textContent = `${closures} rural ${closures === 1 ? 'hospital closes' : 'hospitals close'} this year`;
  } else {
    desc.textContent = `PROJECTED: ${closures} additional closures if cuts pass`;
    event.style.borderLeftColor = config.colors.projection;
  }

  event.appendChild(yearSpan);
  event.appendChild(desc);

  // Add to top of list
  elements.eventsList.insertBefore(event, elements.eventsList.firstChild);

  // Keep only last N events
  while (elements.eventsList.children.length > config.eventFeedMaxItems) {
    elements.eventsList.removeChild(elements.eventsList.lastChild);
  }

  // Scroll to top
  elements.eventsList.scrollTop = 0;
}

function clearEvents() {
  elements.eventsList.innerHTML = `
    <div class="event-item">
      <span class="event-year">${config.startYear}</span>
      <p class="event-desc">Starting point: System intact but financially stressed</p>
    </div>
  `;
}

// ==================== PLAYBACK CONTROLS ====================

function togglePlayback() {
  if (state.get('isPlaying')) {
    stopAnimation();
  } else {
    startAnimation();
  }
}

function startAnimation() {
  const currentYear = state.get('currentYear');

  // Reset if at end
  if (currentYear >= config.endYear) {
    state.set('currentYear', config.startYear);
    elements.yearSlider.value = config.startYear;
    clearEvents();
  }

  state.set('isPlaying', true);
  elements.playBtn.innerHTML = '<span class="btn-icon">⏸</span> Pause';
  elements.playBtn.setAttribute('aria-label', 'Pause timeline animation');

  const speed = state.get('speed');

  state.animationInterval = setInterval(() => {
    const year = state.get('currentYear');

    if (year >= config.endYear) {
      stopAnimation();
      return;
    }

    const nextYear = year + 1;
    state.set('currentYear', nextYear);
    elements.yearSlider.value = nextYear;
    updateVisualization(nextYear);
  }, speed);
}

function stopAnimation() {
  if (state.animationInterval) {
    clearInterval(state.animationInterval);
    state.animationInterval = null;
  }

  state.set('isPlaying', false);
  elements.playBtn.innerHTML = '<span class="btn-icon">▶</span> Play Timeline';
  elements.playBtn.setAttribute('aria-label', 'Play timeline animation');
}

function resetTimeline() {
  stopAnimation();
  state.set('currentYear', config.startYear);
  elements.yearSlider.value = config.startYear;
  clearEvents();
  updateVisualization(config.startYear);
}

function skipToProjection() {
  stopAnimation();
  state.set('currentYear', config.projectionStartYear);
  elements.yearSlider.value = config.projectionStartYear;
  clearEvents();
  updateVisualization(config.projectionStartYear);
}

// ==================== EVENT HANDLERS ====================

function handleSliderChange(event) {
  const year = parseInt(event.target.value);
  state.set('currentYear', year);
  updateVisualization(year);

  // Stop playback when user manually adjusts
  if (state.get('isPlaying')) {
    stopAnimation();
  }
}

function handleSpeedChange(event) {
  const speed = parseInt(event.target.value);
  state.set('speed', speed);

  // Restart with new speed if playing
  if (state.get('isPlaying')) {
    stopAnimation();
    startAnimation();
  }
}

function handleKeyboard(event) {
  // Space: play/pause
  if (event.code === 'Space' && event.target.tagName !== 'INPUT' && event.target.tagName !== 'SELECT') {
    event.preventDefault();
    togglePlayback();
  }

  // Arrow left/right: step
  if (event.code === 'ArrowLeft') {
    const year = Math.max(config.startYear, state.get('currentYear') - 1);
    state.set('currentYear', year);
    elements.yearSlider.value = year;
    updateVisualization(year);
  }

  if (event.code === 'ArrowRight') {
    const year = Math.min(config.endYear, state.get('currentYear') + 1);
    state.set('currentYear', year);
    elements.yearSlider.value = year;
    updateVisualization(year);
  }

  // R: reset
  if (event.code === 'KeyR') {
    resetTimeline();
  }
}

// ==================== UTILITIES ====================

function formatNumber(num) {
  if (num === null || num === undefined || isNaN(num)) return '—';
  return Math.round(num).toLocaleString('en-US');
}

function debounce(func, wait) {
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

// ==================== INITIALIZATION ====================

function init() {
  // Set up event listeners
  elements.yearSlider.addEventListener('input', debounce(handleSliderChange, 50));
  elements.playBtn.addEventListener('click', togglePlayback);
  elements.resetBtn.addEventListener('click', resetTimeline);
  elements.speedSelect.addEventListener('change', handleSpeedChange);
  elements.skipToProjectionBtn.addEventListener('click', skipToProjection);
  document.addEventListener('keydown', handleKeyboard);

  // Initial render
  updateVisualization(config.startYear);

  console.log('Timeline initialized. Keyboard shortcuts:');
  console.log('  Space: Play/Pause');
  console.log('  Arrow Left/Right: Step backward/forward');
  console.log('  R: Reset');
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}

// ==================== REQUIRED HTML STRUCTURE ====================

/*
<div id="timeline-container">
  <div id="timelineHeader">
    <h1 id="timelineTitle">Timeline Title</h1>
    <p id="timelineDescription">Description text</p>
  </div>

  <div id="timelineControls">
    <button id="playBtn" aria-label="Play timeline animation">
      <span class="btn-icon">▶</span> Play Timeline
    </button>
    <button id="resetBtn" aria-label="Reset to beginning">Reset</button>
    <button id="skipToProjectionBtn">Skip to Projection</button>

    <label for="speedSelect">Speed:</label>
    <select id="speedSelect">
      <option value="2000">Slow</option>
      <option value="1000" selected>Normal</option>
      <option value="500">Fast</option>
    </select>
  </div>

  <div id="yearSliderContainer">
    <input type="range" id="yearSlider" min="2010" max="2028" value="2010" aria-label="Select year">
    <div id="currentYear">2010</div>
  </div>

  <div id="timelineProgress"></div>

  <div id="statsContainer">
    <div class="stat-box">
      <div id="historicalClosures" class="stat-value">—</div>
      <div class="stat-label">Historical Closures</div>
    </div>
    <!-- More stat boxes... -->
  </div>

  <div id="eventsList"></div>
</div>
*/

// ==================== REQUIRED CSS ====================

/*
#timeline-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

#timelineProgress {
  height: 6px;
  background: #0ea5e9;
  transition: width 0.3s ease, background 0.3s ease;
  border-radius: 3px;
}

.event-item {
  border-left: 3px solid #0ea5e9;
  padding: 0.75rem 1rem;
  margin-bottom: 0.5rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
}

.event-year {
  font-weight: 700;
  color: #0ea5e9;
  font-size: 1.1em;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.btn-icon {
  display: inline-block;
  width: 1em;
  text-align: center;
}
*/

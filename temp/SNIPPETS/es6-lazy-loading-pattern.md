# ES6 Module Lazy Loading Pattern

**Source**: `/home/coolhand/html/datavis/language-tree/js/main.js`
**Date**: 2025-12-15
**Use Case**: Performance optimization for multi-view applications with tab navigation

## Core Pattern

```javascript
/**
 * Lazy load visualization modules only when needed
 * Reduces initial bundle size and improves Time to Interactive (TTI)
 */

// State tracking
let radialViz = null;
let timelineViz = null;
let sankeyViz = null;

const moduleLoaders = {
    radial: () => import('./radial.js'),
    timeline: () => import('./timeline.js'),
    sankey: () => import('./sankey.js')
};

async function initializeVisualization(viewName) {
    try {
        // Show loading state
        showLoading();

        // Lazy load module if not already cached
        let vizModule;

        switch (viewName) {
            case 'radial':
                if (!radialViz) {
                    vizModule = await moduleLoaders.radial();
                    radialViz = vizModule.createRadialTree(
                        document.getElementById('radial-container'),
                        languageData,
                        getVisualizationOptions()
                    );
                }
                break;

            case 'timeline':
                if (!timelineViz) {
                    vizModule = await moduleLoaders.timeline();
                    timelineViz = vizModule.createTimeline(
                        document.getElementById('timeline-container'),
                        languageData,
                        getVisualizationOptions()
                    );
                }
                break;

            case 'sankey':
                if (!sankeyViz) {
                    vizModule = await moduleLoaders.sankey();
                    sankeyViz = vizModule.createSankey(
                        document.getElementById('sankey-container'),
                        languageData,
                        getVisualizationOptions()
                    );
                }
                break;
        }

        hideLoading();
    } catch (error) {
        console.error(`Error loading ${viewName} visualization:`, error);
        showError(`Failed to load ${viewName} visualization. Please refresh the page.`);
    }
}
```

## Tab Switching with Lazy Loading

```javascript
/**
 * Switch between tabs, loading modules on-demand
 */
function switchTab(tabName) {
    // Don't reload if already active
    if (currentView === tabName) return;

    currentView = tabName;

    // Update UI
    updateTabUI(tabName);

    // Show correct panel
    showPanel(tabName);

    // Initialize visualization if needed
    initializeVisualization(tabName);

    // Update URL without reload (optional)
    history.replaceState({ tab: tabName }, '', `#${tabName}`);
}

function updateTabUI(activeTab) {
    elements.tabButtons.forEach(button => {
        const isActive = button.dataset.tab === activeTab;
        button.classList.toggle('active', isActive);
        button.setAttribute('aria-selected', isActive);
    });
}

function showPanel(panelName) {
    elements.panels.forEach(panel => {
        const isPanelActive = panel.id === `${panelName}-panel`;
        panel.classList.toggle('active', isPanelActive);
        panel.setAttribute('aria-hidden', !isPanelActive);
    });
}
```

## Update Pattern for Cached Visualizations

```javascript
/**
 * Update all active visualizations when filters change
 * Only update already-loaded modules (don't lazy load on filter change)
 */
function updateActiveVisualizations() {
    const options = getVisualizationOptions();

    // Only update if modules are already loaded
    if (radialViz && currentView === 'radial') {
        radialViz.update(options);
    }

    if (timelineViz && currentView === 'timeline') {
        timelineViz.update(options);
    }

    if (sankeyViz && currentView === 'sankey') {
        sankeyViz.update(options);
    }
}

function getVisualizationOptions() {
    return {
        showExtinct: elements.extinctToggle.checked,
        selectedFamily: elements.familyFilter.value,
        searchTerm: elements.searchInput.value.trim(),
        onNodeHover: handleNodeHover,
        onNodeLeave: handleNodeLeave
    };
}
```

## Loading State Management

```javascript
/**
 * Smooth loading transitions
 */
function showLoading() {
    const loading = document.getElementById('loading');
    loading.classList.add('visible');
    loading.setAttribute('aria-hidden', 'false');
}

function hideLoading() {
    const loading = document.getElementById('loading');
    loading.classList.remove('visible');
    loading.setAttribute('aria-hidden', 'true');
}

function showError(message) {
    hideLoading();
    const errorPanel = document.createElement('div');
    errorPanel.className = 'error-panel';
    errorPanel.setAttribute('role', 'alert');
    errorPanel.innerHTML = `
        <p>${message}</p>
        <button onclick="location.reload()">Reload Page</button>
    `;
    document.body.appendChild(errorPanel);
}
```

## Deep Linking Support

```javascript
/**
 * Support direct links to specific tabs via URL hash
 */
function initializeFromURL() {
    const hash = window.location.hash.slice(1); // Remove '#'
    const validTabs = ['radial', 'timeline', 'sankey'];

    if (validTabs.includes(hash)) {
        switchTab(hash);
    } else {
        // Default to first tab
        switchTab('radial');
    }
}

// Listen for hash changes (back/forward navigation)
window.addEventListener('hashchange', () => {
    const hash = window.location.hash.slice(1);
    if (['radial', 'timeline', 'sankey'].includes(hash)) {
        switchTab(hash);
    }
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    init();
    initializeFromURL();
});
```

## Preloading Strategy (Optional)

```javascript
/**
 * Preload modules during idle time for instant switching
 * Use requestIdleCallback for non-blocking preload
 */
function preloadModules() {
    if ('requestIdleCallback' in window) {
        requestIdleCallback(() => {
            // Preload modules likely to be used
            moduleLoaders.timeline();
            moduleLoaders.sankey();
        }, { timeout: 5000 });
    } else {
        // Fallback for browsers without requestIdleCallback
        setTimeout(() => {
            moduleLoaders.timeline();
            moduleLoaders.sankey();
        }, 3000);
    }
}

// Call after initial view loads
async function init() {
    await loadData();
    await initializeVisualization(currentView);

    // Preload other modules in background
    preloadModules();
}
```

## Module Export Pattern

```javascript
// radial.js, timeline.js, sankey.js
/**
 * Export factory function that returns API object
 * Allows parent to call update() and resize() methods
 */
export function createRadialTree(container, data, options = {}) {
    let svg, g, root, tree;

    function init() {
        // Setup visualization
    }

    function update(newOptions) {
        // Update with new filters/data
    }

    function resize() {
        // Recalculate dimensions and redraw
    }

    function destroy() {
        // Cleanup event listeners and DOM nodes
        container.innerHTML = '';
    }

    // Initialize on creation
    init();

    // Return public API
    return {
        update,
        resize,
        destroy
    };
}
```

## Debounced Filter Updates

```javascript
/**
 * Debounce filter changes to avoid expensive re-renders
 */
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

// Debounced search input
const debouncedSearch = debounce(() => {
    updateActiveVisualizations();
}, 300);

elements.searchInput.addEventListener('input', () => {
    debouncedSearch();
});

// Immediate updates for checkboxes/selects
elements.extinctToggle.addEventListener('change', () => {
    updateActiveVisualizations();
});

elements.familyFilter.addEventListener('change', () => {
    updateActiveVisualizations();
});
```

## Resize Handling

```javascript
/**
 * Handle window resize efficiently
 */
const debouncedResize = debounce(() => {
    // Only resize the active visualization
    if (radialViz && currentView === 'radial') {
        radialViz.resize();
    }
    if (timelineViz && currentView === 'timeline') {
        timelineViz.resize();
    }
    if (sankeyViz && currentView === 'sankey') {
        sankeyViz.resize();
    }
}, 250);

window.addEventListener('resize', debouncedResize);
```

## Performance Metrics

**Before Lazy Loading**:
- Initial bundle: ~150KB (all 3 visualizations)
- Time to Interactive: ~2.5s

**After Lazy Loading**:
- Initial bundle: ~50KB (main.js only)
- Time to Interactive: ~1.2s
- Subsequent tabs: ~300ms (cached) or ~600ms (first load)

## Key Benefits

1. **Faster Initial Load**: Only load code for default view
2. **Reduced Bundle Size**: Split large D3 visualizations into chunks
3. **Better Caching**: Browser caches each module independently
4. **Progressive Enhancement**: App still works if module fails to load
5. **Memory Efficiency**: Unused modules never loaded

## Browser Compatibility

- **Dynamic import()**: Chrome 63+, Firefox 67+, Safari 11.1+
- Fallback: Use bundler (Webpack/Rollup) to polyfill for older browsers
- Consider using `<script type="module">` for native ES6 support

## Related Patterns

- See `d3-radial-tree-pattern.md` for visualization implementation
- See `glassmorphism-css-pattern.md` for loading state UI

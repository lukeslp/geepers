# Vanilla JavaScript State Management Pattern

**Language**: JavaScript (Vanilla)
**Pattern**: Centralized State Object
**Use Case**: Single-page search interfaces, complex UI state
**Source**: COCA Diachronica frontend (2025-12-17)

## Implementation

```javascript
// Centralized state object
const state = {
    currentQuery: '',
    currentPeriod: 'contemporary',
    searchType: 'word',
    results: [],
    offset: 0,
    limit: 20,
    totalResults: 0
};

// Configuration mapping
const periodMapping = {
    'old-english': { historical: 'old_english', label: 'Old English' },
    'middle-english': { historical: 'middle_english', label: 'Middle English' },
    'early-modern': { historical: 'early_modern_english', label: 'Early Modern English' },
    'late-modern': { historical: 'late_modern_english', label: 'Late Modern English' },
    'contemporary': { genre: '', label: 'Contemporary (COCA)' }
};

// DOM element references (cached)
const searchForm = document.getElementById('searchForm');
const searchInput = document.getElementById('searchInput');
const resultsSection = document.getElementById('results');
const resultsContainer = document.getElementById('resultsContainer');

// Event handlers update state
document.querySelectorAll('.timeline-period').forEach(period => {
    period.addEventListener('click', () => {
        // Update visual state
        document.querySelectorAll('.timeline-period').forEach(p =>
            p.classList.remove('active'));
        period.classList.add('active');

        // Update application state
        state.currentPeriod = period.dataset.period;

        // Trigger re-render if needed
        if (state.currentQuery) performSearch(state.currentQuery);
    });
});

// State-driven rendering
function performSearch(query) {
    state.currentQuery = query;
    state.offset = 0; // Reset pagination

    // Use state to build API request
    const apiParams = buildApiParams(state);

    // Fetch and update state
    fetchResults(apiParams).then(data => {
        state.results = data.results;
        state.totalResults = data.total;
        renderResults();
    });
}

function renderResults() {
    // Render based on current state
    resultsContainer.textContent = ''; // Clear safely

    state.results.forEach(result => {
        const element = createResultElement(result);
        resultsContainer.appendChild(element);
    });

    updatePaginationUI();
}
```

## Key Features

1. **Single source of truth**: All application state in one object
2. **Cached DOM references**: Element lookups happen once at initialization
3. **Declarative event handlers**: Clear mapping between UI actions and state changes
4. **State-driven rendering**: UI reflects current state
5. **Configuration objects**: Easy to extend and maintain

## Advantages Over Framework State

- No bundle size overhead
- No build step required
- Easier debugging (state object visible in console)
- Direct DOM manipulation for performance
- Perfect for small to medium interfaces

## Best Practices

```javascript
// 1. Initialize state with sensible defaults
const state = {
    currentQuery: '',  // Empty string rather than null
    offset: 0,         // Start at beginning
    limit: 20          // Reasonable page size
};

// 2. Cache DOM queries to avoid repeated lookups
const els = {
    form: document.getElementById('searchForm'),
    input: document.getElementById('searchInput'),
    results: document.getElementById('results')
};

// 3. Use data attributes for configuration
<button data-word="run" data-period="old-english">run</button>

btn.addEventListener('click', () => {
    state.currentQuery = btn.dataset.word;
    state.currentPeriod = btn.dataset.period;
});

// 4. Separate concerns
function updateState(changes) {
    Object.assign(state, changes);
}

function render() {
    // Pure rendering based on state
}

function handleSearch(query) {
    updateState({ currentQuery: query, offset: 0 });
    fetchData().then(render);
}
```

## XSS Prevention

```javascript
// Use textContent instead of innerHTML
element.textContent = state.currentQuery; // Safe

// Or use DOM methods
const span = document.createElement('span');
span.textContent = userInput;
container.appendChild(span);

// Clear containers safely
container.textContent = ''; // Better than innerHTML = ''
container.replaceChildren(); // Modern alternative
```

## Related Patterns

- Event delegation for dynamic elements
- Debouncing for search inputs
- Infinite scroll pagination
- Loading state management

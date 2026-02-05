# Swiss Design Timeline Component

**Language**: HTML/CSS
**Pattern**: Interactive Timeline Navigation
**Use Case**: Historical period selection, chronological data filtering
**Source**: COCA Diachronica frontend (2025-12-17)

## HTML Structure

```html
<section class="timeline-container">
    <h2 class="timeline-title">Select Historical Period</h2>
    <div class="timeline">
        <button class="timeline-period" data-period="old-english">
            <span class="period-label">Old English</span>
            <span class="period-range">450-1150</span>
        </button>
        <button class="timeline-period" data-period="middle-english">
            <span class="period-label">Middle English</span>
            <span class="period-range">1150-1500</span>
        </button>
        <button class="timeline-period" data-period="early-modern">
            <span class="period-label">Early Modern</span>
            <span class="period-range">1500-1800</span>
        </button>
        <button class="timeline-period" data-period="late-modern">
            <span class="period-label">Late Modern</span>
            <span class="period-range">1800-1945</span>
        </button>
        <button class="timeline-period active" data-period="contemporary">
            <span class="period-label">Contemporary</span>
            <span class="period-range">1990-2024</span>
        </button>
    </div>
</section>
```

## CSS (Swiss Design System)

```css
/* Timeline Container */
.timeline-container {
    margin-bottom: 32px;
    background: white;
    border: 1px solid #000;
    padding: 24px;
}

.timeline-title {
    font-size: 16px;
    font-weight: 700;
    margin: 0 0 16px 0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Timeline Layout */
.timeline {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 8px;
}

/* Period Buttons */
.timeline-period {
    background: white;
    border: 1px solid #000;
    padding: 12px 16px;
    cursor: pointer;
    transition: all 0.2s ease;
    font-family: inherit;
    text-align: left;
}

.timeline-period:hover {
    background: #f5f5f5;
}

.timeline-period.active {
    background: #000;
    color: #fff;
}

.timeline-period.active:hover {
    background: #333;
}

/* Period Labels */
.period-label {
    display: block;
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 4px;
}

.period-range {
    display: block;
    font-size: 12px;
    opacity: 0.7;
    font-family: 'Courier New', monospace;
}

.timeline-period.active .period-range {
    opacity: 0.9;
}

/* Responsive Design */
@media (max-width: 768px) {
    .timeline {
        grid-template-columns: 1fr;
    }

    .timeline-period {
        padding: 16px;
    }
}
```

## JavaScript Interaction

```javascript
document.querySelectorAll('.timeline-period').forEach(period => {
    period.addEventListener('click', () => {
        // Remove active state from all periods
        document.querySelectorAll('.timeline-period').forEach(p =>
            p.classList.remove('active'));

        // Add active state to clicked period
        period.classList.add('active');

        // Get selected period
        const selectedPeriod = period.dataset.period;

        // Trigger data update
        updateData(selectedPeriod);
    });
});
```

## Swiss Design Principles Applied

1. **Black and white color scheme**: High contrast, no decorative colors
2. **8px grid system**: All spacing uses 8px increments (8, 16, 24, 32)
3. **Clear typography hierarchy**: Bold labels, lighter metadata
4. **Minimal decoration**: Solid borders, no shadows or gradients
5. **Functional layout**: Grid system for responsive adaptation
6. **Active state clarity**: Inverted colors for selected state

## Accessibility Features

```html
<!-- Add ARIA labels -->
<button class="timeline-period"
        data-period="old-english"
        aria-pressed="false"
        role="button">
    <span class="period-label">Old English</span>
    <span class="period-range">450-1150</span>
</button>

<script>
// Update ARIA state
period.addEventListener('click', () => {
    document.querySelectorAll('.timeline-period').forEach(p =>
        p.setAttribute('aria-pressed', 'false'));
    period.setAttribute('aria-pressed', 'true');
});
</script>
```

## Keyboard Navigation

```javascript
// Add keyboard support
document.querySelectorAll('.timeline-period').forEach((period, index, periods) => {
    period.addEventListener('keydown', (e) => {
        let nextIndex;

        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
            e.preventDefault();
            nextIndex = (index + 1) % periods.length;
            periods[nextIndex].focus();
        } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
            e.preventDefault();
            nextIndex = (index - 1 + periods.length) % periods.length;
            periods[nextIndex].focus();
        } else if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            period.click();
        }
    });
});
```

## Variations

```css
/* Compact horizontal timeline */
.timeline-horizontal {
    display: flex;
    overflow-x: auto;
    gap: 8px;
}

.timeline-horizontal .timeline-period {
    flex: 0 0 auto;
    min-width: 120px;
}

/* Vertical timeline with connector */
.timeline-vertical {
    display: flex;
    flex-direction: column;
    gap: 0;
}

.timeline-vertical .timeline-period {
    border-top: none;
    position: relative;
}

.timeline-vertical .timeline-period:first-child {
    border-top: 1px solid #000;
}

.timeline-vertical .timeline-period::before {
    content: '';
    position: absolute;
    left: -16px;
    top: 50%;
    width: 8px;
    height: 8px;
    background: #000;
    border-radius: 50%;
}
```

## Related Patterns

- Tab navigation
- Segmented controls
- Breadcrumb navigation
- Stepper components

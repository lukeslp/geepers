# Okabe-Ito Colorblind-Safe Palette as CSS Variables

**Category**: accessibility / design-tokens
**Source**: html/datavis/shared/design-tokens.css + billions/styles.css (2026-03-08)
**Tags**: a11y, colorblind, wcag, css-variables, okabe-ito, data-visualization

## Problem

Most default data visualization palettes (D3 schemeSet1, schemeCategory10, Chart.js defaults) fail for users with deuteranopia or protanopia — the most common forms of color vision deficiency. Okabe-Ito is the de facto standard for accessible data palettes.

## Palette

The Okabe-Ito palette (2008, Nature Methods) is distinguishable by all common types of color vision deficiency including deuteranopia, protanopia, and tritanopia.

```css
:root {
  /* Okabe-Ito colorblind-safe palette */
  --ds-blue:       #0173b2;  /* primary accent, country */
  --ds-orange:     #de8f05;  /* individual / person */
  --ds-green:      #029e73;
  --ds-vermillion: #d55e00;
  --ds-pink:       #cc78bc;  /* company */
  --ds-brown:      #ca9161;
  --ds-yellow:     #ece133;
  --ds-light-blue: #56b4e9;
  /* Black (#000000) is also part of the original 8-color palette */
}
```

## Usage in data visualization

```css
/* Semantic aliases for a specific project */
:root {
  --color-country:    var(--ds-blue);       /* #0173b2 */
  --color-individual: var(--ds-orange);     /* #de8f05 */
  --color-company:    var(--ds-pink);       /* #cc78bc */
}

.entity-dot-country    { background: var(--color-country); }
.entity-dot-individual { background: var(--color-individual); }
.entity-dot-company    { background: var(--color-company); }

.type-country    { color: var(--color-country); }
.type-individual { color: var(--color-individual); }
.type-company    { color: var(--color-company); }
```

## D3.js usage

```javascript
// Replace d3.schemeSet2 or schemeCategory10 with Okabe-Ito
const okabeIto = [
    '#0173b2', '#de8f05', '#029e73', '#d55e00',
    '#cc78bc', '#ca9161', '#ece133', '#56b4e9'
];
const colorScale = d3.scaleOrdinal(okabeIto);
```

## Forced-colors (high contrast) safety

When using these as fill/stroke colors in SVG or as background-color in HTML, add a forced-colors block so Windows High Contrast mode users don't lose all category encoding:

```css
@media (forced-colors: active) {
  .entity-dot { forced-color-adjust: none; } /* preserve dot color */
  /* Or add border/shape encoding as fallback */
  tr.entity-country    { border-left: 3px solid currentColor; }
  tr.entity-individual { border-left: 3px solid currentColor; }
  tr.entity-company    { border-left: 3px solid currentColor; }
}
```

## Notes

- Original paper: Bang Wong, "Points of view: Color blindness", Nature Methods 8, 441 (2011)
- Blue (#0173b2) passes WCAG AA contrast on white (4.71:1) — suitable for text
- Orange (#de8f05) passes WCAG AA on white (3.49:1) at large text sizes only; not for body text
- Always supplement color with shape, pattern, or label encoding for full accessibility

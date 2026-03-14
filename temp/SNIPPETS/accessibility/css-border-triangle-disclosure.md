# CSS Border Triangle — Screen Reader Neutral Disclosure Indicator

**Source**: oss-safeguard-ux / safeguard.html — 2026-03-07
**Stack**: CSS, `<details>`/`<summary>`

## Problem

Using Unicode characters (▶ U+25B6, ▼ U+25BC) as disclosure triangles inside
`<summary>` elements causes screen readers to announce the character name
("black right-pointing triangle") to users, adding noise to otherwise clean
headings. `content: "\25B6"` in `::before`/`::after` pseudo-elements has the
same problem on some AT.

## Pattern

Use a zero-content pseudo-element styled with CSS borders to create a purely
visual triangle that AT ignores entirely.

```css
/* Hide the native marker (WebKit) */
summary::-webkit-details-marker { display: none; }

/* CSS border triangle — no text content, screen reader neutral */
summary::before {
  content: '';           /* empty string — AT skips this */
  display: inline-block;
  width: 0;
  height: 0;
  border-style: solid;
  /* right-pointing triangle: top/bottom arms, left hypotenuse */
  border-width: 4px 0 4px 5px;
  border-color: transparent transparent transparent currentColor;
  transition: transform 0.15s;
  flex-shrink: 0;
}

/* Rotate 90° when open — points downward */
details[open] summary::before {
  transform: rotate(90deg);
}
```

## Full `<details>` Example

```html
<details class="sg-policy-wrap">
  <summary>Policy</summary>
  <p>Policy content here.</p>
</details>
```

```css
.sg-policy-wrap summary {
  display: flex;
  align-items: center;
  gap: 5px;
  list-style: none;       /* also suppresses Firefox marker */
  cursor: pointer;
}
.sg-policy-wrap summary::-webkit-details-marker { display: none; }
.sg-policy-wrap summary::before {
  content: '';
  display: inline-block;
  width: 0; height: 0;
  border-style: solid;
  border-width: 4px 0 4px 5px;
  border-color: transparent transparent transparent currentColor;
  transition: transform 0.15s;
  flex-shrink: 0;
}
.sg-policy-wrap[open] summary::before {
  transform: rotate(90deg);
}
```

## Why This Works

- `content: ''` — an empty string in CSS `content` is not announced by AT.
  A non-empty string (including `content: "\25B6"`) IS announced.
- `border-color: transparent transparent transparent currentColor` — the left
  border forms the hypotenuse of a right-pointing triangle using the CSS
  box model. `currentColor` inherits from the element's text color.
- `transform: rotate(90deg)` — rotating the right-pointing triangle 90° produces
  a downward-pointing triangle when the disclosure is open.

## Triangle Size Reference

| border-width | Triangle size |
|---|---|
| `3px 0 3px 4px` | 8×6px (small) |
| `4px 0 4px 5px` | 10×8px (default) |
| `5px 0 5px 6px` | 12×10px (large) |

Adjust `border-width` values to resize. Keep the `0` values on top and bottom arms.

## Notes

- `list-style: none` on the `<summary>` also suppresses the native marker in
  Firefox but does not affect WebKit/Blink — use both rules.
- `flex-shrink: 0` prevents the triangle from collapsing when the summary
  uses `display: flex` for label layout.
- This pattern works equally well for custom accordion/tree components that
  don't use `<details>` — apply the same `::before` to the toggle button.

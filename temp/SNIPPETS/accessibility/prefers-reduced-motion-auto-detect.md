# prefers-reduced-motion — OS Auto-Detect with localStorage Persistence

**Source**: oss-safeguard-ux / safeguard.html — 2026-03-07
**Stack**: Vanilla JS, localStorage

## Problem

A page has a "Reduce motion" toggle stored in localStorage, but first-time
visitors who have already set the OS-level accessibility preference see full
animations. The toggle should auto-initialise from the OS preference on the
first visit, then stay out of the way once the user has made an explicit choice.

## Pattern

Read `localStorage` first. If no stored a11y preferences exist, check
`window.matchMedia('(prefers-reduced-motion: reduce)')` and apply silently
(do not overwrite storage — keep it "first visit only").

```js
const A11Y_KEY = 'sg-a11y';

function loadA11y() {
  try {
    const s = JSON.parse(localStorage.getItem(A11Y_KEY) || '{}');
    if (s.fontSize) setFontSize(s.fontSize, false);
    if (s.reducedMotion !== undefined) setMotion(s.reducedMotion, false);
  } catch {}
}

function saveA11y() {
  localStorage.setItem(A11Y_KEY, JSON.stringify({
    fontSize: document.documentElement.dataset.fontSize || 'md',
    reducedMotion: document.documentElement.dataset.reducedMotion === 'true'
  }));
}

function setMotion(val, save = true) {
  document.documentElement.dataset.reducedMotion = val ? 'true' : 'false';
  const c = document.getElementById('motionCheck');
  if (c) c.checked = !!val;
  if (save) saveA11y();
}

// Load stored prefs first
loadA11y();

// Auto-detect OS setting only when nothing is stored yet
if (!localStorage.getItem(A11Y_KEY)) {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    setMotion(true, false); // apply but don't save — keeps "first visit only" semantics
  }
}
```

## CSS — honour the data attribute

```css
/* Applied by setMotion() to document.documentElement */
[data-reduced-motion="true"] *,
[data-reduced-motion="true"] *::before,
[data-reduced-motion="true"] *::after {
  animation-duration: 0.01ms !important;
  animation-iteration-count: 1 !important;
  transition-duration: 0.01ms !important;
  scroll-behavior: auto !important;
}
```

## HTML — expose the toggle

```html
<div class="sg-popover-row">
  <label for="motionCheck">Reduce motion</label>
  <input type="checkbox" id="motionCheck">
</div>
```

## Key Rules

- `loadA11y()` runs before the OS check so explicit user prefs always win.
- The OS auto-detect uses `setMotion(true, false)` — the `false` means "do not
  persist"; only user-driven changes persist.
- Gate on `!localStorage.getItem(A11Y_KEY)` so the auto-detect fires exactly
  once (first visit) and never overrides a returning user's choice.
- Wire the checkbox `change` event to call `setMotion(e.target.checked)` (with
  save = true, the default) so manual changes persist immediately.

## Notes

- Works identically for `prefers-color-scheme` — same guard pattern applies.
- `data-reduced-motion` on `<html>` is faster than adding/removing a class and
  avoids FOUC when CSS transitions are scoped to `[data-reduced-motion="true"]`.
- The `!important` overrides in CSS are intentional — motion suppression must
  win over component-level transitions.

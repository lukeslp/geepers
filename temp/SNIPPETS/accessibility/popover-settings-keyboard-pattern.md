# Accessible Settings Popover — Keyboard + Focus Pattern

**Source**: oss-safeguard-ux / safeguard.html — 2026-03-07
**Stack**: Vanilla JS, no framework

## Problem

A settings popover (font size, theme toggle, reduced motion) triggered by a gear
button needs to:

- Announce open/closed state to AT via `aria-expanded`
- Move focus inside on open so keyboard users can reach the controls
- Return focus to trigger on close (Escape or outside click)
- Not claim to be a `role="dialog"` unless a proper focus trap is implemented

## Pattern

### HTML

```html
<div class="sg-settings-wrap">
  <button
    id="settingsBtn"
    class="sg-gear"
    aria-controls="settingsPopover"
    aria-expanded="false"
    aria-label="Settings"
  >
    &#9881;
  </button>
  <!-- No role="dialog" unless full focus trap is implemented -->
  <div id="settingsPopover" class="sg-popover" aria-label="Settings">
    <div class="sg-popover-row">
      <span>Theme</span>
      <button class="sg-popover-toggle" id="themeBtn" aria-label="Toggle theme">Toggle</button>
    </div>
    <div class="sg-popover-row">
      <span id="fontSizeLabel">Font size</span>
      <div class="sg-size-btns" role="group" aria-labelledby="fontSizeLabel">
        <button class="sg-size-btn" data-size="sm" aria-label="Small" aria-pressed="false">S</button>
        <button class="sg-size-btn active" data-size="md" aria-label="Medium" aria-pressed="true">M</button>
        <button class="sg-size-btn" data-size="lg" aria-label="Large" aria-pressed="false">L</button>
        <button class="sg-size-btn" data-size="xl" aria-label="Extra large" aria-pressed="false">XL</button>
      </div>
    </div>
    <div class="sg-popover-row">
      <label for="motionCheck">Reduce motion</label>
      <input type="checkbox" id="motionCheck">
    </div>
  </div>
</div>
```

### JS

```js
const settingsBtn = document.getElementById('settingsBtn');
const popover = document.getElementById('settingsPopover');

// Toggle open/close — move focus in on open
settingsBtn.addEventListener('click', e => {
  e.stopPropagation();
  const open = popover.classList.toggle('open');
  settingsBtn.setAttribute('aria-expanded', open);
  if (open) {
    const first = popover.querySelector('button, input, select');
    if (first) first.focus();
  }
});

// Close on outside click
document.addEventListener('click', e => {
  if (!popover.contains(e.target) && e.target !== settingsBtn) {
    popover.classList.remove('open');
    settingsBtn.setAttribute('aria-expanded', 'false');
  }
});

// Close on Escape, return focus to trigger
document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && popover.classList.contains('open')) {
    popover.classList.remove('open');
    settingsBtn.setAttribute('aria-expanded', 'false');
    settingsBtn.focus();
  }
});

// aria-pressed on toggle buttons
function setFontSize(size, save = true) {
  document.documentElement.dataset.fontSize = size;
  document.querySelectorAll('.sg-size-btn').forEach(b => {
    const active = b.dataset.size === size;
    b.classList.toggle('active', active);
    b.setAttribute('aria-pressed', active ? 'true' : 'false');
  });
  if (save) localStorage.setItem('fontSize', size);
}
```

### CSS (focus-visible on popover internal controls)

```css
.sg-popover-toggle:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
.sg-size-btn:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
```

## Key Rules

- No `role="dialog"` without a full focus trap. Use no role or `role="group"`.
- `aria-expanded` on the trigger is the sole AT cue for open/close state.
- Always move focus to first interactive element on open.
- Always return focus to trigger on close (both Escape and outside-click paths).
- Use `aria-pressed` on toggle buttons that represent binary state — not just CSS class.
- Labels cannot be associated to `<button>` via `for`; use `aria-label` on the button directly.

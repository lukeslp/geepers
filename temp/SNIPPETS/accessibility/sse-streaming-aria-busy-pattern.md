# SSE Streaming — aria-busy + aria-label Loading State Pattern

**Source**: oss-safeguard-ux / safeguard.html — 2026-03-07
**Stack**: Vanilla JS, SSE/fetch streaming

## Problem

When an LLM response streams in via SSE/fetch, the UI enters a "loading" state
that is visible (spinner, disabled button, live region filling) but not announced
to screen readers. Users of AT get no cue that the system is working.

## Pattern

Three complementary signals cover all AT:

1. `aria-busy="true"` on the results container — suppresses live region
   announcements during streaming so partial tokens don't flood AT, then
   `aria-busy="false"` when done so AT reads the final content.

2. Dynamic `aria-label` on the trigger button — announces "Evaluating, please wait"
   on start and restores "Evaluate" on finish.

3. `aria-live="polite"` on the status meta line — announces final timing/token
   count once after streaming ends.

## Code

```js
// --- Before fetch ---
resultsRow.setAttribute('aria-busy', 'true');
generateBtn.setAttribute('aria-label', 'Evaluating, please wait');
generateBtn.disabled = true;
generateBtn.classList.add('loading');

// --- In finally block ---
resultsRow.removeAttribute('aria-busy');
generateBtn.setAttribute('aria-label', 'Evaluate');
generateBtn.disabled = false;
generateBtn.classList.remove('loading');
```

```html
<!-- Results container -->
<div class="sg-results-row" id="resultsRow">
  <!-- verdict box, reasoning box -->
</div>

<!-- Status meta line with polite live region -->
<div class="sg-meta" id="metaOut" aria-live="polite"></div>

<!-- Trigger button -->
<button class="sg-evaluate" id="generateBtn" aria-label="Evaluate">
  Evaluate
</button>
```

## Why aria-busy on the container (not the button)

Setting `aria-busy` on the results container suppresses premature announcements
from the `aria-live` regions inside it during streaming. The button's `disabled`
attribute already prevents re-activation; the `aria-label` change announces the
state transition for users who are focused on the button.

## Notes

- Do NOT set `aria-live` directly on the streaming text element while streaming —
  this causes token-by-token announcements. Use `aria-busy` on the parent instead.
- Restore `aria-label` in the `finally` block so it always resets even on error.
- Works equally well for WebSocket and EventSource-based streaming.

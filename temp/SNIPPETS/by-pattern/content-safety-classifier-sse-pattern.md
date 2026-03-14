# Content Safety Classifier — SSE Buffer Split + Verdict Extraction Pattern

**Source**: oss-safeguard-ux / safeguard.html — 2026-03-07
**Stack**: Vanilla JS, Ollama streaming API, SSE/fetch

## Problem

A streaming LLM response mixes chain-of-thought (`<think>...</think>`) with a
final verdict code (e.g. `D-SP4`, `VALID`, `INVALID + ESCALATE`). The client
needs to:

1. Show chain-of-thought in one pane while streaming.
2. Extract and render the verdict code in a separate pane after the fact.
3. Handle cases where the verdict appears before the stream ends (mid-buffer).

## Buffer Split Pattern

```js
let buffer = '', thinkingBuf = '', hasThinking = false, splitFound = false, splitAt = -1;

// Per-chunk handler (inside reader loop):
const chunk = data.message?.content || '';
buffer += chunk;

if (!splitFound) {
  // Detect <think> block
  if (!hasThinking && buffer.includes('<think>')) hasThinking = true;
  if (hasThinking && buffer.includes('</think>')) {
    splitAt = buffer.indexOf('</think>') + '</think>'.length;
    thinkingBuf = buffer.slice(buffer.indexOf('<think>') + '<think>'.length, buffer.indexOf('</think>'));
    splitFound = true;
  }
}

if (splitFound) {
  const responseText = buffer.slice(splitAt);
  // Show thinking in pane A, response in pane B (streaming)
  setOutput(analysisOut, responseText, true, 'reasoning');
  // Try to extract verdict mid-stream (last 5 lines)
  const ex = extractVerdict(responseText);
  if (ex) {
    setOutput(verdictOut, ex, false, 'verdict');
    setSignal(verdictSignal, 'done', 'Verdict');
    applySeverityClass(parseSeverityCode(ex));
    renderCatViz(parseSeverityCode(ex));
  }
} else if (!hasThinking) {
  // No <think> block — treat full buffer as reasoning
  setOutput(analysisOut, buffer, true, 'reasoning');
  // Re-scan for verdict anywhere in buffer
  const ex = extractVerdict(buffer);
  if (ex) { /* same as above */ }
}
```

## Verdict Extraction (reverse-scan last N lines)

```js
function extractVerdict(text) {
  const lines = text.split('\n').map(l => l.trim()).filter(Boolean);
  // Scan last 5 lines in reverse — verdict is always at the end
  for (let i = lines.length - 1; i >= Math.max(0, lines.length - 5); i--) {
    const up = lines[i].toUpperCase();
    if (
      up.match(/[DR]-(SP|VH|HS|SH|SC|FD|WD|HR|MU)\d/) ||
      up.includes('INVALID') ||
      up.includes('VALID') ||
      up.includes('ESCALATE')
    ) {
      return lines[i]; // Return ONLY the matched line, not trailing garbage
    }
  }
  return null;
}
```

## Severity Code Parser

```js
const VALID_SEVS = [0, 2, 3, 4]; // reject e.g. D-SP7

function parseSeverityCode(text) {
  const hasEscalate = /ESCALATE/i.test(text);
  const m = text.match(/([DR])-(SP|VH|HS|SH|SC|FD|WD|HR|MU)(\d)(\.\w+)?/i);
  if (m) {
    const sev = parseInt(m[3]);
    if (!VALID_SEVS.includes(sev)) return null; // reject invalid severity
    return {
      dir: m[1].toUpperCase() === 'D' ? 'Depiction' : 'Request',
      catCode: m[2].toUpperCase(),
      sev,
      subcode: m[4] ? m[4].toUpperCase() : '',
      rawCode: (m[1] + '-' + m[2] + m[3] + (m[4] || '')).toUpperCase(),
      hasEscalate,
    };
  }
  // Fallback: VALID/INVALID without category code
  const up = text.toUpperCase();
  if (up.includes('INVALID') || up.includes('VALID')) {
    const isValid = up.includes('VALID') && !up.includes('INVALID');
    return { dir: null, catCode: null, sev: isValid ? 0 : 3, rawCode: isValid ? 'VALID' : 'INVALID', hasEscalate };
  }
  return null;
}
```

## Key Lessons

- Always search last N lines in reverse for verdict — the model may include
  trailing whitespace or explanation after the code.
- Validate severity codes explicitly — models sometimes hallucinate invalid codes
  like `D-SP7` (only 0/2/3/4 are valid).
- Return only the matched line from `extractVerdict`, not the slice from that
  point forward — prevents policy text embedded earlier from being treated as verdict.
- Re-scan the full buffer on every chunk when no `<think>` split has been found —
  some models output the verdict before any reasoning text.

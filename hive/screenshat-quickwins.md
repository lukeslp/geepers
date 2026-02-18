# Quick Wins: screenshat

**Scan Date**: 2026-02-18
**Total Found**: 8
**Completed**: 0
**Remaining**: 8

## Executive Summary

Screenshat is a well-architected screenshot capture tool with solid accessibility and code quality. Most issues are minor polish improvements: missing ARIA labels on icon-only buttons, console statements in production code, and one potential UX improvement for alt text workflow clarity.

**Risk Level**: Low
**Effort**: 1-5 minutes each
**Total Session Time**: ~20-25 minutes

---

## Quick Wins to Complete

### 1. [A11y] Add aria-label to back button (CaptureResults)
**File**: `/home/coolhand/projects/screenshat/client/src/pages/CaptureResults.tsx:505`
**Current Code**:
```tsx
<button className="h-7 w-7 rounded-md flex items-center justify-center hover:bg-secondary/60 transition-colors">
  <ArrowLeft className="h-3.5 w-3.5" />
</button>
```
**Issue**: Icon-only button with no accessible label. Screen readers won't know its purpose.
**Fix**: Add `aria-label="Go back"` to the button element.
**Time**: 1 minute
**Impact**: High (navigation accessibility)

---

### 2. [A11y] Add aria-label to delete button (History)
**File**: `/home/coolhand/projects/screenshat/client/src/pages/History.tsx:199-209`
**Current Code**:
```tsx
<button
  className="h-7 w-7 rounded-md flex items-center justify-center hover:bg-destructive/10 text-muted-foreground hover:text-destructive transition-colors"
  onClick={...}
  title="Delete"
  disabled={deleteMutation.isPending}
>
  <Trash2 className="h-3 w-3" />
</button>
```
**Issue**: Has `title` attribute but no `aria-label`. `title` is not reliable for screen readers; ARIA is best practice. Button contains only icon.
**Fix**: Add `aria-label="Delete capture"` to complement or replace title.
**Time**: 1 minute
**Impact**: High (destructive action accessibility)

---

### 3. [UX] Add aria-label to generate alt text button (CaptureResults)
**File**: `/home/coolhand/projects/screenshat/client/src/pages/CaptureResults.tsx:235-249`
**Current Code**:
```tsx
<button
  onClick={() => onGenerateAltText(screenshot.id)}
  disabled={isGeneratingAltText}
  className="flex items-center gap-0.5 text-[9px] text-muted-foreground hover:text-primary transition-colors disabled:opacity-50"
  title={currentAltText ? "Regenerate alt text" : "Generate alt text"}
>
  {isGeneratingAltText ? (
    <Loader2 className="h-2.5 w-2.5 animate-spin" />
  ) : currentAltText ? (
    <RotateCcw className="h-2.5 w-2.5" />
  ) : (
    <Sparkles className="h-2.5 w-2.5" />
  )}
  {isGeneratingAltText ? "Generating…" : currentAltText ? "Regenerate" : "Generate"}
</button>
```
**Issue**: Button has title but no aria-label. Has text label but should have aria-label for clarity with icon toggle. Very small (9px text) may be hard to see.
**Fix**: Add `aria-label={currentAltText ? "Regenerate alt text" : "Generate alt text"}` to ensure consistency with title and clear screen reader labeling.
**Time**: 1 minute
**Impact**: Medium (accessibility + clarity)

---

### 4. [Quality] Remove console.log statements from server code
**File**: `/home/coolhand/projects/screenshat/server/screenshotService.ts:25, :37, :77`
**Current Code**:
```ts
console.log(`[ScreenshotService] Found browser at: ${p}`);
console.log(`[ScreenshotService] Found browser via which: ${result}`);
console.log(`[ScreenshotService] Retrying with system browser: ${fallback}`);
```
**Issue**: Debug/informational logs in production code. These should either be removed or behind a debug flag. Server startup will spam logs.
**Fix**: Remove these three console.log statements or wrap them in `if (process.env.DEBUG)` checks.
**Time**: 2 minutes
**Impact**: Medium (cleaner production logs)

---

### 5. [A11y] Add aria-label to retry button (History) when not failed
**File**: `/home/coolhand/projects/screenshat/client/src/pages/History.tsx:188-197`
**Current Code**:
```tsx
<button
  className={`h-7 px-2 rounded-md flex items-center gap-1 hover:bg-secondary/60 transition-colors text-[10px] ${
    isFailed ? "text-primary font-medium" : ""
  }`}
  onClick={e => e.stopPropagation()}
  title="Re-capture"
>
  <RefreshCw className="h-3 w-3" />
  {isFailed && <span>Retry</span>}
</button>
```
**Issue**: When not failed, button shows only icon with no visible text. Title exists but aria-label is better for accessibility.
**Fix**: Add `aria-label={isFailed ? "Retry capture" : "Re-capture"}` to button.
**Time**: 1 minute
**Impact**: Medium (accessibility)

---

### 6. [UX] Make analysis progress indicator more informative (CaptureResults)
**File**: `/home/coolhand/projects/screenshat/client/src/pages/CaptureResults.tsx:556-565`
**Current Code**:
```tsx
{isAnalyzingAll && (
  <Button
    variant="outline"
    size="sm"
    className="h-7 gap-1 text-[11px]"
    disabled
  >
    <Loader2 className="h-3 w-3 animate-spin" />
    Analyzing {analyzeAllProgress} / {unanalyzedCount}…
  </Button>
)}
```
**Issue**: Progress display shows wrong values — counter increments after mutation completes, not before. State updates at wrong time. User sees "Analyzing 0 / 5" then jumps to "Analyzing 5 / 5" with no intermediate feedback.
**Fix**: Move `setAnalyzeAllProgress(i + 1)` to BEFORE the mutation, not after. Or add better real-time feedback by incrementing on mutation start.
**Alternative**: Change `i + 1` to `i` to match 0-based indexing or show it more clearly.
**Time**: 3 minutes
**Impact**: Medium (UX clarity during analysis)

---

### 7. [Quality] Add null check for alt text button title
**File**: `/home/coolhand/projects/screenshat/client/src/pages/CaptureResults.tsx:239`
**Current Code**:
```tsx
title={currentAltText ? "Regenerate alt text" : "Generate alt text"}
```
**Issue**: If `currentAltText` is empty string or null, this is safe, but if `onGenerateAltText` is called while already generating, UI could show confusing state. No validation that button is actually callable.
**Fix**: Add explicit check in disabled prop and clarify title — already good but could add `disabled={isGeneratingAltText || !screenshot.fileUrl}` to prevent orphaned state.
**Time**: 2 minutes
**Impact**: Low (defensive programming)

---

### 8. [Error Handling] Improve JSON parse error message in analysis
**File**: `/home/coolhand/projects/screenshat/server/routers.ts:169`
**Current Code**:
```ts
} catch {
  console.error("Failed to parse LLM JSON response:", content);
}
```
**Issue**: Error is logged but silently fails — user sees no feedback that analysis partially failed (JSON parsing issue vs LLM error). No distinction between "LLM returned junk" vs "real network error".
**Fix**:
- Option A: Throw meaningful error with content sample so user knows analysis failed due to LLM response quality
- Option B: Log structured error with truncated response for debugging
- Option C: Add fallback analysis if JSON fails (don't silently return null)

**Time**: 3-5 minutes
**Impact**: Medium (error transparency)

---

## Summary by Category

| Category | Found | Priority | Time |
|----------|-------|----------|------|
| Accessibility (ARIA labels) | 4 | High | 4 min |
| Code Quality (console, cleanup) | 2 | Medium | 3 min |
| Error Handling | 1 | Medium | 3-5 min |
| UX Improvements | 1 | Medium | 3 min |

**Total Time Estimate**: 20-25 minutes
**Regression Risk**: Very Low (all changes are additive or UI polish)
**Test Impact**: Minimal (mostly UI/accessibility, no logic changes)

---

## Notes

- **Console statements**: Only in service startup paths, not hot code paths, but still should be cleaned up
- **Alt text flow**: The generation feature is well-designed; just needs better button labeling
- **Analysis progress**: Real issue is the state management timing, but minor and easy fix
- **No dead code found**: Imports and functions all appear to be used
- **No missing error handling**: Most mutations have `.onError` handlers with toast feedback
- **Database schema is clean**: All necessary fields present
- **Storage abstraction is solid**: File path handling looks safe


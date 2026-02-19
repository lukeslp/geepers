# Task Queue: wordblocks

**Generated**: 2026-02-18
**Total Tasks**: 12
**Quick Wins**: 3
**Blocked**: 0
**Effort Total**: ~25 hours (dev + testing)

---

## Overview

Three implementation tasks parsed from `/home/coolhand/projects/wordblocks/CLAUDE.md` and project state analysis. The queue prioritizes **critical blockers** (app is broken) before **enhancements** (new features), then **cleanup** (technical debt).

All file paths are absolute. See **Dependencies** section for sequencing.

---

## Ready to Build (Priority Order)

### 1. [CRITICAL] Fix Merge Conflict in grid-grammar-engine.js

- **Source**: /home/coolhand/projects/wordblocks/frontend/js/grid-grammar-engine.js
- **Impact**: 5 | **Effort**: 1 | **Priority**: 9.0
- **Type**: Bug Fix
- **Description**: File has merge conflict markers at line 1 and 463. First line: `/**` followed immediately by `window.GridGrammarEngine = GridGrammarEngine;` at line 463. The file fails to parse as valid JavaScript. Grid initialization at index.html:523 (`new GridGrammarEngine()`) crashes app on load.
- **Files Modified**:
  - `frontend/js/grid-grammar-engine.js` (460 lines)
- **Implementation**:
  1. Open file and identify conflict markers (should be `<<<<<<<`, `=======`, `>>>>>>>`)
  2. Choose correct version (likely post-merge) and remove markers
  3. Verify syntax with `node --check` or browser console
  4. Test grid loads without error
- **Verification**: App loads without JavaScript errors; grid system initializes; console.log shows GridGrammarEngine defined
- **Time**: ~15 minutes

---

### 2. [CRITICAL] Create Missing Grid Engine Base Class

- **Source**: index.html references non-existent `/js/grid/grid-engine.js`
- **Impact**: 5 | **Effort**: 2 | **Priority**: 8.5
- **Type**: Code Generation
- **Description**: Four grid variant classes extend undefined `GridEngine` base class:
  - `expandable-grid.js:7` – `class ExpandableGrammarGrid extends GridEngine {`
  - `scrabble-board.js:7` – `class ScrabbleBoardGrid extends GridEngine {`
  - `magnetic-poetry.js` – similar dependency
  - `index.html:586` – references `LinearGrammarRail` which extends GridEngine

  Base class file `/home/coolhand/projects/wordblocks/frontend/js/grid/grid-engine.js` exists (verified 181 lines), but **is NOT loaded in index.html**. Add script tag before variant grids load.
- **Files Modified**:
  - `frontend/index.html` (add `<script>` tag at line ~506, before `linear-rail.js`)
- **Implementation**:
  1. Verify `grid-engine.js` exists at `/home/coolhand/projects/wordblocks/frontend/js/grid/grid-engine.js`
  2. Add load order:
     ```html
     <script src="js/grid/grid-engine.js"></script>
     <!-- Grid variants depend on GridEngine base class -->
     <script src="js/grids/linear-rail.js"></script>
     <script src="js/grids/expandable-grid.js"></script>
     <script src="js/grids/scrabble-board.js"></script>
     <script src="js/grids/magnetic-poetry.js"></script>
     ```
  3. Test: Grid variant classes should now be defined; expandable/scrabble/magnetic buttons work
- **Verification**: Switch between grid variants (Linear → Expandable → Scrabble → Magnetic) without "undefined class" errors
- **Time**: ~20 minutes

---

### 3. [CRITICAL] Add requests to Backend Requirements

- **Source**: `/home/coolhand/projects/wordblocks/backend/app.py` imports `requests` (line 12) but missing from requirements.txt
- **Impact**: 5 | **Effort**: 1 | **Priority**: 8.0
- **Type**: Dependencies
- **Description**: Fresh venv install fails at app startup: `ModuleNotFoundError: No module named 'requests'`. Module used for xAI API calls in `GrammarProcessor.predict_next_words()` (line 435: `resp = provider.complete(messages, ...)`).
- **Files Modified**:
  - `backend/requirements.txt`
- **Implementation**:
  1. Open `/home/coolhand/projects/wordblocks/backend/requirements.txt`
  2. Add line: `requests==2.31.0` (matches Flask, etc. versions)
  3. Verify with: `pip install -r requirements.txt` in a clean venv
  4. Test backend startup: `python app.py` should not fail on import
- **Verification**: `python -c "import requests; print(requests.__version__)"` succeeds
- **Time**: ~5 minutes

---

### 4. [HIGH] Build Hex Picker UI Component

- **Source**: Task from user specification (not in existing code)
- **Impact**: 4 | **Effort**: 3 | **Priority**: 5.0
- **Type**: Feature Addition (UI Component)
- **Description**: Create interactive hex picker widget (300px diameter) with:
  - Center node: current verb (pink, #FF6B9D)
  - 6 surrounding nodes: semantic slots (WHO, WHAT, WHERE, WHEN, HOW, WHY)
  - Color-coded by POS (verb=pink, noun=orange, etc.)
  - Click slot → word selector opens
  - Call `/api/generate-sentence` with `mode=predict_next` for suggestions
  - Canvas or SVG implementation
- **Files Created**:
  - `frontend/js/components/hex-picker.js` (new, ~200-300 lines)
- **Files Modified**:
  - `frontend/index.html` (add container and script tag)
  - `frontend/css/main.css` (optional: hex-picker specific styles)
- **Dependencies**:
  - Requires grid-engine.js loaded ✓ (Task 2)
  - Requires grid-grammar-engine.js fixed ✓ (Task 1)
  - Requires vocab.js (exists, 274 lines)
  - Backend `/api/generate-sentence` must accept `mode=predict_next` (verify exists: line 915, method exists line 399)
- **Implementation**:
  1. Create `hex-picker.js` class with:
     - Constructor: takes container ID, verb, semantic map
     - `draw()`: renders hex layout (center verb, 6 surrounding slots)
     - `handleClick(slotIndex)`: open word selector modal for that slot
     - `getSlotSuggestions()`: POST to `/api/generate-sentence` with `mode=predict_next`
     - `updateSemanticMap()`: callback to update parent grid
  2. Use canvas 2D API for drawing (consistent with GridEngine)
  3. Add HTML container in index.html (e.g., `<div id="hex-picker-container"></div>`)
  4. Style with AAC color palette from vocabulary.js
  5. Test: click each slot, suggestions appear, semantic map updates
- **Verification**:
  - Hex picker renders 300px diameter, 6 slots visible
  - Clicking slot triggers word selector
  - Selected word updates center verb visual
  - `/api/generate-sentence` called with correct payload
- **Time**: ~2-3 hours (design + implementation + testing)

---

### 5. [HIGH] Dedup main.js / main-grid.js

- **Source**: `/home/coolhand/projects/wordblocks/CLAUDE.md` notes section
- **Impact**: 2 | **Effort**: 1 | **Priority**: 3.0
- **Type**: Cleanup
- **Description**: Two identical files (both 831 lines), both define `WordBlocksGridApp`. Choose canonical copy and delete other.
  - `/home/coolhand/projects/wordblocks/frontend/js/main.js` (26636 bytes)
  - `/home/coolhand/projects/wordblocks/frontend/js/main-grid.js` (26636 bytes)

  Currently index.html doesn't load either (checked load order). Verify which should be kept.
- **Files Modified**:
  - Delete one of `main.js` or `main-grid.js`
  - Update any references in `index.html` if present
- **Implementation**:
  1. Verify byte-for-byte content identical: `cmp frontend/js/main.js frontend/js/main-grid.js`
  2. Check index.html for references to either file
  3. Decision: keep `main-grid.js` (more descriptive name), delete `main.js`
  4. Search codebase for imports: `grep -r "main\.js" frontend/` (expect none, since not in index.html)
- **Verification**: App loads and functions identically; grid system works
- **Time**: ~10 minutes

---

### 6. [MEDIUM] Archive Legacy Radial System

- **Source**: `/home/coolhand/projects/wordblocks/CLAUDE.md` known issues
- **Impact**: 2 | **Effort**: 1 | **Priority**: 2.5
- **Type**: Cleanup
- **Description**: Four legacy radial/canvas system files exist in `frontend/js/` but are NOT loaded by index.html:
  - `frontend/js/radial-menu.js` (543 lines)
  - `frontend/js/radial-menu-simple.js` (272 lines)
  - `frontend/js/radial-vocabulary.js` (239 lines)
  - `frontend/js/semantic-network.js` (1499 lines)

  Archive already exists at `frontend/archive/` (verified). Move these files there and remove from load path.
- **Files Modified**:
  - Move: `frontend/js/radial-menu.js` → `frontend/archive/`
  - Move: `frontend/js/radial-menu-simple.js` → `frontend/archive/`
  - Move: `frontend/js/radial-vocabulary.js` → `frontend/archive/`
  - Move: `frontend/js/semantic-network.js` → `frontend/archive/`
- **Implementation**:
  1. `cd /home/coolhand/projects/wordblocks`
  2. `mv frontend/js/radial-*.js frontend/archive/`
  3. `mv frontend/js/semantic-network.js frontend/archive/`
  4. Verify `frontend/js/` no longer contains these files
  5. Verify `frontend/archive/` contains them
  6. Check index.html doesn't reference them (it shouldn't, already not loaded)
- **Verification**: Index.html works identically; no 404s for missing files; ls shows files moved
- **Time**: ~5 minutes

---

## Blocked Tasks

*None currently. All dependencies satisfied by quick wins above.*

---

## Deferred (Low Priority)

### A. Audit wordblocks_hex_prediction.py

- **Source**: File at project root `/home/coolhand/projects/wordblocks/wordblocks_hex_prediction.py` (exists)
- **Priority**: 1.5
- **Type**: Investigation
- **Description**: Python script at project root. Unknown purpose. Integrate into backend or archive?
- **Action**: Read file, determine purpose, then integrate into backend API or delete

### B. Multi-Provider Prediction Caching

- **Source**: Backend could cache verb analysis results to reduce LLM calls
- **Priority**: 1.0
- **Type**: Performance Optimization
- **Description**: `predict_next_words()` hits xAI API for every verb—expensive and slow
- **Solution**: Add Redis cache keyed on `{verb}:{context}`

### C. Adverb Manner Bug

- **Source**: Grammar engine at `backend/app.py:356-360`
- **Priority**: 2.0
- **Type**: Bug Fix
- **Description**: Hardcodes `with` prefix for manner/adverb slots, producing `I eat with quickly`
- **Solution**: Check if word is adverb (ends in -ly or in COMMON_ADVERBS), skip `with`
- **Note**: Marked as "Low / informational" in CLAUDE.md

### D. Clean Up Root-Level Session Files

- **Source**: `.aider.chat.history.md`, `.aider.input.history` at project root
- **Priority**: 0.5
- **Type**: Cleanup
- **Action**: Delete agent/session debris

---

## Dependency Graph

```
Task 1: Fix merge conflict (grid-grammar-engine.js)
  ↓ (unblocks app load)

Task 2: Create grid-engine.js base class
  ↓ (unblocks grid variants)

Task 3: Add requests to requirements.txt
  ↓ (unblocks backend startup)

App now boots. Grid system functional.

Task 4: Build hex picker UI
  ├─ Requires: Task 1, 2, 3 ✓
  └─ Requires: Backend /api/generate-sentence endpoint ✓ (line 915)

Task 5: Dedup main.js / main-grid.js
  └─ Independent (cleanup)

Task 6: Archive legacy radial files
  └─ Independent (cleanup)
```

**Suggested execution order**:
1. **Session 1** (30 mins): Tasks 1, 2, 3 (critical blockers)
2. **Session 2** (3 hours): Task 4 (hex picker UI)
3. **Session 3** (15 mins): Tasks 5, 6 (cleanup)

---

## Statistics

| Category | Count |
|----------|-------|
| Critical (impact=5) | 3 |
| High (impact=4) | 2 |
| Medium (impact=2) | 1 |
| Quick Wins (effort ≤ 2) | 3 |
| Small (effort ≤ 1 hour) | 4 |
| Medium (effort 1-3 hours) | 1 |
| Large (effort > 3 hours) | 1 |
| **Total Ready to Build** | **6** |

---

## Effort Breakdown

- **Bug Fixes**: 5 hours (Tasks 1–3)
- **New Feature (Hex Picker)**: 3 hours (Task 4)
- **Cleanup**: 15 minutes (Tasks 5–6)
- **Testing**: 2 hours (all tasks)
- **Total**: ~10.25 hours active development

---

## Quality Checklist

- [x] All plan files parsed (CLAUDE.md, recommendations.md)
- [x] Code structure analyzed (frontend/js/ and backend/app.py reviewed)
- [x] Dependencies identified (grid-engine.js base class, requests import)
- [x] Estimates validated (merge conflict ~15min, grid engine ~20min, hex picker ~3hr)
- [x] Quick wins identified (3: merge fix, grid engine load, requests)
- [x] Blocked tasks checked (none—all blockers are in ready queue)
- [x] Load order verified (index.html script tags, grid variant dependencies)

---

## Notes for Implementer

### API Contract (Hex Picker ↔ Backend)

**POST `/api/generate-sentence`** with `mode=predict_next`:

```json
{
  "semantic_map": {
    "root": "eat",
    "relations": {
      "who": {"word": "I"},
      "what": {"word": "apple"}
    },
    "filters": {"tense": "present"}
  },
  "mode": "predict_next"
}
```

**Response**:
```json
{
  "predictions": [
    {"word": "quickly", "slot": "how"},
    {"word": "home", "slot": "where"},
    {"word": "now", "slot": "when"}
  ],
  "success": true
}
```

Backend implementation exists in `/home/coolhand/projects/wordblocks/backend/app.py` (line 399–488).

### AAC Color Coding (for Hex Picker)

From `frontend/js/vocabulary.js` and `index.html`:

```javascript
{
  'verb': '#ef4444',       // Red
  'noun': '#f97316',       // Orange
  'pronoun': '#8b5cf6',    // Purple
  'adjective': '#06b6d4',  // Cyan
  'adverb': '#10b981',     // Green
  'preposition': '#ec4899' // Pink
}
```

### Testing Commands

```bash
# Backend startup
cd /home/coolhand/projects/wordblocks/backend
source venv/bin/activate
pip install -r requirements.txt  # After adding requests
python app.py

# Frontend check (browser console should show no errors)
# Grid switch test: click Linear → Expandable → Scrabble → Magnetic

# Move files
mv frontend/js/radial-*.js frontend/archive/
mv frontend/js/semantic-network.js frontend/archive/

# Dedup check
cmp frontend/js/main.js frontend/js/main-grid.js
rm frontend/js/main.js  # Keep main-grid.js
```

---

## References

- **CLAUDE.md**: `/home/coolhand/projects/wordblocks/CLAUDE.md` (project-specific guidance)
- **Scout Report**: `~/geepers/recommendations/by-project/wordblocks.md` (2026-02-18)
- **Project Root**: `/home/coolhand/projects/wordblocks`
- **Frontend**: `/home/coolhand/projects/wordblocks/frontend/` (index.html, js/, css/)
- **Backend**: `/home/coolhand/projects/wordblocks/backend/app.py` (Flask app, 991 lines)
- **Service Port**: 8847 (managed via `sm start/stop/restart wordblocks`)

---

**Last Updated**: 2026-02-18 18:45 UTC
**Queue Version**: 1.0
**Status**: Ready for Implementation

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>

# Planner Analysis — 2026-03-13

**Date Generated**: 2026-03-13 09:45
**Scope**: Full codebase assessment
**Source Files Analyzed**: MASTER_PLAN.md, hivemind-quickwins.md, geepers recommendations (10 projects), recent commits

---

## Top Priorities (Next 1-2 Days)

### 1. [BLOCKER] Fix aivia test.sh paths
- **Impact**: 5 | **Effort**: 1 | **Priority**: 8.5 | **Status**: High-urgency blocker
- **Location**: `plugins/aivia/test.sh` (lines 8, 137, 140)
- **Issue**: All 33 tests fail because `lib/core.sh` path is wrong. Should be `engine/lib/core.sh`.
- **Files**: `plugins/aivia/test.sh`
- **Time**: 5 minutes
- **Risk**: None (mechanical fix)
- **Depends on**: None
- **Source**: `geepers/recommendations/by-project/aivia.md` (scout report 2026-03-12)

### 2. [QUICK WIN] Extract duplicate GEMINI_TEXT_MODEL constant (hivemind)
- **Impact**: 3 | **Effort**: 1 | **Priority**: 7 | **Status**: Ready
- **Location**:
  - `projects/hivemind/client/src/pages/HiveMindApp.tsx:117`
  - `projects/hivemind/client/src/hooks/useAIGeneration.ts:16`
- **Task**: Create `client/src/constants/models.ts`, move constant there, import in both files
- **Time**: 5-10 minutes
- **Risk**: Low (isolated constant)
- **Depends on**: None
- **Files**: 3 files
- **Source**: `geepers/hive/hivemind-quickwins.md` (remaining quick wins)

### 3. [QUICK WIN] Remove duplicate HexNode type definition (hivemind)
- **Impact**: 3 | **Effort**: 2 | **Priority**: 6.5 | **Status**: Ready
- **Location**:
  - `projects/hivemind/client/src/types/hivemind.d.ts:5-33` (canonical)
  - `projects/hivemind/client/src/components/HexCanvas.tsx:125-149` (duplicate)
  - `projects/hivemind/client/src/hooks/useAIGeneration.ts:40-60` (duplicate)
- **Task**: Keep canonical in types, import in other two files, remove duplicates
- **Time**: 10-15 minutes
- **Risk**: Low (purely structural, established pattern)
- **Depends on**: None
- **Files**: 3 files
- **Source**: `geepers/hive/hivemind-quickwins.md`

### 4. [QUICK WIN] Extract NODE_TYPES configuration (hivemind)
- **Impact**: 4 | **Effort**: 2.5 | **Priority**: 6 | **Status**: Ready
- **Location**:
  - `projects/hivemind/client/src/components/HexCanvas.tsx` (full config)
  - `projects/hivemind/client/src/pages/HiveMindApp.tsx` (separate config)
- **Task**: Create `client/src/constants/nodeTypes.ts`, consolidate, ensure consistent rendering
- **Time**: 20-30 minutes
- **Risk**: Medium (affects rendering/logic, needs verification)
- **Depends on**: Task #2 (same pattern)
- **Files**: 3 files
- **Source**: `geepers/hive/hivemind-quickwins.md`

---

## Medium Priority (This Week)

### 5. Accessibility Atlas — Data source citations
- **Impact**: 5 | **Effort**: 2 | **Priority**: 6.5 | **Status**: Needs action
- **Location**: `datasets/accessibility-atlas/`
- **Issues**:
  - 3 missing files referenced in README (wlasl_index.csv, aac_vocabulary_data.json, aac_100words.pdf)
  - ada_digital_lawsuits.json sources lack URLs
- **Task**: Either add files or update README/dataset_index.json to clarify external references only
- **Files**: README.md, dataset_index.json, ada_digital_lawsuits.json
- **Risk**: Medium (publication blocker if left unresolved)
- **Depends on**: None (can be done anytime)
- **Source**: `geepers/recommendations/by-project/accessibility-atlas.md` (validation 2026-02-14)

### 6. Viewer — Comprehensive accessibility audit
- **Impact**: 4 | **Effort**: 3 | **Priority**: 5.5 | **Status**: In progress
- **Location**: `html/viewer/` (recent work: WCAG 2.2 AA, ARIA dialog, roving tabindex, FocusTrap)
- **Details**: Recent commits show major accessibility work completed. 49KB recommendation file suggests additional improvements queued.
- **Files**: Viewer component/CSS/JS
- **Risk**: Low (established pattern, recent work)
- **Depends on**: None
- **Source**: `geepers/recommendations/by-project/viewer.md` (49KB, latest 2026-03-08)

### 7. Datavis — Billions rebrand to "The Same Scale"
- **Impact**: 3 | **Effort**: 2 | **Priority**: 5 | **Status**: In progress
- **Location**: `html/datavis/billions/`
- **Details**: Recent commit (afee3ebdf) shows cross-project quality overhaul underway
- **Files**: Billions visualization + project collateral
- **Risk**: Low (cosmetic rebrand)
- **Depends on**: None
- **Source**: Recent git commit history

---

## Deferred (Lower Priority)

### 8. TypeScript type safety in visualization config (hivemind)
- **Impact**: 2 | **Effort**: 1.5 | **Priority**: 3 | **Status**: Nice-to-have
- **Task**: Create `VisualizationConfig` union type for chart/map/timeline/diagram, use discriminated union pattern
- **Time**: 10-15 minutes
- **Risk**: Low (feature already works)
- **Note**: Feature is functional; typing would be improvement, not requirement
- **Source**: `geepers/hive/hivemind-quickwins.md`

---

## Task Queue Statistics

| Category | Count | Time (est.) |
|----------|-------|------------|
| Blockers | 1 | 5 min |
| Quick Wins (Ready) | 2 | 15 min |
| Quick Wins (Bundled) | 1 | 30 min |
| Medium Priority | 3 | 2-4 hours |
| Deferred | 1 | 15 min |
| **TOTAL** | **8** | **3-5 hours** |

---

## Dependencies & Sequencing

```
[BLOCKER] aivia test.sh ──→ (nothing depends on this)
│
[QW] GEMINI_TEXT_MODEL ──→ [QW] NODE_TYPES (same pattern)
│                            │
└─────────────────────────→ [READY TO MERGE]

[Accessibility Atlas citations] ──→ (independent, can start anytime)
[Viewer a11y audit] ──→ (independent, active work)
[Datavis rebrand] ──→ (independent, in progress)
[Hivemind type safety] ──→ (deferred, no urgency)
```

---

## Recommendations

1. **Start with aivia test.sh** (5 min blocker) — clears high-priority path
2. **Bundle hivemind constant extraction** (15-30 min) — complete #2, #3, #4 in one session
3. **Parallel track**: Run accessibility atlas citations audit independently
4. **Weekly**: Continue viewer a11y work and datavis rebrand (both in progress)

---

## Notes

- **hivemind-quickwins.md status**: 43% complete (3/7 tasks done). Remaining 4 are low-risk, high-value refactors
- **Recent context**: Last commit (c52e1db7a) was viewer accessibility. Work appears to be focusing on A11y + datavis quality
- **No blockers** except aivia test.sh (trivial fix)
- **Master plan** reflects completed state: publishing, architecture, documentation cleanup mostly done. Current work is incremental feature/quality improvements

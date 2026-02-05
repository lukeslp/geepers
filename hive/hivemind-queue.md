# Task Queue: hivemind

**Generated**: 2026-01-07 23:10
**Total Tasks**: 6
**Quick Wins**: 2
**Blocked**: 1

## Ready to Build (Priority Order)

### 1. [QW] Remove debug console logs in AI generation flow
- **Source**: quickwin scan
- **Impact**: 3 | **Effort**: 1 | **Priority**: 4.5
- **Description**: Remove verbose `console.log` statements from generation and parsing paths.
- **Files**: `hivemind/client/src/pages/HiveMindApp.tsx`

### 2. [QW] Silence Vite analytics placeholder warnings
- **Source**: build output + `hivemind/client/index.html`
- **Impact**: 2 | **Effort**: 1 | **Priority**: 3.0
- **Description**: Remove or guard `%VITE_ANALYTICS_*%` placeholders to avoid build warnings when analytics are disabled.
- **Files**: `hivemind/client/index.html`

### 3. Align app base path with renamed route
- **Source**: rename context + runtime error
- **Impact**: 5 | **Effort**: 2 | **Priority**: 6.0
- **Description**: Update `vite.config.ts` base and deployment env (`BASE_PATH`) to match the renamed path; ensure API routes and static assets resolve.
- **Depends on**: Confirm final public path (e.g., `/hivemand/`).
- **Files**: `hivemind/vite.config.ts`, service env

### 4. Route Build Artifact through backend
- **Source**: code review
- **Impact**: 4 | **Effort**: 2 | **Priority**: 5.0
- **Description**: Replace direct Gemini calls with `/api/generate` to avoid client API keys and unify base path handling.
- **Files**: `hivemind/client/src/components/BuildArtifactModal.tsx`, `hivemind/server/index.ts`

### 5. Mobile pinch-to-zoom + touch improvements
- **Source**: `hivemind/IMPROVEMENTS.md`
- **Impact**: 4 | **Effort**: 3 | **Priority**: 4.5
- **Description**: Add pinch-zoom gesture and tune touch event handling for panning/selection.
- **Files**: `hivemind/client/src/pages/HiveMindApp.tsx`

## Blocked Tasks

### Rename service ID from hexmind -> hivemind
- **Blocked by**: Decision to rename service entry in service manager
- **Reason**: Needs updates to service metadata and possibly Caddy routes

## Deferred (Low Priority)

### Performance virtualization tuning
- **Priority**: 2.5
- **Reason**: Visible node culling exists; revisit after mobile/accessibility work.

## Statistics

| Category | Count |
|----------|-------|
| High priority (>6) | 1 |
| Medium priority (3-6) | 4 |
| Low priority (<3) | 1 |
| Quick wins | 2 |
| Blocked | 1 |

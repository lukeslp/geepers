# Task Queue: skymarshal

**Generated**: 2026-02-14 14:25
**Total Tasks**: 28
**Quick Wins**: 8
**Blocked**: 0
**Analysis Source**: CRITIC.md, INTEGRATION_ANALYSIS.md, REPO_AUDIT.md, recommendations/skymarshal.md

---

## Ready to Build (Priority Order)

### 1. [QW] Update Python README: Remove "WORK IN PROGRESS" Warning
- **Source**: REPO_AUDIT.md:62, 185
- **Impact**: 4 | **Effort**: 1 | **Priority**: 7.0
- **Description**: The skymarshal Python package (v0.1.0) is published to PyPI but README warns "WORK IN PROGRESS". Remove or soften the warning. Also fix license inconsistency (CC0 in PyPI vs MIT in README).
- **Files**: `/home/coolhand/servers/skymarshal/README.md`
- **Depends on**: None
- **Acceptance**: README updated, license field consistent, PyPI version badge added

---

### 2. [QW] Extract Auth Decorator for DRY Pattern
- **Source**: CRITIC.md:76, 234 (TD-004)
- **Impact**: 3 | **Effort**: 2 | **Priority**: 6.5
- **Description**: Every blueprint in the unified backend (`cleanup.py`, `analytics.py`, `network.py`, etc.) duplicates the same 12-line auth guard pattern. Extract to shared `@require_auth` decorator in `skymarshal/api/auth_utils.py` to reduce 168 lines of duplicate code.
- **Files**: `skymarshal/api/auth_utils.py`, `skymarshal/api/blueprints/*.py` (7 files)
- **Depends on**: None
- **Pattern**:
  ```python
  @require_auth
  def route_handler(service: ContentService):
      # service injected by decorator
  ```

---

### 3. [QW] Remove Broken bsky-follow-analyzer Link from README
- **Source**: INTEGRATION_ANALYSIS.md:284
- **Impact**: 3 | **Effort**: 1 | **Priority**: 6.5
- **Description**: README references broken GitHub link (https://github.com/lukeslp/bsky-follow-analyzer - 404). This functionality already exists in skymarshal. Remove link and document built-in analytics features instead.
- **Files**: `/home/coolhand/servers/skymarshal/README.md`
- **Depends on**: None

---

### 4. [QW] Add PyPI Version Badge to Python README
- **Source**: REPO_AUDIT.md:263
- **Impact**: 2 | **Effort**: 1 | **Priority**: 5.5
- **Description**: skymarshal-js has npm version badge, but Python version doesn't have PyPI badge. Add to match presentation quality.
- **Files**: `/home/coolhand/servers/skymarshal/README.md`
- **Depends on**: Task #1

---

### 5. [QW] Clarify Python vs TypeScript Package Relationship in READMEs
- **Source**: REPO_AUDIT.md:186, 206, 267
- **Impact**: 3 | **Effort**: 1 | **Priority**: 6.0
- **Description**: Add "Related Projects" section to Python README linking to skymarshal-js (npm version). Add "Why two versions?" FAQ explaining different ecosystems (CLI/Flask vs npm/library).
- **Files**: `/home/coolhand/servers/skymarshal/README.md`, `/home/coolhand/servers/skymarshal/CLAUDE.md`
- **Depends on**: None

---

### 6. [QW] Create Shared JSON Schema for Cross-System Data Flow
- **Source**: geepers recommendations:1309 (API Architecture Analysis)
- **Impact**: 3 | **Effort**: 2 | **Priority**: 6.0
- **Description**: Define canonical JSON format for engagement data export. Used for: (1) skymarshal → bsky-follow-analyzer data flow, (2) API response consistency, (3) future external API consumers.
- **Files**: `skymarshal/api/schemas.py` (new)
- **Schema Example**:
  ```python
  class EngagementData(BaseModel):
      uri: str
      likes: int
      reposts: int
      replies: int
      timestamp: datetime
      content_type: str
  ```
- **Depends on**: None

---

### 7. [QW] Add OpenAPI/Swagger Spec for Flask Backend
- **Source**: geepers recommendations:1290 (API Quality Improvements)
- **Impact**: 4 | **Effort**: 2 | **Priority**: 6.5
- **Description**: Document all 35 REST API endpoints with OpenAPI 3.0 spec. Use flask-smorest or flasgger to auto-generate interactive /docs. Enables external API consumers and improves discoverability.
- **Files**: `skymarshal/api/__init__.py`, `skymarshal/api/schemas.py` (new)
- **Tools**: flask-smorest or flasgger
- **Depends on**: None

---

### 8. [QW] Verify Production Deployment (Caddy + Service Manager)
- **Source**: geepers recommendations:44 (HIGH PRIORITY), 49
- **Impact**: 5 | **Effort**: 1 | **Priority**: 7.5
- **Description**: Unified backend is code-complete but deployment config needs verification. Check: (1) Caddy routing from port 3001 (Express) to port 5050 (Flask), (2) service manager registration in `/home/coolhand/service_manager.py`, (3) health endpoint responses, (4) Socket.IO connectivity.
- **Files**: `/etc/caddy/Caddyfile`, `/home/coolhand/service_manager.py`, `/home/coolhand/servers/skymarshal/start.sh`
- **Commands**:
  ```bash
  sm status skymarshal
  curl -X GET http://localhost:5050/health
  sm logs skymarshal
  ```
- **Depends on**: None

---

## High-Value Enhancements

### 9. React → Flask Backend E2E Testing
- **Source**: geepers recommendations:60 (MEDIUM)
- **Impact**: 5 | **Effort**: 3 | **Priority**: 5.5
- **Description**: React frontend exists at `/home/coolhand/html/bluesky/unified/` with Vite proxy configured. Write integration tests verifying: (1) login flow (React → Flask auth), (2) firehose streaming (SocketIO), (3) analytics queries, (4) content operations (fetch/delete).
- **Files**: `tests/integration/test_e2e_*.py`, React tests
- **Test Plan**:
  - Auth: POST /api/auth/login → SessionManager → API token issued
  - Analytics: GET /api/analytics/followers → FollowerAnalyzer called
  - Firehose: SocketIO connect → Flask emits initial stats
  - Content: POST /api/content/delete → MultipleProgressUpdates via SocketIO
- **Depends on**: Task #8 (deployment verified)

---

### 10. Build Service Layer Abstraction (ContentService Extension)
- **Source**: CRITIC.md:203, 236 (TD-006)
- **Impact**: 3 | **Effort**: 4 | **Priority**: 4.5
- **Description**: Current API routes directly import domain modules (e.g., `from skymarshal.cleanup.following_cleaner import FollowingCleaner`). Violates dependency inversion. Extend `ContentService` to wrap all domain managers into unified interface. API routes only talk to service, not modules.
- **Files**: `skymarshal/services/content_service.py` (extend), `skymarshal/api/blueprints/*.py` (update)
- **Current Pattern**:
  ```python
  # BAD: Route directly imports module
  from skymarshal.cleanup.following_cleaner import FollowingCleaner
  cleaner = FollowingCleaner(service.auth)
  ```
- **Target Pattern**:
  ```python
  # GOOD: Service layer handles it
  class ContentService:
      def find_cleanup_candidates(self):
          return self._following_cleaner.find_cleanup_candidates()

  # Route just calls service
  result = service.find_cleanup_candidates()
  ```
- **Depends on**: Task #2 (auth decorator refactored)

---

### 11. Database Optimization: Add High-Value Indexes
- **Source**: geepers recommendations:1360 (Immediate Actions)
- **Impact**: 4 | **Effort**: 1 | **Priority**: 6.5
- **Description**: Backend SQLite has 36,275 engagement records. Add 3 strategic indexes to improve query performance 20-100x. (1) `engagement(created_at)` for TTL batch lookups, (2) Frontend compound `contentItems(contentType, engagementScore DESC)`, (3) Covering index `uri_freshness`.
- **Files**: `skymarshal/engagement_cache.py`, `skymarshal/sql/schema_migrations.sql` (new)
- **Queries**:
  ```sql
  CREATE INDEX idx_created_at ON engagement(created_at);
  CREATE INDEX idx_uri_freshness ON engagement(uri, last_updated, ttl);
  PRAGMA journal_mode=WAL;  -- concurrent read optimization
  PRAGMA busy_timeout=5000; -- prevent lock errors
  ```
- **Depends on**: None
- **Testing**: Run VACUUM after indexes, benchmark with `engagement_cache._benchmark_query_times()`

---

### 12. React UI Layer: Expose Backend APIs
- **Source**: CRITIC.md:28, 274 (Quick Win - 2-4 hours), geepers recommendations:1179
- **Impact**: 5 | **Effort**: 3 | **Priority**: 5.0
- **Description**: Backend has 35 API routes but React app exposes only 5-10. Build React components in `/home/coolhand/html/bluesky/unified/app/src/features/followers/` to surface: (1) Follower analysis table, (2) Cleanup candidate list, (3) Network graph visualization.
- **Files**:
  - `FollowerList.tsx` (table with sorting, filtering, bot badges)
  - `CleanupCandidates.tsx` (interactive unfollow flow)
  - `NetworkGraph.tsx` (D3.js visualization)
- **API Calls**: `/api/analytics/followers`, `/api/cleanup/analyze`, `/api/network/fetch`
- **Design**: Match Swiss Design aesthetic (Black/White/Red, 8px grid)
- **Depends on**: Task #8 (deployment verified)

---

### 13. CAR File Download Feature
- **Source**: geepers recommendations:98 (HIGH, 1 hour effort)
- **Impact**: 4 | **Effort**: 1 | **Priority**: 6.5
- **Description**: Add menu option to download CAR file (Content Addressable aRchive of user's Bluesky data) and save locally. Already partially implemented in `data_manager.py`, just needs UI wiring.
- **Files**: `skymarshal/api/content.py`, React UI
- **Depends on**: Task #12 (UI layer exists)

---

### 14. "Nuclear Option" Safe Deletion Mode
- **Source**: geepers recommendations:127 (HIGH, 2-3 hours)
- **Impact**: 5 | **Effort**: 2 | **Priority**: 6.0
- **Description**: Implement "nuke" option to delete ALL content with extreme safety: (1) Multiple confirmations (4+), (2) Typed confirmation phrase ("DELETE EVERYTHING"), (3) 5-second countdown with Ctrl+C interrupt, (4) Mandatory backup reminder.
- **Files**: `skymarshal/deletion.py` (extend), React confirmation modal
- **Pattern**: Inspired by Heroku/GitHub enterprise deletion workflows
- **Depends on**: Task #12 (UI layer exists)

---

## Architecture & Code Quality

### 15. Add API Versioning Strategy
- **Source**: geepers recommendations:1293 (API Quality Improvements)
- **Impact**: 3 | **Effort**: 2 | **Priority**: 4.5
- **Description**: Current routes: `/api/analytics/followers`. Proposed: `/api/v1/analytics/followers` for future compatibility. Add versioning strategy documentation.
- **Files**: `skymarshal/api/__init__.py`, `skymarshal/CLAUDE.md`
- **Depends on**: None

---

### 16. Standardize API Response Envelope
- **Source**: geepers recommendations:1295
- **Impact**: 3 | **Effort**: 2 | **Priority**: 4.5
- **Description**: Inconsistent response formats across endpoints. Standardize to: `{"success": bool, "data": {...}, "error": str, "timestamp": ISO8601}`. Add middleware to wrap all responses.
- **Files**: `skymarshal/api/__init__.py` (response wrapper)
- **Depends on**: None

---

### 17. Add Input Validation with Pydantic
- **Source**: geepers recommendations:1295
- **Impact**: 3 | **Effort**: 2 | **Priority**: 4.5
- **Description**: Replace manual request validation in blueprints with Pydantic schemas. Improves type safety, auto-generates OpenAPI docs, reduces error handling code.
- **Files**: `skymarshal/api/schemas.py`, `skymarshal/api/blueprints/*.py`
- **Pattern**:
  ```python
  class DeleteRequest(BaseModel):
      uris: List[str]
      dry_run: bool = False
  ```
- **Depends on**: Task #6 (schemas.py created), Task #7 (OpenAPI spec)

---

### 18. Extract Configuration Management with Pydantic Settings
- **Source**: geepers recommendations:1416 (Architecture & Infrastructure)
- **Impact**: 3 | **Effort**: 2 | **Priority**: 4.0
- **Description**: Current settings scattered across code. Centralize with Pydantic BaseSettings: batch sizes, cache TTLs, API limits, database paths. Support .env files.
- **Files**: `skymarshal/config.py` (new)
- **Depends on**: None

---

### 19. Implement Structured Logging
- **Source**: geepers recommendations:1529 (Logging Infrastructure)
- **Impact**: 3 | **Effort**: 2 | **Priority**: 4.0
- **Description**: Replace Rich print statements with Python logging module. Logs: API call tracing, cache hits/misses, deletion audit trail. Separate file for API operations.
- **Files**: `skymarshal/logging_config.py` (new)
- **Depends on**: None

---

## Feature Consolidation

### 20. CAR File Management Integration
- **Source**: geepers recommendations:99 (HIGH, 1 hour)
- **Impact**: 4 | **Effort**: 1 | **Priority**: 6.0
- **Description**: FollowerAnalyzer and FollowingCleaner exist. Import/export CAR files to persist backups locally. Add menu: "Download backup" → saves to ~/.skymarshal/backups/.
- **Files**: `skymarshal/services/backup_service.py` (new)
- **Depends on**: Task #13 (CAR download feature)

---

### 21. Follower/Following Management Module Consolidation
- **Source**: geepers recommendations:296, 306
- **Impact**: 4 | **Effort**: 3 | **Priority**: 5.0
- **Description**: FollowerAnalyzer (558 lines) and FollowingCleaner (568 lines) exist but scattered. Consolidate into unified FollowerWorkflow orchestrator: analyze → cleanup → unfollow. Add REST API endpoints.
- **Files**: `skymarshal/services/follower_workflow.py` (new)
- **Features**: Rank, detect bots, cleanup, unfollow, export reports
- **Depends on**: Task #12 (UI for workflows)

---

### 22. Bot Detection Scoring System
- **Source**: geepers recommendations:327 (MEDIUM, 4-6 hours)
- **Impact**: 4 | **Effort**: 3 | **Priority**: 4.5
- **Description**: Implement multi-signal bot scoring: (1) Follower ratio (30%), (2) Profile completeness (20%), (3) Username patterns (20%), (4) Account age (15%), (5) Activity patterns (15%). Already partially in `bot_detection.py`, expand and expose via API.
- **Files**: `skymarshal/bot_detection.py` (extend), `skymarshal/api/profile.py`
- **Depends on**: Task #21 (follower consolidation)

---

### 23. Content Export Formats (CSV, Markdown, HTML, RSS)
- **Source**: geepers recommendations:397 (LOW, 3-4 hours)
- **Impact**: 3 | **Effort**: 3 | **Priority**: 3.5
- **Description**: Add export formats beyond JSON. CSV (spreadsheet), Markdown (human-readable), HTML (self-contained archive), RSS (syndication).
- **Files**: `skymarshal/exporters.py` (new)
- **Depends on**: None

---

### 24. Session JWT Token Reuse
- **Source**: geepers recommendations:161 (MEDIUM, 2 hours)
- **Impact**: 3 | **Effort**: 2 | **Priority**: 4.5
- **Description**: Save JWT tokens for reuse to avoid Bluesky's login rate limit (100/day). Currently re-authenticates every session. Add `SessionTokenManager` to cache and validate tokens.
- **Files**: `skymarshal/auth/session_token_manager.py` (new)
- **Depends on**: None

---

## Polish & Documentation

### 25. Update CLAUDE.md: Document Architecture Clearly
- **Source**: geepers recommendations:6 (Previous session: rewrote CLAUDE.md)
- **Impact**: 3 | **Effort**: 2 | **Priority**: 5.0
- **Description**: Add sections: (1) API endpoint reference, (2) Database schema with indexes, (3) Service layer pattern, (4) SocketIO event flows, (5) Rate limiting strategy.
- **Files**: `/home/coolhand/servers/skymarshal/CLAUDE.md`
- **Depends on**: Task #8 (deployment verified), Task #10 (service layer created)

---

### 26. Add Comparison Table: Python vs TypeScript Packages
- **Source**: REPO_AUDIT.md:248-252
- **Impact**: 2 | **Effort**: 1 | **Priority**: 4.0
- **Description**: Create side-by-side comparison in README explaining when to use Python (CLI/backend) vs TypeScript (npm library). Answer "Why two versions?"
- **Files**: `/home/coolhand/servers/skymarshal/README.md`
- **Depends on**: Task #5

---

### 27. License Field Consistency Check
- **Source**: REPO_AUDIT.md:64, 185
- **Impact**: 2 | **Effort**: 1 | **Priority**: 3.5
- **Description**: PyPI metadata shows CC0, but README shows MIT. Verify pyproject.toml/setup.py and fix discrepancy.
- **Files**: `setup.py` or `pyproject.toml`
- **Depends on**: Task #1

---

### 28. Performance Optimization: Long-Running Operation Monitoring
- **Source**: geepers recommendations:67 (LOW, future)
- **Impact**: 3 | **Effort**: 3 | **Priority**: 3.0
- **Description**: Add progress tracking/monitoring for long-running ops (bulk delete, CAR download, network fetch). Use SocketIO for real-time UI updates.
- **Files**: `skymarshal/api/blueprints/content.py` (extend), React progress components
- **Depends on**: Task #10 (service layer), Task #12 (React UI)

---

## Statistics

| Category | Count |
|----------|-------|
| High priority (>6) | 8 |
| Medium priority (4-6) | 14 |
| Low priority (<4) | 6 |
| Quick wins (Effort ≤2) | 8 |
| Medium effort (Effort 2-3) | 14 |
| High effort (Effort ≥4) | 6 |

---

## Recommended Work Sequence

**Phase 1: Stabilization (Session 1 - 3-4 hours)**
1. Task #8: Verify production deployment (Caddy, service manager)
2. Task #1: README polish (remove WIP, fix license)
3. Task #3: Remove broken bsky-follow-analyzer link
4. Task #2: Extract auth decorator (DRY)

**Phase 2: API Polish (Session 2 - 4-5 hours)**
5. Task #7: Add OpenAPI/Swagger spec
6. Task #6: Create shared JSON schema
7. Task #15: Add API versioning
8. Task #16: Standardize response envelope

**Phase 3: React Integration (Session 3 - 6-8 hours)**
9. Task #12: Build React UI layer (follower analysis, cleanup, network)
10. Task #9: E2E testing (React → Flask)
11. Task #13: CAR file download wiring

**Phase 4: Feature Consolidation (Sessions 4-5 - 8-10 hours)**
12. Task #21: Follower workflow consolidation
13. Task #22: Bot detection expansion
14. Task #14: Nuclear deletion mode
15. Task #10: Service layer abstraction

**Phase 5: Polish & Release (Session 6 - 4-5 hours)**
16. Task #25: Update CLAUDE.md
17. Task #11: Database optimization
18. Task #24: JWT token reuse
19. Task #5: Cross-package documentation

---

## Known Issues & Dependencies

**Deployment Verification Needed** (Task #8):
- Caddy routing from Express (3001) to Flask (5050) - ASSUMED working, needs verification
- Service manager registration - ASSUMED done, needs verification
- Socket.IO path stripping - ASSUMED done, needs verification

**API Quality Baseline**:
- 35 routes exist but no OpenAPI spec
- Response format inconsistency
- No input validation (manual checks)
- Auth guard duplication (7 blueprints × 12 lines)

**Frontend Integration Gaps**:
- React app has Vite proxy configured but uses only 5-10 of 35 API routes
- No UI for: follower analysis, cleanup candidates, network graph
- No real-time progress tracking for long ops

---

## Success Metrics

- **Deployment**: Service starts/stops cleanly, health endpoint responds, logs are informative
- **API Quality**: OpenAPI spec generated, 100% endpoint coverage
- **React Integration**: All 35 API endpoints consumable from UI, E2E tests passing
- **Code Quality**: No duplicate auth logic, service layer handles all domain access
- **Performance**: Index queries run in <50ms, bulk ops show progress in real-time

---

**Report Generated**: 2026-02-14 14:25 by Claude Planner
**Next Review**: After Task #8 deployment verification
**Owner Contact**: Luke Steuber (@lukesteuber.com)

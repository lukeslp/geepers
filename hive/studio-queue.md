# Task Queue: studio

**Generated**: 2026-02-19 17:20
**Project**: Studio (Multi-Provider LLM Interface)
**Last Active Commit**: cc70a79 (2026-02-19 17:06)
**Total Tasks**: 11
**Quick Wins**: 3
**Blocked**: 2
**Deferred**: 2

---

## Executive Summary

Studio is in **MAINTENANCE MODE** with critical dependency updates required. The application is functionally complete with chat, image generation, video generation, vision analysis, TTS, and Swarm Portal with multi-agent search. Two features are partially implemented (task persistence and chat history), and dependency versions are significantly outdated. No critical bugs reported, but security and compatibility issues exist.

---

## Ready to Build (Priority Order)

### 1. [QW] Update Core LLM SDK Versions
- **Source**: `geepers/recommendations/by-project/studio.md` (HIGH PRIORITY)
- **Impact**: 5 | **Effort**: 2 | **Priority**: 8.0
- **Description**: Update anthropic (0.18.0 → 0.40.0), openai (1.0.0 → 1.57.0), google-generativeai (0.3.0 → 0.8.3), and cohere (5.0.0 → 5.12.0). These are multiple major versions behind and may have breaking changes.
- **Files**: `requirements.txt`, `providers/studio_adapters.py` (test interface)
- **Depends on**: None
- **Severity**: Critical (security + compatibility)
- **Testing**: Chat endpoints, vision capabilities, image generation, error handling, response formats

### 2. [QW] Pin All Dependencies in requirements.txt
- **Source**: `geepers/recommendations/by-project/studio.md`
- **Impact**: 4 | **Effort**: 1 | **Priority**: 7.0
- **Description**: Replace `>=` version specifiers with pinned versions (==). Current unpinned deps risk breaking on next install due to transitive dependencies.
- **Files**: `requirements.txt`
- **Depends on**: Task #1 (update versions first)
- **Severity**: High (reproducibility + deployability)
- **Estimate**: 30 min

### 3. [QW] Create requirements-dev.txt
- **Source**: `geepers/recommendations/by-project/studio.md`
- **Impact**: 3 | **Effort**: 1 | **Priority**: 6.0
- **Description**: Add dev/test dependencies: pytest, pytest-cov, black, ruff, mypy, httpx. Enables testing and code quality workflows.
- **Files**: New file `requirements-dev.txt`
- **Depends on**: None
- **Severity**: Low
- **Estimate**: 15 min

### 4. Implement Task Definition Loading from YAML
- **Source**: `blueprints/hive.py:65` (TODO comment)
- **Impact**: 4 | **Effort**: 3 | **Priority**: 5.0
- **Description**: Load task definitions from `swarm_tasks.yaml` instead of returning empty task list. Currently `/hive/tasks` endpoint returns placeholder. Requires YAML schema design and parsing.
- **Files**: `blueprints/hive.py` (update `list_tasks()` func), new file `swarm_tasks.yaml`
- **Depends on**: None
- **Note**: Blocked until YAML spec is defined for Hive tasks

### 5. Implement Chat History Persistence
- **Source**: `blueprints/chat.py:247` (TODO comment)
- **Impact**: 3 | **Effort**: 4 | **Priority**: 3.0
- **Description**: Move conversation history from in-memory dict to persistent storage. Required for `/chat/history` endpoint. Current conversation lost on restart.
- **Files**: `blueprints/chat.py`, `database.py` (configure SQLite), `core/streaming.py` (update history handling)
- **Depends on**: Database schema defined
- **Note**: Blocked until persistence layer design is approved. Currently configured but unused: `swarm_portal.db`

### 6. Add Security Vulnerability Scanning
- **Source**: `geepers/recommendations/by-project/studio.md`
- **Impact**: 4 | **Effort**: 1 | **Priority**: 4.5
- **Description**: Run `pip-audit` and `safety check` against requirements to identify CVEs. Add to pre-commit hooks.
- **Files**: Create `.pre-commit-config.yaml`
- **Depends on**: Task #1 (update SDKs first to reduce false positives)
- **Estimate**: 20 min

### 7. Add Development Test Suite
- **Source**: Best practice gap
- **Impact**: 3 | **Effort**: 4 | **Priority**: 3.5
- **Description**: Write unit tests for provider adapters, streaming pipeline, cache manager, and error handling. Start with `tests/test_providers.py`.
- **Files**: New dir `tests/`, `conftest.py`, test files
- **Depends on**: Task #3 (pytest in requirements-dev.txt)
- **Estimate**: 2-3 hours

### 8. Establish Automated Dependency Updates
- **Source**: Best practice (long-term maintenance)
- **Impact**: 3 | **Effort**: 2 | **Priority**: 2.5
- **Description**: Set up Dependabot or Renovate for quarterly security audits and automated PR creation for dependency updates.
- **Files**: `.github/dependabot.yml` or `renovate.json`
- **Depends on**: Task #1, #2 (pinned versions required first)
- **Estimate**: 1 hour

### 9. Refactor Shared Library Editable Install
- **Source**: `geepers/recommendations/by-project/studio.md` (medium-term)
- **Impact**: 3 | **Effort**: 5 | **Priority**: 2.0
- **Description**: Current `-e /home/coolhand/shared[all]` makes deployment complex (requires filesystem access). Options: package as proper PyPI package, publish to private registry, or use git+https URLs. Architectural decision required.
- **Files**: `requirements.txt`, deployment scripts
- **Depends on**: Task #2 (after pinning)
- **Note**: Blocks cloud deployments; deferred unless migration is planned

### 10. Document Deployment Procedure with Editable Install
- **Source**: Best practice gap
- **Impact**: 2 | **Effort**: 1 | **Priority**: 1.5
- **Description**: Add deployment guide to README noting filesystem requirement for `-e /home/coolhand/shared`. Clarify production vs. dev setup.
- **Files**: `README.md`
- **Depends on**: None
- **Estimate**: 30 min

### 11. Clean Up Archived Cruft Directory
- **Source**: `geepers/recommendations/by-project/studio.md` (cleanup task)
- **Impact**: 1 | **Effort**: 1 | **Priority**: 0.5
- **Description**: Remove or move `ARCHIVED_CRUFT_2026-01-12/` to external storage. Contains old datavis projects, node_modules (360+ files), and stale documentation.
- **Files**: `ARCHIVED_CRUFT_2026-01-12/`
- **Depends on**: None
- **Note**: Low priority; cleanup task
- **Estimate**: 15 min (if just removing)

---

## Blocked Tasks

### Task #4: Implement Task Definition Loading
- **Blocked by**: YAML task specification not yet defined
- **Reason**: Requires consensus on Hive task schema (parameters, tools mapping, execution flow)
- **Unblock when**: `swarm_tasks.yaml` schema is agreed upon and documented

### Task #5: Implement Chat History Persistence
- **Blocked by**: Database schema and persistence layer design not approved
- **Reason**: Current `database.py` is configured but unused; needs schema design and ORM setup decision
- **Unblock when**: Database architecture is documented and approved

---

## Deferred (Low Priority / Medium-Term)

### Task #9: Refactor Shared Library Dependency
- **Priority**: 2.0
- **Reason**: Important for deployment, but only blocks if migrating to cloud
- **Action**: Schedule for post-deployment phase

### Task #10: Document Deployment with Editable Install
- **Priority**: 1.5
- **Reason**: Low-impact docs update; helpful but not urgent
- **Action**: Schedule after core dependency updates complete

---

## Statistics

| Category | Count |
|----------|-------|
| High priority (>6.0) | 4 |
| Medium priority (3.0-6.0) | 5 |
| Low priority (<3.0) | 2 |
| **Quick wins** | 3 |
| **Blocked** | 2 |
| **Deferred** | 2 |

---

## Priority Justification

### Why Update SDKs First (Task #1)
- **Security**: Outdated SDKs may have known CVEs
- **Compatibility**: Breaking changes in latest versions may cause runtime failures
- **Unblocks**: Dependency pinning, security scanning, test suite
- **Risk**: High impact if not addressed; affects all LLM interactions

### Why Pin Versions (Task #2)
- **Deployability**: Ensures reproducible builds across environments
- **Stability**: Prevents transitive dependencies from breaking the build
- **Unblocks**: Production deployments, automated updates
- **Effort**: Trivial once SDKs are updated

### Why Dev Dependencies Matter (Task #3)
- **Testing**: Enables comprehensive test suite (Task #7)
- **Code Quality**: pytest, black, ruff, mypy for CI/CD integration
- **Maintenance**: Makes it easier for contributors
- **Effort**: Minimal; just documenting existing best practices

### Why Chat History is Deferred (Task #5)
- **Impact**: Nice-to-have feature; not critical for core functionality
- **Effort**: Significant (requires database design + schema migration)
- **Blockers**: Persistence layer not yet defined
- **Alternative**: Can be added in future sprint without blocking other work

---

## Implementation Notes

### SDK Update Risks
- **Anthropic 0.18.0 → 0.40.0**: Check vision API parameter changes
- **OpenAI 1.0.0 → 1.57.0**: May deprecate old chat completion fields
- **Google Generative AI 0.3.0 → 0.8.3**: Significant version jump; test thoroughly
- **Cohere 5.0.0 → 5.12.0**: Check streaming response format changes

All provider adapters in `providers/studio_adapters.py` should be tested post-update.

### Testing Strategy (Post-Update)
1. Test each provider's chat endpoint
2. Test image generation (OpenAI + xAI)
3. Test vision analysis (Anthropic + OpenAI)
4. Test TTS (ElevenLabs + OpenAI)
5. Test error handling for invalid API calls
6. Test response parsing for all models

### Deployment Checklist
- [ ] Update SDKs and pin versions
- [ ] Run security scanning
- [ ] Update README with deployment notes
- [ ] Test all provider endpoints
- [ ] Verify cache manager compatibility
- [ ] Test Caddy reverse proxy routing
- [ ] Monitor logs for errors post-deployment

---

## File Summary

**Modified Files (Post-Update)**:
- `requirements.txt` - Pin all versions
- `requirements-dev.txt` - New dev dependencies
- `providers/studio_adapters.py` - Test for API changes
- `blueprints/hive.py` - Load YAML tasks (blocked)
- `blueprints/chat.py` - Persistence layer (blocked)
- `README.md` - Deployment guide

**No Breaking Changes Expected**:
- `app.py` - Provider initialization handles failures gracefully
- `core/` modules - Should work with updated SDKs
- `templates/` - No changes needed
- `static/` - No changes needed

---

## Next Steps

1. **Immediately** (This Session):
   - [ ] Task #1: Update SDK versions and test basic functionality
   - [ ] Task #2: Pin all dependencies
   - [ ] Task #3: Create requirements-dev.txt

2. **This Week**:
   - [ ] Task #6: Add security scanning
   - [ ] Task #7: Create test suite
   - [ ] Task #10: Document deployment

3. **Next Sprint**:
   - [ ] Task #4: Load YAML task definitions (awaiting schema)
   - [ ] Task #5: Implement chat history (awaiting DB design)
   - [ ] Task #9: Refactor shared library (if cloud migration planned)

---

## Commit Message Template

```
chore(deps): update LLM SDKs to latest versions

- anthropic: 0.18.0 → 0.40.0
- openai: 1.0.0 → 1.57.0
- google-generativeai: 0.3.0 → 0.8.3
- cohere: 5.0.0 → 5.12.0

Also pin all transitive dependencies for reproducibility.

Fixes: Outdated SDKs, missing version pinning
Tests: All provider endpoints verified
Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

---

*Generated by geepers_planner on 2026-02-19*
*Analysis includes: git log (15 commits), CLAUDE.md, requirements.txt, code comments, recommendations*

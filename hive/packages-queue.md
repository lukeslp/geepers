# Task Queue: Python Packages Collection

**Generated**: 2026-02-19 18:00
**Total Packages**: 13
**Published to PyPI**: 11
**Local-only Packages**: 3
**Total Tasks**: 18

---

## Quick Summary

### Packages Overview

| Package | Version | Status | Key Issue |
|---------|---------|--------|-----------|
| cleanupx | 2.0.2 | Production | Tests not configured, needs test coverage |
| fileherder | 1.0.0 | Stable | Has tests (core, operations) |
| reference-renamer | 0.1.0 | Development | Tests configured but not implemented |
| citewright | 0.1.1 | Development | Tests configured but not implemented |
| llm-providers | 0.1.0 | Development | Tests configured but not implemented |
| research-data-clients | 0.1.0 | Development | Tests configured but not implemented |
| multi-agent-orchestration | 1.0.2 | Stable | Tests configured but not implemented |
| bluesky-cli | 0.1.1 | Development | No test config |
| todoist-toolkit | 0.1.1 | Development | No test config |
| porkbun-cli | 1.0.0 | Beta | Local only (name taken on PyPI) |
| smart-rename | 0.1.0 | Beta | Local only (name taken on PyPI) |
| slashbash | — | Bash only | Not a Python package |

---

## Ready to Build (Priority Order)

### 1. [QW] Fix cleanupx test configuration + implement basic tests
- **Impact**: 4 | **Effort**: 2 | **Priority**: 7
- **Description**: cleanupx has pytest configured in pyproject.toml but no test files exist. Add `test/` with basic tests for core processors (integrated cleanup, XAI API, legacy compatibility).
- **Files**: `/home/coolhand/packages/cleanupx/test/` (create), `pyproject.toml` (verify config)
- **Depends on**: None
- **Note**: Project plan (June 2025) lists "Testing: Add comprehensive test suite" as next step. Module is production-ready but needs verification.

### 2. [QW] Implement reference-renamer tests
- **Impact**: 3 | **Effort**: 2 | **Priority**: 6
- **Description**: Test structure exists (`test_cli.py`, `test_filename_generator.py`) but files are empty placeholders. Implement tests for filename generation, CLI interaction, and async API calls.
- **Files**: `/home/coolhand/packages/reference-renamer/tests/test_*.py`
- **Depends on**: None
- **Note**: Has GitHub Actions workflow; publishing will fail without tests passing. CLI, filename generator, and content extraction are the critical paths.

### 3. [QW] Implement llm-providers test suite
- **Impact**: 4 | **Effort**: 3 | **Priority**: 6.5
- **Description**: Core abstraction layer with no tests. Tests must cover factory pattern singleton behavior, provider initialization, and graceful fallback for missing optional deps. Start with factory tests + one concrete provider (OpenAI or Ollama).
- **Files**: `/home/coolhand/packages/llm-providers/tests/` (create)
- **Depends on**: None
- **Note**: Used by multiple packages in this collection; test coverage is critical for stability.

### 4. [QW] Implement research-data-clients tests
- **Impact**: 3 | **Effort**: 2 | **Priority**: 5.5
- **Description**: 17 API clients with zero test coverage. Use `responses` library (already in dev deps) to mock HTTP calls. Start with 3-4 critical clients (arXiv, Semantic Scholar, Wikipedia) then expand.
- **Files**: `/home/coolhand/packages/research-data-clients/tests/` (create)
- **Depends on**: None
- **Note**: Factory pattern + consistent dataclass returns make testing straightforward.

### 5. [QW] Implement citewright tests
- **Impact**: 3 | **Effort**: 2 | **Priority**: 5.5
- **Description**: Test structure exists but empty. Focus on PDF metadata extraction, filename generation, and BibTeX output. Mock file I/O for safe testing.
- **Files**: `/home/coolhand/packages/citewright/tests/`
- **Depends on**: None
- **Note**: Most complete file-renaming tool in the collection; good candidate for early test implementation.

### 6. Implement multi-agent-orchestration tests
- **Impact**: 4 | **Effort**: 3 | **Priority**: 6
- **Description**: Abstract orchestration patterns need tests for 5 patterns (DreamCascade, DreamSwarm, Sequential, Conditional, Iterative). Test streaming callbacks, cost tracking, and pattern-specific behavior.
- **Files**: `/home/coolhand/packages/multi-agent-orchestration/tests/`
- **Depends on**: None
- **Note**: No concrete implementations provided; tests should use mock providers.

### 7. Version bump: fileherder 1.0.0 → 1.0.1 (patch)
- **Impact**: 2 | **Effort**: 1 | **Priority**: 4
- **Description**: Package is stable and published. Minor fixes or dependency updates warrant 1.0.1 patch release.
- **Files**: `/home/coolhand/packages/fileherder/fileherder/__init__.py`
- **Depends on**: None
- **Note**: Check git history for unreleased changes since 1.0.0 publication.

### 8. Version bump: cleanupx 2.0.2 → 2.1.0 (minor feature)
- **Impact**: 2 | **Effort**: 1 | **Priority**: 3.5
- **Description**: Current version 2.0.2 has integrated processors, XAI API, legacy compatibility. Next minor release should include test suite completion + any pending enhancements.
- **Files**: `/home/coolhand/packages/cleanupx/cleanupx_core/__init__.py`
- **Depends on**: Task #1 (add tests)
- **Note**: Consider releasing once test suite reaches 70%+ coverage.

---

## Deferred (Low Priority / Local-only)

### porkbun-cli (local only)
- **Reason**: PyPI name owned by another author. Keep locally until public API stabilizes or consider namespace change.
- **Has pytest config**: Yes, ready for test implementation if needed

### smart-rename (local only)
- **Reason**: PyPI name taken. Predecessor to `citewright`. Consider archiving or consolidating with citewright.

### slashbash (bash, not Python)
- **Reason**: Not a Python package; managed separately via `./install.sh`.

### bluesky-cli (0.1.1)
- **Reason**: Early development stage, no test infrastructure. Defer until public API stabilizes.

### todoist-toolkit (0.1.1)
- **Reason**: Simple wrapper around existing API. Minimal test value; defer unless feature-rich.

---

## Statistics

| Category | Count |
|----------|-------|
| High priority (>5.5) | 6 |
| Medium priority (3-5.5) | 2 |
| Low priority (<3) | 4 |
| Quick wins (Impact ≥3, Effort ≤2) | 5 |
| Packages with test config but no tests | 6 |
| Packages with actual test files | 2 |
| Published to PyPI | 11 |
| Local-only packages | 3 |

---

## Recommended Session Plan

### Phase 1: Quick Wins (2-3 hours)
1. **cleanupx**: Create test skeleton + 3-4 basic tests (processor, API, legacy)
2. **reference-renamer**: Implement filename generator tests (simplest path)
3. **Update version**: Commit as 2.1.0 prep

### Phase 2: Core Infrastructure (3-4 hours)
4. **llm-providers**: Factory pattern tests + one provider
5. **research-data-clients**: Mock-based API tests for 3 key clients
6. **Commit & prepare for PyPI validation**

### Phase 3: Polish & Publishing (2-3 hours)
7. **citewright**: PDF extraction tests
8. **multi-agent-orchestration**: Pattern tests
9. **Run full test suite on all packages, prepare changelog entries**
10. **Commit batch: "feat: add comprehensive test suite across packages"**

---

## Notes

- All packages follow modern Python packaging standards (pyproject.toml-first)
- Most use pytest + pytest-cov; consistent test patterns across packages
- Shared library (`~/shared/`) is separate and not included here
- `llm-providers` and `research-data-clients` are foundational; testing them unblocks dependent packages
- See `/home/coolhand/packages/CLAUDE.md` for build/publish commands and PyPI publishing workflow
- System Python 3.10 twine is broken; always use `/tmp/twine-env` venv for uploads

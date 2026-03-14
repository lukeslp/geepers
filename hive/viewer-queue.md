# Task Queue: viewer

**Generated**: 2026-03-07 18:30
**Total Tasks**: 18
**Quick Wins**: 4
**Blocked**: 0

---

## Summary

Viewer is a multi-component image management and viewing system combining:
- High-resolution image viewer (HTML/CSS/JS) with pan/zoom
- Imgur API integration for account data fetching
- LLM-powered alt text generation (Flask server)
- Mobile-optimized interfaces

**Status**: Functional but fragmented. Cruft cleanup complete (PROJECT_PLAN.md, ALT_TEXT_SETUP.md, FILE_STRUCTURE_SUMMARY.md deleted). Main work: consolidate architecture, fix requirements.txt bloat, modernize dependencies.

---

## Ready to Build (Priority Order)

### 1. [QW] Consolidate requirements.txt into lean, maintainable file
- **Source**: Code audit - requirements.txt is 135 lines with Anaconda/Conda artifacts
- **Impact**: 4 | **Effort**: 2 | **Priority**: 7
- **Description**: Current requirements.txt contains conda build environment artifacts (anaconda-client, conda-build, setuptools, etc.) that shouldn't be in production. Create clean, minimal requirements split into core (Flask, requests, Pillow) and optional (openai for alt text).
- **Files**: `/home/coolhand/servers/viewer/requirements.txt`
- **Acceptance**: `pip install -r requirements.txt` installs only runtime deps; no build tools, conda, or development artifacts

### 2. [QW] Update CLAUDE.md to remove stale references to deleted docs
- **Source**: CLAUDE.md lines 183-186 still reference PROJECT_PLAN.md, FILE_STRUCTURE_SUMMARY.md, ALT_TEXT_SETUP.md, SUGGESTIONS.md
- **Impact**: 3 | **Effort**: 1 | **Priority**: 6
- **Description**: These files no longer exist (deleted to clear cruft). Remove lines 183-186 that reference them. These sections still appear in the CLAUDE.md "Key Files" area.
- **Files**: `/home/coolhand/servers/viewer/CLAUDE.md`
- **Depends on**: None
- **Acceptance**: CLAUDE.md no longer references deleted documentation files

### 3. [QW] Verify Flask app is properly set up in start_server.py
- **Source**: Code review - start_server.py imports alt_text_server.app but no Flask app exists at entry point
- **Impact**: 3 | **Effort**: 1 | **Priority**: 5.5
- **Description**: start_server.py calls `from alt_text_server import app` but the actual Flask app needs verification. Check if app.py or start.sh exists, or if alt_text_server.py is the true entry point. Document the correct startup command.
- **Files**: `/home/coolhand/servers/viewer/start_server.py`, `/home/coolhand/servers/viewer/alt_text_server.py`
- **Depends on**: Task #1 (clean requirements)
- **Acceptance**: Running `python start_server.py` successfully starts the Flask server on port 5000

### 4. [QW] Update CLAUDE.md to reference shared library pattern
- **Source**: CLAUDE.md mentions hardcoded API keys but no reference to ConfigManager pattern from ~/shared/
- **Impact**: 2 | **Effort**: 1 | **Priority**: 4
- **Description**: Add section documenting how to use `~/shared/config.py` ConfigManager instead of hardcoded API keys. Document environment variable pattern for xAI API key used by alt_gen_master.py.
- **Files**: `/home/coolhand/servers/viewer/CLAUDE.md`
- **Depends on**: None
- **Acceptance**: CLAUDE.md includes ConfigManager usage example; alt_gen_master.py uses secure API key loading

---

## Functional (Medium Priority)

### 5. Refactor image-data.js to extract metadata generation logic (~3.3MB file is unwieldy)
- **Source**: Code analysis - image-data.js is 6351 lines, contains static gallery data
- **Impact**: 4 | **Effort**: 4 | **Priority**: 4
- **Description**: image-data.js mixes static data (3MB+) with small utility functions. This should be split: gallery.json (data only) + image-metadata.js (utility functions). Loader can merge them at runtime if needed. Will improve maintainability and module clarity.
- **Files**: `/home/coolhand/servers/viewer/image-data.js`, `/home/coolhand/servers/viewer/gallery.js`
- **Depends on**: None
- **Acceptance**: Gallery loads identically; metadata operations now in separate module; data is valid JSON

### 6. Consolidate HTML viewers (viewer.html, mobile-viewer.html, index.html) or clarify responsibilities
- **Source**: Code structure - three separate HTML files with overlapping functionality
- **Impact**: 3 | **Effort**: 4 | **Priority**: 3.5
- **Description**: viewer.html (1447 lines), mobile-viewer.html (869 lines), index.html (851 lines) seem to serve similar purposes. Either: (a) merge into single responsive design, (b) clearly document which one is canonical, (c) use feature detection to load appropriate interface. Currently unclear which is the main entry point.
- **Files**: `/home/coolhand/servers/viewer/viewer.html`, `/home/coolhand/servers/viewer/mobile-viewer.html`, `/home/coolhand/servers/viewer/index.html`
- **Depends on**: None
- **Acceptance**: Single clear entry point documented; no duplicate functionality; mobile responsiveness verified

### 7. Verify alt_text_server.py Flask routes and integrate with alt_gen_master.py
- **Source**: Code review - alt_text_server.py defines endpoints but integration with alt_gen_master.py unclear
- **Impact**: 4 | **Effort**: 3 | **Priority**: 4
- **Description**: alt_text_server.py has `/generate-alt` endpoint but how it calls alt_gen_master.py functions needs verification. Check: (1) endpoint signatures, (2) async handling if needed, (3) error handling, (4) integration with image upload flow.
- **Files**: `/home/coolhand/servers/viewer/alt_text_server.py`, `/home/coolhand/servers/viewer/alt_gen_master.py`, `/home/coolhand/servers/viewer/alt-text-client.js`
- **Depends on**: Task #1 (clean requirements)
- **Acceptance**: POST /generate-alt accepts images, returns JSON with alt text; error handling works; integration tested

### 8. Document Imgur API integration flow and verify OAuth2 implementation
- **Source**: CLAUDE.md references imgur_fetch.py but file not found; API integration path unclear
- **Impact**: 3 | **Effort**: 3 | **Priority**: 3.5
- **Description**: CLAUDE.md documents Imgur auth but process_imgur_data.js (326 lines) handles it. Clarify: (1) Is imgur_fetch.py missing or renamed?, (2) Does OAuth2 flow work end-to-end?, (3) Token storage security?, (4) Which file is canonical entry point?
- **Files**: `/home/coolhand/servers/viewer/process_imgur_data.js`, `/home/coolhand/servers/viewer/CLAUDE.md`
- **Depends on**: None
- **Acceptance**: Imgur OAuth2 flow documented; canonical entry point identified; token handling reviewed for security

---

## Code Quality (Lower Priority)

### 9. Fix hardcoded URL references in viewer.html and related files
- **Source**: Code review - og:image URLs hardcoded (https://i.imgur.com/, https://actuallyusefulai.com/)
- **Impact**: 3 | **Effort**: 2 | **Priority**: 3
- **Description**: Meta tags in viewer.html reference hardcoded domains. These should be environment-aware or parameterized for deployment flexibility. Also check for hardcoded paths in manifest.json references.
- **Files**: `/home/coolhand/servers/viewer/viewer.html`, `/home/coolhand/servers/viewer/index.html`, `/home/coolhand/servers/viewer/mobile-viewer.html`
- **Depends on**: None
- **Acceptance**: Meta tags use environment variables or config-driven URLs; Caddy routing path preserved (/viewer/*)

### 10. Verify CSS dependencies and consolidate style files (5 CSS files)
- **Source**: Code audit - styles.css, index_styles.css, style_guide.css, swiss-chat.css referenced
- **Impact**: 2 | **Effort**: 2 | **Priority**: 2
- **Description**: Multiple CSS files exist; verify: (1) Which is the primary stylesheet?, (2) Are there conflicts or duplicates?, (3) Is style_guide.css actually used?, (4) Can styles be consolidated?
- **Files**: `/home/coolhand/servers/viewer/styles.css`, `/home/coolhand/servers/viewer/index_styles.css`, `/home/coolhand/servers/viewer/style_guide.css`
- **Depends on**: Task #6 (consolidate HTML)
- **Acceptance**: Primary stylesheet identified; unused styles removed; one source of truth for styling

### 11. Add TypeScript-style JSDoc comments to viewer.js and gallery.js
- **Source**: Code best practices - viewer.js (1442 lines) and gallery.js (308 lines) lack doc comments
- **Impact**: 2 | **Effort**: 3 | **Priority**: 2
- **Description**: Add JSDoc comments documenting function signatures, parameters, return types for maintainability. Focus on public API functions first (zoom, pan, gallery navigation). This improves code readability without needing TypeScript migration.
- **Files**: `/home/coolhand/servers/viewer/viewer.js`, `/home/coolhand/servers/viewer/gallery.js`
- **Depends on**: None
- **Acceptance**: All public functions have JSDoc comments; types are documented

### 12. Verify EXIF parsing is implemented in alt_gen_master.py or needs addition
- **Source**: CLAUDE.md mentions EXIF support but implementation unclear
- **Impact**: 2 | **Effort**: 2 | **Priority**: 2
- **Description**: CLAUDE.md claims EXIF parsing but Pillow import check in alt_gen_master.py may not extract it. Verify: (1) Does Pillow._getexif() work?, (2) Is EXIF data exposed to alt text generation?, (3) Should EXIF metadata be cached?
- **Files**: `/home/coolhand/servers/viewer/alt_gen_master.py`
- **Depends on**: None
- **Acceptance**: EXIF parsing tested; metadata available to alt text generation; error handling for files without EXIF

### 13. Create ./test/ directory with basic smoke tests
- **Source**: No tests present; project lacks test coverage
- **Impact**: 2 | **Effort**: 3 | **Priority**: 2
- **Description**: Add minimal tests: (1) Can Flask server start?, (2) Do /health and /generate-alt endpoints exist?, (3) Does image data load in browser?, (4) Imgur API auth flow testable? Start with pytest fixtures for setup.
- **Files**: Create `/home/coolhand/servers/viewer/tests/` directory
- **Depends on**: Task #1 (clean requirements), Task #3 (verify Flask setup)
- **Acceptance**: `pytest` runs and passes; test_start_server.py, test_api_endpoints.py created

---

## Technical Debt & Cleanup

### 14. Remove test/debug files: tester.html
- **Source**: Code audit - tester.html (1390 lines) appears to be a testing interface
- **Impact**: 1 | **Effort**: 1 | **Priority**: 1.5
- **Description**: Verify tester.html is not used in production. If it's a dev-only tool, move to tests/ directory or document its purpose. Currently appears to be dead code cluttering the root.
- **Files**: `/home/coolhand/servers/viewer/tester.html`
- **Depends on**: None
- **Acceptance**: tester.html either documented as essential, moved to tests/, or removed

### 15. Clean up --backups and --storage directories
- **Source**: Directory structure - --backups/ (Mar 7 modified), --storage/ (3.3MB) exist with unclear purpose
- **Impact**: 1 | **Effort**: 1 | **Priority**: 1
- **Description**: Verify --backups/ and --storage/ are not stale. If they're runtime-generated, add to .gitignore. If they contain static data, clarify purpose. Currently they clutter repo and look like temporary directories.
- **Files**: `/home/coolhand/servers/viewer/.gitignore`, `/home/coolhand/servers/viewer/--backups/`, `/home/coolhand/servers/viewer/--storage/`
- **Depends on**: None
- **Acceptance**: Purpose documented in README or CLAUDE.md; .gitignore updated if runtime-generated

### 16. Verify .cursorignore is necessary and correct
- **Source**: File present - .cursorignore exists but purpose unclear for this project
- **Impact**: 1 | **Effort**: 1 | **Priority**: 1
- **Description**: .cursorignore (19 bytes) present but viewer project may not need it or may need updating. Verify it's not blocking access to needed files.
- **Files**: `/home/coolhand/servers/viewer/.cursorignore`
- **Depends on**: None
- **Acceptance**: .cursorignore reviewed and either justified or removed

---

## Deferred (Low Priority / Out of Scope)

### 17. Implement advanced features (annotations, comparison mode)
- **Priority**: 0.5
- **Reason**: Nice-to-have; requires significant architecture work
- **Note**: Listed in original PROJECT_PLAN.md but not critical for MVP

### 18. Performance optimization for very large images (>100MB)
- **Priority**: 0.5
- **Reason**: Edge case; current approach works for typical gallery images
- **Note**: Would require progressive loading, streaming, or tile-based rendering

---

## Statistics

| Category | Count |
|----------|-------|
| High priority (>5) | 6 |
| Medium priority (3-5) | 7 |
| Low priority (<3) | 5 |
| Quick wins | 4 |
| Blocked | 0 |

---

## Cruft Cleanup Complete

The following files have been successfully deleted:
- `PROJECT_PLAN.md` (deleted)
- `ALT_TEXT_SETUP.md` (deleted)
- `FILE_STRUCTURE_SUMMARY.md` (deleted)
- `SUGGESTIONS.md` (not found, assumed cleaned earlier)

**Next Step**: Update CLAUDE.md to remove references to these deleted files (Task #2).

---

## Next Actions

1. **Start with Quick Wins** (Tasks 1-4): 15-30 minutes total
   - Clean requirements.txt
   - Update CLAUDE.md references
   - Verify Flask startup
   - Add ConfigManager documentation

2. **Then Consolidation Work** (Tasks 5-7): 3-4 hours
   - Refactor image-data.js
   - Consolidate HTML viewers
   - Verify alt text integration

3. **Document & Commit**: After each block, commit with proper messages

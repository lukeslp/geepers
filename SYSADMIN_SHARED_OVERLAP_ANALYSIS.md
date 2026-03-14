# Search Results: Overlaps Between ~/sysadmin-scripts and ~/shared/

**Date**: 2026-03-07
**Searcher**: Claude Code
**Task**: Identify overlapping functionality, duplicated utilities, and superseded scripts

---

## Executive Summary

**Finding**: 4 major functional areas show partial overlap or potential consolidation opportunities. Most critically, **Bluesky client functionality exists in sysadmin-scripts but not in shared's extensible client infrastructure**.

### Overlap Categories:
1. **ZERO Overlap** — Archive management (different domains)
2. **Medium Overlap** — File utilities (bash vs Python)
3. **Low Overlap** — Document parsing (superset relationship)
4. **NO Overlap** — Data validation (different scopes)
5. **GAP** — Bluesky data fetching (should be in shared)
6. **No Overlap** — YouTube operations (different capabilities)
7. **Unique** — Humanization (only in shared)

---

## 1. ARCHIVE MANAGEMENT - DIFFERENT DOMAINS (NO OVERLAP)

### In sysadmin-scripts:
- `/home/coolhand/sysadmin-scripts/create_protected_archive.sh`
- `/home/coolhand/sysadmin-scripts/list_archives.sh`
- `/home/coolhand/sysadmin-scripts/remove_archive.sh`
- `/home/coolhand/sysadmin-scripts/compress_archive.sh`
- `/home/coolhand/sysadmin-scripts/archive_maintenance.sh`

### In ~/shared/:
- **`/home/coolhand/shared/data_fetching/archive_client.py`** (551 lines)
  - `ArchiveClient` class for Internet Archive / Wayback Machine
  - Methods: `get_latest_snapshot()`, `archive_url()`, `get_snapshot_at_timestamp()`, `get_all_snapshots()`
  - `MultiArchiveClient` supporting wayback, archiveis, memento, 12ft providers

- **`/home/coolhand/shared/tools/archive_tool.py`** (145 lines)
  - MCP-compatible tool interface

### Analysis:
- **sysadmin-scripts**: Manages **local filesystem archives** (tar, zip, compression)
- **shared**: Queries **web archives** (Wayback Machine snapshots, URL history)
- **VERDICT**: ✓ No overlap — completely different domains

---

## 2. FILE UTILITIES & FILESYSTEM OPERATIONS - COMPLEMENTARY

### In sysadmin-scripts:
- `safe_cleanup.sh` — Safe file deletion with confirmation
- `cleanup_guard.sh` — Protects critical directories
- `backup_redundancy.sh` — Verifies backup integrity
- Various .sh scripts using standard Unix tools

### In ~/shared/:
- **`/home/coolhand/shared/utils/file_utils.py`** (394 lines)
  - `format_size(bytes)` — Format bytes to human-readable (B, KB, MB, GB, TB, PB)
  - `format_timestamp(timestamp)` — Unix timestamp to YYYY-MM-DD HH:MM:SS
  - `calculate_hash(filepath, algorithm, chunk_size)` — SHA256, MD5, SHA1, SHA512 support
  - `get_file_type(filepath)` — Categorize 50+ file formats
  - `get_file_info(filepath, include_hash)` — Comprehensive metadata dict
  - `get_directory_info(dirpath, recursive)` — Directory stats + file type breakdown
  - `find_files_by_extension(dirpath, extension, recursive)` — Glob-based file discovery
  - `get_file_age_days(filepath)` — Calculate file age in days
  - `ensure_directory(dirpath)` — Safe mkdir -p equivalent
  - `safe_filename(filename, replacement)` — Sanitize problematic characters

### Analysis:
- **sysadmin-scripts** uses **bash** (shell operations at OS level)
- **shared** uses **Python** (API/library operations)
- **Functional overlap**:
  - File size formatting (sysadmin uses shell commands; shared has Python function)
  - File discovery (sysadmin uses find/glob; shared has Python wrapper)
  - Safe directory creation (both provide this)
  - File age checks (sysadmin uses `find -mtime`; shared uses Python)
- **VERDICT**: ✓ Complementary — not duplicated. Use shared for Python projects; keep bash for shell automation.

---

## 3. DOCUMENT PARSING & TEXT ANALYSIS - SUPERSET RELATIONSHIP

### In sysadmin-scripts:
- `renamers/rename_academic_pdfs.py` — Extract metadata from PDF to rename files
- `low-hanging-fruit-scanner.py` — Scan code for quality issues
- `low-hanging-fruit-fixer.py` — Auto-fix common issues

### In ~/shared/:
- **`/home/coolhand/shared/utils/document_parsers.py`** (844 lines)
  - Supported formats: PDF, DOCX, DOC, ODT, RTFD, XLSX, XLS, ODS, CSV, TSV, HTML, JSON, JSONL, YAML, TOML, IPYNB, EMAL, MSG, MBOX, ZIP, TAR, 7Z, RAR, and 30+ code file types
  - `parse_file(filepath)` — Universal parser returning {content, metadata, type}
  - `is_supported_file(filepath)` — Format detection
  - Archive inspection (extracts text from ZIP/TAR/7Z)
  - Code parsing with syntax preservation
  - Metadata: page counts, cell ranges, line counts, encoding

- **`/home/coolhand/shared/doc_humanizer.py`** (340+ lines)
  - `DocumentHumanizer` class detecting AI writing patterns:
    - Corporate jargon (15+ words)
    - Passive voice construction
    - Hedge phrases
    - Em-dash overuse
    - Superlatives
    - Weak modifiers
  - Confidence-based matching with transformation suggestions
  - Line-level detection with context

- **`/home/coolhand/shared/batch_humanize_docs.py`** (batch processor)
  - Discovers files in batches
  - Targets: assessments, READMEs, HTML docs, public docs
  - Git integration for safe processing

- **`/home/coolhand/shared/document_generation/pdf_generator.py`** (PDF creation)
  - `PDFGenerator` class using ReportLab
  - Creates professional PDFs from structured content sections
  - Supports metadata, styling, page breaks

### Analysis:
- `rename_academic_pdfs.py` — **Extracts PDF metadata for filename** (narrow, specific)
- `document_parsers.py` — **Parses 50+ formats extracting all content** (superset includes PDF)
- `low-hanging-fruit-*.py` — **Code quality scanning** (different domain entirely)
- `doc_humanizer.py` — **Writing quality analysis** (different focus: AI detection vs code issues)
- **VERDICT**: ⚠ `document_parsers.py` could replace `rename_academic_pdfs.py` functionality, but code quality scanning is orthogonal. Low practical overlap since they solve different problems.

---

## 4. DATA VALIDATION & SCHEMA CHECKING - DIFFERENT SCOPE

### In sysadmin-scripts:
- `validate_claude_md.py` — Validates CLAUDE.md file structure (domain-specific)

### In ~/shared/:
- **`/home/coolhand/shared/utils/data_validation.py`** (100+ lines)
  - Generic validation utilities:
    - `ValidationError`, `SchemaValidationError` exceptions
    - `ensure_fields(data, required_fields)` — Require non-null fields
    - `validate_choices(data, field, choices)` — Enum validation
    - `validate_schema(data, schema)` — JSON-schema-like validation
    - `coerce_types(data, types)` — Type coercion

### Analysis:
- `data_validation.py` is **lightweight, generic schema validation** (reusable for any data)
- `validate_claude_md.py` is **domain-specific CLAUDE.md structure** (one-off use case)
- **VERDICT**: ✓ No overlap — `validate_claude_md.py` is specialized; `data_validation.py` is generic infrastructure.

---

## 5. DATA FETCHING CLIENTS - ARCHITECTURAL GAP

### In sysadmin-scripts:
- **`/home/coolhand/sysadmin-scripts/bluesky_export_kaggle.py`** — Exports Bluesky data to Kaggle
  - Uses AT Protocol (atproto) library
  - Custom Bluesky-specific logic

### In ~/shared/:
- **`/home/coolhand/shared/data_fetching/`** — 20+ client modules:
  - `archive_client.py`, `arxiv_client.py`, `census_client.py`, `fec_client.py`
  - `finance_client.py`, `github_client.py`, `judiciary_client.py`, `mal_client.py`
  - `nasa_client.py`, `news_client.py`, `openlibrary_client.py`, `pubmed_client.py`
  - `semantic_scholar.py`, `weather_client.py`, `wikipedia_client.py`, `wolfram_client.py`
  - `youtube_client.py`

- **`/home/coolhand/shared/data_fetching/factory.py`** (107 lines)
  - `ClientFactory` pattern: `ClientFactory.create_client('github')` → GitHub client
  - Extensible registry: supports adding new clients

- **`/home/coolhand/shared/data_fetching/__init__.py`**
  - Exports all clients for unified import

### Analysis:
- `bluesky_export_kaggle.py` provides **Bluesky-specific data export** (one-off script)
- **shared has NO Bluesky client** — GAP in infrastructure
- **Architectural mismatch**: Bluesky functionality should live in `shared/data_fetching/bluesky_client.py`
- Surrounding Bluesky infrastructure exists in `/home/coolhand/projects/`, `/home/coolhand/html/firehose/`, `/home/coolhand/servers/` (indicating Bluesky is first-class)
- **VERDICT**: ⚠ **CONSOLIDATION OPPORTUNITY** — Migrate `bluesky_export_kaggle.py` logic to `shared/data_fetching/bluesky_client.py` following the factory pattern. Currently a gap in the extensible infrastructure.

---

## 6. YOUTUBE OPERATIONS - DIFFERENT CAPABILITIES

### In sysadmin-scripts:
- **`/home/coolhand/sysadmin-scripts/youtube_audio_extractor.py`** — Downloads audio from YouTube videos
  - Likely uses yt-dlp for actual download/conversion
  - File-based output

### In ~/shared/:
- **`/home/coolhand/shared/tools/youtube_tool.py`** (130 lines)
  - `YouTubeTools` class with methods:
    - `youtube_search_videos(query, max_results, order, safe_search, video_duration)`
    - `youtube_channel_statistics(channel_id)`
    - `youtube_playlist_items(playlist_id, max_results)`
  - MCP-compatible tool interface

- **`/home/coolhand/shared/data_fetching/youtube_client.py`** (199 lines)
  - Lower-level `YouTubeClient` class
  - Uses YouTube Data API v3
  - Returns JSON data, not file streams

### Analysis:
- `youtube_audio_extractor.py` — **Downloads/extracts media files** (yt-dlp wrapper)
- `youtube_tool.py` — **Searches and retrieves metadata** (YouTube Data API)
- **No overlap** — different capabilities:
  - Extraction = file download/conversion
  - API = data retrieval (search, stats, playlists)
- **VERDICT**: ✓ No overlap — justified separation. Could coexist.

---

## 7. HUMANIZATION & DOCUMENTATION QUALITY - UNIQUE TO SHARED

### In sysadmin-scripts:
- No AI/humanization-specific tools

### In ~/shared/:
- **`/home/coolhand/shared/doc_humanizer.py`** (340+ lines)
  - `DocumentHumanizer` class with 15 detection patterns
  - Detects AI-generated writing markers:
    - Corporate jargon (leverage, robust, streamline, consolidation, etc.)
    - Passive voice (`is X-ed`, `was X-ed`, `has been X-ed`)
    - Hedge phrases (appears to, seems to, might be, could potentially, etc.)
    - Em-dash overuse (>2 per paragraph)
    - Superlatives (absolutely, undoubtedly, certainly)
    - Weak modifiers (somewhat, arguably, tends to)
  - Confidence scoring and transformation suggestions

- **`/home/coolhand/shared/batch_humanize_docs.py`** (batch processor)
  - Discovers documentation in batches (assessments, READMEs, HTML docs)
  - Processes with git integration
  - Generates statistics on transformation types

- **`/home/coolhand/shared/document_generation/pdf_generator.py`**
  - Complements humanizer: generates clean PDFs from processed content

### Analysis:
- **UNIQUE to shared** — sysadmin-scripts has no equivalent
- **Critical infrastructure** for `/humanize` skill mentioned in root CLAUDE.md
- **VERDICT**: ✓ Core shared functionality. No sysadmin-scripts equivalent needed.

---

## 8. TESTING INFRASTRUCTURE - BOTH PRESENT (NON-OVERLAPPING)

### In sysadmin-scripts:
- **`/home/coolhand/sysadmin-scripts/run_tests.py`** — Test runner for sysadmin-scripts
- **`/home/coolhand/sysadmin-scripts/test_shared_imports.py`** (100+ lines)
  - Tests that `from shared.config import ConfigManager` works
  - Tests that `from shared.llm_providers import ProviderFactory, Message` works
  - Tests Studio service integration with shared
  - **Integration validation** between sysadmin-scripts and shared

### In ~/shared/:
- **`/home/coolhand/shared/tests/`** (directory)
  - Unit tests for core shared modules
  - test_data_tool_modules.py, test_document_parsers.py, test_time_utils.py, test_tool_registry.py

- **`/home/coolhand/shared/data_fetching/tests/`** (directory)
  - Per-client test modules:
    - test_archive_client.py, test_arxiv_client.py, test_github_client.py, etc.
  - conftest.py with pytest fixtures
  - test_package_interface.py — Public API tests

### Analysis:
- `run_tests.py` — Tests **sysadmin-scripts** functionality
- `test_shared_imports.py` — Tests **integration** (sysadmin → shared)
- `shared/tests/` — Tests **shared library** itself
- **VERDICT**: ✓ No overlap — different scopes. All three are necessary:
  - Sysadmin tests = sysadmin functionality
  - Integration tests = sysadmin + shared interop
  - Shared tests = shared library quality

---

## 9. GIT OPERATIONS & REPO MANAGEMENT - SEPARATE DOMAIN

### In sysadmin-scripts:
- **`/home/coolhand/sysadmin-scripts/repectomy.py`** (actually bash) — Repository creation
- References to git in cleanup scripts (preserve .git directories, etc.)

### In ~/shared/:
- **No direct git utilities** (intentionally separated)
- MCP servers use `subprocess.run(['git', ...])` for OS-level operations
- Orchestrators coordinate git operations for multi-agent workflows

### Analysis:
- **No overlap** — git is **OS-level system operation**, not library functionality
- sysadmin-scripts manages **system repos** (OS concern)
- shared doesn't duplicate git (correct architectural choice)
- **VERDICT**: ✓ Proper separation — git belongs in sysadmin-scripts

---

## CROSS-REFERENCES: SYSADMIN-SCRIPTS DEPENDS ON SHARED

### Evidence of Dependency:

1. **`safe_cleanup.sh`** (explicit exclusion)
   ```bash
   # Excludes: "/home/coolhand/shared"
   ```
   → Acknowledges shared as critical system component

2. **`bulk_update_gitignore.py`** (special directory handling)
   ```python
   SPECIAL_DIRS = ["shared", ...]  # Protected from modification
   ```
   → Treats shared as infrastructure

3. **`test_shared_imports.py`** (integration validation)
   ```python
   sys.path.insert(0, '/home/coolhand/shared')
   from shared.config import ConfigManager
   from shared.llm_providers import ProviderFactory, Message
   ```
   → Tests that sysadmin can import and use shared

### Key Insight:
**sysadmin-scripts explicitly depends on ~/shared/** (one-directional dependency). The reverse is NOT true (shared doesn't import from sysadmin-scripts).

---

## CONSOLIDATION RECOMMENDATIONS

### 🔴 HIGH PRIORITY (Strategic Value)

1. **Migrate Bluesky to shared**
   - **File**: `bluesky_export_kaggle.py` → `shared/data_fetching/bluesky_client.py`
   - **Pattern**: Follow `YouTubeClient` and `ArchiveClient` patterns
   - **Benefit**: Makes Bluesky accessible to all agents/services via `ClientFactory`
   - **Effort**: Low — simple refactoring
   - **Impact**: High — aligns Bluesky with extensible infrastructure

### 🟡 MEDIUM PRIORITY (Nice-to-Have)

2. **PDF metadata extraction**
   - **Replace**: `renamers/rename_academic_pdfs.py`
   - **With**: `shared.utils.document_parsers.parse_file()` + custom renaming logic
   - **Benefit**: Reduces duplication, uses tested parser
   - **Effort**: Medium
   - **Impact**: Medium — consolidates PDF handling

3. **Code quality scanning as shared tool**
   - **Evaluate**: Can `low-hanging-fruit-scanner.py` become `shared/tools/code_quality_tool.py`?
   - **Benefit**: Accessible to agents/services
   - **Effort**: Medium (requires tool interface wrapping)
   - **Impact**: Medium — expands shared infrastructure

### 🟢 LOW PRIORITY (Keep Separate)

4. **Archive management (bash)** — Shell-specific, justified separation
5. **Cleanup guard (bash)** — Safety-critical, belongs in sysadmin
6. **Git operations** — OS-level, proper separation
7. **YouTube audio extraction** — Different from API clients, justified

---

## SUMMARY TABLE

| Domain | sysadmin-scripts | ~/shared/ | Overlap | Status | Recommendation |
|--------|-----------------|-----------|---------|--------|-----------------|
| Archive (Wayback) | None | archive_client.py | ✗ None | Good | Use shared when needed |
| Archive (local) | .sh scripts | None | ✗ None | Good | Keep separate |
| File Utils | .sh scripts | file_utils.py | ⚠ Medium | Good | Use shared for Python |
| Document Parsing | rename_academic_pdfs.py | document_parsers.py | ⚠ Low | OK | Use shared superset |
| Data Validation | validate_claude_md.py | data_validation.py | ✗ None | Good | Different scopes |
| **Bluesky** | **bluesky_export_kaggle.py** | **None** | **GAP** | **⚠ Issue** | **→ Migrate to shared** |
| YouTube | youtube_audio_extractor.py | youtube_tool.py | ✗ None | Good | Different capabilities |
| Code Quality | low-hanging-fruit-*.py | None | ✗ None | OK | Could migrate |
| Humanization | None | doc_humanizer.py | ✗ None | Good | Use shared |
| Testing | run_tests.py, test_*.py | shared/tests/ | ⚠ Medium | Good | Keep both |
| Git Ops | repectomy.py, cleanup | None | ✗ None | Good | Proper separation |

---

## FILE INVENTORY

### sysadmin-scripts Files Analyzed
```
/home/coolhand/sysadmin-scripts/
├── create_protected_archive.sh
├── list_archives.sh
├── remove_archive.sh
├── compress_archive.sh
├── archive_maintenance.sh
├── safe_cleanup.sh
├── cleanup_guard.sh
├── backup_redundancy.sh
├── bulk_update_gitignore.py
├── low-hanging-fruit-scanner.py
├── low-hanging-fruit-fixer.py
├── renamers/
│   └── rename_academic_pdfs.py
├── validate_claude_md.py
├── bluesky_export_kaggle.py
├── youtube_audio_extractor.py
├── run_tests.py
├── test_shared_imports.py
└── repectomy.py
```

### ~/shared/ Files Analyzed
```
/home/coolhand/shared/
├── data_fetching/
│   ├── archive_client.py (551 lines)
│   ├── arxiv_client.py
│   ├── bluesky_client.py [MISSING - GAP]
│   ├── census_client.py
│   ├── fec_client.py
│   ├── finance_client.py
│   ├── github_client.py
│   ├── judiciary_client.py
│   ├── mal_client.py
│   ├── nasa_client.py
│   ├── news_client.py
│   ├── openlibrary_client.py
│   ├── pubmed_client.py
│   ├── semantic_scholar.py
│   ├── weather_client.py
│   ├── wikipedia_client.py
│   ├── youtube_client.py (199 lines)
│   ├── factory.py (107 lines)
│   └── tests/
│       ├── test_archive_client.py
│       ├── test_arxiv_client.py
│       ├── ... (per-client tests)
│       └── conftest.py
├── doc_humanizer.py (340+ lines)
├── batch_humanize_docs.py
├── document_generation/
│   └── pdf_generator.py
├── utils/
│   ├── file_utils.py (394 lines)
│   ├── document_parsers.py (844 lines)
│   ├── data_validation.py (100+ lines)
│   └── ... (other utilities)
├── tools/
│   ├── archive_tool.py (145 lines)
│   ├── youtube_tool.py (130 lines)
│   └── ... (other tools)
└── tests/
    ├── test_data_tool_modules.py
    ├── test_document_parsers.py
    └── ... (other tests)
```

---

## CONCLUSION

**No critical duplications found.** The two repositories maintain clean separation of concerns:

- **~/sysadmin-scripts** = System administration (bash automation + Python glue)
- **~/shared** = Core library infrastructure (extensible, reusable Python)

**One architectural gap identified**: Bluesky data fetching should be in shared's `ClientFactory` infrastructure, not isolated in sysadmin-scripts.

**Recommendation**: Proceed with migration of Bluesky to shared as high-priority improvement for architectural consistency.

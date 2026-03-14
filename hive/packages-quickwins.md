# Quick Wins: ~/packages/

**Scan Date**: 2026-03-07
**Total Found**: 4
**Completed**: 4
**Remaining**: 0

## Completed Quick Wins

### [Build Config] Remove unused setuptools_scm from reference-renamer
- **File**: `reference-renamer/pyproject.toml:2`
- **Issue**: `setuptools_scm>=6.2` in build-requires but no `[tool.setuptools_scm]` config section; version is hardcoded
- **Fix**: Removed `setuptools_scm>=6.2` from requires list
- **Time**: 2 minutes
- **Impact**: Cleaner build config, removes unnecessary dependency

### [Imports] Fix wrong import path in skymarshal-js analytics README
- **File**: `skymarshal-js/src/utils/analytics/README.md:67,89,101,112,120,144,157`
- **Issue**: All import examples reference `skymarshal-core/utils` but package is `skymarshal`
- **Fix**: Replaced all 8 occurrences of `skymarshal-core/utils` → `skymarshal/utils`
- **Time**: 2 minutes
- **Impact**: Users following examples won't get import errors

### [Gitignore] Add .gitignore to fileherder
- **File**: `fileherder/.gitignore` (created)
- **Issue**: Package missing .gitignore; would commit __pycache__, dist/, .pytest_cache/, etc.
- **Fix**: Created standard Python package .gitignore with coverage patterns
- **Time**: 1 minute
- **Impact**: Prevents accidental commits of build artifacts

### [Gitignore] Add .gitignore to todoist-toolkit
- **File**: `todoist-toolkit/.gitignore` (created)
- **Issue**: Package missing .gitignore; would commit __pycache__, dist/, .pytest_cache/, etc.
- **Fix**: Created standard Python package .gitignore with coverage patterns
- **Time**: 1 minute
- **Impact**: Prevents accidental commits of build artifacts

## Package Status Summary

| Package | .gitignore | pyproject.toml Issues | Import Issues |
|---------|------------|----------------------|----------------|
| bluesky-cli | ✓ | None | None |
| citewright | ✓ | None | None |
| cleanupx | ✓ | None | None |
| fileherder | ✓ (created) | None | None |
| porkbun-cli | ✓ | None | None |
| reference-renamer | ✓ | ✓ Fixed | None |
| skymarshal-js | ✓ | None | ✓ Fixed (8 instances) |
| slashbash | ✗ (bash tool) | N/A | None |
| smart-rename | ✓ | None | None |
| todoist-toolkit | ✓ (created) | None | None |

## Notes

- **fileherder rich import**: Already has try/except guard (lines 16-25 of cli.py) and `rich` is properly marked as optional dependency under `[project.optional-dependencies]` → no changes needed
- **slashbash**: Bash tool, not Python package, doesn't need .gitignore in same way
- No broken imports found in Python code
- No commented-out debug code found
- No obvious typos or spelling errors in READMEs

## Time Summary
- Discovery: 15 minutes
- Implementation: 6 minutes
- **Total session**: 21 minutes
- **Average per fix**: 5.25 minutes

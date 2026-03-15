---
description: Release management - version bump, changelog, publish to PyPI/npm, git tag
---

# Release

Manage the full release lifecycle: version bump, changelog, publish, tag.

## Pre-Release Checks (PARALLEL)

Launch these simultaneously before any release:
1. **@geepers_validator** - Verify project configuration
2. **@geepers_testing** - Run tests, check coverage
3. **@geepers_deps** - Dependency audit, vulnerability check
4. **@geepers_security** - Security scan

## Release Workflow

### 1. Determine Version Bump

Follow semver:
- **patch** (0.1.0 → 0.1.1): Bug fixes, no new features
- **minor** (0.1.0 → 0.2.0): New features, backward compatible
- **major** (0.1.0 → 1.0.0): Breaking changes

Check current version:
```bash
# Python
grep version pyproject.toml setup.py setup.cfg 2>/dev/null
# npm
jq .version package.json 2>/dev/null
```

### 2. Generate Changelog

From git history since last tag:
```bash
git log $(git describe --tags --abbrev=0 2>/dev/null || echo "HEAD~20")..HEAD --oneline --no-merges
```

Format as:
```markdown
## v0.X.Y (YYYY-MM-DD)

### Added
- New feature description

### Changed
- Modified behavior

### Fixed
- Bug fix description
```

### 3. Humanize Gate (MANDATORY)

Before publishing, run **@geepers_humanizer** on:
- README.md (if modified)
- CHANGELOG.md
- Package description in pyproject.toml / package.json
- Any release notes

This catches "AI" terminology and robotic language in public-facing content.

### 4. Bump Version

```bash
# Python (pyproject.toml)
# Edit version field

# npm
npm version patch|minor|major --no-git-tag-version
```

### 5. Build & Publish

**PyPI:**
```bash
# Use clean venv for twine (system Python 3.10 twine is broken)
cd /tmp && python3 -m venv twine-env && source twine-env/bin/activate
pip install build twine
cd /path/to/project
python -m build
twine upload dist/*
```

**npm:**
```bash
npm publish
```

### 6. Git Tag & Push
```bash
git add -A
git commit -m "release: v0.X.Y"
git tag v0.X.Y
git push && git push --tags
```

## Package Registry Reference

| Package | Registry | Current Version |
|---------|----------|-----------------|
| skymarshal | npm | 2.3.0 |
| dr-eamer-ai-shared | PyPI | 1.0.1 |
| geepers-llm | PyPI | 1.0.0 |
| geepers-agents | PyPI | 1.0.2 |
| geepers-core | PyPI | 1.0.2 |
| cleanupx | PyPI | 2.0.2 |
| fileherder | PyPI | 1.0.1 |
| todoist-toolkit | PyPI | 0.1.1 |
| bluesky-cli | PyPI | 0.1.1 |
| citewright | PyPI | 0.1.1 |
| llm-providers | PyPI | 0.1.0 |
| geepers-orchestrators | PyPI | 1.0.2 |
| reference-renamer | PyPI | 0.1.0 |
| research-data-clients | PyPI | 0.1.0 |
| dreamwalker | PyPI | 1.0.1 |

**NOT publishable** (name conflicts): porkbun-cli, smart-rename, geepers (bare)

## Gotchas

- PyPI token is in `~/.pypirc`
- npm token is in `~/.npmrc`
- System Python 3.10 twine is broken - always use `/tmp/twine-env`
- Files >100MB in ANY commit get rejected by GitHub
- Large pushes (300+ commits) need batch pushing

## Execute

**Package/version**: $ARGUMENTS

If no arguments:
- Detect project type from current directory
- Show current version and suggest bump type

If "patch", "minor", or "major":
- Run full release workflow with that bump type

If package name:
- Navigate to that package and start release workflow

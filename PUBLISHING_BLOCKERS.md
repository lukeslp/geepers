# Publishing Blockers - Fix Before Release

## CRITICAL - Package Will Not Work

### 1. Hardcoded /home/coolhand/shared Path
**26 files** have this:
```python
sys.path.insert(0, '/home/coolhand/shared')
```

This breaks pip installs. Choose one fix:
- **A) Bundle**: Copy shared/* into geepers/shared/
- **B) Separate package**: Publish shared to PyPI first
- **C) Optional**: Graceful degradation if not found

### 2. Missing MANIFEST.in
Create this file:
```
include LICENSE
include README.md
include pyproject.toml
recursive-include agents *.md
recursive-include .claude-plugin *.json
```

### 3. Wrong Repository URL
`.claude-plugin/plugin.json` line 11:
```json
"url": "https://github.com/lukeslp/kernel"
```
Should be: `lukeslp/geepers` (or correct repo)

## Test Before Publishing
```bash
python3 -m venv /tmp/test
source /tmp/test/bin/activate
python -m build
pip install dist/*.whl
python -c "from geepers.mcp import UnifiedMCPServer"  # Should work
deactivate
```

## Current Status
- ✗ PyPI: BLOCKED (will fail on install)
- ⚠ Claude Plugin: NEAR READY (just fix repo URL)

Full details: ~/geepers/reports/by-date/2025-12-15/quality-geepers-package.md

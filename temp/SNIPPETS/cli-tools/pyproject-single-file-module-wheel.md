# ================================================
# Single-File Module Wheel Detection Pattern
# ================================================
# Language: toml / bash
# Tags: pypi, packaging, setuptools, wheel, pyproject, py-modules, build
# Source: packages/cleanupx — audit session 2026-03-07
# Last Updated: 2026-03-07
# Author: Luke Steuber
# ================================================
# Description:
# setuptools `packages = find:` silently skips top-level single-file modules
# (e.g. cleanupx.py). The module is never included in the wheel, so the
# installed package imports nothing. The fix is to declare py-modules in
# [tool.setuptools] alongside packages. Always verify wheel contents after
# build with `python3 -m zipfile -l dist/*.whl`.
# ================================================

## The Silent Failure

When a package has both a package directory (cleanupx_core/) and a single
top-level module file (cleanupx.py), setuptools `find:` only discovers the
directory. The .py file is silently omitted from the wheel.

Symptoms:
- `pip install` succeeds
- `import cleanupx` raises ImportError or ModuleNotFoundError
- `python3 -m zipfile -l dist/*.whl` shows no cleanupx.py entry

## Fix: pyproject.toml (setuptools backend)

```toml
[tool.setuptools]
# List discovered package directories
packages = ["cleanupx_core", "cleanupx_core.api", "cleanupx_core.utils"]
# ALSO declare single-file top-level modules explicitly
py-modules = ["cleanupx"]
```

Without `py-modules`, cleanupx.py never enters the wheel even though
`packages = find:` appears to scan everything.

## Fix: setup.cfg equivalent

```ini
[options]
packages = find:
py_modules = cleanupx
```

## Fix: setup.py equivalent

```python
from setuptools import setup, find_packages

setup(
    packages=find_packages(),
    py_modules=["cleanupx"],   # explicitly list single-file modules
)
```

## Verification Command (run after every build)

```bash
python3 -m zipfile -l dist/*.whl | grep -E "\.(py|so)$"
```

Expected output must contain both package files and the bare module:

```
cleanupx_core/__init__.py
cleanupx_core/api/client.py
...
cleanupx.py                   # <-- must appear; if missing, wheel is broken
```

## Hatchling alternative (avoids this class of bug entirely)

Hatchling auto-discovers all .py files without any explicit listing:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

No `[tool.setuptools]` section needed. Preferred for new packages.

# ================================================
# Usage Example:
# ================================================
# After adding py-modules to pyproject.toml:
#
#   python3 -m build
#   python3 -m zipfile -l dist/mypackage-1.0.0-py3-none-any.whl | grep mymodule
#   # Should show: mymodule.py

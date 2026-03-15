---
description: Generate or rewrite a polished, humanized README for any project
---

# README Generator

Create or rewrite a project README with proper badges, structure, and humanized language.

## Execute

Launch **@geepers_readme** with the target project directory.

If no argument is provided, use the current working directory.

### What It Does

1. **Scans the project** — reads CLAUDE.md, package.json, pyproject.toml, setup.py to understand the stack
2. **Checks existing README** — preserves any user-written sections worth keeping
3. **Generates badges** — shields.io badges for language, license, registry, live site
4. **Writes the README** — humanized language, no robot voice, no "AI-powered" buzzwords
5. **Adds attribution** — Luke Steuber credit block with links

### Humanization Rules (Enforced)

- No "AI-powered", "AI-enhanced", "AI-driven" — describe what it does instead
- No "leverages", "utilizes", "facilitates" — use "uses", "helps", "runs"
- No "seamless", "robust", "cutting-edge" — just say what it does
- First person ("I built this because..."), not "we"
- Specific over vague ("generates lesson plans in 30 seconds" not "streamlines educational workflows")

### Structure

1. Project name + one-line description
2. Badges (language, license, registry, live site)
3. Screenshot / demo link (if available)
4. Features (verb phrases, scannable)
5. Quick Start (copy-pasteable)
6. Usage (real examples)
7. Configuration (only if meaningful)
8. Author block + MIT license

## Arguments

- Project path or name (optional — defaults to cwd)

## Examples

```
/geepers:readme
/geepers:readme ~/projects/wordblocks
/geepers:readme geepers-mcp
```

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

Geepers is a Claude Code plugin providing 70+ specialized markdown-defined agents, packaged skills, and a Python orchestration library. Two surface areas:

1. **Claude Code Plugin** (`agents/` + `.claude-plugin/`) — Markdown agent definitions loaded via `subagent_type="geepers_*"` in Claude Code's Task tool
2. **Packaged Skills** (`skills/`) — 37+ skills built from agent definitions, installable as Claude Code skills
3. **Python Package** (`geepers/`) — Async orchestration framework for multi-agent workflows with LLM providers

## Commands

```bash
# Install Python package in dev mode
pip install -e .

# Install with all optional LLM/data providers
pip install -e ".[all]"

# Verify installation
python -c "from geepers import ConfigManager; print('OK')"

# Install as Claude Code plugin
# (from Claude Code CLI): /plugin add lukeslp/geepers

# Regenerate skills from agent definitions
python3 skills/package_all_skills.py

# Rebuild skill zips
bash skills/rebuild-zips.sh

# Rebuild a single skill zip
cd skills/source/<skill-name> && zip -r ../../zips/<skill-name>.zip .
```

## Architecture

### Agent System (the main product)

Agents are markdown files in `agents/` with YAML frontmatter (`name`, `description`, `model`, `color`). They're registered in `.claude-plugin/plugin.json` and invoked via Claude Code's Task tool:

```
Task with subagent_type="geepers_scout"
```

**Hierarchy**: `geepers_conductor` (master router) → domain orchestrators (`geepers_orchestrator_*`) → specialist agents (`geepers_*`).

Key domains: checkpoint, deploy, quality, frontend, fullstack, hive, research, games, corpus, web, python, datavis, standalone, system. See `agents/AGENT_DOMAINS.md` for the full routing guide.

### Packaged Skills (`skills/`)

All agents are packaged as Claude Code skills. `skills/package_all_skills.py` generates `SKILL.md` files from agent markdown definitions. Orchestrator skills include sub-agent `.md` files in an `agents/` subdirectory. Standalone skills contain a single `SKILL.md`.

Source in `skills/source/`, built zips in `skills/zips/`. Run `python3 skills/package_all_skills.py && bash skills/rebuild-zips.sh` to rebuild after editing agents.

### Python Package (`geepers/`)

- `config.py` — `ConfigManager` with multi-source config loading (defaults → config file → .env → env vars → CLI args). Handles API key management for 15+ providers.
- `orchestrators/` — Async orchestration framework. `BaseOrchestrator` (ABC) defines: `decompose_task()` → `execute_subtask()` → `synthesize_results()`. Supports parallel/sequential execution, streaming events, retries, and document generation.
- `naming/` — Canonical naming registry mapping roles (conductor/orchestrator/agent/utility) to identifiers across scopes (internal/package/cli/mcp). `LEGACY_MAP` handles old class names.
- `utils/` — Async helpers: rate limiter, cache manager, retry decorator, parallel task execution, graceful import fallbacks.
- `parser/` — Agent markdown file parser.

### Plugin Manifests (`.claude-plugin/`)

- `plugin.json` — Claude Code plugin manifest. Lists all agents with source paths, MCP server definitions, and configuration schema.
- `marketplace.json` — Marketplace metadata with full agent catalog.

## Key Conventions

- All agent IDs are prefixed `geepers_` (e.g., `geepers_scout`, `geepers_orchestrator_deploy`)
- The master router is `geepers_conductor` (not `conductor_geepers`)
- Orchestrators coordinate specialists; standalone agents work independently
- `agents/shared/` contains workflow docs referenced by all agents
- Python package depends on `dr-eamer-ai-shared` (shared library on PyPI)
- `geepers/mcp/` is expected to be symlinked to `~/shared/mcp/` in dev; not committed

## Publishing

```bash
# PyPI
python -m build && twine upload dist/*

# Claude Marketplace
# Push to GitHub — plugins auto-discovered from .claude-plugin/plugin.json
```

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

Geepers is a Claude Code plugin providing 63+ specialized markdown-defined agents and a Python orchestration library. It has two surface areas:

1. **Claude Code Plugin** (`agents/` + `.claude-plugin/`) — Markdown agent definitions loaded via `subagent_type="geepers_*"` in Claude Code's Task tool
2. **Python Package** (`geepers/`) — Async orchestration framework for multi-agent workflows with LLM providers

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

# Rebuild skill zips after editing source
cd skills/source && for s in */; do cd "$s" && zip -r ../../zips/${s%/}.zip . && cd ..; done
```

## Architecture

### Agent System (the main product)

Agents are markdown files in `agents/` with YAML frontmatter (`name`, `description`, `model`, `color`). They're registered in `.claude-plugin/plugin.json` and invoked via Claude Code's Task tool:

```
Task with subagent_type="geepers_scout"
```

**Hierarchy**: `geepers_conductor` (master router) → domain orchestrators (`geepers_orchestrator_*`) → specialist agents (`geepers_*`).

Key domains: checkpoint, deploy, quality, frontend, fullstack, hive, research, games, corpus, web, python, datavis, standalone, system. See `agents/AGENT_DOMAINS.md` for the full routing guide.

### Python Package (`geepers/`)

- `config.py` — `ConfigManager` with multi-source config loading (defaults → config file → .env → env vars → CLI args). Handles API key management for 15+ providers.
- `orchestrators/` — Async orchestration framework. `BaseOrchestrator` (ABC) defines: `decompose_task()` → `execute_subtask()` → `synthesize_results()`. Supports parallel/sequential execution, streaming events, retries, and document generation. Notable implementations: `dream_cascade_orchestrator`, `dream_swarm_orchestrator`, `dreamer_beltalowda_orchestrator`.
- `naming/` — Canonical naming registry mapping roles (conductor/orchestrator/agent/utility) to identifiers across scopes (internal/package/cli/mcp). `LEGACY_MAP` handles old class names.
- `utils/` — Async helpers: rate limiter, cache manager, retry decorator, parallel task execution, graceful import fallbacks.
- `parser/` — Agent markdown file parser.

### Skills (`skills/`)

Claude Desktop skills (zip-packaged). Source in `skills/source/`, built zips in `skills/zips/`. Each skill has `SKILL.md` + optional `scripts/`, `reference/`, `src/` directories.

### Plugin Manifests (`.claude-plugin/`)

- `plugin.json` — Claude Code plugin manifest. Lists all agents with source paths, MCP server definitions, and configuration schema.
- `marketplace.json` — Marketplace metadata with full agent catalog.

## Key Conventions

- All agent IDs are prefixed `geepers_` (e.g., `geepers_scout`, `geepers_orchestrator_deploy`)
- Orchestrators coordinate specialists; standalone agents work independently
- The `shared/` directory under agents contains workflow docs referenced by all agents (`WORKFLOW_REQUIREMENTS.md`, `PARALLEL_WORKFLOWS.md`, `SESSION_WORKFLOWS.md`)
- Python package depends on `dr-eamer-ai-shared` (shared library published to PyPI)
- The `geepers/mcp/` directory is expected to be symlinked to `~/shared/mcp/` in development; it's not committed to this repo

## Publishing

```bash
# PyPI
python -m build && twine upload dist/*

# Claude Marketplace
# Push to GitHub — plugins auto-discovered from .claude-plugin/plugin.json
```

# geepers-skills (ClawHub)

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platform: ClawHub](https://img.shields.io/badge/platform-ClawHub-red.svg)
![Skills: 23](https://img.shields.io/badge/skills-23-brightgreen.svg)

Skill package for ClawHub (formerly OpenClaw API). Full 23-skill set from the canonical geepers release, packaged for the ClawHub distribution format.

## Install

Reference `clawhub-package.json` from your ClawHub config, or copy the `skills/` directory to your ClawHub skill path.

## What's Included

**Orchestration**
- `team` — routes any request to the right specialist
- `executive`, `engineering`, `finance` — domain-specific orchestration
- `dream-swarm`, `swarm`, `mcp-orchestration` — parallel multi-agent workflows

**Planning & Building**
- `planner` — breaks down tasks and sequences work
- `builder` — executes implementation plans
- `scout` — fast project reconnaissance and quick wins
- `quality` — parallel a11y, perf, security, and dep checks
- `testing` — test strategy and implementation

**Dev Tools**
- `git-hygiene-guardian` — repo cleanup and artifact hygiene
- `validator` — config and integration validation
- `server-deploy` — service deployment and routing

**Research & Data**
- `data-fetch` — pulls from 17+ structured APIs (Census, arXiv, GitHub, NASA, etc.)
- `datavis` — D3.js and Chart.js visualization workflows
- `geepers-data` — aggregated data API access
- `geepers-corpus` — COCA corpus linguistics
- `geepers-etymology` — historical linguistics and etymology

**LLM & APIs**
- `geepers-llm` — unified access across multiple model providers
- `geepers-orchestrate` — API-backed Dream Cascade and Dream Swarm execution

**Product**
- `product` — PRD generation and product planning

## Legacy Alias

Previously distributed as `dreamer-api-skills`. The `clawhub-package.json` includes the legacy alias for backwards compatibility.

## Rebuild from Canonical

```bash
python3 scripts/build-platform-packages.py --platform clawhub --clean
```

## Author

**Luke Steuber**
- [lukesteuber.com](https://lukesteuber.com)
- [@lukesteuber.com](https://bsky.app/profile/lukesteuber.com) on Bluesky

## License

MIT

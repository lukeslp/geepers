# geepers-skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Platform: Claude](https://img.shields.io/badge/platform-Claude%20Code-blueviolet.svg)
![Skills: 23](https://img.shields.io/badge/skills-23-brightgreen.svg)

23 skills for Claude Code and Claude Desktop — planning, building, shipping, researching, and auditing from a single install.

Part of the [geepers](https://github.com/lukeslp/geepers) ecosystem — [PyPI](https://pypi.org/project/geepers-llm/) · [MCP servers](https://github.com/lukeslp/geepers-kernel) · [Codex CLI](https://github.com/lukeslp/geepers-gpt) · [Gemini](https://github.com/lukeslp/geepers-gemini) · [Manus](https://github.com/lukeslp/geepers-manus) · [ClawHub](https://github.com/lukeslp/geepers-api-skills) · [beltalowda](https://github.com/lukeslp/beltalowda)

## Install

```bash
plugin add lukeslp/geepers
```

Or drop this directory into your Claude skills path manually.

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
- `server-deploy` — service deployment and Caddy routing

**Research & Data**
- `data-fetch` — pulls from 17+ structured APIs (Census, arXiv, GitHub, NASA, etc.)
- `datavis` — D3.js and Chart.js visualization workflows
- `geepers-data` — aggregated data API access
- `geepers-corpus` — COCA corpus linguistics
- `geepers-etymology` — historical linguistics and etymology

**LLM & APIs**
- `geepers-llm` — unified access to Claude, Grok, Gemini, Mistral, and more
- `geepers-orchestrate` — API-backed Dream Cascade and Dream Swarm execution

**Product**
- `product` — PRD generation and product planning

## Ecosystem

- **Python**: [`geepers-llm`](https://pypi.org/project/geepers-llm/) · [`geepers-kernel`](https://pypi.org/project/geepers-kernel/)
- **MCP servers**: [`geepers-unified` · `geepers-providers` · `geepers-data` · `geepers-websearch`](https://github.com/lukeslp/geepers-kernel)
- **Orchestration**: [beltalowda](https://github.com/lukeslp/beltalowda) · [multi-agent-orchestration](https://github.com/lukeslp/multi-agent-orchestration)
- **Codex CLI**: [geepers-gpt](https://github.com/lukeslp/geepers-gpt)
- **Gemini**: [geepers-gemini](https://github.com/lukeslp/geepers-gemini)
- **Manus**: [geepers-manus](https://github.com/lukeslp/geepers-manus)
- **ClawHub**: [geepers-api-skills](https://github.com/lukeslp/geepers-api-skills)

## Author

**Luke Steuber**
- [lukesteuber.com](https://lukesteuber.com)
- [@lukesteuber.com](https://bsky.app/profile/lukesteuber.com) on Bluesky

## License

MIT

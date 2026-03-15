---
name: geepers-mcp
description: Launch MCP orchestration workflows (Dream Cascade and Dream Swarm) for multi-agent coordination and synthesis.
---

# MCP Orchestration Skill

Multi-agent orchestration via MCP protocol. Launch hierarchical research swarms or parallel domain searches.

## Prerequisites

Requires `geepers-mcp` to be installed:
```bash
pip install geepers-mcp[all]
```

If MCP tools aren't appearing, install the package and restart Claude Code.

## Architecture: Dream Cascade

3-tier hierarchical research swarm:

1. **Tier 1: Belters (Workers)** — Parallel agents (1-30+) with unique specializations
2. **Tier 2: Drummers (Synthesizers)** — Aggregate every 5 Belter responses, filter noise
3. **Tier 3: Camina (Executive)** — Final strategic synthesis report

## Architecture: Dream Swarm

Parallel multi-domain search:

- Fan out across academic, news, code, financial, and web sources simultaneously
- Merge results into a unified synthesis

## Available MCP Tools

| Tool | What it does |
|------|-------------|
| `orchestrate_research` | Beltalowda: 8 agents, Drummer synthesis, Camina summary |
| `orchestrate_search` | Swarm: 5+ parallel domain agents |
| `get_orchestration_status` | Check progress of a running workflow |
| `cancel_orchestration` | Stop mid-execution |
| `list_orchestrator_patterns` | List available patterns |
| `list_registered_tools` | Browse all tool modules |
| `execute_registered_tool` | Run any tool directly |

## Parameters

### `orchestrate_research`
- `task` (string, required): The research topic or question
- `num_agents` (integer): Total number of Belters (default: 5)
- `enable_drummer` (boolean): Enable synthesis tier (default: true)
- `enable_camina` (boolean): Enable executive tier (default: false)
- `provider_name` (string): LLM provider to use (default: "anthropic")

## Related

- `/geepers:research` — Command that uses these MCP tools
- `/geepers:hunt` — Parallel search across sources
- `geepers:orchestrate` — Skill for direct orchestration
- `geepers:data` — Data fetching from 17 APIs

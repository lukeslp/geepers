---
description: Deep research using Dream Cascade (hierarchical) or Dream Swarm (parallel) multi-agent workflows
---

# Research Mode

Launch sophisticated multi-agent research workflows for comprehensive information gathering.

## Two Research Patterns

### Dream Cascade (Hierarchical - Deep Analysis)

Use for:
- Complex topics requiring multiple perspectives
- Comprehensive reports needing structured organization
- Deep dives into unfamiliar domains
- Academic or technical research

Architecture:
```
CAMINA (Executive Synthesis)
    │
DRUMMERS (Mid-level Themes)
    │
BELTERS (Broad Exploration)
```

Launch via MCP:
```
mcp__orchestrator__dream_orchestrate_research
- task: "Research topic"
- num_agents: 8 (default)
- budget_tier: balanced | cheap | premium
```

### Dream Swarm (Parallel - Broad Coverage)

Use for:
- Multi-source search across different APIs
- Rapid information gathering
- Fact-checking against multiple sources
- Comparative analysis

Available domains: arxiv, github, news, wikipedia, pubmed, semantic_scholar, census, nasa, youtube, weather, openlibrary, fec, judiciary, archive, finance, mal, wolfram

Launch via MCP:
```
mcp__orchestrator__dream_orchestrate_search
- query: "Search query"
- num_agents: 5 (default)
- allowed_agent_types: ["arxiv", "github", "news"]
```

## Decision Guide

| Need | Use |
|------|-----|
| Deep analysis, synthesis, report | Dream Cascade |
| Broad coverage, multiple sources | Dream Swarm |
| Academic papers | Dream Swarm with arxiv, pubmed, semantic_scholar |
| Code examples | Dream Swarm with github |
| Current events | Dream Swarm with news |
| Everything | Dream Cascade (comprehensive) |

## Supporting Agents

For research-adjacent tasks:
- **@geepers_orchestrator_research** - Coordinates data, links, diag, fetcher
- **@geepers_fetcher** - Fetch specific URLs
- **@geepers_data** - Data quality and validation
- **@geepers_citations** - Verify citations and sources

## Execute

**Research topic**: $ARGUMENTS

If arguments provided:
1. Determine which pattern fits (cascade vs swarm)
2. Launch appropriate MCP tool
3. Synthesize results

If no arguments:
- Ask what to research and recommend approach

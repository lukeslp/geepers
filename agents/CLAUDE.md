# CLAUDE.md
<!-- Navigation: ~/geepers/agents/CLAUDE.md -->
<!-- Parent: ~/geepers/CLAUDE.md -->
<!-- Map: ~/CLAUDE_MAP.md -->

This file provides guidance to Claude Code (claude.ai/code) when working in this directory.

## What's Here

73 markdown-defined agent definitions across 15 domains. Each `.md` file is loaded by Claude Code as a specialized sub-agent via the `Task` tool (`subagent_type`).

The plugin manifest at `../.claude-plugin/plugin.json` maps agent IDs to these file paths. 52 agents are currently registered. More files exist on disk.

## Agent File Format

Every agent is a markdown file with YAML frontmatter:

```yaml
---
name: geepers_<name>
description: One-sentence description used to decide when to invoke this agent.
model: sonnet
color: "#hexcolor"
---
```

Followed by these structured sections (all required for registered agents):

- **Mission** — What this agent does and when it's invoked
- **Workflow** — Step-by-step process the agent follows
- **Coordination Protocol** — How it hands off to or calls other agents

## Naming Convention

All agent files follow `geepers_<name>.md`. The agent ID in `plugin.json` matches the filename stem. Orchestrators use `geepers_orchestrator_<domain>.md`.

## Routing Hierarchy

```
conductor_geepers (master/)
  → 13 orchestrators (one per domain)
    → ~40 specialists
```

If a task fits a specialist directly, invoke it without going through the conductor. The routing table lives in `AGENT_DOMAINS.md` and `../QUICK_REFERENCE.md`.

## Domain Structure

| Domain | Directory | Has Orchestrator? |
|--------|-----------|-------------------|
| master | `master/` | No (IS the conductor) |
| checkpoint | `checkpoint/` | Yes |
| corpus | `corpus/` | Yes |
| datavis | `datavis/` | Yes |
| deploy | `deploy/` | Yes |
| frontend | `frontend/` | Yes |
| fullstack | `fullstack/` | Yes |
| games | `games/` | Yes |
| hive | `hive/` | Yes |
| python | `python/` | Yes |
| quality | `quality/` | Yes |
| research | `research/` | Yes |
| standalone | `standalone/` | No |
| system | `system/` | No |
| web | `web/` | Yes |

`shared/WORKFLOW_REQUIREMENTS.md` contains workflow rules all agents must follow.

## Adding an Agent

1. Create `<domain>/geepers_<name>.md` with the frontmatter and three sections above
2. Add an entry to `../.claude-plugin/plugin.json` in the `agents` array:
   ```json
   {
     "id": "geepers_<name>",
     "source": "agents/<domain>/geepers_<name>.md"
   }
   ```
3. Update this domain's orchestrator markdown to reference the new specialist
4. Update `AGENT_DOMAINS.md`

## geepers_agents Symlink

`~/geepers_agents` → `~/geepers/agents/` — backward compatibility alias used in some older tool references.

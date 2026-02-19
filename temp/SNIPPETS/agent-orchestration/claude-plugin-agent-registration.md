# Claude Code Plugin Agent Registration Pattern

Pattern for registering markdown-defined agents in a Claude Code plugin's `plugin.json` manifest.

## Structure

Each agent entry in `.claude-plugin/plugin.json` requires:

```json
{
  "agents": [
    {
      "id": "geepers_agent_name",
      "name": "Display Name",
      "description": "One-sentence description of what this agent does.",
      "source": "agents/domain/geepers_agent_name.md"
    }
  ]
}
```

## Key rules

1. **`id` must match the filename stem** — `geepers_agent_name` maps to `agents/domain/geepers_agent_name.md`
2. **Naming convention**: all agent IDs use `geepers_` prefix + snake_case name
3. **Source path** is relative to the repo root (where `plugin.json` lives)
4. **Orchestrators come first** within each domain group for readability
5. **Description count in `plugin.json` metadata** must stay in sync with actual registered count

## Finding unregistered agents

```bash
# List all agent .md files
find agents/ -name "geepers_*.md" | sort

# List all registered IDs
jq -r '.agents[].id' .claude-plugin/plugin.json | sort

# Find orphans (on disk but not registered)
comm -23 \
  <(find agents/ -name "geepers_*.md" -exec basename {} .md \; | sort) \
  <(jq -r '.agents[].id' .claude-plugin/plugin.json | sort)
```

## Discovered

- Project: geepers
- Date: 2026-02-19
- Context: Registering 21 orphaned agents; total count went from 52 to 73

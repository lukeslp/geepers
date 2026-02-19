# Pattern: Batch Agent Registration in plugin.json

**Category**: agent-orchestration
**Harvested**: 2026-02-19
**Source**: geepers/.claude-plugin/plugin.json

## Context

When a Claude Code plugin has agent .md files on disk that are not yet registered in plugin.json,
they are invisible to the Task tool. The registration schema is simple but must be applied to each
agent individually. This pattern shows the minimal registration entry and a checklist for bulk
registration of orphaned agents.

## Registration Schema (minimal)

```json
{
  "agents": [
    {"id": "agent_id_here", "source": "./agents/<domain>/agent_file.md"}
  ]
}
```

- `id` must match how you call it with `subagent_type` in the Task tool
- `source` is relative to the plugin.json file location (which is at the plugin root)
- No other fields are required for basic registration

## Finding Orphaned Agents

```bash
# Count .md files in agents/ (excluding shared docs)
find agents/ -name "*.md" | grep -v "AGENT_DOMAINS\|WORKFLOW_REQUIREMENTS\|README\|CLAUDE\|shared" | wc -l

# Count registered agents in plugin.json
python3 -c "
import json
data = json.load(open('.claude-plugin/plugin.json'))
print('Registered:', len(data['agents']))
"

# Find which files are NOT registered
python3 -c "
import json, os, glob

data = json.load(open('.claude-plugin/plugin.json'))
registered_sources = {a['source'].replace('./', '') for a in data['agents']}

all_agent_files = glob.glob('agents/**/*.md', recursive=True)
ignore_patterns = ['AGENT_DOMAINS', 'WORKFLOW_REQUIREMENTS', 'README', 'CLAUDE', 'shared/']

orphans = []
for f in sorted(all_agent_files):
    if any(p in f for p in ignore_patterns):
        continue
    if f not in registered_sources:
        orphans.append(f)

for o in orphans:
    stem = os.path.basename(o).replace('.md', '')
    print(f'  {{\"id\": \"{stem}\", \"source\": \"./{o}\"}}')
"
```

## Verifying All Sources Exist (post-registration check)

```python
import json, os

with open('.claude-plugin/plugin.json') as f:
    data = json.load(f)

missing = []
for agent in data['agents']:
    src = agent['source'].replace('./', '')
    if not os.path.exists(src):
        missing.append((agent['id'], src))

if missing:
    print(f"MISSING {len(missing)} source files:")
    for id_, path in missing:
        print(f"  {id_} -> {path}")
else:
    print(f"All {len(data['agents'])} agent source files verified on disk.")
```

## Notes

- The `id` in plugin.json must exactly match the `subagent_type` used in Task tool calls
- Common naming mistake: `geepers_docs_standalone` vs `geepers_docs` — use the stem of the .md filename as the id
- After bulk registration, restart the Claude Code session for new agents to be discoverable
- Conductor/orchestrator agents count separately from specialist agents in the manifest

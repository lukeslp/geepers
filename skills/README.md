# Claude Desktop Skills

Custom skills for uploading to Claude Desktop (Pro/Max/Team/Enterprise).

## Directory Structure

```
skills/
├── source/          # Editable source files
│   ├── data-fetch/
│   ├── datavis/
│   ├── dream-cascade/
│   ├── dream-swarm/
│   ├── git-hygiene-guardian/
│   └── server-deploy/
├── zips/            # Ready-to-upload zip files
│   ├── data-fetch.zip
│   ├── datavis.zip
│   ├── dream-cascade.zip
│   ├── dream-swarm.zip
│   ├── git-hygiene-guardian.zip
│   └── server-deploy.zip
└── README.md
```

## Skills Overview

| Skill | Description |
|-------|-------------|
| **data-fetch** | Fetch data from 17+ structured APIs (Census, arXiv, GitHub, NASA, PubMed, Wikipedia, etc.) |
| **datavis** | D3.js/Chart.js visualization toolkit with color palettes, scales, and data pipelines |
| **dream-cascade** | Hierarchical 3-tier research workflows via MCP orchestrator |
| **dream-swarm** | Parallel multi-domain search workflows via MCP orchestrator |
| **git-hygiene-guardian** | Git cleanup, branch management, and repository hygiene |
| **server-deploy** | Service management and Caddy configuration for dr.eamer.dev |

## How to Upload to Claude Desktop

1. Open Claude Desktop
2. Go to **Settings > Features**
3. Find the Skills section
4. Click "Upload Skill" or drag-and-drop
5. Select a `.zip` file from `~/geepers/skills/zips/`

## Rebuilding Zips After Edits

Edit files in `source/`, then rebuild:

```bash
cd ~/geepers/skills/source
for skill in */; do
    cd ~/geepers/skills/source/${skill%/}
    zip -r ~/geepers/skills/zips/${skill%/}.zip .
done
```

## Skill Structure (Anthropic Format)

Each skill folder contains:
- `SKILL.md` - Instructions and prompts (required)
- `scripts/` - Python/JavaScript executables (optional)
- `references/` - Reference documents (optional)
- `assets/` - Images, fonts, templates (optional)

## Synced Location

These skills are mirrored from `~/.claude/skills/` (Claude Code's native skill location).
To keep in sync, edit in `source/` and copy back to `.claude/skills/` as needed.

## References

- [Agent Skills Overview](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
- [Using Skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [Anthropic Skills Announcement](https://www.anthropic.com/news/skills)

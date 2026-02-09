# Geepers Plugin Marketplace Submission Checklist

## Overview

This checklist covers the submission process for adding geepers to Claude Code plugin marketplaces. **Puerto is the recommended first submission** due to its community-friendly process.

---

## Puerto Marketplace Submission (PRIORITY 1)

### Pre-Submission
- [ ] Read: `https://github.com/bandofai/puerto/README.md`
- [ ] Check: Current plugins in `bandofai/puerto/plugins/`
- [ ] Verify: Geepers GitHub repo is public: `https://github.com/lukeslp/geepers`
- [ ] Confirm: All 63 agents are properly documented

### Create Plugin Package

#### Directory Structure
```
Puerto Local Clone
├── plugins/
│   └── geepers/                        # NEW DIRECTORY
│       ├── .claude-plugin/
│       │   └── plugin.json             # NEW - Full metadata
│       ├── agents/                     # SYMLINK OR COPY - ~/geepers/agents/
│       ├── README.md                   # NEW - Comprehensive docs
│       ├── INSTALLATION.md             # NEW - Setup guide
│       ├── AGENT_REFERENCE.md          # NEW - All 63 agents listed
│       ├── EXAMPLES.md                 # NEW - Usage examples
│       └── LICENSE                     # NEW - MIT License
```

#### .claude-plugin/plugin.json
```json
{
  "schema": "1.0",
  "name": "geepers",
  "displayName": "Geepers - Multi-Agent Orchestration",
  "version": "1.0.0",
  "description": "63-agent orchestration system for infrastructure, quality, frontend, fullstack development, games, linguistics, and more",
  "author": "Luke Steuber",
  "repository": "https://github.com/lukeslp/geepers",
  "license": "MIT",
  "tags": [
    "orchestration",
    "agents",
    "infrastructure",
    "quality",
    "frontend",
    "fullstack",
    "development",
    "mcp"
  ],
  "agents": {
    "master": {
      "geepers_conductor": "agents/master/geepers_conductor.md"
    },
    "checkpoint": {
      "scout": "agents/checkpoint/geepers_scout.md",
      "repo": "agents/checkpoint/geepers_repo.md",
      "status": "agents/checkpoint/geepers_status.md",
      "snippets": "agents/checkpoint/geepers_snippets.md"
    },
    "deploy": {
      "caddy": "agents/deploy/geepers_caddy.md",
      "services": "agents/deploy/geepers_services.md",
      "validator": "agents/deploy/geepers_validator.md"
    },
    "quality": {
      "a11y": "agents/quality/geepers_a11y.md",
      "perf": "agents/quality/geepers_perf.md",
      "api": "agents/quality/geepers_api.md",
      "deps": "agents/quality/geepers_deps.md",
      "security": "agents/quality/geepers_security.md",
      "testing": "agents/quality/geepers_testing.md"
    },
    "frontend": {
      "css": "agents/frontend/geepers_css.md",
      "design": "agents/frontend/geepers_design.md",
      "motion": "agents/frontend/geepers_motion.md",
      "typescript": "agents/frontend/geepers_typescript.md",
      "ux": "agents/frontend/geepers_uxpert.md",
      "webperf": "agents/frontend/geepers_webperf.md"
    },
    "fullstack": {
      "db": "agents/fullstack/geepers_db.md",
      "react": "agents/fullstack/geepers_react.md"
    },
    "hive": {
      "builder": "agents/hive/geepers_builder.md",
      "planner": "agents/hive/geepers_planner.md",
      "integrator": "agents/hive/geepers_integrator.md",
      "quickwin": "agents/hive/geepers_quickwin.md",
      "refactor": "agents/hive/geepers_refactor.md"
    },
    "research": {
      "data": "agents/research/geepers_data.md",
      "links": "agents/research/geepers_links.md",
      "diag": "agents/research/geepers_diag.md",
      "citations": "agents/research/geepers_citations.md",
      "fetcher": "agents/research/geepers_fetcher.md",
      "searcher": "agents/research/geepers_searcher.md"
    },
    "games": {
      "game": "agents/games/geepers_game.md",
      "gamedev": "agents/games/geepers_gamedev.md",
      "godot": "agents/games/geepers_godot.md"
    },
    "corpus": {
      "corpus": "agents/corpus/geepers_corpus.md",
      "corpus_ux": "agents/corpus/geepers_corpus_ux.md"
    },
    "web": {
      "flask": "agents/web/geepers_flask.md",
      "express": "agents/web/geepers_express.md"
    },
    "python": {
      "pycli": "agents/python/geepers_pycli.md"
    },
    "standalone": {
      "api": "agents/standalone/geepers_api.md",
      "scalpel": "agents/standalone/geepers_scalpel.md",
      "dashboard": "agents/standalone/geepers_dashboard.md",
      "canary": "agents/standalone/geepers_canary.md",
      "janitor": "agents/standalone/geepers_janitor.md",
      "docs": "agents/standalone/geepers_docs.md",
      "git": "agents/standalone/geepers_git.md"
    },
    "system": {
      "help": "agents/system/geepers_system_help.md",
      "onboard": "agents/system/geepers_system_onboard.md",
      "diag": "agents/system/geepers_system_diag.md"
    }
  },
  "commands": [],
  "skills": [],
  "hooks": [],
  "mcpServers": {
    "geepers": {
      "command": "python",
      "args": ["-m", "geepers.mcp"]
    }
  }
}
```

#### README.md Content Outline
1. **Title & Description** - What is geepers?
2. **Quick Start** - Installation command
3. **What's Included** - List of 63 agents by category
4. **Agent Categories** - Table with descriptions
5. **Usage Examples** - Common workflows
6. **Agent Reference** - Full documentation for each agent
7. **MCP Integration** - Server details
8. **Links** - GitHub, documentation, etc.
9. **License** - MIT

#### INSTALLATION.md
1. Prerequisites
2. Installation steps
3. Configuration
4. Verification
5. Troubleshooting

#### AGENT_REFERENCE.md
Table with all 63 agents:
| Agent ID | Category | Description | Use Case |
|----------|----------|-------------|----------|
| geepers_conductor | Master | Intelligent routing | Route to specialists |
| geepers_scout | Checkpoint | Quick reconnaissance | Project analysis |
| ... | ... | ... | ... |

#### EXAMPLES.md
Real-world usage examples:
- Example 1: Using for infrastructure changes (Caddy)
- Example 2: Frontend development workflow
- Example 3: Quality review automation
- Example 4: Research and data gathering
- Example 5: Game development

### Fork & Clone
```bash
# Fork bandofai/puerto on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/puerto.git
cd puerto
git checkout -b feature/add-geepers-plugin
```

### Create Plugin Files

1. **Create directory:**
   ```bash
   mkdir -p plugins/geepers/.claude-plugin
   ```

2. **Add plugin.json:** (see above)

3. **Create symlinks to agents:**
   ```bash
   ln -s ~/geepers/agents plugins/geepers/agents
   ```
   OR copy relevant files if symlinks don't work

4. **Create README.md** with comprehensive documentation

5. **Create supporting documentation:**
   - INSTALLATION.md
   - AGENT_REFERENCE.md
   - EXAMPLES.md
   - LICENSE (MIT)

### Update Puerto's Main README
- Add geepers to the plugins list
- Include brief description
- Add installation command

### Commit & Push
```bash
git add plugins/geepers/
git commit -m "feat: add geepers multi-agent orchestration plugin

- 63 specialized agents across 13 categories
- Infrastructure, quality, frontend, fullstack, and more
- Intelligent routing via geepers_conductor
- Complete MCP server integration"

git push origin feature/add-geepers-plugin
```

### Create Pull Request
**Title:** "Add geepers multi-agent orchestration plugin"

**Description:**
```markdown
## Overview
Adds geepers - a comprehensive 63-agent system for:
- Infrastructure management (Caddy, services)
- Code quality audits (accessibility, performance, security)
- Frontend development (CSS, design, motion)
- Full-stack features (database, React)
- Game development
- Research and data gathering
- Linguistics and corpus work

## What's Included
- 63 specialized agents
- Master orchestrator for intelligent routing
- Complete MCP server implementation
- Comprehensive documentation for all agents

## Usage Example
```
/plugin install geepers@puerto
```

## Related
- GitHub: https://github.com/lukeslp/geepers
- Author: Luke Steuber

## Tests
- [x] All plugin files in correct structure
- [x] README.md comprehensive and accurate
- [x] All 63 agents documented
- [x] Installation instructions clear
- [x] Examples provided

## Checklist
- [x] Plugin structure follows standard format
- [x] .claude-plugin/plugin.json valid
- [x] All agents referenced in plugin.json exist
- [x] Comprehensive documentation included
- [x] License included (MIT)
```

### Monitor & Iterate
1. Watch for comments/feedback
2. Make requested changes
3. Re-push to same branch (auto-updates PR)
4. Expect merge within hours (Band of AI is very responsive)

---

## Claude Code Official Submission (PRIORITY 2)

### Not a PR Process
- This is Anthropic's official repository
- No CONTRIBUTING.md or open submission process
- Direct contact required

### Contact Method
1. Join Claude Developers Discord: https://anthropic.com/discord
2. Look for #plugin-submissions or similar channel
3. Or email: developers@anthropic.com

### Pitch
Brief overview of geepers value proposition:
- Specialized agents for infrastructure, quality, frontend
- Solves common Claude Code workflows
- Proven in production (Luke Steuber's projects)
- Well-documented and maintained

### Timing
- Submit only after Puerto success
- Demonstrate community adoption
- Get feedback from Puerto submissions

---

## Taskmaster Integration (PRIORITY 3)

### Research Phase
1. Review how Taskmaster uses MCP servers
2. Check CONTRIBUTING.md for MCP additions
3. Evaluate if geepers agents can be wrapped as Taskmaster tasks
4. Consider if agent output fits task format

### Not Recommended Until
- Puerto submission is complete
- Community feedback is positive
- Taskmaster team expresses interest

---

## Post-Submission Activities

### After Puerto Merger
- [ ] Monitor downloads/usage
- [ ] Collect feedback
- [ ] Update geepers repository if needed
- [ ] Consider Claude Code official submission
- [ ] Plan Taskmaster integration research

### Maintenance
- [ ] Keep geepers repository synchronized with marketplace copy
- [ ] Monitor for plugin.json changes needed
- [ ] Update agent listings if new agents added
- [ ] Respond to any issues/feature requests

---

## Important Files to Check Before Submission

1. `/home/coolhand/.claude/plugins/marketplaces/geepers-marketplace/README.md`
   - Current documentation
   - Installation instructions
   - Agent categories

2. `/home/coolhand/.claude/plugins/marketplaces/geepers-marketplace/agents/`
   - All 63 agents exist and documented
   - Proper file naming convention

3. `/home/coolhand/.claude/plugins/marketplaces/geepers-marketplace/.claude-plugin/`
   - Check existing plugin.json structure
   - Reference for marketplace submission

4. `/home/coolhand/geepers/research/MARKETPLACE_RESEARCH.md`
   - Full marketplace analysis
   - Comparison of options
   - Detailed submission guidance

---

## Success Criteria

### Puerto Submission Success
- [ ] PR created successfully
- [ ] PR reviewed (usually within hours)
- [ ] PR merged to main
- [ ] Installation command works: `/plugin install geepers@puerto`
- [ ] Agents available in Claude Code

### Long-term Success
- [ ] Positive community feedback
- [ ] Active usage tracking
- [ ] Potential Claude Code official consideration
- [ ] Taskmaster integration opportunities

---

## Quick Reference Commands

```bash
# Clone puerto
git clone https://github.com/bandofai/puerto.git

# Create feature branch
cd puerto
git checkout -b feature/add-geepers-plugin

# Create plugin directory
mkdir -p plugins/geepers/.claude-plugin

# Verify geepers agents exist
ls ~/geepers/agents/

# Commit changes
git add plugins/geepers/
git commit -m "feat: add geepers multi-agent orchestration plugin"

# Push to fork
git push origin feature/add-geepers-plugin

# Then create PR on GitHub
# https://github.com/bandofai/puerto/compare/main...YOUR_USERNAME:feature/add-geepers-plugin
```

---

## Resource Links

- **Puerto Repository:** https://github.com/bandofai/puerto
- **Geepers Repository:** https://github.com/lukeslp/geepers
- **Claude Code Docs:** https://docs.claude.com/en/docs/claude-code/plugins
- **Claude Developers Discord:** https://anthropic.com/discord
- **Task Master Discord:** https://discord.gg/taskmasterai

---

**Document Created:** December 18, 2025
**Status:** Ready for Action
**Next Step:** Approval to begin Puerto submission

# Claude Code Plugin Submission Checklist

Based on analysis of successful PRs to anthropics/claude-plugins-official and community marketplace requirements.

## Pre-Submission Requirements

### Required Files

- [ ] `.claude-plugin/plugin.json` - Complete metadata
  - [ ] `name` field
  - [ ] `description` field (clear value proposition)
  - [ ] `author` field
  - [ ] `version` field
  - [ ] `homepage` URL

- [ ] `README.md` - Comprehensive documentation
  - [ ] Plugin summary (1-2 sentences)
  - [ ] Key features (bulleted list)
  - [ ] Installation instructions
  - [ ] Usage examples
  - [ ] Configuration/setup requirements
  - [ ] Components inventory (X commands, Y skills, Z agents)

- [ ] `LICENSE` file
  - [ ] MIT, Apache-2.0, or AGPL-3.0
  - [ ] Matches license in plugin.json

### Optional But Recommended

- [ ] `.mcp.json` - MCP server configuration (if using MCP)
- [ ] `commands/` - Slash command definitions
- [ ] `agents/` - Agent definitions
- [ ] `skills/` - Skill definitions
- [ ] `hooks/` - Hook implementations

### Security & Quality

- [ ] No hardcoded credentials
- [ ] No API keys in code
- [ ] No sensitive data in repository
- [ ] All scripts have executable permissions (`chmod +x`)
- [ ] Tested and functioning
- [ ] Dependencies clearly documented
- [ ] Error handling implemented

## PR Submission Format

### PR Title Format
```
feat: add {plugin-name} plugin
```
or
```
Add {plugin-name} plugin for {purpose}
```

### PR Description Template

```markdown
# {Plugin Name} Pull Request

## Summary
{1-2 sentence description of what the plugin does}

## Key Features
- **Feature 1**: Description
- **Feature 2**: Description
- **Feature 3**: Description
- **Feature 4**: Description

## Components
- **X Slash Commands**: `/command1`, `/command2`, ...
- **Y MCP Tools**: `tool1`, `tool2`, ...
- **Z Skills**: Skill descriptions

## Installation
```
/plugin install {plugin-name}@claude-plugins-official
```

## Links
- Homepage: {url}
- Repository: {url}
- Documentation: {url}

## License
{MIT/Apache-2.0/AGPL-3.0}

## Checklist
- [ ] Plugin follows standard directory structure
- [ ] plugin.json includes required fields
- [ ] README.md with installation and usage instructions
- [ ] LICENSE file included
- [ ] MCP server configuration (if applicable)
- [ ] Slash commands documented
- [ ] Skills guide for best practices
- [ ] No hardcoded credentials
- [ ] Tested and functioning
```

## Marketplace-Specific Requirements

### anthropics/claude-plugins-official
- [ ] Add to `/external_plugins/{plugin-name}/`
- [ ] Follow PR template above
- [ ] Be prepared for weeks/months review time
- [ ] Quality and security standards expected

### jeremylongshore/claude-code-plugins-plus
- [ ] Add to `plugins/community/{plugin-name}/`
- [ ] Update `.claude-plugin/marketplace.extended.json`
- [ ] Run `pnpm run sync-marketplace`
- [ ] Preferred licenses: MIT or Apache-2.0

### ananddtyagi/claude-code-marketplace
- [ ] Submit via web form at claudecodecommands.directory/submit
- [ ] Separate form for agents vs commands
- [ ] Review PLUGIN_SCHEMA.md in repository

### Awesome Lists
- [ ] Fork the awesome list repository
- [ ] Add entry in appropriate section (alphabetically)
- [ ] Include: name, description, link, stars/metrics
- [ ] Follow list's CONTRIBUTING.md if exists
- [ ] Submit PR with clear description

## Quality Improvements

### Documentation
- [ ] Clear installation instructions
- [ ] Usage examples with expected output
- [ ] Configuration guide
- [ ] Troubleshooting section
- [ ] API key setup (if required)

### Code Quality
- [ ] Consistent code style
- [ ] Comments for complex logic
- [ ] Error messages are helpful
- [ ] Logging for debugging

### User Experience
- [ ] Clear command names
- [ ] Helpful error messages
- [ ] Progress indicators for long operations
- [ ] Sensible defaults

## Homepage Options

Consider creating a homepage for better visibility:

1. **GitHub Pages** in plugin repository
2. **Dedicated page** on dr.eamer.dev/geepers
3. **README.md** as comprehensive homepage
4. **Documentation site** (e.g., GitHub Wiki, docs/ folder)

## Example: Successful PR (Firecrawl #31)

**What made it good:**
- Clear summary of value proposition
- Bulleted key features (6 items)
- Component inventory (5 commands, 6 tools, 1 skill)
- Links to homepage, repo, docs
- Complete checklist
- 495 additions showing substantial implementation

**Review status:** Still open (submitted recently)

## Timeline Expectations

- **jeremylongshore/claude-code-plugins-plus**: Days to weeks
- **ananddtyagi/claude-code-marketplace**: Auto-sync after approval
- **anthropics/claude-plugins-official**: Weeks to months
- **Awesome lists**: Days to weeks (varies by maintainer)

## Post-Submission

- [ ] Monitor PR for feedback
- [ ] Respond to review comments promptly
- [ ] Update documentation based on feedback
- [ ] Address any security concerns immediately
- [ ] Test installation after merge
- [ ] Update plugin homepage with marketplace badge

---

**Checklist version:** 1.0
**Last updated:** 2025-12-18
**Maintained by:** Luke Steuber (geepers_orchestrator_research)

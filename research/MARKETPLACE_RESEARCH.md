# Geepers Claude Code Plugin Marketplaces Research

**Date:** December 18, 2025
**Research Scope:** Community plugin marketplaces for Claude Code
**Status:** Research Only (No Changes Made)

---

## Summary

We have access to 4 major Claude Code plugin marketplaces. Three accept community submissions (Puerto, Taskmaster, Claude Code), while one is our own geepers-marketplace. No previous PRs found for geepers in any marketplace.

---

## Marketplaces Identified

### 1. Claude Code Official (Anthropic)
**Repository:** https://github.com/anthropics/claude-code
**Type:** Official Anthropic repository
**Access:** Read-only (local clone only)

**Status:**
- Located at: `/home/coolhand/.claude/plugins/marketplaces/claude-code-plugins/`
- Git remote: `origin https://github.com/anthropics/claude-code.git`
- Last commit: Dec 12, 2024

**Plugins Directory:** `./plugins/`
- Contains 13 official plugins (agent-sdk-dev, code-review, feature-dev, frontend-design, hookify, pr-review-toolkit, etc.)
- Does NOT currently contain geepers

**Submission Process:**
- This is the official Anthropic repository - not a community marketplace
- No CONTRIBUTING.md found
- Plugins appear to be Anthropic-maintained only
- **Recommendation:** Contact Anthropic directly for official inclusion (not a PR process)

**Plugin Structure Required:**
```
plugin-name/
├── .claude-plugin/plugin.json      # Metadata
├── commands/                       # Slash commands (optional)
├── agents/                         # Specialized agents (optional)
├── skills/                         # Agent Skills (optional)
├── hooks/                          # Event handlers (optional)
├── .mcp.json                       # External tools (optional)
└── README.md                       # Documentation
```

---

### 2. Puerto (Band of AI)
**Repository:** https://github.com/bandofai/puerto
**Type:** Community-friendly marketplace
**Access:** Forks and PRs accepted

**Status:**
- Located at: `/home/coolhand/.claude/plugins/marketplaces/puerto/`
- Git remote: `origin https://github.com/bandofai/puerto.git`
- Last updated: Dec 12, 2024

**Current Plugins:** 2 plugins in `./plugins/`
- `essentials` - MCP servers + requirements workflow
- `claude-md` - CLAUDE.md file generation

**Submission Process:**
1. Fork the repository
2. Create a new directory in `./plugins/<plugin-name>/`
3. Follow the standard plugin structure
4. Include comprehensive README.md
5. Submit PR to main branch

**Key Details:**
- No CONTRIBUTING.md file found
- Installation: `/plugin marketplace add bandofai/puerto`
- Very open to community contributions
- Appears to be the most lightweight/easiest marketplace to submit to

**Plugin Structure Required:**
Same as Claude Code official (see above)

---

### 3. Taskmaster (Eyal Toledano)
**Repository:** https://github.com/eyaltoledano/claude-task-master
**Type:** Task management system with community contributions
**Access:** PRs welcome, quick reviews

**Status:**
- Located at: `/home/coolhand/.claude/plugins/marketplaces/taskmaster/`
- Git remote: `origin https://github.com/eyaltoledano/claude-task-master.git`
- Last updated: Dec 14, 2024

**Current Plugins:** 0 plugins found (Taskmaster is itself a plugin/MCP server)
- Repository is a complete MCP server implementation, not a plugin marketplace
- However, it accepts community contributions to the core system

**Submission Process (for contributing agents/features):**
1. Fork the repository
2. Create feature branch from `next` (not main)
3. Make changes and add tests
4. Create a changeset (required for user-facing changes)
5. Run full test suite: `npm test`
6. Submit PR to `next` branch

**Key Details:**
- PR-friendly team - quick reviews (usually within hours)
- Comprehensive CONTRIBUTING.md (see: `/home/coolhand/.claude/plugins/marketplaces/taskmaster/CONTRIBUTING.md`)
- Expects tested, well-reviewed code (not AI slop)
- Requires changesets for version management
- Target branch: `next` (not main)
- Installation: `/plugin add taskmaster-ai -- npx -y task-master-ai`

**Note:** Taskmaster is not a plugin marketplace like Puerto. It's a task management system. Geepers could be integrated with Taskmaster but this would be a feature integration, not a plugin submission.

---

### 4. Geepers Marketplace (Our Own)
**Repository:** https://github.com/lukeslp/geepers
**Type:** Our own marketplace
**Access:** Full control

**Status:**
- Located at: `/home/coolhand/.claude/plugins/marketplaces/geepers-marketplace/`
- Git remote: `origin https://github.com/lukeslp/geepers.git`
- Last commits:
  - `30aa0f5` docs: update README for 63 agents, add MCP-Dreamwalker reference
  - `7c141cc` feat(agents): reorganize agent categories and add frontend/hive domains
  - `53a362f` feat: initial commit - geepers multi-agent orchestration system

**Current Status:**
- Already published as its own repository
- README documents 63 specialized agents across 13 categories
- Installation: `/plugin add lukeslp/geepers`
- This is the "home" repository for geepers

**Submission Status:**
- Geepers is already published independently
- No PRs needed here (we control it)

---

## Previous PR Activity

**Search Results:** No previous PRs from lukeslp found in any marketplace

**GitHub PR Search:**
- `gh search prs --author lukeslp --archived false "geepers"` → No results
- `gh search prs --author lukeslp --archived false "plugins"` → No results
- `gh pr list --author lukeslp --state all --limit 100` → No matching PRs

**Conclusion:** This would be the first time submitting geepers to community marketplaces.

---

## Recommendations

### Immediate PR Targets (Community Submission)

#### 1. **Puerto (RECOMMENDED - START HERE)**
**Priority:** HIGH
**Effort:** LOW
**Reasoning:**
- Most community-friendly marketplace
- Smallest/simplest submission process
- No complex requirements (no changesets, no specific branch targets)
- Only 2 existing plugins (less competition)
- Band of AI appears very open to contributions

**PR Template:**
```
Title: Add geepers multi-agent orchestration plugin

Description:
Adds geepers - a comprehensive multi-agent system with 63 specialized agents
for infrastructure, quality, frontend, fullstack development, and more.

Features:
- 63 specialized agents across 13 categories
- Master orchestrator (geepers_conductor) for intelligent routing
- Infrastructure agents (Caddy, services, validators)
- Quality agents (accessibility, performance, security, testing)
- Frontend agents (CSS, design, motion, UX)
- Game development support
- MCP server integration
```

---

#### 2. **Claude Code Official (ASPIRATION - NOT PR)**
**Priority:** MEDIUM
**Effort:** VERY HIGH
**Reasoning:**
- Official Anthropic repository
- Not a community marketplace (read-only)
- Would need direct contact with Anthropic team
- Extremely selective (13 official plugins only)
- Best saved for when geepers matures further

**Action:** Contact Anthropic developers team directly, not via PR

---

#### 3. **Taskmaster Integration (RESEARCH PHASE)**
**Priority:** LOW
**Effort:** MEDIUM
**Reasoning:**
- Taskmaster is a task management system, not a plugin marketplace
- Could integrate geepers agents into Taskmaster's MCP server
- Different type of integration than plugin marketplace submission
- Worth exploring after Puerto submission succeeds

**Action:** Research how to integrate with Taskmaster's MCP tool ecosystem

---

### Files to Create/Modify for PR

#### For Puerto Submission:
```
puerto/plugins/geepers/
├── .claude-plugin/
│   └── plugin.json              # New - plugin metadata
├── agents/                       # Symlink to ~/geepers/agents/
├── geepers/                      # Symlink to ~/geepers/geepers/
├── README.md                     # New - comprehensive documentation
├── INSTALLATION.md               # New - detailed setup guide
├── EXAMPLES.md                   # New - usage examples
└── LICENSE                       # New - MIT License reference
```

#### `.claude-plugin/plugin.json` Structure:
```json
{
  "schema": "1.0",
  "name": "geepers",
  "version": "1.0.0",
  "description": "63-agent orchestration system for infrastructure, quality, frontend, fullstack, games, and more",
  "author": "Luke Steuber",
  "license": "MIT",
  "tags": ["orchestration", "agents", "infrastructure", "quality", "frontend"],
  "agents": [
    {
      "id": "geepers_conductor",
      "path": "agents/master/geepers_conductor.md"
    },
    // ... more agents
  ],
  "requirements": {
    "minVersion": "1.0.0"
  }
}
```

---

## Current Geepers Presence

### In Geepers Marketplace (Our Own)
- **Status:** Published
- **URL:** https://github.com/lukeslp/geepers
- **Installation:** `/plugin add lukeslp/geepers`
- **Contents:** 63 agents across 13 categories
- **Recent Updates:** Dec 18, 2024 (README and agent reorganization)

### Directory Structure
```
~/.claude/plugins/marketplaces/
├── geepers-marketplace/           # Our own marketplace (GitHub-hosted)
├── puerto/                        # Band of AI marketplace (SUBMIT HERE)
├── claude-code-plugins/           # Anthropic official (contact only)
├── taskmaster/                    # Task management system (integration potential)
└── ... 4 other less relevant marketplaces
```

---

## Action Plan

### Phase 1: Puerto Submission (Week of Dec 18)
1. ✓ Research complete (this document)
2. Fork bandofai/puerto
3. Create `plugins/geepers/` directory with:
   - `.claude-plugin/plugin.json` - comprehensive metadata
   - Symlinks to agents and geepers code (or copy relevant files)
   - README.md with full documentation
   - LICENSE file
4. Add entry to puerto's main README.md (plugins list)
5. Create PR with comprehensive description
6. Monitor for feedback and iterate

### Phase 2: Documentation Polish
1. Ensure comprehensive README in geepers plugin
2. Add examples of agent usage
3. Document all 63 agents with categories
4. Include troubleshooting section

### Phase 3: Future Opportunities
1. After Puerto success: Consider Claude Code official (needs Anthropic contact)
2. Evaluate Taskmaster MCP integration
3. Monitor for new community marketplaces

---

## Key Contacts

- **Puerto (Band of AI):** GitHub issues in bandofai/puerto
- **Claude Code Official:** Anthropic Developers Discord / developers@anthropic.com
- **Taskmaster:** GitHub issues in eyaltoledano/claude-task-master (Discord: discord.gg/taskmasterai)

---

## Research Notes

### What We Learned

1. **Puerto is the clear winner** for first submission:
   - Lightweight process
   - Community-focused
   - No complex requirements
   - Only 2 existing plugins (less crowded)

2. **Claude Code official is aspirational:**
   - Not accepting random PRs
   - Direct contact needed
   - Save for when geepers is very mature

3. **Taskmaster is a different beast:**
   - Not a plugin marketplace
   - Could integrate geepers agents
   - Worth exploring separately

4. **No previous activity:**
   - Zero PRs from lukeslp in any marketplace
   - This is our first marketplace submission
   - Fresh start, high potential for success

---

## Files Not Modified

- ✓ No git repos modified
- ✓ No plugin directories changed
- ✓ No submissions made
- ✓ All research is local and non-destructive

---

**Research completed by:** Claude Code
**Status:** Ready for Action Phase
**Next Step:** Approve Phase 1 (Puerto Submission)

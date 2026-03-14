# Codex & Manus Platform Structure Mapping

**Last Updated**: 2026-03-06
**Source**: Complete directory and file scan of `~/geepers/platforms/` directories

---

## Executive Summary

The geepers ecosystem uses a **multi-platform distribution model**. The same 23 skills are packaged identically for 5 different platforms:

1. **Claude** (Claude Code plugin + desktop skills)
2. **Codex** (Codex CLI)
3. **Manus** (Manus runtime)
4. **Gemini** (Google's Gemini platform)
5. **ClawHub** (API-based skills platform)

Each platform has an **identical `skills/` directory structure** with the same 23 skill definitions, but uses platform-specific metadata files for configuration and discovery.

---

## Directory Structure Overview

### Codex Platform (`~/geepers/platforms/codex/`)

```
codex/
├── README.md                      # Platform overview (23 skills, list of inclusions)
├── aliases.json                   # ID → name/description mappings for all 23 skills
├── codex-package.json             # Skill manifest (JSON format, used by Codex)
├── manifest.generated.json        # Generated manifest (30 lines, auto-built)
├── SYNC_INFO.md                   # Build metadata & rebuild instructions
├── skills/
│   ├── builder/                   # Generic skill (framework/orchestration)
│   ├── data-fetch/                # Data fetching skill
│   ├── datavis/                   # Data visualization
│   ├── dream-swarm/               # Parallel multi-agent orchestration
│   ├── engineering/               # Engineering domain orchestrator
│   ├── executive/                 # Executive decision-making
│   ├── finance/                   # Finance domain
│   ├── git-hygiene-guardian/      # Git repo cleanup
│   ├── mcp-orchestration/         # MCP server integration & orchestration
│   ├── planner/                   # Task planning & decomposition
│   ├── product/                   # Product management PRD generation
│   ├── quality/                   # Quality audit orchestrator (a11y, perf, api, deps)
│   ├── scout/                     # Project reconnaissance
│   ├── server-deploy/             # Service deployment & Caddy routing
│   ├── swarm/                     # Parallel multi-agent search
│   ├── team/                      # Team routing orchestrator
│   ├── testing/                   # Testing strategy & implementation
│   ├── validator/                 # Config & integration validation
│   ├── geepers-corpus/            # COCA corpus linguistics API
│   ├── geepers-data/              # Aggregated data API
│   ├── geepers-datavis/           # Datavis API skill (duplicate: datavis)
│   ├── geepers-deploy/            # Deployment API skill (duplicate: server-deploy)
│   ├── geepers-dream-swarm/       # Dream Swarm API skill (duplicate: dream-swarm)
│   ├── geepers-engineering/       # Engineering API skill (duplicate: engineering)
│   ├── geepers-etymology/         # Etymology/linguistics API
│   ├── geepers-executive/         # Executive API skill (duplicate: executive)
│   ├── geepers-fetch/             # Data fetching API skill (duplicate: data-fetch)
│   ├── geepers-finance/           # Finance API skill (duplicate: finance)
│   ├── geepers-git/               # Git management API skill
│   ├── geepers-llm/               # LLM provider access API
│   ├── geepers-mcp/               # MCP integration API (duplicate: mcp-orchestration)
│   ├── geepers-orchestrate/       # Dream Cascade/Swarm API execution
│   ├── geepers-planner/           # Planner API skill (duplicate: planner)
│   ├── geepers-product/           # Product API skill (duplicate: product)
│   ├── geepers-quality/           # Quality API skill (duplicate: quality)
│   ├── geepers-scout/             # Scout API skill (duplicate: scout)
│   ├── geepers-swarm/             # Swarm API skill (duplicate: swarm)
│   ├── geepers-team/              # Team routing API skill (duplicate: team)
│   ├── geepers-testing/           # Testing API skill (duplicate: testing)
│   ├── geepers-validate/          # Validation API skill (duplicate: validator)
│   ├── geepers-builder/           # Builder API skill (duplicate: builder)
└── skills/ (continued)
    └── ... (all skills follow same SKILL.md format)
```

**Total Skills in Codex**: 47 directories (19 core + 28 API variants)

### Manus Platform (`~/geepers/platforms/manus/`)

```
manus/
├── README.md                      # Platform overview (identical to Codex)
├── aliases.json                   # ID → name/description mappings
├── manus-skills.json              # Skill manifest (JSON format, used by Manus)
├── manifest.generated.json        # Generated manifest (30 lines, auto-built)
├── SYNC_INFO.md                   # Build metadata & rebuild instructions
└── skills/
    └── [IDENTICAL STRUCTURE TO CODEX - all 47 skill directories]
```

**Total Skills in Manus**: 47 directories (same as Codex)

---

## Key Configuration Files

### `codex-package.json` / `manus-skills.json` Format

Both platforms use identical JSON structure to register skills:

```json
{
  "name": "geepers-codex-package",  // or "geepers-manus-package"
  "version": "1.0.0",
  "built_at": "2026-02-19T08:07:12.181910+00:00",
  "runtime": "manus",                // Only in Manus; absent in Codex
  "skills": [
    {
      "id": "skill-name",
      "path": "skills/skill-name"
    },
    // ... repeated for all 23 core skills
  ]
}
```

**Note**: Only 23 skills listed in manifest (not 47). The 28 API variants are discovered via other means (likely REST API endpoints).

### `aliases.json` Format

Maps skill IDs to human-readable names and descriptions:

```json
{
  "skill-id": {
    "name": "Human Readable Name",
    "description": "What this skill does"
  }
}
```

### `manifest.generated.json`

Auto-generated file (30 lines). Purpose: likely a canonical manifest used for syncing across platforms.

### `SYNC_INFO.md`

Metadata about the build:
- Platform name
- Skill count
- Build timestamp
- Source file (typically `geepers/manifests/skills-manifest.yaml`)
- Rebuild command: `python3 scripts/build-platform-packages.py --platform {codex|manus} --clean`

---

## Skill Structure (Individual Skill Format)

Each skill is a directory with the following structure:

### Basic Skill (Non-API variant, e.g., `/quality/`)

```
skill-name/
├── SKILL.md                       # Skill definition (Markdown with YAML frontmatter)
├── scripts/                       # Optional: Python/shell scripts
├── src/                           # Optional: Source code for API servers
├── reference/                     # Optional: Reference materials
└── dist/                          # Optional: Pre-built distributions (wheels, tarballs)
```

### SKILL.md Format

```yaml
---
name: skill-name
description: "What this skill does. Can be multi-line.\nIncludes <example> tags with Context/user/assistant."
---

## Mission
Description of what this skill does

## Codex Notes (platform-specific)
Notes specific to the platform (e.g., "This is a Codex CLI skill; treat geepers_* mentions as related skills to invoke explicitly")

## Key Sections
- Output Locations (logs, reports, HTML)
- Workflow Modes
- Coordination Protocol
- Scoring Systems (where applicable)
- Quality Standards
- Triggers (when to use)
```

### Example: Quality Skill (`geepers-quality/`)

- **SKILL.md**: Defines the quality orchestrator (coordinates a11y, perf, api, deps agents)
- **No scripts**: Pure orchestration, calls other agents
- **Output**: Reports to `~/geepers/reports/by-date/YYYY-MM-DD/quality-{project}.md`

### Example: Data Fetch Skill (`geepers-fetch/`)

- **SKILL.md**: Defines data fetching capabilities
- **`src/`**: Server implementation for data fetching API
- **`scripts/`**: Fetch utilities for different APIs (arxiv, etc.)
- **Pre-built lib**: `src/lib/data_fetching/` with 17+ client modules
  - `arxiv_client.py`
  - `census_client.py`
  - `github_client.py`
  - `nasa_client.py`
  - `wikipedia_client.py`
  - `youtube_client.py`
  - ... and 11 others
  - `factory.py` (client factory)

### Example: Product Skill (`product/`)

- **SKILL.md**: Defines PRD generation capabilities
- **`src/server.py`**: Flask server implementation
- **`server.json`**: Server configuration metadata
- **`pyproject.toml`**: Python package definition
- **`dist/`**: Pre-built wheel and tarball (geepers_product-0.1.0)

---

## Platform Comparison Table

| Aspect | Codex | Manus | Claude | Gemini | ClawHub |
|--------|-------|-------|--------|--------|---------|
| **Root Dir** | `~/geepers/platforms/codex/` | `~/geepers/platforms/manus/` | `~/geepers/platforms/claude/` | `~/geepers/platforms/gemini/` | `~/geepers/platforms/clawhub/` |
| **Manifest File** | `codex-package.json` | `manus-skills.json` | (generated) | (generated) | (generated) |
| **Core Skills** | 23 | 23 | 23 | 23 | 23 |
| **API Variants** | 28 | 28 | 28 | 28 | 28 |
| **Total Dirs** | 47 | 47 | 47 | 47 | 47 |
| **Structure** | ✅ Identical | ✅ Identical | ✅ Identical | ✅ Identical | ✅ Identical |
| **All Share** | Same `skills/` directory content | Same `skills/` directory content | Same `skills/` directory content | Same `skills/` directory content | Same `skills/` directory content |

---

## Current Accessibility-Related Skills

### Existing Accessibility Coverage

**In Quality Orchestrator** (`geepers-quality/`):
- Coordinates `geepers_a11y` agent for accessibility audits
- Generates WCAG compliance reports
- Produces accessibility findings + recommendations
- Part of the "is it good enough?" quality check

**In Frontend Orchestrator** (implied, referenced in CLAUDE.md):
- Works with design, CSS, and accessibility agents
- Focus on CSS accessibility patterns
- Likely keyboard navigation, color contrast checks

### No Dedicated Accessibility Skills Found

Search revealed:
- ❌ No `geepers-a11y/` in `skills/` directories
- ❌ No `accessibility/` skill
- ❌ No accessibility-specific SKILL.md files
- ✅ Quality orchestrator calls accessibility agents (but agents are not skills themselves)

---

## Adding Accessibility Skills to Codex & Manus

Based on the current structure, here's what needs to be done:

### Step 1: Create Skill Directories

For each new accessibility skill, create identically-named directories in:
- `/home/coolhand/geepers/platforms/codex/skills/{skill-name}/`
- `/home/coolhand/geepers/platforms/manus/skills/{skill-name}/`

### Step 2: Add SKILL.md Files

Each must follow the format:

```yaml
---
name: {human-readable-name}
description: "{What it does}"
---

## Mission
[Content]

## Codex/Manus Notes
This is a Codex/Manus CLI skill; treat geepers_* mentions as related skills to invoke explicitly.

## [Other Sections]
```

### Step 3: Update Configuration Files

1. **Add to `codex-package.json`** and **`manus-skills.json`**:

```json
{
  "id": "geepers-accessibility",
  "path": "skills/geepers-accessibility"
}
```

2. **Add to `aliases.json`** (both platforms):

```json
{
  "geepers-accessibility": {
    "name": "Accessibility Auditor",
    "description": "Comprehensive accessibility compliance checking"
  }
}
```

3. **Rebuild manifests**:

```bash
python3 scripts/build-platform-packages.py --platform codex --clean
python3 scripts/build-platform-packages.py --platform manus --clean
```

### Step 4: Optional - Add Optional Components

If the skill needs server implementation:
- Add `src/server.py` (Flask app with `/health` endpoint)
- Add `src/` directory with supporting libraries
- Add `scripts/` for utilities
- Add `pyproject.toml` for package metadata

---

## Integration Patterns

### Skill Invocation Pattern in Codex/Manus

Skills are referenced like:
```
geepers_{skill-name}
```

Examples:
- `geepers_quality` - Quality orchestrator
- `geepers_a11y` - Accessibility agent (invoked by quality)
- `geepers_fetch` - Data fetching
- `geepers_scout` - Project reconnaissance

### Accessibility Skills Should Follow

**Option A**: Create a new `geepers_accessibility` skill that:
- Acts like an orchestrator (similar to quality, engineering, executive)
- Coordinates multiple accessibility check agents
- Generates comprehensive accessibility reports
- Outputs to `~/geepers/reports/by-date/YYYY-MM-DD/accessibility-{project}.md`

**Option B**: Create individual skills:
- `geepers_wcag_auditor` - WCAG 2.1 compliance
- `geepers_keyboard_navigator` - Keyboard navigation testing
- `geepers_color_contrast` - Color contrast analysis
- `geepers_screen_reader` - Screen reader compatibility
- Each callable independently or via quality orchestrator

---

## Build & Deployment

### Current Build Process

All 5 platforms use the same build script:

```bash
python3 scripts/build-platform-packages.py --platform {codex|manus|claude|gemini|clawhub} --clean
```

This script:
1. Reads canonical source (`geepers/manifests/skills-manifest.yaml`)
2. Generates `manifest.generated.json` for each platform
3. Syncs `aliases.json`
4. Updates `{platform}-package.json` or `{platform}-skills.json`

### Source of Truth

**File**: `~/geepers/manifests/skills-manifest.yaml`

All platform packages are generated from this single source file. Changes made directly to platform directories may be overwritten on rebuild.

### Sync Info

Each platform's `SYNC_INFO.md` tracks:
- Platform name
- Skill count
- Build timestamp
- Rebuild command

---

## File Summary

### Codex Platform Files

```
~/geepers/platforms/codex/
├── README.md                    (67 lines) - Overview, install, ecosystem
├── aliases.json                 - Skill ID mappings
├── codex-package.json           (100 lines) - Manifest (23 core skills)
├── manifest.generated.json      (30 lines) - Auto-generated canonical manifest
├── SYNC_INFO.md                 (13 lines) - Build metadata
└── skills/                      - 47 skill directories
```

### Manus Platform Files

```
~/geepers/platforms/manus/
├── README.md                    (67 lines) - Overview, install, ecosystem
├── aliases.json                 - Skill ID mappings
├── manus-skills.json            (100 lines) - Manifest (23 core skills)
├── manifest.generated.json      (30 lines) - Auto-generated canonical manifest
├── SYNC_INFO.md                 (13 lines) - Build metadata
└── skills/                      - 47 skill directories
```

### Shared Skill Directories (Both Platforms)

Each skill directory contains:

**Typical Structure** (quality, planner, engineer, etc.):
```
{skill-name}/
└── SKILL.md                     (200-300 lines) - Definition & workflow
```

**Complex Structure** (with server, datavis, etc.):
```
{skill-name}/
├── SKILL.md
├── src/
│   ├── server.py                - Flask/HTTP server
│   ├── lib/                      - Supporting libraries
│   └── test_*.py
├── scripts/
│   ├── fetch-*.py               - Utility scripts
│   └── server.py
├── reference/
│   ├── gallery.md
│   ├── examples.md
│   └── ...
├── dist/
│   ├── *.whl                    - Pre-built wheels
│   └── *.tar.gz                 - Tarballs
├── pyproject.toml               - Package metadata
├── server.json                  - Server config
└── README.md
```

---

## Key Insights for Accessibility Skills

1. **No hierarchy between platforms** - Codex and Manus are treated equally
2. **Shared source** - All changes go to the source once, rebuild for each platform
3. **Skill.md is primary** - The SKILL.md file is the definitive documentation
4. **Output locations** - Skills should write reports to `~/geepers/reports/by-date/YYYY-MM-DD/`
5. **Coordination protocol** - Skills document how they work with other agents/skills
6. **Platform notes** - Add "Codex Notes" or "Manus Notes" sections if platform-specific behavior differs
7. **No existing a11y skills** - Quality orchestrator *references* `geepers_a11y` agent, but there's no corresponding skill directory

---

## Recommended Next Steps

To add accessibility skills to Codex & Manus:

1. **Decide on skill structure**:
   - Single `geepers-accessibility` orchestrator, OR
   - Multiple specialized accessibility skills (WCAG, keyboard, contrast, etc.)

2. **Create skill directories**:
   - `/codex/skills/geepers-accessibility/`
   - `/manus/skills/geepers-accessibility/`

3. **Write SKILL.md** with:
   - Clear mission & use cases
   - Accessibility standards (WCAG 2.1 AA/AAA)
   - Output locations
   - Coordination with quality orchestrator
   - Example invocations

4. **Update manifests**:
   - `skills-manifest.yaml` (source of truth)
   - Run rebuild script for both platforms

5. **Add aliases.json entries** for discoverability

6. **Test accessibility workflows**:
   - Invoke via Codex CLI
   - Invoke via Manus runtime
   - Verify output reports are generated

---

## Related Documentation

- **Geepers CLAUDE.md**: `~/geepers/CLAUDE.md` - Overall geepers architecture
- **Root CLAUDE.md**: `~/CLAUDE.md` - System-wide architecture
- **Skills source**: `~/geepers/skills/source/` - Editable skill definitions (before zipping)
- **Build script**: `scripts/build-platform-packages.py` - Platform package generation
- **Manifests**: `~/geepers/manifests/` - Canonical skill manifest

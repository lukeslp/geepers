# Implementation Plan - Skill & MCP Integration

## Goal
Integrate the foundational components found in `@temp` (`data_fetching`, `document_generation`, `llm_providers`) into the `geepers/skills` ecosystem. This will upgrade existing skills and create new ones, making them ready for Claude Desktop and MCP usage.

## Architecture Change
We are moving from a set of loose library files in `@temp` to structured **Claude Skills** and **MCP Servers**.

### 1. Skill: `data-fetch` (Enhanced)
*   **Source**: `geepers/skills/source/data-fetch`
*   **Integration**:
    *   Copy `geepers/temp/data_fetching` library to `geepers/skills/source/data-fetch/src/lib`.
    *   Create a robust MCP server entry point (`server.py`) that exposes all 12+ clients as tools.
    *   Update `SKILL.md` to expose these new capabilities to Claude.

### 2. Skill: `dream-cascade` (Research Engine)
*   **Source**: `geepers/skills/source/dream-cascade`
*   **Integration**:
    *   Copy `geepers/temp/llm_providers` -> `.../dream-cascade/src/lib/llm`
    *   Copy `geepers/temp/document_generation` -> `.../dream-cascade/src/lib/reporting`
    *   Copy `geepers/temp/SNIPPETS/agent-orchestration` -> `.../dream-cascade/src/lib/orchestration`
    *   Implement the `cascade-research.py` script using these libraries.
    *   Implement `server.py` (MCP Server) exposing `start_research` tool.

### 3. Skill: `datavis` (Data Storyteller)
*   **Source**: `geepers/skills/source/datavis`
*   **Integration**:
    *   Populate with D3 patterns from `geepers/temp/SNIPPETS`.
    *   Create a "Visualization Generator" script that takes JSON and outputs HTML/JS.

## Proposed Steps

### Phase 1: Data Fetching Skill
- [ ] Create `geepers/skills/source/data-fetch/src` structure.
- [ ] Copy `geepers/temp/data_fetching` content.
- [ ] Create `server.py` (MCP Server) exposing:
    - `fetch_census_data`
    - `fetch_arxiv_papers`
    - `fetch_weather`
    - ... (one tool per client source)
- [ ] Create `SKILL.md` with prompts to use these tools.

### Phase 2: MCP Orchestration Skill (formerly Dream Cascade)
- [ ] Create `geepers/skills/source/mcp-orchestration` structure.
    - [ ] `scripts/`
    - [ ] `src/lib/`
- [ ] **Library Integration**:
    - [ ] `document_generation` -> `src/lib/reporting`
    - [ ] `llm_providers` -> `src/lib/llm`
    - [ ] `agent-orchestration` snippets -> `src/lib/orchestration`
- [ ] **Script Implementation**:
    - [ ] `scripts/orchestrator.py` (Main entry point)
    - [ ] `scripts/cascade.py` (Dream Cascade logic)
    - [ ] `scripts/swarm.py` (Dream Swarm logic)
    - [ ] `scripts/monitor.py` (Job monitoring)
    - [ ] `scripts/server.py` (MCP Server implementation)
- [ ] **Documentation**:
    - [ ] `SKILL.md` (metadata & guide)
    - [ ] `reference/examples.md`

### Phase 3: Remaining Core Skills
- [ ] `datavis` (Data Storyteller)
- [ ] `server-deploy`
- [ ] `code-quality`

### Phase 3: Packaging
- [ ] For each skill, run the zip archival process using the provided `rebuild-zips.sh` logic (or manually zip).

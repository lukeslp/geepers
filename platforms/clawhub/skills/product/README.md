# Geepers Product Skill (`geepers-product`)

The "Product Team in a Box". A specialized Product Management agent capable of bidirectional translation between Business Strategy and Engineering Implementation.

## Core Capabilities (Bidirectional Flow)

### 1. 🔄 Reverse Engineering (Engineering -> PRD)
*   **Tool**: `dream_product_reverse_engineer`
*   **Use Case**: Feed it an existing codebase, a messy prototype, or raw engineering outputs.
*   **Output**: A professional **Product Requirements Document (PRD)** including:
    *   Executive Summary
    *   User Personas
    *   User Stories
    *   Technical Architecture (Inferred)
    *   Success Metrics (KPIs)

### 2. 🏗️ Engineering Handoff (PRD -> Engineering)
*   **Tool**: `dream_product_handoff`
*   **Use Case**: Feed it an approved PRD.
*   **Output**: A **Technical Execution Plan** formatted for an Agent Swarm or Engineering Team.
    *   Component Breakdown
    *   Specific Engineering Tasks
    *   Acceptance Criteria
    *   API Contract Stubs

### 3. 🚀 Go-To-Market Strategy
*   **Tool**: `dream_product_market_plan`
*   **Output**: Comprehensive GTM strategy (Audience, Pricing, Distribution).

### 4. ⚖️ Strategic Critique
*   **Tool**: `dream_product_critique`
*   **Output**: "Brutal Honest" analysis of gaps, risks, and flaws.

## Configuration

Add to your `claude_desktop_config.json`:

```json
"geepers-product": {
  "command": "python3",
  "args": ["/path/to/geepers/skills/source/product/src/server.py"],
  "env": {
    "OPENAI_API_KEY": "sk-...",
    "XAI_API_KEY": "xai-..."
  }
}
```

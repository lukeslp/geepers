# MCP Orchestration Skill (formerly Dream Cascade)

The **MCP Orchestration** skill provides advanced multi-agent coordination patterns for Claude. It allows you to launch massive, hierarchical research swarms or task-specific agent teams to solve complex problems that require multiple perspectives or large-scale data processing.

## Architecture: Dream Cascade

The primary pattern is the **Dream Cascade**, a 3-tier hierarchical swarm:

1.  **Tier 1: Belters (Workers)**
    *   Parallel agents (1-30+) that execute specific subtasks.
    *   Each Belter has a unique specialization (Research, Analysis, Technical, etc.).
2.  **Tier 2: Drummers (Synthesizers)**
    *   Aggregation agents that synthesize every 5 Belter responses.
    *   They filter noise and highlight key findings from the worker tier.
3.  **Tier 3: Camina (Executive)**
    *   Final synthesis agent that provides a high-level strategic report based on Drummer syntheses.

## Features

*   **Hierarchical Synthesis**: Automatic aggregation of insights from large swarms.
*   **Multi-Provider Support**: Switch between Anthropic, OpenAI, Gemini, etc.
*   **Cost Optimization**: Uses `ProviderFactory` to select models based on tier and task complexity.
*   **Structured Reporting**: Generates Markdown, PDF, and DOCX reports via the `reporting` library.
*   **Parallel Execution**: Handled with `asyncio` and semaphore-based rate limiting.

## Setup

### Environment Variables
Ensure the following API keys are set:
*   `ANTHROPIC_API_KEY`
*   `OPENAI_API_KEY`
*   `GEMINI_API_KEY`
*   (Other providers defined in `src/core/llm/factory.py`)

### Claude Desktop Configuration
Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "orchestration": {
      "command": "python3",
      "args": ["/home/coolhand/geepers/skills/source/mcp-orchestration/scripts/server.py"]
    }
  }
}
```

## Available Tools

### `dream_orchestrate_research`
Starts a hierarchical 3-tier research workflow.

**Parameters:**
*   `task` (string, required): The research topic or question.
*   `num_agents` (integer): Total number of Belters (default: 5).
*   `enable_drummer` (boolean): Whether to enable synthesis tier (default: true).
*   `enable_camina` (boolean): Whether to enable executive tier (default: false).
*   `provider_name` (string): LLM provider to use (default: "anthropic").

## CLI Usage

You can also run the orchestrator directly from the command line:

```bash
# Basic run with 5 belters
python3 scripts/orchestrator.py "What is the future of AGIs?"

# Advanced run with 15 belters, 3 drummers, and 1 camina
python3 scripts/orchestrator.py "Analyze the global semiconductor supply chain" --belters 15 --drummers 3 --caminas 1 --pdf
```

## Internal Structure
*   `scripts/`: Executable entry points (CLI and Server).
*   `src/core/orchestration/`: Core logic and patterns.
*   `src/core/llm/`: Unified provider factory.
*   `src/core/reporting/`: Multi-format report generation.
*   `reference/`: Examples and templates.

# MCP Orchestration Examples

This document provides examples of how to use the MCP Orchestration skill for various research and coordination tasks.

## Example 1: Basic Research Swarm
Use 5 agents to get a balanced perspective on a topic.

**Tool Call:**
```json
{
  "name": "dream_orchestrate_research",
  "arguments": {
    "task": "Pros and cons of nuclear fusion vs. fission for space travel"
  }
}
```

## Example 2: Large-Scale Technical Analysis
Use 15 agents with a full hierarchy (Drummers and Camina) for a deep dive.

**Tool Call:**
```json
{
  "name": "dream_orchestrate_research",
  "arguments": {
    "task": "Technical roadmap for 2nm semiconductor manufacturing",
    "num_agents": 15,
    "enable_drummer": true,
    "enable_camina": true
  }
}
```

## Example 3: CLI Usage for Local Reports
Generating a PDF report from the terminal.

```bash
python3 scripts/orchestrator.py "History of the Mediterranean Bronze Age collapse" --belters 10 --drummers 2 --pdf
```

## Example 4: Using a Specific Provider
Running the swarm using Gemini Pro for cost-efficiency.

```bash
python3 scripts/orchestrator.py "Sustainable urban farming techniques" --provider gemini --model gemini-1.5-pro
```

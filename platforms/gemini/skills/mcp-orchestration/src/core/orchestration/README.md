# Agent Orchestration Patterns

Comprehensive patterns for building hierarchical multi-agent systems extracted from the Beltalowda platform - a production-grade orchestration system for coordinating swarms of AI agents.

## Overview

These patterns enable scalable coordination of multiple AI agents working in parallel with hierarchical synthesis. The three-tier architecture (Workers → Synthesizers → Executive) automatically scales based on agent count and provides robust error handling, retry logic, and cost tracking.

## Patterns Included

### 1. Hierarchical Agent Coordination
**File:** `hierarchical_agent_coordination.py`

Complete implementation of a three-tier agent hierarchy:
- **Tier 1 (Belters):** Individual task execution agents with specializations
- **Tier 2 (Drummers):** Synthesize outputs from 5 Belters
- **Tier 3 (Camina):** Executive synthesis when 2+ Drummers exist

Key features:
- Automatic scaling of synthesis layers
- Parallel execution with rate limiting
- Progressive temperature reduction for consistency
- Timeout and retry handling

### 2. Parallel Agent Execution
**File:** `parallel_agent_execution.py`

Advanced parallel execution patterns with:
- Semaphore-based concurrency control
- Per-agent timeout handling
- Automatic retry logic for transient failures
- Progress tracking and callbacks
- Graceful degradation on partial failures

### 3. Task Decomposition
**File:** `task_decomposition_pattern.py`

Intelligent task breakdown patterns:
- LLM-based decomposition with fallback
- Domain-specific strategies (research, software, analysis, planning)
- Automatic padding to match agent count
- Subtask validation and quality checking

### 4. Agent Lifecycle Management
**File:** `agent_lifecycle_management.py`

Complete agent lifecycle tracking:
- State management (PENDING → RUNNING → COMPLETED/FAILED)
- Health monitoring and validation
- Metrics tracking (success rate, execution time, cost)
- AgentPoolManager for centralized control

### 5. Provider Abstraction
**File:** `provider_abstraction_pattern.py`

Unified interface for multiple LLM providers:
- Provider-agnostic agent design
- Streaming and non-streaming support
- Cost estimation and budget management
- Model capability detection
- Factory pattern for instantiation

## Architecture Diagram

```
                    ┌─────────────────┐
                    │  Orchestrator   │
                    └────────┬────────┘
                             │
                ┌────────────┼────────────┐
                │            │            │
          [Decompose]   [Coordinate]  [Synthesize]
                │            │            │
                ▼            ▼            ▼
         ┌──────────┐  ┌──────────┐  ┌──────────┐
         │  Tasks   │  │ Belters  │  │ Drummers │
         │  (3-15)  │  │ (1-30)   │  │ (1-6)    │
         └──────────┘  └──────────┘  └──────────┘
                             │            │
                             │            ▼
                             │      ┌──────────┐
                             │      │  Camina  │
                             │      │ (0-1)    │
                             │      └──────────┘
                             │            │
                             └────────────┘
                                    │
                              ┌──────────┐
                              │  Result  │
                              └──────────┘
```

## Quick Start

### Basic Multi-Agent Execution

```python
from hierarchical_agent_coordination import (
    HierarchicalOrchestrator,
    OrchestratorConfig
)

# Configure orchestrator
config = OrchestratorConfig(
    num_agents=10,           # 10 Belters, 2 Drummers, 1 Camina
    enable_drummer=True,
    enable_camina=True,
    max_concurrent_agents=5,
    belter_timeout=60,
    drummer_timeout=90,
    camina_timeout=120
)

# Create orchestrator
orchestrator = HierarchicalOrchestrator(config)

# Execute task
result = await orchestrator.execute_task(
    task="Analyze the impact of AI on healthcare",
    stream_callback=my_progress_callback
)

print(f"Belters: {len(result['belter_responses'])}")
print(f"Drummers: {len(result['drummer_responses'])}")
print(f"Camina: {result['camina_response'] is not None}")
```

### Parallel Execution with Rate Limiting

```python
from parallel_agent_execution import ParallelExecutor, ParallelExecutionConfig

# Configure executor
config = ParallelExecutionConfig(
    max_concurrent=5,
    timeout_seconds=30.0,
    enable_retries=True,
    max_retries=2
)

executor = ParallelExecutor(config)

# Execute tasks in parallel
tasks = [my_async_function1, my_async_function2, ...]
results = await executor.execute_parallel(tasks)
```

### Task Decomposition

```python
from task_decomposition_pattern import DomainSpecializedDecomposer, DecompositionConfig

# Configure decomposer
config = DecompositionConfig(
    min_subtasks=3,
    max_subtasks=15,
    target_agent_count=10
)

decomposer = DomainSpecializedDecomposer(config)

# Decompose task
result = await decomposer.decompose_task(
    task="Research climate change effects on agriculture"
)

print(f"Generated {len(result.subtasks)} subtasks")
for i, subtask in enumerate(result.subtasks, 1):
    print(f"{i}. {subtask}")
```

### Agent Lifecycle Management

```python
from agent_lifecycle_management import AgentPoolManager, BaseAgent

# Create pool manager
pool = AgentPoolManager()

# Register agents
for i in range(5):
    agent = MyAgent(agent_id=f"worker_{i}", role=AgentRole.WORKER)
    await agent.initialize()
    pool.register_agent(agent, group="workers")

# Get pool statistics
stats = pool.get_pool_statistics()
print(f"Total agents: {stats['total_agents']}")
print(f"Success rate: {stats['average_success_rate']:.1%}")

# Cleanup
await pool.shutdown_all()
```

## Design Principles

1. **Hierarchical Synthesis:** Agents work in tiers, with each tier synthesizing outputs from the tier below
2. **Automatic Scaling:** System automatically creates appropriate number of synthesizers based on worker count
3. **Parallel Execution:** Workers execute in parallel with semaphore-based rate limiting
4. **Fault Tolerance:** Timeout handling, retry logic, and graceful degradation
5. **Provider Agnostic:** Agents work with any LLM provider through abstraction layer
6. **Metrics Tracking:** Comprehensive tracking of execution time, costs, and success rates
7. **Progressive Synthesis:** Each tier uses lower temperature for more consistent synthesis

## Configuration Guidelines

### Agent Count Scaling

- **1-4 agents:** Only Belters (no synthesis layers)
- **5-9 agents:** Belters + 1 Drummer
- **10-14 agents:** Belters + 2 Drummers + 1 Camina
- **15-19 agents:** Belters + 3 Drummers + 1 Camina
- **20+ agents:** Belters + 4+ Drummers + 1 Camina

### Timeout Recommendations

- **Belter timeout:** 60-180 seconds (individual tasks)
- **Drummer timeout:** 90-240 seconds (synthesis of 5 tasks)
- **Camina timeout:** 120-300 seconds (executive synthesis)
- **Overall timeout:** 300-600 seconds (full orchestration)

### Concurrency Limits

- **Conservative:** max_concurrent = 3-5 (rate-limited APIs)
- **Moderate:** max_concurrent = 5-10 (standard APIs)
- **Aggressive:** max_concurrent = 10-20 (high-throughput systems)

## Integration Examples

### With Swarm Tool System

```python
from swarm_module_pattern import SwarmModuleBase
from hierarchical_agent_coordination import HierarchicalOrchestrator

class ResearchOrchestrator(SwarmModuleBase):
    def __init__(self):
        self.orchestrator = HierarchicalOrchestrator(config)

    def get_tool_schemas(self):
        return [{
            "name": "research_swarm",
            "description": "Execute research using agent swarm",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {"type": "string"},
                    "agent_count": {"type": "integer"}
                }
            }
        }]

    async def handle_tool_calls(self, tool_calls):
        for call in tool_calls:
            if call["name"] == "research_swarm":
                result = await self.orchestrator.execute_task(
                    task=call["args"]["task"]
                )
                return result
```

### With Streaming UI

```python
async def stream_callback(event_type, data):
    """Send updates to web UI via SSE"""
    yield f"event: {event_type}\n"
    yield f"data: {json.dumps(data)}\n\n"

@app.route('/orchestrate')
async def orchestrate():
    return StreamingResponse(
        orchestrator.execute_task(
            task=request.args.get('task'),
            stream_callback=stream_callback
        ),
        mimetype='text/event-stream'
    )
```

## Performance Characteristics

### Execution Times (10 agents)

- **Sequential:** ~60 seconds (6s per agent)
- **Parallel (max_concurrent=5):** ~12 seconds
- **Parallel (max_concurrent=10):** ~6 seconds
- **With synthesis:** +5-10 seconds (Drummer + Camina)

### Cost Estimates (using GPT-4 equivalent)

- **Per Belter:** ~$0.01-0.03 per task
- **Per Drummer:** ~$0.05-0.10 per synthesis
- **Per Camina:** ~$0.10-0.20 per executive synthesis
- **10-agent swarm:** ~$0.30-0.50 total

## Common Patterns

### Research Swarm

```python
config = OrchestratorConfig(
    num_agents=15,
    enable_drummer=True,
    enable_camina=True,
    specializations=['research', 'analysis', 'news']
)
```

### Software Development Swarm

```python
config = OrchestratorConfig(
    num_agents=10,
    enable_drummer=True,
    enable_camina=False,  # Mid-level synthesis sufficient
    specializations=['coding', 'testing', 'documentation']
)
```

### Analysis Swarm

```python
config = OrchestratorConfig(
    num_agents=8,
    enable_drummer=True,
    enable_camina=False,
    specializations=['analysis', 'financial', 'technical']
)
```

## Troubleshooting

### Agents Timing Out

- Increase timeout values
- Reduce concurrent agents
- Check provider API latency
- Enable retries

### Inconsistent Synthesis

- Lower temperature for synthesis layers
- Increase context window size
- Improve task decomposition clarity

### High Costs

- Use cheaper models for Belters
- Reduce max_tokens
- Implement result caching
- Optimize task decomposition

## Source Attribution

All patterns extracted from:
- **Project:** Beltalowda Multi-Agent Orchestration Platform
- **Author:** Luke Steuber
- **Source Directory:** `/home/coolhand/projects/beltalowda/src/beltalowda/`
- **Primary Files:**
  - `orchestrator.py` - Main orchestration engine
  - `agents/base.py` - Agent base classes
  - `agents/belter.py` - Worker agents
  - `agents/drummer.py` - Synthesis agents
  - `agents/camina.py` - Executive synthesis
  - `providers/base.py` - Provider abstraction

## License

Extracted from open source projects. Use freely in your own projects. Attribution appreciated but not required.

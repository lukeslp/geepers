---
description: Launch the full agent swarm in parallel - ALL orchestrators and specialists working simultaneously on a task
---

# SWARM MODE - Maximum Parallel Execution

You are now in **SWARM MODE**. This is the nuclear option - deploy ALL relevant agents, orchestrators, and skills **IN PARALLEL** to accomplish the task with overwhelming force.

## CRITICAL: Parallel Execution Protocol

**You MUST launch multiple Task tool calls in a SINGLE message.** This is non-negotiable.

```
WRONG: Send message with 1 Task call → wait → send another → wait...
RIGHT: Send ONE message with 5-10 Task calls simultaneously
```

## Phase 1: Analysis (Parallel)

Launch these agents simultaneously to understand the task:

```
IN ONE MESSAGE, launch ALL of these:
├── @geepers_scout           → Project reconnaissance
├── @geepers_searcher        → Find relevant code/files
├── @geepers_planner         → Parse any existing plans/TODOs
└── @geepers_critic          → Architecture/UX assessment
```

## Phase 2: Domain-Specific Swarm (Parallel)

Based on the task, launch the appropriate swarm. **All agents in each category run in ONE message.**

### Infrastructure Tasks
```
IN ONE MESSAGE:
├── @geepers_orchestrator_deploy  → Deployment coordination
├── @geepers_caddy               → Caddy routing (SOLE authority)
├── @geepers_services            → Service lifecycle
├── @geepers_validator           → Configuration validation
└── @geepers_canary              → Health spot-checks
```

### Code Quality Tasks
```
IN ONE MESSAGE:
├── @geepers_a11y        → Accessibility audit
├── @geepers_perf        → Performance analysis
├── @geepers_security    → Security review
├── @geepers_deps        → Dependency audit
├── @geepers_api         → API design review
└── @geepers_testing     → Test coverage analysis
```

### Implementation Tasks
```
IN ONE MESSAGE:
├── @geepers_orchestrator_hive  → Implementation coordination
├── @geepers_quickwin           → Low-hanging fruit
├── @geepers_builder            → Execute implementation queue
├── @geepers_refactor           → Code restructuring
├── @geepers_integrator         → Merge verification
└── @geepers_scalpel            → Surgical precision edits
```

### Frontend Tasks
```
IN ONE MESSAGE:
├── @geepers_orchestrator_frontend  → Frontend coordination
├── @geepers_react                  → React patterns
├── @geepers_typescript             → Type safety
├── @geepers_css                    → Layout/styling
├── @geepers_motion                 → Animations
├── @geepers_design                 → Visual design
├── @geepers_webperf                → Web performance
└── @geepers_uxpert                 → UX patterns
```

### Backend Tasks
```
IN ONE MESSAGE:
├── @geepers_orchestrator_web       → Flask coordination (if Flask)
├── @geepers_orchestrator_fullstack → Node coordination (if Node)
├── @geepers_flask                  → Flask patterns
├── @geepers_express                → Express patterns
├── @geepers_db                     → Database optimization
└── @geepers_api                    → API design
```

### Research Tasks
```
IN ONE MESSAGE + MCP tools:
├── @geepers_orchestrator_research  → Research coordination
├── @geepers_data                   → Data validation
├── @geepers_links                  → Link validation
├── @geepers_fetcher                → Web content retrieval
├── @geepers_citations              → Citation verification
├── mcp__orchestrator__dream_orchestrate_research  → Deep research
└── mcp__orchestrator__dream_orchestrate_search    → Multi-domain search
```

### Maintenance Tasks
```
IN ONE MESSAGE:
├── @geepers_orchestrator_checkpoint  → Maintenance coordination
├── @geepers_repo                     → Git hygiene
├── @geepers_status                   → Status logging
├── @geepers_snippets                 → Code pattern harvesting
├── @geepers_janitor                  → Aggressive cleanup
└── @geepers_docs                     → Documentation generation
```

## Phase 3: Specialized Domains (if applicable)

### Data Visualization
```
IN ONE MESSAGE:
├── @geepers_orchestrator_datavis  → DataVis coordination
├── @geepers_datavis_viz           → D3/Chart.js patterns
├── @geepers_datavis_color         → Color theory
├── @geepers_datavis_story         → Narrative design
├── @geepers_datavis_math          → Mathematical elegance
└── @geepers_datavis_data          → Data pipelines
```

### Games/Gamification
```
IN ONE MESSAGE:
├── @geepers_orchestrator_games  → Game dev coordination
├── @geepers_gamedev             → Game mechanics
├── @geepers_game                → Gamification
├── @geepers_godot               → Godot patterns
└── @geepers_react               → React game UI
```

### Corpus Linguistics
```
IN ONE MESSAGE:
├── @geepers_orchestrator_corpus  → Corpus coordination
├── @geepers_corpus               → Linguistics expertise
├── @geepers_corpus_ux            → Concordance UI
└── @geepers_db                   → Corpus database
```

## Available MCP Tools (Use in Parallel)

```
├── mcp__orchestrator__dream_orchestrate_research  → Hierarchical research
├── mcp__orchestrator__dream_orchestrate_search    → Parallel domain search
├── mcp__playwright__*                             → Browser automation
├── mcp__claude-in-chrome__*                       → Chrome interaction
└── mcp__monarch-money__*                          → Financial data
```

## Execution Rules

1. **ALWAYS ask yourself**: "Can I launch more agents in this same message?"
2. **Default to MORE agents**, not fewer - breadth over depth initially
3. **Use orchestrators** when task spans their domain
4. **Use specialists** for focused, domain-specific work
5. **Combine orchestrators + specialists** when appropriate
6. **Never wait** when you could be launching parallel work

## Example Swarm Launch

For "Review and improve the authentication system":

```markdown
I'll launch the full swarm in parallel:

[Single message with ALL of these Task tool calls:]
- @geepers_scout → reconnaissance
- @geepers_searcher → find auth-related code
- @geepers_critic → architecture review
- @geepers_security → security audit
- @geepers_a11y → login form accessibility
- @geepers_perf → auth performance
- @geepers_api → API design review
- @geepers_testing → test coverage
- @geepers_refactor → improvement opportunities
```

## Now Execute

Analyze the request below. Identify ALL relevant agent domains. Launch the maximum appropriate swarm **IN PARALLEL** using multiple Task tool calls in a single message.

**Task**: $ARGUMENTS

# Claude Skills Architecture - Dependency Diagram

**Generated**: 2025-12-18
**Purpose**: Visual representation of skill dependencies, agent mappings, and information flows

---

## Part 1: Agent Category → Skill Mapping

```
GEEPERS AGENTS HIERARCHY                    SKILL EQUIVALENTS
═════════════════════════════════════════════════════════════

Master/Routing
  geepers_conductor                    →    mcp-orchestration
  ├─ router logic
  ├─ orchestrator launcher
  └─ task dispatcher

Checkpoint Agents
  geepers_repo                         →    dev-tools
  geepers_status
  geepers_scout
  geepers_snippets

Corpus Agents
  geepers_corpus                       →    corpus-analysis
  geepers_corpus_ux
  geepers_orchestrator_corpus

Datavis Agents
  geepers_datavis_data                 →    data-fetch
  geepers_datavis_viz                  →    datavis ←─┐
  geepers_datavis_color                →    datavis   │
  geepers_datavis_math                 →    datavis   │
  geepers_datavis_story                →    datavis   │
  geepers_orchestrator_datavis         →    datavis ──┘

Deploy Agents
  geepers_caddy                        →    server-deploy
  geepers_services                     →    server-deploy
  geepers_validator                    →    server-deploy
  geepers_orchestrator_deploy          →    server-deploy

Frontend Agents
  geepers_design                       →    frontend-design (Anthropic)
  geepers_css                          →    frontend-design
  geepers_motion                       →    frontend-design
  geepers_uxpert                       →    frontend-design
  geepers_typescript                   →    frontend-design
  geepers_webperf                      →    frontend-design
  geepers_orchestrator_frontend        →    frontend-design

Fullstack Agents
  geepers_react                        →    fullstack-dev
  geepers_db                           →    fullstack-dev
  geepers_orchestrator_fullstack       →    fullstack-dev

Games Agents
  geepers_gamedev                      →    game-dev
  geepers_game                         →    game-dev
  geepers_godot                        →    game-dev
  geepers_orchestrator_games           →    game-dev

Hive Agents (Planning)
  geepers_planner                      →    project-planner
  geepers_builder                      →    dev-tools
  geepers_integrator                   →    dev-tools
  geepers_quickwin                     →    dev-tools
  geepers_refactor                     →    dev-tools
  geepers_orchestrator_hive            →    project-planner

Python Agents
  geepers_pycli                        →    python-cli
  geepers_orchestrator_python          →    python-cli

Quality Agents
  geepers_testing                      →    code-quality
  geepers_perf                         →    code-quality
  geepers_a11y                         →    code-quality
  geepers_security                     →    code-quality
  geepers_deps                         →    code-quality
  geepers_critic                       →    code-quality
  geepers_orchestrator_quality         →    code-quality

Research Agents
  geepers_searcher                     →    mcp-orchestration
  geepers_data                         →    data-fetch
  geepers_fetcher                      →    data-fetch
  geepers_citations                    →    data-fetch
  geepers_links                        →    data-fetch
  geepers_diag                         →    mcp-orchestration
  geepers_orchestrator_research        →    mcp-orchestration

Standalone Agents
  geepers_git                          →    dev-tools
  geepers_docs                         →    dev-tools
  geepers_dashboard                    →    dev-tools
  geepers_api                          →    dev-tools
  geepers_canary                       →    dev-tools
  geepers_janitor                      →    dev-tools
  geepers_scalpel                      →    dev-tools

System Agents
  geepers_system_onboard               →    dev-tools
  geepers_system_diag                  →    dev-tools
  geepers_system_help                  →    dev-tools

Web Agents
  geepers_flask                        →    web-orchestration
  geepers_express                      →    web-orchestration
  geepers_orchestrator_web             →    web-orchestration
```

---

## Part 2: Skill Dependency Graph

### Core Dependency Chain

```
                          mcp-orchestration
                          /      |      \
                         /       |       \
                    datavis    code-quality
                    /   |  \        |
              data-fetch | color-   |
                   |     system     |
              Canvas,  CSV         ruff
              JSON    Loader       pytest
              API


                      server-deploy
                      /    |    \
                  caddy   port-  service
                 config   finder  checker
```

### Detailed Skill Dependency Map

```
Legend:
  A ──→ B    = "A requires/uses B"
  [→]        = "optional dependency"
  {→}        = "dynamic dependency"

PRIORITY SKILLS (Core)
══════════════════════

datavis
  ├─ data-fetch [→]          (optional: fetch from external sources)
  ├─ code-quality [→]        (optional: validate generated viz)
  └─ matplotlib, plotly      (Python libs)

server-deploy
  ├─ code-quality [→]        (optional: pre-deploy checks)
  └─ requests, pyyaml        (Python libs)

code-quality
  ├─ data-fetch [→]          (optional: fetch benchmarks)
  └─ pytest, ruff, bandit    (Python tools)

data-fetch
  └─ [No hard dependencies]  (standalone)
      └─ uses: requests, httpx, pandas

mcp-orchestration
  ├─ data-fetch {→}          (dynamic: based on task)
  ├─ code-quality {→}        (dynamic: based on task)
  └─ datavis {→}             (dynamic: based on task)

SECONDARY SKILLS (Feature-Rich)
═══════════════════════════════

fullstack-dev
  ├─ code-quality            (test generated code)
  ├─ server-deploy [→]       (optional: deploy scaffolded app)
  └─ web-orchestration       (uses Flask/Express templates)

project-planner
  ├─ code-quality [→]        (optional: estimate from code)
  └─ datavis [→]             (optional: create Gantt charts)

web-orchestration
  ├─ code-quality            (validate generated code)
  └─ fullstack-dev [→]       (optional: extended scaffolding)

corpus-analysis
  ├─ data-fetch              (fetch corpus data)
  └─ nltk, spacy             (Python libs)

python-cli
  ├─ code-quality            (validate generated code)
  └─ click, typer            (CLI frameworks)

game-dev
  ├─ code-quality [→]        (optional: test game code)
  └─ godot                   (external tool)

NOVEL SKILLS (New Capabilities)
═══════════════════════════════

llm-comparison
  ├─ anthropic-sdk
  ├─ xai-sdk
  ├─ openai-sdk
  └─ [other LLM clients]

visualization-gallery
  ├─ datavis                 (templates from datavis skill)
  └─ dev-tools              (git operations for gallery)

dev-tools
  └─ [No hard dependencies]  (collection of utilities)
```

---

## Part 3: Data Flow Diagram

### Agent → Skill → Execution → Result

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER REQUEST                             │
│                                                                   │
│  "Create a visualization of GDP growth by country"              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              AGENT LAYER (Decision Making)                       │
│                                                                   │
│  geepers_datavis agent receives request                         │
│  ├─ Analyzes intent: "need data + visualization"               │
│  ├─ Checks available skills: datavis, data-fetch               │
│  └─ Decides execution strategy                                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              SKILL ORCHESTRATION LAYER                           │
│                                                                   │
│  SkillRunner receives: (skill='datavis', command='create_...')  │
│  ├─ Validates skill exists                                      │
│  ├─ Checks permissions                                          │
│  ├─ Loads configuration                                         │
│  └─ Executes skill scripts                                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
    ┌─────────┐         ┌────────┐         ┌─────────┐
    │ data-   │         │ datavis│         │ code-   │
    │ fetch   │         │ skill  │         │ quality │
    │ skill   │         │ script │         │ skill   │
    └────┬────┘         └────┬───┘         └────┬────┘
         │                   │                   │
         ▼                   ▼                   ▼
    1. Fetch GDP     2. Generate D3      3. Validate
       from World      HTML/CSS/JS           viz
       Bank API                              (optional)
                   │
                   ├─ Input:
                   │  data=[...],
                   │  theme='modern'
                   │
                   ├─ Processing:
                   │  - Build D3 config
                   │  - Generate SVG
                   │  - Add interactivity
                   │  - Apply color palette
                   │
                   └─ Output: visualization.html

         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│               RESULT ASSEMBLY LAYER                              │
│                                                                   │
│  Skill returns standardized response:                            │
│  {                                                               │
│      'status': 'success',                                        │
│      'file': 'visualization.html',                              │
│      'data': {...},                                             │
│      'metrics': {'duration': 2.34, 'api_calls': 1},            │
│      'next_steps': ['Open in browser', 'Share']                │
│  }                                                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              AGENT RESPONSE LAYER                                │
│                                                                   │
│  geepers_datavis agent:                                         │
│  ├─ Receives skill result                                       │
│  ├─ Formats for user                                            │
│  └─ Provides next recommendations                               │
│                                                                   │
│  "Created visualization at visualization.html"                  │
│  "Contains GDP growth for 195 countries"                        │
│  "Suggestion: Add interactivity for region filtering"           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       USER RECEIVES                              │
│                       RESULT + GUIDANCE                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Part 4: Skill Composition Example

### Complex Workflow: "Build and Deploy a Full-Stack App"

```
fullstack-dev Agent
    │
    ├─→ fullstack-dev Skill
    │       ├─→ Scaffold React app
    │       ├─→ Scaffold API (Flask/Express)
    │       │       └─→ Uses: web-orchestration Skill
    │       └─→ Validate generated code
    │           └─→ Uses: code-quality Skill
    │
    ├─→ code-quality Skill
    │       ├─ Run pytest
    │       ├─ Run ruff
    │       └─ Run security scan
    │
    └─→ server-deploy Skill (optional)
            ├─ Check available port
            ├─ Add Caddy route
            ├─ Deploy service
            └─ Health check


Example Call Chain:

  Agent asks: "Build full-stack todo app on port 5012"

  Step 1: fullstack-dev.scaffold()
    └─→ Returns: { 'frontend': {...}, 'backend': {...} }

  Step 2: code-quality.run_full_scan()
    └─→ Returns: { 'coverage': 92%, 'lint': 0, 'security': clean }

  Step 3: server-deploy.deploy_service()
    └─→ Returns: { 'port': 5012, 'path': '/todoapp/*', 'status': 'running' }

  Final Response to Agent:
    {
      'status': 'success',
      'app_location': '/home/coolhand/projects/todoapp',
      'deployed_url': 'http://dr.eamer.dev/todoapp/',
      'health_check': 'passing',
      'test_coverage': '92%',
      'next_steps': ['Add database', 'Configure auth']
    }
```

---

## Part 5: Script Execution Graph

### datavis Skill - Internal Script Dependencies

```
request: create_d3_viz({data, theme, type})
    │
    ▼
┌──────────────────────────────────────────┐
│ viz_generator.py (main orchestrator)     │
└──────────────┬───────────────────────────┘
               │
       ┌───────┼───────┬────────────┐
       │       │       │            │
       ▼       ▼       ▼            ▼
    ┌────┐ ┌─────┐ ┌──────┐ ┌─────────┐
    │data│ │color│ │d3    │ │template │
    │load│ │sys  │ │helper│ │builder  │
    └────┘ └─────┘ └──────┘ └─────────┘
       │       │       │            │
       │       │       │    Generate D3 HTML/JS
       │       │       │
       │   ┌───┘       │
       │   │           │
       │   ├─ Color palette
       │   └─ Contrast validation (a11y)
       │
       ├─ Data transformation
       │  └─ Normalize, aggregate
       │
       └─→ Cache result
           └─→ Return file path

response: {status, file, metrics}
```

---

## Part 6: Agent-Skill Interface Specification

```
AGENT INVOKES SKILL:
═══════════════════

Agent Code:
  from geepers.skills import SkillRunner

  skill = SkillRunner()
  result = skill.run(
      skill_name='datavis',           # Skill identifier
      command='create_d3_viz',        # Command/function
      args={                          # Arguments
          'data': [...]
          'theme': 'modern'
      },
      async=False,                    # Sync or async
      timeout=300                     # Seconds
  )


SKILL EXECUTES:
═══════════════

Flow:
  1. SkillRunner locates skill
     └─ ~/.claude/skills/datavis/

  2. Validates request
     ├─ Command exists
     ├─ Arguments valid
     └─ Permissions check

  3. Loads configuration
     ├─ .skillrc settings
     └─ API keys

  4. Imports script module
     └─ datavis.scripts.viz_generator

  5. Executes command
     └─ viz_generator.create_d3_viz(args)

  6. Assembles response
     ├─ Status
     ├─ Result data
     ├─ Metrics
     └─ Errors


RETURNS TO AGENT:
═════════════════

{
  'status': 'success',
  'data': {...},
  'file': '/path/to/output',
  'metrics': {...},
  'errors': [],
  'next_steps': [...]
}

Agent processes result and responds to user.
```

---

## Part 7: Distributed Execution Model

### How MCP-Orchestration Skill Delegates

```
User Request
    │
    ▼
geepers_conductor Agent
    │
    ├─ Recognizes need for multi-agent research
    │
    └─→ mcp-orchestration Skill
        │
        ├─→ launch_cascade({
        │       'task': 'Research ML history',
        │       'num_belters': 5
        │   })
        │
        ├─ Spawns distributed agents:
        │  ├─ Belter1: Search academic papers (arXiv)
        │  ├─ Belter2: Search news/blogs
        │  ├─ Belter3: Search GitHub projects
        │  ├─ Belter4: Search Wikipedia
        │  └─ Belter5: Search video lectures
        │
        ├─ Mid-level synthesis:
        │  └─ Drummer: Aggregate findings by theme
        │
        └─ Executive synthesis:
            └─ Camina: Generate comprehensive report

Results Flow:
  Belter agents → Drummer → Camina → Final Report

Timeline:
  T=0s:   launch_cascade() returns task_id
  T=30s:  get_status(task_id) → {progress: 40%, current: 'belter agents'}
  T=60s:  get_status(task_id) → {progress: 70%, current: 'drummer synthesis'}
  T=90s:  get_status(task_id) → {progress: 100%, current: 'complete'}
  T=95s:  get_results(task_id) → {report: {...}, metrics: {...}}
```

---

## Part 8: Configuration Hierarchy

```
System Config
└─ ~/.claude/skills/.skillrc
   ├─ api_keys (all skills)
   ├─ paths (all skills)
   ├─ performance (all skills)
   └─ logging (all skills)
        │
        ├─→ Skill Config 1
        │   └─ ~/.claude/skills/datavis/.skillrc
        │       ├─ default_theme
        │       ├─ d3_version
        │       └─ max_data_points
        │
        ├─→ Skill Config 2
        │   └─ ~/.claude/skills/server-deploy/.skillrc
        │       ├─ caddy_path
        │       ├─ backup_location
        │       └─ validate_timeout
        │
        └─→ Skill Config 3
            └─ ~/.claude/skills/code-quality/.skillrc
                ├─ min_coverage
                ├─ ruff_rules
                └─ pytest_markers
```

---

## Part 9: Directory Structure Visualization

```
~/.claude/
│
├─ skills/                          ← NEW: Skill system root
│  ├─ .skillrc                      ← Global config
│  ├─ _common/                      ← Shared utilities
│  │  └─ skill_runner.py
│  │
│  ├─ datavis/                      ← Skill 1
│  │  ├─ SKILL.md
│  │  ├─ .skillrc
│  │  ├─ scripts/
│  │  │  ├─ viz_generator.py
│  │  │  ├─ d3_helper.py
│  │  │  ├─ color_system.py
│  │  │  └─ requirements.txt
│  │  ├─ reference/
│  │  │  ├─ examples.md
│  │  │  └─ design-guide.md
│  │  └─ tests/
│  │     └─ test_*.py
│  │
│  ├─ server-deploy/                ← Skill 2
│  │  ├─ SKILL.md
│  │  ├─ scripts/
│  │  │  ├─ deploy.py
│  │  │  ├─ caddy_manager.py
│  │  │  └─ port_finder.py
│  │  ├─ reference/
│  │  └─ tests/
│  │
│  ├─ code-quality/                 ← Skill 3
│  │  └─ [similar structure]
│  │
│  ├─ data-fetch/                   ← Skill 4
│  │  ├─ scripts/
│  │  │  ├─ fetcher.py
│  │  │  ├─ clients/
│  │  │  │  ├─ arxiv.py
│  │  │  │  ├─ census.py
│  │  │  │  ├─ github.py
│  │  │  │  └─ [13 more]
│  │  └─ [rest of structure]
│  │
│  ├─ mcp-orchestration/             ← Skill 5
│  │  ├─ scripts/
│  │  │  ├─ orchestrator.py
│  │  │  ├─ cascade.py
│  │  │  └─ swarm.py
│  │  └─ [rest of structure]
│  │
│  └─ [7+ more secondary skills]
│
├─ agents/                          ← UPDATED: Agent system (pre-existing)
│  ├─ datavis/
│  │  ├─ geepers_datavis.md         ← UPDATED: Now references datavis skill
│  │  ├─ geepers_datavis_color.md
│  │  └─ ...
│  │
│  ├─ deploy/
│  │  ├─ geepers_caddy.md           ← UPDATED: Now references server-deploy
│  │  └─ ...
│  │
│  └─ [remaining agent categories]
│
└─ .claude/
   ├─ CLAUDE.md
   └─ [existing config]

~/geepers/                         ← Output/Reports (pre-existing)
├─ reports/
│  └─ skills/                      ← NEW: Skill execution reports
├─ logs/
│  └─ skills/                      ← NEW: Skill logs
└─ cache/
   └─ skills/                      ← NEW: Skill caching layer
```

---

## Part 10: Interaction Examples

### Example 1: Simple Skill Invocation

```
User → "Create a bar chart of Q4 revenue"
         │
         ▼
geepers_datavis Agent
         │
         ├─ Recognizes: Need data + visualization
         │
         └─→ SkillRunner.run(
                 skill_name='datavis',
                 command='create_d3_viz',
                 args={
                     'data': [[2023, 100], [2024, 150]],
                     'type': 'bar-chart'
                 }
             )
             │
             ▼
datavis Skill Scripts:
    viz_generator.py
        ├─ create_d3_viz()
        ├─ Build config
        ├─ Call color_system.py for palette
        ├─ Call d3_helper.js for template
        └─ Generate HTML/CSS/JS
             │
             ▼
Result: {
    'status': 'success',
    'file': 'chart.html',
    'metrics': {'duration': 0.45}
}
         │
         ▼
Agent Response: "Chart created at chart.html"
         │
         ▼
User receives visualization
```

### Example 2: Composite Skill Invocation

```
User → "Build and deploy a new API service"
         │
         ▼
fullstack-dev Agent
         │
         ├─ Calls fullstack-dev Skill
         │  └─→ Scaffolds Flask API
         │      └─→ Calls web-orchestration Skill for templates
         │
         ├─ Calls code-quality Skill
         │  └─→ Runs tests, linting, security
         │
         └─→ Calls server-deploy Skill
             ├─ Finds available port (5015)
             ├─ Calls caddy_manager to add route
             ├─ Validates config
             ├─ Reloads Caddy
             └─ Health checks service
                  │
                  ▼
Result: Fully deployed app on port 5015 at /api/*
```

### Example 3: Orchestrated Skill Invocation

```
User → "Research the impact of generative AI on employment"
         │
         ▼
geepers_conductor Agent
         │
         └─→ mcp-orchestration Skill
             │
             ├─ Launch Dream Cascade
             │  ├─ Belter1: Search arXiv (via data-fetch skill)
             │  ├─ Belter2: Search news databases
             │  ├─ Belter3: Analyze GitHub trends
             │  ├─ Belter4: Query Wikipedia
             │  └─ Belter5: Fetch labor statistics
             │
             ├─ Drummer synthesis (aggregate findings)
             │
             └─ Camina synthesis (generate report)
                  │
                  ▼
Result: Comprehensive research report with sources
```

---

## Key Takeaways

1. **Clear Separation**: Agents (think) + Skills (execute) = better division of labor
2. **Reusability**: Skills used by multiple agents eliminates duplication
3. **Composition**: Skills can call other skills for complex workflows
4. **Standardization**: All skills follow same SKILL.md + scripts/ pattern
5. **Scalability**: Easy to add new skills without modifying core system

---

**Next Document**: Read `/home/coolhand/SKILLS_ARCHITECTURE.md` for 50-page detailed design

**Last Updated**: 2025-12-18

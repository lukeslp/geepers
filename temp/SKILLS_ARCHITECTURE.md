# Claude Skills Architecture for Geepers

**Author**: Luke Steuber
**Date**: 2025-12-18
**Purpose**: Design a skills-based architecture that maps geepers agent categories to executable Claude Skills with embedded scripts and enhanced capabilities.

---

## Executive Summary

This document defines a strategic migration from the current agent-only system to a hybrid **Agent + Skills** architecture. Skills provide executable Python/Shell scripts alongside agent definitions, enabling:

- Direct LLM access to workflow automation (MCP orchestration scripts)
- Data pipeline scripts (Census, arXiv, GitHub, etc.)
- Infrastructure automation (sm, Caddy, validation)
- Real-time code quality checking and linting
- Interactive visualization generation

### Key Insight

**Agents** = Expert guidance and decision-making (instruction-based)
**Skills** = Agents + executable scripts (action-based)

The skill system elevates agents from advisors to automation orchestrators.

---

## Part 1: Agent → Skill Mapping

### Current Geepers Agent Hierarchy

```
Master
├── conductor_geepers (router)
├── Checkpoint agents (repo, status, scout, snippets)
├── Corpus agents (lingustic analysis)
├── Datavis agents (visualization experts)
├── Deploy agents (infrastructure automation)
├── Frontend agents (design, CSS, motion, perf, UX, TS)
├── Fullstack agents (React, DB, orchestration)
├── Games agents (game dev, Godot)
├── Hive agents (planning, building, refactoring, integration)
├── Python agents (CLI tools)
├── Quality agents (testing, A11y, perf, security, deps, critic)
├── Research agents (search, data, citation)
├── Standalone agents (git, docs, dashboard, API, canary, scalpel, janitor)
├── System agents (onboarding, diagnostics, help)
└── Web agents (Flask, Express, orchestration)
```

### Skills Mapping Strategy

| Agent Category | Skill Name | Primary Scripts | Use Case |
|---|---|---|---|
| `datavis/*` | **datavis** | D3 helpers, Chart.js, color palettes, data pipelines | Create production-grade visualizations |
| `deploy/*` | **server-deploy** | sm (service manager), Caddy config, port checker | Deploy and manage services |
| `quality/*` | **code-quality** | pytest, ruff, pytest-cov, pylint, security scanner | Automated code quality checks |
| `research/*` | **data-fetch** | API clients (17+), web scraper, citation manager | Fetch and process data from external sources |
| `fullstack/*` | **fullstack-dev** | React scaffolder, DB migrator, schema validator | Build full-stack applications |
| `frontend/*` | **frontend-design** | Vite scaffolder, CSS framework, design system | Create distinctive web UIs (already Anthropic skill!) |
| `games/*` | **game-dev** | Godot project scaffolder, asset manager, build tools | Game development workflow |
| `hive/*` | **project-planner** | Task queue generator, dependency analyzer, gantt maker | Strategic project planning |
| `web/*` | **web-orchestration** | Flask scaffolder, Express scaffolder, API templates | Web app scaffolding |
| `corpus/*` | **corpus-analysis** | Linguistics analyzer, corpus query engine | Corpus linguistics analysis |
| `python/*` | **python-cli** | Click/Typer scaffolder, CLI builder, package manager | Python CLI tool development |
| `master/*` | **geepers-conductor** | Agent router script, orchestrator launcher, task dispatcher | Master coordination and routing |
| `standalone/*` | **dev-tools** | git automation, docs generator, API client, cleanup | General development utilities |
| `system/*` | **system-admin** | Diagnostic toolkit, onboarding script, help generator | System administration |

**Novel Skills** (new capabilities):

| Skill | Scripts | Purpose |
|---|---|---|
| **mcp-orchestration** | Dream Cascade launcher, Dream Swarm launcher, pattern loader | Advanced multi-agent orchestration |
| **llm-comparison** | Provider benchmark, cost analyzer, capability matcher | Compare LLM providers (Anthropic, xAI, OpenAI, etc.) |
| **visualization-gallery** | Gallery generator, template builder, theme exporter | Manage visualization library |

---

## Part 2: Core Skills Architecture

### Standard Skill Directory Structure

```
skill-name/
├── SKILL.md                 # Metadata + comprehensive guide
├── LICENSE.txt              # Apache 2.0 or MIT
├── scripts/
│   ├── __init__.py         # Python package (if Python-based)
│   ├── main.py             # Entry point for CLI
│   ├── config.py           # Configuration management
│   ├── command1.py         # Major command/script
│   ├── command2.py         # Major command/script
│   ├── command3.sh         # Shell script (if needed)
│   ├── requirements.txt    # Python dependencies (if applicable)
│   └── README.md           # Script documentation
├── reference/
│   ├── examples.md         # Usage examples
│   ├── best-practices.md   # Guiding principles
│   ├── api-reference.md    # Detailed API docs (for complex skills)
│   └── templates/          # Reusable code templates
├── tests/
│   ├── test_*.py          # Unit tests for scripts
│   └── fixtures/           # Test data
└── .skillrc                 # Skill configuration (optional)
```

### SKILL.md Metadata Format

```yaml
---
name: skill-name
description: |
  One-liner description for LLM context window.

  Multi-line description explaining when and why to use this skill.
  Include concrete examples.
license: MIT or Apache 2.0
min_script_version: "1.0"
depends_on: []  # Other skills required
tags: [category, type, usecase]
---

## Overview
[Purpose and design philosophy]

## When to Use This Skill
[Decision criteria]

## Available Commands
- `command1`: Description
- `command2`: Description

## Architecture
[Internal design]

## Integration
[How skill works with agents]

## Safety & Constraints
[Limitations and safeguards]
```

---

## Part 3: Priority Skills (Detailed Design)

### 1. **datavis** Skill

**Maps to**: `geepers_datavis*` agents
**Purpose**: Production-grade data visualization creation with D3, Chart.js, and custom SVG

```
datavis/
├── SKILL.md
│   - Guide for creating visualizations
│   - When to use D3 vs Chart.js vs custom SVG
│   - Design principles (typography, color, motion)
│   - Performance optimization tips
├── scripts/
│   ├── __init__.py
│   ├── viz_generator.py    # Main entry point
│   ├── d3_helper.py        # D3 template & utilities
│   ├── chartjs_helper.py   # Chart.js builder
│   ├── color_system.py     # Color palette generator
│   ├── data_loader.py      # CSV/JSON/API data loading
│   ├── dataset_fetcher.py  # Fetch from Census, World Bank, etc.
│   ├── svg_custom.py       # Custom SVG generation
│   └── requirements.txt
│       - pandas
│       - matplotlib
│       - plotly
│       - requests
├── reference/
│   ├── examples.md
│   │   - D3 bar chart example
│   │   - Chart.js time series
│   │   - Custom SVG network graph
│   │   - Color palette strategies
│   ├── d3-snippets.js      # Reusable D3 patterns
│   ├── chartjs-templates/  # Complete templates
│   │   ├── line-chart.html
│   │   ├── bar-chart.html
│   │   ├── scatter-plot.html
│   │   └── combo-chart.html
│   ├── design-guide.md
│   │   - Typography rules
│   │   - Color theory
│   │   - Motion principles
│   │   - Accessibility (WCAG 2.1)
│   └── data-sources.md     # Supported APIs
│       - Census API
│       - World Bank
│       - arXiv
│       - Wikipedia
│       - GitHub
│       - etc.
└── tests/
    ├── test_d3_helper.py
    ├── test_chartjs_helper.py
    ├── test_color_system.py
    └── fixtures/
        └── sample_data.csv
```

**Key Scripts**:

```python
# viz_generator.py
class VizGenerator:
    def create_d3_viz(spec: Dict) -> str:
        """Generate D3 visualization HTML/JS"""

    def create_chartjs_viz(spec: Dict) -> str:
        """Generate Chart.js visualization"""

    def create_svg_viz(spec: Dict) -> str:
        """Generate custom SVG"""

# color_system.py
class ColorPalette:
    def generate_palette(theme: str, num_colors: int) -> List[str]:
        """Generate harmonious color palette"""

    def get_wcag_contrast(color1: str, color2: str) -> float:
        """Check WCAG contrast ratio"""

# dataset_fetcher.py
class DatasetFetcher:
    def fetch_census(query: str) -> pd.DataFrame:
        """Fetch from Census API"""

    def fetch_arxiv(search_term: str) -> List[Dict]:
        """Fetch from arXiv"""

    def fetch_github(owner: str, repo: str) -> Dict:
        """Fetch from GitHub API"""
```

**Agent Integration**:

When agent calls skill: "Create a D3 bar chart of GDP by country"
- Skill loads `datavis_generator.py`
- Skill calls `fetch_world_bank('gdp')`
- Skill calls `create_d3_viz(theme='modern')`
- Returns complete HTML/CSS/JS

---

### 2. **server-deploy** Skill

**Maps to**: `geepers_caddy`, `geepers_services`, `geepers_validator` agents
**Purpose**: Service deployment, port management, Caddy configuration

```
server-deploy/
├── SKILL.md
│   - Service deployment workflow
│   - Port allocation strategy
│   - Caddy configuration patterns
│   - Troubleshooting guide
├── scripts/
│   ├── __init__.py
│   ├── deploy.py           # Main deployment orchestrator
│   ├── caddy_manager.py    # Caddy config management
│   ├── service_checker.py  # Service health checks
│   ├── port_finder.py      # Port availability checker
│   ├── caddy_validator.py  # Configuration validation
│   └── requirements.txt
│       - requests
│       - pyyaml
├── reference/
│   ├── examples.md
│   │   - Deploy new Flask service
│   │   - Add Caddy route
│   │   - Check port conflicts
│   │   - Validate configuration
│   ├── caddy-patterns.md
│   │   ```
│   │   # Route pattern (strips prefix)
│   │   handle_path /prefix/* {
│   │       reverse_proxy localhost:PORT
│   │   }
│   │
│   │   # Multi-path pattern
│   │   route /path1/* /path2/* {
│   │       reverse_proxy localhost:PORT
│   │   }
│   │
│   │   # Domain-specific
│   │   domain.com {
│   │       reverse_proxy localhost:PORT
│   │   }
│   │   ```
│   └── troubleshooting.md
└── tests/
    ├── test_caddy_manager.py
    ├── test_port_finder.py
    └── fixtures/
        └── sample_caddyfile
```

**Key Scripts**:

```python
# deploy.py
class DeployManager:
    def deploy_service(service: Dict) -> Dict:
        """
        service = {
            'name': 'myapp',
            'port': 5012,
            'path': '/myapp/*',
            'health_endpoint': '/health'
        }
        """

    def add_caddy_route(path: str, port: int, options: Dict) -> bool:
        """Add route to Caddyfile"""

# caddy_manager.py
class CaddyManager:
    def read_caddyfile(self) -> str:
        """Read current Caddyfile"""

    def validate_config(self) -> Tuple[bool, str]:
        """Run caddy validate"""

    def reload_caddy(self) -> bool:
        """Reload Caddy service"""

    def backup_caddyfile(self) -> str:
        """Create timestamped backup"""

# port_finder.py
class PortFinder:
    def is_port_available(port: int) -> bool:
        """Check if port is listening"""

    def find_available_port(start: int = 5010) -> int:
        """Find next available port"""

    def get_allocated_ports(self) -> Dict[int, str]:
        """Get port registry"""

    def update_port_registry(port: int, service: str) -> bool:
        """Update ~/geepers/status/ports.json"""

# service_checker.py
class ServiceChecker:
    def health_check(url: str) -> Dict:
        """Check service health endpoint"""

    def get_service_status(service: str) -> str:
        """Query sm status"""
```

**Agent Integration**:

When agent calls skill: "Deploy service on port 5012 at /myapp/*"
- Skill loads `deploy.py`
- Skill calls `PortFinder.find_available_port()`
- Skill calls `CaddyManager.add_caddy_route()`
- Skill calls `CaddyManager.validate_config()`
- Skill calls `CaddyManager.reload_caddy()`
- Returns success/failure with detailed report

---

### 3. **code-quality** Skill

**Maps to**: `geepers_testing`, `geepers_perf`, `geepers_a11y`, `geepers_security`, `geepers_deps` agents
**Purpose**: Automated code quality checks with pytest, ruff, coverage, security scanning

```
code-quality/
├── SKILL.md
│   - Test strategy guide
│   - Code quality best practices
│   - Coverage targets
│   - Security scanning approach
├── scripts/
│   ├── __init__.py
│   ├── quality_scanner.py  # Main orchestrator
│   ├── pytest_runner.py    # Test execution & coverage
│   ├── ruff_checker.py     # Linting configuration
│   ├── security_scan.py    # Security checks (bandit)
│   ├── perf_analyzer.py    # Performance profiling
│   ├── a11y_checker.py     # Accessibility validation
│   ├── dep_analyzer.py     # Dependency audit
│   ├── coverage_reporter.py# Coverage analysis
│   └── requirements.txt
│       - pytest
│       - pytest-cov
│       - ruff
│       - bandit
│       - safety
│       - licensecheck
├── reference/
│   ├── examples.md
│   │   - Run full quality suite
│   │   - Check test coverage
│   │   - Security audit
│   │   - Performance profile
│   ├── test-strategy.md
│   │   - Unit test patterns
│   │   - Integration test patterns
│   │   - E2E test patterns
│   │   - Fixture strategies
│   ├── ruff-config.toml    # Ruff configuration template
│   ├── pytest.ini          # Pytest configuration template
│   └── coverage-targets.md
└── tests/
    ├── test_pytest_runner.py
    ├── test_ruff_checker.py
    └── fixtures/
        └── sample_project/
```

**Key Scripts**:

```python
# quality_scanner.py
class QualityScanner:
    def run_full_scan(project_path: str) -> Dict:
        """Run all quality checks"""
        return {
            'tests': {...},
            'coverage': {...},
            'lint': {...},
            'security': {...},
            'perf': {...},
            'a11y': {...},
            'deps': {...},
            'score': 0.0-100.0
        }

# pytest_runner.py
class PytestRunner:
    def run_tests(args: List[str]) -> Dict:
        """Run pytest with coverage"""

    def generate_coverage_report(min_coverage: int = 80) -> Dict:
        """Generate coverage HTML report"""

    def find_untested_code(self) -> List[str]:
        """Identify untested functions/classes"""

# ruff_checker.py
class RuffChecker:
    def check_code(path: str) -> Dict:
        """Run ruff linting"""

    def get_violations(self) -> List[Dict]:
        """Get list of violations"""

# security_scan.py
class SecurityScanner:
    def scan_python(path: str) -> List[Dict]:
        """Run bandit security scan"""

    def audit_dependencies(self) -> List[Dict]:
        """Check for vulnerable deps (safety)"""

    def check_licenses(self) -> List[Dict]:
        """Check dependency licenses"""

# a11y_checker.py
class AccessibilityChecker:
    def check_html_a11y(html: str) -> List[Dict]:
        """Check HTML accessibility"""

    def check_color_contrast(colors: List[str]) -> Dict:
        """Verify WCAG contrast ratios"""
```

**Agent Integration**:

When agent calls skill: "Run quality checks on src/"
- Skill loads `quality_scanner.py`
- Skill orchestrates all checks in parallel
- Skill generates report with pass/fail/improve suggestions
- Returns detailed quality score (0-100)

---

### 4. **data-fetch** Skill

**Maps to**: `geepers_data`, `geepers_fetcher` agents
**Purpose**: Fetch data from 17+ external APIs and services

```
data-fetch/
├── SKILL.md
│   - Supported data sources
│   - Authentication setup
│   - Rate limiting & caching
│   - Output formats
├── scripts/
│   ├── __init__.py
│   ├── fetcher.py          # Main API client factory
│   ├── clients/
│   │   ├── __init__.py
│   │   ├── arxiv.py        # arXiv preprints
│   │   ├── census.py       # US Census Bureau
│   │   ├── github.py       # GitHub API
│   │   ├── wikipedia.py    # Wikipedia
│   │   ├── youtube.py      # YouTube Data API
│   │   ├── nasa.py         # NASA APIs
│   │   ├── world_bank.py   # World Bank
│   │   ├── openweather.py  # Weather API
│   │   ├── coinbase.py     # Cryptocurrency
│   │   ├── twilio.py       # Twilio API
│   │   ├── stripe.py       # Stripe API
│   │   ├── slack.py        # Slack API
│   │   ├── twitter.py      # X/Twitter API
│   │   ├── reddit.py       # Reddit API
│   │   ├── elasticsearch.py# Elasticsearch
│   │   ├── postgres.py     # PostgreSQL (local)
│   │   └── sqlite.py       # SQLite (local)
│   ├── cache.py            # Caching layer
│   ├── rate_limiter.py     # Rate limit handling
│   ├── config.py           # API key management
│   └── requirements.txt
│       - requests
│       - httpx
│       - pandas
│       - sqlalchemy
├── reference/
│   ├── examples.md
│   │   - Fetch arXiv papers
│   │   - Get Census data
│   │   - Query GitHub repos
│   │   - World Bank statistics
│   ├── api-reference.md
│   │   - Complete API docs for each client
│   ├── auth-setup.md
│   │   - How to set up API keys
│   │   - Environment variable names
│   │   - OAuth flows (if applicable)
│   └── rate-limits.md
└── tests/
    ├── test_fetcher.py
    ├── test_*.py (per client)
    └── fixtures/
        └── sample_responses/
```

**Key Scripts**:

```python
# fetcher.py
class DataFetcherFactory:
    def get_client(source: str) -> BaseClient:
        """
        source: 'arxiv' | 'census' | 'github' | etc.
        """

    def list_available_sources(self) -> List[str]:
        """List all supported data sources"""

# clients/arxiv.py
class ArxivClient:
    def search(query: str, max_results: int = 100) -> List[Dict]:
        """Search preprints"""

    def get_by_id(arxiv_id: str) -> Dict:
        """Get specific preprint"""

    def get_recent(category: str, limit: int = 50) -> List[Dict]:
        """Get recent papers"""

# clients/census.py
class CensusClient:
    def get_population(state: str = None) -> Dict:
        """Population data"""

    def get_income_data(state: str) -> Dict:
        """Income distribution"""

    def get_demographic_data(query: str) -> Dict:
        """Various demographic data"""

# clients/github.py
class GitHubClient:
    def search_repos(query: str) -> List[Dict]:
        """Search repositories"""

    def get_repo_stats(owner: str, repo: str) -> Dict:
        """Stars, forks, issues, etc."""

    def list_releases(owner: str, repo: str) -> List[Dict]:
        """Get release history"""

# cache.py
class DataCache:
    def get(key: str) -> Optional[Dict]:
        """Get cached data (Redis/SQLite)"""

    def set(key: str, value: Dict, ttl: int = 3600):
        """Cache with TTL"""

    def clear(key_pattern: str = '*'):
        """Clear cache entries"""

# rate_limiter.py
class RateLimiter:
    def check_limit(source: str) -> bool:
        """Check if within rate limit"""

    def wait_if_needed(source: str):
        """Backoff if needed"""
```

**Agent Integration**:

When agent calls skill: "Find latest papers on machine learning"
- Skill loads `fetcher.py`
- Skill calls `ArxivClient.search('machine learning')`
- Skill applies caching for future queries
- Returns formatted results (JSON, CSV, or markdown table)

---

### 5. **mcp-orchestration** Skill (NEW)

**Novel Capability**: Direct access to Dream Cascade and Dream Swarm orchestration from Claude Code
**Purpose**: Multi-agent workflow orchestration and research automation

```
mcp-orchestration/
├── SKILL.md
│   - Dream Cascade pattern (hierarchical)
│   - Dream Swarm pattern (parallel)
│   - When to use each pattern
│   - Monitoring & status checks
├── scripts/
│   ├── __init__.py
│   ├── orchestrator.py     # Main entry point
│   ├── cascade.py          # Dream Cascade implementation
│   ├── swarm.py            # Dream Swarm implementation
│   ├── monitor.py          # Job monitoring
│   ├── patterns.py         # Pattern loader/validator
│   ├── config.py           # Orchestration config
│   └── requirements.txt
│       - httpx
│       - pydantic
│       - pyyaml
├── reference/
│   ├── examples.md
│   │   - Research task with Cascade
│   │   - Parallel search with Swarm
│   │   - Monitor long-running job
│   │   - Cancel running task
│   ├── pattern-specs.md
│   │   - Cascade pattern structure
│   │   - Swarm pattern structure
│   │   - Custom patterns
│   └── job-monitoring.md
│       - Check job status
│       - Stream results
│       - Handle failures
└── tests/
    ├── test_orchestrator.py
    └── fixtures/
        └── sample_tasks.yaml
```

**Key Scripts**:

```python
# orchestrator.py
class MCPOrchestrator:
    def launch_cascade(task: str, config: Dict) -> str:
        """
        Launch Dream Cascade (hierarchical research)
        Returns: task_id for monitoring
        """

    def launch_swarm(query: str, num_agents: int = 5) -> str:
        """
        Launch Dream Swarm (parallel search)
        Returns: task_id for monitoring
        """

    def get_status(task_id: str) -> Dict:
        """Monitor running orchestration"""

    def cancel_task(task_id: str) -> bool:
        """Cancel long-running task"""

    def get_results(task_id: str) -> Dict:
        """Retrieve final results"""

# cascade.py
class DreamCascade:
    def run(task: str, params: Dict) -> Dict:
        """
        Hierarchical pattern:
        - Belter agents (parallel explorers)
        - Drummer agents (mid-level synthesis)
        - Camina executive (final synthesis)
        """

# swarm.py
class DreamSwarm:
    def run(query: str, num_agents: int = 5) -> Dict:
        """
        Parallel pattern:
        - Specialized agent types
        - Concurrent execution
        - Result aggregation
        """

# monitor.py
class OrchestrationMonitor:
    def stream_status(task_id: str, callback):
        """Stream real-time status updates"""

    def get_metrics(task_id: str) -> Dict:
        """Cost, tokens, duration"""

    def estimate_completion(task_id: str) -> datetime:
        """ETA calculation"""
```

**Agent Integration**:

When agent calls skill: "Research the history of machine learning using Cascade pattern"
- Skill loads `orchestrator.py`
- Skill launches Cascade with Belter/Drummer/Camina agents
- Skill monitors progress and streams updates
- Skill aggregates final report
- Returns comprehensive research document

---

## Part 4: Secondary Skills

### **fullstack-dev** Skill

```
fullstack-dev/
├── SKILL.md
├── scripts/
│   ├── scaffolder.py       # Project generator
│   ├── react_builder.py    # React app setup
│   ├── db_migrator.py      # Database migrations
│   ├── schema_validator.py # Schema validation
│   ├── api_generator.py    # API scaffolding
│   └── requirements.txt
├── reference/
│   ├── examples.md
│   ├── project-structure.md
│   ├── templates/
│   │   ├── react-app/
│   │   ├── flask-api/
│   │   ├── fastapi-api/
│   │   └── database/
│   └── best-practices.md
└── tests/
    └── test_scaffolder.py
```

### **project-planner** Skill

```
project-planner/
├── SKILL.md
│   - Strategic planning methodology
│   - Task decomposition
│   - Dependency analysis
│   - Gantt/burndown charts
├── scripts/
│   ├── planner.py          # Main orchestrator
│   ├── task_queue.py       # Queue generation
│   ├── dependency_graph.py # Dependency analysis
│   ├── gantt_generator.py  # Chart generation
│   ├── estimator.py        # Effort estimation
│   └── requirements.txt
├── reference/
│   ├── examples.md
│   ├── methodology.md
│   ├── templates/
│   │   ├── project-plan.md
│   │   ├── task-queue.md
│   │   └── dependency-matrix.md
│   └── prioritization.md
└── tests/
    └── test_planner.py
```

### **llm-comparison** Skill (NEW)

```
llm-comparison/
├── SKILL.md
│   - Supported models (Anthropic, xAI, OpenAI, etc.)
│   - Benchmarking methodology
│   - Cost analysis
│   - Capability matrix
├── scripts/
│   ├── benchmark.py        # Benchmark runner
│   ├── cost_analyzer.py    # Token/pricing calculation
│   ├── capability_matrix.py# Feature comparison
│   ├── clients/
│   │   ├── anthropic.py
│   │   ├── xai.py
│   │   ├── openai.py
│   │   ├── mistral.py
│   │   ├── cohere.py
│   │   ├── groq.py
│   │   └── huggingface.py
│   └── requirements.txt
├── reference/
│   ├── examples.md
│   └── models.md
└── tests/
    └── test_benchmark.py
```

### **web-orchestration** Skill

```
web-orchestration/
├── SKILL.md
├── scripts/
│   ├── scaffolder.py       # Flask/Express scaffolder
│   ├── flask_helper.py     # Flask patterns
│   ├── express_helper.py   # Express patterns
│   ├── middleware.py       # Common middleware
│   └── requirements.txt
├── reference/
│   ├── examples.md
│   ├── templates/
│   │   ├── flask-app/
│   │   └── express-app/
│   └── patterns.md
└── tests/
    └── test_scaffolder.py
```

### **corpus-analysis** Skill

```
corpus-analysis/
├── SKILL.md
│   - Corpus linguistics principles
│   - Query engine
│   - Statistics & analysis
├── scripts/
│   ├── analyzer.py
│   ├── query_engine.py
│   ├── statistics.py
│   ├── collocations.py
│   └── requirements.txt
│       - nltk
│       - spacy
│       - pandas
├── reference/
│   ├── examples.md
│   └── linguistics.md
└── tests/
    └── test_analyzer.py
```

---

## Part 5: Implementation Roadmap

### Phase 1: Infrastructure (Week 1)

**Goal**: Set up skills directory structure and tooling

```bash
# Directory structure
mkdir -p ~/.claude/skills/{datavis,server-deploy,code-quality,data-fetch}
mkdir -p ~/.claude/skills/*/scripts
mkdir -p ~/.claude/skills/*/reference
mkdir -p ~/.claude/skills/*/tests

# Tooling
- Install skill-creator CLI (from /tmp/skills/skills/skill-creator)
- Create skill template generator
- Set up skill validation script
```

**Deliverables**:
- Standard directory structure for all skills
- Skill template generator
- Validation & testing framework

### Phase 2: Core Skills (Weeks 2-3)

**Goal**: Implement 5 priority skills

1. **datavis** skill
   - D3 helpers
   - Chart.js templates
   - Color system
   - Data loaders
   - Visualization agents integration

2. **server-deploy** skill
   - Caddy manager
   - Port finder
   - Service checker
   - Deploy orchestrator

3. **code-quality** skill
   - pytest runner
   - Ruff checker
   - Security scanner
   - Coverage reporter

4. **data-fetch** skill
   - API client factory
   - 17+ data clients
   - Caching layer
   - Rate limiter

5. **mcp-orchestration** skill
   - Cascade launcher
   - Swarm launcher
   - Job monitor
   - Pattern loader

**Deliverables**:
- 5 complete skills with scripts & tests
- Documentation for each skill
- Integration tests with agents

### Phase 3: Secondary Skills (Week 4)

**Goal**: Implement remaining skills

- fullstack-dev
- project-planner
- llm-comparison (NEW)
- web-orchestration
- corpus-analysis
- python-cli
- game-dev

**Deliverables**:
- 7 additional skills
- Comprehensive documentation

### Phase 4: Integration & Migration (Week 5)

**Goal**: Integrate skills with agent system

1. Update agent definitions to reference skills
2. Create skill-to-agent routing logic
3. Implement agent ↔ skill communication
4. Test full workflows (agent + skill + scripts)

**Example**:
```yaml
# geepers_datavis.md (agent)
---
name: geepers_datavis
skills:
  - datavis  # This agent uses the datavis skill
---
```

**Deliverables**:
- Agent-skill mapping finalized
- Integration tests passing
- Documentation updated

### Phase 5: Advanced Features (Week 6+)

**Goal**: Add advanced capabilities

- Skill composition (skill A calls skill B)
- Dynamic skill loading
- Skill marketplace (share/discover skills)
- Performance metrics & monitoring

---

## Part 6: Agent-Skill Communication Protocol

### How Agents Call Skills

```python
# In agent definition (YAML metadata)
---
name: geepers_datavis
description: Create data visualizations
skills:
  - datavis          # Uses this skill
---

# Agent logic calls skill
from geepers.skills import SkillRunner

skill_runner = SkillRunner()
result = skill_runner.run(
    skill_name='datavis',
    command='create_d3_viz',
    args={
        'data': [...],
        'theme': 'modern',
        'type': 'bar-chart'
    }
)
```

### Skill Response Format

```python
{
    'status': 'success|error|partial',
    'data': {...},           # Result data
    'logs': [...],           # Execution logs
    'metrics': {
        'duration': 1.23,    # Seconds
        'calls': 3,          # API calls made
        'tokens': 4500       # LLM tokens (if applicable)
    },
    'errors': [...],         # Any errors encountered
    'next_steps': [...]      # Suggested next actions
}
```

---

## Part 7: Skill Configuration

### Global Skill Config

Create `~/.claude/skills/.skillrc`:

```yaml
# Skill System Configuration

# API Keys (from /home/coolhand/documentation/API_KEYS.md)
api_keys:
  anthropic: "${ANTHROPIC_API_KEY}"
  xai: "${XAI_API_KEY}"
  openai: "${OPENAI_API_KEY}"
  census: "${CENSUS_API_KEY}"
  github: "${GITHUB_TOKEN}"

# Directories
paths:
  scripts: "~/.claude/skills/*/scripts"
  cache: "~/.cache/geepers/skills"
  logs: "~/geepers/logs/skills"
  reports: "~/geepers/reports/skills"

# Performance
performance:
  parallel_clients: 4
  timeout_seconds: 300
  retry_attempts: 3

# Caching
caching:
  enabled: true
  ttl_seconds: 3600
  storage: "sqlite"  # or "redis"

# Logging
logging:
  level: "INFO"
  format: "json"
  output: "file|stdout|both"
```

### Per-Skill Config

Each skill can have `.skillrc` in its directory:

```yaml
# datavis/.skillrc
datavis:
  default_theme: "modern"
  supported_formats: [html, svg, png]
  d3_version: "v7"
  performance:
    max_data_points: 10000
    animation_duration: 800
```

---

## Part 8: Testing & Validation

### Skill Testing Framework

```python
# tests/conftest.py
import pytest
from geepers.skills import SkillRunner

@pytest.fixture
def skill_runner():
    return SkillRunner()

@pytest.fixture
def sample_data():
    return {...}

# tests/test_datavis.py
def test_d3_viz_generation(skill_runner, sample_data):
    result = skill_runner.run(
        skill_name='datavis',
        command='create_d3_viz',
        args={'data': sample_data}
    )
    assert result['status'] == 'success'
    assert 'd3.v7' in result['data']['html']

def test_chartjs_generation(skill_runner):
    result = skill_runner.run(
        skill_name='datavis',
        command='create_chartjs_viz',
        args={...}
    )
    assert result['status'] == 'success'
```

### Skill Validation Checklist

Before publishing a skill:

```bash
# Run linting
ruff check scripts/

# Run tests with coverage
pytest tests/ --cov=scripts --cov-report=html

# Check documentation
- SKILL.md present and complete
- README.md in scripts/ directory
- examples.md with runnable examples
- API reference complete

# Validate scripts
python -m py_compile scripts/**/*.py

# Check dependencies
pip-audit requirements.txt

# Test skill metadata
python -m geepers.skills validate skill-name/
```

---

## Part 9: Security & Access Control

### Skill Permissions

Some skills need elevated permissions (Caddy, service management):

```yaml
# server-deploy/.skillrc
permissions:
  - requires_sudo: true
  - dangerous_operations: ["reload_caddy", "restart_service"]
  - requires_confirmation: true
  - logging: "all_operations"
  - audit: true
```

### API Key Management

```python
# scripts/config.py
from geepers.security import SecureConfig

config = SecureConfig()

# Load from environment
api_key = config.get('github_token')  # Reads from encrypted ~/.claude/secrets

# Or explicit declaration
config.register_key('census_api_key', required=True)
```

---

## Part 10: Deployment & Distribution

### Publishing Skills

```bash
# Package skill
python ~/.claude/skills/scripts/package_skill.py datavis/

# Validates, creates tarball, generates manifest

# Publish to skill registry (hypothetical)
skills-cli publish datavis-skill-v1.0.0.tar.gz

# Share via GitHub gist
# Share via documentation
```

### Version Management

```yaml
# datavis/SKILL.md
---
name: datavis
version: 1.0.0
min_claude_version: "4.5"
dependencies:
  - pandas >= 1.3.0
  - matplotlib >= 3.4.0
---
```

---

## Part 11: Migration Path

### Converting Agents to Agent+Skill Hybrid

**Before** (agent only):
```yaml
---
name: geepers_caddy
description: Caddy configuration manager
---
[500 lines of operational instructions]
```

**After** (agent + skill):
```yaml
---
name: geepers_caddy
description: Caddy configuration manager
skills:
  - server-deploy
---
[Condensed instructions, references to skill scripts]
```

**Benefit**: Agent focuses on decision-making, skill provides execution.

### Backward Compatibility

- Existing agents continue working
- New agents adopt skill pattern
- Gradual migration (no forced refactoring)
- Agents can coexist with or without skills

---

## Part 12: Success Metrics

### Skill System Adoption

| Metric | Target | Current |
|--------|--------|---------|
| Skill coverage (% agents using skills) | 80% | 0% |
| Lines of agent code (reduced) | -40% | 0% |
| Script reusability | 90% | N/A |
| Test coverage (skill scripts) | 85% | N/A |
| Documentation completeness | 100% | N/A |

### Performance Impact

- Agent execution time: -20% (delegation to scripts)
- LLM token usage: -30% (less instruction text)
- Code maintainability: +60% (centralized scripts)
- Developer velocity: +50% (reusable patterns)

---

## Part 13: FAQ & Design Decisions

### Q: Why Skills + Agents instead of just Skills?

**A**: Agents excel at reasoning and decision-making. Skills excel at execution. Together:
- Agents make intelligent routing decisions
- Skills reliably execute repetitive work
- Agents reduce hallucination (delegating to verified scripts)
- Skills improve performance (fast execution)

### Q: Can skills call other skills?

**A**: Yes. Advanced example:
```python
# project-planner skill calls code-quality skill
def run_task_with_quality_checks(task):
    # Build task
    result = build_task(task)

    # Check quality
    quality = SkillRunner().run('code-quality', 'scan', {...})

    # Report
    return {result, quality}
```

### Q: How do skills handle failures?

**A**: Graceful degradation:
```python
try:
    result = api_client.fetch_data()
except RateLimitError:
    return cached_data()  # Fallback
except AuthError:
    return {'status': 'error', 'reason': 'auth_failed'}
```

### Q: What about skill versioning?

**A**: Semantic versioning:
- `1.0.0`: Breaking changes
- `1.1.0`: New features (backward compatible)
- `1.0.1`: Bug fixes

Agents declare minimum skill version:
```yaml
skills:
  - datavis >= 1.0.0
```

---

## Appendix A: File Structure Summary

```
~/.claude/
├── skills/
│   ├── datavis/
│   │   ├── SKILL.md
│   │   ├── LICENSE.txt
│   │   ├── scripts/
│   │   │   ├── __init__.py
│   │   │   ├── viz_generator.py
│   │   │   ├── d3_helper.py
│   │   │   ├── color_system.py
│   │   │   ├── data_loader.py
│   │   │   └── requirements.txt
│   │   ├── reference/
│   │   │   ├── examples.md
│   │   │   ├── d3-snippets.js
│   │   │   └── design-guide.md
│   │   └── tests/
│   │       └── test_*.py
│   ├── server-deploy/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   │   ├── deploy.py
│   │   │   ├── caddy_manager.py
│   │   │   ├── port_finder.py
│   │   │   └── requirements.txt
│   │   ├── reference/
│   │   └── tests/
│   ├── code-quality/
│   ├── data-fetch/
│   ├── mcp-orchestration/
│   └── [12 more skills...]
│
└── agents/
    ├── datavis/
    │   ├── geepers_datavis.md (now references datavis skill)
    │   ├── geepers_datavis_color.md
    │   ├── geepers_datavis_data.md
    │   └── ...
    ├── deploy/
    │   ├── geepers_caddy.md (now references server-deploy skill)
    │   ├── geepers_services.md
    │   └── ...
    └── [remaining agent categories...]
```

---

## Appendix B: Integration Example

### User Request

"Create a data visualization dashboard comparing GDP by country"

### Execution Flow

```
1. User asks geepers_datavis agent
   "Create dashboard of GDP by country"

2. Agent analyzes request:
   - Recognize need for data + visualization
   - Decide to use datavis skill

3. Agent calls datavis skill:
   skill_runner.run('datavis', 'create_dashboard', {
       'data_source': 'world_bank',
       'metric': 'gdp',
       'query': 'all countries'
   })

4. datavis skill executes:
   - Calls data-fetch skill: fetch_world_bank('gdp')
   - Gets data: [{country: 'USA', gdp: ...}, ...]
   - Calls create_d3_viz({data, theme: 'modern'})
   - Generates HTML/CSS/JS
   - Returns result

5. Agent receives result:
   {
       'status': 'success',
       'file': 'dashboard.html',
       'metrics': {...}
   }

6. Agent reports to user:
   "Created dashboard at dashboard.html"
```

---

## Conclusion

This skills architecture transforms geepers from an instruction-based agent system into an execution-capable automation platform. Skills provide:

✅ Reusable, testable code (reduce duplication)
✅ Faster execution (scripts vs. LLM thinking)
✅ Better reliability (verified implementations)
✅ Scalability (skills can evolve independently)
✅ Knowledge transfer (agents + skills = best of both)

**Next step**: Implement Phase 1 infrastructure and begin building core skills.

---

**Document Version**: 1.0
**Last Updated**: 2025-12-18
**Next Review**: 2026-01-15

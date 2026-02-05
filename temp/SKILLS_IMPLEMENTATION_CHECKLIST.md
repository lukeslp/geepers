# Claude Skills Architecture - Implementation Checklist

**Generated**: 2025-12-18
**Author**: Luke Steuber
**Purpose**: Step-by-step implementation guide for building the skills system

---

## Overview

This checklist breaks down the skills architecture into actionable, verifiable steps. Use this to track progress through all 6 phases of implementation.

---

## Phase 1: Infrastructure Setup (Week 1)

### 1.1 Directory Structure

- [ ] Create core directory structure
  ```bash
  mkdir -p ~/.claude/skills/{datavis,server-deploy,code-quality,data-fetch,mcp-orchestration}
  mkdir -p ~/.claude/skills/*/scripts
  mkdir -p ~/.claude/skills/*/reference
  mkdir -p ~/.claude/skills/*/tests
  ```

- [ ] Create shared utilities directory
  ```bash
  mkdir -p ~/.claude/skills/_common
  touch ~/.claude/skills/_common/__init__.py
  ```

- [ ] Create output directories
  ```bash
  mkdir -p ~/geepers/reports/skills
  mkdir -p ~/geepers/logs/skills
  mkdir -p ~/.cache/geepers/skills
  ```

### 1.2 Skill Configuration

- [ ] Create global skill configuration
  ```bash
  # Copy from SKILLS_ARCHITECTURE.md Part 7
  touch ~/.claude/skills/.skillrc
  # Add configuration for:
  # - api_keys
  # - paths
  # - performance
  # - caching
  # - logging
  ```

- [ ] Verify environment variables
  - [ ] `ANTHROPIC_API_KEY` is set
  - [ ] `CENSUS_API_KEY` is set (for data-fetch)
  - [ ] `GITHUB_TOKEN` is set
  - [ ] `XAI_API_KEY` is set (for llm-comparison)
  - [ ] `OPENAI_API_KEY` is set (for llm-comparison)

### 1.3 Skill Runner Framework

- [ ] Create SkillRunner class
  ```python
  # ~/.claude/skills/_common/skill_runner.py
  class SkillRunner:
      def run(self, skill_name, command, args, async=False, timeout=300):
          """Execute skill command with validation"""
          # 1. Locate skill
          # 2. Validate request
          # 3. Load config
          # 4. Import script
          # 5. Execute command
          # 6. Assemble response
          # 7. Return result
  ```

- [ ] Create skill registry
  ```python
  # ~/.claude/skills/_common/registry.py
  SKILLS = {
      'datavis': {...},
      'server-deploy': {...},
      # ... etc
  }
  ```

- [ ] Create response formatter
  ```python
  # ~/.claude/skills/_common/response.py
  class SkillResponse:
      """Standardized response format"""
      status: str  # success|error|partial
      data: dict
      file: str
      logs: list
      metrics: dict
      errors: list
      next_steps: list
  ```

### 1.4 Validation Framework

- [ ] Create SKILL.md validator
  ```bash
  # Script to validate SKILL.md structure
  python ~/.claude/skills/_common/validate_skill.py <skill-name>
  ```

- [ ] Create requirements.txt validator
  ```bash
  # Check for security issues
  pip-audit ~/.claude/skills/<skill>/scripts/requirements.txt
  ```

- [ ] Create script validator
  ```bash
  # Syntax check all Python scripts
  python -m py_compile ~/.claude/skills/<skill>/scripts/**/*.py
  ```

### 1.5 Testing Infrastructure

- [ ] Create test runner
  ```bash
  # Run all tests with coverage
  pytest ~/.claude/skills/*/tests/ -v --cov=scripts
  ```

- [ ] Create fixtures directory structure
  ```bash
  mkdir -p ~/.claude/skills/*/tests/fixtures
  ```

- [ ] Create conftest.py template
  ```python
  # Each skill gets tests/conftest.py with:
  # - SkillRunner fixture
  # - API client mocks
  # - Sample data fixtures
  ```

### 1.6 Documentation Template

- [ ] Create SKILL.md template
  ```markdown
  # Location: ~/.claude/skills/skill-template/SKILL.md
  [Copy from SKILLS_ARCHITECTURE.md Part 2]
  ```

- [ ] Create LICENSE.txt template
  ```text
  Location: ~/.claude/skills/skill-template/LICENSE.txt
  [MIT or Apache 2.0]
  ```

- [ ] Create README.md template for scripts
  ```markdown
  Location: ~/.claude/skills/skill-template/scripts/README.md
  [Script documentation]
  ```

---

## Phase 2: Core Skills Implementation (Weeks 2-3)

### 2.1 datavis Skill

#### Scripts

- [ ] `scripts/viz_generator.py`
  - [ ] `create_d3_viz(data, theme, type)` → HTML/JS
  - [ ] `create_chartjs_viz(spec)` → HTML with Chart.js
  - [ ] `create_svg_viz(spec)` → Custom SVG
  - [ ] Tests: 5+ test cases

- [ ] `scripts/d3_helper.py`
  - [ ] D3 v7 template generation
  - [ ] SVG/HTML output
  - [ ] Interaction setup
  - [ ] Tests: Unit tests for each template

- [ ] `scripts/color_system.py`
  - [ ] `generate_palette(theme, num_colors)` → List[str]
  - [ ] `get_wcag_contrast(color1, color2)` → float
  - [ ] WCAG AA/AAA compliance checking
  - [ ] Tests: Color math verification

- [ ] `scripts/data_loader.py`
  - [ ] `load_csv(path)` → DataFrame
  - [ ] `load_json(path)` → Dict/List
  - [ ] `load_api(url, params)` → DataFrame
  - [ ] Tests: Mock API calls

- [ ] `scripts/dataset_fetcher.py`
  - [ ] `fetch_world_bank(indicator)` → DataFrame
  - [ ] `fetch_census(query)` → DataFrame
  - [ ] `fetch_gapminder(metric)` → DataFrame
  - [ ] Integration tests with real APIs

- [ ] `scripts/requirements.txt`
  - [ ] pandas >= 1.3.0
  - [ ] requests >= 2.28.0
  - [ ] matplotlib >= 3.4.0

#### Documentation

- [ ] `SKILL.md` (complete with examples)
- [ ] `reference/examples.md` (5+ examples)
- [ ] `reference/d3-snippets.js` (reusable patterns)
- [ ] `reference/design-guide.md` (typography, color, motion)
- [ ] `scripts/README.md` (API reference)

#### Tests

- [ ] `tests/test_viz_generator.py` (8+ tests)
- [ ] `tests/test_d3_helper.py` (5+ tests)
- [ ] `tests/test_color_system.py` (5+ tests)
- [ ] `tests/test_data_loader.py` (5+ tests)
- [ ] Coverage: ≥ 80%

#### Quality Checks

- [ ] `ruff check ~/.claude/skills/datavis/scripts/`
- [ ] `pytest tests/ --cov=scripts --cov-report=html`
- [ ] Validate SKILL.md structure
- [ ] Check all examples run without errors

---

### 2.2 server-deploy Skill

#### Scripts

- [ ] `scripts/deploy.py`
  - [ ] `deploy_service(config)` → Dict
  - [ ] Service validation
  - [ ] Pre-deployment checks
  - [ ] Tests: Mock Caddy operations

- [ ] `scripts/caddy_manager.py`
  - [ ] `read_caddyfile()` → str
  - [ ] `validate_config()` → Tuple[bool, str]
  - [ ] `reload_caddy()` → bool
  - [ ] `backup_caddyfile()` → str
  - [ ] `add_route(path, port, options)` → bool
  - [ ] Tests: Mock sudo operations

- [ ] `scripts/port_finder.py`
  - [ ] `is_port_available(port)` → bool
  - [ ] `find_available_port(start)` → int
  - [ ] `get_allocated_ports()` → Dict
  - [ ] `update_port_registry()` → bool
  - [ ] Tests: Mock lsof/ss commands

- [ ] `scripts/service_checker.py`
  - [ ] `health_check(url)` → Dict
  - [ ] `get_service_status(service)` → str
  - [ ] `get_service_logs(service, lines)` → str
  - [ ] Tests: Mock HTTP calls

- [ ] `scripts/requirements.txt`
  - [ ] requests >= 2.28.0
  - [ ] pyyaml >= 6.0

#### Documentation

- [ ] `SKILL.md` (with Caddy patterns)
- [ ] `reference/caddy-patterns.md` (copy from geepers_caddy agent)
- [ ] `reference/troubleshooting.md`
- [ ] `scripts/README.md`

#### Tests

- [ ] `tests/test_caddy_manager.py` (8+ tests)
- [ ] `tests/test_port_finder.py` (6+ tests)
- [ ] `tests/test_service_checker.py` (4+ tests)
- [ ] Coverage: ≥ 80%

#### Quality Checks

- [ ] `ruff check`
- [ ] `pytest`
- [ ] Verify Caddy validation patterns work

---

### 2.3 code-quality Skill

#### Scripts

- [ ] `scripts/quality_scanner.py`
  - [ ] `run_full_scan(path)` → Dict with all results
  - [ ] Parallel execution of checks
  - [ ] Score calculation (0-100)
  - [ ] Tests: Mock all sub-tools

- [ ] `scripts/pytest_runner.py`
  - [ ] `run_tests(args)` → Dict
  - [ ] `generate_coverage_report(min_coverage)` → Dict
  - [ ] `find_untested_code()` → List[str]
  - [ ] Tests: Mock pytest output

- [ ] `scripts/ruff_checker.py`
  - [ ] `check_code(path)` → Dict
  - [ ] `get_violations()` → List[Dict]
  - [ ] Configuration loading
  - [ ] Tests: Test against sample files

- [ ] `scripts/security_scan.py`
  - [ ] `scan_python(path)` → List[Dict]
  - [ ] `audit_dependencies()` → List[Dict]
  - [ ] `check_licenses()` → List[Dict]
  - [ ] Tests: Mock security tools

- [ ] `scripts/perf_analyzer.py`
  - [ ] `profile_code(script)` → Dict
  - [ ] `get_hotspots()` → List
  - [ ] Tests: Mock cProfile

- [ ] `scripts/a11y_checker.py`
  - [ ] `check_html_a11y(html)` → List[Dict]
  - [ ] `check_color_contrast(colors)` → Dict
  - [ ] Tests: Test with sample HTML

- [ ] `scripts/requirements.txt`
  - [ ] pytest >= 7.0
  - [ ] pytest-cov >= 4.0
  - [ ] ruff >= 0.1.0
  - [ ] bandit >= 1.7.0
  - [ ] safety >= 2.0.0

#### Documentation

- [ ] `SKILL.md`
- [ ] `reference/examples.md`
- [ ] `reference/test-strategy.md`
- [ ] `reference/ruff-config.toml`
- [ ] `scripts/README.md`

#### Tests

- [ ] `tests/test_quality_scanner.py` (6+ tests)
- [ ] `tests/test_pytest_runner.py` (4+ tests)
- [ ] `tests/test_ruff_checker.py` (4+ tests)
- [ ] Coverage: ≥ 85%

#### Quality Checks

- [ ] `ruff check`
- [ ] `pytest`
- [ ] All code quality rules pass

---

### 2.4 data-fetch Skill

#### Scripts

- [ ] `scripts/fetcher.py`
  - [ ] `DataFetcherFactory.get_client(source)` → BaseClient
  - [ ] `list_available_sources()` → List[str]
  - [ ] Client routing and initialization
  - [ ] Tests: Mock all client types

- [ ] `scripts/clients/arxiv.py`
  - [ ] `search(query, max_results)` → List[Dict]
  - [ ] `get_by_id(arxiv_id)` → Dict
  - [ ] `get_recent(category, limit)` → List[Dict]
  - [ ] Tests: Mock arXiv API

- [ ] `scripts/clients/census.py`
  - [ ] `get_population(state)` → Dict
  - [ ] `get_income_data(state)` → Dict
  - [ ] `get_demographic_data(query)` → Dict
  - [ ] Tests: Mock Census API

- [ ] `scripts/clients/github.py`
  - [ ] `search_repos(query)` → List[Dict]
  - [ ] `get_repo_stats(owner, repo)` → Dict
  - [ ] `list_releases(owner, repo)` → List[Dict]
  - [ ] Tests: Mock GitHub API

- [ ] `scripts/clients/wikipedia.py`
  - [ ] `search(query)` → List[Dict]
  - [ ] `get_article(title)` → Dict
  - [ ] Tests: Mock Wikipedia API

- [ ] `scripts/clients/world_bank.py`, `clients/nasa.py`, etc.
  - [ ] Implement remaining 12 clients
  - [ ] Follow same pattern as above

- [ ] `scripts/cache.py`
  - [ ] `get(key)` → Optional[Dict]
  - [ ] `set(key, value, ttl)` → bool
  - [ ] `clear(pattern)` → int (num cleared)
  - [ ] SQLite or Redis backend
  - [ ] Tests: Cache behavior verification

- [ ] `scripts/rate_limiter.py`
  - [ ] `check_limit(source)` → bool
  - [ ] `wait_if_needed(source)` → None
  - [ ] Rate limit tracking per source
  - [ ] Tests: Mock time progression

- [ ] `scripts/requirements.txt`
  - [ ] requests >= 2.28.0
  - [ ] httpx >= 0.24.0
  - [ ] pandas >= 1.3.0

#### Documentation

- [ ] `SKILL.md` (all 17+ sources)
- [ ] `reference/examples.md` (5+ examples)
- [ ] `reference/api-reference.md` (complete API docs)
- [ ] `reference/auth-setup.md` (API key setup)
- [ ] `reference/rate-limits.md`

#### Tests

- [ ] `tests/test_fetcher.py` (4+ tests)
- [ ] `tests/test_arxiv.py` (4+ tests)
- [ ] `tests/test_census.py` (4+ tests)
- [ ] `tests/test_github.py` (4+ tests)
- [ ] `tests/test_cache.py` (6+ tests)
- [ ] `tests/test_rate_limiter.py` (4+ tests)
- [ ] Coverage: ≥ 80%

#### Quality Checks

- [ ] All clients working with mocked APIs
- [ ] Rate limiter functional
- [ ] Cache working correctly

---

### 2.5 mcp-orchestration Skill

#### Scripts

- [ ] `scripts/orchestrator.py`
  - [ ] `launch_cascade(task, config)` → str (task_id)
  - [ ] `launch_swarm(query, num_agents)` → str (task_id)
  - [ ] `get_status(task_id)` → Dict
  - [ ] `cancel_task(task_id)` → bool
  - [ ] `get_results(task_id)` → Dict
  - [ ] Tests: Mock MCP server

- [ ] `scripts/cascade.py`
  - [ ] Implement Dream Cascade pattern
  - [ ] Belter agent spawning
  - [ ] Drummer synthesis
  - [ ] Camina executive synthesis
  - [ ] Result aggregation

- [ ] `scripts/swarm.py`
  - [ ] Implement Dream Swarm pattern
  - [ ] Parallel agent execution
  - [ ] Result collection
  - [ ] Aggregation logic

- [ ] `scripts/monitor.py`
  - [ ] `stream_status(task_id, callback)` → None
  - [ ] `get_metrics(task_id)` → Dict
  - [ ] `estimate_completion(task_id)` → datetime
  - [ ] Real-time status updates

- [ ] `scripts/patterns.py`
  - [ ] Load available patterns
  - [ ] Validate task specs
  - [ ] Generate execution plans

- [ ] `scripts/requirements.txt`
  - [ ] httpx >= 0.24.0
  - [ ] pydantic >= 2.0
  - [ ] pyyaml >= 6.0

#### Documentation

- [ ] `SKILL.md` (Cascade vs Swarm)
- [ ] `reference/examples.md` (3+ examples)
- [ ] `reference/pattern-specs.md`
- [ ] `reference/job-monitoring.md`

#### Tests

- [ ] `tests/test_orchestrator.py` (6+ tests)
- [ ] `tests/test_cascade.py` (4+ tests)
- [ ] `tests/test_swarm.py` (4+ tests)
- [ ] `tests/test_monitor.py` (4+ tests)
- [ ] Coverage: ≥ 80%

#### Quality Checks

- [ ] MCP integration functional
- [ ] Pattern validation working

---

## Phase 3: Secondary Skills (Week 4)

Repeat the pattern from Phase 2 for each of these:

### 3.1 fullstack-dev
- [ ] React scaffolder
- [ ] Flask/Express templates
- [ ] DB migrator
- [ ] API generator
- [ ] Tests: ≥ 80% coverage
- [ ] Docs: Complete SKILL.md + examples

### 3.2 project-planner
- [ ] Task queue generator
- [ ] Dependency analyzer
- [ ] Gantt chart generator
- [ ] Effort estimator
- [ ] Tests: ≥ 80% coverage
- [ ] Docs: Complete SKILL.md + examples

### 3.3 web-orchestration
- [ ] Flask scaffolder
- [ ] Express scaffolder
- [ ] Middleware utilities
- [ ] API templates
- [ ] Tests: ≥ 80% coverage

### 3.4 corpus-analysis
- [ ] Query engine
- [ ] Statistics calculator
- [ ] Collocation analysis
- [ ] Tests: ≥ 80% coverage

### 3.5 python-cli
- [ ] Click scaffolder
- [ ] Typer scaffolder
- [ ] Package manager
- [ ] Tests: ≥ 80% coverage

### 3.6 game-dev
- [ ] Godot scaffolder
- [ ] Asset manager
- [ ] Build tools
- [ ] Tests: ≥ 80% coverage

### 3.7 dev-tools
- [ ] git automation
- [ ] docs generator
- [ ] API client helpers
- [ ] Cleanup utilities
- [ ] Tests: ≥ 80% coverage

---

## Phase 4: Integration (Week 5)

### 4.1 Agent-Skill Wiring

For each agent category:

- [ ] Update agent YAML header
  ```yaml
  ---
  name: geepers_datavis
  skills:
    - datavis >= 1.0.0
  ---
  ```

- [ ] Update agent logic to use SkillRunner
  ```python
  from geepers.skills import SkillRunner
  skill = SkillRunner()
  result = skill.run(...)
  ```

- [ ] Remove duplicate instruction text from agent
  - Move script docs → skill/reference/
  - Keep decision logic in agent

### 4.2 Test Agent-Skill Integration

For each agent:

- [ ] Test agent calling skill directly
- [ ] Test skill response handling
- [ ] Test error propagation
- [ ] Test result formatting

### 4.3 Documentation Updates

- [ ] Update /home/coolhand/CLAUDE.md
  - Add skills section
  - Update agent descriptions
  - Add skill usage examples

- [ ] Update each agent definition
  - Add skills reference
  - Update When to Use section
  - Add integration examples

- [ ] Create migration guide
  - Show before/after examples
  - Document breaking changes (none)
  - Backward compatibility notes

### 4.4 Full System Test

- [ ] Test 5 complete workflows
  - [ ] "Create GDP visualization"
  - [ ] "Deploy new service"
  - [ ] "Run code quality scan"
  - [ ] "Fetch ML papers from arXiv"
  - [ ] "Research using Cascade pattern"

---

## Phase 5: Advanced Features (Week 6+)

### 5.1 Skill Composition

- [ ] Allow skills to call other skills
  ```python
  # Inside fullstack-dev skill
  quality_result = SkillRunner().run('code-quality', ...)
  ```

- [ ] Test skill-to-skill calls
  - [ ] fullstack-dev → code-quality
  - [ ] project-planner → datavis
  - [ ] mcp-orchestration → data-fetch

### 5.2 Dynamic Skill Loading

- [ ] Create skill loader system
  ```python
  loader = SkillLoader()
  skills = loader.discover()  # Find all skills
  loader.load('datavis')
  ```

- [ ] Test dynamic loading

### 5.3 Performance Monitoring

- [ ] Add metrics collection
  ```python
  {
    'duration': 1.23,
    'api_calls': 3,
    'tokens': 4500,
    'cache_hits': 2
  }
  ```

- [ ] Create monitoring dashboard

### 5.4 Skill Marketplace

- [ ] Create skill registry API
- [ ] Allow skill sharing
- [ ] Version management
- [ ] Dependency resolution

---

## Phase 6: Validation & Deployment

### 6.1 Security Audit

- [ ] [ ] Audit all skill scripts
  - [ ] No hardcoded secrets
  - [ ] No privilege escalation
  - [ ] API key rotation compatible

- [ ] Penetration testing
  - [ ] Test input validation
  - [ ] Test error handling
  - [ ] Test rate limiting

### 6.2 Performance Testing

- [ ] Benchmark each skill
  - [ ] Measure execution time
  - [ ] Measure memory usage
  - [ ] Measure API quota impact

- [ ] Establish baseline performance
  - Agent execution 20% faster
  - Token usage 30% lower
  - Skill reuse 90%+

### 6.3 Documentation Completeness

- [ ] Every skill has complete SKILL.md
- [ ] Every script has docstrings
- [ ] Every public method documented
- [ ] At least 3 examples per skill
- [ ] FAQ section for each skill

### 6.4 Final Testing

- [ ] Run full test suite
  - [ ] `pytest ~/.claude/skills/*/tests/ --cov`
  - [ ] Coverage ≥ 85%
  - [ ] No warnings

- [ ] Run all 5 workflows again
  - [ ] Visualization creation
  - [ ] Service deployment
  - [ ] Code quality scan
  - [ ] Data fetching
  - [ ] Orchestrated research

- [ ] Get user feedback
  - [ ] 5+ test users
  - [ ] Collect feedback
  - [ ] Iterate based on feedback

---

## Success Criteria

### By end of Phase 2 (Week 3)

- [ ] 5 core skills fully implemented
- [ ] ≥ 80% test coverage on all skills
- [ ] All SKILL.md files complete
- [ ] All examples run without errors
- [ ] No security issues in code audit

### By end of Phase 3 (Week 4)

- [ ] 7+ secondary skills implemented
- [ ] All skills documented
- [ ] All scripts tested

### By end of Phase 4 (Week 5)

- [ ] All agents updated to use skills
- [ ] Agent-skill integration working
- [ ] 5 complete workflows tested
- [ ] Documentation updated

### By end of Phase 6 (Week 6+)

- [ ] Skill composition working
- [ ] Performance targets met
- [ ] Security audit complete
- [ ] Ready for production use

---

## Metrics Tracking

Create `~/geepers/reports/skills/IMPLEMENTATION_METRICS.md`:

```markdown
# Skills Implementation Progress

## Phase 1: Infrastructure
- [ ] Complete: 0%
- Last update: [date]

## Phase 2: Core Skills
- datavis: [COMPLETE|IN PROGRESS|PENDING]
  - Tests: X/Y passing
  - Coverage: X%
  - Docs: X% complete

[... repeat for each skill]

## Overall
- Total tasks: 150+
- Completed: X
- Completion: X%
```

Update weekly.

---

## Emergency Rollback

If implementation fails at any point:

1. Abort current phase
2. Document what went wrong
3. Revert changes: `git checkout HEAD -- ~/.claude/skills/`
4. File issue with reproduction steps
5. Plan alternative approach

No data loss (all in git).

---

## Parallel Work Stream

While implementing skills, parallelize:

- [ ] Update documentation (user guide, examples)
- [ ] Create tutorial videos (optional)
- [ ] Set up monitoring dashboard
- [ ] Plan performance optimization
- [ ] Draft skill marketplace spec

---

## Review Gates

Before proceeding to next phase, have:

- [ ] Code review (at least 1 reviewer)
- [ ] Security review
- [ ] Documentation review
- [ ] Performance testing
- [ ] User feedback

---

**Document Version**: 1.0
**Last Updated**: 2025-12-18
**Next Review**: 2026-01-15

This checklist is your map to success. Update it as you progress, and celebrate each completed item!

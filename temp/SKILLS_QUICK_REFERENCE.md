# Claude Skills Architecture - Quick Reference

**Generated**: 2025-12-18
**Author**: Luke Steuber

## Core Concept

Transform geepers agents from **instruction-based advisors** into **execution-capable orchestrators** by pairing each agent category with executable skills.

```
Agent        +  Skill         =  Automation
(Think)         (Execute)         (Result)
```

---

## Skill Directory Quick Map

### Priority 1: Core Skills (Implement Weeks 2-3)

| Skill | Maps To | Primary Command | Use When |
|-------|---------|-----------------|----------|
| **datavis** | `geepers_datavis*` | `create_d3_viz()` | Need to visualize data with D3/Chart.js |
| **server-deploy** | `geepers_caddy`, `geepers_services` | `deploy_service()` | Need to deploy app or configure Caddy routing |
| **code-quality** | `geepers_testing`, `geepers_perf` | `run_full_scan()` | Need to test, lint, or audit code |
| **data-fetch** | `geepers_data`, `geepers_fetcher` | `get_client('arxiv')` | Need to fetch data from external APIs |
| **mcp-orchestration** | `conductor_geepers` | `launch_cascade()` | Need multi-agent research or complex orchestration |

### Priority 2: Secondary Skills (Implement Week 4)

| Skill | Purpose | Key Scripts |
|-------|---------|-------------|
| **fullstack-dev** | Full-stack scaffolding | React builder, DB migrator, API generator |
| **project-planner** | Strategic planning | Task queue, dependency graph, Gantt charts |
| **web-orchestration** | Web app scaffolding | Flask scaffolder, Express scaffolder |
| **corpus-analysis** | Linguistics analysis | Query engine, statistics, collocations |
| **python-cli** | CLI tool creation | Click scaffolder, package manager |
| **game-dev** | Game development | Godot scaffolder, asset manager |
| **dev-tools** | General utilities | git automation, docs generator |

### Priority 3: Novel Skills (New Capabilities)

| Skill | Purpose | Enables |
|-------|---------|---------|
| **llm-comparison** | Compare LLM providers | Benchmark Anthropic vs xAI vs OpenAI |
| **visualization-gallery** | Manage viz library | Gallery builder, theme exporter |

---

## Skill Directory Structure Template

```
my-skill/
├── SKILL.md              # Metadata + comprehensive guide (200-400 lines)
├── LICENSE.txt           # MIT or Apache 2.0
├── scripts/
│   ├── __init__.py
│   ├── main.py           # Entry point
│   ├── feature1.py       # Core functionality
│   ├── feature2.py       # Core functionality
│   ├── utils.py          # Helpers
│   ├── config.py         # Configuration
│   ├── requirements.txt   # Python dependencies
│   └── README.md         # Script documentation
├── reference/
│   ├── examples.md       # Usage examples
│   ├── api-reference.md  # API docs
│   ├── templates/        # Reusable code templates
│   └── best-practices.md # Principles & patterns
├── tests/
│   ├── test_*.py
│   └── fixtures/
└── .skillrc              # Optional configuration
```

---

## SKILL.md Template

```yaml
---
name: my-skill
description: |
  One-liner summary.

  Multi-paragraph explanation of what this skill does,
  when to use it, and key benefits.

license: MIT or Apache 2.0
min_claude_version: "4.5"
depends_on: []           # Other skills required
tags: [category, usecase]
---

## Overview
[Design philosophy and purpose]

## When to Use This Skill
[Decision criteria and examples]

## Available Commands
- `command1`: Brief description
- `command2`: Brief description

## Architecture
[Internal structure and key components]

## Integration with Agents
[How agents invoke this skill]

## Safety & Constraints
[Limitations, permissions, safeguards]

## Examples
[Concrete usage examples]
```

---

## Agent → Skill Invocation Pattern

### In Agent Definition

```yaml
---
name: geepers_datavis
description: Create data visualizations
skills:
  - datavis >= 1.0.0    # Declare skill dependency
---
```

### In Agent Logic

```python
from geepers.skills import SkillRunner

# Create runner
skill = SkillRunner()

# Execute skill command
result = skill.run(
    skill_name='datavis',
    command='create_d3_viz',
    args={
        'data': [...],
        'theme': 'modern',
        'type': 'bar-chart'
    }
)

# Process result
if result['status'] == 'success':
    print(f"Success! File: {result['file']}")
else:
    print(f"Error: {result['errors']}")
```

---

## Skill Response Format

```python
{
    'status': 'success|error|partial',      # Execution status
    'data': {...},                          # Result data
    'file': '/path/to/output',             # Output file path (if applicable)
    'logs': ['log1', 'log2'],              # Execution logs
    'metrics': {
        'duration': 1.23,                  # Seconds
        'api_calls': 3,                    # External API calls
        'tokens': 4500                     # LLM tokens used
    },
    'errors': [],                          # Any errors encountered
    'warnings': [],                        # Non-fatal warnings
    'next_steps': ['step1', 'step2']      # Suggested actions
}
```

---

## Implementation Timeline

### Week 1: Infrastructure
- [ ] Directory structure setup
- [ ] Skill template generator
- [ ] Validation framework
- [ ] Testing infrastructure

### Week 2-3: Core Skills
- [ ] datavis skill (D3, Chart.js, color system)
- [ ] server-deploy skill (Caddy, services, ports)
- [ ] code-quality skill (pytest, ruff, security)
- [ ] data-fetch skill (17+ API clients)
- [ ] mcp-orchestration skill (Cascade, Swarm)

### Week 4: Secondary Skills
- [ ] fullstack-dev
- [ ] project-planner
- [ ] web-orchestration
- [ ] corpus-analysis
- [ ] python-cli
- [ ] game-dev
- [ ] dev-tools

### Week 5: Integration
- [ ] Agent-skill communication protocol
- [ ] Agent definition updates
- [ ] Integration testing
- [ ] Documentation finalization

### Week 6+: Advanced Features
- [ ] Skill composition (skill → skill calls)
- [ ] Dynamic skill loading
- [ ] Performance monitoring
- [ ] Skill marketplace

---

## 5-Skill Spotlight

### 1. datavis

**Maps to**: geepers_datavis agents
**Key Scripts**:
- `viz_generator.py` - Create D3/Chart.js/SVG visualizations
- `color_system.py` - Generate accessible color palettes
- `data_loader.py` - Load CSV/JSON/API data
- `dataset_fetcher.py` - Fetch from World Bank, Census, etc.

**Example**:
```python
skill.run('datavis', 'create_d3_viz', {
    'data': [...],
    'type': 'bar-chart',
    'theme': 'modern'
})
# Returns: {status: 'success', file: 'chart.html'}
```

### 2. server-deploy

**Maps to**: geepers_caddy, geepers_services
**Key Scripts**:
- `deploy.py` - Deploy services with validation
- `caddy_manager.py` - Add/modify Caddy routes
- `port_finder.py` - Find available ports
- `service_checker.py` - Health checks

**Example**:
```python
skill.run('server-deploy', 'deploy_service', {
    'name': 'myapp',
    'port': 5012,
    'path': '/myapp/*'
})
# Validates, deploys, and reloads Caddy
```

### 3. code-quality

**Maps to**: geepers_testing, geepers_perf, geepers_a11y
**Key Scripts**:
- `quality_scanner.py` - Run all checks
- `pytest_runner.py` - Test execution
- `ruff_checker.py` - Linting
- `security_scan.py` - Bandit, safety checks

**Example**:
```python
result = skill.run('code-quality', 'run_full_scan', {
    'project_path': '/path/to/project',
    'min_coverage': 80
})
# Returns: {score: 85.5, tests: {...}, lint: {...}}
```

### 4. data-fetch

**Maps to**: geepers_data, geepers_fetcher
**Key Scripts**:
- `fetcher.py` - API client factory
- `clients/arxiv.py`, `clients/census.py`, etc. - 17+ data sources
- `cache.py` - Caching layer
- `rate_limiter.py` - Rate limit handling

**Example**:
```python
client = skill.run('data-fetch', 'get_client', {
    'source': 'arxiv'
})
papers = client.search('machine learning', max_results=100)
# Returns: [{title: '...', authors: [...], ...}]
```

### 5. mcp-orchestration

**Maps to**: conductor_geepers
**Key Scripts**:
- `cascade.py` - Dream Cascade (hierarchical)
- `swarm.py` - Dream Swarm (parallel)
- `monitor.py` - Job monitoring
- `orchestrator.py` - Main entry point

**Example**:
```python
task_id = skill.run('mcp-orchestration', 'launch_cascade', {
    'task': 'Research ML history',
    'num_belters': 5
})
# Returns immediately with task_id
status = skill.run('mcp-orchestration', 'get_status', {'task_id': task_id})
# Poll until complete, then retrieve results
```

---

## File Locations

```
~/.claude/
├── skills/                          # All skills live here
│   ├── datavis/
│   ├── server-deploy/
│   ├── code-quality/
│   ├── data-fetch/
│   ├── mcp-orchestration/
│   └── [10 more skills...]
│
└── agents/                          # Agents updated to reference skills
    ├── datavis/
    ├── deploy/
    ├── quality/
    ├── research/
    └── [remaining categories...]

~/geepers/                           # Skill output locations
├── reports/skills/                  # Skill execution reports
├── logs/skills/                     # Skill logs
└── cache/skills/                    # Skill caching layer

~/.claude/skills/.skillrc             # Global skill configuration

~/SKILLS_ARCHITECTURE.md              # Full architecture document (this file's parent)
```

---

## Configuration

### Global Config (~/.claude/skills/.skillrc)

```yaml
api_keys:
  anthropic: "${ANTHROPIC_API_KEY}"
  census: "${CENSUS_API_KEY}"
  github: "${GITHUB_TOKEN}"

paths:
  scripts: "~/.claude/skills/*/scripts"
  cache: "~/.cache/geepers/skills"
  logs: "~/geepers/logs/skills"

performance:
  parallel_clients: 4
  timeout_seconds: 300
```

### Per-Skill Config (datavis/.skillrc)

```yaml
datavis:
  default_theme: "modern"
  d3_version: "v7"
  max_data_points: 10000
```

---

## Testing Skills

```bash
# Run unit tests
pytest skills/datavis/tests/ -v --cov=scripts

# Validate SKILL.md format
python -m geepers.skills validate datavis/

# Check dependencies
pip-audit skills/datavis/scripts/requirements.txt

# Manual test
python -c "
from geepers.skills import SkillRunner
skill = SkillRunner()
result = skill.run('datavis', 'create_d3_viz', {'data': [...]})
print(result)
"
```

---

## Migration Checklist

### For Each Agent Category

- [ ] Create corresponding skill
- [ ] Move scripts from agent docs to skill/scripts/
- [ ] Write SKILL.md with comprehensive guide
- [ ] Add examples to reference/examples.md
- [ ] Write unit tests
- [ ] Update agent definition to reference skill
- [ ] Test agent-skill integration
- [ ] Update documentation

### Overall

- [ ] All core skills implemented
- [ ] All agents updated to use skills
- [ ] Integration tests passing (80% coverage)
- [ ] Documentation complete
- [ ] Performance benchmarks met
- [ ] Security audit complete

---

## Success Metrics

| Metric | Target | Benefit |
|--------|--------|---------|
| Skill adoption | 80% of agents using skills | Consistent execution |
| Code reuse | 90% of skill code reusable | Reduced duplication |
| Agent instruction reduction | -40% lines | Simpler, focused agents |
| Test coverage | 85%+ | Higher quality |
| Execution speed | -20% agent overhead | Faster workflows |
| Token usage | -30% LLM tokens | Lower cost |

---

## Support & Troubleshooting

### Common Issues

**Q: Skill fails with "RateLimitError"**
A: DataFetch skill includes automatic backoff. Check `rate_limiter.py` for configuration.

**Q: Caddy reload fails**
A: ServerDeploy skill validates before reload. Check `caddy_manager.py` logs in `~/geepers/logs/skills/`.

**Q: Visualization is blank**
A: Check data format. Datavis skill expects `[{x: val, y: val}]` format. See `reference/examples.md`.

### Debugging

```bash
# Check skill logs
tail -f ~/geepers/logs/skills/datavis.log

# Monitor skill execution
python ~/.claude/skills/scripts/debug.py --skill datavis --verbose

# Test individual script
cd ~/.claude/skills/datavis/scripts
python viz_generator.py --data sample.json
```

---

## Related Documents

- **Full Architecture**: `/home/coolhand/SKILLS_ARCHITECTURE.md` (50 pages, detailed design)
- **Agent System**: `/home/coolhand/CLAUDE.md#Geepers Agent System`
- **Anthropic Skills**: `/tmp/skills/skills/` (reference implementations)

---

## Next Steps

1. Read full `SKILLS_ARCHITECTURE.md` for comprehensive design
2. Begin Phase 1: Set up directory structure and tooling
3. Implement 5 core skills (Weeks 2-3)
4. Integrate with existing agents (Week 5)
5. Monitor metrics and iterate

---

**Document Version**: 1.0 Quick Reference
**Full Architecture Location**: `/home/coolhand/SKILLS_ARCHITECTURE.md`
**Last Updated**: 2025-12-18

# Geepers Agent Reference

Quick reference for all 51 agents organized by category.

## Master Orchestration (1)

| Agent | Purpose |
|-------|---------|
| `conductor_geepers` | Master orchestrator - routes to all other agents |

## Product Development (7) ⭐ NEW

| Agent | Purpose |
|-------|---------|
| `geepers_orchestrator_product` | Coordinates product development pipeline |
| `geepers_business_plan` | Generate business plans & market analysis |
| `geepers_prd` | Create Product Requirements Documents |
| `geepers_fullstack_dev` | Full-stack code generation from PRD |
| `geepers_intern_pool` | Cost-effective multi-model code generation |
| `geepers_code_checker` | Multi-model code validation & QA |
| `geepers_docs` | Generate documentation (README, setup guides) |

## Checkpoint & Maintenance (5)

| Agent | Purpose |
|-------|---------|
| `geepers_orchestrator_checkpoint` | Session maintenance coordination |
| `geepers_scout` | Project reconnaissance & quick fixes |
| `geepers_repo` | Git hygiene & repository cleanup |
| `geepers_status` | Work logging & status tracking |
| `geepers_snippets` | Harvest reusable code patterns |

## Deployment & Infrastructure (4)

| Agent | Purpose |
|-------|---------|
| `geepers_orchestrator_deploy` | Deployment workflow coordination |
| `geepers_validator` | Configuration & health validation |
| `geepers_caddy` | Caddy proxy configuration |
| `geepers_services` | Service lifecycle management |

## Code Quality (5)

| Agent | Purpose |
|-------|---------|
| `geepers_orchestrator_quality` | Quality audit coordination |
| `geepers_a11y` | Accessibility audits (WCAG) |
| `geepers_perf` | Performance profiling & optimization |
| `geepers_deps` | Dependency audits & security |
| `geepers_critic` | UX & architecture critique |

## Research & Data (6)

| Agent | Purpose |
|-------|---------|
| `geepers_orchestrator_research` | Research workflow coordination |
| `geepers_swarm_research` | Multi-tier research (Quick/Swarm/Hive) ⭐ NEW |
| `geepers_data` | Data quality & validation |
| `geepers_links` | Link validation & checking |
| `geepers_diag` | System diagnostics & log analysis |
| `geepers_citations` | Citation & source validation |

## Full-Stack Development (4)

| Agent | Purpose |
|-------|---------|
| `geepers_orchestrator_fullstack` | Full-stack feature coordination |
| `geepers_db` | Database optimization & queries |
| `geepers_design` | Visual design systems & UI |
| `geepers_react` | React component development |

## Game Development (4)

| Agent | Purpose |
|-------|---------|
| `geepers_orchestrator_games` | Game development coordination |
| `geepers_gamedev` | Game mechanics & design |
| `geepers_game` | Gamification design |
| `geepers_godot` | Godot Engine development |

## Linguistics & NLP (3)

| Agent | Purpose |
|-------|---------|
| `geepers_orchestrator_corpus` | Corpus linguistics coordination |
| `geepers_corpus` | Corpus linguistics & datasets |
| `geepers_corpus_ux` | Corpus UI/UX (KWIC, concordance) |

## Web Development (2)

| Agent | Purpose |
|-------|---------|
| `geepers_orchestrator_web` | Web application coordination |
| `geepers_flask` | Flask patterns & development |

## Python Projects (2)

| Agent | Purpose |
|-------|---------|
| `geepers_orchestrator_python` | Python project coordination |
| `geepers_pycli` | CLI tool development (argparse, click) |

## Standalone Specialists (5)

| Agent | Purpose |
|-------|---------|
| `geepers_api` | API design review & documentation |
| `geepers_scalpel` | Surgical code modifications |
| `geepers_janitor` | Aggressive cleanup & dead code removal |
| `geepers_canary` | Early warning health checks |
| `geepers_dashboard` | Dashboard sync & admin panel |

## System Utilities (3)

| Agent | Purpose |
|-------|---------|
| `geepers_system_help` | Agent reference documentation |
| `geepers_system_onboard` | Project understanding & analysis |
| `geepers_system_diag` | Comprehensive system diagnostic |

---

## Quick Command Patterns

### Common Invocations

```
"I have an idea for..."          → conductor → product orchestrator
"Check this project's health"     → conductor → checkpoint orchestrator
"Deploy this service"             → conductor → deploy orchestrator
"Review code quality"             → conductor → quality orchestrator
"Research X topic deeply"         → conductor → swarm_research (hive mode)
"Build full-stack feature"        → conductor → fullstack orchestrator
"Create a game mechanic"          → conductor → games orchestrator
"Fix Caddy config"                → caddy (direct)
"Quick health check"              → canary (direct)
"What agents exist?"              → system_help (direct)
```

### Direct Agent Access

Use direct access for specific, focused tasks:

```bash
@geepers_scout              # Quick reconnaissance
@geepers_caddy              # Caddy changes only
@geepers_a11y               # Accessibility audit only
@geepers_business_plan      # Just the business plan
@geepers_prd                # Just the PRD
@geepers_swarm_research     # Deep research mode
```

### Orchestrator Access

Use orchestrators for coordinated multi-agent workflows:

```bash
@geepers_orchestrator_product      # Full product pipeline
@geepers_orchestrator_checkpoint   # Session wrap-up
@geepers_orchestrator_deploy       # Infrastructure changes
@geepers_orchestrator_quality      # Comprehensive audit
@geepers_orchestrator_research     # Multi-source data gathering
```

---

**Total Agents**: 51  
**Total Orchestrators**: 11 (10 topic + 1 master)  
**Version**: 1.0.0  
**Last Updated**: 2025-12-15

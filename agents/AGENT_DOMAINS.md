# Geepers Agent Domains

Quick reference for all agents organized by domain.

## Domain Overview

| Domain | Directory | Purpose | Key Agents |
|--------|-----------|---------|------------|
| **Master** | `master/` | Top-level routing | conductor_geepers |
| **Checkpoint** | `checkpoint/` | Session maintenance | scout, repo, status, snippets |
| **Deploy** | `deploy/` | Infrastructure | caddy, services, validator, canary |
| **Quality** | `quality/` | Code quality | a11y, perf, api, deps, critic, testing, security |
| **Frontend** | `frontend/` | UI development | css, typescript, motion, webperf, design, uxpert, react |
| **Fullstack** | `fullstack/` | End-to-end features | orchestrator_fullstack |
| **Web** | `web/` | Web applications | flask, express, orchestrator_web |
| **Hive** | `hive/` | Implementation factory | planner, builder, quickwin, integrator, refactor |
| **Research** | `research/` | Data gathering | data, links, diag, citations, fetcher, searcher |
| **Python** | `python/` | Python projects | orchestrator_python, pycli |
| **Games** | `games/` | Game development | gamedev, game, godot |
| **Corpus** | `corpus/` | Linguistics/NLP | corpus, corpus_ux, db |
| **System** | `system/` | Meta/infrastructure | system_help, system_onboard, system_diag |
| **Standalone** | `standalone/` | Cross-cutting | dashboard, janitor, scalpel, docs, git |

---

## By Orchestrator

### geepers_conductor (Master Router)
Routes to all orchestrators based on task type.

### geepers_orchestrator_checkpoint
Session maintenance and documentation.
- `geepers_scout` - Reconnaissance, identifies issues
- `geepers_repo` - Git hygiene
- `geepers_status` - Work logging
- `geepers_snippets` - Pattern harvesting

### geepers_orchestrator_deploy
Infrastructure and deployment.
- `geepers_caddy` - Caddyfile authority
- `geepers_services` - Service lifecycle
- `geepers_validator` - Configuration validation
- `geepers_canary` - Quick health checks

### geepers_orchestrator_quality
Code quality and auditing.
- `geepers_a11y` - Accessibility (WCAG)
- `geepers_perf` - Backend performance
- `geepers_api` - REST API design
- `geepers_deps` - Dependency security
- `geepers_critic` - UX/architecture critique
- `geepers_testing` - Test strategy and coverage
- `geepers_security` - Security audits (OWASP)

### geepers_orchestrator_frontend
Pure frontend development (no backend changes).
- `geepers_css` - CSS architecture, Tailwind
- `geepers_typescript` - TypeScript patterns
- `geepers_motion` - Animation (Framer Motion)
- `geepers_webperf` - Core Web Vitals
- `geepers_design` - Visual design systems
- `geepers_uxpert` - UX interaction patterns
- `geepers_react` - React components

### geepers_orchestrator_fullstack
Full-stack features (NON-Flask backends).
- Backend: `geepers_api`, `geepers_db`, `geepers_services`, `geepers_express`
- Frontend: `geepers_design`, `geepers_a11y`, `geepers_react`

### geepers_orchestrator_web
Flask-specific web applications.
- Backend: `geepers_flask`, `geepers_api`, `geepers_db`
- Frontend: `geepers_react`, `geepers_design`, `geepers_a11y`
- Quality: `geepers_critic`, `geepers_canary`

### geepers_orchestrator_hive
Implementation factory for building features.
- `geepers_planner` - Architecture planning
- `geepers_builder` - Code generation
- `geepers_quickwin` - Safe quick fixes
- `geepers_integrator` - Integration verification
- `geepers_refactor` - Code restructuring

### geepers_orchestrator_research
Data gathering and validation.
- `geepers_data` - Data quality
- `geepers_links` - URL validation
- `geepers_diag` - System diagnostics
- `geepers_citations` - Reference verification
- `geepers_fetcher` - Web/API retrieval
- `geepers_searcher` - Codebase search

### geepers_orchestrator_python
Python project development.
- `geepers_flask` - Flask patterns
- `geepers_pycli` - CLI tools (click, typer)
- `geepers_api` - API design
- `geepers_deps` - Dependencies

### geepers_orchestrator_games
Game development and gamification.
- `geepers_gamedev` - Game architecture
- `geepers_game` - Gamification patterns
- `geepers_godot` - Godot Engine
- `geepers_react` - React games

### geepers_orchestrator_corpus
Linguistics and NLP projects.
- `geepers_corpus` - Corpus linguistics
- `geepers_corpus_ux` - KWIC/concordance UI
- `geepers_db` - Database optimization

---

## Standalone Agents

These agents work independently or across domains:

| Agent | Purpose |
|-------|---------|
| `geepers_dashboard` | Service persistence, admin panel |
| `geepers_janitor` | Aggressive cleanup |
| `geepers_scalpel` - Surgical code edits |
| `geepers_docs` | Documentation generation |
| `geepers_git` | Git operations, merge conflicts |

---

## Quick Decision Guide

```
What do you need?
│
├─► Frontend work (no backend) ────► @geepers_orchestrator_frontend
│
├─► Flask web app ─────────────────► @geepers_orchestrator_web
│
├─► Node.js/Express backend ───────► @geepers_orchestrator_fullstack
│
├─► Build a feature end-to-end ────► @geepers_orchestrator_hive
│
├─► Code quality review ───────────► @geepers_orchestrator_quality
│
├─► Deploy or infrastructure ──────► @geepers_orchestrator_deploy
│
├─► Gather information ────────────► @geepers_orchestrator_research
│
├─► End of session ────────────────► @geepers_orchestrator_checkpoint
│
├─► Python project ────────────────► @geepers_orchestrator_python
│
├─► Game development ──────────────► @geepers_orchestrator_games
│
├─► Linguistics/NLP ───────────────► @geepers_orchestrator_corpus
│
└─► Not sure ──────────────────────► @geepers_conductor
```

---

## Agent Count by Domain

| Domain | Orchestrators | Specialists | Total |
|--------|---------------|-------------|-------|
| Master | 1 | 0 | 1 |
| Checkpoint | 1 | 4 | 5 |
| Deploy | 1 | 4 | 5 |
| Quality | 1 | 7 | 8 |
| Frontend | 1 | 7 | 8 |
| Fullstack | 1 | 0 | 1 |
| Web | 1 | 2 | 3 |
| Hive | 1 | 5 | 6 |
| Research | 1 | 6 | 7 |
| Python | 1 | 1 | 2 |
| Games | 1 | 3 | 4 |
| Corpus | 1 | 3 | 4 |
| System | 0 | 3 | 3 |
| Standalone | 0 | 5 | 5 |
| **Total** | **12** | **50** | **62** |

---

*Last updated: 2024-12-17*

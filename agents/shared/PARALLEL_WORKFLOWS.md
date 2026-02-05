# Parallel Agent Workflows

Powerful agent combinations that work synergistically when run together.

---

## Workflow 1: Session Startup (Recommended)

### Pattern
```
PARALLEL: geepers_scout + geepers_planner
THEN: geepers_conductor (if direction unclear) OR direct to focused agent
```

### What Happens
- **geepers_scout** (5 min): Scans project health, identifies issues
- **geepers_planner** (5 min): Prioritizes tasks, identifies dependencies
- Result: Clear picture of current state + roadmap for session

### Time Comparison
- **Sequential**: 15 min (scout → planner → analysis)
- **Parallel**: 10 min (scout + planner → analysis)
- **Savings**: 5 minutes + better context

### Use Cases
- Starting work on a project
- Returning to project after time away
- Morning session planning
- Before major refactoring

### Example
```bash
# Start parallel agents
geepers_scout --project=wordblocks
geepers_planner --project=wordblocks

# While running, you'll see both:
# - Scout findings (issues, quick wins)
# - Planner recommendations (prioritized tasks)

# Then route based on findings
geepers_builder --queue=wordblocks-queue.md  # If implementation phase
# OR
geepers_orchestrator_quality --findings=scout-report.md  # If cleanup needed
```

---

## Workflow 2: Feature Implementation Pipeline

### Pattern
```
1. geepers_planner       → Create prioritized task queue
2. geepers_builder       → Implement each item atomically
3. geepers_integrator    → Verify cross-system integrity
4. geepers_critic        → Assess architectural impact
5. geepers_repo          → Clean git history
```

### What Happens
- **Planner**: Breaks down feature into tasks with dependencies
- **Builder**: Implements each task following conventions
- **Integrator**: Checks that pieces work together
- **Critic**: Reviews if architecture stayed clean
- **Repo**: Ensures git history is readable

### Time Comparison
- **Ad-hoc**: 6 hours (code, debug, rework, cleanup)
- **Pipeline**: 4 hours (structured, fewer regressions)
- **Savings**: 2 hours + better code quality

### When to Use
- Implementing major features (>3 files affected)
- Multi-developer work
- High-stakes features (auth, payment, core logic)

### Example
```bash
# Phase 1: Planning
geepers_planner --project=corpus --task="Add lemmatization"
# Output: corpus-queue.md with 5 prioritized tasks

# Phase 2: Building
geepers_builder --project=corpus --queue=corpus-queue.md
# Implements: DB migration → API endpoint → UI component → tests

# Phase 3: Integration testing
geepers_integrator --project=corpus --files="api.py,ui.tsx,schema.py"
# Checks: API works with updated schema, UI calls endpoint correctly

# Phase 4: Architecture review
geepers_critic --project=corpus --focus="lemmatization-feature"
# Assesses: Did we add complexity? Is it maintainable?

# Phase 5: Git cleanup
geepers_repo --project=corpus --cleanup=true
```

---

## Workflow 3: Quality Audit Sprint

### Pattern
```
PARALLEL: geepers_scout + geepers_critic + geepers_testing + geepers_security
THEN: geepers_orchestrator_quality (synthesize findings)
```

### What Happens
- **Scout** (concurrent): Code quality scan
- **Critic** (concurrent): UX/architecture issues
- **Testing** (concurrent): Test coverage analysis
- **Security** (concurrent): Vulnerability scan
- **Orchestrator** (sequential): Summarizes, prioritizes, routes fixes

### Time Comparison
- **Sequential**: 120 min (4 audits × 30 min each)
- **Parallel**: 45 min (30 min audit + 15 min synthesis)
- **Savings**: 75 minutes

### When to Use
- Before major releases
- Quarterly code reviews
- After major refactoring
- When starting work on unfamiliar codebase

### Quality Coverage
- Code quality issues
- UX friction and design problems
- Technical debt inventory
- Test coverage gaps
- Security vulnerabilities
- Dependency risks

### Example
```bash
# Start all audits in parallel
geepers_scout --project=wordblocks &
geepers_critic --project=wordblocks &
geepers_testing --project=wordblocks &
geepers_security --project=wordblocks &

# Wait for all to complete, then synthesize
wait
geepers_orchestrator_quality \
  --scout=reports/scout-wordblocks.md \
  --critic=reports/critic-wordblocks.md \
  --testing=reports/testing-wordblocks.md \
  --security=reports/security-wordblocks.md
```

---

## Workflow 4: Health & Performance Check

### Pattern
```
PARALLEL: geepers_canary + geepers_diag + geepers_perf
THEN: geepers_services (if action needed)
```

### What Happens
- **Canary** (3 min): Quick service health snapshot
- **Diag** (5 min): Deep system analysis
- **Perf** (5 min): Performance metrics and bottlenecks
- **Services** (varies): Apply fixes if needed

### Time Comparison
- **Sequential**: 20 min (each then next)
- **Parallel**: 8 min (all at once + fix time)
- **Savings**: 12 minutes per check

### When to Use
- Daily health monitoring
- Weekly performance reviews
- After deploying changes
- When users report slowness
- Capacity planning

### Health Metrics Collected
- Service availability
- Memory/CPU usage
- Error rates
- Database query performance
- API response times

### Example
```bash
# Morning health check
geepers_canary &
geepers_diag &
geepers_perf &
wait

# If canary found issues, drill deeper
if [ $CANARY_STATUS = "WARN" ]; then
  geepers_services --action=diagnose --issue=$CANARY_FINDING
fi
```

---

## Workflow 5: Refactoring Campaign

### Pattern
```
1. geepers_scout      → Identify refactoring opportunities
2. PARALLEL: geepers_critic + geepers_snippets
3. geepers_planner    → Prioritize refactoring tasks
4. geepers_scalpel    → Implement carefully
5. geepers_integrator → Verify no regressions
```

### What Happens
- **Scout**: Finds code that needs refactoring
- **Critic**: Assesses architectural impact
- **Snippets**: Extracts reusable patterns
- **Planner**: Creates refactoring task queue
- **Scalpel**: Implements with surgical precision
- **Integrator**: Ensures nothing broke

### Time Comparison
- **Naive**: 8 hours (code + debug + rework)
- **Structured**: 5 hours (planned + careful + verified)
- **Savings**: 3 hours + fewer bugs

### When to Use
- Technical debt paydown sprints
- Before adding major features
- Quarterly code health initiatives
- Code smell cleanup

### Refactoring Scope
- Duplicate code consolidation
- Complex function decomposition
- Module reorganization
- Pattern standardization

### Example
```bash
# Phase 1: Identification
geepers_scout --project=diachronica --focus="refactoring"
# Finds: 12 opportunities (duplication, long functions, etc)

# Phase 2: Impact assessment (parallel)
geepers_critic --project=diachronica &
geepers_snippets --project=diachronica --extract=patterns &
wait

# Phase 3: Planning
geepers_planner --project=diachronica \
  --source=scout-report.md,critic-report.md

# Phase 4-5: Implementation with verification
for task in $(cat diachronica-queue.md | grep "^## ")
do
  geepers_scalpel --task=$task
  geepers_integrator --verify-no-regressions
done
```

---

## Workflow 6: Documentation & Knowledge

### Pattern
```
PARALLEL: geepers_scout + geepers_snippets
THEN: geepers_docs
```

### What Happens
- **Scout** (5 min): Generates insights about codebase
- **Snippets** (5 min): Extracts reusable patterns
- **Docs** (15 min): Synthesizes into documentation

### Time Comparison
- **Manual**: 60 min (reading code + writing)
- **Automated**: 25 min (agents + review)
- **Savings**: 35 minutes + higher accuracy

### When to Use
- After major features complete
- Quarterly knowledge updates
- Onboarding new developers
- Creating architecture documentation

### Documentation Output
- API documentation
- Architecture diagrams/descriptions
- Pattern guides
- Module organization
- Common workflows

### Example
```bash
# Collect insights
geepers_scout --project=diachronica --generate-insights &
geepers_snippets --project=diachronica --extract=patterns &
wait

# Generate documentation
geepers_docs --project=diachronica \
  --insights=scout-report.md \
  --patterns=snippets-report.md \
  --output=ARCHITECTURE.md
```

---

## Workflow 7: Bug Investigation & Fix

### Pattern
```
1. geepers_diag       → Root cause analysis
2. geepers_scalpel    → Surgical fix
3. geepers_testing    → Add regression test
4. geepers_repo       → Document fix
```

### What Happens
- **Diag**: Analyzes logs, finds actual problem (not symptom)
- **Scalpel**: Makes precise fix to complex code
- **Testing**: Prevents same bug recurring
- **Repo**: Documents why bug happened

### Time Comparison
- **Ad-hoc**: 90 min (guess → try → fail → debug → retry)
- **Systematic**: 45 min (diagnose → fix → test → document)
- **Savings**: 45 minutes + understanding

### When to Use
- Production bugs
- Mysterious failures
- Performance problems
- Intermittent issues

### Bug Investigation Depth
- Error patterns in logs
- Resource utilization at time of failure
- Correlation with recent changes
- Impact scope

### Example
```bash
# Diagnose the issue
geepers_diag --service=wordblocks --since="2 hours ago"
# Output: "Memory leak in WebSocket handler, lines 234-245"

# Fix with precision
geepers_scalpel --file=src/websocket.ts --lines=234-245

# Prevent recurrence
geepers_testing --add-regression-test \
  --file=test/websocket.test.ts \
  --scenario="memory-leak-on-disconnect"

# Document findings
geepers_repo --commit-message="fix: Prevent WebSocket memory leak on client disconnect

Root cause: Connection cleanup wasn't removing event listeners.
See diag report from $(date).

Fixes: #2847"
```

---

## Workflow Selection Guide

| Goal | Workflow | Time | Complexity |
|---|---|---|---|
| Start session focused | #1 (Startup) | 10 min | Low |
| Build feature right | #2 (Implementation) | 4 hours | High |
| Comprehensive audit | #3 (Quality Sprint) | 45 min | Medium |
| Monitor health | #4 (Health Check) | 8 min | Low |
| Clean up code | #5 (Refactoring) | 5 hours | High |
| Create docs | #6 (Documentation) | 25 min | Low |
| Fix production issue | #7 (Bug Investigation) | 45 min | Medium |

---

## Pro Tips for Parallel Workflows

### Tip 1: Output Consistency
Ensure parallel agents write to different files:
```bash
# Good: Different output files
geepers_scout --output=reports/scout-{project}.md
geepers_planner --output=reports/planner-{project}.md

# Bad: Same output file (conflict)
geepers_scout --output=report.md
geepers_planner --output=report.md
```

### Tip 2: Sequential Dependencies
Respect task dependencies:
```bash
# Good: Scout runs first, then Planner sees results
geepers_scout && geepers_planner

# Bad: Planner runs before Scout findings exist
geepers_planner & geepers_scout
```

### Tip 3: Monitor Progress
Use `geepers_status` to track workflow progress:
```bash
geepers_scout &
geepers_planner &
PIDS=$!
geepers_status --watch --pids=$PIDS
```

### Tip 4: Batch Periodic Checks
Run Workflow #4 on schedule:
```bash
# In crontab
0 */4 * * * /path/to/workflow-health-check.sh
```

### Tip 5: Cost-Benefit Analysis
Use heavier workflows for higher-stakes work:
```bash
# Quick fix: Skip Workflow #2, use geepers_quickwin
# Major feature: Use full Workflow #2 (Planner → Builder → Integrator)
# Production issue: Use full Workflow #7 (Diag → Fix → Test → Docs)
```

---

## Troubleshooting

### Problem: Agents running out of order
**Solution**: Use explicit sequencing
```bash
# Bad: No guarantee of order
geepers_agent1 &
geepers_agent2 &
geepers_agent3 &

# Good: Explicit sequence
geepers_agent1 && geepers_agent2 && geepers_agent3
```

### Problem: Conflicting changes from parallel agents
**Solution**: Design non-overlapping scopes
```bash
# Scout analyzes code quality
# Planner creates task queue (different output)
# They don't conflict because different outputs
```

### Problem: Workflow takes too long
**Solution**: Profile and optimize
```bash
time geepers_scout --project=X
time geepers_planner --project=X
# If one is slow, consider parallelizing differently
```

---

*Last Updated: 2026-01-05*
*Part of Agent Optimization Analysis*

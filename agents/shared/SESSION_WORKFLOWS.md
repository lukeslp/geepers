# Standard Session Workflows

Recommended patterns for starting and ending work sessions.

---

## Session Start: Full Context Workflow

### Recommended Pattern
```
1. PARALLEL: geepers_scout + geepers_planner
2. Review findings
3. Route to focused work based on priorities
```

### Detailed Steps

#### Step 1: Launch Parallel Assessment (5 minutes)

```bash
# Launch both agents in background
geepers_scout --project=$PROJECT &
geepers_planner --project=$PROJECT &

# Wait for completion
wait
```

**Scout generates**:
- Current codebase health
- Quick wins identified
- Issues found
- Architecture observations

**Planner generates**:
- Prioritized task queue
- Effort estimates
- Dependencies mapped
- Risk assessments

#### Step 2: Review Findings (5 minutes)

```bash
# Check what was found
cat ~/geepers/reports/latest/scout-${PROJECT}.md
cat ~/geepers/hive/${PROJECT}-queue.md
```

**Key questions to answer**:
- Are there critical issues to fix first? (scout findings)
- What's the highest-value work? (planner queue)
- Are there quick wins? (scout + planner)
- Any blockers? (planner dependencies)

#### Step 3: Choose Focus Track

**If fixing issues**:
```bash
geepers_orchestrator_quality --findings=scout-report.md
```

**If implementing features**:
```bash
geepers_builder --queue=${PROJECT}-queue.md
```

**If refactoring**:
```bash
geepers_orchestrator_hive --focus=refactoring
```

**If starting from scratch**:
```bash
geepers_conductor --project=$PROJECT --full-assessment
```

### Output
- Clear priorities for the session
- Understanding of current state
- Focused work direction

### Time Investment: 15 minutes for clarity worth hours of wasted effort

---

## Session Middle: Check-in Pattern

Use this when taking breaks or switching contexts during a session.

### Quick Check-in (10 minutes)

```bash
# Current status
geepers_canary --quick

# Any issues since last session?
geepers_diag --since="last-1-hour"

# What's the current priority?
cat ~/geepers/hive/${PROJECT}-queue.md | head -5
```

### Deep Check-in (30 minutes)

```bash
# Full project health scan
geepers_scout --quick-mode

# Any blockers discovered?
cat ~/geepers/logs/builder-*.log | tail -20

# What should we shift focus to?
geepers_planner --reweight-priorities
```

---

## Session End: Checkpoint Workflow

### Recommended Pattern
```
1. Finalize current work
2. geepers_repo --cleanup
3. geepers_orchestrator_checkpoint
4. Optional: Update recommendations
```

### Detailed Steps

#### Step 1: Finalize Current Work (5 minutes)

```bash
# Commit current changes
git add -A
git commit -m "checkpoint: End of session, $(date +'%Y-%m-%d %H:%M')"

# Or, if work is incomplete
git stash  # Save changes for next session
```

#### Step 2: Git Cleanup (5 minutes)

```bash
# Clean up branches, organize history
geepers_repo --project=$PROJECT --cleanup
```

**Cleans up**:
- Merged branches
- Merge conflicts
- Uncommitted changes
- Temporary files

#### Step 3: Full Checkpoint (10 minutes)

```bash
# Run complete checkpoint suite
geepers_orchestrator_checkpoint --project=$PROJECT
```

**Captures**:
- Work completed
- Work in progress status
- Recommendations
- Next session focus
- Code quality metrics

#### Step 4: Update Recommendations (5 minutes)

```bash
# If found new issues or insights
geepers_planner --update-recommendations --findings="$TODAY"
```

### Output Files
- `~/geepers/status/current-session.json` - Updated
- `~/geepers/reports/by-date/YYYY-MM-DD/*` - Daily report
- `~/geepers/recommendations/by-project/${PROJECT}.md` - Updated
- `~/geepers/hive/${PROJECT}-queue.md` - Updated priorities

### Session Summary (generated automatically)
```
Session Summary: 2026-01-05 9:00-17:30 (8h 30m)
Project: wordblocks
Code Quality: 8/10 (+1 from start)
Tasks Completed: 4
Lines Changed: 234
Commits: 6
Next Focus: Database optimization
```

---

## Extended Session: Daily Sprint Pattern

For projects where you're working for multiple days in a row.

### Day 1 Morning (15 min)
```
Session Start: Full Context Workflow
  ↓
Scout + Planner (parallel)
  ↓
Review priorities
```

### Day 1 Midday (10 min)
```
Quick Check-in
  ↓
Any new priorities?
  ↓
Adjust focus if needed
```

### Day 1 Evening (15 min)
```
Session End: Checkpoint Workflow
  ↓
Full checkpoint
  ↓
Update next-day priorities
```

### Day 2 Morning (10 min)
```
Quick Start (lighter than Day 1)
  ↓
Review end-of-day summary
  ↓
geepers_scout --updated-since="last-night"
  ↓
Focus on highest priority
```

### Day 2+ Pattern
```
Morning: Quick check-in (10 min)
  ↓
Work focused track (4 hours)
  ↓
Midday: Adjustment check (10 min)
  ↓
Afternoon: Continue or switch track
  ↓
Evening: Checkpoint
```

---

## Specific Situation Workflows

### Situation 1: Returning After Days Away

**Problem**: "I forgot what I was working on"

**Solution**:
```bash
# See what happened while you were gone
geepers_scout --detailed --comprehensive

# Get updated priorities
geepers_planner --project=$PROJECT

# Check for urgent issues
geepers_canary --alert-mode

# Read the summary
cat ~/geepers/reports/latest/scout-${PROJECT}.md
```

**Time**: 15 minutes to re-contextualize

---

### Situation 2: Stuck or Lost Direction

**Problem**: "I'm not sure what to work on"

**Solution**:
```bash
# Get fresh perspective
geepers_critic --project=$PROJECT

# See what's failing
geepers_diag --show-recent-errors

# Re-prioritize
geepers_planner --reweight

# Consider quick wins
geepers_quickwin --list-available
```

**Time**: 10 minutes to refocus

---

### Situation 3: Found Major Issue Mid-Session

**Problem**: "This is more broken than I thought"

**Solution**:
```bash
# Stash current work
git stash

# Assess the scope
geepers_diag --issue="description"

# Update priorities
geepers_planner --emergency-reweight

# Decide: Fix now or schedule?
# If critical: geepers_scalpel --urgent
# If can wait: Add to queue
```

**Time**: 10 minutes to assess

---

### Situation 4: Code Review Ready

**Problem**: "Is this ready for review?"

**Solution**:
```bash
# Full quality check
geepers_orchestrator_quality

# Check for any regressions
geepers_integrator --comprehensive

# Verify test coverage
geepers_testing --check-coverage

# Architecture assessment
geepers_critic --focus="changes"

# Once all pass: Ready for review
```

**Time**: 30 minutes

---

### Situation 5: Performance Issues Reported

**Problem**: "Users say things are slow"

**Solution**:
```bash
# PARALLEL: Full diagnostics
geepers_canary &
geepers_diag &
geepers_perf &
wait

# Analyze findings
geepers_planner --type="performance-optimization"

# Fix identified bottleneck
geepers_scalpel --optimize

# Verify fix
geepers_integrator --performance-test
```

**Time**: 45 minutes to identify and fix

---

## Session Configuration

### Create ~/.geepers/session.config

```yaml
# Project-specific session settings
project: wordblocks
working_directory: /home/coolhand/servers/clinical

# Session preferences
auto_checkpoint: true
checkpoint_interval: 3600  # seconds (1 hour)

# Alerts
alert_on_errors: true
alert_on_slow_tests: true

# Defaults
default_agents:
  - geepers_scout
  - geepers_planner

# Periodic tasks
daily_health_check: true
weekly_quality_audit: false
monthly_full_assessment: false
```

---

## Session Metrics to Track

### Per-Session
- Duration (start to end)
- Tasks completed
- Code quality change (before/after)
- Lines added/removed
- Files modified
- Tests added/modified

### Weekly
- Total coding time
- Quality trend
- Task completion rate
- Average task duration

### Monthly
- Architecture health
- Technical debt trend
- Code quality trend
- Team velocity

### Use for
- Identifying productivity patterns
- Spotting performance regressions
- Planning refactoring needs
- Recognizing consistent issues

---

## Pro Tips

### Tip 1: Time Box Each Phase
```bash
# Session Start: 15 min max
# Focused Work: 90-120 min (then check-in)
# Session End: 20 min
```

### Tip 2: Use Geepers Status Log
```bash
# See what's been done today
cat ~/geepers/status/current-session.json | jq '.summary'
```

### Tip 3: Commit at Phase Boundaries
```bash
# After Scout + Planner
# After each major feature
# Before switching contexts
# At end of day (always)
```

### Tip 4: Review Recommendations
Always start by checking:
```bash
cat ~/geepers/recommendations/by-project/$PROJECT.md
```

Before session, you might find you've already analyzed the area.

### Tip 5: Skip Steps if Familiar
If you know the project well:
```bash
# Skip full scout
geepers_planner --quick  # Just re-prioritize

# Focus straight to work
geepers_builder --queue=queue.md
```

---

## Common Anti-Patterns

### ❌ Skip Planning
```bash
# DON'T: Start coding immediately
# DO: Run planner first (15 min saves hours)
```

### ❌ Skip Checkpoint
```bash
# DON'T: Just close the laptop
# DO: Run checkpoint (20 min saves confusion next session)
```

### ❌ Ignore Scout Findings
```bash
# DON'T: See scout found issues, ignore them
# DO: Address issues or explicitly defer them
```

### ❌ No Mid-Session Check
```bash
# DON'T: Code 4 hours without checking in
# DO: Check-in every 90 minutes
```

### ❌ Manual Context Switching
```bash
# DON'T: Manually track what you're doing
# DO: Let geepers_status track it
```

---

## Quick Reference Commands

### Session Start
```bash
alias sess-start='geepers_scout --project=$PROJECT & geepers_planner --project=$PROJECT & wait'
```

### Session Check-in
```bash
alias sess-check='geepers_canary --quick && tail -20 ~/geepers/logs/builder-*.log'
```

### Session End
```bash
alias sess-end='git add -A && git commit -m "checkpoint: $(date)" && geepers_orchestrator_checkpoint'
```

### Session Status
```bash
alias sess-status='cat ~/geepers/status/current-session.json | jq .'
```

---

*Last Updated: 2026-01-05*
*Part of Agent Optimization Analysis*

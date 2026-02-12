# Dataset Consolidation: Planner Output README

**Date**: 2026-02-10
**Project**: datavis infrastructure consolidation
**Status**: Analysis Complete → Ready for Execution
**Output Location**: `/home/coolhand/geepers/hive/`

---

## Three Documents Generated

### 1. ANALYSIS-DATAVIS-CONSOLIDATION.md (This Suite)

**What**: Executive summary of the consolidation plan
**Length**: ~400 lines
**For Whom**: Quick orientation, decision-making, success criteria
**Key Sections**:
- What the plan does (consolidated view)
- Critical path & blocking dependencies
- Risk mitigation
- Execution quick reference
- Success checklist

**Start Here If**: You want to understand what's happening at a high level

---

### 2. datavis-consolidation-queue.md (MAIN EXECUTION DOCUMENT)

**What**: 15 prioritized, sequenced tasks with exact commands
**Length**: ~550 lines
**For Whom**: People executing the work
**Format**: Each task includes:
- Impact/Effort/Priority scores
- Description and rationale
- Dependencies listed
- Exact bash/git commands to run
- Verification steps
- File paths affected

**Key Sections**:
- Ready to Build (15 prioritized tasks)
- Deferred tasks (future work)
- Statistics and metrics
- Execution notes (git safety, disk checks)
- Verification checklist

**Start Here If**: You're about to begin execution

---

### 3. planner-datavis-consolidation.md (PLANNING REPORT)

**What**: Comprehensive planning analysis
**Length**: ~550 lines
**For Whom**: Project managers, risk reviewers, documentation
**Format**: Structured analysis document
- Plan source review
- User corrections applied
- Task breakdown with dependencies
- Parallelization opportunities
- Risk assessment (high/medium/low)
- Timeline estimates
- Success criteria

**Key Sections**:
- Executive summary
- Plan analysis
- Task breakdown
- Dependency analysis
- Risk assessment (6 risks identified + mitigations)
- Alternative approaches considered
- Success criteria

**Start Here If**: You need to understand risks, alternatives, and planning rationale

---

## How to Use This Suite

### For Quick Orientation (15 min)

1. Read this README
2. Read "Three Most Impactful Tasks" section of ANALYSIS
3. Review "Critical Path" diagram

**Outcome**: Understand what's being done and why

### For Execution (3 hours)

1. Read ANALYSIS-DATAVIS-CONSOLIDATION.md (full)
2. Open datavis-consolidation-queue.md in separate window
3. Execute Task 1 → Task 15 in order, following exact commands
4. Run verification checks after each major phase
5. Refer to Risk Mitigation section if issues arise

**Outcome**: Consolidated data infrastructure

### For Approval/Review (30 min)

1. Read "Executive Summary" of planner-datavis-consolidation.md
2. Scan "Risk Assessment" section
3. Review "Success Criteria" section
4. Ask questions about any risks identified

**Outcome**: Confidence in plan quality

---

## Quick Start (Copy-Paste)

### If You're Ready to Execute Now

```bash
# Step 1: Verify you have the task queue
cat /home/coolhand/geepers/hive/datavis-consolidation-queue.md | head -50

# Step 2: Do pre-execution checks
df -h /home/coolhand/html/datavis/        # Need ~500MB free
cd /home/coolhand/html/datavis/
git log --oneline -3                       # Confirm current state

# Step 3: Start Task 1 (GitHub auth)
gh auth logout
gh auth login
# Follow interactive prompts...

# Step 4: Test auth works
gh repo list | head -3

# Step 5: Move to Task 2
# Follow commands in datavis-consolidation-queue.md
```

### If You Have Questions

| Question | Answer Location |
|----------|-----------------|
| What blocks what? | planner-datavis-consolidation.md § Dependency Analysis |
| What if GitHub auth fails? | ANALYSIS § Risk Mitigation |
| How long will this take? | planner-datavis-consolidation.md § Timeline Estimate |
| What are the 5 new datasets? | datavis-consolidation-queue.md § Tasks 8-12 |
| What gets deleted? | ANALYSIS § What Gets Archived |
| How do I verify success? | datavis-consolidation-queue.md § Verification Checklist |
| What's the naming convention? | ANALYSIS § Naming Convention |

---

## Key Findings Summary

### What's Being Done

**Consolidation**: Data fragmented across 6+ locations → unified under GitHub + HuggingFace + Kaggle

**Backups**: 452MB unharvested dev/ data → protected in data-hoard (git versioned)

**Elimination**: 350MB redundancy in ~/datasets/ → archived

**Publishing**: 20 real quirky datasets → 5 themed bundles across 3 platforms

**Naming**: All new repos use `-atlas` / `-dataset` / `-data` (NO "kaggle-data")

### What's Ready Now

- All 15 tasks identified and ordered
- All dependencies mapped
- All bash/git commands written
- All risks identified + mitigation
- Backwards compatibility confirmed

### What's Blocked

Nothing. All tasks proceed after Task 1 (GitHub auth).

---

## Naming Convention (Critical)

**Applied to all 5 new repos**:

```
natural-world-atlas         (geographic/mappable)
earth-phenomena-dataset     (categorical/analytical)
historical-sites-atlas      (geographic/historical)
unexplained-dataset         (categorical/niche)
solar-system-data           (analytical/scientific)
```

**NOT used**: "kaggle-data" suffix (user specifically rejected this)

---

## Platform Targets After Consolidation

| Platform | Before | After | New |
|----------|--------|-------|-----|
| GitHub Repos | 8 | 13 | 5 |
| HuggingFace Datasets | 18 | 22 | 4 |
| Kaggle Datasets | 16 | 20 | 4 |
| Existing Repos Renamed | 1 | 1 | data_trove → data-hoard |

---

## Timeline

**Quick** (1.5 hours): If executed with maximum parallelization

**Standard** (3 hours): If executed sequentially with testing between phases

**Phases**:
1. GitHub Auth (5 min)
2. Local Consolidation (40 min)
3. GitHub Repos (45 min)
4. Platform Publication (75 min)
5. Cleanup (10 min)

---

## Success Verification (TL;DR)

```bash
# Quick verification after execution
ls -la /home/coolhand/html/datavis/data_trove      # Should be symlink
find /home/coolhand/html/datavis/data-hoard -type l | wc -l  # Should be 0
ls /home/coolhand/datasets 2>&1                     # Should error (not found)
curl -I https://dr.eamer.dev/datavis/data_trove/  # Should be 200
curl -I https://github.com/lukeslp/data-hoard     # Should be 200
```

---

## Files in This Suite

```
/home/coolhand/geepers/hive/
├── README-DATAVIS-CONSOLIDATION.md (this file)
├── ANALYSIS-DATAVIS-CONSOLIDATION.md (executive summary)
├── datavis-consolidation-queue.md (15 tasks, exact commands)
└── ../reports/by-date/2026-02-10/
    └── planner-datavis-consolidation.md (comprehensive planning report)
```

---

## Git Safety Protocol

Before EVERY commit:

1. `git log --oneline -3` → Confirm latest commit is expected
2. `git diff --stat` → Verify only intended changes
3. `git status` → Check for unexpected files

This prevents agents from overwriting each other's work.

---

## Next Steps

1. **Read**: ANALYSIS-DATAVIS-CONSOLIDATION.md (15 min)
2. **Review**: planner-datavis-consolidation.md if approving (30 min)
3. **Execute**: datavis-consolidation-queue.md Task 1 → Task 15 (3 hours)
4. **Verify**: Run success checklist at end of task queue

---

## Contact / Questions

Refer to appropriate document:
- **"What should I do first?"** → ANALYSIS
- **"What exact command do I run?"** → datavis-consolidation-queue.md
- **"What could go wrong?"** → planner-datavis-consolidation.md § Risk Assessment
- **"Why are we doing this?"** → planner-datavis-consolidation.md § Executive Summary

---

**Status**: READY FOR EXECUTION ✓

All analysis complete. No blockers except GitHub authentication (Task 1).

Proceed to datavis-consolidation-queue.md when ready to execute.

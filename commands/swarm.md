---
description: Parallel build - fan out agents to accomplish tasks simultaneously
---

# Swarm

Parallel building mode. Takes plans, tasks, or backlog items and dispatches multiple builder agents simultaneously to implement them.

**Swarm builds things. For searching, use `/geepers-hunt`. For everything at once, use `/geepers-team`.**

## Execute

### 1. Analyze the Task

Break the input into independent subtasks that can be worked in parallel:
- Read the plan, task list, or description in $ARGUMENTS
- Identify natural boundaries (separate files, independent features, non-overlapping modules)
- Flag any dependencies between subtasks — those must be sequenced, not parallelized

### 2. Dispatch Builders (launch ALL independent tasks in the SAME message)

For each independent subtask, dispatch the appropriate agent:

| Agent | Use When |
|-------|----------|
| **@geepers_builder** | New feature implementation, creating files/functions |
| **@geepers_quickwin** | Small fixes, obvious improvements, low-hanging fruit |
| **@geepers_refactor** | Restructuring without changing functionality |
| **@geepers_planner** | Subtask needs further decomposition before building |

### 3. Collect and Verify

After all agents complete:
- Check for conflicts between parallel work (same files modified, naming collisions)
- Verify each subtask meets its requirements

### 4. Integrate

Launch **@geepers_integrator** to:
- Reconcile any overlapping changes
- Verify cross-subtask consistency
- Run integration checks

### 5. Final Review

Quick sanity check:
- `git diff --stat` to see total changes
- Verify nothing was accidentally overwritten

## Distinction

| Mode | Purpose | Agents |
|------|---------|--------|
| **Swarm** | Parallel BUILDING | builder, quickwin, refactor, integrator |
| **Hunt** | Parallel SEARCHING | searcher, fetcher, data, links, citations |
| **Team** | EVERYTHING at once | all relevant agents, no filter |

## Target

**Task/plan**: $ARGUMENTS

If no arguments, ask what needs to be built.

# ================================================
# git add -A Root-Repo Hazard (Agent Safety Pattern)
# ================================================
# Language: bash
# Tags: git, safety, agents, monorepo, performance, staged-files, background-agents
# Source: packages/ audit session 2026-03-07
# Last Updated: 2026-03-07
# Author: Luke Steuber
# ================================================
# Description:
# Background agents that run `git add -A` from the root of a large monorepo
# (55+ services, 300+ directories) can lock git for 6+ minutes while it
# indexes the entire working tree. This also risks staging unintended files
# from parallel agent runs. Always stage specific files by name. This snippet
# documents the hazard and provides safe alternatives for agent-generated commits.
# ================================================

## The Hazard

Running from a monorepo root with many subdirectories:

```bash
cd /home/coolhand
git add -A        # scans entire tree: html/, servers/, packages/, datasets/, ...
                  # 6+ minutes of wall time, git lock held throughout
                  # may stage files written by OTHER parallel agents
git commit -m "..." # now commits things you didn't write
```

Root-level `git add -A` is a **two-headed hazard**:
1. Performance: multi-minute lock blocks all other git ops
2. Correctness: stages stray files from concurrent agents

## Safe Pattern: stage specific files only

```bash
# Name the files you changed explicitly
git add packages/cleanupx/pyproject.toml packages/cleanupx/.gitignore
git commit -m "fix: add py-modules to wheel manifest"
```

## Safe Pattern: stage only within the target subdirectory

```bash
# cd into the package, then add — limits the scan scope
cd /home/coolhand/packages/cleanupx
git add pyproject.toml .gitignore CHANGELOG.md
git commit -m "fix: wheel manifest and gitignore"
```

## Safe Pattern: verify before every add

```bash
# Mandatory pre-commit checks (from global CLAUDE.md)
git log --oneline -3          # confirm no surprise commits from other agents
git diff --stat               # verify only expected changes are present
git status                    # spot untracked files you didn't create
```

## Detecting a stale lock

```bash
ls -la /home/coolhand/.git/index.lock 2>/dev/null && echo "GIT LOCKED"

# Wait for lock to clear before any git op:
while [ -f /home/coolhand/.git/index.lock ]; do sleep 5; done
```

## Agent instruction template

When writing agent prompts or skills that commit from a monorepo root,
include this block:

```
CRITICAL GIT SAFETY:
- NEVER run `git add -A` or `git add .` from the repo root
- Stage only the specific files you modified: `git add path/to/file1 path/to/file2`
- Before staging, run `git log --oneline -3` to confirm no concurrent agent commits
- Before staging, run `git diff --stat` to verify only your changes are present
- If anything unexpected appears in status or diff, STOP and report to user
```

## Root-cause: why monorepos are especially susceptible

The git index lock is held for the full duration of the tree walk. In a repo
with symlinks (~/geepers/snippets -> ~/SNIPPETS), untracked large dataset dirs
(~/datasets/), and dozens of submodule-like package dirs, `git add -A` from
root can exceed the 2-minute timeout on automated agent runs.

# ================================================
# Usage Example:
# ================================================
# Instead of:
#   git add -A && git commit -m "chore: update cleanupx"
#
# Do:
#   git add /home/coolhand/packages/cleanupx/pyproject.toml \
#           /home/coolhand/packages/cleanupx/.gitignore
#   git commit -m "chore: update cleanupx"

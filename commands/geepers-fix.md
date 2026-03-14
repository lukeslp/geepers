---
description: Quick fixes and surgical code changes - find low-hanging fruit and fix precisely
---

# Fix Mode

Find issues and fix them efficiently, from quick wins to surgical precision.

## Two Fix Modes

### Quick Wins (Default)

Launch **@geepers_quickwin** to:
- Identify high-impact, low-effort improvements
- Fix obvious issues immediately
- Clean up technical debt
- Address linting/formatting issues

Great for:
- Starting a session with visible progress
- Time-limited fix windows
- Warming up on a codebase

### Surgical Precision

Launch **@geepers_scalpel** for:
- Complex files (>200 lines)
- Delicate code with intricate dependencies
- Targeted changes that require high precision
- Fixes where previous edits introduced regressions

Scalpel protocol:
1. Read ENTIRE file context
2. Identify exact change boundaries
3. Make minimal, precise modifications
4. Verify no regressions introduced

## Execute

**Mode/Target**: $ARGUMENTS

If no arguments:
- Run @geepers_quickwin for quick wins sweep

If "quick" or "wins":
- Focus on low-hanging fruit only

If "surgical" or "precise":
- Launch @geepers_scalpel for careful, targeted fixes

If file path or description:
- Analyze the specific target
- Choose appropriate approach (quickwin vs scalpel)

## Supporting Agents

- **@geepers_refactor** - Restructure without changing functionality
- **@geepers_janitor** - Deep cleanup and cruft removal
- **@geepers_diag** - Root cause investigation
- **@geepers_testing** - Verify fixes don't break tests

## Workflow

```
Identify Issue
    │
    ▼
┌─────────────────────────────┐
│ Simple fix in small file?   │
│ YES → @geepers_quickwin     │
│ NO  → ↓                     │
└─────────────────────────────┘
    │
    ▼
┌─────────────────────────────┐
│ Complex/large/delicate?     │
│ YES → @geepers_scalpel      │
│ NO  → Direct fix            │
└─────────────────────────────┘
    │
    ▼
Test & Verify
```

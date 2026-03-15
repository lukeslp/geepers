---
description: Test strategy, coverage analysis, and test writing for any project
---

# Testing Mode

Design test strategy, analyze coverage, and write tests.

## Execute

Launch **@geepers_testing** to:

1. Analyze existing test coverage and identify gaps
2. Recommend test strategy (unit, integration, e2e)
3. Write tests for uncovered code
4. Set up test infrastructure if missing

## Modes

```
/testing               # Full analysis — coverage, gaps, strategy
/testing write         # Write tests for uncovered code
/testing coverage      # Coverage analysis only
/testing strategy      # Recommend test approach without writing
```

## What It Checks

- Test file existence and organization
- Coverage gaps in critical paths
- Test quality (assertions, edge cases, error paths)
- Test infrastructure (pytest config, fixtures, mocks)
- CI integration (test scripts in package.json, Makefile, etc.)

## Technology Detection

Automatically adapts to project stack:
- **Python**: pytest, unittest, coverage.py
- **TypeScript/JS**: vitest, jest, playwright
- **Flask**: test client patterns, fixture setup
- **React**: component testing, hook testing

## Cross-References

- Quality audit: `/audit` (includes test coverage)
- Pre-ship checks: `/ship` (runs tests before deploy)
- Security testing: `/audit` with security focus

**Focus area** (optional): $ARGUMENTS

---
description: Comprehensive quality audit - accessibility, performance, security, dependencies
---

# Audit Mode

Run a comprehensive quality audit across all dimensions.

## Execute in PARALLEL

Launch ALL of these agents simultaneously:

1. **@geepers_a11y** - WCAG 2.1 AA accessibility compliance
2. **@geepers_perf** - performance profiling and bottlenecks
3. **@geepers_security** - security vulnerabilities and OWASP
4. **@geepers_deps** - dependency audit, vulnerabilities, licenses
5. **@geepers_api** - API design review and REST compliance
6. **@geepers_critic** - UX friction and architectural critique
7. **`/context audit`** - CLAUDE.md nav headers, cross-references, cruft

## Alternative

The `/quality-audit` skill provides similar functionality and can be used interchangeably.

## Optional Deep Dives

Based on findings, consider:
- **@geepers_webperf** - frontend-specific performance (Core Web Vitals)
- **@geepers_db** - database optimization
- **@geepers_testing** - test coverage analysis

## Output

Each agent produces findings. Consolidate into actionable priorities:
- **Critical** - fix immediately
- **High** - fix before next release
- **Medium** - schedule for improvement
- **Low** - nice to have

## Store Results

Save audit findings to `~/geepers/recommendations/by-project/<project>.md` for future reference.

## Cross-References

- Quick recon: `/scout`
- Deploy after audit: `/ship`
- Release workflow: `/release`
- Impact analysis: `/foresight`

**Audit scope**: $ARGUMENTS

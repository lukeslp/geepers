---
description: Deploy with full quality checks - validate, test, and ship safely
---

# Ship Mode

Prepare and deploy with comprehensive safety checks.

## Pre-flight Checklist

Launch these agents in PARALLEL:

1. **@geepers_validator** - comprehensive project validation
2. **@geepers_canary** - spot-check critical systems
3. **@geepers_testing** - verify test coverage and run tests
4. **@geepers_security** - security audit before deploy
5. **`/geepers-context audit`** - verify CLAUDE.md nav headers and cross-references

## Deployment

After checks pass:

1. **@geepers_repo** - ensure clean git state, proper commits
2. **@geepers_orchestrator_deploy** - coordinate infrastructure changes
3. **@geepers_caddy** - handle any routing changes (SOLE authority for Caddyfile)
4. **@geepers_services** - manage service lifecycle

## Post-deploy

1. **@geepers_canary** - verify everything is healthy
2. **@geepers_status** - log the deployment

## Rollback

If issues detected post-deploy:
1. `sm stop <service>` - Stop problematic service
2. `git revert HEAD` or restore from backup
3. `sm start <service>` - Restart with previous version
4. Investigate via **@geepers_diag**

## Humanize Gate

If release notes, changelogs, or README updates were created during deployment:
- Run `/humanize` on all front-facing content before pushing
- Catches "AI" terminology, robotic phrasing, press-release tone

## Cross-References

- Pre-release checks: `/geepers-release` (version bump, changelog, publish)
- Impact analysis: `/geepers-foresight` (check what this deploy affects)
- Session management: `/geepers-session`
- Alternative: `/server-deploy` skill

**What to ship**: $ARGUMENTS

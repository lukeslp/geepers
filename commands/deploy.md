---
description: Deploy and manage services - start, stop, restart, routing, port allocation
---

# Deploy Mode

Coordinate service deployment, infrastructure changes, and routing updates.

## Execute

Launch **@geepers_orchestrator_deploy** to coordinate the full deployment:

1. **@geepers_validator** — pre-deploy validation (configs, paths, permissions)
2. **@geepers_caddy** — routing changes (SOLE authority for Caddyfile)
3. **@geepers_services** — service lifecycle (start, stop, restart)

## Quick Actions

```
/deploy start <service>     # Start a service
/deploy stop <service>      # Stop a service
/deploy restart <service>   # Restart a service
/deploy status              # Check all service status
/deploy add <service>       # Register a new service
/deploy route <path>        # Add or modify Caddy routing
```

## New Service Checklist

When deploying a new service:

1. **@geepers_validator** — verify project structure and configs
2. Add to `service_manager.py` with port, health endpoint
3. **@geepers_caddy** — configure Caddy routing
4. **@geepers_services** — start and verify health
5. **@geepers_canary** — post-deploy spot-check

## Post-deploy

1. **@geepers_canary** — verify everything is healthy
2. **@geepers_status** — log the deployment

## Cross-References

- Full ship workflow: `/ship` (includes quality checks)
- Impact analysis: `/foresight` (check what this deploy affects)
- Service health: `/health`

**What to deploy**: $ARGUMENTS

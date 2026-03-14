---
description: Service health monitoring - check all 30+ services, identify issues, restart unhealthy
---

# Health Mode

Monitor and maintain the 30+ services running on dr.eamer.dev.

## Quick Health Check

```bash
sm status                    # All services
sm health                    # Health endpoints only
sm status | grep -v healthy  # Show only issues
```

## Service Tiers

### Critical (always running)
- wordblocks (8847) - AAC communication
- lessonplanner (4108) - EFL lessons
- coca (3034) - Corpus API
- firehose (5052) - Bluesky dashboard

### Standard
- clinical (1266), altproxy (1131), storyblocks (8000)
- dreamboard (9999), studio (5413), luke (5211)
- etymology (5013), social-scout (5010)

### Generators
- insults (5015), antijokes (5016), dadjokes (5017)
- colors (5018), compliments (5019)

### Bluesky Ecosystem
- firehose (5052), unified (3001/5086), bluevibes (5012)
- bipolar-interactive (5082/5083)

## Workflows

### Full Health Audit
Launch in PARALLEL:
1. @geepers_canary - Spot-check critical systems
2. @geepers_services - Service status overview
3. @geepers_diag - Error pattern detection

### Investigate Unhealthy Service
1. `sm logs <service>` - Check recent logs
2. @geepers_diag - Root cause analysis
3. `sm restart <service>` - Restart if needed
4. @geepers_canary - Verify recovery

### Restart All Unhealthy
```bash
# Find and restart unhealthy services
sm status | grep "connection refused" | awk '{print $1}' | xargs -I {} sm restart {}
```

## Common Issues

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Connection refused | Service crashed | `sm restart <service>` |
| Port in use | Zombie process | `lsof -i :<port>` then kill |
| 502 Bad Gateway | Caddy → service mismatch | Check Caddyfile routing |
| Slow response | Resource exhaustion | Check logs, restart |

## Monitoring Locations

```
~/admin/                    # Dashboard and admin tools
/etc/caddy/Caddyfile       # Reverse proxy config
~/servers/                  # Service source code
```

## Execute

**Action**: $ARGUMENTS

If no arguments or "status":
- Show full service status

If "issues" or "problems":
- Show only unhealthy services

If "restart <service>":
- Restart specific service

If "audit":
- Full health audit with parallel agents

If "critical":
- Check only critical tier services

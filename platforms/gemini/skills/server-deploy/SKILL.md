---
name: server-deploy
description: Deploy and manage services on dr.eamer.dev server. Use when (1) starting, stopping, or restarting services, (2) checking service status and health, (3) managing Caddy reverse proxy routes, (4) deploying new services, (5) viewing service logs.
---

# Server Deploy Skill

Manage services and deployments on the dr.eamer.dev server.

## Service Management (sm CLI)

The server runs 27+ services managed by `sm` (service_manager.py).

### Quick Commands

```bash
scripts/service.py status              # All services status
scripts/service.py start wordblocks    # Start service
scripts/service.py stop wordblocks     # Stop service
scripts/service.py restart wordblocks  # Restart service
scripts/service.py logs wordblocks     # View logs
scripts/service.py health              # Health check all services
```

## Available Services

| Service | Port | Type | Description |
|---------|------|------|-------------|
| wordblocks | 8847 | Flask | AAC communication app |
| lessonplanner | 4108 | Flask | EFL lesson generator |
| clinical | 1266 | Flask | Clinical reference |
| coca | 3034 | Gunicorn | Corpus linguistics API |
| storyblocks | 8000 | Flask | LLM API proxy |
| skymarshal | 5050 | Flask | Bluesky management |
| dashboard | 9999 | Flask | System monitoring |
| luke | 5211 | Node/Express | Portfolio site |
| altproxy | 1131 | Flask | Alt text generation |
| mcp-orchestrator | 5060 | Flask | MCP server |
| swarm | 5001 | Flask | Multi-agent AI |
| beltalowda | 5009 | Flask | Hierarchical orchestration |
| etymology | 5013 | Flask | Etymology visualization |

## Caddy Reverse Proxy

**IMPORTANT**: Always use `@geepers_caddy` agent for Caddy changes.

The Caddyfile at `/etc/caddy/Caddyfile` routes:
- `dr.eamer.dev` → various services
- `d.reamwalker.com`, `d.reamwalk.com` → same services

### Caddy Commands

```bash
scripts/caddy.py validate              # Validate config
scripts/caddy.py status                # Show current routes
scripts/caddy.py add-route /api/* 5000 # Add new route
scripts/caddy.py reload                # Reload config
```

## Port Ranges

| Range | Purpose |
|-------|---------|
| 1000-5000 | Production services |
| 5010-5019 | Testing/development |
| 5050-5059 | Testing/development |
| 8000-9999 | Legacy/special |

## Scripts

### Service Operations
```bash
scripts/service.py status              # All services
scripts/service.py status wordblocks   # Specific service
scripts/service.py start <name>        # Start
scripts/service.py stop <name>         # Stop
scripts/service.py restart <name>      # Restart
scripts/service.py logs <name>         # Stream logs
scripts/service.py logs <name> --tail 100  # Last 100 lines
```

### Deployment
```bash
scripts/deploy.py new myservice --port 5015 --type flask
scripts/deploy.py check myservice      # Pre-deploy validation
scripts/deploy.py rollback myservice   # Rollback last deploy
```

### Health Checks
```bash
scripts/health.py                      # All services
scripts/health.py --service wordblocks # Specific service
scripts/health.py --json               # JSON output
```

## Deployment Workflow

1. **Check port availability**
   ```bash
   scripts/service.py ports
   ```

2. **Validate before deploy**
   ```bash
   scripts/deploy.py check myservice
   ```

3. **Add Caddy route** (via agent)
   ```
   Use @geepers_caddy to add route /myservice/* to port 5015
   ```

4. **Start service**
   ```bash
   scripts/service.py start myservice
   ```

5. **Verify health**
   ```bash
   scripts/health.py --service myservice
   ```

## Safety

- **Always validate** Caddy config before reloading
- **Always check** port availability before deploying
- **Always use** the Caddy agent for route changes
- **Never modify** production services without backup

## Troubleshooting

**Service won't start**:
```bash
scripts/service.py logs myservice --tail 50
```

**Port in use**:
```bash
scripts/service.py ports  # Find what's using the port
```

**502 Bad Gateway**:
```bash
scripts/health.py --service myservice  # Check if running
scripts/caddy.py validate              # Check Caddy config
```

## Related Skills

- **code-quality** - Pre-deploy validation
- **data-fetch** - API integration
- **dream-cascade** - Complex workflows

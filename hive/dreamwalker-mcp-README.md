# Dreamwalker MCP Server Deployment - Complete Planning Package

**Status**: ✅ PLANNING COMPLETE - Ready for Implementation
**Date**: 2026-02-06
**Effort**: 2-3 days of work
**Owner**: Claude Code (Luke Steuber)

---

## What This Package Contains

### 📋 Documents (4 Files in This Directory)

1. **dreamwalker-mcp-SUMMARY.md** (5 min read)
   - Executive summary of the entire plan
   - Quick reference for key decisions
   - Configuration examples
   - Best for: Getting the high-level picture quickly

2. **dreamwalker-mcp-deployment-plan.md** (30 min read)
   - Complete detailed implementation plan
   - 7 major sections with code examples
   - Testing strategy and risk mitigation
   - Best for: Implementation guide - follow this to build

3. **dreamwalker-mcp-ARCHITECTURE.md** (20 min read)
   - System architecture diagrams
   - Data flow and component dependencies
   - Deployment architecture
   - Best for: Understanding how everything connects

4. **dreamwalker-mcp-CHECKLIST.md** (Implementation guide)
   - 47 concrete tasks organized by phase
   - Step-by-step instructions
   - Command references
   - Best for: Following during actual implementation

---

## At-a-Glance Summary

### What We're Building
A production-ready remote MCP server that exposes the Dreamwalker orchestrator to Claude Desktop via HTTPS, with bearer token authentication.

### Where It Lives
- **Code**: `/home/coolhand/shared/mcp/http_mcp_server.py` (NEW)
- **Port**: 5059 (localhost only)
- **Public Route**: `https://dr.eamer.dev/mcp`
- **Startup**: `python3 service_manager.py start mcp-orchestrator`

### What Users Can Do
With this deployed, Claude Desktop users can:
- Research topics using Dream Cascade (hierarchical 3-tier agents)
- Search multiple domains in parallel with Dream Swarm
- Check workflow status and cancel running tasks
- List available tools and execute them

### Example Usage in Claude
```
@tools Research quantum entanglement using Dream Cascade with 3 belters
→ [MCP calls dream_orchestrate_research]
→ [Server returns task_id and stream URL]
→ [User can poll status or subscribe to SSE stream]
```

---

## Key Technical Decisions

### 1. Hybrid Approach (Thin HTTP Wrapper)
- **Why**: Avoid duplicating orchestrator logic
- **What**: Create new FastMCP HTTP server
- **Result**: Reuses existing orchestration, clean separation

### 2. Port 5059
- **Why**: Available in allocated 5050-5059 range
- **Verification**: `lsof -i :5059` shows no conflicts
- **Route**: Caddy proxies `/mcp*` to `localhost:5059`

### 3. Bearer Token Authentication
- **Why**: Prevents unauthorized access
- **How**: `Authorization: Bearer <token>` header
- **Storage**: `/home/coolhand/documentation/API_KEYS.md` (gitignored)
- **Health Exception**: GET /health doesn't require token (for monitoring)

### 4. FastMCP Framework
- **Why**: Modern MCP HTTP standard
- **Benefits**: Native async, streaming-ready, Claude Desktop compatible
- **Dependency**: `fastmcp>=0.1.0`

---

## Files to Create/Modify

### Create (2 Files)
```
✅ /home/coolhand/shared/mcp/http_mcp_server.py     (300-400 lines)
✅ /home/coolhand/shared/mcp/start_mcp_http.sh      (20 lines)
```

### Modify (5 Files)
```
📝 /home/coolhand/service_manager.py                 (+10 lines)
📝 /etc/caddy/Caddyfile                              (+15 lines)
📝 /home/coolhand/documentation/API_KEYS.md          (+2 lines)
📝 /home/coolhand/shared/mcp/requirements.txt        (+4 lines)
📝 /home/coolhand/projects/PORT_ALLOCATION.md        (+1 line)
```

### Total: 7 files touched, ~350 lines of new code

---

## Implementation Timeline

### Day 1 (6-8 hours)
- [ ] **Phase 1**: Create FastMCP HTTP server (2 hours)
  - Tool definitions
  - Authentication middleware
  - Health endpoint
- [ ] **Phase 2**: Infrastructure setup (1 hour)
  - Service manager integration
  - Bearer token generation
  - Caddy configuration

### Day 2 (6-8 hours)
- [ ] **Phase 3**: Testing (3 hours)
  - Unit tests
  - Manual local testing
  - Caddy routing verification
- [ ] **Phase 4**: Claude Desktop integration (2 hours)
  - Config update
  - Tool discovery
  - Tool execution testing

### Day 3 (4-6 hours)
- [ ] **Phase 5**: Production hardening (2 hours)
  - Security audit
  - Performance testing
  - Failure scenario testing
- [ ] Documentation & sign-off (2 hours)
  - Update CLAUDE.md
  - Create runbook
  - Final verification

---

## Success Criteria (10 Items)

✅ Service starts: `sm start mcp-orchestrator` → running
✅ Health check passes: `curl http://localhost:5059/health` → 200 OK
✅ HTTPS routing works: `curl https://dr.eamer.dev/mcp/health` → 200 OK
✅ Auth enforced: Missing token → 401, Invalid token → 403
✅ Tools discoverable in Claude Desktop
✅ dream_orchestrate_research callable from Claude Desktop
✅ dreamwalker_status tracks workflow state
✅ Streaming support (optional but recommended)
✅ Service manager monitoring works
✅ No breaking changes to existing services

---

## Dependencies

### Already Exist ✓
- Orchestration framework (`/home/coolhand/shared/orchestration/`)
- LLM providers (`/home/coolhand/shared/llm_providers/`)
- Data clients (`/home/coolhand/shared/data_fetching/`)
- Service manager (`/home/coolhand/service_manager.py`)
- Caddy (`sudo systemctl status caddy`)

### Need to Add (4 Python packages)
```bash
pip install fastmcp>=0.1.0 uvicorn>=0.24.0 aiohttp>=3.8.0 pydantic>=2.0
```

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| **Auth bypass** | Bearer token required; non-hardcoded; from env var |
| **Timeouts on long tasks** | Caddy timeout = 10 min; SSE streaming for progress |
| **Memory leaks** | Workflow cleanup job; max active workflows limit |
| **Claude Desktop compatibility** | Uses standard FastMCP HTTP spec |
| **Service availability** | Health monitoring by service manager |

---

## Rollback Plan

If something breaks during deployment:

**Service won't start**:
```bash
git checkout /home/coolhand/service_manager.py
sm status  # Should not show mcp-orchestrator
```

**Caddy errors**:
```bash
sudo caddy validate --config /etc/caddy/Caddyfile
git checkout /etc/caddy/Caddyfile
sudo systemctl reload caddy
```

**Bearer token issues**:
```bash
# Disable auth temporarily
export MCP_BEARER_TOKEN=disabled
# Or update in API_KEYS.md
```

---

## Future Enhancements (Post-MVP)

1. **SSE Streaming** - Real-time progress via `/stream/{task_id}`
2. **Redis Backend** - Persistent state for multi-instance
3. **Webhooks** - Notifications on completion
4. **Rate Limiting** - Prevent abuse per bearer token
5. **Audit Logging** - Compliance and debugging
6. **Analytics** - Track usage and performance
7. **Load Balancing** - Scale to multiple servers
8. **Cost Tracking** - Billing integration

---

## Document Reading Order

**If you have 5 minutes**:
→ Read this file (README.md)

**If you have 15 minutes**:
→ Read dreamwalker-mcp-SUMMARY.md

**If you have 1 hour**:
→ Read dreamwalker-mcp-deployment-plan.md (Full details)
→ Read dreamwalker-mcp-ARCHITECTURE.md (How it works)

**If you're implementing**:
→ Use dreamwalker-mcp-CHECKLIST.md (47 concrete tasks)
→ Reference dreamwalker-mcp-deployment-plan.md (Code examples)
→ Check dreamwalker-mcp-ARCHITECTURE.md (When confused)

---

## Key Files Quick Reference

### Location of All Planning Documents
```
/home/coolhand/geepers/hive/
├── dreamwalker-mcp-README.md (this file)
├── dreamwalker-mcp-SUMMARY.md
├── dreamwalker-mcp-ARCHITECTURE.md
├── dreamwalker-mcp-deployment-plan.md
└── dreamwalker-mcp-CHECKLIST.md
```

### Critical System Files
```
/home/coolhand/shared/mcp/           # Where MCP server lives
  └── http_mcp_server.py (TO CREATE)
  └── start_mcp_http.sh (TO CREATE)
  └── requirements.txt (TO UPDATE)
  └── mcp_http_bridge.py (EXISTING)
  └── CLAUDE.md (TO UPDATE)

/home/coolhand/service_manager.py    # Service orchestration (TO UPDATE)
/etc/caddy/Caddyfile                 # Reverse proxy (TO UPDATE)
/home/coolhand/documentation/API_KEYS.md  # Bearer token (TO UPDATE)
```

---

## Quick Command Reference

```bash
# Project Setup
cd /home/coolhand/shared/mcp

# Service Operations
python3 /home/coolhand/service_manager.py start mcp-orchestrator
python3 /home/coolhand/service_manager.py status
python3 /home/coolhand/service_manager.py stop mcp-orchestrator
python3 /home/coolhand/service_manager.py logs mcp-orchestrator

# Testing
curl http://localhost:5059/health
export TOKEN=$(grep MCP_BEARER_TOKEN /home/coolhand/documentation/API_KEYS.md | cut -d= -f2)
curl -H "Authorization: Bearer $TOKEN" http://localhost:5059/tools

# Configuration
sudo nano /etc/caddy/Caddyfile
nano /home/coolhand/documentation/API_KEYS.md
nano /home/coolhand/service_manager.py

# Verification
lsof -i :5059
sudo systemctl status caddy
curl -k https://dr.eamer.dev/mcp/health
```

---

## FAQ

**Q: Will this break existing MCP services?**
A: No. We're creating a new server on port 5059, leaving existing services untouched.

**Q: Do I need to modify the orchestrator code?**
A: No. We're wrapping existing orchestrators via imports.

**Q: Where does the bearer token go?**
A: In `API_KEYS.md` (gitignored), loaded by startup script.

**Q: What if a workflow takes longer than 10 minutes?**
A: Caddy timeout is 10 minutes. For longer tasks, implement heartbeat/progress streaming in Phase 5.

**Q: Can I scale this to multiple servers?**
A: Yes, Phase 5 includes Redis backend planning.

**Q: What if authentication fails in Claude Desktop?**
A: Check that bearer token in config matches API_KEYS.md, restart Claude Desktop.

---

## Contact & Attribution

**Plan Created**: Claude Code (claude.ai/code)
**Author**: Luke Steuber
**Project**: Dreamwalker MCP Server Deployment
**Status**: ✅ PLANNING COMPLETE

---

## Next Steps

1. **Review** this planning package (you're doing it!)
2. **Approve** the architecture and timeline
3. **Start** with Phase 1 - use dreamwalker-mcp-CHECKLIST.md
4. **Reference** dreamwalker-mcp-deployment-plan.md for detailed code
5. **Test** following the test strategy in the checklist
6. **Deploy** and monitor via service manager

---

**Ready to implement? Pick up the CHECKLIST and get started!**

Version: 1.0
Last Updated: 2026-02-06

# Dreamwalker MCP Deployment - Quick Summary

**Status**: PLANNING ✅
**Effort**: 2-3 days
**Priority**: HIGH
**Port**: 5059
**Route**: `https://dr.eamer.dev/mcp`

---

## The Ask

Deploy the Dreamwalker orchestrator as a production-ready remote MCP server accessible from Claude Desktop via HTTPS, with bearer token authentication.

---

## What's Already Done (80% Complete)

1. **Orchestration framework** exists at `/home/coolhand/shared/orchestration/`
   - DreamCascadeOrchestrator (hierarchical research)
   - DreamSwarmOrchestrator (parallel search)
   - Streaming support built-in

2. **MCP infrastructure** exists at `/home/coolhand/shared/mcp/`
   - `mcp_http_bridge.py` - stdio↔HTTP translator
   - `cursor_mcp_config.json` - Claude Desktop config template
   - Multiple MCP servers (unified_server.py, etc.)

3. **Shared library** at `/home/coolhand/shared/`
   - 12 LLM providers
   - 17 data clients
   - Tool registry system
   - Full async/await support

---

## What Needs to Be Built (3 Files)

### 1. FastMCP HTTP Server (~300-400 lines)
**File**: `/home/coolhand/shared/mcp/http_mcp_server.py`

- Wrap orchestrators with FastMCP HTTP transport
- Implement 7 tools: dream_orchestrate_research, dream_orchestrate_search, dreamwalker_status, dreamwalker_cancel, dreamwalker_patterns, dreamwalker_list_tools, dreamwalker_execute_tool
- Add health endpoint
- Bearer token authentication middleware
- Workflow state management
- Async/streaming-ready

### 2. Startup Script
**File**: `/home/coolhand/shared/mcp/start_mcp_http.sh`

- Load environment variables
- Set PYTHONPATH
- Start http_mcp_server.py on port 5059

### 3. Configuration Updates (Existing Files)

| File | Change | Impact |
|------|--------|--------|
| `/home/coolhand/service_manager.py` | Add mcp-orchestrator service config | Enables `sm start mcp-orchestrator` |
| `/etc/caddy/Caddyfile` | Add `/mcp*` reverse proxy | HTTPS routing to port 5059 |
| `/home/coolhand/documentation/API_KEYS.md` | Add MCP_BEARER_TOKEN | Authentication secret |
| `/home/coolhand/projects/PORT_ALLOCATION.md` | Document port 5059 | Port tracking |
| `/home/coolhand/shared/mcp/requirements.txt` | Add fastmcp, uvicorn, aiohttp | Dependencies |

---

## Architecture Decision

### Chosen: THIN HTTP WRAPPER (Option 3)
✅ Create new FastMCP HTTP server
✅ Reuse existing orchestrators
✅ Keep unified_server.py unchanged
✅ Compatible with Claude Desktop
✅ Minimal code duplication

---

## Key Implementation Details

### Authentication
- Bearer token in Authorization header: `Authorization: Bearer <token>`
- Token stored in `/home/coolhand/documentation/API_KEYS.md` (gitignored)
- Health endpoint accessible without auth (for monitoring)
- Configurable via `MCP_BEARER_TOKEN` env var

### Caddy Configuration
```caddyfile
handle /mcp* {
    reverse_proxy localhost:5059 {
        flush_interval -1
        header_up Authorization {http.request.header.Authorization}
        transport http {
            response_header_timeout 10m
            idle_conn_timeout 10m
        }
    }
}
```

### Tools Exposed
1. `dream_orchestrate_research` - Hierarchical research (Dream Cascade)
2. `dream_orchestrate_search` - Parallel multi-domain search (Dream Swarm)
3. `dreamwalker_status` - Check workflow status
4. `dreamwalker_cancel` - Cancel running workflow
5. `dreamwalker_patterns` - List available patterns
6. `dreamwalker_list_tools` - List registered tools
7. `dreamwalker_execute_tool` - Execute registered tool

---

## Testing Strategy

### Unit Tests
- Each tool function
- Authentication validation
- Health endpoint

### Integration Tests
- End-to-end workflow execution
- Status tracking
- Cancellation

### Manual Testing
```bash
sm start mcp-orchestrator
curl http://localhost:5059/health
curl -H "Authorization: Bearer $TOKEN" https://dr.eamer.dev/mcp/health

# In Claude Desktop
@tools show orchestrator patterns
@tools research quantum computing with Dream Cascade
```

---

## Implementation Sequence

| Phase | Days | Tasks |
|-------|------|-------|
| 1. Server | Day 1 | Create http_mcp_server.py, startup script, update requirements.txt |
| 2. Infrastructure | Day 1-2 | Service manager, bearer token, Caddy config, port allocation |
| 3. Testing | Day 2 | Unit tests, integration tests, manual testing, Claude Desktop |
| 4. Hardening | Day 3 | SSE streaming, monitoring, documentation, failure scenarios |

---

## Success Criteria (10 Items)

- [x] Service starts: `sm start mcp-orchestrator` → running
- [x] Health check: `curl http://localhost:5059/health` → 200 OK
- [x] HTTPS routing: `curl https://dr.eamer.dev/mcp/health` → 200 OK
- [x] Auth enforced: No bearer token → 401 Unauthorized
- [x] Tools discoverable in Claude Desktop
- [x] dream_orchestrate_research works from Claude Desktop
- [x] Status tracking with dreamwalker_status
- [x] Streaming support (optional but recommended)
- [x] Service manager monitoring passes
- [x] No breaking changes to existing MCP services

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| **Auth bypass** | Bearer token required; rotate periodically; no hardcoded tokens |
| **Long-running timeouts** | Caddy timeout = 10 minutes; implement heartbeat streaming |
| **Memory leaks** | Workflow cleanup job; max active workflows limit |
| **Performance degradation** | Rate limiting; async execution; max concurrent workflows |
| **Claude Desktop incompatibility** | Use standard FastMCP HTTP spec; test with actual client |

---

## Port Assignment

**Allocated**: Port 5059 (in 5050-5059 range)

**Current 5050-5059 Usage**:
- 5050: Skymarshal
- 5051: Karate Dramatizer
- 5052: Firehose Dashboard
- 5053: Pinpoint Geography
- 5054: Alt Text Generator
- 5055: Story Illustrator
- 5056-5058: Unknown/available
- **5059: DREAMWALKER MCP** ← NEW

---

## Configuration Examples

### Service Manager Entry
```python
'mcp-orchestrator': {
    'name': 'Dreamwalker MCP Server',
    'script': '/home/coolhand/shared/mcp/start_mcp_http.sh',
    'working_dir': '/home/coolhand/shared/mcp',
    'port': 5059,
    'health_endpoint': 'http://localhost:5059/health',
    'start_timeout': 15,
    'description': 'Remote MCP server for Dreamwalker orchestrator'
}
```

### Caddy Route
```caddyfile
handle /mcp* {
    reverse_proxy localhost:5059 {
        flush_interval -1
        header_up Authorization {http.request.header.Authorization}
        transport http {
            response_header_timeout 10m
            idle_conn_timeout 10m
        }
    }
}
```

### Cursor MCP Config
```json
{
  "mcpServers": {
    "dreamwalker": {
      "command": "python3",
      "args": [
        "/home/coolhand/shared/mcp/mcp_http_bridge.py",
        "--url",
        "https://dr.eamer.dev/mcp"
      ],
      "env": {
        "MCP_BEARER_TOKEN": "your-token-here"
      }
    }
  }
}
```

---

## Dependencies to Add

```txt
# In /home/coolhand/shared/mcp/requirements.txt
fastmcp>=0.1.0
uvicorn>=0.24.0
aiohttp>=3.8.0
pydantic>=2.0
```

---

## Key Files to Create/Modify

| File | Type | Impact |
|------|------|--------|
| `/home/coolhand/shared/mcp/http_mcp_server.py` | CREATE | MCP HTTP server |
| `/home/coolhand/shared/mcp/start_mcp_http.sh` | CREATE | Startup script |
| `/home/coolhand/service_manager.py` | MODIFY | Add service config |
| `/etc/caddy/Caddyfile` | MODIFY | Add reverse proxy |
| `/home/coolhand/documentation/API_KEYS.md` | MODIFY | Store bearer token |
| `/home/coolhand/projects/PORT_ALLOCATION.md` | MODIFY | Document port 5059 |
| `/home/coolhand/shared/mcp/requirements.txt` | MODIFY | Add dependencies |

---

## Rollback Plan

If something breaks:

1. **Service won't start**: Revert service_manager.py, restore Caddyfile
2. **Caddy errors**: `git checkout /etc/caddy/Caddyfile`, `sudo systemctl reload caddy`
3. **Auth issues**: Update bearer token or set `MCP_BEARER_TOKEN=disabled`
4. **Claude Desktop fails**: Update cursor config to use local stdio server

---

## Future Enhancements (Post-MVP)

1. SSE streaming for real-time progress
2. Redis backend for multi-instance deployment
3. Webhook notifications on completion
4. Rate limiting per token
5. Audit logging for compliance
6. Workflow history archival
7. Custom tool registry
8. Load balancing
9. Usage analytics
10. Cost tracking integration

---

## Why This Design

**Problem**: Dreamwalker is a powerful orchestrator but only accessible via stdio locally. We want Claude Desktop users to access it remotely.

**Solution**: Create thin HTTP wrapper using FastMCP (new MCP HTTP standard) that:
- Delegates to existing orchestrators (no duplication)
- Runs behind Caddy HTTPS reverse proxy
- Uses bearer token auth
- Integrates with service manager
- Supports streaming for long workflows
- Compatible with Claude Desktop's MCP HTTP transport

**Why not modify existing servers?**
- Keep unified_server.py as-is for internal services
- Avoid breaking changes to existing functionality
- Cleaner separation of concerns
- Easier to test and deploy independently

**Why FastMCP?**
- Modern HTTP MCP transport spec
- Native async support
- Streaming-ready
- Claude Desktop compatible
- Actively maintained

---

**Full detailed plan**: See `/home/coolhand/geepers/hive/dreamwalker-mcp-deployment-plan.md`

**Ready for implementation**: YES ✅

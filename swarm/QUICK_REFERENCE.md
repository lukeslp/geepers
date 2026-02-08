# Dreamwalker MCP Server - Quick Reference

## Current Status

✅ **Production MCP Server Running**: Port 5060
❌ **FastMCP NOT Used**: Production uses Flask + HTTP
⚠️ **FastMCP Experimental Only**: Found only in `/admin/Claude-MCP-tools/`

---

## Entry Points

| Component | Location | Type | Status |
|-----------|----------|------|--------|
| Main Server | `/home/coolhand/shared/mcp/app.py` | Flask app | Running |
| Tool Definitions | `/home/coolhand/shared/mcp/unified_server.py` | Python class | Active |
| Startup Script | `/home/coolhand/shared/mcp/start.sh` | Bash | Used |
| Service Manager | `/home/coolhand/service_manager.py` | Python config | Lines 461-475 |

---

## 7 Core Tools

```
1. dream_orchestrate_research        POST /tools/orchestrate_research
2. dream_orchestrate_search          POST /tools/orchestrate_search
3. dreamwalker_status                POST /tools/get_orchestration_status
4. dreamwalker_cancel                POST /tools/cancel_orchestration
5. dreamwalker_patterns              POST /tools/list_orchestrator_patterns
6. dreamwalker_list_tools            POST /tools/list_registered_tools
7. dreamwalker_execute_tool          POST /tools/execute_registered_tool
```

---

## Key Files

### Core Implementation (160+ KB total)
```
/home/coolhand/shared/mcp/
├── app.py                    (22 KB)  Entry point - Flask routes
├── unified_server.py         (51 KB)  Tool definitions - UnifiedMCPServer class
├── streaming.py              (14 KB)  SSE infrastructure
├── tool_registry.py          (15 KB)  Tool discovery
├── background_loop.py        (4 KB)   Async executor
├── streaming_endpoint.py      (11 KB)  SSE routes
└── start.sh                         Gunicorn startup
```

### Supporting Files
```
├── requirements.txt          Flask, gunicorn, gevent
├── providers_server.py       LLM tools
├── data_server.py            Data fetching (arXiv, Census, etc.)
├── cache_server.py           Redis caching
├── utility_server.py         Utilities
├── config_server.py          Configuration
└── __init__.py               Module exports
```

---

## Startup Process

```
1. sm start mcp-server
   ↓
2. Executes: /home/coolhand/shared/mcp/start.sh
   ↓
3. Starts: gunicorn -w 1 -k gevent -b 127.0.0.1:5060 app:app
   ↓
4. Flask initializes:
   - Creates UnifiedMCPServer
   - Loads state_backup.json if exists
   - Registers streaming routes
   - Sets up signal handlers
   ↓
5. Server ready at http://localhost:5060
```

---

## Health Check

```bash
curl http://localhost:5060/health

# Response:
{
  "status": "healthy",
  "service": "dreamwalker-mcp",
  "version": "2.0.0",
  "servers": {
    "orchestration": "active",
    "data_fetching": "active",
    "cache": "active",
    "utilities": "active"
  },
  "tool_count": 53,
  "active_streams": 0,
  "registered_webhooks": 0
}
```

---

## Tool Invocation Example

### Start Research Workflow

```bash
curl -X POST http://localhost:5060/tools/orchestrate_research \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Research quantum computing applications in cryptography",
    "belter_count": 3,
    "drummer_count": 2,
    "camina_count": 1,
    "provider": "xai",
    "model": "grok-3",
    "stream": true
  }'

# Response:
{
  "success": true,
  "task_id": "workflow-abc123",
  "status": "running",
  "stream_url": "/stream/workflow-abc123",
  "message": "Workflow started successfully"
}
```

### Subscribe to Streaming Updates

```bash
curl -N http://localhost:5060/stream/workflow-abc123

# Events:
event: task_started
data: {"task_id": "workflow-abc123", "timestamp": "..."}

event: subtask_completed
data: {"subtask_id": "task-1", "progress": 33}

event: task_completed
data: {"task_id": "workflow-abc123", "result": {...}}
```

### Check Status

```bash
curl -X POST http://localhost:5060/tools/get_orchestration_status \
  -H "Content-Type: application/json" \
  -d '{"task_id": "workflow-abc123"}'

# Response:
{
  "task_id": "workflow-abc123",
  "status": "running",
  "progress": 45,
  "started_at": "2026-02-06T12:00:00Z",
  "current_stage": "synthesis"
}
```

---

## State Persistence

**Location**: `/home/coolhand/shared/mcp/state_backup.json`

```json
{
  "active_workflows": {
    "workflow-abc123": {
      "task_id": "workflow-abc123",
      "status": "completed",
      "created_at": "2026-02-06T12:00:00Z",
      "config": {...}
    }
  },
  "completed_workflows": {
    "workflow-xyz789": {...}
  }
}
```

---

## Service Configuration

```python
# In /home/coolhand/service_manager.py (lines 461-475)

'mcp-server': {
    'name': 'MCP Orchestrator Server',
    'script': '/home/coolhand/shared/mcp/start.sh',
    'working_dir': '/home/coolhand/shared/mcp',
    'port': 5060,
    'health_endpoint': 'http://localhost:5060/health',
    'start_timeout': 20,
    'description': 'Unified MCP server for orchestrator agents with SSE streaming',
    'env': {
        'PORT': '5060',
        'WORKERS': '1',
        'TIMEOUT': '300',
        'SKIP_PIP_INSTALL': '1'
    }
}
```

---

## Dependencies

```
Flask >= 3.0.0
Flask-CORS >= 4.0.0
Gunicorn >= 21.0.0
gevent >= 24.0.0         (for async greenlet support)
aiohttp >= 3.9.0
reportlab >= 4.0.0       (document generation)
python-docx >= 1.0.0     (document generation)
-e /home/coolhand/shared (shared library, editable)
```

---

## Common Operations

### Start/Stop Service
```bash
sm start mcp-server      # Start
sm stop mcp-server       # Stop
sm restart mcp-server    # Restart
sm status                # Status of all services
sm logs mcp-server       # View logs
```

### View Streaming Stats
```bash
curl http://localhost:5060/stats

# Response:
{
  "active_streams": 0,
  "total_streams_created": 42,
  "registered_webhooks": 3,
  "cleanup_cycles": 128
}
```

### List Available Tools
```bash
curl http://localhost:5060/tools

# Returns: name, description, inputSchema for all 53 tools
```

---

## Architecture Overview

```
HTTP Request
    ↓
Flask Route (app.py)
    ↓
UnifiedMCPServer.<tool_method>()
    ↓
Background Task Executor
    ↓
DreamCascadeOrchestrator / DreamSwarmOrchestrator
    ↓
LLM Providers + Data Sources
    ↓
SSE Event → StreamingBridge → Client
Webhook → WebhookManager → External Service
Result → WorkflowState → state_backup.json
```

---

## FastMCP References (Experimental Only)

**Locations** (NOT used in production):
- `/admin/Claude-MCP-tools/claude-code-integration-mcp/enhanced_server.py`
- `/admin/Claude-MCP-tools/claude-code-integration-mcp/minimal_server.py`
- `/admin/Claude-MCP-tools/servers/agenticseek-mcp/server_fastmcp.py`

**Status**: Test/experimental code only
**Integration**: None (production uses Flask)

---

## Monitoring

### Health Endpoint
```
GET /health → Full service status
```

### Logs
```bash
sm logs mcp-server

# Or directly:
tail -f /home/coolhand/.service_manager/logs/mcp-server.log
```

### Streaming Activity
```bash
curl http://localhost:5060/stats
```

---

## Known Limits

| Limit | Value | Location |
|-------|-------|----------|
| Max active workflows | 50 | unified_server.py:82 |
| Max concurrent streams | 100 | streaming.py:46 |
| Stream TTL | 3600s (1hr) | streaming.py:48 |
| Request timeout | 300s (5min) | start.sh:TIMEOUT |
| Completed workflows retained | 100 | unified_server.py:89 |

---

## Debugging

### Check if Server Running
```bash
curl http://localhost:5060/health
```

### View Service Logs
```bash
sm logs mcp-server
```

### Verify Port
```bash
lsof -i :5060
```

### Manual Startup (for debugging)
```bash
cd /home/coolhand/shared/mcp
source venv/bin/activate
python app.py     # Runs Flask dev server on 5000
# or
gunicorn -w 1 -k gevent -b 127.0.0.1:5060 app:app
```

---

## Version Info

- **Service**: Dreamwalker MCP Server 2.0.0
- **Framework**: Flask 3.0+
- **Worker Type**: Gunicorn + Gevent
- **Python Version**: 3.9+
- **Implementation Date**: December 2025+

---

## For More Details

See:
- `/home/coolhand/geepers/swarm/search-log.md` - Complete findings
- `/home/coolhand/geepers/swarm/RESEARCH_SUMMARY.md` - Executive summary
- `/home/coolhand/shared/mcp/CLAUDE.md` - Developer guide

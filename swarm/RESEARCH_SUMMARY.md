# Dreamwalker MCP Server Research Summary

**Research Date**: 2026-02-06
**Research Type**: Code architecture analysis (research only, no edits)
**Searcher**: Claude Code

---

## Quick Answer: FastMCP Status

**Is FastMCP currently used in the Dreamwalker MCP server?**
**No.** The production Dreamwalker orchestrator MCP server does NOT use FastMCP. It uses Flask + Gunicorn with HTTP/REST transport.

FastMCP appears only in experimental/test code in `/home/coolhand/admin/Claude-MCP-tools/`.

---

## Executive Summary

### Current Implementation (Production)

| Aspect | Detail |
|--------|--------|
| **Framework** | Flask 3.0+ with Gunicorn |
| **Transport** | HTTP/REST (NOT JSON-RPC/stdio) |
| **Port** | 5060 |
| **Entry Point** | `/home/coolhand/shared/mcp/app.py` |
| **Service** | `mcp-server` (managed by service_manager.py) |
| **Startup** | Gunicorn with gevent async workers |
| **Tools** | 7 core orchestrator tools + 46 utility/data tools |
| **Streaming** | Server-Sent Events (SSE) via `/stream/{task_id}` |
| **State** | Persisted in `/home/coolhand/shared/mcp/state_backup.json` |

### Core Tools (7)

All HTTP POST endpoints with JSON request bodies:

1. **dream_orchestrate_research** - Execute Dream Cascade hierarchical research
2. **dream_orchestrate_search** - Execute Dream Swarm multi-agent search
3. **dreamwalker_status** - Check workflow status
4. **dreamwalker_cancel** - Cancel running workflow
5. **dreamwalker_patterns** - List available orchestrator patterns
6. **dreamwalker_list_tools** - List registered tools
7. **dreamwalker_execute_tool** - Execute a registered tool

### Architecture Layers

```
Flask HTTP Routes (app.py)
    ↓
UnifiedMCPServer class (unified_server.py)
    ├─ WorkflowState (manage active orchestrations)
    ├─ Tool definitions (7 tools exposed as methods)
    └─ ToolRegistry integration
    ↓
Infrastructure Services
    ├─ StreamingBridge (SSE event routing)
    ├─ WebhookManager (async webhooks)
    ├─ BackgroundLoop (persistent async execution)
    └─ State persistence
    ↓
Orchestration Framework
    ├─ DreamCascadeOrchestrator
    └─ DreamSwarmOrchestrator
```

---

## File Map

### Main Implementation (7 files, 160+ KB)

```
/home/coolhand/shared/mcp/
├── app.py                      (22 KB) - Flask app & HTTP routes
├── unified_server.py           (51 KB) - UnifiedMCPServer class + tool definitions
├── streaming.py                (14 KB) - SSE bridge & webhook manager
├── tool_registry.py            (15 KB) - Tool discovery system
├── background_loop.py          (4 KB)  - Async task executor
├── streaming_endpoint.py        (11 KB) - SSE Flask route handlers
└── start.sh                    (executable) - Gunicorn startup script
```

### Supporting Modules (all in `/home/coolhand/shared/mcp/`)

- `providers_server.py` - LLM provider tools
- `data_server.py` - Data fetching tools (Census, arXiv, etc.)
- `cache_server.py` - Redis caching tools
- `utility_server.py` - Utility tools
- `config_server.py` - Configuration tools
- `requirements.txt` - Flask, gunicorn, gevent dependencies
- `__init__.py` - Module exports

---

## Tool Definitions (Complete List)

### Orchestrator Tools (7 total)

**Location**: `unified_server.py` lines 1139-1245 (tool manifest generation)

```python
get_tools_manifest() returns:
[
  {
    "name": "dream_orchestrate_research",
    "description": "Execute Dream Cascade hierarchical research workflow...",
    "inputSchema": {
      "type": "object",
      "properties": {
        "task": {"type": "string"},
        "belter_count": {"type": "integer", "default": 3},
        "drummer_count": {"type": "integer", "default": 2},
        "camina_count": {"type": "integer", "default": 1},
        "provider": {"type": "string", "default": "xai"},
        "model": {"type": "string"},
        "stream": {"type": "boolean", "default": true},
        "webhook_url": {"type": "string"}
      }
    }
  },
  // ... 6 more tools
]
```

### HTTP Endpoint Mapping

```
Tool Method                         → Flask Route
────────────────────────────────────────────────────────────
tool_dream_orchestrate_research()   → POST /tools/orchestrate_research
tool_dream_orchestrate_search()     → POST /tools/orchestrate_search
tool_dream_get_orchestration_status() → POST /tools/get_orchestration_status
tool_dream_cancel_orchestration()   → POST /tools/cancel_orchestration
tool_dream_list_orchestrator_patterns() → POST /tools/list_orchestrator_patterns
tool_dream_list_registered_tools()  → POST /tools/list_registered_tools
tool_dream_execute_registered_tool() → POST /tools/execute_registered_tool
```

---

## Streaming Architecture

### SSE Setup

```
GET /stream/{task_id}
├─ Opens persistent HTTP connection
├─ Pushes server-sent events as task progresses
└─ Connection closes when task completes or times out
```

### Event Types

- `task_started` - Workflow initialized
- `subtask_created` - New subtask created
- `subtask_completed` - Subtask finished
- `synthesis_started` - Results being synthesized
- `task_completed` - Workflow finished
- `task_error` - Workflow failed
- Custom events from specific orchestrators

### Infrastructure

```python
class StreamingBridge:
    - 100 concurrent streams max
    - 1 hour TTL per stream
    - Async queue-based event distribution
    - Automatic cleanup of stale streams

class WebhookManager:
    - Async webhook delivery
    - Retry logic (3 retries)
    - HMAC-SHA256 payload signing
    - Configurable request timeout (10s)
```

---

## State Management

### WorkflowState Class

Tracks running and completed orchestrations:

```python
class WorkflowState:
    MAX_ACTIVE_WORKFLOWS = 50  # Prevent DoS

    active_workflows: Dict[task_id -> info]
    completed_workflows: Dict[task_id -> result]
    active_tasks: Dict[task_id -> asyncio.Task]

    # Automatically retains last 100 completed workflows
    max_completed_retention = 100
```

### Persistence

- **File**: `/home/coolhand/shared/mcp/state_backup.json`
- **Trigger**: On server shutdown (signal handlers: SIGTERM, SIGINT)
- **Restoration**: On server startup if backup exists
- **Data**: task_id, status, config, created_at, agent_results

---

## Service Configuration

### service_manager.py Entry

```python
'mcp-server': {
    'name': 'MCP Orchestrator Server',
    'script': '/home/coolhand/shared/mcp/start.sh',
    'working_dir': '/home/coolhand/shared/mcp',
    'port': 5060,
    'health_endpoint': 'http://localhost:5060/health',
    'start_timeout': 20,
    'env': {
        'PORT': '5060',
        'WORKERS': '1',
        'TIMEOUT': '300',      # Long timeout for orchestrations
        'SKIP_PIP_INSTALL': '1'
    }
}
```

### Startup Command

```bash
gunicorn \
    -w 1 \
    -k gevent \
    -b 127.0.0.1:5060 \
    --timeout 300 \
    app:app
```

---

## FastMCP References (Not Used in Production)

### Where FastMCP Appears

**Directory**: `/home/coolhand/admin/Claude-MCP-tools/`

```
admin/Claude-MCP-tools/
├── claude-code-integration-mcp/
│   ├── enhanced_server.py          (imports FastMCP)
│   ├── minimal_server.py           (imports FastMCP with fallback)
│   └── test_server_startup.py      (tests FastMCP import)
│
└── servers/agenticseek-mcp/
    └── server_fastmcp.py           (experimental)
```

**Status**: These are experimental/test servers, NOT integrated into production.

### FastMCP Import Pattern (from the experimental code)

```python
from fastmcp import FastMCP

mcp = FastMCP("Server Name")

@mcp.tool()
def my_tool(param: str) -> str:
    """Tool description"""
    return result

mcp.run(transport="stdio")
```

---

## Key Design Decisions

### Why Flask + HTTP Instead of FastMCP/stdio?

1. **Ease of Integration**: HTTP is easier to integrate with web clients
2. **Existing Infrastructure**: Flask is well-established at port 5060
3. **SSE Streaming**: SSE is well-suited for progress updates
4. **State Persistence**: Easier with HTTP-based service
5. **Webhook Support**: Native HTTP webhook delivery

### Trade-offs

| Aspect | Flask/HTTP | FastMCP/stdio |
|--------|-----------|---------------|
| Claude Desktop native | ❌ Not compatible | ✅ Native |
| Web client access | ✅ Easy | ⚠️ Needs wrapper |
| Streaming support | ✅ SSE | ❌ Not built-in |
| State persistence | ✅ Easy | ❌ Needs implementation |
| Webhook support | ✅ Built-in | ❌ Not built-in |
| Current deployment | ✅ Active | ❌ Experimental only |

---

## Integration Points (If FastMCP Migration Needed)

### 1. Tool Definitions
- Current: Methods in UnifiedMCPServer class
- Target: FastMCP `@mcp.tool()` decorators
- Effort: Low (straightforward conversion)

### 2. Streaming Support
- Current: SSE via Flask routes
- Target: Return streaming results in tool responses
- Effort: Medium (different paradigm)

### 3. State Management
- Current: WorkflowState class + JSON file
- Target: Can be reused as-is
- Effort: None (compatible)

### 4. Orchestration Framework
- Current: DreamCascadeOrchestrator, DreamSwarmOrchestrator
- Target: No changes needed (framework-agnostic)
- Effort: None

### 5. Service Manager
- Current: Gunicorn + Flask
- Target: FastMCP stdio process
- Effort: Low (script change)

---

## Recommendations

### For Understanding Current System
1. Read `/home/coolhand/shared/mcp/app.py` (entry point)
2. Read `/home/coolhand/shared/mcp/unified_server.py` (tool definitions)
3. Check `/home/coolhand/shared/mcp/streaming.py` (SSE infrastructure)

### For Implementation of New Features
- Add new tools in `UnifiedMCPServer` class
- Register with tool registry via decorators or method registration
- Leverage existing StreamingBridge for progress updates

### If FastMCP Migration Needed
1. Create new FastMCP server using `@mcp.tool()` decorators
2. Reuse WorkflowState and orchestration classes as-is
3. Adapt streaming for FastMCP message format
4. Update service_manager.py to run FastMCP stdio process
5. Maintain backward compatibility with HTTP interface during transition

---

## Notes & Observations

### Strengths of Current Design
- ✅ Production-grade with state persistence
- ✅ Comprehensive tool set (53 tools total)
- ✅ Robust streaming and webhook infrastructure
- ✅ Clear separation of concerns
- ✅ Well-documented code with detailed docstrings
- ✅ Handles concurrent workflows safely (50 max active)

### Areas for Enhancement
- Monitoring/metrics dashboard (currently only stats endpoint)
- Tool-level caching beyond response caching
- Advanced retry logic per tool
- Cost optimization per workflow
- Resource limits per workflow type

### Current Limitations
- ❌ Not compatible with Claude Desktop's stdio MCP protocol
- ⚠️ Single-worker gunicorn (could scale horizontally with load balancer)
- ⚠️ State only in memory + single backup file (not distributed)

---

## Search Log Location

Detailed findings: `/home/coolhand/geepers/swarm/search-log.md`

This document contains:
- Complete tool definitions
- HTTP endpoint mapping (53 endpoints)
- Detailed dependency analysis
- File-by-file examination results
- Architecture diagrams
- Integration point analysis

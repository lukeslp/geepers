# Dreamwalker MCP Server Research - Search Log

**Date**: 2026-02-06
**Searcher**: Claude Code (Searcher Agent)
**Task**: Understand existing dreamwalker MCP implementation and FastMCP usage

## Search Strategy

Searched for:
1. FastMCP usage across codebase
2. MCP server implementations and structure
3. Tool definitions and registry
4. Service manager configuration
5. Current Flask-based MCP server entry points
6. Streaming infrastructure
7. Configuration files

---

## KEY FINDINGS

### 1. CURRENT MCP SERVER ARCHITECTURE

**Location**: `/home/coolhand/shared/mcp/`

#### Entry Points:
- **Primary**: `app.py` (Flask application) - **NOT using FastMCP**
- **Unified Server**: `unified_server.py` (tool definitions, orchestrator integration)
- **Service Manager**: Runs via `/home/coolhand/shared/mcp/start.sh`
- **Port**: 5060 (configured in service_manager.py)

#### Current Implementation (Flask-based)
The MCP server is currently implemented using Flask HTTP with the following architecture:

```
/home/coolhand/shared/mcp/
├── app.py                      # Flask app entry point (22KB, 673 lines)
├── unified_server.py           # UnifiedMCPServer class (51KB, 1600+ lines)
├── streaming.py                # SSE/Webhook infrastructure
├── tool_registry.py            # Tool discovery and execution
├── streaming_endpoint.py        # SSE endpoints
├── background_loop.py          # Async task runner
├── start.sh                    # Startup script (gunicorn with gevent)
├── requirements.txt            # Dependencies
├── providers_server.py         # LLM provider tools
├── data_server.py              # Data fetching tools
├── cache_server.py             # Redis caching tools
├── utility_server.py           # Utility tools
└── config_server.py            # Configuration tools
```

**Transport Method**: HTTP/REST (not stdio/JSON-RPC)
**Framework**: Flask (web framework)
**Worker Type**: Gunicorn with gevent greenlet-based concurrency

---

### 2. CURRENT MCP TOOLS EXPOSED

The `unified_server.py` file defines 7 core orchestrator tools available through HTTP endpoints:

#### Orchestrator Tools (Tools):

```python
# In unified_server.py, class UnifiedMCPServer

1. dream_orchestrate_research
   - Signature: async def tool_dream_orchestrate_research(arguments: Dict[str, Any])
   - Task: Execute Dream Cascade hierarchical research workflow
   - Parameters:
     * task (string, required): Research task description
     * belter_count (int): Tier 1 agents (default: 3)
     * drummer_count (int): Tier 2 agents (default: 2)
     * camina_count (int): Tier 3 agents (default: 1)
     * provider (string): LLM provider (default: 'xai')
     * model (string): Model to use
     * stream (bool): Enable SSE streaming
     * webhook_url (string): Optional webhook URL
   - Line: 581 in unified_server.py

2. dream_orchestrate_search
   - Signature: async def tool_dream_orchestrate_search(arguments: Dict[str, Any])
   - Task: Execute Dream Swarm multi-agent search workflow
   - Parameters: Similar to research but for search (task, num_agents, domains, etc.)
   - Line: 677 in unified_server.py

3. dream_get_orchestration_status / dreamwalker_status
   - Check workflow status by task_id
   - Returns: status, progress, agent results, current stage

4. dream_cancel_orchestration / dreamwalker_cancel
   - Cancel a running orchestration
   - Parameters: task_id

5. dream_list_orchestrator_patterns / dreamwalker_patterns
   - List available orchestrator patterns
   - Returns: List of pattern metadata (dream_cascade, dream_swarm, etc.)

6. dream_list_registered_tools / dreamwalker_list_tools
   - List tools registered in tool registry
   - Parameters: Optional category filter
   - Returns: Tool definitions with schemas

7. dream_execute_registered_tool / dreamwalker_execute_tool
   - Execute a registered tool from the registry
   - Parameters: tool_name, tool_args

```

**Tool Manifest Export**:
- Method: `get_tools_manifest()` returns list of tool definitions
- Location: Lines 1139-1245 in unified_server.py
- Format: MCP tool schema with name, description, inputSchema

---

### 3. HTTP ENDPOINT MAPPING (Flask Routes in app.py)

**Tool Execution Endpoints** (POST with JSON body):

```
POST /tools/orchestrate_research         → Calls mcp_server.tool_dream_orchestrate_research()
POST /tools/orchestrate_search           → Calls mcp_server.tool_dream_orchestrate_search()
POST /tools/get_orchestration_status     → Calls mcp_server.tool_dream_get_orchestration_status()
POST /tools/cancel_orchestration         → Calls mcp_server.tool_dream_cancel_orchestration()
POST /tools/list_orchestrator_patterns   → Calls mcp_server.tool_dream_list_orchestrator_patterns()
POST /tools/list_registered_tools        → Calls mcp_server.tool_dream_list_registered_tools()
POST /tools/execute_registered_tool      → Calls mcp_server.tool_dream_execute_registered_tool()
```

**Discovery Endpoints** (GET):

```
GET  /              → Server info (name, version, endpoints)
GET  /health        → Health check with tool counts
GET  /tools         → List all available tools (from 4 servers)
GET  /resources     → List available resources
GET  /stream/{task_id}  → SSE stream for workflow progress (GET with streaming response)
```

**Webhook Endpoints** (POST):

```
POST /webhook/register    → Register webhook for task notifications
POST /webhook/unregister  → Unregister webhook
GET  /stats               → Streaming bridge statistics
```

**Other Tool Endpoints** (46 additional endpoints for data/cache/utility):
- Census, arXiv, Semantic Scholar, Wayback Machine endpoints
- Cache operations (get, set, delete, increment, expire, list_keys)
- Utility tools (parse_document, multi_provider_search, extract_citations)

---

### 4. FASTMCP USAGE IN CODEBASE

**Status**: FastMCP IS NOT currently used in the production Dreamwalker implementation

**Locations where FastMCP appears** (all in `/home/coolhand/admin/Claude-MCP-tools/`):

1. `/admin/Claude-MCP-tools/claude-code-integration-mcp/enhanced_server.py`
   - FastMCP import: `from fastmcp import FastMCP`
   - Server creation: `mcp = FastMCP("Enhanced Claude Code Integration")`
   - Status: **Experimental/Test server only**

2. `/admin/Claude-MCP-tools/claude-code-integration-mcp/minimal_server.py`
   - FastMCP import with fallback handling
   - Status: **Diagnostic/Testing mode**

3. `/admin/Claude-MCP-tools/servers/agenticseek-mcp/server_fastmcp.py`
   - Status: **Test/experimental**

**Production Status**:
- The Dreamwalker orchestrator MCP server does NOT use FastMCP
- It uses Flask with HTTP/REST transport, not JSON-RPC/stdio
- These FastMCP examples are in the `admin/Claude-MCP-tools` archive for reference only

---

### 5. STREAMING INFRASTRUCTURE (SSE Bridge)

**File**: `/home/coolhand/shared/mcp/streaming.py` (14KB)

**Components**:

```python
class StreamingBridge:
    """Manages concurrent SSE streams for multiple orchestrations"""
    - max_streams: 100 concurrent streams
    - stream_ttl: 3600 seconds (1 hour)
    - active_streams: Dict[task_id -> asyncio.Queue]
    - create_stream(task_id) -> asyncio.Queue
    - send_event(task_id, event_type, data)
    - subscribe(task_id) -> AsyncIterator[event]
    - cleanup_old_streams()

class WebhookManager:
    """Async webhook delivery with retry logic"""
    - max_retries: 3
    - retry_delay: 1.0 seconds
    - request_timeout: 10 seconds
    - deliver_webhook_async(url, payload, headers, metadata)
    - sign_payload(payload, secret) -> HMAC-SHA256 signature

# Global singletons
get_streaming_bridge() -> StreamingBridge
get_webhook_manager() -> WebhookManager
```

**SSE Event Flow**:
1. Orchestrator workflow starts, registers stream: `bridge.register_stream(task_id)`
2. Orchestrator sends progress events: `bridge.send_event(task_id, event_type, data)`
3. Client receives via SSE: `curl -N http://localhost:5060/stream/{task_id}`
4. Events include: task_started, subtask_created, subtask_completed, synthesis_started, task_completed

---

### 6. TOOL REGISTRY SYSTEM

**File**: `/home/coolhand/shared/mcp/tool_registry.py` (15KB)

**Architecture**:

```python
@dataclass
class ToolParameter:
    name: str
    type: str              # string, integer, number, boolean, array, object
    description: str
    required: bool
    default: Optional[Any]
    enum: Optional[List]
    items: Optional[Dict]  # For arrays
    properties: Optional[Dict]  # For objects

@dataclass
class ToolDefinition:
    name: str
    description: str
    function: Callable
    parameters: Dict[str, ToolParameter]
    category: str          # data, utility, cache, orchestration
    metadata: Dict

class ToolRegistry:
    - register_tool(name, schema, handler, module_name)
    - get_all_tools() -> List[ToolDefinition]
    - get_tools_by_category(category) -> List[ToolDefinition]
    - call_tool(tool_name, arguments) -> Result
    - unregister_tool(name)

# Global singleton
get_tool_registry() -> ToolRegistry
```

**Tool Categories**:
- `orchestration`: Dream Cascade, Dream Swarm, status, cancel, patterns
- `data`: arXiv, Census, Semantic Scholar, Wayback, Wikipedia
- `cache`: Redis operations (get, set, delete, increment)
- `utility`: Document parsing, multi-search, citations

---

### 7. SERVICE MANAGER CONFIGURATION

**File**: `/home/coolhand/service_manager.py`

**MCP-Server Service Entry** (lines 461-475):

```python
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
},

'dreamwalker': {
    'name': 'Dreamwalker Control Panel',
    'script': '/home/coolhand/shared/web/dreamwalker/server.py',
    'working_dir': '/home/coolhand/shared',
    'port': 5080,
    # ... (separate UI service)
}
```

**Startup Command** (from start.sh):

```bash
exec gunicorn \
    -w "$WORKERS" \
    -k gevent \
    -b "127.0.0.1:$PORT" \
    --timeout "$TIMEOUT" \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    app:app
```

---

### 8. WORKFLOW STATE MANAGEMENT

**File**: `/home/coolhand/shared/mcp/unified_server.py` (class WorkflowState)

**State Persistence**:

```python
class WorkflowState:
    MAX_ACTIVE_WORKFLOWS = 50  # Prevent unbounded growth
    active_workflows: Dict[task_id -> workflow_info]
    completed_workflows: Dict[task_id -> OrchestratorResult]
    active_tasks: Dict[task_id -> asyncio.Task]
    max_completed_retention = 100

    # Methods:
    create_workflow(task_id, orchestrator_type, task, config)
    update_workflow_status(task_id, status, error=None)
    get_workflow(task_id) -> workflow_info
    cleanup_completed(max_retain=100)
    serialize_state() -> dict
    load_state(state_dict)
```

**State Backup**:
- File: `/home/coolhand/shared/mcp/state_backup.json`
- Saved on shutdown via `save_state_on_shutdown()` handler
- Restored on startup if backup exists
- Tracks: task_id, status, created_at, config, agent results

---

### 9. DEPENDENCIES

**File**: `/home/coolhand/shared/mcp/requirements.txt`

```
# Core dependencies
flask>=3.0.0
flask-cors>=4.0.0
gunicorn>=21.0.0

# Async support
aiohttp>=3.9.0
gevent>=24.0.0      # Greenlet-based async (for Flask workers)

# Document generation
reportlab>=4.0.0
python-docx>=1.0.0

# Shared library (editable install)
-e /home/coolhand/shared
```

**No FastMCP dependency** - uses standard Flask instead

---

### 10. CONFIGURATION FILES

**MCP Configuration** (if it exists):

Searched for MCP config in:
- `~/.claude/settings.json` → No MCP-specific config (general Claude settings)
- `/home/coolhand/shared/mcp/cursor_mcp_config.json` → Found in legacy storage

**Legacy Storage**:
- `/home/coolhand/.storage/legacy-repos/dreamwalker-mcp/dreamwalker_mcp/mcp/cursor_mcp_config.json`
- This appears to be from previous iteration

---

## ARCHITECTURE SUMMARY

### Current Stack (Production - NOT using FastMCP)

```
┌─────────────────────────────────────────────────────────┐
│  Dreamwalker MCP Server (Port 5060)                     │
│  Framework: Flask + Gunicorn + Gevent                   │
│  Transport: HTTP/REST (not JSON-RPC/stdio)              │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Flask Routes (app.py)                           │   │
│  │  ├─ GET /health, /tools, /resources              │   │
│  │  ├─ POST /tools/* (7 orchestrator tools)         │   │
│  │  ├─ GET /stream/{task_id} (SSE)                  │   │
│  │  └─ POST /webhook/* (webhook management)         │   │
│  └──────────────────────────────────────────────────┘   │
│                          ↓                                │
│  ┌──────────────────────────────────────────────────┐   │
│  │  UnifiedMCPServer (unified_server.py)            │   │
│  │  ├─ WorkflowState (manage active orchestrations) │   │
│  │  ├─ Tool definitions (7 orchestrator tools)      │   │
│  │  ├─ ToolRegistry (dynamic tool discovery)        │   │
│  │  └─ Integration with orchestration framework     │   │
│  └──────────────────────────────────────────────────┘   │
│                          ↓                                │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Infrastructure                                   │   │
│  │  ├─ StreamingBridge (SSE event routing)          │   │
│  │  ├─ WebhookManager (async webhook delivery)      │   │
│  │  ├─ BackgroundLoop (persistent async executor)   │   │
│  │  └─ State persistence (state_backup.json)        │   │
│  └──────────────────────────────────────────────────┘   │
│                          ↓                                │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Orchestration Framework                         │   │
│  │  ├─ DreamCascadeOrchestrator (hierarchical)      │   │
│  │  ├─ DreamSwarmOrchestrator (parallel multi-domain)   │
│  │  ├─ OrchestratorConfig (configuration)           │   │
│  │  └─ TaskStatus, AgentResult, OrchestratorResult  │   │
│  └──────────────────────────────────────────────────┘   │
│                          ↓                                │
│  ┌──────────────────────────────────────────────────┐   │
│  │  LLM Providers & Data                            │   │
│  │  ├─ ProviderFactory (12 LLM providers)           │   │
│  │  ├─ TieredProviderSelector (cost optimization)   │   │
│  │  └─ Data sources (arXiv, Census, etc.)           │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Startup Flow

```
1. service_manager.py starts 'mcp-server' service
   ↓
2. Executes: /home/coolhand/shared/mcp/start.sh
   ↓
3. start.sh launches gunicorn with gevent:
   gunicorn -w 1 -k gevent -b 127.0.0.1:5060 --timeout 300 app:app
   ↓
4. app.py Flask app initializes:
   - Creates UnifiedMCPServer instance
   - Registers streaming routes
   - Initializes StreamingBridge and WebhookManager
   - Loads state_backup.json if exists
   ↓
5. Routes accept HTTP requests and forward to UnifiedMCPServer
   ↓
6. Tools execute orchestrations asynchronously via background_loop
   ↓
7. Progress streamed via SSE, results persisted in state
```

---

## KEY DIFFERENCES: Current vs. FastMCP

### Current Implementation (Flask HTTP)
- ✅ Already deployed and working at port 5060
- ✅ Built-in SSE streaming support
- ✅ Webhook support for async notifications
- ✅ State persistence (state_backup.json)
- ✅ Can be accessed via HTTP/REST from any client
- ❌ NOT compatible with Claude Desktop's stdio/JSON-RPC MCP protocol
- ❌ No native MCP protocol support (different from standard MCP)

### FastMCP (Standard MCP)
- ✅ Compatible with Claude Desktop stdio/JSON-RPC
- ✅ Proper MCP tool schema support
- ✅ Standard tool/resource definition format
- ✅ Async Python language support (3.8+)
- ❌ No built-in SSE streaming (needs manual implementation)
- ❌ Different initialization pattern

---

## INTEGRATION POINTS

### For FastMCP Conversion (if needed):

1. **Existing Tool Definitions**:
   - Already defined in UnifiedMCPServer
   - Can be directly ported to FastMCP decorators

2. **Streaming Infrastructure**:
   - Would need to adapt StreamingBridge for FastMCP's message format
   - SSE would become tool results instead of async streams

3. **State Management**:
   - WorkflowState class can be reused as-is
   - State persistence pattern can continue

4. **Orchestration Framework**:
   - No changes needed - works with any MCP implementation

5. **Service Manager**:
   - Would need new start script that runs FastMCP stdio
   - Port 5060 would be replaced with stdio transport

---

## FILES EXAMINED

### Primary Implementation
- `/home/coolhand/shared/mcp/app.py` (22KB) - Flask entry point
- `/home/coolhand/shared/mcp/unified_server.py` (51KB) - Tool definitions and server logic
- `/home/coolhand/shared/mcp/streaming.py` (14KB) - SSE infrastructure
- `/home/coolhand/shared/mcp/tool_registry.py` (15KB) - Tool discovery system
- `/home/coolhand/shared/mcp/start.sh` - Startup script
- `/home/coolhand/shared/mcp/requirements.txt` - Dependencies

### Configuration & Service
- `/home/coolhand/service_manager.py` (lines 461-490) - Service definition
- `/home/coolhand/.claude/settings.json` - No MCP config
- `/home/coolhand/packages/multi-agent-orchestration/pyproject.toml` - Dreamwalker package

### Supporting Infrastructure
- `/home/coolhand/shared/mcp/background_loop.py` - Async task runner
- `/home/coolhand/shared/mcp/streaming_endpoint.py` - SSE endpoints
- `/home/coolhand/shared/mcp/__init__.py` - Module exports
- `/home/coolhand/shared/mcp/providers_server.py` - LLM provider tools
- `/home/coolhand/shared/mcp/data_server.py` - Data fetching tools
- `/home/coolhand/shared/mcp/cache_server.py` - Caching tools
- `/home/coolhand/shared/mcp/utility_server.py` - Utility tools

### FastMCP References (experimental)
- `/home/coolhand/admin/Claude-MCP-tools/claude-code-integration-mcp/enhanced_server.py`
- `/home/coolhand/admin/Claude-MCP-tools/claude-code-integration-mcp/minimal_server.py`
- `/home/coolhand/admin/Claude-MCP-tools/servers/agenticseek-mcp/server_fastmcp.py`

---

## SUMMARY

The current Dreamwalker MCP server is a **production-grade Flask-based HTTP REST service** running on port 5060 with:

- **7 core orchestrator tools** for research and search workflows
- **Comprehensive SSE streaming** for real-time progress updates
- **Webhook support** for async notifications
- **State persistence** across restarts
- **Dynamic tool registry** for extensibility

It is **NOT using FastMCP** - FastMCP appears only in experimental code in the admin tools directory. The current implementation uses Flask + Gunicorn + Gevent, which is a solid architecture but different from the standard MCP stdio/JSON-RPC protocol that Claude Desktop expects.


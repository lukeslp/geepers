# Implementation Plan: Dreamwalker MCP Server Deployment

**Project:** Remote MCP Server for Claude Desktop Integration
**Status:** PLANNING
**Priority:** High
**Effort Estimate:** 2-3 days
**Date:** 2026-02-06

---

## Executive Summary

Deploy the existing Dreamwalker orchestrator as a production-ready remote MCP server accessible from Claude Desktop via HTTPS on dr.eamer.dev. The infrastructure is 80% complete—an HTTP bridge (`mcp_http_bridge.py`) and cursor config already exist. This plan covers production hardening, authentication, service integration, and testing.

**Key Finding**: The existing MCP infrastructure already has:
- Working HTTP bridge (`mcp_http_bridge.py`) - converts stdio MCP to HTTP
- Cursor config template (`cursor_mcp_config.json`) - points to `https://dr.eamer.dev/mcp`
- Multiple MCP servers in `/home/coolhand/shared/mcp/` (unified_server.py, providers_server.py, data_server.py, etc.)
- Shared orchestration framework with streaming support

**Gap Analysis**: Production deployment requires:
1. HTTP MCP server with FastMCP streamable transport (currently stdio/bridge only)
2. Bearer token authentication & request validation
3. Service manager integration (add to service_manager.py)
4. Health endpoint implementation
5. Caddy reverse proxy configuration
6. Port selection (5059 is free in 5050-5059 range)
7. Testing & monitoring suite

---

## Architecture Decision: Thin HTTP Wrapper vs. Full Integration

### Recommendation: HYBRID APPROACH (Thin HTTP Wrapper + Unified Server)

**Option 1: Extend Existing HTTP Bridge** ❌
- Current `mcp_http_bridge.py` is stdio↔HTTP translator (one-way)
- Only handles client→server, not true HTTP MCP
- Would require extensive modification

**Option 2: Modify Unified Server to Support HTTP** ❌
- `unified_server.py` is Flask app but not MCP-compliant HTTP
- Endpoints are custom REST (/tools/call, /tools/list)
- Would lose compatibility with existing stdio tests

**Option 3: Create New FastMCP HTTP Server (CHOSEN)** ✅
- Wrap existing orchestrator functionality in FastMCP HTTP transport
- Keep unified_server.py as-is (used by internal services)
- New server: `/home/coolhand/shared/mcp/http_mcp_server.py`
- 300-400 lines of FastMCP boilerplate
- Reuses all orchestrator logic via imports
- Implements MCP HTTP spec for Claude Desktop compatibility

### Architecture Diagram

```
Claude Desktop
    ↓
Custom Connector Config (cursor_mcp_config.json)
    ↓
HTTPS: https://dr.eamer.dev/mcp/
    ↓
Caddy Reverse Proxy (/etc/caddy/Caddyfile)
    ↓
Port 5059: http_mcp_server.py (FastMCP HTTP)
    ↓
Dreamwalker Orchestration Layers:
  - dream_orchestrate_research (Dream Cascade)
  - dream_orchestrate_search (Dream Swarm)
  - dreamwalker_status, cancel, patterns
  - dreamwalker_list_tools, execute_tool
    ↓
Backend Services:
  - LLM Providers (xAI, Anthropic, OpenAI, etc.)
  - Data Fetching Clients (arXiv, GitHub, NASA, etc.)
  - Orchestration Framework
```

---

## 1. FastMCP HTTP Server Implementation

### Location
`/home/coolhand/shared/mcp/http_mcp_server.py`

### Dependencies
Add to `/home/coolhand/shared/mcp/requirements.txt`:
```
fastmcp>=0.1.0
aiohttp>=3.8.0
pydantic>=2.0
```

### Implementation Skeleton

```python
#!/usr/bin/env python3
"""
FastMCP HTTP Server for Dreamwalker Orchestration
Exposes dream_orchestrate_research, dream_orchestrate_search, and control tools
via HTTP MCP endpoint compatible with Claude Desktop.

Port: 5059
Health: GET /health
Auth: Bearer token in Authorization header
"""

import os
import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime

import sys
sys.path.insert(0, '/home/coolhand/shared')

from fastmcp import Server, Tool
from pydantic import BaseModel
import uvicorn

from orchestration import DreamCascadeOrchestrator, DreamSwarmOrchestrator, OrchestratorConfig
from llm_providers import ProviderFactory

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Authentication
BEARER_TOKEN = os.getenv('MCP_BEARER_TOKEN', 'not-set')
if BEARER_TOKEN == 'not-set':
    logger.warning("MCP_BEARER_TOKEN not set - authentication disabled")

# Server instance
mcp_server = Server("dreamwalker-mcp-http")

# Tool input models
class DreamResearchRequest(BaseModel):
    task: str
    belter_count: int = 3
    drummer_count: int = 2
    camina_count: int = 1
    provider: str = "xai"
    model: Optional[str] = None
    stream: bool = True
    webhook_url: Optional[str] = None

class DreamSearchRequest(BaseModel):
    task: str
    num_agents: int = 5
    domains: list = None
    max_parallel: int = 3
    provider: str = "xai"
    model: Optional[str] = None
    stream: bool = True

class StatusRequest(BaseModel):
    task_id: str

class CancelRequest(BaseModel):
    task_id: str

class ExecuteToolRequest(BaseModel):
    tool_name: str
    tool_args: Dict[str, Any]

# Global workflow state (could be moved to Redis for production)
workflow_state = {}

# ============================================================================
# TOOLS
# ============================================================================

@mcp_server.tool()
async def dream_orchestrate_research(
    task: str,
    belter_count: int = 3,
    drummer_count: int = 2,
    camina_count: int = 1,
    provider: str = "xai",
    model: Optional[str] = None,
    stream: bool = True,
    webhook_url: Optional[str] = None
) -> Dict[str, Any]:
    """
    Execute hierarchical research workflow using Dream Cascade orchestrator.

    Tier 1 (Belter): Quick parallel searches
    Tier 2 (Drummer): Deep analysis of findings
    Tier 3 (Camina): Final synthesis

    Args:
        task: Research topic or question
        belter_count: Number of parallel searchers (1-10)
        drummer_count: Number of analyzers (1-5)
        camina_count: Number of synthesizers (1-3)
        provider: LLM provider (xai, anthropic, openai)
        model: Specific model to use
        stream: Enable SSE streaming
        webhook_url: Optional webhook for completion notification

    Returns:
        {
            "task_id": "workflow-abc123",
            "status": "running",
            "stream_url": "/stream/workflow-abc123"
        }
    """
    try:
        task_id = f"research-{datetime.now().timestamp()}"

        # Create configuration
        config = OrchestratorConfig(
            num_agents=belter_count + drummer_count + camina_count,
            primary_model=model or 'grok-3',
            parallel_execution=True,
            enable_cost_tracking=True,
            timeout_seconds=600
        )

        # Create provider
        llm_provider = ProviderFactory.create_provider(provider, model=model or 'grok-3')

        # Create orchestrator
        orchestrator = DreamCascadeOrchestrator(config, provider=llm_provider)

        # Store workflow state
        workflow_state[task_id] = {
            "status": "running",
            "type": "research",
            "task": task,
            "created_at": datetime.now().isoformat(),
            "config": {
                "belter_count": belter_count,
                "drummer_count": drummer_count,
                "camina_count": camina_count,
                "provider": provider
            },
            "webhook_url": webhook_url
        }

        logger.info(f"Research workflow {task_id} started: {task}")

        return {
            "task_id": task_id,
            "status": "running",
            "stream_url": f"/stream/{task_id}",
            "message": "Workflow started successfully"
        }

    except Exception as e:
        logger.error(f"Error starting research workflow: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to start research workflow"
        }


@mcp_server.tool()
async def dream_orchestrate_search(
    task: str,
    num_agents: int = 5,
    domains: Optional[list] = None,
    max_parallel: int = 3,
    provider: str = "xai",
    model: Optional[str] = None,
    stream: bool = True
) -> Dict[str, Any]:
    """
    Execute multi-domain parallel search using Dream Swarm orchestrator.

    Searches across multiple data sources in parallel.

    Args:
        task: Search query
        num_agents: Number of parallel agents (1-20)
        domains: List of domains to search (arxiv, github, news, wikipedia, etc.)
        max_parallel: Max concurrent agents (1-10)
        provider: LLM provider
        model: Specific model
        stream: Enable SSE streaming

    Returns:
        {"task_id": "search-abc123", "status": "running"}
    """
    try:
        task_id = f"search-{datetime.now().timestamp()}"

        config = OrchestratorConfig(
            num_agents=num_agents,
            primary_model=model or 'grok-3',
            parallel_execution=True,
            max_concurrent_agents=max_parallel,
            timeout_seconds=600
        )

        llm_provider = ProviderFactory.create_provider(provider, model=model or 'grok-3')

        orchestrator = DreamSwarmOrchestrator(config, provider=llm_provider)

        workflow_state[task_id] = {
            "status": "running",
            "type": "search",
            "task": task,
            "created_at": datetime.now().isoformat(),
            "config": {
                "num_agents": num_agents,
                "domains": domains or ["arxiv", "github", "news"],
                "provider": provider
            }
        }

        logger.info(f"Search workflow {task_id} started: {task}")

        return {
            "task_id": task_id,
            "status": "running",
            "stream_url": f"/stream/{task_id}",
            "message": "Workflow started successfully"
        }

    except Exception as e:
        logger.error(f"Error starting search workflow: {e}")
        return {"success": False, "error": str(e)}


@mcp_server.tool()
async def dreamwalker_status(task_id: str) -> Dict[str, Any]:
    """
    Get status of a running or completed workflow.

    Args:
        task_id: Workflow task ID

    Returns:
        {"status": "running|completed|failed", "progress": 50, ...}
    """
    if task_id not in workflow_state:
        return {
            "success": False,
            "error": "Task not found",
            "task_id": task_id
        }

    workflow = workflow_state[task_id]
    return {
        "task_id": task_id,
        "status": workflow.get("status"),
        "type": workflow.get("type"),
        "progress": workflow.get("progress", 0),
        "created_at": workflow.get("created_at"),
        "result": workflow.get("result")
    }


@mcp_server.tool()
async def dreamwalker_cancel(task_id: str) -> Dict[str, Any]:
    """Cancel a running workflow."""
    if task_id not in workflow_state:
        return {
            "success": False,
            "error": "Task not found",
            "task_id": task_id
        }

    workflow_state[task_id]["status"] = "cancelled"
    logger.info(f"Workflow {task_id} cancelled")

    return {
        "success": True,
        "message": "Workflow cancelled",
        "task_id": task_id
    }


@mcp_server.tool()
async def dreamwalker_patterns() -> Dict[str, Any]:
    """List available orchestrator patterns."""
    return {
        "patterns": [
            {
                "name": "dream_cascade",
                "description": "Hierarchical research with 3-tier agents (Belter → Drummer → Camina)",
                "config_options": {
                    "belter_count": "integer (1-10)",
                    "drummer_count": "integer (1-5)",
                    "camina_count": "integer (1-3)"
                }
            },
            {
                "name": "dream_swarm",
                "description": "Multi-domain parallel search",
                "config_options": {
                    "num_agents": "integer (1-20)",
                    "domains": "list of strings",
                    "max_parallel": "integer (1-10)"
                }
            }
        ]
    }


@mcp_server.tool()
async def dreamwalker_list_tools(category: Optional[str] = None) -> Dict[str, Any]:
    """List registered tools available in orchestration system."""
    # Placeholder - would enumerate actual tools
    return {
        "tools": [
            {
                "name": "arxiv_search",
                "category": "data",
                "description": "Search academic papers on arXiv"
            },
            {
                "name": "github_search",
                "category": "data",
                "description": "Search GitHub repositories"
            }
        ]
    }


@mcp_server.tool()
async def dreamwalker_execute_tool(tool_name: str, tool_args: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a specific registered tool."""
    try:
        logger.info(f"Executing tool: {tool_name} with args: {tool_args}")
        # Placeholder - would dispatch to actual tool
        return {
            "success": True,
            "tool_name": tool_name,
            "result": "Tool executed successfully"
        }
    except Exception as e:
        logger.error(f"Error executing tool {tool_name}: {e}")
        return {"success": False, "error": str(e)}


# ============================================================================
# HTTP ENDPOINTS
# ============================================================================

from fastapi import FastAPI, Request, HTTPException, Header
from contextlib import asynccontextmanager

# Authentication middleware
async def verify_bearer_token(authorization: Optional[str] = Header(None)):
    if BEARER_TOKEN == "not-set":
        logger.warning("Bearer token authentication disabled")
        return None

    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    token = authorization[7:]  # Remove "Bearer " prefix
    if token != BEARER_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")

    return token


# Lifecycle
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Dreamwalker MCP HTTP Server started")
    yield
    logger.info("Dreamwalker MCP HTTP Server shutting down")


# Create FastAPI app (wrapped by FastMCP)
app = mcp_server.app()

# Health endpoint (no auth required)
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "dreamwalker-mcp",
        "active_workflows": len(workflow_state)
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    port = int(os.getenv("MCP_PORT", 5059))
    host = os.getenv("MCP_HOST", "127.0.0.1")

    logger.info(f"Starting Dreamwalker MCP HTTP Server on {host}:{port}")

    uvicorn.run(
        "http_mcp_server:app",
        host=host,
        port=port,
        reload=os.getenv("ENV", "production") == "development"
    )
```

### Key Features
- **Async/await** support for long-running workflows
- **Streaming-ready** (SSE can be added via `/stream/{task_id}` endpoint)
- **Stateful workflows** (task_id tracking in memory; Redis for production)
- **Bearer token auth** (configurable via env var)
- **Health endpoint** (no auth, used by service manager)
- **Structured logging** (to stderr; stdout for MCP protocol)

---

## 2. Authentication Mechanism

### Bearer Token Implementation

**Where to store**:
- Development: `MCP_BEARER_TOKEN` environment variable
- Production: `/home/coolhand/documentation/API_KEYS.md` (gitignored)

**Setup Steps**:
1. Generate token (UUID):
   ```bash
   python3 -c "import uuid; print(uuid.uuid4().hex)"
   ```
2. Store in `API_KEYS.md`:
   ```
   # MCP Server
   MCP_BEARER_TOKEN=abc123def456xyz789...
   ```
3. Service manager loads from environment

**Request Format**:
```bash
curl -H "Authorization: Bearer abc123def456xyz789" \
  https://dr.eamer.dev/mcp/tools/dream_orchestrate_research \
  -d '{"task": "Research quantum computing", ...}'
```

**Cursor Config** (will be in cursor_mcp_config.json):
- Cannot embed auth in config (plaintext issue)
- Use Claude Desktop environment variables or credential store
- Alternative: Bearer token only for remote deployment; stdio for local testing

### Disable in Development
```python
if os.getenv('MCP_ENV') == 'development':
    BEARER_TOKEN = "disabled"
```

---

## 3. Caddy Reverse Proxy Configuration

### Location: `/etc/caddy/Caddyfile`

Add after other service entries:

```caddyfile
# Dreamwalker MCP Server
handle /mcp* {
    # HTTPS only (Caddy enforces automatically)
    reverse_proxy localhost:5059 {
        # MCP streams long-running connections
        flush_interval -1

        # Preserve headers for auth
        header_up Authorization {http.request.header.Authorization}

        # Long timeouts for workflows (10 minutes)
        transport http {
            dial_timeout 10s
            response_header_timeout 10m
            idle_conn_timeout 10m
        }
    }
}
```

**Notes:**
- `flush_interval -1` = disable buffering for SSE streams
- `dial_timeout` = initial connection timeout
- `response_header_timeout` = timeout to receive first response byte
- `idle_conn_timeout` = keep-alive timeout for idle connections

### Verification
```bash
sudo caddy validate --config /etc/caddy/Caddyfile
sudo systemctl reload caddy
curl -H "Authorization: Bearer TOKEN" https://dr.eamer.dev/mcp/health
```

---

## 4. Service Manager Integration

### Location: `/home/coolhand/service_manager.py`

Add to `SERVICES` dict:

```python
'mcp-orchestrator': {
    'name': 'Dreamwalker MCP Server',
    'script': '/home/coolhand/shared/mcp/start_mcp_http.sh',
    'working_dir': '/home/coolhand/shared/mcp',
    'port': 5059,
    'health_endpoint': 'http://localhost:5059/health',
    'start_timeout': 15,
    'description': 'Remote MCP server for Dreamwalker orchestrator, accessible from Claude Desktop'
},
```

### Startup Script: `/home/coolhand/shared/mcp/start_mcp_http.sh`

```bash
#!/bin/bash
set -e

# Load environment
source /home/coolhand/documentation/API_KEYS.md 2>/dev/null || true

# Set defaults
export MCP_PORT=${MCP_PORT:-5059}
export MCP_HOST=${MCP_HOST:-127.0.0.1}
export MCP_BEARER_TOKEN=${MCP_BEARER_TOKEN:-}
export PYTHONPATH=/home/coolhand/shared:$PYTHONPATH

cd /home/coolhand/shared/mcp
exec python3 http_mcp_server.py
```

### Testing Service Manager
```bash
sm start mcp-orchestrator
sm status
sm logs mcp-orchestrator
sm health mcp-orchestrator

# Verify
curl http://localhost:5059/health
curl -H "Authorization: Bearer $MCP_BEARER_TOKEN" http://localhost:5059/tools
```

---

## 5. Health Endpoint Implementation

### GET /health

```python
@app.get("/health")
async def health_check():
    """Health check endpoint (no authentication required)."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "dreamwalker-mcp",
        "version": "1.0.0",
        "uptime_seconds": get_uptime(),
        "active_workflows": len(workflow_state),
        "memory_usage_mb": get_memory_usage(),
        "dependencies": {
            "orchestration": "available",
            "llm_providers": "available",
            "data_fetching": "available"
        }
    }
```

**Used by:**
- Service manager monitoring
- Caddy health checks
- External monitoring (Prometheus, etc.)

---

## 6. Port Selection: 5059

**Rationale:**
- Port range allocated: 5050-5059 (10 services)
- Current usage:
  - 5050: Skymarshal
  - 5051: Karate Dramatizer
  - 5052: Firehose Dashboard
  - 5053: Pinpoint Geography
  - 5054: Alt Text Generator
  - 5055: Story Illustrator
  - 5056: (check current usage)
  - 5057: (check current usage)
  - 5058: (check current usage)
  - **5059: AVAILABLE** ← Assign to MCP Server

**Verification:**
```bash
lsof -i :5059
netstat -tuln | grep 5059
```

---

## 7. Testing Strategy

### Unit Tests
Location: `/home/coolhand/shared/mcp/tests/test_http_mcp_server.py`

```python
import pytest
from http_mcp_server import mcp_server, workflow_state

@pytest.mark.asyncio
async def test_dream_research_tool():
    """Test research workflow initiation."""
    result = await mcp_server.tools["dream_orchestrate_research"].execute({
        "task": "Test research",
        "belter_count": 1,
        "drummer_count": 1,
        "camina_count": 1
    })

    assert "task_id" in result
    assert result["status"] == "running"
    assert "stream_url" in result


@pytest.mark.asyncio
async def test_status_endpoint():
    """Test status checking."""
    # Create a workflow first
    result = await dream_orchestrate_research("test")
    task_id = result["task_id"]

    # Check status
    status = await dreamwalker_status(task_id)
    assert status["task_id"] == task_id
    assert status["status"] in ["running", "completed", "failed"]


@pytest.mark.asyncio
async def test_cancel_endpoint():
    """Test workflow cancellation."""
    result = await dream_orchestrate_research("test")
    task_id = result["task_id"]

    cancel = await dreamwalker_cancel(task_id)
    assert cancel["success"] == True

    status = await dreamwalker_status(task_id)
    assert status["status"] == "cancelled"


def test_health_endpoint(client):
    """Test health check (HTTP)."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

### Integration Tests
```python
@pytest.mark.asyncio
async def test_full_research_workflow():
    """Test end-to-end research workflow."""
    # Initiate
    result = await dream_orchestrate_research(
        task="What is quantum entanglement?",
        belter_count=2,
        drummer_count=1,
        provider="xai"
    )

    task_id = result["task_id"]

    # Wait for completion (with timeout)
    for _ in range(60):
        status = await dreamwalker_status(task_id)
        if status["status"] == "completed":
            assert "result" in status
            break
        await asyncio.sleep(1)
```

### Manual Testing
```bash
# Start server
sm start mcp-orchestrator

# Test health (no auth)
curl http://localhost:5059/health

# Test with bearer token
export TOKEN=$(grep MCP_BEARER_TOKEN /home/coolhand/documentation/API_KEYS.md | cut -d= -f2)

# List tools
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5059/tools

# Call research tool
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"task":"Test","belter_count":1}' \
  http://localhost:5059/tools/dream_orchestrate_research

# Check status
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5059/tools/dreamwalker_status \
  -d '{"task_id":"research-12345"}'
```

### Claude Desktop Testing
After deployment:
1. Update `~/.cursor/mcp_config.json`:
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
           "MCP_BEARER_TOKEN": "abc123..."
         }
       }
     }
   }
   ```

2. In Claude Desktop, use the tool:
   > @tools show me available orchestration patterns
   > @tools can you research quantum computing using Dream Cascade with 3 belters?

3. Monitor backend:
   ```bash
   sm logs mcp-orchestrator
   ```

---

## Implementation Sequence

### Phase 1: Server Implementation (Day 1)
- [ ] Create `/home/coolhand/shared/mcp/http_mcp_server.py`
  - Tool definitions (dream_orchestrate_research, dream_orchestrate_search, etc.)
  - FastMCP integration
  - Health endpoint
  - Authentication middleware
  - Workflow state management
- [ ] Update `/home/coolhand/shared/mcp/requirements.txt`
  - Add fastmcp, uvicorn, aiohttp, pydantic
- [ ] Create startup script `/home/coolhand/shared/mcp/start_mcp_http.sh`

### Phase 2: Infrastructure Integration (Day 1-2)
- [ ] Update `/home/coolhand/service_manager.py`
  - Add mcp-orchestrator service config
  - Port 5059 assigned
  - Health endpoint configured
- [ ] Generate and store bearer token
  - Add to `/home/coolhand/documentation/API_KEYS.md`
- [ ] Update `/etc/caddy/Caddyfile`
  - Add `/mcp*` reverse proxy block
  - Configure timeouts for long-running workflows
  - Validate config
  - Reload Caddy
- [ ] Update `/home/coolhand/projects/PORT_ALLOCATION.md`
  - Document port 5059 assignment

### Phase 3: Testing (Day 2)
- [ ] Create test suite `/home/coolhand/shared/mcp/tests/test_http_mcp_server.py`
  - Unit tests for each tool
  - Integration tests for workflows
  - Authentication tests
  - Health endpoint tests
- [ ] Manual testing
  - Service manager start/status/logs
  - Local HTTP testing with curl
  - Bearer token validation
  - Caddy routing verification
- [ ] Claude Desktop integration
  - Update cursor config
  - Test tool discovery
  - Test tool execution

### Phase 4: Production Hardening (Day 3)
- [ ] Implement SSE streaming for `/stream/{task_id}` (optional but recommended)
- [ ] Add Redis state backend (optional, for multi-instance)
- [ ] Add rate limiting to prevent abuse
- [ ] Add request logging/audit trail
- [ ] Add monitoring/alerting
- [ ] Document in `/home/coolhand/shared/mcp/CLAUDE.md`
- [ ] Create backup startup script
- [ ] Test failure scenarios

---

## Key Configuration Files

### 1. `/home/coolhand/shared/mcp/http_mcp_server.py` (NEW)
FastMCP HTTP server wrapping orchestrators. ~300-400 lines.

### 2. `/home/coolhand/shared/mcp/requirements.txt` (MODIFY)
Add dependencies:
```
fastmcp>=0.1.0
uvicorn>=0.24.0
aiohttp>=3.8.0
pydantic>=2.0
```

### 3. `/home/coolhand/shared/mcp/start_mcp_http.sh` (NEW)
Service startup script.

### 4. `/home/coolhand/service_manager.py` (MODIFY)
Add mcp-orchestrator to SERVICES dict.

### 5. `/etc/caddy/Caddyfile` (MODIFY)
Add `/mcp*` reverse proxy block.

### 6. `/home/coolhand/documentation/API_KEYS.md` (MODIFY)
Add MCP_BEARER_TOKEN.

### 7. `/home/coolhand/projects/PORT_ALLOCATION.md` (MODIFY)
Document port 5059 allocation.

### 8. `/home/coolhand/shared/mcp/CLAUDE.md` (MODIFY)
Update with HTTP server documentation.

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| **Auth bypass** | Bearer token required; service manager can rotate token; no hardcoded tokens in code |
| **Long-running timeouts** | Caddy timeout = 10m; implement heartbeat/progress streaming |
| **Memory leaks** (old workflows) | Implement workflow cleanup; max_workflows limit; state pruning |
| **Cascading failures** | Health endpoint for service manager; fallback to stdio server; circuit breaker pattern |
| **Performance degradation** | Rate limiting; max concurrent workflows; async execution |
| **Incompatibility with Claude Desktop** | Use standard FastMCP HTTP transport; test against actual Claude Desktop client |

---

## Success Criteria

- [ ] **Service starts**: `sm start mcp-orchestrator` → status "running"
- [ ] **Health check passes**: `curl http://localhost:5059/health` → 200 OK
- [ ] **Caddy routing works**: `curl https://dr.eamer.dev/mcp/health` → 200 OK (HTTPS)
- [ ] **Authentication enforced**: Requests without bearer token → 401 Unauthorized
- [ ] **Tools discoverable**: Claude Desktop can list available tools
- [ ] **Tools executable**: `dream_orchestrate_research` can be called from Claude Desktop
- [ ] **Workflows tracked**: `dreamwalker_status` returns current workflow state
- [ ] **Streaming works** (optional): SSE `/stream/{task_id}` endpoint returns progress events
- [ ] **Monitoring integrated**: Service manager health checks pass every 30s
- [ ] **No breaking changes**: Existing stdio MCP server still works for local development

---

## Rollback Plan

If deployment fails:

1. **Service won't start**:
   - Revert changes to `service_manager.py`
   - Revert Caddy config
   - Keep http_mcp_server.py for future fixes

2. **Caddy errors**:
   - `sudo caddy validate --config /etc/caddy/Caddyfile`
   - Restore previous Caddyfile: `git checkout /etc/caddy/Caddyfile`
   - `sudo systemctl reload caddy`

3. **Bearer token issues**:
   - Disable auth: `export MCP_BEARER_TOKEN=disabled`
   - Or update token in API_KEYS.md

4. **Claude Desktop still uses old config**:
   - Update `~/.cursor/mcp_config.json` to point to local stdio server
   - Or restart Cursor

---

## Future Enhancements

1. **SSE Streaming**: Implement `/stream/{task_id}` for real-time progress
2. **Redis Backend**: Move workflow state from in-memory to Redis for scalability
3. **Webhook Notifications**: POST to webhook_url when workflow completes
4. **Rate Limiting**: Limit requests per token per minute
5. **Audit Logging**: Log all tool calls for compliance
6. **Workflow History**: Archive completed workflows to database
7. **Custom Tool Registry**: Allow runtime registration of new tools
8. **Multi-instance**: Load balance across multiple MCP servers
9. **Analytics**: Track tool usage, performance metrics
10. **Cost Tracking**: Integrate with orchestrator cost tracking for billing

---

## Related Documentation

- **Orchestration Framework**: `/home/coolhand/shared/orchestration/ORCHESTRATOR_GUIDE.md`
- **Service Manager**: `/home/coolhand/service_manager.py`
- **Caddy Config**: `/etc/caddy/Caddyfile`
- **Port Allocation**: `/home/coolhand/projects/PORT_ALLOCATION.md`
- **API Keys**: `/home/coolhand/documentation/API_KEYS.md`
- **FastMCP Docs**: https://github.com/jlowin/fastmcp
- **MCP Spec**: https://modelcontextprotocol.io/

---

## Contact & Attribution

**Plan Created**: Claude Code (claude.ai/code)
**Author**: Luke Steuber
**Project**: Dreamwalker MCP Server Deployment
**Status**: PLANNING - Ready for implementation review

For questions or modifications, refer to this document or contact the development team.

---

**Document Version**: 1.0
**Last Updated**: 2026-02-06
**Next Review**: Upon implementation completion

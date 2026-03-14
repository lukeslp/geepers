# Dreamwalker MCP Deployment - Architecture & Dependency Map

---

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLAUDE DESKTOP                            │
│                  (Running on user's machine)                     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    MCP Config File
              (~/.cursor/mcp_config.json)
                              ↓
         HTTPClient Bridge (mcp_http_bridge.py)
                              ↓
                  HTTPS Request with Bearer Token
        Authorization: Bearer abc123def456xyz789
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   dr.eamer.dev (HTTPS)                           │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  CADDY REVERSE PROXY (/etc/caddy/Caddyfile)              │ │
│  │                                                            │ │
│  │  handle /mcp* {                                            │ │
│  │    reverse_proxy localhost:5059 {                          │ │
│  │      flush_interval -1  # for SSE                         │ │
│  │      response_header_timeout 10m                          │ │
│  │    }                                                        │ │
│  │  }                                                          │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              ↓                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  PORT 5059: FastMCP HTTP SERVER                           │ │
│  │  (http_mcp_server.py)                                      │ │
│  │                                                            │ │
│  │  ✓ Bearer Token Authentication Middleware                │ │
│  │  ✓ Tool Definitions & Handlers                           │ │
│  │  ✓ Workflow State Management                             │ │
│  │  ✓ Health Endpoint (/health - no auth)                   │ │
│  │  ✓ SSE Streaming Support (/stream/{task_id})             │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              ↓                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  TOOLS EXPOSED (7 MCP Tools)                              │ │
│  │                                                            │ │
│  │  1. dream_orchestrate_research                            │ │
│  │     → DreamCascadeOrchestrator (3-tier: Belter/Drummer)  │ │
│  │                                                            │ │
│  │  2. dream_orchestrate_search                              │ │
│  │     → DreamSwarmOrchestrator (multi-domain parallel)      │ │
│  │                                                            │ │
│  │  3. dreamwalker_status                                    │ │
│  │     → Query workflow status                               │ │
│  │                                                            │ │
│  │  4. dreamwalker_cancel                                    │ │
│  │     → Stop running workflow                               │ │
│  │                                                            │ │
│  │  5. dreamwalker_patterns                                  │ │
│  │     → List orchestrator patterns                          │ │
│  │                                                            │ │
│  │  6. dreamwalker_list_tools                                │ │
│  │     → List available tools in ecosystem                   │ │
│  │                                                            │ │
│  │  7. dreamwalker_execute_tool                              │ │
│  │     → Execute specific tool                               │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              ↓                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  ORCHESTRATION FRAMEWORK                                  │ │
│  │  (/home/coolhand/shared/orchestration/)                   │ │
│  │                                                            │ │
│  │  ├── dream_cascade_orchestrator.py                        │ │
│  │  │   • 3-tier: Belter (search) → Drummer (analyze)       │ │
│  │  │   • → Camina (synthesize)                             │ │
│  │  │   • Streaming progress callbacks                       │ │
│  │  │                                                        │ │
│  │  ├── dream_swarm_orchestrator.py                          │ │
│  │  │   • Multi-domain parallel search                       │ │
│  │  │   • Configurable concurrent agents                     │ │
│  │  │                                                        │ │
│  │  └── base_orchestrator.py                                 │ │
│  │      • Abstract base class                                │ │
│  │      • Cost tracking, streaming, retry logic             │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              ↓                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  LLM PROVIDERS                                             │ │
│  │  (/home/coolhand/shared/llm_providers/)                   │ │
│  │                                                            │ │
│  │  12 Providers via ProviderFactory:                        │ │
│  │  • xAI (Grok) ← Default                                   │ │
│  │  • Anthropic (Claude)                                     │ │
│  │  • OpenAI (GPT-4)                                         │ │
│  │  • Mistral, Cohere, Gemini, Perplexity                   │ │
│  │  • Groq, HuggingFace, Ollama (local), etc.               │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              ↓                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  DATA FETCHING CLIENTS                                    │ │
│  │  (/home/coolhand/shared/data_fetching/)                   │ │
│  │                                                            │ │
│  │  17 Data Sources via ClientFactory:                       │ │
│  │  • arxiv, github, news, wikipedia, youtube                │ │
│  │  • nasa, census, semantic_scholar, finance                │ │
│  │  • pubmed, wolfram, wayback_machine, etc.                 │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Dependency Map

### Tier 1: HTTP Transport Layer
```
FastMCP HTTP Server (http_mcp_server.py)
├── FastMCP Framework (fastmcp>=0.1.0)
├── Uvicorn (uvicorn>=0.24.0)
├── Pydantic (pydantic>=2.0) - Request/response validation
├── AIOHTTP (aiohttp>=3.8.0) - Async HTTP client
└── Logging - Python stdlib
```

### Tier 2: Authentication & State
```
MCP HTTP Server
├── Bearer Token Validation
│   └── Environment Variable: MCP_BEARER_TOKEN
├── Workflow State Management
│   ├── In-memory dict (development)
│   └── Redis (future: production scaling)
└── Health Monitoring
    └── Service Manager integration
```

### Tier 3: Tool Definitions
```
7 MCP Tools
├── dream_orchestrate_research
│   └── DreamCascadeOrchestrator
├── dream_orchestrate_search
│   └── DreamSwarmOrchestrator
├── dreamwalker_status
│   └── Workflow State Query
├── dreamwalker_cancel
│   └── Workflow Cancellation
├── dreamwalker_patterns
│   └── Pattern Enumeration
├── dreamwalker_list_tools
│   └── Tool Registry
└── dreamwalker_execute_tool
    └── Tool Dispatcher
```

### Tier 4: Orchestration Framework
```
Orchestration Layer (/home/coolhand/shared/orchestration/)
├── DreamCascadeOrchestrator
│   ├── decompose_task() → List[SubTask]
│   ├── execute_subtask() → AgentResult
│   └── synthesize_results() → OrchestratorResult
├── DreamSwarmOrchestrator
│   ├── Multi-agent parallel execution
│   └── Domain-specific searching
├── BaseOrchestrator (abstract)
│   ├── Config validation
│   ├── Cost tracking
│   ├── Streaming callbacks
│   └── Retry logic
└── Supporting Utilities
    ├── models.py - SubTask, AgentResult, OrchestratorResult
    ├── config.py - OrchestratorConfig
    ├── streaming.py - Progress streaming
    └── utils.py - Helper functions
```

### Tier 5: LLM Providers
```
LLM Providers (/home/coolhand/shared/llm_providers/)
├── BaseLLMProvider (abstract)
│   ├── complete() - sync chat completion
│   ├── stream_complete() - streaming
│   ├── generate_image() - image generation
│   └── analyze_image() - vision
├── ProviderFactory
│   └── create_provider(name, **kwargs)
└── 12 Implementations
    ├── xai_provider.py (xAI/Grok) - PRIMARY
    ├── anthropic_provider.py (Claude)
    ├── openai_provider.py (GPT)
    ├── ollama_provider.py (local models)
    ├── mistral_provider.py
    ├── cohere_provider.py
    ├── gemini_provider.py
    ├── perplexity_provider.py
    ├── groq_provider.py
    ├── huggingface_provider.py
    ├── manus_provider.py
    └── elevenlabs_provider.py (TTS)
```

### Tier 6: Data Fetching
```
Data Fetching Clients (/home/coolhand/shared/data_fetching/)
├── ClientFactory
│   └── create_client(name) → Client
├── BaseClient (abstract)
│   └── search(**kwargs) → List[Result]
└── 17 Implementations
    ├── arxiv_client.py - Academic papers
    ├── github_client.py - Code repos
    ├── news_client.py - News articles
    ├── wikipedia_client.py - Encyclopedia
    ├── youtube_client.py - Videos
    ├── nasa_client.py - NASA data
    ├── census_client.py - US Census
    ├── semantic_scholar_client.py - Academic
    ├── weather_client.py - Weather data
    ├── openlibrary_client.py - Books
    ├── finance_client.py - Financial data
    ├── pubmed_client.py - Medical research
    ├── wolfram_client.py - Computation
    ├── wayback_machine_client.py - Archives
    ├── judiciary_client.py - Court records
    ├── fec_client.py - Campaign finance
    └── mal_client.py - Malware/security
```

---

## Data Flow Diagram

### Request Flow (Happy Path)

```
1. INITIATE WORKFLOW
   Claude Desktop User:
   "Research quantum entanglement using Dream Cascade"

   ↓

2. CLAUDE SENDS MCP REQUEST
   POST /tools/dream_orchestrate_research
   Authorization: Bearer token123
   Body: {
     "task": "Research quantum entanglement",
     "belter_count": 3,
     "drummer_count": 2,
     "camina_count": 1,
     "provider": "xai",
     "stream": true
   }

   ↓

3. HTTP SERVER VALIDATION
   • Parse JSON request
   • Validate bearer token (401 if invalid)
   • Create OrchestratorConfig
   • Initialize DreamCascadeOrchestrator
   • Generate task_id = "research-1707123456.789"

   ↓

4. RETURN IMMEDIATELY (Non-blocking)
   Response (200 OK):
   {
     "task_id": "research-1707123456.789",
     "status": "running",
     "stream_url": "/stream/research-1707123456.789",
     "message": "Workflow started successfully"
   }

   ↓
   (Workflow runs in background)

5. USER POLLS STATUS
   GET /tools/dreamwalker_status
   Body: {"task_id": "research-1707123456.789"}

   Response:
   {
     "task_id": "research-1707123456.789",
     "status": "running",
     "progress": 45,
     "current_stage": "Drummer tier (analysis)",
     "created_at": "2026-02-06T12:34:56Z"
   }

   ↓
   (Optional: Subscribe to stream)

6. STREAM PROGRESS (SSE)
   GET /stream/research-1707123456.789

   Events:
   event: task_started
   data: {"message": "Starting research workflow..."}

   event: agent_complete
   data: {"agent": "belter-1", "progress": 33}

   event: stage_change
   data: {"stage": "Drummer tier", "progress": 50}

   event: task_completed
   data: {
     "status": "completed",
     "result": {
       "summary": "Quantum entanglement is...",
       "details": [...],
       "total_cost": "$0.05",
       "execution_time": 45.2
     }
   }

   ↓

7. WORKFLOW COMPLETION
   Claude Desktop receives result and uses for next action
```

### Error Flow

```
Invalid Bearer Token:
  ↓
Request: Authorization: Bearer invalid_token
  ↓
HTTP Server:
  1. Parse header
  2. Extract token → "invalid_token"
  3. Compare to MCP_BEARER_TOKEN
  4. Mismatch detected
  ↓
Response (403 Forbidden):
  {
    "error": "Invalid token",
    "message": "Authentication failed"
  }

Claude Desktop:
  ↓
User sees: "Not authenticated - check bearer token"
```

---

## Deployment Architecture

```
┌────────────────────────────────────────────────────────┐
│                    DEPLOYMENT STACK                    │
├────────────────────────────────────────────────────────┤
│                                                        │
│  Layer 5: Service Orchestration                       │
│  ┌────────────────────────────────────────────────┐  │
│  │ Service Manager (service_manager.py)           │  │
│  │ ├── Start/Stop/Restart mcp-orchestrator        │  │
│  │ ├── Health monitoring (every 30s)              │  │
│  │ ├── Log collection                             │  │
│  │ └── Status reporting                           │  │
│  └────────────────────────────────────────────────┘  │
│                                                        │
│  Layer 4: HTTP Reverse Proxy                         │
│  ┌────────────────────────────────────────────────┐  │
│  │ Caddy Server (systemd: caddy.service)          │  │
│  │ ├── HTTPS termination (dr.eamer.dev)           │  │
│  │ ├── Route /mcp* → localhost:5059               │  │
│  │ ├── Long timeout support (10m)                 │  │
│  │ └── SSL/TLS certificate management              │  │
│  └────────────────────────────────────────────────┘  │
│                                                        │
│  Layer 3: Application Server                         │
│  ┌────────────────────────────────────────────────┐  │
│  │ Uvicorn + FastMCP (http_mcp_server.py)         │  │
│  │ ├── Port: 5059                                 │  │
│  │ ├── Host: 127.0.0.1 (localhost only)           │  │
│  │ ├── Workers: 1 (single process)                │  │
│  │ └── Logging: stderr                            │  │
│  └────────────────────────────────────────────────┘  │
│                                                        │
│  Layer 2: Python Runtime & Dependencies              │
│  ┌────────────────────────────────────────────────┐  │
│  │ Python 3.10+ Virtual Environment                │  │
│  │ ├── /home/coolhand/shared (installation)       │  │
│  │ ├── requirements.txt (pip packages)             │  │
│  │ └── Environment variables (API_KEYS.md)         │  │
│  └────────────────────────────────────────────────┘  │
│                                                        │
│  Layer 1: System Services                            │
│  ┌────────────────────────────────────────────────┐  │
│  │ Linux (Ubuntu 20.04+)                          │  │
│  │ ├── systemd (caddy.service)                    │  │
│  │ ├── File system (all code in /home/coolhand)  │  │
│  │ ├── Networking (port 5059, HTTPS 443)         │  │
│  │ └── Monitoring (lsof, ps, curl health checks) │  │
│  └────────────────────────────────────────────────┘  │
│                                                        │
└────────────────────────────────────────────────────────┘
```

---

## Authentication & Authorization

### Bearer Token Flow

```
Token Storage:
  /home/coolhand/documentation/API_KEYS.md (gitignored)
  └─ MCP_BEARER_TOKEN=abc123def456xyz789...

Token Generation:
  $ python3 -c "import uuid; print(uuid.uuid4().hex)"
  → abc123def456xyz789...

Token Usage:

  Client (Claude Desktop):
  $ curl -H "Authorization: Bearer abc123def456xyz789" \
    https://dr.eamer.dev/mcp/tools/dreamwalker_patterns

  HTTP Server:
  def verify_bearer_token(authorization: str):
      if not authorization.startswith("Bearer "):
          raise 401 Unauthorized
      token = authorization[7:]  # Extract token
      if token != os.getenv("MCP_BEARER_TOKEN"):
          raise 403 Forbidden
      return True

Exempt Endpoints:
  - GET /health (allows service monitoring without token)
  - Others require bearer token
```

---

## Configuration Sources (Priority Order)

### 1. Environment Variables (Highest Priority)
```bash
export MCP_PORT=5059
export MCP_HOST=127.0.0.1
export MCP_BEARER_TOKEN=abc123...
export MCP_ENV=production
export LOG_LEVEL=INFO
```

### 2. Startup Script
```bash
# /home/coolhand/shared/mcp/start_mcp_http.sh
source /home/coolhand/documentation/API_KEYS.md
export PYTHONPATH=/home/coolhand/shared:$PYTHONPATH
python3 http_mcp_server.py
```

### 3. Service Manager Config
```python
# /home/coolhand/service_manager.py
'mcp-orchestrator': {
    'script': '.../start_mcp_http.sh',
    'port': 5059,
    'health_endpoint': 'http://localhost:5059/health'
}
```

### 4. Default Values (Lowest Priority)
```python
# http_mcp_server.py
MCP_PORT = int(os.getenv("MCP_PORT", 5059))
MCP_HOST = os.getenv("MCP_HOST", "127.0.0.1")
MCP_BEARER_TOKEN = os.getenv("MCP_BEARER_TOKEN", "not-set")
```

---

## Port & Network Architecture

### Port Allocation

```
Server Listening:
  Local: 127.0.0.1:5059 (Uvicorn/FastMCP HTTP Server)
         └─ Accepts connections from localhost only
         └─ NEVER expose to network directly

Caddy Proxy:
  Local:  0.0.0.0:80 (redirects to HTTPS)
  Local:  0.0.0.0:443 (HTTPS with SSL cert)
         └─ Listens on all interfaces
         └─ Routes /mcp* to localhost:5059

External Access:
  https://dr.eamer.dev/mcp → Caddy (443) → Localhost:5059

Verification:
  $ lsof -i :5059
  COMMAND     PID  USER   FD TYPE DEVICE SIZE NODE NAME
  python3  12345  cool    3u IPv4 ...    TCP 127.0.0.1:5059 (LISTEN)
           └─ Note: 127.0.0.1 only, NOT 0.0.0.0
```

---

## Health Check Architecture

### Service Manager Health Monitoring

```
Every 30 seconds:
  ┌─────────────────────────────────────┐
  │ Service Manager                     │
  │ (service_manager.py)                │
  └─────────────────────────────────────┘
                    ↓
         GET http://localhost:5059/health
                    ↓
  ┌─────────────────────────────────────┐
  │ FastMCP Server                      │
  │ (http_mcp_server.py)                │
  │                                     │
  │ @app.get("/health")                 │
  │ async def health_check():           │
  │     return {                        │
  │         "status": "healthy",        │
  │         "timestamp": "...",         │
  │         "active_workflows": 5,      │
  │         "memory_usage_mb": 245      │
  │     }                               │
  └─────────────────────────────────────┘
                    ↓
              200 OK Response
                    ↓
  ┌─────────────────────────────────────┐
  │ Service Manager                     │
  │ ├─ Status: HEALTHY                  │
  │ ├─ Last check: 2 seconds ago         │
  │ ├─ Uptime: 5 days 12 hours          │
  │ └─ Next check: in 30 seconds         │
  └─────────────────────────────────────┘
```

### Caddy Health Monitoring

```
Caddy monitors service manager status:
  If service_manager reports mcp-orchestrator DOWN:
  ├─ All requests to /mcp* → 502 Bad Gateway
  └─ Caddy logs: "upstream not available"

Users see:
  curl https://dr.eamer.dev/mcp/health
  → 502 Bad Gateway (service down)
```

---

## Scaling Considerations (Future)

### Current (MVP)
```
Single Instance:
  - In-memory workflow state
  - One Uvicorn worker
  - Max ~10 concurrent workflows
  - Memory: ~200-300 MB
```

### Phase 2 (Production)
```
Multi-Instance Setup:
  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
  │ MCP Server 1 │  │ MCP Server 2 │  │ MCP Server 3 │
  │ Port 5059    │  │ Port 5060    │  │ Port 5061    │
  └──────────────┘  └──────────────┘  └──────────────┘
         ↑                 ↑                  ↑
         └─────────────────┴──────────────────┘
                    ↓
         Load Balancer (Caddy/HAProxy)
                    ↓
         Shared State: Redis
         Shared Logging: ELK Stack
         Shared Monitoring: Prometheus
```

### Scaling Features
- Redis backend for workflow state (cluster-safe)
- Multiple Uvicorn workers per instance
- Load balancer at Caddy level
- Monitoring with Prometheus + Grafana
- Rate limiting per bearer token
- Request queuing if overload detected

---

## Dependency Graph (Implementation Order)

```
1. PREREQUISITES (No changes needed)
   ✓ Orchestration framework exists
   ✓ LLM providers available
   ✓ Data fetching clients ready
   ✓ Service manager running
   ✓ Caddy configured

2. PHASE 1: Server Implementation
   └─ CREATE: http_mcp_server.py
      ├─ Tool definitions (7 tools)
      ├─ FastMCP integration
      ├─ Bearer token auth
      ├─ Workflow state mgmt
      └─ Health endpoint

3. PHASE 2: Startup & Environment
   ├─ CREATE: start_mcp_http.sh
   └─ UPDATE: requirements.txt (fastmcp, uvicorn, aiohttp, pydantic)

4. PHASE 3: Configuration
   ├─ UPDATE: service_manager.py (add mcp-orchestrator)
   ├─ UPDATE: /etc/caddy/Caddyfile (add /mcp* route)
   ├─ UPDATE: API_KEYS.md (add MCP_BEARER_TOKEN)
   └─ UPDATE: PORT_ALLOCATION.md (document port 5059)

5. PHASE 4: Testing & Verification
   ├─ Unit tests (tool functions, auth)
   ├─ Integration tests (workflow execution)
   ├─ Manual testing (curl, Claude Desktop)
   └─ Production readiness checks

6. PHASE 5: Documentation
   ├─ UPDATE: /home/coolhand/shared/mcp/CLAUDE.md
   ├─ CREATE: Deployment guide
   └─ CREATE: Troubleshooting guide
```

---

## Production Readiness Checklist

- [ ] Code review (http_mcp_server.py)
- [ ] Security audit (bearer token, input validation)
- [ ] Load testing (max concurrent workflows)
- [ ] Failure scenario testing (service restart, network outage)
- [ ] Monitoring setup (Prometheus metrics)
- [ ] Logging aggregation (ELK or similar)
- [ ] Documentation complete
- [ ] Runbook for on-call
- [ ] Backup strategy for workflow state
- [ ] Disaster recovery plan

---

**Generated**: 2026-02-06
**For**: Dreamwalker MCP Deployment
**Version**: 1.0

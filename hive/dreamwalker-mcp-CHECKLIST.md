# Dreamwalker MCP Deployment Checklist

**Total Tasks**: 47
**Estimated Effort**: 2-3 days
**Status**: PLANNING PHASE

---

## PRE-IMPLEMENTATION REVIEW

- [ ] Read full deployment plan: `/home/coolhand/geepers/hive/dreamwalker-mcp-deployment-plan.md`
- [ ] Review architecture diagram: `/home/coolhand/geepers/hive/dreamwalker-mcp-ARCHITECTURE.md`
- [ ] Understand port allocation: Port 5059 in 5050-5059 range
- [ ] Verify existing MCP infrastructure: `/home/coolhand/shared/mcp/`
- [ ] Confirm Caddy is running: `sudo systemctl status caddy`
- [ ] Confirm service_manager.py exists: `ls /home/coolhand/service_manager.py`
- [ ] Verify API_KEYS.md exists: `ls /home/coolhand/documentation/API_KEYS.md`

---

## PHASE 1: SERVER IMPLEMENTATION (Day 1)

### 1.1 Create FastMCP HTTP Server

**File**: `/home/coolhand/shared/mcp/http_mcp_server.py`

- [ ] Create Python file with shebang: `#!/usr/bin/env python3`
- [ ] Import FastMCP and dependencies
- [ ] Create `mcp_server = Server("dreamwalker-mcp-http")`
- [ ] Implement tool: `dream_orchestrate_research`
  - [ ] Accept parameters: task, belter_count, drummer_count, camina_count, provider, model, stream, webhook_url
  - [ ] Create OrchestratorConfig
  - [ ] Initialize DreamCascadeOrchestrator
  - [ ] Generate task_id
  - [ ] Store in workflow_state
  - [ ] Return task_id, status, stream_url
- [ ] Implement tool: `dream_orchestrate_search`
  - [ ] Accept parameters: task, num_agents, domains, max_parallel, provider, model, stream
  - [ ] Create DreamSwarmOrchestrator
  - [ ] Return task_id, status, stream_url
- [ ] Implement tool: `dreamwalker_status`
  - [ ] Accept task_id parameter
  - [ ] Query workflow_state
  - [ ] Return status, progress, created_at, result
- [ ] Implement tool: `dreamwalker_cancel`
  - [ ] Accept task_id parameter
  - [ ] Update workflow_state[task_id]["status"] = "cancelled"
  - [ ] Return success confirmation
- [ ] Implement tool: `dreamwalker_patterns`
  - [ ] Return list of available patterns with config options
- [ ] Implement tool: `dreamwalker_list_tools`
  - [ ] Accept optional category parameter
  - [ ] Return list of available tools
- [ ] Implement tool: `dreamwalker_execute_tool`
  - [ ] Accept tool_name and tool_args
  - [ ] Dispatch to tool handler
  - [ ] Return execution result
- [ ] Add authentication middleware
  - [ ] Extract Authorization header
  - [ ] Validate bearer token
  - [ ] Return 401 if missing, 403 if invalid
  - [ ] Allow /health endpoint without auth
- [ ] Add health endpoint
  - [ ] GET /health
  - [ ] Return: status, timestamp, service name, active_workflows, memory_usage
- [ ] Add logging
  - [ ] Configure logging to stderr
  - [ ] Log tool calls, errors, workflow lifecycle
- [ ] Add main block
  - [ ] Read MCP_PORT, MCP_HOST, MCP_BEARER_TOKEN from environment
  - [ ] Start Uvicorn server
  - [ ] Log startup message with port info
- [ ] Add docstrings and comments
  - [ ] Module docstring explaining purpose
  - [ ] Function docstrings for all tools
  - [ ] Inline comments for complex logic
- [ ] Test syntax: `python3 -m py_compile http_mcp_server.py`

### 1.2 Update Requirements

**File**: `/home/coolhand/shared/mcp/requirements.txt`

- [ ] Add: `fastmcp>=0.1.0`
- [ ] Add: `uvicorn>=0.24.0`
- [ ] Add: `aiohttp>=3.8.0`
- [ ] Add: `pydantic>=2.0`
- [ ] Run: `pip install -r /home/coolhand/shared/mcp/requirements.txt`
- [ ] Verify installations: `python3 -c "import fastmcp; import uvicorn; import pydantic"`

### 1.3 Create Startup Script

**File**: `/home/coolhand/shared/mcp/start_mcp_http.sh`

- [ ] Create file with shebang: `#!/bin/bash`
- [ ] Add `set -e` for error handling
- [ ] Load API keys: `source /home/coolhand/documentation/API_KEYS.md`
- [ ] Export defaults:
  - [ ] `export MCP_PORT=${MCP_PORT:-5059}`
  - [ ] `export MCP_HOST=${MCP_HOST:-127.0.0.1}`
  - [ ] `export PYTHONPATH=/home/coolhand/shared:$PYTHONPATH`
- [ ] Change directory: `cd /home/coolhand/shared/mcp`
- [ ] Run server: `exec python3 http_mcp_server.py`
- [ ] Make executable: `chmod +x /home/coolhand/shared/mcp/start_mcp_http.sh`
- [ ] Test run: `/home/coolhand/shared/mcp/start_mcp_http.sh` (should start server)
- [ ] Kill with Ctrl+C

---

## PHASE 2: INFRASTRUCTURE INTEGRATION (Day 1-2)

### 2.1 Service Manager Integration

**File**: `/home/coolhand/service_manager.py`

- [ ] Open service_manager.py in editor
- [ ] Locate SERVICES dictionary (around line 20-100)
- [ ] Find last service entry
- [ ] Add new service block:
  ```python
  'mcp-orchestrator': {
      'name': 'Dreamwalker MCP Server',
      'script': '/home/coolhand/shared/mcp/start_mcp_http.sh',
      'working_dir': '/home/coolhand/shared/mcp',
      'port': 5059,
      'health_endpoint': 'http://localhost:5059/health',
      'start_timeout': 15,
      'description': 'Remote MCP server for Dreamwalker orchestrator, accessible from Claude Desktop'
  }
  ```
- [ ] Verify syntax: `python3 service_manager.py status` (should not error)
- [ ] Test new service: `python3 service_manager.py start mcp-orchestrator`
- [ ] Check status: `python3 service_manager.py status`
- [ ] Stop service: `python3 service_manager.py stop mcp-orchestrator`

### 2.2 Bearer Token Generation & Storage

**File**: `/home/coolhand/documentation/API_KEYS.md`

- [ ] Generate token: `python3 -c "import uuid; print(uuid.uuid4().hex)"`
- [ ] Copy output (32-character hex string)
- [ ] Open API_KEYS.md
- [ ] Add section:
  ```
  # MCP Server (Port 5059)
  MCP_BEARER_TOKEN=<paste-hex-string>
  ```
- [ ] Save file
- [ ] Verify readable: `grep MCP_BEARER_TOKEN /home/coolhand/documentation/API_KEYS.md`
- [ ] Note: File should be gitignored (check .gitignore)

### 2.3 Caddy Reverse Proxy Configuration

**File**: `/etc/caddy/Caddyfile`

- [ ] Open Caddyfile: `sudo nano /etc/caddy/Caddyfile`
- [ ] Find section for other routes (look for handle /wordblocks, etc.)
- [ ] Add new block (after wordblocks, before closing):
  ```
  # Dreamwalker MCP Server
  handle /mcp* {
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
- [ ] Save and exit: Ctrl+O, Enter, Ctrl+X
- [ ] Validate config: `sudo caddy validate --config /etc/caddy/Caddyfile`
- [ ] Expected output: "valid"
- [ ] Reload Caddy: `sudo systemctl reload caddy`
- [ ] Check Caddy status: `sudo systemctl status caddy`
- [ ] Monitor Caddy logs: `sudo journalctl -u caddy -n 20`

### 2.4 Port Allocation Documentation

**File**: `/home/coolhand/projects/PORT_ALLOCATION.md`

- [ ] Open PORT_ALLOCATION.md
- [ ] Locate the "Port 5050s Breakdown" section
- [ ] Find "5055: Story Illustrator" entry
- [ ] Add after 5055:
  ```
  | 5059 | Dreamwalker MCP Server | /shared/mcp | /health | https://dr.eamer.dev/mcp | ✅ |
  ```
- [ ] Also update the "Port Ranges" section:
  - [ ] Update "5050-5059: Bluesky and generation tools" to include MCP
- [ ] Save file
- [ ] Verify formatting: `cat /home/coolhand/projects/PORT_ALLOCATION.md | grep -A 2 "5055"`

---

## PHASE 3: TESTING (Day 2)

### 3.1 Unit Testing Setup

**File**: `/home/coolhand/shared/mcp/tests/test_http_mcp_server.py`

- [ ] Create tests directory if not exists: `mkdir -p /home/coolhand/shared/mcp/tests`
- [ ] Create __init__.py: `touch /home/coolhand/shared/mcp/tests/__init__.py`
- [ ] Create test file: `touch /home/coolhand/shared/mcp/tests/test_http_mcp_server.py`
- [ ] Add test imports:
  ```python
  import pytest
  import asyncio
  from http_mcp_server import (
      mcp_server, workflow_state, dream_orchestrate_research,
      dreamwalker_status, dreamwalker_cancel
  )
  ```
- [ ] Write test: `test_dream_research_tool()`
  - [ ] Call dream_orchestrate_research with test parameters
  - [ ] Assert task_id in result
  - [ ] Assert status == "running"
- [ ] Write test: `test_dream_search_tool()`
  - [ ] Similar to research test
- [ ] Write test: `test_status_endpoint()`
  - [ ] Create workflow, get status, verify response
- [ ] Write test: `test_cancel_endpoint()`
  - [ ] Create workflow, cancel it, verify status changes
- [ ] Write test: `test_patterns_endpoint()`
  - [ ] Get patterns, verify list contains dream_cascade and dream_swarm
- [ ] Run tests: `cd /home/coolhand/shared/mcp && pytest tests/test_http_mcp_server.py -v`
- [ ] All tests should pass (green)

### 3.2 Manual Local Testing

**Start server**:
- [ ] `python3 service_manager.py start mcp-orchestrator`
- [ ] Wait 5 seconds for startup
- [ ] Verify running: `lsof -i :5059`

**Test health endpoint** (no auth):
- [ ] `curl http://localhost:5059/health`
- [ ] Expect: `{"status": "healthy", "timestamp": "...", ...}`

**Test with bearer token** (from API_KEYS.md):
- [ ] `export TOKEN=$(grep MCP_BEARER_TOKEN /home/coolhand/documentation/API_KEYS.md | cut -d= -f2)`
- [ ] Echo token to verify: `echo $TOKEN`

**Test tool listing**:
- [ ] `curl -H "Authorization: Bearer $TOKEN" http://localhost:5059/tools`
- [ ] Expect: JSON list of available tools

**Test research workflow**:
- [ ] Create request:
  ```bash
  curl -X POST -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"task":"What is quantum entanglement?","belter_count":1,"drummer_count":1,"camina_count":1}' \
    http://localhost:5059/tools/dream_orchestrate_research
  ```
- [ ] Expect: `{"task_id": "research-...", "status": "running"}`
- [ ] Note the task_id

**Test status checking**:
- [ ] `curl -H "Authorization: Bearer $TOKEN" -d '{"task_id":"research-..."}' http://localhost:5059/tools/dreamwalker_status`
- [ ] Expect: Status response with current state

**Test authentication rejection** (invalid token):
- [ ] `curl -H "Authorization: Bearer invalid" http://localhost:5059/tools/dreamwalker_patterns`
- [ ] Expect: 403 Forbidden

**Test authentication rejection** (missing token):
- [ ] `curl http://localhost:5059/tools/dreamwalker_patterns`
- [ ] Expect: 401 Unauthorized (or allowed if token is "disabled")

**Check logs**:
- [ ] `python3 service_manager.py logs mcp-orchestrator`
- [ ] Should show startup message and request logs

**Stop server**:
- [ ] `python3 service_manager.py stop mcp-orchestrator`
- [ ] Verify stopped: `lsof -i :5059` (should return nothing)

### 3.3 Caddy Routing Testing

- [ ] Start server: `python3 service_manager.py start mcp-orchestrator`
- [ ] Test health via Caddy (HTTPS):
  - [ ] `curl https://dr.eamer.dev/mcp/health`
  - [ ] May show SSL error on first test (self-signed cert expected)
  - [ ] Add `-k` to ignore: `curl -k https://dr.eamer.dev/mcp/health`
  - [ ] Expect: `{"status": "healthy", ...}`
- [ ] Test with bearer token via Caddy:
  - [ ] `curl -k -H "Authorization: Bearer $TOKEN" https://dr.eamer.dev/mcp/tools`
  - [ ] Expect: Tool list
- [ ] Check Caddy logs for any errors:
  - [ ] `sudo journalctl -u caddy -n 20 | grep -i mcp`

### 3.4 Integration Testing

- [ ] Test full workflow execution:
  - [ ] Call dream_orchestrate_research
  - [ ] Poll dreamwalker_status every 5 seconds
  - [ ] Wait for completion or timeout after 2 minutes
  - [ ] Verify result contains expected data
- [ ] Test error handling:
  - [ ] Missing required parameters → 400 Bad Request
  - [ ] Invalid provider name → Error response
  - [ ] Non-existent task_id → Appropriate error
- [ ] Test concurrent workflows:
  - [ ] Start 3 workflows rapidly
  - [ ] Verify all tracked independently
  - [ ] Status queries work for all

---

## PHASE 4: CLAUDE DESKTOP INTEGRATION (Day 2-3)

### 4.1 Update Cursor/Claude Config

**File**: `~/.cursor/mcp_config.json` or `~/.config/Claude/claude_desktop_config.json`

- [ ] Locate config file (path depends on OS and installation)
- [ ] Open in editor
- [ ] Locate or create "mcpServers" section
- [ ] Add/update dreamwalker server:
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
          "MCP_BEARER_TOKEN": "paste-token-here"
        }
      }
    }
  }
  ```
- [ ] Save file
- [ ] Restart Claude Desktop / Cursor (fully close and reopen)

### 4.2 Test Tool Discovery

- [ ] In Claude Desktop, open a conversation
- [ ] Try to use a tool: `@tools show me available patterns`
- [ ] Should list dream_cascade and dream_swarm patterns
- [ ] If not working, check Claude Desktop logs

### 4.3 Test Tool Execution

- [ ] Try command: `@tools can you research quantum computing using Dream Cascade?`
- [ ] Claude should call the tool
- [ ] Should return task_id and status: "running"
- [ ] Monitor server logs: `sm logs mcp-orchestrator`
- [ ] Should see request logs

### 4.4 Test Status Polling

- [ ] After research tool called, ask: `@tools what's the status of that workflow?`
- [ ] Claude should call dreamwalker_status
- [ ] Should show progress and current stage

### 4.5 Troubleshooting

If tools don't appear:
- [ ] Check Config file syntax (JSON valid?)
- [ ] Restart Claude Desktop completely
- [ ] Check server logs: `sm logs mcp-orchestrator`
- [ ] Test bridge directly: `python3 mcp_http_bridge.py`

If authorization fails:
- [ ] Verify bearer token in config matches API_KEYS.md
- [ ] Test with curl directly: `curl -H "Authorization: Bearer $TOKEN" https://dr.eamer.dev/mcp/health`
- [ ] Check Caddy logs: `sudo journalctl -u caddy -n 50`

---

## PHASE 5: PRODUCTION HARDENING (Day 3)

### 5.1 Security Audit

- [ ] Bearer token not in code (check http_mcp_server.py for hardcoded tokens)
- [ ] Bearer token loaded from environment only
- [ ] Authentication required for all non-health endpoints
- [ ] Input validation on all tool parameters
- [ ] No SQL injection vectors (no SQL used)
- [ ] No command injection vectors (check subprocess usage)
- [ ] Error messages don't leak sensitive info

### 5.2 Performance Testing

- [ ] Load test: 10 concurrent workflow requests
  - [ ] Server should handle without crashing
  - [ ] Response times remain reasonable
- [ ] Stress test: 100 status check requests
  - [ ] Server stays responsive
- [ ] Memory check: `ps aux | grep http_mcp_server`
  - [ ] Memory usage stable over time
  - [ ] No memory leak indicators

### 5.3 Failure Scenario Testing

**Restart resilience**:
- [ ] Start server
- [ ] Start multiple workflows
- [ ] Kill server: `sm stop mcp-orchestrator`
- [ ] Restart server: `sm start mcp-orchestrator`
- [ ] Note: Workflow state lost (expected for MVP)
- [ ] For production, add Redis persistence

**Network interruption**:
- [ ] During workflow execution, simulate network issue (or test locally)
- [ ] Restart service
- [ ] Verify graceful handling

**Invalid configuration**:
- [ ] Set invalid API key
- [ ] Try to start workflow
- [ ] Should return appropriate error
- [ ] Server should remain running

### 5.4 Monitoring & Alerting Setup

- [ ] Add Prometheus metrics (optional but recommended):
  - [ ] Request count by tool
  - [ ] Request latency histogram
  - [ ] Active workflows gauge
  - [ ] Workflow success/failure ratio
- [ ] Add basic alerting:
  - [ ] Service manager health check fails → Alert
  - [ ] Health endpoint returns error → Alert
  - [ ] Response time exceeds 30s → Alert
- [ ] Test alerts by simulating failure conditions

### 5.5 Documentation Updates

**File**: `/home/coolhand/shared/mcp/CLAUDE.md`

- [ ] Add HTTP server section
- [ ] Document tools and parameters
- [ ] Add usage examples
- [ ] Include troubleshooting section
- [ ] Add deployment instructions

**File**: New operational runbook

- [ ] Create: `/home/coolhand/geepers/runbooks/mcp-orchestrator-runbook.md`
- [ ] Document common operations:
  - [ ] Starting/stopping service
  - [ ] Viewing logs
  - [ ] Checking health
  - [ ] Rotating bearer token
  - [ ] Recovering from failures
  - [ ] Scaling considerations

---

## VERIFICATION & SIGN-OFF

### Final Checklist

- [ ] All 47 tasks completed
- [ ] All tests passing
- [ ] Service starts successfully: `sm start mcp-orchestrator` → status running
- [ ] Health check works: `curl https://dr.eamer.dev/mcp/health` → 200 OK
- [ ] Authentication enforced: No token → 401, Invalid token → 403
- [ ] Claude Desktop can discover tools
- [ ] Claude Desktop can execute tools
- [ ] Service manager monitoring works
- [ ] Logs are clean (no errors)
- [ ] Documentation complete
- [ ] No breaking changes to existing services
- [ ] Caddy still routing other services correctly

### Sign-Off

- [ ] Implementation reviewer approves code
- [ ] Security reviewer approves authentication
- [ ] Operations reviewer approves service integration
- [ ] Deployment date scheduled
- [ ] Rollback plan documented and tested
- [ ] Status: READY FOR PRODUCTION

---

## QUICK COMMANDS REFERENCE

```bash
# Verification
lsof -i :5059                                    # Check port in use
python3 service_manager.py status               # Check service
sudo systemctl status caddy                     # Check Caddy
curl http://localhost:5059/health               # Test health
curl https://dr.eamer.dev/mcp/health -k        # Test via Caddy

# Startup/Shutdown
python3 service_manager.py start mcp-orchestrator
python3 service_manager.py stop mcp-orchestrator
python3 service_manager.py restart mcp-orchestrator

# Logs
python3 service_manager.py logs mcp-orchestrator
sudo journalctl -u caddy -f                     # Caddy logs

# Testing
export TOKEN=$(grep MCP_BEARER_TOKEN /home/coolhand/documentation/API_KEYS.md | cut -d= -f2)
curl -H "Authorization: Bearer $TOKEN" http://localhost:5059/tools
curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"task":"Test"}' http://localhost:5059/tools/dream_orchestrate_research

# Configuration
nano /home/coolhand/service_manager.py          # Add service
sudo nano /etc/caddy/Caddyfile                  # Add route
sudo caddy validate --config /etc/caddy/Caddyfile
nano /home/coolhand/documentation/API_KEYS.md   # Bearer token
```

---

**Document Version**: 1.0
**Status**: PLANNING PHASE - READY FOR IMPLEMENTATION
**Last Updated**: 2026-02-06
**Estimated Completion**: Within 2-3 days

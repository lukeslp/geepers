#!/usr/bin/env python3
import sys
import json
import asyncio
import traceback
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add project root to path
script_dir = Path(__file__).parent
project_root = script_dir.parent
sys.path.append(str(project_root))

from src.core.orchestration.cascade import DreamCascadeOrchestrator, OrchestratorConfig

class OrchestrationMCPServer:
    """MCP Server for the Orchestration Skill."""

    def __init__(self):
        self.orchestrator = None

    async def run(self):
        """Run the server loop reading from stdin and writing to stdout."""
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break
                
                request = json.loads(line)
                method = request.get("method")
                params = request.get("params", {})
                request_id = request.get("id")

                if method == "initialize":
                    response = self._handle_initialize(request_id)
                elif method == "tools/list":
                    response = self._handle_tool_list(request_id)
                elif method == "tools/call":
                    response = await self._handle_tool_call(request_id, params)
                else:
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {"code": -32601, "message": f"Method not found: {method}"}
                    }

                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()

            except EOFError:
                break
            except Exception as e:
                # Log to stderr since stdout is for JSON-RPC
                print(f"Error: {traceback.format_exc()}", file=sys.stderr)

    def _handle_initialize(self, request_id):
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "geepers-mcp-orchestration",
                    "version": "1.0.0"
                }
            }
        }

    def _handle_tool_list(self, request_id):
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": [
                    {
                        "name": "dream_orchestrate_research",
                        "description": "Start a hierarchical 3-tier research workflow (Dream Cascade).",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "task": {"type": "string", "description": "The research topic or question."},
                                "num_agents": {"type": "integer", "description": "Number of Belter agents (total workers).", "default": 5},
                                "enable_drummer": {"type": "boolean", "description": "Enable synthesis tier.", "default": True},
                                "enable_camina": {"type": "boolean", "description": "Enable executive tier.", "default": False},
                                "provider_name": {"type": "string", "description": "LLM provider name.", "default": "anthropic"}
                            },
                            "required": ["task"]
                        }
                    }
                ]
            }
        }

    async def _handle_tool_call(self, request_id, params):
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        if tool_name == "dream_orchestrate_research":
            task = arguments.get("task")
            num_agents = arguments.get("num_agents", 5)
            enable_drummer = arguments.get("enable_drummer", True)
            enable_camina = arguments.get("enable_camina", False)
            provider_name = arguments.get("provider_name", "anthropic")

            try:
                config = OrchestratorConfig(
                    num_agents=num_agents,
                    enable_drummer=enable_drummer,
                    enable_camina=enable_camina
                )
                
                orchestrator = DreamCascadeOrchestrator(
                    provider_name=provider_name,
                    config=config
                )

                # Execute
                result = await orchestrator.execute_task(task)
                
                # Format response content
                content_text = f"Orchestration Summary for: {task}\n"
                content_text += f"Status: COMPLETED\n"
                content_text += f"Total Agents: {result['total_agents']}\n"
                
                if result.get('camina_response'):
                    content_text += f"\nExecutive Summary:\n{result['camina_response'].content}\n"
                elif result['drummer_responses']:
                    content_text += f"\nSynthesis Findings:\n"
                    for i, r in enumerate(result['drummer_responses']):
                        content_text += f"[{i+1}] {r.content[:500]}...\n"
                
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                                {
                                    "type": "text",
                                    "text": content_text
                                }
                        ]
                    }
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32603, "message": f"Execution failed: {str(e)}"}
                }
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32601, "message": f"Tool not found: {tool_name}"}
            }

if __name__ == "__main__":
    server = OrchestrationMCPServer()
    asyncio.run(server.run())

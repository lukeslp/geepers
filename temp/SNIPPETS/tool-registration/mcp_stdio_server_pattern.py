#!/usr/bin/env python3
# ================================================
# MCP Stdio Server Pattern
# ================================================
# Language: python
# Tags: mcp, protocol, stdio, server, orchestration
# Source: geepers-orchestrators/mcp/stdio_servers/checkpoint_stdio.py
# Last Updated: 2025-12-12
# Author: Luke Steuber
# ================================================
# Description:
# Complete implementation pattern for MCP (Model Context Protocol) stdio servers.
# Enables tools to be exposed via Claude Code marketplace or other MCP clients.
# Handles JSON-RPC protocol, initialization handshake, tool registration, and
# asynchronous tool execution over stdin/stdout.
#
# Use Cases:
# - Exposing custom tools to Claude Code
# - Creating marketplace-ready MCP servers
# - Building orchestration systems accessible via MCP
# - Wrapping existing Python functionality as MCP tools
#
# Dependencies:
# - asyncio (built-in)
# - json (built-in)
# - logging (built-in)
# - sys (built-in)
#
# Notes:
# - Logging must go to stderr (stdout is reserved for MCP protocol)
# - Implements MCP protocol version 2024-11-05
# - Supports JSON-RPC 2.0 format
# - Tool calls return structured responses with content arrays
# - Initialize handshake required before tool calls
#
# Related Snippets:
# - /home/coolhand/SNIPPETS/tool-registration/swarm_module_pattern.py
# - /home/coolhand/SNIPPETS/async-patterns/concurrent_task_execution.py
# ================================================

import asyncio
import json
import logging
import sys
from typing import Any, Dict, Optional, List

# Configure logging to stderr (stdout is for MCP protocol)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)


# ============================================================================
# MCP PROTOCOL CONSTANTS
# ============================================================================

PROTOCOL_VERSION = "2024-11-05"


# ============================================================================
# JSON-RPC HELPERS
# ============================================================================

def create_mcp_response(request_id: Any, result: Any) -> Dict[str, Any]:
    """Create a JSON-RPC 2.0 success response."""
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": result,
    }


def create_mcp_error(request_id: Any, code: int, message: str) -> Dict[str, Any]:
    """
    Create a JSON-RPC 2.0 error response.

    Standard error codes:
    - -32700: Parse error
    - -32600: Invalid request
    - -32601: Method not found
    - -32602: Invalid params
    - -32603: Internal error
    - -32002: Server not initialized
    """
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {
            "code": code,
            "message": message,
        },
    }


# ============================================================================
# ABSTRACT BASE MCP SERVER
# ============================================================================

class BaseMCPServer:
    """
    Abstract base class for MCP stdio servers.

    Subclass this and implement:
    - get_server_info(): Return server name and version
    - get_tools_manifest(): Return list of tool definitions
    - handle_tool_call(): Execute tool and return result
    """

    def __init__(self):
        """Initialize the MCP server."""
        self.initialized = False

    def get_server_info(self) -> Dict[str, str]:
        """
        Return server information.

        Returns:
            Dict with 'name' and 'version' keys
        """
        return {
            "name": "example-mcp-server",
            "version": "1.0.0",
        }

    def get_capabilities(self) -> Dict[str, Any]:
        """
        Return server capabilities.

        Standard capabilities:
        - tools: Server supports tool calls
        - prompts: Server supports prompt templates
        - resources: Server supports resource access
        """
        return {
            "tools": {},  # We support tools
        }

    def get_tools_manifest(self) -> List[Dict[str, Any]]:
        """
        Return list of available tools.

        Each tool should have:
        - name: Unique tool identifier
        - description: Human-readable description
        - inputSchema: JSON Schema for parameters

        Returns:
            List of tool definitions
        """
        return [
            {
                "name": "example_tool",
                "description": "Example tool that echoes input",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "Message to echo",
                        },
                    },
                    "required": ["message"],
                },
            }
        ]

    async def handle_tool_call(
        self, tool_name: str, arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle a tool call and return result.

        Args:
            tool_name: Name of the tool being called
            arguments: Tool arguments from client

        Returns:
            Result dict with 'content' array and optional 'isError' flag
        """
        # Example implementation
        if tool_name == "example_tool":
            message = arguments.get("message", "")
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Echo: {message}",
                    }
                ]
            }

        # Tool not found
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Unknown tool: {tool_name}",
                }
            ],
            "isError": True,
        }

    async def handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Handle an incoming MCP request.

        Args:
            request: JSON-RPC request dict

        Returns:
            JSON-RPC response or None for notifications
        """
        method = request.get("method", "")
        params = request.get("params", {})
        request_id = request.get("id")

        logger.debug(f"Handling request: {method}")

        try:
            # Initialization handshake
            if method == "initialize":
                self.initialized = True
                return create_mcp_response(request_id, {
                    "protocolVersion": PROTOCOL_VERSION,
                    "capabilities": self.get_capabilities(),
                    "serverInfo": self.get_server_info(),
                })

            # Initialized notification (no response needed)
            if method == "notifications/initialized":
                logger.info("Client initialized")
                return None

            # Check initialization for other methods
            if not self.initialized and method not in ["initialize"]:
                return create_mcp_error(
                    request_id,
                    -32002,
                    "Server not initialized"
                )

            # Tools list
            if method == "tools/list":
                return create_mcp_response(request_id, {
                    "tools": self.get_tools_manifest()
                })

            # Tool call
            if method == "tools/call":
                tool_name = params.get("name", "")
                arguments = params.get("arguments", {})

                try:
                    result = await self.handle_tool_call(tool_name, arguments)
                    return create_mcp_response(request_id, result)
                except Exception as e:
                    logger.error(f"Tool call failed: {e}")
                    return create_mcp_response(request_id, {
                        "content": [
                            {
                                "type": "text",
                                "text": f"Error: {str(e)}",
                            }
                        ],
                        "isError": True,
                    })

            # Ping
            if method == "ping":
                return create_mcp_response(request_id, {})

            # Unknown method
            return create_mcp_error(
                request_id,
                -32601,
                f"Method not found: {method}"
            )

        except Exception as e:
            logger.error(f"Request handling failed: {e}")
            return create_mcp_error(
                request_id,
                -32603,
                f"Internal error: {str(e)}"
            )


# ============================================================================
# STDIO SERVER RUNNER
# ============================================================================

async def run_mcp_stdio_server(server: BaseMCPServer):
    """
    Run an MCP server using stdio transport.

    Reads JSON-RPC requests from stdin, writes responses to stdout.
    Logging goes to stderr.

    Args:
        server: BaseMCPServer instance to run
    """
    logger.info(f"Starting MCP server: {server.get_server_info()['name']}")

    # Set up stdio streams
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    await asyncio.get_event_loop().connect_read_pipe(lambda: protocol, sys.stdin)

    writer_transport, writer_protocol = await asyncio.get_event_loop().connect_write_pipe(
        asyncio.streams.FlowControlMixin, sys.stdout
    )
    writer = asyncio.StreamWriter(writer_transport, writer_protocol, None, asyncio.get_event_loop())

    try:
        while True:
            # Read a line from stdin
            line = await reader.readline()
            if not line:
                logger.info("EOF received, shutting down")
                break

            line = line.decode('utf-8').strip()
            if not line:
                continue

            logger.debug(f"Received: {line[:100]}...")

            # Parse JSON-RPC request
            try:
                request = json.loads(line)
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON: {e}")
                error = create_mcp_error(None, -32700, f"Parse error: {e}")
                writer.write((json.dumps(error) + '\n').encode('utf-8'))
                await writer.drain()
                continue

            # Handle the request
            response = await server.handle_request(request)

            # Send response (if not a notification)
            if response is not None:
                response_str = json.dumps(response) + '\n'
                writer.write(response_str.encode('utf-8'))
                await writer.drain()
                logger.debug(f"Sent response for {request.get('method')}")

    except asyncio.CancelledError:
        logger.info("Server cancelled")
    except Exception as e:
        logger.error(f"Server error: {e}")
    finally:
        logger.info("Server shutting down")


# ============================================================================
# EXAMPLE IMPLEMENTATION
# ============================================================================

class ExampleMCPServer(BaseMCPServer):
    """Example MCP server with multiple tools."""

    def get_server_info(self) -> Dict[str, str]:
        return {
            "name": "example-mcp-server",
            "version": "1.0.0",
        }

    def get_tools_manifest(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "echo",
                "description": "Echo a message back to the caller",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "Message to echo",
                        },
                    },
                    "required": ["message"],
                },
            },
            {
                "name": "add",
                "description": "Add two numbers together",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "a": {
                            "type": "number",
                            "description": "First number",
                        },
                        "b": {
                            "type": "number",
                            "description": "Second number",
                        },
                    },
                    "required": ["a", "b"],
                },
            },
        ]

    async def handle_tool_call(
        self, tool_name: str, arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle tool calls for echo and add."""

        if tool_name == "echo":
            message = arguments.get("message", "")
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Echo: {message}",
                    }
                ]
            }

        elif tool_name == "add":
            a = arguments.get("a", 0)
            b = arguments.get("b", 0)
            result = a + b
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"{a} + {b} = {result}",
                    }
                ]
            }

        else:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Unknown tool: {tool_name}",
                    }
                ],
                "isError": True,
            }


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

def main():
    """Entry point for the MCP server."""
    server = ExampleMCPServer()

    try:
        asyncio.run(run_mcp_stdio_server(server))
    except KeyboardInterrupt:
        logger.info("Interrupted")


if __name__ == "__main__":
    main()


# ============================================================================
# TESTING THE SERVER
# ============================================================================

# To test this server locally, save it to a file and run:
#
# 1. Start the server:
#    python mcp_stdio_server_pattern.py
#
# 2. Send requests via stdin (one JSON object per line):
#
#    {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
#    {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}
#    {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
#    {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "echo", "arguments": {"message": "Hello MCP!"}}}
#    {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "add", "arguments": {"a": 5, "b": 3}}}
#
# 3. Observe responses on stdout and logs on stderr
#
# For Claude Code marketplace integration, add to mcp_config.json:
# {
#   "mcpServers": {
#     "example-server": {
#       "command": "python",
#       "args": ["/path/to/mcp_stdio_server_pattern.py"]
#     }
#   }
# }

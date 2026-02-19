#!/usr/bin/env python3
"""
Dream Cascade Research Launcher

Starts a hierarchical 3-tier research workflow via the MCP server.

Usage:
    python cascade-research.py "Research quantum computing applications"
    python cascade-research.py "AI safety" --belters 8 --drummers 3
    python cascade-research.py "Market analysis" --provider anthropic --stream

Author: Luke Steuber
"""

import argparse
import json
import sys
import requests
from typing import Optional

MCP_BASE_URL = "http://localhost:5060"


def start_research(
    task: str,
    belter_count: int = 5,
    drummer_count: int = 2,
    camina_count: int = 1,
    provider: str = "xai",
    model: Optional[str] = None,
    stream: bool = False,
    webhook_url: Optional[str] = None,
    output_format: str = "stdout"
) -> dict:
    """
    Start a Dream Cascade research workflow.

    Args:
        task: Research topic/question
        belter_count: Number of Tier 1 exploration agents (1-10)
        drummer_count: Number of Tier 2 synthesis agents (1-5)
        camina_count: Number of Tier 3 executive agents (1-3)
        provider: LLM provider name
        model: Specific model to use
        stream: Enable SSE streaming
        webhook_url: URL for async notifications
        output_format: Output format (stdout, json, markdown)

    Returns:
        Workflow info dict with task_id, status, etc.
    """
    # Build request payload
    payload = {
        "task": task,
        "num_agents": belter_count,  # Legacy field
        "enable_drummer": drummer_count > 0,
        "enable_camina": camina_count > 0,
        "provider_name": provider,
        "generate_documents": True,
        "document_formats": ["markdown"]
    }

    if model:
        payload["model"] = model
    if webhook_url:
        payload["webhook_url"] = webhook_url

    try:
        response = requests.post(
            f"{MCP_BASE_URL}/mcp",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": "dream_orchestrate_research",
                    "arguments": payload
                }
            },
            timeout=30
        )
        response.raise_for_status()
        result = response.json()

        if "error" in result:
            return {"error": result["error"]["message"]}

        return result.get("result", result)

    except requests.exceptions.ConnectionError:
        return {
            "error": "Cannot connect to MCP server. Start it with: sm start mcp-orchestrator"
        }
    except requests.exceptions.Timeout:
        return {"error": "Request timed out"}
    except Exception as e:
        return {"error": str(e)}


def stream_results(task_id: str):
    """
    Stream SSE events for a running workflow.

    Args:
        task_id: Workflow task ID
    """
    try:
        import sseclient
    except ImportError:
        print("SSE streaming requires sseclient-py: pip install sseclient-py", file=sys.stderr)
        return

    try:
        response = requests.get(
            f"{MCP_BASE_URL}/stream/{task_id}",
            stream=True
        )
        client = sseclient.SSEClient(response)

        for event in client.events():
            if event.event == "task_completed":
                data = json.loads(event.data)
                print(f"\n{'='*60}")
                print("WORKFLOW COMPLETED")
                print('='*60)
                print(json.dumps(data, indent=2))
                break
            elif event.event == "error":
                print(f"Error: {event.data}", file=sys.stderr)
                break
            else:
                print(f"[{event.event}] {event.data}")

    except KeyboardInterrupt:
        print("\nStreaming interrupted")
    except Exception as e:
        print(f"Streaming error: {e}", file=sys.stderr)


def format_output(result: dict, output_format: str) -> str:
    """Format the result for output."""
    if output_format == "json":
        return json.dumps(result, indent=2)
    elif output_format == "markdown":
        lines = [
            f"# Research Results",
            "",
            f"**Task ID**: {result.get('task_id', 'N/A')}",
            f"**Status**: {result.get('status', 'N/A')}",
            ""
        ]
        if "result" in result:
            r = result["result"]
            if isinstance(r, dict):
                if "executive_summary" in r:
                    lines.extend([
                        "## Executive Summary",
                        r["executive_summary"],
                        ""
                    ])
                if "key_findings" in r:
                    lines.extend(["## Key Findings", ""])
                    for finding in r["key_findings"]:
                        lines.append(f"- {finding}")
                    lines.append("")
        return "\n".join(lines)
    else:
        # stdout format - human readable
        lines = [
            f"Task ID: {result.get('task_id', 'N/A')}",
            f"Status: {result.get('status', 'N/A')}"
        ]
        if "stream_url" in result:
            lines.append(f"Stream: {MCP_BASE_URL}{result['stream_url']}")
        if "message" in result:
            lines.append(f"Message: {result['message']}")
        if "error" in result:
            lines.append(f"Error: {result['error']}")
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Launch Dream Cascade hierarchical research workflow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Research quantum computing applications"
  %(prog)s "AI safety implications" --belters 8 --drummers 3
  %(prog)s "Market analysis" --provider anthropic --output json
  %(prog)s "Technical deep dive" --stream
        """
    )

    parser.add_argument(
        "task",
        help="Research topic or question"
    )
    parser.add_argument(
        "--belters", "-b",
        type=int,
        default=5,
        help="Number of Tier 1 exploration agents (1-10, default: 5)"
    )
    parser.add_argument(
        "--drummers", "-d",
        type=int,
        default=2,
        help="Number of Tier 2 synthesis agents (1-5, default: 2)"
    )
    parser.add_argument(
        "--caminas", "-c",
        type=int,
        default=1,
        help="Number of Tier 3 executive agents (1-3, default: 1)"
    )
    parser.add_argument(
        "--provider", "-p",
        default="xai",
        help="LLM provider (xai, anthropic, openai, etc. Default: xai)"
    )
    parser.add_argument(
        "--model", "-m",
        help="Specific model to use (default: provider's default)"
    )
    parser.add_argument(
        "--stream", "-s",
        action="store_true",
        help="Enable real-time SSE streaming"
    )
    parser.add_argument(
        "--webhook",
        help="URL for async completion notifications"
    )
    parser.add_argument(
        "--output", "-o",
        choices=["stdout", "json", "markdown"],
        default="stdout",
        help="Output format (default: stdout)"
    )

    args = parser.parse_args()

    # Validate agent counts
    if not 1 <= args.belters <= 10:
        print("Error: belters must be between 1 and 10", file=sys.stderr)
        sys.exit(1)
    if not 0 <= args.drummers <= 5:
        print("Error: drummers must be between 0 and 5", file=sys.stderr)
        sys.exit(1)
    if not 0 <= args.caminas <= 3:
        print("Error: caminas must be between 0 and 3", file=sys.stderr)
        sys.exit(1)

    print(f"Starting Dream Cascade research workflow...", file=sys.stderr)
    print(f"Topic: {args.task}", file=sys.stderr)
    print(f"Agents: {args.belters} belters, {args.drummers} drummers, {args.caminas} caminas", file=sys.stderr)
    print(f"Provider: {args.provider}", file=sys.stderr)
    print("", file=sys.stderr)

    result = start_research(
        task=args.task,
        belter_count=args.belters,
        drummer_count=args.drummers,
        camina_count=args.caminas,
        provider=args.provider,
        model=args.model,
        stream=args.stream,
        webhook_url=args.webhook,
        output_format=args.output
    )

    # Print formatted output
    print(format_output(result, args.output))

    # If streaming enabled and we got a task_id, stream results
    if args.stream and "task_id" in result and "error" not in result:
        print("\nStreaming results...", file=sys.stderr)
        stream_results(result["task_id"])

    # Exit with error code if there was an error
    if "error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()

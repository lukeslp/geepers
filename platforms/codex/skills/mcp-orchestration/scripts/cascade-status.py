#!/usr/bin/env python3
"""
Dream Cascade Workflow Status Checker

Check the status of running or completed research workflows.

Usage:
    python cascade-status.py workflow-abc123
    python cascade-status.py --list
    python cascade-status.py workflow-abc123 --cancel

Author: Luke Steuber
"""

import argparse
import json
import sys
import requests

MCP_BASE_URL = "http://localhost:5060"


def get_status(task_id: str) -> dict:
    """
    Get status of a specific workflow.

    Args:
        task_id: Workflow task ID

    Returns:
        Status dict with progress, results, etc.
    """
    try:
        response = requests.post(
            f"{MCP_BASE_URL}/mcp",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": "dreamwalker_status",
                    "arguments": {"task_id": task_id}
                }
            },
            timeout=10
        )
        response.raise_for_status()
        result = response.json()

        if "error" in result:
            return {"error": result["error"]["message"]}

        return result.get("result", result)

    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to MCP server. Start with: sm start mcp-orchestrator"}
    except Exception as e:
        return {"error": str(e)}


def cancel_workflow(task_id: str) -> dict:
    """
    Cancel a running workflow.

    Args:
        task_id: Workflow task ID

    Returns:
        Cancellation result
    """
    try:
        response = requests.post(
            f"{MCP_BASE_URL}/mcp",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": "dreamwalker_cancel",
                    "arguments": {"task_id": task_id}
                }
            },
            timeout=10
        )
        response.raise_for_status()
        result = response.json()

        if "error" in result:
            return {"error": result["error"]["message"]}

        return result.get("result", result)

    except Exception as e:
        return {"error": str(e)}


def list_patterns() -> dict:
    """List available orchestrator patterns."""
    try:
        response = requests.post(
            f"{MCP_BASE_URL}/mcp",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": "dreamwalker_patterns",
                    "arguments": {}
                }
            },
            timeout=10
        )
        response.raise_for_status()
        result = response.json()

        if "error" in result:
            return {"error": result["error"]["message"]}

        return result.get("result", result)

    except Exception as e:
        return {"error": str(e)}


def format_status(status: dict) -> str:
    """Format status for human-readable output."""
    if "error" in status:
        return f"Error: {status['error']}"

    lines = [
        f"Task ID: {status.get('task_id', 'N/A')}",
        f"Status: {status.get('status', 'N/A')}",
    ]

    if "progress" in status:
        lines.append(f"Progress: {status['progress']}%")

    if "started_at" in status:
        lines.append(f"Started: {status['started_at']}")

    if "current_stage" in status:
        lines.append(f"Current Stage: {status['current_stage']}")

    if "agent_results" in status and status["agent_results"]:
        lines.append(f"Completed Agents: {len(status['agent_results'])}")

    if "result" in status and status["result"]:
        lines.append("")
        lines.append("Results available. Use --json for full output.")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Check status of Dream Cascade workflows",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s workflow-abc123              # Check specific workflow
  %(prog)s workflow-abc123 --json       # Full JSON output
  %(prog)s workflow-abc123 --cancel     # Cancel workflow
  %(prog)s --patterns                   # List orchestrator patterns
        """
    )

    parser.add_argument(
        "task_id",
        nargs="?",
        help="Workflow task ID to check"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output full JSON response"
    )
    parser.add_argument(
        "--cancel",
        action="store_true",
        help="Cancel the specified workflow"
    )
    parser.add_argument(
        "--patterns",
        action="store_true",
        help="List available orchestrator patterns"
    )

    args = parser.parse_args()

    if args.patterns:
        result = list_patterns()
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if "error" in result:
                print(f"Error: {result['error']}", file=sys.stderr)
                sys.exit(1)
            print("Available Orchestrator Patterns:")
            print("="*40)
            for pattern in result.get("patterns", []):
                print(f"\n{pattern.get('name', 'Unknown')}")
                print(f"  {pattern.get('description', 'No description')}")
        sys.exit(0)

    if not args.task_id:
        parser.print_help()
        print("\nError: task_id required (or use --patterns)", file=sys.stderr)
        sys.exit(1)

    if args.cancel:
        result = cancel_workflow(args.task_id)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if "error" in result:
                print(f"Error: {result['error']}", file=sys.stderr)
                sys.exit(1)
            print(f"Workflow {args.task_id} cancelled successfully")
    else:
        result = get_status(args.task_id)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(format_status(result))
            if "error" in result:
                sys.exit(1)


if __name__ == "__main__":
    main()

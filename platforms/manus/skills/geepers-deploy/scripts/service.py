#!/usr/bin/env python3
"""
Service Manager CLI Wrapper

Wrapper around the sm (service_manager) CLI for managing server services.

Usage:
    python service.py status
    python service.py start wordblocks
    python service.py stop wordblocks
    python service.py restart wordblocks
    python service.py logs wordblocks
    python service.py ports

Author: Luke Steuber
"""

import argparse
import subprocess
import sys
import json
from typing import Optional

SM_PATH = "/home/coolhand/service_manager.py"


def run_sm(command: str, service: Optional[str] = None, extra_args: list = None) -> dict:
    """
    Run a service manager command.

    Args:
        command: SM command (status, start, stop, restart, logs)
        service: Optional service name
        extra_args: Additional arguments

    Returns:
        Result dict with output and status
    """
    cmd = ["python3", SM_PATH, command]

    if service:
        cmd.append(service)

    if extra_args:
        cmd.extend(extra_args)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Command timed out"}
    except FileNotFoundError:
        return {"success": False, "error": f"Service manager not found at {SM_PATH}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def status(service: Optional[str] = None, json_output: bool = False) -> str:
    """Get service status."""
    result = run_sm("status", service)

    if not result["success"]:
        return f"Error: {result['error']}"

    if json_output:
        # Parse output into JSON
        lines = result["output"].strip().split("\n")
        services = []
        for line in lines:
            if ":" in line and not line.startswith(" "):
                parts = line.split(":")
                if len(parts) >= 2:
                    name = parts[0].strip()
                    status = parts[1].strip()
                    services.append({"name": name, "status": status})
        return json.dumps(services, indent=2)

    return result["output"]


def start(service: str) -> str:
    """Start a service."""
    if not service:
        return "Error: Service name required"

    result = run_sm("start", service)

    if result["success"]:
        return f"Service '{service}' started successfully"
    else:
        return f"Failed to start '{service}': {result['error']}"


def stop(service: str) -> str:
    """Stop a service."""
    if not service:
        return "Error: Service name required"

    result = run_sm("stop", service)

    if result["success"]:
        return f"Service '{service}' stopped successfully"
    else:
        return f"Failed to stop '{service}': {result['error']}"


def restart(service: str) -> str:
    """Restart a service."""
    if not service:
        return "Error: Service name required"

    result = run_sm("restart", service)

    if result["success"]:
        return f"Service '{service}' restarted successfully"
    else:
        return f"Failed to restart '{service}': {result['error']}"


def logs(service: str, tail: int = 50, follow: bool = False) -> str:
    """Get service logs."""
    if not service:
        return "Error: Service name required"

    extra_args = []
    if tail:
        extra_args.extend(["--tail", str(tail)])
    if follow:
        extra_args.append("--follow")

    result = run_sm("logs", service, extra_args)

    if result["success"]:
        return result["output"]
    else:
        return f"Failed to get logs for '{service}': {result['error']}"


def ports() -> str:
    """List port allocations."""
    result = run_sm("status")

    if not result["success"]:
        return f"Error: {result['error']}"

    # Parse and format port info
    lines = ["Port Allocations:", "=" * 40]
    output_lines = result["output"].strip().split("\n")

    for line in output_lines:
        if "port" in line.lower() or any(c.isdigit() for c in line):
            lines.append(line)

    if len(lines) == 2:
        lines.append("(No port information available)")

    return "\n".join(lines)


def health(service: Optional[str] = None) -> str:
    """Check service health."""
    result = run_sm("status", service)

    if not result["success"]:
        return f"Error: {result['error']}"

    lines = ["Health Check:", "=" * 40]

    # Check for running/stopped in output
    running = 0
    stopped = 0

    for line in result["output"].split("\n"):
        if "running" in line.lower():
            running += 1
            lines.append(f"✓ {line.strip()}")
        elif "stopped" in line.lower() or "not running" in line.lower():
            stopped += 1
            lines.append(f"✗ {line.strip()}")

    lines.append("")
    lines.append(f"Summary: {running} running, {stopped} stopped")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Service manager CLI wrapper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s status                  # All services
  %(prog)s status wordblocks       # Specific service
  %(prog)s start wordblocks        # Start service
  %(prog)s stop wordblocks         # Stop service
  %(prog)s restart wordblocks      # Restart service
  %(prog)s logs wordblocks         # View logs
  %(prog)s logs wordblocks --tail 100  # Last 100 lines
  %(prog)s ports                   # List port allocations
  %(prog)s health                  # Health check all
        """
    )

    parser.add_argument(
        "command",
        choices=["status", "start", "stop", "restart", "logs", "ports", "health"],
        help="Command to run"
    )
    parser.add_argument(
        "service",
        nargs="?",
        help="Service name (required for start/stop/restart/logs)"
    )
    parser.add_argument(
        "--tail", "-t",
        type=int,
        default=50,
        help="Number of log lines (default: 50)"
    )
    parser.add_argument(
        "--follow", "-f",
        action="store_true",
        help="Follow log output"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output as JSON"
    )

    args = parser.parse_args()

    if args.command == "status":
        print(status(args.service, args.json))
    elif args.command == "start":
        print(start(args.service))
    elif args.command == "stop":
        print(stop(args.service))
    elif args.command == "restart":
        print(restart(args.service))
    elif args.command == "logs":
        print(logs(args.service, args.tail, args.follow))
    elif args.command == "ports":
        print(ports())
    elif args.command == "health":
        print(health(args.service))


if __name__ == "__main__":
    main()

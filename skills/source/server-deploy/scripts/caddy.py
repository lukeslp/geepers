#!/usr/bin/env python3
"""
Caddy Configuration Utility - READ-ONLY Operations

This script provides read-only access to Caddy configuration for validation
and status checking. It does NOT modify the Caddyfile.

IMPORTANT: All route modifications MUST go through @geepers_caddy agent.
This script is for viewing and validation only.

Commands:
    validate    - Validate Caddy configuration syntax
    status      - Show Caddy service status
    routes      - List all configured routes
    ports       - List all ports in use by Caddy
    domains     - List all domains configured
    help        - Show this help message

Author: Luke Steuber
"""

import subprocess
import sys
import re
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

# Configuration
CADDYFILE_PATH = "/etc/caddy/Caddyfile"
SUDO_PASSWORD = "G@nym3de"

# ANSI colors for terminal output
class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"


def print_warning_banner():
    """Print a warning that this is read-only."""
    print(f"\n{Colors.YELLOW}{Colors.BOLD}{'=' * 70}{Colors.RESET}")
    print(f"{Colors.YELLOW}{Colors.BOLD}  READ-ONLY MODE - No modifications allowed{Colors.RESET}")
    print(f"{Colors.YELLOW}  To add/modify routes, use: @geepers_caddy agent{Colors.RESET}")
    print(f"{Colors.YELLOW}{Colors.BOLD}{'=' * 70}{Colors.RESET}\n")


def run_sudo_command(command: list[str], capture_output: bool = True) -> subprocess.CompletedProcess:
    """Run a command with sudo, providing password via stdin."""
    full_command = ["sudo", "-S"] + command
    return subprocess.run(
        full_command,
        input=f"{SUDO_PASSWORD}\n",
        capture_output=capture_output,
        text=True
    )


def read_caddyfile() -> Optional[str]:
    """Read the Caddyfile contents."""
    result = run_sudo_command(["cat", CADDYFILE_PATH])
    if result.returncode == 0:
        return result.stdout
    print(f"{Colors.RED}Error reading Caddyfile: {result.stderr}{Colors.RESET}")
    return None


@dataclass
class Route:
    """Represents a parsed route from the Caddyfile."""
    path: str
    port: Optional[int]
    route_type: str  # handle, handle_path, reverse_proxy, file_server, redir
    domain: str = "dr.eamer.dev"
    notes: str = ""


def parse_routes(caddyfile_content: str) -> list[Route]:
    """Parse routes from Caddyfile content."""
    routes = []
    current_domain = None

    lines = caddyfile_content.split('\n')

    # Domain patterns
    domain_pattern = re.compile(r'^([a-zA-Z0-9._-]+\.(?:com|dev|org)(?:,\s*[a-zA-Z0-9._-]+\.(?:com|dev|org))*)\s*\{')

    # Route patterns
    handle_path_pattern = re.compile(r'handle_path\s+(/[^\s{]+)')
    handle_pattern = re.compile(r'handle\s+(/[^\s{]+)')
    reverse_proxy_pattern = re.compile(r'reverse_proxy\s+localhost:(\d+)')
    redir_pattern = re.compile(r'redir\s+([^\s]+)')

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Check for domain block
        domain_match = domain_pattern.match(stripped)
        if domain_match:
            current_domain = domain_match.group(1).split(',')[0].strip()
            continue

        # Check for handle_path
        hp_match = handle_path_pattern.search(stripped)
        if hp_match:
            path = hp_match.group(1)
            # Look for reverse_proxy in next few lines
            port = None
            for j in range(i, min(i + 5, len(lines))):
                rp_match = reverse_proxy_pattern.search(lines[j])
                if rp_match:
                    port = int(rp_match.group(1))
                    break
            routes.append(Route(
                path=path,
                port=port,
                route_type="handle_path",
                domain=current_domain or "dr.eamer.dev"
            ))
            continue

        # Check for handle (but not handle_path or handle_errors)
        if stripped.startswith('handle ') and not stripped.startswith('handle_errors'):
            h_match = handle_pattern.search(stripped)
            if h_match:
                path = h_match.group(1)
                # Look for reverse_proxy in next few lines
                port = None
                for j in range(i, min(i + 10, len(lines))):
                    rp_match = reverse_proxy_pattern.search(lines[j])
                    if rp_match:
                        port = int(rp_match.group(1))
                        break
                    # Check for file_server
                    if 'file_server' in lines[j]:
                        routes.append(Route(
                            path=path,
                            port=None,
                            route_type="file_server",
                            domain=current_domain or "dr.eamer.dev"
                        ))
                        break
                else:
                    if port:
                        routes.append(Route(
                            path=path,
                            port=port,
                            route_type="handle",
                            domain=current_domain or "dr.eamer.dev"
                        ))

    return routes


def extract_port_mappings(caddyfile_content: str) -> dict[int, list[str]]:
    """Extract port to path mappings from Caddyfile."""
    port_mappings: dict[int, list[str]] = {}

    lines = caddyfile_content.split('\n')
    current_path = None

    path_pattern = re.compile(r'handle(?:_path)?\s+(/[^\s{]+)')
    proxy_pattern = re.compile(r'reverse_proxy\s+localhost:(\d+)')

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Track current path context
        path_match = path_pattern.search(stripped)
        if path_match:
            current_path = path_match.group(1)

        # Find reverse_proxy lines
        proxy_match = proxy_pattern.search(stripped)
        if proxy_match:
            port = int(proxy_match.group(1))
            path = current_path or "/"

            if port not in port_mappings:
                port_mappings[port] = []
            if path not in port_mappings[port]:
                port_mappings[port].append(path)

    return port_mappings


def extract_domains(caddyfile_content: str) -> list[tuple[str, str]]:
    """Extract domain configurations from Caddyfile."""
    domains = []

    # Match only top-level domain blocks (no leading whitespace)
    # Valid patterns: domain.com {, domain.com, other.com {, :80 {
    lines = caddyfile_content.split('\n')

    i = 0
    while i < len(lines):
        line = lines[i]

        # Skip if line starts with whitespace (nested block)
        if line and line[0] in ' \t':
            i += 1
            continue

        # Skip comments and empty lines
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            i += 1
            continue

        # Check for domain block pattern (no leading whitespace, ends with {)
        # Must contain a domain-like pattern or :80
        if stripped.endswith('{'):
            domain_part = stripped[:-1].strip()

            # Check for :80 catch-all
            if domain_part == ':80':
                domains.append((':80', 'Catch-all for IP access'))
                i += 1
                continue

            # Check for valid domain pattern (contains . and valid TLD)
            # e.g., dr.eamer.dev, d.reamwalker.com, diachronica.com
            domain_candidates = [d.strip() for d in domain_part.split(',')]

            valid_domains = []
            for d in domain_candidates:
                # Basic domain validation: contains dot, has valid TLD
                if re.match(r'^[a-zA-Z0-9][a-zA-Z0-9.-]*\.(com|dev|org|net|io)$', d):
                    valid_domains.append(d)

            if valid_domains:
                # Get description from comments above or first content line
                description = ""
                # Look for comment above
                if i > 0:
                    prev_line = lines[i - 1].strip()
                    if prev_line.startswith('#'):
                        description = prev_line[1:].strip()[:60]

                # If no description from comment, look at first content line
                if not description and i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if next_line and not next_line.startswith('#'):
                        # Extract key directive
                        if next_line.startswith('reverse_proxy'):
                            port_match = re.search(r'localhost:(\d+)', next_line)
                            if port_match:
                                description = f"Proxies to port {port_match.group(1)}"
                        elif next_line.startswith('redir'):
                            description = "Redirect"
                        elif next_line.startswith('root'):
                            description = "Static file server"

                for d in valid_domains:
                    domains.append((d, description))

        i += 1

    return domains


def cmd_validate():
    """Validate Caddy configuration."""
    print_warning_banner()
    print(f"{Colors.CYAN}Validating Caddy configuration...{Colors.RESET}\n")

    result = run_sudo_command(["caddy", "validate", "--config", CADDYFILE_PATH])

    if result.returncode == 0:
        print(f"{Colors.GREEN}{Colors.BOLD}[VALID]{Colors.RESET} Configuration is valid")
        # Show any warnings
        if result.stderr and "warn" in result.stderr.lower():
            print(f"\n{Colors.YELLOW}Warnings:{Colors.RESET}")
            print(result.stderr)
    else:
        print(f"{Colors.RED}{Colors.BOLD}[INVALID]{Colors.RESET} Configuration has errors:\n")
        print(result.stderr or result.stdout)
        return 1

    return 0


def cmd_status():
    """Show Caddy service status."""
    print_warning_banner()
    print(f"{Colors.CYAN}Caddy Service Status{Colors.RESET}\n")

    # Get systemctl status
    result = subprocess.run(
        ["systemctl", "status", "caddy", "--no-pager"],
        capture_output=True,
        text=True
    )

    # Parse active state
    if "active (running)" in result.stdout:
        print(f"{Colors.GREEN}{Colors.BOLD}[RUNNING]{Colors.RESET} Caddy is active and running\n")
    elif "inactive" in result.stdout:
        print(f"{Colors.RED}{Colors.BOLD}[STOPPED]{Colors.RESET} Caddy is not running\n")
    else:
        print(f"{Colors.YELLOW}{Colors.BOLD}[UNKNOWN]{Colors.RESET} Unable to determine status\n")

    # Show key details
    for line in result.stdout.split('\n'):
        line = line.strip()
        if any(k in line.lower() for k in ['loaded:', 'active:', 'main pid:', 'memory:', 'cpu:']):
            print(f"  {line}")

    print(f"\n{Colors.DIM}Full status: systemctl status caddy{Colors.RESET}")
    return 0


def cmd_routes():
    """List all configured routes."""
    print_warning_banner()
    print(f"{Colors.CYAN}Configured Routes{Colors.RESET}\n")

    content = read_caddyfile()
    if not content:
        return 1

    routes = parse_routes(content)

    # Group by domain
    by_domain: dict[str, list[Route]] = {}
    for route in routes:
        if route.domain not in by_domain:
            by_domain[route.domain] = []
        by_domain[route.domain].append(route)

    for domain, domain_routes in sorted(by_domain.items()):
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}{domain}{Colors.RESET}")
        print(f"{Colors.DIM}{'─' * 60}{Colors.RESET}")

        for route in sorted(domain_routes, key=lambda r: r.path):
            port_str = f":{route.port}" if route.port else ""
            type_color = Colors.BLUE if route.route_type == "handle_path" else Colors.CYAN

            if route.port:
                print(f"  {Colors.GREEN}{route.path:<35}{Colors.RESET} -> localhost{Colors.YELLOW}{port_str}{Colors.RESET}  {type_color}({route.route_type}){Colors.RESET}")
            else:
                print(f"  {Colors.GREEN}{route.path:<35}{Colors.RESET}    {Colors.DIM}(static){Colors.RESET}  {type_color}({route.route_type}){Colors.RESET}")

    print(f"\n{Colors.DIM}Total routes: {len(routes)}{Colors.RESET}")
    return 0


def cmd_ports():
    """List all ports in use by Caddy."""
    print_warning_banner()
    print(f"{Colors.CYAN}Port Allocations in Caddy{Colors.RESET}\n")

    content = read_caddyfile()
    if not content:
        return 1

    port_mappings = extract_port_mappings(content)

    print(f"{'Port':<8} {'Paths'}")
    print(f"{Colors.DIM}{'─' * 60}{Colors.RESET}")

    for port in sorted(port_mappings.keys()):
        paths = port_mappings[port]
        paths_str = ", ".join(sorted(set(paths)))
        print(f"{Colors.YELLOW}{port:<8}{Colors.RESET} {Colors.GREEN}{paths_str}{Colors.RESET}")

    print(f"\n{Colors.DIM}Total ports in use: {len(port_mappings)}{Colors.RESET}")

    # Show available test ports
    test_range = set(range(5010, 5020)) | set(range(5050, 5060))
    used_ports = set(port_mappings.keys())
    available = sorted(test_range - used_ports)

    if available:
        print(f"\n{Colors.CYAN}Available test ports:{Colors.RESET} {', '.join(map(str, available[:10]))}")

    return 0


def cmd_domains():
    """List all configured domains."""
    print_warning_banner()
    print(f"{Colors.CYAN}Configured Domains{Colors.RESET}\n")

    content = read_caddyfile()
    if not content:
        return 1

    domains = extract_domains(content)

    for domain, context in domains:
        print(f"  {Colors.MAGENTA}{Colors.BOLD}{domain}{Colors.RESET}")
        if context:
            print(f"    {Colors.DIM}{context}...{Colors.RESET}")

    print(f"\n{Colors.DIM}Total domain blocks: {len(domains)}{Colors.RESET}")
    return 0


def cmd_help():
    """Show help message."""
    print(__doc__)
    print(f"\n{Colors.YELLOW}{Colors.BOLD}REMINDER:{Colors.RESET}")
    print(f"{Colors.YELLOW}  This script is READ-ONLY. To modify Caddy routes:{Colors.RESET}")
    print(f"{Colors.YELLOW}  1. Use @geepers_caddy agent in Claude Code{Colors.RESET}")
    print(f"{Colors.YELLOW}  2. The agent will backup, validate, and safely apply changes{Colors.RESET}")
    print(f"{Colors.YELLOW}  3. Port registry is maintained at ~/geepers/status/ports.json{Colors.RESET}\n")
    return 0


def main():
    """Main entry point."""
    commands = {
        "validate": cmd_validate,
        "status": cmd_status,
        "routes": cmd_routes,
        "ports": cmd_ports,
        "domains": cmd_domains,
        "help": cmd_help,
        "--help": cmd_help,
        "-h": cmd_help,
    }

    if len(sys.argv) < 2:
        cmd_help()
        print(f"{Colors.RED}Error: No command specified{Colors.RESET}")
        print(f"Usage: caddy.py <command>")
        print(f"Commands: {', '.join(c for c in commands if not c.startswith('-'))}")
        return 1

    command = sys.argv[1].lower()

    if command not in commands:
        print(f"{Colors.RED}Unknown command: {command}{Colors.RESET}")
        print(f"Available commands: {', '.join(c for c in commands if not c.startswith('-'))}")
        return 1

    return commands[command]()


if __name__ == "__main__":
    sys.exit(main())

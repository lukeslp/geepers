"""
Geepers MCP Naming System

Extends the shared naming registry with MCP-specific functionality.

Author: Luke Steuber
"""

from .core import (
    Role,
    PREFIXES,
    PACKAGE_PREFIX,
    NamingEntry,
    LEGACY_MAP,
    get_identifier,
    resolve_legacy,
)
from .mcp_naming import (
    get_mcp_tool_name,
    get_mcp_resource_uri,
    parse_mcp_tool_name,
    parse_mcp_resource_uri,
    resolve_legacy_tool_name,
    resolve_legacy_resource_uri,
    get_pattern_info,
    PATTERN_MAP,
)

__all__ = [
    # Core exports
    "Role",
    "PREFIXES",
    "PACKAGE_PREFIX",
    "NamingEntry",
    "LEGACY_MAP",
    "get_identifier",
    "resolve_legacy",
    # MCP-specific exports
    "get_mcp_tool_name",
    "get_mcp_resource_uri",
    "parse_mcp_tool_name",
    "parse_mcp_resource_uri",
    "resolve_legacy_tool_name",
    "resolve_legacy_resource_uri",
    "get_pattern_info",
    "PATTERN_MAP",
]
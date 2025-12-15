"""
MCP-specific naming utilities for Geepers.

Provides functions for generating and parsing MCP tool names and resource URIs
following the conductor.slug.action pattern.

Author: Luke Steuber
"""

from typing import Dict, Tuple, Optional, Any
from .core import Role, NamingEntry, resolve_legacy

# Map old pattern names to new slugs
PATTERN_MAP = {
    # Old name → canonical slug
    "dream-cascade": "cascade",
    "dream-swarm": "swarm",
    "beltalowda": "cascade",  # Legacy name - map to cascade
    "cascade": "cascade",  # Already correct
    "swarm": "swarm",  # Already correct
}

# Pattern display information
PATTERN_INFO = {
    "cascade": {
        "name": "cascade",
        "display_name": "Dream Cascade Hierarchical Research",
        "description": "Three-tier cascading synthesis with workers (parallel execution), mid-level synthesis, and executive synthesis",
        "use_cases": [
            "Comprehensive research tasks",
            "Academic literature review",
            "Multi-faceted analysis requiring synthesis",
            "Complex problem decomposition"
        ],
        "role": Role.ORCHESTRATOR,
    },
    "swarm": {
        "name": "swarm", 
        "display_name": "Dream Swarm Multi-Agent Search",
        "description": "Parallel specialized agents for multi-domain search and analysis",
        "use_cases": [
            "Broad information gathering",
            "Multi-source data aggregation",
            "Competitive analysis",
            "Market research"
        ],
        "role": Role.ORCHESTRATOR,
    },
}

# Legacy tool name mappings
LEGACY_TOOL_MAP = {
    # Orchestration tools
    "dream_orchestrate_research": ("orchestrate", "cascade"),
    "dream_orchestrate_search": ("orchestrate", "swarm"),
    "geepers_status": ("utility", "status"),
    "geepers_cancel": ("utility", "cancel"),
    "geepers_patterns": ("utility", "patterns"),
    "geepers_list_tools": ("utility", "registry.list"),
    "geepers_execute_tool": ("utility", "registry.execute"),
    
    # Provider tools (generate for multi-modal)
    "list_available_providers": ("utility", "providers.list"),
    "create_provider": ("utility", "providers.create"),
    "list_provider_models": ("utility", "providers.models"),
    "chat_completion": ("generate", "text"),
    "generate_image": ("generate", "image"),
    "analyze_image": ("generate", "analyze"),
    
    # Data fetching tools (individual tools, not agents)
    "dream_of_census_acs": ("tool", "census.acs"),
    "dream_of_census_saipe": ("tool", "census.saipe"),
    "dream_of_census_variables": ("tool", "census.variables"),
    "dream_of_arxiv": ("tool", "arxiv"),
    "dream_of_semantic_scholar": ("tool", "scholar"),
    "dream_of_semantic_scholar_paper": ("tool", "scholar.paper"),
    "dream_of_wayback": ("tool", "wayback"),
    "dream_of_wayback_snapshots": ("tool", "wayback.snapshots"),
    "dream_of_finance_stock": ("tool", "finance.stock"),
    "dream_of_github_repos": ("tool", "github"),
    "dream_of_nasa_apod": ("tool", "nasa.apod"),
    "dream_of_news": ("tool", "news"),
    "dream_of_books": ("tool", "books"),
    "dream_of_weather": ("tool", "weather"),
    "dream_of_wikipedia": ("tool", "wikipedia"),
    "dream_of_youtube": ("tool", "youtube"),
    
    # Cache tools (utilities)
    "cache_get": ("utility", "cache.get"),
    "cache_set": ("utility", "cache.set"),
    "cache_delete": ("utility", "cache.delete"),
    "cache_increment": ("utility", "cache.increment"),
    "cache_exists": ("utility", "cache.exists"),
    "cache_expire": ("utility", "cache.expire"),
    "cache_list_keys": ("utility", "cache.list"),
    
    # Utility tools
    "parse_document": ("utility", "parse.document"),
    "multi_provider_search": ("agent", "researcher"),
    "extract_citations": ("utility", "citations.extract"),
    "format_citation_bibtex": ("utility", "citations.bibtex"),
    
    # Web search (utility since it aggregates engines)
    "web_search": ("utility", "search.web"),
}


def get_mcp_tool_name(type_name: str, name: str) -> str:
    """
    Generate MCP tool name following geepers_type_name pattern.
    
    Args:
        type_name: Type category (orchestrate, agent, tool, generate, utility)
        name: Specific name (e.g., "cascade", "arxiv", "anthropic")
    
    Returns:
        MCP tool name (e.g., "geepers_orchestrate_cascade")
    """
    # Replace dots with underscores to comply with MCP naming rules
    name = name.replace('.', '_')
    return f"geepers_{type_name}_{name}"


def get_mcp_resource_uri(role: str, slug: Optional[str], path: str = "") -> str:
    """
    Generate MCP resource URI.
    
    Args:
        role: Role name
        slug: Component slug (can be None)
        path: Additional path components
    
    Returns:
        MCP resource URI (e.g., "geepers://orchestrator.cascade/info")
    """
    # Special case: geepers as conductor doesn't need role prefix
    if role == "conductor" or role == "geepers":
        if slug:
            base = f"geepers://{slug}"
        else:
            base = f"geepers://"
    else:
        if slug:
            base = f"geepers://{role}.{slug}"
        else:
            base = f"geepers://{role}"
    
    if path:
        return f"{base}/{path}"
    return base


def parse_mcp_tool_name(name: str) -> Tuple[str, str, str]:
    """
    Parse MCP tool name into components.
    
    Args:
        name: MCP tool name (e.g., "geepers_orchestrate_cascade")
    
    Returns:
        Tuple of (prefix, type, name) where prefix should be "geepers"
    """
    parts = name.split("_", 2)  # Split into at most 3 parts
    
    if len(parts) < 3:
        raise ValueError(f"Invalid MCP tool name format: {name}. Expected geepers_type_name")
    
    return parts[0], parts[1], parts[2]


def parse_mcp_resource_uri(uri: str) -> Dict[str, Any]:
    """
    Parse MCP resource URI into components.
    
    Args:
        uri: Resource URI (e.g., "geepers://conductor.beltalowda/info")
    
    Returns:
        Dict with parsed components
    """
    if not uri.startswith("geepers://"):
        # Handle legacy orchestrator:// URIs
        if uri.startswith("orchestrator://"):
            uri = uri.replace("orchestrator://", "geepers://conductor.")
        else:
            raise ValueError(f"Invalid URI scheme: {uri}")
    
    # Remove scheme
    path = uri.replace("geepers://", "")
    
    # Split into base and path
    if "/" in path:
        base, resource_path = path.split("/", 1)
    else:
        base = path
        resource_path = ""
    
    # Parse base (role.slug or just role)
    base_parts = base.split(".")
    if len(base_parts) == 1:
        role = base_parts[0]
        slug = None
    elif len(base_parts) == 2:
        role = base_parts[0]
        slug = base_parts[1]
    else:
        raise ValueError(f"Invalid URI base format: {base}")
    
    return {
        "role": role,
        "slug": slug,
        "path": resource_path,
        "full_uri": uri
    }


def resolve_legacy_tool_name(legacy_name: str) -> str:
    """
    Convert legacy tool name to new format.
    
    Args:
        legacy_name: Old tool name (e.g., "dream_orchestrate_research")
    
    Returns:
        New tool name (e.g., "geepers_orchestrate_cascade")
    """
    if legacy_name in LEGACY_TOOL_MAP:
        type_name, name = LEGACY_TOOL_MAP[legacy_name]
        return get_mcp_tool_name(type_name, name)
    
    # Check if it's already in new format
    if legacy_name.startswith("geepers_"):
        return legacy_name
    
    # Unknown legacy name
    return legacy_name


def resolve_legacy_resource_uri(legacy_uri: str) -> str:
    """
    Convert legacy resource URI to new format.
    
    Args:
        legacy_uri: Old URI (e.g., "orchestrator://dream-cascade/info")
    
    Returns:
        New URI (e.g., "geepers://orchestrator.cascade/info")
    """
    if legacy_uri.startswith("orchestrator://"):
        # Extract pattern and path
        uri_part = legacy_uri.replace("orchestrator://", "")
        if "/" in uri_part:
            pattern, path = uri_part.split("/", 1)
        else:
            pattern = uri_part
            path = ""
        
        # Resolve pattern name
        if pattern in PATTERN_MAP:
            slug = PATTERN_MAP[pattern]
            return get_mcp_resource_uri("orchestrator", slug, path)
        elif pattern in ["research", "search"]:
            # Handle task IDs
            return get_mcp_resource_uri("geepers", None, uri_part)
        else:
            # Assume it's a task ID
            return get_mcp_resource_uri("geepers", None, uri_part)
    
    # Already in new format or unknown
    return legacy_uri


def get_pattern_info(pattern_name: str) -> Dict[str, Any]:
    """
    Get pattern information by name.
    
    Args:
        pattern_name: Pattern name (old or new format)
    
    Returns:
        Pattern info dict
    """
    # Resolve old name if needed
    if pattern_name in PATTERN_MAP:
        pattern_name = PATTERN_MAP[pattern_name]
    
    if pattern_name in PATTERN_INFO:
        return PATTERN_INFO[pattern_name]
    
    raise ValueError(f"Unknown pattern: {pattern_name}")
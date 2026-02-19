#!/usr/bin/env python3
"""
Universal Data Fetcher

Quick access to all 17 data sources through a single interface.

Usage:
    python fetch.py arxiv "quantum computing"
    python fetch.py github search "react hooks"
    python fetch.py census population --state CA
    python fetch.py nasa apod

Author: Luke Steuber
"""

import argparse
import json
import sys
import os

# Add shared library to path
sys.path.insert(0, '/home/coolhand/shared')

try:
    from data_fetching import ClientFactory
except ImportError:
    print("Error: Cannot import shared library. Ensure /home/coolhand/shared is accessible.", file=sys.stderr)
    sys.exit(1)


SOURCES = [
    "arxiv", "github", "census", "nasa", "pubmed", "wikipedia",
    "news", "weather", "youtube", "openlibrary", "semantic_scholar",
    "fec", "judiciary", "archive", "finance", "wolfram", "mal"
]


def fetch_data(source: str, query: str = None, action: str = "search", max_results: int = 10, **kwargs) -> dict:
    """
    Fetch data from specified source.

    Args:
        source: Data source name
        query: Search query or identifier
        action: Action type (search, get, list, etc.)
        max_results: Maximum number of results
        **kwargs: Source-specific parameters

    Returns:
        Results dict
    """
    try:
        client = ClientFactory.create_client(source)
    except ValueError as e:
        return {"error": f"Unknown source: {source}. Available: {', '.join(SOURCES)}"}
    except Exception as e:
        return {"error": f"Failed to create client for {source}: {str(e)}"}

    try:
        if action == "search" and query:
            results = client.search(query=query, max_results=max_results, **kwargs)
        elif hasattr(client, action):
            method = getattr(client, action)
            if query:
                results = method(query, **kwargs)
            else:
                results = method(**kwargs)
        else:
            results = client.search(query=query or "", max_results=max_results, **kwargs)

        return {"source": source, "query": query, "action": action, "results": results}

    except Exception as e:
        return {"error": f"Fetch failed: {str(e)}"}


def format_results(data: dict, output_format: str) -> str:
    """Format results for output."""
    if "error" in data:
        return f"Error: {data['error']}"

    if output_format == "json":
        return json.dumps(data, indent=2, default=str)

    # Human-readable format
    lines = [
        f"Source: {data.get('source', 'Unknown')}",
        f"Query: {data.get('query', 'N/A')}",
        f"Action: {data.get('action', 'search')}",
        ""
    ]

    results = data.get("results", [])
    if isinstance(results, list):
        lines.append(f"Results ({len(results)}):")
        lines.append("-" * 40)
        for i, item in enumerate(results[:10], 1):
            if isinstance(item, dict):
                title = item.get("title", item.get("name", item.get("id", f"Item {i}")))
                lines.append(f"{i}. {title}")
                if "url" in item:
                    lines.append(f"   URL: {item['url']}")
                if "description" in item:
                    desc = item["description"][:100] + "..." if len(item.get("description", "")) > 100 else item.get("description", "")
                    lines.append(f"   {desc}")
            else:
                lines.append(f"{i}. {item}")
            lines.append("")
    elif isinstance(results, dict):
        for key, value in results.items():
            if isinstance(value, (str, int, float)):
                lines.append(f"{key}: {value}")
            elif isinstance(value, list) and len(value) < 5:
                lines.append(f"{key}: {', '.join(str(v) for v in value)}")
    else:
        lines.append(str(results))

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Universal data fetcher for 17+ sources",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Available sources:
  {', '.join(SOURCES)}

Examples:
  %(prog)s arxiv "quantum computing"
  %(prog)s github search "react hooks"
  %(prog)s census population --state CA
  %(prog)s nasa apod
  %(prog)s wikipedia "Machine learning"
  %(prog)s news "AI regulation" --max 5
        """
    )

    parser.add_argument(
        "source",
        choices=SOURCES,
        help="Data source to query"
    )
    parser.add_argument(
        "action_or_query",
        nargs="?",
        default="search",
        help="Action (search, get, list) or search query"
    )
    parser.add_argument(
        "query",
        nargs="?",
        help="Search query (if action specified first)"
    )
    parser.add_argument(
        "--max", "-m",
        type=int,
        default=10,
        help="Maximum results (default: 10)"
    )
    parser.add_argument(
        "--output", "-o",
        choices=["stdout", "json"],
        default="stdout",
        help="Output format (default: stdout)"
    )
    parser.add_argument(
        "--state",
        help="State code for census queries"
    )
    parser.add_argument(
        "--county",
        help="County name for census queries"
    )
    parser.add_argument(
        "--year",
        type=int,
        help="Year for time-based queries"
    )
    parser.add_argument(
        "--lat",
        type=float,
        help="Latitude for geo queries"
    )
    parser.add_argument(
        "--lon",
        type=float,
        help="Longitude for geo queries"
    )
    parser.add_argument(
        "--list-sources",
        action="store_true",
        help="List all available sources and exit"
    )

    args = parser.parse_args()

    if args.list_sources:
        print("Available data sources:")
        for source in SOURCES:
            print(f"  - {source}")
        sys.exit(0)

    # Determine action and query
    known_actions = ["search", "get", "list", "apod", "quote", "repo", "issues", "org", "population", "income"]

    if args.action_or_query in known_actions:
        action = args.action_or_query
        query = args.query
    else:
        action = "search"
        query = args.action_or_query

    # Build kwargs from optional args
    kwargs = {}
    if args.state:
        kwargs["state"] = args.state
    if args.county:
        kwargs["county"] = args.county
    if args.year:
        kwargs["year"] = args.year
    if args.lat:
        kwargs["lat"] = args.lat
    if args.lon:
        kwargs["lon"] = args.lon

    print(f"Fetching from {args.source}...", file=sys.stderr)

    result = fetch_data(
        source=args.source,
        query=query,
        action=action,
        max_results=args.max,
        **kwargs
    )

    print(format_results(result, args.output))

    if "error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()

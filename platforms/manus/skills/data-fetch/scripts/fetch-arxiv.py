#!/usr/bin/env python3
"""
arXiv Paper Fetcher

Search and retrieve academic papers from arXiv.

Usage:
    python fetch-arxiv.py "quantum computing" --max 10
    python fetch-arxiv.py "machine learning" --category cs.AI
    python fetch-arxiv.py --id 2005.14165

Author: Luke Steuber
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional

ARXIV_API = "http://export.arxiv.org/api/query"


def search_arxiv(
    query: str,
    max_results: int = 10,
    category: Optional[str] = None,
    sort_by: str = "relevance"
) -> List[Dict]:
    """
    Search arXiv for papers.

    Args:
        query: Search query
        max_results: Maximum number of results
        category: arXiv category (e.g., cs.AI, physics.quant-ph)
        sort_by: Sort order (relevance, lastUpdatedDate, submittedDate)

    Returns:
        List of paper dicts
    """
    # Build search query
    search_query = f"all:{query}"
    if category:
        search_query = f"cat:{category} AND {search_query}"

    params = {
        "search_query": search_query,
        "start": 0,
        "max_results": max_results,
        "sortBy": sort_by,
        "sortOrder": "descending"
    }

    url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = response.read().decode('utf-8')
    except Exception as e:
        return [{"error": f"API request failed: {str(e)}"}]

    # Parse XML
    root = ET.fromstring(data)
    ns = {"atom": "http://www.w3.org/2005/Atom"}

    papers = []
    for entry in root.findall("atom:entry", ns):
        paper = {
            "id": entry.find("atom:id", ns).text.split("/abs/")[-1] if entry.find("atom:id", ns) is not None else "",
            "title": entry.find("atom:title", ns).text.strip().replace("\n", " ") if entry.find("atom:title", ns) is not None else "",
            "summary": entry.find("atom:summary", ns).text.strip().replace("\n", " ")[:500] if entry.find("atom:summary", ns) is not None else "",
            "authors": [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns) if a.find("atom:name", ns) is not None],
            "published": entry.find("atom:published", ns).text[:10] if entry.find("atom:published", ns) is not None else "",
            "updated": entry.find("atom:updated", ns).text[:10] if entry.find("atom:updated", ns) is not None else "",
            "url": f"https://arxiv.org/abs/{entry.find('atom:id', ns).text.split('/abs/')[-1]}" if entry.find("atom:id", ns) is not None else "",
            "pdf_url": f"https://arxiv.org/pdf/{entry.find('atom:id', ns).text.split('/abs/')[-1]}.pdf" if entry.find("atom:id", ns) is not None else "",
            "categories": [c.get("term") for c in entry.findall("atom:category", ns)]
        }
        papers.append(paper)

    return papers


def get_paper(arxiv_id: str) -> Dict:
    """Get a specific paper by arXiv ID."""
    params = {"id_list": arxiv_id}
    url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = response.read().decode('utf-8')
    except Exception as e:
        return {"error": f"API request failed: {str(e)}"}

    root = ET.fromstring(data)
    ns = {"atom": "http://www.w3.org/2005/Atom"}

    entry = root.find("atom:entry", ns)
    if entry is None:
        return {"error": f"Paper not found: {arxiv_id}"}

    return {
        "id": arxiv_id,
        "title": entry.find("atom:title", ns).text.strip().replace("\n", " ") if entry.find("atom:title", ns) is not None else "",
        "summary": entry.find("atom:summary", ns).text.strip() if entry.find("atom:summary", ns) is not None else "",
        "authors": [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns) if a.find("atom:name", ns) is not None],
        "published": entry.find("atom:published", ns).text[:10] if entry.find("atom:published", ns) is not None else "",
        "url": f"https://arxiv.org/abs/{arxiv_id}",
        "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}.pdf",
        "categories": [c.get("term") for c in entry.findall("atom:category", ns)]
    }


def format_output(papers: List[Dict], output_format: str) -> str:
    """Format papers for output."""
    if output_format == "json":
        return json.dumps(papers, indent=2)

    if not papers:
        return "No papers found."

    if "error" in papers[0]:
        return f"Error: {papers[0]['error']}"

    lines = [f"Found {len(papers)} papers:", ""]

    for i, paper in enumerate(papers, 1):
        lines.append(f"{i}. {paper['title']}")
        lines.append(f"   Authors: {', '.join(paper['authors'][:3])}{'...' if len(paper['authors']) > 3 else ''}")
        lines.append(f"   Published: {paper['published']}")
        lines.append(f"   Categories: {', '.join(paper['categories'][:3])}")
        lines.append(f"   URL: {paper['url']}")
        lines.append(f"   PDF: {paper['pdf_url']}")
        if output_format != "brief":
            summary = paper['summary'][:200] + "..." if len(paper['summary']) > 200 else paper['summary']
            lines.append(f"   Abstract: {summary}")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Search and fetch papers from arXiv",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "quantum computing"
  %(prog)s "machine learning" --category cs.AI --max 20
  %(prog)s --id 2005.14165
  %(prog)s "transformer" --output json
        """
    )

    parser.add_argument(
        "query",
        nargs="?",
        help="Search query"
    )
    parser.add_argument(
        "--id",
        help="Get specific paper by arXiv ID"
    )
    parser.add_argument(
        "--max", "-m",
        type=int,
        default=10,
        help="Maximum results (default: 10)"
    )
    parser.add_argument(
        "--category", "-c",
        help="arXiv category (e.g., cs.AI, physics.quant-ph)"
    )
    parser.add_argument(
        "--sort",
        choices=["relevance", "lastUpdatedDate", "submittedDate"],
        default="relevance",
        help="Sort order (default: relevance)"
    )
    parser.add_argument(
        "--output", "-o",
        choices=["stdout", "json", "brief"],
        default="stdout",
        help="Output format (default: stdout)"
    )

    args = parser.parse_args()

    if args.id:
        result = [get_paper(args.id)]
    elif args.query:
        result = search_arxiv(
            query=args.query,
            max_results=args.max,
            category=args.category,
            sort_by=args.sort
        )
    else:
        parser.print_help()
        sys.exit(1)

    print(format_output(result, args.output))


if __name__ == "__main__":
    main()

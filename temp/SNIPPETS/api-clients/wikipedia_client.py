#!/usr/bin/env python3
"""
Wikipedia API Client

Description: Client for Wikipedia's API supporting article search, summaries,
             full content retrieval, and random articles across multiple languages.

Use Cases:
- Knowledge base enrichment for AI agents
- Reference and fact-checking tools
- Content research and gathering
- Educational applications
- Multilingual content retrieval
- Building encyclopedic search features

Dependencies:
- requests

Notes:
- No API key required (public API)
- Supports 300+ language editions
- Uses OpenSearch for search, Query API for content
- Includes page images when available
- Returns structured dictionaries with consistent format

Related Snippets:
- api-clients/arxiv_client.py (academic papers)
- api-clients/jina_web_scraper.py (web content)

Source Attribution:
- Extracted from: /home/coolhand/shared/data_fetching/wikipedia_client.py
- Author: Luke Steuber
"""

import requests
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class WikipediaClient:
    """Client for Wikipedia API."""

    def __init__(self, language: str = "en"):
        """
        Initialize Wikipedia client.

        Args:
            language: Wikipedia language code (en, es, fr, de, ja, zh, etc.)
        """
        self.language = language
        self.base_url = f"https://{language}.wikipedia.org/w/api.php"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'WikipediaClient/1.0 (contact@example.com)'
        })

    def search(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """
        Search Wikipedia articles.

        Args:
            query: Search query
            limit: Maximum results (default: 10)

        Returns:
            Dict with search results
        """
        try:
            response = self.session.get(
                self.base_url,
                params={
                    'action': 'opensearch',
                    'search': query,
                    'limit': limit,
                    'format': 'json'
                },
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            # OpenSearch returns [query, titles, descriptions, urls]
            if len(data) >= 4:
                results = []
                for i in range(len(data[1])):
                    results.append({
                        "title": data[1][i],
                        "description": data[2][i] if i < len(data[2]) else "",
                        "url": data[3][i] if i < len(data[3]) else ""
                    })

                return {
                    "success": True,
                    "query": query,
                    "results": results,
                    "count": len(results)
                }

            return {"success": True, "query": query, "results": [], "count": 0}

        except Exception as e:
            logger.error(f"Wikipedia search error: {e}")
            return {"success": False, "error": str(e)}

    def get_summary(self, title: str) -> Dict[str, Any]:
        """
        Get article summary (intro section).

        Args:
            title: Article title

        Returns:
            Dict with summary and metadata
        """
        try:
            response = self.session.get(
                self.base_url,
                params={
                    'action': 'query',
                    'prop': 'extracts|pageimages',
                    'exintro': True,
                    'explaintext': True,
                    'titles': title,
                    'format': 'json',
                    'piprop': 'original'
                },
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            pages = data.get('query', {}).get('pages', {})
            if pages:
                page = list(pages.values())[0]

                if page.get('missing') is not None:
                    return {"success": False, "error": "Article not found"}

                return {
                    "success": True,
                    "title": page.get("title"),
                    "summary": page.get("extract"),
                    "page_id": page.get("pageid"),
                    "image": page.get("original", {}).get("source"),
                    "url": f"https://{self.language}.wikipedia.org/wiki/{title.replace(' ', '_')}"
                }

            return {"success": False, "error": "Article not found"}

        except Exception as e:
            logger.error(f"Wikipedia summary error: {e}")
            return {"success": False, "error": str(e)}

    def get_full_content(self, title: str) -> Dict[str, Any]:
        """
        Get full article content.

        Args:
            title: Article title

        Returns:
            Dict with full content
        """
        try:
            response = self.session.get(
                self.base_url,
                params={
                    'action': 'query',
                    'prop': 'extracts',
                    'explaintext': True,
                    'titles': title,
                    'format': 'json'
                },
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            pages = data.get('query', {}).get('pages', {})
            if pages:
                page = list(pages.values())[0]

                if page.get('missing') is not None:
                    return {"success": False, "error": "Article not found"}

                content = page.get("extract", "")

                return {
                    "success": True,
                    "title": page.get("title"),
                    "content": content,
                    "page_id": page.get("pageid"),
                    "word_count": len(content.split()),
                    "url": f"https://{self.language}.wikipedia.org/wiki/{title.replace(' ', '_')}"
                }

            return {"success": False, "error": "Article not found"}

        except Exception as e:
            logger.error(f"Wikipedia content error: {e}")
            return {"success": False, "error": str(e)}

    def get_random(self, limit: int = 1) -> Dict[str, Any]:
        """
        Get random article(s).

        Args:
            limit: Number of random articles

        Returns:
            Dict with random article info
        """
        try:
            response = self.session.get(
                self.base_url,
                params={
                    'action': 'query',
                    'list': 'random',
                    'rnnamespace': 0,  # Main articles only
                    'rnlimit': limit,
                    'format': 'json'
                },
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            articles = []
            for item in data.get('query', {}).get('random', []):
                title = item.get('title')
                articles.append({
                    "title": title,
                    "page_id": item.get('id'),
                    "url": f"https://{self.language}.wikipedia.org/wiki/{title.replace(' ', '_')}"
                })

            return {
                "success": True,
                "articles": articles,
                "count": len(articles)
            }

        except Exception as e:
            logger.error(f"Wikipedia random error: {e}")
            return {"success": False, "error": str(e)}

    def get_categories(self, title: str) -> Dict[str, Any]:
        """
        Get categories for an article.

        Args:
            title: Article title

        Returns:
            Dict with category list
        """
        try:
            response = self.session.get(
                self.base_url,
                params={
                    'action': 'query',
                    'prop': 'categories',
                    'titles': title,
                    'format': 'json',
                    'cllimit': 50
                },
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            pages = data.get('query', {}).get('pages', {})
            if pages:
                page = list(pages.values())[0]
                categories = [
                    cat['title'].replace('Category:', '')
                    for cat in page.get('categories', [])
                ]

                return {
                    "success": True,
                    "title": page.get("title"),
                    "categories": categories,
                    "count": len(categories)
                }

            return {"success": False, "error": "Article not found"}

        except Exception as e:
            logger.error(f"Wikipedia categories error: {e}")
            return {"success": False, "error": str(e)}

    def get_links(self, title: str, limit: int = 50) -> Dict[str, Any]:
        """
        Get internal links from an article.

        Args:
            title: Article title
            limit: Maximum links to return

        Returns:
            Dict with link list
        """
        try:
            response = self.session.get(
                self.base_url,
                params={
                    'action': 'query',
                    'prop': 'links',
                    'titles': title,
                    'format': 'json',
                    'pllimit': limit,
                    'plnamespace': 0  # Main namespace only
                },
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            pages = data.get('query', {}).get('pages', {})
            if pages:
                page = list(pages.values())[0]
                links = [link['title'] for link in page.get('links', [])]

                return {
                    "success": True,
                    "title": page.get("title"),
                    "links": links,
                    "count": len(links)
                }

            return {"success": False, "error": "Article not found"}

        except Exception as e:
            logger.error(f"Wikipedia links error: {e}")
            return {"success": False, "error": str(e)}


# Convenience functions
def search_wikipedia(query: str, language: str = "en", limit: int = 10) -> List[Dict]:
    """
    Convenience function for searching Wikipedia.

    Args:
        query: Search query
        language: Language code
        limit: Maximum results

    Returns:
        List of result dictionaries
    """
    client = WikipediaClient(language=language)
    result = client.search(query, limit)
    if result.get("success"):
        return result.get("results", [])
    return []


def get_article_summary(title: str, language: str = "en") -> Optional[str]:
    """
    Convenience function to get article summary text.

    Args:
        title: Article title
        language: Language code

    Returns:
        Summary text or None
    """
    client = WikipediaClient(language=language)
    result = client.get_summary(title)
    if result.get("success"):
        return result.get("summary")
    return None


def format_for_llm(articles: List[Dict], include_content: bool = False) -> str:
    """
    Format Wikipedia articles for LLM context.

    Args:
        articles: List of article dictionaries (from search results)
        include_content: Whether to fetch and include full content

    Returns:
        Formatted string for LLM context
    """
    client = WikipediaClient()
    output = ["# Wikipedia Articles\n"]

    for i, article in enumerate(articles[:5], 1):
        title = article.get('title', '')
        output.append(f"## {i}. {title}")

        if article.get('description'):
            output.append(f"{article['description']}\n")

        if include_content:
            summary = client.get_summary(title)
            if summary.get("success"):
                output.append(summary.get("summary", "")[:500] + "...\n")

        if article.get('url'):
            output.append(f"[Read more]({article['url']})\n")

    return '\n'.join(output)


# Usage example
if __name__ == "__main__":
    print("Wikipedia Client Demo")
    print("=" * 50)

    client = WikipediaClient()

    # Search
    print("\nSearching for 'artificial intelligence'...")
    results = client.search("artificial intelligence", limit=5)

    if results.get("success"):
        print(f"Found {results['count']} results:")
        for r in results['results'][:3]:
            print(f"  - {r['title']}")
            if r['description']:
                print(f"    {r['description'][:60]}...")

    # Get summary
    print("\n" + "-" * 50)
    print("Getting summary for 'Python (programming language)'...")

    summary = client.get_summary("Python (programming language)")
    if summary.get("success"):
        print(f"Title: {summary['title']}")
        print(f"Summary: {summary['summary'][:200]}...")
        if summary.get('image'):
            print(f"Image: {summary['image']}")

    # Get random article
    print("\n" + "-" * 50)
    print("Getting random article...")

    random_result = client.get_random(limit=1)
    if random_result.get("success"):
        for article in random_result['articles']:
            print(f"Random: {article['title']}")
            print(f"URL: {article['url']}")

    # Different language
    print("\n" + "-" * 50)
    print("Searching Spanish Wikipedia...")

    es_client = WikipediaClient(language="es")
    es_results = es_client.search("inteligencia artificial", limit=3)

    if es_results.get("success"):
        for r in es_results['results']:
            print(f"  - {r['title']}")

    # LLM formatting
    print("\n" + "-" * 50)
    print("LLM-formatted output:\n")

    if results.get("success"):
        print(format_for_llm(results['results'][:3]))

"""
Wikipedia API Client

Provides access to Wikipedia's API for:
- Article search
- Article summaries
- Full article content
- Random articles

Author: Luke Steuber
"""

import requests
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class WikipediaClient:
    """Client for Wikipedia API."""

    BASE_URL = "https://en.wikipedia.org/w/api.php"

    def __init__(self, language: str = "en"):
        """
        Initialize Wikipedia client.

        Args:
            language: Wikipedia language code (en, es, fr, etc.)
        """
        self.language = language
        self.base_url = f"https://{language}.wikipedia.org/w/api.php"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'SharedLibraryWikipediaClient/1.0'
        })

    def search(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """
        Search Wikipedia articles.

        Args:
            query: Search query
            limit: Maximum results

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
                    "query": query,
                    "results": results,
                    "count": len(results)
                }

            return {"query": query, "results": [], "count": 0}
        except Exception as e:
            logger.error(f"Wikipedia search error: {e}")
            return {"error": str(e)}

    def get_summary(self, title: str) -> Dict[str, Any]:
        """
        Get article summary (extract).

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

                return {
                    "title": page.get("title"),
                    "summary": page.get("extract"),
                    "page_id": page.get("pageid"),
                    "image": page.get("original", {}).get("source"),
                    "url": f"https://{self.language}.wikipedia.org/wiki/{title.replace(' ', '_')}"
                }

            return {"error": "Article not found"}
        except Exception as e:
            logger.error(f"Wikipedia summary error: {e}")
            return {"error": str(e)}

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

                return {
                    "title": page.get("title"),
                    "content": page.get("extract"),
                    "page_id": page.get("pageid"),
                    "word_count": len(page.get("extract", "").split()),
                    "url": f"https://{self.language}.wikipedia.org/wiki/{title.replace(' ', '_')}"
                }

            return {"error": "Article not found"}
        except Exception as e:
            logger.error(f"Wikipedia content error: {e}")
            return {"error": str(e)}

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
                "articles": articles,
                "count": len(articles)
            }
        except Exception as e:
            logger.error(f"Wikipedia random error: {e}")
            return {"error": str(e)}


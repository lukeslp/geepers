"""
News API Client

Provides access to News API for:
- Top headlines
- Everything search
- Sources listing

Requires NEWS_API_KEY environment variable.

Author: Luke Steuber
"""

import os
import requests
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class NewsClient:
    """Client for News API."""

    BASE_URL = "https://newsapi.org/v2"

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize News API client.

        Args:
            api_key: News API key
        """
        self.api_key = api_key or os.getenv('NEWS_API_KEY')
        if not self.api_key:
            raise ValueError("NEWS_API_KEY is required")

        self.session = requests.Session()

    def get_top_headlines(
        self,
        country: str = "us",
        category: Optional[str] = None,
        query: Optional[str] = None,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """
        Get top headlines.

        Args:
            country: Country code (us, gb, etc.)
            category: Category (business, technology, etc.)
            query: Search query
            page_size: Number of results

        Returns:
            Dict with headlines
        """
        try:
            params = {
                'apiKey': self.api_key,
                'country': country,
                'pageSize': page_size
            }

            if category:
                params['category'] = category
            if query:
                params['q'] = query

            response = self.session.get(
                f"{self.BASE_URL}/top-headlines",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            articles = []
            for item in data.get('articles', []):
                articles.append({
                    "title": item.get("title"),
                    "description": item.get("description"),
                    "url": item.get("url"),
                    "source": item.get("source", {}).get("name"),
                    "published_at": item.get("publishedAt"),
                    "author": item.get("author"),
                    "image_url": item.get("urlToImage")
                })

            return {
                "status": data.get('status'),
                "total_results": data.get('totalResults', 0),
                "articles": articles
            }
        except Exception as e:
            logger.error(f"News API headlines error: {e}")
            return {"error": str(e)}

    def search_everything(
        self,
        query: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        language: str = "en",
        sort_by: str = "publishedAt",
        page_size: int = 20
    ) -> Dict[str, Any]:
        """
        Search all articles.

        Args:
            query: Search query
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)
            language: Language code
            sort_by: Sort by (relevancy, popularity, publishedAt)
            page_size: Number of results

        Returns:
            Dict with search results
        """
        try:
            params = {
                'apiKey': self.api_key,
                'q': query,
                'language': language,
                'sortBy': sort_by,
                'pageSize': page_size
            }

            if from_date:
                params['from'] = from_date
            if to_date:
                params['to'] = to_date

            response = self.session.get(
                f"{self.BASE_URL}/everything",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            articles = []
            for item in data.get('articles', []):
                articles.append({
                    "title": item.get("title"),
                    "description": item.get("description"),
                    "content": item.get("content"),
                    "url": item.get("url"),
                    "source": item.get("source", {}).get("name"),
                    "published_at": item.get("publishedAt"),
                    "author": item.get("author")
                })

            return {
                "query": query,
                "total_results": data.get('totalResults', 0),
                "articles": articles
            }
        except Exception as e:
            logger.error(f"News API search error: {e}")
            return {"error": str(e)}

    def get_sources(
        self,
        category: Optional[str] = None,
        language: str = "en",
        country: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get news sources.

        Args:
            category: Filter by category
            language: Language code
            country: Country code

        Returns:
            Dict with sources
        """
        try:
            params = {'apiKey': self.api_key, 'language': language}

            if category:
                params['category'] = category
            if country:
                params['country'] = country

            response = self.session.get(
                f"{self.BASE_URL}/sources",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            sources = []
            for item in data.get('sources', []):
                sources.append({
                    "id": item.get("id"),
                    "name": item.get("name"),
                    "description": item.get("description"),
                    "url": item.get("url"),
                    "category": item.get("category"),
                    "country": item.get("country"),
                    "language": item.get("language")
                })

            return {
                "sources": sources,
                "count": len(sources)
            }
        except Exception as e:
            logger.error(f"News API sources error: {e}")
            return {"error": str(e)}


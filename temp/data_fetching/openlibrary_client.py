"""
OpenLibrary API Client

Provides access to OpenLibrary API for:
- Book search
- Book details by ISBN
- Author information
- Subject browsing

No API key required.

Author: Luke Steuber
"""

import requests
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class OpenLibraryClient:
    """Client for OpenLibrary API."""

    BASE_URL = "https://openlibrary.org"

    def __init__(self):
        """Initialize OpenLibrary client."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'SharedLibraryOpenLibraryClient/1.0'
        })

    def search_books(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """
        Search for books.

        Args:
            query: Search query (title, author, ISBN, etc.)
            limit: Maximum results

        Returns:
            Dict with book search results
        """
        try:
            response = self.session.get(
                f"{self.BASE_URL}/search.json",
                params={'q': query, 'limit': limit},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            books = []
            for doc in data.get('docs', []):
                books.append({
                    "title": doc.get("title"),
                    "author": doc.get("author_name", []),
                    "first_publish_year": doc.get("first_publish_year"),
                    "isbn": doc.get("isbn", []),
                    "publisher": doc.get("publisher", []),
                    "language": doc.get("language", []),
                    "subject": doc.get("subject", [])[:5],  # First 5 subjects
                    "key": doc.get("key"),
                    "cover_id": doc.get("cover_i")
                })

            return {
                "query": query,
                "num_found": data.get('numFound', 0),
                "books": books
            }
        except Exception as e:
            logger.error(f"OpenLibrary search error: {e}")
            return {"error": str(e)}

    def get_book_by_isbn(self, isbn: str) -> Dict[str, Any]:
        """
        Get book details by ISBN.

        Args:
            isbn: ISBN-10 or ISBN-13

        Returns:
            Dict with book details
        """
        try:
            response = self.session.get(
                f"{self.BASE_URL}/api/books",
                params={'bibkeys': f'ISBN:{isbn}', 'format': 'json', 'jscmd': 'data'},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            book_data = data.get(f'ISBN:{isbn}', {})
            if not book_data:
                return {"error": "Book not found"}

            return {
                "title": book_data.get("title"),
                "authors": [a.get("name") for a in book_data.get("authors", [])],
                "publish_date": book_data.get("publish_date"),
                "publishers": [p.get("name") for p in book_data.get("publishers", [])],
                "number_of_pages": book_data.get("number_of_pages"),
                "subjects": [s.get("name") for s in book_data.get("subjects", [])],
                "cover": book_data.get("cover", {}).get("large"),
                "url": book_data.get("url")
            }
        except Exception as e:
            logger.error(f"OpenLibrary ISBN error: {e}")
            return {"error": str(e)}

    def get_author(self, author_key: str) -> Dict[str, Any]:
        """
        Get author information.

        Args:
            author_key: Author key (e.g., /authors/OL23919A)

        Returns:
            Dict with author info
        """
        try:
            # Ensure key format
            if not author_key.startswith('/authors/'):
                author_key = f'/authors/{author_key}'

            response = self.session.get(
                f"{self.BASE_URL}{author_key}.json",
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            return {
                "name": data.get("name"),
                "birth_date": data.get("birth_date"),
                "death_date": data.get("death_date"),
                "bio": data.get("bio", {}).get("value") if isinstance(data.get("bio"), dict) else data.get("bio"),
                "photo": data.get("photos", [None])[0],
                "wikipedia": data.get("wikipedia"),
                "key": data.get("key")
            }
        except Exception as e:
            logger.error(f"OpenLibrary author error: {e}")
            return {"error": str(e)}

    def get_subjects(self, subject: str, limit: int = 10) -> Dict[str, Any]:
        """
        Browse books by subject.

        Args:
            subject: Subject name (e.g., "science_fiction")
            limit: Maximum results

        Returns:
            Dict with books in subject
        """
        try:
            response = self.session.get(
                f"{self.BASE_URL}/subjects/{subject}.json",
                params={'limit': limit},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            books = []
            for work in data.get('works', []):
                books.append({
                    "title": work.get("title"),
                    "authors": [a.get("name") for a in work.get("authors", [])],
                    "first_publish_year": work.get("first_publish_year"),
                    "key": work.get("key"),
                    "cover_id": work.get("cover_id")
                })

            return {
                "subject": subject,
                "work_count": data.get('work_count', 0),
                "books": books
            }
        except Exception as e:
            logger.error(f"OpenLibrary subject error: {e}")
            return {"error": str(e)}


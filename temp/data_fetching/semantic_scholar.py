"""
Semantic Scholar API Client
Access to academic paper metadata from Semantic Scholar.

Extracted from schollama for reuse across projects.
"""

import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


logger = logging.getLogger(__name__)


@dataclass
class SemanticScholarPaper:
    """Represents a paper from Semantic Scholar"""
    title: str
    authors: List[str]
    year: Optional[int]
    abstract: Optional[str]
    doi: Optional[str]
    keywords: List[str]
    venue: Optional[str]
    url: Optional[str]
    paper_id: Optional[str] = None
    citation_count: Optional[int] = None
    reference_count: Optional[int] = None
    influential_citation_count: Optional[int] = None

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'SemanticScholarPaper':
        """Create SemanticScholarPaper from API response"""
        # Extract authors
        authors = []
        for author in data.get('authors', []):
            name = author.get('name')
            if name:
                authors.append(name)

        # Extract keywords from topics
        keywords = []
        for topic in data.get('topics', []):
            topic_name = topic.get('topic')
            if topic_name:
                keywords.append(topic_name)

        return cls(
            title=data.get('title', ''),
            authors=authors,
            year=data.get('year'),
            abstract=data.get('abstract'),
            doi=data.get('doi'),
            keywords=keywords,
            venue=data.get('venue'),
            url=data.get('url'),
            paper_id=data.get('paperId'),
            citation_count=data.get('citationCount'),
            reference_count=data.get('referenceCount'),
            influential_citation_count=data.get('influentialCitationCount')
        )

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'title': self.title,
            'authors': self.authors,
            'year': self.year,
            'abstract': self.abstract,
            'doi': self.doi,
            'keywords': self.keywords,
            'venue': self.venue,
            'url': self.url,
            'paper_id': self.paper_id,
            'citation_count': self.citation_count,
            'reference_count': self.reference_count,
            'influential_citation_count': self.influential_citation_count,
            'source': 'semantic_scholar'
        }


class SemanticScholarClient:
    """Client for interacting with Semantic Scholar API"""

    BASE_URL = "https://api.semanticscholar.org/graph/v1"

    DEFAULT_FIELDS = [
        "title",
        "authors",
        "year",
        "abstract",
        "doi",
        "venue",
        "url",
        "paperId",
        "citationCount",
        "referenceCount",
        "influentialCitationCount"
    ]

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Semantic Scholar client.

        Args:
            api_key: Optional API key for higher rate limits
                    (not required for basic usage)
        """
        self.api_key = api_key
        self.base_url = self.BASE_URL

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests"""
        headers = {"Accept": "application/json"}
        if self.api_key:
            headers["x-api-key"] = self.api_key
        return headers

    def search(
        self,
        query: str,
        limit: int = 10,
        fields: Optional[List[str]] = None
    ) -> List[SemanticScholarPaper]:
        """
        Search for papers (synchronous).

        Args:
            query: Search query
            limit: Maximum number of results (default: 10)
            fields: Fields to retrieve (default: DEFAULT_FIELDS)

        Returns:
            List of SemanticScholarPaper objects

        Raises:
            ImportError: If requests library not available
            Exception: If API request fails

        Example:
            >>> client = SemanticScholarClient()
            >>> papers = client.search("machine learning", limit=5)  # doctest: +SKIP
            >>> len(papers)  # doctest: +SKIP
            5
        """
        if not REQUESTS_AVAILABLE:
            raise ImportError("requests library required. Install with: pip install requests")

        fields = fields or self.DEFAULT_FIELDS

        try:
            url = f"{self.base_url}/paper/search"
            params = {
                "query": query,
                "limit": limit,
                "fields": ",".join(fields)
            }

            logger.info(f"Searching Semantic Scholar: '{query}' (limit={limit})")

            response = requests.get(
                url,
                params=params,
                headers=self._get_headers(),
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            papers = [
                SemanticScholarPaper.from_api_response(paper)
                for paper in data.get('data', [])
                if paper.get('title')
            ]

            logger.info(f"Found {len(papers)} papers")
            return papers

        except Exception as e:
            logger.error(f"Error searching Semantic Scholar: {e}")
            raise

    def get_by_doi(
        self,
        doi: str,
        fields: Optional[List[str]] = None
    ) -> Optional[SemanticScholarPaper]:
        """
        Get paper by DOI (synchronous).

        Args:
            doi: Paper DOI
            fields: Fields to retrieve (default: DEFAULT_FIELDS)

        Returns:
            SemanticScholarPaper or None if not found

        Example:
            >>> client = SemanticScholarClient()
            >>> paper = client.get_by_doi("10.1234/example")  # doctest: +SKIP
        """
        if not REQUESTS_AVAILABLE:
            raise ImportError("requests library required. Install with: pip install requests")

        fields = fields or self.DEFAULT_FIELDS

        try:
            url = f"{self.base_url}/paper/{doi}"
            params = {"fields": ",".join(fields)}

            logger.info(f"Fetching paper by DOI: {doi}")

            response = requests.get(
                url,
                params=params,
                headers=self._get_headers(),
                timeout=30
            )

            if response.status_code == 404:
                logger.info(f"Paper not found: {doi}")
                return None

            response.raise_for_status()

            data = response.json()
            paper = SemanticScholarPaper.from_api_response(data)

            logger.info(f"Retrieved paper: {paper.title}")
            return paper

        except Exception as e:
            logger.error(f"Error fetching paper by DOI: {e}")
            raise

    def get_by_arxiv_id(
        self,
        arxiv_id: str,
        fields: Optional[List[str]] = None
    ) -> Optional[SemanticScholarPaper]:
        """
        Get paper by arXiv ID (synchronous).

        Args:
            arxiv_id: arXiv paper ID (e.g., "2301.07041")
            fields: Fields to retrieve (default: DEFAULT_FIELDS)

        Returns:
            SemanticScholarPaper or None if not found

        Example:
            >>> client = SemanticScholarClient()
            >>> paper = client.get_by_arxiv_id("2301.07041")  # doctest: +SKIP
        """
        # Clean arXiv ID
        clean_id = arxiv_id.replace('arxiv:', '').replace('arXiv:', '')
        return self.get_by_doi(f"arXiv:{clean_id}", fields)

    async def search_async(
        self,
        query: str,
        limit: int = 10,
        fields: Optional[List[str]] = None
    ) -> List[SemanticScholarPaper]:
        """
        Search for papers (asynchronous).

        Args:
            query: Search query
            limit: Maximum number of results (default: 10)
            fields: Fields to retrieve (default: DEFAULT_FIELDS)

        Returns:
            List of SemanticScholarPaper objects

        Raises:
            ImportError: If aiohttp library not available
        """
        if not AIOHTTP_AVAILABLE:
            raise ImportError("aiohttp library required. Install with: pip install aiohttp")

        fields = fields or self.DEFAULT_FIELDS

        try:
            url = f"{self.base_url}/paper/search"
            params = {
                "query": query,
                "limit": limit,
                "fields": ",".join(fields)
            }

            logger.info(f"Searching Semantic Scholar (async): '{query}' (limit={limit})")

            async with aiohttp.ClientSession(headers=self._get_headers()) as session:
                async with session.get(url, params=params, timeout=30) as response:
                    response.raise_for_status()
                    data = await response.json()

                    papers = [
                        SemanticScholarPaper.from_api_response(paper)
                        for paper in data.get('data', [])
                        if paper.get('title')
                    ]

                    logger.info(f"Found {len(papers)} papers")
                    return papers

        except Exception as e:
            logger.error(f"Error searching Semantic Scholar (async): {e}")
            raise


# Convenience functions
def search_papers(query: str, limit: int = 10) -> List[Dict]:
    """
    Convenience function to search papers (returns dicts).

    Args:
        query: Search query
        limit: Maximum number of results

    Returns:
        List of paper dictionaries
    """
    client = SemanticScholarClient()
    papers = client.search(query, limit)
    return [paper.to_dict() for paper in papers]


def get_paper_by_doi(doi: str) -> Optional[Dict]:
    """
    Convenience function to get paper by DOI (returns dict).

    Args:
        doi: Paper DOI

    Returns:
        Paper dictionary or None
    """
    client = SemanticScholarClient()
    paper = client.get_by_doi(doi)
    return paper.to_dict() if paper else None

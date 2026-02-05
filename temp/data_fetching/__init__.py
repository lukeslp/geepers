"""
Data fetching utilities for external APIs

This module provides clients for common data sources used across projects.
"""

from .census_client import CensusClient
from .arxiv_client import ArxivClient, ArxivPaper, search_arxiv, get_paper_by_id
from .archive_client import (
    ArchiveClient,
    ArchivedSnapshot,
    ArchiveResult,
    archive_url,
    get_latest_archive,
)
from .semantic_scholar import (
    SemanticScholarClient,
    SemanticScholarPaper,
    search_papers,
    get_paper_by_doi,
)
from .github_client import GitHubClient
from .wikipedia_client import WikipediaClient
from .news_client import NewsClient
from .weather_client import WeatherClient
from .openlibrary_client import OpenLibraryClient
from .nasa_client import NASAClient
from .youtube_client import YouTubeClient
from .finance_client import FinanceClient

__all__ = [
    "CensusClient",
    "ArxivClient",
    "ArxivPaper",
    "search_arxiv",
    "get_paper_by_id",
    "ArchiveClient",
    "ArchivedSnapshot",
    "ArchiveResult",
    "archive_url",
    "get_latest_archive",
    "SemanticScholarClient",
    "SemanticScholarPaper",
    "search_papers",
    "get_paper_by_doi",
    "GitHubClient",
    "WikipediaClient",
    "NewsClient",
    "WeatherClient",
    "OpenLibraryClient",
    "NASAClient",
    "YouTubeClient",
    "FinanceClient",
]

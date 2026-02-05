"""
Data Fetching Factory

Factory pattern for creating data fetching clients.

Author: Luke Steuber
"""

from typing import Any, List
import logging

logger = logging.getLogger(__name__)


class DataFetchingFactory:
    """Factory for creating data fetching clients."""

    @staticmethod
    def create_client(source: str, **kwargs) -> Any:
        """
        Create a data fetching client.

        Args:
            source: Data source name
            **kwargs: Client-specific arguments

        Returns:
            Client instance

        Raises:
            ValueError: If source is unknown
        """
        source = source.lower()

        if source == "census":
            from .census_client import CensusClient
            return CensusClient(**kwargs)

        elif source == "arxiv":
            from .arxiv_client import ArxivClient
            return ArxivClient(**kwargs)

        elif source == "semantic_scholar" or source == "semanticscholar":
            from .semantic_scholar import SemanticScholarClient
            return SemanticScholarClient(**kwargs)

        elif source == "archive" or source == "wayback":
            from .archive_client import ArchiveClient
            return ArchiveClient(**kwargs)

        elif source == "github":
            from .github_client import GitHubClient
            return GitHubClient(**kwargs)

        elif source == "wikipedia" or source == "wiki":
            from .wikipedia_client import WikipediaClient
            return WikipediaClient(**kwargs)

        elif source == "news":
            from .news_client import NewsClient
            return NewsClient(**kwargs)

        elif source == "weather" or source == "noaa":
            from .weather_client import WeatherClient
            return WeatherClient(**kwargs)

        elif source == "openlibrary" or source == "books":
            from .openlibrary_client import OpenLibraryClient
            return OpenLibraryClient(**kwargs)

        elif source == "nasa":
            from .nasa_client import NASAClient
            return NASAClient(**kwargs)

        elif source == "youtube":
            from .youtube_client import YouTubeClient
            return YouTubeClient(**kwargs)

        elif source in {"finance", "alphavantage", "alpha_vantage"}:
            from .finance_client import FinanceClient
            return FinanceClient(**kwargs)

        else:
            raise ValueError(
                f"Unknown data source: {source}. "
                f"Available: census, arxiv, semantic_scholar, archive, github, "
                f"wikipedia, news, weather, openlibrary, nasa, youtube, finance"
            )

    @staticmethod
    def list_sources() -> List[str]:
        """
        List all available data sources.

        Returns:
            List of source names
        """
        return [
            "census",
            "arxiv",
            "semantic_scholar",
            "archive",
            "github",
            "wikipedia",
            "news",
            "weather",
            "openlibrary",
            "nasa",
            "youtube",
            "finance",
        ]

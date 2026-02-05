#!/usr/bin/env python3
"""
BBC News RSS Client

Description: Client for fetching news articles from BBC News RSS feeds with support
             for multiple categories and full article content extraction.

Use Cases:
- News aggregation and monitoring
- Current events tracking for AI agents
- Research and content gathering
- Building news digest applications
- Media monitoring systems

Dependencies:
- requests
- beautifulsoup4

Notes:
- Uses public BBC RSS feeds (no API key required)
- Supports 20+ news categories (world, tech, business, etc.)
- Article content extraction requires BeautifulSoup
- Returns structured data with title, description, link, and date
- Media thumbnails extracted when available

Related Snippets:
- api-clients/jina_web_scraper.py (alternative web content extraction)

Source Attribution:
- Extracted from: /home/coolhand/inbox/scratchpad/to_strip/bbc_news.py
- Original authors: nathanwindisch, igna503 (MIT License)
- Adapted by: Luke Steuber
"""

import re
import json
import logging
import requests
import xml.etree.ElementTree as ElementTree
from typing import Dict, List, Any, Optional
from datetime import datetime

# Optional BeautifulSoup for article extraction
try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

logger = logging.getLogger(__name__)

# BBC News categories and their RSS feed endpoints
BBC_CATEGORIES = {
    "top_stories": "",
    "world": "world",
    "uk": "uk",
    "business": "business",
    "politics": "politics",
    "health": "health",
    "education": "education",
    "science_and_environment": "science_and_environment",
    "technology": "technology",
    "entertainment_and_arts": "entertainment_and_arts",
    "england": "england",
    "northern_ireland": "northern_ireland",
    "scotland": "scotland",
    "wales": "wales",
    "africa": "world/africa",
    "asia": "world/asia",
    "australia": "world/australia",
    "europe": "world/europe",
    "latin_america": "world/latin_america",
    "middle_east": "world/middle_east",
    "us_and_canada": "world/us_and_canada",
}

# Regex to match BBC News article URLs
BBC_URI_REGEX = re.compile(
    r"^(https?:\/\/)(www\.)?bbc\.(com|co\.uk)\/news\/(articles|videos|\w+(-\w+)*-\d+).*$"
)


class BBCNewsClient:
    """
    BBC News RSS feed client.

    Fetches news articles from BBC's public RSS feeds and optionally
    extracts full article content.

    Features:
    - 20+ category feeds
    - Structured article data
    - Media thumbnail extraction
    - Full article content extraction (with BeautifulSoup)
    """

    BASE_FEED_URL = "https://feeds.bbci.co.uk/news"
    USER_AGENT = "BBCNewsClient/1.0"

    def __init__(self, user_agent: Optional[str] = None):
        """
        Initialize BBC News client.

        Args:
            user_agent: Optional custom user agent string
        """
        self.user_agent = user_agent or self.USER_AGENT

    @staticmethod
    def get_categories() -> List[str]:
        """Get list of available news categories."""
        return list(BBC_CATEGORIES.keys())

    def get_feed_url(self, category: str) -> str:
        """
        Get RSS feed URL for a category.

        Args:
            category: Category key from BBC_CATEGORIES

        Returns:
            Full RSS feed URL
        """
        if category not in BBC_CATEGORIES:
            raise ValueError(f"Invalid category: {category}. Use get_categories() for valid options.")

        category_path = BBC_CATEGORIES[category]
        if category == "top_stories" or not category_path:
            return f"{self.BASE_FEED_URL}/rss.xml"
        return f"{self.BASE_FEED_URL}/{category_path}/rss.xml"

    def get_feed(self, category: str = "top_stories") -> Dict[str, Any]:
        """
        Get news articles from a BBC RSS feed.

        Args:
            category: News category (default: top_stories)

        Returns:
            Dictionary with success status and list of articles
        """
        try:
            feed_url = self.get_feed_url(category)
            headers = {"User-Agent": self.user_agent}

            response = requests.get(feed_url, headers=headers, timeout=15)
            response.raise_for_status()

            articles = self._parse_feed(response.content)

            return {
                "success": True,
                "category": category,
                "display_category": self._format_category(category),
                "count": len(articles),
                "articles": articles,
            }

        except ValueError as e:
            return {"success": False, "error": str(e)}
        except requests.RequestException as e:
            logger.error(f"Error fetching BBC feed: {e}")
            return {"success": False, "error": str(e), "category": category}

    def get_articles(self, category: str = "top_stories") -> List[Dict[str, Any]]:
        """
        Get just the articles list from a feed.

        Args:
            category: News category

        Returns:
            List of article dictionaries
        """
        result = self.get_feed(category)
        if result.get("success"):
            return result.get("articles", [])
        return []

    def get_article_content(self, url: str) -> Dict[str, Any]:
        """
        Extract full content from a BBC News article.

        Requires BeautifulSoup to be installed.

        Args:
            url: BBC News article URL

        Returns:
            Dictionary with title and content paragraphs
        """
        if not BS4_AVAILABLE:
            return {"success": False, "error": "BeautifulSoup not installed"}

        if not self._is_valid_bbc_url(url):
            return {"success": False, "error": "Invalid BBC News URL"}

        try:
            headers = {"User-Agent": self.user_agent}
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")
            article = soup.find("article")

            if not article:
                return {"success": False, "error": "Article content not found", "url": url}

            # Extract title
            title_tag = soup.find("h1")
            title = title_tag.text.strip() if title_tag else ""

            # Extract paragraphs
            paragraphs = []
            for p in article.find_all("p"):
                # Skip captions and summaries
                if p.parent.name not in ["figcaption", "summary"]:
                    text = p.text.strip()
                    if text:
                        paragraphs.append(text)

            # Join as full text
            content = "\n\n".join(paragraphs)

            return {
                "success": True,
                "url": url,
                "title": title,
                "content": content,
                "paragraph_count": len(paragraphs),
            }

        except requests.RequestException as e:
            logger.error(f"Error fetching article: {e}")
            return {"success": False, "error": str(e), "url": url}

    def _parse_feed(self, xml_content: bytes) -> List[Dict[str, Any]]:
        """Parse RSS feed XML into article list."""
        articles = []

        try:
            root = ElementTree.fromstring(xml_content)

            for item in root.iter("item"):
                title_el = item.find("title")
                desc_el = item.find("description")
                link_el = item.find("link")
                date_el = item.find("pubDate")

                # Get media thumbnail if available
                media = item.find(".//{http://search.yahoo.com/mrss/}thumbnail")
                media_url = media.get("url") if media is not None else None

                articles.append({
                    "title": title_el.text if title_el is not None else "",
                    "description": desc_el.text if desc_el is not None else "",
                    "link": link_el.text if link_el is not None else "",
                    "published": date_el.text if date_el is not None else "",
                    "image_url": media_url,
                })

        except ElementTree.ParseError as e:
            logger.error(f"Error parsing RSS feed: {e}")

        return articles

    @staticmethod
    def _format_category(category: str) -> str:
        """Format category key as display name."""
        return category.replace("_", " ").title()

    @staticmethod
    def _is_valid_bbc_url(url: str) -> bool:
        """Check if URL is a valid BBC News article URL."""
        if not url:
            return False
        if BBC_URI_REGEX.match(url):
            return True
        if url.startswith("https://www.bbc.com/news/") or url.startswith("https://www.bbc.co.uk/news/"):
            return True
        return False


def get_top_headlines(count: int = 10) -> List[Dict[str, Any]]:
    """
    Convenience function to get top BBC headlines.

    Args:
        count: Maximum number of headlines to return

    Returns:
        List of article dictionaries
    """
    client = BBCNewsClient()
    articles = client.get_articles("top_stories")
    return articles[:count]


def get_category_headlines(category: str, count: int = 10) -> List[Dict[str, Any]]:
    """
    Get headlines from a specific category.

    Args:
        category: BBC News category
        count: Maximum number of headlines

    Returns:
        List of article dictionaries
    """
    client = BBCNewsClient()
    articles = client.get_articles(category)
    return articles[:count]


def format_for_llm(articles: List[Dict[str, Any]], max_articles: int = 5) -> str:
    """
    Format articles for LLM context.

    Args:
        articles: List of article dictionaries
        max_articles: Maximum articles to include

    Returns:
        Formatted string for LLM context
    """
    output = ["# BBC News Headlines\n"]

    for i, article in enumerate(articles[:max_articles], 1):
        output.append(f"## {i}. {article['title']}")
        output.append(f"*Published: {article['published']}*\n")
        output.append(article["description"] or "No description available")
        output.append(f"\n[Read more]({article['link']})\n")

    return "\n".join(output)


# Usage example
if __name__ == "__main__":
    print("BBC News Client Demo")
    print("=" * 50)

    client = BBCNewsClient()

    # Show available categories
    print("\nAvailable categories:")
    categories = client.get_categories()
    for i, cat in enumerate(categories, 1):
        print(f"  {i:2}. {cat}")

    # Fetch top stories
    print("\n" + "-" * 50)
    print("Fetching top stories...")

    result = client.get_feed("top_stories")

    if result["success"]:
        print(f"Found {result['count']} articles\n")

        for article in result["articles"][:5]:
            print(f"  {article['title'][:60]}...")
            if article.get("published"):
                print(f"    Published: {article['published']}")
            print()
    else:
        print(f"Error: {result.get('error')}")

    # Fetch technology news
    print("-" * 50)
    print("Fetching technology news...")

    tech_articles = client.get_articles("technology")
    print(f"Found {len(tech_articles)} technology articles\n")

    for article in tech_articles[:3]:
        print(f"  {article['title'][:60]}...")

    # Demo LLM formatting
    print("\n" + "-" * 50)
    print("LLM-formatted output:\n")
    print(format_for_llm(tech_articles, max_articles=3))

    # Test article extraction (if BeautifulSoup available)
    if BS4_AVAILABLE and tech_articles:
        print("-" * 50)
        print("Testing article extraction...")
        url = tech_articles[0]["link"]
        content = client.get_article_content(url)
        if content["success"]:
            print(f"Title: {content['title']}")
            print(f"Paragraphs: {content['paragraph_count']}")
            print(f"Content preview: {content['content'][:200]}...")
        else:
            print(f"Could not extract: {content.get('error')}")

#!/usr/bin/env python3
"""
Jina Reader Web Scraper

Description: Web scraping client using Jina Reader API (r.jina.ai) to extract clean,
             markdown-formatted text content from web pages. Useful for LLM processing
             as it removes navigation, ads, and other non-content elements.

Use Cases:
- Web content extraction for RAG pipelines
- Clean text extraction for LLM context
- Research and data gathering automation
- Content archiving and analysis
- Bypassing JavaScript-rendered pages

Dependencies:
- requests

Notes:
- Jina Reader converts web pages to clean markdown
- Free tier available with rate limits
- API key optional but recommended for higher rate limits
- Supports caching control and alt-text generation
- Returns structured content with Title, URL, and cleaned text

Related Snippets:
- api-clients/multi_provider_abstraction.py
- utilities/retry_decorator.py

Source Attribution:
- Extracted from: /home/coolhand/inbox/scratchpad/tools_collection/chat_apis/
- Original authors: ekatiyar, Pyotr Growpotkin (MIT License)
- Adapted by: Luke Steuber
"""

import requests
import re
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class JinaReaderClient:
    """
    Client for Jina Reader web scraping API.

    Jina Reader (r.jina.ai) extracts clean, readable content from web pages
    in markdown format, ideal for LLM processing.

    Features:
    - Removes ads, navigation, and boilerplate
    - Converts to clean markdown
    - Handles JavaScript-rendered pages
    - Optional image alt-text generation
    - Configurable caching
    """

    def __init__(self, api_key: Optional[str] = None, disable_cache: bool = False):
        """
        Initialize Jina Reader client.

        Args:
            api_key: Optional Jina API key for higher rate limits
            disable_cache: Bypass Jina's cache for fresh content
        """
        self.api_key = api_key
        self.disable_cache = disable_cache
        self.base_url = "https://r.jina.ai"

    def scrape(
        self,
        url: str,
        clean_urls: bool = True,
        generate_alt: bool = True,
    ) -> Dict[str, Any]:
        """
        Scrape a web page and extract clean content.

        Args:
            url: URL to scrape
            clean_urls: Remove URLs from content (reduces tokens)
            generate_alt: Generate alt text for images

        Returns:
            Dictionary with title, url, content, and success status
        """
        jina_url = f"{self.base_url}/{url}"

        headers = {
            "X-No-Cache": "true" if self.disable_cache else "false",
            "X-With-Generated-Alt": "true" if generate_alt else "false",
        }

        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            response = requests.get(jina_url, headers=headers, timeout=30)
            response.raise_for_status()

            content = response.text

            # Extract title from response
            title = self._extract_title(content)

            # Clean URLs if requested
            if clean_urls:
                content = self._clean_urls(content)

            return {
                "success": True,
                "url": url,
                "title": title,
                "content": content,
                "content_length": len(content),
            }

        except requests.Timeout:
            logger.error(f"Timeout scraping {url}")
            return {"success": False, "url": url, "error": "Request timed out"}

        except requests.RequestException as e:
            logger.error(f"Error scraping {url}: {e}")
            return {"success": False, "url": url, "error": str(e)}

    def scrape_text(self, url: str, clean_urls: bool = True) -> Optional[str]:
        """
        Simple text extraction.

        Args:
            url: URL to scrape
            clean_urls: Remove URLs from content

        Returns:
            Extracted text content or None on error
        """
        result = self.scrape(url, clean_urls=clean_urls)
        if result.get("success"):
            return result.get("content")
        return None

    def scrape_multiple(
        self,
        urls: list,
        clean_urls: bool = True,
    ) -> list:
        """
        Scrape multiple URLs.

        Args:
            urls: List of URLs to scrape
            clean_urls: Remove URLs from content

        Returns:
            List of result dictionaries
        """
        results = []
        for url in urls:
            result = self.scrape(url, clean_urls=clean_urls)
            results.append(result)
        return results

    @staticmethod
    def _extract_title(text: str) -> Optional[str]:
        """Extract title from Jina response."""
        match = re.search(r'Title: (.*)\n', text)
        return match.group(1).strip() if match else None

    @staticmethod
    def _clean_urls(text: str) -> str:
        """Remove markdown URLs from text to reduce token count."""
        # Remove markdown link URLs but keep link text
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        # Remove standalone URLs in parentheses
        text = re.sub(r'\((http[^)]+)\)', '', text)
        # Remove bare URLs
        text = re.sub(r'https?://\S+', '', text)
        return text


def scrape_url(url: str, api_key: Optional[str] = None) -> Optional[str]:
    """
    Convenience function for simple URL scraping.

    Args:
        url: URL to scrape
        api_key: Optional Jina API key

    Returns:
        Extracted text content or None
    """
    client = JinaReaderClient(api_key=api_key)
    return client.scrape_text(url)


def scrape_for_llm(url: str, api_key: Optional[str] = None, max_chars: int = 10000) -> str:
    """
    Scrape URL and format for LLM context.

    Args:
        url: URL to scrape
        api_key: Optional Jina API key
        max_chars: Maximum characters to return (truncates if longer)

    Returns:
        Formatted string for LLM context
    """
    client = JinaReaderClient(api_key=api_key)
    result = client.scrape(url, clean_urls=True)

    if not result.get("success"):
        return f"Error scraping {url}: {result.get('error', 'Unknown error')}"

    content = result["content"]
    title = result.get("title", "Unknown Title")

    # Truncate if too long
    if len(content) > max_chars:
        content = content[:max_chars] + "\n\n[Content truncated...]"

    return f"# {title}\nSource: {url}\n\n{content}"


# Usage example
if __name__ == "__main__":
    import os

    print("Jina Reader Web Scraper Demo")
    print("=" * 50)

    api_key = os.environ.get("JINA_API_KEY")

    if api_key:
        print(f"Using API key: {api_key[:8]}...")
    else:
        print("No API key set (using free tier with rate limits)")
        print("Set JINA_API_KEY environment variable for higher limits\n")

    # Test URLs
    test_urls = [
        "https://toscrape.com/",
        "https://example.com/",
    ]

    client = JinaReaderClient(api_key=api_key)

    for url in test_urls:
        print(f"\nScraping: {url}")
        print("-" * 30)

        result = client.scrape(url, clean_urls=True)

        if result["success"]:
            print(f"Title: {result.get('title', 'N/A')}")
            print(f"Content length: {result['content_length']} chars")
            # Show first 200 chars
            preview = result["content"][:200].replace("\n", " ")
            print(f"Preview: {preview}...")
        else:
            print(f"Error: {result.get('error')}")

    # Demo LLM formatting
    print("\n" + "=" * 50)
    print("LLM-formatted output demo:")
    print("-" * 30)
    llm_content = scrape_for_llm("https://example.com/", max_chars=500)
    print(llm_content)

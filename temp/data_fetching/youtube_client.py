"""
YouTube Data API Client

Provides a lightweight wrapper around the YouTube Data API v3 for common tasks:
- Searching for videos
- Fetching channel statistics
- Retrieving playlist items

The client focuses on JSON-friendly responses suitable for downstream tools.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

import requests


class YouTubeClient:
    """Client for interacting with the YouTube Data API v3."""

    BASE_URL = "https://www.googleapis.com/youtube/v3"

    def __init__(
        self,
        api_key: Optional[str] = None,
        timeout: int = 30,
    ) -> None:
        """
        Initialize YouTube client.

        Args:
            api_key: YouTube Data API key. Falls back to YOUTUBE_API_KEY env var.
            timeout: HTTP request timeout in seconds.

        Raises:
            RuntimeError: If the API key is missing.
        """
        self.api_key = api_key or os.getenv("YOUTUBE_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "YouTube API key not configured. "
                "Set YOUTUBE_API_KEY or provide via constructor."
            )

        self.timeout = timeout
        self.session = requests.Session()

    def _request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Internal helper to perform a GET request against the API."""
        params = {**params, "key": self.api_key}
        response = self.session.get(
            f"{self.BASE_URL}/{endpoint}",
            params=params,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def search_videos(
        self,
        query: str,
        max_results: int = 10,
        order: str = "relevance",
        safe_search: str = "moderate",
        video_duration: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Search for videos on YouTube.

        Args:
            query: Search query string.
            max_results: Number of results to return (max 50).
            order: Sorting order (e.g., relevance, viewCount, date).
            safe_search: Safety filtering (none, moderate, strict).
            video_duration: Optional duration filter (any, short, medium, long).

        Returns:
            Dict containing the search metadata and simplified video records.
        """
        params: Dict[str, Any] = {
            "part": "snippet",
            "type": "video",
            "q": query,
            "maxResults": max(1, min(max_results, 50)),
            "order": order,
            "safeSearch": safe_search,
        }

        if video_duration:
            params["videoDuration"] = video_duration

        data = self._request("search", params)
        videos: List[Dict[str, Any]] = []
        for item in data.get("items", []):
            snippet = item.get("snippet", {})
            videos.append(
                {
                    "video_id": item.get("id", {}).get("videoId"),
                    "title": snippet.get("title"),
                    "description": snippet.get("description"),
                    "channel_title": snippet.get("channelTitle"),
                    "channel_id": snippet.get("channelId"),
                    "publish_time": snippet.get("publishTime"),
                    "thumbnails": snippet.get("thumbnails", {}),
                }
            )

        return {
            "query": query,
            "total_results": len(videos),
            "videos": videos,
            "next_page_token": data.get("nextPageToken"),
        }

    def get_channel_statistics(
        self,
        channel_id: str,
    ) -> Dict[str, Any]:
        """
        Fetch statistics and snippet details for a channel.

        Args:
            channel_id: YouTube channel ID.

        Returns:
            Dict containing channel metadata and statistics.
        """
        data = self._request(
            "channels",
            {
                "part": "snippet,statistics,brandingSettings",
                "id": channel_id,
            },
        )

        if not data.get("items"):
            return {"error": f"Channel {channel_id} not found"}

        item = data["items"][0]
        snippet = item.get("snippet", {})
        statistics = item.get("statistics", {})
        branding = item.get("brandingSettings", {}).get("channel", {})

        return {
            "channel_id": channel_id,
            "title": snippet.get("title"),
            "description": snippet.get("description"),
            "published_at": snippet.get("publishedAt"),
            "custom_url": snippet.get("customUrl"),
            "thumbnails": snippet.get("thumbnails", {}),
            "country": snippet.get("country"),
            "view_count": int(statistics.get("viewCount", 0)),
            "subscriber_count": int(statistics.get("subscriberCount", 0))
            if statistics.get("hiddenSubscriberCount") is not True
            else None,
            "video_count": int(statistics.get("videoCount", 0)),
            "keywords": branding.get("keywords"),
        }

    def get_playlist_items(
        self,
        playlist_id: str,
        max_results: int = 25,
    ) -> Dict[str, Any]:
        """
        Retrieve items from a playlist (e.g., uploads).

        Args:
            playlist_id: YouTube playlist ID.
            max_results: Number of items to return (max 50).

        Returns:
            Dict with playlist metadata and list of videos.
        """
        data = self._request(
            "playlistItems",
            {
                "part": "snippet,contentDetails",
                "playlistId": playlist_id,
                "maxResults": max(1, min(max_results, 50)),
            },
        )

        items: List[Dict[str, Any]] = []
        for item in data.get("items", []):
            snippet = item.get("snippet", {})
            content_details = item.get("contentDetails", {})
            items.append(
                {
                    "video_id": content_details.get("videoId"),
                    "title": snippet.get("title"),
                    "description": snippet.get("description"),
                    "published_at": snippet.get("publishedAt"),
                    "position": snippet.get("position"),
                    "thumbnails": snippet.get("thumbnails", {}),
                }
            )

        return {
            "playlist_id": playlist_id,
            "items": items,
            "total_results": len(items),
            "next_page_token": data.get("nextPageToken"),
        }


__all__ = ["YouTubeClient"]


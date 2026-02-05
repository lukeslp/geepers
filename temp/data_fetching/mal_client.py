"""
MyAnimeList API Client

Provides access to MyAnimeList data for:
- Anime search and details
- Manga search and details
- User lists and recommendations
- Seasonal anime
- Top rankings

API Documentation: https://myanimelist.net/apiconfig/references/api/v2

Author: Luke Steuber
"""

import os
import requests
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)


class MyAnimeListClient:
    """Client for MyAnimeList API v2."""

    BASE_URL = "https://api.myanimelist.net/v2"

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize MAL client.

        Args:
            api_key: MAL API client ID
        """
        self.api_key = api_key or os.getenv('MAL_API_KEY') or os.getenv('MYANIMELIST_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "MyAnimeList API key is required. Get one at https://myanimelist.net/apiconfig "
                "and set MAL_API_KEY environment variable"
            )

        self.session = requests.Session()
        self.session.headers.update({
            'X-MAL-CLIENT-ID': self.api_key
        })

    def search_anime(
        self,
        query: str,
        limit: int = 10,
        fields: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Search for anime.

        Args:
            query: Search query
            limit: Max results
            fields: Comma-separated field list (e.g., "mean,rank,popularity")

        Returns:
            Dict with anime results
        """
        try:
            params = {'q': query, 'limit': limit}
            if fields:
                params['fields'] = fields
            else:
                params['fields'] = 'mean,rank,popularity,num_episodes,genres,studios'

            response = self.session.get(
                f"{self.BASE_URL}/anime",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            anime_list = []
            for item in data.get('data', []):
                node = item.get('node', {})
                anime_list.append({
                    "id": node.get("id"),
                    "title": node.get("title"),
                    "mean_score": node.get("mean"),
                    "rank": node.get("rank"),
                    "popularity": node.get("popularity"),
                    "num_episodes": node.get("num_episodes"),
                    "genres": [g.get("name") for g in node.get("genres", [])],
                    "studios": [s.get("name") for s in node.get("studios", [])],
                })

            return {"anime": anime_list, "total": len(anime_list)}

        except requests.exceptions.RequestException as e:
            logger.error(f"MAL API error searching anime: {e}")
            return {"error": str(e), "anime": []}

    def get_anime_details(self, anime_id: int) -> Dict[str, Any]:
        """Get detailed info for an anime."""
        try:
            response = self.session.get(
                f"{self.BASE_URL}/anime/{anime_id}",
                params={'fields': 'synopsis,mean,rank,popularity,num_episodes,start_season,genres,studios,rating'},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            return {
                "id": data.get("id"),
                "title": data.get("title"),
                "synopsis": data.get("synopsis"),
                "mean_score": data.get("mean"),
                "rank": data.get("rank"),
                "popularity": data.get("popularity"),
                "num_episodes": data.get("num_episodes"),
                "start_season": data.get("start_season"),
                "genres": [g.get("name") for g in data.get("genres", [])],
                "studios": [s.get("name") for s in data.get("studios", [])],
                "rating": data.get("rating"),
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"MAL API error getting anime details: {e}")
            return {"error": str(e)}

    def get_season_anime(self, year: int, season: str, limit: int = 20) -> Dict[str, Any]:
        """
        Get anime for a season.

        Args:
            year: Year
            season: winter, spring, summer, fall
            limit: Max results

        Returns:
            Dict with seasonal anime
        """
        try:
            response = self.session.get(
                f"{self.BASE_URL}/anime/season/{year}/{season}",
                params={'limit': limit, 'fields': 'mean,rank,genres'},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            anime_list = []
            for item in data.get('data', []):
                node = item.get('node', {})
                anime_list.append({
                    "id": node.get("id"),
                    "title": node.get("title"),
                    "mean_score": node.get("mean"),
                    "genres": [g.get("name") for g in node.get("genres", [])],
                })

            return {"anime": anime_list, "season": f"{season} {year}"}

        except requests.exceptions.RequestException as e:
            logger.error(f"MAL API error getting season anime: {e}")
            return {"error": str(e), "anime": []}

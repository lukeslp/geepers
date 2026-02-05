"""
NASA API Client

Provides access to NASA APIs:
- Astronomy Picture of the Day (APOD)
- Mars Rover Photos
- Earth Imagery
- NEO (Near Earth Objects)

Requires NASA_API_KEY (or uses DEMO_KEY with limits).

Author: Luke Steuber
"""

import os
import requests
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class NASAClient:
    """Client for NASA APIs."""

    BASE_URL = "https://api.nasa.gov"

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize NASA client.

        Args:
            api_key: NASA API key (defaults to DEMO_KEY if not provided)
        """
        self.api_key = api_key or os.getenv('NASA_API_KEY') or 'DEMO_KEY'
        self.session = requests.Session()

    def get_apod(self, date: Optional[str] = None, count: Optional[int] = None) -> Dict[str, Any]:
        """
        Get Astronomy Picture of the Day.

        Args:
            date: Date in YYYY-MM-DD format (default: today)
            count: Number of random APODs (ignores date if set)

        Returns:
            Dict with APOD data
        """
        try:
            params = {'api_key': self.api_key}

            if count:
                params['count'] = count
            elif date:
                params['date'] = date

            response = self.session.get(
                f"{self.BASE_URL}/planetary/apod",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            # Handle single vs multiple results
            if isinstance(data, list):
                return {"apods": data, "count": len(data)}
            else:
                return {
                    "date": data.get("date"),
                    "title": data.get("title"),
                    "explanation": data.get("explanation"),
                    "url": data.get("url"),
                    "hdurl": data.get("hdurl"),
                    "media_type": data.get("media_type"),
                    "copyright": data.get("copyright")
                }
        except Exception as e:
            logger.error(f"NASA APOD error: {e}")
            return {"error": str(e)}

    def get_mars_photos(
        self,
        sol: int,
        rover: str = "curiosity",
        camera: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get Mars Rover photos.

        Args:
            sol: Martian sol (day)
            rover: Rover name (curiosity, opportunity, spirit)
            camera: Specific camera (FHAZ, RHAZ, MAST, etc.)

        Returns:
            Dict with Mars photos
        """
        try:
            params = {'sol': sol, 'api_key': self.api_key}

            if camera:
                params['camera'] = camera

            response = self.session.get(
                f"{self.BASE_URL}/mars-photos/api/v1/rovers/{rover}/photos",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            photos = []
            for photo in data.get('photos', []):
                photos.append({
                    "id": photo.get("id"),
                    "sol": photo.get("sol"),
                    "camera": photo.get("camera", {}).get("name"),
                    "img_src": photo.get("img_src"),
                    "earth_date": photo.get("earth_date"),
                    "rover": photo.get("rover", {}).get("name")
                })

            return {
                "rover": rover,
                "sol": sol,
                "photos": photos,
                "count": len(photos)
            }
        except Exception as e:
            logger.error(f"NASA Mars photos error: {e}")
            return {"error": str(e)}

    def get_earth_imagery(
        self,
        lat: float,
        lon: float,
        date: Optional[str] = None,
        dim: float = 0.025
    ) -> Dict[str, Any]:
        """
        Get Earth satellite imagery.

        Args:
            lat: Latitude
            lon: Longitude
            date: Date in YYYY-MM-DD format
            dim: Image width/height in degrees

        Returns:
            Dict with imagery URL and metadata
        """
        try:
            params = {
                'lat': lat,
                'lon': lon,
                'dim': dim,
                'api_key': self.api_key
            }

            if date:
                params['date'] = date

            response = self.session.get(
                f"{self.BASE_URL}/planetary/earth/imagery",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            return {
                "date": data.get("date"),
                "url": data.get("url"),
                "cloud_score": data.get("cloud_score"),
                "location": {"latitude": lat, "longitude": lon}
            }
        except Exception as e:
            logger.error(f"NASA Earth imagery error: {e}")
            return {"error": str(e)}

    def get_neo(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get Near Earth Objects data.

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)

        Returns:
            Dict with NEO data
        """
        if not start_date:
            start_date = datetime.now().strftime('%Y-%m-%d')
        if not end_date:
            end_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')

        try:
            response = self.session.get(
                f"{self.BASE_URL}/neo/rest/v1/feed",
                params={
                    'start_date': start_date,
                    'end_date': end_date,
                    'api_key': self.api_key
                },
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            return {
                "element_count": data.get("element_count", 0),
                "near_earth_objects": data.get("near_earth_objects", {}),
                "start_date": start_date,
                "end_date": end_date
            }
        except Exception as e:
            logger.error(f"NASA NEO error: {e}")
            return {"error": str(e)}


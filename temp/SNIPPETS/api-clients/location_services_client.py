#!/usr/bin/env python3
"""
Location Services Client (MapQuest, WalkScore, Air Quality)

Description: Unified client for location-based APIs including geocoding (MapQuest),
             walkability scores (WalkScore), and air quality data (WAQI).

Use Cases:
- Property evaluation and real estate tools
- Location-based recommendations
- Environmental monitoring dashboards
- Address geocoding and coordinate lookup
- Urban planning and livability analysis

Dependencies:
- requests

Notes:
- MapQuest provides forward geocoding (address to coordinates)
- WalkScore requires coordinates - use with MapQuest for full workflow
- Air Quality uses WAQI (World Air Quality Index) API
- All clients support async event emitters for progress tracking
- API keys required from respective services (free tiers available)

Related Snippets:
- api-clients/wolfram_alpha_client.py
- api-clients/multi_provider_abstraction.py

Source Attribution:
- Extracted from: /home/coolhand/inbox/apis/api-schema/tools/property/
- Author: Luke Steuber
"""

import requests
import logging
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)


class MapQuestClient:
    """
    MapQuest Geocoding API client.

    Converts addresses to geographic coordinates (latitude/longitude).
    Free tier: 15,000 transactions/month.
    """

    def __init__(self, api_key: str):
        """
        Initialize MapQuest client.

        Args:
            api_key: MapQuest API key from developer.mapquest.com
        """
        self.api_key = api_key
        self.base_url = "https://www.mapquestapi.com/geocoding/v1/address"

    def geocode(self, address: str) -> Dict[str, Any]:
        """
        Geocode an address to coordinates.

        Args:
            address: Full address string to geocode

        Returns:
            Dictionary with lat, lng, and formatted address
        """
        params = {
            "key": self.api_key,
            "location": address,
            "outFormat": "json",
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=15)
            response.raise_for_status()
            results = response.json().get("results", [])

            if not results or not results[0].get("locations"):
                return {"success": False, "error": f"No results for '{address}'"}

            location = results[0]["locations"][0]
            lat = location["latLng"]["lat"]
            lng = location["latLng"]["lng"]

            return {
                "success": True,
                "address": address,
                "lat": lat,
                "lng": lng,
                "formatted_address": location.get("street", ""),
                "city": location.get("adminArea5", ""),
                "state": location.get("adminArea3", ""),
                "country": location.get("adminArea1", ""),
                "postal_code": location.get("postalCode", ""),
            }

        except requests.RequestException as e:
            logger.error(f"MapQuest API error: {e}")
            return {"success": False, "error": str(e)}

    def get_coordinates(self, address: str) -> Optional[Tuple[float, float]]:
        """
        Simple coordinate lookup.

        Args:
            address: Address to geocode

        Returns:
            Tuple of (latitude, longitude) or None
        """
        result = self.geocode(address)
        if result.get("success"):
            return (result["lat"], result["lng"])
        return None


class WalkScoreClient:
    """
    WalkScore API client.

    Provides Walk Score, Transit Score, and Bike Score for locations.
    Free tier: 5,000 requests/day.
    """

    def __init__(self, api_key: str):
        """
        Initialize WalkScore client.

        Args:
            api_key: WalkScore API key from walkscore.com/professional/api
        """
        self.api_key = api_key
        self.base_url = "https://api.walkscore.com/score"

    def get_scores(self, address: str, lat: float, lng: float) -> Dict[str, Any]:
        """
        Get walkability scores for a location.

        Args:
            address: Street address
            lat: Latitude
            lng: Longitude

        Returns:
            Dictionary with walk_score, transit_score, bike_score
        """
        params = {
            "format": "json",
            "address": address,
            "lat": lat,
            "lon": lng,
            "wsapikey": self.api_key,
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            if data.get("status") != 1:
                return {"success": False, "error": f"No scores for '{address}'"}

            return {
                "success": True,
                "address": address,
                "walk_score": data.get("walkscore"),
                "walk_description": data.get("description"),
                "transit_score": data.get("transit", {}).get("score"),
                "transit_description": data.get("transit", {}).get("description"),
                "bike_score": data.get("bike", {}).get("score"),
                "bike_description": data.get("bike", {}).get("description"),
                "info_link": data.get("more_info_link"),
            }

        except requests.RequestException as e:
            logger.error(f"WalkScore API error: {e}")
            return {"success": False, "error": str(e)}

    def get_walk_score(self, address: str, lat: float, lng: float) -> Optional[int]:
        """
        Simple walk score lookup.

        Args:
            address: Street address
            lat: Latitude
            lng: Longitude

        Returns:
            Walk score (0-100) or None
        """
        result = self.get_scores(address, lat, lng)
        if result.get("success"):
            return result.get("walk_score")
        return None


class AirQualityClient:
    """
    World Air Quality Index (WAQI) API client.

    Provides real-time air quality data for cities worldwide.
    Free tier available with registration.
    """

    def __init__(self, api_key: str):
        """
        Initialize Air Quality client.

        Args:
            api_key: WAQI API token from aqicn.org/data-platform/token/
        """
        self.api_key = api_key
        self.base_url = "https://api.waqi.info/feed"

    def get_air_quality(self, city: str) -> Dict[str, Any]:
        """
        Get air quality data for a city.

        Args:
            city: City name or "geo:lat;lng" for coordinates

        Returns:
            Dictionary with AQI and pollutant data
        """
        url = f"{self.base_url}/{city}/?token={self.api_key}"

        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()

            if data.get("status") != "ok":
                return {"success": False, "error": f"No data for '{city}'"}

            aqi_data = data["data"]

            return {
                "success": True,
                "city": aqi_data["city"]["name"],
                "aqi": aqi_data["aqi"],
                "dominant_pollutant": aqi_data.get("dominentpol", "unknown"),
                "time": aqi_data.get("time", {}).get("s"),
                "info_url": aqi_data["city"].get("url"),
                "pollutants": {
                    "pm25": aqi_data.get("iaqi", {}).get("pm25", {}).get("v"),
                    "pm10": aqi_data.get("iaqi", {}).get("pm10", {}).get("v"),
                    "o3": aqi_data.get("iaqi", {}).get("o3", {}).get("v"),
                    "no2": aqi_data.get("iaqi", {}).get("no2", {}).get("v"),
                    "so2": aqi_data.get("iaqi", {}).get("so2", {}).get("v"),
                    "co": aqi_data.get("iaqi", {}).get("co", {}).get("v"),
                },
            }

        except requests.RequestException as e:
            logger.error(f"WAQI API error: {e}")
            return {"success": False, "error": str(e)}

    def get_aqi(self, city: str) -> Optional[int]:
        """
        Simple AQI lookup.

        Args:
            city: City name

        Returns:
            AQI value or None
        """
        result = self.get_air_quality(city)
        if result.get("success"):
            return result.get("aqi")
        return None

    def get_aqi_by_coords(self, lat: float, lng: float) -> Dict[str, Any]:
        """
        Get air quality by coordinates.

        Args:
            lat: Latitude
            lng: Longitude

        Returns:
            Air quality data dictionary
        """
        return self.get_air_quality(f"geo:{lat};{lng}")


class LocationServices:
    """
    Unified location services client combining all providers.

    Provides a convenient interface for complete location analysis.
    """

    def __init__(
        self,
        mapquest_key: Optional[str] = None,
        walkscore_key: Optional[str] = None,
        airquality_key: Optional[str] = None,
    ):
        """
        Initialize location services.

        Args:
            mapquest_key: MapQuest API key (optional)
            walkscore_key: WalkScore API key (optional)
            airquality_key: WAQI API key (optional)
        """
        self.mapquest = MapQuestClient(mapquest_key) if mapquest_key else None
        self.walkscore = WalkScoreClient(walkscore_key) if walkscore_key else None
        self.airquality = AirQualityClient(airquality_key) if airquality_key else None

    def analyze_location(self, address: str) -> Dict[str, Any]:
        """
        Complete location analysis combining all available services.

        Args:
            address: Full address to analyze

        Returns:
            Dictionary with geocoding, walkability, and air quality data
        """
        result = {
            "address": address,
            "geocoding": None,
            "walkability": None,
            "air_quality": None,
        }

        # Step 1: Geocode
        if self.mapquest:
            geo = self.mapquest.geocode(address)
            result["geocoding"] = geo

            if geo.get("success"):
                lat, lng = geo["lat"], geo["lng"]

                # Step 2: Walk Score (requires coordinates)
                if self.walkscore:
                    result["walkability"] = self.walkscore.get_scores(address, lat, lng)

                # Step 3: Air Quality (can use coordinates)
                if self.airquality:
                    result["air_quality"] = self.airquality.get_aqi_by_coords(lat, lng)

        elif self.airquality:
            # Can still get air quality by city name
            city = address.split(",")[0].strip()
            result["air_quality"] = self.airquality.get_air_quality(city)

        return result


def interpret_aqi(aqi: int) -> str:
    """
    Interpret AQI value into human-readable category.

    Args:
        aqi: Air Quality Index value

    Returns:
        Category description
    """
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups"
    elif aqi <= 200:
        return "Unhealthy"
    elif aqi <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"


def interpret_walk_score(score: int) -> str:
    """
    Interpret Walk Score into human-readable category.

    Args:
        score: Walk Score value (0-100)

    Returns:
        Category description
    """
    if score >= 90:
        return "Walker's Paradise"
    elif score >= 70:
        return "Very Walkable"
    elif score >= 50:
        return "Somewhat Walkable"
    elif score >= 25:
        return "Car-Dependent"
    else:
        return "Almost All Errands Require a Car"


# Usage example
if __name__ == "__main__":
    import os

    print("Location Services Client Demo")
    print("=" * 50)

    # Get API keys from environment
    mapquest_key = os.environ.get("MAPQUEST_API_KEY")
    walkscore_key = os.environ.get("WALKSCORE_API_KEY")
    airquality_key = os.environ.get("WAQI_API_KEY")

    if not any([mapquest_key, walkscore_key, airquality_key]):
        print("\nNote: Set environment variables for actual API calls:")
        print("  MAPQUEST_API_KEY, WALKSCORE_API_KEY, WAQI_API_KEY")
        print("\nDemo mode - showing expected output structure:\n")

        # Demo output structure
        demo = {
            "address": "1600 Amphitheatre Parkway, Mountain View, CA",
            "geocoding": {
                "success": True,
                "lat": 37.4221,
                "lng": -122.0841,
                "city": "Mountain View",
                "state": "CA",
            },
            "walkability": {
                "success": True,
                "walk_score": 54,
                "walk_description": "Somewhat Walkable",
                "transit_score": 36,
                "bike_score": 72,
            },
            "air_quality": {
                "success": True,
                "city": "Mountain View",
                "aqi": 42,
                "dominant_pollutant": "pm25",
            },
        }

        print(f"Address: {demo['address']}")
        print(f"\nGeocoding: {demo['geocoding']['lat']}, {demo['geocoding']['lng']}")
        print(f"\nWalkability:")
        print(f"  Walk Score: {demo['walkability']['walk_score']} ({demo['walkability']['walk_description']})")
        print(f"  Transit Score: {demo['walkability']['transit_score']}")
        print(f"  Bike Score: {demo['walkability']['bike_score']}")
        print(f"\nAir Quality:")
        print(f"  AQI: {demo['air_quality']['aqi']} ({interpret_aqi(demo['air_quality']['aqi'])})")

    else:
        # Real API calls
        services = LocationServices(
            mapquest_key=mapquest_key,
            walkscore_key=walkscore_key,
            airquality_key=airquality_key,
        )

        address = "1600 Amphitheatre Parkway, Mountain View, CA"
        print(f"\nAnalyzing: {address}\n")

        result = services.analyze_location(address)

        if result["geocoding"] and result["geocoding"].get("success"):
            geo = result["geocoding"]
            print(f"Coordinates: {geo['lat']}, {geo['lng']}")

        if result["walkability"] and result["walkability"].get("success"):
            walk = result["walkability"]
            print(f"\nWalk Score: {walk['walk_score']} ({walk['walk_description']})")
            if walk.get("transit_score"):
                print(f"Transit Score: {walk['transit_score']}")
            if walk.get("bike_score"):
                print(f"Bike Score: {walk['bike_score']}")

        if result["air_quality"] and result["air_quality"].get("success"):
            air = result["air_quality"]
            print(f"\nAir Quality: {air['aqi']} ({interpret_aqi(air['aqi'])})")
            print(f"Dominant Pollutant: {air['dominant_pollutant']}")

"""
NOAA Weather API Client

Provides access to NOAA weather data:
- Current weather conditions
- Forecasts
- Weather alerts
- Historical data

No API key required for basic access.

Author: Luke Steuber
"""

import requests
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class WeatherClient:
    """Client for NOAA Weather API."""

    BASE_URL = "https://api.weather.gov"

    def __init__(self):
        """Initialize NOAA Weather client."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'SharedLibraryWeatherClient/1.0',
            'Accept': 'application/geo+json'
        })

    def get_current_weather(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """
        Get current weather conditions.

        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate

        Returns:
            Dict with current weather
        """
        try:
            # First, get the forecast office and grid point
            points_response = self.session.get(
                f"{self.BASE_URL}/points/{latitude},{longitude}",
                timeout=30
            )
            points_response.raise_for_status()
            points_data = points_response.json()

            # Get the forecast URL
            forecast_url = points_data.get('properties', {}).get('forecast')
            if not forecast_url:
                return {"error": "Could not get forecast URL for location"}

            # Get the forecast
            forecast_response = self.session.get(forecast_url, timeout=30)
            forecast_response.raise_for_status()
            forecast_data = forecast_response.json()

            # Get current period (usually first period)
            periods = forecast_data.get('properties', {}).get('periods', [])
            if periods:
                current = periods[0]
                return {
                    "location": {
                        "latitude": latitude,
                        "longitude": longitude,
                        "city": points_data.get('properties', {}).get('relativeLocation', {}).get('properties', {}).get('city'),
                        "state": points_data.get('properties', {}).get('relativeLocation', {}).get('properties', {}).get('state')
                    },
                    "current": {
                        "name": current.get("name"),
                        "temperature": current.get("temperature"),
                        "temperature_unit": current.get("temperatureUnit"),
                        "wind_speed": current.get("windSpeed"),
                        "wind_direction": current.get("windDirection"),
                        "short_forecast": current.get("shortForecast"),
                        "detailed_forecast": current.get("detailedForecast")
                    }
                }

            return {"error": "No forecast data available"}
        except Exception as e:
            logger.error(f"Weather API error: {e}")
            return {"error": str(e)}

    def get_forecast(self, latitude: float, longitude: float, periods: int = 7) -> Dict[str, Any]:
        """
        Get weather forecast.

        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            periods: Number of forecast periods

        Returns:
            Dict with forecast
        """
        try:
            # Get points data
            points_response = self.session.get(
                f"{self.BASE_URL}/points/{latitude},{longitude}",
                timeout=30
            )
            points_response.raise_for_status()
            points_data = points_response.json()

            # Get forecast
            forecast_url = points_data.get('properties', {}).get('forecast')
            forecast_response = self.session.get(forecast_url, timeout=30)
            forecast_response.raise_for_status()
            forecast_data = forecast_response.json()

            forecast_periods = []
            for period in forecast_data.get('properties', {}).get('periods', [])[:periods]:
                forecast_periods.append({
                    "name": period.get("name"),
                    "temperature": period.get("temperature"),
                    "temperature_unit": period.get("temperatureUnit"),
                    "wind_speed": period.get("windSpeed"),
                    "wind_direction": period.get("windDirection"),
                    "icon": period.get("icon"),
                    "short_forecast": period.get("shortForecast"),
                    "detailed_forecast": period.get("detailedForecast")
                })

            return {
                "location": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "forecast": forecast_periods
            }
        except Exception as e:
            logger.error(f"Weather forecast error: {e}")
            return {"error": str(e)}

    def get_alerts(self, state: str) -> Dict[str, Any]:
        """
        Get weather alerts for a state.

        Args:
            state: State code (e.g., CA, NY)

        Returns:
            Dict with active alerts
        """
        try:
            response = self.session.get(
                f"{self.BASE_URL}/alerts/active/area/{state}",
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            alerts = []
            for feature in data.get('features', []):
                props = feature.get('properties', {})
                alerts.append({
                    "event": props.get("event"),
                    "headline": props.get("headline"),
                    "severity": props.get("severity"),
                    "urgency": props.get("urgency"),
                    "areas": props.get("areaDesc"),
                    "effective": props.get("effective"),
                    "expires": props.get("expires"),
                    "description": props.get("description")
                })

            return {
                "state": state,
                "alerts": alerts,
                "count": len(alerts)
            }
        except Exception as e:
            logger.error(f"Weather alerts error: {e}")
            return {"error": str(e)}


"""
Alpha Vantage Finance API Client

Provides a minimal wrapper around Alpha Vantage endpoints that are useful for
financial analytics and reporting:
- Equity time series (intraday and daily)
- Foreign exchange rates
- Cryptocurrency quotes
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests


class FinanceClient:
    """Client for Alpha Vantage financial data."""

    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(
        self,
        api_key: Optional[str] = None,
        timeout: int = 30,
    ) -> None:
        """
        Initialize finance client.

        Args:
            api_key: Alpha Vantage API key. Falls back to ALPHAVANTAGE_API_KEY env var.
            timeout: Request timeout in seconds.

        Raises:
            RuntimeError: If the API key is missing.
        """
        self.api_key = api_key or os.getenv("ALPHAVANTAGE_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "Alpha Vantage API key not configured. "
                "Set ALPHAVANTAGE_API_KEY or provide via constructor."
            )

        self.timeout = timeout
        self.session = requests.Session()

    def _request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Perform a GET request with the provided parameters."""
        params = {**params, "apikey": self.api_key}
        response = self.session.get(self.BASE_URL, params=params, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()
        if "Note" in data:
            # Rate limit or usage message from Alpha Vantage
            return {"error": data["Note"]}
        if "Error Message" in data:
            return {"error": data["Error Message"]}
        return data

    def get_daily_time_series(
        self,
        symbol: str,
        output_size: str = "compact",
    ) -> Dict[str, Any]:
        """
        Retrieve daily time series data for an equity.

        Args:
            symbol: Ticker symbol (e.g., "AAPL").
            output_size: "compact" (last 100 data points) or "full".

        Returns:
            Dict with metadata and price series.
        """
        data = self._request(
            {
                "function": "TIME_SERIES_DAILY_ADJUSTED",
                "symbol": symbol,
                "outputsize": output_size,
            }
        )

        if "error" in data:
            return data

        metadata = data.get("Meta Data", {})
        series = data.get("Time Series (Daily)", {})
        prices = [
            {
                "date": date,
                "open": float(values.get("1. open", 0.0)),
                "high": float(values.get("2. high", 0.0)),
                "low": float(values.get("3. low", 0.0)),
                "close": float(values.get("4. close", 0.0)),
                "adjusted_close": float(values.get("5. adjusted close", 0.0)),
                "volume": int(values.get("6. volume", 0)),
            }
            for date, values in series.items()
        ]

        # Sort by descending date (most recent first)
        prices.sort(key=lambda item: item["date"], reverse=True)

        return {"metadata": metadata, "prices": prices}

    def get_fx_rate(self, from_currency: str, to_currency: str) -> Dict[str, Any]:
        """
        Fetch real-time foreign exchange rate.

        Args:
            from_currency: Base currency code (e.g., "USD").
            to_currency: Quote currency code (e.g., "EUR").

        Returns:
            Dict with exchange rate information.
        """
        data = self._request(
            {
                "function": "CURRENCY_EXCHANGE_RATE",
                "from_currency": from_currency,
                "to_currency": to_currency,
            }
        )

        if "error" in data:
            return data

        rate = data.get("Realtime Currency Exchange Rate", {})
        return {
            "from_currency": rate.get("1. From_Currency Code"),
            "to_currency": rate.get("3. To_Currency Code"),
            "exchange_rate": float(rate.get("5. Exchange Rate", 0.0)),
            "last_refreshed": rate.get("6. Last Refreshed"),
            "bid_price": float(rate.get("8. Bid Price", 0.0)),
            "ask_price": float(rate.get("9. Ask Price", 0.0)),
        }

    def get_crypto_quote(self, symbol: str, market: str = "USD") -> Dict[str, Any]:
        """
        Retrieve digital currency (crypto) quote.

        Args:
            symbol: Crypto symbol (e.g., "BTC").
            market: Market currency (e.g., "USD").

        Returns:
            Dict with crypto quote information.
        """
        data = self._request(
            {
                "function": "DIGITAL_CURRENCY_DAILY",
                "symbol": symbol,
                "market": market,
            }
        )

        if "error" in data:
            return data

        metadata = data.get("Meta Data", {})
        series = data.get("Time Series (Digital Currency Daily)", {})

        quotes = [
            {
                "date": date,
                "open": float(values.get(f"1a. open ({market})", 0.0)),
                "high": float(values.get(f"2a. high ({market})", 0.0)),
                "low": float(values.get(f"3a. low ({market})", 0.0)),
                "close": float(values.get(f"4a. close ({market})", 0.0)),
                "volume": float(values.get("5. volume", 0.0)),
                "market_cap": float(values.get("6. market cap (USD)", 0.0)),
            }
            for date, values in series.items()
        ]

        quotes.sort(key=lambda item: item["date"], reverse=True)
        return {"metadata": metadata, "quotes": quotes}


__all__ = ["FinanceClient"]


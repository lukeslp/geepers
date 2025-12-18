#!/usr/bin/env python3
"""
Production-ready market cap data retrieval
Includes caching, error handling, and fallback strategies
"""

import yfinance as yf
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cache configuration
CACHE_DIR = Path.home() / '.cache' / 'market_cap'
CACHE_DURATION = timedelta(hours=1)  # Cache for 1 hour

class MarketCapFetcher:
    """Production-ready market cap data fetcher with caching"""

    def __init__(self, cache_dir: Path = CACHE_DIR, cache_duration: timedelta = CACHE_DURATION):
        self.cache_dir = cache_dir
        self.cache_duration = cache_duration
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_path(self, ticker: str) -> Path:
        """Get cache file path for a ticker"""
        return self.cache_dir / f"{ticker}.json"

    def _is_cache_valid(self, cache_path: Path) -> bool:
        """Check if cache file exists and is still valid"""
        if not cache_path.exists():
            return False

        try:
            with open(cache_path, 'r') as f:
                data = json.load(f)
                cached_time = datetime.fromisoformat(data.get('timestamp', '2000-01-01'))
                return datetime.now() - cached_time < self.cache_duration
        except Exception as e:
            logger.warning(f"Cache validation error: {e}")
            return False

    def _load_from_cache(self, ticker: str) -> Optional[Dict]:
        """Load data from cache if valid"""
        cache_path = self._get_cache_path(ticker)

        if self._is_cache_valid(cache_path):
            try:
                with open(cache_path, 'r') as f:
                    data = json.load(f)
                    logger.info(f"Loaded {ticker} from cache")
                    return data
            except Exception as e:
                logger.error(f"Error loading cache for {ticker}: {e}")

        return None

    def _save_to_cache(self, ticker: str, data: Dict):
        """Save data to cache"""
        cache_path = self._get_cache_path(ticker)

        try:
            data['timestamp'] = datetime.now().isoformat()
            with open(cache_path, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Cached data for {ticker}")
        except Exception as e:
            logger.error(f"Error saving cache for {ticker}: {e}")

    def get_market_cap(self, ticker: str, use_cache: bool = True) -> Optional[Dict]:
        """
        Get market cap for a ticker with caching and error handling

        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL')
            use_cache: Whether to use cached data if available

        Returns:
            Dictionary with market cap data or None if failed
        """
        # Try cache first
        if use_cache:
            cached = self._load_from_cache(ticker)
            if cached:
                return cached

        # Fetch fresh data
        try:
            logger.info(f"Fetching fresh data for {ticker}")
            stock = yf.Ticker(ticker)
            info = stock.info

            # Validate data
            if not info or 'marketCap' not in info:
                logger.error(f"No market cap data for {ticker}")
                return None

            market_cap = info.get('marketCap', 0)

            # Sanity check
            if market_cap <= 0:
                logger.error(f"Invalid market cap for {ticker}: {market_cap}")
                return None

            # Prepare data
            data = {
                'ticker': ticker,
                'name': info.get('longName', 'N/A'),
                'market_cap': market_cap,
                'market_cap_billions': market_cap / 1e9,
                'market_cap_formatted': f"${market_cap / 1e9:.2f}B",
                'price': info.get('currentPrice', info.get('regularMarketPrice', 0)),
                'currency': info.get('currency', 'USD'),
                'exchange': info.get('exchange', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'pe_ratio': info.get('trailingPE', None),
                'dividend_yield': info.get('dividendYield', None),
                'fifty_two_week_high': info.get('fiftyTwoWeekHigh', None),
                'fifty_two_week_low': info.get('fiftyTwoWeekLow', None),
                'success': True
            }

            # Cache the data
            if use_cache:
                self._save_to_cache(ticker, data)

            return data

        except Exception as e:
            logger.error(f"Error fetching {ticker}: {e}")
            return {
                'ticker': ticker,
                'error': str(e),
                'success': False
            }

    def get_multiple_market_caps(self, tickers: List[str], use_cache: bool = True,
                                  delay: float = 0.1) -> List[Dict]:
        """
        Get market caps for multiple tickers

        Args:
            tickers: List of ticker symbols
            use_cache: Whether to use cached data
            delay: Delay between requests (seconds) to be respectful

        Returns:
            List of dictionaries with market cap data
        """
        results = []

        for i, ticker in enumerate(tickers):
            result = self.get_market_cap(ticker, use_cache=use_cache)
            if result:
                results.append(result)

            # Small delay between requests (be respectful)
            if i < len(tickers) - 1:
                time.sleep(delay)

        return results

    def clear_cache(self, ticker: Optional[str] = None):
        """Clear cache for specific ticker or all tickers"""
        if ticker:
            cache_path = self._get_cache_path(ticker)
            if cache_path.exists():
                cache_path.unlink()
                logger.info(f"Cleared cache for {ticker}")
        else:
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()
            logger.info("Cleared all cache")


def main():
    """Example usage"""
    print("Production-Ready Market Cap Fetcher")
    print("=" * 70)

    # Initialize fetcher
    fetcher = MarketCapFetcher()

    # Major tech companies
    tickers = ['AAPL', 'MSFT', 'NVDA', 'GOOGL', 'AMZN', 'META', 'TSLA', 'BRK-B']

    # Fetch data (will use cache if available)
    print("\nFetching market cap data...")
    print("-" * 70)

    start_time = time.time()
    results = fetcher.get_multiple_market_caps(tickers)
    elapsed = time.time() - start_time

    print(f"\nRetrieved {len(results)} companies in {elapsed:.2f} seconds")
    print("-" * 70)

    # Display results
    print(f"\n{'Ticker':<8} {'Company':<35} {'Market Cap':<15} {'Price':<10}")
    print("-" * 70)

    for result in results:
        if result.get('success'):
            print(f"{result['ticker']:<8} {result['name'][:33]:<35} "
                  f"{result['market_cap_formatted']:<15} ${result['price']:<9.2f}")
        else:
            print(f"{result['ticker']:<8} ERROR: {result.get('error', 'Unknown')}")

    # Example: Get single company with detailed info
    print("\n" + "=" * 70)
    print("Detailed Info: Apple Inc.")
    print("=" * 70)

    apple = fetcher.get_market_cap('AAPL')
    if apple and apple.get('success'):
        print(f"Company: {apple['name']}")
        print(f"Market Cap: {apple['market_cap_formatted']}")
        print(f"Current Price: ${apple['price']:.2f}")
        print(f"Exchange: {apple['exchange']}")
        print(f"Sector: {apple['sector']}")
        print(f"Industry: {apple['industry']}")
        print(f"P/E Ratio: {apple['pe_ratio']:.2f}" if apple['pe_ratio'] else "P/E Ratio: N/A")
        print(f"52-Week High: ${apple['fifty_two_week_high']:.2f}" if apple['fifty_two_week_high'] else "52-Week High: N/A")
        print(f"52-Week Low: ${apple['fifty_two_week_low']:.2f}" if apple['fifty_two_week_low'] else "52-Week Low: N/A")

    # Cache info
    print("\n" + "=" * 70)
    print("Cache Information")
    print("=" * 70)
    print(f"Cache directory: {fetcher.cache_dir}")
    print(f"Cache duration: {fetcher.cache_duration}")
    cache_files = list(fetcher.cache_dir.glob("*.json"))
    print(f"Cached tickers: {len(cache_files)}")

    print("\nNote: Subsequent calls will use cached data (1 hour cache)")
    print("To force fresh data: fetcher.get_market_cap('AAPL', use_cache=False)")
    print("To clear cache: fetcher.clear_cache() or fetcher.clear_cache('AAPL')")


if __name__ == '__main__':
    main()

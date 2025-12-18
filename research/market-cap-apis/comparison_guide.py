#!/usr/bin/env python3
"""
Comprehensive comparison of market cap data sources
Demonstrates batch retrieval and efficiency patterns
"""

import yfinance as yf
from datetime import datetime
import time

def yfinance_batch_method(tickers):
    """
    Most efficient method for getting market caps
    No API key required, no rate limits
    """
    print("\n" + "="*70)
    print("METHOD 1: yfinance (RECOMMENDED)")
    print("="*70)
    print("Pros:")
    print("  ✓ No API key required")
    print("  ✓ No rate limits")
    print("  ✓ Free and unlimited")
    print("  ✓ Fast batch retrieval")
    print("  ✓ Comprehensive data (price, fundamentals, financials)")
    print("  ✓ Daily updates")
    print("\nCons:")
    print("  ✗ Not official Yahoo API (may break)")
    print("  ✗ Limited to Yahoo Finance data")
    print("="*70)

    start_time = time.time()
    results = []

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            results.append({
                'ticker': ticker,
                'name': info.get('longName', 'N/A'),
                'market_cap': info.get('marketCap', 0),
                'market_cap_billions': info.get('marketCap', 0) / 1e9 if info.get('marketCap') else 0,
                'price': info.get('currentPrice', 'N/A'),
                'pe_ratio': info.get('trailingPE', 'N/A')
            })
        except Exception as e:
            results.append({'ticker': ticker, 'error': str(e)})

    elapsed = time.time() - start_time

    print(f"\nRetrieved {len(results)} companies in {elapsed:.2f} seconds")
    print(f"Average: {elapsed/len(results):.2f} seconds per company\n")

    for result in results:
        if 'error' not in result:
            print(f"{result['ticker']:6} | {result['name']:35} | ${result['market_cap_billions']:8.2f}B | ${result['price']:7.2f}")

    return results, elapsed

def yfinance_super_fast_method(tickers):
    """
    Ultra-fast batch download method
    Gets OHLCV data for all tickers in one call
    Note: Doesn't include market cap, but very fast for price data
    """
    print("\n" + "="*70)
    print("METHOD 2: yfinance Batch Download (for price data)")
    print("="*70)
    print("Use when you need: Quick price data for many stocks")
    print("Note: For market cap, use Method 1")
    print("="*70)

    start_time = time.time()
    tickers_str = ' '.join(tickers)

    # Download OHLCV data for all tickers at once
    data = yf.download(tickers_str, period='1d', progress=False)

    elapsed = time.time() - start_time
    print(f"\nDownloaded price data for {len(tickers)} companies in {elapsed:.2f} seconds")
    print(f"Data shape: {data.shape}")
    print("\nLatest Close Prices:")

    if len(tickers) == 1:
        print(f"{tickers[0]}: ${data['Close'].iloc[-1]:.2f}")
    else:
        for ticker in tickers:
            if ticker in data['Close'].columns:
                print(f"{ticker}: ${data['Close'][ticker].iloc[-1]:.2f}")

    return elapsed

def comparison_summary():
    """Print comprehensive comparison of all methods"""
    print("\n" + "="*70)
    print("COMPLETE API COMPARISON FOR MARKET CAP DATA")
    print("="*70)

    comparison = {
        "yfinance": {
            "cost": "Free, unlimited",
            "rate_limit": "None",
            "api_key": "Not required",
            "market_cap": "✓ Yes",
            "real_time": "✓ Yes (15min delay)",
            "coverage": "All Yahoo Finance stocks",
            "ease_of_use": "⭐⭐⭐⭐⭐",
            "reliability": "⭐⭐⭐⭐",
            "setup_time": "< 1 minute",
            "best_for": "Most use cases, prototyping, personal projects"
        },
        "Alpha Vantage": {
            "cost": "Free tier: 25/day",
            "rate_limit": "5 requests/minute",
            "api_key": "Required (free)",
            "market_cap": "✓ Yes",
            "real_time": "✓ Yes (premium)",
            "coverage": "US stocks, global data",
            "ease_of_use": "⭐⭐⭐⭐",
            "reliability": "⭐⭐⭐⭐⭐",
            "setup_time": "2-3 minutes",
            "best_for": "Production apps with modest volume"
        },
        "Finnhub": {
            "cost": "Free tier: 60 calls/min",
            "rate_limit": "60 requests/minute",
            "api_key": "Required (free)",
            "market_cap": "✓ Yes",
            "real_time": "✓ Yes",
            "coverage": "Global exchanges",
            "ease_of_use": "⭐⭐⭐⭐",
            "reliability": "⭐⭐⭐⭐⭐",
            "setup_time": "2-3 minutes",
            "best_for": "Real-time data, global coverage"
        },
        "Polygon.io": {
            "cost": "Free (limited), $29/mo starter",
            "rate_limit": "Low (free tier)",
            "api_key": "Required",
            "market_cap": "✓ Yes",
            "real_time": "✓ Yes",
            "coverage": "US exchanges, detailed",
            "ease_of_use": "⭐⭐⭐⭐",
            "reliability": "⭐⭐⭐⭐⭐",
            "setup_time": "2-3 minutes",
            "best_for": "Professional apps, institutional data"
        },
        "IEX Cloud": {
            "cost": "Service discontinued",
            "rate_limit": "N/A",
            "api_key": "N/A",
            "market_cap": "N/A",
            "real_time": "N/A",
            "coverage": "N/A",
            "ease_of_use": "N/A",
            "reliability": "N/A",
            "setup_time": "N/A",
            "best_for": "DISCONTINUED - Use alternatives"
        }
    }

    for api_name, details in comparison.items():
        print(f"\n{api_name}")
        print("-" * 70)
        for key, value in details.items():
            print(f"  {key.replace('_', ' ').title():15}: {value}")

    print("\n" + "="*70)
    print("RECOMMENDATION")
    print("="*70)
    print("""
For most use cases: USE YFINANCE

Reasons:
1. No API key setup required
2. No rate limits or daily caps
3. Completely free
4. Easy to install: pip install yfinance
5. Rich data including market cap, fundamentals, financials
6. Good for prototyping and production

When to consider alternatives:
- Need guaranteed SLA (use Alpha Vantage or Polygon)
- Need real-time < 15min delay (use Finnhub)
- Building enterprise application (use Polygon.io)
- Need global exchanges (use Finnhub)
- Require institutional-grade data (use Polygon.io paid)
    """)

def main():
    # Test with major tech companies
    tickers = ['AAPL', 'MSFT', 'NVDA', 'GOOGL', 'AMZN', 'META', 'TSLA', 'BRK-B']

    print("\n" + "="*70)
    print("MARKET CAP DATA SOURCES - LIVE COMPARISON")
    print("="*70)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Testing with {len(tickers)} major companies")
    print("="*70)

    # Method 1: Individual ticker info (includes market cap)
    results1, time1 = yfinance_batch_method(tickers)

    # Method 2: Fast batch download (OHLCV only)
    time2 = yfinance_super_fast_method(tickers)

    # Print comprehensive comparison
    comparison_summary()

    # Print code snippet
    print("\n" + "="*70)
    print("QUICK START CODE")
    print("="*70)
    print("""
# Install
pip install yfinance

# Get market cap for multiple companies
import yfinance as yf

tickers = ['AAPL', 'MSFT', 'NVDA', 'GOOGL', 'AMZN']

for ticker in tickers:
    stock = yf.Ticker(ticker)
    info = stock.info
    market_cap = info.get('marketCap', 0) / 1e9  # In billions
    print(f"{ticker}: ${market_cap:.2f}B")
    """)

if __name__ == '__main__':
    main()

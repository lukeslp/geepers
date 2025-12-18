#!/usr/bin/env python3
"""
Test yfinance library for market cap data retrieval
"""

import yfinance as yf
from datetime import datetime

def get_market_cap(ticker):
    """Get market cap for a single ticker"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            'ticker': ticker,
            'name': info.get('longName', 'N/A'),
            'market_cap': info.get('marketCap', 0),
            'market_cap_billions': info.get('marketCap', 0) / 1e9 if info.get('marketCap') else 0,
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'currency': info.get('currency', 'USD'),
            'exchange': info.get('exchange', 'N/A')
        }
    except Exception as e:
        return {
            'ticker': ticker,
            'error': str(e)
        }

def get_multiple_market_caps(tickers):
    """Get market caps for multiple tickers"""
    results = []
    for ticker in tickers:
        print(f"Fetching {ticker}...")
        data = get_market_cap(ticker)
        results.append(data)
    return results

def main():
    # Test with major tech companies
    tickers = ['AAPL', 'MSFT', 'NVDA', 'GOOGL', 'AMZN', 'META', 'TSLA', 'BRK-B']

    print("Testing yfinance Market Cap Data Retrieval")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    results = get_multiple_market_caps(tickers)

    print("\nResults:")
    print("-" * 60)
    for result in results:
        if 'error' in result:
            print(f"{result['ticker']}: ERROR - {result['error']}")
        else:
            print(f"{result['ticker']}: {result['name']}")
            print(f"  Market Cap: ${result['market_cap_billions']:.2f}B")
            print(f"  Sector: {result['sector']}")
            print(f"  Exchange: {result['exchange']}")
            print()

    # Test fast batch retrieval
    print("\nTesting batch download (faster for multiple stocks):")
    print("-" * 60)
    tickers_str = ' '.join(tickers)
    data = yf.download(tickers_str, period='1d', progress=False)
    print(f"Successfully downloaded data for {len(tickers)} stocks")
    print(f"Data shape: {data.shape}")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Test Polygon.io (now Massive.com) API for market cap data retrieval
Requires API key from https://polygon.io/dashboard/api-keys
"""

import requests
import json
from datetime import datetime

# Get your free API key from: https://polygon.io/dashboard/api-keys
API_KEY = 'YOUR_API_KEY_HERE'  # Replace with your actual API key

def get_ticker_details(ticker):
    """
    Get ticker details including market cap from Polygon.io
    Free tier has limited rate limits
    """
    url = f'https://api.polygon.io/v3/reference/tickers/{ticker}?apiKey={API_KEY}'

    try:
        response = requests.get(url)
        data = response.json()

        if data.get('status') == 'OK' and 'results' in data:
            results = data['results']
            return {
                'ticker': ticker,
                'name': results.get('name', 'N/A'),
                'market_cap': results.get('market_cap', 0),
                'market_cap_billions': results.get('market_cap', 0) / 1e9 if results.get('market_cap') else 0,
                'weighted_shares_outstanding': results.get('weighted_shares_outstanding', 'N/A'),
                'share_class_shares_outstanding': results.get('share_class_shares_outstanding', 'N/A'),
                'locale': results.get('locale', 'N/A'),
                'primary_exchange': results.get('primary_exchange', 'N/A'),
                'type': results.get('type', 'N/A'),
                'currency_name': results.get('currency_name', 'USD')
            }
        else:
            return {
                'ticker': ticker,
                'error': data.get('error', 'Unknown error')
            }
    except Exception as e:
        return {
            'ticker': ticker,
            'error': str(e)
        }

def main():
    if API_KEY == 'YOUR_API_KEY_HERE':
        print("ERROR: Please set your Polygon.io API key")
        print("Get one free at: https://polygon.io/dashboard/api-keys")
        return

    # Test with major tech companies
    tickers = ['AAPL', 'MSFT', 'NVDA', 'GOOGL', 'AMZN']

    print("Testing Polygon.io (Massive) Market Cap Data Retrieval")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print("\nFree Tier Notes:")
    print("  - Limited rate limits (low for free tier)")
    print("  - Starter plan: $29/month for higher limits")
    print("  - Real-time and historical data available")
    print("  - Market cap calculated: share price × weighted shares")
    print("=" * 60)

    results = []
    for ticker in tickers:
        print(f"\nFetching {ticker}...")
        result = get_ticker_details(ticker)
        results.append(result)

    print("\n\nResults:")
    print("-" * 60)
    for result in results:
        if 'error' in result:
            print(f"{result['ticker']}: ERROR - {result['error']}")
        else:
            print(f"{result['ticker']}: {result['name']}")
            print(f"  Market Cap: ${result['market_cap_billions']:.2f}B")
            print(f"  Exchange: {result['primary_exchange']}")
            print(f"  Weighted Shares: {result['weighted_shares_outstanding']}")
            print()

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Test Alpha Vantage API for market cap data retrieval
Requires API key from https://www.alphavantage.co/support/#api-key
"""

import requests
import json
from datetime import datetime
import time

# Get your free API key from: https://www.alphavantage.co/support/#api-key
API_KEY = 'demo'  # Replace with your actual API key

def get_company_overview(symbol):
    """
    Get company overview including market cap from Alpha Vantage
    Free tier: 25 requests per day, 5 requests per minute
    """
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={API_KEY}'

    try:
        response = requests.get(url)
        data = response.json()

        if 'MarketCapitalization' in data:
            return {
                'ticker': symbol,
                'name': data.get('Name', 'N/A'),
                'market_cap': int(data.get('MarketCapitalization', 0)),
                'market_cap_billions': int(data.get('MarketCapitalization', 0)) / 1e9,
                'sector': data.get('Sector', 'N/A'),
                'industry': data.get('Industry', 'N/A'),
                'exchange': data.get('Exchange', 'N/A'),
                'currency': data.get('Currency', 'USD'),
                'pe_ratio': data.get('PERatio', 'N/A'),
                'dividend_yield': data.get('DividendYield', 'N/A')
            }
        else:
            return {
                'ticker': symbol,
                'error': data.get('Note', data.get('Error Message', 'Unknown error'))
            }
    except Exception as e:
        return {
            'ticker': symbol,
            'error': str(e)
        }

def main():
    # Test with major tech companies
    # Note: Free tier limited to 5 requests per minute
    tickers = ['AAPL', 'MSFT', 'NVDA']

    print("Testing Alpha Vantage Market Cap Data Retrieval")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("API Key: " + ("demo (limited)" if API_KEY == 'demo' else "custom"))
    print("=" * 60)
    print("\nFree Tier Limits:")
    print("  - 25 requests per day")
    print("  - 5 requests per minute")
    print("  - 100 data points per request")
    print("=" * 60)

    results = []
    for i, ticker in enumerate(tickers):
        print(f"\nFetching {ticker}...")
        result = get_company_overview(ticker)
        results.append(result)

        # Rate limiting: wait 12 seconds between requests to stay under 5/minute
        if i < len(tickers) - 1:
            print("  (waiting 12s for rate limit...)")
            time.sleep(12)

    print("\n\nResults:")
    print("-" * 60)
    for result in results:
        if 'error' in result:
            print(f"{result['ticker']}: ERROR - {result['error']}")
        else:
            print(f"{result['ticker']}: {result['name']}")
            print(f"  Market Cap: ${result['market_cap_billions']:.2f}B")
            print(f"  Sector: {result['sector']}")
            print(f"  Industry: {result['industry']}")
            print(f"  PE Ratio: {result['pe_ratio']}")
            print()

if __name__ == '__main__':
    print("\nIMPORTANT: Replace API_KEY with your free key from:")
    print("https://www.alphavantage.co/support/#api-key\n")
    main()

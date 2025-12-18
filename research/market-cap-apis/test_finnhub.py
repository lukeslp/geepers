#!/usr/bin/env python3
"""
Test Finnhub API for market cap data retrieval
Requires API key from https://finnhub.io/register
"""

import requests
import json
from datetime import datetime

# Get your free API key from: https://finnhub.io/register
API_KEY = 'YOUR_API_KEY_HERE'  # Replace with your actual API key

def get_company_profile(symbol):
    """
    Get company profile including market cap from Finnhub
    Free tier: 60 API calls/minute
    """
    url = f'https://finnhub.io/api/v1/stock/profile2?symbol={symbol}&token={API_KEY}'

    try:
        response = requests.get(url)
        data = response.json()

        if data and 'marketCapitalization' in data:
            # Finnhub returns market cap in millions
            market_cap_millions = data.get('marketCapitalization', 0)
            return {
                'ticker': symbol,
                'name': data.get('name', 'N/A'),
                'market_cap': market_cap_millions * 1e6,  # Convert to actual value
                'market_cap_billions': market_cap_millions / 1000,  # Millions to billions
                'country': data.get('country', 'N/A'),
                'currency': data.get('currency', 'USD'),
                'exchange': data.get('exchange', 'N/A'),
                'ipo': data.get('ipo', 'N/A'),
                'share_outstanding': data.get('shareOutstanding', 'N/A'),
                'industry': data.get('finnhubIndustry', 'N/A'),
                'logo': data.get('logo', 'N/A'),
                'weburl': data.get('weburl', 'N/A')
            }
        else:
            return {
                'ticker': symbol,
                'error': 'No data returned or invalid symbol'
            }
    except Exception as e:
        return {
            'ticker': symbol,
            'error': str(e)
        }

def get_quote(symbol):
    """Get real-time quote data"""
    url = f'https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}'

    try:
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as e:
        return {'error': str(e)}

def main():
    if API_KEY == 'YOUR_API_KEY_HERE':
        print("ERROR: Please set your Finnhub API key")
        print("Get one free at: https://finnhub.io/register")
        return

    # Test with major tech companies
    tickers = ['AAPL', 'MSFT', 'NVDA', 'GOOGL', 'AMZN', 'META']

    print("Testing Finnhub Market Cap Data Retrieval")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print("\nFree Tier Limits:")
    print("  - 60 API calls per minute")
    print("  - Real-time data for US stocks")
    print("  - Company fundamentals included")
    print("=" * 60)

    results = []
    for ticker in tickers:
        print(f"\nFetching {ticker}...")
        result = get_company_profile(ticker)
        results.append(result)

    print("\n\nResults:")
    print("-" * 60)
    for result in results:
        if 'error' in result:
            print(f"{result['ticker']}: ERROR - {result['error']}")
        else:
            print(f"{result['ticker']}: {result['name']}")
            print(f"  Market Cap: ${result['market_cap_billions']:.2f}B")
            print(f"  Exchange: {result['exchange']}")
            print(f"  Country: {result['country']}")
            print(f"  Industry: {result['industry']}")
            print(f"  Shares Outstanding: {result['share_outstanding']}M")
            print()

    # Example: Get real-time quote
    print("\nBonus: Real-time quote for AAPL:")
    print("-" * 60)
    quote = get_quote('AAPL')
    if 'error' not in quote:
        print(f"Current Price: ${quote.get('c', 'N/A')}")
        print(f"High: ${quote.get('h', 'N/A')}")
        print(f"Low: ${quote.get('l', 'N/A')}")
        print(f"Open: ${quote.get('o', 'N/A')}")
        print(f"Previous Close: ${quote.get('pc', 'N/A')}")

if __name__ == '__main__':
    main()

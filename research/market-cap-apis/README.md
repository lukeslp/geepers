# Market Cap Data Sources - Quick Reference

This directory contains research and working code examples for retrieving company market capitalization data programmatically.

## TL;DR - Use yfinance

```bash
pip install yfinance
```

```python
import yfinance as yf

stock = yf.Ticker("AAPL")
market_cap = stock.info['marketCap'] / 1e9  # In billions
print(f"Apple Market Cap: ${market_cap:.2f}B")
```

## Files in This Directory

| File | Description |
|------|-------------|
| `RESEARCH_REPORT.md` | Comprehensive research findings and recommendations |
| `comparison_guide.py` | Live comparison of all methods with benchmarks |
| `test_yfinance.py` | yfinance examples (RECOMMENDED) |
| `test_alpha_vantage.py` | Alpha Vantage API examples |
| `test_finnhub.py` | Finnhub API examples |
| `test_polygon.py` | Polygon.io API examples |
| `README.md` | This file |

## Quick Comparison

| Source | Free? | API Key? | Rate Limit | Best For |
|--------|-------|----------|------------|----------|
| **yfinance** ⭐ | ✓ Yes | ✗ No | None | Most use cases |
| Alpha Vantage | Limited | ✓ Yes | 5/min, 25/day | Production apps |
| Finnhub | ✓ Yes | ✓ Yes | 60/min | Real-time data |
| Polygon.io | Limited | ✓ Yes | Very low | Enterprise ($29+/mo) |

## Run Examples

### Test yfinance (Recommended)
```bash
python3 test_yfinance.py
```

### Run Full Comparison
```bash
python3 comparison_guide.py
```

### Test Other APIs
```bash
# Alpha Vantage (requires API key)
python3 test_alpha_vantage.py

# Finnhub (requires API key)
python3 test_finnhub.py

# Polygon.io (requires API key)
python3 test_polygon.py
```

## Get API Keys (if needed)

- Alpha Vantage: https://www.alphavantage.co/support/#api-key
- Finnhub: https://finnhub.io/register
- Polygon.io: https://polygon.io/dashboard/api-keys

## Recommendation

**Use yfinance for 99% of use cases.** It's free, unlimited, requires no API key, and works perfectly for major companies including AAPL, MSFT, NVDA, GOOGL, AMZN, META, TSLA, etc.

Only consider paid alternatives if you need guaranteed SLA or sub-15-minute real-time data.

## Support

See `RESEARCH_REPORT.md` for detailed analysis, performance benchmarks, code examples, and implementation guidance.

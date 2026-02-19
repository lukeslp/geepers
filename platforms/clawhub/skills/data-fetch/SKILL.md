---
name: data-fetch
description: Universal data fetching MCP server providing access to arXiv, Census, Weather, News, and GitHub.
---

# Data Fetch MCP Server

A specialized MCP server that provides tools for fetching data from various external sources.

## Tools

### `dream_of_arxiv`
Search arXiv for academic papers.
- **query**: Search terms
- **max_results**: Number of results (default: 5)
- **category**: Filter by category (e.g., `cs.AI`, `physics.gen-ph`)

### `dream_of_census_acs`
Fetch US Census American Community Survey (ACS) data.
- **year**: Census year (e.g., 2022)
- **variables**: Dictionary of variable codes to names (e.g., `{"B01001_001E": "total_population"}`)
- **state**: State FIPS code (e.g., "06" for CA)
- **geography**: Geographic level (default: "county:*")

### `dream_of_weather`
Get current weather for a specific location.
- **location**: City name (e.g., "San Francisco, CA")

### `dream_of_news`
Search for current news articles.
- **query**: Search keywords
- **category**: News category

### `dream_of_github_repos`
Search for GitHub repositories.
- **query**: Search keywords
- **sort**: Sort by stars, forks, or updated

## Configuration

Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "data-fetch": {
      "command": "python3",
      "args": [
        "/absolute/path/to/geepers/skills/source/data-fetch/src/server.py"
      ],
      "env": {
        "CENSUS_API_KEY": "your_key",
        "NEWS_API_KEY": "your_key",
        "OPENWEATHER_KEY": "your_key",
        "GITHUB_TOKEN": "your_token"
      }
    }
  }
}
```

## Underlying Library
This server is built on top of the `data_fetching` library, which supports additional sources (NASA, Finance, etc.). These can be exposed by extending `server.py`.

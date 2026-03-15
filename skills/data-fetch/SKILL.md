---
name: data-fetch
description: Universal data fetching MCP server providing access to arXiv, Census, Weather, News, and GitHub.
---

# Data Fetch MCP Server

Fetches structured data from external APIs via MCP tools.

## Prerequisites

Requires `geepers-mcp` to be installed:
```bash
pip install geepers-mcp[all]
```

If MCP tools aren't appearing, install the package and restart Claude Code.

## Tools

### `dream_of_arxiv`
Search arXiv for academic papers.
- **query**: Search terms
- **max_results**: Number of results (default: 5)
- **category**: Filter by category (e.g., `cs.CL`, `physics.gen-ph`)

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

## API Keys

Set in your environment for the data sources you want to use:
- `CENSUS_API_KEY` — US Census Bureau
- `NEWS_API_KEY` — NewsAPI
- `OPENWEATHER_API_KEY` — OpenWeatherMap
- `GITHUB_TOKEN` — GitHub API
- `NASA_API_KEY` — NASA APIs
- `YOUTUBE_API_KEY` — YouTube Data API

## Related

- `geepers:data` — Skill for fetching from 17 structured APIs
- `/geepers:research` — Research workflows using these data sources

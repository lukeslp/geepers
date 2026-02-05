"""
GitHub API Client

Provides access to GitHub API for:
- Repository search
- Issue and PR management
- Code search
- User and organization info

Author: Luke Steuber
"""

import os
import requests
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class GitHubClient:
    """Client for GitHub API."""

    BASE_URL = "https://api.github.com"

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize GitHub client.

        Args:
            api_key: GitHub personal access token (optional but recommended for higher rate limits)
        """
        self.api_key = api_key or os.getenv('GITHUB_TOKEN') or os.getenv('GITHUB_API_KEY')
        self.session = requests.Session()

        if self.api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}',
                'Accept': 'application/vnd.github.v3+json'
            })
        else:
            logger.warning("No GitHub API key provided. Rate limits will be restrictive (60 requests/hour)")

    def search_repositories(
        self,
        query: str,
        sort: str = "stars",
        order: str = "desc",
        per_page: int = 30
    ) -> Dict[str, Any]:
        """
        Search GitHub repositories.

        Args:
            query: Search query (e.g., "language:python stars:>1000")
            sort: Sort by (stars, forks, updated)
            order: asc or desc
            per_page: Results per page

        Returns:
            Dict with search results
        """
        try:
            response = self.session.get(
                f"{self.BASE_URL}/search/repositories",
                params={
                    "q": query,
                    "sort": sort,
                    "order": order,
                    "per_page": per_page
                },
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            repos = []
            for item in data.get('items', []):
                repos.append({
                    "name": item.get("full_name"),
                    "description": item.get("description"),
                    "stars": item.get("stargazers_count"),
                    "forks": item.get("forks_count"),
                    "language": item.get("language"),
                    "url": item.get("html_url"),
                    "topics": item.get("topics", [])
                })

            return {
                "query": query,
                "total_count": data.get('total_count', 0),
                "repositories": repos
            }
        except Exception as e:
            logger.error(f"GitHub search error: {e}")
            return {"error": str(e)}

    def search_code(
        self,
        query: str,
        per_page: int = 30
    ) -> Dict[str, Any]:
        """
        Search GitHub code.

        Args:
            query: Search query (e.g., "addClass in:file language:js")
            per_page: Results per page

        Returns:
            Dict with code search results
        """
        try:
            response = self.session.get(
                f"{self.BASE_URL}/search/code",
                params={"q": query, "per_page": per_page},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            results = []
            for item in data.get('items', []):
                results.append({
                    "name": item.get("name"),
                    "path": item.get("path"),
                    "repository": item.get("repository", {}).get("full_name"),
                    "url": item.get("html_url"),
                    "language": item.get("language")
                })

            return {
                "query": query,
                "total_count": data.get('total_count', 0),
                "results": results
            }
        except Exception as e:
            logger.error(f"GitHub code search error: {e}")
            return {"error": str(e)}

    def get_repository(self, owner: str, repo: str) -> Dict[str, Any]:
        """
        Get repository details.

        Args:
            owner: Repository owner
            repo: Repository name

        Returns:
            Dict with repository info
        """
        try:
            response = self.session.get(
                f"{self.BASE_URL}/repos/{owner}/{repo}",
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            return {
                "name": data.get("full_name"),
                "description": data.get("description"),
                "stars": data.get("stargazers_count"),
                "forks": data.get("forks_count"),
                "watchers": data.get("watchers_count"),
                "language": data.get("language"),
                "topics": data.get("topics", []),
                "created_at": data.get("created_at"),
                "updated_at": data.get("updated_at"),
                "url": data.get("html_url"),
                "homepage": data.get("homepage"),
                "license": data.get("license", {}).get("name")
            }
        except Exception as e:
            logger.error(f"GitHub repo fetch error: {e}")
            return {"error": str(e)}

    def search_issues(
        self,
        query: str,
        sort: str = "created",
        order: str = "desc",
        per_page: int = 30
    ) -> Dict[str, Any]:
        """
        Search GitHub issues and pull requests.

        Args:
            query: Search query
            sort: Sort by (created, updated, comments)
            order: asc or desc
            per_page: Results per page

        Returns:
            Dict with issue search results
        """
        try:
            response = self.session.get(
                f"{self.BASE_URL}/search/issues",
                params={
                    "q": query,
                    "sort": sort,
                    "order": order,
                    "per_page": per_page
                },
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            issues = []
            for item in data.get('items', []):
                issues.append({
                    "title": item.get("title"),
                    "number": item.get("number"),
                    "state": item.get("state"),
                    "user": item.get("user", {}).get("login"),
                    "repository": item.get("repository_url", "").split("/")[-2:],
                    "created_at": item.get("created_at"),
                    "url": item.get("html_url"),
                    "labels": [l.get("name") for l in item.get("labels", [])]
                })

            return {
                "query": query,
                "total_count": data.get('total_count', 0),
                "issues": issues
            }
        except Exception as e:
            logger.error(f"GitHub issue search error: {e}")
            return {"error": str(e)}


#!/usr/bin/env python3
"""
ArXiv API Client

Description: Client for searching and retrieving academic papers from arXiv.org
             with dataclass-based paper representation and multiple search methods.

Use Cases:
- Academic research paper discovery
- Literature review automation
- Citation and reference gathering
- Research trend analysis
- Building academic search tools
- AI agent knowledge base enrichment

Dependencies:
- arxiv (pip install arxiv)

Notes:
- No API key required (public API)
- Rate limiting handled by arxiv package
- Supports search by query, author, or category
- Returns structured ArxivPaper dataclass objects
- Includes paper formatting for display

Related Snippets:
- api-clients/wikipedia_client.py (knowledge base)
- api-clients/pubmed_client.py (biomedical papers)

Source Attribution:
- Extracted from: /home/coolhand/shared/data_fetching/arxiv_client.py
- Author: Luke Steuber
"""

from typing import List, Dict, Optional
from datetime import datetime
from dataclasses import dataclass
import logging

try:
    import arxiv
except ImportError:
    raise ImportError("arxiv package is required. Install with: pip install arxiv")


logger = logging.getLogger(__name__)


@dataclass
class ArxivPaper:
    """Dataclass representing an arXiv paper."""
    title: str
    authors: List[str]
    summary: str
    published: datetime
    updated: datetime
    arxiv_id: str
    pdf_url: str
    categories: List[str]
    entry_id: str
    doi: Optional[str] = None
    comment: Optional[str] = None
    journal_ref: Optional[str] = None
    primary_category: Optional[str] = None

    @classmethod
    def from_arxiv_result(cls, paper: 'arxiv.Result') -> 'ArxivPaper':
        """Create ArxivPaper from arxiv.Result object."""
        return cls(
            title=paper.title,
            authors=[author.name for author in paper.authors],
            summary=paper.summary,
            published=paper.published,
            updated=paper.updated,
            arxiv_id=paper.entry_id.split('/')[-1],
            pdf_url=paper.pdf_url,
            categories=paper.categories,
            entry_id=paper.entry_id,
            doi=getattr(paper, 'doi', None),
            comment=getattr(paper, 'comment', None),
            journal_ref=getattr(paper, 'journal_ref', None),
            primary_category=getattr(paper, 'primary_category', None)
        )

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'title': self.title,
            'authors': self.authors,
            'summary': self.summary,
            'published': self.published.isoformat(),
            'updated': self.updated.isoformat(),
            'arxiv_id': self.arxiv_id,
            'pdf_url': self.pdf_url,
            'categories': self.categories,
            'entry_id': self.entry_id,
            'doi': self.doi,
            'comment': self.comment,
            'journal_ref': self.journal_ref,
            'primary_category': self.primary_category
        }


class ArxivClient:
    """Client for interacting with the arXiv API."""

    def __init__(self):
        """Initialize the arXiv client."""
        self.client = arxiv.Client()

    def search(
        self,
        query: str,
        max_results: int = 5,
        sort_by: str = "relevance"
    ) -> List[ArxivPaper]:
        """
        Search arXiv for papers matching the query.

        Args:
            query: Search query string
            max_results: Maximum number of results to return (default: 5)
            sort_by: Sort order - "relevance" or "date" (default: "relevance")

        Returns:
            List of ArxivPaper objects
        """
        if sort_by not in ["relevance", "date"]:
            raise ValueError(f"Invalid sort_by: {sort_by}. Must be 'relevance' or 'date'")

        try:
            logger.info(f"Searching arXiv for: '{query}' (max: {max_results}, sort: {sort_by})")

            sort_criterion = (
                arxiv.SortCriterion.Relevance
                if sort_by == "relevance"
                else arxiv.SortCriterion.LastUpdatedDate
            )

            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=sort_criterion
            )

            results = list(self.client.results(search))
            papers = [ArxivPaper.from_arxiv_result(paper) for paper in results]

            logger.info(f"Found {len(papers)} papers for query: '{query}'")
            return papers

        except Exception as e:
            logger.error(f"Error searching arXiv: {e}")
            raise

    def get_by_id(self, paper_id: str) -> Optional[ArxivPaper]:
        """
        Get a specific paper by its arXiv ID.

        Args:
            paper_id: arXiv paper ID (e.g., "2301.07041" or "arxiv:2301.07041")

        Returns:
            ArxivPaper object if found, None otherwise
        """
        try:
            clean_id = paper_id.replace('arxiv:', '')
            logger.info(f"Fetching arXiv paper: {clean_id}")

            search = arxiv.Search(id_list=[clean_id])
            results = list(self.client.results(search))

            if not results:
                logger.warning(f"Paper not found: {clean_id}")
                return None

            paper = ArxivPaper.from_arxiv_result(results[0])
            logger.info(f"Retrieved paper: {paper.title}")
            return paper

        except Exception as e:
            logger.error(f"Error fetching arXiv paper {paper_id}: {e}")
            raise

    def get_by_ids(self, paper_ids: List[str]) -> List[ArxivPaper]:
        """
        Get multiple papers by their arXiv IDs.

        Args:
            paper_ids: List of arXiv paper IDs

        Returns:
            List of ArxivPaper objects
        """
        try:
            clean_ids = [pid.replace('arxiv:', '') for pid in paper_ids]
            logger.info(f"Fetching {len(clean_ids)} arXiv papers")

            search = arxiv.Search(id_list=clean_ids)
            results = list(self.client.results(search))

            papers = [ArxivPaper.from_arxiv_result(paper) for paper in results]
            logger.info(f"Retrieved {len(papers)}/{len(clean_ids)} papers")
            return papers

        except Exception as e:
            logger.error(f"Error fetching arXiv papers: {e}")
            raise

    def search_by_author(
        self,
        author: str,
        max_results: int = 10,
        sort_by: str = "date"
    ) -> List[ArxivPaper]:
        """
        Search for papers by a specific author.

        Args:
            author: Author name (e.g., "John Smith")
            max_results: Maximum number of results (default: 10)
            sort_by: Sort order (default: "date")

        Returns:
            List of ArxivPaper objects
        """
        query = f'au:"{author}"'
        return self.search(query, max_results, sort_by)

    def search_by_category(
        self,
        category: str,
        max_results: int = 10,
        sort_by: str = "date"
    ) -> List[ArxivPaper]:
        """
        Search for papers in a specific category.

        Args:
            category: arXiv category (e.g., "cs.AI", "cs.LG", "physics.optics")
            max_results: Maximum number of results (default: 10)
            sort_by: Sort order (default: "date")

        Returns:
            List of ArxivPaper objects
        """
        query = f'cat:{category}'
        return self.search(query, max_results, sort_by)

    def format_paper(self, paper: ArxivPaper, index: Optional[int] = None) -> str:
        """
        Format a paper for display.

        Args:
            paper: ArxivPaper object
            index: Optional paper number for display

        Returns:
            Formatted string representation
        """
        output = []

        if index:
            output.append(f"\n{'='*70}")
            output.append(f"Paper #{index}")
            output.append('='*70)

        output.append(f"Title: {paper.title}")
        output.append(f"Authors: {', '.join(paper.authors)}")
        output.append(f"Published: {paper.published.strftime('%Y-%m-%d')}")
        output.append(f"Updated: {paper.updated.strftime('%Y-%m-%d')}")
        output.append(f"ArXiv ID: {paper.arxiv_id}")
        output.append(f"PDF: {paper.pdf_url}")
        output.append(f"Categories: {', '.join(paper.categories)}")

        if paper.doi:
            output.append(f"DOI: {paper.doi}")
        if paper.journal_ref:
            output.append(f"Journal: {paper.journal_ref}")
        if paper.comment:
            output.append(f"Comment: {paper.comment}")

        output.append(f"\nAbstract:\n{paper.summary}")

        return '\n'.join(output)


# Convenience functions
def search_arxiv(query: str, max_results: int = 5, sort_by: str = "relevance") -> List[Dict]:
    """
    Convenience function for searching arXiv (returns dicts).

    Args:
        query: Search query string
        max_results: Maximum number of results
        sort_by: Sort order

    Returns:
        List of paper dictionaries
    """
    client = ArxivClient()
    papers = client.search(query, max_results, sort_by)
    return [paper.to_dict() for paper in papers]


def get_paper_by_id(paper_id: str) -> Optional[Dict]:
    """
    Convenience function for getting a paper by ID (returns dict).

    Args:
        paper_id: arXiv paper ID

    Returns:
        Paper dictionary if found, None otherwise
    """
    client = ArxivClient()
    paper = client.get_by_id(paper_id)
    return paper.to_dict() if paper else None


def format_for_llm(papers: List[ArxivPaper], max_papers: int = 5) -> str:
    """
    Format papers for LLM context.

    Args:
        papers: List of ArxivPaper objects
        max_papers: Maximum papers to include

    Returns:
        Formatted string for LLM context
    """
    output = ["# ArXiv Research Papers\n"]

    for i, paper in enumerate(papers[:max_papers], 1):
        output.append(f"## {i}. {paper.title}")
        output.append(f"**Authors:** {', '.join(paper.authors)}")
        output.append(f"**Published:** {paper.published.strftime('%Y-%m-%d')}")
        output.append(f"**Categories:** {', '.join(paper.categories)}")
        output.append(f"\n{paper.summary}\n")
        output.append(f"[PDF]({paper.pdf_url}) | arXiv:{paper.arxiv_id}\n")

    return '\n'.join(output)


# Usage example
if __name__ == "__main__":
    print("ArXiv Client Demo")
    print("=" * 50)

    client = ArxivClient()

    # Search for papers
    print("\nSearching for 'machine learning' papers...")
    papers = client.search("machine learning", max_results=3)

    for paper in papers:
        print(f"\n  Title: {paper.title[:60]}...")
        print(f"  Authors: {', '.join(paper.authors[:3])}...")
        print(f"  Published: {paper.published.strftime('%Y-%m-%d')}")
        print(f"  Categories: {', '.join(paper.categories[:3])}")

    # Search by author
    print("\n" + "-" * 50)
    print("Searching by author 'Yoshua Bengio'...")
    author_papers = client.search_by_author("Yoshua Bengio", max_results=2)

    for paper in author_papers:
        print(f"\n  {paper.title[:50]}...")

    # Search by category
    print("\n" + "-" * 50)
    print("Searching category 'cs.AI'...")
    ai_papers = client.search_by_category("cs.AI", max_results=2)

    for paper in ai_papers:
        print(f"\n  {paper.title[:50]}...")

    # LLM formatting
    print("\n" + "-" * 50)
    print("LLM-formatted output:\n")
    print(format_for_llm(papers, max_papers=2))

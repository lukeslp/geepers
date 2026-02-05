#!/usr/bin/env python3
"""
Academic Citation Parser

Description: Multi-style citation extractor supporting APA, MLA, Chicago, Harvard, and IEEE
             formats with BibTeX generation capability. Extracts both in-text citations
             and reference list entries.

Use Cases:
- Extracting citations from academic papers
- Converting citations between formats
- Building bibliography databases
- Academic writing tools and validators
- Reference management applications

Dependencies:
- None (stdlib only)

Notes:
- Regex patterns handle common citation variations but may miss edge cases
- BibTeX generation is best-effort and may require manual review
- Style detection works on both in-text citations and reference lists
- Format conversion is placeholder - full implementation requires citation parsing

Related Snippets:
- api-clients/wolfram_alpha_client.py (for academic data queries)

Source Attribution:
- Extracted from: /home/coolhand/inbox/apis/llamni/utils/citations.py
- Author: Luke Steuber
"""

import logging
import re
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

# Regular expressions for different citation styles
CITATION_PATTERNS = {
    'apa': [
        # APA in-text citations: (Smith, 2020) or (Smith et al., 2020)
        r'\(([A-Za-z\-]+(?:,? (?:et al\.)?)?(?:, (?:19|20)\d{2}(?:[a-z])?)?(?:; [A-Za-z\-]+(?:,? (?:et al\.)?)?, (?:19|20)\d{2}(?:[a-z])?)*)\)',
        # APA reference list entries
        r'([A-Za-z\-]+,\s[A-Z]\.(?:\s[A-Z]\.)?\s\((?:19|20)\d{2}\)\..*?\.(?:\s+doi:.+?|Retrieved from.+?)?)(?:\n|\r\n?|$)'
    ],
    'mla': [
        # MLA in-text citations: (Smith 45) or (Smith and Jones 45-50)
        r'\(([A-Za-z\-]+(?: and [A-Za-z\-]+)*(?: \d+(?:-\d+)?)?)\)',
        # MLA Works Cited entries
        r'([A-Za-z\-]+,\s[A-Za-z]+(?:,? et al)?\..*?(?:19|20)\d{2}\.(?:.*?\.)?(?:\s+(?:Print|Web)\.))(?:\n|\r\n?|$)'
    ],
    'chicago': [
        # Chicago footnote citations
        r'(?:^|\n)\d+\.\s([A-Za-z\-]+(?: [A-Za-z\-]+)*,.*?(?:19|20)\d{2}.*?\.)',
        # Chicago bibliography entries
        r'([A-Za-z\-]+,\s[A-Za-z]+(?:,? et al)?\..*?(?:19|20)\d{2}\.(?:.*?\.)?)(?:\n|\r\n?|$)'
    ],
    'harvard': [
        # Harvard in-text citations (similar to APA)
        r'\(([A-Za-z\-]+(?:,? (?:et al\.)?)?(?:, (?:19|20)\d{2}(?:[a-z])?)?(?:; [A-Za-z\-]+(?:,? (?:et al\.)?)?, (?:19|20)\d{2}(?:[a-z])?)*)\)',
        # Harvard reference list entries
        r'([A-Za-z\-]+,\s[A-Z]\.(?:\s[A-Z]\.)?\s\((?:19|20)\d{2}\)\..*?\.)(?:\n|\r\n?|$)'
    ],
    'ieee': [
        # IEEE in-text citations: [1] or [1-3] or [1, 2, 5]
        r'\[(\d+(?:-\d+)?(?:, \d+(?:-\d+)?)*)\]',
        # IEEE reference list entries
        r'(?:^|\n)\[(\d+)\]\s([A-Za-z\.\s\-]+,.*?(?:19|20)\d{2}\.(?:.*?\.)?)(?:\n|\r\n?|$)'
    ]
}


def extract_citations(text: str, styles: Optional[List[str]] = None) -> Dict[str, Dict[str, List[str]]]:
    """
    Extract citations from text according to specified citation styles.

    Args:
        text: Text to extract citations from
        styles: Citation styles to look for (default: all styles)
                Options: 'apa', 'mla', 'chicago', 'harvard', 'ieee'

    Returns:
        Dictionary with citations by style, each containing:
        - in_text: List of in-text citations found
        - references: List of reference list entries found
    """
    if not text:
        return {}

    styles = styles or list(CITATION_PATTERNS.keys())

    # Validate styles
    valid_styles = []
    for style in styles:
        if style.lower() in CITATION_PATTERNS:
            valid_styles.append(style.lower())
        else:
            logger.warning(f"Unknown citation style: {style}")

    results = {}

    for style in valid_styles:
        style_results = {
            'in_text': [],
            'references': []
        }

        patterns = CITATION_PATTERNS[style]

        # Extract in-text citations
        if len(patterns) > 0:
            in_text_pattern = patterns[0]
            in_text_matches = re.findall(in_text_pattern, text)
            style_results['in_text'] = list(set(in_text_matches))

        # Extract reference list entries
        if len(patterns) > 1:
            reference_pattern = patterns[1]
            reference_matches = re.findall(reference_pattern, text, re.MULTILINE)

            if style == 'ieee' and reference_matches:
                references = []
                for match in reference_matches:
                    if isinstance(match, tuple) and len(match) == 2:
                        ref_num, ref_text = match
                        references.append(f"[{ref_num}] {ref_text}")
                    else:
                        references.append(match)
                style_results['references'] = references
            else:
                style_results['references'] = list(set(reference_matches))

        results[style] = style_results

    return results


def format_citation(citation: str, from_style: str, to_style: str) -> str:
    """
    Convert a citation from one style to another.

    Args:
        citation: Citation text
        from_style: Original citation style
        to_style: Target citation style

    Returns:
        Reformatted citation (placeholder - full implementation requires parsing)
    """
    logger.warning("Citation format conversion not fully implemented")
    return f"[Converted from {from_style} to {to_style}]: {citation}"


def generate_bibtex(citations: Dict[str, Dict[str, List[str]]]) -> str:
    """
    Generate BibTeX entries from extracted citations.

    Args:
        citations: Dictionary with citations by style (from extract_citations)

    Returns:
        BibTeX formatted string with all entries
    """
    bibtex_entries = []

    for style, entries in citations.items():
        if 'references' in entries and entries['references']:
            for ref in entries['references']:
                try:
                    key = _generate_bibtex_key(ref, style)
                    entry = _convert_to_bibtex(ref, key, style)
                    if entry:
                        bibtex_entries.append(entry)
                except Exception as e:
                    logger.error(f"Error generating BibTeX for citation: {str(e)}")

    # Remove duplicates while preserving order
    unique_entries = []
    seen_keys = set()

    for entry in bibtex_entries:
        key_match = re.search(r'@\w+{([^,]+),', entry)
        if key_match:
            key = key_match.group(1)
            if key not in seen_keys:
                seen_keys.add(key)
                unique_entries.append(entry)

    return "\n\n".join(unique_entries)


def _generate_bibtex_key(citation: str, style: str) -> str:
    """Generate a BibTeX key from a citation."""
    key = f"citation_{hash(citation) % 10000:04d}"

    try:
        if style in ['apa', 'harvard']:
            author_match = re.search(r'^([A-Za-z\-]+)', citation)
            year_match = re.search(r'\((\d{4})[a-z]?\)', citation)
            if author_match and year_match:
                author = author_match.group(1).strip().lower()
                year = year_match.group(1)
                key = f"{author}{year}"

        elif style == 'mla':
            author_match = re.search(r'^([A-Za-z\-]+)', citation)
            year_match = re.search(r'(\d{4})', citation)
            if author_match and year_match:
                author = author_match.group(1).strip().lower()
                year = year_match.group(1)
                key = f"{author}{year}"

        elif style == 'chicago':
            author_match = re.search(r'^([A-Za-z\-]+)', citation)
            year_match = re.search(r'(\d{4})', citation)
            if author_match and year_match:
                author = author_match.group(1).strip().lower()
                year = year_match.group(1)
                key = f"{author}{year}"

        elif style == 'ieee':
            num_match = re.search(r'^\[(\d+)\]', citation)
            if num_match:
                num = num_match.group(1)
                key = f"ieee{num}"
                author_match = re.search(r'\]\s+([A-Za-z\-]+)', citation)
                if author_match:
                    author = author_match.group(1).strip().lower()
                    key = f"{author}{num}"

    except Exception as e:
        logger.warning(f"Error generating BibTeX key: {str(e)}")

    key = re.sub(r'[^a-z0-9]', '', key)
    return key


def _convert_to_bibtex(citation: str, key: str, style: str) -> Optional[str]:
    """Convert a citation to BibTeX format."""
    try:
        # Determine entry type
        entry_type = "misc"
        if "journal" in citation.lower() or "proceedings" in citation.lower():
            entry_type = "article"
        elif "book" in citation.lower() or "press" in citation.lower():
            entry_type = "book"
        elif "conference" in citation.lower() or "symposium" in citation.lower():
            entry_type = "inproceedings"
        elif "thesis" in citation.lower() or "dissertation" in citation.lower():
            entry_type = "phdthesis"

        fields = {"title": "{Unknown Title}"}

        # Extract author
        author_match = None
        if style in ['apa', 'harvard', 'mla', 'chicago']:
            author_match = re.search(r'^([A-Za-z\-]+,\s[A-Za-z\.]+(?:,? et al\.)?)', citation)
        elif style == 'ieee':
            author_match = re.search(r'\]\s+([A-Za-z\.\s\-]+,)', citation)
        if author_match:
            fields["author"] = "{" + author_match.group(1).strip() + "}"

        # Extract year
        year_match = re.search(r'(\d{4})[a-z]?', citation)
        if year_match:
            fields["year"] = year_match.group(1)

        # Extract title
        title_match = None
        if style in ['apa', 'harvard']:
            title_match = re.search(r'\.\s+([^\.]+)\.', citation)
        elif style in ['mla', 'chicago']:
            if "\"" in citation:
                title_match = re.search(r'\"([^\"]+)\"', citation)
            else:
                title_match = re.search(r'\.\s+([^\.]+)\.', citation)
        elif style == 'ieee':
            title_match = re.search(r',\s+\"([^\"]+)\"', citation)
            if not title_match:
                title_match = re.search(r',\s+([^,\.]+)\.', citation)
        if title_match:
            fields["title"] = "{" + title_match.group(1).strip() + "}"

        # Extract journal/publisher
        if re.search(r'(?:In |in )([^\.]+)', citation):
            journal_match = re.search(r'(?:In |in )([^\.]+)', citation)
            fields["journal"] = "{" + journal_match.group(1).strip() + "}"
        elif re.search(r'\d{4}[a-z]?\.\s+([^\.]+)', citation):
            journal_match = re.search(r'\d{4}[a-z]?\.\s+([^\.]+)', citation)
            fields["journal"] = "{" + journal_match.group(1).strip() + "}"

        # Extract DOI
        doi_match = re.search(r'doi:([^\s]+)', citation)
        if doi_match:
            fields["doi"] = doi_match.group(1).strip()

        # Extract URL
        url_match = re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', citation)
        if url_match:
            fields["url"] = url_match.group(0).strip()

        # Format the BibTeX entry
        entry = f"@{entry_type}{{{key},\n"
        for field, value in fields.items():
            entry += f"  {field} = {value},\n"
        entry += "}"

        return entry

    except Exception as e:
        logger.error(f"Error converting citation to BibTeX: {str(e)}")
        return None


def detect_citation_style(text: str) -> Optional[str]:
    """
    Attempt to detect the predominant citation style in a text.

    Args:
        text: Text to analyze

    Returns:
        Detected style name or None if unclear
    """
    results = extract_citations(text)

    style_scores = {}
    for style, data in results.items():
        score = len(data.get('in_text', [])) + len(data.get('references', []))
        if score > 0:
            style_scores[style] = score

    if style_scores:
        return max(style_scores, key=style_scores.get)
    return None


# Usage example
if __name__ == "__main__":
    sample_text = """
    Research has shown significant results (Smith, 2020). Other studies
    (Jones et al., 2019; Williams, 2021) have confirmed these findings.
    The methodology follows established practices (Brown and Davis, 2018).

    References:

    Smith, J. A. (2020). A study of citation patterns. Journal of Research, 15(2), 45-67.
    Jones, B., Williams, C., & Brown, D. (2019). Multi-author studies. Academic Press.
    Williams, E. (2021). Recent developments in citation analysis. doi:10.1234/example.2021
    Brown, F., & Davis, G. (2018). Collaborative research methods. Retrieved from https://example.com

    IEEE style example:
    [1] A. Smith, "Machine learning approaches," IEEE Trans., vol. 5, pp. 123-145, 2020.
    [2] B. Jones and C. Williams, "Deep learning review," in Proc. Conf., 2021.
    """

    print("Citation Parser Demo")
    print("=" * 50)

    # Detect style
    detected = detect_citation_style(sample_text)
    print(f"Detected predominant style: {detected}")

    # Extract all citations
    print("\nExtracted Citations:")
    print("-" * 30)

    citations = extract_citations(sample_text)
    for style, data in citations.items():
        if data['in_text'] or data['references']:
            print(f"\n{style.upper()}:")
            if data['in_text']:
                print(f"  In-text ({len(data['in_text'])}):")
                for cite in data['in_text'][:3]:
                    print(f"    - {cite}")
            if data['references']:
                print(f"  References ({len(data['references'])}):")
                for ref in data['references'][:2]:
                    print(f"    - {ref[:60]}...")

    # Generate BibTeX
    print("\nBibTeX Output:")
    print("-" * 30)
    bibtex = generate_bibtex(citations)
    if bibtex:
        print(bibtex[:500] + "..." if len(bibtex) > 500 else bibtex)
    else:
        print("No BibTeX entries generated")

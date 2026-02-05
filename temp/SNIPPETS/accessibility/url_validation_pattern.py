"""
Comprehensive URL Validation Pattern

Description: Robust pattern for validating, testing, and enriching URLs in web applications,
particularly useful for accessibility audits, link checkers, and content management systems.

Use Cases:
- Accessibility audits: Validate all external links in documentation
- Content management: Check for broken links before publishing
- SEO tools: Identify redirects and broken links
- Migration tools: Validate links during content migration
- Quality assurance: Automated link checking in CI/CD

Dependencies:
- urllib.request (stdlib)
- urllib.error (stdlib)
- urllib.parse (stdlib)
- socket (stdlib)
- time (stdlib)
- typing (stdlib)

Notes:
- Includes rate limiting to avoid overwhelming servers
- Supports retry logic with exponential backoff
- Detects redirects and returns final URLs
- Handles various error types (404, 403, timeouts, SSL errors)
- User-agent spoofing to avoid bot detection
- Respects common web scraping etiquette

Related Snippets:
- error-handling/graceful_import_fallbacks.py - Error handling patterns
- utilities/retry_with_backoff.py - Retry logic patterns

Source Attribution:
- Extracted from: /home/coolhand/html/accessibility/link_validator.py
- Author: Luke Steuber
- Project: Accessibility Resource Platform (dr.eamer.dev/accessibility)
"""

import re
import time
import urllib.request
import urllib.error
import urllib.parse
import socket
from typing import Dict, Optional, Tuple
from html.parser import HTMLParser


# Configuration constants
REQUEST_TIMEOUT = 10  # seconds
RATE_LIMIT_DELAY = 0.5  # seconds between requests
MAX_RETRIES = 2
USER_AGENT = 'Mozilla/5.0 (compatible; AccessibilityLinkValidator/1.0)'


class LinkExtractor(HTMLParser):
    """
    Extract all external links from HTML content.

    This parser tracks context like section IDs to provide better
    error reporting and organization of extracted links.
    """

    def __init__(self):
        super().__init__()
        self.links = []
        self.current_section = None
        self.current_link_text = ''

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        # Track sections for context
        if tag == 'section':
            self.current_section = attrs_dict.get('id', 'unknown')

        # Extract links
        if tag == 'a' and 'href' in attrs_dict:
            href = attrs_dict['href']
            if href.startswith('http'):
                self.links.append({
                    'url': href,
                    'text': '',
                    'section': self.current_section,
                    'attrs': attrs_dict
                })
                self.current_link_text = ''

    def handle_data(self, data):
        # Capture link text
        if self.links and not self.links[-1]['text']:
            self.links[-1]['text'] = data.strip()


def extract_markdown_links(content: str) -> list:
    """
    Extract links from Markdown content.

    Finds all [text](url) patterns and returns structured data
    including section context.

    Args:
        content: Markdown content as string

    Returns:
        List of dicts with keys: url, text, section, line
    """
    links = []
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'

    current_section = None
    for line in content.split('\n'):
        # Track sections (markdown headers)
        if line.startswith('## '):
            current_section = line[3:].strip()

        matches = re.finditer(pattern, line)
        for match in matches:
            text, url = match.groups()
            if url.startswith('http'):
                links.append({
                    'url': url,
                    'text': text,
                    'section': current_section or 'unknown',
                    'line': line
                })

    return links


def validate_url(url: str, retries: int = MAX_RETRIES) -> Dict:
    """
    Validate a single URL and return comprehensive status information.

    This function performs robust URL validation with retry logic,
    redirect detection, and detailed error reporting.

    Args:
        url: The URL to validate
        retries: Number of retry attempts (default: MAX_RETRIES)

    Returns:
        Dict containing:
            - url: Original URL
            - status: 'success', 'error', or 'timeout'
            - status_code: HTTP status code (if available)
            - final_url: Final URL after redirects
            - error: Error message (if failed)
            - redirect_count: Number of redirects followed
            - content_type: Content-Type header value
    """
    result = {
        'url': url,
        'status': None,
        'status_code': None,
        'final_url': url,
        'error': None,
        'redirect_count': 0,
        'content_type': None
    }

    for attempt in range(retries):
        try:
            # Create request with proper headers to avoid bot detection
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': USER_AGENT,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Connection': 'close'
                }
            )

            # Make request with timeout
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as response:
                result['status'] = 'success'
                result['status_code'] = response.status
                result['final_url'] = response.url
                result['content_type'] = response.headers.get('Content-Type', '')

                # Check for redirects
                if response.url != url:
                    result['redirect_count'] = 1

                return result

        except urllib.error.HTTPError as e:
            result['status'] = 'error'
            result['status_code'] = e.code
            result['error'] = f'HTTP {e.code}: {e.reason}'

            # Don't retry on certain permanent errors
            if e.code in [404, 403, 410]:
                return result

        except urllib.error.URLError as e:
            result['status'] = 'error'
            result['error'] = f'URL Error: {str(e.reason)}'

        except socket.timeout:
            result['status'] = 'timeout'
            result['error'] = 'Request timed out'

        except Exception as e:
            result['status'] = 'error'
            result['error'] = f'Unexpected error: {str(e)}'

        # Wait before retry (simple exponential backoff)
        if attempt < retries - 1:
            time.sleep(1 * (attempt + 1))

    return result


def validate_urls_batch(urls: list, rate_limit: float = RATE_LIMIT_DELAY) -> Dict:
    """
    Validate a batch of URLs with rate limiting.

    Args:
        urls: List of URL strings or dicts with 'url' key
        rate_limit: Delay between requests in seconds

    Returns:
        Dict with validation results and statistics
    """
    results = {
        'total': len(urls),
        'checked': 0,
        'success': 0,
        'errors': 0,
        'timeouts': 0,
        'redirects': 0,
        'links': []
    }

    for i, url_item in enumerate(urls, 1):
        # Handle both strings and dicts
        url = url_item if isinstance(url_item, str) else url_item.get('url')

        # Validate the URL
        validation = validate_url(url)

        # Merge with original metadata if dict was provided
        if isinstance(url_item, dict):
            full_result = {**url_item, **validation}
        else:
            full_result = validation

        results['links'].append(full_result)

        # Update counters
        results['checked'] += 1
        if validation['status'] == 'success':
            results['success'] += 1
            if validation['redirect_count'] > 0:
                results['redirects'] += 1
        elif validation['status'] == 'timeout':
            results['timeouts'] += 1
        else:
            results['errors'] += 1

        # Progress update every 10 URLs
        if i % 10 == 0:
            print(f"Progress: {i}/{len(urls)} - "
                  f"Success: {results['success']}, "
                  f"Errors: {results['errors']}, "
                  f"Timeouts: {results['timeouts']}")

        # Rate limiting
        if i < len(urls):  # Don't sleep after last request
            time.sleep(rate_limit)

    return results


def deduplicate_urls(url_list: list) -> list:
    """
    Remove duplicate URLs while preserving context and metadata.

    If the same URL appears in multiple sections, track all sections
    in 'additional_sections' field.

    Args:
        url_list: List of URL dicts

    Returns:
        List of unique URL dicts with merged metadata
    """
    seen = {}
    unique_urls = []

    for item in url_list:
        url = item['url']
        if url not in seen:
            seen[url] = item
            unique_urls.append(item)
        else:
            # Add section context if different
            if 'section' in item and item['section'] != seen[url].get('section'):
                if 'additional_sections' not in seen[url]:
                    seen[url]['additional_sections'] = []
                seen[url]['additional_sections'].append(item['section'])

    return unique_urls


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == '__main__':
    print("=" * 80)
    print("URL Validation Pattern - Usage Examples")
    print("=" * 80)

    # Example 1: Validate a single URL
    print("\n1. Single URL Validation:")
    print("-" * 80)

    test_url = 'https://www.w3.org/WAI/WCAG21/quickref/'
    result = validate_url(test_url)

    print(f"URL: {result['url']}")
    print(f"Status: {result['status']}")
    print(f"Status Code: {result['status_code']}")
    print(f"Final URL: {result['final_url']}")
    if result['redirect_count'] > 0:
        print(f"⚠ Redirected {result['redirect_count']} times")
    if result['error']:
        print(f"Error: {result['error']}")

    # Example 2: Extract and validate links from HTML
    print("\n2. Extract Links from HTML:")
    print("-" * 80)

    sample_html = '''
    <section id="resources">
        <h2>Resources</h2>
        <a href="https://www.w3.org/WAI/">WAI Resources</a>
        <a href="https://webaim.org/">WebAIM</a>
    </section>
    '''

    parser = LinkExtractor()
    parser.feed(sample_html)

    print(f"Found {len(parser.links)} links:")
    for link in parser.links:
        print(f"  - {link['text']}: {link['url']} (section: {link['section']})")

    # Example 3: Extract links from Markdown
    print("\n3. Extract Links from Markdown:")
    print("-" * 80)

    sample_markdown = '''
## Accessibility Guidelines

- [WCAG 2.1](https://www.w3.org/WAI/WCAG21/quickref/)
- [Section 508](https://www.section508.gov/)
    '''

    md_links = extract_markdown_links(sample_markdown)
    print(f"Found {len(md_links)} markdown links:")
    for link in md_links:
        print(f"  - {link['text']}: {link['url']}")

    # Example 4: Batch validation with rate limiting
    print("\n4. Batch URL Validation:")
    print("-" * 80)

    test_urls = [
        'https://www.w3.org/WAI/',
        'https://webaim.org/',
        'https://example.com/this-page-does-not-exist-404',
    ]

    print(f"Validating {len(test_urls)} URLs...")
    batch_results = validate_urls_batch(test_urls, rate_limit=0.5)

    print(f"\nResults:")
    print(f"  Total: {batch_results['total']}")
    print(f"  Success: {batch_results['success']}")
    print(f"  Errors: {batch_results['errors']}")
    print(f"  Timeouts: {batch_results['timeouts']}")
    print(f"  Redirects: {batch_results['redirects']}")

    # Example 5: Deduplication
    print("\n5. URL Deduplication:")
    print("-" * 80)

    duplicate_urls = [
        {'url': 'https://www.w3.org/WAI/', 'section': 'intro'},
        {'url': 'https://www.w3.org/WAI/', 'section': 'resources'},
        {'url': 'https://webaim.org/', 'section': 'tools'},
    ]

    unique = deduplicate_urls(duplicate_urls)
    print(f"Original: {len(duplicate_urls)} items")
    print(f"After deduplication: {len(unique)} unique URLs")
    for item in unique:
        print(f"  - {item['url']}")
        if 'additional_sections' in item:
            print(f"    Also appears in: {', '.join(item['additional_sections'])}")

    print("\n" + "=" * 80)
    print("Examples complete!")
    print("=" * 80)

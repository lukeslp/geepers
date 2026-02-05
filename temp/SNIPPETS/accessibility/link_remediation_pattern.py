"""
Link Remediation and Fixing Pattern

Description: Automated pattern for fixing broken links, applying redirects, and updating
URLs in HTML and Markdown content. Useful for maintaining large documentation sites,
accessibility resources, and content management systems.

Use Cases:
- Content maintenance: Update broken links in documentation
- Migration tools: Update old URLs to new domains
- Accessibility audits: Fix broken links found during audits
- SEO optimization: Update redirected URLs to final destinations
- Automated link hygiene: Periodic link cleanup in CI/CD

Dependencies:
- re (stdlib)
- typing (stdlib)
- json (stdlib) - for validation results

Notes:
- Supports both HTML (href attributes) and Markdown ([text](url) format)
- Uses regex for safe replacement of exact matches
- Maintains separate fix dictionaries for different error types
- Can process validation results from url_validation_pattern.py
- Includes changelog generation for tracking changes

Related Snippets:
- accessibility/url_validation_pattern.py - URL validation
- file-operations/batch_file_processor.py - File processing patterns
- utilities/changelog_generator.py - Change tracking

Source Attribution:
- Extracted from: /home/coolhand/html/accessibility/link_fixer.py
- Author: Luke Steuber
- Project: Accessibility Resource Platform (dr.eamer.dev/accessibility)
"""

import re
from typing import Dict, List, Tuple, Set


# ============================================================================
# FIX DICTIONARIES - Customize these for your specific needs
# ============================================================================

# Example: Known broken links with replacement URLs
# In production, populate these from validation results or manual research
BROKEN_LINK_FIXES = {
    # Format: 'old_url': 'new_url'
    'https://example.com/old-page': 'https://example.com/new-page',
    'https://defunct-site.com/resource': 'https://archive.org/details/resource',
}

# SSL/Certificate issues - use alternative URLs
SSL_FIXES = {
    'https://broken-ssl.com/': 'http://broken-ssl.com/',  # Fallback to HTTP
}

# Defunct services to remove or flag
LINKS_TO_REMOVE = {
    'https://defunct-service.com/',
}


# ============================================================================
# CORE FUNCTIONS
# ============================================================================

def apply_redirects(
    content: str,
    file_type: str,
    redirects: List[Dict]
) -> Tuple[str, List[str]]:
    """
    Apply redirect fixes to content (update old URLs to final URLs).

    Args:
        content: File content (HTML or Markdown)
        file_type: 'html' or 'markdown'
        redirects: List of dicts with 'from' and 'to' keys

    Returns:
        Tuple of (updated_content, list_of_changes)
    """
    changes = []

    for redirect in redirects:
        old_url = redirect['from']
        new_url = redirect['to']

        # Skip if URLs are identical
        if old_url == new_url:
            continue

        if file_type == 'html':
            # Update HTML href attributes
            old_pattern = f'href="{re.escape(old_url)}"'
            new_pattern = f'href="{new_url}"'
            if old_pattern in content:
                content = content.replace(old_pattern, new_pattern)
                changes.append(f"Updated redirect: {old_url} -> {new_url}")

        elif file_type == 'markdown':
            # Update Markdown links [text](url)
            old_pattern = f']({re.escape(old_url)})'
            new_pattern = f']({new_url})'
            if old_pattern in content:
                content = content.replace(old_pattern, new_pattern)
                changes.append(f"Updated redirect: {old_url} -> {new_url}")

    return content, changes


def apply_broken_link_fixes(
    content: str,
    file_type: str,
    fix_dict: Dict[str, str] = None
) -> Tuple[str, List[str]]:
    """
    Apply fixes for broken links using a fix dictionary.

    Args:
        content: File content
        file_type: 'html' or 'markdown'
        fix_dict: Dictionary mapping old URLs to new URLs

    Returns:
        Tuple of (updated_content, list_of_changes)
    """
    if fix_dict is None:
        fix_dict = BROKEN_LINK_FIXES

    changes = []

    for old_url, new_url in fix_dict.items():
        if file_type == 'html':
            old_pattern = f'href="{re.escape(old_url)}"'
            new_pattern = f'href="{new_url}"'
            if old_pattern in content:
                content = content.replace(old_pattern, new_pattern)
                changes.append(f"Fixed broken link: {old_url} -> {new_url}")

        elif file_type == 'markdown':
            old_pattern = f']({re.escape(old_url)})'
            new_pattern = f']({new_url})'
            if old_pattern in content:
                content = content.replace(old_pattern, new_pattern)
                changes.append(f"Fixed broken link: {old_url} -> {new_url}")

    return content, changes


def apply_ssl_fixes(
    content: str,
    file_type: str,
    ssl_fix_dict: Dict[str, str] = None
) -> Tuple[str, List[str]]:
    """
    Apply SSL certificate fixes (usually HTTPS -> HTTP fallback or alternative domain).

    Args:
        content: File content
        file_type: 'html' or 'markdown'
        ssl_fix_dict: Dictionary mapping problematic URLs to alternatives

    Returns:
        Tuple of (updated_content, list_of_changes)
    """
    if ssl_fix_dict is None:
        ssl_fix_dict = SSL_FIXES

    changes = []

    for old_url, new_url in ssl_fix_dict.items():
        if file_type == 'html':
            old_pattern = f'href="{re.escape(old_url)}"'
            new_pattern = f'href="{new_url}"'
            if old_pattern in content:
                content = content.replace(old_pattern, new_pattern)
                changes.append(f"Fixed SSL issue: {old_url} -> {new_url}")

        elif file_type == 'markdown':
            old_pattern = f']({re.escape(old_url)})'
            new_pattern = f']({new_url})'
            if old_pattern in content:
                content = content.replace(old_pattern, new_pattern)
                changes.append(f"Fixed SSL issue: {old_url} -> {new_url}")

    return content, changes


def flag_defunct_links(
    content: str,
    file_type: str,
    defunct_urls: Set[str] = None
) -> Tuple[str, List[str]]:
    """
    Identify defunct links that should be removed or replaced.

    This function doesn't modify content, just reports what was found.

    Args:
        content: File content
        file_type: 'html' or 'markdown'
        defunct_urls: Set of URLs known to be defunct

    Returns:
        Tuple of (content, list_of_warnings)
    """
    if defunct_urls is None:
        defunct_urls = LINKS_TO_REMOVE

    warnings = []

    for url in defunct_urls:
        if url in content:
            warnings.append(f"⚠ Defunct link found: {url} - Consider removing or replacing")

    return content, warnings


def apply_all_fixes(
    content: str,
    file_type: str,
    validation_results: Dict = None,
    broken_fixes: Dict = None,
    ssl_fixes: Dict = None
) -> Tuple[str, List[str]]:
    """
    Apply all fixes in sequence: redirects, broken links, SSL issues.

    Args:
        content: File content
        file_type: 'html' or 'markdown'
        validation_results: Optional dict from url_validation_pattern.py
        broken_fixes: Optional custom broken link fixes
        ssl_fixes: Optional custom SSL fixes

    Returns:
        Tuple of (updated_content, all_changes)
    """
    all_changes = []

    # 1. Apply redirects (if validation results provided)
    if validation_results and 'categories' in validation_results:
        redirects = validation_results['categories'].get('redirected', [])
        content, changes = apply_redirects(content, file_type, redirects)
        all_changes.extend(changes)

    # 2. Fix broken 404 links
    content, changes = apply_broken_link_fixes(content, file_type, broken_fixes)
    all_changes.extend(changes)

    # 3. Fix SSL issues
    content, changes = apply_ssl_fixes(content, file_type, ssl_fixes)
    all_changes.extend(changes)

    # 4. Flag defunct links
    content, warnings = flag_defunct_links(content, file_type)
    all_changes.extend(warnings)

    return content, all_changes


def generate_changelog(changes: Dict[str, List[str]], title: str = "Link Updates") -> str:
    """
    Generate a human-readable changelog from fix results.

    Args:
        changes: Dict mapping file paths to lists of changes
        title: Changelog title

    Returns:
        Formatted changelog string
    """
    lines = []

    lines.append("=" * 80)
    lines.append(title.upper())
    lines.append("=" * 80)
    lines.append("")

    total_changes = sum(len(c) for c in changes.values())
    lines.append(f"Total changes: {total_changes}")
    lines.append(f"Files modified: {len(changes)}")
    lines.append("")

    for file_path, file_changes in changes.items():
        lines.append(f"FILE: {file_path}")
        lines.append("-" * 80)
        for change in file_changes:
            lines.append(f"  • {change}")
        lines.append("")

    lines.append("=" * 80)
    lines.append("END OF CHANGELOG")
    lines.append("=" * 80)

    return "\n".join(lines)


def process_file(
    input_file: str,
    output_file: str,
    file_type: str,
    validation_results: Dict = None,
    **kwargs
) -> List[str]:
    """
    Process a single file: read, apply fixes, write back.

    Args:
        input_file: Path to input file
        output_file: Path to output file (can be same as input)
        file_type: 'html' or 'markdown'
        validation_results: Optional validation results dict
        **kwargs: Additional arguments passed to apply_all_fixes

    Returns:
        List of changes made
    """
    # Read file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Apply all fixes
    updated_content, changes = apply_all_fixes(
        content,
        file_type,
        validation_results,
        **kwargs
    )

    # Write back
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    return changes


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == '__main__':
    print("=" * 80)
    print("Link Remediation Pattern - Usage Examples")
    print("=" * 80)

    # Example 1: Fix HTML content
    print("\n1. Fix Links in HTML Content:")
    print("-" * 80)

    sample_html = '''
    <div>
        <a href="https://example.com/old-page">Old Link</a>
        <a href="https://example.com/redirect-source">Redirected Link</a>
    </div>
    '''

    # Define custom fixes for this example
    example_fixes = {
        'https://example.com/old-page': 'https://example.com/new-page'
    }

    # Simulate redirect data
    example_redirects = [
        {'from': 'https://example.com/redirect-source', 'to': 'https://example.com/redirect-final'}
    ]

    validation_results = {
        'categories': {
            'redirected': example_redirects
        }
    }

    updated_html, changes = apply_all_fixes(
        sample_html,
        'html',
        validation_results=validation_results,
        broken_fixes=example_fixes
    )

    print(f"Changes made: {len(changes)}")
    for change in changes:
        print(f"  • {change}")

    print("\nUpdated HTML:")
    print(updated_html)

    # Example 2: Fix Markdown content
    print("\n2. Fix Links in Markdown Content:")
    print("-" * 80)

    sample_markdown = '''
## Resources

- [Old Resource](https://example.com/old-page)
- [Working Link](https://example.com/good-page)
    '''

    updated_md, changes = apply_broken_link_fixes(
        sample_markdown,
        'markdown',
        example_fixes
    )

    print(f"Changes made: {len(changes)}")
    for change in changes:
        print(f"  • {change}")

    # Example 3: Apply redirects only
    print("\n3. Apply Redirects Only:")
    print("-" * 80)

    content = '<a href="https://old.com/">Link</a>'
    redirects = [{'from': 'https://old.com/', 'to': 'https://new.com/'}]

    updated, changes = apply_redirects(content, 'html', redirects)
    print(f"Original: {content}")
    print(f"Updated: {updated}")

    # Example 4: Generate changelog
    print("\n4. Generate Changelog:")
    print("-" * 80)

    changes_by_file = {
        '/path/to/index.html': [
            'Updated redirect: https://old.com/ -> https://new.com/',
            'Fixed broken link: https://broken.com/ -> https://working.com/'
        ],
        '/path/to/README.md': [
            'Fixed SSL issue: https://ssl-error.com/ -> http://ssl-error.com/'
        ]
    }

    changelog = generate_changelog(changes_by_file, "Accessibility Link Fixes")
    print(changelog)

    # Example 5: Flag defunct links
    print("\n5. Flag Defunct Links:")
    print("-" * 80)

    content_with_defunct = '''
    <a href="https://good-site.com/">Good</a>
    <a href="https://defunct-service.com/">Bad</a>
    '''

    _, warnings = flag_defunct_links(content_with_defunct, 'html')
    print(f"Found {len(warnings)} defunct link(s):")
    for warning in warnings:
        print(f"  {warning}")

    print("\n" + "=" * 80)
    print("Examples complete!")
    print("=" * 80)
    print("\nTip: Combine with url_validation_pattern.py for automated")
    print("link maintenance workflow:")
    print("  1. Validate all links")
    print("  2. Identify broken links and redirects")
    print("  3. Apply fixes automatically")
    print("  4. Generate changelog")

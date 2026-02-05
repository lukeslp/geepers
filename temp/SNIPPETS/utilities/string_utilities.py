"""
String Manipulation Utilities

Description: Comprehensive string manipulation utilities for text processing, sanitization,
formatting, and validation. Essential for working with user input, API responses, and text data.

Use Cases:
- Sanitizing user input for security
- Creating URL-safe slugs from titles
- Truncating text with ellipsis
- Stripping HTML tags and formatting
- Case conversion and normalization
- Extracting and validating data from strings

Dependencies:
- re (stdlib)
- html (stdlib)
- typing (stdlib)
- Optional: unidecode for better slug generation

Notes:
- All functions handle None and empty strings gracefully
- Unicode-aware string operations
- No external dependencies required (unidecode is optional)
- Performance-optimized with regex caching

Related Snippets:
- /home/coolhand/SNIPPETS/data-processing/ - Data transformation
- /home/coolhand/SNIPPETS/utilities/datetime_utilities.py - Date formatting

Source Attribution:
- Extracted from: Multiple swarm modules and web applications
- Related patterns: /home/coolhand/projects/swarm/slate/js/interface.js
- Author: Luke Steuber
"""

import re
import html
from typing import Optional, List, Pattern
import logging


logger = logging.getLogger(__name__)

# Compile regex patterns once for performance
HTML_TAG_PATTERN: Pattern = re.compile(r'<[^>]+>')
WHITESPACE_PATTERN: Pattern = re.compile(r'\s+')
SLUG_PATTERN: Pattern = re.compile(r'[^\w\s-]')
SLUG_SEPARATOR_PATTERN: Pattern = re.compile(r'[-\s]+')


def truncate(
    text: str,
    max_length: int = 100,
    suffix: str = "..."
) -> str:
    """
    Truncate text to maximum length with suffix.

    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to add when truncated (default: "...")

    Returns:
        Truncated text with suffix if needed

    Example:
        >>> truncate("This is a very long text that needs truncating", 20)
        'This is a very lo...'
        >>>
        >>> truncate("Short text", 100)
        'Short text'
    """
    if not text:
        return ""

    if len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix


def strip_html(text: str) -> str:
    """
    Remove HTML tags from text.

    Args:
        text: HTML text to strip

    Returns:
        Plain text without HTML tags

    Example:
        >>> strip_html("<p>Hello <strong>world</strong>!</p>")
        'Hello world!'
        >>>
        >>> strip_html("Plain text")
        'Plain text'
    """
    if not text:
        return ""

    # Unescape HTML entities first
    text = html.unescape(text)

    # Remove HTML tags
    text = HTML_TAG_PATTERN.sub('', text)

    # Normalize whitespace
    text = WHITESPACE_PATTERN.sub(' ', text)

    return text.strip()


def slugify(text: str, separator: str = "-", lowercase: bool = True) -> str:
    """
    Convert text to URL-safe slug.

    Args:
        text: Text to convert
        separator: Separator character (default: hyphen)
        lowercase: Convert to lowercase (default: True)

    Returns:
        URL-safe slug

    Example:
        >>> slugify("Hello World! This is a Test")
        'hello-world-this-is-a-test'
        >>>
        >>> slugify("Product Name (2025)", separator="_", lowercase=False)
        'Product_Name_2025'
    """
    if not text:
        return ""

    # Try to use unidecode for better unicode handling
    try:
        from unidecode import unidecode
        text = unidecode(text)
    except ImportError:
        # Fallback to basic ASCII conversion
        text = text.encode('ascii', 'ignore').decode('ascii')

    if lowercase:
        text = text.lower()

    # Remove non-word characters (except spaces and hyphens)
    text = SLUG_PATTERN.sub('', text)

    # Replace spaces and repeated separators with single separator
    text = SLUG_SEPARATOR_PATTERN.sub(separator, text)

    # Remove leading/trailing separators
    text = text.strip(separator)

    return text


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace in text.

    Replaces multiple whitespace characters with single space,
    removes leading/trailing whitespace.

    Args:
        text: Text to normalize

    Returns:
        Normalized text

    Example:
        >>> normalize_whitespace("Hello    world\\n\\t!")
        'Hello world !'
        >>>
        >>> normalize_whitespace("  spaces  everywhere  ")
        'spaces everywhere'
    """
    if not text:
        return ""

    return WHITESPACE_PATTERN.sub(' ', text).strip()


def sanitize_filename(filename: str, replacement: str = "_") -> str:
    """
    Sanitize filename by removing/replacing invalid characters.

    Args:
        filename: Filename to sanitize
        replacement: Character to replace invalid chars (default: underscore)

    Returns:
        Safe filename

    Example:
        >>> sanitize_filename("my file?.txt")
        'my_file_.txt'
        >>>
        >>> sanitize_filename("report (2025).pdf")
        'report__2025_.pdf'
    """
    if not filename:
        return ""

    # Remove path separators and other dangerous characters
    invalid_chars = r'[<>:"/\\|?*\x00-\x1f]'
    filename = re.sub(invalid_chars, replacement, filename)

    # Remove leading/trailing dots and spaces
    filename = filename.strip('. ')

    return filename


def extract_numbers(text: str) -> List[float]:
    """
    Extract all numbers from text.

    Args:
        text: Text containing numbers

    Returns:
        List of numbers found

    Example:
        >>> extract_numbers("Price: $19.99, Quantity: 5")
        [19.99, 5.0]
        >>>
        >>> extract_numbers("No numbers here")
        []
    """
    if not text:
        return []

    # Match integers and floats
    pattern = r'-?\d+\.?\d*'
    matches = re.findall(pattern, text)

    return [float(m) for m in matches if m]


def extract_urls(text: str) -> List[str]:
    """
    Extract URLs from text.

    Args:
        text: Text containing URLs

    Returns:
        List of URLs found

    Example:
        >>> text = "Check out https://example.com and http://test.org"
        >>> extract_urls(text)
        ['https://example.com', 'http://test.org']
    """
    if not text:
        return []

    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    return re.findall(url_pattern, text)


def extract_emails(text: str) -> List[str]:
    """
    Extract email addresses from text.

    Args:
        text: Text containing emails

    Returns:
        List of email addresses found

    Example:
        >>> text = "Contact: user@example.com or admin@test.org"
        >>> extract_emails(text)
        ['user@example.com', 'admin@test.org']
    """
    if not text:
        return []

    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(email_pattern, text)


def capitalize_words(text: str, exceptions: Optional[List[str]] = None) -> str:
    """
    Capitalize first letter of each word (title case) with exceptions.

    Args:
        text: Text to capitalize
        exceptions: Words to keep lowercase (articles, prepositions, etc.)

    Returns:
        Title-cased text

    Example:
        >>> capitalize_words("the quick brown fox")
        'The Quick Brown Fox'
        >>>
        >>> exceptions = ['the', 'and', 'of', 'in']
        >>> capitalize_words("the lord of the rings", exceptions)
        'The Lord of the Rings'
    """
    if not text:
        return ""

    exceptions = exceptions or []
    exceptions_lower = [e.lower() for e in exceptions]

    words = text.split()
    result = []

    for i, word in enumerate(words):
        # Always capitalize first word
        if i == 0:
            result.append(word.capitalize())
        # Keep exception words lowercase
        elif word.lower() in exceptions_lower:
            result.append(word.lower())
        # Capitalize other words
        else:
            result.append(word.capitalize())

    return ' '.join(result)


def mask_sensitive(
    text: str,
    mask_char: str = "*",
    visible_start: int = 4,
    visible_end: int = 4
) -> str:
    """
    Mask sensitive information (API keys, tokens, etc.).

    Args:
        text: Text to mask
        mask_char: Character to use for masking
        visible_start: Number of characters to show at start
        visible_end: Number of characters to show at end

    Returns:
        Masked text

    Example:
        >>> mask_sensitive("sk-1234567890abcdef", visible_start=3, visible_end=4)
        'sk-***********cdef'
        >>>
        >>> mask_sensitive("secret_api_key_12345")
        'secr***********2345'
    """
    if not text:
        return ""

    length = len(text)

    if length <= visible_start + visible_end:
        # Too short to mask meaningfully
        return mask_char * length

    masked_length = length - visible_start - visible_end
    return (
        text[:visible_start] +
        mask_char * masked_length +
        text[-visible_end:]
    )


def word_count(text: str) -> int:
    """
    Count words in text.

    Args:
        text: Text to count words in

    Returns:
        Number of words

    Example:
        >>> word_count("Hello world! This is a test.")
        6
    """
    if not text:
        return 0

    # Remove extra whitespace and count
    words = WHITESPACE_PATTERN.sub(' ', text).strip().split()
    return len(words)


def char_count(text: str, exclude_whitespace: bool = False) -> int:
    """
    Count characters in text.

    Args:
        text: Text to count characters in
        exclude_whitespace: If True, don't count whitespace

    Returns:
        Number of characters

    Example:
        >>> char_count("Hello world!")
        12
        >>>
        >>> char_count("Hello world!", exclude_whitespace=True)
        10
    """
    if not text:
        return 0

    if exclude_whitespace:
        return len(re.sub(r'\s', '', text))

    return len(text)


def remove_duplicates(text: str, case_sensitive: bool = True) -> str:
    """
    Remove duplicate words while preserving order.

    Args:
        text: Text with potential duplicates
        case_sensitive: Consider case when finding duplicates

    Returns:
        Text with duplicates removed

    Example:
        >>> remove_duplicates("the the quick brown brown fox")
        'the quick brown fox'
        >>>
        >>> remove_duplicates("The the quick", case_sensitive=False)
        'The quick'
    """
    if not text:
        return ""

    words = text.split()
    seen = set()
    result = []

    for word in words:
        check_word = word if case_sensitive else word.lower()

        if check_word not in seen:
            seen.add(check_word)
            result.append(word)

    return ' '.join(result)


def wrap_text(text: str, width: int = 80, indent: str = "") -> str:
    """
    Wrap text to specified width.

    Args:
        text: Text to wrap
        width: Maximum line width
        indent: String to indent each line

    Returns:
        Wrapped text

    Example:
        >>> long_text = "This is a very long line that needs to be wrapped"
        >>> print(wrap_text(long_text, width=20))
        This is a very long
        line that needs to
        be wrapped
    """
    if not text:
        return ""

    import textwrap
    return textwrap.fill(text, width=width, initial_indent=indent, subsequent_indent=indent)


# Example usage and testing
if __name__ == "__main__":
    print("String Manipulation Utilities Examples")
    print("=" * 60)

    # Example 1: Truncation
    print("\n1. Text Truncation")
    print("-" * 60)
    long_text = "This is a very long text that needs to be truncated for display purposes."
    print(f"Original: {long_text}")
    print(f"Truncated (30): {truncate(long_text, 30)}")
    print(f"Truncated (50): {truncate(long_text, 50)}")

    # Example 2: HTML stripping
    print("\n2. HTML Stripping")
    print("-" * 60)
    html_text = "<p>Hello <strong>world</strong>! This is <em>HTML</em>.</p>"
    print(f"HTML: {html_text}")
    print(f"Stripped: {strip_html(html_text)}")

    # Example 3: Slugify
    print("\n3. URL Slug Generation")
    print("-" * 60)
    titles = [
        "Hello World! This is a Test",
        "Product Name (2025)",
        "Luke's Blog Post #42"
    ]
    for title in titles:
        print(f"{title} -> {slugify(title)}")

    # Example 4: Sanitize filename
    print("\n4. Filename Sanitization")
    print("-" * 60)
    filenames = [
        "my file?.txt",
        "report (2025).pdf",
        "data/export.csv"
    ]
    for filename in filenames:
        print(f"{filename} -> {sanitize_filename(filename)}")

    # Example 5: Extract data
    print("\n5. Data Extraction")
    print("-" * 60)
    sample_text = "Price: $19.99, Quantity: 5. Visit https://example.com or email support@example.com"
    print(f"Text: {sample_text}")
    print(f"Numbers: {extract_numbers(sample_text)}")
    print(f"URLs: {extract_urls(sample_text)}")
    print(f"Emails: {extract_emails(sample_text)}")

    # Example 6: Masking
    print("\n6. Sensitive Data Masking")
    print("-" * 60)
    api_key = "sk-1234567890abcdefghijklmnop"
    print(f"Original: {api_key}")
    print(f"Masked: {mask_sensitive(api_key)}")

    # Example 7: Title case
    print("\n7. Title Case with Exceptions")
    print("-" * 60)
    title = "the lord of the rings: the return of the king"
    exceptions = ['the', 'of']
    print(f"Original: {title}")
    print(f"Title case: {capitalize_words(title, exceptions)}")

    # Example 8: Whitespace normalization
    print("\n8. Whitespace Normalization")
    print("-" * 60)
    messy_text = "   Hello    world  \\n\\t  with   spaces   "
    print(f"Messy: '{messy_text}'")
    print(f"Normalized: '{normalize_whitespace(messy_text)}'")

    # Example 9: Word/char counting
    print("\n9. Counting")
    print("-" * 60)
    sample = "Hello world! This is a test."
    print(f"Text: {sample}")
    print(f"Words: {word_count(sample)}")
    print(f"Characters (with spaces): {char_count(sample)}")
    print(f"Characters (without spaces): {char_count(sample, exclude_whitespace=True)}")

    print("\n" + "=" * 60)
    print("All examples completed!")

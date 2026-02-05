"""
Data Sanitization and Cleaning Patterns

Description: Comprehensive patterns for sanitizing, cleaning, and normalizing data from various sources including user input, API responses, and file uploads. Includes text cleaning, email validation, URL sanitization, and data normalization.

Use Cases:
- Sanitizing user input before database storage
- Cleaning API response data for consistency
- Normalizing text data for search and comparison
- Validating and formatting email addresses and URLs
- Removing sensitive information from logs
- Preparing data for machine learning pipelines

Dependencies:
- re (stdlib)
- html (stdlib)
- urllib.parse (stdlib)
- typing (stdlib)
- unicodedata (stdlib)

Notes:
- All functions preserve Unicode characters properly
- Email validation is basic; use dedicated libraries for RFC-compliant validation
- URL sanitization removes dangerous protocols (javascript:, data:)
- Text normalization includes multiple strategies (lowercase, remove accents, etc.)
- HTML entity decoding prevents injection attacks
- All sanitization is conservative - preserves data when uncertain

Related Snippets:
- data-processing/pydantic_validation_patterns.py - Schema validation
- data-processing/json_validation_patterns.py - JSON-specific validation
- error-handling/graceful_import_fallbacks.py - Safe imports

Source Attribution:
- Patterns extracted from multiple projects handling user input
- Inspired by security best practices from /home/coolhand/projects/tools_bluesky
- Text processing patterns from /home/coolhand/projects/swarm
"""

import re
import html
import unicodedata
from typing import Any, Dict, List, Optional, Set, Union
from urllib.parse import urlparse, urlunparse, quote, unquote


# ===== Text Sanitization =====

def sanitize_text(
    text: str,
    strip_whitespace: bool = True,
    remove_control_chars: bool = True,
    normalize_whitespace: bool = True,
    max_length: Optional[int] = None
) -> str:
    """
    Sanitize text by removing unwanted characters and normalizing whitespace.

    Args:
        text: Input text to sanitize
        strip_whitespace: Remove leading/trailing whitespace
        remove_control_chars: Remove control characters
        normalize_whitespace: Replace multiple spaces with single space
        max_length: Maximum length (truncate if longer)

    Returns:
        Sanitized text

    Example:
        >>> text = "  Hello\\n\\nWorld  \\t "
        >>> sanitize_text(text)
        'Hello World'

        >>> sanitize_text("Test\\x00String", remove_control_chars=True)
        'TestString'
    """
    if strip_whitespace:
        text = text.strip()

    if remove_control_chars:
        # Remove all control characters except newline, tab
        text = ''.join(char for char in text
                      if not unicodedata.category(char).startswith('C')
                      or char in '\n\t')

    if normalize_whitespace:
        # Replace multiple spaces/tabs with single space
        text = ' '.join(text.split())

    if max_length is not None and len(text) > max_length:
        text = text[:max_length]

    return text


def normalize_text_for_comparison(
    text: str,
    lowercase: bool = True,
    remove_accents: bool = False,
    remove_punctuation: bool = False
) -> str:
    """
    Normalize text for comparison or search operations.

    Args:
        text: Input text
        lowercase: Convert to lowercase
        remove_accents: Remove diacritical marks (café → cafe)
        remove_punctuation: Remove punctuation characters

    Returns:
        Normalized text

    Example:
        >>> normalize_text_for_comparison("Café!")
        'café!'

        >>> normalize_text_for_comparison("Café!", remove_accents=True, remove_punctuation=True)
        'cafe'
    """
    if lowercase:
        text = text.lower()

    if remove_accents:
        # Decompose Unicode characters and remove combining marks
        text = ''.join(
            char for char in unicodedata.normalize('NFD', text)
            if unicodedata.category(char) != 'Mn'
        )

    if remove_punctuation:
        # Remove punctuation (keep alphanumeric and spaces)
        text = re.sub(r'[^\w\s]', '', text, flags=re.UNICODE)

    return sanitize_text(text)


def remove_html_tags(text: str, decode_entities: bool = True) -> str:
    """
    Remove HTML tags from text.

    Args:
        text: Text potentially containing HTML
        decode_entities: Decode HTML entities (&amp; → &)

    Returns:
        Text with HTML removed

    Example:
        >>> remove_html_tags("<p>Hello <b>world</b>!</p>")
        'Hello world!'

        >>> remove_html_tags("&lt;script&gt;alert('xss')&lt;/script&gt;")
        "<script>alert('xss')</script>"
    """
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    if decode_entities:
        text = html.unescape(text)

    return text


# ===== Email Sanitization =====

def sanitize_email(email: str) -> Optional[str]:
    """
    Sanitize and validate email address (basic validation).

    Args:
        email: Email address to sanitize

    Returns:
        Sanitized email or None if invalid

    Example:
        >>> sanitize_email("  USER@EXAMPLE.COM  ")
        'user@example.com'

        >>> sanitize_email("invalid-email") is None
        True
    """
    # Basic sanitization
    email = email.strip().lower()

    # Basic validation
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return None

    return email


def extract_emails_from_text(text: str) -> List[str]:
    """
    Extract and sanitize all email addresses from text.

    Args:
        text: Text potentially containing emails

    Returns:
        List of sanitized email addresses

    Example:
        >>> text = "Contact us at support@example.com or sales@example.com"
        >>> extract_emails_from_text(text)
        ['support@example.com', 'sales@example.com']
    """
    email_pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
    emails = re.findall(email_pattern, text)
    return [email.lower() for email in emails]


# ===== URL Sanitization =====

def sanitize_url(
    url: str,
    allowed_schemes: Optional[Set[str]] = None,
    remove_query_params: Optional[Set[str]] = None
) -> Optional[str]:
    """
    Sanitize URL by validating scheme and removing dangerous components.

    Args:
        url: URL to sanitize
        allowed_schemes: Set of allowed URL schemes (default: http, https)
        remove_query_params: Set of query parameter names to remove

    Returns:
        Sanitized URL or None if invalid/dangerous

    Example:
        >>> sanitize_url("https://example.com/path")
        'https://example.com/path'

        >>> sanitize_url("javascript:alert('xss')") is None
        True

        >>> sanitize_url("http://example.com?token=secret&id=123",
        ...              remove_query_params={'token'})
        'http://example.com?id=123'
    """
    if allowed_schemes is None:
        allowed_schemes = {'http', 'https'}

    url = url.strip()

    try:
        parsed = urlparse(url)

        # Check scheme
        if parsed.scheme and parsed.scheme.lower() not in allowed_schemes:
            return None

        # Remove specified query parameters
        if remove_query_params and parsed.query:
            from urllib.parse import parse_qs, urlencode
            query_dict = parse_qs(parsed.query)
            filtered_query = {
                k: v for k, v in query_dict.items()
                if k not in remove_query_params
            }
            query_string = urlencode(filtered_query, doseq=True)
            parsed = parsed._replace(query=query_string)

        return urlunparse(parsed)

    except Exception:
        return None


def normalize_url(url: str) -> str:
    """
    Normalize URL for comparison (remove trailing slashes, lowercase domain, etc.).

    Args:
        url: URL to normalize

    Returns:
        Normalized URL

    Example:
        >>> normalize_url("HTTPS://EXAMPLE.COM/PATH/")
        'https://example.com/path'
    """
    parsed = urlparse(url.strip())

    # Lowercase scheme and netloc
    scheme = parsed.scheme.lower() if parsed.scheme else ''
    netloc = parsed.netloc.lower() if parsed.netloc else ''

    # Remove trailing slash from path
    path = parsed.path.rstrip('/') if parsed.path else ''

    # Reconstruct
    normalized = urlunparse((
        scheme,
        netloc,
        path,
        parsed.params,
        parsed.query,
        parsed.fragment
    ))

    return normalized


# ===== Data Type Sanitization =====

def sanitize_int(value: Any, default: int = 0, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
    """
    Sanitize value to integer with bounds checking.

    Args:
        value: Value to convert to int
        default: Default value if conversion fails
        min_val: Minimum allowed value
        max_val: Maximum allowed value

    Returns:
        Sanitized integer

    Example:
        >>> sanitize_int("123")
        123

        >>> sanitize_int("invalid", default=0)
        0

        >>> sanitize_int(150, max_val=100)
        100
    """
    try:
        result = int(value)
    except (ValueError, TypeError):
        return default

    if min_val is not None and result < min_val:
        result = min_val

    if max_val is not None and result > max_val:
        result = max_val

    return result


def sanitize_float(value: Any, default: float = 0.0, precision: Optional[int] = None) -> float:
    """
    Sanitize value to float with optional precision.

    Args:
        value: Value to convert to float
        default: Default value if conversion fails
        precision: Number of decimal places (None for no rounding)

    Returns:
        Sanitized float

    Example:
        >>> sanitize_float("3.14159", precision=2)
        3.14

        >>> sanitize_float("invalid", default=0.0)
        0.0
    """
    try:
        result = float(value)
    except (ValueError, TypeError):
        return default

    if precision is not None:
        result = round(result, precision)

    return result


def sanitize_bool(value: Any, default: bool = False) -> bool:
    """
    Sanitize value to boolean with string parsing.

    Args:
        value: Value to convert to bool
        default: Default value if conversion fails

    Returns:
        Boolean value

    Example:
        >>> sanitize_bool("true")
        True

        >>> sanitize_bool("yes")
        True

        >>> sanitize_bool("0")
        False
    """
    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        value_lower = value.lower().strip()
        if value_lower in ('true', 'yes', '1', 'on'):
            return True
        elif value_lower in ('false', 'no', '0', 'off'):
            return False

    if isinstance(value, (int, float)):
        return bool(value)

    return default


# ===== String Sanitization =====

def sanitize_username(username: str, min_length: int = 3, max_length: int = 50) -> Optional[str]:
    """
    Sanitize username (alphanumeric, underscores, hyphens only).

    Args:
        username: Username to sanitize
        min_length: Minimum length
        max_length: Maximum length

    Returns:
        Sanitized username or None if invalid

    Example:
        >>> sanitize_username("  User_123  ")
        'user_123'

        >>> sanitize_username("user@#$") is None
        True
    """
    # Remove whitespace and convert to lowercase
    username = username.strip().lower()

    # Allow only alphanumeric, underscore, hyphen
    if not re.match(r'^[a-z0-9_-]+$', username):
        return None

    # Check length
    if len(username) < min_length or len(username) > max_length:
        return None

    return username


def sanitize_filename(filename: str, max_length: int = 255) -> str:
    """
    Sanitize filename by removing dangerous characters.

    Args:
        filename: Filename to sanitize
        max_length: Maximum filename length

    Returns:
        Sanitized filename

    Example:
        >>> sanitize_filename("my file.txt")
        'my_file.txt'

        >>> sanitize_filename("../../../etc/passwd")
        'etc_passwd'
    """
    # Remove directory traversal attempts
    filename = filename.replace('..', '')

    # Remove path separators
    filename = filename.replace('/', '_').replace('\\', '_')

    # Remove other dangerous characters
    filename = re.sub(r'[<>:"|?*]', '', filename)

    # Replace spaces with underscores
    filename = filename.replace(' ', '_')

    # Remove leading/trailing dots and underscores
    filename = filename.strip('._')

    # Limit length
    if len(filename) > max_length:
        # Preserve extension if possible
        parts = filename.rsplit('.', 1)
        if len(parts) == 2:
            name, ext = parts
            max_name_length = max_length - len(ext) - 1
            filename = name[:max_name_length] + '.' + ext
        else:
            filename = filename[:max_length]

    return filename or 'file'


# ===== Dictionary Sanitization =====

def sanitize_dict_keys(
    data: Dict[str, Any],
    allowed_keys: Optional[Set[str]] = None,
    forbidden_keys: Optional[Set[str]] = None,
    recursive: bool = False
) -> Dict[str, Any]:
    """
    Sanitize dictionary by filtering keys.

    Args:
        data: Dictionary to sanitize
        allowed_keys: If set, only these keys are kept
        forbidden_keys: If set, these keys are removed
        recursive: Apply to nested dictionaries

    Returns:
        Sanitized dictionary

    Example:
        >>> data = {"name": "Alice", "password": "secret", "email": "alice@ex.com"}
        >>> sanitize_dict_keys(data, forbidden_keys={"password"})
        {'name': 'Alice', 'email': 'alice@ex.com'}
    """
    result = {}

    for key, value in data.items():
        # Check if key is allowed
        if allowed_keys is not None and key not in allowed_keys:
            continue

        if forbidden_keys is not None and key in forbidden_keys:
            continue

        # Recursively sanitize nested dicts
        if recursive and isinstance(value, dict):
            value = sanitize_dict_keys(value, allowed_keys, forbidden_keys, recursive)

        result[key] = value

    return result


def remove_null_values(data: Dict[str, Any], recursive: bool = True) -> Dict[str, Any]:
    """
    Remove None/null values from dictionary.

    Args:
        data: Dictionary to clean
        recursive: Apply to nested dictionaries

    Returns:
        Dictionary without None values

    Example:
        >>> data = {"a": 1, "b": None, "c": {"d": None, "e": 2}}
        >>> remove_null_values(data)
        {'a': 1, 'c': {'e': 2}}
    """
    result = {}

    for key, value in data.items():
        if value is None:
            continue

        if recursive and isinstance(value, dict):
            value = remove_null_values(value, recursive)
            if value:  # Only include non-empty dicts
                result[key] = value
        else:
            result[key] = value

    return result


# ===== Usage Examples =====

if __name__ == "__main__":
    print("=" * 70)
    print("Data Sanitization Patterns - Usage Examples")
    print("=" * 70)

    # 1. Text Sanitization
    print("\n1. Text Sanitization:")
    print("-" * 70)
    dirty_text = "  Hello\\n\\nWorld  \\t\\x00 "
    clean_text = sanitize_text(dirty_text)
    print(f"Original: {repr(dirty_text)}")
    print(f"Sanitized: {repr(clean_text)}")

    # 2. Text Normalization
    print("\n2. Text Normalization for Comparison:")
    print("-" * 70)
    text1 = "Café"
    text2 = "CAFE"
    normalized1 = normalize_text_for_comparison(text1, remove_accents=True)
    normalized2 = normalize_text_for_comparison(text2, remove_accents=True)
    print(f"{text1} → {normalized1}")
    print(f"{text2} → {normalized2}")
    print(f"Match: {normalized1 == normalized2}")

    # 3. HTML Removal
    print("\n3. HTML Tag Removal:")
    print("-" * 70)
    html_text = "<p>Hello <b>world</b>! &amp; welcome.</p>"
    clean_html = remove_html_tags(html_text)
    print(f"Original: {html_text}")
    print(f"Cleaned: {clean_html}")

    # 4. Email Sanitization
    print("\n4. Email Sanitization:")
    print("-" * 70)
    emails = ["  USER@EXAMPLE.COM  ", "valid@test.com", "invalid-email"]
    for email in emails:
        sanitized = sanitize_email(email)
        print(f"{email} → {sanitized}")

    # 5. URL Sanitization
    print("\n5. URL Sanitization:")
    print("-" * 70)
    urls = [
        "https://example.com/path",
        "javascript:alert('xss')",
        "http://example.com?token=secret&id=123"
    ]
    for url in urls:
        sanitized = sanitize_url(url, remove_query_params={'token'})
        print(f"{url}")
        print(f"  → {sanitized}")

    # 6. Type Sanitization
    print("\n6. Data Type Sanitization:")
    print("-" * 70)
    print(f"sanitize_int('123'): {sanitize_int('123')}")
    print(f"sanitize_int('invalid', default=0): {sanitize_int('invalid', default=0)}")
    print(f"sanitize_int(150, max_val=100): {sanitize_int(150, max_val=100)}")
    print(f"sanitize_bool('yes'): {sanitize_bool('yes')}")
    print(f"sanitize_float('3.14159', precision=2): {sanitize_float('3.14159', precision=2)}")

    # 7. Username Sanitization
    print("\n7. Username Sanitization:")
    print("-" * 70)
    usernames = ["  User_123  ", "valid-user", "user@#$", "ab"]
    for username in usernames:
        sanitized = sanitize_username(username)
        print(f"{username} → {sanitized}")

    # 8. Filename Sanitization
    print("\n8. Filename Sanitization:")
    print("-" * 70)
    filenames = ["my file.txt", "../../../etc/passwd", "file<>:name.doc"]
    for filename in filenames:
        sanitized = sanitize_filename(filename)
        print(f"{filename} → {sanitized}")

    # 9. Dictionary Sanitization
    print("\n9. Dictionary Key Filtering:")
    print("-" * 70)
    data = {
        "name": "Alice",
        "password": "secret123",
        "email": "alice@example.com",
        "internal_id": "xyz"
    }
    sanitized = sanitize_dict_keys(data, forbidden_keys={"password", "internal_id"})
    print(f"Original keys: {list(data.keys())}")
    print(f"Sanitized keys: {list(sanitized.keys())}")

    # 10. Remove Null Values
    print("\n10. Remove Null Values:")
    print("-" * 70)
    data_with_nulls = {
        "a": 1,
        "b": None,
        "c": {"d": None, "e": 2},
        "f": {"g": None}
    }
    cleaned = remove_null_values(data_with_nulls)
    print(f"Original: {data_with_nulls}")
    print(f"Cleaned: {cleaned}")

    print("\n" + "=" * 70)
    print("Examples complete!")
    print("=" * 70)

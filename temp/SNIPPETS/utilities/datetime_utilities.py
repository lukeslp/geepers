"""
Date and Time Utilities

Description: Production-ready date and time manipulation utilities for parsing, formatting,
and working with timestamps, timezones, and human-readable time representations.

Use Cases:
- Parsing ISO 8601 timestamps from APIs
- Converting between timezones
- Human-readable time formatting ("2 hours ago", "in 3 days")
- Calculating time differences and durations
- Working with Unix timestamps

Dependencies:
- datetime (stdlib)
- typing (stdlib)
- Optional: pytz for advanced timezone support

Notes:
- Handles timezone-aware and naive datetimes
- Graceful fallback for parsing failures
- Support for multiple date formats
- Compatible with ISO 8601, RFC 3339, and common formats

Related Snippets:
- /home/coolhand/SNIPPETS/utilities/string_utilities.py - String formatting
- /home/coolhand/SNIPPETS/data-processing/ - Data transformation

Source Attribution:
- Extracted from: /home/coolhand/projects/swarm/llms/anthropic_chat.py
- Related patterns: /home/coolhand/html/beltalowda/task-swarm/test_next/cli/anthropic_api.py
- Author: Luke Steuber
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Union
import logging


logger = logging.getLogger(__name__)


def format_date(date_str: str, output_format: str = "%B %d, %Y") -> str:
    """
    Format a date string in a human-readable format.

    Handles multiple input formats including ISO 8601, RFC 3339,
    and common date formats. Gracefully falls back to original
    string if parsing fails.

    Args:
        date_str: Date string to format (ISO 8601, RFC 3339, etc.)
        output_format: strftime format string (default: "Month Day, Year")

    Returns:
        Formatted date string, or original string if parsing fails

    Example:
        >>> format_date("2025-01-15T14:30:00Z")
        'January 15, 2025'
        >>>
        >>> format_date("2025-01-15T14:30:00+00:00", "%Y-%m-%d")
        '2025-01-15'
        >>>
        >>> format_date("2025-01-15", "%m/%d/%Y")
        '01/15/2025'
    """
    try:
        # Handle ISO 8601 with 'Z' timezone indicator
        normalized = date_str.replace('Z', '+00:00')
        dt = datetime.fromisoformat(normalized)
        return dt.strftime(output_format)
    except (ValueError, AttributeError) as e:
        logger.debug(f"Failed to parse date '{date_str}': {e}")
        return date_str


def parse_iso_timestamp(timestamp: str) -> Optional[datetime]:
    """
    Parse an ISO 8601 timestamp into a datetime object.

    Handles both timezone-aware and naive timestamps.

    Args:
        timestamp: ISO 8601 timestamp string

    Returns:
        datetime object or None if parsing fails

    Example:
        >>> dt = parse_iso_timestamp("2025-01-15T14:30:00Z")
        >>> print(dt)
        2025-01-15 14:30:00+00:00
        >>>
        >>> dt = parse_iso_timestamp("2025-01-15T14:30:00")
        >>> print(dt)
        2025-01-15 14:30:00
    """
    try:
        # Handle 'Z' timezone indicator
        normalized = timestamp.replace('Z', '+00:00')
        return datetime.fromisoformat(normalized)
    except (ValueError, AttributeError) as e:
        logger.error(f"Failed to parse timestamp '{timestamp}': {e}")
        return None


def unix_to_datetime(timestamp: Union[int, float], tz: Optional[timezone] = None) -> datetime:
    """
    Convert Unix timestamp to datetime object.

    Args:
        timestamp: Unix timestamp (seconds since epoch)
        tz: Timezone (default: UTC)

    Returns:
        datetime object

    Example:
        >>> dt = unix_to_datetime(1705329000)
        >>> print(dt)
        2025-01-15 14:30:00+00:00
        >>>
        >>> # With timezone
        >>> from datetime import timezone, timedelta
        >>> eastern = timezone(timedelta(hours=-5))
        >>> dt = unix_to_datetime(1705329000, tz=eastern)
    """
    tz = tz or timezone.utc
    return datetime.fromtimestamp(timestamp, tz=tz)


def datetime_to_unix(dt: datetime) -> int:
    """
    Convert datetime object to Unix timestamp.

    Args:
        dt: datetime object

    Returns:
        Unix timestamp (seconds since epoch)

    Example:
        >>> from datetime import datetime
        >>> dt = datetime(2025, 1, 15, 14, 30)
        >>> timestamp = datetime_to_unix(dt)
        >>> print(timestamp)
        1705329000
    """
    return int(dt.timestamp())


def time_ago(dt: datetime) -> str:
    """
    Convert datetime to human-readable "time ago" format.

    Args:
        dt: datetime object (should be timezone-aware)

    Returns:
        Human-readable time difference string

    Example:
        >>> from datetime import datetime, timedelta, timezone
        >>> now = datetime.now(timezone.utc)
        >>> two_hours_ago = now - timedelta(hours=2)
        >>> print(time_ago(two_hours_ago))
        '2 hours ago'
        >>>
        >>> yesterday = now - timedelta(days=1)
        >>> print(time_ago(yesterday))
        '1 day ago'
    """
    now = datetime.now(timezone.utc)

    # Ensure both datetimes are timezone-aware
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    diff = now - dt

    # Calculate time components
    seconds = int(diff.total_seconds())
    minutes = seconds // 60
    hours = minutes // 60
    days = diff.days

    if seconds < 60:
        return "just now"
    elif minutes < 60:
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif hours < 24:
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif days < 7:
        return f"{days} day{'s' if days != 1 else ''} ago"
    elif days < 30:
        weeks = days // 7
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"
    elif days < 365:
        months = days // 30
        return f"{months} month{'s' if months != 1 else ''} ago"
    else:
        years = days // 365
        return f"{years} year{'s' if years != 1 else ''} ago"


def time_until(dt: datetime) -> str:
    """
    Convert datetime to human-readable "time until" format.

    Args:
        dt: Future datetime object

    Returns:
        Human-readable time difference string

    Example:
        >>> from datetime import datetime, timedelta, timezone
        >>> now = datetime.now(timezone.utc)
        >>> in_two_hours = now + timedelta(hours=2)
        >>> print(time_until(in_two_hours))
        'in 2 hours'
    """
    now = datetime.now(timezone.utc)

    # Ensure both datetimes are timezone-aware
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    diff = dt - now

    if diff.total_seconds() < 0:
        return time_ago(dt)

    # Calculate time components
    seconds = int(diff.total_seconds())
    minutes = seconds // 60
    hours = minutes // 60
    days = diff.days

    if seconds < 60:
        return "in less than a minute"
    elif minutes < 60:
        return f"in {minutes} minute{'s' if minutes != 1 else ''}"
    elif hours < 24:
        return f"in {hours} hour{'s' if hours != 1 else ''}"
    elif days < 7:
        return f"in {days} day{'s' if days != 1 else ''}"
    elif days < 30:
        weeks = days // 7
        return f"in {weeks} week{'s' if weeks != 1 else ''}"
    elif days < 365:
        months = days // 30
        return f"in {months} month{'s' if months != 1 else ''}"
    else:
        years = days // 365
        return f"in {years} year{'s' if years != 1 else ''}"


def format_duration(seconds: Union[int, float]) -> str:
    """
    Format duration in seconds to human-readable format.

    Args:
        seconds: Duration in seconds

    Returns:
        Human-readable duration string

    Example:
        >>> format_duration(125)
        '2m 5s'
        >>>
        >>> format_duration(3665)
        '1h 1m 5s'
        >>>
        >>> format_duration(45)
        '45s'
    """
    seconds = int(seconds)

    if seconds < 60:
        return f"{seconds}s"

    minutes = seconds // 60
    remaining_seconds = seconds % 60

    if minutes < 60:
        if remaining_seconds > 0:
            return f"{minutes}m {remaining_seconds}s"
        return f"{minutes}m"

    hours = minutes // 60
    remaining_minutes = minutes % 60

    parts = [f"{hours}h"]
    if remaining_minutes > 0:
        parts.append(f"{remaining_minutes}m")
    if remaining_seconds > 0:
        parts.append(f"{remaining_seconds}s")

    return " ".join(parts)


def is_recent(dt: datetime, hours: int = 24) -> bool:
    """
    Check if a datetime is within the last N hours.

    Args:
        dt: datetime to check
        hours: Number of hours to consider as "recent" (default: 24)

    Returns:
        True if datetime is within the last N hours

    Example:
        >>> from datetime import datetime, timedelta, timezone
        >>> now = datetime.now(timezone.utc)
        >>> recent = now - timedelta(hours=12)
        >>> old = now - timedelta(days=2)
        >>>
        >>> print(is_recent(recent))
        True
        >>> print(is_recent(old))
        False
    """
    now = datetime.now(timezone.utc)

    # Ensure both datetimes are timezone-aware
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    cutoff = now - timedelta(hours=hours)
    return dt >= cutoff


def get_date_range(days: int = 7) -> tuple[datetime, datetime]:
    """
    Get start and end datetimes for a date range.

    Args:
        days: Number of days in the range (default: 7)

    Returns:
        Tuple of (start_date, end_date) as timezone-aware datetimes

    Example:
        >>> start, end = get_date_range(7)
        >>> print(f"Last 7 days: {start} to {end}")
        >>>
        >>> # Get last 30 days
        >>> start, end = get_date_range(30)
    """
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)
    return start, end


def normalize_timestamp(timestamp: Union[str, int, float, datetime]) -> datetime:
    """
    Normalize various timestamp formats to timezone-aware datetime.

    Args:
        timestamp: String, Unix timestamp, or datetime object

    Returns:
        Timezone-aware datetime object

    Raises:
        ValueError: If timestamp format is not recognized

    Example:
        >>> # From ISO string
        >>> dt = normalize_timestamp("2025-01-15T14:30:00Z")
        >>>
        >>> # From Unix timestamp
        >>> dt = normalize_timestamp(1705329000)
        >>>
        >>> # From datetime
        >>> from datetime import datetime
        >>> dt = normalize_timestamp(datetime.now())
    """
    if isinstance(timestamp, datetime):
        # Ensure timezone-aware
        if timestamp.tzinfo is None:
            return timestamp.replace(tzinfo=timezone.utc)
        return timestamp

    if isinstance(timestamp, str):
        # Parse ISO 8601
        result = parse_iso_timestamp(timestamp)
        if result is None:
            raise ValueError(f"Unable to parse timestamp: {timestamp}")
        return result

    if isinstance(timestamp, (int, float)):
        # Unix timestamp
        return unix_to_datetime(timestamp)

    raise ValueError(f"Unsupported timestamp type: {type(timestamp)}")


# Example usage and testing
if __name__ == "__main__":
    print("Date and Time Utilities Examples")
    print("=" * 60)

    # Example 1: Format dates
    print("\n1. Formatting Dates")
    print("-" * 60)
    print(f"ISO 8601: {format_date('2025-01-15T14:30:00Z')}")
    print(f"RFC 3339: {format_date('2025-01-15T14:30:00+00:00')}")
    print(f"Custom format: {format_date('2025-01-15T14:30:00Z', '%Y-%m-%d')}")

    # Example 2: Time ago
    print("\n2. Relative Time (Time Ago)")
    print("-" * 60)
    now = datetime.now(timezone.utc)
    examples = [
        (now - timedelta(minutes=5), "5 minutes ago"),
        (now - timedelta(hours=2), "2 hours ago"),
        (now - timedelta(days=1), "1 day ago"),
        (now - timedelta(weeks=2), "2 weeks ago"),
    ]
    for dt, expected in examples:
        result = time_ago(dt)
        print(f"{expected}: {result}")

    # Example 3: Time until
    print("\n3. Future Time (Time Until)")
    print("-" * 60)
    future_examples = [
        (now + timedelta(hours=3), "in 3 hours"),
        (now + timedelta(days=5), "in 5 days"),
    ]
    for dt, expected in future_examples:
        result = time_until(dt)
        print(f"{expected}: {result}")

    # Example 4: Duration formatting
    print("\n4. Duration Formatting")
    print("-" * 60)
    durations = [45, 125, 3665, 7325]
    for seconds in durations:
        print(f"{seconds}s = {format_duration(seconds)}")

    # Example 5: Unix timestamps
    print("\n5. Unix Timestamp Conversion")
    print("-" * 60)
    unix_ts = 1705329000
    dt = unix_to_datetime(unix_ts)
    print(f"Unix {unix_ts} = {dt}")
    print(f"Back to Unix: {datetime_to_unix(dt)}")

    # Example 6: Recent check
    print("\n6. Checking if Recent")
    print("-" * 60)
    recent = now - timedelta(hours=12)
    old = now - timedelta(days=3)
    print(f"12 hours ago is recent (24h): {is_recent(recent)}")
    print(f"3 days ago is recent (24h): {is_recent(old)}")

    # Example 7: Date ranges
    print("\n7. Date Ranges")
    print("-" * 60)
    start, end = get_date_range(7)
    print(f"Last 7 days: {start.date()} to {end.date()}")

    # Example 8: Normalize timestamps
    print("\n8. Normalizing Various Timestamp Formats")
    print("-" * 60)
    formats = [
        "2025-01-15T14:30:00Z",
        1705329000,
        datetime.now()
    ]
    for fmt in formats:
        normalized = normalize_timestamp(fmt)
        print(f"{fmt} -> {normalized}")

    print("\n" + "=" * 60)
    print("All examples completed!")

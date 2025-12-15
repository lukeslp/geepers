"""
Retry Decorator with Exponential Backoff

Description: A production-ready retry decorator that handles transient failures with exponential backoff,
configurable exception handling, and comprehensive logging. Essential for robust API integrations and
network operations.

Use Cases:
- API calls that may fail due to rate limiting or network issues
- Database operations with connection failures
- External service integrations (OpenAI, SerpAPI, etc.)
- File operations with lock contention
- Any operation that might transiently fail

Dependencies:
- functools (stdlib)
- time (stdlib)
- logging (stdlib)
- typing (stdlib)

Notes:
- Exponential backoff prevents overwhelming failing services
- Configurable exception types allow selective retry logic
- Logs provide visibility into retry attempts
- Preserves function metadata with @wraps
- Thread-safe implementation

Related Snippets:
- geepers.utils.async_* - Async retry patterns
- geepers.utils.rate_limiter - Rate limiting for API calls

Source Attribution:
- Extracted from: /home/coolhand/SNIPPETS/utilities/retry_decorator.py
- Author: Luke Steuber
"""

import logging
import time
from functools import wraps
from typing import Callable, Tuple, Type, TypeVar, Any


logger = logging.getLogger(__name__)

T = TypeVar('T')


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Retry decorator with exponential backoff.

    Automatically retries a function when it raises specified exceptions,
    with exponentially increasing delays between attempts.

    Args:
        max_attempts: Maximum number of retry attempts (default: 3)
        delay: Initial delay between retries in seconds (default: 1.0)
        backoff: Multiplier for delay after each retry (default: 2.0)
        exceptions: Tuple of exception types to catch and retry (default: (Exception,))

    Returns:
        Decorated function that will retry on failure

    Raises:
        The last exception encountered after all retry attempts are exhausted

    Example:
        Basic usage with default settings:
        >>> @retry(max_attempts=3, delay=1.0)
        ... def api_call():
        ...     return requests.get("https://api.example.com/data")

        Custom exception handling:
        >>> @retry(
        ...     max_attempts=5,
        ...     delay=0.5,
        ...     backoff=1.5,
        ...     exceptions=(requests.RequestException, ConnectionError)
        ... )
        ... def fetch_data(url):
        ...     response = requests.get(url)
        ...     response.raise_for_status()
        ...     return response.json()

        Using with OpenAI API:
        >>> from openai import OpenAI, APIError, RateLimitError
        >>>
        >>> @retry(
        ...     max_attempts=3,
        ...     delay=2.0,
        ...     exceptions=(APIError, RateLimitError)
        ... )
        ... def generate_completion(prompt):
        ...     client = OpenAI()
        ...     return client.chat.completions.create(
        ...         model="gpt-4",
        ...         messages=[{"role": "user", "content": prompt}]
        ...     )
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            current_delay = delay
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(
                            f"{func.__name__} failed (attempt {attempt + 1}/{max_attempts}): {e}. "
                            f"Retrying in {current_delay}s..."
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(
                            f"{func.__name__} failed after {max_attempts} attempts: {e}"
                        )

            # This will always be set if we get here
            raise last_exception  # type: ignore

        return wrapper
    return decorator


def retry_with_jitter(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Retry decorator with exponential backoff and jitter.

    Similar to @retry but adds random jitter to prevent thundering herd problem
    when multiple clients retry simultaneously.

    Args:
        max_attempts: Maximum number of retry attempts
        base_delay: Base delay in seconds (will be randomized)
        max_delay: Maximum delay between retries
        exceptions: Tuple of exception types to catch and retry

    Returns:
        Decorated function that will retry on failure with jitter

    Example:
        >>> import random
        >>>
        >>> @retry_with_jitter(max_attempts=5, base_delay=1.0, max_delay=30.0)
        ... def call_rate_limited_api():
        ...     # API call that might hit rate limits
        ...     return requests.get("https://api.example.com/limited")
    """
    import random

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        # Calculate delay with exponential backoff and jitter
                        delay = min(base_delay * (2 ** attempt), max_delay)
                        jittered_delay = delay * (0.5 + random.random())

                        logger.warning(
                            f"{func.__name__} failed (attempt {attempt + 1}/{max_attempts}): {e}. "
                            f"Retrying in {jittered_delay:.2f}s..."
                        )
                        time.sleep(jittered_delay)
                    else:
                        logger.error(
                            f"{func.__name__} failed after {max_attempts} attempts: {e}"
                        )

            raise last_exception  # type: ignore

        return wrapper
    return decorator


__all__ = [
    'retry',
    'retry_with_jitter',
]

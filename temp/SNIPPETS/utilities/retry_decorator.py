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
- /home/coolhand/SNIPPETS/async-patterns/ - Async retry patterns
- /home/coolhand/SNIPPETS/error-handling/ - Error handling strategies

Source Attribution:
- Extracted from: /home/coolhand/shared/utils/__init__.py
- Related patterns: /home/coolhand/projects/swarm/core/
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


# Example usage and testing
if __name__ == "__main__":
    import random

    # Configure logging for demo
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    print("Example 1: Retry with exponential backoff")
    print("-" * 60)

    @retry(max_attempts=3, delay=0.5, backoff=2.0)
    def flaky_api_call(fail_count: int = 2):
        """Simulates an API call that fails a few times then succeeds."""
        if not hasattr(flaky_api_call, 'attempts'):
            flaky_api_call.attempts = 0

        flaky_api_call.attempts += 1

        if flaky_api_call.attempts <= fail_count:
            raise ConnectionError(f"Connection failed (attempt {flaky_api_call.attempts})")

        return {"status": "success", "data": "Important data"}

    try:
        result = flaky_api_call(fail_count=2)
        print(f"Success: {result}")
        flaky_api_call.attempts = 0  # Reset for next example
    except Exception as e:
        print(f"Failed: {e}")

    print("\n" + "=" * 60)
    print("Example 2: Retry with custom exceptions")
    print("-" * 60)

    class RateLimitError(Exception):
        pass

    @retry(
        max_attempts=4,
        delay=0.3,
        exceptions=(RateLimitError, ValueError)
    )
    def rate_limited_call():
        """Simulates a rate-limited API."""
        if not hasattr(rate_limited_call, 'calls'):
            rate_limited_call.calls = 0

        rate_limited_call.calls += 1

        if rate_limited_call.calls < 3:
            raise RateLimitError("Rate limit exceeded")

        return {"tokens_remaining": 100}

    try:
        result = rate_limited_call()
        print(f"Success: {result}")
        rate_limited_call.calls = 0
    except Exception as e:
        print(f"Failed: {e}")

    print("\n" + "=" * 60)
    print("Example 3: Retry with jitter (prevents thundering herd)")
    print("-" * 60)

    @retry_with_jitter(max_attempts=3, base_delay=0.2, max_delay=5.0)
    def api_with_jitter():
        """Simulates API with randomized retry delays."""
        if not hasattr(api_with_jitter, 'attempt'):
            api_with_jitter.attempt = 0

        api_with_jitter.attempt += 1

        if api_with_jitter.attempt < 2:
            raise ConnectionError("Temporary connection issue")

        return {"jittered": True}

    try:
        result = api_with_jitter()
        print(f"Success: {result}")
        api_with_jitter.attempt = 0
    except Exception as e:
        print(f"Failed: {e}")

    print("\n" + "=" * 60)
    print("All examples completed!")

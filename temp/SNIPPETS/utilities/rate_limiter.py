"""
Rate Limiting Utilities

Description: Production-ready rate limiting implementations for both synchronous and asynchronous code.
Includes semaphore-based concurrency control, token bucket algorithm, and decorator-based rate limiting
to prevent API throttling and service overload.

Use Cases:
- Preventing API rate limit errors (OpenAI, SerpAPI, etc.)
- Controlling concurrent requests to external services
- Implementing fair-use policies for multi-user systems
- Graceful degradation under load
- Protecting downstream services from overload

Dependencies:
- asyncio (stdlib)
- threading (stdlib)
- time (stdlib)
- typing (stdlib)
- functools (stdlib)

Notes:
- Async semaphore-based limiter for concurrent operations
- Token bucket algorithm for request rate limiting
- Per-provider rate limit configuration
- Thread-safe implementations
- Minimal performance overhead

Related Snippets:
- /home/coolhand/SNIPPETS/utilities/retry_decorator.py - Retry with rate limiting
- /home/coolhand/SNIPPETS/async-patterns/ - Async concurrency patterns
- /home/coolhand/SNIPPETS/utilities/redis_cache_manager.py - Distributed rate limiting

Source Attribution:
- Extracted from: /home/coolhand/projects/swarm/SUGGESTIONS.md
- Related patterns: /home/coolhand/enterprise_orchestration/core/
- Author: Luke Steuber
"""

import asyncio
import time
import threading
from collections import deque
from contextlib import asynccontextmanager, contextmanager
from functools import wraps
from typing import Callable, Optional, TypeVar, Any
import logging


logger = logging.getLogger(__name__)

T = TypeVar('T')


class AsyncRateLimiter:
    """
    Asynchronous rate limiter using semaphore for concurrency control.

    Controls the number of concurrent operations and adds configurable delay
    between operations to prevent overwhelming external services.

    Attributes:
        max_concurrent: Maximum concurrent operations allowed
        delay: Minimum delay between operations in seconds
        semaphore: Internal asyncio.Semaphore for concurrency control
    """

    def __init__(self, max_concurrent: int = 5, delay: float = 0.2):
        """
        Initialize async rate limiter.

        Args:
            max_concurrent: Maximum concurrent operations (default: 5)
            delay: Delay between operations in seconds (default: 0.2)

        Example:
            >>> limiter = AsyncRateLimiter(max_concurrent=3, delay=0.5)
        """
        self.max_concurrent = max_concurrent
        self.delay = delay
        self.semaphore = asyncio.Semaphore(max_concurrent)

    @asynccontextmanager
    async def acquire(self):
        """
        Acquire rate limiter (async context manager).

        Use with 'async with' to automatically manage semaphore and delay.

        Example:
            >>> limiter = AsyncRateLimiter(max_concurrent=3)
            >>> async with limiter.acquire():
            ...     result = await call_external_api()
        """
        async with self.semaphore:
            try:
                yield
            finally:
                await asyncio.sleep(self.delay)


class TokenBucketRateLimiter:
    """
    Token bucket rate limiter for controlling request rates.

    Allows bursts of requests up to bucket capacity while maintaining
    a steady average rate. Thread-safe for synchronous code.

    Attributes:
        rate: Tokens added per second (requests/second)
        capacity: Maximum bucket capacity (max burst size)
        tokens: Current number of available tokens
    """

    def __init__(self, rate: float, capacity: int):
        """
        Initialize token bucket rate limiter.

        Args:
            rate: Tokens added per second (requests/second)
            capacity: Maximum bucket capacity (max burst size)

        Example:
            >>> # Allow 10 requests/second with burst of 20
            >>> limiter = TokenBucketRateLimiter(rate=10, capacity=20)
        """
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last_update = time.time()
        self.lock = threading.Lock()

    def _add_tokens(self):
        """Add tokens based on elapsed time since last update."""
        now = time.time()
        elapsed = now - self.last_update
        new_tokens = elapsed * self.rate

        self.tokens = min(self.capacity, self.tokens + new_tokens)
        self.last_update = now

    def acquire(self, tokens: int = 1, blocking: bool = True) -> bool:
        """
        Acquire tokens from the bucket.

        Args:
            tokens: Number of tokens to acquire (default: 1)
            blocking: If True, wait until tokens available (default: True)

        Returns:
            True if tokens acquired, False if not available and non-blocking

        Example:
            >>> limiter = TokenBucketRateLimiter(rate=5, capacity=10)
            >>> if limiter.acquire():
            ...     make_api_call()
        """
        with self.lock:
            self._add_tokens()

            if self.tokens >= tokens:
                self.tokens -= tokens
                return True

            if not blocking:
                return False

        # Blocking mode: wait for tokens
        wait_time = (tokens - self.tokens) / self.rate
        time.sleep(wait_time)

        with self.lock:
            self._add_tokens()
            self.tokens -= tokens
            return True

    @contextmanager
    def limit(self, tokens: int = 1):
        """
        Context manager for rate limiting.

        Args:
            tokens: Number of tokens to acquire (default: 1)

        Example:
            >>> limiter = TokenBucketRateLimiter(rate=10, capacity=20)
            >>> with limiter.limit():
            ...     response = requests.get("https://api.example.com")
        """
        self.acquire(tokens)
        yield


class SlidingWindowRateLimiter:
    """
    Sliding window rate limiter for precise rate control.

    Tracks request timestamps in a sliding window to enforce
    exact rate limits. More precise than token bucket but with
    higher memory overhead.

    Attributes:
        max_requests: Maximum requests allowed in window
        window_seconds: Time window in seconds
        requests: Deque of request timestamps
    """

    def __init__(self, max_requests: int, window_seconds: float):
        """
        Initialize sliding window rate limiter.

        Args:
            max_requests: Maximum requests in window
            window_seconds: Window size in seconds

        Example:
            >>> # Allow 100 requests per 60 seconds
            >>> limiter = SlidingWindowRateLimiter(100, 60)
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: deque = deque()
        self.lock = threading.Lock()

    def _clean_old_requests(self, now: float):
        """Remove requests outside the current window."""
        cutoff = now - self.window_seconds
        while self.requests and self.requests[0] < cutoff:
            self.requests.popleft()

    def acquire(self, blocking: bool = True) -> bool:
        """
        Acquire permission to make a request.

        Args:
            blocking: If True, wait until request allowed

        Returns:
            True if request allowed, False otherwise

        Example:
            >>> limiter = SlidingWindowRateLimiter(10, 60)
            >>> if limiter.acquire():
            ...     make_api_call()
        """
        with self.lock:
            now = time.time()
            self._clean_old_requests(now)

            if len(self.requests) < self.max_requests:
                self.requests.append(now)
                return True

            if not blocking:
                return False

            # Wait until oldest request expires
            wait_time = self.requests[0] + self.window_seconds - now

        if wait_time > 0:
            time.sleep(wait_time)

        with self.lock:
            now = time.time()
            self._clean_old_requests(now)
            self.requests.append(now)
            return True


def async_rate_limit(max_concurrent: int = 5, delay: float = 0.2):
    """
    Decorator for async rate limiting.

    Args:
        max_concurrent: Maximum concurrent calls
        delay: Delay between calls in seconds

    Returns:
        Decorated async function with rate limiting

    Example:
        >>> @async_rate_limit(max_concurrent=3, delay=0.5)
        ... async def fetch_data(url: str):
        ...     async with aiohttp.ClientSession() as session:
        ...         async with session.get(url) as response:
        ...             return await response.json()
    """
    limiter = AsyncRateLimiter(max_concurrent, delay)

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            async with limiter.acquire():
                return await func(*args, **kwargs)
        return wrapper
    return decorator


def rate_limit(rate: float, capacity: int):
    """
    Decorator for synchronous rate limiting using token bucket.

    Args:
        rate: Requests per second
        capacity: Burst capacity

    Returns:
        Decorated function with rate limiting

    Example:
        >>> @rate_limit(rate=10, capacity=20)
        ... def call_api(endpoint: str):
        ...     return requests.get(f"https://api.example.com/{endpoint}")
        >>>
        >>> # Automatically rate limited
        >>> result = call_api("users/123")
    """
    limiter = TokenBucketRateLimiter(rate, capacity)

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs):
            with limiter.limit():
                return func(*args, **kwargs)
        return wrapper
    return decorator


class MultiProviderRateLimiter:
    """
    Rate limiter with per-provider configurations.

    Manages different rate limits for different service providers
    (OpenAI, Anthropic, SerpAPI, etc.).

    Example:
        >>> limiter = MultiProviderRateLimiter({
        ...     "openai": {"rate": 50, "capacity": 100},
        ...     "anthropic": {"rate": 40, "capacity": 80},
        ...     "serpapi": {"rate": 10, "capacity": 20}
        ... })
        >>>
        >>> with limiter.limit("openai"):
        ...     response = openai_client.chat.completions.create(...)
    """

    def __init__(self, provider_configs: dict[str, dict[str, int]]):
        """
        Initialize multi-provider rate limiter.

        Args:
            provider_configs: Dict mapping provider name to rate config
                             Each config should have 'rate' and 'capacity' keys

        Example:
            >>> configs = {
            ...     "openai": {"rate": 50, "capacity": 100},
            ...     "serpapi": {"rate": 10, "capacity": 20}
            ... }
            >>> limiter = MultiProviderRateLimiter(configs)
        """
        self.limiters = {
            provider: TokenBucketRateLimiter(
                rate=config["rate"],
                capacity=config["capacity"]
            )
            for provider, config in provider_configs.items()
        }

    def limit(self, provider: str, tokens: int = 1):
        """
        Get rate limiter for specific provider.

        Args:
            provider: Provider name
            tokens: Number of tokens to acquire

        Returns:
            Context manager for rate limiting

        Example:
            >>> limiter = MultiProviderRateLimiter({
            ...     "openai": {"rate": 50, "capacity": 100}
            ... })
            >>> with limiter.limit("openai"):
            ...     call_openai_api()
        """
        if provider not in self.limiters:
            raise ValueError(f"Unknown provider: {provider}")

        return self.limiters[provider].limit(tokens)


# Example usage and testing
if __name__ == "__main__":
    import asyncio
    import random

    print("Rate Limiting Utilities Examples")
    print("=" * 60)

    # Example 1: Async rate limiter
    print("\n1. Async Rate Limiter")
    print("-" * 60)

    async def example_async_rate_limiter():
        limiter = AsyncRateLimiter(max_concurrent=3, delay=0.3)

        async def fetch_data(item_id: int):
            async with limiter.acquire():
                print(f"  Fetching item {item_id}...")
                await asyncio.sleep(0.1)  # Simulate API call
                return f"Data {item_id}"

        # Run multiple concurrent requests
        tasks = [fetch_data(i) for i in range(10)]
        results = await asyncio.gather(*tasks)
        print(f"Completed {len(results)} requests")

    asyncio.run(example_async_rate_limiter())

    # Example 2: Token bucket rate limiter
    print("\n2. Token Bucket Rate Limiter")
    print("-" * 60)

    limiter = TokenBucketRateLimiter(rate=5, capacity=10)

    for i in range(8):
        with limiter.limit():
            print(f"  Request {i+1} processed")

    # Example 3: Sliding window rate limiter
    print("\n3. Sliding Window Rate Limiter")
    print("-" * 60)

    window_limiter = SlidingWindowRateLimiter(max_requests=3, window_seconds=2)

    for i in range(5):
        if window_limiter.acquire(blocking=False):
            print(f"  Request {i+1} allowed")
        else:
            print(f"  Request {i+1} blocked (waiting...)")
            window_limiter.acquire(blocking=True)
            print(f"  Request {i+1} now allowed")

    # Example 4: Decorator usage
    print("\n4. Rate Limit Decorator")
    print("-" * 60)

    @rate_limit(rate=2, capacity=5)
    def api_call(endpoint: str):
        print(f"  Calling {endpoint}")
        return f"Response from {endpoint}"

    for i in range(4):
        result = api_call(f"/api/endpoint{i}")

    # Example 5: Multi-provider rate limiter
    print("\n5. Multi-Provider Rate Limiter")
    print("-" * 60)

    multi_limiter = MultiProviderRateLimiter({
        "openai": {"rate": 10, "capacity": 20},
        "serpapi": {"rate": 5, "capacity": 10}
    })

    for i in range(3):
        with multi_limiter.limit("openai"):
            print(f"  OpenAI request {i+1}")

    for i in range(3):
        with multi_limiter.limit("serpapi"):
            print(f"  SerpAPI request {i+1}")

    print("\n" + "=" * 60)
    print("All examples completed!")

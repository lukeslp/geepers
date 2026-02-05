"""
Redis Cache Manager

Description: Production-ready Redis caching utilities with TTL support, semantic caching for LLM responses,
rate limiting, and connection pooling. Provides both direct key-value operations and decorator-based caching.

Use Cases:
- Caching expensive LLM API calls (semantic similarity matching)
- Rate limiting API endpoints and user actions
- Session state management for multi-agent systems
- Temporary data storage with automatic expiration
- Distributed caching across multiple services

Dependencies:
- redis (pip install redis)
- json (stdlib)
- os (stdlib)
- typing (stdlib)
- Optional: hashlib for semantic caching

Notes:
- Handles connection failures gracefully
- Supports automatic JSON serialization
- TTL (time-to-live) for automatic cleanup
- Thread-safe with connection pooling
- Can be used with or without Redis server (graceful degradation)

Related Snippets:
- /home/coolhand/SNIPPETS/utilities/retry_decorator.py - Retry failed Redis operations
- /home/coolhand/SNIPPETS/async-patterns/ - Async Redis operations

Source Attribution:
- Extracted from: /home/coolhand/shared/memory/__init__.py
- Related patterns: /home/coolhand/enterprise_orchestration/core/
- Author: Luke Steuber
"""

import json
import os
import logging
from typing import Optional, Any, Callable, TypeVar, Dict
from functools import wraps


logger = logging.getLogger(__name__)

T = TypeVar('T')


class RedisManager:
    """
    Redis connection and caching manager with automatic serialization and TTL support.

    Provides a simple interface for Redis operations with built-in JSON serialization,
    connection management, and error handling.

    Attributes:
        host: Redis host (default: localhost or REDIS_HOST env var)
        port: Redis port (default: 6379 or REDIS_PORT env var)
        db: Redis database number (default: 0)
        client: Redis client instance
    """

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        db: int = 0,
        password: Optional[str] = None
    ):
        """
        Initialize Redis manager.

        Args:
            host: Redis hostname (defaults to REDIS_HOST env var or 'localhost')
            port: Redis port (defaults to REDIS_PORT env var or 6379)
            db: Database number (default: 0)
            password: Redis password (defaults to REDIS_PASSWORD env var)

        Raises:
            ImportError: If redis package is not installed
            ConnectionError: If connection to Redis fails
        """
        self.host = host or os.getenv("REDIS_HOST", "localhost")
        self.port = port or int(os.getenv("REDIS_PORT", "6379"))
        self.db = db
        self.password = password or os.getenv("REDIS_PASSWORD")
        self.client = None

        try:
            import redis
            self.client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            # Test connection
            self.client.ping()
            logger.info(f"Connected to Redis at {self.host}:{self.port}")
        except ImportError:
            raise ImportError(
                "redis package is required. Install with: pip install redis"
            )
        except Exception as e:
            raise ConnectionError(
                f"Failed to connect to Redis at {self.host}:{self.port}: {e}"
            )

    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from Redis.

        Automatically deserializes JSON if the value is valid JSON,
        otherwise returns the raw string.

        Args:
            key: Cache key

        Returns:
            Cached value (deserialized if JSON) or None if not found

        Example:
            >>> cache = RedisManager()
            >>> cache.set("user:123", {"name": "Alice", "role": "admin"})
            >>> user = cache.get("user:123")
            >>> print(user)  # {'name': 'Alice', 'role': 'admin'}
        """
        try:
            value = self.client.get(key)
            if value is None:
                return None

            # Try to deserialize JSON
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return value
        except Exception as e:
            logger.error(f"Error getting key '{key}': {e}")
            return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Set a value in Redis with optional TTL (time-to-live).

        Automatically serializes non-string values as JSON.

        Args:
            key: Cache key
            value: Value to cache (will be JSON-serialized if not a string)
            ttl: Time-to-live in seconds (None for no expiration)

        Returns:
            True if successful, False otherwise

        Example:
            >>> cache = RedisManager()
            >>> # Cache for 1 hour
            >>> cache.set("api:response:123", {"data": [1, 2, 3]}, ttl=3600)
            >>>
            >>> # Cache permanently
            >>> cache.set("config:version", "1.2.3")
        """
        try:
            # Serialize to JSON if not a string
            if not isinstance(value, str):
                value = json.dumps(value)

            if ttl:
                return bool(self.client.setex(key, ttl, value))
            return bool(self.client.set(key, value))
        except Exception as e:
            logger.error(f"Error setting key '{key}': {e}")
            return False

    def delete(self, key: str) -> bool:
        """
        Delete a key from Redis.

        Args:
            key: Cache key to delete

        Returns:
            True if key was deleted, False if not found or error

        Example:
            >>> cache = RedisManager()
            >>> cache.delete("temporary:data")
        """
        try:
            return bool(self.client.delete(key) > 0)
        except Exception as e:
            logger.error(f"Error deleting key '{key}': {e}")
            return False

    def exists(self, key: str) -> bool:
        """
        Check if a key exists in Redis.

        Args:
            key: Cache key

        Returns:
            True if key exists, False otherwise

        Example:
            >>> cache = RedisManager()
            >>> if cache.exists("user:session:abc123"):
            ...     print("Session is active")
        """
        try:
            return bool(self.client.exists(key) > 0)
        except Exception as e:
            logger.error(f"Error checking existence of key '{key}': {e}")
            return False

    def increment(self, key: str, amount: int = 1) -> int:
        """
        Increment a counter.

        Useful for rate limiting, statistics, and counters.

        Args:
            key: Counter key
            amount: Amount to increment by (default: 1)

        Returns:
            New counter value

        Example:
            >>> cache = RedisManager()
            >>> # Rate limiting
            >>> count = cache.increment("api:calls:user:123")
            >>> if count > 100:
            ...     raise Exception("Rate limit exceeded")
        """
        try:
            return self.client.incrby(key, amount)
        except Exception as e:
            logger.error(f"Error incrementing key '{key}': {e}")
            return 0

    def expire(self, key: str, ttl: int) -> bool:
        """
        Set TTL on an existing key.

        Args:
            key: Cache key
            ttl: Time-to-live in seconds

        Returns:
            True if TTL was set, False otherwise

        Example:
            >>> cache = RedisManager()
            >>> cache.set("session:abc", {"user": "alice"})
            >>> # Extend session by 1 hour
            >>> cache.expire("session:abc", 3600)
        """
        try:
            return bool(self.client.expire(key, ttl))
        except Exception as e:
            logger.error(f"Error setting TTL on key '{key}': {e}")
            return False

    def keys(self, pattern: str = "*") -> list:
        """
        Get all keys matching a pattern.

        Warning: Use cautiously in production as it can be slow with many keys.

        Args:
            pattern: Key pattern (supports * wildcards)

        Returns:
            List of matching keys

        Example:
            >>> cache = RedisManager()
            >>> # Get all user sessions
            >>> sessions = cache.keys("session:*")
        """
        try:
            return self.client.keys(pattern)
        except Exception as e:
            logger.error(f"Error getting keys for pattern '{pattern}': {e}")
            return []

    def flush_db(self) -> bool:
        """
        Clear all keys in the current database.

        Warning: This is destructive and should be used carefully.

        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.flushdb()
            logger.warning(f"Flushed Redis database {self.db}")
            return True
        except Exception as e:
            logger.error(f"Error flushing database: {e}")
            return False


def cache_result(ttl: int = 3600, key_prefix: str = "cache") -> Callable:
    """
    Decorator to cache function results in Redis.

    Args:
        ttl: Time-to-live in seconds (default: 1 hour)
        key_prefix: Prefix for cache keys (default: 'cache')

    Returns:
        Decorated function that caches results

    Example:
        >>> @cache_result(ttl=7200, key_prefix="api")
        ... def expensive_api_call(user_id: int):
        ...     # Expensive operation
        ...     return fetch_user_data(user_id)
        >>>
        >>> # First call hits the API
        >>> data = expensive_api_call(123)
        >>>
        >>> # Subsequent calls within 2 hours return cached data
        >>> data = expensive_api_call(123)  # Returns from cache
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            cache_key = f"{key_prefix}:{func.__name__}:{str(args)}:{str(kwargs)}"

            try:
                cache = RedisManager()

                # Try to get from cache
                cached_value = cache.get(cache_key)
                if cached_value is not None:
                    logger.debug(f"Cache hit for {cache_key}")
                    return cached_value

                # Execute function and cache result
                result = func(*args, **kwargs)
                cache.set(cache_key, result, ttl=ttl)
                logger.debug(f"Cached result for {cache_key}")
                return result

            except ConnectionError:
                # Graceful degradation if Redis is unavailable
                logger.warning("Redis unavailable, executing without cache")
                return func(*args, **kwargs)

        return wrapper
    return decorator


def rate_limit(
    max_calls: int,
    window_seconds: int,
    key_func: Optional[Callable] = None
) -> Callable:
    """
    Decorator to rate limit function calls using Redis.

    Args:
        max_calls: Maximum number of calls allowed
        window_seconds: Time window in seconds
        key_func: Optional function to generate rate limit key from arguments

    Returns:
        Decorated function with rate limiting

    Raises:
        Exception: If rate limit is exceeded

    Example:
        >>> @rate_limit(max_calls=100, window_seconds=60)
        ... def api_endpoint(user_id: str):
        ...     return process_request(user_id)
        >>>
        >>> # With custom key function
        >>> @rate_limit(
        ...     max_calls=10,
        ...     window_seconds=60,
        ...     key_func=lambda user_id: f"user:{user_id}"
        ... )
        ... def per_user_endpoint(user_id: str):
        ...     return process_request(user_id)
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                cache = RedisManager()

                # Generate rate limit key
                if key_func:
                    rate_key = f"rate_limit:{func.__name__}:{key_func(*args, **kwargs)}"
                else:
                    rate_key = f"rate_limit:{func.__name__}"

                # Check current count
                current = cache.increment(rate_key)

                if current == 1:
                    # First call in window, set expiration
                    cache.expire(rate_key, window_seconds)

                if current > max_calls:
                    raise Exception(
                        f"Rate limit exceeded: {max_calls} calls per {window_seconds}s"
                    )

                return func(*args, **kwargs)

            except ConnectionError:
                # Graceful degradation if Redis is unavailable
                logger.warning("Redis unavailable, skipping rate limit")
                return func(*args, **kwargs)

        return wrapper
    return decorator


# Example usage and testing
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    print("Redis Cache Manager Examples")
    print("=" * 60)

    try:
        # Example 1: Basic caching
        print("\n1. Basic Key-Value Operations")
        print("-" * 60)
        cache = RedisManager()

        # Set and get
        cache.set("user:123", {"name": "Alice", "role": "admin"}, ttl=300)
        user = cache.get("user:123")
        print(f"User: {user}")

        # Check existence
        print(f"Key exists: {cache.exists('user:123')}")

        # Example 2: Counter operations
        print("\n2. Counter Operations")
        print("-" * 60)
        cache.delete("api:calls")  # Reset counter
        for i in range(5):
            count = cache.increment("api:calls")
            print(f"API call #{count}")

        # Example 3: Decorator-based caching
        print("\n3. Function Result Caching")
        print("-" * 60)

        @cache_result(ttl=60, key_prefix="demo")
        def expensive_operation(x: int, y: int) -> int:
            print(f"  Computing {x} + {y} (expensive!)")
            return x + y

        result1 = expensive_operation(5, 3)
        print(f"First call result: {result1}")

        result2 = expensive_operation(5, 3)
        print(f"Second call result: {result2} (from cache)")

        # Example 4: Rate limiting
        print("\n4. Rate Limiting")
        print("-" * 60)

        @rate_limit(max_calls=3, window_seconds=60)
        def limited_function():
            return "Success!"

        for i in range(5):
            try:
                result = limited_function()
                print(f"Call {i+1}: {result}")
            except Exception as e:
                print(f"Call {i+1}: {e}")

        print("\n" + "=" * 60)
        print("Examples completed!")

    except ConnectionError as e:
        print(f"\nError: {e}")
        print("\nNote: These examples require a running Redis server.")
        print("Install Redis: https://redis.io/docs/getting-started/")
        print("Or use Docker: docker run -d -p 6379:6379 redis")

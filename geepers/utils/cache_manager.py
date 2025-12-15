"""
Cache Manager with Redis and In-Memory Fallback

Description: Production-ready cache manager that uses Redis when available
and gracefully falls back to in-memory dict. Includes TTL support, statistics
tracking, and automatic key generation.

Use Cases:
- LLM response caching to reduce API costs
- API rate limiting
- Session storage
- Expensive computation caching
- Multi-instance cache sharing (Redis) with local fallback

Dependencies:
- redis (optional)

Notes:
- Automatically tests Redis connection on init
- Falls back to in-memory dict if Redis unavailable
- In-memory cache respects TTL via expiration timestamps
- Statistics tracked for cache hit rate analysis
- SHA256 hash for compact cache keys

Related Snippets:
- geepers.utils.rate_limiter - Rate limiting
- geepers.utils.retry_decorator - Retry logic

Source Attribution:
- Extracted from: /home/coolhand/SNIPPETS/utilities/cache_manager_redis_fallback.py
- Author: Luke Steuber
"""

import hashlib
import json
import logging
from typing import Optional, Any, Dict
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CacheManager:
    """
    Manages caching with Redis primary and in-memory fallback.

    Example:
        cache = CacheManager(use_redis=True)

        # Cache a value
        cache.set("provider", "model", {"messages": [...]}, {"response": "..."}, ttl=3600)

        # Retrieve cached value
        cached = cache.get("provider", "model", {"messages": [...]})
        if cached:
            print("Cache hit!")

        # View statistics
        stats = cache.get_stats()
        print(f"Hit rate: {stats['hit_rate']}")

        # Clear cache
        cache.clear()
    """

    def __init__(
        self,
        use_redis: bool = True,
        redis_host: str = "localhost",
        redis_port: int = 6379,
        key_prefix: str = "app"
    ):
        """
        Initialize cache manager.

        Args:
            use_redis: Whether to attempt Redis connection
            redis_host: Redis server host
            redis_port: Redis server port
            key_prefix: Prefix for all cache keys (namespace)
        """
        self.use_redis = use_redis
        self.redis_client = None
        self.memory_cache: Dict[str, tuple] = {}  # {key: (data, expires_at)}
        self.cache_hits = 0
        self.cache_misses = 0
        self.key_prefix = key_prefix

        if use_redis:
            try:
                import redis
                self.redis_client = redis.Redis(
                    host=redis_host,
                    port=redis_port,
                    db=0,
                    decode_responses=True,
                    socket_connect_timeout=2,
                    socket_timeout=2
                )
                # Test connection
                self.redis_client.ping()
                logger.info(f"Redis cache connected at {redis_host}:{redis_port}")
            except ImportError:
                logger.warning("Redis package not installed, using in-memory cache")
                self.redis_client = None
                self.use_redis = False
            except Exception as e:
                logger.warning(f"Redis not available, using in-memory cache: {e}")
                self.redis_client = None
                self.use_redis = False

    def _generate_cache_key(self, namespace: str, identifier: str, data: Any) -> str:
        """
        Generate deterministic cache key.

        Args:
            namespace: Cache namespace (e.g., provider name)
            identifier: Secondary identifier (e.g., model name)
            data: Data to include in key (will be JSON-serialized)

        Returns:
            Cache key with format: prefix:namespace:hash
        """
        # Create deterministic string from data
        cache_data = {
            "namespace": namespace,
            "identifier": identifier,
            "data": data
        }
        cache_string = json.dumps(cache_data, sort_keys=True)

        # Hash for compact key (16 chars from 64-char hex)
        key_hash = hashlib.sha256(cache_string.encode()).hexdigest()[:16]

        return f"{self.key_prefix}:cache:{namespace}:{key_hash}"

    def get(self, namespace: str, identifier: str, data: Any) -> Optional[Any]:
        """
        Retrieve cached value.

        Args:
            namespace: Cache namespace
            identifier: Secondary identifier
            data: Data used to generate cache key

        Returns:
            Cached value or None if not found/expired
        """
        cache_key = self._generate_cache_key(namespace, identifier, data)

        try:
            if self.redis_client:
                # Try Redis
                cached = self.redis_client.get(cache_key)
                if cached:
                    self.cache_hits += 1
                    logger.debug(f"Cache HIT (Redis) for {namespace}/{identifier}")
                    return json.loads(cached)
            else:
                # Try in-memory cache
                if cache_key in self.memory_cache:
                    cached_data, expires_at = self.memory_cache[cache_key]

                    # Check expiration
                    if datetime.now() < expires_at:
                        self.cache_hits += 1
                        logger.debug(f"Cache HIT (memory) for {namespace}/{identifier}")
                        return cached_data
                    else:
                        # Expired, remove it
                        del self.memory_cache[cache_key]
                        logger.debug(f"Cache entry expired for {namespace}/{identifier}")

        except Exception as e:
            logger.warning(f"Cache get error: {e}")

        self.cache_misses += 1
        logger.debug(f"Cache MISS for {namespace}/{identifier}")
        return None

    def set(
        self,
        namespace: str,
        identifier: str,
        data: Any,
        value: Any,
        ttl: int = 3600
    ):
        """
        Cache a value.

        Args:
            namespace: Cache namespace
            identifier: Secondary identifier
            data: Data used to generate cache key
            value: Value to cache
            ttl: Time to live in seconds (default 1 hour)
        """
        cache_key = self._generate_cache_key(namespace, identifier, data)

        try:
            if self.redis_client:
                # Store in Redis with TTL
                self.redis_client.setex(
                    cache_key,
                    ttl,
                    json.dumps(value)
                )
                logger.debug(f"Cached in Redis: {namespace}/{identifier} (TTL: {ttl}s)")
            else:
                # Store in memory with expiration timestamp
                expires_at = datetime.now() + timedelta(seconds=ttl)
                self.memory_cache[cache_key] = (value, expires_at)
                logger.debug(f"Cached in memory: {namespace}/{identifier} (TTL: {ttl}s)")

        except Exception as e:
            logger.warning(f"Cache set error: {e}")

    def delete(self, namespace: str, identifier: str, data: Any):
        """Delete a specific cache entry"""
        cache_key = self._generate_cache_key(namespace, identifier, data)

        try:
            if self.redis_client:
                self.redis_client.delete(cache_key)
            else:
                self.memory_cache.pop(cache_key, None)
            logger.debug(f"Deleted cache entry: {namespace}/{identifier}")
        except Exception as e:
            logger.warning(f"Cache delete error: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dict with hits, misses, total, hit_rate, backend, etc.
        """
        total_requests = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total_requests * 100) if total_requests > 0 else 0

        stats = {
            "hits": self.cache_hits,
            "misses": self.cache_misses,
            "total": total_requests,
            "hit_rate": f"{hit_rate:.1f}%",
            "backend": "redis" if self.redis_client else "memory"
        }

        # Add memory cache size if using in-memory
        if not self.redis_client:
            stats["memory_cache_size"] = len(self.memory_cache)

            # Clean up expired entries and report
            now = datetime.now()
            expired_keys = [
                k for k, (_, exp) in self.memory_cache.items()
                if now >= exp
            ]
            for k in expired_keys:
                del self.memory_cache[k]

            if expired_keys:
                stats["expired_cleaned"] = len(expired_keys)

        return stats

    def clear(self):
        """Clear all cached data"""
        if self.redis_client:
            try:
                # Delete all keys with our prefix
                pattern = f"{self.key_prefix}:cache:*"
                keys = self.redis_client.keys(pattern)
                if keys:
                    self.redis_client.delete(*keys)
                    logger.info(f"Cleared {len(keys)} cache entries from Redis")
            except Exception as e:
                logger.warning(f"Cache clear error: {e}")
        else:
            self.memory_cache.clear()
            logger.info("Cleared memory cache")

        # Reset statistics
        self.cache_hits = 0
        self.cache_misses = 0


__all__ = [
    'CacheManager',
]

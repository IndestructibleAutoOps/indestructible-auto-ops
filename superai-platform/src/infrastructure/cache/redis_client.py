"""Redis client with connection pooling and utilities."""
from __future__ import annotations

import json
from typing import Any

import redis.asyncio as aioredis

from src.infrastructure.config import get_settings

_redis_pool: aioredis.Redis | None = None


async def get_redis() -> aioredis.Redis:
    global _redis_pool
    if _redis_pool is None:
        settings = get_settings()
        _redis_pool = aioredis.from_url(
            settings.redis.url,
            max_connections=settings.redis.max_connections,
            socket_timeout=settings.redis.socket_timeout,
            socket_connect_timeout=settings.redis.socket_connect_timeout,
            retry_on_timeout=settings.redis.retry_on_timeout,
            decode_responses=settings.redis.decode_responses,
        )
    return _redis_pool


class CacheService:
    """High-level caching service with serialization."""

    def __init__(self, prefix: str = "superai", default_ttl: int = 3600):
        self._prefix = prefix
        self._default_ttl = default_ttl

    def _key(self, key: str) -> str:
        return f"{self._prefix}:{key}"

    async def get(self, key: str) -> Any | None:
        redis = await get_redis()
        value = await redis.get(self._key(key))
        if value is None:
            return None
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value

    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        redis = await get_redis()
        serialized = json.dumps(value) if not isinstance(value, str) else value
        await redis.set(self._key(key), serialized, ex=ttl or self._default_ttl)

    async def delete(self, key: str) -> None:
        redis = await get_redis()
        await redis.delete(self._key(key))

    async def exists(self, key: str) -> bool:
        redis = await get_redis()
        return bool(await redis.exists(self._key(key)))

    async def increment(self, key: str, amount: int = 1) -> int:
        redis = await get_redis()
        return await redis.incrby(self._key(key), amount)

    async def get_or_set(self, key: str, factory: Any, ttl: int | None = None) -> Any:
        cached = await self.get(key)
        if cached is not None:
            return cached
        if callable(factory):
            value = await factory() if hasattr(factory, '__await__') or hasattr(factory, '__aiter__') else factory()
        else:
            value = factory
        await self.set(key, value, ttl)
        return value

    async def flush_pattern(self, pattern: str) -> int:
        redis = await get_redis()
        count = 0
        async for key in redis.scan_iter(match=self._key(pattern)):
            await redis.delete(key)
            count += 1
        return count
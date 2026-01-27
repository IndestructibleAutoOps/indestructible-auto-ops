"""
Cache Middleware: Integration layer for LLM provider caching.

This module provides middleware for transparently caching LLM responses
from providers like OpenAI, Anthropic, and others.

GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module research/agent-memory-cache/implementation
@gl-semantic-anchor GL-00-IMPL_CACHE_MIDDLEWARE
@gl-evidence-required false
GL Unified Charter Activated
"""

import asyncio
import hashlib
import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, Union

import aiohttp


logger = logging.getLogger(__name__)


# =============================================================================
# Data Models
# =============================================================================


@dataclass
class CacheKey:
    """Cache key components."""
    provider: str
    model: str
    messages_hash: str
    parameters_hash: str
    extra_params: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.extra_params is None:
            self.extra_params = {}
    
    def to_string(self) -> str:
        """Convert to cache key string."""
        components = [
            self.provider,
            self.model,
            self.messages_hash,
            self.parameters_hash
        ]
        
        if self.extra_params:
            extra_str = json.dumps(self.extra_params, sort_keys=True)
            components.append(hashlib.sha256(extra_str.encode()).hexdigest()[:16])
        
        return ":".join(components)


@dataclass
class CacheEntry:
    """Cache entry with metadata."""
    key: str
    value: Any
    created_at: datetime
    last_accessed: datetime
    ttl: int
    hit_count: int = 0
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    @property
    def is_expired(self) -> bool:
        """Check if entry is expired."""
        now = datetime.utcnow()
        age = (now - self.created_at).total_seconds()
        return age >= self.ttl
    
    @property
    def age_seconds(self) -> float:
        """Get age in seconds."""
        return (datetime.utcnow() - self.created_at).total_seconds()


@dataclass
class CacheStats:
    """Cache statistics."""
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    total_queries: int = 0
    
    @property
    def hit_rate(self) -> float:
        """Calculate hit rate."""
        if self.total_queries == 0:
            return 0.0
        return self.hits / self.total_queries
    
    @property
    def miss_rate(self) -> float:
        """Calculate miss rate."""
        if self.total_queries == 0:
            return 0.0
        return self.misses / self.total_queries


# =============================================================================
# Event Handlers
# =============================================================================


class CacheEventHandler(ABC):
    """Abstract base class for cache event handlers."""
    
    @abstractmethod
    async def on_cache_hit(self, key: str, entry: CacheEntry):
        """Handle cache hit event."""
        pass
    
    @abstractmethod
    async def on_cache_miss(self, key: str):
        """Handle cache miss event."""
        pass
    
    @abstractmethod
    async def on_cache_set(self, key: str, entry: CacheEntry):
        """Handle cache set event."""
        pass
    
    @abstractmethod
    async def on_cache_evict(self, key: str):
        """Handle cache eviction event."""
        pass


class LoggingEventHandler(CacheEventHandler):
    """Event handler that logs cache events."""
    
    def __init__(self, log_level: str = "INFO"):
        self.logger = logging.getLogger("cache.events")
        self.logger.setLevel(getattr(logging, log_level))
    
    async def on_cache_hit(self, key: str, entry: CacheEntry):
        """Log cache hit."""
        self.logger.debug(f"Cache hit: {key[:50]}... (hit count: {entry.hit_count})")
    
    async def on_cache_miss(self, key: str):
        """Log cache miss."""
        self.logger.debug(f"Cache miss: {key[:50]}...")
    
    async def on_cache_set(self, key: str, entry: CacheEntry):
        """Log cache set."""
        self.logger.debug(f"Cache set: {key[:50]}... (TTL: {entry.ttl}s)")
    
    async def on_cache_evict(self, key: str):
        """Log cache eviction."""
        self.logger.debug(f"Cache evict: {key[:50]}...")


class MetricsEventHandler(CacheEventHandler):
    """Event handler that tracks metrics."""
    
    def __init__(self):
        self.stats = CacheStats()
    
    async def on_cache_hit(self, key: str, entry: CacheEntry):
        """Record cache hit."""
        self.stats.hits += 1
        self.stats.total_queries += 1
    
    async def on_cache_miss(self, key: str):
        """Record cache miss."""
        self.stats.misses += 1
        self.stats.total_queries += 1
    
    async def on_cache_set(self, key: str, entry: CacheEntry):
        """Record cache set."""
        pass
    
    async def on_cache_evict(self, key: str):
        """Record cache eviction."""
        self.stats.evictions += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics."""
        return {
            "hits": self.stats.hits,
            "misses": self.stats.misses,
            "evictions": self.stats.evictions,
            "total_queries": self.stats.total_queries,
            "hit_rate": self.stats.hit_rate,
            "miss_rate": self.stats.miss_rate
        }
    
    def reset(self):
        """Reset statistics."""
        self.stats = CacheStats()


# =============================================================================
# Request Normalization
# =============================================================================


class RequestNormalizer:
    """Normalizes LLM requests for consistent caching."""
    
    @staticmethod
    def normalize_messages(messages: List[Dict[str, Any]]) -> str:
        """Normalize messages to a hashable string."""
        normalized = []
        for msg in messages:
            normalized_msg = {
                "role": msg.get("role", "").lower(),
                "content": msg.get("content", "").strip()
            }
            normalized.append(normalized_msg)
        
        return hashlib.sha256(
            json.dumps(normalized, sort_keys=True).encode()
        ).hexdigest()
    
    @staticmethod
    def normalize_parameters(params: Dict[str, Any]) -> str:
        """Normalize parameters to a hashable string."""
        # Sort keys and normalize values
        normalized = {}
        
        for key in sorted(params.keys()):
            value = params[key]
            if isinstance(value, (list, dict)):
                value = json.dumps(value, sort_keys=True)
            elif isinstance(value, float):
                value = round(value, 6)
            normalized[key] = str(value)
        
        return hashlib.sha256(
            json.dumps(normalized, sort_keys=True).encode()
        ).hexdigest()
    
    @staticmethod
    def create_cache_key(
        provider: str,
        model: str,
        messages: List[Dict[str, Any]],
        parameters: Dict[str, Any],
        extra_params: Optional[Dict[str, Any]] = None
    ) -> CacheKey:
        """Create cache key from request components."""
        messages_hash = RequestNormalizer.normalize_messages(messages)
        parameters_hash = RequestNormalizer.normalize_parameters(parameters)
        
        return CacheKey(
            provider=provider,
            model=model,
            messages_hash=messages_hash,
            parameters_hash=parameters_hash,
            extra_params=extra_params or {}
        )


# =============================================================================
# Cache Middleware
# =============================================================================


class CacheMiddleware:
    """Middleware for caching LLM responses."""
    
    def __init__(
        self,
        cache_backend,
        default_ttl: int = 3600,
        event_handlers: Optional[List[CacheEventHandler]] = None
    ):
        """
        Initialize cache middleware.
        
        Args:
            cache_backend: Cache backend instance (e.g., SemanticCacheV2)
            default_ttl: Default TTL in seconds
            event_handlers: List of event handlers
        """
        self.cache = cache_backend
        self.default_ttl = default_ttl
        self.normalizer = RequestNormalizer()
        self.event_handlers = event_handlers or []
        self._stats = MetricsEventHandler()
        self.event_handlers.append(self._stats)
    
    async def get(
        self,
        provider: str,
        model: str,
        messages: List[Dict[str, Any]],
        parameters: Dict[str, Any],
        ttl: Optional[int] = None
    ) -> Optional[Any]:
        """
        Get cached response.
        
        Args:
            provider: LLM provider name
            model: Model name
            messages: Message list
            parameters: Request parameters
            ttl: Optional TTL override
            
        Returns:
            Cached response or None if not found
        """
        key = self.normalizer.create_cache_key(
            provider, model, messages, parameters
        )
        
        cache_key = key.to_string()
        
        # Check cache
        result = await self.cache.get(cache_key)
        
        if result is not None:
            # Cache hit
            for handler in self.event_handlers:
                await handler.on_cache_hit(cache_key, result)
            return result
        
        # Cache miss
        for handler in self.event_handlers:
            await handler.on_cache_miss(cache_key)
        return None
    
    async def set(
        self,
        provider: str,
        model: str,
        messages: List[Dict[str, Any]],
        parameters: Dict[str, Any],
        value: Any,
        ttl: Optional[int] = None
    ):
        """
        Set cached response.
        
        Args:
            provider: LLM provider name
            model: Model name
            messages: Message list
            parameters: Request parameters
            value: Response to cache
            ttl: Optional TTL override
        """
        key = self.normalizer.create_cache_key(
            provider, model, messages, parameters
        )
        cache_key = key.to_string()
        
        entry_ttl = ttl or self.default_ttl
        
        await self.cache.set(cache_key, value, ttl=entry_ttl)
        
        entry = CacheEntry(
            key=cache_key,
            value=value,
            created_at=datetime.utcnow(),
            last_accessed=datetime.utcnow(),
            ttl=entry_ttl
        )
        
        for handler in self.event_handlers:
            await handler.on_cache_set(cache_key, entry)
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return self._stats.get_stats()
    
    def reset_stats(self):
        """Reset cache statistics."""
        self._stats.reset()


# =============================================================================
# LLM Provider Integration
# =============================================================================


class LLMProviderWithCache:
    """LLM provider with transparent caching."""
    
    def __init__(
        self,
        provider_name: str,
        base_url: str,
        api_key: str,
        cache_middleware: CacheMiddleware
    ):
        """
        Initialize cached LLM provider.
        
        Args:
            provider_name: Name of the provider
            base_url: API base URL
            api_key: API key
            cache_middleware: Cache middleware instance
        """
        self.provider_name = provider_name
        self.base_url = base_url
        self.api_key = api_key
        self.cache = cache_middleware
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session."""
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=60)
            self.session = aiohttp.ClientSession(timeout=timeout)
        return self.session
    
    async def chat_completion(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Get chat completion with caching.
        
        Args:
            model: Model name
            messages: Message list
            temperature: Sampling temperature
            max_tokens: Maximum tokens
            **kwargs: Additional parameters
            
        Returns:
            Completion response
        """
        parameters = {
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs
        }
        
        # Try cache first
        cached = await self.cache.get(
            provider=self.provider_name,
            model=model,
            messages=messages,
            parameters=parameters
        )
        
        if cached is not None:
            return cached
        
        # Cache miss - make API call
        response = await self._make_api_request(
            model=model,
            messages=messages,
            **parameters
        )
        
        # Cache the response
        await self.cache.set(
            provider=self.provider_name,
            model=model,
            messages=messages,
            parameters=parameters,
            value=response
        )
        
        return response
    
    async def _make_api_request(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        **kwargs
    ) -> Dict[str, Any]:
        """Make actual API request."""
        session = await self._get_session()
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            **kwargs
        }
        
        async with session.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload
        ) as response:
            if response.status != 200:
                error_text = await response.text()
                raise Exception(f"API error: {response.status} - {error_text}")
            
            return await response.json()
    
    async def close(self):
        """Close HTTP session."""
        if self.session and not self.session.closed:
            await self.session.close()


# =============================================================================
# Factory Functions
# =============================================================================


def create_cached_openai_provider(
    api_key: str,
    cache_middleware: CacheMiddleware,
    base_url: str = "https://api.openai.com/v1"
) -> LLMProviderWithCache:
    """
    Create cached OpenAI provider.
    
    Args:
        api_key: OpenAI API key
        cache_middleware: Cache middleware instance
        base_url: API base URL
        
    Returns:
        LLMProviderWithCache instance
    """
    return LLMProviderWithCache(
        provider_name="openai",
        base_url=base_url,
        api_key=api_key,
        cache_middleware=cache_middleware
    )


# =============================================================================
# Example Usage
# =============================================================================


async def example_usage():
    """Example usage of cache middleware."""
    
    from semantic_cache import SemanticCacheV2
    from redis_backend import RedisMemoryBackend
    
    # Create cache backend
    cache_backend = SemanticCacheV2()
    await cache_backend.initialize()
    
    # Create cache middleware
    middleware = CacheMiddleware(
        cache_backend=cache_backend,
        default_ttl=3600
    )
    
    # Create cached provider
    provider = create_cached_openai_provider(
        api_key="your-api-key",
        cache_middleware=middleware
    )
    
    # Use with caching
    messages = [
        {"role": "user", "content": "Hello, how are you?"}
    ]
    
    response = await provider.chat_completion(
        model="gpt-4",
        messages=messages,
        temperature=0.7
    )
    
    print(f"Response: {response}")
    
    # Check cache stats
    stats = await middleware.get_stats()
    print(f"Cache stats: {stats}")
    
    await provider.close()


if __name__ == "__main__":
    asyncio.run(example_usage())
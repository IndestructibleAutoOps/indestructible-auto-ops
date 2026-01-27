import asyncio
import hashlib
import json
import time
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
from functools import wraps


class CacheStrategy(Enum):
    """Cache strategy types."""
    EXACT = "exact"  # Exact match only
    SEMANTIC = "semantic"  # Semantic similarity
    HYBRID = "hybrid"  # Exact + semantic


@dataclass
class CacheEvent:
    """Cache event for monitoring."""
    event_type: str  # "hit", "miss", "write", "evict"
    key: str
    timestamp: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EventHandler:
    """Base class for cache event handlers."""
    def handle(self, event: CacheEvent) -> None:
        """Handle a cache event."""
        raise NotImplementedError


class LoggingEventHandler(EventHandler):
    """Log cache events for debugging."""
    
    def handle(self, event: CacheEvent) -> None:
        print(f"[{event.event_type.upper()}] {event.key} at {event.timestamp}")


class MetricsEventHandler(EventHandler):
    """Track cache metrics."""
    
    def __init__(self):
        self.hits = 0
        self.misses = 0
        self.writes = 0
        self.evictions = 0
    
    def handle(self, event: CacheEvent) -> None:
        if event.event_type == "hit":
            self.hits += 1
        elif event.event_type == "miss":
            self.misses += 1
        elif event.event_type == "write":
            self.writes += 1
        elif event.event_type == "evict":
            self.evictions += 1
    
    def get_stats(self) -> Dict[str, int]:
        """Get metrics statistics."""
        return {
            "hits": self.hits,
            "misses": self.misses,
            "writes": self.writes,
            "evictions": self.evictions,
            "hit_rate": self.hits / (self.hits + self.misses) if (self.hits + self.misses) > 0 else 0.0
        }


@dataclass
class CacheConfig:
    """Configuration for cache middleware."""
    cache_client: Any
    embedding_service: Any = None
    strategy: CacheStrategy = CacheStrategy.HYBRID
    ttl: int = 3600
    semantic_threshold: float = 0.85
    max_keys: int = 10000
    key_prefix: str = "cache:"
    enable_event_handlers: bool = True


class CacheMiddleware:
    """Middleware for caching LLM API responses.
    
    This middleware provides:
    - Transparent caching for LLM API calls
    - Exact match and semantic similarity caching
    - Configurable cache strategies
    - Event handling for monitoring
    - Automatic cache invalidation
    
    Usage:
        config = CacheConfig(
            cache_client=redis_client,
            embedding_service=embedding_service,
            strategy=CacheStrategy.HYBRID
        )
        middleware = CacheMiddleware(config)
        
        # Wrap OpenAI client
        client = middleware.wrap_openai_client(openai_client)
        
        # Use normally - responses will be cached automatically
        response = client.chat.completions.create(...)
    """
    
    def __init__(self, config: CacheConfig):
        """Initialize cache middleware.
        
        Args:
            config: Cache configuration
        """
        self.config = config
        self.event_handlers: List[EventHandler] = []
        
        if self.config.enable_event_handlers:
            self.event_handlers.append(LoggingEventHandler())
            self.event_handlers.append(MetricsEventHandler())
    
    def _generate_cache_key(self, request: Dict[str, Any]) -> str:
        """Generate cache key from request.
        
        Args:
            request: API request dictionary
            
        Returns:
            Cache key string
        """
        # Normalize request
        normalized = {
            "model": request.get("model"),
            "messages": request.get("messages"),
            "temperature": request.get("temperature"),
            "max_tokens": request.get("max_tokens")
        }
        
        # Generate hash
        request_str = json.dumps(normalized, sort_keys=True)
        request_hash = hashlib.md5(request_str.encode()).hexdigest()
        
        return f"{self.config.key_prefix}{request_hash}"
    
    def _emit_event(self, event_type: str, key: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Emit a cache event.
        
        Args:
            event_type: Type of event
            key: Cache key
            metadata: Optional metadata
        """
        event = CacheEvent(
            event_type=event_type,
            key=key,
            timestamp=time.time(),
            metadata=metadata or {}
        )
        
        for handler in self.event_handlers:
            handler.handle(event)
    
    def get_cached_response(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get cached response for a request.
        
        Args:
            request: API request dictionary
            
        Returns:
            Cached response or None if not found
        """
        key = self._generate_cache_key(request)
        
        # Try exact match first
        cached = self.config.cache_client.get(key)
        if cached:
            self._emit_event("hit", key, {"strategy": "exact"})
            return json.loads(cached)
        
        # Try semantic match if enabled
        if self.config.strategy in [CacheStrategy.SEMANTIC, CacheStrategy.HYBRID]:
            semantic_result = self._get_semantic_match(request)
            if semantic_result:
                self._emit_event("hit", key, {"strategy": "semantic"})
                return semantic_result
        
        self._emit_event("miss", key)
        return None
    
    def cache_response(self, request: Dict[str, Any], response: Dict[str, Any]) -> None:
        """Cache a response.
        
        Args:
            request: API request dictionary
            response: API response dictionary
        """
        key = self._generate_cache_key(request)
        
        # Store response
        self.config.cache_client.setex(
            key,
            self.config.ttl,
            json.dumps(response)
        )
        
        self._emit_event("write", key)
    
    def _get_semantic_match(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find semantically similar cached response.
        
        Args:
            request: API request dictionary
            
        Returns:
            Cached response or None if no match found
        """
        if not self.config.embedding_service:
            return None
        
        # Generate embedding for current request
        messages = request.get("messages", [])
        text = " ".join([msg.get("content", "") for msg in messages])
        
        embedding_result = self.config.embedding_service.embed(text)
        if not embedding_result.embedding:
            return None
        
        # Search for similar cached requests
        # This is simplified - in production, use vector index
        return None
    
    def wrap_openai_client(self, client: Any) -> Any:
        """Wrap OpenAI client with caching.
        
        Args:
            client: OpenAI client instance
            
        Returns:
            Wrapped client with caching
        """
        class CachedOpenAIClient:
            def __init__(self, middleware, original_client):
                self.middleware = middleware
                self.original_client = original_client
            
            def __getattr__(self, name):
                attr = getattr(self.original_client, name)
                
                if name == "chat":
                    return CachedChatCompletions(self.middleware, attr)
                
                return attr
        
        class CachedChatCompletions:
            def __init__(self, middleware, original_chat):
                self.middleware = middleware
                self.original_chat = original_chat
            
            @property
            def completions(self):
                return CachedCompletions(self.middleware, self.original_chat.completions)
        
        class CachedCompletions:
            def __init__(self, middleware, original_completions):
                self.middleware = middleware
                self.original_completions = original_completions
            
            def create(self, **kwargs):
                # Check cache
                cached_response = self.middleware.get_cached_response(kwargs)
                
                if cached_response:
                    # Return cached response
                    return self._parse_response(cached_response)
                
                # Call original API
                response = self.original_completions.create(**kwargs)
                
                # Cache response
                response_dict = self._serialize_response(response)
                self.middleware.cache_response(kwargs, response_dict)
                
                return response
            
            def _parse_response(self, response_dict: Dict[str, Any]) -> Any:
                """Parse cached response back to object."""
                # Simplified - in production, reconstruct proper response object
                return response_dict
            
            def _serialize_response(self, response: Any) -> Dict[str, Any]:
                """Serialize response to dictionary."""
                # Simplified - in production, proper serialization
                return {
                    "content": response.choices[0].message.content,
                    "model": response.model,
                    "usage": {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens
                    }
                }
        
        return CachedOpenAIClient(self, client)
    
    def wrap_anthropic_client(self, client: Any) -> Any:
        """Wrap Anthropic client with caching.
        
        Args:
            client: Anthropic client instance
            
        Returns:
            Wrapped client with caching
        """
        class CachedAnthropicClient:
            def __init__(self, middleware, original_client):
                self.middleware = middleware
                self.original_client = original_client
            
            def messages_create(self, **kwargs):
                # Check cache
                cached_response = self.middleware.get_cached_response(kwargs)
                
                if cached_response:
                    return self._parse_response(cached_response)
                
                # Call original API
                response = self.original_client.messages.create(**kwargs)
                
                # Cache response
                response_dict = self._serialize_response(response)
                self.middleware.cache_response(kwargs, response_dict)
                
                return response
            
            def _parse_response(self, response_dict: Dict[str, Any]) -> Any:
                """Parse cached response back to object."""
                return response_dict
            
            def _serialize_response(self, response: Any) -> Dict[str, Any]:
                """Serialize response to dictionary."""
                return {
                    "content": response.content[0].text,
                    "model": response.model,
                    "usage": {
                        "input_tokens": response.usage.input_tokens,
                        "output_tokens": response.usage.output_tokens
                    }
                }
        
        return CachedAnthropicClient(self, client)
    
    def invalidate_cache(self, pattern: str = None) -> int:
        """Invalidate cache entries.
        
        Args:
            pattern: Optional key pattern to match
            
        Returns:
            Number of invalidated entries
        """
        if pattern:
            # Scan and delete matching keys
            count = 0
            for key in self.config.cache_client.scan_iter(match=pattern):
                self.config.cache_client.delete(key)
                self._emit_event("evict", key)
                count += 1
            return count
        else:
            # Clear all cache
            keys = self.config.cache_client.keys(f"{self.config.key_prefix}*")
            for key in keys:
                self._emit_event("evict", key)
            if keys:
                self.config.cache_client.delete(*keys)
            return len(keys)
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        stats = {
            "strategy": self.config.strategy.value,
            "ttl": self.config.ttl,
            "semantic_threshold": self.config.semantic_threshold
        }
        
        # Get metrics from handlers
        for handler in self.event_handlers:
            if isinstance(handler, MetricsEventHandler):
                stats.update(handler.get_stats())
        
        return stats
    
    def health_check(self) -> Dict[str, Any]:
        """Check health of cache middleware.
        
        Returns:
            Health status dictionary
        """
        try:
            # Test cache operation
            test_key = f"{self.config.key_prefix}health_check"
            self.config.cache_client.setex(test_key, 10, "ok")
            result = self.config.cache_client.get(test_key)
            self.config.cache_client.delete(test_key)
            
            return {
                "status": "healthy",
                "cache_connected": result is not None,
                "event_handlers": len(self.event_handlers)
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
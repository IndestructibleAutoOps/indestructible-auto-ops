"""
Cache Middleware: Integration layer for LLM providers with semantic caching.

Provides transparent caching for various LLM providers including:
- OpenAI
- Azure OpenAI
- Anthropic
- Google (Gemini)
- Local models (Ollama)

GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module ns-root/namespaces-adk/adk/plugins/memory_plugins
@gl-semantic-anchor GL-00-PLUGINS_MEMORYPL_CACHEMW
@gl-evidence-required false
GL Unified Charter Activated
"""

import asyncio
import functools
import hashlib
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union

from .semantic_cache_v2 import SemanticCacheV2, CacheStrategy, CacheHit


@dataclass
class CacheMiddlewareConfig:
    """Configuration for cache middleware."""
    enabled: bool = True
    strategy: CacheStrategy = CacheStrategy.HYBRID
    cache_streaming: bool = True
    include_system_prompt: bool = False
    include_temperature: bool = True
    include_max_tokens: bool = False
    bypass_on_error: bool = True
    log_cache_events: bool = True
    
    # Request normalization
    normalize_whitespace: bool = True
    lowercase_queries: bool = False
    
    # Response handling
    store_on_error: bool = False
    min_response_length: int = 10
    max_response_length: int = 100000


@dataclass
class CacheEvent:
    """Event emitted by cache middleware."""
    event_type: str  # "hit", "miss", "store", "error", "bypass"
    query_hash: str
    model: str
    timestamp: float = field(default_factory=time.time)
    similarity: Optional[float] = None
    lookup_time_ms: Optional[float] = None
    tokens_saved: Optional[int] = None
    error: Optional[str] = None


class CacheEventHandler(ABC):
    """Abstract handler for cache events."""
    
    @abstractmethod
    async def handle(self, event: CacheEvent) -> None:
        """Handle a cache event."""
        pass


class LoggingEventHandler(CacheEventHandler):
    """Event handler that logs cache events."""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self._logger = logger or logging.getLogger(__name__)
    
    async def handle(self, event: CacheEvent) -> None:
        if event.event_type == "hit":
            self._logger.info(
                f"Cache HIT: model={event.model}, similarity={event.similarity:.3f}, "
                f"time={event.lookup_time_ms:.1f}ms, tokens_saved={event.tokens_saved}"
            )
        elif event.event_type == "miss":
            self._logger.debug(f"Cache MISS: model={event.model}")
        elif event.event_type == "store":
            self._logger.debug(f"Cache STORE: model={event.model}")
        elif event.event_type == "error":
            self._logger.warning(f"Cache ERROR: {event.error}")


class MetricsEventHandler(CacheEventHandler):
    """Event handler that collects metrics."""
    
    def __init__(self):
        self.metrics = {
            "total_requests": 0,
            "hits": 0,
            "misses": 0,
            "stores": 0,
            "errors": 0,
            "total_tokens_saved": 0,
            "total_lookup_time_ms": 0.0,
            "by_model": {},
        }
    
    async def handle(self, event: CacheEvent) -> None:
        self.metrics["total_requests"] += 1
        
        if event.event_type == "hit":
            self.metrics["hits"] += 1
            self.metrics["total_tokens_saved"] += event.tokens_saved or 0
            self.metrics["total_lookup_time_ms"] += event.lookup_time_ms or 0
        elif event.event_type == "miss":
            self.metrics["misses"] += 1
        elif event.event_type == "store":
            self.metrics["stores"] += 1
        elif event.event_type == "error":
            self.metrics["errors"] += 1
        
        # Track by model
        if event.model not in self.metrics["by_model"]:
            self.metrics["by_model"][event.model] = {"hits": 0, "misses": 0}
        
        if event.event_type == "hit":
            self.metrics["by_model"][event.model]["hits"] += 1
        elif event.event_type == "miss":
            self.metrics["by_model"][event.model]["misses"] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        total = self.metrics["hits"] + self.metrics["misses"]
        return {
            **self.metrics,
            "hit_rate": self.metrics["hits"] / total if total > 0 else 0,
            "avg_lookup_time_ms": (
                self.metrics["total_lookup_time_ms"] / self.metrics["hits"]
                if self.metrics["hits"] > 0 else 0
            ),
        }


class CacheMiddleware:
    """
    Middleware for transparent LLM response caching.
    
    Can be used as a decorator or wrapper for LLM calls.
    """
    
    def __init__(
        self,
        cache: SemanticCacheV2,
        config: Optional[CacheMiddlewareConfig] = None,
        event_handlers: Optional[List[CacheEventHandler]] = None,
    ):
        """
        Initialize cache middleware.
        
        Args:
            cache: Semantic cache instance
            config: Middleware configuration
            event_handlers: List of event handlers
        """
        self._cache = cache
        self.config = config or CacheMiddlewareConfig()
        self._event_handlers = event_handlers or []
        self._logger = logging.getLogger(__name__)
        
        # Add default logging handler if enabled
        if self.config.log_cache_events:
            self._event_handlers.append(LoggingEventHandler(self._logger))

    def add_event_handler(self, handler: CacheEventHandler) -> None:
        """Add an event handler."""
        self._event_handlers.append(handler)

    async def _emit_event(self, event: CacheEvent) -> None:
        """Emit event to all handlers."""
        for handler in self._event_handlers:
            try:
                await handler.handle(event)
            except Exception as e:
                self._logger.warning(f"Event handler error: {e}")

    def _build_cache_key(
        self,
        messages: List[Dict[str, str]],
        model: str,
        **kwargs,
    ) -> str:
        """Build cache key from request parameters."""
        # Extract user messages
        user_messages = []
        for msg in messages:
            role = msg.get("role", "")
            content = msg.get("content", "")
            
            if role == "user":
                user_messages.append(content)
            elif role == "system" and self.config.include_system_prompt:
                user_messages.append(f"[system]{content}")
        
        query = "\n".join(user_messages)
        
        # Normalize
        if self.config.normalize_whitespace:
            query = " ".join(query.split())
        if self.config.lowercase_queries:
            query = query.lower()
        
        # Include parameters in key
        key_parts = [query]
        
        if self.config.include_temperature:
            temp = kwargs.get("temperature", 1.0)
            key_parts.append(f"temp:{temp}")
        
        if self.config.include_max_tokens:
            max_tokens = kwargs.get("max_tokens", "default")
            key_parts.append(f"max:{max_tokens}")
        
        return "|".join(key_parts)

    async def wrap_completion(
        self,
        completion_fn: Callable,
        messages: List[Dict[str, str]],
        model: str,
        **kwargs,
    ) -> Any:
        """
        Wrap a completion function with caching.
        
        Args:
            completion_fn: The completion function to wrap
            messages: Chat messages
            model: Model identifier
            **kwargs: Additional arguments for completion
            
        Returns:
            Completion response (cached or fresh)
        """
        if not self.config.enabled:
            return await completion_fn(messages=messages, model=model, **kwargs)
        
        # Build cache key
        cache_key = self._build_cache_key(messages, model, **kwargs)
        query_hash = hashlib.sha256(cache_key.encode()).hexdigest()[:16]
        
        try:
            # Try cache lookup
            hit = await self._cache.get(
                query=cache_key,
                model=model,
                strategy=self.config.strategy,
            )
            
            if hit:
                # Cache hit
                await self._emit_event(CacheEvent(
                    event_type="hit",
                    query_hash=query_hash,
                    model=model,
                    similarity=hit.similarity,
                    lookup_time_ms=hit.lookup_time_ms,
                    tokens_saved=hit.entry.tokens_saved,
                ))
                
                # Return cached response in expected format
                return self._format_cached_response(hit.entry.response, model)
            
            # Cache miss
            await self._emit_event(CacheEvent(
                event_type="miss",
                query_hash=query_hash,
                model=model,
            ))
            
        except Exception as e:
            await self._emit_event(CacheEvent(
                event_type="error",
                query_hash=query_hash,
                model=model,
                error=str(e),
            ))
            
            if not self.config.bypass_on_error:
                raise
        
        # Call actual completion
        response = await completion_fn(messages=messages, model=model, **kwargs)
        
        # Extract and cache response
        try:
            response_text = self._extract_response_text(response)
            tokens_used = self._extract_token_count(response)
            
            if (
                response_text
                and len(response_text) >= self.config.min_response_length
                and len(response_text) <= self.config.max_response_length
            ):
                await self._cache.set(
                    query=cache_key,
                    response=response_text,
                    model=model,
                    tokens_used=tokens_used,
                )
                
                await self._emit_event(CacheEvent(
                    event_type="store",
                    query_hash=query_hash,
                    model=model,
                ))
                
        except Exception as e:
            self._logger.warning(f"Failed to cache response: {e}")
        
        return response

    def _format_cached_response(self, text: str, model: str) -> Dict[str, Any]:
        """Format cached text as completion response."""
        return {
            "id": f"cached-{hashlib.sha256(text.encode()).hexdigest()[:8]}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": text,
                    },
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
            },
            "_cached": True,
        }

    def _extract_response_text(self, response: Any) -> Optional[str]:
        """Extract text from completion response."""
        try:
            # OpenAI format
            if isinstance(response, dict):
                choices = response.get("choices", [])
                if choices:
                    message = choices[0].get("message", {})
                    return message.get("content", "")
            
            # Object with attributes
            if hasattr(response, "choices") and response.choices:
                message = response.choices[0].message
                return getattr(message, "content", "")
            
        except Exception:
            pass
        
        return None

    def _extract_token_count(self, response: Any) -> int:
        """Extract token count from completion response."""
        try:
            if isinstance(response, dict):
                usage = response.get("usage", {})
                return usage.get("total_tokens", 0)
            
            if hasattr(response, "usage"):
                return getattr(response.usage, "total_tokens", 0)
                
        except Exception:
            pass
        
        return 0

    def cached(
        self,
        model: Optional[str] = None,
        ttl: Optional[int] = None,
    ) -> Callable:
        """
        Decorator for caching LLM completions.
        
        Args:
            model: Model identifier (if not in function args)
            ttl: Cache TTL override
            
        Returns:
            Decorated function
        """
        def decorator(fn: Callable) -> Callable:
            @functools.wraps(fn)
            async def wrapper(*args, **kwargs) -> Any:
                # Extract messages and model from args/kwargs
                messages = kwargs.get("messages", args[0] if args else [])
                fn_model = kwargs.get("model", model or "unknown")
                
                return await self.wrap_completion(
                    completion_fn=fn,
                    messages=messages,
                    model=fn_model,
                    **{k: v for k, v in kwargs.items() if k not in ("messages", "model")},
                )
            
            return wrapper
        return decorator


class OpenAICacheMiddleware(CacheMiddleware):
    """Cache middleware specifically for OpenAI API."""
    
    async def create_completion(
        self,
        client: Any,
        messages: List[Dict[str, str]],
        model: str = "gpt-4",
        **kwargs,
    ) -> Any:
        """
        Create a cached completion using OpenAI client.
        
        Args:
            client: OpenAI client instance
            messages: Chat messages
            model: Model name
            **kwargs: Additional OpenAI parameters
            
        Returns:
            Completion response
        """
        async def completion_fn(**kw):
            return await client.chat.completions.create(**kw)
        
        return await self.wrap_completion(
            completion_fn=completion_fn,
            messages=messages,
            model=model,
            **kwargs,
        )


class AnthropicCacheMiddleware(CacheMiddleware):
    """Cache middleware specifically for Anthropic API."""
    
    async def create_message(
        self,
        client: Any,
        messages: List[Dict[str, str]],
        model: str = "claude-3-opus-20240229",
        max_tokens: int = 4096,
        **kwargs,
    ) -> Any:
        """
        Create a cached message using Anthropic client.
        
        Args:
            client: Anthropic client instance
            messages: Chat messages
            model: Model name
            max_tokens: Maximum tokens
            **kwargs: Additional Anthropic parameters
            
        Returns:
            Message response
        """
        async def completion_fn(**kw):
            return await client.messages.create(**kw)
        
        return await self.wrap_completion(
            completion_fn=completion_fn,
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            **kwargs,
        )

    def _extract_response_text(self, response: Any) -> Optional[str]:
        """Extract text from Anthropic response."""
        try:
            if hasattr(response, "content") and response.content:
                return response.content[0].text
        except Exception:
            pass
        return super()._extract_response_text(response)

    def _extract_token_count(self, response: Any) -> int:
        """Extract token count from Anthropic response."""
        try:
            if hasattr(response, "usage"):
                return response.usage.input_tokens + response.usage.output_tokens
        except Exception:
            pass
        return 0
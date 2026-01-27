"""
Unit tests for Semantic Cache V2 (P3).
Tests enhanced semantic caching with vector search integration.
"""

import pytest
import asyncio
import time
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Any, Dict, List

from adk.plugins.memory_plugins.semantic_cache_v2 import (
    SemanticCacheV2,
    SemanticCacheConfigV2,
    CacheStrategy,
    EvictionPolicy,
    CacheEntry,
    CacheHit,
    CacheStats,
)
from adk.plugins.memory_plugins.cache_middleware import (
    CacheMiddleware,
    CacheMiddlewareConfig,
    CacheEvent,
    LoggingEventHandler,
    MetricsEventHandler,
    OpenAICacheMiddleware,
)


class TestSemanticCacheConfigV2:
    """Tests for SemanticCacheConfigV2."""

    def test_default_config(self):
        """Test default configuration values."""
        config = SemanticCacheConfigV2()
        assert config.similarity_threshold == 0.85
        assert config.default_ttl == 3600
        assert config.max_entries == 10000
        assert config.eviction_policy == EvictionPolicy.ADAPTIVE

    def test_custom_config(self):
        """Test custom configuration."""
        config = SemanticCacheConfigV2(
            similarity_threshold=0.9,
            default_ttl=7200,
            max_entries=5000,
            eviction_policy=EvictionPolicy.LRU,
            enable_adaptive_ttl=False,
        )
        assert config.similarity_threshold == 0.9
        assert config.default_ttl == 7200
        assert config.eviction_policy == EvictionPolicy.LRU


class TestCacheEntry:
    """Tests for CacheEntry."""

    def test_entry_creation(self):
        """Test creating a cache entry."""
        entry = CacheEntry(
            id="test123",
            query="What is AI?",
            query_hash="abc123",
            response="AI is artificial intelligence.",
            embedding=[0.1] * 1536,
            model="gpt-4",
        )
        assert entry.id == "test123"
        assert entry.query == "What is AI?"
        assert entry.access_count == 0
        assert entry.importance_score == 1.0

    def test_entry_with_metadata(self):
        """Test entry with metadata."""
        entry = CacheEntry(
            id="test456",
            query="Test query",
            query_hash="def456",
            response="Test response",
            embedding=[0.2] * 1536,
            metadata={"user_id": "user1", "session": "sess1"},
            tokens_saved=150,
        )
        assert entry.metadata["user_id"] == "user1"
        assert entry.tokens_saved == 150


class TestCacheStats:
    """Tests for CacheStats."""

    def test_hit_rate_calculation(self):
        """Test hit rate calculation."""
        stats = CacheStats(total_requests=100, hits=75, misses=25)
        assert stats.hit_rate == 0.75

    def test_hit_rate_zero_requests(self):
        """Test hit rate with zero requests."""
        stats = CacheStats()
        assert stats.hit_rate == 0.0


class TestSemanticCacheV2:
    """Tests for SemanticCacheV2."""

    @pytest.fixture
    def mock_redis(self):
        """Create mock Redis client."""
        client = AsyncMock()
        client.ft = MagicMock(return_value=AsyncMock())
        client.json = MagicMock(return_value=AsyncMock())
        client.scan_iter = MagicMock(return_value=AsyncMock())
        client.delete = AsyncMock(return_value=1)
        client.expire = AsyncMock()
        client.ttl = AsyncMock(return_value=3600)
        return client

    @pytest.fixture
    def mock_embedding_service(self):
        """Create mock embedding service."""
        service = AsyncMock()
        service.embed = AsyncMock(return_value=[0.1] * 1536)
        return service

    @pytest.fixture
    def cache(self, mock_redis, mock_embedding_service):
        """Create SemanticCacheV2 instance."""
        return SemanticCacheV2(
            redis_client=mock_redis,
            embedding_service=mock_embedding_service,
        )

    @pytest.mark.asyncio
    async def test_initialize(self, cache, mock_redis):
        """Test cache initialization."""
        mock_redis.ft().info = AsyncMock(side_effect=Exception("Index not found"))
        mock_redis.ft().create_index = AsyncMock()
        
        await cache.initialize()
        
        assert cache._initialized is True

    @pytest.mark.asyncio
    async def test_set_entry(self, cache, mock_redis, mock_embedding_service):
        """Test storing a cache entry."""
        cache._initialized = True
        cache._index_manager = MagicMock()
        
        entry_id = await cache.set(
            query="What is Python?",
            response="Python is a programming language.",
            model="gpt-4",
            tokens_used=50,
        )
        
        assert entry_id is not None
        assert cache._stats.stores == 1
        mock_embedding_service.embed.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_cache_miss(self, cache, mock_redis):
        """Test cache miss."""
        cache._initialized = True
        cache._index_manager = MagicMock()
        cache._search_executor = AsyncMock()
        
        # Mock empty scan
        async def empty_scan():
            return
            yield  # Make it an async generator that yields nothing
        
        mock_redis.scan_iter = MagicMock(return_value=empty_scan())
        
        # Mock search returning no results
        cache._search_executor.search = AsyncMock(return_value=MagicMock(results=[]))
        
        result = await cache.get("Unknown query")
        
        assert result is None
        assert cache._stats.misses == 1

    @pytest.mark.asyncio
    async def test_get_or_compute_cached(self, cache):
        """Test get_or_compute with cached value."""
        cache._initialized = True
        
        # Mock cache hit
        mock_entry = CacheEntry(
            id="test",
            query="test",
            query_hash="hash",
            response="Cached response",
            embedding=[0.1] * 1536,
        )
        
        with patch.object(cache, 'get', return_value=CacheHit(
            entry=mock_entry,
            similarity=0.95,
            is_exact_match=False,
            lookup_time_ms=5.0,
        )):
            response, was_cached = await cache.get_or_compute(
                query="test query",
                compute_fn=lambda: "Computed response",
            )
        
        assert response == "Cached response"
        assert was_cached is True

    @pytest.mark.asyncio
    async def test_get_or_compute_not_cached(self, cache):
        """Test get_or_compute without cached value."""
        cache._initialized = True
        
        with patch.object(cache, 'get', return_value=None):
            with patch.object(cache, 'set', return_value="new_id"):
                response, was_cached = await cache.get_or_compute(
                    query="test query",
                    compute_fn=lambda: "Computed response",
                )
        
        assert response == "Computed response"
        assert was_cached is False

    def test_normalize_query(self, cache):
        """Test query normalization."""
        result = cache._normalize_query("  Hello   World  ")
        assert result == "hello world"

    def test_hash_query(self, cache):
        """Test query hashing."""
        hash1 = cache._hash_query("test query")
        hash2 = cache._hash_query("test query")
        hash3 = cache._hash_query("different query")
        
        assert hash1 == hash2
        assert hash1 != hash3
        assert len(hash1) == 64  # SHA256 hex length

    def test_dict_to_entry(self, cache):
        """Test dictionary to entry conversion."""
        data = {
            "id": "test123",
            "query": "Test query",
            "query_hash": "hash123",
            "response": "Test response",
            "embedding": [0.1] * 10,
            "model": "gpt-4",
            "access_count": 5,
            "tokens_saved": 100,
        }
        
        entry = cache._dict_to_entry(data)
        
        assert entry.id == "test123"
        assert entry.access_count == 5
        assert entry.tokens_saved == 100

    def test_get_stats(self, cache):
        """Test getting cache statistics."""
        cache._stats.hits = 80
        cache._stats.misses = 20
        cache._stats.total_requests = 100
        
        stats = cache.get_stats()
        
        assert stats["hits"] == 80
        assert stats["hit_rate"] == 0.8


class TestCacheMiddlewareConfig:
    """Tests for CacheMiddlewareConfig."""

    def test_default_config(self):
        """Test default configuration."""
        config = CacheMiddlewareConfig()
        assert config.enabled is True
        assert config.strategy == CacheStrategy.HYBRID
        assert config.bypass_on_error is True

    def test_custom_config(self):
        """Test custom configuration."""
        config = CacheMiddlewareConfig(
            enabled=False,
            strategy=CacheStrategy.SEMANTIC_ONLY,
            include_system_prompt=True,
        )
        assert config.enabled is False
        assert config.strategy == CacheStrategy.SEMANTIC_ONLY


class TestCacheEvent:
    """Tests for CacheEvent."""

    def test_event_creation(self):
        """Test creating a cache event."""
        event = CacheEvent(
            event_type="hit",
            query_hash="abc123",
            model="gpt-4",
            similarity=0.95,
            lookup_time_ms=5.0,
            tokens_saved=100,
        )
        assert event.event_type == "hit"
        assert event.similarity == 0.95
        assert event.tokens_saved == 100


class TestMetricsEventHandler:
    """Tests for MetricsEventHandler."""

    @pytest.mark.asyncio
    async def test_handle_hit(self):
        """Test handling hit event."""
        handler = MetricsEventHandler()
        
        event = CacheEvent(
            event_type="hit",
            query_hash="abc",
            model="gpt-4",
            tokens_saved=100,
            lookup_time_ms=5.0,
        )
        
        await handler.handle(event)
        
        assert handler.metrics["hits"] == 1
        assert handler.metrics["total_tokens_saved"] == 100

    @pytest.mark.asyncio
    async def test_handle_miss(self):
        """Test handling miss event."""
        handler = MetricsEventHandler()
        
        event = CacheEvent(
            event_type="miss",
            query_hash="abc",
            model="gpt-4",
        )
        
        await handler.handle(event)
        
        assert handler.metrics["misses"] == 1

    @pytest.mark.asyncio
    async def test_get_metrics(self):
        """Test getting metrics."""
        handler = MetricsEventHandler()
        handler.metrics["hits"] = 75
        handler.metrics["misses"] = 25
        
        metrics = handler.get_metrics()
        
        assert metrics["hit_rate"] == 0.75


class TestCacheMiddleware:
    """Tests for CacheMiddleware."""

    @pytest.fixture
    def mock_cache(self):
        """Create mock cache."""
        cache = AsyncMock()
        cache.get = AsyncMock(return_value=None)
        cache.set = AsyncMock(return_value="entry_id")
        return cache

    @pytest.fixture
    def middleware(self, mock_cache):
        """Create CacheMiddleware instance."""
        config = CacheMiddlewareConfig(log_cache_events=False)
        return CacheMiddleware(cache=mock_cache, config=config)

    def test_build_cache_key(self, middleware):
        """Test building cache key."""
        messages = [
            {"role": "system", "content": "You are helpful."},
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
            {"role": "user", "content": "How are you?"},
        ]
        
        key = middleware._build_cache_key(messages, "gpt-4", temperature=0.7)
        
        assert "Hello" in key
        assert "How are you?" in key
        assert "temp:0.7" in key

    def test_format_cached_response(self, middleware):
        """Test formatting cached response."""
        response = middleware._format_cached_response("Test response", "gpt-4")
        
        assert response["model"] == "gpt-4"
        assert response["choices"][0]["message"]["content"] == "Test response"
        assert response["_cached"] is True

    def test_extract_response_text_dict(self, middleware):
        """Test extracting response text from dict."""
        response = {
            "choices": [
                {"message": {"content": "Test content"}}
            ]
        }
        
        text = middleware._extract_response_text(response)
        
        assert text == "Test content"

    def test_extract_token_count(self, middleware):
        """Test extracting token count."""
        response = {
            "usage": {"total_tokens": 150}
        }
        
        count = middleware._extract_token_count(response)
        
        assert count == 150

    @pytest.mark.asyncio
    async def test_wrap_completion_cache_hit(self, middleware, mock_cache):
        """Test wrap_completion with cache hit."""
        mock_entry = CacheEntry(
            id="test",
            query="test",
            query_hash="hash",
            response="Cached response",
            embedding=[0.1] * 1536,
            tokens_saved=50,
        )
        
        mock_cache.get = AsyncMock(return_value=CacheHit(
            entry=mock_entry,
            similarity=0.95,
            is_exact_match=False,
            lookup_time_ms=5.0,
        ))
        
        async def mock_completion(**kwargs):
            return {"choices": [{"message": {"content": "Fresh response"}}]}
        
        result = await middleware.wrap_completion(
            completion_fn=mock_completion,
            messages=[{"role": "user", "content": "Hello"}],
            model="gpt-4",
        )
        
        assert result["choices"][0]["message"]["content"] == "Cached response"
        assert result["_cached"] is True

    @pytest.mark.asyncio
    async def test_wrap_completion_cache_miss(self, middleware, mock_cache):
        """Test wrap_completion with cache miss."""
        mock_cache.get = AsyncMock(return_value=None)
        
        async def mock_completion(**kwargs):
            return {
                "choices": [{"message": {"content": "Fresh response"}}],
                "usage": {"total_tokens": 100},
            }
        
        result = await middleware.wrap_completion(
            completion_fn=mock_completion,
            messages=[{"role": "user", "content": "Hello"}],
            model="gpt-4",
        )
        
        assert result["choices"][0]["message"]["content"] == "Fresh response"
        mock_cache.set.assert_called_once()

    @pytest.mark.asyncio
    async def test_disabled_middleware(self, mock_cache):
        """Test disabled middleware passes through."""
        config = CacheMiddlewareConfig(enabled=False)
        middleware = CacheMiddleware(cache=mock_cache, config=config)
        
        async def mock_completion(**kwargs):
            return {"choices": [{"message": {"content": "Direct response"}}]}
        
        result = await middleware.wrap_completion(
            completion_fn=mock_completion,
            messages=[{"role": "user", "content": "Hello"}],
            model="gpt-4",
        )
        
        assert result["choices"][0]["message"]["content"] == "Direct response"
        mock_cache.get.assert_not_called()


class TestEvictionPolicy:
    """Tests for eviction policies."""

    def test_eviction_policy_values(self):
        """Test eviction policy enum values."""
        assert EvictionPolicy.LRU.value == "lru"
        assert EvictionPolicy.LFU.value == "lfu"
        assert EvictionPolicy.TTL.value == "ttl"
        assert EvictionPolicy.ADAPTIVE.value == "adaptive"


class TestCacheStrategy:
    """Tests for cache strategies."""

    def test_cache_strategy_values(self):
        """Test cache strategy enum values."""
        assert CacheStrategy.EXACT_ONLY.value == "exact_only"
        assert CacheStrategy.SEMANTIC_ONLY.value == "semantic_only"
        assert CacheStrategy.HYBRID.value == "hybrid"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
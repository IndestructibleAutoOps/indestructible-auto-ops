"""
Unit tests for Vector Search Integration (P2).
Tests vector index manager, embedding service, and vector search.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Any

# Import modules under test
from adk.plugins.memory_plugins.vector_index_manager import (
    VectorIndexManager,
    VectorIndexConfig,
    DistanceMetric,
    VectorAlgorithm,
    DEFAULT_MEMORY_INDEX,
)
from adk.plugins.memory_plugins.embedding_service import (
    EmbeddingService,
    EmbeddingConfig,
    EmbeddingProvider,
)
from adk.plugins.memory_plugins.vector_search import (
    VectorSearchQueryBuilder,
    VectorSearchExecutor,
    FilterCondition,
    FilterOperator,
    SearchResult,
    SemanticMemorySearch,
)


class TestVectorIndexConfig:
    """Tests for VectorIndexConfig."""

    def test_default_config(self):
        """Test default configuration values."""
        config = VectorIndexConfig(name="test", prefix="test:")
        assert config.name == "test"
        assert config.prefix == "test:"
        assert config.dimension == 1536
        assert config.distance_metric == DistanceMetric.COSINE
        assert config.algorithm == VectorAlgorithm.HNSW

    def test_custom_config(self):
        """Test custom configuration."""
        config = VectorIndexConfig(
            name="custom",
            prefix="custom:",
            dimension=768,
            distance_metric=DistanceMetric.L2,
            algorithm=VectorAlgorithm.FLAT,
            text_fields=["title", "body"],
            tag_fields=["category"],
            numeric_fields=["score"]
        )
        assert config.dimension == 768
        assert config.distance_metric == DistanceMetric.L2
        assert config.algorithm == VectorAlgorithm.FLAT
        assert "title" in config.text_fields
        assert "category" in config.tag_fields


class TestVectorIndexManager:
    """Tests for VectorIndexManager."""

    @pytest.fixture
    def mock_redis(self):
        """Create mock Redis client."""
        client = AsyncMock()
        client.ft = MagicMock(return_value=AsyncMock())
        client.json = MagicMock(return_value=AsyncMock())
        client.execute_command = AsyncMock()
        client.delete = AsyncMock(return_value=1)
        return client

    @pytest.fixture
    def manager(self, mock_redis):
        """Create VectorIndexManager instance."""
        return VectorIndexManager(mock_redis)

    @pytest.mark.asyncio
    async def test_create_index_new(self, manager, mock_redis):
        """Test creating a new index."""
        mock_redis.ft().info = AsyncMock(side_effect=Exception("Index not found"))
        
        config = VectorIndexConfig(name="test_idx", prefix="test:")
        result = await manager.create_index(config)
        
        assert result is True
        mock_redis.execute_command.assert_called_once()
        assert "test_idx" in manager.get_registered_indices()

    @pytest.mark.asyncio
    async def test_create_index_exists(self, manager, mock_redis):
        """Test creating an index that already exists."""
        mock_redis.ft().info = AsyncMock(return_value={"name": "test_idx"})
        
        config = VectorIndexConfig(name="test_idx", prefix="test:")
        result = await manager.create_index(config)
        
        assert result is False

    @pytest.mark.asyncio
    async def test_drop_index(self, manager, mock_redis):
        """Test dropping an index."""
        manager._indices["test_idx"] = VectorIndexConfig(name="test_idx", prefix="test:")
        
        result = await manager.drop_index("test_idx")
        
        assert result is True
        assert "test_idx" not in manager.get_registered_indices()

    @pytest.mark.asyncio
    async def test_store_document(self, manager, mock_redis):
        """Test storing a document."""
        config = VectorIndexConfig(name="test_idx", prefix="test:")
        manager._indices["test_idx"] = config
        
        key = await manager.store_document(
            index_name="test_idx",
            doc_id="doc1",
            content="Test content",
            embedding=[0.1] * 1536,
            metadata={"type": "test"}
        )
        
        assert key == "test:doc1"
        mock_redis.json().set.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_document(self, manager, mock_redis):
        """Test deleting a document."""
        config = VectorIndexConfig(name="test_idx", prefix="test:")
        manager._indices["test_idx"] = config
        
        result = await manager.delete_document("test_idx", "doc1")
        
        assert result is True
        mock_redis.delete.assert_called_with("test:doc1")

    def test_generate_doc_id(self):
        """Test document ID generation."""
        id1 = VectorIndexManager.generate_doc_id("content1")
        id2 = VectorIndexManager.generate_doc_id("content1")
        id3 = VectorIndexManager.generate_doc_id("content2")
        
        assert id1 == id2  # Same content = same ID
        assert id1 != id3  # Different content = different ID
        assert len(id1) == 16


class TestEmbeddingConfig:
    """Tests for EmbeddingConfig."""

    def test_openai_config(self):
        """Test OpenAI configuration."""
        config = EmbeddingConfig(
            provider=EmbeddingProvider.OPENAI,
            model="text-embedding-ada-002",
            dimension=1536,
            api_key="test-key"
        )
        assert config.provider == EmbeddingProvider.OPENAI
        assert config.dimension == 1536

    def test_ollama_config(self):
        """Test Ollama configuration."""
        config = EmbeddingConfig(
            provider=EmbeddingProvider.OLLAMA,
            model="nomic-embed-text",
            dimension=768,
            api_base="http://localhost:11434"
        )
        assert config.provider == EmbeddingProvider.OLLAMA
        assert config.api_base == "http://localhost:11434"


class TestEmbeddingService:
    """Tests for EmbeddingService."""

    @pytest.fixture
    def mock_cache(self):
        """Create mock cache client."""
        cache = AsyncMock()
        cache.get = AsyncMock(return_value=None)
        cache.setex = AsyncMock()
        return cache

    @pytest.mark.asyncio
    async def test_embed_with_cache_miss(self, mock_cache):
        """Test embedding with cache miss."""
        config = EmbeddingConfig(
            provider=EmbeddingProvider.OPENAI,
            model="text-embedding-ada-002",
            dimension=1536,
            api_key="test-key"
        )
        
        with patch.object(EmbeddingService, 'PROVIDER_MAP') as mock_map:
            mock_provider = MagicMock()
            mock_provider.return_value.embed_text = AsyncMock(return_value=[0.1] * 1536)
            mock_provider.return_value.dimension = 1536
            mock_map.__getitem__ = MagicMock(return_value=mock_provider)
            mock_map.get = MagicMock(return_value=mock_provider)
            
            service = EmbeddingService(config, cache_client=mock_cache)
            result = await service.embed("test text")
            
            assert len(result) == 1536
            assert service.get_stats()["cache_misses"] == 1

    @pytest.mark.asyncio
    async def test_embed_with_cache_hit(self, mock_cache):
        """Test embedding with cache hit."""
        import json
        cached_embedding = [0.2] * 1536
        mock_cache.get = AsyncMock(return_value=json.dumps(cached_embedding))
        
        config = EmbeddingConfig(
            provider=EmbeddingProvider.OPENAI,
            model="text-embedding-ada-002",
            dimension=1536
        )
        
        with patch.object(EmbeddingService, 'PROVIDER_MAP') as mock_map:
            mock_provider = MagicMock()
            mock_provider.return_value.dimension = 1536
            mock_map.get = MagicMock(return_value=mock_provider)
            
            service = EmbeddingService(config, cache_client=mock_cache)
            result = await service.embed("test text")
            
            assert result == cached_embedding
            assert service.get_stats()["cache_hits"] == 1


class TestVectorSearchQueryBuilder:
    """Tests for VectorSearchQueryBuilder."""

    def test_basic_query(self):
        """Test building a basic query."""
        vector = [0.1] * 1536
        query = (
            VectorSearchQueryBuilder()
            .with_vector(vector)
            .with_top_k(5)
            .build()
        )
        
        assert query.vector == vector
        assert query.top_k == 5

    def test_query_with_filters(self):
        """Test building a query with filters."""
        vector = [0.1] * 1536
        query = (
            VectorSearchQueryBuilder()
            .with_vector(vector)
            .filter_eq("agent_id", "agent1")
            .filter_gte("importance", 0.5)
            .filter_in("type", ["episodic", "semantic"])
            .build()
        )
        
        assert len(query.filters) == 3
        assert query.filters[0].field == "agent_id"
        assert query.filters[0].operator == FilterOperator.EQ

    def test_query_with_return_fields(self):
        """Test building a query with custom return fields."""
        vector = [0.1] * 1536
        query = (
            VectorSearchQueryBuilder()
            .with_vector(vector)
            .with_return_fields(["content", "summary", "timestamp"])
            .with_scores(True)
            .with_vectors(False)
            .build()
        )
        
        assert "summary" in query.return_fields
        assert query.include_scores is True
        assert query.include_vectors is False

    def test_query_without_vector_raises(self):
        """Test that building without vector raises error."""
        with pytest.raises(ValueError, match="Query vector is required"):
            VectorSearchQueryBuilder().with_top_k(5).build()


class TestVectorSearchExecutor:
    """Tests for VectorSearchExecutor."""

    @pytest.fixture
    def mock_redis(self):
        """Create mock Redis client."""
        client = AsyncMock()
        mock_ft = AsyncMock()
        mock_ft.search = AsyncMock()
        client.ft = MagicMock(return_value=mock_ft)
        return client

    @pytest.fixture
    def executor(self, mock_redis):
        """Create VectorSearchExecutor instance."""
        return VectorSearchExecutor(mock_redis, "idx:test")

    def test_build_filter_string_empty(self, executor):
        """Test building empty filter string."""
        result = executor._build_filter_string([])
        assert result == "*"

    def test_build_filter_string_eq(self, executor):
        """Test building equality filter string."""
        filters = [FilterCondition("agent_id", FilterOperator.EQ, "agent1")]
        result = executor._build_filter_string(filters)
        assert "@agent_id:{agent1}" in result

    def test_build_filter_string_numeric(self, executor):
        """Test building numeric filter string."""
        filters = [FilterCondition("importance", FilterOperator.GE, 0.5)]
        result = executor._build_filter_string(filters)
        assert "@importance:[0.5 +inf]" in result

    def test_vector_to_bytes(self, executor):
        """Test vector to bytes conversion."""
        vector = [1.0, 2.0, 3.0]
        result = executor._vector_to_bytes(vector)
        
        import struct
        expected = struct.pack("3f", 1.0, 2.0, 3.0)
        assert result == expected

    @pytest.mark.asyncio
    async def test_similarity_search(self, executor, mock_redis):
        """Test similarity search."""
        mock_result = MagicMock()
        mock_result.docs = []
        mock_redis.ft().search = AsyncMock(return_value=mock_result)
        
        results = await executor.similarity_search(
            vector=[0.1] * 1536,
            top_k=5,
            min_score=0.5
        )
        
        assert isinstance(results, list)


class TestSemanticMemorySearch:
    """Tests for SemanticMemorySearch."""

    @pytest.fixture
    def mock_redis(self):
        """Create mock Redis client."""
        client = AsyncMock()
        mock_ft = AsyncMock()
        mock_ft.search = AsyncMock(return_value=MagicMock(docs=[]))
        client.ft = MagicMock(return_value=mock_ft)
        return client

    @pytest.fixture
    def mock_embedding_service(self):
        """Create mock embedding service."""
        service = AsyncMock()
        service.embed = AsyncMock(return_value=[0.1] * 1536)
        return service

    @pytest.fixture
    def memory_search(self, mock_redis, mock_embedding_service):
        """Create SemanticMemorySearch instance."""
        return SemanticMemorySearch(mock_redis, mock_embedding_service)

    @pytest.mark.asyncio
    async def test_search_basic(self, memory_search, mock_embedding_service):
        """Test basic semantic search."""
        results = await memory_search.search("test query", top_k=5)
        
        mock_embedding_service.embed.assert_called_once()
        assert isinstance(results, list)

    @pytest.mark.asyncio
    async def test_search_with_filters(self, memory_search):
        """Test search with filters."""
        results = await memory_search.search(
            query="test query",
            agent_id="agent1",
            memory_type="episodic",
            min_importance=0.5
        )
        
        assert isinstance(results, list)

    @pytest.mark.asyncio
    async def test_get_context(self, memory_search):
        """Test getting context for LLM."""
        context = await memory_search.get_context(
            query="test query",
            max_tokens=1000,
            agent_id="agent1"
        )
        
        assert isinstance(context, str)


class TestFilterCondition:
    """Tests for FilterCondition."""

    def test_filter_condition_creation(self):
        """Test creating filter conditions."""
        condition = FilterCondition("field", FilterOperator.EQ, "value")
        assert condition.field == "field"
        assert condition.operator == FilterOperator.EQ
        assert condition.value == "value"

    def test_filter_operators(self):
        """Test all filter operators."""
        operators = [
            FilterOperator.EQ,
            FilterOperator.NE,
            FilterOperator.GT,
            FilterOperator.GE,
            FilterOperator.LT,
            FilterOperator.LE,
            FilterOperator.IN,
            FilterOperator.CONTAINS,
        ]
        assert len(operators) == 8


class TestSearchResult:
    """Tests for SearchResult."""

    def test_search_result_creation(self):
        """Test creating search results."""
        result = SearchResult(
            doc_id="doc1",
            score=0.95,
            content="Test content",
            metadata={"type": "test"}
        )
        assert result.doc_id == "doc1"
        assert result.score == 0.95
        assert result.content == "Test content"
        assert result.metadata["type"] == "test"

    def test_search_result_with_vector(self):
        """Test search result with vector."""
        vector = [0.1] * 1536
        result = SearchResult(
            doc_id="doc1",
            score=0.9,
            content="Test",
            vector=vector
        )
        assert result.vector == vector


class TestDefaultConfigs:
    """Tests for default configurations."""

    def test_default_memory_index(self):
        """Test default memory index config."""
        assert DEFAULT_MEMORY_INDEX.name == "idx:memory"
        assert DEFAULT_MEMORY_INDEX.prefix == "memory:"
        assert "content" in DEFAULT_MEMORY_INDEX.text_fields
        assert "agent_id" in DEFAULT_MEMORY_INDEX.tag_fields

    def test_distance_metrics(self):
        """Test distance metric enum values."""
        assert DistanceMetric.COSINE.value == "COSINE"
        assert DistanceMetric.L2.value == "L2"
        assert DistanceMetric.IP.value == "IP"

    def test_vector_algorithms(self):
        """Test vector algorithm enum values."""
        assert VectorAlgorithm.FLAT.value == "FLAT"
        assert VectorAlgorithm.HNSW.value == "HNSW"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
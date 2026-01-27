"""Unit tests for EmbeddingService."""
import pytest
import unittest
from unittest.mock import Mock, MagicMock, AsyncMock, patch
import asyncio
from unittest.mock import Mock, AsyncMock

from adk.plugins.memory_plugins.embedding_service import (
    EmbeddingService,
    EmbeddingConfig,
    EmbeddingProvider,
)


class TestEmbeddingService:
class TestEmbeddingService(unittest.IsolatedAsyncioTestCase):
    """Test cases for EmbeddingService."""

    @pytest.fixture
    def config(self):
        """Create test configuration."""
        return EmbeddingConfig(
            provider=EmbeddingProvider.OPENAI,
            model="text-embedding-ada-002",
            dimension=1536,
            api_key="test-key"
        )
        self.service = EmbeddingService(self.config, cache_client=None)
        self.service = EmbeddingService(self.config, None)

    @pytest.fixture
    def service(self, config):
        """Create EmbeddingService instance."""
        return EmbeddingService(config, None)

    def test_init(self, service):
        """Test initialization."""
        assert service.config.provider == EmbeddingProvider.OPENAI
        assert service.config.model == "text-embedding-ada-002"

    @pytest.mark.asyncio
    async def test_embed_text(self, service):
    async def test_embed_text(self):
        """Test embedding generation with mock."""
        # Mock the provider's embed_text method using AsyncMock
        # Mock the provider's embed_text method
        mock_provider = Mock()
        mock_provider.embed_text = AsyncMock(return_value=[0.1, 0.2, 0.3])
        
        service._provider = mock_provider
        
        # Run async test
        result = await service.embed("test text")
        
        assert result == [0.1, 0.2, 0.3]
        result = await self.service.embed("test text")
        
        # Verify the result
        self.assertEqual(result, [0.1, 0.2, 0.3])
        # Verify that embed_text was called with the correct argument
        mock_provider.embed_text.assert_called_once_with("test text")

    def test_get_stats(self, service):
        """Test getting service statistics."""
        stats = service.get_stats()
        
        # Check that stats dictionary has expected keys
        assert "total_requests" in stats
        assert "cache_hits" in stats
        assert "cache_misses" in stats
        assert "total_tokens" in stats


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
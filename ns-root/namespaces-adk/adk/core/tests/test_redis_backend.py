"""
Tests for Redis Memory Backend.

GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module ns-root/namespaces-adk/adk/core/tests
@gl-semantic-anchor GL-00-TESTS_REDIS_BACKEND
@gl-evidence-required false
GL Unified Charter Activated
"""

import asyncio
import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import sys
sys.path.insert(0, str(__file__).rsplit("/", 4)[0])

from adk.core.memory_manager import MemoryEntry, MemoryQuery, MemoryType


class TestRedisMemoryBackend:
    """Test cases for RedisMemoryBackend."""

    @pytest.fixture
    def mock_redis(self):
        """Create mock Redis client."""
        mock = AsyncMock()
        mock.ping = AsyncMock(return_value=True)
        mock.json = MagicMock(return_value=AsyncMock())
        mock.ft = MagicMock(return_value=AsyncMock())
        mock.exists = AsyncMock(return_value=True)
        mock.delete = AsyncMock(return_value=1)
        mock.expire = AsyncMock(return_value=True)
        return mock

    @pytest.mark.asyncio
    async def test_add_entry(self, mock_redis):
        """Test adding a memory entry."""
        with patch("redis.asyncio.Redis", return_value=mock_redis):
            from adk.plugins.memory_plugins.redis_backend import RedisMemoryBackend

            backend = RedisMemoryBackend()
            backend._client = mock_redis

            entry = MemoryEntry(
                id="test-123",
                content="Test content",
                memory_type=MemoryType.LONG_TERM,
                session_id="session-1",
            )

            result = await backend.add(entry)
            assert result == "test-123"
            mock_redis.json().set.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_entry(self, mock_redis):
        """Test getting a memory entry."""
        mock_redis.json().get = AsyncMock(
            return_value={
                "id": "test-123",
                "content": "Test content",
                "memory_type": "long_term",
                "session_id": "session-1",
                "user_id": None,
                "metadata": {},
                "embedding": None,
                "created_at": datetime.now().timestamp(),
                "updated_at": datetime.now().timestamp(),
                "importance": 1.0,
                "access_count": 0,
            }
        )

        with patch("redis.asyncio.Redis", return_value=mock_redis):
            from adk.plugins.memory_plugins.redis_backend import RedisMemoryBackend

            backend = RedisMemoryBackend()
            backend._client = mock_redis

            result = await backend.get("test-123")
            assert result is not None
            assert result.id == "test-123"
            assert result.content == "Test content"

    @pytest.mark.asyncio
    async def test_delete_entry(self, mock_redis):
        """Test deleting a memory entry."""
        with patch("redis.asyncio.Redis", return_value=mock_redis):
            from adk.plugins.memory_plugins.redis_backend import RedisMemoryBackend

            backend = RedisMemoryBackend()
            backend._client = mock_redis

            result = await backend.delete("test-123")
            assert result is True
            mock_redis.delete.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
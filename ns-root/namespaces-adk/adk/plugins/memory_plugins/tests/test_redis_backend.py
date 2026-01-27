"""Unit tests for RedisMemoryBackend."""
import unittest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import asyncio
from dataclasses import dataclass
from typing import Any, Dict, Optional
import sys
import os

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

# Mock all external dependencies before any imports
sys.modules['redis'] = MagicMock()
sys.modules['redis.asyncio'] = MagicMock()
sys.modules['redis.commands'] = MagicMock()
sys.modules['redis.commands.search'] = MagicMock()
sys.modules['redis.commands.search.field'] = MagicMock()
sys.modules['redis.commands.search.indexDefinition'] = MagicMock()
sys.modules['redis.commands.search.query'] = MagicMock()
sys.modules['networkx'] = MagicMock()
sys.modules['openai'] = MagicMock()
sys.modules['aiohttp'] = MagicMock()
sys.modules['anthropic'] = MagicMock()

# Import only the specific module we need
from unittest.mock import Mock, AsyncMock, MagicMock, patch
import asyncio
from datetime import datetime

from adk.core.memory_manager import MemoryEntry, MemoryQuery, MemoryType
from adk.plugins.memory_plugins.redis_backend import RedisMemoryBackend
from adk.core.memory_manager import MemoryEntry, MemoryQuery, MemoryType

from adk.plugins.memory_plugins.redis_backend import RedisMemoryBackend
from adk.core.memory_manager import MemoryEntry, MemoryQuery


class TestRedisBackend(unittest.TestCase):
    """Test cases for RedisMemoryBackend."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_redis = Mock()
        # RedisMemoryBackend doesn't accept redis_client parameter
        # The Redis client is created internally during initialize()
        # For testing, we create the backend and inject the mock client
        self.backend = RedisMemoryBackend()
        self.backend._client = self.mock_redis
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        # Mock Redis client and its methods
        self.mock_redis = AsyncMock()
        self.mock_json = AsyncMock()
        self.mock_ft = AsyncMock()
        
        # Set up the mock chain for Redis JSON operations
        self.mock_redis.json.return_value = self.mock_json
        self.mock_redis.ft.return_value = self.mock_ft
        
        # Create backend with mocked Redis client
        with patch('adk.plugins.memory_plugins.redis_backend.REDIS_AVAILABLE', True):
            self.backend = RedisMemoryBackend(host="localhost", port=6379)
            self.backend._client = self.mock_redis

    def tearDown(self):
        """Tear down test fixtures."""
        self.loop.close()

    def test_init(self):
        """Test initialization."""
        self.assertIsNotNone(self.backend)
        self.assertEqual(self.backend.host, "localhost")
        self.assertEqual(self.backend.port, 6379)

    def test_add(self):
        """Test adding a memory entry."""
        # Mock Redis JSON set and expire
        self.mock_json.set = AsyncMock(return_value=True)
        self.mock_redis.expire = AsyncMock(return_value=True)
        
        entry = MemoryEntry(
            id="mem1",
            content="test content",
            metadata={"key": "value"},
            memory_type=MemoryType.SHORT_TERM,
            session_id="session1",
            user_id="user1"
            memory_type=MemoryType.LONG_TERM
        )
        
        result = self.loop.run_until_complete(self.backend.add(entry))
        
        # Verify the entry ID is returned
        self.assertEqual(result, "mem1")
        
        # Verify Redis JSON set was called with correct parameters
        self.mock_json.set.assert_called_once()
        call_args = self.mock_json.set.call_args
        self.assertEqual(call_args[0][0], "memory:mem1")  # key
        self.assertEqual(call_args[0][1], "$")  # path
        
        # Verify expire was called for TTL
        self.mock_redis.expire.assert_called_once()

    def test_get(self):
        """Test getting a memory entry."""
        # Mock Redis JSON get and numincrby
        mock_data = {
            "id": "mem1",
            "content": "test content",
            "metadata": {"key": "value"},
            "embedding": None,
            "memory_type": "short_term",
            "session_id": "session1",
            "user_id": "user1",
            "created_at": datetime.now().timestamp(),
            "updated_at": datetime.now().timestamp(),
            "importance": 1.0,
            "access_count": 0
        }
        self.mock_json.get = AsyncMock(return_value=mock_data)
        self.mock_json.numincrby = AsyncMock(return_value=1)
        """Test getting a memory."""
        # Mock the async get method
        mock_entry = MemoryEntry(
            id="mem1",
        """Test initialization with correct constructor parameters."""
        # RedisMemoryBackend accepts host, port, db, prefix, vector_dim, etc.
        # It does NOT accept redis_client as a parameter
        backend = RedisMemoryBackend(
            host="localhost",
            port=6379,
            db=0,
            prefix="test:",
            vector_dim=1536
        )
        
        self.assertIsNotNone(backend)
        self.assertEqual(backend.prefix, "test:")
        self.assertEqual(backend.vector_dim, 1536)
        self.assertEqual(backend.host, "localhost")
        self.assertEqual(backend.port, 6379)

    def test_memory_entry_creation(self):
        """Test that MemoryEntry can be created with correct fields."""
        # This validates we're using the real MemoryEntry from core.memory_manager
        entry = MemoryEntry(
            id="test123",
            content="test content",
            metadata={"key": "value"},
            memory_type=MemoryType.LONG_TERM
        )
        
        result = self.loop.run_until_complete(self.backend.get("mem1"))
        
        # Verify result
        self.assertIsNotNone(result)
        self.assertEqual(result.id, "mem1")
        self.assertEqual(result.content, "test content")
        
        # Verify Redis get was called
        self.mock_json.get.assert_called_once_with("memory:mem1")
        
        # Verify access count was incremented
        self.mock_json.numincrby.assert_called_once_with("memory:mem1", "$.access_count", 1)

    def test_get_not_found(self):
        """Test getting a non-existent memory."""
        # Mock Redis JSON get to return None
        self.mock_json.get = AsyncMock(return_value=None)
        
        result = self.loop.run_until_complete(self.backend.get("nonexistent"))
        
        # Verify result is None
        self.assertIsNone(result)
        
        # Verify Redis get was called
        self.mock_json.get.assert_called_once_with("memory:nonexistent")

    def test_update(self):
        """Test updating a memory entry."""
        # Mock Redis exists and JSON set
        self.mock_redis.exists = AsyncMock(return_value=1)
        self.mock_json.set = AsyncMock(return_value=True)
        
        updates = {"content": "updated content"}
        result = self.loop.run_until_complete(
            self.backend.update("mem1", updates)
        )
        
        # Verify result
        self.assertTrue(result)
        
        # Verify exists was called
        self.mock_redis.exists.assert_called_once_with("memory:mem1")
        
        # Verify JSON set was called for each update field (content + updated_at)
        self.assertGreaterEqual(self.mock_json.set.call_count, 2)

    def test_update_not_found(self):
        """Test updating a non-existent memory."""
        # Mock Redis exists to return 0
        self.mock_redis.exists = AsyncMock(return_value=0)
        
        result = self.loop.run_until_complete(
            self.backend.update("nonexistent", {"content": "new"})
        )
        
        # Verify result is False
        self.assertFalse(result)
        
        # Verify exists was called
        self.mock_redis.exists.assert_called_once_with("memory:nonexistent")

    def test_delete(self):
        """Test deleting a memory entry."""
        # Mock Redis delete
        self.mock_redis.delete = AsyncMock(return_value=1)
        
        result = self.loop.run_until_complete(self.backend.delete("mem1"))
        
        # Verify result
        self.assertTrue(result)
        
        # Verify Redis delete was called
        self.mock_redis.delete.assert_called_once_with("memory:mem1")

    def test_delete_not_found(self):
        """Test deleting a non-existent memory."""
        # Mock Redis delete to return 0
        self.mock_redis.delete = AsyncMock(return_value=0)
        
        result = self.loop.run_until_complete(self.backend.delete("nonexistent"))
        
        # Verify result is False
        self.assertFalse(result)

    def test_query_basic(self):
        """Test basic query without vector search."""
        # Mock Redis FT search
        mock_doc = Mock()
        mock_doc.id = "memory:mem1"
        
        mock_results = Mock()
        mock_results.docs = [mock_doc]
        
        self.mock_ft.search = AsyncMock(return_value=mock_results)
        
        # Mock JSON get for fetching full entry data
        mock_data = {
            "id": "mem1",
            "content": "test content",
            "metadata": {},
            "embedding": None,
            "memory_type": "short_term",
            "session_id": "session1",
            "user_id": "user1",
            "created_at": datetime.now().timestamp(),
            "updated_at": datetime.now().timestamp(),
            "importance": 1.0,
            "access_count": 0
        }
        self.mock_json.get = AsyncMock(return_value=mock_data)
    def test_query(self):
        """Test querying memories."""
        # Mock the async query method
        mock_entries = [
            MemoryEntry(
                id="mem1",
                content="test content",
                memory_type=MemoryType.LONG_TERM
            )
        ]
        self.backend.query = AsyncMock(return_value=mock_entries)
        
        query = MemoryQuery(query_text="test", limit=10)
        results = self.loop.run_until_complete(self.backend.query(query))
        
        # Verify results
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, "mem1")
        
        # Verify search was called
        self.mock_ft.search.assert_called_once()

    def test_get_ttl_short_term(self):
        """Test TTL calculation for short-term memory."""
        ttl = self.backend._get_ttl(MemoryType.SHORT_TERM, 0.5)
        # Short-term: 3600 * (1 + 3 * 0.5) = 3600 * 2.5 = 9000
        self.assertEqual(ttl, 9000)

    def test_get_ttl_long_term(self):
        """Test TTL calculation for long-term memory."""
        ttl = self.backend._get_ttl(MemoryType.LONG_TERM, 0.5)
        # Long-term: 86400 * (1 + 29 * 0.5) = 86400 * 15.5 = 1339200
        self.assertEqual(ttl, 1339200)
        self.assertGreater(len(results), 0)
        self.assertEqual(entry.id, "test123")
        self.assertEqual(entry.content, "test content")
        self.assertEqual(entry.metadata["key"], "value")

    def test_memory_query_creation(self):
        """Test that MemoryQuery can be created with correct fields."""
        # This validates we're using the real MemoryQuery from core.memory_manager
        query = MemoryQuery(
            query_text="test query",
            limit=5,
            threshold=0.8
        )
        
        self.assertEqual(query.query_text, "test query")
        self.assertEqual(query.limit, 5)
        self.assertEqual(query.threshold, 0.8)


if __name__ == "__main__":
    unittest.main()
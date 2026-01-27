"""
Unit tests for MemoryManager.

Tests for critical functionality to ensure code quality and reliability.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import sys
from pathlib import Path

# Add the module to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

try:
    from adk.plugins.memory_plugins.memory_manager import MemoryManager
    from adk.plugins.memory_plugins.redis_backend import RedisBackend
except ImportError as e:
    pytest.skip(f"Could not import memory_manager module: {e}", allow_module_level=True)


class TestMemoryManager:
    """Test cases for MemoryManager"""

    def setup_method(self):
        """Set up test fixtures"""
        self.mock_backend = Mock(spec=RedisBackend)
        self.memory_manager = MemoryManager(backend=self.mock_backend)

    def teardown_method(self):
        """Tear down test fixtures"""
        pass

    def test_initialization(self):
        """Test that MemoryManager initializes correctly"""
        assert self.memory_manager is not None
        assert self.memory_manager.backend == self.mock_backend

    def test_add_memory(self):
        """Test adding a memory entry"""
        # Mock the backend add operation
        self.mock_backend.add.return_value = "test_memory_id"
        
        memory_data = {
            "content": "Test memory content",
            "metadata": {"source": "test"},
            "timestamp": datetime.now().isoformat()
        }
        
        result = self.memory_manager.add_memory(memory_data)
        
        assert result == "test_memory_id"
        self.mock_backend.add.assert_called_once()

    def test_get_memory(self):
        """Test retrieving a memory entry"""
        # Mock the backend get operation
        expected_memory = {
            "id": "test_id",
            "content": "Test content",
            "metadata": {}
        }
        self.mock_backend.get.return_value = expected_memory
        
        result = self.memory_manager.get_memory("test_id")
        
        assert result == expected_memory
        self.mock_backend.get.assert_called_once_with("test_id")

    def test_get_memory_not_found(self):
        """Test retrieving a non-existent memory entry"""
        self.mock_backend.get.return_value = None
        
        result = self.memory_manager.get_memory("non_existent_id")
        
        assert result is None
        self.mock_backend.get.assert_called_once_with("non_existent_id")

    def test_update_memory(self):
        """Test updating a memory entry"""
        # Mock the backend update operation
        self.mock_backend.update.return_value = True
        
        update_data = {
            "content": "Updated content"
        }
        
        result = self.memory_manager.update_memory("test_id", update_data)
        
        assert result is True
        self.mock_backend.update.assert_called_once()

    def test_delete_memory(self):
        """Test deleting a memory entry"""
        # Mock the backend delete operation
        self.mock_backend.delete.return_value = True
        
        result = self.memory_manager.delete_memory("test_id")
        
        assert result is True
        self.mock_backend.delete.assert_called_once_with("test_id")

    def test_list_memories(self):
        """Test listing memory entries"""
        # Mock the backend list operation
        expected_memories = [
            {"id": "id1", "content": "Content 1"},
            {"id": "id2", "content": "Content 2"}
        ]
        self.mock_backend.list.return_value = expected_memories
        
        result = self.memory_manager.list_memories(limit=10)
        
        assert result == expected_memories
        self.mock_backend.list.assert_called_once()

    def test_search_memories(self):
        """Test searching memory entries"""
        # Mock the backend search operation
        expected_results = [
            {"id": "id1", "content": "Matching content", "score": 0.95}
        ]
        self.mock_backend.search.return_value = expected_results
        
        result = self.memory_manager.search_memories("search query", limit=5)
        
        assert result == expected_results
        self.mock_backend.search.assert_called_once()

    def test_get_memory_stats(self):
        """Test getting memory statistics"""
        # Mock the backend stats operation
        expected_stats = {
            "total_memories": 100,
            "total_size": 1024000,
            "oldest_memory": "2024-01-01T00:00:00",
            "newest_memory": "2024-01-27T12:00:00"
        }
        self.mock_backend.get_stats.return_value = expected_stats
        
        result = self.memory_manager.get_memory_stats()
        
        assert result == expected_stats
        self.mock_backend.get_stats.assert_called_once()

    def test_add_memory_with_error(self):
        """Test error handling when adding memory fails"""
        # Mock the backend to raise an exception
        self.mock_backend.add.side_effect = Exception("Backend error")
        
        memory_data = {"content": "Test content"}
        
        with pytest.raises(Exception):
            self.memory_manager.add_memory(memory_data)

    def test_get_memory_with_invalid_id(self):
        """Test retrieving memory with invalid ID"""
        self.mock_backend.get.side_effect = ValueError("Invalid ID format")
        
        with pytest.raises(ValueError):
            self.memory_manager.get_memory("invalid_id")

    def test_bulk_add_memories(self):
        """Test adding multiple memories in bulk"""
        # Mock the backend bulk add operation
        self.mock_backend.bulk_add.return_value = ["id1", "id2", "id3"]
        
        memories = [
            {"content": "Memory 1"},
            {"content": "Memory 2"},
            {"content": "Memory 3"}
        ]
        
        result = self.memory_manager.bulk_add_memories(memories)
        
        assert result == ["id1", "id2", "id3"]
        self.mock_backend.bulk_add.assert_called_once()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
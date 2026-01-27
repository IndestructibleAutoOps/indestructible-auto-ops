"""
Unit tests for MemoryCompactor.

Tests for memory compaction functionality including various
compaction strategies and rules.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add the module to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

try:
    from adk.plugins.memory_plugins.memory_compactor import (
        MemoryCompactor,
        CompactionStrategy,
        CompactionRule
    )
    from adk.plugins.memory_plugins.memory_manager import MemoryManager
except ImportError as e:
    pytest.skip(f"Could not import memory_compactor module: {e}", allow_module_level=True)


class TestMemoryCompactor:
    """Test cases for MemoryCompactor"""

    def setup_method(self):
        """Set up test fixtures"""
        self.mock_memory_manager = Mock(spec=MemoryManager)
        self.compactor = MemoryCompactor(memory_manager=self.mock_memory_manager)

    def teardown_method(self):
        """Tear down test fixtures"""
        pass

    def test_initialization(self):
        """Test that MemoryCompactor initializes correctly"""
        assert self.compactor is not None
        assert self.compactor.memory_manager == self.mock_memory_manager

    def test_compact_with_summary_strategy(self):
        """Test compaction using LLM summarization strategy"""
        # Mock memory manager operations
        self.mock_memory_manager.list_memories.return_value = [
            {"id": "mem1", "content": "Long content to summarize", "size": 5000},
            {"id": "mem2", "content": "Another long content", "size": 6000}
        ]
        self.mock_memory_manager.update_memory.return_value = True
        
        result = self.compactor.compact(
            strategy=CompactionStrategy.SUMMARIZATION,
            max_size=3000
        )
        
        assert result is not None
        assert "compacted_count" in result

    def test_compact_with_statistical_strategy(self):
        """Test compaction using statistical strategy"""
        # Mock memory manager operations
        self.mock_memory_manager.list_memories.return_value = [
            {"id": "mem1", "content": "Data", "access_count": 10},
            {"id": "mem2", "content": "Data", "access_count": 5}
        ]
        self.mock_memory_manager.delete_memory.return_value = True
        
        result = self.compactor.compact(
            strategy=CompactionStrategy.STATISTICAL,
            threshold=0.3
        )
        
        assert result is not None
        assert "compacted_count" in result

    def test_compact_with_temporal_strategy(self):
        """Test compaction using temporal windowing strategy"""
        # Mock memory manager operations
        old_date = (datetime.now() - timedelta(days=90)).isoformat()
        recent_date = datetime.now().isoformat()
        
        self.mock_memory_manager.list_memories.return_value = [
            {"id": "mem1", "timestamp": old_date},
            {"id": "mem2", "timestamp": recent_date}
        ]
        self.mock_memory_manager.delete_memory.return_value = True
        
        result = self.compactor.compact(
            strategy=CompactionStrategy.TEMPORAL,
            days_threshold=60
        )
        
        assert result is not None
        assert "compacted_count" in result

    def test_compact_with_importance_strategy(self):
        """Test compaction using importance priority strategy"""
        # Mock memory manager operations
        self.mock_memory_manager.list_memories.return_value = [
            {"id": "mem1", "importance": 0.9},
            {"id": "mem2", "importance": 0.3}
        ]
        self.mock_memory_manager.delete_memory.return_value = True
        
        result = self.compactor.compact(
            strategy=CompactionStrategy.IMPORTANCE,
            min_importance=0.5
        )
        
        assert result is not None
        assert "compacted_count" in result

    def test_compact_with_hybrid_strategy(self):
        """Test compaction using hybrid strategy"""
        # Mock memory manager operations
        self.mock_memory_manager.list_memories.return_value = [
            {
                "id": "mem1",
                "size": 10000,
                "access_count": 2,
                "timestamp": (datetime.now() - timedelta(days=100)).isoformat(),
                "importance": 0.2
            }
        ]
        self.mock_memory_manager.update_memory.return_value = True
        self.mock_memory_manager.delete_memory.return_value = True
        
        result = self.compactor.compact(
            strategy=CompactionStrategy.HYBRID,
            max_size=5000,
            min_access_count=5
        )
        
        assert result is not None
        assert "compacted_count" in result

    def test_get_compaction_stats(self):
        """Test getting compaction statistics"""
        # Mock stats
        expected_stats = {
            "total_compactions": 10,
            "total_memory_saved": 500000,
            "average_compaction_ratio": 0.4,
            "last_compaction": datetime.now().isoformat()
        }
        self.mock_memory_manager.get_memory_stats.return_value = expected_stats
        
        stats = self.compactor.get_stats()
        
        assert stats is not None
        assert "total_compactions" in stats

    def test_compact_with_rule(self):
        """Test compaction with custom rule"""
        # Create a custom rule
        rule = CompactionRule(
            name="large_files",
            condition=lambda mem: mem.get("size", 0) > 10000,
            action="delete"
        )
        
        # Mock memory manager operations
        self.mock_memory_manager.list_memories.return_value = [
            {"id": "mem1", "size": 15000},
            {"id": "mem2", "size": 5000}
        ]
        self.mock_memory_manager.delete_memory.return_value = True
        
        result = self.compactor.compact_with_rules([rule])
        
        assert result is not None
        assert "compacted_count" in result

    def test_compact_by_token_threshold(self):
        """Test compaction by token threshold"""
        # Mock memory manager operations
        self.mock_memory_manager.list_memories.return_value = [
            {"id": "mem1", "token_count": 2000},
            {"id": "mem2", "token_count": 3000}
        ]
        self.mock_memory_manager.update_memory.return_value = True
        
        result = self.compactor.compact_by_tokens(max_tokens=1500)
        
        assert result is not None
        assert "compacted_count" in result

    def test_compact_error_handling(self):
        """Test error handling during compaction"""
        # Mock memory manager to raise an exception
        self.mock_memory_manager.list_memories.side_effect = Exception("Memory error")
        
        with pytest.raises(Exception):
            self.compactor.compact(strategy=CompactionStrategy.SUMMARIZATION)

    def test_auto_compact(self):
        """Test automatic compaction based on memory usage"""
        # Mock memory manager operations
        self.mock_memory_manager.get_memory_stats.return_value = {
            "total_memories": 1000,
            "total_size": 10485760,  # 10MB
            "memory_usage_percent": 85
        }
        self.mock_memory_manager.list_memories.return_value = []
        self.mock_memory_manager.delete_memory.return_value = True
        
        result = self.compactor.auto_compact(
            threshold_percent=80,
            target_percent=60
        )
        
        assert result is not None
        assert "compacted" in result

    def test_get_compaction_recommendations(self):
        """Test getting compaction recommendations"""
        # Mock memory manager operations
        self.mock_memory_manager.get_memory_stats.return_value = {
            "total_memories": 500,
            "total_size": 5242880,
            "average_size": 10485
        }
        self.mock_memory_manager.list_memories.return_value = []
        
        recommendations = self.compactor.get_recommendations()
        
        assert recommendations is not None
        assert isinstance(recommendations, list)

    def test_compact_with_custom_strategy(self):
        """Test compaction with custom strategy function"""
        def custom_strategy(memories, **kwargs):
            # Custom logic: compress all memories
            return [mem for mem in memories], len(memories)
        
        # Mock memory manager operations
        self.mock_memory_manager.list_memories.return_value = [
            {"id": "mem1", "content": "Data"},
            {"id": "mem2", "content": "Data"}
        ]
        self.mock_memory_manager.update_memory.return_value = True
        
        result = self.compactor.compact(strategy=custom_strategy)
        
        assert result is not None

    def test_compact_dry_run(self):
        """Test compaction in dry-run mode (no actual changes)"""
        # Mock memory manager operations
        self.mock_memory_manager.list_memories.return_value = [
            {"id": "mem1", "size": 10000},
            {"id": "mem2", "size": 5000}
        ]
        
        result = self.compactor.compact(
            strategy=CompactionStrategy.STATISTICAL,
            dry_run=True
        )
        
        assert result is not None
        assert "would_compact_count" in result
        # Ensure no actual delete was called
        self.mock_memory_manager.delete_memory.assert_not_called()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
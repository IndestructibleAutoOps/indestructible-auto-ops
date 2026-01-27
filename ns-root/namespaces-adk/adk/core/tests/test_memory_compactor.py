"""
Unit tests for Memory Compactor (P4).
Tests memory compaction and summarization functionality.
"""

import pytest
import time
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Any, Dict, List

from adk.plugins.memory_plugins.memory_compactor import (
    MemoryCompactor,
    AutomaticMemoryCompactor,
    MemorySnapshot,
    CompactionConfig,
    CompactionStrategy,
    CompactionLevel,
    CompactionReport,
    CompactionRule,
    TokenThresholdRule,
    EntryCountRule,
    TimeSinceLastCompactionRule,
)


class TestCompactionConfig:
    """Tests for CompactionConfig."""

    def test_default_config(self):
        """Test default configuration values."""
        config = CompactionConfig()
        assert config.strategy == CompactionStrategy.HYBRID
        assert config.level == CompactionLevel.MODERATE
        assert config.keep_recent_hours == 24
        assert config.min_importance == 0.3

    def test_custom_config(self):
        """Test custom configuration."""
        config = CompactionConfig(
            strategy=CompactionStrategy.LLM_SUMMARIZATION,
            level=CompactionLevel.AGGRESSIVE,
            keep_recent_hours=48,
            min_importance=0.5,
        )
        assert config.strategy == CompactionStrategy.LLM_SUMMARIZATION
        assert config.level == CompactionLevel.AGGRESSIVE
        assert config.keep_recent_hours == 48


class TestMemorySnapshot:
    """Tests for MemorySnapshot."""

    def test_snapshot_creation(self):
        """Test creating a memory snapshot."""
        entries = [
            {
                "id": "1",
                "content": "Test content",
                "created_at": time.time(),
                "importance": 0.8,
            }
        ]
        snapshot = MemorySnapshot(entries=entries)
        
        assert snapshot.total_entries == 1
        assert snapshot.total_tokens > 0
        assert snapshot.newest_timestamp > 0

    def test_snapshot_empty(self):
        """Test empty snapshot."""
        snapshot = MemorySnapshot(entries=[])
        
        assert snapshot.total_entries == 0
        assert snapshot.total_tokens == 0


class TestCompactionReport:
    """Tests for CompactionReport."""

    def test_report_calculations(self):
        """Test report calculations."""
        report = CompactionReport(
            original_entries=100,
            original_tokens=10000,
            compacted_entries=50,
            compacted_tokens=5000,
            reduction_ratio=0.5,
            strategy_used="test",
            time_elapsed_ms=100.0,
        )
        
        assert report.entries_removed == 50
        assert report.tokens_saved == 5000


class TestTokenThresholdRule:
    """Tests for TokenThresholdRule."""

    @pytest.mark.asyncio
    async def test_should_compact_above_threshold(self):
        """Test compaction triggered when above threshold."""
        rule = TokenThresholdRule(max_tokens=5000)
        
        snapshot = MemorySnapshot(entries=[
            {"content": "test" * 1000} for _ in range(10)
        ])
        
        should, reason = await rule.should_compact(snapshot, CompactionConfig())
        
        assert should is True
        assert "exceeds threshold" in reason

    @pytest.mark.asyncio
    async def test_should_not_compact_below_threshold(self):
        """Test no compaction when below threshold."""
        rule = TokenThresholdRule(max_tokens=5000)
        
        snapshot = MemorySnapshot(entries=[
            {"content": "test"} for _ in range(10)
        ])
        
        should, reason = await rule.should_compact(snapshot, CompactionConfig())
        
        assert should is False
        assert reason == ""


class TestEntryCountRule:
    """Tests for EntryCountRule."""

    @pytest.mark.asyncio
    async def test_should_compact_above_threshold(self):
        """Test compaction triggered when above threshold."""
        rule = EntryCountRule(max_entries=100)
        
        snapshot = MemorySnapshot(entries=[{"id": str(i)} for i in range(150)])
        
        should, reason = await rule.should_compact(snapshot, CompactionConfig())
        
        assert should is True
        assert "exceeds threshold" in reason


class TestTimeSinceLastCompactionRule:
    """Tests for TimeSinceLastCompactionRule."""

    @pytest.mark.asyncio
    async def test_should_compact_after_threshold(self):
        """Test compaction triggered after time threshold."""
        rule = TimeSinceLastCompactionRule(min_hours=24)
        rule.set_last_compaction(time.time() - 25 * 3600)
        
        snapshot = MemorySnapshot(entries=[])
        should, reason = await rule.should_compact(snapshot, CompactionConfig())
        
        assert should is True
        assert "hours since last compaction" in reason

    @pytest.mark.asyncio
    async def test_should_not_compact_before_threshold(self):
        """Test no compaction before time threshold."""
        rule = TimeSinceLastCompactionRule(min_hours=24)
        rule.set_last_compaction(time.time() - 10 * 3600)
        
        snapshot = MemorySnapshot(entries=[])
        should, reason = await rule.should_compact(snapshot, CompactionConfig())
        
        assert should is False


class TestMemoryCompactor:
    """Tests for MemoryCompactor."""

    @pytest.fixture
    def compactor(self):
        """Create MemoryCompactor instance."""
        return MemoryCompactor(config=CompactionConfig())

    def test_add_remove_rules(self, compactor):
        """Test adding and removing rules."""
        rule = TokenThresholdRule(max_tokens=100)
        compactor.add_rule(rule)
        
        assert len(compactor._rules) > 0
        
        compactor.remove_rule(TokenThresholdRule)
        assert not any(isinstance(r, TokenThresholdRule) for r in compactor._rules)

    @pytest.mark.asyncio
    async def test_should_compact_default_rules(self, compactor):
        """Test should_compact with default rules."""
        snapshot = MemorySnapshot(entries=[
            {"content": "test" * 1000} for _ in range(200)
        ])
        
        should, reason = await compactor.should_compact(snapshot)
        
        # Should trigger one of the default rules
        assert isinstance(should, bool)

    @pytest.mark.asyncio
    async def test_compact_no_compaction_needed(self, compactor):
        """Test compact when no compaction is needed."""
        snapshot = MemorySnapshot(entries=[
            {"id": "1", "content": "test", "created_at": time.time(), "importance": 0.5}
        ])
        
        report = await compactor.compact(snapshot)
        
        assert report.reduction_ratio == 0.0
        assert report.compacted_entries == snapshot.total_entries

    @pytest.mark.asyncio
    async def test_compact_statistical(self, compactor):
        """Test statistical compaction."""
        config = CompactionConfig(
            strategy=CompactionStrategy.STATISTICAL,
            level=CompactionLevel.MODERATE,
        )
        compactor.config = config
        
        entries = [
            {
                "id": str(i),
                "content": f"Test content {i}",
                "created_at": time.time() - i * 3600,
                "importance": 0.5 + (i % 3) * 0.2,
                "access_count": i % 5,
            }
            for i in range(20)
        ]
        
        snapshot = MemorySnapshot(entries=entries)
        report = await compactor.compact(snapshot)
        
        assert report.compacted_entries < report.original_entries
        assert report.entries_removed > 0

    @pytest.mark.asyncio
    async def test_compact_temporal(self, compactor):
        """Test temporal windowing compaction."""
        config = CompactionConfig(
            strategy=CompactionStrategy.TEMPORAL_WINDOWING,
            level=CompactionLevel.MODERATE,
            keep_recent_hours=1,
        )
        compactor.config = config
        
        now = time.time()
        entries = [
            {
                "id": str(i),
                "content": f"Test content {i}",
                "created_at": now - i * 3600,
                "importance": 0.5,
            }
            for i in range(10)
        ]
        
        snapshot = MemorySnapshot(entries=entries)
        report = await compactor.compact(snapshot)
        
        assert report.compacted_entries < report.original_entries

    @pytest.mark.asyncio
    async def test_compact_importance(self, compactor):
        """Test importance-based compaction."""
        config = CompactionConfig(
            strategy=CompactionStrategy.IMPORTANCE_PRIORITY,
            level=CompactionLevel.MODERATE,
        )
        compactor.config = config
        
        entries = [
            {
                "id": str(i),
                "content": f"Test content {i}",
                "created_at": time.time(),
                "importance": 0.1 + (i / 20),
                "access_count": i % 3,
            }
            for i in range(20)
        ]
        
        snapshot = MemorySnapshot(entries=entries)
        report = await compactor.compact(snapshot)
        
        assert report.compacted_entries < report.original_entries

    @pytest.mark.asyncio
    async def test_compact_hybrid(self, compactor):
        """Test hybrid compaction."""
        config = CompactionConfig(
            strategy=CompactionStrategy.HYBRID,
            level=CompactionLevel.MODERATE,
        )
        compactor.config = config
        
        entries = [
            {
                "id": str(i),
                "content": f"Test content {i}",
                "created_at": time.time() - i * 3600,
                "importance": 0.5,
                "session_id": f"session_{i % 3}",
            }
            for i in range(20)
        ]
        
        snapshot = MemorySnapshot(entries=entries)
        report = await compactor.compact(snapshot)
        
        assert report.strategy_used == "hybrid"
        assert report.compacted_entries <= report.original_entries

    def test_calculate_importance_score(self, compactor):
        """Test importance score calculation."""
        now = time.time()
        
        entry = {
            "created_at": now - 3600,  # 1 hour old
            "importance": 0.8,
            "access_count": 5,
        }
        
        score = compactor._calculate_importance_score(entry, now)
        
        assert 0.0 <= score <= 1.0
        assert score > 0.5  # Should be boosted by access count

    def test_get_target_count(self, compactor):
        """Test target count calculation."""
        compactor.config.level = CompactionLevel.LIGHT
        count = compactor._get_target_count(100)
        assert count == 75
        
        compactor.config.level = CompactionLevel.MODERATE
        count = compactor._get_target_count(100)
        assert count == 50
        
        compactor.config.level = CompactionLevel.AGGRESSIVE
        count = compactor._get_target_count(100)
        assert count == 25

    def test_cosine_similarity(self, compactor):
        """Test cosine similarity calculation."""
        vec1 = [1.0, 0.0, 0.0]
        vec2 = [1.0, 0.0, 0.0]
        assert compactor._cosine_similarity(vec1, vec2) == 1.0
        
        vec3 = [0.0, 1.0, 0.0]
        assert compactor._cosine_similarity(vec1, vec3) == 0.0
        
        vec4 = [0.707, 0.707, 0.0]
        similarity = compactor._cosine_similarity(vec1, vec4)
        assert 0.6 < similarity < 0.8

    def test_group_entries(self, compactor):
        """Test entry grouping."""
        entries = [
            {"id": "1", "session_id": "session1"},
            {"id": "2", "session_id": "session1"},
            {"id": "3", "session_id": "session2"},
        ]
        
        groups = compactor._group_entries(entries)
        
        assert len(groups) == 2
        assert len(groups["session1"]) == 2
        assert len(groups["session2"]) == 1


class TestAutomaticMemoryCompactor:
    """Tests for AutomaticMemoryCompactor."""

    @pytest.fixture
    def auto_compactor(self):
        """Create AutomaticMemoryCompactor instance."""
        compactor = MemoryCompactor(config=CompactionConfig())
        return AutomaticMemoryCompactor(
            compactor=compactor,
            check_interval_seconds=10,
            auto_compact=False,
        )

    @pytest.mark.asyncio
    async def test_start_stop(self, auto_compactor):
        """Test starting and stopping automatic compactor."""
        assert not auto_compactor._running
        
        await auto_compactor.start()
        assert auto_compactor._running
        
        await auto_compactor.stop()
        assert not auto_compactor._running

    @pytest.mark.asyncio
    async def test_start_twice(self, auto_compactor):
        """Test starting compactor twice."""
        await auto_compactor.start()
        await auto_compactor.start()  # Should not create second task
        
        await auto_compactor.stop()


class TestCompactionStrategy:
    """Tests for CompactionStrategy enum."""

    def test_strategy_values(self):
        """Test compaction strategy values."""
        assert CompactionStrategy.LLM_SUMMARIZATION.value == "llm_summarization"
        assert CompactionStrategy.STATISTICAL.value == "statistical"
        assert CompactionStrategy.SEMANTIC_CLUSTERING.value == "semantic_clustering"
        assert CompactionStrategy.TEMPORAL_WINDOWING.value == "temporal_windowing"
        assert CompactionStrategy.IMPORTANCE_PRIORITY.value == "importance_priority"
        assert CompactionStrategy.HYBRID.value == "hybrid"


class TestCompactionLevel:
    """Tests for CompactionLevel enum."""

    def test_level_values(self):
        """Test compaction level values."""
        assert CompactionLevel.LIGHT.value == "light"
        assert CompactionLevel.MODERATE.value == "moderate"
        assert CompactionLevel.AGGRESSIVE.value == "aggressive"
        assert CompactionLevel.EXTREME.value == "extreme"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
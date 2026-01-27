"""Unit tests for CacheOptimizer."""
import pytest
import time
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock

# Add the module to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from cache_optimizer import (
        CacheOptimizer, 
        OptimizationStrategy,
        AccessPattern
    )
except ImportError as e:
    pytest.skip(f"Could not import cache_optimizer module: {e}", allow_module_level=True)


class TestCacheOptimizer:
    """Test cases for CacheOptimizer."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_cache_layer = Mock()
        self.mock_cache_layer.l1_cache = {}
        self.mock_cache_layer.embedding_service = None
        self.optimizer = CacheOptimizer(
            cache_layer=self.mock_cache_layer,
            optimization_window=300,
            min_accesses_for_analysis=3
        )

    def test_initialization(self):
        """Test that optimizer initializes correctly."""
        assert self.optimizer is not None
        assert self.optimizer.cache_layer == self.mock_cache_layer
        assert self.optimizer.optimization_window == 300
        assert self.optimizer.min_accesses_for_analysis == 3
        assert len(self.optimizer.access_patterns) == 0

    def test_record_access(self):
        """Test recording cache access for pattern analysis."""
        key = "user:123"
        
        # Record multiple accesses
        self.optimizer.record_access(key)
        time.sleep(0.01)
        self.optimizer.record_access(key)
        time.sleep(0.01)
        self.optimizer.record_access(key)
        
        # Verify access pattern was recorded
        assert key in self.optimizer.access_patterns
        pattern = self.optimizer.access_patterns[key]
        assert pattern.key == key
        assert pattern.access_count == 3
        assert len(pattern.access_times) == 3
        assert pattern.last_accessed > 0

    def test_analyze_access_patterns_high_frequency(self):
        """Test analyzing high-frequency access patterns."""
        key = "hot_key"
        
        # Simulate high-frequency accesses
        for _ in range(50):
            self.optimizer.record_access(key)
            time.sleep(0.001)  # Very short intervals for high frequency
        
        # Analyze patterns
        recommendations = self.optimizer.analyze_access_patterns()
        
        # Should recommend promoting high-frequency key
        assert len(recommendations) > 0
        promote_recs = [r for r in recommendations if r.action == "promote"]
        assert any(r.key == key for r in promote_recs)

    def test_analyze_access_patterns_low_frequency(self):
        """Test analyzing low-frequency access patterns."""
        key = "cold_key"
        
        # Simulate low-frequency accesses (just meet minimum)
        for i in range(3):
            self.optimizer.record_access(key)
            if i < 2:
                time.sleep(100)  # Long intervals for low frequency (simulated)
        
        # Manually set very low frequency for testing
        self.optimizer.access_patterns[key].access_frequency = 0.0001
        
        # Analyze patterns
        recommendations = self.optimizer.analyze_access_patterns()
        
        # Should recommend evicting low-frequency key
        evict_recs = [r for r in recommendations if r.action == "evict"]
        assert any(r.key == key for r in evict_recs)

    def test_analyze_access_patterns_min_accesses(self):
        """Test that keys with insufficient accesses are not analyzed."""
        key = "new_key"
        
        # Record only 2 accesses (below minimum of 3)
        self.optimizer.record_access(key)
        self.optimizer.record_access(key)
        
        # Analyze patterns
        recommendations = self.optimizer.analyze_access_patterns()
        
        # Should not generate recommendations for keys below minimum
        assert not any(r.key == key for r in recommendations)

    def test_get_recommendations(self):
        """Test getting optimization recommendations."""
        # Set up some access patterns
        for _ in range(10):
            self.optimizer.record_access("frequent_key")
            time.sleep(0.001)
        
        # Get recommendations with default strategies
        recommendations = self.optimizer.get_recommendations()
        
        # Should return a list of recommendations
        assert isinstance(recommendations, list)
        # Recommendations should be sorted by priority
        if len(recommendations) > 1:
            for i in range(len(recommendations) - 1):
                assert recommendations[i].priority >= recommendations[i+1].priority

    def test_optimize_with_recommendations(self):
        """Test the optimize method generates and applies recommendations."""
        # Set up mock delete method
        self.mock_cache_layer.delete = Mock()
        
        # Create access patterns that will generate recommendations
        for _ in range(10):
            self.optimizer.record_access("test_key")
            time.sleep(0.001)
        
        # Run optimization
        result = self.optimizer.optimize()
        
        # Verify result structure
        assert "recommendations_count" in result
        assert "applied_count" in result
        assert "success_count" in result
        assert "success_rate" in result
        assert "applied_recommendations" in result
        assert isinstance(result["recommendations_count"], int)
        assert isinstance(result["applied_count"], int)

    def test_adaptive_ttl_recommendations(self):
        """Test adaptive TTL recommendations based on access frequency."""
        key = "ttl_test_key"
        
        # Record accesses to meet minimum
        for _ in range(5):
            self.optimizer.record_access(key)
        
        # Set specific frequency for testing
        self.optimizer.access_patterns[key].access_frequency = 0.06  # High frequency
        
        # Get adaptive TTL recommendations
        recommendations = self.optimizer.analyze_adaptive_ttl()
        
        # Should recommend TTL adjustment
        ttl_recs = [r for r in recommendations if r.key == key and r.action == "adjust_ttl"]
        assert len(ttl_recs) > 0
        # High frequency should get longer TTL
        assert ttl_recs[0].metadata["recommended_ttl"] == 7200  # 2 hours

    def test_get_stats(self):
        """Test getting optimizer statistics."""
        # Record some accesses
        self.optimizer.record_access("key1")
        self.optimizer.record_access("key2")
        
        stats = self.optimizer.get_stats()
        
        assert "tracked_keys" in stats
        assert stats["tracked_keys"] == 2
        assert "optimizations_applied" in stats
        assert "enabled_strategies" in stats
        assert "optimization_window" in stats

    def test_reset_tracking(self):
        """Test resetting access pattern tracking."""
        # Record some accesses
        self.optimizer.record_access("key1")
        self.optimizer.record_access("key2")
        
        assert len(self.optimizer.access_patterns) == 2
        
        # Reset tracking
        self.optimizer.reset_tracking()
        
        assert len(self.optimizer.access_patterns) == 0
        assert len(self.optimizer.semantic_clusters) == 0
        assert self.optimizer.cache_layer is self.mock_cache_layer

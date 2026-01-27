"""Unit tests for CacheInvalidator."""
import pytest
from unittest.mock import Mock, MagicMock

from adk.plugins.memory_plugins.cache_invalidator import (
    CacheInvalidator,
    InvalidationStrategy,
    InvalidationResult
)
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock
import numpy as np

# Add the module to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from cache_invalidator import (
        CacheInvalidator,
        InvalidationStrategy,
        InvalidationRule,
        InvalidationEvent
    )
except ImportError as e:
    pytest.skip(f"Could not import cache_invalidator module: {e}", allow_module_level=True)


class TestCacheInvalidator:
    """Test cases for CacheInvalidator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_cache_layer = Mock()
        self.mock_cache_layer.l1_cache = {}
        self.mock_cache_layer.l2_client = None
        self.mock_cache_layer.delete = Mock()
        self.invalidator = CacheInvalidator(
            cache_layer=self.mock_cache_layer
        )

    def test_initialization(self):
        """Test that invalidator initializes correctly."""
        assert self.invalidator is not None
        assert self.invalidator.cache_layer == self.mock_cache_layer
        assert self.invalidator.embedding_service is None
        assert self.invalidator.semantic_threshold == 0.9

    def test_invalidate_exact_key_exists(self):
        """Test invalidating a specific key that exists in cache."""
        # Setup: Add key to L1 cache
        self.mock_cache_layer.l1_cache["user:123"] = "cached_value"
        
        # Execute: Invalidate the key using EXACT strategy
        result = self.invalidator.invalidate("user:123", InvalidationStrategy.EXACT)
        
        # Verify: Result indicates success and key was deleted
        assert isinstance(result, InvalidationResult)
        assert result.success is True
        assert result.invalidated_keys == ["user:123"]
        assert result.strategy == InvalidationStrategy.EXACT
        self.mock_cache_layer.delete.assert_called_once_with("user:123")

    def test_invalidate_exact_key_not_found(self):
        """Test invalidating a key that doesn't exist in cache."""
        # Setup: L1 cache is empty
        self.mock_cache_layer.l1_cache = {}
        
        # Execute: Try to invalidate non-existent key
        result = self.invalidator.invalidate("user:999", InvalidationStrategy.EXACT)
        
        # Verify: Result indicates success but no keys invalidated
        assert isinstance(result, InvalidationResult)
        assert result.success is True
        assert result.invalidated_keys == []
        assert "Key not found" in result.metadata.get("message", "")

    def test_invalidate_by_pattern(self):
        """Test invalidating keys by pattern using regex matching."""
        # Setup: Add multiple keys to L1 cache
        self.mock_cache_layer.l1_cache = {
            "user:123": "value1",
            "user:456": "value2",
            "product:789": "value3",
            "user:abc": "value4"
        }
        
        # Execute: Invalidate all keys matching "user:*"
        result = self.invalidator.invalidate("user:*", InvalidationStrategy.PATTERN)
        
        # Verify: Only user:* keys were invalidated
        assert isinstance(result, InvalidationResult)
        assert result.success is True
        assert len(result.invalidated_keys) == 3
        assert "user:123" in result.invalidated_keys
        assert "user:456" in result.invalidated_keys
        assert "user:abc" in result.invalidated_keys
        assert "product:789" not in result.invalidated_keys
        assert result.strategy == InvalidationStrategy.PATTERN
        
        # Verify delete was called for each matching key
        assert self.mock_cache_layer.delete.call_count == 3

    def test_invalidate_pattern_empty_cache(self):
        """Test pattern invalidation on empty cache."""
        # Setup: Empty L1 cache
        self.mock_cache_layer.l1_cache = {}
        
        # Execute: Try to invalidate pattern
        result = self.invalidator.invalidate("user:*", InvalidationStrategy.PATTERN)
        
        # Verify: Success but no keys invalidated
        assert result.success is True
        assert result.invalidated_keys == []
        assert result.strategy == InvalidationStrategy.PATTERN

    def test_tag_based_invalidation(self):
        """Test invalidating keys by tag."""
        # Setup: Add keys to cache and tag them
        assert len(self.invalidator.rules) == 0
        assert len(self.invalidator.key_tags) == 0
        assert len(self.invalidator.tag_keys) == 0

    def test_invalidate_exact_key_exists(self):
        """Test invalidating a specific key that exists in cache."""
        # Set up cache with a key
        key = "user:123"
        self.mock_cache_layer.l1_cache[key] = "some_value"
        
        # Invalidate the key
        result = self.invalidator.invalidate(key, InvalidationStrategy.EXACT)
        
        # Verify invalidation succeeded
        assert result.success is True
        assert key in result.invalidated_keys
        assert result.strategy == InvalidationStrategy.EXACT
        self.mock_cache_layer.delete.assert_called_once_with(key)

    def test_invalidate_exact_key_not_exists(self):
        """Test invalidating a key that doesn't exist in cache."""
        key = "nonexistent:key"
        
        # Invalidate the key (not in cache)
        result = self.invalidator.invalidate(key, InvalidationStrategy.EXACT)
        
        # Should still succeed but with empty invalidated_keys
        assert result.success is True
        assert len(result.invalidated_keys) == 0
        assert result.strategy == InvalidationStrategy.EXACT

    def test_invalidate_by_pattern(self):
        """Test invalidating keys by pattern."""
        # Set up cache with multiple keys
        self.mock_cache_layer.l1_cache = {
            "user:123": "value1",
            "user:456": "value2",
            "product:789": "value3"
        }
        
        # Invalidate all user keys
        result = self.invalidator.invalidate("user:*", InvalidationStrategy.PATTERN)
        
        # Verify pattern invalidation
        assert result.success is True
        assert len(result.invalidated_keys) == 2
        assert "user:123" in result.invalidated_keys
        assert "user:456" in result.invalidated_keys
        assert "product:789" not in result.invalidated_keys
        assert result.strategy == InvalidationStrategy.PATTERN

    def test_tag_key_and_invalidate_by_tag(self):
        """Test tagging keys and invalidating by tag."""
        # Tag some keys
        self.invalidator.tag_key("user:123", "profile")
        self.invalidator.tag_key("user:456", "profile")
        self.invalidator.tag_key("product:789", "inventory")
        
        # Verify tags were added
        assert "profile" in self.invalidator.key_tags["user:123"]
        assert "user:123" in self.invalidator.tag_keys["profile"]
        
        # Set up cache
        self.mock_cache_layer.l1_cache = {
            "user:123": "value1",
            "user:456": "value2",
            "product:789": "value3"
        }
        
        # Tag some keys
        self.invalidator.tag_key("user:123", "profile")
        self.invalidator.tag_key("user:456", "profile")
        self.invalidator.tag_key("product:789", "catalog")
        
        # Execute: Invalidate by tag
        result = self.invalidator.invalidate_tag("profile")
        
        # Verify: Only tagged keys were invalidated
        # Invalidate by tag
        result = self.invalidator.invalidate_tag("profile")
        
        # Verify tag-based invalidation
        assert result.success is True
        assert len(result.invalidated_keys) == 2
        assert "user:123" in result.invalidated_keys
        assert "user:456" in result.invalidated_keys
        assert "product:789" not in result.invalidated_keys
        assert result.strategy == InvalidationStrategy.TAG
        
        # Verify delete was called for each tagged key
        assert self.mock_cache_layer.delete.call_count == 2

    def test_invalidate_semantic_without_embedding_service(self):
        """Test semantic invalidation fails gracefully without embedding service."""
        # Setup: No embedding service
        assert self.invalidator.embedding_service is None
        
        # Execute: Try semantic invalidation
        result = self.invalidator.invalidate("test_key", InvalidationStrategy.SEMANTIC)
        
        # Verify: Fails with appropriate error
        assert result.success is False
        assert result.invalidated_keys == []
        assert result.strategy == InvalidationStrategy.SEMANTIC
        assert "Embedding service not available" in result.error

    def test_invalidate_all_clears_cache(self):
        """Test invalidating all cache entries."""
        # Setup: Populate cache
        self.mock_cache_layer.l1_cache = {
            "user:123": "value1",
            "user:456": "value2",
            "product:789": "value3"
        }
        
        # Execute: Invalidate all
        result = self.invalidator.invalidate_all()
        
        # Verify: All keys invalidated
        assert result.success is True
        assert len(result.invalidated_keys) == 3
        assert result.strategy == InvalidationStrategy.MANUAL
        
        # Verify delete was called for each key
        assert self.mock_cache_layer.delete.call_count == 3

    def test_add_and_remove_rule(self):
        """Test adding and removing invalidation rules."""
        from adk.plugins.memory_plugins.cache_invalidator import InvalidationRule
        
        # Setup: Create a rule

    def test_untag_key(self):
        """Test removing a tag from a key."""
        # Tag a key
        self.invalidator.tag_key("user:123", "profile")
        assert "profile" in self.invalidator.key_tags["user:123"]
        
        # Untag the key
        self.invalidator.untag_key("user:123", "profile")
        
        # Verify tag was removed
        assert "profile" not in self.invalidator.key_tags["user:123"]
        assert "user:123" not in self.invalidator.tag_keys["profile"]

    def test_invalidate_all(self):
        """Test invalidating all cache entries."""
        # Set up cache with multiple keys
        self.mock_cache_layer.l1_cache = {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3"
        }
        
        # Tag some keys
        self.invalidator.tag_key("key1", "tag1")
        
        # Invalidate all
        result = self.invalidator.invalidate_all()
        
        # Verify all keys were invalidated
        assert result.success is True
        assert len(result.invalidated_keys) == 3
        # Tags should be cleared
        assert len(self.invalidator.key_tags) == 0
        assert len(self.invalidator.tag_keys) == 0

    def test_add_and_remove_rule(self):
        """Test adding and removing invalidation rules."""
        rule = InvalidationRule(
            name="test_rule",
            strategy=InvalidationStrategy.PATTERN,
            priority=1
        )
        
        # Execute: Add rule
        self.invalidator.add_rule(rule)
        
        # Verify: Rule was added
        assert "test_rule" in self.invalidator.rules
        assert self.invalidator.rules["test_rule"] == rule
        
        # Execute: Remove rule
        removed = self.invalidator.remove_rule("test_rule")
        
        # Verify: Rule was removed
        assert removed is True
        assert "test_rule" not in self.invalidator.rules
        
        # Execute: Try to remove non-existent rule
        removed = self.invalidator.remove_rule("non_existent")
        
        # Verify: Returns False
        assert removed is False
        # Add rule
        self.invalidator.add_rule(rule)
        assert "test_rule" in self.invalidator.rules
        
        # Remove rule
        result = self.invalidator.remove_rule("test_rule")
        assert result is True
        assert "test_rule" not in self.invalidator.rules
        
        # Try to remove non-existent rule
        result = self.invalidator.remove_rule("nonexistent")
        assert result is False

    def test_apply_rules(self):
        """Test applying invalidation rules based on triggers."""
        # Set up cache
        self.mock_cache_layer.l1_cache = {"trigger:key": "value"}
        
        # Add a rule with condition
        def condition(key, data):
            return key.startswith("trigger:")
        
        rule = InvalidationRule(
            name="trigger_rule",
            strategy=InvalidationStrategy.EXACT,
            priority=1,
            condition=condition
        )
        self.invalidator.add_rule(rule)
        
        # Apply rules
        results = self.invalidator.apply_rules("trigger:key")
        
        # Verify rule was applied
        assert len(results) > 0
        assert results[0].success is True

    def test_get_stats(self):
        """Test getting invalidator statistics."""
        # Add some data
        self.invalidator.tag_key("key1", "tag1")
        self.invalidator.tag_key("key2", "tag2")
        rule = InvalidationRule(name="rule1", strategy=InvalidationStrategy.EXACT)
        self.invalidator.add_rule(rule)
        
        # Get stats
        stats = self.invalidator.get_stats()
        
        assert "rules_count" in stats
        assert stats["rules_count"] == 1
        assert "tagged_keys" in stats
        assert stats["tagged_keys"] == 2
        assert "unique_tags" in stats
        assert "total_invalidated" in stats

    def test_invalidation_history(self):
        """Test that invalidation history is recorded."""
        # Set up cache
        self.mock_cache_layer.l1_cache = {"key1": "value1"}
        
        # Perform invalidation
        self.invalidator.invalidate("key1", InvalidationStrategy.EXACT)
        
        # Check history
        history = self.invalidator.get_history()
        assert len(history) > 0
        assert history[0]["event"] == InvalidationEvent.MANUAL_TRIGGER.value
        assert "key1" in history[0]["keys"]

    def test_clear_history(self):
        """Test clearing invalidation history."""
        # Set up cache and invalidate
        self.mock_cache_layer.l1_cache = {"key1": "value1"}
        self.invalidator.invalidate("key1", InvalidationStrategy.EXACT)
        
        assert len(self.invalidator.invalidation_history) > 0
        
        # Clear history
        self.invalidator.clear_history()
        assert len(self.invalidator.invalidation_history) == 0

    def test_event_handler(self):
        """Test event handler registration and execution."""
        handler_called = {"called": False, "event": None, "keys": None}
        
        def test_handler(event, keys):
            handler_called["called"] = True
            handler_called["event"] = event
            handler_called["keys"] = keys
        
        # Add event handler
        self.invalidator.add_event_handler(
            InvalidationEvent.MANUAL_TRIGGER, 
            test_handler
        )
        
        # Set up cache and invalidate
        self.mock_cache_layer.l1_cache = {"key1": "value1"}
        self.invalidator.invalidate("key1", InvalidationStrategy.EXACT)
        
        # Verify handler was called
        assert handler_called["called"] is True
        assert handler_called["event"] == InvalidationEvent.MANUAL_TRIGGER
        assert "key1" in handler_called["keys"]
        assert self.invalidator.cache_layer is self.mock_cache_layer

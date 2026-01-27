"""Unit tests for SemanticCacheV2."""
import unittest

from adk.plugins.memory_plugins.semantic_cache_v2 import (
    SemanticCacheConfigV2,
    CacheStrategy,
)
    SemanticCacheConfigV2,
    CacheStrategy,



class TestSemanticCacheConfigV2(unittest.TestCase):
    """Test cases for SemanticCacheConfigV2."""

    def test_config_creation(self):
        """Test creating cache configuration."""
        config = SemanticCacheConfigV2(
            default_ttl=3600,
            similarity_threshold=0.85
        )
        self.assertIsNotNone(config)

    def test_strategy_enum(self):
        """Test cache strategy enum values."""
        self.assertEqual(CacheStrategy.EXACT_ONLY.value, "exact_only")
        self.assertEqual(CacheStrategy.SEMANTIC_ONLY.value, "semantic_only")
        self.assertEqual(CacheStrategy.HYBRID.value, "hybrid")


if __name__ == "__main__":
    unittest.main()
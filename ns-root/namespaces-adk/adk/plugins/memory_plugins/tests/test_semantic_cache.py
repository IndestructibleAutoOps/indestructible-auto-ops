"""Unit tests for SemanticCache."""
import unittest

from adk.plugins.memory_plugins.semantic_cache import SemanticCache, CacheConfig
from adk.plugins.memory_plugins.semantic_cache import CacheConfig
from adk.plugins.memory_plugins.semantic_cache import CacheConfig


class TestSemanticCache(unittest.TestCase):
    """Test cases for SemanticCache."""

    def test_cache_config_creation(self):
        """Test creating cache configuration."""
        config = CacheConfig()
        self.assertIsNotNone(config)

    def test_cache_config_with_defaults(self):
        """Test cache config with default values."""
        config = CacheConfig()
        # Verify all default values are set correctly
        self.assertEqual(config.redis_host, "localhost")
        self.assertEqual(config.redis_port, 6379)
        self.assertEqual(config.redis_db, 1)
        self.assertIsNone(config.redis_password)
        self.assertEqual(config.prefix, "semcache:")
        self.assertEqual(config.similarity_threshold, 0.85)
        self.assertEqual(config.default_ttl, 3600)
        self.assertEqual(config.max_entries, 10000)
        self.assertEqual(config.vector_dim, 1536)
        self.assertEqual(config.eviction_policy, "lru")
        self.assertTrue(config.enable_adaptive_ttl)
        self.assertEqual(config.ttl_boost_threshold, 10)
        self.assertEqual(config.ttl_boost_multiplier, 1.5)
        self.assertEqual(config.max_ttl, 604800)

    def test_cache_config_with_custom_values(self):
        """Test cache config with custom values."""
        config = CacheConfig(
            redis_host="custom.redis.com",
            redis_port=6380,
            redis_db=2,
            redis_password="secret",
            prefix="custom:",
            similarity_threshold=0.90,
            default_ttl=7200,
            max_entries=5000,
            vector_dim=768,
            eviction_policy="lfu",
            enable_adaptive_ttl=False,
            ttl_boost_threshold=20,
            ttl_boost_multiplier=2.0,
            max_ttl=1209600
        )
        # Verify custom values are set correctly
        self.assertEqual(config.redis_host, "custom.redis.com")
        self.assertEqual(config.redis_port, 6380)
        self.assertEqual(config.redis_db, 2)
        self.assertEqual(config.redis_password, "secret")
        self.assertEqual(config.prefix, "custom:")
        self.assertEqual(config.similarity_threshold, 0.90)
        self.assertEqual(config.default_ttl, 7200)
        self.assertEqual(config.max_entries, 5000)
        self.assertEqual(config.vector_dim, 768)
        self.assertEqual(config.eviction_policy, "lfu")
        self.assertFalse(config.enable_adaptive_ttl)
        self.assertEqual(config.ttl_boost_threshold, 20)
        self.assertEqual(config.ttl_boost_multiplier, 2.0)
        self.assertEqual(config.max_ttl, 1209600)
        # Verify config has expected default attributes
        self.assertTrue(hasattr(config, 'similarity_threshold'))
        self.assertTrue(hasattr(config, 'max_cache_size'))


if __name__ == "__main__":
    unittest.main()
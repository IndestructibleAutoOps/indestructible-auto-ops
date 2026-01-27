"""Unit tests for CacheMiddleware."""
import unittest
from unittest.mock import Mock

from adk.plugins.memory_plugins.cache_middleware import (
    CacheMiddleware,
    CacheMiddlewareConfig,
)
from adk.plugins.memory_plugins.semantic_cache_v2 import (
    SemanticCacheV2,
    CacheStrategy,
)
from adk.plugins.memory_plugins.semantic_cache_v2 import CacheStrategy


class TestCacheMiddleware(unittest.TestCase):
    """Test cases for CacheMiddleware."""

    def setUp(self):
        """Set up test fixtures."""
        # Create mock cache instance
        self.mock_cache = Mock(spec=SemanticCacheV2)
        
        # Create config
        self.config = CacheMiddlewareConfig(
            strategy=CacheStrategy.HYBRID
        )
        
        # Create middleware with mock cache and config
        self.middleware = CacheMiddleware(self.mock_cache, self.config)
        # Mock the SemanticCacheV2 instance required by CacheMiddleware
        self.mock_cache = Mock(spec=SemanticCacheV2)
        
        self.mock_cache = Mock()
        self.config = CacheMiddlewareConfig(
            strategy=CacheStrategy.HYBRID
        )
        self.middleware = CacheMiddleware(
            cache=self.mock_cache,
            config=self.config
        )

    def test_init(self):
        """Test initialization."""
        self.assertIsNotNone(self.middleware)
        self.assertEqual(self.middleware.config.strategy, CacheStrategy.HYBRID)


if __name__ == "__main__":
    unittest.main()
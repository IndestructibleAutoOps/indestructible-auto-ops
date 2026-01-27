"""Unit tests for VectorSearch."""
import unittest

from adk.plugins.memory_plugins.vector_search import (
    VectorSearchQueryBuilder,
    VectorSearchExecutor,
    VectorSearchQuery,
)


class TestVectorSearchQueryBuilder(unittest.TestCase):
    """Test cases for VectorSearchQueryBuilder."""

    def setUp(self):
        """Set up test fixtures."""
        self.builder = VectorSearchQueryBuilder()

    def test_build_query(self):
        """Test building a search query."""
        query = (
            self.builder
            .with_vector([0.1, 0.2, 0.3])
            .with_top_k(10)
            .build()
        )
        
        self.assertIsNotNone(query)
        self.assertEqual(query.vector, [0.1, 0.2, 0.3])
        self.assertEqual(query.top_k, 10)


class TestVectorSearchExecutor(unittest.TestCase):
    """Test cases for VectorSearchExecutor."""

    def test_init(self):
        """Test executor initialization."""
        mock_client = Mock()
        executor = VectorSearchExecutor(mock_client)
        self.assertIsNotNone(executor)


if __name__ == "__main__":
    unittest.main()
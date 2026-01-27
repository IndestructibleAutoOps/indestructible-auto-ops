"""Unit tests for VectorIndexManager."""
import unittest
from unittest.mock import Mock, AsyncMock

from adk.plugins.memory_plugins.vector_index_manager import (
    VectorIndexManager,
    VectorIndexConfig,
    DistanceMetric,
    VectorAlgorithm,
)


class TestVectorIndexManager(unittest.IsolatedAsyncioTestCase):
    """Test cases for VectorIndexManager."""

    def test_init(self):
        """Test initialization."""
        mock_client = Mock()
        manager = VectorIndexManager(mock_client)
        self.assertIsNotNone(manager)

    async def test_create_index_new(self):
        """Test creating a new index."""
    def test_config_creation(self):
        """Test creating a valid index configuration."""
        config = VectorIndexConfig(
            name="test_index",
            prefix="test:",
            dimension=1536,
            distance_metric=DistanceMetric.COSINE,
            algorithm=VectorAlgorithm.HNSW
        )
        
        # Mock Redis client methods
        mock_ft = Mock()
        mock_ft.info = AsyncMock(side_effect=Exception("Index doesn't exist"))
        self.mock_client.ft = Mock(return_value=mock_ft)
        self.mock_client.execute_command = AsyncMock(return_value="OK")
        
        # Test async behavior
        result = await self.manager.create_index(config)
        
        # Verify index was created
        self.assertTrue(result)
        self.mock_client.execute_command.assert_called_once()
        
        # Verify command structure
        call_args = self.mock_client.execute_command.call_args[0][0]
        self.assertIn("FT.CREATE", call_args)
        self.assertIn("test_index", call_args)
        self.assertIn("test:", call_args)
        self.assertIn("HNSW", call_args)
        self.assertIn("COSINE", call_args)
        self.assertIn("1536", call_args)

    async def test_create_index_already_exists(self):
        """Test creating an index that already exists."""
        config = VectorIndexConfig(
            name="existing_index",
            prefix="test:",
            dimension=1536
        )
        
        # Mock Redis client to return index exists
        mock_ft = Mock()
        mock_ft.info = AsyncMock(return_value={"index_name": "existing_index"})
        self.mock_client.ft = Mock(return_value=mock_ft)
        
        # Test async behavior
        result = await self.manager.create_index(config)
        
        # Verify index creation was skipped
        self.assertFalse(result)

    async def test_create_index_with_flat_algorithm(self):
        """Test creating an index with FLAT algorithm."""
        config = VectorIndexConfig(
            name="flat_index",
            prefix="flat:",
            dimension=768,
            algorithm=VectorAlgorithm.FLAT
        )
        
        # Mock Redis client methods
        mock_ft = Mock()
        mock_ft.info = AsyncMock(side_effect=Exception("Index doesn't exist"))
        self.mock_client.ft = Mock(return_value=mock_ft)
        self.mock_client.execute_command = AsyncMock(return_value="OK")
        
        # Test async behavior
        result = await self.manager.create_index(config)
        
        # Verify command includes FLAT algorithm
        self.assertTrue(result)
        call_args = self.mock_client.execute_command.call_args[0][0]
        self.assertIn("FLAT", call_args)
        self.assertIn("768", call_args)

    async def test_drop_index(self):
        """Test dropping an index."""
        self.mock_client.execute_command = AsyncMock(return_value="OK")
        
        # Test async behavior
        result = await self.manager.drop_index("test_index")
        
        # Verify index was dropped
        self.assertTrue(result)
        self.mock_client.execute_command.assert_called_once_with("FT.DROPINDEX test_index")

    async def test_drop_index_with_delete_docs(self):
        """Test dropping an index with document deletion."""
        self.mock_client.execute_command = AsyncMock(return_value="OK")
        
        # Test async behavior
        result = await self.manager.drop_index("test_index", delete_docs=True)
        
        # Verify index was dropped with DD flag
        self.assertTrue(result)
        self.mock_client.execute_command.assert_called_once_with("FT.DROPINDEX test_index DD")

    async def test_index_exists_true(self):
        """Test checking if an index exists - true case."""
        mock_ft = Mock()
        mock_ft.info = AsyncMock(return_value={"index_name": "test_index"})
        self.mock_client.ft = Mock(return_value=mock_ft)
        
        # Test async behavior
        result = await self.manager.index_exists("test_index")
        
        self.assertTrue(result)

    async def test_index_exists_false(self):
        """Test checking if an index exists - false case."""
        mock_ft = Mock()
        mock_ft.info = AsyncMock(side_effect=Exception("Index not found"))
        self.mock_client.ft = Mock(return_value=mock_ft)
        
        # Test async behavior
        result = await self.manager.index_exists("test_index")
        
        self.assertFalse(result)
        self.assertEqual(config.name, "test_index")
        self.assertEqual(config.prefix, "test")
        self.assertEqual(config.dimension, 1536)
        self.assertEqual(config.distance_metric, DistanceMetric.COSINE)
        self.assertEqual(config.algorithm, VectorAlgorithm.HNSW)


if __name__ == "__main__":
    unittest.main()
"""
Tests for GL20 Data Ingestion Module
"""

import sys
from pathlib import Path

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from ingestion.base_ingestor import BatchIngestor, StreamIngestor


class TestDataIngestor:
    """Test cases for DataIngestor base class"""

    def test_batch_ingestor_initialization(self):
        """Test BatchIngestor initialization"""
        config = {
            'source_type': 'batch',
            'batch_size': 100
        }
        ingestor = BatchIngestor(config)

        assert ingestor.ingestion_metadata['source_type'] == 'batch'
        assert ingestor.batch_size == 100
        assert ingestor.ingestion_metadata['status'] == 'INITIALIZED'

    def test_batch_ingestor_connect(self):
        """Test BatchIngestor connection"""
        config = {'source_type': 'batch', 'batch_size': 100}
        ingestor = BatchIngestor(config)

        result = ingestor.connect()
        assert result is True

    def test_batch_ingestor_extract(self):
        """Test BatchIngestor extraction"""
        config = {'source_type': 'batch', 'batch_size': 10}
        ingestor = BatchIngestor(config)

        data = ingestor.extract()
        assert len(data) == 10
        assert all('id' in record for record in data)

    def test_batch_ingestor_validate(self):
        """Test BatchIngestor validation"""
        config = {'source_type': 'batch', 'batch_size': 10}
        ingestor = BatchIngestor(config)

        data = ingestor.extract()
        result = ingestor.validate(data)
        assert result is True

    def test_batch_ingestor_ingest(self):
        """Test complete BatchIngestor ingestion pipeline"""
        config = {'source_type': 'batch', 'batch_size': 10}
        ingestor = BatchIngestor(config)

        result = ingestor.ingest()
        assert result['status'] == 'SUCCESS'
        assert result['record_count'] == 10

    def test_stream_ingestor_initialization(self):
        """Test StreamIngestor initialization"""
        config = {
            'source_type': 'stream',
            'stream_config': {'buffer_size': 1000}
        }
        ingestor = StreamIngestor(config)

        assert ingestor.ingestion_metadata['source_type'] == 'stream'

    def test_stream_ingestor_connect(self):
        """Test StreamIngestor connection"""
        config = {'source_type': 'stream', 'stream_config': {}}
        ingestor = StreamIngestor(config)

        result = ingestor.connect()
        assert result is True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

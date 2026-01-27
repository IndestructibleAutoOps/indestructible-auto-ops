"""
Vector Index Manager: Redis Stack vector index management.

This module provides comprehensive vector index management for Redis Stack,
including index creation, document operations, and query execution.

GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module research/agent-memory-cache/implementation
@gl-semantic-anchor GL-00-IMPL_VECTOR_INDEX
@gl-evidence-required false
GL Unified Charter Activated
"""

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Union

try:
    import redis
    from redis.commands.search.field import (
        TextField,
        NumericField,
        TagField,
        VectorField
    )
    from redis.commands.search.indexDefinition import IndexDefinition, IndexType
    from redis.commands.search.query import Query
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None


logger = logging.getLogger(__name__)


# =============================================================================
# Data Models
# =============================================================================


class VectorAlgorithm(Enum):
    """Vector index algorithms."""
    FLAT = "FLAT"
    HNSW = "HNSW"


class DistanceMetric(Enum):
    """Distance metrics for vector similarity."""
    COSINE = "COSINE"
    L2 = "L2"
    IP = "INNER_PRODUCT"


@dataclass
class VectorIndexConfig:
    """Configuration for vector index."""
    index_name: str
    prefix: str = "doc:"
    vector_field: str = "vector"
    dimension: int = 1536
    algorithm: VectorAlgorithm = VectorAlgorithm.HNSW
    distance_metric: DistanceMetric = DistanceMetric.COSINE
    
    # HNSW-specific parameters
    m: int = 16
    ef_construction: int = 200
    ef_runtime: int = 10
    
    # Additional fields
    text_fields: List[str] = None
    tag_fields: List[str] = None
    numeric_fields: List[str] = None
    
    def __post_init__(self):
        if self.text_fields is None:
            self.text_fields = ["content"]
        if self.tag_fields is None:
            self.tag_fields = ["metadata_type"]
        if self.numeric_fields is None:
            self.numeric_fields = ["importance", "timestamp"]


@dataclass
class Document:
    """Document with vector embedding."""
    id: str
    vector: List[float]
    content: str
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    def to_redis_dict(self, vector_field: str = "vector") -> Dict[str, Any]:
        """Convert to Redis document format."""
        doc = {
            "vector": self._vector_to_bytes(self.vector),
            "content": self.content,
            "importance": self.metadata.get("importance", 0),
            "timestamp": self.metadata.get("timestamp", 0),
        }
        
        # Add metadata fields
        for key, value in self.metadata.items():
            if key not in ["importance", "timestamp"]:
                doc[f"metadata_{key}"] = str(value)
        
        return doc
    
    @staticmethod
    def _vector_to_bytes(vector: List[float]) -> bytes:
        """Convert vector list to bytes."""
        import struct
        return struct.pack(f"{len(vector)}f", *vector)
    
    @staticmethod
    def _bytes_to_vector(data: bytes) -> List[float]:
        """Convert bytes to vector list."""
        import struct
        return list(struct.unpack(f"{len(data) // 4}f", data))


@dataclass
class SearchResult:
    """Vector search result."""
    id: str
    score: float
    content: str
    metadata: Dict[str, Any] = None


# =============================================================================
# Vector Index Manager
# =============================================================================


class VectorIndexManager:
    """Manages vector indexes in Redis Stack."""
    
    def __init__(
        self,
        redis_client: "redis.Redis",
        config: VectorIndexConfig
    ):
        """
        Initialize vector index manager.
        
        Args:
            redis_client: Redis client instance
            config: Index configuration
        """
        if not REDIS_AVAILABLE:
            raise ImportError(
                "Redis package is required. "
                "Install with: pip install redis[hiredis]"
            )
        
        self.client = redis_client
        self.config = config
    
    def create_index(self, drop_if_exists: bool = False) -> bool:
        """
        Create vector index.
        
        Args:
            drop_if_exists: Drop existing index before creating
            
        Returns:
            True if index created successfully
        """
        try:
            # Drop existing index if requested
            if drop_if_exists:
                try:
                    self.client.ft(self.config.index_name).dropindex()
                    logger.info(f"Dropped existing index: {self.config.index_name}")
                except Exception as e:
                    logger.debug(f"No existing index to drop: {e}")
            
            # Create index definition
            index_def = IndexDefinition(
                prefix=[self.config.prefix],
                index_type=IndexType.HASH
            )
            
            # Create fields
            fields = self._create_fields()
            
            # Create index
            self.client.ft(self.config.index_name).create_index(
                fields=fields,
                definition=index_def
            )
            
            logger.info(f"Created vector index: {self.config.index_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create index: {e}")
            raise
    
    def _create_fields(self) -> List:
        """Create field definitions for index."""
        fields = []
        
        # Text fields
        for field_name in self.config.text_fields:
            fields.append(TextField(field_name))
        
        # Tag fields
        for field_name in self.config.tag_fields:
            fields.append(TagField(field_name))
        
        # Numeric fields
        for field_name in self.config.numeric_fields:
            fields.append(NumericField(field_name))
        
        # Vector field
        vector_field = VectorField(
            self.config.vector_field,
            self.config.algorithm.value,
            {
                "TYPE": "FLOAT32",
                "DIM": self.config.dimension,
                "DISTANCE_METRIC": self.config.distance_metric.value,
                "INITIAL_CAP": 1000,
            }
        )
        
        if self.config.algorithm == VectorAlgorithm.HNSW:
            vector_field.attrs.update({
                "M": self.config.m,
                "EF_CONSTRUCTION": self.config.ef_construction,
                "EF_RUNTIME": self.config.ef_runtime,
            })
        
        fields.append(vector_field)
        return fields
    
    def index_exists(self) -> bool:
        """Check if index exists."""
        try:
            info = self.client.ft(self.config.index_name).info()
            return info is not None
        except Exception:
            return False
    
    def drop_index(self) -> bool:
        """Drop the vector index."""
        try:
            self.client.ft(self.config.index_name).dropindex()
            logger.info(f"Dropped index: {self.config.index_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to drop index: {e}")
            return False
    
    def add_document(self, document: Document) -> bool:
        """
        Add document to index.
        
        Args:
            document: Document to add
            
        Returns:
            True if added successfully
        """
        try:
            doc_id = f"{self.config.prefix}{document.id}"
            doc_data = document.to_redis_dict(self.config.vector_field)
            
            self.client.hset(doc_id, mapping=doc_data)
            logger.debug(f"Added document: {doc_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to add document: {e}")
            return False
    
    def add_documents_batch(self, documents: List[Document]) -> int:
        """
        Add multiple documents in batch.
        
        Args:
            documents: List of documents to add
            
        Returns:
            Number of documents added
        """
        pipeline = self.client.pipeline()
        added = 0
        
        for doc in documents:
            try:
                doc_id = f"{self.config.prefix}{doc.id}"
                doc_data = doc.to_redis_dict(self.config.vector_field)
                pipeline.hset(doc_id, mapping=doc_data)
                added += 1
            except Exception as e:
                logger.error(f"Failed to add document {doc.id}: {e}")
        
        pipeline.execute()
        logger.info(f"Added {added}/{len(documents)} documents")
        return added
    
    def get_document(self, doc_id: str) -> Optional[Document]:
        """
        Retrieve document by ID.
        
        Args:
            doc_id: Document ID
            
        Returns:
            Document or None if not found
        """
        try:
            full_id = f"{self.config.prefix}{doc_id}"
            data = self.client.hgetall(full_id)
            
            if not data:
                return None
            
            # Decode bytes to strings
            data = {k.decode() if isinstance(k, bytes) else k: 
                    v.decode() if isinstance(v, bytes) else v 
                    for k, v in data.items()}
            
            # Extract vector
            vector = Document._bytes_to_vector(data.get("vector", b""))
            
            # Extract metadata
            metadata = {
                "importance": float(data.get("importance", 0)),
                "timestamp": float(data.get("timestamp", 0)),
            }
            
            for key, value in data.items():
                if key.startswith("metadata_"):
                    metadata[key[9:]] = value
            
            return Document(
                id=doc_id,
                vector=vector,
                content=data.get("content", ""),
                metadata=metadata
            )
        except Exception as e:
            logger.error(f"Failed to get document: {e}")
            return None
    
    def delete_document(self, doc_id: str) -> bool:
        """
        Delete document from index.
        
        Args:
            doc_id: Document ID
            
        Returns:
            True if deleted successfully
        """
        try:
            full_id = f"{self.config.prefix}{doc_id}"
            self.client.delete(full_id)
            logger.debug(f"Deleted document: {doc_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete document: {e}")
            return False
    
    def get_index_info(self) -> Dict[str, Any]:
        """
        Get index information.
        
        Returns:
            Index information dictionary
        """
        try:
            info = self.client.ft(self.config.index_name).info()
            return {
                "name": self.config.index_name,
                "num_docs": info.get("num_docs", 0),
                "indexing": info.get("indexing", 0),
                "total_indexing_time": info.get("total_indexing_time", 0),
                "fields": info.get("fields", []),
            }
        except Exception as e:
            logger.error(f"Failed to get index info: {e}")
            return {}


# =============================================================================
# Factory Functions
# =============================================================================


def create_vector_index_manager(
    redis_client: "redis.Redis",
    index_name: str,
    dimension: int = 1536,
    algorithm: str = "HNSW",
    distance_metric: str = "COSINE",
    **kwargs
) -> VectorIndexManager:
    """
    Factory function to create vector index manager.
    
    Args:
        redis_client: Redis client instance
        index_name: Name of the index
        dimension: Embedding dimension
        algorithm: Vector algorithm (FLAT or HNSW)
        distance_metric: Distance metric (COSINE, L2, IP)
        **kwargs: Additional configuration
        
    Returns:
        Configured VectorIndexManager instance
    """
    config = VectorIndexConfig(
        index_name=index_name,
        dimension=dimension,
        algorithm=VectorAlgorithm(algorithm),
        distance_metric=DistanceMetric(distance_metric),
        **kwargs
    )
    
    return VectorIndexManager(redis_client, config)


# =============================================================================
# Example Usage
# =============================================================================


def example_usage():
    """Example usage of vector index manager."""
    
    import redis
    
    # Connect to Redis
    client = redis.Redis(host="localhost", port=6379, decode_responses=False)
    
    # Create index configuration
    config = VectorIndexConfig(
        index_name="memory-index",
        prefix="memory:",
        dimension=1536,
        algorithm=VectorAlgorithm.HNSW,
        distance_metric=DistanceMetric.COSINE
    )
    
    # Create index manager
    manager = VectorIndexManager(client, config)
    
    # Create index
    manager.create_index(drop_if_exists=True)
    
    # Add documents
    doc1 = Document(
        id="doc1",
        vector=[0.1, 0.2, 0.3] * 512,
        content="First memory",
        metadata={"importance": 0.9}
    )
    manager.add_document(doc1)
    
    # Get index info
    info = manager.get_index_info()
    print(f"Index has {info['num_docs']} documents")


if __name__ == "__main__":
    example_usage()
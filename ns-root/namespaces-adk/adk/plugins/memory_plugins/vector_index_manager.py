"""
Vector Index Manager for Redis Stack.
Manages vector indices for semantic memory search.
"""

import json
import hashlib
from typing import Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class DistanceMetric(Enum):
    """Supported distance metrics for vector search."""
    COSINE = "COSINE"
    L2 = "L2"
    IP = "IP"  # Inner Product


class VectorAlgorithm(Enum):
    """Supported vector indexing algorithms."""
    FLAT = "FLAT"
    HNSW = "HNSW"


@dataclass
class VectorIndexConfig:
    """Configuration for a vector index."""
    name: str
    prefix: str
    vector_field: str = "embedding"
    dimension: int = 1536
    distance_metric: DistanceMetric = DistanceMetric.COSINE
    algorithm: VectorAlgorithm = VectorAlgorithm.HNSW
    # HNSW specific parameters
    hnsw_m: int = 16
    hnsw_ef_construction: int = 200
    hnsw_ef_runtime: int = 10
    # Additional indexed fields
    text_fields: list[str] = field(default_factory=lambda: ["content"])
    tag_fields: list[str] = field(default_factory=lambda: ["type", "agent_id"])
    numeric_fields: list[str] = field(default_factory=lambda: ["timestamp", "importance"])


class VectorIndexManager:
    """
    Manages vector indices in Redis Stack.
    Supports creating, updating, and deleting vector indices.
    """

    def __init__(self, redis_client: Any):
        """
        Initialize the vector index manager.
        
        Args:
            redis_client: Redis client with RediSearch support
        """
        self._client = redis_client
        self._indices: dict[str, VectorIndexConfig] = {}

    async def create_index(self, config: VectorIndexConfig) -> bool:
        """
        Create a vector index in Redis.
        
        Args:
            config: Vector index configuration
            
        Returns:
            True if index was created, False if it already exists
        """
        try:
            # Check if index exists
            try:
                await self._client.ft(config.name).info()
                self._indices[config.name] = config
                return False  # Index already exists
            except Exception:
                pass  # Index doesn't exist, create it

            # Build schema
            schema_parts = []
            
            # Add text fields
            for field_name in config.text_fields:
                schema_parts.append(f"$.{field_name} AS {field_name} TEXT")
            
            # Add tag fields
            for field_name in config.tag_fields:
                schema_parts.append(f"$.{field_name} AS {field_name} TAG")
            
            # Add numeric fields
            for field_name in config.numeric_fields:
                schema_parts.append(f"$.{field_name} AS {field_name} NUMERIC")
            
            # Add vector field
            if config.algorithm == VectorAlgorithm.HNSW:
                vector_schema = (
                    f"$.{config.vector_field} AS {config.vector_field} VECTOR HNSW 6 "
                    f"TYPE FLOAT32 DIM {config.dimension} DISTANCE_METRIC {config.distance_metric.value}"
                )
            else:
                vector_schema = (
                    f"$.{config.vector_field} AS {config.vector_field} VECTOR FLAT 6 "
                    f"TYPE FLOAT32 DIM {config.dimension} DISTANCE_METRIC {config.distance_metric.value}"
                )
            schema_parts.append(vector_schema)

            # Create index command
            schema = " ".join(schema_parts)
            create_cmd = f"FT.CREATE {config.name} ON JSON PREFIX 1 {config.prefix} SCHEMA {schema}"
            
            await self._client.execute_command(create_cmd)
            self._indices[config.name] = config
            return True

        except Exception as e:
            raise RuntimeError(f"Failed to create index {config.name}: {e}") from e

    async def drop_index(self, index_name: str, delete_docs: bool = False) -> bool:
        """
        Drop a vector index.
        
        Args:
            index_name: Name of the index to drop
            delete_docs: If True, also delete all indexed documents
            
        Returns:
            True if index was dropped
        """
        try:
            dd_flag = "DD" if delete_docs else ""
            await self._client.execute_command(f"FT.DROPINDEX {index_name} {dd_flag}".strip())
            self._indices.pop(index_name, None)
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to drop index {index_name}: {e}") from e

    async def index_exists(self, index_name: str) -> bool:
        """Check if an index exists."""
        try:
            await self._client.ft(index_name).info()
            return True
        except Exception:
            return False

    async def get_index_info(self, index_name: str) -> dict[str, Any]:
        """Get information about an index."""
        try:
            info = await self._client.ft(index_name).info()
            return dict(info) if info else {}
        except Exception as e:
            raise RuntimeError(f"Failed to get index info for {index_name}: {e}") from e

    async def store_document(
        self,
        index_name: str,
        doc_id: str,
        content: str,
        embedding: list[float],
        metadata: Optional[dict[str, Any]] = None
    ) -> str:
        """
        Store a document with its embedding in Redis.
        
        Args:
            index_name: Name of the index
            doc_id: Document ID
            content: Text content
            embedding: Vector embedding
            metadata: Additional metadata
            
        Returns:
            The document key
        """
        config = self._indices.get(index_name)
        if not config:
            raise ValueError(f"Index {index_name} not found in manager")

        # Build document
        doc = {
            "content": content,
            "embedding": embedding,
            "doc_id": doc_id,
            **(metadata or {})
        }

        # Generate key
        key = f"{config.prefix}{doc_id}"
        
        # Store as JSON
        await self._client.json().set(key, "$", doc)
        return key

    async def delete_document(self, index_name: str, doc_id: str) -> bool:
        """Delete a document from the index."""
        config = self._indices.get(index_name)
        if not config:
            raise ValueError(f"Index {index_name} not found in manager")

        key = f"{config.prefix}{doc_id}"
        result = await self._client.delete(key)
        return result > 0

    async def get_document(self, index_name: str, doc_id: str) -> Optional[dict[str, Any]]:
        """Get a document by ID."""
        config = self._indices.get(index_name)
        if not config:
            raise ValueError(f"Index {index_name} not found in manager")

        key = f"{config.prefix}{doc_id}"
        try:
            doc = await self._client.json().get(key)
            return doc
        except Exception:
            return None

    def get_registered_indices(self) -> list[str]:
        """Get list of registered index names."""
        return list(self._indices.keys())

    @staticmethod
    def generate_doc_id(content: str, namespace: str = "") -> str:
        """Generate a deterministic document ID from content."""
        hash_input = f"{namespace}:{content}"
        return hashlib.sha256(hash_input.encode()).hexdigest()[:16]


# Default index configurations
DEFAULT_MEMORY_INDEX = VectorIndexConfig(
    name="idx:memory",
    prefix="memory:",
    dimension=1536,
    text_fields=["content", "summary"],
    tag_fields=["type", "agent_id", "session_id"],
    numeric_fields=["timestamp", "importance", "access_count"]
)

DEFAULT_CACHE_INDEX = VectorIndexConfig(
    name="idx:cache",
    prefix="cache:",
    dimension=1536,
    text_fields=["query", "response"],
    tag_fields=["model", "agent_id"],
    numeric_fields=["timestamp", "ttl", "hit_count"]
)

DEFAULT_KNOWLEDGE_INDEX = VectorIndexConfig(
    name="idx:knowledge",
    prefix="knowledge:",
    dimension=1536,
    text_fields=["content", "title", "source"],
    tag_fields=["category", "domain", "agent_id"],
    numeric_fields=["timestamp", "relevance_score"]
)
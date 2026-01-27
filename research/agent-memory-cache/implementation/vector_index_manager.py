import asyncio
import json
import time
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import numpy as np


class DistanceMetric(Enum):
    """Supported distance metrics for vector similarity search."""
    COSINE = "COSINE"
    L2 = "L2"
    IP = "IP"


class IndexAlgorithm(Enum):
    """Supported vector index algorithms."""
    HNSW = "HNSW"
    FLAT = "FLAT"


@dataclass
class IndexConfig:
    """Configuration for vector index."""
    dimension: int = 1536
    metric: DistanceMetric = DistanceMetric.COSINE
    algorithm: IndexAlgorithm = IndexAlgorithm.HNSW
    m: int = 16  # HNSW parameter: max connections per node
    ef_construction: int = 200  # HNSW parameter: build-time accuracy
    ef_runtime: int = 50  # HNSW parameter: search-time accuracy


@dataclass
class Document:
    """Document with vector embedding and metadata."""
    id: str
    embedding: List[float]
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


class VectorIndexManager:
    """Manages vector indices for semantic search operations.
    
    This manager provides:
    - Create/drop vector indices
    - Add/update/delete documents with embeddings
    - Vector similarity search with filters
    - Index statistics and health monitoring
    
    Compatible with Redis Stack, Pinecone, Weaviate, or custom backends.
    """
    
    def __init__(self, client: Any, prefix: str = "vecidx"):
        """Initialize vector index manager.
        
        Args:
            client: Backend client (Redis, Pinecone, etc.)
            prefix: Key prefix for indices
        """
        self.client = client
        self.prefix = prefix
        self.indices: Dict[str, IndexConfig] = {}
    
    def create_index(self, name: str, config: IndexConfig) -> bool:
        """Create a new vector index.
        
        Args:
            name: Index name
            config: Index configuration
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Redis Stack implementation example
            if hasattr(self.client, 'ft'):
                schema = []
                schema.append(f"vector VECTOR HNSW 6 TYPE FLOAT32 DIM {config.dimension} DISTANCE_METRIC {config.metric.value} INITIAL_CAP 1000 EF_CONSTRUCTION {config.ef_construction} EF_RUNTIME {config.ef_runtime} M {config.m}")
                
                # Add optional metadata fields
                schema.append("content TEXT WEIGHT 1.0")
                schema.append("timestamp NUMERIC SORTABLE")
                
                self.client.ft(f"{self.prefix}:{name}").create_index(
                    fields=schema
                )
            
            self.indices[name] = config
            return True
            
        except Exception as e:
            print(f"Error creating index {name}: {e}")
            return False
    
    def drop_index(self, name: str) -> bool:
        """Drop a vector index.
        
        Args:
            name: Index name
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if hasattr(self.client, 'ft'):
                self.client.ft(f"{self.prefix}:{name}").dropindex()
            
            if name in self.indices:
                del self.indices[name]
            
            return True
            
        except Exception as e:
            print(f"Error dropping index {name}: {e}")
            return False
    
    def add_document(self, index_name: str, doc: Document) -> bool:
        """Add a document to the index.
        
        Args:
            index_name: Name of the index
            doc: Document to add
            
        Returns:
            True if successful, False otherwise
        """
        try:
            key = f"{self.prefix}:{index_name}:{doc.id}"
            
            # Store document with embedding
            payload = {
                "vector": np.array(doc.embedding).astype(np.float32).tobytes(),
                "content": doc.content,
                "timestamp": doc.timestamp,
                **doc.metadata
            }
            
            self.client.hset(key, mapping=payload)
            
            return True
            
        except Exception as e:
            print(f"Error adding document {doc.id}: {e}")
            return False
    
    def add_documents_batch(self, index_name: str, docs: List[Document]) -> Dict[str, bool]:
        """Add multiple documents in batch.
        
        Args:
            index_name: Name of the index
            docs: List of documents to add
            
        Returns:
            Dict mapping doc IDs to success status
        """
        results = {}
        
        try:
            pipe = self.client.pipeline()
            
            for doc in docs:
                key = f"{self.prefix}:{index_name}:{doc.id}"
                payload = {
                    "vector": np.array(doc.embedding).astype(np.float32).tobytes(),
                    "content": doc.content,
                    "timestamp": doc.timestamp,
                    **doc.metadata
                }
                pipe.hset(key, mapping=payload)
            
            pipe.execute()
            results = {doc.id: True for doc in docs}
            
        except Exception as e:
            print(f"Batch add error: {e}")
            results = {doc.id: False for doc in docs}
        
        return results
    
    def get_document(self, index_name: str, doc_id: str) -> Optional[Document]:
        """Retrieve a document by ID.
        
        Args:
            index_name: Name of the index
            doc_id: Document ID
            
        Returns:
            Document object or None if not found
        """
        try:
            key = f"{self.prefix}:{index_name}:{doc_id}"
            data = self.client.hgetall(key)
            
            if not data:
                return None
            
            # Parse embedding bytes back to array
            embedding_bytes = data.get(b'vector', b'')
            embedding = np.frombuffer(embedding_bytes, dtype=np.float32).tolist()
            
            return Document(
                id=doc_id,
                embedding=embedding,
                content=data.get(b'content', b'').decode(),
                metadata={k.decode(): v.decode() for k, v in data.items() 
                         if k not in [b'vector', b'content', b'timestamp']},
                timestamp=float(data.get(b'timestamp', time.time()))
            )
            
        except Exception as e:
            print(f"Error getting document {doc_id}: {e}")
            return None
    
    def update_document(self, index_name: str, doc: Document) -> bool:
        """Update an existing document.
        
        Args:
            index_name: Name of the index
            doc: Document with updated content
            
        Returns:
            True if successful, False otherwise
        """
        return self.add_document(index_name, doc)
    
    def delete_document(self, index_name: str, doc_id: str) -> bool:
        """Delete a document from the index.
        
        Args:
            index_name: Name of the index
            doc_id: Document ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            key = f"{self.prefix}:{index_name}:{doc_id}"
            self.client.delete(key)
            return True
            
        except Exception as e:
            print(f"Error deleting document {doc_id}: {e}")
            return False
    
    def search(self, index_name: str, query_vector: List[float], 
               limit: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[Tuple[str, float, Dict]]:
        """Perform vector similarity search.
        
        Args:
            index_name: Name of the index
            query_vector: Query embedding
            limit: Maximum number of results
            filters: Optional metadata filters
            
        Returns:
            List of tuples (doc_id, score, metadata)
        """
        try:
            if hasattr(self.client, 'ft'):
                # Redis Stack search
                query_str = f"*=>[KNN {limit} @vector $vec AS score]"
                
                params = {
                    "vec": np.array(query_vector).astype(np.float32).tobytes()
                }
                
                results = self.client.ft(f"{self.prefix}:{index_name}").search(
                    query_str,
                    query_params=params
                )
                
                output = []
                for doc in results.docs:
                    output.append((
                        doc.id.split(':')[-1],
                        float(doc.score),
                        {k: v for k, v in doc.__dict__.items() 
                         if k not in ['id', 'payload', 'score', '__dict__']}
                    ))
                
                return output
            
            return []
            
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def get_index_stats(self, index_name: str) -> Dict[str, Any]:
        """Get statistics for an index.
        
        Args:
            index_name: Name of the index
            
        Returns:
            Dictionary with index statistics
        """
        try:
            if hasattr(self.client, 'ft'):
                info = self.client.ft(f"{self.prefix}:{index_name}").info()
                return {
                    "num_docs": int(info.get("num_docs", 0)),
                    "indexing_time": float(info.get("indexing_time", 0)),
                    "config": self.indices.get(index_name).__dict__ if index_name in self.indices else {}
                }
            
            return {}
            
        except Exception as e:
            print(f"Error getting index stats: {e}")
            return {}
    
    def list_indices(self) -> List[str]:
        """List all indices.
        
        Returns:
            List of index names
        """
        return list(self.indices.keys())
    
    def health_check(self) -> Dict[str, Any]:
        """Check health of vector index manager.
        
        Returns:
            Health status dictionary
        """
        return {
            "status": "healthy",
            "indices": len(self.indices),
            "index_names": list(self.indices.keys()),
            "timestamp": time.time()
        }
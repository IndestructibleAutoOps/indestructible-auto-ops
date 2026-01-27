from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
from .vector_index_manager import VectorIndexManager, DistanceMetric, Document


class SearchStrategy(Enum):
    """Search strategies for vector similarity."""
    KNN = "knn"  # K-nearest neighbors
    HYBRID = "hybrid"  # Vector + keyword
    FILTERED = "filtered"  # Vector with metadata filters
    RERANK = "rerank"  # Vector search with reranking


@dataclass
class SearchQuery:
    """Search query with parameters."""
    text: str
    embedding: Optional[List[float]] = None
    filters: Optional[Dict[str, Any]] = None
    limit: int = 10
    threshold: float = 0.7
    strategy: SearchStrategy = SearchStrategy.KNN
    metadata_fields: List[str] = field(default_factory=list)
    return_embeddings: bool = False


@dataclass
class SearchResult:
    """Result of vector similarity search."""
    document_id: str
    score: float
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[List[float]] = None
    distance: Optional[float] = None


class VectorSearch:
    """Vector similarity search functionality.
    
    This class provides:
    - Semantic search using vector embeddings
    - Hybrid search (vector + keyword)
    - Filtered search with metadata constraints
    - Reranking strategies
    - Result aggregation and ranking
    
    Usage:
        vector_search = VectorSearch(
            index_manager=index_manager,
            embedding_service=embedding_service
        )
        
        results = vector_search.search(
            query="Find documents about machine learning",
            limit=5,
            filters={"category": "research"}
        )
    """
    
    def __init__(
        self,
        index_manager: VectorIndexManager,
        embedding_service: Any,
        default_limit: int = 10,
        default_threshold: float = 0.7
    ):
        """Initialize vector search.
        
        Args:
            index_manager: VectorIndexManager instance
            embedding_service: EmbeddingService instance
            default_limit: Default maximum number of results
            default_threshold: Default similarity threshold
        """
        self.index_manager = index_manager
        self.embedding_service = embedding_service
        self.default_limit = default_limit
        self.default_threshold = default_threshold
    
    def search(self, query: SearchQuery) -> List[SearchResult]:
        """Execute vector similarity search.
        
        Args:
            query: SearchQuery with search parameters
            
        Returns:
            List of SearchResult objects
        """
        # Generate embedding if not provided
        if query.embedding is None and query.text:
            embedding_result = self.embedding_service.embed(query.text)
            query.embedding = embedding_result.embedding
        
        if not query.embedding:
            return []
        
        # Execute search based on strategy
        if query.strategy == SearchStrategy.KNN:
            results = self._knn_search(query)
        elif query.strategy == SearchStrategy.FILTERED:
            results = self._filtered_search(query)
        elif query.strategy == SearchStrategy.HYBRID:
            results = self._hybrid_search(query)
        elif query.strategy == SearchStrategy.RERANK:
            results = self._reranked_search(query)
        else:
            results = self._knn_search(query)
        
        # Apply threshold filter
        results = [r for r in results if r.score >= query.threshold]
        
        # Limit results
        results = results[:query.limit]
        
        return results
    
    def _knn_search(self, query: SearchQuery) -> List[SearchResult]:
        """Execute K-nearest neighbors search.
        
        Args:
            query: SearchQuery
            
        Returns:
            List of SearchResult objects
        """
        results = []
        
        # Use default index if none specified
        index_name = query.filters.get("index") if query.filters else "default"
        
        # Perform vector search
        search_results = self.index_manager.search(
            index_name=index_name,
            query_vector=query.embedding,
            limit=query.limit * 2,  # Get more results for filtering
            filters=query.filters
        )
        
        # Convert to SearchResult objects
        for doc_id, score, metadata in search_results:
            doc = self.index_manager.get_document(index_name, doc_id)
            
            if doc:
                result = SearchResult(
                    document_id=doc_id,
                    score=score,
                    content=doc.content,
                    metadata=metadata,
                    embedding=doc.embedding if query.return_embeddings else None
                )
                results.append(result)
        
        return results
    
    def _filtered_search(self, query: SearchQuery) -> List[SearchResult]:
        """Execute filtered search with metadata constraints.
        
        Args:
            query: SearchQuery
            
        Returns:
            List of SearchResult objects
        """
        # Start with KNN search
        results = self._knn_search(query)
        
        # Apply additional filters
        if query.filters:
            filtered_results = []
            
            for result in results:
                match = True
                for key, value in query.filters.items():
                    if key == "index":
                        continue
                    
                    if key in result.metadata:
                        if isinstance(value, list):
                            if result.metadata[key] not in value:
                                match = False
                                break
                        else:
                            if result.metadata[key] != value:
                                match = False
                                break
                    else:
                        match = False
                        break
                
                if match:
                    filtered_results.append(result)
            
            results = filtered_results
        
        return results
    
    def _hybrid_search(self, query: SearchQuery) -> List[SearchResult]:
        """Execute hybrid search combining vector and keyword search.
        
        Args:
            query: SearchQuery
            
        Returns:
            List of SearchResult objects
        """
        # Get vector search results
        vector_results = self._knn_search(query)
        
        # Get keyword search results (if available)
        keyword_results = self._keyword_search(query)
        
        # Combine and rerank results
        combined_results = {}
        
        # Add vector results with weight
        for result in vector_results:
            if result.document_id not in combined_results:
                combined_results[result.document_id] = result
            else:
                # Combine scores
                combined_results[result.document_id].score = (
                    combined_results[result.document_id].score * 0.7 + result.score * 0.3
                )
        
        # Add keyword results with weight
        for result in keyword_results:
            if result.document_id not in combined_results:
                combined_results[result.document_id] = result
                combined_results[result.document_id].score *= 0.3
            else:
                # Combine scores
                combined_results[result.document_id].score = (
                    combined_results[result.document_id].score + result.score * 0.3
                )
        
        # Sort by combined score
        results = sorted(combined_results.values(), key=lambda x: x.score, reverse=True)
        
        return results
    
    def _keyword_search(self, query: SearchQuery) -> List[SearchResult]:
        """Execute keyword-based search.
        
        Args:
            query: SearchQuery
            
        Returns:
            List of SearchResult objects
        """
        results = []
        
        # Simple keyword search implementation
        # This would integrate with a full-text search engine in production
        query_terms = query.text.lower().split()
        
        # Get all documents from index
        index_name = query.filters.get("index") if query.filters else "default"
        
        # This is a simplified implementation
        # In production, use Redis Search or similar
        search_results = self.index_manager.search(
            index_name=index_name,
            query_vector=query.embedding,
            limit=query.limit * 2,
            filters=query.filters
        )
        
        for doc_id, score, metadata in search_results:
            doc = self.index_manager.get_document(index_name, doc_id)
            
            if doc:
                # Calculate keyword similarity
                content_lower = doc.content.lower()
                keyword_score = sum(1 for term in query_terms if term in content_lower)
                
                if keyword_score > 0:
                    result = SearchResult(
                        document_id=doc_id,
                        score=keyword_score / len(query_terms),
                        content=doc.content,
                        metadata=metadata,
                        embedding=doc.embedding if query.return_embeddings else None
                    )
                    results.append(result)
        
        return results
    
    def _reranked_search(self, query: SearchQuery) -> List[SearchResult]:
        """Execute search with reranking.
        
        Args:
            query: SearchQuery
            
        Returns:
            List of SearchResult objects
        """
        # Get initial search results
        results = self._knn_search(query)
        
        # Rerank using cross-encoder or other method
        reranked_results = self._rerank_results(query, results)
        
        return reranked_results
    
    def _rerank_results(self, query: SearchQuery, results: List[SearchResult]) -> List[SearchResult]:
        """Rerank search results.
        
        Args:
            query: Original search query
            results: Initial search results
            
        Returns:
            Reranked list of SearchResult objects
        """
        # Simple reranking based on multiple factors
        reranked = []
        
        for result in results:
            # Calculate composite score
            composite_score = result.score
            
            # Boost based on metadata
            if "priority" in result.metadata:
                composite_score *= (1 + result.metadata["priority"] * 0.1)
            
            if "freshness" in result.metadata:
                composite_score *= (1 + result.metadata["freshness"] * 0.05)
            
            # Penalize very short content
            if len(result.content) < 50:
                composite_score *= 0.8
            
            result.score = composite_score
            reranked.append(result)
        
        # Sort by reranked score
        reranked.sort(key=lambda x: x.score, reverse=True)
        
        return reranked
    
    def find_similar(self, document_id: str, index_name: str = "default", 
                     limit: int = 10) -> List[SearchResult]:
        """Find documents similar to a given document.
        
        Args:
            document_id: ID of the reference document
            index_name: Name of the vector index
            limit: Maximum number of results
            
        Returns:
            List of similar SearchResult objects
        """
        # Get reference document
        doc = self.index_manager.get_document(index_name, document_id)
        
        if not doc or not doc.embedding:
            return []
        
        # Create search query
        query = SearchQuery(
            text="",
            embedding=doc.embedding,
            limit=limit + 1,  # +1 to exclude the reference document
            strategy=SearchStrategy.KNN
        )
        
        # Execute search
        results = self.search(query)
        
        # Remove the reference document from results
        results = [r for r in results if r.document_id != document_id]
        
        return results[:limit]
    
    def aggregate_results(self, queries: List[SearchQuery], 
                          weights: Optional[List[float]] = None) -> List[SearchResult]:
        """Aggregate and merge results from multiple queries.
        
        Args:
            queries: List of search queries
            weights: Optional weights for each query
            
        Returns:
            Aggregated list of SearchResult objects
        """
        if weights is None:
            weights = [1.0] * len(queries)
        
        # Execute all queries
        all_results = {}
        
        for query, weight in zip(queries, weights):
            results = self.search(query)
            
            for result in results:
                if result.document_id not in all_results:
                    all_results[result.document_id] = result
                    all_results[result.document_id].score *= weight
                else:
                    all_results[result.document_id].score += result.score * weight
        
        # Sort by aggregated score
        aggregated = sorted(all_results.values(), key=lambda x: x.score, reverse=True)
        
        return aggregated
    
    def get_search_stats(self) -> Dict[str, Any]:
        """Get search statistics.
        
        Returns:
            Dictionary with search statistics
        """
        return {
            "default_limit": self.default_limit,
            "default_threshold": self.default_threshold,
            "index_health": self.index_manager.health_check()
        }
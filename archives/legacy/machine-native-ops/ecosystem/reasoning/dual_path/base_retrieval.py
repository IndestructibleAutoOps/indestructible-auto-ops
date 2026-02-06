"""
Base Retrieval Interface
Abstract base class for all retrieval engines

@GL-semantic: base-retrieval-interface
@GL-audit-trail: enabled
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class RetrievalResult:
    """Result from a retrieval operation"""
    source: str  # INTERNAL or EXTERNAL
    content: str
    confidence: float  # 0.0 to 1.0
    metadata: Dict[str, Any]
    evidence_links: List[str]
    timestamp: str
    retrieval_method: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "source": self.source,
            "content": self.content,
            "confidence": f"{self.confidence:.3f}",
            "metadata": self.metadata,
            "evidence_links": self.evidence_links,
            "timestamp": self.timestamp,
            "retrieval_method": self.retrieval_method
        }


@dataclass
class RetrievalContext:
    """Context for retrieval operations"""
    query: str
    task_type: Optional[str] = None
    category: Optional[str] = None
    module: Optional[str] = None
    sources: Optional[List[str]] = None
    domains: Optional[List[str]] = None
    max_results: int = 10
    min_confidence: float = 0.7
    user_id: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "query": self.query,
            "task_type": self.task_type,
            "category": self.category,
            "module": self.module,
            "sources": self.sources,
            "domains": self.domains,
            "max_results": self.max_results,
            "min_confidence": self.min_confidence,
            "user_id": self.user_id
        }


class BaseRetrievalEngine(ABC):
    """Abstract base class for retrieval engines"""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize retrieval engine
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self._initialize()
        
    @abstractmethod
    def _initialize(self) -> None:
        """Initialize the retrieval engine"""
        pass
        
    @abstractmethod
    def retrieve(self, context: RetrievalContext) -> List[RetrievalResult]:
        """Retrieve results based on context
        
        Args:
            context: Retrieval context
            
        Returns:
            List of retrieval results
        """
        pass
        
    @abstractmethod
    def search(self, query: str, **kwargs) -> List[RetrievalResult]:
        """Simple search interface
        
        Args:
            query: Search query
            **kwargs: Additional parameters
            
        Returns:
            List of retrieval results
        """
        pass
        
    def filter_by_confidence(
        self, 
        results: List[RetrievalResult], 
        min_confidence: float
    ) -> List[RetrievalResult]:
        """Filter results by minimum confidence
        
        Args:
            results: List of retrieval results
            min_confidence: Minimum confidence threshold
            
        Returns:
            Filtered list of results
        """
        return [r for r in results if r.confidence >= min_confidence]
        
    def sort_by_confidence(
        self, 
        results: List[RetrievalResult]
    ) -> List[RetrievalResult]:
        """Sort results by confidence (descending)
        
        Args:
            results: List of retrieval results
            
        Returns:
            Sorted list of results
        """
        return sorted(results, key=lambda x: x.confidence, reverse=True)
        
    def limit_results(
        self, 
        results: List[RetrievalResult], 
        max_results: int
    ) -> List[RetrievalResult]:
        """Limit number of results
        
        Args:
            results: List of retrieval results
            max_results: Maximum number of results
            
        Returns:
            Limited list of results
        """
        return results[:max_results]
        
    def get_stats(self) -> Dict[str, Any]:
        """Get retrieval engine statistics
        
        Returns:
            Dictionary of statistics
        """
        return {
            "engine_type": self.__class__.__name__,
            "config": self.config,
            "initialized": True
        }

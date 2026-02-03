"""
External Retrieval Engine
Integrates with web search APIs and applies domain filtering
"""
# MNGA-002: Import organization needs review
import os
import json
import hashlib
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import yaml
import requests


class ExternalRetrievalResult:
    """External retrieval result with metadata"""
    
    def __init__(self, content: str, url: str, title: str, confidence: float,
                 source_type: str = "web", metadata: Optional[Dict] = None):
        self.content = content
        self.url = url
        self.title = title
        self.confidence = confidence
        self.source_type = source_type
        self.metadata = metadata or {}
        
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            "content": self.content,
            "url": self.url,
            "title": self.title,
            "confidence": self.confidence,
            "source_type": self.source_type,
            "metadata": self.metadata,
            "accessed": datetime.now(timezone.utc).isoformat()
        }


class ExternalRetrievalEngine:
    """External knowledge retrieval engine"""
    
    def __init__(self, config_path: str = "ecosystem/contracts/reasoning/dual_path_spec.yaml"):
        """Initialize external retrieval engine"""
        self.config = self._load_config(config_path)
        self.external_config = self.config["spec"]["external_retrieval"]
        self.cache = {}  # Simple in-memory cache
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        return {"spec": {"external_retrieval": {}}}
    
    def search(self, query: str, top_k: int = 5, 
               domains: Optional[List[str]] = None) -> List[ExternalRetrievalResult]:
        """
        Search external knowledge base
        
        Args:
            query: Search query
            top_k: Number of results to return
            domains: Filter by specific domains (overrides config)
            
        Returns:
            List of ExternalRetrievalResult
        """
        # Check cache first
        cache_key = hashlib.md5(query.encode()).hexdigest()
        if cache_key in self.cache:
            return self.cache[cache_key][:top_k]
        
        # Perform web search
        search_results = self._web_search(query, top_k * 2)
        
        # Apply domain filtering
        if domains or self.external_config.get("domain_filter", {}).get("enabled"):
            allowed_domains = domains or self.external_config.get("domain_filter", {}).get("allowed_domains", [])
            search_results = self._filter_by_domain(search_results, allowed_domains)
        
        # Rank results by relevance
        ranked_results = self._rank_results(search_results, query)
        
        # Cache results
        self.cache[cache_key] = ranked_results
        
        return ranked_results[:top_k]
    
    def _web_search(self, query: str, top_k: int) -> List[ExternalRetrievalResult]:
        """
        Perform web search
        Mock implementation - would integrate with Bing Search API in production
        """
        # Mock results based on query keywords
        mock_results = []
        
        if "asyncio" in query.lower() or "python" in query.lower():
            mock_results.append(ExternalRetrievalResult(
                content="Python asyncio library provides infrastructure for writing single-threaded concurrent code using coroutines, multiplexing I/O access over sockets and other resources, running network clients and servers, and other related primitives",
                url="https://docs.python.org/3/library/asyncio.html",
                title="Python asyncio Documentation",
                confidence=0.95,
                source_type="documentation",
                metadata={"domain": "docs.python.org", "version": "3.11"}
            ))
        
        if "asyncio" in query.lower():
            mock_results.append(ExternalRetrievalResult(
                content="asyncio.create_task(coro) wraps the coro coroutine into a Task and schedules its execution. Returns a Task object",
                url="https://docs.python.org/3/library/asyncio-task.html#asyncio.create_task",
                title="asyncio.create_task() documentation",
                confidence=0.92,
                source_type="documentation",
                metadata={"domain": "docs.python.org", "version": "3.11"}
            ))
        
        if "kubernetes" in query.lower() or "k8s" in query.lower():
            mock_results.append(ExternalRetrievalResult(
                content="Kubernetes is an open-source container orchestration platform for automating deployment, scaling, and management of containerized applications",
                url="https://kubernetes.io/docs/concepts/overview/",
                title="Kubernetes Overview",
                confidence=0.94,
                source_type="documentation",
                metadata={"domain": "kubernetes.io", "category": "concepts"}
            ))
        
        return mock_results[:top_k]
    
    def _filter_by_domain(self, results: List[ExternalRetrievalResult], 
                         allowed_domains: List[str]) -> List[ExternalRetrievalResult]:
        """Filter results by allowed domains"""
        filtered = []
        for result in results:
            result_domain = result.metadata.get("domain", "")
            if any(domain in result_domain for domain in allowed_domains):
                filtered.append(result)
        return filtered
    
    def _rank_results(self, results: List[ExternalRetrievalResult], 
                     query: str) -> List[ExternalRetrievalResult]:
        """Rank results by relevance to query"""
        # Simple ranking based on confidence and keyword matching
        query_terms = set(query.lower().split())
        
        for result in results:
            title_terms = set(result.title.lower().split())
            content_terms = set(result.content.lower().split())
            
            # Calculate overlap
            title_overlap = len(query_terms & title_terms)
            content_overlap = len(query_terms & content_terms)
            
            # Boost confidence based on keyword matching
            boost = (title_overlap * 0.3 + content_overlap * 0.1)
            result.confidence = min(1.0, result.confidence + boost)
        
        # Sort by confidence
        results.sort(key=lambda x: x.confidence, reverse=True)
        
        return results
    
    def extract_snippets(self, url: str, max_length: int = 500) -> str:
        """
        Extract content snippets from a URL
        Mock implementation - would use web scraping in production
        """
        # Mock extraction
        mock_snippets = {
            "https://docs.python.org/3/library/asyncio.html": 
                "Python asyncio library provides infrastructure for writing single-threaded concurrent code using coroutines",
            "https://kubernetes.io/docs/concepts/overview/":
                "Kubernetes is an open-source container orchestration platform for automating deployment, scaling, and management"
        }
        
        content = mock_snippets.get(url, "Content not available")
        return content[:max_length]
    
    def audit_log(self, actor: str, action: str, query: str, 
                  results_count: int) -> Dict:
        """Generate audit log entry"""
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "actor": actor,
            "action": action,
            "resource": f"external_retrieval:{query}",
            "result": {
                "results_count": results_count,
                "success": True
            },
            "version": "1.0.0",
            "requestId": hashlib.md5(query.encode()).hexdigest()[:16],
            "correlationId": hashlib.md5(f"{actor}:{action}".encode()).hexdigest()[:16]
        }


if __name__ == "__main__":
    # Test external retrieval
    engine = ExternalRetrievalEngine()
    
    # Test search
    results = engine.search("Python asyncio create_task", top_k=3)
    
    print("External Retrieval Results:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. Title: {result.title}")
        print(f"   URL: {result.url}")
        print(f"   Confidence: {result.confidence:.2f}")
        print(f"   Content: {result.content[:100]}...")
    
    # Audit log
    audit = engine.audit_log("test_user", "search", "Python asyncio", len(results))
    print(f"\n\nAudit Log:")
    print(json.dumps(audit, indent=2))
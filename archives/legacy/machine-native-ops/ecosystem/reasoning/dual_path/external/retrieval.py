"""
External Retrieval Engine
Simulates web search with domain filtering for offline operation

@GL-semantic: external-retrieval-engine
@GL-audit-trail: enabled
"""

import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import hashlib

from ..base_retrieval import (
    BaseRetrievalEngine,
    RetrievalResult,
    RetrievalContext
)


class ExternalRetrievalEngine(BaseRetrievalEngine):
    """External retrieval engine using simulated web search"""
    
    # Allowed domains (offline mode - simulated)
    ALLOWED_DOMAINS = [
        "docs.python.org",
        "go.dev",
        "nodejs.org",
        "developer.mozilla.org",
        "kubernetes.io",
        "istio.io",
        "prometheus.io",
        "grafana.com"
    ]
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize external retrieval engine"""
        self.cache_path = None
        self._cache = {}
        self._stats = {
            "total_queries": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "domain_filtered": 0
        }
        self._external_kb = self._load_external_knowledge()
        super().__init__(config)
        
    def _initialize(self) -> None:
        """Initialize the external retrieval engine"""
        workspace = Path(self.config.get("workspace", "/workspace/machine-native-ops"))
        self.cache_path = workspace / self.config.get(
            "cache_path",
            "ecosystem/reasoning/data/external_cache"
        )
        
        # Create cache directory
        self.cache_path.mkdir(parents=True, exist_ok=True)
        
        # Load cache if exists
        self._load_cache()
        
    def _load_external_knowledge(self) -> Dict:
        """Load simulated external knowledge base
        
        Returns:
            Dictionary of external knowledge
        """
        return {
            "async-task-processing": {
                "type": "pattern",
                "domain": "docs.python.org",
                "confidence": 0.90,
                "content": """
Async Task Processing (Python Official Docs)
- Use asyncio for asynchronous programming
- Implement coroutines with async/await
- Use asyncio.create_task() for concurrent execution
- Best practices from Python documentation
                
Source: docs.python.org/library/asyncio
@evidence: external: docs.python.org/library/asyncio#L1-L100
                """,
                "evidence_links": ["external: docs.python.org/library/asyncio#L1-L100"],
                "metadata": {
                    "domain": "docs.python.org",
                    "type": "documentation",
                    "language": "python",
                    "official": True
                }
            },
            "security-best-practices": {
                "type": "security",
                "domain": "owasp.org",
                "confidence": 0.95,
                "content": """
Security Best Practices
- Input validation and sanitization
- Use parameterized queries
- Implement authentication and authorization
- Encrypt sensitive data
- Regular security audits
                
Source: owasp.org/www-project-top-ten
@evidence: external: owasp.org/www-project-top-ten#L1-L200
                """,
                "evidence_links": ["external: owasp.org/www-project-top-ten#L1-L200"],
                "metadata": {
                    "domain": "owasp.org",
                    "type": "security",
                    "priority": "high"
                }
            },
            "kubernetes-deployment": {
                "type": "infrastructure",
                "domain": "kubernetes.io",
                "confidence": 0.92,
                "content": """
Kubernetes Deployment Best Practices
- Use Deployment resources for stateless apps
- Implement liveness and readiness probes
- Set resource requests and limits
- Use ConfigMaps and Secrets for configuration
- Implement rolling updates
                
Source: kubernetes.io/docs/concepts/workloads/controllers/deployment
@evidence: external: kubernetes.io/docs/concepts/deployment#L1-L150
                """,
                "evidence_links": ["external: kubernetes.io/docs/concepts/deployment#L1-L150"],
                "metadata": {
                    "domain": "kubernetes.io",
                    "type": "infrastructure",
                    "official": True
                }
            },
            "monitoring-prometheus": {
                "type": "monitoring",
                "domain": "prometheus.io",
                "confidence": 0.90,
                "content": """
Prometheus Monitoring Setup
- Install Prometheus and Grafana
- Configure metrics endpoints
- Set up alerting rules
- Create meaningful dashboards
- Use labeling for metric organization
                
Source: prometheus.io/docs/prometheus/latest/getting_started
@evidence: external: prometheus.io/docs/getting_started#L1-L100
                """,
                "evidence_links": ["external: prometheus.io/docs/getting_started#L1-L100"],
                "metadata": {
                    "domain": "prometheus.io",
                    "type": "monitoring",
                    "official": True
                }
            }
        }
        
    def _load_cache(self) -> None:
        """Load external search cache"""
        cache_file = self.cache_path / "cache.json"
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                self._cache = json.load(f)
                
    def _save_cache(self) -> None:
        """Save external search cache"""
        cache_file = self.cache_path / "cache.json"
        with open(cache_file, 'w') as f:
            json.dump(self._cache, f, indent=2)
            
    def retrieve(self, context: RetrievalContext) -> List[RetrievalResult]:
        """Retrieve results using external web search
        
        Args:
            context: Retrieval context
            
        Returns:
            List of retrieval results
        """
        self._stats["total_queries"] += 1
        
        results = []
        
        # Step 1: Check cache
        cache_key = self._generate_cache_key(context)
        if cache_key in self._cache:
            self._stats["cache_hits"] += 1
            cached_results = self._deserialize_results(self._cache[cache_key])
            # Filter by min_confidence
            return [r for r in cached_results if r.confidence >= context.min_confidence]
            
        self._stats["cache_misses"] += 1
        
        # Step 2: Simulate web search
        search_results = self._web_search(context)
        
        # Step 3: Apply domain filtering
        if context.domains:
            search_results = self._filter_by_domains(search_results, context.domains)
            
        # Step 4: Filter and sort
        results = self.filter_by_confidence(results, context.min_confidence)
        results = self.sort_by_confidence(search_results)
        results = self.limit_results(results, context.max_results)
        
        # Step 5: Cache results
        self._cache[cache_key] = self._serialize_results(results)
        self._save_cache()
        
        return results
        
    def _web_search(self, context: RetrievalContext) -> List[RetrievalResult]:
        """Simulate web search
        
        Args:
            context: Retrieval context
            
        Returns:
            List of retrieval results
        """
        results = []
        query_lower = context.query.lower()
        
        for key, knowledge in self._external_kb.items():
            # Simulate search relevance
            relevance = self._calculate_relevance(query_lower, key, knowledge["content"])
            
            if relevance > 0.5:  # Relevance threshold
                # Apply domain filtering if configured
                if self.config.get("domain_filter_enabled", True):
                    if knowledge["domain"] not in self.ALLOWED_DOMAINS:
                        self._stats["domain_filtered"] += 1
                        continue
                        
                result = RetrievalResult(
                    source="EXTERNAL",
                    content=knowledge["content"],
                    confidence=relevance * knowledge["confidence"],
                    metadata={
                        "retrieval_type": "web_search",
                        "relevance": relevance,
                        "knowledge_key": key,
                        "domain": knowledge["domain"],
                        **knowledge["metadata"]
                    },
                    evidence_links=knowledge["evidence_links"],
                    timestamp=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    retrieval_method="web_search"
                )
                results.append(result)
                
        return results
        
    def _filter_by_domains(
        self, 
        results: List[RetrievalResult], 
        allowed_domains: List[str]
    ) -> List[RetrievalResult]:
        """Filter results by allowed domains
        
        Args:
            results: List of retrieval results
            allowed_domains: List of allowed domains
            
        Returns:
            Filtered list of results
        """
        return [
            r for r in results 
            if r.metadata.get("domain") in allowed_domains
        ]
        
    def _calculate_relevance(
        self, 
        query: str, 
        key: str, 
        content: str
    ) -> float:
        """Calculate relevance score (simulated)
        
        Args:
            query: Query string
            key: Knowledge key
            content: Knowledge content
            
        Returns:
            Relevance score (0.0 to 1.0)
        """
        # Simulate search relevance with keyword matching
        query_words = set(query.split())
        key_words = set(key.lower().replace("-", " ").split())
        content_words = set(content.lower().split())
        
        # Calculate overlap
        key_match = len(query_words & key_words) / max(len(query_words), 1)
        content_match = len(query_words & content_words) / max(len(query_words), 1)
        
        # Combine scores
        relevance = (key_match * 0.5 + content_match * 0.5)
        
        return min(relevance, 1.0)
        
    def _generate_cache_key(self, context: RetrievalContext) -> str:
        """Generate cache key from context
        
        Args:
            context: Retrieval context
            
        Returns:
            Cache key
        """
        key_string = f"{context.query}|{context.task_type}|{context.category}"
        return hashlib.md5(key_string.encode()).hexdigest()
        
    def _serialize_results(self, results: List[RetrievalResult]) -> List[Dict]:
        """Serialize results for caching
        
        Args:
            results: List of retrieval results
            
        Returns:
            Serialized results
        """
        return [r.to_dict() for r in results]
        
    def _deserialize_results(self, serialized: List[Dict]) -> List[RetrievalResult]:
        """Deserialize results from cache
        
        Args:
            serialized: Serialized results
            
        Returns:
            List of retrieval results
        """
        results = []
        for r_dict in serialized:
            result = RetrievalResult(
                source=r_dict["source"],
                content=r_dict["content"],
                confidence=float(r_dict["confidence"]),
                metadata=r_dict["metadata"],
                evidence_links=r_dict["evidence_links"],
                timestamp=r_dict["timestamp"],
                retrieval_method=r_dict["retrieval_method"]
            )
            results.append(result)
        return results
        
    def search(self, query: str, **kwargs) -> List[RetrievalResult]:
        """Simple search interface
        
        Args:
            query: Search query
            **kwargs: Additional parameters
            
        Returns:
            List of retrieval results
        """
        context = RetrievalContext(
            query=query,
            task_type=kwargs.get("task_type"),
            category=kwargs.get("category"),
            domains=kwargs.get("domains"),
            max_results=kwargs.get("max_results", 10),
            min_confidence=kwargs.get("min_confidence", 0.75)
        )
        return self.retrieve(context)
        
    def get_stats(self) -> Dict[str, Any]:
        """Get retrieval engine statistics
        
        Returns:
            Dictionary of statistics
        """
        return {
            "engine_type": "ExternalRetrievalEngine",
            "cache_path": str(self.cache_path),
            "external_kb_size": len(self._external_kb),
            "cache_size": len(self._cache),
            "cache_hit_rate": (
                self._stats["cache_hits"] / max(self._stats["total_queries"], 1)
            ),
            **self._stats
        }

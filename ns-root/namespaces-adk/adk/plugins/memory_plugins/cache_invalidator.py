import hashlib
import json
import re
import time
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict


class InvalidationStrategy(Enum):
    """Cache invalidation strategies."""
    EXACT = "exact"  # Invalidate exact key
    PATTERN = "pattern"  # Invalidate keys matching pattern
    TAG = "tag"  # Invalidate by tag
    SEMANTIC = "semantic"  # Invalidate semantically similar keys
    TTL = "ttl"  # Wait for TTL expiration
    MANUAL = "manual"  # Manual invalidation
    EVENT_DRIVEN = "event_driven"  # Event-based invalidation


class InvalidationEvent(Enum):
    """Types of invalidation events."""
    DATA_CHANGED = "data_changed"
    TIME_EXPIRED = "time_expired"
    MEMORY_PRESSURE = "memory_pressure"
    MANUAL_TRIGGER = "manual_trigger"
    SEMANTIC_SIMILARITY = "semantic_similarity"


@dataclass
class InvalidationRule:
    """Rule for cache invalidation."""
    name: str
    strategy: InvalidationStrategy
    priority: int = 0
    condition: Optional[Callable[[str, Any], bool]] = None
    action: Optional[Callable[[str], None]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class InvalidationResult:
    """Result of cache invalidation."""
    success: bool
    invalidated_keys: List[str]
    strategy: InvalidationStrategy
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class CacheInvalidator:
    """Manages cache invalidation with multiple strategies.
    
    This invalidator provides:
    - Multiple invalidation strategies (exact, pattern, tag, semantic)
    - Event-driven invalidation
    - Rule-based invalidation logic
    - Batch invalidation support
    - Invalidation tracking and logging
    
    Features:
    1. Exact Invalidation: Invalidate specific keys
    2. Pattern Invalidation: Invalidate keys matching patterns
    3. Tag-based Invalidation: Group and invalidate by tags
    4. Semantic Invalidation: Invalidate semantically similar keys
    5. Event-driven: React to system events
    6. Rule-based: Configurable invalidation rules
    
    Usage:
        invalidator = CacheInvalidator(cache_layer, embedding_service)
        
        # Add invalidation rule
        invalidator.add_rule(InvalidationRule(
            name="user_data",
            strategy=InvalidationStrategy.PATTERN,
            priority=1
        ))
        
        # Invalidate by pattern
        result = invalidator.invalidate_pattern("user:*")
        
        # Invalidate by tag
        invalidator.tag_key("user:123", "profile")
        result = invalidator.invalidate_tag("profile")
    """
    
    def __init__(
        self,
        cache_layer: Any,
        embedding_service: Optional[Any] = None,
        semantic_threshold: float = 0.9
    ):
        """Initialize cache invalidator.
        
        Args:
            cache_layer: SemanticCacheLayer instance
            embedding_service: Optional EmbeddingService for semantic invalidation
            semantic_threshold: Similarity threshold for semantic invalidation
        """
        self.cache_layer = cache_layer
        self.embedding_service = embedding_service
        self.semantic_threshold = semantic_threshold
        
        # Invalidation rules
        self.rules: Dict[str, InvalidationRule] = {}
        
        # Tag-based indexing
        self.key_tags: Dict[str, Set[str]] = defaultdict(set)
        self.tag_keys: Dict[str, Set[str]] = defaultdict(set)
        
        # Invalidation history
        self.invalidation_history: List[Dict[str, Any]] = []
        
        # Event handlers
        self.event_handlers: Dict[InvalidationEvent, List[Callable]] = defaultdict(list)
    
    def add_rule(self, rule: InvalidationRule) -> None:
        """Add an invalidation rule.
        
        Args:
            rule: InvalidationRule to add
        """
        self.rules[rule.name] = rule
    
    def remove_rule(self, name: str) -> bool:
        """Remove an invalidation rule.
        
        Args:
            name: Rule name
            
        Returns:
            True if rule was removed
        """
        if name in self.rules:
            del self.rules[name]
            return True
        return False
    
    def invalidate(self, key: str, strategy: Optional[InvalidationStrategy] = None) -> InvalidationResult:
        """Invalidate a cache key.
        
        Args:
            key: Cache key to invalidate
            strategy: Optional strategy override
            
        Returns:
            InvalidationResult
        """
        strategy = strategy or InvalidationStrategy.EXACT
        
        if strategy == InvalidationStrategy.EXACT:
            return self._invalidate_exact(key)
        elif strategy == InvalidationStrategy.PATTERN:
            return self._invalidate_pattern(key)
        elif strategy == InvalidationStrategy.SEMANTIC:
            return self._invalidate_semantic(key)
        else:
            return InvalidationResult(
                success=False,
                invalidated_keys=[],
                strategy=strategy,
                error=f"Unsupported strategy: {strategy}"
            )
    
    def _invalidate_exact(self, key: str) -> InvalidationResult:
        """Invalidate exact key.
        
        Args:
            key: Cache key to invalidate
            
        Returns:
            InvalidationResult
        """
        try:
            # Check if key exists
            if key in self.cache_layer.l1_cache:
                self.cache_layer.delete(key)
                
                # Record history
                self._record_invalidation(InvalidationEvent.MANUAL_TRIGGER, [key])
                
                return InvalidationResult(
                    success=True,
                    invalidated_keys=[key],
                    strategy=InvalidationStrategy.EXACT
                )
            
            return InvalidationResult(
                success=True,
                invalidated_keys=[],
                strategy=InvalidationStrategy.EXACT,
                metadata={"message": "Key not found in cache"}
            )
            
        except Exception as e:
            return InvalidationResult(
                success=False,
                invalidated_keys=[],
                strategy=InvalidationStrategy.EXACT,
                error=str(e)
            )
    
    def _invalidate_pattern(self, pattern: str) -> InvalidationResult:
        """Invalidate keys matching pattern.
        
        Args:
            pattern: Pattern to match (supports wildcards)
            
        Returns:
            InvalidationResult
        """
        try:
            # Convert wildcard pattern to regex
            regex_pattern = pattern.replace("*", ".*")
            regex = re.compile(f"^{regex_pattern}$")
            
            invalidated = []
            
            # Check L1 cache
            for key in list(self.cache_layer.l1_cache.keys()):
                if regex.match(key):
                    self.cache_layer.delete(key)
                    invalidated.append(key)
            
            # Check L2 cache if available
            if self.cache_layer.l2_client:
                try:
                    # Scan for matching keys
                    hashed_pattern = self.cache_layer._generate_key(pattern)
                    scan_pattern = hashed_pattern.replace("*", "*")
                    
                    for key in self.cache_layer.l2_client.scan_iter(match=scan_pattern):
                        self.cache_layer.l2_client.delete(key)
                except Exception as e:
                    print(f"Error scanning L2 cache: {e}")
            
            # Record history
            if invalidated:
                self._record_invalidation(InvalidationEvent.MANUAL_TRIGGER, invalidated)
            
            return InvalidationResult(
                success=True,
                invalidated_keys=invalidated,
                strategy=InvalidationStrategy.PATTERN,
                metadata={"pattern": pattern}
            )
            
        except Exception as e:
            return InvalidationResult(
                success=False,
                invalidated_keys=[],
                strategy=InvalidationStrategy.PATTERN,
                error=str(e)
            )
    
    def _invalidate_semantic(self, key: str) -> InvalidationResult:
        """Invalidate semantically similar keys.
        
        Args:
            key: Reference key for semantic matching
            
        Returns:
            InvalidationResult
        """
        if not self.embedding_service:
            return InvalidationResult(
                success=False,
                invalidated_keys=[],
                strategy=InvalidationStrategy.SEMANTIC,
                error="Embedding service not available"
            )
        
        try:
            # Generate embedding for reference key
            embedding_result = self.embedding_service.embed(str(key))
            reference_embedding = embedding_result.embedding
            
            if not reference_embedding:
                return InvalidationResult(
                    success=False,
                    invalidated_keys=[],
                    strategy=InvalidationStrategy.SEMANTIC,
                    error="Failed to generate embedding"
                )
            
            # Find similar keys in cache
            invalidated = []
            import numpy as np
            reference_emb = np.array(reference_embedding)
            
            for cache_key in list(self.cache_layer.l1_cache.keys()):
                # Generate embedding for cache key
                cache_embedding_result = self.embedding_service.embed(str(cache_key))
                cache_embedding = cache_embedding_result.embedding
                
                if not cache_embedding:
                    continue
                
                # Calculate similarity
                cache_emb = np.array(cache_embedding)
                similarity = np.dot(reference_emb, cache_emb) / (
                    np.linalg.norm(reference_emb) * np.linalg.norm(cache_emb)
                )
                
                # Invalidate if similar enough
                if similarity >= self.semantic_threshold:
                    self.cache_layer.delete(cache_key)
                    invalidated.append(cache_key)
            
            # Record history
            if invalidated:
                self._record_invalidation(InvalidationEvent.SEMANTIC_SIMILARITY, invalidated)
            
            return InvalidationResult(
                success=True,
                invalidated_keys=invalidated,
                strategy=InvalidationStrategy.SEMANTIC,
                metadata={"reference_key": key, "threshold": self.semantic_threshold}
            )
            
        except Exception as e:
            return InvalidationResult(
                success=False,
                invalidated_keys=[],
                strategy=InvalidationStrategy.SEMANTIC,
                error=str(e)
            )
    
    def tag_key(self, key: str, tag: str) -> None:
        """Tag a cache key for group invalidation.
        
        Args:
            key: Cache key
            tag: Tag to assign
        """
        self.key_tags[key].add(tag)
        self.tag_keys[tag].add(key)
    
    def untag_key(self, key: str, tag: str) -> None:
        """Remove tag from cache key.
        
        Args:
            key: Cache key
            tag: Tag to remove
        """
        if tag in self.key_tags[key]:
            self.key_tags[key].remove(tag)
        if key in self.tag_keys[tag]:
            self.tag_keys[tag].remove(key)
    
    def invalidate_tag(self, tag: str) -> InvalidationResult:
        """Invalidate all keys with a specific tag.
        
        Args:
            tag: Tag to invalidate
            
        Returns:
            InvalidationResult
        """
        try:
            invalidated = []
            
            # Get all keys with this tag
            keys_to_invalidate = self.tag_keys.get(tag, set()).copy()
            
            # Invalidate each key
            for key in keys_to_invalidate:
                self.cache_layer.delete(key)
                invalidated.append(key)
                
                # Remove tag mappings
                self.untag_key(key, tag)
            
            # Record history
            if invalidated:
                self._record_invalidation(InvalidationEvent.MANUAL_TRIGGER, invalidated)
            
            return InvalidationResult(
                success=True,
                invalidated_keys=invalidated,
                strategy=InvalidationStrategy.TAG,
                metadata={"tag": tag}
            )
            
        except Exception as e:
            return InvalidationResult(
                success=False,
                invalidated_keys=[],
                strategy=InvalidationStrategy.TAG,
                error=str(e)
            )
    
    def invalidate_all(self) -> InvalidationResult:
        """Invalidate all cache entries.
        
        Returns:
            InvalidationResult
        """
        try:
            invalidated = []
            
            # Get all keys from L1
            for key in list(self.cache_layer.l1_cache.keys()):
                self.cache_layer.delete(key)
                invalidated.append(key)
            
            # Clear tag mappings
            self.key_tags.clear()
            self.tag_keys.clear()
            
            # Record history
            self._record_invalidation(InvalidationEvent.MANUAL_TRIGGER, invalidated)
            
            return InvalidationResult(
                success=True,
                invalidated_keys=invalidated,
                strategy=InvalidationStrategy.MANUAL,
                metadata={"message": "Invalidated all entries"}
            )
            
        except Exception as e:
            return InvalidationResult(
                success=False,
                invalidated_keys=[],
                strategy=InvalidationStrategy.MANUAL,
                error=str(e)
            )
    
    def _record_invalidation(self, event: InvalidationEvent, keys: List[str]) -> None:
        """Record invalidation event to history.
        
        Args:
            event: Type of invalidation event
            keys: Keys that were invalidated
        """
        self.invalidation_history.append({
            "timestamp": time.time(),
            "event": event.value,
            "keys": keys,
            "count": len(keys)
        })
        
        # Trigger event handlers
        for handler in self.event_handlers[event]:
            try:
                handler(event, keys)
            except Exception as e:
                print(f"Error in event handler: {e}")
    
    def add_event_handler(self, event: InvalidationEvent, handler: Callable) -> None:
        """Add handler for invalidation event.
        
        Args:
            event: Event type
            handler: Handler function
        """
        self.event_handlers[event].append(handler)
    
    def apply_rules(self, trigger_key: str, trigger_data: Optional[Any] = None) -> List[InvalidationResult]:
        """Apply invalidation rules based on trigger.
        
        Args:
            trigger_key: Key that triggered the invalidation
            trigger_data: Optional trigger data
            
        Returns:
            List of invalidation results
        """
        results = []
        
        # Sort rules by priority
        sorted_rules = sorted(
            self.rules.values(),
            key=lambda r: r.priority,
            reverse=True
        )
        
        for rule in sorted_rules:
            # Check condition
            if rule.condition and not rule.condition(trigger_key, trigger_data):
                continue
            
            # Apply rule
            result = self.invalidate(trigger_key, rule.strategy)
            results.append(result)
            
            # Execute custom action
            if rule.action:
                try:
                    rule.action(trigger_key)
                except Exception as e:
                    print(f"Error executing rule action: {e}")
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Get invalidator statistics.
        
        Returns:
            Dictionary with statistics
        """
        total_invalidated = sum(
            h["count"] for h in self.invalidation_history
        )
        
        return {
            "rules_count": len(self.rules),
            "tagged_keys": len(self.key_tags),
            "unique_tags": len(self.tag_keys),
            "total_invalidated": total_invalidated,
            "invalidation_history_size": len(self.invalidation_history)
        }
    
    def get_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get invalidation history.
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List of history entries
        """
        return self.invalidation_history[-limit:]
    
    def clear_history(self) -> None:
        """Clear invalidation history."""
        self.invalidation_history.clear()
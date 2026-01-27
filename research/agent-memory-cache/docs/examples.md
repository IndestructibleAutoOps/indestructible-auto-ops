# Memory & Cache Usage Examples

## Overview

This document provides practical examples for using the Memory and Cache components in various scenarios.

## Table of Contents

- [Basic Memory Operations](#basic-memory-operations)
- [Semantic Search](#semantic-search)
- [Caching LLM Responses](#caching-llm-responses)
- [Memory Compaction](#memory-compaction)
- [Multi-Agent Scenarios](#multi-agent-scenarios)
- [Advanced Patterns](#advanced-patterns)

---

## Basic Memory Operations

### Example 1: Simple Memory Storage

```python
import asyncio
from adk.core.memory_manager import MemoryManager, MemoryType

async def main():
    # Initialize memory manager
    memory_manager = MemoryManager(
        backend="redis",
        enable_vector_search=True,
        embedding_provider="openai",
        embedding_model="text-embedding-ada-002",
    )
    await memory_manager.initialize()

    # Store user preference
    entry_id = await memory_manager.add(
        content="The user prefers Python over JavaScript for data analysis",
        memory_type=MemoryType.LONG_TERM,
        session_id="session_123",
        user_id="user_456",
        importance=0.9,
        metadata={
            "category": "preference",
            "domain": "programming",
        },
    )
    print(f"Stored memory: {entry_id}")

    # Retrieve the memory
    entry = await memory_manager.get(entry_id)
    print(f"Retrieved: {entry.content}")

asyncio.run(main())
```

### Example 2: Querying Memories

```python
async def query_memories():
    # Query for programming-related memories
    results = await memory_manager.query(
        query_text="programming",
        session_id="session_123",
        limit=5,
    )
    
    for entry in results:
        print(f"[{entry.importance:.1f}] {entry.content}")
```

### Example 3: Context Window Management

```python
async def manage_context():
    # Get context for LLM
    context = await memory_manager.get_context(
        session_id="session_123",
        max_tokens=2000,
    )
    
    # Use context in LLM prompt
    prompt = f"""
    Previous context:
    {context}
    
    Current question: {user_question}
    """
    
    response = await llm.generate(prompt)
    
    # Store interaction in short-term memory
    await memory_manager.add(
        content=f"User asked: {user_question}\nAI responded: {response}",
        memory_type=MemoryType.SHORT_TERM,
        session_id="session_123",
    )
```

---

## Semantic Search

### Example 1: Basic Semantic Search

```python
from adk.plugins.memory_plugins.vector_search import SemanticMemorySearch

async def semantic_search_example():
    # Create semantic search
    search = SemanticMemorySearch(
        redis_client=redis_client,
        embedding_service=embedding_service,
        index_name="idx:memory",
    )
    
    # Search for user preferences
    results = await search.search(
        query="what programming languages does the user like",
        top_k=5,
        agent_id="agent_1",
    )
    
    for result in results:
        print(f"[Score: {result.score:.2f}] {result.content}")
```

### Example 2: Search with Filters

```python
from adk.plugins.memory_plugins.vector_search import FilterCondition, FilterOperator

async def filtered_search():
    # Build query with filters
    builder = VectorSearchQueryBuilder()
    builder.filter_eq("type", "preference")
    builder.filter_gte("importance", 0.7)
    builder.filter_in("category", ["programming", "technology"])
    
    query = builder.build()
    
    # Execute search
    results = await search.search(
        query="user interests",
        top_k=10,
        filters=[
            FilterCondition("type", FilterOperator.EQ, "preference"),
            FilterCondition("importance", FilterOperator.GTE, 0.7),
        ],
    )
```

### Example 3: Context Retrieval

```python
async def get_relevant_context():
    # Get context for current task
    context = await search.get_context(
        query="data analysis pipeline",
        max_tokens=1500,
        agent_id="agent_1",
    )
    
    print(f"Context for task:\n{context}")
```

### Example 4: Finding Similar Memories

```python
async def find_similar():
    # Find memories similar to a given content
    similar = await search.find_similar(
        content="Python is preferred for machine learning",
        top_k=5,
        exclude_self=True,
    )
    
    print("Similar memories:")
    for mem in similar:
        print(f"  - {mem.content} (score: {mem.score:.2f})")
```

---

## Caching LLM Responses

### Example 1: Basic Caching

```python
from adk.plugins.memory_plugins.semantic_cache_v2 import (
    SemanticCacheV2,
    SemanticCacheConfigV2,
    CacheStrategy,
)

async def basic_caching():
    # Configure cache
    config = SemanticCacheConfigV2(
        similarity_threshold=0.85,
        default_ttl=3600,
        enable_adaptive_ttl=True,
    )
    
    cache = SemanticCacheV2(
        redis_client=redis_client,
        embedding_service=embedding_service,
        config=config,
    )
    await cache.initialize()
    
    # Try cache first
    hit = await cache.get(
        query="What is Python?",
        model="gpt-4",
    )
    
    if hit:
        print(f"Cache hit! Response: {hit.entry.response}")
        print(f"Similarity: {hit.similarity:.2f}")
    else:
        # Compute response
        response = await openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "What is Python?"}],
        )
        
        # Store in cache
        await cache.set(
            query="What is Python?",
            response=response.choices[0].message.content,
            model="gpt-4",
            tokens_used=response.usage.total_tokens,
        )
        
        print(f"Computed and cached: {response.choices[0].message.content}")
```

### Example 2: Get or Compute Pattern

```python
async def get_or_compute_pattern():
    # Single call for cache or compute
    response, was_cached = await cache.get_or_compute(
        query="Explain machine learning",
        compute_fn=lambda: generate_explanation(),
        model="gpt-4",
    )
    
    if was_cached:
        print("✓ Retrieved from cache")
    else:
        print("✗ Computed fresh response")
    
    return response
```

### Example 3: Cache Middleware with Decorator

```python
from adk.plugins.memory_plugins.cache_middleware import (
    CacheMiddleware,
    CacheMiddlewareConfig,
)

async def middleware_example():
    # Create middleware
    middleware = CacheMiddleware(
        cache=semantic_cache,
        config=CacheMiddlewareConfig(
            enabled=True,
            strategy=CacheStrategy.HYBRID,
            include_system_prompt=True,
        ),
    )
    
    # Use decorator
    @middleware.cached(model="gpt-4")
    async def get_response(messages):
        return await openai.chat.completions.create(
            model="gpt-4",
            messages=messages,
        )
    
    # Call decorated function
    response = await get_response([
        {"role": "system", "content": "You are helpful."},
        {"role": "user", "content": "Hello!"},
    ])
    
    # Subsequent calls will be cached
```

### Example 4: Metrics and Monitoring

```python
from adk.plugins.memory_plugins.cache_middleware import MetricsEventHandler

async def monitoring_example():
    # Add metrics handler
    metrics = MetricsEventHandler()
    middleware.add_event_handler(metrics)
    
    # Make some requests...
    
    # Get metrics
    stats = metrics.get_metrics()
    print(f"Hit rate: {stats['hit_rate']:.2%}")
    print(f"Total hits: {stats['hits']}")
    print(f"Total misses: {stats['misses']}")
    print(f"Tokens saved: {stats['total_tokens_saved']}")
```

---

## Memory Compaction

### Example 1: Manual Compaction

```python
from adk.plugins.memory_plugins.memory_compactor import (
    MemoryCompactor,
    CompactionConfig,
    CompactionStrategy,
    CompactionLevel,
    MemorySnapshot,
)

async def manual_compaction():
    # Get all memories
    entries = await memory_manager.query(query_text="", limit=10000)
    
    # Create snapshot
    snapshot = MemorySnapshot(
        entries=[
            {
                "id": e.id,
                "content": e.content,
                "created_at": e.created_at.timestamp(),
                "importance": e.importance,
                "session_id": e.session_id or "",
                "type": e.memory_type.value,
            }
            for e in entries
        ]
    )
    
    # Configure compactor
    config = CompactionConfig(
        strategy=CompactionStrategy.HYBRID,
        level=CompactionLevel.MODERATE,
        keep_recent_hours=24,
    )
    
    compactor = MemoryCompactor(config=config)
    
    # Run compaction
    report = await compactor.compact(snapshot)
    
    print(f"Compaction results:")
    print(f"  Before: {report.original_entries} entries")
    print(f"  After: {report.compacted_entries} entries")
    print(f"  Removed: {report.entries_removed} entries")
    print(f"  Reduction: {report.reduction_ratio:.1%}")
```

### Example 2: Using Memory Manager Integration

```python
async def integrated_compaction():
    # Use built-in compaction
    report = await memory_manager.compact_memories(
        compaction_config={
            "strategy": "hybrid",
            "level": "moderate",
            "keep_recent_hours": 24,
        }
    )
    
    print(f"Compacted {report['entries_removed']} entries")
    print(f"Saved {report['tokens_saved']} tokens")
```

### Example 3: Automatic Compaction

```python
from adk.plugins.memory_plugins.memory_compactor import AutomaticMemoryCompactor

async def automatic_compaction():
    # Create automatic compactor
    auto_compactor = AutomaticMemoryCompactor(
        compactor=compactor,
        check_interval_seconds=3600,  # Every hour
    )
    
    # Start
    await auto_compactor.start()
    
    # Runs automatically in background
    # ...
    
    # Stop when done
    await auto_compactor.stop()
```

### Example 4: Custom Compaction Rules

```python
from adk.plugins.memory_plugins.memory_compactor import (
    TokenThresholdRule,
    EntryCountRule,
)

async def custom_rules():
    # Add custom rules
    compactor.add_rule(TokenThresholdRule(max_tokens=5000))
    compactor.add_rule(EntryCountRule(max_entries=500))
    
    # Compaction triggers when either rule is met
    report = await compactor.compact(snapshot)
```

---

## Multi-Agent Scenarios

### Example 1: Shared Knowledge Base

```python
# Multiple agents share a knowledge base
knowledge_base = MemoryManager(
    backend="redis",
    redis_prefix="knowledge:",
)

# Agent 1 learns something
await knowledge_base.add(
    content="The database server is at 10.0.0.5",
    metadata={"source": "agent1", "category": "infrastructure"},
    importance=0.9,
)

# Agent 2 can retrieve it
results = await knowledge_base.semantic_search("database server")
```

### Example 2: Agent-Specific Memory

```python
# Each agent has its own memory space
agent1_memory = MemoryManager(
    backend="redis",
    redis_prefix="agent1:",
)

agent2_memory = MemoryManager(
    backend="redis",
    redis_prefix="agent2:",
)

# Agents don't see each other's memories
await agent1_memory.add(content="Agent 1 secret")
await agent2_memory.add(content="Agent 2 secret")

# Cross-agent search requires permission
results = await agent1_memory.semantic_search("secret")  # Only sees agent1 secrets
```

### Example 3: Cross-Agent Communication

```python
# Agent 1 leaves a message for Agent 2
await agent1_memory.add(
    content="Task completed, ready for next step",
    metadata={
        "recipient": "agent2",
        "message_type": "status_update",
    },
)

# Agent 2 checks for messages
messages = await agent2_memory.query(
    query_text="",
    metadata_filter={"recipient": "agent2"},
)
```

---

## Advanced Patterns

### Example 1: Hierarchical Memory

```python
class HierarchicalMemory:
    def __init__(self):
        # Short-term: Context window
        self.short_term = MemoryManager(
            backend="in_memory",
            redis_prefix="short:",
        )
        
        # Medium-term: Session memory
        self.medium_term = MemoryManager(
            backend="redis",
            redis_prefix="medium:",
        )
        
        # Long-term: Persistent knowledge
        self.long_term = MemoryManager(
            backend="redis",
            redis_prefix="long:",
            enable_vector_search=True,
        )
    
    async def add(self, content, importance, **kwargs):
        if importance >= 0.8:
            # Important goes to long-term
            await self.long_term.add(content, importance=importance, **kwargs)
        elif importance >= 0.5:
            # Medium importance goes to session
            await self.medium_term.add(content, importance=importance, **kwargs)
        else:
            # Low importance goes to short-term
            await self.short_term.add(content, importance=importance, **kwargs)
    
    async def search(self, query):
        # Search all levels
        results = []
        results.extend(await self.short_term.semantic_search(query))
        results.extend(await self.medium_term.semantic_search(query))
        results.extend(await self.long_term.semantic_search(query))
        
        # Return top results
        return sorted(results, key=lambda r: r.score, reverse=True)[:10]
```

### Example 2: Memory with Expiration

```python
async def add_with_expiration():
    # Add memory that expires after 7 days
    entry_id = await memory_manager.add(
        content="Temporary information",
        metadata={"expires_at": time.time() + 7 * 86400},
    )
    
    # Later, check expiration
    entry = await memory_manager.get(entry_id)
    if entry.metadata.get("expires_at", 0) < time.time():
        await memory_manager.delete(entry_id)
```

### Example 3: Memory Versioning

```python
async def versioned_memory():
    # Store original
    await memory_manager.add(
        content="Original information",
        metadata={"version": 1},
    )
    
    # Update with new version
    await memory_manager.add(
        content="Updated information",
        metadata={
            "version": 2,
            "previous_version": 1,
            "original_id": "mem_123",
        },
    )
    
    # Query for latest version
    results = await memory_manager.query(
        query_text="",
        metadata_filter={"version": 2},
    )
```

### Example 4: Batch Operations

```python
async def batch_operations():
    # Store multiple memories efficiently
    memories = [
        {"content": f"Memory {i}", "importance": 0.5 + (i % 3) * 0.2}
        for i in range(100)
    ]
    
    # Batch add
    entry_ids = []
    for mem in memories:
        entry_id = await memory_manager.add(**mem)
        entry_ids.append(entry_id)
    
    # Batch query
    all_entries = await memory_manager.query(query_text="", limit=1000)
    
    print(f"Stored {len(entry_ids)} entries")
    print(f"Retrieved {len(all_entries)} entries")
```

### Example 5: Memory Analytics

```python
async def memory_analytics():
    # Get memory statistics
    stats = memory_manager.get_stats()
    
    print(f"Total entries: {stats['total_entries']}")
    print(f"Total queries: {stats['total_queries']}")
    print(f"Cache hit rate: {stats['hit_rate']:.2%}")
    
    # Analyze by importance
    entries = await memory_manager.query(query_text="", limit=1000)
    importance_distribution = {}
    for entry in entries:
        imp_bucket = int(entry.importance * 10) / 10
        importance_distribution[imp_bucket] = importance_distribution.get(imp_bucket, 0) + 1
    
    print("Importance distribution:")
    for imp, count in sorted(importance_distribution.items()):
        print(f"  {imp:.1f}: {count} entries")
```

---

## Error Handling Examples

### Example 1: Graceful Degradation

```python
async def robust_search(query):
    try:
        # Try semantic search first
        results = await memory_manager.semantic_search(query)
    except Exception as e:
        logger.warning(f"Semantic search failed: {e}")
        # Fallback to keyword search
        results = await memory_manager.query(query_text=query)
    
    return results
```

### Example 2: Retry Logic

```python
import asyncio

async def retry_operation(operation, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await operation()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

### Example 3: Circuit Breaker

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.last_failure_time = 0
        self.state = "closed"  # closed, open, half-open
    
    async def call(self, func):
        if self.state == "open":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "half-open"
            else:
                raise Exception("Circuit is open")
        
        try:
            result = await func()
            if self.state == "half-open":
                self.state = "closed"
            self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = "open"
            raise
```
"""
Redis Backend V2: Production-ready Redis backend with advanced features.

This module provides a comprehensive Redis backend implementation with:
- Connection pool management
- Automatic retry with exponential backoff
- Circuit breaker pattern
- Health checks and monitoring
- Batch operations with pipelines
- Transaction support
- Performance metrics
- Comprehensive logging
- Configuration management

GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module ns-root/namespaces-adk/adk/plugins/memory_plugins
@gl-semantic-anchor GL-00-PLUGINS_MEMORYPL_REDIS_V2
@gl-evidence-required false
GL Unified Charter Activated
"""

import asyncio
import json
import logging
import struct
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import aiohttp

from ...core.memory_manager import (
    MemoryBackend,
    MemoryEntry,
    MemoryQuery,
    MemoryType,
)

try:
    import redis.asyncio as redis
    from redis.asyncio import ConnectionPool
    from redis.commands.search.field import NumericField, TagField, TextField, VectorField
    from redis.commands.search.indexDefinition import IndexDefinition, IndexType
    from redis.commands.search.query import Query
    from redis.exceptions import ConnectionError, RedisError, TimeoutError
    from redis.exceptions import ResponseError as RedisResponseError
    
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False


logger = logging.getLogger(__name__)


# =============================================================================
# Enums and Data Models
# =============================================================================


class RedisBackendState(Enum):
    """Redis backend states."""
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    ERROR = "error"
    CIRCUIT_OPEN = "circuit_open"


class RetryStrategy(Enum):
    """Retry strategies."""
    EXPONENTIAL_BACKOFF = "exponential_backoff"
    LINEAR_BACKOFF = "linear_backoff"
    FIXED_DELAY = "fixed_delay"


@dataclass
class RedisConfig:
    """Redis configuration."""
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None
    username: Optional[str] = None
    prefix: str = "memory:"
    vector_dim: int = 1536
    default_ttl: int = 86400
    
    # Connection pool settings
    max_connections: int = 50
    min_connections: int = 5
    connection_timeout: int = 10
    socket_timeout: int = 10
    socket_connect_timeout: int = 5
    retry_on_timeout: bool = True
    
    # Retry settings
    max_retries: int = 3
    retry_strategy: RetryStrategy = RetryStrategy.EXPONENTIAL_BACKOFF
    retry_delay: float = 0.1
    retry_max_delay: float = 10.0
    
    # Circuit breaker settings
    circuit_breaker_enabled: bool = True
    circuit_breaker_failure_threshold: int = 5
    circuit_breaker_recovery_timeout: float = 60.0
    
    # Health check settings
    health_check_enabled: bool = True
    health_check_interval: float = 30.0
    
    # Performance settings
    enable_pipeline: bool = True
    pipeline_max_size: int = 100
    batch_size: int = 100
    
    # Monitoring settings
    enable_metrics: bool = True
    metrics_prefix: str = "redis_backend"


@dataclass
class RedisMetrics:
    """Redis performance metrics."""
    total_operations: int = 0
    successful_operations: int = 0
    failed_operations: int = 0
    total_retries: int = 0
    total_latency_ms: float = 0.0
    circuit_breaker_trips: int = 0
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.total_operations == 0:
            return 0.0
        return self.successful_operations / self.total_operations
    
    @property
    def avg_latency_ms(self) -> float:
        """Calculate average latency."""
        if self.total_operations == 0:
            return 0.0
        return self.total_latency_ms / self.total_operations
    
    def reset(self):
        """Reset all metrics."""
        self.total_operations = 0
        self.successful_operations = 0
        self.failed_operations = 0
        self.total_retries = 0
        self.total_latency_ms = 0.0
        self.circuit_breaker_trips = 0


@dataclass
class CircuitBreakerState:
    """Circuit breaker state."""
    failure_count: int = 0
    last_failure_time: Optional[float] = None
    open_time: Optional[float] = None
    state: RedisBackendState = RedisBackendState.CONNECTED


# =============================================================================
# Circuit Breaker
# =============================================================================


class CircuitBreaker:
    """Circuit breaker for Redis operations."""
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        metrics: Optional[RedisMetrics] = None
    ):
        """
        Initialize circuit breaker.
        
        Args:
            failure_threshold: Number of failures before opening
            recovery_timeout: Seconds to wait before attempting recovery
            metrics: Metrics instance to track trips
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.metrics = metrics
        self.state = CircuitBreakerState()
        self._lock = asyncio.Lock()
    
    async def execute(self, operation: Callable) -> Any:
        """
        Execute operation with circuit breaker protection.
        
        Args:
            operation: Async callable to execute
            
        Returns:
            Operation result
            
        Raises:
            Exception: If circuit is open
        """
        async with self._lock:
            # Check if circuit is open and recovery timeout has passed
            if self.state.state == RedisBackendState.CIRCUIT_OPEN:
                if self._should_attempt_recovery():
                    logger.info("Attempting circuit breaker recovery")
                    self.state.state = RedisBackendState.CONNECTING
                else:
                    raise Exception("Circuit breaker is open")
        
        try:
            result = await operation()
            
            # Reset failure count on success
            async with self._lock:
                self.state.failure_count = 0
                if self.state.state == RedisBackendState.CONNECTING:
                    self.state.state = RedisBackendState.CONNECTED
                    logger.info("Circuit breaker recovered")
            
            return result
            
        except Exception as e:
            async with self._lock:
                self.state.failure_count += 1
                self.state.last_failure_time = time.time()
                
                if self.state.failure_count >= self.failure_threshold:
                    self.state.state = RedisBackendState.CIRCUIT_OPEN
                    self.state.open_time = time.time()
                    
                    if self.metrics:
                        self.metrics.circuit_breaker_trips += 1
                    
                    logger.warning(
                        f"Circuit breaker opened after {self.state.failure_count} failures"
                    )
            
            raise
    
    def _should_attempt_recovery(self) -> bool:
        """Check if recovery should be attempted."""
        if self.state.open_time is None:
            return True
        
        elapsed = time.time() - self.state.open_time
        return elapsed >= self.recovery_timeout
    
    def get_state(self) -> Dict[str, Any]:
        """Get circuit breaker state."""
        return {
            "state": self.state.state.value,
            "failure_count": self.state.failure_count,
            "last_failure_time": self.state.last_failure_time,
            "open_time": self.state.open_time,
        }


# =============================================================================
# Retry Handler
# =============================================================================


class RetryHandler:
    """Retry handler with exponential backoff."""
    
    def __init__(
        self,
        max_retries: int = 3,
        strategy: RetryStrategy = RetryStrategy.EXPONENTIAL_BACKOFF,
        delay: float = 0.1,
        max_delay: float = 10.0,
        metrics: Optional[RedisMetrics] = None
    ):
        """
        Initialize retry handler.
        
        Args:
            max_retries: Maximum number of retries
            strategy: Retry strategy
            delay: Initial delay in seconds
            max_delay: Maximum delay in seconds
            metrics: Metrics instance
        """
        self.max_retries = max_retries
        self.strategy = strategy
        self.delay = delay
        self.max_delay = max_delay
        self.metrics = metrics
    
    async def execute(self, operation: Callable) -> Any:
        """
        Execute operation with retry logic.
        
        Args:
            operation: Async callable to execute
            
        Returns:
            Operation result
            
        Raises:
            Exception: If all retries fail
        """
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                return await operation()
                
            except (ConnectionError, TimeoutError, RedisError) as e:
                last_exception = e
                
                if self.metrics:
                    self.metrics.total_retries += 1
                
                if attempt == self.max_retries:
                    logger.error(
                        f"Operation failed after {self.max_retries} retries: {e}"
                    )
                    raise
                
                # Calculate delay
                retry_delay = self._calculate_delay(attempt)
                logger.warning(
                    f"Attempt {attempt + 1}/{self.max_retries + 1} failed: {e}. "
                    f"Retrying in {retry_delay:.2f}s"
                )
                await asyncio.sleep(retry_delay)
            
            except Exception as e:
                # Non-retryable exception
                logger.error(f"Non-retryable exception: {e}")
                raise
        
        raise last_exception
    
    def _calculate_delay(self, attempt: int) -> float:
        """Calculate retry delay based on strategy."""
        if self.strategy == RetryStrategy.EXPONENTIAL_BACKOFF:
            delay = self.delay * (2 ** attempt)
        elif self.strategy == RetryStrategy.LINEAR_BACKOFF:
            delay = self.delay * (attempt + 1)
        else:  # FIXED_DELAY
            delay = self.delay
        
        return min(delay, self.max_delay)


# =============================================================================
# Health Checker
# =============================================================================


class HealthChecker:
    """Health checker for Redis connection."""
    
    def __init__(
        self,
        client: redis.Redis,
        interval: float = 30.0,
        enabled: bool = True
    ):
        """
        Initialize health checker.
        
        Args:
            client: Redis client
            interval: Health check interval in seconds
            enabled: Enable health checking
        """
        self.client = client
        self.interval = interval
        self.enabled = enabled
        self._task: Optional[asyncio.Task] = None
        self._healthy = True
        self._last_check_time: Optional[float] = None
        self._lock = asyncio.Lock()
    
    async def start(self):
        """Start health checker."""
        if not self.enabled:
            return
        
        self._task = asyncio.create_task(self._health_check_loop())
        logger.info("Health checker started")
    
    async def stop(self):
        """Stop health checker."""
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            logger.info("Health checker stopped")
    
    async def _health_check_loop(self):
        """Health check loop."""
        while True:
            try:
                is_healthy = await self.check()
                
                async with self._lock:
                    old_healthy = self._healthy
                    self._healthy = is_healthy
                    self._last_check_time = time.time()
                    
                    if old_healthy and not is_healthy:
                        logger.error("Redis health check failed")
                    elif not old_healthy and is_healthy:
                        logger.info("Redis health check recovered")
                
            except Exception as e:
                logger.error(f"Health check error: {e}")
                async with self._lock:
                    self._healthy = False
                    self._last_check_time = time.time()
            
            await asyncio.sleep(self.interval)
    
    async def check(self) -> bool:
        """
        Check Redis health.
        
        Returns:
            True if healthy, False otherwise
        """
        try:
            await self.client.ping()
            return True
        except Exception as e:
            logger.warning(f"Health check failed: {e}")
            return False
    
    def is_healthy(self) -> bool:
        """Check if Redis is healthy."""
        return self._healthy
    
    def get_status(self) -> Dict[str, Any]:
        """Get health checker status."""
        return {
            "healthy": self._healthy,
            "enabled": self.enabled,
            "interval": self.interval,
            "last_check_time": self._last_check_time,
        }


# =============================================================================
# Redis Backend V2
# =============================================================================


class RedisBackendV2(MemoryBackend):
    """
    Production-ready Redis backend with advanced features.
    
    Features:
    - Connection pool management
    - Automatic retry with exponential backoff
    - Circuit breaker pattern
    - Health checks and monitoring
    - Batch operations with pipelines
    - Transaction support
    - Performance metrics
    - Comprehensive logging
    """
    
    def __init__(
        self,
        config: Optional[RedisConfig] = None,
        **kwargs
    ):
        """
        Initialize Redis backend V2.
        
        Args:
            config: Redis configuration
            **kwargs: Override config parameters
        """
        if not REDIS_AVAILABLE:
            raise ImportError(
                "Redis package not available. Install with: pip install redis[hiredis]"
            )
        
        # Merge config
        if config is None:
            config = RedisConfig()
        
        self.config = self._merge_config(config, kwargs)
        
        # State
        self._client: Optional[redis.Redis] = None
        self._pool: Optional[ConnectionPool] = None
        self._state = RedisBackendState.DISCONNECTED
        
        # Components
        self._metrics = RedisMetrics() if self.config.enable_metrics else None
        self._circuit_breaker = CircuitBreaker(
            failure_threshold=self.config.circuit_breaker_failure_threshold,
            recovery_timeout=self.config.circuit_breaker_recovery_timeout,
            metrics=self._metrics
        ) if self.config.circuit_breaker_enabled else None
        
        self._retry_handler = RetryHandler(
            max_retries=self.config.max_retries,
            strategy=self.config.retry_strategy,
            delay=self.config.retry_delay,
            max_delay=self.config.retry_max_delay,
            metrics=self._metrics
        )
        
        self._health_checker: Optional[HealthChecker] = None
        
        # Logger
        self._logger = logging.getLogger(__name__)
    
    def _merge_config(self, config: RedisConfig, kwargs: Dict[str, Any]) -> RedisConfig:
        """Merge config with kwargs."""
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)
        return config
    
    async def initialize(self) -> None:
        """Initialize Redis connection and components."""
        self._state = RedisBackendState.CONNECTING
        
        try:
            # Create connection pool
            self._pool = ConnectionPool(
                host=self.config.host,
                port=self.config.port,
                db=self.config.db,
                username=self.config.username,
                password=self.config.password,
                max_connections=self.config.max_connections,
                socket_timeout=self.config.socket_timeout,
                socket_connect_timeout=self.config.socket_connect_timeout,
                decode_responses=True,
            )
            
            # Create client
            self._client = redis.Redis(connection_pool=self._pool)
            
            # Test connection
            await self._client.ping()
            
            # Create index
            await self._create_index()
            
            # Initialize health checker
            if self.config.health_check_enabled:
                self._health_checker = HealthChecker(
                    client=self._client,
                    interval=self.config.health_check_interval,
                    enabled=True
                )
                await self._health_checker.start()
            
            self._state = RedisBackendState.CONNECTED
            self._logger.info(
                f"Connected to Redis at {self.config.host}:{self.config.port}"
            )
            
        except Exception as e:
            self._state = RedisBackendState.ERROR
            self._logger.error(f"Failed to initialize Redis: {e}")
            raise
    
    async def _create_index(self) -> None:
        """Create RediSearch index for memory entries."""
        index_name = f"{self.config.prefix}idx"
        
        try:
            await self._client.ft(index_name).info()
            self._logger.debug(f"Index {index_name} already exists")
        except RedisResponseError:
            schema = (
                TextField("$.content", as_name="content"),
                TextField("$.session_id", as_name="session_id"),
                TextField("$.user_id", as_name="user_id"),
                TagField("$.memory_type", as_name="memory_type"),
                NumericField("$.importance", as_name="importance"),
                NumericField("$.created_at", as_name="created_at"),
                NumericField("$.updated_at", as_name="updated_at"),
                NumericField("$.access_count", as_name="access_count"),
                VectorField(
                    "$.embedding",
                    "FLAT",
                    {
                        "TYPE": "FLOAT32",
                        "DIM": self.config.vector_dim,
                        "DISTANCE_METRIC": "COSINE",
                    },
                    as_name="embedding",
                ),
            )
            definition = IndexDefinition(
                prefix=[self.config.prefix],
                index_type=IndexType.JSON,
            )
            await self._client.ft(index_name).create_index(schema, definition=definition)
            self._logger.info(f"Created index {index_name}")
    
    async def add(self, entry: MemoryEntry) -> str:
        """
        Add a memory entry to Redis.
        
        Args:
            entry: Memory entry to add
            
        Returns:
            Entry ID
        """
        return await self._execute_with_protection(
            self._add_entry,
            entry
        )
    
    async def _add_entry(self, entry: MemoryEntry) -> str:
        """Internal add entry implementation."""
        key = f"{self.config.prefix}{entry.id}"
        data = self._serialize_entry(entry)
        
        await self._client.json().set(key, "$", data)
        
        # Set TTL
        ttl = self._get_ttl(entry.memory_type, entry.importance)
        if ttl:
            await self._client.expire(key, ttl)
        
        self._logger.debug(f"Added entry {entry.id}")
        return entry.id
    
    def _serialize_entry(self, entry: MemoryEntry) -> Dict[str, Any]:
        """Serialize MemoryEntry to dict."""
        return {
            "id": entry.id,
            "content": entry.content,
            "metadata": entry.metadata,
            "embedding": entry.embedding,
            "memory_type": entry.memory_type.value,
            "session_id": entry.session_id,
            "user_id": entry.user_id,
            "created_at": entry.created_at.timestamp(),
            "updated_at": entry.updated_at.timestamp(),
            "importance": entry.importance,
            "access_count": entry.access_count,
        }
    
    def _get_ttl(self, memory_type: MemoryType, importance: float) -> Optional[int]:
        """Calculate TTL based on memory type and importance."""
        if memory_type == MemoryType.SHORT_TERM:
            return int(3600 * (1 + 3 * importance))
        elif memory_type == MemoryType.LONG_TERM:
            return int(86400 * (1 + 29 * importance))
        return self.config.default_ttl
    
    async def get(self, entry_id: str) -> Optional[MemoryEntry]:
        """
        Get a memory entry by ID.
        
        Args:
            entry_id: Entry ID
            
        Returns:
            MemoryEntry or None
        """
        return await self._execute_with_protection(
            self._get_entry,
            entry_id
        )
    
    async def _get_entry(self, entry_id: str) -> Optional[MemoryEntry]:
        """Internal get entry implementation."""
        key = f"{self.config.prefix}{entry_id}"
        data = await self._client.json().get(key)
        
        if not data:
            return None
        
        # Increment access count
        await self._client.json().numincrby(key, "$.access_count", 1)
        
        return self._deserialize_entry(data)
    
    def _deserialize_entry(self, data: Dict[str, Any]) -> MemoryEntry:
        """Deserialize dict to MemoryEntry."""
        return MemoryEntry(
            id=data["id"],
            content=data["content"],
            metadata=data.get("metadata", {}),
            embedding=data.get("embedding"),
            memory_type=MemoryType(data["memory_type"]),
            session_id=data.get("session_id"),
            user_id=data.get("user_id"),
            created_at=datetime.fromtimestamp(data["created_at"]),
            updated_at=datetime.fromtimestamp(data["updated_at"]),
            importance=data.get("importance", 1.0),
            access_count=data.get("access_count", 0),
        )
    
    async def update(self, entry_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update a memory entry.
        
        Args:
            entry_id: Entry ID
            updates: Fields to update
            
        Returns:
            True if updated, False if not found
        """
        return await self._execute_with_protection(
            self._update_entry,
            entry_id,
            updates
        )
    
    async def _update_entry(self, entry_id: str, updates: Dict[str, Any]) -> bool:
        """Internal update entry implementation."""
        key = f"{self.config.prefix}{entry_id}"
        
        if not await self._client.exists(key):
            return False
        
        updates["updated_at"] = datetime.now().timestamp()
        
        for field_name, value in updates.items():
            await self._client.json().set(key, f"$.{field_name}", value)
        
        self._logger.debug(f"Updated entry {entry_id}")
        return True
    
    async def delete(self, entry_id: str) -> bool:
        """
        Delete a memory entry.
        
        Args:
            entry_id: Entry ID
            
        Returns:
            True if deleted, False if not found
        """
        return await self._execute_with_protection(
            self._delete_entry,
            entry_id
        )
    
    async def _delete_entry(self, entry_id: str) -> bool:
        """Internal delete entry implementation."""
        key = f"{self.config.prefix}{entry_id}"
        result = await self._client.delete(key)
        
        if result > 0:
            self._logger.debug(f"Deleted entry {entry_id}")
        
        return result > 0
    
    async def query(self, memory_query: MemoryQuery) -> List[MemoryEntry]:
        """
        Query memory entries with optional vector search.
        
        Args:
            memory_query: Memory query
            
        Returns:
            List of memory entries
        """
        return await self._execute_with_protection(
            self._query_entries,
            memory_query
        )
    
    async def _query_entries(self, memory_query: MemoryQuery) -> List[MemoryEntry]:
        """Internal query implementation."""
        index_name = f"{self.config.prefix}idx"
        query_parts = []
        
        # Build filter query
        if memory_query.session_id:
            query_parts.append(f"@session_id:{{{memory_query.session_id}}}")
        if memory_query.user_id:
            query_parts.append(f"@user_id:{{{memory_query.user_id}}}")
        if memory_query.memory_type:
            query_parts.append(f"@memory_type:{{{memory_query.memory_type.value}}}")
        
        query_str = " ".join(query_parts) if query_parts else "*"
        
        # Vector search
        if hasattr(memory_query, "embedding") and memory_query.embedding:
            query = (
                Query(f"({query_str})=>[KNN {memory_query.limit} @embedding $vec AS score]")
                .sort_by("score")
                .return_fields(
                    "id", "content", "session_id", "user_id",
                    "memory_type", "importance", "created_at", "score"
                )
                .dialect(2)
            )
            params = {
                "vec": struct.pack(f"{len(memory_query.embedding)}f", *memory_query.embedding)
            }
        else:
            query = (
                Query(query_str)
                .sort_by("created_at", asc=False)
                .paging(0, memory_query.limit)
            )
            params = {}
        
        # Execute search
        try:
            results = await self._client.ft(index_name).search(query, params)
        except RedisResponseError as e:
            self._logger.error(f"Query error: {e}")
            return []
        
        # Fetch full entries
        entries = []
        for doc in results.docs:
            entry_id = doc.id.replace(self.config.prefix, "")
            data = await self._client.json().get(f"{self.config.prefix}{entry_id}")
            if data:
                entries.append(self._deserialize_entry(data))
        
        return entries
    
    async def add_batch(self, entries: List[MemoryEntry]) -> List[str]:
        """
        Add multiple entries in batch using pipeline.
        
        Args:
            entries: List of memory entries
            
        Returns:
            List of entry IDs
        """
        return await self._execute_with_protection(
            self._add_entries_batch,
            entries
        )
    
    async def _add_entries_batch(self, entries: List[MemoryEntry]) -> List[str]:
        """Internal batch add implementation."""
        if not self.config.enable_pipeline:
            # Fallback to individual adds
            ids = []
            for entry in entries:
                ids.append(await self._add_entry(entry))
            return ids
        
        # Process in batches
        all_ids = []
        batch_size = self.config.batch_size
        
        for i in range(0, len(entries), batch_size):
            batch = entries[i:i + batch_size]
            batch_ids = []
            
            async with self._client.pipeline(transaction=True) as pipe:
                for entry in batch:
                    key = f"{self.config.prefix}{entry.id}"
                    data = self._serialize_entry(entry)
                    pipe.json().set(key, "$", data)
                    
                    ttl = self._get_ttl(entry.memory_type, entry.importance)
                    if ttl:
                        pipe.expire(key, ttl)
                    
                    batch_ids.append(entry.id)
                
                await pipe.execute()
            
            all_ids.extend(batch_ids)
        
        self._logger.debug(f"Added {len(all_ids)} entries in batch")
        return all_ids
    
    async def summarize(self, session_id: str, max_tokens: int = 1000) -> str:
        """
        Summarize memory for a session.
        
        Args:
            session_id: Session ID
            max_tokens: Maximum tokens in summary
            
        Returns:
            Summary string
        """
        entries = await self.query(
            MemoryQuery(query_text="", session_id=session_id, limit=100)
        )
        
        if not entries:
            return ""
        
        # Sort by importance and creation time
        entries.sort(key=lambda e: (e.importance, e.created_at), reverse=True)
        
        # Build summary
        summary_parts = []
        total_tokens = 0
        
        for entry in entries:
            entry_tokens = len(entry.content.split())
            if total_tokens + entry_tokens > max_tokens:
                break
            summary_parts.append(entry.content)
            total_tokens += entry_tokens
        
        return " ".join(summary_parts)
    
    async def _execute_with_protection(self, operation: Callable, *args, **kwargs) -> Any:
        """
        Execute operation with retry and circuit breaker protection.
        
        Args:
            operation: Operation to execute
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Operation result
        """
        start_time = time.time()
        
        if self._metrics:
            self._metrics.total_operations += 1
        
        try:
            # Execute with retry handler
            if self._circuit_breaker:
                result = await self._circuit_breaker.execute(
                    lambda: self._retry_handler.execute(
                        lambda: operation(*args, **kwargs)
                    )
                )
            else:
                result = await self._retry_handler.execute(
                    lambda: operation(*args, **kwargs)
                )
            
            # Record success
            if self._metrics:
                self._metrics.successful_operations += 1
                latency_ms = (time.time() - start_time) * 1000
                self._metrics.total_latency_ms += latency_ms
            
            return result
            
        except Exception as e:
            # Record failure
            if self._metrics:
                self._metrics.failed_operations += 1
            
            self._logger.error(f"Operation failed: {e}")
            raise
    
    def get_metrics(self) -> Optional[Dict[str, Any]]:
        """
        Get performance metrics.
        
        Returns:
            Metrics dictionary or None if metrics disabled
        """
        if not self._metrics:
            return None
        
        return {
            "total_operations": self._metrics.total_operations,
            "successful_operations": self._metrics.successful_operations,
            "failed_operations": self._metrics.failed_operations,
            "success_rate": self._metrics.success_rate,
            "total_retries": self._metrics.total_retries,
            "avg_latency_ms": self._metrics.avg_latency_ms,
            "circuit_breaker_trips": self._metrics.circuit_breaker_trips,
        }
    
    def get_health_status(self) -> Dict[str, Any]:
        """
        Get health status.
        
        Returns:
            Health status dictionary
        """
        status = {
            "state": self._state.value,
            "connected": self._state == RedisBackendState.CONNECTED,
        }
        
        if self._health_checker:
            status["health_check"] = self._health_checker.get_status()
        
        if self._circuit_breaker:
            status["circuit_breaker"] = self._circuit_breaker.get_state()
        
        if self._metrics:
            status["metrics"] = self.get_metrics()
        
        return status
    
    async def close(self) -> None:
        """Close Redis connection and cleanup."""
        self._state = RedisBackendState.DISCONNECTED
        
        # Stop health checker
        if self._health_checker:
            await self._health_checker.stop()
        
        # Close pool
        if self._pool:
            await self._pool.disconnect()
        
        if self._client:
            await self._client.close()
        
        self._logger.info("Redis connection closed")


# =============================================================================
# Factory Functions
# =============================================================================


def create_redis_backend_v2(
    host: str = "localhost",
    port: int = 6379,
    db: int = 0,
    password: Optional[str] = None,
    **kwargs
) -> RedisBackendV2:
    """
    Factory function to create Redis backend V2.
    
    Args:
        host: Redis host
        port: Redis port
        db: Redis database number
        password: Redis password
        **kwargs: Additional configuration
        
    Returns:
        RedisBackendV2 instance
    """
    config = RedisConfig(
        host=host,
        port=port,
        db=db,
        password=password,
        **kwargs
    )
    
    return RedisBackendV2(config=config)


# =============================================================================
# Example Usage
# =============================================================================


async def example_usage():
    """Example usage of Redis backend V2."""
    
    # Create backend
    backend = RedisBackendV2(
        host="localhost",
        port=6379,
        config=RedisConfig(
            max_connections=50,
            circuit_breaker_enabled=True,
            health_check_enabled=True,
        )
    )
    
    # Initialize
    await backend.initialize()
    
    # Add entry
    entry = MemoryEntry(
        id="test1",
        content="Test memory",
        memory_type=MemoryType.LONG_TERM,
        importance=0.9
    )
    await backend.add(entry)
    
    # Get entry
    retrieved = await backend.get("test1")
    print(f"Retrieved: {retrieved}")
    
    # Get metrics
    metrics = backend.get_metrics()
    print(f"Metrics: {metrics}")
    
    # Get health status
    health = backend.get_health_status()
    print(f"Health: {health}")
    
    # Close
    await backend.close()


if __name__ == "__main__":
    asyncio.run(example_usage())
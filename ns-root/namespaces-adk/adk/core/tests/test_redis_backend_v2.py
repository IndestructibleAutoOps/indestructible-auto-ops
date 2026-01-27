"""
Tests for Redis Backend V2.

GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module ns-root/namespaces-adk/adk/core/tests
@gl-semantic-anchor GL-00-TESTS_REDIS_V2
@gl-evidence-required false
GL Unified Charter Activated
"""

import asyncio
import pytest

from ...plugins.memory_plugins.redis_backend_v2 import (
    RedisBackendV2,
    RedisConfig,
    CircuitBreaker,
    RetryHandler,
    HealthChecker,
    RedisMetrics,
    RetryStrategy,
)
from ...core.memory_manager import MemoryEntry, MemoryType


@pytest.fixture
async def redis_backend():
    """Create Redis backend instance."""
    backend = RedisBackendV2(
        config=RedisConfig(
            host="localhost",
            port=6379,
            db=0,
            circuit_breaker_enabled=True,
            health_check_enabled=False,  # Disable for tests
        )
    )
    await backend.initialize()
    yield backend
    await backend.close()


@pytest.fixture
def sample_entry():
    """Create sample memory entry."""
    return MemoryEntry(
        id="test_entry_1",
        content="This is a test memory entry",
        memory_type=MemoryType.LONG_TERM,
        importance=0.8,
        session_id="test_session",
        user_id="test_user",
    )


class TestRedisBackendV2:
    """Test Redis Backend V2 functionality."""
    
    @pytest.mark.asyncio
    async def test_initialize(self, redis_backend):
        """Test backend initialization."""
        assert redis_backend._state.value == "connected"
        assert redis_backend._client is not None
    
    @pytest.mark.asyncio
    async def test_add_entry(self, redis_backend, sample_entry):
        """Test adding a memory entry."""
        entry_id = await redis_backend.add(sample_entry)
        assert entry_id == sample_entry.id
    
    @pytest.mark.asyncio
    async def test_get_entry(self, redis_backend, sample_entry):
        """Test retrieving a memory entry."""
        await redis_backend.add(sample_entry)
        retrieved = await redis_backend.get(sample_entry.id)
        
        assert retrieved is not None
        assert retrieved.id == sample_entry.id
        assert retrieved.content == sample_entry.content
        assert retrieved.access_count == 1
    
    @pytest.mark.asyncio
    async def test_update_entry(self, redis_backend, sample_entry):
        """Test updating a memory entry."""
        await redis_backend.add(sample_entry)
        
        updated = await redis_backend.update(
            sample_entry.id,
            {"content": "Updated content", "importance": 0.9}
        )
        
        assert updated is True
        
        retrieved = await redis_backend.get(sample_entry.id)
        assert retrieved.content == "Updated content"
        assert retrieved.importance == 0.9
    
    @pytest.mark.asyncio
    async def test_delete_entry(self, redis_backend, sample_entry):
        """Test deleting a memory entry."""
        await redis_backend.add(sample_entry)
        
        deleted = await redis_backend.delete(sample_entry.id)
        assert deleted is True
        
        retrieved = await redis_backend.get(sample_entry.id)
        assert retrieved is None
    
    @pytest.mark.asyncio
    async def test_add_batch(self, redis_backend):
        """Test batch adding entries."""
        entries = [
            MemoryEntry(
                id=f"batch_{i}",
                content=f"Batch entry {i}",
                memory_type=MemoryType.LONG_TERM,
            )
            for i in range(10)
        ]
        
        ids = await redis_backend.add_batch(entries)
        assert len(ids) == 10
        
        # Verify all entries were added
        for entry_id in ids:
            retrieved = await redis_backend.get(entry_id)
            assert retrieved is not None
    
    @pytest.mark.asyncio
    async def test_query_by_session_id(self, redis_backend):
        """Test querying by session ID."""
        entries = [
            MemoryEntry(
                id=f"query_{i}",
                content=f"Query entry {i}",
                memory_type=MemoryType.LONG_TERM,
                session_id="session_1",
            )
            for i in range(5)
        ]
        
        for entry in entries:
            await redis_backend.add(entry)
        
        from ...core.memory_manager import MemoryQuery
        results = await redis_backend.query(
            MemoryQuery(session_id="session_1", limit=10)
        )
        
        assert len(results) == 5
    
    @pytest.mark.asyncio
    async def test_get_metrics(self, redis_backend, sample_entry):
        """Test getting performance metrics."""
        await redis_backend.add(sample_entry)
        await redis_backend.get(sample_entry.id)
        
        metrics = redis_backend.get_metrics()
        
        assert metrics is not None
        assert metrics["total_operations"] > 0
        assert metrics["successful_operations"] > 0
    
    @pytest.mark.asyncio
    async def test_get_health_status(self, redis_backend):
        """Test getting health status."""
        status = redis_backend.get_health_status()
        
        assert status["state"] == "connected"
        assert status["connected"] is True
        assert "circuit_breaker" in status
    
    @pytest.mark.asyncio
    async def test_summarize(self, redis_backend):
        """Test memory summarization."""
        entries = [
            MemoryEntry(
                id=f"summary_{i}",
                content=f"Summary content {i} " * 10,
                memory_type=MemoryType.LONG_TERM,
                session_id="summary_session",
                importance=0.9,
            )
            for i in range(5)
        ]
        
        for entry in entries:
            await redis_backend.add(entry)
        
        summary = await redis_backend.summarize("summary_session", max_tokens=50)
        
        assert len(summary) > 0
        assert len(summary.split()) <= 50


class TestCircuitBreaker:
    """Test circuit breaker functionality."""
    
    @pytest.mark.asyncio
    async def test_circuit_breaker_opens_on_failures(self):
        """Test circuit breaker opens after threshold failures."""
        metrics = RedisMetrics()
        breaker = CircuitBreaker(
            failure_threshold=3,
            recovery_timeout=1.0,
            metrics=metrics
        )
        
        failing_operation = lambda: (_ for _ in ()).throw(Exception("Test error"))
        
        # Trigger failures
        for _ in range(3):
            try:
                await breaker.execute(failing_operation)
            except Exception:
                pass
        
        # Circuit should be open
        state = breaker.get_state()
        assert state["state"] == "circuit_open"
        assert metrics.circuit_breaker_trips == 1
    
    @pytest.mark.asyncio
    async def test_circuit_breaker_recovers(self):
        """Test circuit breaker recovery."""
        breaker = CircuitBreaker(
            failure_threshold=2,
            recovery_timeout=0.5,  # Short recovery time
        )
        
        failing_operation = lambda: (_ for _ in ()).throw(Exception("Test error"))
        successful_operation = lambda: "success"
        
        # Trigger failures
        for _ in range(2):
            try:
                await breaker.execute(failing_operation)
            except Exception:
                pass
        
        # Wait for recovery
        await asyncio.sleep(0.6)
        
        # Should recover
        result = await breaker.execute(successful_operation)
        assert result == "success"


class TestRetryHandler:
    """Test retry handler functionality."""
    
    @pytest.mark.asyncio
    async def test_retry_on_failure(self):
        """Test retry on connection errors."""
        metrics = RedisMetrics()
        handler = RetryHandler(
            max_retries=3,
            delay=0.01,
            metrics=metrics
        )
        
        attempt_count = [0]
        
        async def failing_operation():
            attempt_count[0] += 1
            if attempt_count[0] < 3:
                raise ConnectionError("Connection failed")
            return "success"
        
        result = await handler.execute(failing_operation)
        
        assert result == "success"
        assert attempt_count[0] == 3
        assert metrics.total_retries == 2
    
    @pytest.mark.asyncio
    async def test_exponential_backoff(self):
        """Test exponential backoff strategy."""
        handler = RetryHandler(
            max_retries=3,
            strategy=RetryStrategy.EXPONENTIAL_BACKOFF,
            delay=0.01,
        )
        
        delays = []
        
        async def failing_operation():
            raise ConnectionError("Failed")
        
        start_time = asyncio.get_event_loop().time()
        
        for _ in range(handler.max_retries + 1):
            try:
                await handler.execute(failing_operation)
            except Exception:
                delays.append(asyncio.get_event_loop().time() - start_time)
        
        # Check that delays increase exponentially
        assert len(delays) > 1
        assert delays[-1] > delays[0]


class TestHealthChecker:
    """Test health checker functionality."""
    
    @pytest.mark.asyncio
    async def test_health_check(self):
        """Test health check."""
        import redis.asyncio as redis
        
        client = redis.Redis(host="localhost", port=6379, decode_responses=True)
        checker = HealthChecker(client, interval=0.1, enabled=True)
        
        await checker.start()
        
        # Wait for a health check
        await asyncio.sleep(0.2)
        
        assert checker.is_healthy()
        
        await checker.stop()
    
    @pytest.mark.asyncio
    async def test_health_status(self):
        """Test health status reporting."""
        import redis.asyncio as redis
        
        client = redis.Redis(host="localhost", port=6379, decode_responses=True)
        checker = HealthChecker(client, interval=0.1, enabled=True)
        
        await checker.start()
        await asyncio.sleep(0.2)
        
        status = checker.get_status()
        
        assert status["healthy"] is True
        assert status["enabled"] is True
        assert status["last_check_time"] is not None
        
        await checker.stop()


class TestRedisMetrics:
    """Test Redis metrics functionality."""
    
    def test_metrics_initialization(self):
        """Test metrics initialization."""
        metrics = RedisMetrics()
        
        assert metrics.total_operations == 0
        assert metrics.successful_operations == 0
        assert metrics.failed_operations == 0
        assert metrics.success_rate == 0.0
    
    def test_success_rate_calculation(self):
        """Test success rate calculation."""
        metrics = RedisMetrics()
        metrics.total_operations = 10
        metrics.successful_operations = 8
        
        assert metrics.success_rate == 0.8
    
    def test_avg_latency_calculation(self):
        """Test average latency calculation."""
        metrics = RedisMetrics()
        metrics.total_operations = 5
        metrics.total_latency_ms = 250.0
        
        assert metrics.avg_latency_ms == 50.0
    
    def test_metrics_reset(self):
        """Test metrics reset."""
        metrics = RedisMetrics()
        metrics.total_operations = 10
        metrics.successful_operations = 8
        metrics.failed_operations = 2
        
        metrics.reset()
        
        assert metrics.total_operations == 0
        assert metrics.successful_operations == 0
        assert metrics.failed_operations == 0


class TestRedisConfig:
    """Test Redis configuration."""
    
    def test_config_defaults(self):
        """Test default configuration."""
        config = RedisConfig()
        
        assert config.host == "localhost"
        assert config.port == 6379
        assert config.db == 0
        assert config.max_connections == 50
        assert config.circuit_breaker_enabled is True
    
    def test_config_override(self):
        """Test configuration override."""
        config = RedisConfig(
            host="redis.example.com",
            port=6380,
            max_connections=100,
        )
        
        assert config.host == "redis.example.com"
        assert config.port == 6380
        assert config.max_connections == 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
"""Unit tests for RedisBackendV2."""
import unittest
from unittest.mock import Mock, MagicMock, patch
import time

from adk.plugins.memory_plugins.redis_backend_v2 import (
    RedisBackendV2,
    RedisConfig,
    CircuitBreaker,
    RetryHandler
)


class TestCircuitBreaker(unittest.TestCase):
    """Test cases for CircuitBreaker."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=3,
            timeout=60
        )
    
    def test_init(self):
        """Test initialization."""
        self.assertEqual(self.circuit_breaker.failure_threshold, 3)
        self.assertEqual(self.circuit_breaker.timeout, 60)
    
    def test_record_success(self):
        """Test recording success."""
        self.circuit_breaker.record_success()
        
        self.assertEqual(self.circuit_breaker.failure_count, 0)
        self.assertEqual(self.circuit_breaker.state, "connected")
    
    def test_record_failure(self):
        """Test recording failure."""
        for _ in range(3):
            self.circuit_breaker.record_failure()
        
        self.assertEqual(self.circuit_breaker.state, "circuit_open")
    
    def test_allow_request(self):
        """Test checking if request is allowed."""
        # Initially allowed
        self.assertTrue(self.circuit_breaker.allow_request())
        
        # After failures
        for _ in range(3):
            self.circuit_breaker.record_failure()
        
        self.assertFalse(self.circuit_breaker.allow_request())


class TestRetryHandler(unittest.TestCase):
    """Test cases for RetryHandler."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.handler = RetryHandler(
            max_retries=3,
            base_delay=1.0
        )
    
    def test_init(self):
        """Test initialization."""
        self.assertEqual(self.handler.max_retries, 3)
    
    def test_retry_success(self):
        """Test successful retry."""
        call_count = 0
        
        def test_func():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise Exception("Fail")
            return "Success"
        
        result = self.handler.retry(test_func)
        
        self.assertEqual(result, "Success")
        self.assertEqual(call_count, 2)
    
    def test_retry_exhausted(self):
        """Test retry exhaustion."""
        def test_func():
            raise Exception("Always fail")
        
        with self.assertRaises(Exception):
            self.handler.retry(test_func)


class TestRedisBackendV2(unittest.TestCase):
    """Test cases for RedisBackendV2."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_redis = Mock()
        self.config = RedisConfig(host="localhost", port=6379)
        self.backend = RedisBackendV2(
            redis_client=self.mock_redis,
            config=self.config
        )
    
    def test_init(self):
        """Test initialization."""
        self.assertIsNotNone(self.backend)
        self.assertIsNotNone(self.backend.circuit_breaker)
        self.assertIsNotNone(self.backend.retry_handler)
    
    def test_add_with_circuit_breaker(self):
        """Test adding with circuit breaker."""
        self.mock_redis.hset.return_value = 1
        
        result = self.backend.add(
            memory_id="mem1",
            content="test content"
        )
        
        self.assertTrue(result)
    
    def test_get_with_retry(self):
        """Test getting with retry."""
        self.mock_redis.hgetall.return_value = {
            b"content": b"test content",
            b"metadata": b"{}"
        }
        
        result = self.backend.get("mem1")
        
        self.assertIsNotNone(result)
    
    def test_batch_operations(self):
        """Test batch operations."""
        operations = [
            ("add", {"memory_id": "mem1", "content": "content1"}),
            ("add", {"memory_id": "mem2", "content": "content2"})
        ]
        
        results = self.backend.batch_operations(operations)
        
        self.assertEqual(len(results), 2)
    
    def test_get_metrics(self):
        """Test getting backend metrics."""
        metrics = self.backend.get_metrics()
        
        self.assertIn("total_operations", metrics)
        self.assertIn("successful_operations", metrics)
    
    def test_health_check(self):
        """Test health check."""
        self.mock_redis.ping.return_value = True
        
        health = self.backend.health_check()
        
        self.assertEqual(health["status"], "healthy")


if __name__ == "__main__":
    unittest.main()
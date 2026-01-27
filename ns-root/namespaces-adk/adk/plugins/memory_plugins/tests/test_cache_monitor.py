"""Unit tests for CacheMonitor."""
import unittest
from unittest.mock import Mock, MagicMock
import time

from adk.plugins.memory_plugins.cache_monitor import (
    CacheMonitor,
    MetricType,
    Metric,
    Alert
)


class TestMetric(unittest.TestCase):
    """Test cases for Metric."""
    
    def test_counter_metric(self):
        """Test counter metric."""
        metric = Metric(name="test_counter", type=MetricType.COUNTER)
        metric.record(1.0)
        metric.record(2.0)
        
        self.assertEqual(metric.value, 3.0)
    
    def test_gauge_metric(self):
        """Test gauge metric."""
        metric = Metric(name="test_gauge", type=MetricType.GAUGE)
        metric.record(10.0)
        metric.record(20.0)
        
        self.assertEqual(metric.value, 20.0)
    
    def test_histogram_metric(self):
        """Test histogram metric."""
        metric = Metric(name="test_histogram", type=MetricType.HISTOGRAM)
        metric.record(10.0)
        metric.record(20.0)
        metric.record(30.0)
        
        self.assertEqual(metric.count, 3)
        self.assertEqual(metric.sum_value, 60.0)
        self.assertEqual(metric.min_value, 10.0)
        self.assertEqual(metric.max_value, 30.0)
        self.assertEqual(metric.get_stats()["avg"], 20.0)


class TestCacheMonitor(unittest.TestCase):
    """Test cases for CacheMonitor."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_cache_layer = Mock()
        self.mock_cache_layer.layer_stats = {
            "l1": {"hits": 100, "misses": 50},
            "l2": {"hits": 30, "misses": 20},
            "l3": {"hits": 10, "misses": 5}
        }
        self.mock_cache_layer.l1_cache = {}
        self.monitor = CacheMonitor(self.mock_cache_layer)
    
    def test_init(self):
        """Test initialization."""
        self.assertIsNotNone(self.monitor)
        self.assertGreater(len(self.monitor.metrics), 0)
    
    def test_record_hit(self):
        """Test recording cache hit."""
        self.monitor.record_hit()
        self.monitor.record_hit()
        
        self.assertEqual(self.monitor.metrics["cache_hits"].value, 2.0)
    
    def test_record_miss(self):
        """Test recording cache miss."""
        self.monitor.record_miss()
        self.monitor.record_miss()
        
        self.assertEqual(self.monitor.metrics["cache_misses"].value, 2.0)
    
    def test_record_write(self):
        """Test recording cache write."""
        self.monitor.record_write()
        
        self.assertEqual(self.monitor.metrics["cache_writes"].value, 1.0)
    
    def test_record_eviction(self):
        """Test recording cache eviction."""
        self.monitor.record_eviction()
        
        self.assertEqual(self.monitor.metrics["cache_evictions"].value, 1.0)
    
    def test_record_latency(self):
        """Test recording latency."""
        self.monitor.record_latency(10.5)
        self.monitor.record_latency(20.3)
        
        self.assertEqual(self.monitor.metrics["latency_ms"].count, 2)
    
    def test_update_hit_rate(self):
        """Test hit rate update."""
        self.monitor.record_hit()
        self.monitor.record_hit()
        self.monitor.record_hit()
        self.monitor.record_miss()
        
        self.assertEqual(self.monitor.metrics["hit_rate"].value, 0.75)
        self.assertEqual(self.monitor.metrics["miss_rate"].value, 0.25)
    
    def test_update_layer_metrics(self):
        """Test layer metrics update."""
        self.monitor.update_layer_metrics()
        
        self.assertEqual(self.monitor.metrics["l1_hit_rate"].value, 0.6666666666666666)
        self.assertEqual(self.monitor.metrics["l2_hit_rate"].value, 0.6)
        self.assertEqual(self.monitor.metrics["l3_hit_rate"].value, 0.6666666666666666)
    
    def test_check_alerts(self):
        """Test alert checking."""
        # Set low hit rate
        self.monitor.metrics["hit_rate"].value = 0.5
        
        alerts = self.monitor.check_alerts()
        
        self.assertGreater(len(alerts), 0)
    
    def test_resolve_alert(self):
        """Test alert resolution."""
        alert = Alert(
            id="test_alert",
            metric_name="hit_rate",
            condition="hit_rate < threshold",
            threshold=0.7,
            current_value=0.5,
            severity="warning",
            message="Test alert"
        )
        self.monitor.active_alerts["test_alert"] = alert
        
        result = self.monitor.resolve_alert("test_alert")
        
        self.assertTrue(result)
        self.assertNotIn("test_alert", self.monitor.active_alerts)
    
    def test_get_stats(self):
        """Test getting statistics."""
        self.monitor.record_hit()
        self.monitor.record_miss()
        
        stats = self.monitor.get_stats()
        
        self.assertIn("metrics", stats)
        self.assertIn("alerts", stats)
    
    def test_check_health(self):
        """Test health check."""
        self.mock_cache_layer.health_check.return_value = {"status": "healthy"}
        
        health = self.monitor.check_health()
        
        self.assertEqual(health["status"], "healthy")
    
    def test_start_stop_monitoring(self):
        """Test starting and stopping monitoring."""
        self.monitor.start_monitoring(interval=1)
        
        self.assertTrue(self.monitor.monitoring_active)
        
        time.sleep(0.5)
        
        self.monitor.stop_monitoring()
        
        self.assertFalse(self.monitor.monitoring_active)
    
    def test_get_historical_data(self):
        """Test getting historical data."""
        self.monitor.record_hit()
        self.monitor._store_historical_data()
        
        historical = self.monitor.get_historical_data("cache_hits", limit=10)
        
        self.assertGreater(len(historical), 0)
    
    def test_reset_metrics(self):
        """Test resetting metrics."""
        self.monitor.record_hit()
        self.monitor.record_miss()
        
        self.monitor.reset_metrics()
        
        self.assertEqual(self.monitor.metrics["cache_hits"].value, 0.0)
        self.assertEqual(self.monitor.metrics["cache_misses"].value, 0.0)
    
    def test_get_exported_metrics(self):
        """Test getting exported metrics."""
        self.monitor.record_hit()
        self.monitor.record_latency(10.0)
        
        exported = self.monitor.get_exported_metrics()
        
        self.assertIn("cache_hits", exported)
        self.assertIn("latency_ms_count", exported)
        self.assertIn("latency_ms_avg", exported)


if __name__ == "__main__":
    unittest.main()
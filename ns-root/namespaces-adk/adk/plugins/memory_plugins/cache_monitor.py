"""CacheMonitor implementation for production environment."""
import time
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import threading


class MetricType(Enum):
    """Types of cache metrics."""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


@dataclass
class Metric:
    """Represents a cache metric."""
    name: str
    type: MetricType
    value: float = 0.0
    count: int = 0
    sum_value: float = 0.0
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    timestamps: List[float] = field(default_factory=list)
    
    def record(self, value: float) -> None:
        """Record a metric value."""
        if self.type == MetricType.COUNTER:
            self.value += value
        elif self.type == MetricType.GAUGE:
            self.value = value
        elif self.type in [MetricType.HISTOGRAM, MetricType.SUMMARY]:
            self.count += 1
            self.sum_value += value
            if self.min_value is None or value < self.min_value:
                self.min_value = value
            if self.max_value is None or value > self.max_value:
                self.max_value = value
            self.timestamps.append(time.time())
    
    def get_stats(self) -> Dict[str, Any]:
        """Get metric statistics."""
        stats = {
            "name": self.name,
            "type": self.type.value,
            "value": self.value
        }
        
        if self.type in [MetricType.HISTOGRAM, MetricType.SUMMARY]:
            stats.update({
                "count": self.count,
                "sum": self.sum_value,
                "min": self.min_value,
                "max": self.max_value,
                "avg": self.sum_value / self.count if self.count > 0 else 0.0
            })
        
        return stats


@dataclass
class Alert:
    """Represents a monitoring alert."""
    id: str
    metric_name: str
    condition: str
    threshold: float
    current_value: float
    severity: str
    message: str
    timestamp: float = field(default_factory=time.time)
    resolved: bool = False


class CacheMonitor:
    """Monitors cache performance and health with metrics and alerts.
    
    This monitor provides:
    - Real-time metrics collection
    - Performance tracking
    - Health monitoring
    - Alerting system
    - Historical data analysis
    """
    
    def __init__(
        self,
        cache_layer: Any,
        metrics_window: int = 3600,
        alert_thresholds: Optional[Dict[str, float]] = None
    ):
        """Initialize cache monitor."""
        self.cache_layer = cache_layer
        self.metrics_window = metrics_window
        
        # Metrics storage
        self.metrics: Dict[str, Metric] = {}
        self._initialize_metrics()
        
        # Alert configuration
        self.alert_thresholds = alert_thresholds or self._default_alert_thresholds()
        self.active_alerts: Dict[str, Alert] = {}
        self.alert_history: List[Alert] = []
        
        # Historical data
        self.historical_data: Dict[str, deque] = defaultdict(
            lambda: deque(maxlen=1000)
        )
        
        # Monitoring thread
        self.monitoring_active = False
        self.monitor_thread: Optional[threading.Thread] = None
    
    def _initialize_metrics(self) -> None:
        """Initialize standard cache metrics."""
        self._create_metric("cache_hits", MetricType.COUNTER)
        self._create_metric("cache_misses", MetricType.COUNTER)
        self._create_metric("cache_writes", MetricType.COUNTER)
        self._create_metric("cache_evictions", MetricType.COUNTER)
        self._create_metric("hit_rate", MetricType.GAUGE)
        self._create_metric("miss_rate", MetricType.GAUGE)
        self._create_metric("latency_ms", MetricType.HISTOGRAM)
        self._create_metric("throughput", MetricType.GAUGE)
        self._create_metric("memory_usage_bytes", MetricType.GAUGE)
        self._create_metric("l1_size", MetricType.GAUGE)
        self._create_metric("l1_hit_rate", MetricType.GAUGE)
        self._create_metric("l2_hit_rate", MetricType.GAUGE)
        self._create_metric("l3_hit_rate", MetricType.GAUGE)
    
    def _create_metric(self, name: str, metric_type: MetricType) -> None:
        """Create a metric."""
        self.metrics[name] = Metric(name=name, type=metric_type)
    
    def _default_alert_thresholds(self) -> Dict[str, float]:
        """Get default alert thresholds."""
        return {
            "hit_rate_min": 0.7,
            "latency_max_ms": 100.0,
            "memory_usage_max_percent": 90.0,
            "l1_hit_rate_min": 0.5,
            "error_rate_max": 0.05
        }
    
    def record_hit(self, layer: str = "overall") -> None:
        """Record a cache hit."""
        metric_name = f"{layer}_hits" if layer != "overall" else "cache_hits"
        if metric_name in self.metrics:
            self.metrics[metric_name].record(1.0)
        self._update_hit_rate()
    
    def record_miss(self, layer: str = "overall") -> None:
        """Record a cache miss."""
        metric_name = f"{layer}_misses" if layer != "overall" else "cache_misses"
        if metric_name in self.metrics:
            self.metrics[metric_name].record(1.0)
        self._update_hit_rate()
    
    def record_write(self) -> None:
        """Record a cache write."""
        if "cache_writes" in self.metrics:
            self.metrics["cache_writes"].record(1.0)
    
    def record_eviction(self) -> None:
        """Record a cache eviction."""
        if "cache_evictions" in self.metrics:
            self.metrics["cache_evictions"].record(1.0)
    
    def record_latency(self, latency_ms: float) -> None:
        """Record cache operation latency."""
        if "latency_ms" in self.metrics:
            self.metrics["latency_ms"].record(latency_ms)
    
    def record_memory_usage(self, bytes_used: float) -> None:
        """Record memory usage."""
        if "memory_usage_bytes" in self.metrics:
            self.metrics["memory_usage_bytes"].record(bytes_used)
    
    def _update_hit_rate(self) -> None:
        """Update hit rate metrics."""
        hits = self.metrics["cache_hits"].value
        misses = self.metrics["cache_misses"].value
        total = hits + misses
        
        if total > 0:
            hit_rate = hits / total
            miss_rate = misses / total
            
            if "hit_rate" in self.metrics:
                self.metrics["hit_rate"].value = hit_rate
            if "miss_rate" in self.metrics:
                self.metrics["miss_rate"].value = miss_rate
    
    def update_layer_metrics(self) -> None:
        """Update layer-specific metrics."""
        # Update L1 metrics
        if hasattr(self.cache_layer, 'layer_stats'):
            l1_hits = self.cache_layer.layer_stats.get("l1", {}).get("hits", 0)
            l1_misses = self.cache_layer.layer_stats.get("l1", {}).get("misses", 0)
            l1_total = l1_hits + l1_misses
            
            if "l1_hit_rate" in self.metrics and l1_total > 0:
                self.metrics["l1_hit_rate"].value = l1_hits / l1_total
            
            if "l1_size" in self.metrics:
                self.metrics["l1_size"].value = len(self.cache_layer.l1_cache)
        
        # Update L2 and L3 metrics similarly
        if hasattr(self.cache_layer, 'l2_client'):
            l2_hits = self.cache_layer.layer_stats.get("l2", {}).get("hits", 0)
            l2_misses = self.cache_layer.layer_stats.get("l2", {}).get("misses", 0)
            l2_total = l2_hits + l2_misses
            
            if "l2_hit_rate" in self.metrics and l2_total > 0:
                self.metrics["l2_hit_rate"].value = l2_hits / l2_total
        
        if hasattr(self.cache_layer, 'l3_client'):
            l3_hits = self.cache_layer.layer_stats.get("l3", {}).get("hits", 0)
            l3_misses = self.cache_layer.layer_stats.get("l3", {}).get("misses", 0)
            l3_total = l3_hits + l3_misses
            
            if "l3_hit_rate" in self.metrics and l3_total > 0:
                self.metrics["l3_hit_rate"].value = l3_hits / l3_total
    
    def check_alerts(self) -> List[Alert]:
        """Check metrics against alert thresholds."""
        alerts = []
        
        # Check hit rate
        if "hit_rate" in self.metrics:
            hit_rate = self.metrics["hit_rate"].value
            min_threshold = self.alert_thresholds.get("hit_rate_min", 0.7)
            if hit_rate < min_threshold:
                alert = self._create_alert(
                    "hit_rate",
                    "hit_rate < threshold",
                    min_threshold,
                    hit_rate,
                    "warning",
                    f"Hit rate ({hit_rate:.2%}) below threshold ({min_threshold:.2%})"
                )
                alerts.append(alert)
        
        # Check latency
        if "latency_ms" in self.metrics:
            latency_metric = self.metrics["latency_ms"]
            avg_latency = latency_metric.sum_value / latency_metric.count if latency_metric.count > 0 else 0
            max_threshold = self.alert_thresholds.get("latency_max_ms", 100.0)
            if avg_latency > max_threshold:
                alert = self._create_alert(
                    "latency_ms",
                    "latency > threshold",
                    max_threshold,
                    avg_latency,
                    "warning",
                    f"Average latency ({avg_latency:.2f}ms) above threshold ({max_threshold:.2f}ms)"
                )
                alerts.append(alert)
        
        # Update active alerts
        for alert in alerts:
            self.active_alerts[alert.id] = alert
        
        return alerts
    
    def _create_alert(
        self,
        metric_name: str,
        condition: str,
        threshold: float,
        current_value: float,
        severity: str,
        message: str
    ) -> Alert:
        """Create an alert."""
        alert_id = f"{metric_name}_{int(time.time())}"
        return Alert(
            id=alert_id,
            metric_name=metric_name,
            condition=condition,
            threshold=threshold,
            current_value=current_value,
            severity=severity,
            message=message
        )
    
    def resolve_alert(self, alert_id: str) -> bool:
        """Resolve an alert."""
        if alert_id in self.active_alerts:
            alert = self.active_alerts[alert_id]
            alert.resolved = True
            self.alert_history.append(alert)
            del self.active_alerts[alert_id]
            return True
        return False
    
    def get_alerts(self, active_only: bool = True) -> List[Alert]:
        """Get alerts."""
        if active_only:
            return list(self.active_alerts.values())
        else:
            return list(self.active_alerts.values()) + self.alert_history
    
    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive monitoring statistics."""
        # Update layer metrics
        self.update_layer_metrics()
        
        # Collect all metrics
        metrics_stats = {}
        for name, metric in self.metrics.items():
            metrics_stats[name] = metric.get_stats()
        
        return {
            "metrics": metrics_stats,
            "alerts": {
                "active_count": len(self.active_alerts),
                "history_count": len(self.alert_history)
            }
        }
    
    def check_health(self) -> Dict[str, Any]:
        """Check cache health status."""
        health = {
            "status": "healthy",
            "monitoring": {
                "active": self.monitoring_active,
                "metrics_count": len(self.metrics),
                "active_alerts": len(self.active_alerts)
            }
        }
        
        # Check cache layer health if available
        if hasattr(self.cache_layer, 'health_check'):
            try:
                cache_health = self.cache_layer.health_check()
                health.update(cache_health)
            except Exception as e:
                health["status"] = "degraded"
                health["error"] = str(e)
        
        return health
    
    def start_monitoring(self, interval: int = 60) -> None:
        """Start background monitoring."""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        
        def monitor_loop():
            while self.monitoring_active:
                try:
                    self.update_layer_metrics()
                    self.check_alerts()
                    self._store_historical_data()
                    time.sleep(interval)
                except Exception as e:
                    print(f"Error in monitoring loop: {e}")
        
        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self) -> None:
        """Stop background monitoring."""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
    
    def _store_historical_data(self) -> None:
        """Store current metrics for historical analysis."""
        timestamp = time.time()
        
        for name, metric in self.metrics.items():
            self.historical_data[name].append({
                "timestamp": timestamp,
                "value": metric.value
            })
    
    def get_historical_data(self, metric_name: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get historical data for a metric."""
        return list(self.historical_data[metric_name])[-limit:]
    
    def reset_metrics(self) -> None:
        """Reset all metrics."""
        for metric in self.metrics.values():
            metric.value = 0.0
            metric.count = 0
            metric.sum_value = 0.0
            metric.min_value = None
            metric.max_value = None
            metric.timestamps.clear()
    
    def get_exported_metrics(self) -> Dict[str, float]:
        """Get metrics in export format."""
        exported = {}
        for name, metric in self.metrics.items():
            if metric.type in [MetricType.COUNTER, MetricType.GAUGE]:
                exported[name] = metric.value
            elif metric.type in [MetricType.HISTOGRAM, MetricType.SUMMARY]:
                exported[f"{name}_count"] = metric.count
                exported[f"{name}_sum"] = metric.sum_value
                exported[f"{name}_avg"] = metric.sum_value / metric.count if metric.count > 0 else 0.0
        
        return exported
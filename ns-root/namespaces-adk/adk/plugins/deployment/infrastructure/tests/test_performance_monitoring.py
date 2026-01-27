"""
Unit tests for Performance Monitoring Manager (APM)
"""

import pytest
import asyncio
from datetime import datetime, timedelta

import sys
sys.path.insert(0, '/workspace/machine-native-ops')

from adk.plugins.deployment.infrastructure.performance_monitoring import (
    PerformanceMonitoringManager,
    APMConfig,
    Span,
    Trace,
    Metric,
    PerformanceBaseline,
    PerformanceAnomaly,
    ServiceDependency,
    APMResult,
    TracingProvider,
    MetricType,
    SpanKind
)


class TestAPMConfig:
    """Test APMConfig dataclass"""
    
    def test_default_config(self):
        """Test default configuration"""
        config = APMConfig()
        
        assert config.enabled is True
        assert config.tracing_enabled is True
        assert config.tracing_sample_rate == 0.1
        assert config.metrics_enabled is True
        assert config.baseline_enabled is True
        assert config.anomaly_detection_enabled is True
    
    def test_custom_config(self):
        """Test custom configuration"""
        config = APMConfig(
            tracing_sample_rate=0.5,
            metrics_interval_seconds=30,
            baseline_calculation_period_days=14,
            anomaly_detection_threshold=3.0
        )
        
        assert config.tracing_sample_rate == 0.5
        assert config.metrics_interval_seconds == 30
        assert config.baseline_calculation_period_days == 14
        assert config.anomaly_detection_threshold == 3.0


class TestSpan:
    """Test Span class"""
    
    def test_span_creation(self):
        """Test creating span"""
        span = Span(
            trace_id="trace-123",
            span_id="span-456",
            parent_span_id=None,
            operation_name="GET /api/users",
            service_name="user-service",
            start_time=datetime.now(),
            end_time=datetime.now(),
            duration_ms=100.5,
            kind=SpanKind.SERVER
        )
        
        assert span.trace_id == "trace-123"
        assert span.span_id == "span-456"
        assert span.operation_name == "GET /api/users"
        assert span.duration_ms == 100.5
    
    def test_span_to_dict(self):
        """Test converting span to dictionary"""
        now = datetime.now()
        span = Span(
            trace_id="trace-123",
            span_id="span-456",
            parent_span_id=None,
            operation_name="GET /api/users",
            service_name="user-service",
            start_time=now,
            end_time=now,
            duration_ms=50.0,
            kind=SpanKind.SERVER
        )
        
        span_dict = span.to_dict()
        
        assert span_dict["trace_id"] == "trace-123"
        assert span_dict["span_id"] == "span-456"
        assert span_dict["operation_name"] == "GET /api/users"
        assert span_dict["kind"] == "server"


class TestMetric:
    """Test Metric class"""
    
    def test_metric_creation(self):
        """Test creating metric"""
        metric = Metric(
            name="request_duration",
            type=MetricType.HISTOGRAM,
            value=100.5,
            timestamp=datetime.now(),
            labels={"service": "api", "endpoint": "/users"}
        )
        
        assert metric.name == "request_duration"
        assert metric.type == MetricType.HISTOGRAM
        assert metric.value == 100.5
        assert metric.labels["service"] == "api"


class TestPerformanceMonitoringManager:
    """Test PerformanceMonitoringManager class"""
    
    @pytest.fixture
    def config(self):
        """Create test configuration"""
        return APMConfig()
    
    @pytest.fixture
    def manager(self, config):
        """Create performance monitoring manager instance"""
        return PerformanceMonitoringManager(config)
    
    def test_manager_initialization(self, manager):
        """Test manager initialization"""
        assert manager.config is not None
        assert manager._traces == {}
        assert manager._spans == []
        assert manager._metrics == []
        assert manager._baselines == {}
        assert manager._anomalies == []
    
    @pytest.mark.asyncio
    async def test_start_and_end_trace(self, manager):
        """Test starting and ending a trace"""
        trace_id = "trace-123"
        
        # Start span
        span = await manager.start_trace(
            trace_id=trace_id,
            operation_name="GET /api/users",
            service_name="api-service",
            kind=SpanKind.SERVER
        )
        
        assert span is not None
        assert span.trace_id == trace_id
        assert span.operation_name == "GET /api/users"
        
        # End span
        await manager.end_trace(span, status_code=200)
        
        assert span.duration_ms > 0
        assert span.status_code == 200
    
    @pytest.mark.asyncio
    async def test_record_metric(self, manager):
        """Test recording metric"""
        await manager.record_metric(
            name="request_count",
            value=1,
            metric_type=MetricType.COUNTER,
            labels={"service": "api", "method": "GET"}
        )
        
        assert len(manager._metrics) == 1
        assert manager._metrics[0].name == "request_count"
    
    @pytest.mark.asyncio
    async def test_get_trace(self, manager):
        """Test getting trace by ID"""
        trace_id = "trace-789"
        
        # Create a trace
        span = await manager.start_trace(
            trace_id=trace_id,
            operation_name="GET /api/products",
            service_name="api-service",
            kind=SpanKind.SERVER
        )
        await manager.end_trace(span)
        
        # Get trace
        trace = await manager.get_trace(trace_id)
        
        assert trace is not None
        assert trace.trace_id == trace_id
        assert len(trace.spans) >= 1
    
    @pytest.mark.asyncio
    async def test_get_statistics(self, manager):
        """Test getting APM statistics"""
        # Create some data
        for i in range(5):
            span = await manager.start_trace(
                trace_id=f"trace-{i}",
                operation_name=f"operation-{i}",
                service_name="service",
                kind=SpanKind.SERVER
            )
            await manager.end_trace(span)
        
        await manager.record_metric(name="metric1", value=100)
        await manager.record_metric(name="metric2", value=200)
        
        # Get statistics
        stats = await manager.get_statistics()
        
        assert stats["total_spans"] >= 5
        assert stats["total_traces"] >= 1
        assert stats["total_metrics"] >= 2


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
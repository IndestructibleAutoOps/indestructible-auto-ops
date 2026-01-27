"""
Enterprise-Grade Performance Monitoring Manager (APM)

Provides comprehensive application performance monitoring including
distributed tracing, metrics collection, and performance analytics.

Features:
- Distributed tracing with span tracking
- Real-time metrics collection
- Performance baseline and anomaly detection
- Service dependency mapping
- Root cause analysis
"""

import asyncio
import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
import yaml
import logging
import statistics

logger = logging.getLogger(__name__)


class TracingProvider(Enum):
    """Tracing providers"""
    JAEGER = "jaeger"
    ZIPKIN = "zipkin"
    DATADOG = "datadog"
    NEWRELIC = "newrelic"
    ELASTIC_APM = "elastic_apm"
    OPENTELEMETRY = "opentelemetry"


class MetricType(Enum):
    """Metric types"""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


class SpanKind(Enum):
    """Span kinds"""
    SERVER = "server"
    CLIENT = "client"
    PRODUCER = "producer"
    CONSUMER = "consumer"
    INTERNAL = "internal"


@dataclass
class APMConfig:
    """APM configuration"""
    enabled: bool = True
    tracing_provider: TracingProvider = TracingProvider.OPENTELEMETRY
    metrics_provider: str = "prometheus"
    
    # Tracing
    tracing_enabled: bool = True
    tracing_sample_rate: float = 0.1  # 10% sample rate
    max_span_count: int = 1000
    span_export_timeout_seconds: int = 30
    
    # Metrics
    metrics_enabled: bool = True
    metrics_interval_seconds: int = 15
    histogram_buckets: List[int] = field(default_factory=lambda: [1, 5, 10, 25, 50, 100, 250, 500, 1000])
    
    # Performance baselines
    baseline_enabled: bool = True
    baseline_calculation_period_days: int = 7
    anomaly_detection_enabled: bool = True
    anomaly_detection_threshold: float = 2.0  # 2 standard deviations
    
    # Service mapping
    service_mapping_enabled: bool = True
    dependency_tracking_enabled: bool = True
    
    # Alerting
    alerting_enabled: bool = True
    slow_threshold_ms: int = 500
    error_threshold_percent: float = 1.0
    
    # Storage
    data_retention_days: int = 30
    archive_enabled: bool = True
    archive_retention_days: int = 90


@dataclass
class Span:
    """Trace span"""
    trace_id: str
    span_id: str
    parent_span_id: Optional[str]
    operation_name: str
    service_name: str
    start_time: datetime
    end_time: datetime
    duration_ms: float
    kind: SpanKind
    tags: Dict[str, str] = field(default_factory=dict)
    logs: List[Dict[str, Any]] = field(default_factory=list)
    status_code: Optional[int] = None
    status_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_span_id": self.parent_span_id,
            "operation_name": self.operation_name,
            "service_name": self.service_name,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "duration_ms": self.duration_ms,
            "kind": self.kind.value,
            "tags": self.tags,
            "logs": self.logs,
            "status_code": self.status_code,
            "status_message": self.status_message
        }


@dataclass
class Trace:
    """Trace with multiple spans"""
    trace_id: str
    root_span_id: str
    spans: List[Span]
    start_time: datetime
    end_time: datetime
    duration_ms: float
    service_names: Set[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "trace_id": self.trace_id,
            "root_span_id": self.root_span_id,
            "spans": [span.to_dict() for span in self.spans],
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "duration_ms": self.duration_ms,
            "service_names": list(self.service_names)
        }


@dataclass
class Metric:
    """Metric data point"""
    name: str
    type: MetricType
    value: float
    timestamp: datetime
    labels: Dict[str, str] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "type": self.type.value,
            "value": self.value,
            "timestamp": self.timestamp.isoformat(),
            "labels": self.labels
        }


@dataclass
class PerformanceBaseline:
    """Performance baseline"""
    metric_name: str
    service_name: str
    operation_name: Optional[str]
    p50: float
    p95: float
    p99: float
    mean: float
    std_dev: float
    min_value: float
    max_value: float
    sample_count: int
    calculated_at: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "metric_name": self.metric_name,
            "service_name": self.service_name,
            "operation_name": self.operation_name,
            "p50": self.p50,
            "p95": self.p95,
            "p99": self.p99,
            "mean": self.mean,
            "std_dev": self.std_dev,
            "min_value": self.min_value,
            "max_value": self.max_value,
            "sample_count": self.sample_count,
            "calculated_at": self.calculated_at.isoformat()
        }


@dataclass
class PerformanceAnomaly:
    """Performance anomaly"""
    metric_name: str
    service_name: str
    operation_name: Optional[str]
    detected_at: datetime
    anomaly_type: str
    expected_value: float
    actual_value: float
    deviation: float
    severity: str  # low, medium, high, critical
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "metric_name": self.metric_name,
            "service_name": self.service_name,
            "operation_name": self.operation_name,
            "detected_at": self.detected_at.isoformat(),
            "anomaly_type": self.anomaly_type,
            "expected_value": self.expected_value,
            "actual_value": self.actual_value,
            "deviation": self.deviation,
            "severity": self.severity
        }


@dataclass
class ServiceDependency:
    """Service dependency"""
    source_service: str
    target_service: str
    dependency_type: str
    call_count: int
    avg_latency_ms: float
    error_rate: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "source_service": self.source_service,
            "target_service": self.target_service,
            "dependency_type": self.dependency_type,
            "call_count": self.call_count,
            "avg_latency_ms": self.avg_latency_ms,
            "error_rate": self.error_rate
        }


@dataclass
class APMResult:
    """APM operation result"""
    success: bool
    message: str
    data: Optional[Any] = None
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    execution_time: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data,
            "warnings": self.warnings,
            "errors": self.errors,
            "execution_time": self.execution_time
        }


class PerformanceMonitoringManager:
    """
    Enterprise-grade performance monitoring manager (APM)
    
    Provides comprehensive application performance monitoring including
    distributed tracing, metrics collection, and performance analytics.
    """
    
    def __init__(self, config: APMConfig):
        """
        Initialize performance monitoring manager
        
        Args:
            config: APM configuration
        """
        self.config = config
        self._traces: Dict[str, Trace] = {}
        self._spans: List[Span] = []
        self._metrics: List[Metric] = []
        self._baselines: Dict[str, PerformanceBaseline] = {}
        self._anomalies: List[PerformanceAnomaly] = []
        self._dependencies: Dict[str, ServiceDependency] = {}
        self._active_traces: Dict[str, List[Span]] = {}
        
        logger.info("PerformanceMonitoringManager initialized (APM)")
    
    async def start_trace(
        self,
        trace_id: str,
        operation_name: str,
        service_name: str,
        kind: SpanKind = SpanKind.SERVER,
        parent_span_id: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None
    ) -> Span:
        """
        Start a new trace span
        
        Args:
            trace_id: Trace ID
            operation_name: Operation name
            service_name: Service name
            kind: Span kind
            parent_span_id: Parent span ID
            tags: Span tags
        
        Returns:
            Started span
        """
        if not self.config.tracing_enabled:
            return None
        
        span_id = self._generate_span_id()
        start_time = datetime.now()
        
        span = Span(
            trace_id=trace_id,
            span_id=span_id,
            parent_span_id=parent_span_id,
            operation_name=operation_name,
            service_name=service_name,
            start_time=start_time,
            end_time=start_time,
            duration_ms=0,
            kind=kind,
            tags=tags or {}
        )
        
        # Add to active traces
        if trace_id not in self._active_traces:
            self._active_traces[trace_id] = []
        self._active_traces[trace_id].append(span)
        
        logger.debug(f"Started span: {span_id} for trace: {trace_id}")
        return span
    
    async def end_trace(
        self,
        span: Span,
        status_code: Optional[int] = None,
        status_message: Optional[str] = None
    ) -> None:
        """
        End a trace span
        
        Args:
            span: Span to end
            status_code: Status code
            status_message: Status message
        """
        if not span:
            return
        
        span.end_time = datetime.now()
        span.duration_ms = (span.end_time - span.start_time).total_seconds() * 1000
        span.status_code = status_code
        span.status_message = status_message
        
        # Add to spans list
        self._spans.append(span)
        
        # Collect metrics from span
        if self.config.metrics_enabled:
            await self._collect_span_metrics(span)
        
        # Check for slow spans
        if self.config.alerting_enabled:
            await self._check_slow_span(span)
        
        # Update dependencies
        if self.config.dependency_tracking_enabled:
            await self._update_dependencies(span)
        
        # Check if trace is complete
        if span.trace_id in self._active_traces:
            active_spans = self._active_traces[span.trace_id]
            if span in active_spans:
                active_spans.remove(span)
            
            # If no more active spans, finalize trace
            if not active_spans:
                await self._finalize_trace(span.trace_id)
        
        logger.debug(f"Ended span: {span.span_id} (duration: {span.duration_ms:.2f}ms)")
    
    async def record_metric(
        self,
        name: str,
        value: float,
        metric_type: MetricType = MetricType.GAUGE,
        labels: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Record a metric
        
        Args:
            name: Metric name
            value: Metric value
            metric_type: Metric type
            labels: Metric labels
        """
        if not self.config.metrics_enabled:
            return
        
        metric = Metric(
            name=name,
            type=metric_type,
            value=value,
            timestamp=datetime.now(),
            labels=labels or {}
        )
        
        self._metrics.append(metric)
        
        # Check for anomalies
        if self.config.anomaly_detection_enabled:
            await self._check_for_anomaly(metric)
        
        logger.debug(f"Recorded metric: {name} = {value}")
    
    async def get_trace(
        self,
        trace_id: str
    ) -> Optional[Trace]:
        """
        Get trace by ID
        
        Args:
            trace_id: Trace ID
        
        Returns:
            Trace or None
        """
        return self._traces.get(trace_id)
    
    async def search_traces(
        self,
        service_name: Optional[str] = None,
        operation_name: Optional[str] = None,
        min_duration_ms: Optional[float] = None,
        max_duration_ms: Optional[float] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 100
    ) -> List[Trace]:
        """
        Search traces
        
        Args:
            service_name: Filter by service name
            operation_name: Filter by operation name
            min_duration_ms: Minimum duration
            max_duration_ms: Maximum duration
            start_time: Start time
            end_time: End time
            limit: Maximum number of results
        
        Returns:
            List of matching traces
        """
        results = []
        
        for trace in self._traces.values():
            # Filter by service name
            if service_name and service_name not in trace.service_names:
                continue
            
            # Filter by operation name
            if operation_name:
                has_operation = any(
                    span.operation_name == operation_name
                    for span in trace.spans
                )
                if not has_operation:
                    continue
            
            # Filter by duration
            if min_duration_ms and trace.duration_ms < min_duration_ms:
                continue
            
            if max_duration_ms and trace.duration_ms > max_duration_ms:
                continue
            
            # Filter by time range
            if start_time and trace.start_time < start_time:
                continue
            
            if end_time and trace.end_time > end_time:
                continue
            
            results.append(trace)
            
            if len(results) >= limit:
                break
        
        return results
    
    async def get_metrics(
        self,
        metric_name: Optional[str] = None,
        labels: Optional[Dict[str, str]] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 1000
    ) -> List[Metric]:
        """
        Get metrics
        
        Args:
            metric_name: Filter by metric name
            labels: Filter by labels
            start_time: Start time
            end_time: End time
            limit: Maximum number of results
        
        Returns:
            List of matching metrics
        """
        results = []
        
        for metric in self._metrics:
            # Filter by name
            if metric_name and metric.name != metric_name:
                continue
            
            # Filter by labels
            if labels:
                if not all(metric.labels.get(k) == v for k, v in labels.items()):
                    continue
            
            # Filter by time range
            if start_time and metric.timestamp < start_time:
                continue
            
            if end_time and metric.timestamp > end_time:
                continue
            
            results.append(metric)
            
            if len(results) >= limit:
                break
        
        return results
    
    async def calculate_baseline(
        self,
        metric_name: str,
        service_name: str,
        operation_name: Optional[str] = None
    ) -> PerformanceBaseline:
        """
        Calculate performance baseline
        
        Args:
            metric_name: Metric name
            service_name: Service name
            operation_name: Operation name
        
        Returns:
            Performance baseline
        """
        # Get metric values for baseline calculation
        metric_values = []
        
        for metric in self._metrics:
            if metric.name == metric_name:
                service_match = metric.labels.get("service") == service_name
                
                operation_match = True
                if operation_name:
                    operation_match = metric.labels.get("operation") == operation_name
                
                if service_match and operation_match:
                    metric_values.append(metric.value)
        
        if not metric_values:
            # Return default baseline
            return PerformanceBaseline(
                metric_name=metric_name,
                service_name=service_name,
                operation_name=operation_name,
                p50=0,
                p95=0,
                p99=0,
                mean=0,
                std_dev=0,
                min_value=0,
                max_value=0,
                sample_count=0,
                calculated_at=datetime.now()
            )
        
        # Calculate statistics
        sorted_values = sorted(metric_values)
        count = len(sorted_values)
        
        p50_index = int(count * 0.5)
        p95_index = int(count * 0.95)
        p99_index = int(count * 0.99)
        
        baseline = PerformanceBaseline(
            metric_name=metric_name,
            service_name=service_name,
            operation_name=operation_name,
            p50=sorted_values[p50_index],
            p95=sorted_values[p95_index],
            p99=sorted_values[p99_index],
            mean=statistics.mean(metric_values),
            std_dev=statistics.stdev(metric_values) if count > 1 else 0,
            min_value=min(metric_values),
            max_value=max(metric_values),
            sample_count=count,
            calculated_at=datetime.now()
        )
        
        # Store baseline
        baseline_key = self._get_baseline_key(metric_name, service_name, operation_name)
        self._baselines[baseline_key] = baseline
        
        logger.info(f"Calculated baseline for {baseline_key}")
        return baseline
    
    async def detect_anomalies(self) -> List[PerformanceAnomaly]:
        """
        Detect performance anomalies
        
        Returns:
            List of detected anomalies
        """
        anomalies = []
        
        for metric in self._metrics[-1000:]:  # Check last 1000 metrics
            baseline_key = self._get_baseline_key(
                metric.name,
                metric.labels.get("service", ""),
                metric.labels.get("operation")
            )
            
            baseline = self._baselines.get(baseline_key)
            if not baseline:
                continue
            
            # Calculate deviation
            if baseline.std_dev > 0:
                deviation = abs(metric.value - baseline.mean) / baseline.std_dev
                
                # Check if anomaly
                if deviation > self.config.anomaly_detection_threshold:
                    # Determine severity
                    if deviation > 5.0:
                        severity = "critical"
                    elif deviation > 3.0:
                        severity = "high"
                    elif deviation > 2.0:
                        severity = "medium"
                    else:
                        severity = "low"
                    
                    anomaly = PerformanceAnomaly(
                        metric_name=metric.name,
                        service_name=metric.labels.get("service", ""),
                        operation_name=metric.labels.get("operation"),
                        detected_at=datetime.now(),
                        anomaly_type="statistical",
                        expected_value=baseline.mean,
                        actual_value=metric.value,
                        deviation=deviation,
                        severity=severity
                    )
                    
                    anomalies.append(anomaly)
                    self._anomalies.append(anomaly)
        
        logger.info(f"Detected {len(anomalies)} anomalies")
        return anomalies
    
    async def get_service_dependencies(self) -> List[ServiceDependency]:
        """Get service dependencies"""
        return list(self._dependencies.values())
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Get APM statistics"""
        total_spans = len(self._spans)
        total_traces = len(self._traces)
        total_metrics = len(self._metrics)
        total_baselines = len(self._baselines)
        total_anomalies = len(self._anomalies)
        
        # Calculate span statistics
        if total_spans > 0:
            durations = [span.duration_ms for span in self._spans]
            avg_duration = statistics.mean(durations)
            p95_duration = sorted(durations)[int(len(durations) * 0.95)]
        else:
            avg_duration = 0
            p95_duration = 0
        
        return {
            "total_spans": total_spans,
            "total_traces": total_traces,
            "total_metrics": total_metrics,
            "total_baselines": total_baselines,
            "total_anomalies": total_anomalies,
            "avg_span_duration_ms": avg_duration,
            "p95_span_duration_ms": p95_duration,
            "total_dependencies": len(self._dependencies)
        }
    
    async def _collect_span_metrics(self, span: Span) -> None:
        """Collect metrics from span"""
        # Record duration metric
        await self.record_metric(
            name="span_duration",
            value=span.duration_ms,
            metric_type=MetricType.HISTOGRAM,
            labels={
                "service": span.service_name,
                "operation": span.operation_name,
                "kind": span.kind.value
            }
        )
        
        # Record status metric
        if span.status_code:
            await self.record_metric(
                name="span_status",
                value=1,
                metric_type=MetricType.COUNTER,
                labels={
                    "service": span.service_name,
                    "operation": span.operation_name,
                    "status_code": str(span.status_code)
                }
            )
    
    async def _check_slow_span(self, span: Span) -> None:
        """Check for slow spans"""
        if span.duration_ms > self.config.slow_threshold_ms:
            logger.warning(
                f"Slow span detected: {span.operation_name} "
                f"(duration: {span.duration_ms:.2f}ms, threshold: {self.config.slow_threshold_ms}ms)"
            )
    
    async def _update_dependencies(self, span: Span) -> None:
        """Update service dependencies"""
        if span.kind in [SpanKind.CLIENT, SpanKind.PRODUCER]:
            target_service = span.tags.get("peer.service", "unknown")
            dependency_key = f"{span.service_name}->{target_service}"
            
            if dependency_key not in self._dependencies:
                self._dependencies[dependency_key] = ServiceDependency(
                    source_service=span.service_name,
                    target_service=target_service,
                    dependency_type="rpc",
                    call_count=0,
                    avg_latency_ms=0,
                    error_rate=0
                )
            
            dependency = self._dependencies[dependency_key]
            dependency.call_count += 1
            
            # Update average latency
            total_calls = dependency.call_count
            dependency.avg_latency_ms = (
                (dependency.avg_latency_ms * (total_calls - 1) + span.duration_ms) / total_calls
            )
    
    async def _finalize_trace(self, trace_id: str) -> None:
        """Finalize trace"""
        # Get all spans for this trace
        trace_spans = [span for span in self._spans if span.trace_id == trace_id]
        
        if not trace_spans:
            return
        
        # Find root span (no parent)
        root_span = None
        for span in trace_spans:
            if span.parent_span_id is None:
                root_span = span
                break
        
        if not root_span:
            root_span = trace_spans[0]  # Use first span as root
        
        # Calculate trace duration
        start_time = min(span.start_time for span in trace_spans)
        end_time = max(span.end_time for span in trace_spans)
        duration_ms = (end_time - start_time).total_seconds() * 1000
        
        # Get unique service names
        service_names = set(span.service_name for span in trace_spans)
        
        # Create trace
        trace = Trace(
            trace_id=trace_id,
            root_span_id=root_span.span_id,
            spans=trace_spans,
            start_time=start_time,
            end_time=end_time,
            duration_ms=duration_ms,
            service_names=service_names
        )
        
        # Store trace
        self._traces[trace_id] = trace
        
        # Remove from active traces
        self._active_traces.pop(trace_id, None)
        
        logger.debug(f"Finalized trace: {trace_id} ({len(trace_spans)} spans, {duration_ms:.2f}ms)")
    
    async def _check_for_anomaly(self, metric: Metric) -> None:
        """Check metric for anomaly"""
        baseline_key = self._get_baseline_key(
            metric.name,
            metric.labels.get("service", ""),
            metric.labels.get("operation")
        )
        
        baseline = self._baselines.get(baseline_key)
        if not baseline:
            return
        
        if baseline.std_dev > 0:
            deviation = abs(metric.value - baseline.mean) / baseline.std_dev
            if deviation > self.config.anomaly_detection_threshold:
                logger.warning(
                    f"Anomaly detected: {metric.name} = {metric.value} "
                    f"(expected: {baseline.mean:.2f}, deviation: {deviation:.2f}σ)"
                )
    
    def _generate_span_id(self) -> str:
        """Generate span ID"""
        import secrets
        return secrets.token_hex(8)
    
    def _get_baseline_key(
        self,
        metric_name: str,
        service_name: str,
        operation_name: Optional[str]
    ) -> str:
        """Get baseline key"""
        key = f"{metric_name}:{service_name}"
        if operation_name:
            key += f":{operation_name}"
        return key
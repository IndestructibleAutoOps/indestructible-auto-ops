"""
Observability Module: Logging, tracing, metrics, and event schemas.

This package provides comprehensive observability capabilities including
structured logging, distributed tracing, metrics collection, and
event schema definitions.

GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module ns-root/namespaces-adk/adk/observability
@gl-semantic-anchor GL-00-ADK_OBSERVAB_INIT
@gl-evidence-required false
GL Unified Charter Activated
"""

from .event_schema import EventSchemaDef, EventSchemaRegistry, EventType
from .logging import LogContext, Logger, LogLevel
from .metrics import Metric, MetricsCollector, MetricType, Timer
from .tracing import Span, SpanStatus, Trace, Tracer

__all__ = [
    # Logging
    "Logger",
    "LogLevel",
    "LogContext",
    # Tracing
    "Tracer",
    "Span",
    "Trace",
    "SpanStatus",
    # Metrics
    "MetricsCollector",
    "Metric",
    "MetricType",
    "Timer",
    # Event Schemas
    "EventSchemaDef",
    "EventSchemaRegistry",
    "EventType",
]

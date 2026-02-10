#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL50-59
# @GL-semantic: audit-logging
# @GL-audit-trail: ./governance/GL_SEMANTIC_ANCHOR.json
#
"""
Audit Logging Module
====================
GL Layer: GL50-59 Observability Layer

Provides comprehensive audit logging with:
- Full audit fields (actor, action, resource, result, hash, version, requestId, correlationId, ip, userAgent)
- UTC RFC3339 timestamps
- OpenTelemetry compatible tracing
- JSONL format for centralized logging
- Replayable audit logs
"""

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
# MNGA-002: Import organization needs review
import os
import json
import hashlib
import socket
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, asdict, field
from enum import Enum


class AuditAction(Enum):
    """Audit action types"""

    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    VALIDATE = "validate"
    EXECUTE = "execute"
    BOOTSTRAP = "bootstrap"
    VERIFY = "verify"
    DEPLOY = "deploy"
    ROLLBACK = "rollback"
    GOVERNANCE = "governance"


class AuditResult(Enum):
    """Audit result types"""

    SUCCESS = "success"
    FAILURE = "failure"
    WARNING = "warning"
    SKIPPED = "skipped"
    PENDING = "pending"


@dataclass
class AuditEntry:
    """
    Comprehensive audit entry with all required fields.

    Fields:
    - timestamp: UTC RFC3339 format timestamp
    - actor: The user or system performing the action
    - action: The action being performed
    - resource: The resource being acted upon
    - result: The outcome of the action
    - hash: SHA256 hash of the entry content for integrity
    - version: Version of the audit schema
    - requestId: Unique identifier for this request
    - correlationId: Identifier to correlate related requests
    - ip: IP address of the actor
    - userAgent: User agent or system identifier
    - traceId: OpenTelemetry trace ID
    - spanId: OpenTelemetry span ID
    - parentSpanId: Parent span ID for distributed tracing
    - details: Additional details about the action
    - metadata: Extra metadata
    """

    timestamp: str
    actor: str
    action: str
    resource: str
    result: str
    hash: str = ""
    version: str = "1.0.0"
    requestId: str = ""
    correlationId: str = ""
    ip: str = "127.0.0.1"
    userAgent: str = "audit-logger/1.0.0"
    traceId: str = ""
    spanId: str = ""
    parentSpanId: str = ""
    details: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Generate computed fields after initialization"""
        if not self.requestId:
            self.requestId = self._generate_request_id()
        if not self.correlationId:
            self.correlationId = self.requestId
        if not self.traceId:
            self.traceId = self._generate_trace_id()
        if not self.spanId:
            self.spanId = self._generate_span_id()
        if not self.hash:
            self.hash = self._calculate_hash()

    def _generate_request_id(self) -> str:
        """Generate unique request ID"""
        return f"{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8]}"

    def _generate_trace_id(self) -> str:
        """Generate OpenTelemetry compatible trace ID (32 hex chars)"""
        return uuid.uuid4().hex

    def _generate_span_id(self) -> str:
        """Generate OpenTelemetry compatible span ID (16 hex chars)"""
        return uuid.uuid4().hex[:16]

    def _calculate_hash(self) -> str:
        """Calculate SHA256 hash of entry content"""
        content = (
            f"{self.timestamp}|{self.actor}|{self.action}|{self.resource}|{self.result}"
        )
        return hashlib.sha256(content.encode()).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)

    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), ensure_ascii=False)

    def to_jsonl(self) -> str:
        """Convert to JSONL format (single line)"""
        return json.dumps(self.to_dict(), ensure_ascii=False, separators=(",", ":"))


class AuditLogger:
    """
    Comprehensive audit logger with OpenTelemetry and JSONL support.

    Features:
    - Full audit fields
    - UTC RFC3339 timestamps
    - OpenTelemetry compatible tracing
    - JSONL format for centralized logging
    - Replayable audit logs
    """

    VERSION = "1.0.0"

    def __init__(
        self,
        log_dir: Optional[str] = None,
        actor: Optional[str] = None,
        user_agent: str = "audit-logger/1.0.0",
        enable_file_logging: bool = True,
        enable_console_logging: bool = False,
    ):
        """
        Initialize audit logger.

        Args:
            log_dir: Directory for audit log files
            actor: Default actor name (defaults to current user)
            user_agent: User agent string
            enable_file_logging: Enable logging to files
            enable_console_logging: Enable logging to console
        """
        self.log_dir = Path(log_dir) if log_dir else self._get_default_log_dir()
        self.actor = actor or os.environ.get("USER", "system")
        self.user_agent = user_agent
        self.enable_file_logging = enable_file_logging
        self.enable_console_logging = enable_console_logging

        # Current trace context
        self._trace_id: Optional[str] = None
        self._span_stack: List[str] = []

        # IP address
        self._ip = self._get_ip_address()

        # Ensure log directory exists
        if self.enable_file_logging:
            self.log_dir.mkdir(parents=True, exist_ok=True)

    def _get_default_log_dir(self) -> Path:
        """Get default log directory"""
        # Try to find project root
        current = Path(__file__).parent
        while current != current.parent:
            if (current / "ecosystem").exists():
                return current / "ecosystem" / "logs" / "audit-logs"
            current = current.parent

        # Fallback to current directory
        return Path("./logs/audit-logs")

    def _get_ip_address(self) -> str:
        """Get current IP address"""
        # Try SSH_CLIENT first
        ssh_client = os.environ.get("SSH_CLIENT", "")
        if ssh_client:
            return ssh_client.split()[0]

        # Try to get local IP
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    @staticmethod
    def get_utc_timestamp() -> str:
        """Get current UTC timestamp in RFC3339 format"""
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def start_trace(self, trace_id: Optional[str] = None) -> str:
        """Start a new trace and return the trace ID"""
        self._trace_id = trace_id or uuid.uuid4().hex
        self._span_stack = []
        return self._trace_id

    def start_span(self) -> str:
        """Start a new span and return the span ID"""
        span_id = uuid.uuid4().hex[:16]
        self._span_stack.append(span_id)
        return span_id

    def end_span(self) -> Optional[str]:
        """End the current span and return the span ID"""
        if self._span_stack:
            return self._span_stack.pop()
        return None

    def get_parent_span_id(self) -> str:
        """Get the parent span ID"""
        if len(self._span_stack) > 1:
            return self._span_stack[-2]
        return ""

    def log(
        self,
        action: str,
        resource: str,
        result: str,
        actor: Optional[str] = None,
        details: str = "",
        metadata: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
    ) -> AuditEntry:
        """
        Log an audit entry.

        Args:
            action: The action being performed
            resource: The resource being acted upon
            result: The outcome of the action
            actor: Override default actor
            details: Additional details
            metadata: Extra metadata
            request_id: Override request ID
            correlation_id: Override correlation ID

        Returns:
            AuditEntry object
        """
        # Create audit entry
        entry = AuditEntry(
            timestamp=self.get_utc_timestamp(),
            actor=actor or self.actor,
            action=action,
            resource=resource,
            result=result,
            version=self.VERSION,
            requestId=request_id or "",
            correlationId=correlation_id or "",
            ip=self._ip,
            userAgent=self.user_agent,
            traceId=self._trace_id or "",
            spanId=self._span_stack[-1] if self._span_stack else "",
            parentSpanId=self.get_parent_span_id(),
            details=details,
            metadata=metadata or {},
        )

        # Recalculate hash after all fields are set
        entry.hash = entry._calculate_hash()

        # Write to file
        if self.enable_file_logging:
            self._write_to_file(entry)

        # Write to console
        if self.enable_console_logging:
            self._write_to_console(entry)

        return entry

    def log_action(
        self, action: AuditAction, resource: str, result: AuditResult, **kwargs
    ) -> AuditEntry:
        """Log an audit entry using enum types"""
        return self.log(
            action=action.value, resource=resource, result=result.value, **kwargs
        )

    def _write_to_file(self, entry: AuditEntry):
        """Write audit entry to JSONL file"""
        # Use date-based file naming
        date_str = datetime.now(timezone.utc).strftime("%Y-%m")
        log_file = self.log_dir / f"audit-{date_str}.jsonl"

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(entry.to_jsonl() + "\n")

    def _write_to_console(self, entry: AuditEntry):
        """Write audit entry to console"""
        print(
            f"[AUDIT] {entry.timestamp} | {entry.actor} | {entry.action} | {entry.resource} | {entry.result}"
        )

    def replay_logs(
        self,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        filter_action: Optional[str] = None,
        filter_resource: Optional[str] = None,
        filter_result: Optional[str] = None,
    ) -> List[AuditEntry]:
        """
        Replay audit logs with optional filtering.

        Args:
            start_time: Start time filter (RFC3339)
            end_time: End time filter (RFC3339)
            filter_action: Filter by action
            filter_resource: Filter by resource (substring match)
            filter_result: Filter by result

        Returns:
            List of matching AuditEntry objects
        """
        entries = []

        # Read all JSONL files in log directory
        for log_file in sorted(self.log_dir.glob("audit-*.jsonl")):
            with open(log_file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        data = json.loads(line.strip())
                        entry = AuditEntry(**data)

                        # Apply filters
                        if start_time and entry.timestamp < start_time:
                            continue
                        if end_time and entry.timestamp > end_time:
                            continue
                        if filter_action and entry.action != filter_action:
                            continue
                        if filter_resource and filter_resource not in entry.resource:
                            continue
                        if filter_result and entry.result != filter_result:
                            continue

                        entries.append(entry)
                    except (json.JSONDecodeError, TypeError):
                        continue

        return entries

    def verify_integrity(self, entry: AuditEntry) -> bool:
        """
        Verify the integrity of an audit entry.

        Args:
            entry: AuditEntry to verify

        Returns:
            True if the hash is valid, False otherwise
        """
        expected_hash = hashlib.sha256(
            f"{entry.timestamp}|{entry.actor}|{entry.action}|{entry.resource}|{entry.result}".encode()
        ).hexdigest()

        return entry.hash == expected_hash

    def get_audit_summary(
        self, start_time: Optional[str] = None, end_time: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get a summary of audit logs.

        Args:
            start_time: Start time filter (RFC3339)
            end_time: End time filter (RFC3339)

        Returns:
            Dictionary with audit summary
        """
        entries = self.replay_logs(start_time=start_time, end_time=end_time)

        actions = {}
        results = {}
        actors = {}

        for entry in entries:
            actions[entry.action] = actions.get(entry.action, 0) + 1
            results[entry.result] = results.get(entry.result, 0) + 1
            actors[entry.actor] = actors.get(entry.actor, 0) + 1

        return {
            "total_entries": len(entries),
            "actions": actions,
            "results": results,
            "actors": actors,
            "time_range": {
                "start": entries[0].timestamp if entries else None,
                "end": entries[-1].timestamp if entries else None,
            },
        }


# Global logger instance
_global_logger: Optional[AuditLogger] = None


def get_audit_logger(log_dir: Optional[str] = None, **kwargs) -> AuditLogger:
    """
    Get the global audit logger instance.

    Args:
        log_dir: Optional log directory override
        **kwargs: Additional arguments for AuditLogger

    Returns:
        AuditLogger instance
    """
    global _global_logger

    if _global_logger is None or log_dir is not None:
        _global_logger = AuditLogger(log_dir=log_dir, **kwargs)

    return _global_logger


def audit_log(action: str, resource: str, result: str, **kwargs) -> AuditEntry:
    """
    Convenience function to log an audit entry.

    Args:
        action: The action being performed
        resource: The resource being acted upon
        result: The outcome of the action
        **kwargs: Additional arguments

    Returns:
        AuditEntry object
    """
    logger = get_audit_logger()
    return logger.log(action=action, resource=resource, result=result, **kwargs)


# OpenTelemetry compatible exporter
class OpenTelemetryExporter:
    """
    Export audit logs to OpenTelemetry format.
    """

    @staticmethod
    def to_otel_span(entry: AuditEntry) -> Dict[str, Any]:
        """
        Convert AuditEntry to OpenTelemetry span format.

        Args:
            entry: AuditEntry to convert

        Returns:
            Dictionary in OpenTelemetry span format
        """
        return {
            "traceId": entry.traceId,
            "spanId": entry.spanId,
            "parentSpanId": entry.parentSpanId,
            "name": f"{entry.action}:{entry.resource}",
            "kind": "INTERNAL",
            "startTimeUnixNano": int(
                datetime.fromisoformat(
                    entry.timestamp.replace("Z", "+00:00")
                ).timestamp()
                * 1e9
            ),
            "endTimeUnixNano": int(
                datetime.fromisoformat(
                    entry.timestamp.replace("Z", "+00:00")
                ).timestamp()
                * 1e9
            ),
            "attributes": [
                {"key": "actor", "value": {"stringValue": entry.actor}},
                {"key": "action", "value": {"stringValue": entry.action}},
                {"key": "resource", "value": {"stringValue": entry.resource}},
                {"key": "result", "value": {"stringValue": entry.result}},
                {"key": "requestId", "value": {"stringValue": entry.requestId}},
                {"key": "correlationId", "value": {"stringValue": entry.correlationId}},
                {"key": "ip", "value": {"stringValue": entry.ip}},
                {"key": "userAgent", "value": {"stringValue": entry.userAgent}},
            ],
            "status": {
                "code": (
                    "OK"
                    if entry.result in ["success", "passed", "completed"]
                    else "ERROR"
                )
            },
        }

    @staticmethod
    def export_to_json(entries: List[AuditEntry]) -> str:
        """
        Export multiple entries to OpenTelemetry JSON format.

        Args:
            entries: List of AuditEntry objects

        Returns:
            JSON string in OpenTelemetry format
        """
        spans = [OpenTelemetryExporter.to_otel_span(e) for e in entries]

        return json.dumps(
            {
                "resourceSpans": [
                    {
                        "resource": {
                            "attributes": [
                                {
                                    "key": "service.name",
                                    "value": {"stringValue": "machine-native-ops"},
                                },
                                {
                                    "key": "service.version",
                                    "value": {"stringValue": AuditLogger.VERSION},
                                },
                            ]
                        },
                        "scopeSpans": [
                            {
                                "scope": {
                                    "name": "audit-logger",
                                    "version": AuditLogger.VERSION,
                                },
                                "spans": spans,
                            }
                        ],
                    }
                ]
            },
            indent=2,
        )


if __name__ == "__main__":
    # Demo usage
    logger = AuditLogger(enable_console_logging=True)

    # Start a trace
    trace_id = logger.start_trace()
    print(f"Started trace: {trace_id}")

    # Start a span
    span_id = logger.start_span()
    print(f"Started span: {span_id}")

    # Log some entries
    entry1 = logger.log(
        action="bootstrap",
        resource="ecosystem",
        result="success",
        details="System bootstrap completed",
    )
    print(f"Logged entry: {entry1.requestId}")

    entry2 = logger.log_action(
        action=AuditAction.VALIDATE,
        resource="governance-manifest",
        result=AuditResult.SUCCESS,
        details="GL compliance validated",
    )
    print(f"Logged entry: {entry2.requestId}")

    # End span
    logger.end_span()

    # Verify integrity
    is_valid = logger.verify_integrity(entry1)
    print(f"Entry integrity valid: {is_valid}")

    # Export to OpenTelemetry format
    otel_export = OpenTelemetryExporter.export_to_json([entry1, entry2])
    print(f"\nOpenTelemetry export:\n{otel_export}")

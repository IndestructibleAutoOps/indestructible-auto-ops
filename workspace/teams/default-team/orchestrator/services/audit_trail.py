#!/usr/bin/env python3
"""
Audit Trail Service for SuperAgent

Provides complete audit logging for all operations including:
- Message processing
- State transitions
- Consensus decisions
- Agent communications
"""

import asyncio
import hashlib
import json
import uuid
from collections import deque
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class AuditAction(str, Enum):
    """Types of auditable actions."""

    # Message Actions
    MESSAGE_RECEIVED = "message_received"
    MESSAGE_VALIDATED = "message_validated"
    MESSAGE_REJECTED = "message_rejected"
    MESSAGE_ROUTED = "message_routed"
    MESSAGE_PROCESSED = "message_processed"
    MESSAGE_SENT = "message_sent"

    # Incident Actions
    INCIDENT_CREATED = "incident_created"
    INCIDENT_UPDATED = "incident_updated"
    INCIDENT_TRANSITIONED = "incident_transitioned"
    INCIDENT_CLOSED = "incident_closed"

    # Consensus Actions
    CONSENSUS_REQUESTED = "consensus_requested"
    CONSENSUS_VOTE_RECEIVED = "consensus_vote_received"
    CONSENSUS_REACHED = "consensus_reached"
    CONSENSUS_FAILED = "consensus_failed"

    # Agent Actions
    AGENT_REGISTERED = "agent_registered"
    AGENT_DEREGISTERED = "agent_deregistered"
    AGENT_HEALTH_CHECK = "agent_health_check"
    AGENT_COMMUNICATION_FAILED = "agent_communication_failed"

    # System Actions
    SYSTEM_STARTUP = "system_startup"
    SYSTEM_SHUTDOWN = "system_shutdown"
    CONFIG_CHANGED = "config_changed"
    ERROR_OCCURRED = "error_occurred"


class AuditEntry(BaseModel):
    """Single audit log entry."""

    audit_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), description="Unique audit entry ID"
    )
    timestamp: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Entry timestamp",
    )
    action: AuditAction = Field(..., description="Type of action")
    actor: str = Field(..., description="Agent or user performing action")
    target: str | None = Field(default=None, description="Target of the action")
    trace_id: str | None = Field(default=None, description="Related trace ID")
    incident_id: str | None = Field(default=None, description="Related incident ID")
    message_type: str | None = Field(
        default=None, description="Related message type"
    )
    success: bool = Field(default=True, description="Whether action succeeded")
    details: dict[str, Any] = Field(default_factory=dict, description="Action details")
    previous_state: str | None = Field(
        default=None, description="State before action"
    )
    new_state: str | None = Field(default=None, description="State after action")
    error_message: str | None = Field(
        default=None, description="Error if action failed"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )
    checksum: str | None = Field(
        default=None, description="Entry integrity checksum"
    )

    def compute_checksum(self) -> str:
        """Compute SHA256 checksum of entry content."""
        content = json.dumps(
            {
                "audit_id": self.audit_id,
                "timestamp": self.timestamp,
                "action": self.action.value,
                "actor": self.actor,
                "target": self.target,
                "trace_id": self.trace_id,
                "incident_id": self.incident_id,
                "success": self.success,
                "details": self.details,
            },
            sort_keys=True,
        )
        return hashlib.sha256(content.encode()).hexdigest()

    def finalize(self) -> "AuditEntry":
        """Finalize entry with checksum."""
        self.checksum = self.compute_checksum()
        return self

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "audit_id": self.audit_id,
            "timestamp": self.timestamp,
            "action": self.action.value,
            "actor": self.actor,
            "target": self.target,
            "trace_id": self.trace_id,
            "incident_id": self.incident_id,
            "message_type": self.message_type,
            "success": self.success,
            "details": self.details,
            "previous_state": self.previous_state,
            "new_state": self.new_state,
            "error_message": self.error_message,
            "metadata": self.metadata,
            "checksum": self.checksum,
        }


class AuditTrail:
    """
    Audit trail manager for complete operation tracking.

    Provides:
    - Append-only audit log
    - Checksum verification for integrity
    - Query by various filters
    - Export capabilities
    """

    def __init__(
        self, max_entries: int = 100000, persistence_path: str | None = None
    ):
        self._entries: deque[AuditEntry] = deque(maxlen=max_entries)
        self._lock = asyncio.Lock()
        self._persistence_path = persistence_path
        self._entry_count = 0

    async def log(
        self,
        action: AuditAction,
        actor: str,
        target: str | None = None,
        trace_id: str | None = None,
        incident_id: str | None = None,
        message_type: str | None = None,
        success: bool = True,
        details: dict[str, Any] | None = None,
        previous_state: str | None = None,
        new_state: str | None = None,
        error_message: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> AuditEntry:
        """Log an audit entry."""
        entry = AuditEntry(
            action=action,
            actor=actor,
            target=target,
            trace_id=trace_id,
            incident_id=incident_id,
            message_type=message_type,
            success=success,
            details=details or {},
            previous_state=previous_state,
            new_state=new_state,
            error_message=error_message,
            metadata=metadata or {},
        ).finalize()

        async with self._lock:
            self._entries.append(entry)
            self._entry_count += 1

        return entry

    async def log_message_received(
        self,
        trace_id: str,
        source_agent: str,
        message_type: str,
        success: bool = True,
        details: dict[str, Any] | None = None,
    ) -> AuditEntry:
        """Log message reception."""
        return await self.log(
            action=AuditAction.MESSAGE_RECEIVED,
            actor=source_agent,
            target="super-agent",
            trace_id=trace_id,
            message_type=message_type,
            success=success,
            details=details,
        )

    async def log_incident_transition(
        self,
        incident_id: str,
        trace_id: str,
        actor: str,
        previous_state: str,
        new_state: str,
        trigger: str,
    ) -> AuditEntry:
        """Log incident state transition."""
        return await self.log(
            action=AuditAction.INCIDENT_TRANSITIONED,
            actor=actor,
            target=incident_id,
            trace_id=trace_id,
            incident_id=incident_id,
            previous_state=previous_state,
            new_state=new_state,
            details={"trigger": trigger},
        )

    async def log_consensus_result(
        self,
        consensus_id: str,
        trace_id: str,
        result: str,
        votes: dict[str, Any],
    ) -> AuditEntry:
        """Log consensus result."""
        return await self.log(
            action=(
                AuditAction.CONSENSUS_REACHED
                if result in ["approved", "rejected"]
                else AuditAction.CONSENSUS_FAILED
            ),
            actor="consensus-manager",
            target=consensus_id,
            trace_id=trace_id,
            success=result in ["approved", "rejected"],
            details={"result": result, "votes": votes},
        )

    async def log_error(
        self,
        trace_id: str | None,
        actor: str,
        error_message: str,
        details: dict[str, Any] | None = None,
    ) -> AuditEntry:
        """Log an error."""
        return await self.log(
            action=AuditAction.ERROR_OCCURRED,
            actor=actor,
            trace_id=trace_id,
            success=False,
            error_message=error_message,
            details=details,
        )

    async def get_entries(
        self,
        limit: int = 100,
        offset: int = 0,
        action: AuditAction | None = None,
        actor: str | None = None,
        trace_id: str | None = None,
        incident_id: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        success_only: bool | None = None,
    ) -> list[AuditEntry]:
        """Query audit entries with filters."""
        async with self._lock:
            filtered = list(self._entries)

        # Apply filters
        if action is not None:
            filtered = [e for e in filtered if e.action == action]
        if actor is not None:
            filtered = [e for e in filtered if e.actor == actor]
        if trace_id is not None:
            filtered = [e for e in filtered if e.trace_id == trace_id]
        if incident_id is not None:
            filtered = [e for e in filtered if e.incident_id == incident_id]
        if start_time is not None:
            filtered = [e for e in filtered if e.timestamp >= start_time]
        if end_time is not None:
            filtered = [e for e in filtered if e.timestamp <= end_time]
        if success_only is not None:
            filtered = [e for e in filtered if e.success == success_only]

        # Apply pagination
        return filtered[offset: offset + limit]

    async def get_incident_audit(self, incident_id: str) -> list[AuditEntry]:
        """Get all audit entries for an incident."""
        return await self.get_entries(incident_id=incident_id, limit=1000)

    async def get_trace_audit(self, trace_id: str) -> list[AuditEntry]:
        """Get all audit entries for a trace."""
        return await self.get_entries(trace_id=trace_id, limit=1000)

    async def verify_integrity(self) -> dict[str, Any]:
        """Verify integrity of all entries."""
        async with self._lock:
            entries = list(self._entries)

        valid_count = 0
        invalid_count = 0
        invalid_entries = []

        for entry in entries:
            expected_checksum = entry.compute_checksum()
            if entry.checksum == expected_checksum:
                valid_count += 1
            else:
                invalid_count += 1
                invalid_entries.append(entry.audit_id)

        return {
            "total_entries": len(entries),
            "valid_entries": valid_count,
            "invalid_entries": invalid_count,
            "integrity_percentage": (
                (valid_count / len(entries) * 100) if entries else 100
            ),
            "invalid_entry_ids": invalid_entries[:10],  # Only return first 10
        }

    async def get_statistics(self) -> dict[str, Any]:
        """Get audit trail statistics."""
        async with self._lock:
            entries = list(self._entries)

        if not entries:
            return {"total_entries": 0, "actions": {}}

        action_counts: dict[str, int] = {}
        success_count = 0
        failure_count = 0

        for entry in entries:
            action_counts[entry.action.value] = (
                action_counts.get(entry.action.value, 0) + 1
            )
            if entry.success:
                success_count += 1
            else:
                failure_count += 1

        return {
            "total_entries": len(entries),
            "success_count": success_count,
            "failure_count": failure_count,
            "success_rate": success_count / len(entries) * 100,
            "actions": action_counts,
            "oldest_entry": entries[0].timestamp if entries else None,
            "newest_entry": entries[-1].timestamp if entries else None,
        }

    async def export_json(self, entries: list[AuditEntry] | None = None) -> str:
        """Export entries to JSON."""
        if entries is None:
            async with self._lock:
                entries = list(self._entries)

        return json.dumps([e.to_dict() for e in entries], indent=2)

    def __len__(self) -> int:
        """Return number of entries."""
        return len(self._entries)

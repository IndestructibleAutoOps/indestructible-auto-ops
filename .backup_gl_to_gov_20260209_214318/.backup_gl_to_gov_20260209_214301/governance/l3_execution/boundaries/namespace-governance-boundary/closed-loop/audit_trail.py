#!/usr/bin/env python3
"""
NG 閉環審計追蹤
Cryptographic Audit Trail

所有閉環操作形成不可變審計鏈：
- 每個事件密碼學簽名
- 事件鏈具備防篡改能力
- 完整的 Provenance（來源追溯）
- 支援合規查詢（by time, actor, event type）
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha3_256(data: bytes) -> str:
    return hashlib.sha3_256(data).hexdigest()


def _canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


class AuditEventType(Enum):
    """審計事件類型"""
    CYCLE_STARTED = "cycle_started"
    STATE_LOCKED = "state_locked"
    VERIFICATION_COMPLETED = "verification_completed"
    DECISION_MADE = "decision_made"
    COST_RECORDED = "cost_recorded"
    ADJUSTMENT_APPLIED = "adjustment_applied"
    CYCLE_COMPLETED = "cycle_completed"
    CYCLE_TERMINATED = "cycle_terminated"
    ERROR_OCCURRED = "error_occurred"
    OVERRIDE_APPLIED = "override_applied"
    CHAIN_VALIDATED = "chain_validated"


class AuditSeverity(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class AuditEvent:
    """不可變審計事件"""
    event_id: int
    event_type: AuditEventType
    severity: AuditSeverity
    cycle_id: str
    actor: str
    timestamp: str
    payload: Dict[str, Any]
    event_hash: str = ""
    previous_hash: str = ""

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["event_type"] = self.event_type.value
        d["severity"] = self.severity.value
        return d


class AuditTrail:
    """
    不可變審計追蹤

    事件形成密碼學鏈：
      Event_0 -> Event_1 -> Event_2 -> ...
    """

    def __init__(self, storage_path: Optional[Path] = None, actor: str = "system"):
        self._events: List[AuditEvent] = []
        self._storage_path = storage_path
        self._default_actor = actor

    @property
    def length(self) -> int:
        return len(self._events)

    def record(
        self,
        event_type: AuditEventType,
        cycle_id: str,
        payload: Dict[str, Any],
        severity: AuditSeverity = AuditSeverity.INFO,
        actor: Optional[str] = None,
    ) -> AuditEvent:
        """
        記錄一個審計事件。

        Returns:
            不可變的 AuditEvent（已計算 hash）
        """
        event_id = len(self._events)
        previous_hash = self._events[-1].event_hash if self._events else ""
        timestamp = _utc_now()

        hashable = {
            "event_id": event_id,
            "event_type": event_type.value,
            "severity": severity.value,
            "cycle_id": cycle_id,
            "actor": actor or self._default_actor,
            "timestamp": timestamp,
            "payload": payload,
            "previous_hash": previous_hash,
        }
        event_hash = _sha3_256(_canonical(hashable))

        event = AuditEvent(
            event_id=event_id,
            event_type=event_type,
            severity=severity,
            cycle_id=cycle_id,
            actor=actor or self._default_actor,
            timestamp=timestamp,
            payload=payload,
            event_hash=event_hash,
            previous_hash=previous_hash,
        )

        self._events.append(event)
        self._persist()
        return event

    def verify_integrity(self) -> Dict[str, Any]:
        """驗證審計鏈完整性"""
        errors: List[str] = []

        for i, event in enumerate(self._events):
            if event.event_id != i:
                errors.append(f"Event {i}: event_id mismatch")

            if i == 0:
                if event.previous_hash != "":
                    errors.append("Event 0: previous_hash should be empty")
            else:
                if event.previous_hash != self._events[i - 1].event_hash:
                    errors.append(f"Event {i}: chain broken (previous_hash mismatch)")

            hashable = {
                "event_id": event.event_id,
                "event_type": event.event_type.value,
                "severity": event.severity.value,
                "cycle_id": event.cycle_id,
                "actor": event.actor,
                "timestamp": event.timestamp,
                "payload": event.payload,
                "previous_hash": event.previous_hash,
            }
            recomputed = _sha3_256(_canonical(hashable))
            if recomputed != event.event_hash:
                errors.append(f"Event {i}: hash tampered")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "total_events": len(self._events),
        }

    def query_by_cycle(self, cycle_id: str) -> List[Dict[str, Any]]:
        return [e.to_dict() for e in self._events if e.cycle_id == cycle_id]

    def query_by_type(self, event_type: AuditEventType) -> List[Dict[str, Any]]:
        return [e.to_dict() for e in self._events if e.event_type == event_type]

    def query_by_severity(self, min_severity: AuditSeverity) -> List[Dict[str, Any]]:
        severity_order = [AuditSeverity.DEBUG, AuditSeverity.INFO, AuditSeverity.WARNING,
                          AuditSeverity.ERROR, AuditSeverity.CRITICAL]
        min_idx = severity_order.index(min_severity)
        return [e.to_dict() for e in self._events
                if severity_order.index(e.severity) >= min_idx]

    def export_all(self) -> List[Dict[str, Any]]:
        return [e.to_dict() for e in self._events]

    def _persist(self) -> None:
        if self._storage_path is not None:
            self._storage_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self._storage_path, "w", encoding="utf-8") as f:
                json.dump(self.export_all(), f, indent=2, ensure_ascii=False)

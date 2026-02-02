#!/usr/bin/env python3

"""
GL Event Emitter
================
Event emission and handling infrastructure for governance operations.

Features:
- Event emission for governance operations
- Event subscription and handling
- Event queuing and persistence
- Event filtering and routing
"""

import json
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
import sqlite3
from queue import Queue, Empty


class EventType(Enum):
    """Governance event types."""
    VALIDATION_START = "validation_start"
    VALIDATION_COMPLETE = "validation_complete"
    VALIDATION_FAILED = "validation_failed"
    QUALITY_GATE_FAILED = "quality_gate_failed"
    REMEDIATION_SUGGESTED = "remediation_suggested"
    EVIDENCE_COLLECTED = "evidence_collected"
    AUDIT_LOGGED = "audit_logged"
    CONTRACT_LOADED = "contract_loaded"
    POLICY_ENFORCED = "policy_enforced"


@dataclass
class GovernanceEvent:
    """
    Governance event structure.
    
    Attributes:
        event_type: Type of event
        timestamp: ISO 8601 timestamp
        operation_id: Unique operation identifier
        metadata: Additional event metadata
        data: Event-specific data
        priority: Event priority (1=highest, 10=lowest)
    """
    event_type: EventType
    timestamp: str
    operation_id: str
    metadata: Dict[str, Any]
    data: Dict[str, Any]
    priority: int = 5
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary."""
        return {
            "event_type": self.event_type.value,
            "timestamp": self.timestamp,
            "operation_id": self.operation_id,
            "metadata": self.metadata,
            "data": self.data,
            "priority": self.priority
        }
    
    def to_json(self) -> str:
        """Convert event to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


class EventHandler:
    """
    Base event handler class.
    
    Subclasses should implement the handle() method to process events.
    """
    
    def __init__(self, name: str, event_types: List[EventType]):
        """
        Initialize event handler.
        
        Args:
            name: Handler name
            event_types: Event types this handler subscribes to
        """
        self.name = name
        self.event_types = event_types
    
    def can_handle(self, event: GovernanceEvent) -> bool:
        """
        Check if handler can handle this event.
        
        Args:
            event: Event to check
        
        Returns:
            True if handler can handle event
        """
        return event.event_type in self.event_types
    
    def handle(self, event: GovernanceEvent):
        """
        Handle the event.
        
        Args:
            event: Event to handle
        """
        raise NotImplementedError("Subclasses must implement handle()")


class LoggingEventHandler(EventHandler):
    """Event handler that logs events."""
    
    def __init__(self, log_file: str = None):
        """
        Initialize logging handler.
        
        Args:
            log_file: Path to log file (optional)
        """
        super().__init__("LoggingEventHandler", list(EventType))
        self.log_file = Path(log_file) if log_file else None
    
    def handle(self, event: GovernanceEvent):
        """Log event to file or console."""
        message = f"[{event.timestamp}] {event.event_type.value} - {event.operation_id}"
        
        if self.log_file:
            with open(self.log_file, 'a') as f:
                f.write(f"{message}\n{event.to_json()}\n\n")
        else:
            print(message)


class AuditEventHandler(EventHandler):
    """Event handler that records events to audit trail."""
    
    def __init__(self, db_path: str):
        """
        Initialize audit event handler.
        
        Args:
            db_path: Path to audit trail database
        """
        super().__init__("AuditEventHandler", list(EventType))
        self.db_path = Path(db_path)
        self._init_events_table()
    
    def _init_events_table(self):
        """Initialize events table in audit database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS governance_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                event_type TEXT NOT NULL,
                operation_id TEXT NOT NULL,
                metadata TEXT,
                data TEXT,
                priority INTEGER
            )
        ''')
        
        # Create indexes for common queries
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_timestamp ON governance_events(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_type ON governance_events(event_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_operation ON governance_events(operation_id)')
        
        conn.commit()
        conn.close()
    
    def handle(self, event: GovernanceEvent):
        """Record event to audit database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO governance_events
            (timestamp, event_type, operation_id, metadata, data, priority)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            event.timestamp,
            event.event_type.value,
            event.operation_id,
            json.dumps(event.metadata),
            json.dumps(event.data),
            event.priority
        ))
        
        conn.commit()
        conn.close()


class EventEmitter:
    """
    Event emission and handling infrastructure.
    
    Manages event emission, subscription, and delivery to handlers.
    """
    
    def __init__(self, db_path: str = None, base_path: str = "/workspace/machine-native-ops"):
        """
        Initialize event emitter.
        
        Args:
            db_path: Path to audit trail database
            base_path: Base path for default database location
        """
        self.base_path = Path(base_path)
        
        if db_path:
            self.db_path = Path(db_path)
        else:
            self.db_path = self.base_path / "ecosystem" / "logs" / "audit-logs" / "audit_trail.db"
        
        self.handlers: List[EventHandler] = []
        self.event_queue = Queue()
        self.running = False
        self.worker_thread = None
        
        # Add default handlers
        self.add_handler(AuditEventHandler(self.db_path))
    
    def add_handler(self, handler: EventHandler):
        """
        Add event handler.
        
        Args:
            handler: Handler to add
        """
        self.handlers.append(handler)
    
    def remove_handler(self, handler: EventHandler):
        """
        Remove event handler.
        
        Args:
            handler: Handler to remove
        """
        if handler in self.handlers:
            self.handlers.remove(handler)
    
    def emit(self, event: GovernanceEvent):
        """
        Emit event to all subscribed handlers.
        
        Args:
            event: Event to emit
        """
        # Add to queue for async processing
        self.event_queue.put(event)
        
        # Start worker thread if not running
        if not self.running:
            self.start()
    
    def emit_sync(self, event: GovernanceEvent):
        """
        Emit event synchronously.
        
        Args:
            event: Event to emit
        """
        self._process_event(event)
    
    def _process_event(self, event: GovernanceEvent):
        """
        Process event through all handlers.
        
        Args:
            event: Event to process
        """
        for handler in self.handlers:
            if handler.can_handle(event):
                try:
                    handler.handle(event)
                except Exception as e:
                    print(f"⚠️  Error in handler {handler.name}: {e}")
    
    def start(self):
        """Start event processing worker thread."""
        if self.running:
            return
        
        self.running = True
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()
    
    def stop(self):
        """Stop event processing worker thread."""
        self.running = False
        
        if self.worker_thread:
            self.worker_thread.join(timeout=5)
            self.worker_thread = None
    
    def _worker_loop(self):
        """Worker thread loop for processing events."""
        while self.running:
            try:
                event = self.event_queue.get(timeout=1)
                self._process_event(event)
                self.event_queue.task_done()
            except Empty:
                continue
            except Exception as e:
                print(f"⚠️  Error processing event: {e}")
    
    def create_event(self,
                    event_type: EventType,
                    operation_id: str,
                    metadata: Dict[str, Any] = None,
                    data: Dict[str, Any] = None,
                    priority: int = 5) -> GovernanceEvent:
        """
        Create a governance event.
        
        Args:
            event_type: Type of event
            operation_id: Unique operation identifier
            metadata: Event metadata
            data: Event data
            priority: Event priority
        
        Returns:
            GovernanceEvent instance
        """
        return GovernanceEvent(
            event_type=event_type,
            timestamp=datetime.utcnow().isoformat(),
            operation_id=operation_id,
            metadata=metadata or {},
            data=data or {},
            priority=priority
        )
    
    def get_event_count(self,
                       event_type: EventType = None,
                       operation_id: str = None,
                       start_date: str = None,
                       end_date: str = None) -> int:
        """
        Get count of events matching criteria.
        
        Args:
            event_type: Filter by event type
            operation_id: Filter by operation ID
            start_date: Filter events after this date
            end_date: Filter events before this date
        
        Returns:
            Count of matching events
        """
        query = "SELECT COUNT(*) FROM governance_events WHERE 1=1"
        params = []
        
        if event_type:
            query += " AND event_type = ?"
            params.append(event_type.value)
        
        if operation_id:
            query += " AND operation_id = ?"
            params.append(operation_id)
        
        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(query, params)
        count = cursor.fetchone()[0]
        
        conn.close()
        
        return count
    
    def get_recent_events(self, limit: int = 10) -> List[Dict]:
        """
        Get recent events.
        
        Args:
            limit: Maximum number of events to return
        
        Returns:
            List of event dictionaries
        """
        query = """
            SELECT * FROM governance_events 
            ORDER BY timestamp DESC 
            LIMIT ?
        """
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(query, (limit,))
        rows = cursor.fetchall()
        
        events = []
        for row in rows:
            event = dict(row)
            event["metadata"] = json.loads(event["metadata"])
            event["data"] = json.loads(event["data"])
            events.append(event)
        
        conn.close()
        
        return events


# Global event emitter instance
_global_emitter = None


def get_global_emitter(db_path: str = None, base_path: str = "/workspace/machine-native-ops") -> EventEmitter:
    """
    Get global event emitter instance.
    
    Args:
        db_path: Path to audit trail database
        base_path: Base path for default database location
    
    Returns:
        Global EventEmitter instance
    """
    global _global_emitter
    
    if _global_emitter is None:
        _global_emitter = EventEmitter(db_path, base_path)
    
    return _global_emitter


def emit_event(event_type: EventType,
               operation_id: str,
               metadata: Dict[str, Any] = None,
               data: Dict[str, Any] = None,
               priority: int = 5):
    """
    Convenience function to emit event using global emitter.
    
    Args:
        event_type: Type of event
        operation_id: Unique operation identifier
        metadata: Event metadata
        data: Event data
        priority: Event priority
    """
    emitter = get_global_emitter()
    event = emitter.create_event(event_type, operation_id, metadata, data, priority)
    emitter.emit(event)
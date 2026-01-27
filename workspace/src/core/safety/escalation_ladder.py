"""
Escalation Ladder System (升級階梯系統)

Progressive escalation system for handling incidents based on severity.

Reference: Escalation ladders are part of the trust scaffolding [1]
"""

import asyncio
import contextlib
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class EscalationLevel(Enum):
    """Escalation levels from least to most severe"""

    LEVEL_0_NORMAL = 0  # Normal operation
    LEVEL_1_WARNING = 1  # Warning - increased monitoring
    LEVEL_2_ALERT = 2  # Alert - notify team
    LEVEL_3_CRITICAL = 3  # Critical - immediate action required
    LEVEL_4_EMERGENCY = 4  # Emergency - stop all operations
    LEVEL_5_DISASTER = 5  # Disaster - full system shutdown


@dataclass
class EscalationAction:
    """Action to take at each escalation level"""

    level: EscalationLevel
    name: str
    description: str
    handler: Callable[..., Any] | None = None
    # Seconds before auto-escalating
    auto_escalate_after: float | None = None
    requires_acknowledgment: bool = False
    notification_channels: list[str] = field(default_factory=list)


@dataclass
class EscalationConfig:
    """Configuration for escalation ladder"""

    name: str = "default"
    initial_level: EscalationLevel = EscalationLevel.LEVEL_0_NORMAL
    auto_de_escalate: bool = True
    de_escalate_after: float = 300.0  # Seconds of stability before de-escalating
    max_escalation_rate: int = 3  # Max escalations per minute


@dataclass
class EscalationEvent:
    """Record of an escalation event"""

    timestamp: datetime
    from_level: EscalationLevel
    to_level: EscalationLevel
    reason: str
    triggered_by: str
    acknowledged: bool = False
    acknowledged_by: str | None = None
    acknowledged_at: datetime | None = None


class EscalationLadder:
    """
    Progressive Escalation System

    Handles incidents through progressively more severe responses,
    from warnings to full system shutdown.

    Example:
        ladder = EscalationLadder(EscalationConfig(name="production"))
        ladder.register_action(EscalationAction(
            level=EscalationLevel.LEVEL_2_ALERT,
            name="notify_team",
            description="Send alert to on-call team"
        ))
        await ladder.escalate("High error rate detected", "monitoring_system")
    """

    def __init__(self, config: EscalationConfig | None = None):
        self.config = config or EscalationConfig()
        self._current_level = self.config.initial_level
        self._actions: dict[EscalationLevel, list[EscalationAction]] = {
            level: [] for level in EscalationLevel
        }
        self._history: list[EscalationEvent] = []
        self._listeners: list[Callable[[EscalationEvent], None]] = []
        self._last_escalation_times: list[float] = []
        self._stable_since: float | None = None
        self._pending_acknowledgments: list[EscalationEvent] = []

        # Register default actions
        self._register_default_actions()

    def _register_default_actions(self) -> None:
        """Register default actions for each level"""
        defaults = [
            EscalationAction(
                level=EscalationLevel.LEVEL_1_WARNING,
                name="increase_monitoring",
                description="Increase monitoring frequency and logging",
                notification_channels=["logs"],
            ),
            EscalationAction(
                level=EscalationLevel.LEVEL_2_ALERT,
                name="notify_team",
                description="Send alert to engineering team",
                notification_channels=["slack", "email"],
            ),
            EscalationAction(
                level=EscalationLevel.LEVEL_3_CRITICAL,
                name="page_oncall",
                description="Page on-call engineer",
                requires_acknowledgment=True,
                auto_escalate_after=300.0,  # 5 minutes
                notification_channels=["pagerduty", "phone"],
            ),
            EscalationAction(
                level=EscalationLevel.LEVEL_4_EMERGENCY,
                name="stop_non_critical",
                description="Stop all non-critical operations",
                requires_acknowledgment=True,
                notification_channels=["all"],
            ),
            EscalationAction(
                level=EscalationLevel.LEVEL_5_DISASTER,
                name="full_shutdown",
                description="Full system shutdown",
                requires_acknowledgment=True,
                notification_channels=["all", "executive"],
            ),
        ]

        for action in defaults:
            self._actions[action.level].append(action)

    @property
    def current_level(self) -> EscalationLevel:
        """Get current escalation level"""
        return self._current_level

    @property
    def history(self) -> list[EscalationEvent]:
        """Get escalation history"""
        return self._history.copy()

    @property
    def pending_acknowledgments(self) -> list[EscalationEvent]:
        """Get events pending acknowledgment"""
        return self._pending_acknowledgments.copy()

    def register_action(self, action: EscalationAction) -> None:
        """Register an action for a specific escalation level"""
        self._actions[action.level].append(action)

    def add_listener(self, listener: Callable[[EscalationEvent], None]) -> None:
        """Add listener for escalation events"""
        self._listeners.append(listener)

    def _notify_listeners(self, event: EscalationEvent) -> None:
        """Notify all listeners of an escalation event"""
        for listener in self._listeners:
            with contextlib.suppress(Exception):
                listener(event)

    def _can_escalate(self) -> bool:
        """Check if escalation is allowed (rate limiting)"""
        import time

        current_time = time.time()

        # Remove old escalation times
        self._last_escalation_times = [
            t for t in self._last_escalation_times if current_time - t < 60
        ]

        return len(self._last_escalation_times) < self.config.max_escalation_rate

    async def escalate(
        self, reason: str, triggered_by: str, levels: int = 1
    ) -> EscalationEvent:
        """
        Escalate to a higher level

        Args:
            reason: Reason for escalation
            triggered_by: What/who triggered the escalation
            levels: Number of levels to escalate (default 1)

        Returns:
            EscalationEvent record
        """
        import time

        if not self._can_escalate():
            raise EscalationRateLimitError(
                f"Escalation rate limit exceeded ({self.config.max_escalation_rate}/min)"
            )

        old_level = self._current_level
        new_level_value = min(
            old_level.value + levels, EscalationLevel.LEVEL_5_DISASTER.value
        )
        new_level = EscalationLevel(new_level_value)

        if new_level == old_level:
            # Already at max level
            return self._history[-1] if self._history else None

        # Create event
        event = EscalationEvent(
            timestamp=datetime.now(),
            from_level=old_level,
            to_level=new_level,
            reason=reason,
            triggered_by=triggered_by,
        )

        # Update state
        self._current_level = new_level
        self._history.append(event)
        self._last_escalation_times.append(time.time())
        self._stable_since = None

        # Execute actions
        await self._execute_level_actions(new_level, reason)

        # Check if acknowledgment required
        for action in self._actions[new_level]:
            if action.requires_acknowledgment:
                self._pending_acknowledgments.append(event)
                break

        # Notify listeners
        self._notify_listeners(event)

        return event

    async def de_escalate(
        self, reason: str, triggered_by: str, levels: int = 1
    ) -> EscalationEvent:
        """
        De-escalate to a lower level

        Args:
            reason: Reason for de-escalation
            triggered_by: What/who triggered the de-escalation
            levels: Number of levels to de-escalate (default 1)

        Returns:
            EscalationEvent record
        """
        old_level = self._current_level
        new_level_value = max(
            old_level.value - levels, EscalationLevel.LEVEL_0_NORMAL.value
        )
        new_level = EscalationLevel(new_level_value)

        if new_level == old_level:
            return self._history[-1] if self._history else None

        # Create event
        event = EscalationEvent(
            timestamp=datetime.now(),
            from_level=old_level,
            to_level=new_level,
            reason=reason,
            triggered_by=triggered_by,
        )

        # Update state
        self._current_level = new_level
        self._history.append(event)

        # Notify listeners
        self._notify_listeners(event)

        return event

    async def set_level(
        self, level: EscalationLevel, reason: str, triggered_by: str
    ) -> EscalationEvent:
        """
        Set escalation to a specific level

        Args:
            level: Target escalation level
            reason: Reason for setting level
            triggered_by: What/who set the level

        Returns:
            EscalationEvent record
        """
        old_level = self._current_level

        if level == old_level:
            return self._history[-1] if self._history else None

        event = EscalationEvent(
            timestamp=datetime.now(),
            from_level=old_level,
            to_level=level,
            reason=reason,
            triggered_by=triggered_by,
        )

        self._current_level = level
        self._history.append(event)

        if level.value > old_level.value:
            await self._execute_level_actions(level, reason)

        self._notify_listeners(event)

        return event

    async def acknowledge(
        self, event_timestamp: datetime, acknowledged_by: str
    ) -> bool:
        """
        Acknowledge an escalation event

        Args:
            event_timestamp: Timestamp of event to acknowledge
            acknowledged_by: Who is acknowledging

        Returns:
            True if acknowledged, False if not found
        """
        for event in self._pending_acknowledgments:
            if event.timestamp == event_timestamp:
                event.acknowledged = True
                event.acknowledged_by = acknowledged_by
                event.acknowledged_at = datetime.now()
                self._pending_acknowledgments.remove(event)
                return True
        return False

    async def _execute_level_actions(self, level: EscalationLevel, reason: str) -> None:
        """Execute all actions for a level"""
        for action in self._actions[level]:
            if action.handler:
                try:
                    if asyncio.iscoroutinefunction(action.handler):
                        await action.handler(level, reason)
                    else:
                        action.handler(level, reason)
                except Exception:
                    pass  # Don't let action failures stop escalation

    def reset(self) -> None:
        """Reset to initial level"""
        self._current_level = self.config.initial_level
        self._pending_acknowledgments.clear()
        import time

        self._stable_since = time.time()

    def get_status(self) -> dict[str, Any]:
        """Get current escalation status"""
        return {
            "name": self.config.name,
            "current_level": self._current_level.name,
            "current_level_value": self._current_level.value,
            "pending_acknowledgments": len(self._pending_acknowledgments),
            "history_count": len(self._history),
            "recent_events": [
                {
                    "timestamp": e.timestamp.isoformat(),
                    "from": e.from_level.name,
                    "to": e.to_level.name,
                    "reason": e.reason,
                }
                for e in self._history[-5:]
            ],
        }


class EscalationRateLimitError(Exception):
    """Raised when escalation rate limit is exceeded"""

    pass

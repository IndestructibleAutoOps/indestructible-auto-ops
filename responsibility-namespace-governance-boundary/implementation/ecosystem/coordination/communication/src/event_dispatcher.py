#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: coordination
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
GL Event Dispatcher
===================
事件分發器 - 事件路由和處理

GL Governance Layer: GL10-29 (Operational Layer)
"""

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
import threading
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from collections import defaultdict
import logging

from message_bus import Message, MessageBus


@dataclass
class EventHandler:
    """事件處理器"""

    id: str
    event_type: str
    handler: Callable[[Message], None]
    priority: int = 0  # 優先級（數字越大越高）


class EventDispatcher:
    """事件分發器"""

    def __init__(
        self, message_bus: MessageBus, config: Optional[Dict[str, Any]] = None
    ):
        """
        初始化事件分發器

        Args:
            message_bus: 消息總線
            config: 配置字典
        """
        self.message_bus = message_bus
        self.config = config or {}
        self.logger = self._setup_logger()

        # 事件處理器: {event_type: [EventHandler]}
        self._handlers: Dict[str, List[EventHandler]] = defaultdict(list)

        # 統計
        self._events_processed = 0
        self._events_failed = 0

        # 鎖
        self._lock = threading.RLock()

        self.logger.info("Event Dispatcher initialized")

    def _setup_logger(self) -> logging.Logger:
        """設置日誌"""
        logger = logging.getLogger("EventDispatcher")
        level = (
            self.config.get("monitoring", {}).get("logging", {}).get("level", "INFO")
        )
        logger.setLevel(getattr(logging, level))

        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger

    def register_handler(
        self, event_type: str, handler: Callable[[Message], None], priority: int = 0
    ) -> str:
        """
        註冊事件處理器

        Args:
            event_type: 事件類型
            handler: 處理函數
            priority: 優先級

        Returns:
            處理器ID
        """
        with self._lock:
            import uuid

            handler_id = str(uuid.uuid4())

            event_handler = EventHandler(
                id=handler_id, event_type=event_type, handler=handler, priority=priority
            )

            self._handlers[event_type].append(event_handler)

            # 按優先級排序
            self._handlers[event_type].sort(key=lambda h: h.priority, reverse=True)

            self.logger.info(
                f"Event handler registered: {handler_id} for {event_type} "
                f"(priority: {priority})"
            )

            return handler_id

    def unregister_handler(self, handler_id: str) -> bool:
        """
        取消註冊處理器

        Args:
            handler_id: 處理器ID

        Returns:
            成功返回True
        """
        with self._lock:
            for event_type, handlers in self._handlers.items():
                for handler in handlers:
                    if handler.id == handler_id:
                        handlers.remove(handler)
                        self.logger.info(f"Event handler unregistered: {handler_id}")
                        return True

            self.logger.warning(f"Event handler not found: {handler_id}")
            return False

    def dispatch_event(
        self,
        topic: str,
        event_type: str,
        payload: Dict[str, Any],
        source: Optional[str] = None,
    ) -> str:
        """
        分發事件

        Args:
            topic: 主題
            event_type: 事件類型
            payload: 事件數據
            source: 事件來源

        Returns:
            消息ID
        """
        # 通過消息總線發布
        message_id = self.message_bus.publish(
            topic=topic, event_type=event_type, payload=payload, source=source
        )

        self.logger.debug(f"Event dispatched: {event_type} to topic {topic}")
        return message_id

    def process_event(self, message: Message):
        """
        處理事件

        Args:
            message: 消息
        """
        with self._lock:
            handlers = self._handlers.get(message.event_type, [])

            if not handlers:
                self.logger.debug(f"No handlers for event type {message.event_type}")
                return

            for handler in handlers:
                try:
                    handler.handler(message)
                    self._events_processed += 1
                except Exception as e:
                    self._events_failed += 1
                    self.logger.error(
                        f"Error in event handler {handler.id} "
                        f"for event {message.event_type}: {e}"
                    )

    def subscribe_to_events(
        self, topic: str, event_types: Optional[List[str]] = None
    ) -> str:
        """
        訂閱事件

        Args:
            topic: 主題
            event_types: 事件類型列表（None表示所有）

        Returns:
            訂閱ID
        """

        def event_filter(message: Message) -> bool:
            if event_types is None:
                return True
            return message.event_type in event_types

        return self.message_bus.subscribe(
            topic=topic,
            handler=self.process_event,
            filter_func=event_filter if event_types else None,
        )

    def get_stats(self) -> Dict[str, Any]:
        """獲取統計信息"""
        with self._lock:
            return {
                "events_processed": self._events_processed,
                "events_failed": self._events_failed,
                "event_types": len(self._handlers),
                "total_handlers": sum(
                    len(handlers) for handlers in self._handlers.values()
                ),
            }

    def list_event_types(self) -> List[str]:
        """列出所有事件類型"""
        with self._lock:
            return list(self._handlers.keys())

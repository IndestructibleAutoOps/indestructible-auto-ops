"""事件觸發系統"""

import logging
from typing import Callable, Dict, List

logger = logging.getLogger(__name__)


class EventBus:
    """事件總線"""

    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}

    def on(self, event_name: str, handler: Callable):
        """註冊事件監聽器"""
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(handler)
        logger.info(f"✅ 事件註冊：{event_name} → {handler}")

    def emit(self, event_name: str, *args, **kwargs):
        """觸發事件"""
        if event_name not in self.listeners:
            logger.warning(f"⚠️  無人監聽事件：{event_name}")
            return

        logger.info(f"🔔 觸發事件：{event_name}")
        for handler in self.listeners[event_name]:
            try:
                handler(*args, **kwargs)
            except Exception as e:
                logger.error(f"❌ 事件處理失敗 {event_name}: {e}")

    def off(self, event_name: str, handler: Callable = None):
        """取消註冊事件監聽器"""
        if event_name not in self.listeners:
            return

        if handler is None:
            # 移除所有監聽器
            del self.listeners[event_name]
            logger.info(f"🗑️  移除所有監聽器：{event_name}")
        else:
            # 移除特定監聽器
            self.listeners[event_name].remove(handler)
            logger.info(f"🗑️  移除監聽器：{event_name} → {handler}")


# 全域實例
event_bus = EventBus()

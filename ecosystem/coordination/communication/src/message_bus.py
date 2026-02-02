#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: coordination
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
GL Message Bus
==============
消息總線 - 跨平台消息傳遞

GL Governance Layer: GL10-29 (Operational Layer)
"""

import threading
import time
import uuid
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from queue import Queue, Empty
from collections import defaultdict
import logging


@dataclass
class Message:
    """消息"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    topic: str = ""
    event_type: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    source: str = ""
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Subscription:
    """訂閱"""
    id: str
    topic: str
    handler: Callable[[Message], None]
    filter_func: Optional[Callable[[Message], bool]] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class MessageBus:
    """消息總線"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化消息總線
        
        Args:
            config: 配置字典
        """
        self.config = config or {}
        self.logger = self._setup_logger()
        
        # 訂閱者: {topic: [Subscription]}
        self._subscriptions: Dict[str, List[Subscription]] = defaultdict(list)
        
        # 消息隊列
        self.max_queue_size = self.config.get('message_bus', {}).get('max_queue_size', 10000)
        self._message_queue: Queue = Queue(maxsize=self.max_queue_size)
        
        # 統計
        self._published_count = 0
        self._delivered_count = 0
        self._failed_count = 0
        
        # 工作線程
        self._worker_thread: Optional[threading.Thread] = None
        self._running = False
        
        # 鎖
        self._lock = threading.RLock()
        
        self.logger.info("Message Bus initialized")
    
    def _setup_logger(self) -> logging.Logger:
        """設置日誌"""
        logger = logging.getLogger('MessageBus')
        level = self.config.get('monitoring', {}).get('logging', {}).get('level', 'INFO')
        logger.setLevel(getattr(logging, level))
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def start(self):
        """啟動消息總線"""
        if self._running:
            self.logger.warning("Message bus already running")
            return
        
        self._running = True
        self._worker_thread = threading.Thread(
            target=self._worker_loop,
            daemon=True
        )
        self._worker_thread.start()
        self.logger.info("Message bus started")
    
    def stop(self):
        """停止消息總線"""
        if not self._running:
            return
        
        self._running = False
        if self._worker_thread:
            self._worker_thread.join(timeout=5)
        self.logger.info("Message bus stopped")
    
    def publish(
        self,
        topic: str,
        event_type: str,
        payload: Dict[str, Any],
        source: Optional[str] = None
    ) -> str:
        """
        發布消息
        
        Args:
            topic: 主題
            event_type: 事件類型
            payload: 消息負載
            source: 消息來源
            
        Returns:
            消息ID
        """
        message = Message(
            topic=topic,
            event_type=event_type,
            payload=payload,
            source=source or "unknown"
        )
        
        try:
            self._message_queue.put(message, block=False)
            self._published_count += 1
            self.logger.debug(f"Message published: {message.id} to topic {topic}")
            return message.id
        except Exception as e:
            self.logger.error(f"Failed to publish message: {e}")
            return ""
    
    def subscribe(
        self,
        topic: str,
        handler: Callable[[Message], None],
        filter_func: Optional[Callable[[Message], bool]] = None
    ) -> str:
        """
        訂閱主題
        
        Args:
            topic: 主題
            handler: 消息處理函數
            filter_func: 過濾函數（可選）
            
        Returns:
            訂閱ID
        """
        with self._lock:
            subscription = Subscription(
                id=str(uuid.uuid4()),
                topic=topic,
                handler=handler,
                filter_func=filter_func
            )
            
            self._subscriptions[topic].append(subscription)
            self.logger.info(f"Subscription created: {subscription.id} for topic {topic}")
            
            return subscription.id
    
    def unsubscribe(self, subscription_id: str) -> bool:
        """
        取消訂閱
        
        Args:
            subscription_id: 訂閱ID
            
        Returns:
            成功返回True
        """
        with self._lock:
            for topic, subscriptions in self._subscriptions.items():
                for sub in subscriptions:
                    if sub.id == subscription_id:
                        subscriptions.remove(sub)
                        self.logger.info(f"Subscription cancelled: {subscription_id}")
                        return True
            
            self.logger.warning(f"Subscription not found: {subscription_id}")
            return False
    
    def _worker_loop(self):
        """工作循環 - 處理消息隊列"""
        while self._running:
            try:
                # 從隊列獲取消息
                message = self._message_queue.get(timeout=1)
                
                # 分發消息
                self._deliver_message(message)
                
            except Empty:
                continue
            except Exception as e:
                self.logger.error(f"Error in worker loop: {e}")
                time.sleep(1)
    
    def _deliver_message(self, message: Message):
        """
        分發消息給訂閱者
        
        Args:
            message: 消息
        """
        with self._lock:
            subscriptions = self._subscriptions.get(message.topic, [])
            
            if not subscriptions:
                self.logger.debug(f"No subscribers for topic {message.topic}")
                return
            
            for subscription in subscriptions:
                try:
                    # 應用過濾器
                    if subscription.filter_func:
                        if not subscription.filter_func(message):
                            continue
                    
                    # 調用處理器
                    subscription.handler(message)
                    self._delivered_count += 1
                    
                except Exception as e:
                    self._failed_count += 1
                    self.logger.error(
                        f"Error delivering message {message.id} "
                        f"to subscription {subscription.id}: {e}"
                    )
    
    def get_stats(self) -> Dict[str, Any]:
        """
        獲取統計信息
        
        Returns:
            統計信息字典
        """
        with self._lock:
            return {
                'published': self._published_count,
                'delivered': self._delivered_count,
                'failed': self._failed_count,
                'queue_size': self._message_queue.qsize(),
                'topics': len(self._subscriptions),
                'subscriptions': sum(len(subs) for subs in self._subscriptions.values())
            }
    
    def list_topics(self) -> List[str]:
        """列出所有主題"""
        with self._lock:
            return list(self._subscriptions.keys())
    
    def get_topic_info(self, topic: str) -> Optional[Dict[str, Any]]:
        """
        獲取主題信息
        
        Args:
            topic: 主題名稱
            
        Returns:
            主題信息字典或None
        """
        with self._lock:
            if topic not in self._subscriptions:
                return None
            
            subscriptions = self._subscriptions[topic]
            return {
                'topic': topic,
                'subscribers': len(subscriptions),
                'subscription_ids': [sub.id for sub in subscriptions]
            }

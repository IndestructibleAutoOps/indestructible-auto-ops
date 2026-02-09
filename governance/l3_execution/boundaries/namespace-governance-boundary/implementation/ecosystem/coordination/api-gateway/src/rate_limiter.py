#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: coordination
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
GL API Gateway Rate Limiter
============================
速率限制器 - Token Bucket 算法

GL Governance Layer: GL10-29 (Operational Layer)
"""

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
import time
import threading
from typing import Dict, Optional, Any, Tuple
from dataclasses import dataclass
from collections import defaultdict
import logging


@dataclass
class RateLimitConfig:
    """速率限制配置"""

    limit: int  # 每分鐘請求數
    burst: int  # 突發容量
    window: int = 60  # 時間窗口（秒）


class TokenBucket:
    """令牌桶"""

    def __init__(self, capacity: int, refill_rate: float):
        """
        初始化令牌桶

        Args:
            capacity: 桶容量
            refill_rate: 填充速率（令牌/秒）
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = float(capacity)
        self.last_refill = time.time()
        self.lock = threading.Lock()

    def consume(self, tokens: int = 1) -> bool:
        """
        消費令牌

        Args:
            tokens: 消費的令牌數

        Returns:
            成功返回True
        """
        with self.lock:
            self._refill()

            if self.tokens >= tokens:
                self.tokens -= tokens
                return True

            return False

    def _refill(self):
        """填充令牌"""
        now = time.time()
        elapsed = now - self.last_refill

        # 計算應該添加的令牌數
        tokens_to_add = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now

    def get_tokens(self) -> float:
        """獲取當前令牌數"""
        with self.lock:
            self._refill()
            return self.tokens


class RateLimiter:
    """速率限制器"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化速率限制器

        Args:
            config: 配置字典
        """
        self.config = config or {}
        self.logger = self._setup_logger()

        # 默認限制
        default_limit = self.config.get("rate_limiting", {}).get("default_limit", 1000)
        default_burst = self.config.get("rate_limiting", {}).get("burst", 100)

        self.default_config = RateLimitConfig(limit=default_limit, burst=default_burst)

        # 路由特定限制
        self.route_limits: Dict[str, RateLimitConfig] = {}
        self._load_route_limits()

        # 令牌桶存儲: {client_id: {route: TokenBucket}}
        self.buckets: Dict[str, Dict[str, TokenBucket]] = defaultdict(dict)

        # 啟用狀態
        self.enabled = self.config.get("rate_limiting", {}).get("enabled", True)

        # 清理線程
        self._cleanup_thread = None
        self._cleanup_running = False
        if self.enabled:
            self._start_cleanup()

        self.logger.info("Rate Limiter initialized")

    def _setup_logger(self) -> logging.Logger:
        """設置日誌"""
        logger = logging.getLogger("RateLimiter")
        level = self.config.get("logging", {}).get("level", "INFO")
        logger.setLevel(getattr(logging, level))

        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger

    def _load_route_limits(self):
        """從配置加載路由限制"""
        per_route = self.config.get("rate_limiting", {}).get("per_route", {})

        for route, limit in per_route.items():
            self.route_limits[route] = RateLimitConfig(
                limit=limit, burst=limit // 10  # 突發容量為限制的10%
            )

    def check_rate_limit(
        self, client_id: str, route: str = "default"
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        檢查速率限制

        Args:
            client_id: 客戶端ID (IP地址、用戶ID等)
            route: 路由路徑

        Returns:
            (是否允許, 限制信息)
        """
        if not self.enabled:
            return True, {}

        # 獲取限制配置
        limit_config = self.route_limits.get(route, self.default_config)

        # 獲取或創建令牌桶
        if route not in self.buckets[client_id]:
            refill_rate = limit_config.limit / 60.0  # 每秒填充速率
            self.buckets[client_id][route] = TokenBucket(
                capacity=limit_config.burst, refill_rate=refill_rate
            )

        bucket = self.buckets[client_id][route]

        # 嘗試消費令牌
        allowed = bucket.consume(1)

        # 構建限制信息
        limit_info = {
            "limit": limit_config.limit,
            "remaining": int(bucket.get_tokens()),
            "reset": int(time.time() + 60),
        }

        if not allowed:
            self.logger.warning(
                f"Rate limit exceeded for client {client_id} on route {route}"
            )

        return allowed, limit_info

    def set_route_limit(self, route: str, limit: int, burst: Optional[int] = None):
        """
        設置路由限制

        Args:
            route: 路由路徑
            limit: 每分鐘請求數
            burst: 突發容量
        """
        if burst is None:
            burst = limit // 10

        self.route_limits[route] = RateLimitConfig(limit=limit, burst=burst)

        self.logger.info(f"Route limit set for {route}: {limit}/min, burst: {burst}")

    def reset_client_limits(self, client_id: str):
        """
        重置客戶端限制

        Args:
            client_id: 客戶端ID
        """
        if client_id in self.buckets:
            del self.buckets[client_id]
            self.logger.info(f"Limits reset for client {client_id}")

    def _start_cleanup(self):
        """啟動清理線程"""
        self._cleanup_running = True
        self._cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self._cleanup_thread.start()
        self.logger.info("Cleanup thread started")

    def _cleanup_loop(self):
        """清理循環 - 定期清理不活躍的客戶端"""
        while self._cleanup_running:
            try:
                time.sleep(300)  # 每5分鐘清理一次

                # 清理令牌已滿且長時間未使用的桶
                inactive_clients = []
                for client_id, routes in self.buckets.items():
                    all_full = all(
                        bucket.get_tokens() >= bucket.capacity
                        for bucket in routes.values()
                    )
                    if all_full:
                        inactive_clients.append(client_id)

                for client_id in inactive_clients:
                    del self.buckets[client_id]

                if inactive_clients:
                    self.logger.debug(
                        f"Cleaned up {len(inactive_clients)} inactive clients"
                    )

            except Exception as e:
                self.logger.error(f"Error in cleanup loop: {e}")

    def stop_cleanup(self):
        """停止清理線程"""
        if self._cleanup_running:
            self._cleanup_running = False
            if self._cleanup_thread:
                self._cleanup_thread.join(timeout=5)
            self.logger.info("Cleanup thread stopped")

    def get_stats(self) -> Dict[str, Any]:
        """
        獲取統計信息

        Returns:
            統計信息字典
        """
        total_clients = len(self.buckets)
        total_routes = sum(len(routes) for routes in self.buckets.values())

        return {
            "enabled": self.enabled,
            "total_clients": total_clients,
            "total_buckets": total_routes,
            "default_limit": self.default_config.limit,
            "route_limits": {
                route: config.limit for route, config in self.route_limits.items()
            },
        }

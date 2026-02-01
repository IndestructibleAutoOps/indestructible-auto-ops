#!/usr/bin/env python3
"""
GL Conflict Resolver
====================
衝突解決器 - 處理數據同步衝突

GL Governance Layer: GL10-29 (Operational Layer)
"""

from typing import Dict, Optional, Any, Callable
from dataclasses import dataclass
from datetime import datetime
import logging


@dataclass
class Conflict:
    """衝突"""
    id: str
    item_id: str
    source_version: Any
    target_version: Any
    source_timestamp: str
    target_timestamp: str
    resolved: bool = False
    resolution: Optional[Any] = None
    strategy_used: Optional[str] = None


class ConflictResolver:
    """衝突解決器"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化衝突解決器
        
        Args:
            config: 配置字典
        """
        self.config = config or {}
        self.logger = self._setup_logger()
        
        # 衝突歷史
        self._conflicts: Dict[str, Conflict] = {}
        
        # 自定義解決策略
        self._custom_strategies: Dict[str, Callable] = {}
        
        self.logger.info("Conflict Resolver initialized")
    
    def _setup_logger(self) -> logging.Logger:
        """設置日誌"""
        logger = logging.getLogger('ConflictResolver')
        level = self.config.get('monitoring', {}).get('logging', {}).get('level', 'INFO')
        logger.setLevel(getattr(logging, level))
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def resolve(
        self,
        item_id: str,
        source_data: Any,
        target_data: Any,
        source_timestamp: str,
        target_timestamp: str,
        strategy: str = "last-write-wins"
    ) -> Any:
        """
        解決衝突
        
        Args:
            item_id: 數據項ID
            source_data: 源數據
            target_data: 目標數據
            source_timestamp: 源時間戳
            target_timestamp: 目標時間戳
            strategy: 解決策略
            
        Returns:
            解決後的數據
        """
        import uuid
        
        # 記錄衝突
        conflict = Conflict(
            id=str(uuid.uuid4()),
            item_id=item_id,
            source_version=source_data,
            target_version=target_data,
            source_timestamp=source_timestamp,
            target_timestamp=target_timestamp
        )
        
        # 選擇策略
        if strategy == "last-write-wins":
            resolution = self._last_write_wins(source_data, target_data, source_timestamp, target_timestamp)
        elif strategy == "merge":
            resolution = self._merge(source_data, target_data)
        elif strategy == "custom" and strategy in self._custom_strategies:
            resolution = self._custom_strategies[strategy](source_data, target_data)
        else:
            # 默認策略
            resolution = self._last_write_wins(source_data, target_data, source_timestamp, target_timestamp)
        
        # 更新衝突記錄
        conflict.resolved = True
        conflict.resolution = resolution
        conflict.strategy_used = strategy
        self._conflicts[conflict.id] = conflict
        
        self.logger.info(
            f"Conflict resolved for {item_id} using {strategy}: "
            f"source_ts={source_timestamp}, target_ts={target_timestamp}"
        )
        
        return resolution
    
    def _last_write_wins(
        self,
        source_data: Any,
        target_data: Any,
        source_timestamp: str,
        target_timestamp: str
    ) -> Any:
        """
        Last-Write-Wins 策略
        
        Args:
            source_data: 源數據
            target_data: 目標數據
            source_timestamp: 源時間戳
            target_timestamp: 目標時間戳
            
        Returns:
            選中的數據
        """
        if source_timestamp > target_timestamp:
            self.logger.debug("LWW: source wins")
            return source_data
        else:
            self.logger.debug("LWW: target wins")
            return target_data
    
    def _merge(self, source_data: Any, target_data: Any) -> Any:
        """
        Merge 策略
        
        Args:
            source_data: 源數據
            target_data: 目標數據
            
        Returns:
            合併後的數據
        """
        # 如果是字典，合併鍵值
        if isinstance(source_data, dict) and isinstance(target_data, dict):
            merged = target_data.copy()
            merged.update(source_data)
            self.logger.debug(f"Merged {len(source_data)} fields from source")
            return merged
        
        # 如果是列表，合併並去重
        if isinstance(source_data, list) and isinstance(target_data, list):
            merged = list(set(target_data + source_data))
            self.logger.debug(f"Merged lists: {len(merged)} unique items")
            return merged
        
        # 其他情況，使用源數據
        return source_data
    
    def register_custom_strategy(
        self,
        name: str,
        strategy_func: Callable[[Any, Any], Any]
    ):
        """
        註冊自定義解決策略
        
        Args:
            name: 策略名稱
            strategy_func: 策略函數
        """
        self._custom_strategies[name] = strategy_func
        self.logger.info(f"Custom strategy registered: {name}")
    
    def get_conflict_history(self, item_id: Optional[str] = None) -> list:
        """
        獲取衝突歷史
        
        Args:
            item_id: 數據項ID（可選，None表示所有）
            
        Returns:
            衝突列表
        """
        if item_id:
            return [
                conflict for conflict in self._conflicts.values()
                if conflict.item_id == item_id
            ]
        return list(self._conflicts.values())
    
    def get_stats(self) -> Dict[str, Any]:
        """獲取統計信息"""
        total = len(self._conflicts)
        resolved = sum(1 for c in self._conflicts.values() if c.resolved)
        
        return {
            'total_conflicts': total,
            'resolved_conflicts': resolved,
            'unresolved_conflicts': total - resolved,
            'strategies_used': {
                strategy: sum(
                    1 for c in self._conflicts.values()
                    if c.strategy_used == strategy
                )
                for strategy in set(
                    c.strategy_used for c in self._conflicts.values()
                    if c.strategy_used
                )
            }
        }

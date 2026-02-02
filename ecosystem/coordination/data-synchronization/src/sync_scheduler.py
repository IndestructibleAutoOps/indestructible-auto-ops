#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: coordination
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
GL Sync Scheduler
=================
同步調度器 - 定時同步任務

GL Governance Layer: GL10-29 (Operational Layer)
"""

import threading
import time
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from datetime import datetime
import logging


@dataclass
class Schedule:
    """調度配置"""
    name: str
    source: str
    destinations: List[str]
    interval: int  # seconds
    enabled: bool = True
    last_run: Optional[str] = None
    next_run: Optional[str] = None
    run_count: int = 0


class SyncScheduler:
    """同步調度器"""
    
    def __init__(
        self,
        sync_callback: Callable[[str, str, List[str]], str],
        config: Optional[Dict[str, Any]] = None
    ):
        """
        初始化同步調度器
        
        Args:
            sync_callback: 同步回調函數 (dataset, source, destinations) -> job_id
            config: 配置字典
        """
        self.sync_callback = sync_callback
        self.config = config or {}
        self.logger = self._setup_logger()
        
        # 調度表
        self._schedules: Dict[str, Schedule] = {}
        
        # 調度線程
        self._scheduler_thread: Optional[threading.Thread] = None
        self._running = False
        
        # 從配置加載調度
        self._load_schedules_from_config()
        
        self.logger.info("Sync Scheduler initialized")
    
    def _setup_logger(self) -> logging.Logger:
        """設置日誌"""
        logger = logging.getLogger('SyncScheduler')
        level = self.config.get('monitoring', {}).get('logging', {}).get('level', 'INFO')
        logger.setLevel(getattr(logging, level))
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def _load_schedules_from_config(self):
        """從配置加載調度"""
        schedules_config = self.config.get('scheduler', {}).get('schedules', [])
        
        for schedule_data in schedules_config:
            if not schedule_data.get('enabled', True):
                continue
            
            schedule = Schedule(
                name=schedule_data['name'],
                source=schedule_data['source'],
                destinations=schedule_data['destinations'],
                interval=schedule_data.get('interval', 3600),
                enabled=schedule_data.get('enabled', True)
            )
            
            self._schedules[schedule.name] = schedule
            self.logger.info(
                f"Schedule loaded: {schedule.name} "
                f"(interval: {schedule.interval}s)"
            )
    
    def start(self):
        """啟動調度器"""
        if self._running:
            self.logger.warning("Scheduler already running")
            return
        
        self._running = True
        self._scheduler_thread = threading.Thread(
            target=self._scheduler_loop,
            daemon=True
        )
        self._scheduler_thread.start()
        self.logger.info("Scheduler started")
    
    def stop(self):
        """停止調度器"""
        if not self._running:
            return
        
        self._running = False
        if self._scheduler_thread:
            self._scheduler_thread.join(timeout=5)
        self.logger.info("Scheduler stopped")
    
    def add_schedule(
        self,
        name: str,
        source: str,
        destinations: List[str],
        interval: int,
        enabled: bool = True
    ) -> bool:
        """
        添加調度
        
        Args:
            name: 調度名稱
            source: 源位置
            destinations: 目標位置列表
            interval: 間隔（秒）
            enabled: 是否啟用
            
        Returns:
            成功返回True
        """
        if name in self._schedules:
            self.logger.warning(f"Schedule already exists: {name}")
            return False
        
        schedule = Schedule(
            name=name,
            source=source,
            destinations=destinations,
            interval=interval,
            enabled=enabled
        )
        
        self._schedules[name] = schedule
        self.logger.info(f"Schedule added: {name}")
        
        return True
    
    def remove_schedule(self, name: str) -> bool:
        """
        移除調度
        
        Args:
            name: 調度名稱
            
        Returns:
            成功返回True
        """
        if name not in self._schedules:
            self.logger.warning(f"Schedule not found: {name}")
            return False
        
        del self._schedules[name]
        self.logger.info(f"Schedule removed: {name}")
        
        return True
    
    def enable_schedule(self, name: str) -> bool:
        """啟用調度"""
        if name not in self._schedules:
            return False
        
        self._schedules[name].enabled = True
        self.logger.info(f"Schedule enabled: {name}")
        return True
    
    def disable_schedule(self, name: str) -> bool:
        """禁用調度"""
        if name not in self._schedules:
            return False
        
        self._schedules[name].enabled = False
        self.logger.info(f"Schedule disabled: {name}")
        return True
    
    def _scheduler_loop(self):
        """調度循環"""
        while self._running:
            try:
                current_time = time.time()
                
                for schedule in self._schedules.values():
                    if not schedule.enabled:
                        continue
                    
                    # 檢查是否需要執行
                    should_run = False
                    
                    if schedule.last_run is None:
                        # 首次運行
                        should_run = True
                    else:
                        # 計算距上次運行的時間
                        last_run_time = datetime.fromisoformat(schedule.last_run).timestamp()
                        if current_time - last_run_time >= schedule.interval:
                            should_run = True
                    
                    if should_run:
                        self._execute_schedule(schedule)
                
                # 休眠
                time.sleep(10)  # 每10秒檢查一次
                
            except Exception as e:
                self.logger.error(f"Error in scheduler loop: {e}")
                time.sleep(5)
    
    def _execute_schedule(self, schedule: Schedule):
        """
        執行調度
        
        Args:
            schedule: 調度配置
        """
        try:
            self.logger.info(f"Executing schedule: {schedule.name}")
            
            # 調用同步回調
            job_id = self.sync_callback(
                schedule.name,  # dataset
                schedule.source,
                schedule.destinations
            )
            
            # 更新調度信息
            schedule.last_run = datetime.utcnow().isoformat()
            schedule.run_count += 1
            
            self.logger.info(
                f"Schedule executed: {schedule.name} (job_id: {job_id})"
            )
            
        except Exception as e:
            self.logger.error(f"Failed to execute schedule {schedule.name}: {e}")
    
    def get_schedules(self) -> List[Dict[str, Any]]:
        """獲取所有調度"""
        return [
            {
                'name': schedule.name,
                'source': schedule.source,
                'destinations': schedule.destinations,
                'interval': schedule.interval,
                'enabled': schedule.enabled,
                'last_run': schedule.last_run,
                'run_count': schedule.run_count
            }
            for schedule in self._schedules.values()
        ]
    
    def get_schedule_info(self, name: str) -> Optional[Dict[str, Any]]:
        """獲取調度信息"""
        schedule = self._schedules.get(name)
        if not schedule:
            return None
        
        return {
            'name': schedule.name,
            'source': schedule.source,
            'destinations': schedule.destinations,
            'interval': schedule.interval,
            'enabled': schedule.enabled,
            'last_run': schedule.last_run,
            'run_count': schedule.run_count
        }

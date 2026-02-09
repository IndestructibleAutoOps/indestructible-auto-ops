#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: coordination
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
GL Sync Engine
==============
同步引擎 - 數據同步核心

GL Governance Layer: GL10-29 (Operational Layer)
"""

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
import uuid
import time
import hashlib
import threading
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging


class SyncMode(Enum):
    """同步模式"""

    REAL_TIME = "real-time"
    SCHEDULED = "scheduled"
    MANUAL = "manual"


class SyncStatus(Enum):
    """同步狀態"""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ConflictStrategy(Enum):
    """衝突解決策略"""

    LAST_WRITE_WINS = "last-write-wins"
    MERGE = "merge"
    CUSTOM = "custom"


@dataclass
class DataItem:
    """數據項"""

    id: str
    data: Any
    version: int = 1
    checksum: str = ""
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """計算校驗和"""
        if not self.checksum:
            self.checksum = self._calculate_checksum()

    def _calculate_checksum(self) -> str:
        """計算數據校驗和"""
        import json

        data_str = json.dumps(self.data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()


@dataclass
class SyncJob:
    """同步任務"""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    dataset: str = ""
    source: str = ""
    destinations: List[str] = field(default_factory=list)
    mode: SyncMode = SyncMode.MANUAL
    status: SyncStatus = SyncStatus.PENDING
    items_total: int = 0
    items_synced: int = 0
    items_failed: int = 0
    conflicts: int = 0
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error: Optional[str] = None


class SyncEngine:
    """同步引擎"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化同步引擎

        Args:
            config: 配置字典
        """
        self.config = config or {}
        self.logger = self._setup_logger()

        # 數據存儲: {dataset: {item_id: DataItem}}
        self._data_store: Dict[str, Dict[str, DataItem]] = {}

        # 同步任務: {job_id: SyncJob}
        self._jobs: Dict[str, SyncJob] = {}

        # 統計
        self._sync_count = 0
        self._conflict_count = 0
        self._error_count = 0

        # 鎖
        self._lock = threading.RLock()

        # 配置
        self.batch_size = self.config.get("sync_engine", {}).get("batch_size", 1000)
        self.max_retries = self.config.get("sync_engine", {}).get("max_retries", 3)
        self.retry_delay = self.config.get("sync_engine", {}).get("retry_delay", 5)

        self.logger.info("Sync Engine initialized")

    def _setup_logger(self) -> logging.Logger:
        """設置日誌"""
        logger = logging.getLogger("SyncEngine")
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

    def create_sync_job(
        self,
        dataset: str,
        source: str,
        destinations: List[str],
        mode: SyncMode = SyncMode.MANUAL,
    ) -> str:
        """
        創建同步任務

        Args:
            dataset: 數據集名稱
            source: 源位置
            destinations: 目標位置列表
            mode: 同步模式

        Returns:
            任務ID
        """
        with self._lock:
            job = SyncJob(
                dataset=dataset, source=source, destinations=destinations, mode=mode
            )

            self._jobs[job.id] = job
            self.logger.info(f"Sync job created: {job.id} ({source} -> {destinations})")

            return job.id

    def execute_sync_job(self, job_id: str) -> bool:
        """
        執行同步任務

        Args:
            job_id: 任務ID

        Returns:
            成功返回True
        """
        with self._lock:
            job = self._jobs.get(job_id)
            if not job:
                self.logger.error(f"Sync job not found: {job_id}")
                return False

            if job.status == SyncStatus.IN_PROGRESS:
                self.logger.warning(f"Sync job already in progress: {job_id}")
                return False

            # 更新狀態
            job.status = SyncStatus.IN_PROGRESS
            job.started_at = datetime.utcnow().isoformat()

            try:
                # 執行同步
                self._perform_sync(job)

                # 更新狀態
                job.status = SyncStatus.COMPLETED
                job.completed_at = datetime.utcnow().isoformat()

                self._sync_count += 1
                self.logger.info(
                    f"Sync job completed: {job_id} "
                    f"({job.items_synced}/{job.items_total} items synced)"
                )

                return True

            except Exception as e:
                job.status = SyncStatus.FAILED
                job.error = str(e)
                job.completed_at = datetime.utcnow().isoformat()

                self._error_count += 1
                self.logger.error(f"Sync job failed: {job_id}: {e}")

                return False

    def _perform_sync(self, job: SyncJob):
        """
        執行同步操作

        Args:
            job: 同步任務
        """
        # 獲取源數據
        source_data = self._data_store.get(job.source, {})
        job.items_total = len(source_data)

        if not source_data:
            self.logger.warning(f"No data found in source: {job.source}")
            return

        # 同步到每個目標
        for destination in job.destinations:
            self._sync_to_destination(job, source_data, destination)

    def _sync_to_destination(
        self, job: SyncJob, source_data: Dict[str, DataItem], destination: str
    ):
        """
        同步到目標位置

        Args:
            job: 同步任務
            source_data: 源數據
            destination: 目標位置
        """
        # 確保目標數據存儲存在
        if destination not in self._data_store:
            self._data_store[destination] = {}

        dest_data = self._data_store[destination]

        # 批量處理
        items = list(source_data.items())
        for i in range(0, len(items), self.batch_size):
            batch = items[i : i + self.batch_size]

            for item_id, item in batch:
                try:
                    # 檢查目標是否已存在
                    if item_id in dest_data:
                        # 檢測衝突
                        existing = dest_data[item_id]
                        if existing.checksum != item.checksum:
                            # 解決衝突
                            resolved = self._resolve_conflict(existing, item, job)
                            dest_data[item_id] = resolved
                            job.conflicts += 1
                        # else: 數據相同，無需同步
                    else:
                        # 複製數據
                        dest_data[item_id] = DataItem(
                            id=item.id,
                            data=item.data,
                            version=item.version,
                            checksum=item.checksum,
                            timestamp=item.timestamp,
                            metadata=item.metadata.copy(),
                        )

                    job.items_synced += 1

                except Exception as e:
                    job.items_failed += 1
                    self.logger.error(f"Failed to sync item {item_id}: {e}")

    def _resolve_conflict(
        self, existing: DataItem, incoming: DataItem, job: SyncJob
    ) -> DataItem:
        """
        解決衝突

        Args:
            existing: 現有數據
            incoming: 傳入數據
            job: 同步任務

        Returns:
            解決後的數據
        """
        strategy = self.config.get("conflict_resolution", {}).get(
            "default_strategy", "last-write-wins"
        )

        if strategy == "last-write-wins":
            # 選擇時間戳較新的
            if incoming.timestamp > existing.timestamp:
                self.logger.debug(
                    f"Conflict resolved: using incoming data for {incoming.id}"
                )
                return incoming
            else:
                self.logger.debug(
                    f"Conflict resolved: keeping existing data for {existing.id}"
                )
                return existing

        elif strategy == "merge":
            # 合併數據
            merged_data = self._merge_data(existing.data, incoming.data)
            merged = DataItem(
                id=existing.id,
                data=merged_data,
                version=max(existing.version, incoming.version) + 1,
                timestamp=datetime.utcnow().isoformat(),
            )
            self.logger.debug(f"Conflict resolved: merged data for {merged.id}")
            return merged

        else:
            # 默認使用 last-write-wins
            return incoming if incoming.timestamp > existing.timestamp else existing

    def _merge_data(self, existing: Any, incoming: Any) -> Any:
        """
        合併數據

        Args:
            existing: 現有數據
            incoming: 傳入數據

        Returns:
            合併後的數據
        """
        # 簡單合併邏輯：如果是字典，則合併鍵值
        if isinstance(existing, dict) and isinstance(incoming, dict):
            merged = existing.copy()
            merged.update(incoming)
            return merged

        # 否則返回傳入數據
        return incoming

    def add_data(self, location: str, item_id: str, data: Any) -> bool:
        """
        添加數據

        Args:
            location: 數據位置
            item_id: 數據項ID
            data: 數據

        Returns:
            成功返回True
        """
        with self._lock:
            if location not in self._data_store:
                self._data_store[location] = {}

            item = DataItem(id=item_id, data=data)
            self._data_store[location][item_id] = item

            self.logger.debug(f"Data added: {item_id} to {location}")
            return True

    def get_data(self, location: str, item_id: str) -> Optional[DataItem]:
        """
        獲取數據

        Args:
            location: 數據位置
            item_id: 數據項ID

        Returns:
            數據項或None
        """
        with self._lock:
            return self._data_store.get(location, {}).get(item_id)

    def list_data(self, location: str) -> List[str]:
        """
        列出數據項

        Args:
            location: 數據位置

        Returns:
            數據項ID列表
        """
        with self._lock:
            return list(self._data_store.get(location, {}).keys())

    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """
        獲取任務狀態

        Args:
            job_id: 任務ID

        Returns:
            任務狀態字典或None
        """
        with self._lock:
            job = self._jobs.get(job_id)
            if not job:
                return None

            return {
                "id": job.id,
                "dataset": job.dataset,
                "source": job.source,
                "destinations": job.destinations,
                "status": job.status.value,
                "items_total": job.items_total,
                "items_synced": job.items_synced,
                "items_failed": job.items_failed,
                "conflicts": job.conflicts,
                "created_at": job.created_at,
                "started_at": job.started_at,
                "completed_at": job.completed_at,
                "error": job.error,
            }

    def get_stats(self) -> Dict[str, Any]:
        """
        獲取統計信息

        Returns:
            統計信息字典
        """
        with self._lock:
            total_items = sum(len(data) for data in self._data_store.values())

            return {
                "locations": len(self._data_store),
                "total_items": total_items,
                "total_jobs": len(self._jobs),
                "sync_count": self._sync_count,
                "conflict_count": self._conflict_count,
                "error_count": self._error_count,
                "jobs_by_status": {
                    status.value: sum(
                        1 for job in self._jobs.values() if job.status == status
                    )
                    for status in SyncStatus
                },
            }

#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: coordination
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
GL Service Registry
===================
服務註冊中心 - 存儲和管理所有已註冊的服務

GL Governance Layer: GL10-29 (Operational Layer)
"""

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
# MNGA-002: Import organization needs review
import json
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict, field
from datetime import datetime
from enum import Enum
import logging


class ServiceStatus(Enum):
    """服務狀態"""

    ACTIVE = "active"
    INACTIVE = "inactive"
    UNHEALTHY = "unhealthy"
    DEPRECATED = "deprecated"


class HealthStatus(Enum):
    """健康狀態"""

    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class ServiceMetadata:
    """服務元數據"""

    name: str
    platform: str
    endpoint: str
    type: Optional[str] = None
    version: Optional[str] = "1.0.0"
    tags: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)
    region: Optional[str] = None
    zone: Optional[str] = None
    custom_metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HealthCheck:
    """健康檢查配置"""

    type: str  # http, tcp, custom
    endpoint: Optional[str] = None
    interval: int = 30
    timeout: int = 5
    retries: int = 3
    custom_check: Optional[callable] = None


@dataclass
class ServiceInstance:
    """服務實例"""

    id: str
    metadata: ServiceMetadata
    health_check: Optional[HealthCheck] = None
    status: ServiceStatus = ServiceStatus.ACTIVE
    health_status: HealthStatus = HealthStatus.UNKNOWN
    registered_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    last_heartbeat: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    ttl: int = 300  # seconds
    failure_count: int = 0
    success_count: int = 0
    connection_count: int = 0


class ServiceRegistry:
    """服務註冊中心"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化服務註冊中心

        Args:
            config: 配置字典
        """
        self.config = config or {}
        self.logger = self._setup_logger()

        # 服務存儲: {service_id: ServiceInstance}
        self._services: Dict[str, ServiceInstance] = {}

        # 索引: {service_name: [service_ids]}
        self._name_index: Dict[str, List[str]] = {}

        # 索引: {platform: [service_ids]}
        self._platform_index: Dict[str, List[str]] = {}

        # 索引: {type: [service_ids]}
        self._type_index: Dict[str, List[str]] = {}

        # 鎖
        self._lock = threading.RLock()

        # 持久化
        self.persistence_enabled = self.config.get("registry", {}).get(
            "persistence", True
        )
        self.storage_path = Path(
            self.config.get("registry", {}).get("storage_path", "/tmp/service-registry")
        )

        if self.persistence_enabled:
            self._load_from_storage()

        self.logger.info("Service Registry initialized")

    def _setup_logger(self) -> logging.Logger:
        """設置日誌"""
        logger = logging.getLogger("ServiceRegistry")
        level = (
            self.config.get("monitoring", {}).get("logging", {}).get("level", "INFO")
        )
        logger.setLevel(getattr(logging, level))

        # Avoid adding duplicate stream handlers if multiple registries are instantiated
        has_stream_handler = any(
            isinstance(handler, logging.StreamHandler) for handler in logger.handlers
        )
        if not has_stream_handler:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def register_service(self, instance: ServiceInstance) -> bool:
        """
        註冊服務

        Args:
            instance: 服務實例

        Returns:
            註冊成功返回True
        """
        with self._lock:
            try:
                # 檢查是否已存在
                if instance.id in self._services:
                    self.logger.warning(
                        f"Service {instance.id} already registered, updating"
                    )

                # 存儲服務
                self._services[instance.id] = instance

                # 更新索引
                self._update_indices(instance)

                # 持久化
                if self.persistence_enabled:
                    self._save_to_storage()

                self.logger.info(
                    f"Service registered: {instance.metadata.name} "
                    f"(id={instance.id}, platform={instance.metadata.platform})"
                )

                return True

            except Exception as e:
                self.logger.error(f"Failed to register service {instance.id}: {e}")
                return False

    def deregister_service(self, service_id: str) -> bool:
        """
        註銷服務

        Args:
            service_id: 服務ID

        Returns:
            註銷成功返回True
        """
        with self._lock:
            try:
                if service_id not in self._services:
                    self.logger.warning(f"Service {service_id} not found")
                    return False

                instance = self._services[service_id]

                # 從索引中移除
                self._remove_from_indices(instance)

                # 刪除服務
                del self._services[service_id]

                # 持久化
                if self.persistence_enabled:
                    self._save_to_storage()

                self.logger.info(f"Service deregistered: {service_id}")

                return True

            except Exception as e:
                self.logger.error(f"Failed to deregister service {service_id}: {e}")
                return False

    def get_service(self, service_id: str) -> Optional[ServiceInstance]:
        """
        獲取服務實例

        Args:
            service_id: 服務ID

        Returns:
            服務實例或None
        """
        with self._lock:
            return self._services.get(service_id)

    def discover_services(
        self,
        name: Optional[str] = None,
        platform: Optional[str] = None,
        service_type: Optional[str] = None,
        tags: Optional[List[str]] = None,
        status: Optional[ServiceStatus] = None,
        health_status: Optional[HealthStatus] = None,
    ) -> List[ServiceInstance]:
        """
        發現服務

        Args:
            name: 服務名稱
            platform: 平台名稱
            service_type: 服務類型
            tags: 標籤列表
            status: 服務狀態
            health_status: 健康狀態

        Returns:
            匹配的服務實例列表
        """
        with self._lock:
            # 從索引獲取候選服務
            candidates = set()

            if name:
                candidates.update(self._name_index.get(name, []))
            elif platform:
                candidates.update(self._platform_index.get(platform, []))
            elif service_type:
                candidates.update(self._type_index.get(service_type, []))
            else:
                candidates.update(self._services.keys())

            # 過濾
            results = []
            for service_id in candidates:
                instance = self._services.get(service_id)
                if not instance:
                    continue

                # 應用過濾器
                if name and instance.metadata.name != name:
                    continue
                if platform and instance.metadata.platform != platform:
                    continue
                if service_type and instance.metadata.type != service_type:
                    continue
                if status and instance.status != status:
                    continue
                if health_status and instance.health_status != health_status:
                    continue
                if tags:
                    if not all(tag in instance.metadata.tags for tag in tags):
                        continue

                results.append(instance)

            self.logger.debug(f"Discovered {len(results)} services matching criteria")
            return results

    def update_health_status(
        self, service_id: str, health_status: HealthStatus
    ) -> bool:
        """
        更新服務健康狀態

        Args:
            service_id: 服務ID
            health_status: 健康狀態

        Returns:
            更新成功返回True
        """
        with self._lock:
            instance = self._services.get(service_id)
            if not instance:
                return False

            old_status = instance.health_status
            instance.health_status = health_status
            instance.last_heartbeat = datetime.utcnow().isoformat()

            if health_status == HealthStatus.HEALTHY:
                instance.success_count += 1
                instance.failure_count = 0
            elif health_status == HealthStatus.UNHEALTHY:
                instance.failure_count += 1

            if old_status != health_status:
                self.logger.info(
                    f"Service {service_id} health status changed: "
                    f"{old_status.value} -> {health_status.value}"
                )

            return True

    def update_heartbeat(self, service_id: str) -> bool:
        """
        更新服務心跳

        Args:
            service_id: 服務ID

        Returns:
            更新成功返回True
        """
        with self._lock:
            instance = self._services.get(service_id)
            if not instance:
                return False

            instance.last_heartbeat = datetime.utcnow().isoformat()
            return True

    def get_statistics(self) -> Dict[str, Any]:
        """
        獲取註冊中心統計信息

        Returns:
            統計信息字典
        """
        with self._lock:
            total = len(self._services)
            active = sum(
                1 for s in self._services.values() if s.status == ServiceStatus.ACTIVE
            )
            healthy = sum(
                1
                for s in self._services.values()
                if s.health_status == HealthStatus.HEALTHY
            )

            return {
                "total_services": total,
                "active_services": active,
                "healthy_services": healthy,
                "platforms": len(self._platform_index),
                "service_types": len(self._type_index),
                "by_platform": {
                    platform: len(service_ids)
                    for platform, service_ids in self._platform_index.items()
                },
                "by_type": {
                    service_type: len(service_ids)
                    for service_type, service_ids in self._type_index.items()
                },
            }

    def _update_indices(self, instance: ServiceInstance):
        """更新索引"""
        # 名稱索引
        if instance.metadata.name not in self._name_index:
            self._name_index[instance.metadata.name] = []
        if instance.id not in self._name_index[instance.metadata.name]:
            self._name_index[instance.metadata.name].append(instance.id)

        # 平台索引
        if instance.metadata.platform not in self._platform_index:
            self._platform_index[instance.metadata.platform] = []
        if instance.id not in self._platform_index[instance.metadata.platform]:
            self._platform_index[instance.metadata.platform].append(instance.id)

        # 類型索引
        if instance.metadata.type:
            if instance.metadata.type not in self._type_index:
                self._type_index[instance.metadata.type] = []
            if instance.id not in self._type_index[instance.metadata.type]:
                self._type_index[instance.metadata.type].append(instance.id)

    def _remove_from_indices(self, instance: ServiceInstance):
        """從索引中移除"""
        # 名稱索引
        if instance.metadata.name in self._name_index:
            if instance.id in self._name_index[instance.metadata.name]:
                self._name_index[instance.metadata.name].remove(instance.id)
            if not self._name_index[instance.metadata.name]:
                del self._name_index[instance.metadata.name]

        # 平台索引
        if instance.metadata.platform in self._platform_index:
            if instance.id in self._platform_index[instance.metadata.platform]:
                self._platform_index[instance.metadata.platform].remove(instance.id)
            if not self._platform_index[instance.metadata.platform]:
                del self._platform_index[instance.metadata.platform]

        # 類型索引
        if instance.metadata.type and instance.metadata.type in self._type_index:
            if instance.id in self._type_index[instance.metadata.type]:
                self._type_index[instance.metadata.type].remove(instance.id)
            if not self._type_index[instance.metadata.type]:
                del self._type_index[instance.metadata.type]

    def _save_to_storage(self):
        """持久化到存儲"""
        try:
            self.storage_path.mkdir(parents=True, exist_ok=True)
            registry_file = self.storage_path / "registry.json"

            data = {
                "services": {
                    service_id: self._serialize_instance(instance)
                    for service_id, instance in self._services.items()
                },
                "updated_at": datetime.utcnow().isoformat(),
            }

            with open(registry_file, "w") as f:
                json.dump(data, f, indent=2)

            self.logger.debug(f"Registry saved to {registry_file}")

        except Exception as e:
            self.logger.error(f"Failed to save registry to storage: {e}")

    def _load_from_storage(self):
        """從存儲加載"""
        try:
            registry_file = self.storage_path / "registry.json"

            if not registry_file.exists():
                self.logger.info("No existing registry file found")
                return

            with open(registry_file, "r") as f:
                data = json.load(f)

            for service_id, service_data in data.get("services", {}).items():
                instance = self._deserialize_instance(service_data)
                self._services[service_id] = instance
                self._update_indices(instance)

            self.logger.info(f"Loaded {len(self._services)} services from storage")

        except Exception as e:
            self.logger.error(f"Failed to load registry from storage: {e}")

    def _serialize_instance(self, instance: ServiceInstance) -> Dict[str, Any]:
        """序列化服務實例"""
        data = {
            "id": instance.id,
            "metadata": asdict(instance.metadata),
            "status": instance.status.value,
            "health_status": instance.health_status.value,
            "registered_at": instance.registered_at,
            "last_heartbeat": instance.last_heartbeat,
            "ttl": instance.ttl,
            "failure_count": instance.failure_count,
            "success_count": instance.success_count,
            "connection_count": instance.connection_count,
        }

        if instance.health_check:
            data["health_check"] = {
                "type": instance.health_check.type,
                "endpoint": instance.health_check.endpoint,
                "interval": instance.health_check.interval,
                "timeout": instance.health_check.timeout,
                "retries": instance.health_check.retries,
            }

        return data

    def _deserialize_instance(self, data: Dict[str, Any]) -> ServiceInstance:
        """反序列化服務實例"""
        metadata = ServiceMetadata(**data["metadata"])

        health_check = None
        if "health_check" in data:
            hc_data = data["health_check"]
            health_check = HealthCheck(
                type=hc_data["type"],
                endpoint=hc_data.get("endpoint"),
                interval=hc_data.get("interval", 30),
                timeout=hc_data.get("timeout", 5),
                retries=hc_data.get("retries", 3),
            )

        return ServiceInstance(
            id=data["id"],
            metadata=metadata,
            health_check=health_check,
            status=ServiceStatus(data["status"]),
            health_status=HealthStatus(data["health_status"]),
            registered_at=data["registered_at"],
            last_heartbeat=data["last_heartbeat"],
            ttl=data.get("ttl", 300),
            failure_count=data.get("failure_count", 0),
            success_count=data.get("success_count", 0),
            connection_count=data.get("connection_count", 0),
        )

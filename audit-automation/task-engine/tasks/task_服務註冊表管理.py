"""服務註冊表管理任務

整合自: ecosystem/tools/registry/service_registry_manager.py
用途: 管理服務註冊、健康檢查、服務發現
"""

import logging
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from auto_executor import Task, executor

logger = logging.getLogger(__name__)


class ServiceRegistryManager:
    """服務註冊表管理器"""

    def __init__(self, registry_path: str = None):
        """初始化管理器"""
        if registry_path is None:
            registry_path = "tasks/registries/service-registry.yaml"

        self.registry_path = Path(registry_path)
        self.services = self._load_registry()

    def _load_registry(self) -> Dict[str, Any]:
        """加載註冊表"""
        if not self.registry_path.exists():
            return {
                "services": [],
                "metadata": {"version": "1.0.0", "updated": datetime.now().isoformat()},
            }

        try:
            with open(self.registry_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                return data or {"services": []}
        except Exception as e:
            logger.error(f"加載服務註冊表失敗: {e}")
            return {"services": []}

    def _save_registry(self) -> bool:
        """保存註冊表"""
        try:
            self.registry_path.parent.mkdir(parents=True, exist_ok=True)

            # 更新時間戳
            if "metadata" not in self.services:
                self.services["metadata"] = {}
            self.services["metadata"]["updated"] = datetime.now().isoformat()

            with open(self.registry_path, "w", encoding="utf-8") as f:
                yaml.dump(
                    self.services, f, default_flow_style=False, allow_unicode=True
                )

            logger.info(f"✅ 服務註冊表已保存: {self.registry_path}")
            return True
        except Exception as e:
            logger.error(f"保存服務註冊表失敗: {e}")
            return False

    def register_service(
        self,
        name: str,
        endpoint: str,
        service_type: str = "http",
        status: str = "active",
        **kwargs,
    ) -> bool:
        """註冊服務"""
        service_entry = {
            "name": name,
            "endpoint": endpoint,
            "type": service_type,
            "status": status,
            "registered_at": datetime.now().isoformat(),
            "health": "unknown",
            **kwargs,
        }

        # 檢查是否已存在
        for i, svc in enumerate(self.services.get("services", [])):
            if svc.get("name") == name:
                self.services["services"][i] = service_entry
                logger.info(f"🔄 更新服務: {name}")
                return self._save_registry()

        # 新增
        if "services" not in self.services:
            self.services["services"] = []

        self.services["services"].append(service_entry)
        logger.info(f"✅ 註冊服務: {name}")
        return self._save_registry()

    def list_services(self, status: str = None, service_type: str = None) -> List[Dict]:
        """列出服務"""
        services = self.services.get("services", [])

        if status:
            services = [s for s in services if s.get("status") == status]

        if service_type:
            services = [s for s in services if s.get("type") == service_type]

        return services

    def health_check_all(self) -> Dict[str, int]:
        """檢查所有服務健康狀態"""
        results = {"healthy": 0, "unhealthy": 0, "unknown": 0}

        for service in self.services.get("services", []):
            health = service.get("health", "unknown")
            if health in results:
                results[health] += 1

        return results


class ServiceRegistryTask(Task):
    """服務註冊表管理任務"""

    name = "服務註冊表管理"
    priority = 3

    def __init__(self):
        super().__init__()
        self.manager = ServiceRegistryManager()

    def execute(self):
        """執行服務註冊表維護"""
        logger.info("🔍 檢查服務註冊表...")

        # 列出所有服務
        all_services = self.manager.list_services()
        logger.info(f"📊 總服務數: {len(all_services)}")

        # 按狀態分類
        active = self.manager.list_services(status="active")
        inactive = self.manager.list_services(status="inactive")

        logger.info(f"  ✓ 活躍: {len(active)}")
        logger.info(f"  - 停用: {len(inactive)}")

        # 健康檢查統計
        health_stats = self.manager.health_check_all()
        logger.info(f"🏥 健康狀態:")
        logger.info(f"  ✓ 健康: {health_stats['healthy']}")
        logger.info(f"  ✗ 不健康: {health_stats['unhealthy']}")
        logger.info(f"  ? 未知: {health_stats['unknown']}")

        # 列出前 5 個服務
        if all_services:
            logger.info("📋 服務列表（前5個）:")
            for svc in all_services[:5]:
                logger.info(
                    f"  - {svc.get('name')} [{svc.get('type')}] @ {svc.get('endpoint', 'N/A')}"
                )


# 註冊任務：每小時檢查一次
executor.register(ServiceRegistryTask, interval=3600, priority=3)

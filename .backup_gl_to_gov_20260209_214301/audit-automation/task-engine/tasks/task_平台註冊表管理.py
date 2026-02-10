"""平台註冊表管理任務

整合自: ecosystem/tools/registry/platform_registry_manager.py
用途: 管理平台註冊、更新、查詢、驗證
"""

import logging
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from auto_executor import Task, executor

logger = logging.getLogger(__name__)


class PlatformRegistryManager:
    """平台註冊表管理器"""

    def __init__(self, registry_path: str = None):
        """初始化管理器"""
        if registry_path is None:
            registry_path = "tasks/registries/platform-registry.yaml"

        self.registry_path = Path(registry_path)
        self.platforms = self._load_registry()

    def _load_registry(self) -> Dict[str, Any]:
        """加載註冊表"""
        if not self.registry_path.exists():
            return {
                "platforms": [],
                "metadata": {"version": "1.0.0", "updated": datetime.now().isoformat()},
            }

        try:
            with open(self.registry_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                return data or {"platforms": []}
        except Exception as e:
            logger.error(f"加載註冊表失敗: {e}")
            return {"platforms": []}

    def _save_registry(self) -> bool:
        """保存註冊表"""
        try:
            self.registry_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.registry_path, "w", encoding="utf-8") as f:
                yaml.dump(
                    self.platforms, f, default_flow_style=False, allow_unicode=True
                )

            logger.info(f"✅ 註冊表已保存: {self.registry_path}")
            return True
        except Exception as e:
            logger.error(f"保存註冊表失敗: {e}")
            return False

    def register_platform(
        self, name: str, layer: str, status: str = "active", **kwargs
    ) -> bool:
        """註冊平台"""
        platform_entry = {
            "name": name,
            "layer": layer,
            "status": status,
            "registered_at": datetime.now().isoformat(),
            **kwargs,
        }

        # 檢查是否已存在
        for i, p in enumerate(self.platforms.get("platforms", [])):
            if p.get("name") == name:
                self.platforms["platforms"][i] = platform_entry
                logger.info(f"🔄 更新平台: {name}")
                return self._save_registry()

        # 新增
        if "platforms" not in self.platforms:
            self.platforms["platforms"] = []

        self.platforms["platforms"].append(platform_entry)
        logger.info(f"✅ 註冊平台: {name}")
        return self._save_registry()

    def list_platforms(self, layer: str = None, status: str = None) -> List[Dict]:
        """列出平台"""
        platforms = self.platforms.get("platforms", [])

        if layer:
            platforms = [p for p in platforms if p.get("layer") == layer]

        if status:
            platforms = [p for p in platforms if p.get("status") == status]

        return platforms

    def get_platform(self, name: str) -> Optional[Dict]:
        """取得平台資訊"""
        for platform in self.platforms.get("platforms", []):
            if platform.get("name") == name:
                return platform
        return None

    def update_platform_status(self, name: str, status: str) -> bool:
        """更新平台狀態"""
        for i, p in enumerate(self.platforms.get("platforms", [])):
            if p.get("name") == name:
                self.platforms["platforms"][i]["status"] = status
                self.platforms["platforms"][i][
                    "updated_at"
                ] = datetime.now().isoformat()
                logger.info(f"🔄 更新平台狀態: {name} → {status}")
                return self._save_registry()

        logger.warning(f"⚠️  平台不存在: {name}")
        return False

    def validate_registry(self) -> Dict[str, Any]:
        """驗證註冊表完整性"""
        results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "platform_count": len(self.platforms.get("platforms", [])),
        }

        for i, platform in enumerate(self.platforms.get("platforms", [])):
            if not platform.get("name"):
                results["errors"].append(f"平台 #{i+1} 缺少名稱")
                results["valid"] = False

            if not platform.get("layer"):
                results["warnings"].append(
                    f"平台 {platform.get('name', i)} 缺少 GL layer"
                )

        return results


class PlatformRegistryTask(Task):
    """平台註冊表管理任務"""

    name = "平台註冊表管理"
    priority = 4

    def __init__(self):
        super().__init__()
        self.manager = PlatformRegistryManager()

    def execute(self):
        """執行註冊表維護"""
        logger.info("🔍 檢查平台註冊表...")

        # 驗證註冊表
        validation = self.manager.validate_registry()
        logger.info(f"📊 平台數量: {validation['platform_count']}")

        if validation["errors"]:
            logger.error(f"❌ 發現 {len(validation['errors'])} 個錯誤")
            for error in validation["errors"]:
                logger.error(f"  - {error}")

        if validation["warnings"]:
            logger.warning(f"⚠️  發現 {len(validation['warnings'])} 個警告")
            for warning in validation["warnings"]:
                logger.warning(f"  - {warning}")

        if validation["valid"]:
            logger.info("✅ 平台註冊表驗證通過")

        # 列出活躍平台
        active_platforms = self.manager.list_platforms(status="active")
        logger.info(f"📋 活躍平台: {len(active_platforms)}")
        for platform in active_platforms[:5]:
            logger.info(f"  - {platform.get('name')} [{platform.get('layer')}]")


# 註冊任務：每天檢查一次
executor.register(PlatformRegistryTask, cron="0 10 * * *", priority=4)

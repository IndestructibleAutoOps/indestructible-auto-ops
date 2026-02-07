"""數據目錄管理任務

整合自: ecosystem/tools/registry/data_catalog_manager.py
用途: 管理數據集註冊、Schema 驗證、數據發現
"""

import logging
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from auto_executor import Task, executor

logger = logging.getLogger(__name__)


class DataCatalogManager:
    """數據目錄管理器"""

    def __init__(self, catalog_path: str = None):
        """初始化管理器"""
        if catalog_path is None:
            catalog_path = "tasks/registries/data-registry/data-catalog.yaml"

        self.catalog_path = Path(catalog_path)
        self.catalog = self._load_catalog()

    def _load_catalog(self) -> Dict[str, Any]:
        """加載數據目錄"""
        if not self.catalog_path.exists():
            return {
                "datasets": [],
                "metadata": {
                    "version": "1.0.0",
                    "updated": datetime.now().isoformat(),
                    "dataset_count": 0,
                },
            }

        try:
            with open(self.catalog_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                return data or {"datasets": []}
        except Exception as e:
            logger.error(f"加載數據目錄失敗: {e}")
            return {"datasets": []}

    def _save_catalog(self) -> bool:
        """保存數據目錄"""
        try:
            self.catalog_path.parent.mkdir(parents=True, exist_ok=True)

            # 更新元數據
            if "metadata" not in self.catalog:
                self.catalog["metadata"] = {}

            self.catalog["metadata"]["updated"] = datetime.now().isoformat()
            self.catalog["metadata"]["dataset_count"] = len(
                self.catalog.get("datasets", [])
            )

            with open(self.catalog_path, "w", encoding="utf-8") as f:
                yaml.dump(self.catalog, f, default_flow_style=False, allow_unicode=True)

            logger.info(f"✅ 數據目錄已保存: {self.catalog_path}")
            return True
        except Exception as e:
            logger.error(f"保存數據目錄失敗: {e}")
            return False

    def register_dataset(
        self,
        name: str,
        description: str,
        schema: Dict[str, Any],
        owner: str,
        tags: List[str] = None,
        **kwargs,
    ) -> bool:
        """註冊數據集"""
        dataset_entry = {
            "name": name,
            "description": description,
            "schema": schema,
            "owner": owner,
            "tags": tags or [],
            "registered_at": datetime.now().isoformat(),
            "status": "active",
            **kwargs,
        }

        # 檢查是否已存在
        for i, ds in enumerate(self.catalog.get("datasets", [])):
            if ds.get("name") == name:
                self.catalog["datasets"][i] = dataset_entry
                logger.info(f"🔄 更新數據集: {name}")
                return self._save_catalog()

        # 新增
        if "datasets" not in self.catalog:
            self.catalog["datasets"] = []

        self.catalog["datasets"].append(dataset_entry)
        logger.info(f"✅ 註冊數據集: {name}")
        return self._save_catalog()

    def list_datasets(self, owner: str = None, tags: List[str] = None) -> List[Dict]:
        """列出數據集"""
        datasets = self.catalog.get("datasets", [])

        if owner:
            datasets = [ds for ds in datasets if ds.get("owner") == owner]

        if tags:
            datasets = [
                ds for ds in datasets if any(tag in ds.get("tags", []) for tag in tags)
            ]

        return datasets

    def get_dataset(self, name: str) -> Optional[Dict]:
        """取得數據集資訊"""
        for dataset in self.catalog.get("datasets", []):
            if dataset.get("name") == name:
                return dataset
        return None

    def validate_schemas(self) -> Dict[str, Any]:
        """驗證所有數據集 Schema"""
        results = {"total": 0, "valid": 0, "invalid": 0, "issues": []}

        for dataset in self.catalog.get("datasets", []):
            results["total"] += 1

            schema = dataset.get("schema", {})
            if not schema:
                results["invalid"] += 1
                results["issues"].append(f"{dataset.get('name')}: 缺少 schema")
            elif not isinstance(schema, dict):
                results["invalid"] += 1
                results["issues"].append(f"{dataset.get('name')}: schema 格式錯誤")
            else:
                results["valid"] += 1

        return results


class DataCatalogTask(Task):
    """數據目錄管理任務"""

    name = "數據目錄管理"
    priority = 5

    def __init__(self):
        super().__init__()
        self.manager = DataCatalogManager()

    def execute(self):
        """執行數據目錄維護"""
        logger.info("🔍 檢查數據目錄...")

        # 列出所有數據集
        all_datasets = self.manager.list_datasets()
        logger.info(f"📊 數據集總數: {len(all_datasets)}")

        # 驗證 Schema
        validation = self.manager.validate_schemas()
        logger.info(f"🔬 Schema 驗證:")
        logger.info(f"  總計: {validation['total']}")
        logger.info(f"  ✓ 有效: {validation['valid']}")
        logger.info(f"  ✗ 無效: {validation['invalid']}")

        if validation["issues"]:
            logger.warning(f"⚠️  發現問題:")
            for issue in validation["issues"][:5]:
                logger.warning(f"  - {issue}")

        # 按擁有者分組
        owners = {}
        for ds in all_datasets:
            owner = ds.get("owner", "unknown")
            owners[owner] = owners.get(owner, 0) + 1

        logger.info(f"👥 擁有者分布:")
        for owner, count in sorted(owners.items(), key=lambda x: x[1], reverse=True)[
            :5
        ]:
            logger.info(f"  - {owner}: {count} 個數據集")


# 註冊任務：每天檢查一次
executor.register(DataCatalogTask, cron="0 11 * * *", priority=5)

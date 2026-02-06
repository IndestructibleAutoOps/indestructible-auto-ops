"""註冊表同步任務

用途: 同步所有註冊表數據，確保一致性
整合: 跨註冊表數據驗證和同步
"""

import logging
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
from auto_executor import Task, executor
from event_bus import event_bus

logger = logging.getLogger(__name__)


class RegistrySynchronizer:
    """註冊表同步器"""

    def __init__(self, registries_dir: str = "tasks/registries"):
        """初始化同步器"""
        self.registries_dir = Path(registries_dir)
        self.registries = {}

    def load_all_registries(self) -> Dict[str, Any]:
        """加載所有註冊表"""
        loaded = {}

        if not self.registries_dir.exists():
            logger.warning(f"⚠️  註冊表目錄不存在: {self.registries_dir}")
            return loaded

        # 加載 JSON 註冊表
        for json_file in self.registries_dir.glob("*.json"):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    loaded[json_file.stem] = json.load(f)
                logger.info(f"  ✓ {json_file.name}")
            except Exception as e:
                logger.error(f"  ✗ {json_file.name}: {e}")

        # 加載 YAML 註冊表
        for yaml_file in self.registries_dir.glob("*.yaml"):
            try:
                with open(yaml_file, "r", encoding="utf-8") as f:
                    loaded[yaml_file.stem] = yaml.safe_load(f)
                logger.info(f"  ✓ {yaml_file.name}")
            except Exception as e:
                logger.error(f"  ✗ {yaml_file.name}: {e}")

        self.registries = loaded
        return loaded

    def validate_consistency(self) -> Dict[str, Any]:
        """驗證註冊表一致性"""
        results = {
            "consistent": True,
            "issues": [],
            "warnings": [],
            "registry_count": len(self.registries),
        }

        # 檢查每個註冊表的基本結構
        for name, registry in self.registries.items():
            if not isinstance(registry, dict):
                results["issues"].append(f"{name}: 格式錯誤（不是字典）")
                results["consistent"] = False
                continue

            # 檢查元數據
            if "metadata" not in registry:
                results["warnings"].append(f"{name}: 缺少 metadata")

            # 檢查是否為空
            if not registry or len(registry) <= 1:  # 只有 metadata
                results["warnings"].append(f"{name}: 註冊表為空")

        return results

    def generate_sync_report(self) -> str:
        """生成同步報告"""
        report_lines = [
            "=" * 60,
            "註冊表同步報告",
            "=" * 60,
            f"生成時間: {datetime.now().isoformat()}",
            f"註冊表數量: {len(self.registries)}",
            "",
        ]

        for name, registry in self.registries.items():
            report_lines.append(f"📋 {name}:")

            if isinstance(registry, dict):
                # 計算項目數
                item_count = 0
                for key, value in registry.items():
                    if isinstance(value, list):
                        item_count += len(value)

                report_lines.append(f"  - 項目數: {item_count}")

                if "metadata" in registry:
                    metadata = registry["metadata"]
                    if "version" in metadata:
                        report_lines.append(f"  - 版本: {metadata['version']}")
                    if "updated" in metadata:
                        report_lines.append(f"  - 更新: {metadata['updated']}")

            report_lines.append("")

        return "\n".join(report_lines)


class RegistrySyncTask(Task):
    """註冊表同步任務"""

    name = "註冊表同步"
    priority = 6

    def __init__(self):
        super().__init__()
        self.synchronizer = RegistrySynchronizer()

    def execute(self):
        """執行註冊表同步"""
        logger.info("🔄 開始同步註冊表...")

        # 加載所有註冊表
        registries = self.synchronizer.load_all_registries()
        logger.info(f"📂 已加載 {len(registries)} 個註冊表")

        # 驗證一致性
        validation = self.synchronizer.validate_consistency()

        if validation["issues"]:
            logger.error(f"❌ 發現 {len(validation['issues'])} 個問題:")
            for issue in validation["issues"]:
                logger.error(f"  - {issue}")

            # 觸發警報事件
            event_bus.emit("registry_error", issues=validation["issues"])

        if validation["warnings"]:
            logger.warning(f"⚠️  發現 {len(validation['warnings'])} 個警告:")
            for warning in validation["warnings"]:
                logger.warning(f"  - {warning}")

        if validation["consistent"]:
            logger.info("✅ 所有註冊表一致性驗證通過")

        # 生成同步報告
        report = self.synchronizer.generate_sync_report()
        logger.info("\n" + report)

        # 保存報告
        report_path = Path("logs/registry-sync-report.txt")
        report_path.parent.mkdir(exist_ok=True)
        report_path.write_text(report)
        logger.info(f"📄 同步報告已保存: {report_path}")


# 註冊任務：每 12 小時同步一次
executor.register(RegistrySyncTask, interval=43200, priority=6)

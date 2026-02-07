"""註冊表備份任務

用途: 定期備份所有註冊表數據
整合: 跨註冊表備份策略
"""

import logging
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
from auto_executor import Task, executor

logger = logging.getLogger(__name__)


class RegistryBackupManager:
    """註冊表備份管理器"""

    def __init__(
        self,
        registries_dir: str = "tasks/registries",
        backup_dir: str = "backups/registries",
    ):
        """初始化備份管理器"""
        self.registries_dir = Path(registries_dir)
        self.backup_dir = Path(backup_dir)

    def create_backup(self) -> Dict[str, Any]:
        """創建備份"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / timestamp

        results = {
            "timestamp": timestamp,
            "backup_path": str(backup_path),
            "files_backed_up": 0,
            "total_size": 0,
            "errors": [],
        }

        try:
            # 創建備份目錄
            backup_path.mkdir(parents=True, exist_ok=True)

            # 備份所有註冊表文件
            if self.registries_dir.exists():
                for file in self.registries_dir.rglob("*"):
                    if file.is_file() and not file.name.startswith("."):
                        try:
                            # 保持目錄結構
                            relative_path = file.relative_to(self.registries_dir)
                            dest_path = backup_path / relative_path
                            dest_path.parent.mkdir(parents=True, exist_ok=True)

                            shutil.copy2(file, dest_path)
                            results["files_backed_up"] += 1
                            results["total_size"] += file.stat().st_size
                        except Exception as e:
                            results["errors"].append(f"{file.name}: {e}")

            # 保存備份元數據
            metadata = {
                "created_at": datetime.now().isoformat(),
                "files_count": results["files_backed_up"],
                "total_size_bytes": results["total_size"],
                "source": str(self.registries_dir),
            }

            metadata_path = backup_path / "backup_metadata.json"
            with open(metadata_path, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)

            logger.info(f"✅ 備份完成: {backup_path}")

        except Exception as e:
            logger.error(f"❌ 備份失敗: {e}")
            results["errors"].append(str(e))

        return results

    def cleanup_old_backups(self, keep_days: int = 30) -> int:
        """清理舊備份"""
        if not self.backup_dir.exists():
            return 0

        removed_count = 0
        cutoff_time = datetime.now().timestamp() - (keep_days * 86400)

        for backup_folder in self.backup_dir.iterdir():
            if backup_folder.is_dir():
                try:
                    folder_time = backup_folder.stat().st_mtime
                    if folder_time < cutoff_time:
                        shutil.rmtree(backup_folder)
                        removed_count += 1
                        logger.info(f"🗑️  移除舊備份: {backup_folder.name}")
                except Exception as e:
                    logger.error(f"移除備份失敗 {backup_folder.name}: {e}")

        return removed_count

    def list_backups(self) -> List[Dict[str, Any]]:
        """列出所有備份"""
        backups = []

        if not self.backup_dir.exists():
            return backups

        for backup_folder in sorted(self.backup_dir.iterdir(), reverse=True):
            if backup_folder.is_dir():
                metadata_path = backup_folder / "backup_metadata.json"

                if metadata_path.exists():
                    try:
                        with open(metadata_path, "r", encoding="utf-8") as f:
                            metadata = json.load(f)
                        backups.append(
                            {
                                "name": backup_folder.name,
                                "path": str(backup_folder),
                                **metadata,
                            }
                        )
                    except Exception as e:
                        logger.error(f"讀取備份元數據失敗 {backup_folder.name}: {e}")

        return backups


class RegistryBackupTask(Task):
    """註冊表備份任務"""

    name = "註冊表備份"
    priority = 2  # 高優先級（數據保護）

    def __init__(self):
        super().__init__()
        self.backup_manager = RegistryBackupManager()

    def execute(self):
        """執行註冊表備份"""
        logger.info("💾 開始備份註冊表...")

        # 創建備份
        results = self.backup_manager.create_backup()

        logger.info(f"📦 備份結果:")
        logger.info(f"  備份時間: {results['timestamp']}")
        logger.info(f"  檔案數: {results['files_backed_up']}")
        logger.info(f"  總大小: {results['total_size'] / 1024:.1f} KB")

        if results["errors"]:
            logger.error(f"❌ 備份錯誤 ({len(results['errors'])}):")
            for error in results["errors"]:
                logger.error(f"  - {error}")
        else:
            logger.info("✅ 備份完成，無錯誤")

        # 清理舊備份（保留 30 天）
        removed = self.backup_manager.cleanup_old_backups(keep_days=30)
        if removed > 0:
            logger.info(f"🗑️  清理了 {removed} 個舊備份")

        # 列出現有備份
        backups = self.backup_manager.list_backups()
        logger.info(f"📚 現有備份數: {len(backups)}")
        if backups:
            logger.info(f"  最新備份: {backups[0]['name']}")


# 註冊任務：每天凌晨 3 點備份
executor.register(RegistryBackupTask, cron="0 3 * * *", priority=2)

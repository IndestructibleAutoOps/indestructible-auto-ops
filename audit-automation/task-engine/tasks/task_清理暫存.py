"""清理暫存檔案任務"""

import logging
from auto_executor import Task, executor

logger = logging.getLogger(__name__)


class CleanTempTask(Task):
    """清理暫存檔案任務"""

    name = "清理暫存"
    priority = 8  # 低優先級

    def execute(self):
        """執行清理"""
        logger.info("🗑️  開始清理暫存檔案...")

        # 實際清理邏輯
        # import shutil
        # shutil.rmtree("/tmp/cache")

        logger.info("✅ 清理完成")


# 註冊任務：每小時執行一次
executor.register(CleanTempTask, interval=3600, priority=8)

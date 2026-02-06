"""每日備份任務"""

import logging
from datetime import datetime
from auto_executor import Task, executor

logger = logging.getLogger(__name__)


class DailyBackupTask(Task):
    """每日備份任務"""

    name = "每日備份"
    priority = 1  # 最高優先級

    def execute(self):
        """執行備份"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        logger.info(f"📦 開始備份... [{timestamp}]")

        # 實際備份邏輯
        # import shutil
        # shutil.copytree("/data", f"/backup/data_{timestamp}")

        logger.info("✅ 備份完成")


# 註冊任務：每天凌晨 2 點執行
executor.register(DailyBackupTask, cron="0 2 * * *", priority=1)

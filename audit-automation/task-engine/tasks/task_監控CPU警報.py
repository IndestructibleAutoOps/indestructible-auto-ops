"""監控 CPU 使用率並觸發警報"""

import logging
from auto_executor import Task, executor
from event_bus import event_bus

logger = logging.getLogger(__name__)


class CpuMonitorTask(Task):
    """CPU 監控任務"""

    name = "CPU監控"
    priority = 2  # 高優先級

    def execute(self):
        """執行監控"""
        # 模擬 CPU 檢查
        # import psutil
        # cpu_usage = psutil.cpu_percent(interval=1)
        cpu_usage = 75  # 模擬值

        logger.info(f"🖥️  CPU 使用率：{cpu_usage}%")

        if cpu_usage > 80:
            logger.warning(f"⚠️  CPU 使用率過高：{cpu_usage}%")
            event_bus.emit("high_cpu", cpu_usage)


# 註冊任務：每 5 分鐘檢查一次
executor.register(CpuMonitorTask, interval=300, priority=2)


# 綁定事件處理器
def handle_high_cpu(cpu_usage):
    """處理高 CPU 警報"""
    logger.error(f"🚨 警報！CPU 使用率：{cpu_usage}%")
    # 發送通知、觸發自動擴容等...


event_bus.on("high_cpu", handle_high_cpu)

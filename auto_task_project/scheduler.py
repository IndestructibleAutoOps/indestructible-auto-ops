"""APScheduler 排程系統（cron + interval）"""
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


def start_scheduler():
    """啟動排程器"""
    from auto_executor import executor
    
    for task_info in executor.get_all_tasks():
        instance = task_info["instance"]
        task_name = instance.name
        
        # 添加 interval 觸發器
        if task_info["interval"]:
            scheduler.add_job(
                instance.execute,
                trigger=IntervalTrigger(seconds=task_info["interval"]),
                id=f"{task_name}_interval",
                name=task_name,
                replace_existing=True
            )
            logger.info(f"⏰ 排程（間隔）：{task_name} 每 {task_info['interval']} 秒")
        
        # 添加 cron 觸發器
        if task_info["cron"]:
            scheduler.add_job(
                instance.execute,
                trigger=CronTrigger.from_crontab(task_info["cron"]),
                id=f"{task_name}_cron",
                name=task_name,
                replace_existing=True
            )
            logger.info(f"⏰ 排程（cron）：{task_name} → {task_info['cron']}")
    
    scheduler.start()
    logger.info("✅ APScheduler 已啟動")

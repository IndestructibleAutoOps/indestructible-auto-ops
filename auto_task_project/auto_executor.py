"""核心：Task、register、優先級執行"""
import importlib
import logging
from pathlib import Path
from typing import Any, Dict, List, Type

logger = logging.getLogger(__name__)


class Task:
    """任務基類"""
    
    name: str = "未命名任務"
    priority: int = 5  # 1=最高 10=最低
    
    def execute(self):
        """執行任務（子類必須實作）"""
        raise NotImplementedError(f"{self.__class__.__name__} 必須實作 execute()")


class TaskExecutor:
    """任務執行器"""
    
    def __init__(self):
        self.tasks: List[Dict[str, Any]] = []
    
    def register(
        self,
        task_class: Type[Task],
        interval: int = None,
        cron: str = None,
        priority: int = 5
    ):
        """
        註冊任務
        
        Args:
            task_class: 任務類別
            interval: 間隔秒數（可選）
            cron: Cron 表達式（可選）
            priority: 優先級 1-10
        """
        task_info = {
            "class": task_class,
            "interval": interval,
            "cron": cron,
            "priority": priority,
            "instance": task_class()
        }
        self.tasks.append(task_info)
        logger.info(
            f"✅ 註冊任務：{task_class.__name__} "
            f"[優先級={priority}, interval={interval}, cron={cron}]"
        )
    
    def execute_all(self):
        """執行所有任務（按優先級排序）"""
        sorted_tasks = sorted(self.tasks, key=lambda x: x["priority"])
        
        logger.info(f"🚀 開始執行 {len(sorted_tasks)} 個任務...")
        for task_info in sorted_tasks:
            try:
                instance = task_info["instance"]
                logger.info(f"▶️  執行：{instance.name} [優先級={task_info['priority']}]")
                instance.execute()
                logger.info(f"✅ 完成：{instance.name}")
            except Exception as e:
                logger.error(f"❌ 任務失敗 {instance.name}: {e}")
    
    def auto_discover(self, tasks_dir: str = "tasks"):
        """
        自動發現並載入 tasks/ 目錄下的所有任務
        
        Args:
            tasks_dir: 任務目錄名稱
        """
        tasks_path = Path(tasks_dir)
        if not tasks_path.exists():
            logger.warning(f"⚠️  任務目錄不存在：{tasks_dir}")
            return
        
        logger.info(f"🔍 自動發現任務：{tasks_dir}/")
        
        for py_file in tasks_path.glob("task_*.py"):
            module_name = f"{tasks_dir}.{py_file.stem}"
            try:
                importlib.import_module(module_name)
                logger.info(f"  ✓ 載入：{module_name}")
            except Exception as e:
                logger.error(f"  ✗ 載入失敗 {module_name}: {e}")
    
    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """取得所有已註冊任務"""
        return self.tasks


# 全域執行器實例
executor = TaskExecutor()

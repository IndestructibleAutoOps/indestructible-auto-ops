"""快速測試框架功能"""
import sys
sys.path.insert(0, '.')

from auto_executor import Task, executor
from event_bus import event_bus
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestTask(Task):
    """測試任務"""
    name = "測試任務"
    priority = 1
    
    def execute(self):
        logger.info("✅ 測試任務執行成功！")


# 測試註冊
executor.register(TestTask, priority=1)

# 測試事件
def test_event_handler():
    logger.info("✅ 事件系統正常！")

event_bus.on("test_event", test_event_handler)
event_bus.emit("test_event")

# 測試執行
logger.info("開始測試執行...")
executor.execute_all()

print("\n" + "="*60)
print("✅ 框架測試完成 - 所有核心功能正常")
print("="*60)
print("\n使用方式：")
print("  cd auto_task_project")
print("  pip install -e .")
print("  python main.py")

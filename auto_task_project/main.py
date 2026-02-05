"""總入口（永遠不改）"""
import time
from auto_executor import executor
from logger import setup_logger
from scheduler import start_scheduler
from event_bus import event_bus

if __name__ == "__main__":
    setup_logger()
    executor.auto_discover("tasks")
    executor.execute_all()  # 啟動時按優先級跑一次
    start_scheduler()

    # 範例：綁定事件（可任意加）
    # event_bus.on("high_cpu", lambda: print("CPU 警報！"))

    print("✅ 系統完全啟動（APScheduler + 事件 + 優先級 + 日誌寫檔案）")
    print("   Ctrl+C 結束")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n關閉中...")

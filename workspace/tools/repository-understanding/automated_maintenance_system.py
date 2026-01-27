#!/usr/bin/env python3
"""
完全自動化的維護系統
在每次工作中自動偵測並維護儲存庫理解系統
"""

import subprocess
import threading
import time
import logging

logger = logging.getLogger(__name__)
from datetime import datetime
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class AutoMaintenanceSystem:
    def __init__(self, watch_path='.'):
        self.watch_path = Path(watch_path)
        self.last_scan_time = None
        self.change_detected = False
        self.maintenance_interval = 300  # 5分鐘
        self.observer = None
        self.running = False

    def start_background_monitoring(self):
        """啟動背景監控"""
        logger.info("🔍 啟動自動維護系統...")

        # 創建檔案系統監控器
        event_handler = MaintenanceEventHandler(self)
        self.observer = Observer()
        self.observer.schedule(event_handler, str(self.watch_path), recursive=True)
        self.observer.start()

        # 啟動定期維護線程
        self.running = True
        maintenance_thread = threading.Thread(target=self.periodic_maintenance)
        maintenance_thread.daemon = True
        maintenance_thread.start()

        logger.info("✅ 自動維護系統已啟動")
        logger.info(f"📁 監控路徑: {self.watch_path}")
        logger.info(f"⏰ 維護間隔: {self.maintenance_interval} 秒")

    def stop_background_monitoring(self):
        """停止背景監控"""
        self.running = False
        if self.observer:
            self.observer.stop()
            self.observer.join()
        logger.info("🛑 自動維護系統已停止")

    def periodic_maintenance(self):
        """定期執行維護任務"""
        while self.running:
            try:
                time.sleep(self.maintenance_interval)

                if self.change_detected:
                    logger.info(f"\n🔄 [{datetime.now()
                    self.perform_automatic_maintenance()
                    self.change_detected = False

            except Exception as e:
                logger.info(f"❌ 維護過程中發生錯誤: {e}")

    def perform_automatic_maintenance(self):
        """執行自動維護"""
        try:
            # 1. 重新掃描儲存庫
            logger.info("📊 重新掃描儲存庫...")
            subprocess.run(['python3', 'phase1_scanner.py'],
                          capture_output=True, text=True)

            # 2. 驗證操作檢查機制
            logger.info("🛡️  驗證操作檢查機制...")
            subprocess.run(['python3', 'phase2_operation_checker.py'],
                          capture_output=True, text=True)

            # 3. 更新查詢系統
            logger.info("🔍 更新查詢系統...")
            subprocess.run(['python3', 'phase3_visualizer.py'],
                          capture_output=True, text=True)

            # 4. 執行學習系統
            logger.info("🧠 執行學習系統...")
            subprocess.run(['python3', 'phase4_learning_system.py'],
                          capture_output=True, text=True)

            self.last_scan_time = datetime.now()
            logger.info(f"✅ 自動維護完成於 {self.last_scan_time.strftime('%H:%M:%S')

        except Exception as e:
            logger.info(f"❌ 自動維護失敗: {e}")

    def trigger_maintenance_now(self):
        """立即觸發維護"""
        logger.info("🚨 手動觸發維護...")
        self.perform_automatic_maintenance()

    def get_status(self):
        """獲取系統狀態"""
        return {
            'running': self.running,
            'last_scan': self.last_scan_time.isoformat() if self.last_scan_time else None,
            'changes_detected': self.change_detected,
            'watch_path': str(self.watch_path)
        }


class MaintenanceEventHandler(FileSystemEventHandler):
    """檔案系統變化事件處理器"""

    def __init__(self, maintenance_system):
        self.maintenance_system = maintenance_system
        self.ignore_patterns = ['__', '.git', 'node_modules', '__pycache__',
                               '.pyc', 'phase', 'knowledge_base', 'backup']

    def on_modified(self, event):
        """檔案修改事件"""
        if self.should_ignore(event.src_path):
            return

        logger.info(f"📝 檢測到修改: {Path(event.src_path)
        self.maintenance_system.change_detected = True

    def on_created(self, event):
        """檔案創建事件"""
        if self.should_ignore(event.src_path) or event.is_directory:
            return

        logger.info(f"🆕 檢測到新檔案: {Path(event.src_path)
        self.maintenance_system.change_detected = True

    def on_deleted(self, event):
        """檔案刪除事件"""
        if self.should_ignore(event.src_path) or event.is_directory:
            return

        logger.info(f"🗑️  檢測到刪除: {Path(event.src_path)
        self.maintenance_system.change_detected = True

    def should_ignore(self, path):
        """判斷是否應忽略此路徑"""
        path_str = path.lower()
        return any(pattern in path_str for pattern in self.ignore_patterns)


def start_auto_maintenance_daemon():
    """啟動自動維護守護進程"""
    logger.info("="*60)
    logger.info("🤖 自動化維護系統守護進程")
    logger.info("="*60)

    maintenance_system = AutoMaintenanceSystem()
    maintenance_system.start_background_monitoring()

    try:
        logger.info("\n系統正在運行，按 Ctrl+C 停止...")
        while True:
            time.sleep(1)

            # 顯示狀態（每60秒一次）
            status = maintenance_system.get_status()
            if status['running']:
                current_time = datetime.now().strftime('%H:%M:%S')
                status_msg = "📊 狀態: 運行中 | "
                status_msg += f"最後掃描: {status['last_scan'] or '尚未掃描'} | "
                status_msg += f"變化待處理: {'是' if status['changes_detected'] else '否'}"
                logger.info(f"\r[{current_time}] {status_msg}", end='', flush=True)

    except KeyboardInterrupt:
        logger.info("\n\n收到停止信號...")
        maintenance_system.stop_background_monitoring()
        logger.info("✅ 系統已正常停止")
    except Exception as e:
        logger.info(f"\n❌ 發生錯誤: {e}")
        maintenance_system.stop_background_monitoring()


if __name__ == '__main__':
    # 檢查是否安裝了 watchdog
    try:
        import watchdog
    except ImportError:
        logger.info("❌ 需要安裝 watchdog 套件")
        logger.info("請執行: pip install watchdog")
        exit(1)

    start_auto_maintenance_daemon()

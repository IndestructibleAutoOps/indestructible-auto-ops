#!/usr/bin/env python3
"""
重構執行器 - 執行重構操作的主要工具
"""

import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import logging

from whitelist_manager import WhitelistManager


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)


class RefactorExecutor:
    """重構執行器"""
    
    def __init__(self, workspace: Path, whitelist_path: Path):
        self.workspace = workspace
        self.whitelist = WhitelistManager(whitelist_path)
        self.operations: List[Dict] = []
        self.rollback_ops: List[Dict] = []
    
    def add_operation(self, op_type: str, source: str, target: Optional[str] = None, 
                      reason: str = ""):
        """添加操作記錄"""
        operation = {
            "type": op_type,
            "source": source,
            "target": target,
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
            "status": "pending"
        }
        self.operations.append(operation)
        logger.info(f"➕ 添加操作: {op_type} {source} -> {target}")
        
        # 添加回滾操作
        if op_type == "move":
            self.rollback_ops.append({
                "type": "move_back",
                "source": target,
                "target": source
            })
        elif op_type == "rename":
            self.rollback_ops.append({
                "type": "rename_back",
                "source": target,
                "target": source
            })
    
    def move_directory(self, source: str, target: str, reason: str = ""):
        """移動目錄"""
        src_path = self.workspace / source
        tgt_path = self.workspace / target
        
        if not src_path.exists():
            logger.warning(f"⚠️  源目錄不存在: {source}")
            return False
        
        # 檢查是否在白名單中
        if self.whitelist.is_whitelisted(src_path.name):
            logger.info(f"⏭️  跳過白名單項目: {source}")
            return True
        
        try:
            # 創建目標目錄
            tgt_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 移動目錄
            shutil.move(str(src_path), str(tgt_path))
            
            self.add_operation("move", source, target, reason)
            logger.info(f"✅ 移動成功: {source} -> {target}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 移動失敗: {source} -> {target}, 錯誤: {e}")
            return False
    
    def rename_directory(self, old_name: str, new_name: str, reason: str = ""):
        """重命名目錄"""
        old_path = self.workspace / old_name
        new_path = self.workspace / new_name
        
        if not old_path.exists():
            logger.warning(f"⚠️  源目錄不存在: {old_name}")
            return False
        
        try:
            old_path.rename(new_path)
            self.add_operation("rename", old_name, new_name, reason)
            logger.info(f"✅ 重命名成功: {old_name} -> {new_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 重命名失敗: {old_name} -> {new_name}, 錯誤: {e}")
            return False
    
    def delete_directory(self, path: str, reason: str = ""):
        """刪除目錄"""
        dir_path = self.workspace / path
        
        if not dir_path.exists():
            logger.warning(f"⚠️  目錄不存在: {path}")
            return True
        
        # 檢查是否在白名單中
        if self.whitelist.is_whitelisted(dir_path.name):
            logger.info(f"⏭️  跳過白名單項目: {path}")
            return True
        
        try:
            # 先備份
            backup_path = self.workspace / "refactor" / "backups" / path.replace("/", "_")
            shutil.copytree(dir_path, backup_path)
            
            # 刪除目錄
            shutil.rmtree(dir_path)
            
            self.add_operation("delete", path, str(backup_path), reason)
            logger.info(f"✅ 刪除成功: {path}（備份至: {backup_path}）")
            return True
            
        except Exception as e:
            logger.error(f"❌ 刪除失敗: {path}, 錯誤: {e}")
            return False
    
    def rollback(self):
        """執行回滾"""
        logger.warning("🔄 開始回滾...")
        
        for op in reversed(self.rollback_ops):
            try:
                if op["type"] == "move_back":
                    src_path = self.workspace / op["source"]
                    tgt_path = self.workspace / op["target"]
                    if src_path.exists():
                        shutil.move(str(src_path), str(tgt_path))
                        logger.info(f"✅ 回滾移動: {op['source']} -> {op['target']}")
                
                elif op["type"] == "rename_back":
                    src_path = self.workspace / op["source"]
                    tgt_path = self.workspace / op["target"]
                    if src_path.exists():
                        src_path.rename(tgt_path)
                        logger.info(f"✅ 回滾重命名: {op['source']} -> {op['target']}")
                
            except Exception as e:
                logger.error(f"❌ 回滾失敗: {op}, 錯誤: {e}")
        
        logger.warning("✅ 回滾完成")
    
    def save_report(self):
        """保存操作報告"""
        report_path = self.workspace / "refactor" / "reports" / f"operations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "operations": self.operations,
            "rollback_operations": self.rollback_ops,
            "total_operations": len(self.operations),
            "successful_operations": len([op for op in self.operations if op["status"] == "completed"])
        }
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📄 操作報告已保存: {report_path}")


def main():
    """測試重構執行器"""
    workspace = Path('/workspace/indestructibleautoops')
    whitelist_path = workspace / 'refactor' / 'tools' / 'whitelist.json'
    
    executor = RefactorExecutor(workspace, whitelist_path)
    
    # 測試操作
    logger.info("🧪 測試重構執行器")
    
    # 創建測試目錄
    test_dir = workspace / "test_dir"
    test_dir.mkdir(exist_ok=True)
    (test_dir / "test.txt").write_text("test")
    
    # 測試重命名
    executor.rename_directory("test_dir", "test_renamed", "測試重命名")
    
    # 測試移動
    executor.move_directory("test_renamed", "refactor/tests/test_moved", "測試移動")
    
    # 保存報告
    executor.save_report()


if __name__ == '__main__':
    main()
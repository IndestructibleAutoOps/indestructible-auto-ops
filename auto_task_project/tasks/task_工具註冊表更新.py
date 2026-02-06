"""工具註冊表更新任務

整合自: ecosystem/tools/update_registry.py
用途: 自動發現並更新工具註冊表
"""
import logging
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
from auto_executor import Task, executor

logger = logging.getLogger(__name__)


class ToolRegistryUpdater:
    """工具註冊表更新器"""
    
    def __init__(self, registry_path: str = None, tools_dir: str = None):
        """初始化更新器"""
        if registry_path is None:
            registry_path = "tasks/registries/tools-registry.json"
        if tools_dir is None:
            tools_dir = "../../ecosystem/tools"  # 相對於 tasks/
        
        self.registry_path = Path(registry_path)
        self.tools_dir = Path(tools_dir)
        self.registry = self._load_registry()
    
    def _load_registry(self) -> Dict[str, Any]:
        """加載註冊表"""
        if not self.registry_path.exists():
            return {
                'tools': [],
                'metadata': {
                    'version': '1.0.0',
                    'last_scan': None,
                    'tool_count': 0
                }
            }
        
        try:
            with open(self.registry_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加載工具註冊表失敗: {e}")
            return {'tools': []}
    
    def _save_registry(self) -> bool:
        """保存註冊表"""
        try:
            self.registry_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 更新元數據
            if 'metadata' not in self.registry:
                self.registry['metadata'] = {}
            
            self.registry['metadata']['last_scan'] = datetime.now().isoformat()
            self.registry['metadata']['tool_count'] = len(self.registry.get('tools', []))
            
            with open(self.registry_path, 'w', encoding='utf-8') as f:
                json.dump(self.registry, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ 工具註冊表已保存: {self.registry_path}")
            return True
        except Exception as e:
            logger.error(f"保存工具註冊表失敗: {e}")
            return False
    
    def scan_tools(self) -> int:
        """掃描工具目錄"""
        if not self.tools_dir.exists():
            logger.warning(f"⚠️  工具目錄不存在: {self.tools_dir}")
            return 0
        
        discovered_tools = []
        
        for py_file in self.tools_dir.rglob("*.py"):
            if py_file.name.startswith("test_") or py_file.name == "__init__.py":
                continue
            
            tool_info = {
                'name': py_file.stem,
                'path': str(py_file.relative_to(self.tools_dir)),
                'discovered_at': datetime.now().isoformat(),
                'type': 'python_script'
            }
            
            discovered_tools.append(tool_info)
        
        logger.info(f"🔍 發現 {len(discovered_tools)} 個工具")
        
        # 更新註冊表（保留已存在的元數據）
        existing_tools = {t['name']: t for t in self.registry.get('tools', [])}
        
        for tool in discovered_tools:
            if tool['name'] in existing_tools:
                # 保留元數據，更新路徑
                existing_tools[tool['name']]['path'] = tool['path']
                existing_tools[tool['name']]['last_seen'] = tool['discovered_at']
            else:
                # 新工具
                existing_tools[tool['name']] = tool
        
        self.registry['tools'] = list(existing_tools.values())
        
        return len(discovered_tools)
    
    def get_tool_stats(self) -> Dict[str, Any]:
        """取得工具統計"""
        tools = self.registry.get('tools', [])
        
        stats = {
            'total': len(tools),
            'by_type': {}
        }
        
        for tool in tools:
            tool_type = tool.get('type', 'unknown')
            stats['by_type'][tool_type] = stats['by_type'].get(tool_type, 0) + 1
        
        return stats


class ToolRegistryUpdateTask(Task):
    """工具註冊表更新任務"""
    
    name = "工具註冊表更新"
    priority = 5
    
    def __init__(self):
        super().__init__()
        self.updater = ToolRegistryUpdater()
    
    def execute(self):
        """執行註冊表更新"""
        logger.info("🔄 更新工具註冊表...")
        
        # 掃描工具
        discovered = self.updater.scan_tools()
        
        # 保存更新
        if self.updater._save_registry():
            logger.info(f"✅ 工具註冊表更新完成: {discovered} 個工具")
        
        # 顯示統計
        stats = self.updater.get_tool_stats()
        logger.info(f"📊 工具統計:")
        logger.info(f"  總計: {stats['total']}")
        for tool_type, count in stats['by_type'].items():
            logger.info(f"  - {tool_type}: {count}")


# 註冊任務：每 6 小時更新一次
executor.register(ToolRegistryUpdateTask, interval=21600, priority=5)

"""命名規範註冊表管理任務

整合自: ecosystem/registry/naming/
用途: 管理 GL 命名規範、驗證命名合規性
"""
import logging
import yaml
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
from auto_executor import Task, executor

logger = logging.getLogger(__name__)


class NamingRegistryManager:
    """命名規範註冊表管理器"""
    
    def __init__(self, registry_path: str = None):
        """初始化管理器"""
        if registry_path is None:
            registry_path = "tasks/registries/naming/gl-naming-contracts-registry.yaml"
        
        self.registry_path = Path(registry_path)
        self.naming_rules = self._load_registry()
    
    def _load_registry(self) -> Dict[str, Any]:
        """加載命名規範註冊表"""
        if not self.registry_path.exists():
            return {
                'naming_rules': [],
                'patterns': {},
                'metadata': {
                    'version': '1.0.0',
                    'updated': datetime.now().isoformat()
                }
            }
        
        try:
            with open(self.registry_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                return data or {'naming_rules': []}
        except Exception as e:
            logger.error(f"加載命名規範註冊表失敗: {e}")
            return {'naming_rules': []}
    
    def validate_name(self, name: str, component_type: str = "module") -> Dict[str, Any]:
        """驗證名稱是否符合規範"""
        result = {
            'valid': True,
            'violations': [],
            'suggestions': []
        }
        
        rules = self.naming_rules.get('naming_rules', [])
        patterns = self.naming_rules.get('patterns', {})
        
        # 基本檢查
        if not name:
            result['valid'] = False
            result['violations'].append("名稱不能為空")
            return result
        
        # 檢查命名格式（kebab-case for GL modules）
        if component_type == "gl_module":
            if not all(c.islower() or c == '-' or c.isdigit() for c in name):
                result['valid'] = False
                result['violations'].append("GL 模組必須使用 kebab-case（小寫+連字號）")
                result['suggestions'].append(f"建議: {name.lower().replace('_', '-').replace('.', '-')}")
        
        # 檢查 GL 前綴
        if component_type == "gl_module" and not name.startswith('gl-'):
            result['violations'].append("GL 模組建議使用 'gl-' 前綴")
            result['suggestions'].append(f"建議: gl-{name}")
        
        return result
    
    def get_naming_statistics(self) -> Dict[str, Any]:
        """取得命名規範統計"""
        return {
            'total_rules': len(self.naming_rules.get('naming_rules', [])),
            'total_patterns': len(self.naming_rules.get('patterns', {})),
            'registry_path': str(self.registry_path),
            'last_updated': self.naming_rules.get('metadata', {}).get('updated', 'unknown')
        }


class NamingRegistryTask(Task):
    """命名規範註冊表管理任務"""
    
    name = "命名規範註冊表"
    priority = 6
    
    def __init__(self):
        super().__init__()
        self.manager = NamingRegistryManager()
    
    def execute(self):
        """執行命名規範檢查"""
        logger.info("🔍 檢查命名規範註冊表...")
        
        # 統計資訊
        stats = self.manager.get_naming_statistics()
        logger.info(f"📊 命名規範統計:")
        logger.info(f"  規則數: {stats['total_rules']}")
        logger.info(f"  模式數: {stats['total_patterns']}")
        logger.info(f"  更新時間: {stats['last_updated']}")
        
        # 測試驗證功能
        test_cases = [
            ("gl-runtime-engine", "gl_module"),
            ("GL_RUNTIME_ENGINE", "gl_module"),
            ("runtime.engine", "gl_module"),
        ]
        
        logger.info("🧪 測試命名驗證:")
        for name, comp_type in test_cases:
            validation = self.manager.validate_name(name, comp_type)
            status = "✅" if validation['valid'] else "❌"
            logger.info(f"  {status} {name}: {'符合' if validation['valid'] else '不符合'}")
            
            if validation['violations']:
                for violation in validation['violations']:
                    logger.info(f"      違規: {violation}")
            
            if validation['suggestions']:
                for suggestion in validation['suggestions']:
                    logger.info(f"      建議: {suggestion}")


# 註冊任務：每天檢查一次
executor.register(NamingRegistryTask, cron="0 9 * * *", priority=6)

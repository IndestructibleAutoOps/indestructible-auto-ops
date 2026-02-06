"""註冊表驗證任務

整合自: scripts/validate_module_registry.py
用途: 驗證所有註冊表的完整性和合規性
"""
import logging
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
from auto_executor import Task, executor

logger = logging.getLogger(__name__)


class RegistryValidator:
    """註冊表驗證器"""
    
    def __init__(self, registries_dir: str = "tasks/registries"):
        """初始化驗證器"""
        self.registries_dir = Path(registries_dir)
        self.validation_rules = {
            'required_fields': ['name', 'version'],
            'required_metadata': ['updated', 'version'],
            'valid_statuses': ['active', 'inactive', 'deprecated']
        }
    
    def validate_all(self) -> Dict[str, Any]:
        """驗證所有註冊表"""
        results = {
            'total_registries': 0,
            'passed': 0,
            'failed': 0,
            'details': []
        }
        
        if not self.registries_dir.exists():
            logger.warning(f"⚠️  註冊表目錄不存在: {self.registries_dir}")
            return results
        
        # 驗證所有註冊表文件
        registry_files = list(self.registries_dir.glob("*.json")) + list(self.registries_dir.glob("*.yaml"))
        results['total_registries'] = len(registry_files)
        
        for registry_file in registry_files:
            validation = self._validate_single_registry(registry_file)
            results['details'].append(validation)
            
            if validation['passed']:
                results['passed'] += 1
            else:
                results['failed'] += 1
        
        return results
    
    def _validate_single_registry(self, registry_file: Path) -> Dict[str, Any]:
        """驗證單個註冊表"""
        result = {
            'file': registry_file.name,
            'passed': True,
            'errors': [],
            'warnings': []
        }
        
        try:
            # 加載文件
            if registry_file.suffix == '.json':
                with open(registry_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:  # .yaml
                with open(registry_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
            
            if not isinstance(data, dict):
                result['errors'].append("不是有效的字典格式")
                result['passed'] = False
                return result
            
            # 檢查元數據
            if 'metadata' not in data:
                result['warnings'].append("缺少 metadata 區塊")
            else:
                metadata = data['metadata']
                for field in self.validation_rules['required_metadata']:
                    if field not in metadata:
                        result['warnings'].append(f"metadata 缺少 {field}")
            
            # 檢查是否為空
            item_count = sum(len(v) for v in data.values() if isinstance(v, list))
            if item_count == 0:
                result['warnings'].append("註冊表為空")
            
            # 驗證項目
            for key, value in data.items():
                if isinstance(value, list):
                    for i, item in enumerate(value):
                        if isinstance(item, dict):
                            # 檢查必要欄位
                            if 'name' not in item:
                                result['errors'].append(f"{key}[{i}] 缺少 name 欄位")
                                result['passed'] = False
            
        except json.JSONDecodeError as e:
            result['errors'].append(f"JSON 解析錯誤: {e}")
            result['passed'] = False
        except yaml.YAMLError as e:
            result['errors'].append(f"YAML 解析錯誤: {e}")
            result['passed'] = False
        except Exception as e:
            result['errors'].append(f"驗證失敗: {e}")
            result['passed'] = False
        
        return result
    
    def generate_validation_report(self, results: Dict[str, Any]) -> str:
        """生成驗證報告"""
        report_lines = [
            "=" * 60,
            "註冊表驗證報告",
            "=" * 60,
            f"驗證時間: {datetime.now().isoformat()}",
            f"總註冊表數: {results['total_registries']}",
            f"✅ 通過: {results['passed']}",
            f"❌ 失敗: {results['failed']}",
            ""
        ]
        
        for detail in results['details']:
            status = "✅" if detail['passed'] else "❌"
            report_lines.append(f"{status} {detail['file']}")
            
            if detail['errors']:
                for error in detail['errors']:
                    report_lines.append(f"    ❌ {error}")
            
            if detail['warnings']:
                for warning in detail['warnings']:
                    report_lines.append(f"    ⚠️  {warning}")
            
            report_lines.append("")
        
        return "\n".join(report_lines)


class RegistryValidationTask(Task):
    """註冊表驗證任務"""
    
    name = "註冊表驗證"
    priority = 4
    
    def __init__(self):
        super().__init__()
        self.validator = RegistryValidator()
    
    def execute(self):
        """執行註冊表驗證"""
        logger.info("🔍 開始驗證註冊表...")
        
        # 執行驗證
        results = self.validator.validate_all()
        
        # 顯示結果
        logger.info(f"📊 驗證結果:")
        logger.info(f"  總計: {results['total_registries']}")
        logger.info(f"  ✅ 通過: {results['passed']}")
        logger.info(f"  ❌ 失敗: {results['failed']}")
        
        # 生成報告
        report = self.validator.generate_validation_report(results)
        
        # 保存報告
        report_path = Path("logs/registry-validation-report.txt")
        report_path.parent.mkdir(exist_ok=True)
        report_path.write_text(report)
        logger.info(f"📄 驗證報告已保存: {report_path}")
        
        # 如果有失敗，觸發警報
        if results['failed'] > 0:
            logger.error(f"❌ 檢測到 {results['failed']} 個註冊表驗證失敗")
            event_bus.emit("registry_validation_failed", results=results)
        else:
            logger.info("✅ 所有註冊表驗證通過")


# 註冊任務：每天驗證一次
executor.register(RegistryValidationTask, cron="0 8 * * *", priority=4)

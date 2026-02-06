#!/usr/bin/env python3
"""
Scan ecosystem for unbound modules
掃描 ecosystem 目錄，識別尚未綁定到 enforce.py 的模組和組件
"""

import os
import re
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Set

@dataclass
class EcosystemModule:
    """生態系統模組"""
    path: str
    module_type: str
    description: str
    imported_in_enforce: bool
    has_main_class: bool
    suggested_check: str = ""

class EcosystemScanner:
    def __init__(self, workspace_path: Path):
        self.workspace_path = workspace_path
        self.ecosystem_path = workspace_path / "ecosystem"
        self.enforce_path = self.ecosystem_path / "enforce.py"
        self.modules: List[EcosystemModule] = []
        
    def load_enforce_py(self) -> str:
        """載入 enforce.py 內容"""
        with open(self.enforce_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def scan_ecosystem_modules(self) -> List[EcosystemModule]:
        """掃描所有 ecosystem 模組"""
        enforce_content = self.load_enforce_py()
        
        # 模組類型定義
        module_categories = {
            'enforcers': {
                'description': '治理強制執行器',
                'check_method': 'check_governance_enforcer',
                'pattern': r'class\s+(\w+Enforcer|Enforcer)'
            },
            'governance': {
                'description': '治理引擎和工具',
                'check_method': 'check_governance_layer',
                'pattern': r'class\s+(\w+Engine|Governance\w+)'
            },
            'reasoning': {
                'description': '推理系統組件',
                'check_method': 'check_reasoning_layer',
                'pattern': r'class\s+(\w+Agent|Reasoner|Arbitrator|Retrieval)'
            },
            'foundation': {
                'description': '基礎層組件',
                'check_method': 'check_foundation_layer',
                'pattern': r'class\s+(\w+Enforcer|DAG)'
            },
            'coordination': {
                'description': '協調層組件',
                'check_method': 'check_coordination_layer',
                'pattern': r'class\s+(\w+Gateway|Dispatcher|Registry|SyncEngine)'
            },
            'tools': {
                'description': '工具腳本',
                'check_method': 'check_tools_layer',
                'pattern': r'def\s+(\w+|main)'
            },
            'validators': {
                'description': '驗證器',
                'check_method': 'check_validators_layer',
                'pattern': r'class\s+\w+Validator'
            },
            'events': {
                'description': '事件處理',
                'check_method': 'check_events_layer',
                'pattern': r'class\s+\w+Emitter'
            }
        }
        
        # 掃描每個類別的模組
        for category, config in module_categories.items():
            category_path = self.ecosystem_path / category
            if not category_path.exists():
                continue
                
            for py_file in category_path.rglob('*.py'):
                if py_file.name.startswith('_'):
                    continue
                    
                module = self.analyze_module(py_file, enforce_content, category, config)
                if module:
                    self.modules.append(module)
        
        return self.modules
    
    def analyze_module(self, py_file: Path, enforce_content: str, 
                       category: str, config: dict) -> EcosystemModule:
        """分析單個模組"""
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return None
        
        rel_path = str(py_file.relative_to(self.workspace_path))
        
        # 檢查是否在 enforce.py 中被導入
        module_name = py_file.stem
        imported = False
        if module_name in enforce_content:
            imported = True
        
        # 檢查是否有主要類
        has_main_class = False
        matches = re.findall(config['pattern'], content)
        if matches:
            has_main_class = True
        
        # 建議的檢查方法
        suggested_check = config['check_method']
        
        return EcosystemModule(
            path=rel_path,
            module_type=category,
            description=config['description'],
            imported_in_enforce=imported,
            has_main_class=has_main_class,
            suggested_check=suggested_check
        )
    
    def generate_report(self) -> str:
        """生成掃描報告"""
        modules = self.scan_ecosystem_modules()
        
        # 分類
        bound_modules = [m for m in modules if m.imported_in_enforce]
        unbound_modules = [m for m in modules if not m.imported_in_enforce]
        unbound_with_class = [m for m in unbound_modules if m.has_main_class]
        
        # 按類型統計
        type_stats: Dict[str, Dict] = {}
        for m in modules:
            if m.module_type not in type_stats:
                type_stats[m.module_type] = {'total': 0, 'bound': 0, 'unbound': 0}
            type_stats[m.module_type]['total'] += 1
            if m.imported_in_enforce:
                type_stats[m.module_type]['bound'] += 1
            else:
                type_stats[m.module_type]['unbound'] += 1
        
        report = []
        report.append("=" * 80)
        report.append("Ecosystem Unbound Modules Scan Report")
        report.append("=" * 80)
        report.append("")
        
        # 摘要
        report.append("## 📊 Summary")
        report.append(f"Total modules scanned: {len(modules)}")
        report.append(f"Modules bound to enforce.py: {len(bound_modules)}")
        report.append(f"Modules NOT bound to enforce.py: {len(unbound_modules)}")
        report.append(f"Unbound modules with main class: {len(unbound_with_class)}")
        report.append("")
        
        # 按類型統計
        report.append("## 📈 Statistics by Module Type")
        report.append("")
        report.append(f"{'Type':<20} {'Total':>8} {'Bound':>8} {'Unbound':>8} {'Coverage':>10}")
        report.append("-" * 60)
        for mtype, stats in sorted(type_stats.items()):
            coverage = f"{(stats['bound']/stats['total']*100):.1f}%" if stats['total'] > 0 else "0%"
            report.append(f"{mtype:<20} {stats['total']:>8} {stats['bound']:>8} {stats['unbound']:>8} {coverage:>10}")
        report.append("")
        
        # 高優先級未綁定模組
        report.append("## 🚨 High Priority Unbound Modules (with main class)")
        report.append("")
        for m in sorted(unbound_with_class, key=lambda x: x.module_type):
            report.append(f"- [{m.module_type.upper()}] {m.path}")
            report.append(f"  Suggested check: {m.suggested_check}")
            report.append(f"  Description: {m.description}")
            report.append("")
        
        # 所有未綁定模組
        report.append("## 📋 All Unbound Modules")
        report.append("")
        for m in sorted(unbound_modules, key=lambda x: (x.module_type, x.path)):
            status = "🔴" if m.has_main_class else "⚪"
            report.append(f"{status} [{m.module_type.upper()}] {m.path}")
        
        # 建議
        report.append("")
        report.append("## 💡 Recommendations")
        report.append("")
        report.append("1. **Priority 1**: Bind all modules with main classes to enforce.py")
        report.append("2. **Priority 2**: Add checks for foundation and coordination layers")
        report.append("3. **Priority 3**: Integrate tools into the enforcement pipeline")
        report.append("4. **Priority 4**: Add validation for governance engines")
        report.append("")
        
        return "\n".join(report)

def main():
    workspace = Path("/workspace")
    scanner = EcosystemScanner(workspace)
    report = scanner.generate_report()
    print(report)
    
    # 保存報告
    report_path = workspace / "reports" / "ecosystem-unbound-modules-scan.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n📄 Report saved to: {report_path}")

if __name__ == "__main__":
    main()
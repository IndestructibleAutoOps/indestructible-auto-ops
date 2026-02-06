#!/usr/bin/env python3
"""Validation Script - Verify GL Governance Compliance"""

import os
import json
from pathlib import Path
from collections import defaultdict

REPO_ROOT = Path(__file__).resolve().parent

def check_file_compliance(file_path):
    """檢查單個檔案的合規性"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 檢查 GL 標記
        has_governed = '@GL-governed' in content
        has_layer = '@GL-layer:' in content
        has_semantic = '@GL-semantic:' in content
        has_audit_trail = '@GL-audit-trail:' in content
        
        return {
            'path': str(file_path.relative_to(REPO_ROOT)),
            'has_governed': has_governed,
            'has_layer': has_layer,
            'has_semantic': has_semantic,
            'has_audit_trail': has_audit_trail,
            'is_compliant': all([has_governed, has_layer, has_semantic, has_audit_trail])
        }
    except:
        return None

def validate_structure():
    """驗證檔案結構"""
    results = {
        'structure_checks': {},
        'naming_checks': {},
        'import_checks': {},
        'compliance_checks': {}
    }
    
    # 檢查目標目錄結構
    print("Checking directory structure...")
    
    expected_dirs = [
        'gl-platform',
        'gl-platform/GL90-99-Meta-Specification-Layer',
        'gl-platform/GL90-99-Meta-Specification-Layer/governance',
        'gl-platform/GL90-99-Meta-Specification-Layer/governance/archived/legacy',
        'gl-platform/GL30-49-Execution-Layer',
        'gl-platform/GL90-99-Meta-Specification-Layer/governance/GL90-99-semantic-engine'
    ]
    
    for dir_path in expected_dirs:
        full_path = REPO_ROOT / dir_path
        if full_path.exists():
            results['structure_checks'][dir_path] = "EXISTS"
        else:
            results['structure_checks'][dir_path] = "NOT_FOUND"
    
    # 檢查關鍵檔案
    key_files = [
        'gl-platform/GL90-99-Meta-Specification-Layer/governance/GL-ROOT-SEMANTIC-ANCHOR.yaml',
        'gl-platform/GL90-99-Meta-Specification-Layer/governance/GL-UNIFIED-NAMING-CHARTER.yaml',
        'gl-platform/GL90-99-Meta-Specification-Layer/governance/GL90-99-semantic-engine'
    ]
    
    for file_path in key_files:
        full_path = REPO_ROOT / file_path
        if full_path.exists():
            results['structure_checks'][file_path] = "EXISTS"
        else:
            results['structure_checks'][file_path] = "NOT_FOUND"
    
    return results

def validate_compliance():
    """驗證合規性"""
    print("Checking GL compliance...")
    
    # 掃描所有檔案
    python_files = list(REPO_ROOT.rglob('*.py'))
    yaml_files = list(REPO_ROOT.rglob('*.yaml'))
    
    results = {
        'python_files': len(python_files),
        'yaml_files': len(yaml_files),
        'compliant': 0,
        'non_compliant': 0,
        'compliance_rate': 0.0
    }
    
    # 檢查 Python 檔案
    for file_path in python_files:
        check_result = check_file_compliance(file_path)
        if check_result and check_result['is_compliant']:
            results['compliant'] += 1
        elif check_result:
            results['non_compliant'] += 1
    
    # 檢查 YAML 檔案
    for file_path in yaml_files:
        check_result = check_file_compliance(file_path)
        if check_result and check_result['is_compliant']:
            results['compliant'] += 1
        elif check_result:
            results['non_compliant'] += 1
    
    # 計算合規率
    total = results['python_files'] + results['yaml_files']
    if total > 0:
        results['compliance_rate'] = (results['compliant'] / total) * 100
    
    return results

def generate_report(structure_results, compliance_results):
    """生成驗證報告"""
    report = f"""# GL Governance Validation Report

## 執行摘要
- 驗證時間: {os.popen('date').read().strip()}
- 驗證範圍: MachineNativeOps/machine-native-ops

## 結構驗證
"""
    
    for dir_path, status in structure_results.items():
        status_icon = "✓" if status == "EXISTS" else "✗"
        report += f"\n{status_icon} {dir_path}: {status}\n"
    
    report += """

## 合規性驗證
"""
    
    report += f"""
### Python 檔案
- 總數: {compliance_results['python_files']}
- 合規: {compliance_results['compliant']}
- 不合規: {compliance_results['non_compliant']}

### YAML 檔案
- 總數: {compliance_results['yaml_files']}
- 合規: {compliance_results['compliant']}
- 不合規: {compliance_results['non_compliant']}

### 總計
- 總檔案: {compliance_results['python_files'] + compliance_results['yaml_files']}
- 完全合規: {compliance_results['compliant']}
- 需要調整: {compliance_results['non_compliant']}
- 合規率: {compliance_results['compliance_rate']:.2f}%
"""
    
    # 保存報告
    with open('/workspace/validation_report.md', 'w') as f:
        f.write(report)
    
    return report

def main():
    """主執行驗證"""
    print("="*60)
    print("GL Governance Validation")
    print("="*60)
    print()
    
    # 執行驗證
    print("Step 1: Validating structure...")
    structure_results = validate_structure()
    
    print("\nStep 2: Validating compliance...")
    compliance_results = validate_compliance()
    
    # 生成報告
    print("\nStep 3: Generating report...")
    report = generate_report(structure_results, compliance_results)
    print(report)
    
    print("\n" + "="*60)
    print("Validation Complete")
    print("="*60)

if __name__ == '__main__':
    main()
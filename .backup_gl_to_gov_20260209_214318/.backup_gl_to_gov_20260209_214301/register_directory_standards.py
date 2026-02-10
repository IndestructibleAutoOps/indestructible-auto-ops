#!/usr/bin/env python3
"""
註冊目錄標準到 naming-governance
"""
import os
import json
import yaml
from pathlib import Path

def register_directory_standards():
    """將目錄標準註冊到 naming-governance"""
    
    # 源文件
    standards_file = Path("naming_governance_directory_standards.yaml")
    
    # 目標位置
    target_dir = Path("machine-native-ops/gl-platform/governance/naming-governance/contracts/")
    
    # 創建目錄（如果不存在）
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # 複製文件
    target_file = target_dir / "directory-standards.yaml"
    
    print(f"Registering directory standards to: {target_file}")
    
    # 讀取源文件
    with open(standards_file, 'r', encoding='utf-8') as f:
        standards_content = f.read()
    
    # 寫入目標文件
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(standards_content)
    
    print(f"✓ Directory standards registered successfully")
    
    # 更新 naming-conventions.yaml 以包含目錄標準
    update_naming_conventions(target_dir)
    
    # 生成註冊報告
    generate_registration_report()

def update_naming_conventions(target_dir):
    """更新 naming-conventions.yaml"""
    conventions_file = target_dir / "naming-conventions.yaml"
    
    print(f"Updating naming conventions: {conventions_file}")
    
    with open(conventions_file, 'r', encoding='utf-8') as f:
        conventions = yaml.safe_load(f)
    
    # 添加目錄標準引用
    if 'spec' not in conventions:
        conventions['spec'] = {}
    if 'references' not in conventions['spec']:
        conventions['spec']['references'] = []
    
    conventions['spec']['references'].append({
        'type': 'directory-standards',
        'file': 'directory-standards.yaml',
        'version': 'v2.0.0',
        'purpose': '大型儲存庫目錄編排規範'
    })
    
    # 寫回文件
    with open(conventions_file, 'w', encoding='utf-8') as f:
        yaml.dump(conventions, f, default_flow_style=False, allow_unicode=True)
    
    print(f"✓ Naming conventions updated")

def generate_registration_report():
    """生成註冊報告"""
    report = {
        'registration_type': 'directory-standards',
        'timestamp': '2026-01-31T00:00:00Z',
        'version': 'v2.0.0',
        'status': 'REGISTERED',
        'location': 'gl-platform/governance/naming-governance/contracts/directory-standards.yaml',
        'key_features': [
            '8層企業架構定義',
            '責任邊界規範',
            '目錄命名規範',
            '多平台並行支援',
            '大型儲存庫組織',
            '驗證與合規檢查',
            '文檔化要求'
        ],
        'applicability': [
            '大型儲存庫（>1000 文件）',
            '多平台並行架構',
            '微服務架構',
            'Monorepo 結構'
        ],
        'next_steps': [
            '實施目錄結構驗證器',
            '更新現有目錄結構',
            '集成到 CI/CD 流程',
            '生成遷移指南'
        ]
    }
    
    # 保存報告
    with open('directory_standards_registration_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"✓ Registration report generated")

if __name__ == "__main__":
    print("=== Directory Standards Registration ===")
    register_directory_standards()
    print("\nRegistration complete!")
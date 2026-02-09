#!/usr/bin/env python3

"""
NG10100 Indestructible AutoOps 目录修复脚本
"""

import os
import json
from pathlib import Path
from datetime import datetime

def convert_to_kebab_case(name):
    """将目录名转换为 kebab-case"""
    converted = name.replace('_', '-')
    converted = converted.replace('.', '-')
    converted = converted.replace('(', '').replace(')', '')
    converted = converted.lower()
    return converted

def rename_directory(old_path, new_path):
    """重命名目录"""
    try:
        if old_path.exists() and not new_path.exists():
            print(f"重命名: {old_path} -> {new_path}")
            old_path.rename(new_path)
            return True
        return False
    except Exception as e:
        print(f"错误: 无法重命名 {old_path} -> {new_path}: {e}")
        return False

def update_file_references(workspace, old_name, new_name):
    """更新文件中的路径引用"""
    updated_files = 0
    
    extensions = {'.py', '.js', '.ts', '.json', '.yaml', '.yml', '.md', '.txt', '.sh', '.toml', '.cfg', '.ini'}
    
    for file_path in workspace.rglob('*'):
        if not file_path.is_file() or file_path.suffix not in extensions:
            continue
            
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            original = content
            
            if old_name in content:
                content = content.replace(old_name + '/', new_name + '/')
                content = content.replace('/' + old_name + '/', '/' + new_name + '/')
                content = content.replace('/' + old_name + '"', '/' + new_name + '"')
                content = content.replace('/' + old_name + "'", '/' + new_name + "'")
                content = content.replace('/' + old_name + ')', '/' + new_name + ')')
                content = content.replace('/' + old_name + ']', '/' + new_name + ']')
                content = content.replace('/' + old_name + '}', '/' + new_name + '}')
                content = content.replace('"' + old_name + '"', '"' + new_name + '"')
                content = content.replace("'" + old_name + "'", "'" + new_name + "'")
                
                if content != original:
                    file_path.write_text(content, encoding='utf-8')
                    updated_files += 1
                    
        except Exception as e:
            continue
    
    return updated_files

def main():
    workspace = Path('/workspace')
    
    print("=" * 60)
    print("NG10100 Indestructible AutoOps 目录修复")
    print("=" * 60)
    print(f"工作目录: {workspace}")
    print()
    
    # 只处理 indestructible-autoops-governance 目录中的剩余问题
    directories = [
        "indestructible-autoops-governance/gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/gl90-99-semantic-engine",
        "indestructible-autoops-governance/gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/quantum-naming-v4-0-0",
        "indestructible-autoops-governance/gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/naming-governance-v1-0-0-extended",
        "indestructible-autoops-governance/gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/naming-governance-v1-0-0",
        "indestructible-autoops-governance/gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-d36",
        "indestructible-autoops-governance/gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-2c8",
        "indestructible-autoops-governance/gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-9ad",
        "indestructible-autoops-governance/gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-388",
        "indestructible-autoops-governance/gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-a15",
        "indestructible-autoops-governance/gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-61c",
        "indestructible-autoops-governance/gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-9a2",
        "indestructible-autoops-governance/gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-2a5",
        "indestructible-autoops-governance/gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-086",
        "indestructible-autoops-governance/gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-2d4",
        "indestructible-autoops-governance/gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-bfe",
        "indestructible-autoops-governance/gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-2025-12-22-d09",
        "indestructible-autoops-governance/machine-native-ops/ecosystem/reasoning/dual-path",
        "indestructible-autoops-governance/gov-runtime-execution-platform/engine/aep-engine-app/app/tabs",
        "indestructible-autoops-governance/gov-runtime-engine-platform/aep-engine-app/app/tabs",
    ]
    
    renamed_count = 0
    files_updated = 0
    
    print("第一阶段：重命名目录")
    print("=" * 60)
    
    rename_mapping = {}
    for dir_path in directories:
        old_full_path = workspace / dir_path
        if old_full_path.exists() and old_full_path.is_dir():
            old_name = old_full_path.name
            new_name = convert_to_kebab_case(old_name)
            
            if old_name != new_name:
                new_full_path = old_full_path.parent / new_name
                if rename_directory(old_full_path, new_full_path):
                    renamed_count += 1
                    rename_mapping[old_name] = new_name
    
    print()
    print("第二阶段：更新文件中的路径引用")
    print("=" * 60)
    
    for old_name, new_name in rename_mapping.items():
        print(f"更新引用: {old_name} -> {new_name}")
        updated = update_file_references(workspace, old_name, new_name)
        files_updated += updated
    
    print()
    print("=" * 60)
    print("修复完成")
    print("=" * 60)
    print(f"重命名目录数: {renamed_count}")
    print(f"更新文件数: {files_updated}")
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "workspace": str(workspace),
        "summary": {
            "directories_renamed": renamed_count,
            "files_updated": files_updated,
        },
        "rename_mapping": rename_mapping,
    }
    
    report_path = workspace / "ng10100-fix-indestructible-report.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"修复报告已保存: {report_path}")

if __name__ == "__main__":
    main()
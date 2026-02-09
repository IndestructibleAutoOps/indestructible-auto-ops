#!/usr/bin/env python3

"""
NG10100 补充修复脚本
处理剩余的目录命名违规
"""

import os
import json
from pathlib import Path
from datetime import datetime

def convert_to_kebab_case(name):
    """将目录名转换为 kebab-case（保留点号用于版本号）"""
    # 将下划线替换为连字符
    converted = name.replace('_', '-')
    # 转换为小写
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
    print("NG10100 补充修复")
    print("=" * 60)
    print(f"工作目录: {workspace}")
    print()
    
    # 剩余需要修复的目录
    directories = [
        # 根目录
        "summarized_conversations",
        # 版本目录（保持点号，但转换大小写）
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/quantum-naming-v4-0-0",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/naming-governance-v1-0-0-extended",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/naming-governance-v1-0-0",
        # 平台目录（将点号改为连字符）
        "machine-native-ops/gov-runtime-engine-platform",
        "platforms/gov-platform-ide",
        "platforms/gov-platform-assistant",
        # Indestructible AutoOps 目录（重复项）
        "indestructible-autoops-governance/gov-governance-architecture-platform/gl90-99-meta-specification-layer",
        "indestructible-autoops-governance/gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/gl90-99-semantic-engine",
        "indestructible-autoops-governance/gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/quantum-naming-v4-0-0",
        "indestructible-autoops-governance/gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/naming-governance-v1-0-0-extended",
        "indestructible-autoops-governance/gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/naming-governance-v1-0-0",
        "indestructible-autoops-governance/machine-native-ops/gov-runtime-engine-platform",
        "indestructible-autoops-governance/platforms/gov-platform-ide",
        "indestructible-autoops-governance/platforms/gov-platform-assistant",
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
            
            # 对于包含点号的目录名，将点号改为连字符
            if '.' in old_name and not (old_name.startswith('.') or old_name.endswith('.')):
                new_name = new_name.replace('.', '-')
            
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
    print("补充修复完成")
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
    
    report_path = workspace / "ng10100-fix-remaining-report.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"修复报告已保存: {report_path}")

if __name__ == "__main__":
    main()
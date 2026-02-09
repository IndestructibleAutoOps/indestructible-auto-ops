#!/usr/bin/env python3

"""
NG10100 自动修复脚本 v2
修复所有目录命名违规，转换为 kebab-case 格式
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

def convert_to_kebab_case(name):
    """将目录名转换为 kebab-case"""
    converted = name.replace('_', '-')
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
    print("NG10100 目录命名自动修复")
    print("=" * 60)
    print(f"工作目录: {workspace}")
    print()
    
    directories = [
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-003",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-086",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-2a5",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-2c8",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-2d4",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-388",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-61c",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-9a2",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-9ad",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-a15",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-bfe",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-2025-12-22-d09",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/naming-governance-v1-0-0-extended",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/quantum-naming-v4-0-0",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/naming-governance-v1-0-0",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-d36",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-2c8",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-9ad",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-388",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-a15",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-61c",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-9a2",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-2a5",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-086",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-2d4",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-bfe",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-2025-12-22-d09",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/standards",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/tests/performance",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/tests/unit",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/tests/e2e",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/tests",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/rollback/points",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/rollback",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/security",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/compliance",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/reports",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/gl90-99-semantic-engine",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance",
        "gov-governance-architecture-platform/gl90-99-meta-specification-layer",
        "tests/gl/autonomy-boundary/external-api-unavailable",
        "ecosystem/tests/semantic-defense/test-complement-missing",
        "ecosystem/tests/semantic-defense/test-yaml-failure",
        "ecosystem/tests/semantic-defense/test-semantic-corruption",
        "ecosystem/tests/semantic-defense/test-hash-divergence",
        "ecosystem/tests/semantic-defense/test-layered-sorting",
        "ecosystem/tests/semantic-defense/test-canonicalization-invariant",
        "ecosystem/tests/semantic-defense/test-tool-registry",
        "ecosystem/tests/semantic-defense/test-pipeline-interrupted",
        "ecosystem/tests/semantic-defense/test-event-missing-field",
        "ecosystem/tests/semantic-defense",
        "ecosystem/.evidence/semantic-tokens",
        "ecosystem/.evidence/autonomy-boundary/era-seals",
        "ecosystem/.evidence/autonomy-boundary/replayability-reports",
        "ecosystem/.evidence/autonomy-boundary/hash-boundaries",
        "ecosystem/.evidence/autonomy-boundary/wagb/append-only-events",
        "ecosystem/.evidence/autonomy-boundary/wagb",
        "ecosystem/.evidence/autonomy-boundary",
        "ecosystem/governance/hash-spec",
        "ecosystem/governance/gov-semantic-anchors",
        "ecosystem/governance/templates/artifact-schemas",
        "ecosystem/governance/templates/tool-stubs",
        "ecosystem/governance/templates/event-schemas",
        "ecosystem/governance/templates",
        "ecosystem/reasoning/dual-path",
        "ng-namespace-governance",
        "machine-native-ops/ecosystem/reasoning/dual-path",
        "docs/runbooks",
        "docs/training",
        "docs/migration",
        "platforms/gov-platform-ide",
        "platforms/gov-platform-assistant",
        "gov-runtime-execution-platform/engine/tools-legacy/path-tools",
        "gov-runtime-execution-platform/engine/aep-engine-app/app/tabs",
        "gov-runtime-execution-platform/engine/tools-legacy",
        "gov-runtime-engine-platform/tools-legacy/path-tools",
        "gov-runtime-engine-platform/aep-engine-app/app/tabs",
        "gov-runtime-engine-platform/tools-legacy",
        "indestructible-autoops-governance/auto-task-project",
        "indestructible-autoops-governance/tests/gl/autonomy-boundary/external-api-unavailable",
        "indestructible-autoops-governance/ecosystem/tests/semantic-defense/test-semantic-corruption",
        "indestructible-autoops-governance/ecosystem/tests/semantic-defense/test-hash-divergence",
        "indestructible-autoops-governance/ecosystem/tests/semantic-defense",
        "indestructible-autoops-governance/ecosystem/.evidence/semantic-tokens",
        "indestructible-autoops-governance/ecosystem/.evidence/autonomy-boundary/era-seals",
        "indestructible-autoops-governance/ecosystem/.evidence/autonomy-boundary/replayability-reports",
        "indestructible-autoops-governance/ecosystem/.evidence/autonomy-boundary/hash-boundaries",
        "indestructible-autoops-governance/ecosystem/.evidence/autonomy-boundary/wagb/append-only-events",
        "indestructible-autoops-governance/ecosystem/.evidence/autonomy-boundary/wagb",
        "indestructible-autoops-governance/ecosystem/.evidence/autonomy-boundary",
        "indestructible-autoops-governance/ecosystem/governance/hash-spec",
        "indestructible-autoops-governance/ecosystem/governance/gov-semantic-anchors",
        "indestructible-autoops-governance/ecosystem/reasoning/dual-path",
        "indestructible-autoops-governance/docs/runbooks",
        "indestructible-autoops-governance/docs/training",
        "indestructible-autoops-governance/docs/migration",
        "indestructible-autoops-governance/platforms/gov-platform-ide",
        "indestructible-autoops-governance/platforms/gov-platform-assistant",
        "indestructible-autoops-governance/gov-runtime-execution-platform/engine/tools-legacy/path-tools",
        "indestructible-autoops-governance/gov-runtime-execution-platform/engine/aep-engine-app/app/tabs",
        "indestructible-autoops-governance/gov-runtime-execution-platform/engine/tools-legacy",
        "indestructible-autoops-governance/gov-runtime-engine-platform/tools-legacy/path-tools",
        "indestructible-autoops-governance/gov-runtime-engine-platform/aep-engine-app/app/tabs",
        "indestructible-autoops-governance/gov-runtime-engine-platform/tools-legacy",
        "summarized_conversations",
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
    
    report_path = workspace / "ng10100-fix-report.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"修复报告已保存: {report_path}")

if __name__ == "__main__":
    main()
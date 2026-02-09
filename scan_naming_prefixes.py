#!/usr/bin/env python3
"""
掃描專案中的命名前綴規則
"""

import re
from pathlib import Path
from collections import defaultdict
import json

def scan_naming_patterns(workspace: Path):
    """掃描命名模式"""
    patterns = {
        'gl-': defaultdict(list),           # kebab-case with gl- prefix
        'gl.': defaultdict(list),           # dot notation
        'gl_': defaultdict(list),           # snake_case with gl_ prefix
        'GL_': defaultdict(list),           # UPPER_CASE with GL_ prefix
        'gl_': defaultdict(list),           # Chinese naming
        'governance': defaultdict(list),    # governance-related
        'gov_': defaultdict(list),          # gov_ prefix
        'ng_': defaultdict(list),           # ng_ prefix (old)
        'mng_': defaultdict(list),          # mng_ prefix (old)
        'responsibility-': defaultdict(list), # responsibility boundaries
        'enterprise-': defaultdict(list),    # enterprise systems
    }
    
    # 掃描目錄名稱
    for dir_path in workspace.rglob('*'):
        if dir_path.is_dir():
            dir_name = dir_path.name
            rel_path = str(dir_path.relative_to(workspace))
            
            for prefix, collection in patterns.items():
                if dir_name.startswith(prefix):
                    collection[dir_name].append({
                        'type': 'directory',
                        'path': rel_path,
                        'depth': len(dir_path.relative_to(workspace).parts)
                    })
                    break
    
    # 掃描文件名稱
    for file_path in workspace.rglob('*'):
        if file_path.is_file() and file_path.suffix in ['.py', '.yaml', '.yml', '.json', '.md']:
            file_name = file_path.stem
            rel_path = str(file_path.relative_to(workspace))
            
            for prefix, collection in patterns.items():
                if file_name.startswith(prefix):
                    collection[file_name].append({
                        'type': 'file',
                        'path': rel_path,
                        'extension': file_path.suffix
                    })
                    break
    
    return patterns

def analyze_directory_structure(workspace: Path):
    """分析目錄結構"""
    root_dirs = [d for d in workspace.iterdir() if d.is_dir() and not d.name.startswith('.')]
    
    structure = {
        'total_root_dirs': len(root_dirs),
        'root_dirs': [],
        'duplicate_prefixes': defaultdict(list),
        'inconsistent_naming': []
    }
    
    # 分析根層目錄
    for dir_path in sorted(root_dirs):
        name = dir_path.name
        structure['root_dirs'].append({
            'name': name,
            'prefix': name.split('-')[0] if '-' in name else name.split('_')[0],
            'items': len(list(dir_path.iterdir())) if dir_path.exists() else 0
        })
    
    # 檢查重複前綴
    prefixes = defaultdict(list)
    for dir_info in structure['root_dirs']:
        prefix = dir_info['prefix']
        prefixes[prefix].append(dir_info['name'])
    
    for prefix, names in prefixes.items():
        if len(names) > 1:
            structure['duplicate_prefixes'][prefix] = names
    
    # 檢查不一致的命名
    for dir_info in structure['root_dirs']:
        name = dir_info['name']
        has_dash = '-' in name
        has_underscore = '_' in name
        has_uppercase = any(c.isupper() for c in name if c not in '-_')
        
        if has_dash and has_underscore:
            structure['inconsistent_naming'].append({
                'name': name,
                'issue': '混合使用 - 和 _'
            })
        elif has_uppercase and not has_dash and not has_underscore:
            structure['inconsistent_naming'].append({
                'name': name,
                'issue': '使用大寫字母'
            })
    
    return structure

def main():
    workspace = Path('/workspace/indestructibleautoops')
    
    print("=" * 80)
    print("命名前綴規則掃描報告")
    print("=" * 80)
    
    # 掃描命名模式
    patterns = scan_naming_patterns(workspace)
    
    print("\n## 1. 命名前綴統計")
    print("-" * 80)
    for prefix, collection in patterns.items():
        if collection:
            print(f"\n{prefix}:")
            print(f"  總數: {len(collection)}")
            # 顯示前 10 個
            for name, items in list(collection.items())[:10]:
                print(f"  - {name} ({len(items)} 項)")
    
    # 分析目錄結構
    structure = analyze_directory_structure(workspace)
    
    print("\n## 2. 根層目錄結構分析")
    print("-" * 80)
    print(f"總目錄數: {structure['total_root_dirs']}")
    print("\n根層目錄列表:")
    for dir_info in structure['root_dirs']:
        print(f"  - {dir_info['name']:40s} (前綴: {dir_info['prefix']:15s}, 項目: {dir_info['items']:4d})")
    
    print("\n## 3. 重複前綴檢測")
    print("-" * 80)
    if structure['duplicate_prefixes']:
        for prefix, names in structure['duplicate_prefixes'].items():
            print(f"  {prefix}: {', '.join(names)}")
    else:
        print("  無重複前綴")
    
    print("\n## 4. 命名不一致問題")
    print("-" * 80)
    if structure['inconsistent_naming']:
        for item in structure['inconsistent_naming']:
            print(f"  - {item['name']}: {item['issue']}")
    else:
        print("  無不一致命名")
    
    # 生成 JSON 報告
    report = {
        'patterns': {k: {name: items for name, items in v.items()} for k, v in patterns.items() if v},
        'structure': structure
    }
    
    report_path = workspace / 'naming_scan_report.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n完整報告已保存至: {report_path}")
    print("=" * 80)

if __name__ == '__main__':
    main()
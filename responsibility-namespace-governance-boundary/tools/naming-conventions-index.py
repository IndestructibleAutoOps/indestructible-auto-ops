#!/usr/bin/env python3
"""
命名規範索引器 - 掃描整個儲存庫中的命名規範
"""
import os
import re
import json
from pathlib import Path
from collections import defaultdict

def find_naming_files(root_path="."):
    """查找所有包含命名相關關鍵詞的文件"""
    naming_keywords = [
        "naming.*convention", "naming.*standard", "naming.*policy",
        "naming.*rule", "naming.*governance", "naming.*specification",
        "naming.*charter", "naming.*registry"
    ]
    
    naming_files = []
    for ext in ['*.yaml', '*.yml', '*.json', '*.md', '*.py', '*.rego']:
        for pattern in naming_keywords:
            cmd = f'find {root_path} -type f -name "*naming*" -exec grep -l "{pattern}" {{}} \\;'
            # This would need to be executed via subprocess
            pass
    
    return naming_files

def extract_naming_conventions(file_path):
    """從文件中提取命名約定"""
    conventions = {
        'file_path': str(file_path),
        'comment_patterns': [],
        'variable_patterns': [],
        'function_patterns': [],
        'class_patterns': [],
        'file_patterns': [],
        'directory_patterns': [],
        'service_patterns': []
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取各種命名模式
        # Comment patterns
        comment_matches = re.findall(r'# (gl[:\.\w\-]+)', content)
        if comment_matches:
            conventions['comment_patterns'] = list(set(comment_matches))
        
        # Variable patterns
        var_matches = re.findall(r'GL[A-Z_]+', content)
        if var_matches:
            conventions['variable_patterns'] = list(set(var_matches))
        
        # Service patterns
        service_matches = re.findall(r'gl[-\w]+-svc', content)
        if service_matches:
            conventions['service_patterns'] = list(set(service_matches))
            
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return conventions

def build_naming_index():
    """構建命名規範索引"""
    root_path = Path("machine-native-ops")
    
    # 查找所有命名相關文件
    naming_files = []
    for pattern in ['*naming*', '*convention*', '*charter*']:
        naming_files.extend(root_path.rglob(pattern))
    
    # 過濾文件
    naming_files = [f for f in naming_files if f.is_file()]
    
    print(f"Found {len(naming_files)} naming-related files")
    
    # 建立索引
    index = {
        'total_files': len(naming_files),
        'files': [],
        'patterns': defaultdict(int),
        'categories': defaultdict(list)
    }
    
    for file_path in naming_files:
        conventions = extract_naming_conventions(file_path)
        
        if conventions:
            index['files'].append({
                'path': str(file_path),
                'patterns': conventions
            })
            
            # 統計模式
            for pattern_type, patterns in conventions.items():
                for pattern in patterns:
                    index['patterns'][pattern_type] += 1
            
            # 分類
            file_str = str(file_path)
            if 'governance' in file_str:
                index['categories']['governance'].append(str(file_path))
            elif 'github' in file_str:
                index['categories']['github'].append(str(file_path))
            elif 'engine' in file_str:
                index['categories']['engine'].append(str(file_path))
            elif 'gl-platform' in file_str:
                index['categories']['platform'].append(str(file_path))
    
    return index

def main():
    """主函數"""
    print("=== Naming Conventions Indexer ===")
    print("Building index of naming conventions...")
    
    index = build_naming_index()
    
    # 保存索引
    with open('naming_conventions_index.json', 'w') as f:
        json.dump(index, f, indent=2)
    
    print(f"Index saved to naming_conventions_index.json")
    print(f"Total files analyzed: {index['total_files']}")
    print(f"Categories found: {len(index['categories'])}")
    
    for category, files in index['categories'].items():
        print(f"  {category}: {len(files)} files")

if __name__ == "__main__":
    main()
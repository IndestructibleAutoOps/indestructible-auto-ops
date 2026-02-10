#!/usr/bin/env python3
"""
術語統一替換腳本
基於 TOGAF、FEAF、ISO/IEC/IEEE 42010 等國際標準
"""

import os
import re
import json
from pathlib import Path

# 術語映射表
TERMINOLOGY_MAP = {
    # 英文術語替換
    "GL_UNIFIED_FRAMEWORK": "GL_UNIFIED_FRAMEWORK",
    "Unified Architecture Governance Framework": "Unified Architecture Governance Framework",
    "governance framework": "governance framework",
    "governance-framework-baseline": "governance-framework-baseline",
    
    # 中文術語替換
    "框架": "框架",
    "統一框架": "統一架構治理框架",
    "治理框架": "治理框架",
    
    # Platform Universe 替換
    "gov-platform": "gov-platform",
    "gov-platform": "gov-platform",
    "platform": "platform",
}

# 文件重命名映射
FILE_RENAME_MAP = {
    "ecosystem/governance/gov-semantic-anchors/GL00-GL99-unified-charter.json": 
        "ecosystem/governance/gov-semantic-anchors/GL00-GL99-unified-framework.json",
}

# 需要更新的文件模式
FILE_PATTERNS = [
    "*.json",
    "*.yaml",
    "*.yml",
    "*.py",
    "*.md",
]

def should_skip_file(filepath):
    """跳過不需要更新的文件"""
    skip_patterns = [
        "node_modules",
        ".git",
        "__pycache__",
        "dist",
        "build",
        ".next",
        "coverage",
        "venv",
        ".venv",
    ]
    
    for pattern in skip_patterns:
        if pattern in str(filepath):
            return True
    return False

def replace_terminology_in_file(filepath):
    """在文件中替換術語"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 執行替換
        for old_term, new_term in TERMINOLOGY_MAP.items():
            content = content.replace(old_term, new_term)
        
        # 只在內容發生變化時寫回
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def update_json_file_structure(filepath):
    """更新 JSON 文件的結構（特別是 GL_UNIFIED_FRAMEWORK → GL_UNIFIED_FRAMEWORK）"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        updated = False
        
        # 替換頂層鍵
        if "GL_UNIFIED_FRAMEWORK" in data:
            data["GL_UNIFIED_FRAMEWORK"] = data.pop("GL_UNIFIED_FRAMEWORK")
            updated = True
        
        # 更新描述
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    if "description" in value:
                        old_desc = value["description"]
                        new_desc = old_desc.replace("Unified Architecture Governance Framework", "Unified Architecture Governance Framework")
                        if new_desc != old_desc:
                            value["description"] = new_desc
                            updated = True
        
        if updated:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        
        return False
    except Exception as e:
        print(f"Error updating JSON structure in {filepath}: {e}")
        return False

def main():
    """主函數"""
    workspace = Path("/workspace")
    
    print("🔄 開始術語統一替換...")
    print(f"📁 工作目錄: {workspace}")
    print()
    
    updated_files = []
    renamed_files = []
    
    # Phase 1: 文件重命名
    print("📝 Phase 1: 文件重命名...")
    for old_path, new_path in FILE_RENAME_MAP.items():
        old_file = workspace / old_path
        new_file = workspace / new_path
        
        if old_file.exists():
            print(f"  🔧 重命名: {old_path} → {new_path}")
            old_file.rename(new_file)
            renamed_files.append(str(new_file))
        else:
            print(f"  ⚠️  文件不存在: {old_path}")
    
    print(f"✅ 完成重命名 {len(renamed_files)} 個文件\n")
    
    # Phase 2: 文件內容替換
    print("📝 Phase 2: 文件內容替換...")
    
    # 遍歷所有文件
    for pattern in FILE_PATTERNS:
        print(f"  🔍 處理模式: {pattern}")
        for filepath in workspace.rglob(pattern):
            if should_skip_file(filepath):
                continue
            
            # 對 JSON 文件進行結構更新
            if filepath.suffix == '.json':
                if update_json_file_structure(filepath):
                    updated_files.append(str(filepath))
            
            # 進行文本替換
            if replace_terminology_in_file(filepath):
                updated_files.append(str(filepath))
    
    print(f"✅ 完成更新 {len(updated_files)} 個文件\n")
    
    # 摘要
    print("=" * 80)
    print("📊 替換摘要")
    print("=" * 80)
    print(f"📁 重命名文件: {len(renamed_files)}")
    print(f"📝 更新文件: {len(updated_files)}")
    print(f"📋 總計: {len(set(renamed_files + updated_files))}")
    print()
    
    print("✅ 術語統一替換完成！")
    print()
    print("⚠️  請運行以下命令驗證:")
    print("   python ecosystem/enforce.py --audit")

if __name__ == "__main__":
    main()
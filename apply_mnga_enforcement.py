#!/usr/bin/env python3
"""
MNGA 全儲存庫強制執行腳本
Apply MNGA Enforcement to Entire Repository

此腳本將：
1. 為核心治理文件添加 GL 標註
2. 修復目錄命名（下劃線 -> 連字符）
3. 創建缺失的 event-stream.jsonl 文件
4. 驗證並報告結果
"""

import os
import re
import json
import shutil
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Tuple

WORKSPACE = Path("/workspace")

# GL 標註模板
GL_ANNOTATION_TEMPLATE = '''#!/usr/bin/env python3
"""
{description}

@GL-governed
@GL-layer: {gl_layer}
@GL-semantic: {semantic}
"""
'''

# 需要添加 GL 標註的文件
FILES_NEEDING_GL_ANNOTATION = {
    "ecosystem/enforcers/self_auditor.py": {
        "gl_layer": "GL40-49",
        "semantic": "governance-self-audit",
        "description": "Self Auditor - 自我審計器"
    },
    "ecosystem/enforcers/governance_enforcer.py": {
        "gl_layer": "GL30-39",
        "semantic": "governance-enforcement",
        "description": "Governance Enforcer - 治理強制執行器"
    },
    "ecosystem/tools/audit_trail_report.py": {
        "gl_layer": "GL70-79",
        "semantic": "audit-trail-reporting",
        "description": "Audit Trail Report - 審計追蹤報告"
    },
    "ecosystem/tools/audit_trail_query.py": {
        "gl_layer": "GL70-79",
        "semantic": "audit-trail-query",
        "description": "Audit Trail Query - 審計追蹤查詢"
    },
}

# 需要重命名的目錄（下劃線 -> 連字符）
DIRECTORIES_TO_RENAME = [
    ("ecosystem/reasoning/dual-path", "ecosystem/reasoning/dual-path"),
    ("ecosystem/indexes/internal/code_vectors", "ecosystem/indexes/internal/code-vectors"),
    ("ecosystem/indexes/internal/docs_index", "ecosystem/indexes/internal/docs-index"),
]

# 需要創建 event-stream.jsonl 的目錄
GOVERNANCE_DIRS_NEEDING_EVENT_STREAM = [
    "gl-runtime-engine-platform/engine/.governance",
    "gl-runtime-execution-platform/engine/engine/.governance",
]


def add_gl_annotation(file_path: Path, config: Dict) -> bool:
    """為文件添加 GL 標註"""
    try:
        content = file_path.read_text(encoding='utf-8')
        
        # 檢查是否已有 GL 標註
        if '@GL-governed' in content or '@GL-layer' in content:
            print(f"  ⏭️  {file_path} 已有 GL 標註")
            return False
        
        # 找到第一個 docstring 或 import 語句
        lines = content.split('\n')
        insert_pos = 0
        
        # 跳過 shebang
        if lines and lines[0].startswith('#!'):
            insert_pos = 1
        
        # 跳過編碼聲明
        while insert_pos < len(lines) and lines[insert_pos].startswith('# -*-'):
            insert_pos += 1
        
        # 構建 GL 標註
        gl_annotation = f'''#
# @GL-governed
# @GL-layer: {config["gl_layer"]}
# @GL-semantic: {config["semantic"]}
#
'''
        
        # 插入標註
        lines.insert(insert_pos, gl_annotation)
        new_content = '\n'.join(lines)
        
        file_path.write_text(new_content, encoding='utf-8')
        print(f"  ✅ 已添加 GL 標註: {file_path}")
        return True
        
    except Exception as e:
        print(f"  ❌ 添加 GL 標註失敗 {file_path}: {e}")
        return False


def rename_directory(old_path: Path, new_path: Path) -> bool:
    """重命名目錄"""
    try:
        if not old_path.exists():
            print(f"  ⏭️  {old_path} 不存在")
            return False
        
        if new_path.exists():
            print(f"  ⏭️  {new_path} 已存在")
            return False
        
        # 確保父目錄存在
        new_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 重命名
        shutil.move(str(old_path), str(new_path))
        print(f"  ✅ 已重命名: {old_path} -> {new_path}")
        return True
        
    except Exception as e:
        print(f"  ❌ 重命名失敗 {old_path}: {e}")
        return False


def create_event_stream(gov_dir: Path) -> bool:
    """創建 event-stream.jsonl 文件"""
    try:
        event_stream_path = gov_dir / "event-stream.jsonl"
        
        if event_stream_path.exists():
            print(f"  ⏭️  {event_stream_path} 已存在")
            return False
        
        # 確保目錄存在
        gov_dir.mkdir(parents=True, exist_ok=True)
        
        # 創建初始事件
        initial_event = {
            "event_id": "init-001",
            "event_type": "governance_initialized",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source": "mnga-enforcement",
            "data": {
                "message": "Governance event stream initialized",
                "version": "1.0.0"
            }
        }
        
        with open(event_stream_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(initial_event, ensure_ascii=False) + '\n')
        
        print(f"  ✅ 已創建: {event_stream_path}")
        return True
        
    except Exception as e:
        print(f"  ❌ 創建 event-stream.jsonl 失敗 {gov_dir}: {e}")
        return False


def update_imports_after_rename(old_name: str, new_name: str) -> int:
    """更新重命名後的導入語句"""
    count = 0
    old_module = old_name.replace('/', '.').replace('-', '_')
    new_module = new_name.replace('/', '.').replace('-', '_')
    
    # 掃描所有 Python 文件
    for py_file in WORKSPACE.rglob("*.py"):
        try:
            content = py_file.read_text(encoding='utf-8')
            
            # 檢查是否包含舊的導入
            if old_module in content or old_name in content:
                new_content = content.replace(old_module, new_module)
                new_content = new_content.replace(old_name, new_name)
                
                if new_content != content:
                    py_file.write_text(new_content, encoding='utf-8')
                    count += 1
                    
        except Exception:
            pass
    
    return count


def fix_all_underscore_directories() -> List[Tuple[str, str]]:
    """找出所有使用下劃線的目錄"""
    renamed = []
    
    # 排除的目錄
    exclude_patterns = ['.git', '__pycache__', 'node_modules', '.venv', 'site-packages']
    
    # 找出所有使用下劃線的目錄
    for dir_path in sorted(WORKSPACE.rglob("*"), key=lambda p: len(str(p)), reverse=True):
        if not dir_path.is_dir():
            continue
        
        # 檢查是否應該排除
        if any(ex in str(dir_path) for ex in exclude_patterns):
            continue
        
        dir_name = dir_path.name
        
        # 檢查是否包含下劃線（排除 Python 特殊目錄）
        if '_' in dir_name and not dir_name.startswith('__') and not dir_name.startswith('.'):
            # 轉換為 kebab-case
            new_name = dir_name.replace('_', '-')
            new_path = dir_path.parent / new_name
            
            if not new_path.exists():
                renamed.append((str(dir_path.relative_to(WORKSPACE)), str(new_path.relative_to(WORKSPACE))))
    
    return renamed


def main():
    """主函數"""
    print("=" * 70)
    print("🛡️  MNGA 全儲存庫強制執行")
    print("=" * 70)
    print()
    
    changes_made = 0
    
    # 1. 添加 GL 標註
    print("📝 Phase 1: 添加 GL 標註到核心治理文件")
    print("-" * 50)
    for file_rel, config in FILES_NEEDING_GL_ANNOTATION.items():
        file_path = WORKSPACE / file_rel
        if file_path.exists():
            if add_gl_annotation(file_path, config):
                changes_made += 1
    print()
    
    # 2. 創建缺失的 event-stream.jsonl
    print("📄 Phase 2: 創建缺失的 event-stream.jsonl")
    print("-" * 50)
    for gov_dir_rel in GOVERNANCE_DIRS_NEEDING_EVENT_STREAM:
        gov_dir = WORKSPACE / gov_dir_rel
        if create_event_stream(gov_dir):
            changes_made += 1
    
    # 也檢查其他 .governance 目錄
    for gov_dir in WORKSPACE.rglob(".governance"):
        event_stream = gov_dir / "event-stream.jsonl"
        if not event_stream.exists():
            if create_event_stream(gov_dir):
                changes_made += 1
    print()
    
    # 3. 重命名目錄（下劃線 -> 連字符）
    print("📁 Phase 3: 重命名目錄 (下劃線 -> 連字符)")
    print("-" * 50)
    
    # 找出所有需要重命名的目錄
    dirs_to_rename = fix_all_underscore_directories()
    
    print(f"  找到 {len(dirs_to_rename)} 個需要重命名的目錄")
    
    # 由於重命名可能影響 Python 導入，我們只重命名非 Python 模組的目錄
    # 或者提供報告讓用戶決定
    safe_to_rename = []
    needs_review = []
    
    for old_rel, new_rel in dirs_to_rename:
        old_path = WORKSPACE / old_rel
        
        # 檢查是否是 Python 模組（包含 __init__.py 或 .py 文件）
        has_python = any(old_path.rglob("*.py"))
        
        if has_python:
            needs_review.append((old_rel, new_rel))
        else:
            safe_to_rename.append((old_rel, new_rel))
    
    # 重命名安全的目錄
    for old_rel, new_rel in safe_to_rename:
        old_path = WORKSPACE / old_rel
        new_path = WORKSPACE / new_rel
        if rename_directory(old_path, new_path):
            changes_made += 1
    
    if needs_review:
        print(f"\n  ⚠️  以下 {len(needs_review)} 個目錄包含 Python 模組，需要謹慎處理：")
        for old_rel, new_rel in needs_review[:10]:
            print(f"      {old_rel} -> {new_rel}")
        if len(needs_review) > 10:
            print(f"      ... 還有 {len(needs_review) - 10} 個")
    print()
    
    # 4. 總結
    print("=" * 70)
    print(f"📊 執行完成: 共進行 {changes_made} 項更改")
    print("=" * 70)
    
    return changes_made


if __name__ == "__main__":
    main()
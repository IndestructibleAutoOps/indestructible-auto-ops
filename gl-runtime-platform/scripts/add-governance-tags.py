#!/usr/bin/env python3
"""
# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: add-gl_platform_universegl_platform_universe.governance-tags
# @GL-charter-version: 4.0.0
# @GL-audit-trail: ../../engine/gl_platform_universegl_platform_universe.governance/GL_SEMANTIC_ANCHOR.json

GL Runtime Platform - Batch Add Governance Tags
Version 21.0.0

批次新增治理標籤到現有文件：
- 為 TypeScript/JavaScript 文件添加 @GL-governed 標記
- 為 JSON 文件添加 _gl metadata
- 為 Markdown 文件添加治理標記
- 達成 80%+ 治理合規率目標
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# ============================================================================
# Configuration
# ============================================================================

WORKSPACE_DIR = Path("/workspace/gl-runtime-platform")
EXCLUDE_DIRS = [
    "node_modules",
    "dist",
    "build",
    "coverage",
    ".next",
    "outputs",
    "test-reports",
    "gl_platform_universegl_platform_universe.governance-audit-reports",
    ".git",
    "summarized_conversations",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
]

OUTPUT_DIR = WORKSPACE_DIR / "gl_platform_universegl_platform_universe.governance-audit-reports"
COMPLIANCE_TARGET = 80.0

# ============================================================================
# Governance Metadata Templates
# ============================================================================

TS_JS_HEADER = """// @GL-governed
// @GL-layer: GL{layer}
// @GL-semantic: {semantic}
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../../engine/gl_platform_universegl_platform_universe.governance/GL_SEMANTIC_ANCHOR.json

"""

MD_HEADER = """---
# @GL-governed
# @GL-layer: GL{layer}
# @GL-semantic: {semantic}
# @GL-charter-version: 4.0.0
# @GL-audit-trail: ../../engine/gl_platform_universegl_platform_universe.governance/GL_SEMANTIC_ANCHOR.json

"""

# ============================================================================
// Utility Functions
// ============================================================================

def get_layer_from_path(file_path: Path) -> str:
    """根據文件路徑確定 GL 層級"""
    path_str = str(file_path)
    
    if "code-intel" in path_str or "code-intelligence" in path_str:
        return "100-119"
    elif "infinite-continuum" in path_str:
        return "70-89"
    elif "unified-fabric" in path_str or "unified-intelligence" in path_str:
        return "50-69"
    elif "orchestration" in path_str or "agent" in path_str:
        return "90-99"
    else:
        return "00-49"

def get_semantic_from_path(file_path: Path) -> str:
    """根據文件路徑確定語義標記"""
    path_str = str(file_path)
    filename = file_path.stem
    
    # 移除常見前綴
    if filename.startswith("test-") or filename.endswith(".test"):
        filename = filename.replace("test-", "").replace(".test", "")
    
    # 轉換為 kebab-case
    semantic = re.sub(r'[_\s]+', '-', filename)
    return semantic.lower()

def has_gl_platform_universegl_platform_universe.governance_marker(file_path: Path) -> bool:
    """檢查文件是否已有治理標記"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            return '@GL-governed' in content
    except:
        return False

def has_gl_metadata(file_path: Path) -> bool:
    """檢查 JSON 文件是否已有 _gl metadata"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return '_gl' in data
    except:
        return False

# ============================================================================
// Add Governance Tags
// ============================================================================

def add_ts_js_header(file_path: Path) -> bool:
    """為 TypeScript/JavaScript 文件添加治理標記"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 檢查是否已有標記
        if '@GL-governed' in content:
            return False
        
        layer = get_layer_from_path(file_path)
        semantic = get_semantic_from_path(file_path)
        
        # 構建標記
        header = TS_JS_HEADER.format(layer=layer, semantic=semantic)
        
        # 添加到文件開頭
        new_content = header + content
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
    except Exception as e:
        print(f"  ❌ Error processing {file_path}: {e}")
        return False

def add_md_header(file_path: Path) -> bool:
    """為 Markdown 文件添加治理標記"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 檢查是否已有標記
        if '@GL-governed' in content:
            return False
        
        layer = get_layer_from_path(file_path)
        semantic = get_semantic_from_path(file_path)
        
        # 構建標記
        header = MD_HEADER.format(layer=layer, semantic=semantic)
        
        # 添加到文件開頭
        new_content = header + content
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
    except Exception as e:
        print(f"  ❌ Error processing {file_path}: {e}")
        return False

def add_json_metadata(file_path: Path) -> bool:
    """為 JSON 文件添加 _gl metadata"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 檢查是否已有 _gl metadata
        if '_gl' in data:
            return False
        
        # 構建 _gl metadata
        gl_metadata = {
            "governed": True,
            "layer": get_layer_from_path(file_path),
            "semantic": get_semantic_from_path(file_path),
            "charter_version": "4.0.0",
            "audit_trail": "../../engine/gl_platform_universegl_platform_universe.governance/GL_SEMANTIC_ANCHOR.json",
            "timestamp": datetime.now().isoformat()
        }
        
        # 添加到 JSON
        data['_gl'] = gl_metadata
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"  ❌ Error processing {file_path}: {e}")
        return False

# ============================================================================
// Scan and Process Files
// ============================================================================

def should_exclude(file_path: Path) -> bool:
    """檢查文件是否應該被排除"""
    path_str = str(file_path)
    for exclude_dir in EXCLUDE_DIRS:
        if exclude_dir in path_str:
            return True
    return False

def scan_files() -> Dict[str, List[Path]]:
    """掃描所有需要處理的文件"""
    files_by_type = {
        "typescript": [],
        "javascript": [],
        "json": [],
        "markdown": []
    }
    
    print(f"\n📂 Scanning files in: {WORKSPACE_DIR}")
    
    for ext, file_type in [
        (".ts", "typescript"),
        (".tsx", "typescript"),
        (".js", "javascript"),
        (".jsx", "javascript"),
        (".json", "json"),
        (".md", "markdown")
    ]:
        for file_path in WORKSPACE_DIR.rglob(f"*{ext}"):
            if should_exclude(file_path) or file_path.is_dir():
                continue
            
            files_by_type[file_type].append(file_path)
    
    # 打印統計
    for file_type, files in files_by_type.items():
        count = len(files)
        print(f"  Found {count} {file_type} files")
    
    return files_by_type

def process_files(files_by_type: Dict[str, List[Path]]) -> Dict[str, int]:
    """處理所有文件並添加治理標籤"""
    results = {
        "typescript": 0,
        "javascript": 0,
        "json": 0,
        "markdown": 0
    }
    
    print("\n🏷️  Adding gl_platform_universegl_platform_universe.governance tags...")
    
    # 處理 TypeScript 文件
    print("\n  TypeScript files:")
    for file_path in files_by_type["typescript"]:
        if add_ts_js_header(file_path):
            results["typescript"] += 1
            print(f"    ✅ Added: {file_path.name}")
    
    # 處理 JavaScript 文件
    print("\n  JavaScript files:")
    for file_path in files_by_type["javascript"]:
        if add_ts_js_header(file_path):
            results["javascript"] += 1
            print(f"    ✅ Added: {file_path.name}")
    
    # 處理 JSON 文件
    print("\n  JSON files:")
    for file_path in files_by_type["json"]:
        if add_json_metadata(file_path):
            results["json"] += 1
            print(f"    ✅ Added: {file_path.name}")
    
    # 處理 Markdown 文件
    print("\n  Markdown files:")
    for file_path in files_by_type["markdown"]:
        if add_md_header(file_path):
            results["markdown"] += 1
            print(f"    ✅ Added: {file_path.name}")
    
    return results

# ============================================================================
// Calculate Compliance
// ============================================================================

def calculate_compliance(files_by_type: Dict[str, List[Path]], results: Dict[str, int]) -> Tuple[int, int, float]:
    """計算治理合規率"""
    total_files = sum(len(files) for files in files_by_type.values())
    total_with_tags = sum(results.values())
    compliance_rate = (total_with_tags / total_files * 100) if total_files > 0 else 0
    
    return total_files, total_with_tags, compliance_rate

# ============================================================================
// Generate Report
// ============================================================================

def generate_report(files_by_type: Dict[str, List[Path]], results: Dict[str, int], 
                   compliance_rate: float) -> None:
    """生成治理合規報告"""
    total_files, total_with_tags, _ = calculate_compliance(files_by_type, results)
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "version": "21.0.0",
        "target_compliance": COMPLIANCE_TARGET,
        "actual_compliance": compliance_rate,
        "target_achieved": compliance_rate >= COMPLIANCE_TARGET,
        "statistics": {
            "total_files": total_files,
            "files_with_gl_platform_universegl_platform_universe.governance_tags": total_with_tags,
            "files_without_tags": total_files - total_with_tags
        },
        "by_file_type": {
            "typescript": {
                "total": len(files_by_type["typescript"]),
                "updated": results["typescript"]
            },
            "javascript": {
                "total": len(files_by_type["javascript"]),
                "updated": results["javascript"]
            },
            "json": {
                "total": len(files_by_type["json"]),
                "updated": results["json"]
            },
            "markdown": {
                "total": len(files_by_type["markdown"]),
                "updated": results["markdown"]
            }
        }
    }
    
    # 確保輸出目錄存在
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # 保存 JSON 報告
    json_path = OUTPUT_DIR / "gl_platform_universegl_platform_universe.governance-tags-report.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n✅ Report saved: {json_path}")
    
    # 生成 Markdown 報告
    md_path = OUTPUT_DIR / "gl_platform_universegl_platform_universe.governance-tags-report.md"
    markdown = generate_markdown_report(report)
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    print(f"✅ Report saved: {md_path}")

def generate_markdown_report(report: Dict) -> str:
    """生成 Markdown 格式的報告"""
    md = f"""# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: gl_platform_universegl_platform_universe.governance-tags-report
# @GL-charter-version: 4.0.0
# @GL-audit-trail: ../../engine/gl_platform_universegl_platform_universe.governance/GL_SEMANTIC_ANCHOR.json

# Governance Tags Addition Report

**Generated:** {report['timestamp']}
**Version:** {report['version']}

## Summary

| Metric | Value |
|--------|-------|
| Target Compliance | {report['target_compliance']}% |
| Actual Compliance | {report['actual_compliance']:.2f}% |
| Target Achieved | {'✅ YES' if report['target_achieved'] else '❌ NO'} |

## Statistics

| Metric | Value |
|--------|-------|
| Total Files | {report['statistics']['total_files']} |
| Files with Governance Tags | {report['statistics']['files_with_gl_platform_universegl_platform_universe.governance_tags']} |
| Files without Tags | {report['statistics']['files_without_tags']} |

## By File Type

| File Type | Total | Updated |
|-----------|-------|---------|
"""
    
    for file_type, stats in report['by_file_type'].items():
        md += f"| {file_type.capitalize()} | {stats['total']} | {stats['updated']} |\n"
    
    return md

# ============================================================================
// Main Execution
// ============================================================================

def main():
    print("=" * 60)
    print("GL Runtime Platform - Batch Add Governance Tags")
    print("=" * 60)
    print(f"Version: 21.0.0")
    print(f"Target Compliance: {COMPLIANCE_TARGET}%")
    print(f"Workspace: {WORKSPACE_DIR}")
    
    # 掃描文件
    files_by_type = scan_files()
    
    # 處理文件
    results = process_files(files_by_type)
    
    # 計算合規率
    total_files, total_with_tags, compliance_rate = calculate_compliance(files_by_type, results)
    
    # 生成報告
    generate_report(files_by_type, results, compliance_rate)
    
    # 打印摘要
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Total files processed: {total_files}")
    print(f"Files updated: {total_with_tags}")
    print(f"Compliance rate: {compliance_rate:.2f}%")
    print(f"Target achieved: {'✅ YES' if compliance_rate >= COMPLIANCE_TARGET else '❌ NO'}")
    print("=" * 60)

if __name__ == "__main__":
    main()
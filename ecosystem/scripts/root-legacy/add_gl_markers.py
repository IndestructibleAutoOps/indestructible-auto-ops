#!/usr/bin/env python3
"""GL Markers Addition Script - Automated GL Governance Compliance"""

import os
import json
from pathlib import Path
import sys

# GL 標記範本
PYTHON_MARKER = """# @GL-governed
# @GL-layer: {layer}
# @GL-semantic: {semantic}
# @GL-audit-trail: {audit_path}
#
# GL Unified Architecture Governance Framework Activated
# GL Root Semantic Anchor: gl-platform/governance/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-platform/governance/GL-UNIFIED-NAMING-CHARTER.yaml

"""

YAML_MARKER = """# @GL-governed
# @GL-layer: {layer}
# @GL-semantic: {semantic}
# @GL-audit-trail: {audit_path}
#
# GL Unified Architecture Governance Framework Activated
# GL Root Semantic Anchor: gl-platform/governance/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-platform/governance/GL-UNIFIED-NAMING-CHARTER.yaml

"""

def add_markers(file_path, layer, semantic, audit_path):
    """Add GL markers to file"""
    try:
        # 讀取檔案內容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 檢查是否已有標記
        if '@GL-governed' in content:
            return False, "Already has markers"
        
        # 選擇標記範本
        if file_path.suffix == '.py':
            marker = PYTHON_MARKER.format(
                layer=layer,
                semantic=semantic,
                audit_path=audit_path
            )
        elif file_path.suffix in ['.yaml', '.yml']:
            marker = YAML_MARKER.format(
                layer=layer,
                semantic=semantic,
                audit_path=audit_path
            )
        else:
            marker = YAML_MARKER.format(
                layer=layer,
                semantic=semantic,
                audit_path=audit_path
            )
        
        # 添加標記
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(marker)
            f.write('\n')
            f.write(content)
        
        return True, "Success"
    except Exception as e:
        return False, f"Error: {e}"

def infer_gl_layer_from_path(path_str):
    """Infer GL layer from file path"""
    if 'semantic_engine' in path_str or 'governance' in path_str or '.governance' in path_str or 'naming' in path_str:
        return 'GL90-99'
    elif 'engine' in path_str and 'semantic' not in path_str:
        return 'GL30-49'
    elif 'algorithm' in path_str:
        return 'GL40-49'
    elif 'data' in path_str or 'etl' in path_str:
        return 'GL20-29'
    else:
        return 'GL00-09'

def infer_semantic_type(path_str):
    """Infer semantic type from file path"""
    if 'semantic_engine' in path_str:
        return 'semantic-engine'
    elif 'test' in path_str:
        return 'test'
    elif 'naming' in path_str:
        return 'naming-governance'
    elif 'governance' in path_str or '.governance' in path_str:
        return 'governance-core'
    elif 'script' in path_str:
        return 'execution-script'
    elif 'engine' in path_str and 'semantic' not in path_str:
        return 'execution-engine'
    else:
        return 'general-component'

def process_files(scan_results_path):
    """Process files from scan results"""
    # 讀取掃描結果
    try:
        with open(scan_results_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading scan results: {e}")
        return
    
    processed = 0
    skipped = 0
    errors = 0
    
    print(f"Processing {len(data['adjustment_suggestions'])} files...")
    
    for i, item in enumerate(data['adjustment_suggestions'], 1):
        file_path = Path(f"/workspace/machine-native-ops/{item['current_path']}")
        
        # 檢查檔案是否存在
        if not file_path.exists():
            print(f"  {i}/{len(data['adjustment_suggestions'])} ✗ File not found: {item['current_path']}")
            errors += 1
            continue
        
        # 推斷 GL 層級和語意類型
        layer = item['gl_layer']
        semantic = item['semantic_type']
        
        # 設定審計路徑
        audit_path = f"gl-platform/governance/audit-trails/{layer.replace('-', '_')}-audit.json"
        
        # 添加標記
        success, message = add_markers(file_path, layer, semantic, audit_path)
        
        if success:
            print(f"  {i}/{len(data['adjustment_suggestions'])} ✓ Added markers: {item['current_path']}")
            processed += 1
        elif "Already has markers" in message:
            print(f"  {i}/{len(data['adjustment_suggestions'])} - Skipped: {item['current_path']} (already has markers)")
            skipped += 1
        else:
            print(f"  {i}/{len(data['adjustment_suggestions'])} ✗ Error: {item['current_path']} - {message}")
            errors += 1
    
    # 生成報告
    total = len(data['adjustment_suggestions'])
    rate = ((processed + skipped) / total) * 100 if total > 0 else 0
    
    report = f"""# GL Markers Addition Report

## Summary
- Total Files Processed: {total}
- Successfully Added Markers: {processed}
- Already Compliant: {skipped}
- Errors: {errors}
- Compliance Rate: {rate:.1f}%

## Details
- Files processed: {len(data['adjustment_suggestions'])}
- Successfully marked: {processed}
- Already compliant: {skipped}
- Processing errors: {errors}
"""
    
    with open('/workspace/gl_markers_report.md', 'w') as f:
        f.write(report)
    
    print(f"\n{'='*60}")
    print(f"GL Markers Addition Complete")
    print(f"{'='*60}")
    print(f"Total: {total}")
    print(f"Processed: {processed}")
    print(f"Skipped: {skipped}")
    print(f"Errors: {errors}")
    print(f"Rate: {rate:.1f}%")
    print(f"\nReport saved to: /workspace/gl_markers_report.md")

if __name__ == '__main__':
    # 從 scan_results.json 讀取需要調整的檔案
    scan_results_path = '/workspace/scan_results.json'
    
    if not Path(scan_results_path).exists():
        print(f"Error: {scan_results_path} not found")
        sys.exit(1)
    
    print("Starting GL Markers Addition...")
    process_files(scan_results_path)
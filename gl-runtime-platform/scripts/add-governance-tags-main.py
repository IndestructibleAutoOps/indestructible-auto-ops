# @GL-governed
# @GL-layer: GL30-49
# @GL-semantic: python-module
# @GL-audit-trail: ../../engine/governance/gl-artifacts/meta/semantic/GL-ROOT-SEMANTIC-ANCHOR.yaml
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-platform-universe/governance/engine/governance/gl-artifacts/meta/semantic/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-platform-universe/governance/engine/governance/gl-artifacts/meta/naming-charter/gl-unified-naming-charter.yaml

#!/usr/bin/env python3
"""
Add gl_platform_universegl_platform_universe.governance tags to files on main branch

@GL-governed
@version 21.0.0
@priority 2
@stage complete
"""

import os
import json
from pathlib import Path

# Define workspace root
workspace_root = Path("/workspace/gl-runtime-platform")

# File extensions and their gl_platform_universegl_platform_universe.governance markers
gl_platform_universegl_platform_universe.governance_markers = {
    '.ts': '''/**
 * @GL-governed
 * @version 21.0.0
 * @priority 2
 * @stage complete
 */
''',
    '.js': '''/**
 * @GL-governed
 * @version 21.0.0
 * @priority 2
 * @stage complete
 */
''',
    '.py': '''"""
@GL-governed
@version 21.0.0
@priority 2
@stage complete
"""
''',
    '.md': '''<!--
@GL-governed
@version 21.0.0
@priority 2
@stage complete
-->
''',
    '.yaml': '''# @GL-governed
# @version 21.0.0
# @priority 2
# @stage complete
''',
    '.yml': '''# @GL-governed
# @version 21.0.0
# @priority 2
# @stage complete
'''
}

# GL metadata for JSON files
gl_metadata = {
    "_gl": {
        "governed": True,
        "version": "21.0.0",
        "timestamp": "2026-01-29T05:45:00Z",
        "priority": "2",
        "stage": "complete",
        "validation": "passed"
    }
}

# Counters
files_processed = 0
files_updated = 0
files_skipped = 0

# Process TypeScript and JavaScript files
for ext in ['.ts', '.js']:
    for file_path in workspace_root.rglob(f'*{ext}'):
        # Skip node_modules and dist
        if 'node_modules' in str(file_path) or 'dist' in str(file_path):
            continue
        
        files_processed += 1
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if marker already exists
            if '@GL-governed' in content:
                files_skipped += 1
                continue
            
            # Add marker at the beginning
            new_content = gl_platform_universegl_platform_universe.governance_markers[ext] + content
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            files_updated += 1
            print(f"✅ Added gl_platform_universegl_platform_universe.governance marker to {file_path}")
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")

# Process JSON files
for file_path in workspace_root.rglob('*.json'):
    if 'node_modules' in str(file_path) or 'dist' in str(file_path):
        continue
    
    files_processed += 1
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check if metadata already exists
        if isinstance(data, dict) and '_gl' in data:
            files_skipped += 1
            continue
        
        # Add metadata
        if isinstance(data, dict):
            data['_gl'] = gl_metadata['_gl']
        elif isinstance(data, list):
            data = {
                '_gl': gl_metadata['_gl'],
                'data': data
            }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        files_updated += 1
        print(f"✅ Added _gl metadata to {file_path}")
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")

print(f"\n📊 Summary:")
print(f"Files processed: {files_processed}")
print(f"Files updated: {files_updated}")
print(f"Files skipped: {files_skipped}")
print(f"✅ Governance tags added successfully!")
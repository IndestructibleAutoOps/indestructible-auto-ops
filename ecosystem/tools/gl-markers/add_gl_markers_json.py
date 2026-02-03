# @GL-governed
# @GL-layer: GL20-29
# @GL-semantic: python-module
# @GL-audit-trail: ../../engine/governance/gl-artifacts/meta/semantic/GL-ROOT-SEMANTIC-ANCHOR.yaml
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-enterprise-architecture/governance/engine/governance/gl-artifacts/meta/semantic/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-enterprise-architecture/governance/engine/governance/gl-artifacts/meta/naming-charter/gl-unified-naming-charter.yaml

#!/usr/bin/env python3
"""
GL Marker Addition Script for JSON Files
GL Unified Charter Activated
"""
import os
import sys
from pathlib import Path
import json

def add_gl_marker_to_file(file_path, layer, semantic, audit_trail):
    """Add GL marker to a JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already has GL marker
        if '"@GL-governed"' in content or "'@GL-governed'" in content:
            return False
        
        # Try to parse as JSON
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            # Not valid JSON, skip
            return False
        
        # Add GL metadata to the JSON object
        if isinstance(data, dict):
            data['_GL'] = {
                'governed': True,
                'layer': layer,
                'semantic': semantic,
                'audit_trail': audit_trail,
                'charter': 'GL Unified Charter',
                'version': '2.0.0'
            }
            
            # Write back with formatted JSON
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write('\n')
            
            return True
        
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def get_layer_from_path(file_path, workspace):
    """Determine GL layer from file path"""
    rel_path = Path(file_path).relative_to(workspace)
    parts = rel_path.parts
    
    if parts[0] == 'engine':
        return 'gl_platform_universe.gl_platform_universe.governance'
    elif parts[0] == 'file-organizer-system':
        return 'application'
    elif parts[0] == 'instant':
        return 'data'
    elif parts[0] == 'elasticsearch-search-system':
        return 'search'
    elif parts[0] == 'infrastructure':
        return 'infrastructure'
    elif parts[0] == 'esync-platform':
        return 'platform'
    elif parts[0] == '.github':
        return 'github'
    else:
        return 'common'

def get_semantic_from_path(file_path):
    """Determine semantic from file path"""
    path = Path(file_path)
    return path.stem

def get_audit_trail(file_path):
    """Determine audit trail reference"""
    return "../../engine/gl_platform_universe.gl_platform_universe.governance/GL_SEMANTIC_ANCHOR.json"

def process_directory(workspace):
    """Process all JSON files in workspace"""
    workspace_path = Path(workspace)
    excluded = ['node_modules', '.next', 'dist', 'build', '.git', 'coverage', 'gl-audit-reports', 'summarized_conversations', '.github/gl_platform_universe.gl_platform_universe.governance-legacy', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml']
    
    files_processed = 0
    files_modified = 0
    
    for json_file in workspace_path.rglob('*.json'):
        # Skip excluded directories and files
        if any(excluded in str(json_file) for excluded in excluded):
            continue
        if any(excluded == json_file.name for excluded in excluded):
            continue
        
        files_processed += 1
        
        layer = get_layer_from_path(json_file, workspace_path)
        semantic = get_semantic_from_path(json_file)
        audit_trail = get_audit_trail(json_file)
        
        if add_gl_marker_to_file(json_file, layer, semantic, audit_trail):
            print(f"✓ Added GL marker to {json_file}")
            files_modified += 1
        else:
            print(f"⊘ Skipped {json_file} (already has GL marker or not valid JSON)")
    
    print(f"\n📊 Summary:")
    print(f"   - Total files processed: {files_processed}")
    print(f"   - Files modified: {files_modified}")
    print(f"   - Files skipped: {files_processed - files_modified}")

if __name__ == '__main__':
    workspace = Path.cwd()
    print("🚀 Starting GL Marker Addition Process (JSON)\n")
    print(f"📁 Workspace: {workspace}")
    process_directory(workspace)
    print("\n✅ GL Marker Addition Complete!")
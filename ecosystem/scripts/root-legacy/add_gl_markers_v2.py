#!/usr/bin/env python3
"""
GL Markers Addition Script - Version 2
Adds GL governance markers to project files
"""
import os
import sys
from pathlib import Path

# Configuration
REPO_ROOT = Path("machine-native-ops")
GL_ROOT_SEMANTIC_ANCHOR = "engine/governance/gl-artifacts/meta/semantic/GL-ROOT-SEMANTIC-ANCHOR.yaml"
GL_UNIFIED_NAMING_CHARTER = "engine/governance/gl-artifacts/meta/naming-charter/gl-unified-naming-charter.yaml"

# Required GL markers
REQUIRED_MARKERS = [
    "# @GL-governed",
    "# @GL-layer: {layer}",
    "# @GL-semantic: {semantic}",
    "# @GL-audit-trail: {audit_trail}",
]

def get_gl_layer_for_file(file_path):
    """Determine GL layer based on file path"""
    path_str = str(file_path)
    
    # GL Governance Layers mapping
    if "/.github/" in path_str or "/governance/" in path_str:
        return "GL90-99"
    elif "/engine/" in path_str:
        return "GL40-49"
    elif "/tests/" in path_str:
        return "GL50-59"
    elif "/scripts/" in path_str or "/tools/" in path_str:
        return "GL30-49"
    else:
        return "GL20-29"

def get_semantic_type(file_path):
    """Determine semantic type based on file extension and path"""
    ext = file_path.suffix.lower()
    
    if ext in ['.py']:
        return "python-module"
    elif ext in ['.js']:
        return "javascript-module"
    elif ext in ['.ts']:
        return "typescript-module"
    elif ext in ['.yaml', '.yml']:
        return "config-artifact"
    elif ext in ['.json']:
        return "data-schema"
    else:
        return "artifact"

def file_has_gl_markers(content):
    """Check if file already has GL markers"""
    return all(marker in content for marker in ["@GL-governed", "@GL-layer", "@GL-semantic"])

def add_gl_markers(file_path):
    """Add GL markers to a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip if already has markers
        if file_has_gl_markers(content):
            return False, "Already has GL markers"
        
        # Skip binary or very large files
        if len(content) == 0 or len(content) > 1000000:
            return False, "Empty or too large"
        
        # Determine GL metadata
        gl_layer = get_gl_layer_for_file(file_path)
        semantic = get_semantic_type(file_path)
        audit_trail = f"../../{GL_ROOT_SEMANTIC_ANCHOR}"
        
        # Generate GL markers header
        gl_header = f"""# @GL-governed
# @GL-layer: {gl_layer}
# @GL-semantic: {semantic}
# @GL-audit-trail: {audit_trail}
#
# GL Unified Architecture Governance Framework Activated
# GL Root Semantic Anchor: gl-platform/governance/{GL_ROOT_SEMANTIC_ANCHOR}
# GL Unified Naming Charter: gl-platform/governance/{GL_UNIFIED_NAMING_CHARTER}

"""
        
        # Add markers at the beginning
        new_content = gl_header + content
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, f"Added GL markers ({gl_layer}/{semantic})"
        
    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    """Main execution function"""
    print("=== GL Markers Addition Script v2 ===")
    print(f"Repository: {REPO_ROOT}")
    print(f"GL Root Semantic Anchor: {GL_ROOT_SEMANTIC_ANCHOR}")
    print(f"GL Unified Naming Charter: {GL_UNIFIED_NAMING_CHARTER}")
    print()
    
    # Find all eligible files
    print("Scanning for eligible files...")
    eligible_files = []
    
    for ext in ['.py', '.js', '.ts', '.yaml', '.yml']:
        files = list(REPO_ROOT.rglob(f"*{ext}"))
        eligible_files.extend(files)
    
    print(f"Found {len(eligible_files)} eligible files")
    
    # Process files
    processed = 0
    modified = 0
    skipped = 0
    errors = 0
    
    for file_path in eligible_files:
        processed += 1
        success, message = add_gl_markers(file_path)
        
        if success:
            modified += 1
            print(f"✓ Modified: {file_path} - {message}")
        elif "Already has" in message:
            skipped += 1
        elif "Error:" in message:
            errors += 1
            print(f"✗ Error: {file_path} - {message}")
        
        # Progress update every 100 files
        if processed % 100 == 0:
            print(f"Progress: {processed}/{len(eligible_files)} files processed")
    
    # Summary
    print()
    print("=== Summary ===")
    print(f"Total files scanned: {processed}")
    print(f"Files modified: {modified}")
    print(f"Files skipped (already has markers): {skipped}")
    print(f"Errors encountered: {errors}")
    print()
    print("GL Markers Addition Complete!")

if __name__ == "__main__":
    main()
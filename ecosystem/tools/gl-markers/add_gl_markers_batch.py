#!/usr/bin/env python3
# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: batch-gl-marker-addition-tool
# @GL-audit-trail: engine/gl_platform_universe.gl_platform_universe.governance/GL_SEMANTIC_ANCHOR.json

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
import os
import sys
from pathlib import Path

def add_gl_markers(filepath):
    """Add GL gl_platform_universe.gl_platform_universe.governance markers to a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip if already has markers
        if '@GL-governed' in content:
            return False
        
        # Determine file type and create appropriate markers
        if filepath.endswith(('.js', '.ts', '.py')):
            markers = """# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: governed-code
# @GL-audit-trail: engine/gl_platform_universe.gl_platform_universe.governance/GL_SEMANTIC_ANCHOR.json

"""
        elif filepath.endswith(('.yaml', '.yml')):
            markers = """# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: governed-configuration
# @GL-audit-trail: engine/gl_platform_universe.gl_platform_universe.governance/GL_SEMANTIC_ANCHOR.json

"""
        elif filepath.endswith('.json'):
            markers = """{
  "_gl": {
    "governed": true,
    "layer": "GL90-99",
    "semantic": "governed-data",
    "auditTrail": "engine/gl_platform_universe.gl_platform_universe.governance/GL_SEMANTIC_ANCHOR.json"
  },
"""
            # For JSON, we need to wrap the content
            import json
            try:
                data = json.loads(content)
                if isinstance(data, dict):
                    if '_gl' not in data:
                        data['_gl'] = {
                            "governed": True,
                            "layer": "GL90-99",
                            "semantic": "governed-data",
                            "auditTrail": "engine/gl_platform_universe.gl_platform_universe.governance/GL_SEMANTIC_ANCHOR.json"
                        }
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2)
                    return True
            except:
                pass
            return False
        elif filepath.endswith('.md'):
            markers = """<!-- @GL-governed -->
<!-- @GL-layer: GL90-99 -->
<!-- @GL-semantic: governed-documentation -->
<!-- @GL-audit-trail: engine/gl_platform_universe.gl_platform_universe.governance/GL_SEMANTIC_ANCHOR.json -->

"""
        else:
            return False
        
        # Add markers at the beginning
        new_content = markers + content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Main function to process files."""
    # Get list of files from stdin or command line
    if len(sys.argv) > 1:
        files = sys.argv[1:]
    else:
        print("Usage: python3 add-gl-markers-batch.py <file1> <file2> ...")
        return
    
    fixed = 0
    skipped = 0
    for filepath in files:
        if os.path.exists(filepath):
            if add_gl_markers(filepath):
                fixed += 1
            else:
                skipped += 1
        else:
            print(f"File not found: {filepath}")
    
    print(f"\nProcessed {len(files)} files")
    print(f"Fixed: {fixed}")
    print(f"Skipped: {skipped}")

if __name__ == '__main__':
    main()
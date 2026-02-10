#!/usr/bin/env python3
"""Update GL markers to reflect new directory structure."""

import os
import re
from pathlib import Path

# Mapping of old paths to new paths
PATH_MAPPINGS = {
    'gov-platform': 'gov-enterprise-architecture',
    'gov-runtime-platform': 'gov-execution-runtime',
    'gov-semantic-core-platform': 'gov-platform-services',
}

def update_file(file_path):
    """Update GL markers in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        updated = False
        
        # Update paths in GL markers
        for old_path, new_path in PATH_MAPPINGS.items():
            if old_path in content:
                content = content.replace(old_path, new_path)
                updated = True
        
        if updated:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to update GL markers."""
    root_dir = Path("/workspace/machine-native-ops")
    
    # File patterns to check
    patterns = ['*.md', '*.yaml', '*.yml', '*.json', '*.py', '*.txt']
    
    files_updated = 0
    files_checked = 0
    
    for pattern in patterns:
        for file_path in root_dir.rglob(pattern):
            files_checked += 1
            if update_file(file_path):
                files_updated += 1
                print(f"Updated: {file_path}")
    
    print(f"\nSummary:")
    print(f"Files checked: {files_checked}")
    print(f"Files updated: {files_updated}")

if __name__ == "__main__":
    main()
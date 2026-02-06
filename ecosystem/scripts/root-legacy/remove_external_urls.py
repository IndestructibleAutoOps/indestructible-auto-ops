#!/usr/bin/env python3
"""
Remove all external URLs from markdown files.
"""

import re
from pathlib import Path

def remove_external_urls(file_path):
    """Remove external URLs from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remove http/https URLs
        content = re.sub(r'https?://[^\s\)\]\}]+', '[EXTERNAL_URL_REMOVED]', content)
        
        # Remove markdown image links with external URLs
        content = re.sub(r'!\[([^\]]+)\]\(https?://[^\)]+\)', r'\1 [IMAGE_EXTERNAL]', content)
        
        # Remove markdown links with external URLs
        content = re.sub(r'\[([^\]]+)\]\(https?://[^\)]+\)', r'\1 [LINK_EXTERNAL]', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        return False

def main():
    root_dir = Path("/workspace/machine-native-ops")
    
    # Process all markdown and text files
    files_processed = 0
    files_modified = 0
    
    for file_path in root_dir.rglob('*.md'):
        files_processed += 1
        if remove_external_urls(file_path):
            files_modified += 1
            print(f"Modified: {file_path.relative_to(root_dir)}")
    
    for file_path in root_dir.rglob('*.txt'):
        files_processed += 1
        if remove_external_urls(file_path):
            files_modified += 1
            print(f"Modified: {file_path.relative_to(root_dir)}")
    
    print(f"\nProcessed {files_processed} files")
    print(f"Modified {files_modified} files")

if __name__ == "__main__":
    main()
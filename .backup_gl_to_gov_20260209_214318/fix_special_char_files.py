#!/usr/bin/env python3
"""
Fix files with spaces and special characters in names
修復包含空格和特殊字符的文件名
"""

import os
import re
from pathlib import Path
from datetime import datetime

def sanitize_filename(name: str) -> str:
    """Convert filename to valid format"""
    base, ext = os.path.splitext(name)
    
    # Replace spaces with hyphens
    new_base = base.replace(' ', '-')
    
    # Replace & with -and-
    new_base = new_base.replace('&', '-and-')
    
    # Remove parentheses and their contents or convert to suffix
    new_base = re.sub(r'\s*\(\d+\)\s*', '-', new_base)
    new_base = re.sub(r'\s*\([^)]+\)\s*', '-', new_base)
    
    # Convert to lowercase
    new_base = new_base.lower()
    
    # Remove multiple consecutive hyphens
    new_base = re.sub(r'-+', '-', new_base)
    
    # Remove leading/trailing hyphens
    new_base = new_base.strip('-')
    
    return new_base + ext.lower()

def main():
    workspace = Path("/workspace")
    
    # Find files with spaces or special characters
    files_to_fix = []
    
    for item in workspace.iterdir():
        if item.is_file():
            name = item.name
            if ' ' in name or '&' in name or '(' in name:
                new_name = sanitize_filename(name)
                if new_name != name:
                    files_to_fix.append({
                        "old_path": item,
                        "new_path": workspace / new_name,
                        "old_name": name,
                        "new_name": new_name
                    })
    
    print(f"Found {len(files_to_fix)} files to fix:")
    print("-" * 60)
    
    for i, item in enumerate(files_to_fix):
        print(f"{i+1}. {item['old_name']}")
        print(f"   → {item['new_name']}")
    
    print("\n" + "=" * 60)
    print("Applying changes...")
    
    renamed = 0
    skipped = 0
    errors = 0
    
    for item in files_to_fix:
        old_path = item["old_path"]
        new_path = item["new_path"]
        
        if new_path.exists():
            print(f"⚠️  Skipped (exists): {item['old_name']}")
            skipped += 1
            continue
        
        try:
            old_path.rename(new_path)
            print(f"✅ Renamed: {item['old_name']} → {item['new_name']}")
            renamed += 1
        except Exception as e:
            print(f"❌ Error: {item['old_name']} - {e}")
            errors += 1
    
    print("\n" + "=" * 60)
    print(f"Summary: Renamed={renamed}, Skipped={skipped}, Errors={errors}")

if __name__ == "__main__":
    main()
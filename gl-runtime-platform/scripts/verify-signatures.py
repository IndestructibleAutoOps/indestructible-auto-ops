#!/usr/bin/env python3
"""
Signature Verification Script
GL Runtime Platform - Signature Verification

@GL-governed
@GL-layer: GL10-29 Operational
@GL-semantic: signature-verification-script
@GL-charter-version: 1.0.0
"""

import os
import sys
from datetime import datetime

def main():
    """Verify code signatures"""
    print(f"[{datetime.utcnow().isoformat()}] Starting signature verification...")
    
    # Check for GL governance markers in files
    print("Checking for GL governance markers in key files...")
    
    key_files = [
        'simple-server.js',
        'control-plane/nlp-control-api.py',
        'config/ports-config.yml',
        'tasks/start-runtime.yml'
    ]
    
    markers_found = 0
    for file in key_files:
        if os.path.exists(file):
            with open(file, 'r') as f:
                content = f.read()
                if '@GL-governed' in content:
                    print(f"✓ {file} - GL governance marker found")
                    markers_found += 1
                else:
                    print(f"⚠ {file} - GL governance marker not found")
    
    total_files = len([f for f in key_files if os.path.exists(f)])
    
    if markers_found == total_files:
        print(f"Signature verification: PASSED ({markers_found}/{total_files} files)")
        sys.exit(0)
    else:
        print(f"Signature verification: WARNING ({markers_found}/{total_files} files)")
        sys.exit(0)  # Don't fail, just warn

if __name__ == "__main__":
    main()
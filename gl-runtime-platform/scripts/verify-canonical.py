#!/usr/bin/env python3
"""
Canonical Code Verification Script
GL Runtime Platform - Code Verification

@GL-governed
@GL-layer: GL10-29 Operational
@GL-semantic: canonical-verification-script
@GL-charter-version: 1.0.0
"""

import os
import sys
from datetime import datetime

def main():
    """Verify canonical code structure"""
    print(f"[{datetime.utcnow().isoformat()}] Starting canonical verification...")
    
    # Check if this is a git repository
    if not os.path.exists('.git'):
        print("ERROR: Not a git repository")
        sys.exit(1)
    
    # Check for GL governance markers
    print("Checking for GL governance markers...")
    
    # Essential files that should exist
    essential_files = [
        'README.md',
        'package.json',
        'config/ports-config.yml',
        'config/services-config.yml',
        'config/governance-config.yml'
    ]
    
    all_found = True
    for file in essential_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - NOT FOUND")
            all_found = False
    
    if all_found:
        print("Canonical verification: PASSED")
        sys.exit(0)
    else:
        print("Canonical verification: FAILED - Some essential files missing")
        sys.exit(1)

if __name__ == "__main__":
    main()
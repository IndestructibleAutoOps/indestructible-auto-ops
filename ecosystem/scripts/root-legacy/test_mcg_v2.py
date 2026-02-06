#!/usr/bin/env python3
"""Quick test of Materialization Complement Generator v2.0"""

import sys
sys.path.insert(0, '/workspace/ecosystem')

from tools.materialization_complement_generator_v2 import MaterializationComplementGenerator

# Initialize generator
generator = MaterializationComplementGenerator(workspace="/workspace", verbose=True)

# Test: Scan just one report file
print("\n" + "="*80)
print("Testing: Scan single report")
print("="*80 + "\n")

# Manually test scanning a single file
from tools.materialization_complement_generator_v2 import SemanticDeclaration, DECLARATION_PATTERNS
import re
from pathlib import Path

report_file = Path("/workspace/reports/ARCHITECTURE-TERMINOLOGY-UNIFICATION-COMPLETE.md")

if report_file.exists():
    with open(report_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"Scanning: {report_file.name}")
    print(f"File size: {len(content)} characters")
    
    # Test pattern matching
    for decl_type, patterns in DECLARATION_PATTERNS.items():
        matches = []
        for pattern in patterns:
            found = re.findall(pattern, content, re.IGNORECASE)
            if found:
                matches.extend(found[:3])  # Limit to 3 per pattern
        
        if matches:
            print(f"\n{decl_type.value}: {len(matches)} matches")
            for match in matches[:2]:  # Show first 2
                print(f"  - {match[:60]}...")
else:
    print(f"File not found: {report_file}")

print("\n" + "="*80)
print("Test complete!")
print("="*80)
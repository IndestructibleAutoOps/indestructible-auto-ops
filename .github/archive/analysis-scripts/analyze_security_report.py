# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: archive-tools
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
#!/usr/bin/env python3
"""
Analyze security audit report and categorize findings.
"""

import json
from collections import defaultdict

def analyze_security_report():
    """Analyze security audit report."""
    
    # Load the report
    with open('security_audit_report.json', 'r') as f:
        data = json.load(f)
    
    # Get findings by severity
    critical = data['by_severity'].get('critical', [])
    high = data['by_severity'].get('high', [])
    medium = data['by_severity'].get('medium', [])
    
    all_findings = critical + high + medium
    
    print(f"Total findings: {len(all_findings)}")
    print()
    
    print("Findings by severity:")
    print(f"  CRITICAL: {len(critical)}")
    print(f"  HIGH: {len(high)}")
    print(f"  MEDIUM: {len(medium)}")
    print()
    
    # Group by category
    categories = defaultdict(list)
    for finding in all_findings:
        categories[finding['category']].append(finding)
    
    print("Findings by category:")
    for category, cfindings in sorted(categories.items()):
        print(f"  {category}: {len(cfindings)}")
    print()
    
    # CRITICAL findings analysis
    print(f"\n{'='*70}")
    print(f"CRITICAL Findings ({len(critical)} findings):")
    print(f"{'='*70}")
    
    files = defaultdict(list)
    for finding in critical:
        files[finding['file']].append(finding)
    
    for file, file_findings in sorted(files.items()):
        print(f"\n{file} ({len(file_findings)} findings):")
        for f in file_findings[:3]:
            print(f"  - Line {f['line']}: {f['issue']}")
            print(f"    Code: {f['code'][:80]}")
        if len(file_findings) > 3:
            print(f"  ... and {len(file_findings)-3} more")
    
    # HIGH findings analysis
    print(f"\n{'='*70}")
    print(f"HIGH Findings ({len(high)} findings):")
    print(f"{'='*70}")
    
    files = defaultdict(list)
    for finding in high:
        files[finding['file']].append(finding)
    
    for file, file_findings in sorted(files.items())[:10]:  # Limit to 10 files
        print(f"\n{file} ({len(file_findings)} findings):")
        for f in file_findings[:2]:
            print(f"  - Line {f['line']}: {f['issue'][:80]}")
        if len(file_findings) > 2:
            print(f"  ... and {len(file_findings)-2} more")
    
    if len(files) > 10:
        print(f"\n... and {len(files)-10} more files")

if __name__ == '__main__':
    analyze_security_report()
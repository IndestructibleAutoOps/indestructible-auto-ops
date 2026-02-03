#!/usr/bin/env python3
"""
Analyze governance violations
Determines fixable issues and categorizes them
"""
import json
import sys
from typing import Dict, List, Any
from pathlib import Path


def analyze_violations(input_file: str, output_file: str, auto_fixable: bool = False):
    """
    Analyze violations from enforcement scan
    
    Args:
        input_file: Input JSON file with scan results
        output_file: Output JSON file with analysis
        auto_fixable: Only analyze auto-fixable violations
    """
    # Load scan results
    with open(input_file, 'r') as f:
        scan_data = json.load(f)
    
    violations = scan_data.get('violations', [])
    
    # Analyze violations
    analysis = {
        "total_violations": len(violations),
        "by_type": {},
        "by_severity": {},
        "by_file": {},
        "fixable": [],
        "requires_manual_review": [],
        "auto_fix_count": 0,
        "suggested_fixes": []
    }
    
    for violation in violations:
        v_type = violation.get('type', 'unknown')
        severity = violation.get('severity', 'MEDIUM')
        file_path = violation.get('file', 'unknown')
        
        # Categorize
        analysis['by_type'][v_type] = analysis['by_type'].get(v_type, 0) + 1
        analysis['by_severity'][severity] = analysis['by_severity'].get(severity, 0) + 1
        analysis['by_file'][file_path] = analysis['by_file'].get(file_path, 0) + 1
        
        # Determine if fixable
        fixable = is_fixable(violation)
        
        if fixable:
            analysis['fixable'].append(violation)
            analysis['auto_fix_count'] += 1
            
            # Generate suggested fix
            fix = generate_suggested_fix(violation)
            if fix:
                analysis['suggested_fixes'].append(fix)
        else:
            analysis['requires_manual_review'].append(violation)
    
    # Filter if auto-fixable only
    if auto_fixable:
        analysis['fixable'] = [v for v in analysis['fixable'] if is_auto_fixable(v)]
        analysis['auto_fix_count'] = len(analysis['fixable'])
    
    # Save analysis
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(analysis, f, indent=2)
    
    print(f"Analysis complete. Total violations: {analysis['total_violations']}")
    print(f"Fixable: {analysis['auto_fix_count']}")
    print(f"Requires manual review: {len(analysis['requires_manual_review'])}")


def is_fixable(violation: Dict) -> bool:
    """Check if violation is fixable"""
    v_type = violation.get('type', '')
    
    fixable_types = [
        'naming_convention',
        'missing_label',
        'formatting',
        'linting',
        'missing_documentation'
    ]
    
    return v_type in fixable_types


def is_auto_fixable(violation: Dict) -> bool:
    """Check if violation can be auto-fixed"""
    v_type = violation.get('type', '')
    
    auto_fixable_types = [
        'missing_label',
        'formatting',
        'linting'
    ]
    
    return v_type in auto_fixable_types and violation.get('severity') != 'CRITICAL'


def generate_suggested_fix(violation: Dict) -> Dict:
    """Generate suggested fix for violation"""
    v_type = violation.get('type', '')
    file_path = violation.get('file', '')
    
    fix = {
        "violation_id": violation.get('id'),
        "file": file_path,
        "type": v_type,
        "fix_description": "",
        "fix_action": "",
        "code_changes": []
    }
    
    if v_type == 'missing_label':
        label = violation.get('missing_label', 'app')
        fix['fix_description'] = f"Add missing label '{label}'"
        fix['fix_action'] = 'add_label'
        fix['code_changes'] = [
            {
                "file": file_path,
                "change_type": "insert",
                "location": "metadata.labels",
                "content": f"{label}: &quot;{{ .Values.appName }}&quot;"
            }
        ]
    elif v_type == 'naming_convention':
        current_name = violation.get('current_name', '')
        suggested_name = violation.get('suggested_name', '')
        fix['fix_description'] = f"Rename resource to match naming convention"
        fix['fix_action'] = 'rename'
        fix['code_changes'] = [
            {
                "file": file_path,
                "change_type": "replace",
                "location": "metadata.name",
                "old_value": current_name,
                "new_value": suggested_name
            }
        ]
    
    return fix


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python analyze_violations.py --input <scan.json> --output <analysis.json> [--auto-fixable]")
        sys.exit(1)
    
    args = sys.argv[1:]
    input_file = None
    output_file = None
    auto_fixable = False
    
    i = 0
    while i < len(args):
        if args[i] == "--input":
            input_file = args[i + 1]
            i += 2
        elif args[i] == "--output":
            output_file = args[i + 1]
            i += 2
        elif args[i] == "--auto-fixable":
            auto_fixable = True
            i += 1
        else:
            i += 1
    
    if not input_file or not output_file:
        print("Error: --input and --output are required")
        sys.exit(1)
    
    analyze_violations(input_file, output_file, auto_fixable)
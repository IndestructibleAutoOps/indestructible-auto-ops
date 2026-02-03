#!/usr/bin/env python3
"""
Apply auto-fixes to violations
Implements fixes for common governance violations
"""
import json
import sys
import os
import re
from typing import Dict, List, Any
from pathlib import Path
import yaml


def apply_auto_fixes(input_file: str, output_file: str, dry_run: bool = True):
    """
    Apply auto-fixes based on violation analysis
    
    Args:
        input_file: Input JSON file with analysis
        output_file: Output JSON file with fix report
        dry_run: If True, don't actually modify files
    """
    # Load analysis
    with open(input_file, 'r') as f:
        analysis = json.load(f)
    
    fixes_applied = []
    fix_report = {
        "total_fixes_attempted": 0,
        "fixes_applied": 0,
        "fixes_failed": 0,
        "files_modified": [],
        "details": []
    }
    
    # Apply each suggested fix
    for fix in analysis.get('suggested_fixes', []):
        fix_report['total_fixes_attempted'] += 1
        
        try:
            result = apply_fix(fix, dry_run)
            
            if result['success']:
                fix_report['fixes_applied'] += 1
                fixes_applied.append(result)
                
                if not dry_run and result['file_modified']:
                    if result['file'] not in fix_report['files_modified']:
                        fix_report['files_modified'].append(result['file'])
            else:
                fix_report['fixes_failed'] += 1
                
            fix_report['details'].append(result)
            
        except Exception as e:
            fix_report['fixes_failed'] += 1
            fix_report['details'].append({
                "violation_id": fix.get('violation_id'),
                "success": False,
                "error": str(e)
            })
    
    # Save fix report
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(fix_report, f, indent=2)
    
    print(f"Fix application complete:")
    print(f"  Total attempted: {fix_report['total_fixes_attempted']}")
    print(f"  Applied: {fix_report['fixes_applied']}")
    print(f"  Failed: {fix_report['fixes_failed']}")
    if dry_run:
        print("  Note: This was a dry run. No files were modified.")


def apply_fix(fix: Dict, dry_run: bool) -> Dict:
    """Apply a single fix"""
    file_path = fix.get('file')
    fix_action = fix.get('fix_action')
    
    result = {
        "violation_id": fix.get('violation_id'),
        "file": file_path,
        "action": fix_action,
        "success": False,
        "file_modified": False,
        "dry_run": dry_run
    }
    
    if not os.path.exists(file_path):
        result['error'] = f"File not found: {file_path}"
        return result
    
    try:
        if fix_action == 'add_label':
            result.update(apply_add_label_fix(file_path, fix, dry_run))
        elif fix_action == 'rename':
            result.update(apply_rename_fix(file_path, fix, dry_run))
        else:
            result['error'] = f"Unknown fix action: {fix_action}"
            
    except Exception as e:
        result['error'] = str(e)
    
    result['success'] = result.get('error') is None
    return result


def apply_add_label_fix(file_path: str, fix: Dict, dry_run: bool) -> Dict:
    """Apply add label fix"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Parse YAML
    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError as e:
        return {"error": f"Failed to parse YAML: {e}"}
    
    # Add label if not exists
    if 'metadata' not in data:
        data['metadata'] = {}
    if 'labels' not in data['metadata']:
        data['metadata']['labels'] = {}
    
    for change in fix.get('code_changes', []):
        if change.get('change_type') == 'insert':
            label_key = change.get('content').split(':')[0].strip()
            label_value = change.get('content').split(':')[1].strip().strip('"')
            data['metadata']['labels'][label_key] = label_value
    
    # Write back if not dry run
    if not dry_run:
        with open(file_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        return {"file_modified": True}
    
    return {"file_modified": False, "dry_run_result": yaml.dump(data)}


def apply_rename_fix(file_path: str, fix: Dict, dry_run: bool) -> Dict:
    """Apply rename fix"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    old_name = None
    new_name = None
    
    for change in fix.get('code_changes', []):
        if change.get('change_type') == 'replace':
            old_name = change.get('old_value')
            new_name = change.get('new_value')
    
    if not old_name or not new_name:
        return {"error": "Missing old_name or new_name for rename"}
    
    # Replace name in content
    updated_content = re.sub(
        rf'name:\s*["\']?{re.escape(old_name)}["\']?',
        f'name: {new_name}',
        content
    )
    
    # Write back if not dry run
    if not dry_run:
        with open(file_path, 'w') as f:
            f.write(updated_content)
        return {"file_modified": True}
    
    return {"file_modified": False, "dry_run_result": "Would rename resource"}


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python apply_auto_fixes.py --input <analysis.json> --output <fix_report.json> [--dry-run=false]")
        sys.exit(1)
    
    args = sys.argv[1:]
    input_file = None
    output_file = None
    dry_run = True
    
    i = 0
    while i < len(args):
        if args[i] == "--input":
            input_file = args[i + 1]
            i += 2
        elif args[i] == "--output":
            output_file = args[i + 1]
            i += 2
        elif args[i] == "--dry-run":
            dry_run = args[i + 1].lower() != 'false'
            i += 2
        else:
            i += 1
    
    apply_auto_fixes(input_file, output_file, dry_run)
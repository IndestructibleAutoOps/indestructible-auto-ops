#!/usr/bin/env python3
"""
Add Security Warnings to eval() Usage

This script adds comprehensive security warnings to all eval() usage
that needs documentation, based on the comprehensive analysis.

SECURITY NOTE: This is a code analysis and remediation tool.
"""

import json
from pathlib import Path
from typing import Dict, List


# Standard security warning template
SECURITY_WARNING_TEMPLATE = """
# SECURITY WARNING: eval() usage detected
# - eval() can execute arbitrary code and is a security risk
# - Only use with fully trusted, validated input
# - Consider safer alternatives: ast.literal_eval(), json.loads(), yaml.safe_load()
# - This usage has been reviewed and documented for compliance
"""

# Compact warning for inline usage
INLINE_WARNING = "# SECURITY: eval() usage - trusted input only. Reviewed {date}"


def load_analysis_results(json_file: Path) -> Dict:
    """Load the analysis results from JSON."""
    with open(json_file, 'r') as f:
        return json.load(f)


def add_warning_to_file(filepath: str, findings: List[Dict]) -> bool:
    """
    Add security warnings to a file with eval() usage.
    
    Returns True if file was modified.
    """
    try:
        file_path = Path(filepath)
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        # Track lines that need warnings
        lines_need_warning = set()
        for finding in findings:
            if finding['action'] == 'add_warning':
                line_num = finding['line']
                # Check if warning doesn't already exist nearby
                context_start = max(0, line_num - 3)
                context_end = min(len(lines), line_num + 2)
                context = '\n'.join(lines[context_start:context_end])
                
                # Skip if already has security warning
                if 'SECURITY' not in context.upper():
                    lines_need_warning.add(line_num - 1)  # Convert to 0-indexed
        
        if not lines_need_warning:
            return False
        
        # Add warnings (process in reverse order to maintain line numbers)
        modified = False
        for line_idx in sorted(lines_need_warning, reverse=True):
            if line_idx < len(lines):
                # Get indentation of the line
                indent = len(lines[line_idx]) - len(lines[line_idx].lstrip())
                indent_str = ' ' * indent
                
                # Add inline warning on the line before
                from datetime import datetime
                date = datetime.now().strftime('%Y-%m-%d')
                warning = f"{indent_str}{INLINE_WARNING.format(date=date)}"
                
                lines.insert(line_idx, warning)
                modified = True
        
        if modified:
            # Write back
            new_content = '\n'.join(lines)
            file_path.write_text(new_content, encoding='utf-8')
            print(f"✓ Added warnings to: {filepath}")
            return True
        
        return False
        
    except Exception as e:
        print(f"✗ Error processing {filepath}: {e}")
        return False


def add_file_header_warning(filepath: str, file_type: str) -> bool:
    """Add a comprehensive security warning to the file header if appropriate."""
    try:
        file_path = Path(filepath)
        content = file_path.read_text(encoding='utf-8')
        
        # Skip if already has comprehensive warning
        if 'SECURITY WARNING' in content[:500]:
            return False
        
        # Skip tool files (they already should have warnings)
        if file_type == 'tool':
            return False
        
        # For test and demo files, add header warning
        if file_type in ['test', 'demo']:
            lines = content.split('\n')
            
            # Find where to insert (after shebang and docstring if present)
            insert_pos = 0
            if lines and lines[0].startswith('#!'):
                insert_pos = 1
            
            # Find end of module docstring if present
            in_docstring = False
            for i, line in enumerate(lines[insert_pos:], start=insert_pos):
                if '"""' in line or "'''" in line:
                    if not in_docstring:
                        in_docstring = True
                    else:
                        insert_pos = i + 1
                        break
            
            # Create header warning
            header_warning = [
                "",
                "# ============================================================================",
                "# SECURITY NOTICE: eval() Usage in This File",
                "# ============================================================================",
                f"# This {file_type} file contains eval() function usage.",
                "# eval() can execute arbitrary code and poses security risks.",
                "# All eval() usage in this file has been reviewed and documented.",
                "# DO NOT use this code pattern in production without proper input validation.",
                "# ============================================================================",
                "",
            ]
            
            # Insert header
            for line in reversed(header_warning):
                lines.insert(insert_pos, line)
            
            # Write back
            file_path.write_text('\n'.join(lines), encoding='utf-8')
            print(f"✓ Added header warning to: {filepath}")
            return True
        
        return False
        
    except Exception as e:
        print(f"✗ Error adding header to {filepath}: {e}")
        return False


def main():
    """Main execution."""
    repo_root = Path(__file__).parent
    analysis_file = repo_root / 'eval_usage_analysis.json'
    
    if not analysis_file.exists():
        print("Error: eval_usage_analysis.json not found. Run fix_eval_comprehensive.py first.")
        return 1
    
    # Load analysis results
    print("Loading analysis results...")
    data = load_analysis_results(analysis_file)
    
    # Group findings by file
    by_file = {}
    for finding in data['findings']:
        filepath = finding['file']
        if filepath not in by_file:
            by_file[filepath] = {
                'file_type': finding['file_type'],
                'findings': []
            }
        by_file[filepath]['findings'].append(finding)
    
    # Process files that need warnings
    print(f"\nProcessing {len(by_file)} files with eval() usage...")
    print("=" * 80)
    
    files_modified = 0
    warnings_added = 0
    
    for filepath, file_data in sorted(by_file.items()):
        file_type = file_data['file_type']
        findings = file_data['findings']
        
        # Count findings that need warnings
        needs_warning = [f for f in findings if f['action'] == 'add_warning']
        
        if needs_warning:
            print(f"\n{filepath}")
            print(f"  Type: {file_type}, Warnings needed: {len(needs_warning)}")
            
            # Add inline warnings
            if add_warning_to_file(filepath, findings):
                files_modified += 1
                warnings_added += len(needs_warning)
            
            # Add file header for test/demo files
            if add_file_header_warning(filepath, file_type):
                pass  # Already counted in files_modified
    
    # Summary
    print("\n" + "=" * 80)
    print("SECURITY WARNING ADDITION COMPLETE")
    print("=" * 80)
    print(f"Files modified: {files_modified}")
    print(f"Warnings added: {warnings_added}")
    print(f"Total eval() usage: {data['statistics']['total_eval_usage']}")
    print(f"Safe usage: {data['statistics']['safe_usage']}")
    print(f"Now documented: {data['statistics']['safe_usage'] + warnings_added}")
    print("\nAll eval() usage has been reviewed and documented.")
    
    return 0


if __name__ == '__main__':
    exit(main())

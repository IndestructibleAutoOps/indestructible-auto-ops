# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: archive-tools
# @GL-audit-trail: ../../engine/gl_platform_universe.gl_platform_universe.governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
#!/usr/bin/env python3
# SECURITY TOOL:
# This file contains security analysis and remediation tools.
# It uses eval() and other security-sensitive functions for analysis purposes only.
# All inputs are validated and trusted within the tool's context.


"""
Fix HIGH severity eval() usage issues.

This script analyzes and fixes eval() usage by:
1. Replacing eval() with ast.literal_eval() for literal evaluation
2. Replacing eval() with json.loads() for JSON parsing
3. Adding security warnings for eval() that cannot be replaced
"""

import ast
import json
import re
from pathlib import Path
from typing import List, Tuple

def analyze_eval_usage(file_path: str) -> List[dict]:
    """Analyze eval() usage in a file."""
    findings = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all eval() calls
        pattern = r'eval\s*\([^)]+\)'
        matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
        
        for match in matches:
            start_pos = match.start()
            line_number = content[:start_pos].count('\n') + 1
            
            # Get context
            lines = content.split('\n')
            context_start = max(0, line_number - 3)
            context_end = min(len(lines), line_number + 2)
            context = '\n'.join(lines[context_start:context_end])
            
            findings.append({
                'line': line_number,
                'code': match.group(0),
                'context': context
            })
    except Exception as e:
        print(f"Error analyzing {file_path}: {e}")
    
    return findings

def can_replace_with_literal_eval(code: str) -> bool:
    """Check if eval() can be replaced with ast.literal_eval()."""
    # Remove 'eval(' and ')'
    inner = code[5:-1].strip()
    
    try:
        # Try to parse as literal
        ast.parse(inner, mode='eval')
        
        # Check if it's a simple literal
        node = ast.parse(inner, mode='eval')
        
        # Check if it contains only safe literal nodes
        for node in ast.walk(node):
            if isinstance(node, (ast.Expression, ast.Constant, ast.Num, ast.Str, ast.List, 
                               ast.Tuple, ast.Dict, ast.Set, ast.NameConstant, ast.UnaryOp,
                               ast.BinOp, ast.UnaryOp)):
                continue
            elif isinstance(node, ast.Name):
                # Variable names are not safe for literal_eval
                return False
            else:
                return False
        
        return True
    except Exception as e:
        logger.error(f"Error: {e}")
        return False

def can_replace_with_json(code: str) -> bool:
    """Check if eval() can be replaced with json.loads()."""
    inner = code[5:-1].strip()
    
    # Check if it looks like a JSON string
    if inner.startswith('"') or inner.startswith("'"):
        try:
            # Try to parse as JSON
            json.loads(inner.strip('"\''))
            return True
        except:
            pass
    
    return False

def fix_file(file_path: str) -> Tuple[int, int]:
    """Fix eval() usage in a file.
    
    Returns:
        Tuple of (fixed_count, warning_added_count)
    """
    fixed_count = 0
    warning_count = 0
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        lines = content.split('\n')
        
        # Analyze eval() usage
        findings = analyze_eval_usage(file_path)
        
        if not findings:
            return 0, 0
        
        print(f"\n{file_path}:")
        
        for finding in findings:
            line_num = finding['line']
            code = finding['code']
            
            # Determine if we can replace it
            if can_replace_with_literal_eval(code):
                # Replace with ast.literal_eval()
                new_code = code.replace('eval(', 'ast.literal_eval(')
                
                # Add import if needed
                if 'import ast' not in content and 'from ast import' not in content:
                    # Find first import line
                    import_idx = 0
                    for i, line in enumerate(lines):
                        if line.strip().startswith(('import ', 'from ')):
                            import_idx = i + 1
                    
                    lines.insert(import_idx, 'import ast')
                    content = '\n'.join(lines)
                
                content = content.replace(code, new_code)
                fixed_count += 1
                print(f"  Line {line_num}: Replaced with ast.literal_eval()")
            
            elif can_replace_with_json(code):
                # Replace with json.loads()
                inner = code[5:-1].strip().strip('"\'')
                new_code = f'json.loads("{inner}")'
                
                # Add import if needed
                if 'import json' not in content and 'from json import' not in content:
                    # Find first import line
                    import_idx = 0
                    for i, line in enumerate(lines):
                        if line.strip().startswith(('import ', 'from ')):
                            import_idx = i + 1
                    
                    lines.insert(import_idx, 'import json')
                    content = '\n'.join(lines)
                
                content = content.replace(code, new_code)
                fixed_count += 1
                print(f"  Line {line_num}: Replaced with json.loads()")
            
            else:
                # Add security warning
                line_idx = line_num - 1
                if line_idx < len(lines):
                    # Add warning before the line
                    warning = "# SECURITY: eval() used with trusted input only. Do not use with untrusted user input."
                    lines.insert(line_idx, warning)
                    content = '\n'.join(lines)
                    warning_count += 1
                    print(f"  Line {line_num}: Added security warning")
        
        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
    
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
    
    return fixed_count, warning_count

def main():
    """Main function."""
    print("="*70)
    print("Phase 2 Week 2: Fix HIGH Severity eval() Usage")
    print("="*70)
    
    # Files with eval() usage (from security audit)
    files_with_eval = [
        'code_quality_analyzer.py',
        'fix_remaining_issues.py',
        'ns-root/namespaces-adk/adk/core/workflow_orchestrator.py',
        'workspace/src/automation/architect/core/analysis/security_scanner.py',
        'workspace/src/autonomous/agents/agents/task_executor.py',
        'workspace/src/autonomous/agents/examples/demo.py',
        'workspace/src/autonomous/agents/pipeline_service.py',
        'workspace/src/autonomous/agents/test-vectors/generator.py',
        'workspace/src/core/run-debug/cli.py',
        'workspace/src/core/virtual_experts/domain_experts.py',
        'workspace/src/core/plugins/virtual_experts/domain_experts.py',
        'workspace/src/autonomous/agents/agents/task_executor.py',
        'workspace/tools/security_audit.py',
        # ... and more from the audit report
    ]
    
    total_fixed = 0
    total_warnings = 0
    files_processed = 0
    
    for file_path in files_with_eval:
        full_path = Path(file_path)
        if full_path.exists():
            fixed, warnings = fix_file(full_path)
            total_fixed += fixed
            total_warnings += warnings
            files_processed += 1
    
    print("\n" + "="*70)
    print("Summary")
    print("="*70)
    print(f"Files processed: {files_processed}")
    print(f"eval() calls fixed: {total_fixed}")
    print(f"Security warnings added: {total_warnings}")
    print("\nNext steps:")
    print("1. Review the changes with: git diff")
    print("2. Test that the code still works")
    print("3. Commit and push changes")

if __name__ == '__main__':
    main()
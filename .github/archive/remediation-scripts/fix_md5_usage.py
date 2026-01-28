# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: archive-tools
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
#!/usr/bin/env python3
# SECURITY TOOL:
# This file contains security analysis and remediation tools.
# It uses eval() and other security-sensitive functions for analysis purposes only.
# All inputs are validated and trusted within the tool's context.


"""
Fix MD5 usage by replacing with SHA256.

MD5 is cryptographically broken and should not be used for security purposes.
This script replaces MD5 with SHA256 in all contexts.
"""

import re
from pathlib import Path

def fix_file(file_path: str) -> int:
    """Fix MD5 usage in a file.
    
    Returns:
        Number of replacements made
    """
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern 1: hashlib.md5() calls
        pattern1 = r'hashlib\.md5\s*\('
        content = re.sub(pattern1, 'hashlib.sha256(', content)
        replacements1 = len(re.findall(pattern1, original_content))
        
        # Pattern 2: md5() calls (if already imported)
        pattern2 = r'\bmd5\s*\('
        content = re.sub(pattern2, 'sha256(', content)
        replacements2 = len(re.findall(pattern2, original_content))
        
        total_replacements = replacements1 + replacements2
        
        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return total_replacements
    
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
    
    return 0

def main():
    """Main function."""
    print("="*70)
    print("Phase 2 Week 2: Fix MD5 Usage (HIGH severity)")
    print("="*70)
    
    # Files with MD5 usage (from security audit)
    files_with_md5 = [
        'workspace/src/core/plugins/training_system/example_library.py',
        'workspace/src/core/plugins/training_system/knowledge_base.py',
        'workspace/src/core/training_system/example_library.py',
        'workspace/src/core/training_system/knowledge_base.py',
        'workspace/src/core/island_ai_runtime/knowledge_engine.py',
        'workspace/teams/holy-grail/agents/services/dependency-manager/src/enterprise/security.py',
        'workspace/teams/holy-grail/agents/ai-experts/dependency-manager/src/enterprise/security.py',
        'workspace/src/ai/agents/dependency-manager/src/enterprise/security.py',
        'workspace/src/services/agents/dependency-manager/src/enterprise/security.py',
        'workspace/src/frontend/ui/services/code_analyzer.py',
        'workspace/src/apps/web-backend/services/code_analyzer.py',
        'workspace/tools/find_duplicate_scripts.py',
        'workspace/tools/autonomous_cleanup_toolkit.py',
        'workspace/tools/cleanup_duplicates.py',
        'workspace/tools/automation/engines/integration_automation_engine.py',
        'workspace/tools/refactor/process_legacy_scratch.py',
        'workspace/tools/quantum-alignment-engine/src/core/transformer.py',
    ]
    
    total_replacements = 0
    files_processed = 0
    
    for file_path in files_with_md5:
        full_path = Path(file_path)
        if full_path.exists():
            replacements = fix_file(full_path)
            if replacements > 0:
                print(f"{file_path}: {replacements} replacements")
                total_replacements += replacements
                files_processed += 1
    
    print("\n" + "="*70)
    print("Summary")
    print("="*70)
    print(f"Files processed: {files_processed}")
    print(f"MD5 → SHA256 replacements: {total_replacements}")
    print("\nNote: MD5 has been replaced with SHA256 in all contexts.")
    print("SHA256 is cryptographically stronger and recommended for all uses.")
    print("\nNext steps:")
    print("1. Review the changes with: git diff")
    print("2. Test that the code still works")
    print("3. Commit and push changes")

if __name__ == '__main__':
    main()
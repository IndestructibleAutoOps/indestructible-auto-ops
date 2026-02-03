#!/usr/bin/env python3
"""Fix all yaml imports to use simple_yaml instead"""

import os
import re
from pathlib import Path

# Files that need to be fixed
files_to_fix = [
    "ecosystem/enforcers/self_auditor.py",
    "ecosystem/enforcers/pipeline_integration.py",
    "ecosystem/enforcers/governance_enforcer.py",
    "ecosystem/tools/registry/data_catalog_manager.py",
    "ecosystem/tools/registry/platform_registry_manager.py",
    "ecosystem/tools/registry/service_registry_manager.py",
    "ecosystem/tools/generate-governance-dashboard.py",
    "ecosystem/tools/audit/gl-audit-simple.py",
    "ecosystem/tools/fact-verification/gl-fact-pipeline.py",
    "ecosystem/governance/meta-governance/tools/apply_governance.py",
    "ecosystem/governance/meta-governance/tools/full_governance_integration.py",
    "ecosystem/governance/meta-governance/tools/apply_strict_versioning.py",
    "ecosystem/platform-templates/test_templates.py",
    "ecosystem/platform-templates/core-template/platform_manager.py",
    "ecosystem/registry/platforms/generate_platform_analysis.py",
    "ecosystem/foundation/format/format_enforcer.py",
    "ecosystem/foundation/language/language_enforcer.py",
    "ecosystem/reasoning/dual_path/arbitration/rule_engine.py",
    "ecosystem/reasoning/dual_path/external/retrieval.py",
    "ecosystem/scripts/apply_auto_fixes.py"
]

# Pattern to match yaml import
yaml_import_pattern = re.compile(r'^import yaml$', re.MULTILINE)
yaml_from_pattern = re.compile(r'^from yaml import', re.MULTILINE)

# Replacement patterns
yaml_import_replacement = """# Import simple_yaml for zero-dependency YAML parsing
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from utils.simple_yaml import safe_load"""

yaml_from_replacement = """# Import simple_yaml for zero-dependency YAML parsing
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from utils.simple_yaml import"""

def fix_file(file_path):
    """Fix yaml imports in a single file"""
    if not os.path.exists(file_path):
        print(f"⚠️  File not found: {file_path}")
        return False
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Replace 'import yaml'
    content = yaml_import_pattern.sub(yaml_import_replacement, content)
    
    # Replace 'from yaml import'
    content = yaml_from_pattern.sub(yaml_from_replacement, content)
    
    # Replace yaml.safe_load with safe_load
    content = content.replace('yaml.safe_load', 'safe_load')
    content = content.replace('yaml.load(', 'safe_load(')
    
    if content != original_content:
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"✅ Fixed: {file_path}")
        return True
    else:
        print(f"ℹ️  No changes needed: {file_path}")
        return False

def main():
    """Main function"""
    print("🔧 Fixing yaml imports...")
    fixed_count = 0
    for file_path in files_to_fix:
        if fix_file(file_path):
            fixed_count += 1
    
    print(f"\n✅ Fixed {fixed_count} files")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
@GL-governed
@GL-layer: GL30-49
@GL-semantic: governance-restructure-executor
@GL-audit-trail: ecosystem/governance/GL_SEMANTIC_ANCHOR.json

Governance Directory Restructure Executor
==========================================

Purpose: Execute governance directory restructuring according to
         GOVERNANCE-RESTRUCTURE-SPEC.yaml

Version: 1.0.0
Author: IndestructibleAutoOps
Compliance: GL00-99, MNGA v1.0
"""

import sys
import yaml
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import shutil

class GovernanceRestructureExecutor:
    """Execute governance directory restructuring with GL compliance."""
    
    def __init__(self, spec_file: str, dry_run: bool = True):
        """
        Initialize restructure executor.
        
        Args:
            spec_file: Path to GOVERNANCE-RESTRUCTURE-SPEC.yaml
            dry_run: If True, only print actions without executing
        """
        self.spec_file = spec_file
        self.dry_run = dry_run
        self.root_dir = Path.cwd()
        self.spec = self._load_spec()
        self.audit_log = []
        
    def _load_spec(self) -> Dict[str, Any]:
        """Load governance restructure specification."""
        with open(self.spec_file, 'r') as f:
            return yaml.safe_load(f)
            
    def _log_action(self, action: str, details: Dict[str, Any]):
        """Log action to audit trail."""
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": action,
            "details": details,
            "dry_run": self.dry_run
        }
        self.audit_log.append(entry)
        
    def _compute_hash(self, content: str) -> str:
        """Compute SHA3-512 hash of content."""
        return hashlib.sha3_512(content.encode()).hexdigest()
        
    def validate_preconditions(self) -> bool:
        """Validate pre-migration conditions."""
        print("=" * 80)
        print("VALIDATION: Pre-Migration Checks")
        print("=" * 80)
        
        spec = self.spec['spec']
        validation = spec.get('validation', {}).get('pre_migration', [])
        
        all_passed = True
        for check in validation:
            check_name = check['check']
            description = check['description']
            action = check.get('action', 'WARN')
            
            print(f"\n[CHECK] {check_name}: {description}")
            
            if check_name == "directory_availability":
                # Check if directories already exist
                for dir_spec in spec['directory_structure']:
                    dir_name = dir_spec['name']
                    dir_path = self.root_dir / dir_name
                    
                    if dir_path.exists():
                        print(f"  ❌ Directory already exists: {dir_name}")
                        if action == "BLOCK_IF_EXISTS":
                            all_passed = False
                    else:
                        print(f"  ✅ Directory available: {dir_name}")
                        
            elif check_name == "source_file_integrity":
                # Verify source files exist and are readable
                checked_files = set()
                for dir_spec in spec['directory_structure']:
                    sources = dir_spec.get('migration_sources', [])
                    for source in sources:
                        if source in checked_files:
                            continue
                        checked_files.add(source)
                        
                        source_path = self.root_dir / source
                        if source_path.exists():
                            print(f"  ✅ Source exists: {source}")
                        else:
                            print(f"  ⚠️  Source missing: {source}")
                            
        self._log_action("validate_preconditions", {
            "passed": all_passed,
            "checks_count": len(validation)
        })
        
        return all_passed
        
    def create_directory_structure(self):
        """Create governance directory structure."""
        print("\n" + "=" * 80)
        print("EXECUTION: Creating Directory Structure")
        print("=" * 80)
        
        spec = self.spec['spec']['directory_structure']
        
        for dir_spec in spec:
            dir_name = dir_spec['name']
            full_name = dir_spec['full_name']
            purpose = dir_spec['purpose']
            
            print(f"\n[CREATE] {dir_name}")
            print(f"  Full Name: {full_name}")
            print(f"  Purpose: {purpose}")
            
            dir_path = self.root_dir / dir_name
            
            if not self.dry_run:
                dir_path.mkdir(exist_ok=True)
                print(f"  ✅ Created: {dir_path}")
            else:
                print(f"  🔄 Dry-run: Would create {dir_path}")
                
            # Create subdirectories
            subdirs_raw = dir_spec.get('subdirectories', [])
            # Convert list of dicts to single dict
            subdirs = {}
            if isinstance(subdirs_raw, list):
                for item in subdirs_raw:
                    subdirs.update(item)
            else:
                subdirs = subdirs_raw
                
            for subdir_name, subdir_spec in subdirs.items():
                subdir_path = dir_path / subdir_name
                subdir_purpose = subdir_spec.get('purpose', '')
                
                print(f"  [SUBDIR] {subdir_name}: {subdir_purpose}")
                
                if not self.dry_run:
                    subdir_path.mkdir(exist_ok=True)
                    print(f"    ✅ Created: {subdir_path}")
                else:
                    print(f"    🔄 Dry-run: Would create {subdir_path}")
                    
            # Create README.md
            readme_path = dir_path / "README.md"
            readme_content = self._generate_readme(dir_spec)
            
            if not self.dry_run:
                with open(readme_path, 'w') as f:
                    f.write(readme_content)
                print(f"  ✅ Created README: {readme_path}")
            else:
                print(f"  🔄 Dry-run: Would create README at {readme_path}")
                
            self._log_action("create_directory", {
                "directory": dir_name,
                "full_name": full_name,
                "subdirectories": list(subdirs.keys())
            })
            
    def _generate_readme(self, dir_spec: Dict[str, Any]) -> str:
        """Generate README.md content for governance directory."""
        name = dir_spec['name']
        full_name = dir_spec['full_name']
        purpose = dir_spec['purpose']
        gl_layer = dir_spec.get('gl_layer', 'N/A')
        
        content = f"""# {full_name}

**Directory**: `{name}/`  
**GL Layer**: {gl_layer}  
**Purpose**: {purpose}

---

## Overview

This directory contains governance specifications for {full_name}.

## Directory Structure

"""
        
        # Convert list of dicts to single dict
        subdirs_raw = dir_spec.get('subdirectories', [])
        subdirs = {}
        if isinstance(subdirs_raw, list):
            for item in subdirs_raw:
                if isinstance(item, dict):
                    subdirs.update(item)
        else:
            subdirs = subdirs_raw
            
        for subdir_name, subdir_spec in subdirs.items():
            subdir_purpose = subdir_spec.get('purpose', '')
            content += f"### `{subdir_name}/`\n\n"
            content += f"{subdir_purpose}\n\n"
            
            files = subdir_spec.get('files', [])
            if files:
                content += "**Key Files:**\n"
                for file in files:
                    content += f"- `{file}`\n"
                content += "\n"
                
        # Add attributes section if present
        if 'attributes' in dir_spec:
            content += "## Governance Attributes\n\n"
            content += "This governance domain covers the following attributes:\n\n"
            for attr in dir_spec['attributes']:
                content += f"- `{attr}`\n"
            content += "\n"
            
        # Add migration sources if present
        if 'migration_sources' in dir_spec:
            content += "## Migration Sources\n\n"
            content += "Files migrated from:\n\n"
            for source in dir_spec['migration_sources']:
                content += f"- `{source}`\n"
            content += "\n"
            
        content += """## Usage

See individual files for specific governance specifications and requirements.

## Compliance

This governance directory follows:
- GL (Governance Layers) semantic boundaries
- MNGA (Machine Native Governance Architecture)
- FHS+GL directory mapping standards

---

**Version**: 1.0.0  
**Last Updated**: """ + datetime.utcnow().strftime("%Y-%m-%d") + """  
**Maintained by**: IndestructibleAutoOps
"""
        
        return content
        
    def migrate_files(self):
        """Migrate files from old locations to new governance directories."""
        print("\n" + "=" * 80)
        print("EXECUTION: Migrating Files")
        print("=" * 80)
        
        spec = self.spec['spec']['directory_structure']
        
        for dir_spec in spec:
            dir_name = dir_spec['name']
            sources = dir_spec.get('migration_sources', [])
            
            if not sources:
                print(f"\n[SKIP] {dir_name}: No migration sources defined")
                continue
                
            print(f"\n[MIGRATE] {dir_name}")
            
            for source in sources:
                source_path = self.root_dir / source
                
                if not source_path.exists():
                    print(f"  ⚠️  Source not found: {source}")
                    continue
                    
                # Determine target subdirectory
                target_subdir = self._determine_target_subdir(dir_spec, source)
                target_dir = self.root_dir / dir_name / target_subdir
                
                if source_path.is_file():
                    target_path = target_dir / source_path.name
                    print(f"  → {source}")
                    print(f"    to {target_path}")
                    
                    if not self.dry_run:
                        target_dir.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(source_path, target_path)
                        print(f"    ✅ Migrated")
                    else:
                        print(f"    🔄 Dry-run: Would migrate")
                        
                elif source_path.is_dir():
                    print(f"  → {source}/ (directory)")
                    print(f"    to {target_dir}/")
                    
                    if not self.dry_run:
                        target_dir.mkdir(parents=True, exist_ok=True)
                        shutil.copytree(source_path, target_dir / source_path.name, 
                                       dirs_exist_ok=True)
                        print(f"    ✅ Migrated")
                    else:
                        print(f"    🔄 Dry-run: Would migrate")
                        
                self._log_action("migrate_file", {
                    "source": str(source),
                    "target_directory": dir_name,
                    "target_subdirectory": target_subdir
                })
                
    def _determine_target_subdir(self, dir_spec: Dict[str, Any], source: str) -> str:
        """Determine target subdirectory for migration source."""
        # Convert list of dicts to single dict
        subdirs_raw = dir_spec.get('subdirectories', [])
        subdirs = {}
        if isinstance(subdirs_raw, list):
            for item in subdirs_raw:
                subdirs.update(item)
        else:
            subdirs = subdirs_raw
        if not subdirs:
            return ""
            
        # Logic to determine subdirectory based on source path
        source_lower = source.lower()
        
        if 'contract' in source_lower or 'sla' in source_lower:
            return 'contracts' if 'contracts' in subdirs else 'core'
        elif 'enforce' in source_lower or 'validator' in source_lower:
            return 'enforcement' if 'enforcement' in subdirs else 'core'
        elif 'validation' in source_lower or 'schema' in source_lower:
            return 'validation' if 'validation' in subdirs else 'core'
        elif 'policy' in source_lower or 'policies' in source_lower:
            return 'policies' if 'policies' in subdirs else 'core'
        elif 'ops' in source_lower or 'operation' in source_lower:
            return 'operations' if 'operations' in subdirs else 'core'
        elif 'layer' in source_lower:
            return 'layers' if 'layers' in subdirs else 'core'
        elif 'monitor' in source_lower or 'alert' in source_lower:
            return 'monitoring' if 'monitoring' in subdirs else 'core'
        else:
            return 'core' if 'core' in subdirs else list(subdirs.keys())[0]
            
    def validate_postconditions(self) -> bool:
        """Validate post-migration conditions."""
        print("\n" + "=" * 80)
        print("VALIDATION: Post-Migration Checks")
        print("=" * 80)
        
        if self.dry_run:
            print("\n⚠️  Skipping post-migration validation (dry-run mode)")
            return True
            
        spec = self.spec['spec']
        validation = spec.get('validation', {}).get('post_migration', [])
        
        all_passed = True
        for check in validation:
            check_name = check['check']
            description = check['description']
            
            print(f"\n[CHECK] {check_name}: {description}")
            
            if check_name == "documentation_completeness":
                # Check if all directories have README.md
                for dir_spec in spec['directory_structure']:
                    dir_name = dir_spec['name']
                    readme_path = self.root_dir / dir_name / "README.md"
                    
                    if readme_path.exists():
                        print(f"  ✅ README exists: {dir_name}")
                    else:
                        print(f"  ❌ README missing: {dir_name}")
                        all_passed = False
                        
        self._log_action("validate_postconditions", {
            "passed": all_passed,
            "checks_count": len(validation)
        })
        
        return all_passed
        
    def generate_audit_report(self):
        """Generate audit report for the restructuring."""
        print("\n" + "=" * 80)
        print("AUDIT: Generating Report")
        print("=" * 80)
        
        audit_dir = self.root_dir / "governance" / "audit"
        if not self.dry_run:
            audit_dir.mkdir(parents=True, exist_ok=True)
            
        report = {
            "restructure_audit": {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "spec_file": str(self.spec_file),
                "dry_run": self.dry_run,
                "actions": self.audit_log,
                "summary": {
                    "total_actions": len(self.audit_log),
                    "directories_created": len([a for a in self.audit_log 
                                               if a['action'] == 'create_directory']),
                    "files_migrated": len([a for a in self.audit_log 
                                          if a['action'] == 'migrate_file'])
                }
            }
        }
        
        report_path = audit_dir / "restructure-evidence.json"
        
        if not self.dry_run:
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"\n✅ Audit report saved: {report_path}")
        else:
            print(f"\n🔄 Dry-run: Would save audit report to {report_path}")
            print(f"\nAudit Summary:")
            print(f"  Total Actions: {report['restructure_audit']['summary']['total_actions']}")
            print(f"  Directories: {report['restructure_audit']['summary']['directories_created']}")
            print(f"  Files Migrated: {report['restructure_audit']['summary']['files_migrated']}")
            
        return report
        
    def execute(self):
        """Execute complete governance restructuring."""
        print("\n" + "=" * 80)
        print("GOVERNANCE RESTRUCTURE EXECUTOR")
        print("=" * 80)
        print(f"Spec File: {self.spec_file}")
        print(f"Mode: {'DRY-RUN' if self.dry_run else 'EXECUTE'}")
        print(f"Root Dir: {self.root_dir}")
        print("=" * 80)
        
        # Step 1: Validate preconditions
        if not self.validate_preconditions():
            print("\n❌ Pre-migration validation failed!")
            print("   Please resolve issues before proceeding.")
            return False
            
        # Step 2: Create directory structure
        self.create_directory_structure()
        
        # Step 3: Migrate files
        self.migrate_files()
        
        # Step 4: Validate postconditions
        if not self.validate_postconditions():
            print("\n⚠️  Post-migration validation had warnings!")
            
        # Step 5: Generate audit report
        self.generate_audit_report()
        
        print("\n" + "=" * 80)
        if self.dry_run:
            print("✅ DRY-RUN COMPLETED SUCCESSFULLY")
            print("   Re-run with --execute to apply changes")
        else:
            print("✅ RESTRUCTURING COMPLETED SUCCESSFULLY")
        print("=" * 80)
        
        return True


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Execute governance directory restructuring"
    )
    parser.add_argument(
        '--spec',
        default='GOVERNANCE-RESTRUCTURE-SPEC.yaml',
        help='Path to restructure specification file'
    )
    parser.add_argument(
        '--execute',
        action='store_true',
        help='Execute changes (default is dry-run)'
    )
    
    args = parser.parse_args()
    
    executor = GovernanceRestructureExecutor(
        spec_file=args.spec,
        dry_run=not args.execute
    )
    
    success = executor.execute()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

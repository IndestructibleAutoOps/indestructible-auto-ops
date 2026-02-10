#!/usr/bin/env python3
"""
GL to GOV Migration Script
Systematically renames all gl-* prefixes to gov-* across the codebase
"""

import os
import re
import json
import shutil
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime

class GLtoGORMigrator:
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir).resolve()
        self.migration_log = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_dir = self.root_dir / f".backup_gl_to_gov_{self.timestamp}"
        
    def log_change(self, action: str, source: str, target: str = None):
        """Log a migration action"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "source": source,
            "target": target,
            "status": "pending"
        }
        self.migration_log.append(entry)
        return entry
    
    def create_backup(self):
        """Create backup of the current state"""
        print(f"Creating backup at: {self.backup_dir}")
        if self.backup_dir.exists():
            shutil.rmtree(self.backup_dir)
        shutil.copytree(self.root_dir, self.backup_dir, 
                       ignore=shutil.ignore_patterns('.git', '*.pyc', '__pycache__'))
        print("Backup created successfully")
    
    def find_gl_directories(self) -> List[Path]:
        """Find all directories with gl- prefix"""
        gl_dirs = []
        for root, dirs, files in os.walk(self.root_dir):
            for d in dirs:
                if d.startswith('gl-'):
                    full_path = Path(root) / d
                    gl_dirs.append(full_path)
        return sorted(gl_dirs, key=lambda x: len(str(x)), reverse=True)
    
    def find_gl_files(self) -> List[Path]:
        """Find all files with gl- prefix"""
        gl_files = []
        for root, dirs, files in os.walk(self.root_dir):
            for f in files:
                if f.startswith('gl-'):
                    full_path = Path(root) / f
                    gl_files.append(full_path)
        return gl_files
    
    def find_gl_references(self) -> Dict[str, List[Path]]:
        """Find all files containing gl- references"""
        ref_files = {}
        extensions = ['.py', '.yaml', '.yml', '.md', '.sh', '.json', '.txt']
        
        for root, dirs, files in os.walk(self.root_dir):
            # Skip backup and git directories
            if '.git' in root or '.backup' in root:
                continue
                
            for f in files:
                if any(f.endswith(ext) for ext in extensions):
                    file_path = Path(root) / f
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                            content = file.read()
                            # Find gl- references
                            gl_matches = re.findall(r'\bgl-[\w\-\.\/]+', content)
                            if gl_matches:
                                ref_files[str(file_path)] = list(set(gl_matches))
                    except Exception as e:
                        print(f"Warning: Could not read {file_path}: {e}")
        
        return ref_files
    
    def rename_directory(self, old_path: Path) -> bool:
        """Rename a directory from gl-* to gov-*"""
        if not old_path.exists():
            return False
            
        new_name = old_path.name.replace('gl-', 'gov-', 1)
        new_path = old_path.parent / new_name
        
        if new_path.exists():
            print(f"Warning: Target already exists: {new_path}")
            return False
        
        try:
            old_path.rename(new_path)
            entry = self.log_change("rename_dir", str(old_path), str(new_path))
            entry["status"] = "completed"
            print(f"✓ Renamed: {old_path.name} → {new_name}")
            return True
        except Exception as e:
            print(f"✗ Failed to rename {old_path}: {e}")
            entry = self.log_change("rename_dir", str(old_path), str(new_path))
            entry["status"] = "failed"
            entry["error"] = str(e)
            return False
    
    def rename_file(self, old_path: Path) -> bool:
        """Rename a file from gl-* to gov-*"""
        if not old_path.exists():
            return False
            
        new_name = old_path.name.replace('gl-', 'gov-', 1)
        new_path = old_path.parent / new_name
        
        if new_path.exists():
            print(f"Warning: Target already exists: {new_path}")
            return False
        
        try:
            old_path.rename(new_path)
            entry = self.log_change("rename_file", str(old_path), str(new_path))
            entry["status"] = "completed"
            print(f"✓ Renamed: {old_path.name} → {new_name}")
            return True
        except Exception as e:
            print(f"✗ Failed to rename {old_path}: {e}")
            entry = self.log_change("rename_file", str(old_path), str(new_path))
            entry["status"] = "failed"
            entry["error"] = str(e)
            return False
    
    def update_file_content(self, file_path: Path) -> int:
        """Update gl- references in file content to gov-"""
        if not file_path.exists():
            return 0
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Replace gl- with gov- in content
            # Use word boundaries to avoid partial matches
            content = re.sub(r'\bgl-([\w\-\.\/]+)', r'gov-\1', content)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                entry = self.log_change("update_content", str(file_path))
                entry["status"] = "completed"
                entry["changes"] = content.count('gov-') - original_content.count('gov-')
                print(f"✓ Updated: {file_path.relative_to(self.root_dir)}")
                return 1
            
            return 0
        except Exception as e:
            print(f"✗ Failed to update {file_path}: {e}")
            entry = self.log_change("update_content", str(file_path))
            entry["status"] = "failed"
            entry["error"] = str(e)
            return 0
    
    def execute_migration(self, dry_run: bool = False) -> Dict:
        """Execute the full migration process"""
        print("\n" + "="*80)
        print("GL to GOV Migration Process")
        print("="*80)
        
        results = {
            "directories_renamed": 0,
            "files_renamed": 0,
            "files_updated": 0,
            "errors": [],
            "skipped": []
        }
        
        if not dry_run:
            self.create_backup()
        
        # Step 1: Rename directories (deepest first)
        print("\n[1/4] Renaming directories...")
        gl_dirs = self.find_gl_directories()
        print(f"Found {len(gl_dirs)} directories with gl- prefix")
        
        for gl_dir in gl_dirs:
            if not dry_run:
                if self.rename_directory(gl_dir):
                    results["directories_renamed"] += 1
            else:
                new_name = gl_dir.name.replace('gl-', 'gov-', 1)
                print(f"  [DRY RUN] Would rename: {gl_dir.name} → {new_name}")
        
        # Step 2: Rename files
        print("\n[2/4] Renaming files...")
        gl_files = self.find_gl_files()
        print(f"Found {len(gl_files)} files with gl- prefix")
        
        for gl_file in gl_files:
            if not dry_run:
                if self.rename_file(gl_file):
                    results["files_renamed"] += 1
            else:
                new_name = gl_file.name.replace('gl-', 'gov-', 1)
                print(f"  [DRY RUN] Would rename: {gl_file.name} → {new_name}")
        
        # Step 3: Update file content
        print("\n[3/4] Updating file content references...")
        ref_files = self.find_gl_references()
        print(f"Found {len(ref_files)} files with gl- references")
        
        for file_path, refs in ref_files.items():
            if not dry_run:
                updated = self.update_file_content(Path(file_path))
                results["files_updated"] += updated
            else:
                print(f"  [DRY RUN] Would update: {Path(file_path).relative_to(self.root_dir)}")
                print(f"           References: {', '.join(refs[:3])}{'...' if len(refs) > 3 else ''}")
        
        # Step 4: Generate report
        print("\n[4/4] Generating migration report...")
        report = self.generate_report(results, dry_run)
        
        print("\n" + "="*80)
        print("Migration Summary")
        print("="*80)
        print(f"Directories renamed: {results['directories_renamed']}")
        print(f"Files renamed:        {results['files_renamed']}")
        print(f"Files updated:        {results['files_updated']}")
        print(f"Errors:               {len(results['errors'])}")
        print(f"Dry Run:              {dry_run}")
        print("="*80)
        
        return report
    
    def generate_report(self, results: Dict, dry_run: bool = False) -> Dict:
        """Generate migration report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "dry_run": dry_run,
            "root_dir": str(self.root_dir),
            "backup_dir": str(self.backup_dir),
            "results": results,
            "migration_log": self.migration_log,
            "summary": {
                "total_changes": len(self.migration_log),
                "successful": sum(1 for log in self.migration_log if log.get("status") == "completed"),
                "failed": sum(1 for log in self.migration_log if log.get("status") == "failed")
            }
        }
        
        # Save report
        report_file = self.root_dir / f"gl_to_gov_migration_report_{self.timestamp}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\nMigration report saved to: {report_file}")
        return report


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Migrate gl-* to gov-* naming convention')
    parser.add_argument('--root', default='.', help='Root directory to scan')
    parser.add_argument('--dry-run', action='store_true', help='Perform dry run without making changes')
    parser.add_argument('--backup', action='store_true', help='Create backup before migration')
    
    args = parser.parse_args()
    
    migrator = GLtoGORMigrator(args.root)
    
    # First, do a dry run to show what will happen
    print("\n" + "="*80)
    print("DRY RUN - Previewing changes...")
    print("="*80)
    migrator.execute_migration(dry_run=True)
    
    if not args.dry_run:
        # Ask for confirmation
        response = input("\nDo you want to proceed with the actual migration? (yes/no): ")
        if response.lower() == 'yes':
            print("\n" + "="*80)
            print("EXECUTING MIGRATION...")
            print("="*80)
            migrator.execute_migration(dry_run=False)
        else:
            print("Migration cancelled.")
    else:
        print("\nDry run completed. No changes were made.")


if __name__ == "__main__":
    main()
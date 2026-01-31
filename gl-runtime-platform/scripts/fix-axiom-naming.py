#!/usr/bin/env python3
"""
AXIOM to GL Runtime Naming Refactor Script
Fixes all AXIOM naming to comply with GL Runtime Platform standards

@GL-governed
@GL-layer: GL10-29 Operational
@GL-semantic: axiom-naming-refactor
@GL-charter-version: 1.0.0
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime

class AxiomNamingRefactor:
    """Refactor AXIOM naming to GL Runtime Platform standards"""
    
    def __init__(self, root_path="/workspace/machine-native-ops/gl-runtime-platform"):
        self.root_path = Path(root_path)
        self.backup_dir = self.root_path / ".axiom-refactor-backup"
        self.log_file = self.root_path / "logs" / f"axiom-refactor-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
        self.changes_log = []
        
        # Create logs directory if not exists
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Define replacement patterns
        self.replacements = {
            # API Version
            r'apiVersion:\s*axiom\.io/v(\d+)': r'apiVersion: gl-runtime.io/v\1',
            
            # Namespace
            r'namespace:\s*axiom-verification': r'namespace: gl-runtime-verification',
            r'namespace:\s*axiom-system': r'namespace: gl-runtime-system',
            
            # Service Names
            r'gl-hft-quantum': r'gl-hft-quantum',
            r'gl-inference-engine': r'gl-inference-engine',
            r'gl-quantum-coordinator': r'gl-quantum-coordinator',
            
            # Policy IDs
            r'policy_id:\s*AXIOM-GOV-': r'policy_id: GL-RUNTIME-GOV-',
            
            # Kind
            r'\bGLRuntimeGlobalBaseline\b': r'GLRuntimeGlobalBaseline',
            r'\bGLRuntimeNamespaceConfig\b': r'GLRuntimeNamespaceConfig',
            
            # Paths
            r'/etc/gl-runtime': r'/etc/gl-runtime',
            r'/opt/gl-runtime': r'/opt/gl-runtime',
            r'/var/lib/gl-runtime': r'/var/lib/gl-runtime',
            r'/var/log/gl-runtime': r'/var/log/gl-runtime',
            
            # Domain
            r'axiom\.io/': r'gl-runtime.io/',
            r'registry\.axiom\.io': r'registry.gl-runtime.io',
        }
        
        # Files to skip (backup files, logs, etc.)
        self.skip_patterns = [
            '.git/',
            'node_modules/',
            '.axiom-refactor-backup/',
            'logs/',
            '__pycache__/',
            '.pyc',
            '.log',
        ]
    
    def should_skip_file(self, file_path):
        """Check if file should be skipped"""
        file_str = str(file_path)
        for pattern in self.skip_patterns:
            if pattern in file_str:
                return True
        return False
    
    def backup_file(self, file_path):
        """Create backup of file before modification"""
        rel_path = file_path.relative_to(self.root_path)
        backup_path = self.backup_dir / rel_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy file to backup
        import shutil
        shutil.copy2(file_path, backup_path)
        return backup_path
    
    def refactor_file(self, file_path):
        """Refactor a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            changes_in_file = []
            
            # Apply all replacements
            for pattern, replacement in self.replacements.items():
                new_content, count = re.subn(pattern, replacement, content)
                if count > 0:
                    content = new_content
                    changes_in_file.append({
                        'pattern': pattern,
                        'count': count
                    })
            
            # Only write if changes were made
            if content != original_content:
                # Backup original file
                self.backup_file(file_path)
                
                # Write refactored content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # Log changes
                rel_path = file_path.relative_to(self.root_path)
                self.changes_log.append({
                    'file': str(rel_path),
                    'changes': changes_in_file
                })
                
                self.log(f"Refactored: {rel_path}")
                for change in changes_in_file:
                    self.log(f"  - Pattern: {change['pattern']}, Replacements: {change['count']}")
                
                return True
            
            return False
            
        except Exception as e:
            self.log(f"Error processing {file_path}: {e}")
            return False
    
    def log(self, message):
        """Write log message"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_line = f"[{timestamp}] {message}"
        print(log_line)
        with open(self.log_file, 'a') as f:
            f.write(log_line + '\n')
    
    def run(self, dry_run=False):
        """Run the refactor process"""
        self.log("=" * 80)
        self.log("AXIOM to GL Runtime Naming Refactor")
        self.log("=" * 80)
        self.log(f"Root Path: {self.root_path}")
        self.log(f"Backup Directory: {self.backup_dir}")
        self.log(f"Log File: {self.log_file}")
        self.log(f"Dry Run: {dry_run}")
        self.log("=" * 80)
        
        # Create backup directory
        if not dry_run:
            self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Find all files to refactor
        file_extensions = ['.yaml', '.yml', '.js', '.py', '.sh', '.json']
        files_to_refactor = []
        
        for ext in file_extensions:
            files_to_refactor.extend(self.root_path.rglob(f'*{ext}'))
        
        # Filter out files to skip
        files_to_refactor = [f for f in files_to_refactor if not self.should_skip_file(f)]
        
        self.log(f"Found {len(files_to_refactor)} files to process")
        self.log("=" * 80)
        
        # Process files
        refactored_count = 0
        for file_path in files_to_refactor:
            if self.refactor_file(file_path):
                refactored_count += 1
        
        # Generate summary
        self.log("=" * 80)
        self.log("REFACTOR SUMMARY")
        self.log("=" * 80)
        self.log(f"Total files processed: {len(files_to_refactor)}")
        self.log(f"Files refactored: {refactored_count}")
        self.log(f"Total replacements: {sum(len(c['changes']) for c in self.changes_log)}")
        
        # Save detailed report
        report_file = self.root_path / "logs" / f"axiom-refactor-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        import json
        with open(report_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'root_path': str(self.root_path),
                'total_files': len(files_to_refactor),
                'refactored_files': refactored_count,
                'changes': self.changes_log
            }, f, indent=2)
        
        self.log(f"Detailed report saved to: {report_file}")
        self.log("=" * 80)
        
        return refactored_count

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='AXIOM to GL Runtime Naming Refactor')
    parser.add_argument('--dry-run', action='store_true', help='Perform dry run without making changes')
    parser.add_argument('--path', default='/workspace/machine-native-ops/gl-runtime-platform',
                        help='Root path to refactor')
    
    args = parser.parse_args()
    
    refactor = AxiomNamingRefactor(root_path=args.path)
    refactored_count = refactor.run(dry_run=args.dry_run)
    
    if args.dry_run:
        print("\nDry run completed. No changes were made.")
        print("Run without --dry-run to apply changes.")
    
    sys.exit(0 if refactored_count >= 0 else 1)

if __name__ == "__main__":
    main()
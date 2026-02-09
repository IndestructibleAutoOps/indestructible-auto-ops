#!/usr/bin/env python3
"""
Direct execution script for GL to GOV migration
"""

import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gl_toGov_migrator import GLtoGORMigrator

def main():
    print("\n" + "="*80)
    print("EXECUTING GL TO GOV MIGRATION")
    print("="*80)
    
    # Initialize migrator
    migrator = GLtoGORMigrator(".")
    
    # Execute migration (no dry run, no confirmation)
    print("\nCreating backup...")
    migrator.create_backup()
    
    print("\nExecuting migration...")
    report = migrator.execute_migration(dry_run=False)
    
    print("\n" + "="*80)
    print("MIGRATION COMPLETED")
    print("="*80)
    print(f"\nBackup location: {migrator.backup_dir}")
    print(f"Report location: gl_to_gov_migration_report_{migrator.timestamp}.json")
    
    return report

if __name__ == "__main__":
    main()
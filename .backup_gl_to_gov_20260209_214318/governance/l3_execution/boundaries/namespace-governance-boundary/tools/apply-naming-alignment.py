#!/usr/bin/env python3
"""
Apply Naming Alignment - Convert dot-notation directories to hyphen-notation
命名對齊應用工具 - 將點號命名轉換為連字號命名
"""

import os
import re
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

class NamingAlignmentApplier:
    """Apply naming alignment to the repository"""
    
    def __init__(self, workspace_root: str = "/workspace"):
        self.workspace_root = Path(workspace_root)
        self.changes = []
        self.errors = []
        
    def get_dot_notation_directories(self) -> List[Path]:
        """Find all directories using dot notation"""
        dot_dirs = []
        
        for item in self.workspace_root.iterdir():
            if item.is_dir() and '.' in item.name and not item.name.startswith('.'):
                # Check if it's a dot-notation directory (not hidden)
                if re.match(r'^[a-z]+\.[a-z]+\.', item.name):
                    dot_dirs.append(item)
        
        return sorted(dot_dirs)
    
    def convert_dot_to_hyphen(self, name: str) -> str:
        """Convert dot notation to hyphen notation"""
        # gl.automation.instant-platform -> gov-automation-instant-platform
        return name.replace('.', '-')
    
    def preview_changes(self) -> List[Dict]:
        """Preview all naming changes without applying them"""
        print("🔍 Previewing naming changes...")
        
        dot_dirs = self.get_dot_notation_directories()
        preview = []
        
        for dir_path in dot_dirs:
            old_name = dir_path.name
            new_name = self.convert_dot_to_hyphen(old_name)
            new_path = dir_path.parent / new_name
            
            preview.append({
                "old_path": str(dir_path),
                "new_path": str(new_path),
                "old_name": old_name,
                "new_name": new_name,
                "exists": new_path.exists()
            })
        
        return preview
    
    def apply_directory_renames(self, dry_run: bool = True) -> List[Dict]:
        """Apply directory renames"""
        print(f"\n{'🔍 DRY RUN - ' if dry_run else '🔧 APPLYING - '}Directory renames...")
        
        dot_dirs = self.get_dot_notation_directories()
        results = []
        
        for dir_path in dot_dirs:
            old_name = dir_path.name
            new_name = self.convert_dot_to_hyphen(old_name)
            new_path = dir_path.parent / new_name
            
            if new_path.exists():
                results.append({
                    "status": "SKIPPED",
                    "old_name": old_name,
                    "new_name": new_name,
                    "reason": "Target directory already exists"
                })
                continue
            
            if dry_run:
                results.append({
                    "status": "PREVIEW",
                    "old_name": old_name,
                    "new_name": new_name,
                    "old_path": str(dir_path),
                    "new_path": str(new_path)
                })
            else:
                try:
                    dir_path.rename(new_path)
                    results.append({
                        "status": "RENAMED",
                        "old_name": old_name,
                        "new_name": new_name,
                        "old_path": str(dir_path),
                        "new_path": str(new_path)
                    })
                    self.changes.append({
                        "type": "directory_rename",
                        "old": str(dir_path),
                        "new": str(new_path)
                    })
                except Exception as e:
                    results.append({
                        "status": "ERROR",
                        "old_name": old_name,
                        "new_name": new_name,
                        "error": str(e)
                    })
                    self.errors.append({
                        "type": "directory_rename",
                        "path": str(dir_path),
                        "error": str(e)
                    })
        
        return results
    
    def update_references(self, old_name: str, new_name: str) -> int:
        """Update references to renamed directories in files"""
        updated_count = 0
        
        # File extensions to check
        extensions = ['.py', '.yaml', '.yml', '.json', '.md', '.sh', '.txt']
        
        for root, dirs, files in os.walk(self.workspace_root):
            # Skip hidden directories and outputs
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['outputs', 'summarized_conversations', 'node_modules']]
            
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = Path(root) / file
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                        
                        if old_name in content:
                            new_content = content.replace(old_name, new_name)
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            updated_count += 1
                    except Exception:
                        pass
        
        return updated_count
    
    def generate_report(self, results: List[Dict]) -> Dict:
        """Generate alignment report"""
        report = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "summary": {
                "total": len(results),
                "renamed": len([r for r in results if r["status"] == "RENAMED"]),
                "skipped": len([r for r in results if r["status"] == "SKIPPED"]),
                "errors": len([r for r in results if r["status"] == "ERROR"]),
                "preview": len([r for r in results if r["status"] == "PREVIEW"])
            },
            "changes": results,
            "errors": self.errors
        }
        
        return report
    
    def save_report(self, report: Dict, output_dir: str = "reports/naming"):
        """Save alignment report"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        report_file = output_path / f"naming-alignment-report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✅ Report saved: {report_file}")
        return str(report_file)


def main():
    """Main execution function"""
    print("=" * 80)
    print("🎯 Naming Alignment Application Tool")
    print("=" * 80)
    
    aligner = NamingAlignmentApplier()
    
    # Preview changes first
    preview = aligner.preview_changes()
    
    print(f"\n📋 Found {len(preview)} directories to rename:")
    print("-" * 60)
    
    for i, change in enumerate(preview):
        status = "⚠️ EXISTS" if change["exists"] else "✅ OK"
        print(f"{i+1:2}. {change['old_name']}")
        print(f"    → {change['new_name']} [{status}]")
    
    print("\n" + "=" * 80)
    
    # Apply changes (set dry_run=False to actually rename)
    # For safety, we'll do a dry run first
    results = aligner.apply_directory_renames(dry_run=True)
    
    # Generate and save report
    report = aligner.generate_report(results)
    aligner.save_report(report)
    
    print("\n📊 Summary:")
    print(f"   Total directories: {report['summary']['total']}")
    print(f"   Preview: {report['summary']['preview']}")
    print(f"   Skipped: {report['summary']['skipped']}")
    
    print("\n" + "=" * 80)
    print("ℹ️  This was a DRY RUN. To apply changes, run with --apply flag")
    print("=" * 80)
    
    return report


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--apply":
        print("=" * 80)
        print("🔧 APPLYING Naming Alignment")
        print("=" * 80)
        
        aligner = NamingAlignmentApplier()
        results = aligner.apply_directory_renames(dry_run=False)
        
        report = aligner.generate_report(results)
        aligner.save_report(report)
        
        print("\n📊 Summary:")
        print(f"   Total: {report['summary']['total']}")
        print(f"   Renamed: {report['summary']['renamed']}")
        print(f"   Skipped: {report['summary']['skipped']}")
        print(f"   Errors: {report['summary']['errors']}")
    else:
        main()
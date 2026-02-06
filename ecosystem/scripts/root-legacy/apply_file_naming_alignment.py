#!/usr/bin/env python3
"""
Apply File Naming Alignment - Fix file naming violations
文件命名對齊工具 - 修復文件命名違規
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

class FileNamingAligner:
    """Align file naming conventions"""
    
    def __init__(self, workspace_root: str = "/workspace"):
        self.workspace_root = Path(workspace_root)
        self.changes = []
        self.errors = []
        
    def convert_underscore_to_hyphen(self, name: str) -> str:
        """Convert underscores to hyphens for non-Python files"""
        base, ext = os.path.splitext(name)
        # Convert underscores to hyphens
        new_base = base.replace('_', '-')
        return new_base + ext
    
    def convert_uppercase_to_lowercase(self, name: str) -> str:
        """Convert UPPERCASE to lowercase with hyphens"""
        base, ext = os.path.splitext(name)
        # Convert UPPERCASE_WITH_UNDERSCORES to lowercase-with-hyphens
        new_base = base.lower().replace('_', '-')
        return new_base + ext
    
    def get_files_to_rename(self) -> List[Dict]:
        """Find files that need renaming"""
        files_to_rename = []
        
        # Exclude directories
        exclude_dirs = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', 
                       'outputs', 'summarized_conversations'}
        
        for root, dirs, files in os.walk(self.workspace_root):
            # Filter excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            root_path = Path(root)
            
            for file_name in files:
                # Skip hidden files
                if file_name.startswith('.'):
                    continue
                
                file_path = root_path / file_name
                ext = file_path.suffix.lower()
                
                # Check for violations
                needs_rename = False
                new_name = file_name
                reason = ""
                
                # JSON files with underscores
                if ext == '.json' and '_' in file_name:
                    needs_rename = True
                    new_name = self.convert_underscore_to_hyphen(file_name)
                    reason = "JSON files should use hyphens, not underscores"
                
                # YAML files with underscores
                elif ext in ['.yaml', '.yml'] and '_' in file_name:
                    needs_rename = True
                    new_name = self.convert_underscore_to_hyphen(file_name)
                    reason = "YAML files should use hyphens, not underscores"
                
                # Markdown files with underscores (not UPPERCASE)
                elif ext == '.md' and '_' in file_name and not file_name.isupper():
                    needs_rename = True
                    new_name = self.convert_underscore_to_hyphen(file_name)
                    reason = "Markdown files should use hyphens, not underscores"
                
                # Shell scripts with underscores
                elif ext == '.sh' and '_' in file_name:
                    needs_rename = True
                    new_name = self.convert_underscore_to_hyphen(file_name)
                    reason = "Shell scripts should use hyphens, not underscores"
                
                if needs_rename and new_name != file_name:
                    files_to_rename.append({
                        "old_path": str(file_path),
                        "new_path": str(root_path / new_name),
                        "old_name": file_name,
                        "new_name": new_name,
                        "reason": reason
                    })
        
        return files_to_rename
    
    def apply_renames(self, files_to_rename: List[Dict], dry_run: bool = True) -> List[Dict]:
        """Apply file renames"""
        results = []
        
        for item in files_to_rename:
            old_path = Path(item["old_path"])
            new_path = Path(item["new_path"])
            
            if not old_path.exists():
                results.append({
                    "status": "SKIPPED",
                    "old_name": item["old_name"],
                    "reason": "File not found"
                })
                continue
            
            if new_path.exists():
                results.append({
                    "status": "SKIPPED",
                    "old_name": item["old_name"],
                    "new_name": item["new_name"],
                    "reason": "Target file already exists"
                })
                continue
            
            if dry_run:
                results.append({
                    "status": "PREVIEW",
                    "old_name": item["old_name"],
                    "new_name": item["new_name"],
                    "reason": item["reason"]
                })
            else:
                try:
                    old_path.rename(new_path)
                    results.append({
                        "status": "RENAMED",
                        "old_name": item["old_name"],
                        "new_name": item["new_name"]
                    })
                    self.changes.append(item)
                except Exception as e:
                    results.append({
                        "status": "ERROR",
                        "old_name": item["old_name"],
                        "error": str(e)
                    })
                    self.errors.append({
                        "file": item["old_name"],
                        "error": str(e)
                    })
        
        return results
    
    def generate_report(self, results: List[Dict]) -> Dict:
        """Generate alignment report"""
        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "summary": {
                "total": len(results),
                "renamed": len([r for r in results if r.get("status") == "RENAMED"]),
                "skipped": len([r for r in results if r.get("status") == "SKIPPED"]),
                "errors": len([r for r in results if r.get("status") == "ERROR"]),
                "preview": len([r for r in results if r.get("status") == "PREVIEW"])
            },
            "changes": results,
            "errors": self.errors
        }
    
    def save_report(self, report: Dict, output_dir: str = "reports/naming"):
        """Save alignment report"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        report_file = output_path / f"file-naming-alignment-report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✅ Report saved: {report_file}")
        return str(report_file)


def main(apply: bool = False):
    """Main execution function"""
    print("=" * 80)
    print("🎯 File Naming Alignment Tool")
    print("=" * 80)
    
    aligner = FileNamingAligner()
    
    # Get files to rename
    files_to_rename = aligner.get_files_to_rename()
    
    print(f"\n📋 Found {len(files_to_rename)} files to rename:")
    print("-" * 60)
    
    # Show first 20 files
    for i, item in enumerate(files_to_rename[:20]):
        print(f"{i+1:3}. {item['old_name']}")
        print(f"     → {item['new_name']}")
        print(f"     Reason: {item['reason']}")
    
    if len(files_to_rename) > 20:
        print(f"\n... and {len(files_to_rename) - 20} more files")
    
    print("\n" + "=" * 80)
    
    # Apply or preview
    results = aligner.apply_renames(files_to_rename, dry_run=not apply)
    
    # Generate and save report
    report = aligner.generate_report(results)
    aligner.save_report(report)
    
    print("\n📊 Summary:")
    print(f"   Total files: {report['summary']['total']}")
    if apply:
        print(f"   Renamed: {report['summary']['renamed']}")
    else:
        print(f"   Preview: {report['summary']['preview']}")
    print(f"   Skipped: {report['summary']['skipped']}")
    print(f"   Errors: {report['summary']['errors']}")
    
    print("\n" + "=" * 80)
    if not apply:
        print("ℹ️  This was a DRY RUN. To apply changes, run with --apply flag")
    print("=" * 80)
    
    return report


if __name__ == "__main__":
    import sys
    
    apply_flag = "--apply" in sys.argv
    main(apply=apply_flag)
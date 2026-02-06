#!/usr/bin/env python3
"""
Naming Consistency Alignment Tool
命名一致性全對齊工具

Enforces naming conventions according to GL60 (Field Definitions) and GL65 (Format Constraints)
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Naming Convention Rules based on GL60 and enforcement-rules.yaml
NAMING_RULES = {
    "gl_anchors": {
        "pattern": r"^GL[0-9]{2}$",
        "description": "GL anchors must follow GL00-GL99 pattern",
        "examples": ["GL00", "GL50", "GL99"],
        "gl_binding": "GL60"
    },
    "yaml_files": {
        "pattern": r"^[a-z][a-z0-9-]*\.(yaml|yml)$",
        "description": "YAML files must use lowercase with hyphens",
        "examples": ["governance-framework-baseline.yaml", "meta-spec.yaml"],
        "gl_binding": "GL00"
    },
    "json_files": {
        "pattern": r"^[a-z][a-z0-9-]*\.json$",
        "description": "JSON files must use lowercase with hyphens",
        "examples": ["unified-governance-integration.json"],
        "gl_binding": "GL01"
    },
    "schema_files": {
        "pattern": r"^[a-z][a-z0-9-]*\.schema\.json$",
        "description": "Schema files must use .schema.json suffix",
        "examples": ["governance.schema.json", "meta-format.schema.json"],
        "gl_binding": "GL50"
    },
    "python_files": {
        "pattern": r"^[a-z][a-z0-9_]*\.py$",
        "description": "Python files must use lowercase with underscores",
        "examples": ["governance_enforcer.py", "apply_auto_fixes.py"],
        "gl_binding": "GL03"
    },
    "shell_scripts": {
        "pattern": r"^[a-z][a-z0-9-]*\.sh$",
        "description": "Shell scripts must use lowercase with hyphens",
        "examples": ["run-tests.sh", "deploy.sh"],
        "gl_binding": "GL04"
    },
    "markdown_files": {
        "pattern": r"^[A-Z][A-Za-z0-9-]*\.md$|^[a-z][a-z0-9-]*\.md$",
        "description": "Markdown files can use PascalCase or lowercase with hyphens",
        "examples": ["readme.md", "governance-guide.md"],
        "gl_binding": "GL02"
    },
    "contract_files": {
        "pattern": r"^[a-z][a-z0-9-]*-contract\.(yaml|json)$",
        "description": "Contract files must use -contract suffix",
        "examples": ["governance-contract.yaml", "adapter-contract.json"],
        "gl_binding": "GL36"
    },
    "directories": {
        "pattern": r"^[a-z][a-z0-9-]*$",
        "description": "Directories must use lowercase with hyphens",
        "examples": ["governance", "meta-governance", "dual-path"],
        "gl_binding": "GL60"
    }
}

# Special naming patterns for specific contexts
SPECIAL_PATTERNS = {
    "gl_semantic_anchors": {
        "pattern": r"^GL[0-9]{2}-GL[0-9]{2}.*\.json$",
        "description": "GL semantic anchor files",
        "examples": ["GL00-GL99-unified-charter.json"]
    },
    "audit_reports": {
        "pattern": r"^audit_report_[0-9]{8}_[0-9]{6}\.json$",
        "description": "Audit report files with timestamp",
        "examples": ["audit_report_20260203_161835.json"]
    },
    "layer_directories": {
        "pattern": r"^l[0-9]{2}-[a-z]+$",
        "description": "Layer directories with L prefix",
        "examples": ["l00-language", "l50-format"]
    }
}

class NamingConsistencyChecker:
    """Check and enforce naming consistency across the repository"""
    
    def __init__(self, workspace_root: str = "/workspace"):
        self.workspace_root = Path(workspace_root)
        self.violations = []
        self.compliant = []
        self.suggestions = []
        
    def check_file_naming(self, file_path: Path) -> Tuple[bool, str, Optional[str]]:
        """Check if a file follows naming conventions"""
        file_name = file_path.name
        file_ext = file_path.suffix.lower()
        
        # Determine which rule applies
        if file_ext in ['.yaml', '.yml']:
            if '-contract' in file_name:
                rule = NAMING_RULES["contract_files"]
            else:
                rule = NAMING_RULES["yaml_files"]
        elif file_ext == '.json':
            if '.schema.json' in file_name:
                rule = NAMING_RULES["schema_files"]
            elif file_name.startswith('GL'):
                # Special case for GL semantic anchor files
                return True, "GL semantic anchor file", None
            else:
                rule = NAMING_RULES["json_files"]
        elif file_ext == '.py':
            rule = NAMING_RULES["python_files"]
        elif file_ext == '.sh':
            rule = NAMING_RULES["shell_scripts"]
        elif file_ext == '.md':
            rule = NAMING_RULES["markdown_files"]
        else:
            return True, "No specific naming rule", None
        
        # Check against pattern
        if re.match(rule["pattern"], file_name):
            return True, rule["description"], None
        else:
            # Generate suggestion
            suggestion = self._generate_suggestion(file_name, rule)
            return False, rule["description"], suggestion
    
    def check_directory_naming(self, dir_path: Path) -> Tuple[bool, str, Optional[str]]:
        """Check if a directory follows naming conventions"""
        dir_name = dir_path.name
        
        # Skip hidden directories
        if dir_name.startswith('.'):
            return True, "Hidden directory", None
        
        # Check for layer directories
        if re.match(SPECIAL_PATTERNS["layer_directories"]["pattern"], dir_name):
            return True, "Layer directory", None
        
        # Check standard directory naming
        rule = NAMING_RULES["directories"]
        if re.match(rule["pattern"], dir_name):
            return True, rule["description"], None
        else:
            suggestion = self._generate_suggestion(dir_name, rule)
            return False, rule["description"], suggestion
    
    def _generate_suggestion(self, name: str, rule: Dict) -> str:
        """Generate a naming suggestion based on the rule"""
        # Convert to lowercase with hyphens
        suggested = re.sub(r'([A-Z])', r'-\1', name).lower()
        suggested = re.sub(r'^-', '', suggested)
        suggested = re.sub(r'_', '-', suggested)
        suggested = re.sub(r'--+', '-', suggested)
        return suggested
    
    def scan_repository(self) -> Dict:
        """Scan the repository for naming consistency"""
        print("🔍 Scanning repository for naming consistency...")
        
        # Directories to exclude
        exclude_dirs = {
            '.git', '__pycache__', 'node_modules', '.venv', 'venv',
            'outputs', 'summarized_conversations'
        }
        
        # Scan files and directories
        for root, dirs, files in os.walk(self.workspace_root):
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            root_path = Path(root)
            
            # Check directory naming
            for dir_name in dirs:
                dir_path = root_path / dir_name
                is_compliant, rule_desc, suggestion = self.check_directory_naming(dir_path)
                
                if is_compliant:
                    self.compliant.append({
                        "type": "directory",
                        "path": str(dir_path),
                        "name": dir_name,
                        "rule": rule_desc
                    })
                else:
                    self.violations.append({
                        "type": "directory",
                        "path": str(dir_path),
                        "name": dir_name,
                        "rule": rule_desc,
                        "suggestion": suggestion
                    })
            
            # Check file naming
            for file_name in files:
                # Skip hidden files
                if file_name.startswith('.'):
                    continue
                
                file_path = root_path / file_name
                is_compliant, rule_desc, suggestion = self.check_file_naming(file_path)
                
                if is_compliant:
                    self.compliant.append({
                        "type": "file",
                        "path": str(file_path),
                        "name": file_name,
                        "rule": rule_desc
                    })
                else:
                    self.violations.append({
                        "type": "file",
                        "path": str(file_path),
                        "name": file_name,
                        "rule": rule_desc,
                        "suggestion": suggestion
                    })
        
        return {
            "total_checked": len(self.compliant) + len(self.violations),
            "compliant": len(self.compliant),
            "violations": len(self.violations),
            "compliance_rate": f"{len(self.compliant) / (len(self.compliant) + len(self.violations)) * 100:.1f}%" if (len(self.compliant) + len(self.violations)) > 0 else "N/A"
        }
    
    def generate_report(self) -> Dict:
        """Generate a detailed naming consistency report"""
        print("\n📊 Generating naming consistency report...")
        
        report = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "summary": {
                "total_checked": len(self.compliant) + len(self.violations),
                "compliant": len(self.compliant),
                "violations": len(self.violations),
                "compliance_rate": f"{len(self.compliant) / (len(self.compliant) + len(self.violations)) * 100:.1f}%" if (len(self.compliant) + len(self.violations)) > 0 else "N/A"
            },
            "naming_rules": NAMING_RULES,
            "violations": self.violations[:100],  # Limit to first 100 violations
            "violation_categories": {}
        }
        
        # Categorize violations
        for violation in self.violations:
            category = violation["type"]
            if category not in report["violation_categories"]:
                report["violation_categories"][category] = []
            report["violation_categories"][category].append(violation)
        
        return report
    
    def print_summary(self):
        """Print a summary of naming consistency check"""
        print("\n" + "=" * 80)
        print("📋 Naming Consistency Check Summary")
        print("=" * 80)
        
        total = len(self.compliant) + len(self.violations)
        compliance_rate = len(self.compliant) / total * 100 if total > 0 else 0
        
        print(f"\n✅ Compliant: {len(self.compliant)}")
        print(f"❌ Violations: {len(self.violations)}")
        print(f"📊 Compliance Rate: {compliance_rate:.1f}%")
        
        if self.violations:
            print("\n⚠️  Top Violations:")
            for i, violation in enumerate(self.violations[:10]):
                print(f"   {i+1}. {violation['name']}")
                print(f"      Path: {violation['path']}")
                print(f"      Rule: {violation['rule']}")
                if violation.get('suggestion'):
                    print(f"      Suggestion: {violation['suggestion']}")
    
    def save_report(self, output_dir: str = "reports/naming"):
        """Save the naming consistency report"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        report = self.generate_report()
        report_file = output_path / f"naming-consistency-report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✅ Report saved: {report_file}")
        return str(report_file)


class NamingAligner:
    """Align naming conventions across the repository"""
    
    def __init__(self, workspace_root: str = "/workspace"):
        self.workspace_root = Path(workspace_root)
        self.changes = []
        
    def suggest_renames(self, violations: List[Dict]) -> List[Dict]:
        """Generate rename suggestions for violations"""
        suggestions = []
        
        for violation in violations:
            if violation.get('suggestion'):
                suggestions.append({
                    "original": violation['path'],
                    "suggested": violation['suggestion'],
                    "type": violation['type'],
                    "rule": violation['rule']
                })
        
        return suggestions
    
    def apply_renames(self, suggestions: List[Dict], dry_run: bool = True) -> List[Dict]:
        """Apply rename suggestions (dry_run=True for preview only)"""
        results = []
        
        for suggestion in suggestions:
            original_path = Path(suggestion['original'])
            
            if not original_path.exists():
                results.append({
                    "status": "SKIPPED",
                    "original": suggestion['original'],
                    "reason": "File/directory not found"
                })
                continue
            
            # Generate new path
            new_name = suggestion['suggested']
            new_path = original_path.parent / new_name
            
            if dry_run:
                results.append({
                    "status": "PREVIEW",
                    "original": str(original_path),
                    "new": str(new_path),
                    "type": suggestion['type']
                })
            else:
                try:
                    original_path.rename(new_path)
                    results.append({
                        "status": "RENAMED",
                        "original": str(original_path),
                        "new": str(new_path),
                        "type": suggestion['type']
                    })
                except Exception as e:
                    results.append({
                        "status": "ERROR",
                        "original": str(original_path),
                        "error": str(e)
                    })
        
        return results


def main():
    """Main execution function"""
    print("=" * 80)
    print("🎯 Naming Consistency Alignment Tool")
    print("=" * 80)
    
    # Initialize checker
    checker = NamingConsistencyChecker()
    
    # Scan repository
    summary = checker.scan_repository()
    
    # Print summary
    checker.print_summary()
    
    # Save report
    report_file = checker.save_report()
    
    # Generate alignment suggestions if there are violations
    if checker.violations:
        print("\n" + "=" * 80)
        print("🔧 Alignment Suggestions")
        print("=" * 80)
        
        aligner = NamingAligner()
        suggestions = aligner.suggest_renames(checker.violations[:20])
        
        if suggestions:
            print("\nTop rename suggestions:")
            for i, suggestion in enumerate(suggestions[:10]):
                print(f"   {i+1}. {suggestion['original']}")
                print(f"      → {suggestion['suggested']}")
    
    print("\n" + "=" * 80)
    print("✅ Naming Consistency Check Complete")
    print("=" * 80)
    
    return summary


if __name__ == "__main__":
    main()
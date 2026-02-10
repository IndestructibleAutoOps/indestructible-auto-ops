#!/usr/bin/env python3
"""
Integration Testing Script for Phase 4: gl-* to gov-* Migration
Validates all changes and ensures no breaking changes
"""

import os
import sys
import re
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime

class IntegrationTester:
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir).resolve()
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "python_tests": {},
            "yaml_tests": {},
            "shell_tests": {},
            "markdown_tests": {},
            "ci_cd_tests": {},
            "summary": {
                "total_files_tested": 0,
                "files_passed": 0,
                "files_failed": 0,
                "issues_found": []
            }
        }
        
    def find_files_by_extension(self, extensions: List[str]) -> List[Path]:
        """Find all files with given extensions"""
        files = []
        for ext in extensions:
            files.extend(self.root_dir.rglob(f"*{ext}"))
        # Exclude backup directories
        files = [f for f in files if ".backup" not in str(f)]
        return files
    
    def test_python_imports(self) -> Dict:
        """Test Python files for import issues"""
        print("\n[1/5] Testing Python Import Resolution...")
        python_files = self.find_files_by_extension([".py"])
        results = {
            "total_files": len(python_files),
            "files_tested": 0,
            "files_passed": 0,
            "files_failed": 0,
            "issues": []
        }
        
        for py_file in python_files:
            results["files_tested"] += 1
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Check for broken imports
                issues = []
                
                # Check for gl- imports that should be gov-
                gl_imports = re.findall(r'from\s+gl-[\w\.]+\s+import|import\s+gl-[\w\.]+', content)
                if gl_imports:
                    issues.append({
                        "file": str(py_file.relative_to(self.root_dir)),
                        "type": "legacy_gl_import",
                        "details": f"Found {len(gl_imports)} gl- imports: {gl_imports[:3]}"
                    })
                
                # Check for gov- imports
                gov_imports = re.findall(r'from\s+gov-[\w\.]+\s+import|import\s+gov-[\w\.]+', content)
                
                # Syntax check using Python compiler
                try:
                    compile(content, str(py_file), 'exec')
                except SyntaxError as e:
                    issues.append({
                        "file": str(py_file.relative_to(self.root_dir)),
                        "type": "syntax_error",
                        "details": f"Line {e.lineno}: {e.msg}"
                    })
                
                if issues:
                    results["files_failed"] += 1
                    results["issues"].extend(issues)
                else:
                    results["files_passed"] += 1
                    
            except Exception as e:
                results["files_failed"] += 1
                results["issues"].append({
                    "file": str(py_file.relative_to(self.root_dir)),
                    "type": "read_error",
                    "details": str(e)
                })
        
        self.results["python_tests"] = results
        self.results["summary"]["total_files_tested"] += results["files_tested"]
        self.results["summary"]["files_passed"] += results["files_passed"]
        self.results["summary"]["files_failed"] += results["files_failed"]
        self.results["summary"]["issues_found"].extend(results["issues"])
        
        print(f"  ✓ Tested {results['files_tested']} Python files")
        print(f"    Passed: {results['files_passed']}, Failed: {results['files_failed']}")
        print(f"    Issues found: {len(results['issues'])}")
        
        return results
    
    def test_yaml_configs(self) -> Dict:
        """Test YAML configuration files"""
        print("\n[2/5] Testing YAML Configuration Files...")
        yaml_files = self.find_files_by_extension([".yaml", ".yml"])
        results = {
            "total_files": len(yaml_files),
            "files_tested": 0,
            "files_passed": 0,
            "files_failed": 0,
            "issues": []
        }
        
        try:
            import yaml
        except ImportError:
            print("  ⚠ PyYAML not installed, skipping YAML validation")
            return results
        
        for yaml_file in yaml_files:
            results["files_tested"] += 1
            try:
                with open(yaml_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                issues = []
                
                # Check for gl- references
                gl_refs = re.findall(r'\bgl-[\w\-\.\/]+', content)
                if gl_refs:
                    issues.append({
                        "file": str(yaml_file.relative_to(self.root_dir)),
                        "type": "legacy_gl_reference",
                        "details": f"Found {len(gl_refs)} gl- references: {gl_refs[:3]}"
                    })
                
                # Parse YAML to check structure
                try:
                    yaml.safe_load(content)
                except yaml.YAMLError as e:
                    issues.append({
                        "file": str(yaml_file.relative_to(self.root_dir)),
                        "type": "yaml_error",
                        "details": str(e)
                    })
                
                if issues:
                    results["files_failed"] += 1
                    results["issues"].extend(issues)
                else:
                    results["files_passed"] += 1
                    
            except Exception as e:
                results["files_failed"] += 1
                results["issues"].append({
                    "file": str(yaml_file.relative_to(self.root_dir)),
                    "type": "read_error",
                    "details": str(e)
                })
        
        self.results["yaml_tests"] = results
        self.results["summary"]["total_files_tested"] += results["files_tested"]
        self.results["summary"]["files_passed"] += results["files_passed"]
        self.results["summary"]["files_failed"] += results["files_failed"]
        self.results["summary"]["issues_found"].extend(results["issues"])
        
        print(f"  ✓ Tested {results['files_tested']} YAML files")
        print(f"    Passed: {results['files_passed']}, Failed: {results['files_failed']}")
        print(f"    Issues found: {len(results['issues'])}")
        
        return results
    
    def test_shell_scripts(self) -> Dict:
        """Test shell scripts"""
        print("\n[3/5] Testing Shell Scripts...")
        shell_files = self.find_files_by_extension([".sh"])
        results = {
            "total_files": len(shell_files),
            "files_tested": 0,
            "files_passed": 0,
            "files_failed": 0,
            "issues": []
        }
        
        for shell_file in shell_files:
            results["files_tested"] += 1
            try:
                with open(shell_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                issues = []
                
                # Check for gl- paths
                gl_refs = re.findall(r'[/\s]gl-[\w\-\.\/]+', content)
                if gl_refs:
                    issues.append({
                        "file": str(shell_file.relative_to(self.root_dir)),
                        "type": "legacy_gl_path",
                        "details": f"Found {len(gl_refs)} gl- paths: {gl_refs[:3]}"
                    })
                
                # Check for executable permission
                if not os.access(shell_file, os.X_OK):
                    issues.append({
                        "file": str(shell_file.relative_to(self.root_dir)),
                        "type": "permission_warning",
                        "details": "Script is not executable"
                    })
                
                # Basic syntax check (shebang)
                if not content.startswith("#!"):
                    issues.append({
                        "file": str(shell_file.relative_to(self.root_dir)),
                        "type": "missing_shebang",
                        "details": "Script missing shebang line"
                    })
                
                if issues:
                    results["files_failed"] += 1
                    results["issues"].extend(issues)
                else:
                    results["files_passed"] += 1
                    
            except Exception as e:
                results["files_failed"] += 1
                results["issues"].append({
                    "file": str(shell_file.relative_to(self.root_dir)),
                    "type": "read_error",
                    "details": str(e)
                })
        
        self.results["shell_tests"] = results
        self.results["summary"]["total_files_tested"] += results["files_tested"]
        self.results["summary"]["files_passed"] += results["files_passed"]
        self.results["summary"]["files_failed"] += results["files_failed"]
        self.results["summary"]["issues_found"].extend(results["issues"])
        
        print(f"  ✓ Tested {results['files_tested']} shell scripts")
        print(f"    Passed: {results['files_passed']}, Failed: {results['files_failed']}")
        print(f"    Issues found: {len(results['issues'])}")
        
        return results
    
    def test_markdown_links(self) -> Dict:
        """Test markdown documentation links"""
        print("\n[4/5] Testing Markdown Documentation Links...")
        markdown_files = self.find_files_by_extension([".md"])
        results = {
            "total_files": len(markdown_files),
            "files_tested": 0,
            "files_passed": 0,
            "files_failed": 0,
            "issues": []
        }
        
        for md_file in markdown_files:
            results["files_tested"] += 1
            try:
                with open(md_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                issues = []
                
                # Check for gl- links in markdown
                gl_links = re.findall(r'\[([^\]]+)\]\([^)]*gl-[^)]*\)', content)
                if gl_links:
                    issues.append({
                        "file": str(md_file.relative_to(self.root_dir)),
                        "type": "legacy_gl_link",
                        "details": f"Found {len(gl_links)} gl- links"
                    })
                
                # Check for broken internal links (simple check)
                internal_links = re.findall(r'\]\(([^)]+)\)', content)
                for link in internal_links:
                    if link.startswith('http'):
                        continue  # Skip external links
                    # Check if linked file exists (relative path)
                    link_path = md_file.parent / link.split('#')[0]
                    if link_path and not link_path.exists() and link_path.suffix in ['.md', '.yaml', '.py']:
                        issues.append({
                            "file": str(md_file.relative_to(self.root_dir)),
                            "type": "broken_link",
                            "details": f"Broken link: {link}"
                        })
                
                if issues:
                    results["files_failed"] += 1
                    results["issues"].extend(issues)
                else:
                    results["files_passed"] += 1
                    
            except Exception as e:
                results["files_failed"] += 1
                results["issues"].append({
                    "file": str(md_file.relative_to(self.root_dir)),
                    "type": "read_error",
                    "details": str(e)
                })
        
        self.results["markdown_tests"] = results
        self.results["summary"]["total_files_tested"] += results["files_tested"]
        self.results["summary"]["files_passed"] += results["files_passed"]
        self.results["summary"]["files_failed"] += results["files_failed"]
        self.results["summary"]["issues_found"].extend(results["issues"])
        
        print(f"  ✓ Tested {results['files_tested']} markdown files")
        print(f"    Passed: {results['files_passed']}, Failed: {results['files_failed']}")
        print(f"    Issues found: {len(results['issues'])}")
        
        return results
    
    def test_ci_cd_workflows(self) -> Dict:
        """Test CI/CD workflow files"""
        print("\n[5/5] Testing CI/CD Workflows...")
        workflow_dir = self.root_dir / ".github" / "workflows"
        results = {
            "total_files": 0,
            "files_tested": 0,
            "files_passed": 0,
            "files_failed": 0,
            "issues": []
        }
        
        if not workflow_dir.exists():
            print("  ⚠ No .github/workflows directory found")
            return results
        
        workflow_files = list(workflow_dir.rglob("*.yml")) + list(workflow_dir.rglob("*.yaml"))
        results["total_files"] = len(workflow_files)
        
        try:
            import yaml
        except ImportError:
            print("  ⚠ PyYAML not installed, skipping workflow validation")
            return results
        
        for workflow_file in workflow_files:
            results["files_tested"] += 1
            try:
                with open(workflow_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                issues = []
                
                # Check for gl- references
                gl_refs = re.findall(r'\bgl-[\w\-\.\/]+', content)
                if gl_refs:
                    issues.append({
                        "file": str(workflow_file.relative_to(self.root_dir)),
                        "type": "legacy_gl_reference",
                        "details": f"Found {len(gl_refs)} gl- references: {gl_refs[:3]}"
                    })
                
                # Parse workflow YAML
                try:
                    workflow = yaml.safe_load(content)
                    
                    # Check for required fields
                    if workflow and isinstance(workflow, dict):
                        if 'name' not in workflow:
                            issues.append({
                                "file": str(workflow_file.relative_to(self.root_dir)),
                                "type": "missing_field",
                                "details": "Missing 'name' field"
                            })
                        if 'on' not in workflow and 'trigger' not in workflow:
                            issues.append({
                                "file": str(workflow_file.relative_to(self.root_dir)),
                                "type": "missing_field",
                                "details": "Missing 'on' trigger field"
                            })
                except yaml.YAMLError as e:
                    issues.append({
                        "file": str(workflow_file.relative_to(self.root_dir)),
                        "type": "yaml_error",
                        "details": str(e)
                    })
                
                if issues:
                    results["files_failed"] += 1
                    results["issues"].extend(issues)
                else:
                    results["files_passed"] += 1
                    
            except Exception as e:
                results["files_failed"] += 1
                results["issues"].append({
                    "file": str(workflow_file.relative_to(self.root_dir)),
                    "type": "read_error",
                    "details": str(e)
                })
        
        self.results["ci_cd_tests"] = results
        self.results["summary"]["total_files_tested"] += results["files_tested"]
        self.results["summary"]["files_passed"] += results["files_passed"]
        self.results["summary"]["files_failed"] += results["files_failed"]
        self.results["summary"]["issues_found"].extend(results["issues"])
        
        print(f"  ✓ Tested {results['files_tested']} CI/CD workflow files")
        print(f"    Passed: {results['files_passed']}, Failed: {results['files_failed']}")
        print(f"    Issues found: {len(results['issues'])}")
        
        return results
    
    def run_all_tests(self) -> Dict:
        """Run all integration tests"""
        print("="*80)
        print("PHASE 4: INTEGRATION TESTING")
        print("="*80)
        print(f"Root directory: {self.root_dir}")
        print(f"Testing started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run all test suites
        self.test_python_imports()
        self.test_yaml_configs()
        self.test_shell_scripts()
        self.test_markdown_links()
        self.test_ci_cd_workflows()
        
        # Generate summary
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)
        print(f"Total files tested: {self.results['summary']['total_files_tested']}")
        print(f"Files passed: {self.results['summary']['files_passed']}")
        print(f"Files failed: {self.results['summary']['files_failed']}")
        print(f"Total issues found: {len(self.results['summary']['issues_found'])}")
        
        if self.results['summary']['issues_found']:
            print("\n📋 Issues by Type:")
            issue_types = {}
            for issue in self.results['summary']['issues_found']:
                issue_type = issue.get('type', 'unknown')
                issue_types[issue_type] = issue_types.get(issue_type, 0) + 1
            
            for issue_type, count in sorted(issue_types.items(), key=lambda x: x[1], reverse=True):
                print(f"  - {issue_type}: {count}")
        
        print("="*80)
        
        return self.results
    
    def save_results(self, output_file: str = None):
        """Save test results to JSON file"""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"phase4_integration_test_results_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\nTest results saved to: {output_file}")
        return output_file


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Run integration tests for gl-* to gov-* migration')
    parser.add_argument('--root', default='.', help='Root directory to test')
    parser.add_argument('--output', help='Output file for test results')
    
    args = parser.parse_args()
    
    tester = IntegrationTester(args.root)
    results = tester.run_all_tests()
    
    # Save results
    output_file = tester.save_results(args.output)
    
    # Exit with appropriate code
    if results['summary']['files_failed'] > 0:
        print(f"\n⚠ {results['summary']['files_failed']} file(s) failed tests")
        sys.exit(1)
    else:
        print("\n✅ All tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
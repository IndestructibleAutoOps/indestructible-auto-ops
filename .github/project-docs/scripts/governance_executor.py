# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: legacy-scripts
# @GL-audit-trail: ../../engine/gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
#!/usr/bin/env python3
"""
System Governance Executor
Executes all gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance files systematically and detects problems
"""

import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
from enhanced_yaml_parser import EnhancedYAMLParser

class GovernanceExecutor:
    def __init__(self, base_path: str = "/workspace/machine-native-ops"):
        self.base_path = Path(base_path)
        self.gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance_path = self.base_path / "gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance"
        self.results = {
            "execution_timestamp": datetime.now().isoformat(),
            "total_files": 0,
            "executed_files": 0,
            "failed_files": 0,
            "problems_detected": [],
            "compliance_status": {},
            "execution_log": []
        }
        
    def scan_gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance_files(self) -> List[Path]:
        """Scan all gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance files excluding evidence archives"""
        gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance_files = []
        for file_path in self.gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance_path.rglob("*"):
            if file_path.is_file() and file_path.suffix in ['.md', '.yaml', '.yml', '.json']:
                # Skip evidence directories
                if 'evidence' not in str(file_path) and '.tar.gz' not in str(file_path):
                    gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance_files.append(file_path)
        return sorted(gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance_files)
    
    def execute_markdown_file(self, file_path: Path) -> Dict[str, Any]:
        """Execute/analyze markdown file"""
        result = {
            "file": str(file_path),
            "status": "success",
            "content_lines": 0,
            "headers": [],
            "problems": []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                result["content_lines"] = len(lines)
                
                # Extract headers
                for line in lines:
                    if line.startswith('#'):
                        result["headers"].append(line.strip())
                
                # Detect potential problems
                if "TODO" in content or "FIXME" in content or "XXX" in content:
                    result["problems"].append("Contains TODO/FIXME markers")
                
                if len(lines) < 5:
                    result["problems"].append("File appears to be very short or incomplete")
                    
        except Exception as e:
            result["status"] = "error"
            result["problems"].append(f"Reading error: {str(e)}")
            
        return result
    
    def execute_yaml_file(self, file_path: Path) -> Dict[str, Any]:
        """Execute/validate YAML file"""
        result = {
            "file": str(file_path),
            "status": "success",
            "structure": {},
            "problems": []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8'):
                # Use EnhancedYAMLParser for multi-document support
                parser = EnhancedYAMLParser()
                parse_result = parser.parse_and_validate(file_path)
                
                # Initialize first_doc to None
                first_doc = None
                
                # Get the first document for structure validation
                # Handle both list (multi-doc) and dict (single-doc) results
                if parse_result.get("data"):
                    if isinstance(parse_result["data"], list):
                        first_doc = parse_result["data"][0]
                    else:
                        first_doc = parse_result["data"]
                    result["structure"] = str(type(first_doc))
                    
                    # Validate YAML structure
                    if first_doc is None:
                        result["problems"].append("YAML file is empty")
                    elif isinstance(first_doc, dict):
                        if not first_doc:
                            result["problems"].append("YAML dictionary is empty")
                    
                    # Add any warnings from the parser
                    if parse_result.get("warnings"):
                        result["problems"].extend(parse_result["warnings"])
                else:
                    result["problems"].append("No documents found")
                
                # Check for common gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance issues
                if first_doc is not None and isinstance(first_doc, dict):
                    if 'version' not in first_doc and 'metadata' not in first_doc:
                        result["problems"].append("Missing version or metadata section")
                        
        except yaml.YAMLError as e:
            result["status"] = "error"
            result["problems"].append(f"YAML parsing error: {str(e)}")
        except Exception as e:
            result["status"] = "error"
            result["problems"].append(f"Processing error: {str(e)}")
            
        return result
    
    def execute_json_file(self, file_path: Path) -> Dict[str, Any]:
        """Execute/validate JSON file"""
        result = {
            "file": str(file_path),
            "status": "success",
            "structure": {},
            "problems": []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
                result["structure"] = str(type(content))
                
                # Validate JSON structure
                if content is None:
                    result["problems"].append("JSON file is empty")
                elif isinstance(content, dict):
                    if not content:
                        result["problems"].append("JSON object is empty")
                        
        except json.JSONDecodeError as e:
            result["status"] = "error"
            result["problems"].append(f"JSON parsing error: {str(e)}")
        except Exception as e:
            result["status"] = "error"
            result["problems"].append(f"Processing error: {str(e)}")
            
        return result
    
    def execute_file(self, file_path: Path) -> Dict[str, Any]:
        """Execute appropriate handler based on file type"""
        if file_path.suffix == '.md':
            return self.execute_markdown_file(file_path)
        elif file_path.suffix in ['.yaml', '.yml']:
            return self.execute_yaml_file(file_path)
        elif file_path.suffix == '.json':
            return self.execute_json_file(file_path)
        else:
            return {
                "file": str(file_path),
                "status": "skipped",
                "problems": ["Unsupported file type"]
            }
    
    def detect_system_problems(self) -> List[Dict[str, Any]]:
        """Detect problems across the entire system"""
        problems = []
        
        # Check ETL Pipeline
        etl_path = self.base_path / "etl-pipeline"
        if etl_path.exists():
            var_path = etl_path / "var" / "evidence"
            if not var_path.exists() or not list(var_path.iterdir()):
                problems.append({
                    "component": "ETL Pipeline",
                    "severity": "warning",
                    "issue": "Evidence directory is empty or missing",
                    "location": str(var_path)
                })
        
        # Check Elasticsearch System
        es_path = self.base_path / "elasticsearch-search-system"
        if es_path.exists():
            var_path = es_path / "var" / "evidence"
            if not var_path.exists() or not list(var_path.iterdir()):
                problems.append({
                    "component": "Elasticsearch System",
                    "severity": "warning",
                    "issue": "Evidence directory is empty or missing",
                    "location": str(var_path)
                })
        
        return problems
    
    def run_execution(self):
        """Execute all gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance files"""
        print(f"\n{'='*60}")
        print("Governance File Execution Starting")
        print(f"{'='*60}\n")
        
        # Scan gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance files
        files = self.scan_gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance_files()
        self.results["total_files"] = len(files)
        
        print(f"Found {len(files)} gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance files to process\n")
        
        # Execute each file
        for idx, file_path in enumerate(files, 1):
            print(f"[{idx}/{len(files)}] Processing: {file_path.relative_to(self.base_path)}")
            
            result = self.execute_file(file_path)
            self.results["execution_log"].append(result)
            
            if result["status"] == "error":
                self.results["failed_files"] += 1
                self.results["problems_detected"].extend(result["problems"])
            elif result["problems"]:
                self.results["problems_detected"].extend(
                    [f"{file_path.name}: {p}" for p in result["problems"]]
                )
            else:
                self.results["executed_files"] += 1
            
            print(f"  Status: {result['status'].upper()}")
            if result["problems"]:
                print(f"  Problems: {len(result['problems'])}")
                for problem in result["problems"][:2]:  # Show first 2 problems
                    print(f"    - {problem}")
            print()
        
        # Detect system problems
        print("\nDetecting system problems...")
        system_problems = self.detect_system_problems()
        self.results["problems_detected"].extend(
            [f"{p['component']}: {p['issue']}" for p in system_problems]
        )
        
        print(f"Found {len(system_problems)} system-level problems\n")
        
        # Calculate compliance status
        if self.results["failed_files"] == 0:
            self.results["compliance_status"]["overall"] = "compliant"
        elif self.results["failed_files"] < 3:
            self.results["compliance_status"]["overall"] = "partial"
        else:
            self.results["compliance_status"]["overall"] = "non-compliant"
        
        self.print_summary()
    
    def print_summary(self):
        """Print execution summary"""
        print(f"\n{'='*60}")
        print("Execution Summary")
        print(f"{'='*60}\n")
        
        print(f"Total Files: {self.results['total_files']}")
        print(f"Executed Successfully: {self.results['executed_files']}")
        print(f"Failed: {self.results['failed_files']}")
        print(f"Total Problems Detected: {len(self.results['problems_detected'])}")
        print(f"Compliance Status: {self.results['compliance_status']['overall'].upper()}")
        
        if self.results["problems_detected"]:
            print(f"\n{'='*60}")
            print("Problems Detected:")
            print(f"{'='*60}\n")
            for idx, problem in enumerate(self.results["problems_detected"][:10], 1):
                print(f"{idx}. {problem}")
            
            if len(self.results["problems_detected"]) > 10:
                print(f"\n... and {len(self.results['problems_detected']) - 10} more problems")
        
        print(f"\n{'='*60}\n")
    
    def save_report(self, output_path: str = "/workspace/machine-native-ops/workspace/gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance_execution_report.json"):
        """Save execution report to JSON file"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2)
        print(f"Report saved to: {output_path}")

def main():
    executor = GovernanceExecutor()
    executor.run_execution()
    executor.save_report()

if __name__ == "__main__":
    main()
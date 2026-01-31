#!/usr/bin/env python3
"""
GL Governance Simple Audit
Quick validation of GL gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance markers in YAML/JSON files

GL Unified Charter Activated ✓
"""

import json
import yaml
from pathlib import Path
from datetime import datetime

def check_file(file_path: Path) -> dict:
    """Check a single file for GL gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance markers."""
    result = {
        "file": str(file_path),
        "status": "unknown",
        "markers": {
            "@GL-governed": False,
            "@GL-layer": False,
            "@GL-semantic": False,
            "@GL-audit-trail": False
        },
        "issues": []
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for GL markers in content
        for marker in result["markers"]:
            result["markers"][marker] = marker in content
        
        # Try to parse YAML/JSON
        ext = file_path.suffix.lower()
        if ext in ['.yaml', '.yml']:
            try:
                yaml.safe_load(content)
                data = yaml.safe_load(content)
                result["status"] = "parsed"
            except yaml.YAMLError as e:
                result["status"] = "error"
                result["issues"].append(f"YAML parse error: {e}")
        elif ext == '.json':
            try:
                json.loads(content)
                data = json.loads(content)
                result["status"] = "parsed"
            except json.JSONDecodeError as e:
                result["status"] = "error"
                result["issues"].append(f"JSON parse error: {e}")
        else:
            result["status"] = "skipped"
        
    except Exception as e:
        result["status"] = "error"
        result["issues"].append(f"Read error: {e}")
    
    return result

def main():
    """Run simple GL gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance audit."""
    print("=" * 60)
    print("GL Governance Simple Audit")
    print("=" * 60)
    
    # Scan for YAML and JSON files
    yaml_files = list(Path('.').rglob('*.yaml')) + list(Path('.').rglob('*.yml'))
    json_files = list(Path('.').rglob('*.json'))
    
    all_files = yaml_files + json_files
    
    # Exclude node_modules and other common directories
    excluded_dirs = ['node_modules', '.git', '__pycache__', 'dist', 'build']
    filtered_files = [
        f for f in all_files 
        if not any(excluded in str(f) for excluded in excluded_dirs)
    ]
    
    print(f"\n📊 Found {len(filtered_files)} YAML/JSON files\n")
    
    results = []
    compliant = 0
    non_compliant = 0
    
    for file_path in filtered_files:
        result = check_file(file_path)
        results.append(result)
        
        # Check if compliant (has all required markers)
        if all(result["markers"].values()):
            compliant += 1
            status = "✅"
        else:
            non_compliant += 1
            status = "❌"
        
        print(f"{status} {file_path}")
        missing = [k for k, v in result["markers"].items() if not v]
        if missing:
            print(f"   Missing: {', '.join(missing)}")
        if result["issues"]:
            print(f"   Issues: {', '.join(result['issues'])}")
    
    # Generate summary
    summary = {
        "audit_date": datetime.now().isoformat(),
        "total_files": len(filtered_files),
        "compliant": compliant,
        "non_compliant": non_compliant,
        "compliance_rate": f"{(compliant/len(filtered_files)*100):.2f}%" if filtered_files else "0%",
        "results": results
    }
    
    # Save report
    report_path = Path("gl-simple-audit-report.json")
    with open(report_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("\n" + "=" * 60)
    print("Audit Summary")
    print("=" * 60)
    print(f"Total Files: {summary['total_files']}")
    print(f"Compliant: {compliant} ✅")
    print(f"Non-Compliant: {non_compliant} ❌")
    print(f"Compliance Rate: {summary['compliance_rate']}")
    print(f"\nReport saved: {report_path}")
    
    return summary

if __name__ == "__main__":
    main()
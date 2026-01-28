# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: legacy-scripts
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
#!/usr/bin/env python3
"""
GL Unified Charter - Comprehensive Workflow Cleanup & Fixer
Identifies and fixes ALL workflow issues including misclassified files
"""

import re
from pathlib import Path
import json

def is_workflow_file(file_path: Path) -> bool:
    """Check if a file is actually a workflow file or just a config file"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check if it has workflow structure
        has_name = bool(re.search(r'^name:\s*[\w\s-]+', content, re.MULTILINE))
        has_on = bool(re.search(r'^on:\s*$', content, re.MULTILINE) or re.search(r"^'on':", content, re.MULTILINE))
        has_jobs = bool(re.search(r'^jobs:\s*$', content, re.MULTILINE))
        
        # If it has all three, it's a workflow
        if has_name and has_on and has_jobs:
            return True
        
        # If it's clearly just config, return False
        if 'core:' in content and 'optional:' in content and 'linting:' in content:
            return False
        
        # Default to treating as workflow if it has 'on:' or 'jobs:'
        return has_on or has_jobs
        
    except Exception:
        return False

def analyze_all_workflows(repo_path: Path) -> dict:
    """Analyze all files in workflows directory"""
    workflow_dir = repo_path / ".github" / "workflows"
    
    yml_files = list(workflow_dir.glob("*.yml"))
    yaml_files = list(workflow_dir.glob("*.yaml"))
    all_files = yml_files + yaml_files
    
    results = {
        "total_files": len(all_files),
        "actual_workflows": [],
        "config_files": [],
        "problem_files": []
    }
    
    for file_path in all_files:
        if is_workflow_file(file_path):
            results["actual_workflows"].append(str(file_path.name))
        else:
            results["config_files"].append(str(file_path.name))
    
    return results

def main():
    repo_path = Path("/workspace/machine-native-ops")
    
    print(f"\n{'='*80}")
    print("GL WORKFLOW CLEANUP ANALYZER")
    print(f"{'='*80}\n")
    
    results = analyze_all_workflows(repo_path)
    
    print(f"Total files in .github/workflows/: {results['total_files']}")
    print(f"Actual workflow files: {len(results['actual_workflows'])}")
    print(f"Config files (should be moved): {len(results['config_files'])}")
    
    if results['config_files']:
        print("\nConfig files found (should be moved to config/):")
        for cfg in results['config_files']:
            print(f"  - {cfg}")
    
    if results['actual_workflows']:
        print("\nActual workflow files:")
        for wf in results['actual_workflows'][:10]:
            print(f"  - {wf}")
        if len(results['actual_workflows']) > 10:
            print(f"  ... and {len(results['actual_workflows']) - 10} more")
    
    # Save results
    json_path = repo_path / "WORKFLOW_CLEANUP_ANALYSIS.json"
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nAnalysis saved to: {json_path}\n")
    
    return results

if __name__ == "__main__":
    main()
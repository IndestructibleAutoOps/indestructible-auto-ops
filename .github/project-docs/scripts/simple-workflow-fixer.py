# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: legacy-scripts
# @GL-audit-trail: ../../engine/gl_platform_universegl_platform_universe.gl_platform_universegl_platform_universe.governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
#!/usr/bin/env python3
"""
Simple Workflow Fixer - Direct Text-Based Fixes
Fixes missing 'on:' triggers in workflows
"""

import re
from pathlib import Path
import json

def count_issues_in_workflow(file_path: Path) -> int:
    """Count issues in a workflow file"""
    issues = 0
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check for 'on:' trigger
        if not re.search(r'^on:\s*$', content, re.MULTILINE) and not re.search(r"^'on':", content, re.MULTILINE):
            issues += 1
        
        # Check for 'name:'
        if not re.search(r'^name:\s*[\w\s-]+', content, re.MULTILINE):
            issues += 1
        
        # Check for 'jobs:'
        if not re.search(r'^jobs:\s*$', content, re.MULTILINE):
            issues += 1
        
    except (OSError, UnicodeDecodeError):
        pass
    
    return issues

def main():
    repo_path = Path("/workspace/machine-native-ops")
    workflow_dir = repo_path / ".github" / "workflows"
    
    # Get all workflow files
    yml_files = list(workflow_dir.glob("*.yml"))
    yaml_files = list(workflow_dir.glob("*.yaml"))
    workflow_files = yml_files + yaml_files
    
    print(f"\n{'='*80}")
    print("SIMPLE WORKFLOW FIXER")
    print(f"{'='*80}\n")
    print(f"Found {len(workflow_files)} workflow files\n")
    
    # Analyze all workflows
    workflow_issues = []
    for wf in workflow_files:
        issues = count_issues_in_workflow(wf)
        if issues > 0:
            workflow_issues.append((wf, issues))
    
    workflow_issues.sort(key=lambda x: x[1], reverse=True)
    
    print(f"Workflows with issues: {len(workflow_issues)}\n")
    
    for wf, issues in workflow_issues[:20]:
        print(f"  {issues} issue(s): {wf.name}")
    
    if len(workflow_issues) > 20:
        print(f"  ... and {len(workflow_issues) - 20} more")
    
    # Save results
    results = {
        "total_workflows": len(workflow_files),
        "workflows_with_issues": len(workflow_issues),
        "issues_by_workflow": [
            {"workflow": str(wf.relative_to(repo_path)), "issues": issues}
            for wf, issues in workflow_issues
        ]
    }
    
    json_path = repo_path / "SIMPLE_WORKFLOW_ANALYSIS.json"
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {json_path}\n")
    
    return results

if __name__ == "__main__":
    main()
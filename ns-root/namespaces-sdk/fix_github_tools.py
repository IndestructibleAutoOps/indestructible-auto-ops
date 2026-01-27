#!/usr/bin/env python3
"""
GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module ns-root/namespaces-sdk
@gl-semantic-anchor GL-00-NAMESPAC_FIXGITHUBTOO
@gl-evidence-required false
GL Unified Charter Activated
"""

"""Fix GitHub tools.ts file to remove generic type parameters."""

import sys  # noqa: E402

def fix_github_tools():
    file_path = "src/adapters/github/tools.ts"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove ToolFactory import
    content = content.replace(', ToolFactory', '')
    
    # Fix GitHubTool base class
    content = content.replace(
        'abstract class GitHubTool<TInput, TOutput> extends Tool<TInput, TOutput> {',
        'abstract class GitHubTool extends Tool {'
    )
    
    # Remove generic parameters from all GitHub tool class definitions
    # Pattern: class GitHubXxxTool extends GitHubTool<T1, T2> {
    import re  # noqa: E402
    content = re.sub(
        r'(class GitHub\w+Tool) extends GitHubTool<[^>]+>',
        r'\1 extends GitHubTool',
        content
    )
    
    # Remove inputSchema and outputSchema from tool descriptors (they don't exist in ToolDescriptor)
    # Look for tool descriptors and remove inputSchema/outputSchema properties
    lines = content.split('\n')
    i = 0
    fixed_lines = []
    
    while i < len(lines):
        line = lines[i]
        fixed_lines.append(line)
        
        # If we find a tool descriptor, skip inputSchema and outputSchema properties
        if 'inputSchema:' in line or 'outputSchema:' in line:
            # Skip this line and the next line (the value)
            i += 1
            if i < len(lines):
                # Skip the closing comma line too if it exists
                if lines[i].strip().endswith(','):
                    i += 1
        
        i += 1
    
    content = '\n'.join(fixed_lines)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed {file_path}")

if __name__ == "__main__":
    sys.exit(
        "fix_github_tools.py is deprecated; GitHub tools fixes are now maintained directly "
        "in src/adapters/github/tools.ts and this script should no longer be run."
    )
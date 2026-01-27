#!/usr/bin/env python3
"""
GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module ns-root/namespaces-sdk
@gl-semantic-anchor GL-00-NAMESPAC_COMPREHENSIV
@gl-evidence-required false
GL Unified Charter Activated
"""

"""Comprehensive TypeScript fix script for Phase 12"""

import os  # noqa: E402
import re  # noqa: E402

def fix_adapter_files():
    """Fix adapter files to use BaseServiceAdapter instead of ServiceAdapter"""
    adapters = [
        'src/adapters/cloudflare-adapter.ts',
        'src/adapters/github-adapter.ts',
        'src/adapters/google-adapter.ts',
        'src/adapters/openai-adapter.ts'
    ]
    
    for adapter_file in adapters:
        if not os.path.exists(adapter_file):
            continue
            
        with open(adapter_file, 'r') as f:
            content = f.read()
        
        # Fix import
        content = content.replace(
            "import { ServiceAdapter } from '../core/service-adapter';",
            "import { BaseServiceAdapter } from '../core/service-adapter';"
        )
        
        # Fix class declaration - extend BaseServiceAdapter
        content = re.sub(
            r'export class (\w+) extends ServiceAdapter',
            r'export class \1 extends BaseServiceAdapter',
            content
        )
        
        with open(adapter_file, 'w') as f:
            f.write(content)
        
        print(f"Fixed {adapter_file}")

def fix_github_tools():
    """Fix GitHub tools.ts"""
    file_path = 'src/adapters/github/tools.ts'
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Process line by line
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Remove ToolFactory import
        if 'ToolFactory' in line and 'import' in line:
            line = line.replace(', ToolFactory', '')
        
        # Fix GitHubTool base class
        if 'abstract class GitHubTool<TInput, TOutput>' in line:
            line = line.replace(
                'abstract class GitHubTool<TInput, TOutput> extends Tool<TInput, TOutput>',
                'abstract class GitHubTool extends Tool'
            )
        
        # Fix GitHubListReposTool generic parameters
        if re.search(r'^\s*class\s+GitHubListReposTool\s+extends\s+GitHubTool\s*<', line):
            # Skip the generic parameter lines until we reach the closing '> {'
            i += 1
            while i < len(lines) and '> {' not in lines[i]:
                i += 1
            # Replace the entire generic class declaration with a non-generic one
            line = 'class GitHubListReposTool extends GitHubTool {\n'
            if i < len(lines):
                i += 1
        
        # Add override modifier to methods that need it
        if re.match(r'\s+getInputSchema\(\):', line):
            line = line.replace('getInputSchema():', 'override getInputSchema():')
        if re.match(r'\s+getOutputSchema\(\):', line):
            line = line.replace('getOutputSchema():', 'override getOutputSchema():')
        
        # Fix invoke method to be public
        if re.match(r'\s+protected async invoke\(', line):
            line = line.replace('protected async invoke(', 'async invoke(')
        
        # Remove inputSchema and outputSchema from tool descriptors
        if 'inputSchema:' in line or 'outputSchema:' in line:
            # Skip these lines
            i += 1
            continue
        
        # Fix ToolFactory type to proper function signature
        if 'factory: ToolFactory' in line:
            line = line.replace('factory: ToolFactory', 'factory: (credentialManager: any, config: any) => Tool')
        
        new_lines.append(line)
        i += 1
    
    with open(file_path, 'w') as f:
        f.writelines(new_lines)
    
    print(f"Fixed {file_path}")

if __name__ == "__main__":
    print("Starting comprehensive fix...")
    fix_adapter_files()
    fix_github_tools()
    print("Fix complete!")
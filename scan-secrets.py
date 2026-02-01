# @GL-governed
# @GL-layer: GL20-29
# @GL-semantic: python-module
# @GL-audit-trail: ../../engine/governance/gl-artifacts/meta/semantic/GL-ROOT-SEMANTIC-ANCHOR.yaml
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-enterprise-architecture/governance/engine/governance/gl-artifacts/meta/semantic/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-enterprise-architecture/governance/engine/governance/gl-artifacts/meta/naming-charter/gl-unified-naming-charter.yaml

#!/usr/bin/env python3
"""
Simple secret scanner to detect potential secrets in the codebase
"""
@GL-governed
import os
import re
from pathlib import Path

# Patterns to detect secrets
SECRET_PATTERNS = [
    (r'github_pat_[a-zA-Z0-9_]{36,}', 'GitHub Personal Access Token'),
    (r'ghp_[a-zA-Z0-9]{36}', 'GitHub Personal Access Token (classic)'),
    (r'gho_[a-zA-Z0-9]{36}', 'GitHub OAuth Token'),
    (r'ghu_[a-zA-Z0-9]{36}', 'GitHub User Token'),
    (r'ghs_[a-zA-Z0-9]{36}', 'GitHub Server Token'),
    (r'ghr_[a-zA-Z0-9]{36}', 'GitHub Refresh Token'),
    (r'xoxb-[a-zA-Z0-9-]+', 'Slack Bot Token'),
    (r'xoxp-[a-zA-Z0-9-]+', 'Slack User Token'),
    (r'AKIA[0-9A-Z]{16}', 'AWS Access Key'),
    (r'[0-9a-f]{32}', 'Potential API Key (32 hex)'),
    (r'[0-9a-f]{40}', 'Potential API Key (40 hex)'),
    (r'-----BEGIN [A-Z]+ PRIVATE KEY-----', 'Private Key'),
    (r'password\s*=\s*["\'][^"\']+["\']', 'Hardcoded Password'),
    (r'secret\s*=\s*["\'][^"\']+["\']', 'Hardcoded Secret'),
    (r'api[_-]?key\s*=\s*["\'][^"\']+["\']', 'Hardcoded API Key'),
    (r'token\s*=\s*["\'][^"\']+["\']', 'Hardcoded Token'),
]

# Directories to exclude
EXCLUDE_DIRS = [
    'node_modules',
    '.git',
    'dist',
    'build',
    'coverage',
    '.next',
    'outputs',
    'summarized_conversations',
    '.venv',
    'venv',
    '__pycache__',
]

# File extensions to scan
SCAN_EXTENSIONS = [
    '.ts', '.js', '.tsx', '.jsx',
    '.py',
    '.json', '.yaml', '.yml',
    '.md', '.txt',
    '.env', '.conf', '.config',
]

def should_scan_file(filepath):
    """Check if file should be scanned"""
    # Check extension
    if not any(filepath.suffix.lower() in ext for ext in SCAN_EXTENSIONS):
        return False
    
    # Check if in excluded directory
    for exclude_dir in EXCLUDE_DIRS:
        if exclude_dir in filepath.parts:
            return False
    
    return True

def scan_file(filepath):
    """Scan a single file for secrets"""
    findings = []
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
        
        for pattern, secret_type in SECRET_PATTERNS:
            for i, line in enumerate(lines, 1):
                matches = re.finditer(pattern, line)
                for match in matches:
                    # Filter out comments
                    stripped = line.strip()
                    if stripped.startswith('//') or stripped.startswith('#') or stripped.startswith('*'):
                        continue
                    
                    findings.append({
                        'line': i,
                        'type': secret_type,
                        'pattern': pattern,
                        'match': match.group(0)[:50] + '...' if len(match.group(0)) > 50 else match.group(0),
                    })
    except Exception as e:
        pass
    
    return findings

def scan_directory(root_dir):
    """Scan all files in directory"""
    root_path = Path(root_dir)
    all_findings = {}
    
    for filepath in root_path.rglob('*'):
        if filepath.is_file() and should_scan_file(filepath):
            findings = scan_file(filepath)
            if findings:
                relative_path = filepath.relative_to(root_path)
                all_findings[str(relative_path)] = findings
    
    return all_findings

def main():
    print("🔍 Scanning for potential secrets...\n")
    
    # Scan current directory
    findings = scan_directory('/workspace')
    
    # Generate report
    total_files = len(findings)
    total_findings = sum(len(f) for f in findings.values())
    
    print(f"📊 Scan Results:")
    print(f"   Files with findings: {total_files}")
    print(f"   Total findings: {total_findings}\n")
    
    if total_files == 0:
        print("✅ No potential secrets found!")
        return
    
    # Group by type
    type_counts = {}
    for filepath, file_findings in findings.items():
        for finding in file_findings:
            secret_type = finding['type']
            type_counts[secret_type] = type_counts.get(secret_type, 0) + 1
    
    print("📈 Findings by type:")
    for secret_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   {secret_type}: {count}")
    
    print("\n📝 Detailed findings:")
    for filepath, file_findings in findings.items():
        print(f"\n📄 {filepath}")
        for finding in file_findings[:3]:  # Show first 3 findings per file
            print(f"   Line {finding['line']}: {finding['type']}")
            print(f"      Match: {finding['match']}")
        if len(file_findings) > 3:
            print(f"   ... and {len(file_findings) - 3} more")
    
    print(f"\n⚠️  Found {total_findings} potential secrets across {total_files} files.")
    print("   Please review and redact any actual secrets.")

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
Quick scan for external dependencies in configuration files only.
"""

import re
from pathlib import Path

# Key files to check
KEY_FILES = [
    'package.json',
    'package-lock.json',
    'requirements.txt',
    'Pipfile',
    'setup.py',
    'pom.xml',
    'build.gradle',
    'Dockerfile',
    'docker-compose.yml',
    '.github/workflows/*.yml',
    '.github/workflows/*.yaml',
]

# External patterns to detect
PATTERNS = {
    'npm_registry': r'(?:https?://)?(?:www\.)?npmjs\.com',
    'npm_packages': r'"[^"]+@[^"]+"\s*:',
    'pip_packages': r'^[a-zA-Z0-9_-]+[><=~]+',
    'docker_images': r'(?:docker|ghcr|quay|k8s\.gcr|gcr)\.io/[^\s:]+(?::\d+)?',
    'github_actions': r'uses:\s*[a-z0-9-]+/[a-z0-9-]+@[a-z0-9]+',
    'external_urls': r'https?://(?:registry|api|cdn|www)\.[a-z0-9.-]+\.[a-z]{2,}',
}

def scan_file(file_path):
    """Scan a single file for dependencies."""
    results = {}
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        for name, pattern in PATTERNS.items():
            matches = re.findall(pattern, content, re.MULTILINE)
            if matches:
                results[name] = matches
        
    except Exception as e:
        pass
    
    return results

def main():
    """Main function."""
    root_dir = Path("/workspace/machine-native-ops")
    
    print("Quick Dependency Scan")
    print("=" * 60)
    
    all_results = {}
    
    # Check specific file types
    for pattern in KEY_FILES:
        for file_path in root_dir.rglob(pattern):
            if file_path.is_file():
                results = scan_file(file_path)
                if results:
                    all_results[str(file_path.relative_to(root_dir))] = results
    
    # Check YAML files in common directories
    yaml_dirs = [
        root_dir / '.github/workflows',
        root_dir / 'gov-platform-services/quantum-platform',
    ]
    
    for yaml_dir in yaml_dirs:
        if yaml_dir.exists():
            for file_path in yaml_dir.rglob('*.yaml'):
                results = scan_file(file_path)
                if results:
                    all_results[str(file_path.relative_to(root_dir))] = results
            for file_path in yaml_dir.rglob('*.yml'):
                results = scan_file(file_path)
                if results:
                    all_results[str(file_path.relative_to(root_dir))] = results
    
    # Print results
    print(f"\nFiles with external dependencies: {len(all_results)}")
    
    for file_path, deps in all_results.items():
        print(f"\n{file_path}:")
        for dep_type, matches in deps.items():
            print(f"  {dep_type}: {len(matches)} matches")
            for match in matches[:3]:
                print(f"    - {str(match)[:80]}")
    
    # Summary
    total_deps = sum(len(deps) for deps in all_results.values())
    print(f"\nTotal dependencies found: {total_deps}")
    
    # Save results
    output_file = root_dir / "quick_dependency_scan_results.txt"
    with open(output_file, 'w') as f:
        f.write("Quick Dependency Scan Results\n")
        f.write("=" * 60 + "\n\n")
        for file_path, deps in all_results.items():
            f.write(f"{file_path}:\n")
            for dep_type, matches in deps.items():
                f.write(f"  {dep_type}:\n")
                for match in matches:
                    f.write(f"    - {str(match)}\n")
            f.write("\n")
    
    print(f"\nResults saved to: {output_file}")

if __name__ == "__main__":
    main()
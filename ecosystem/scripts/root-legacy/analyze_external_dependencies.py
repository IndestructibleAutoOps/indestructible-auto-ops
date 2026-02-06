#!/usr/bin/env python3
"""
Analyze and identify all external dependencies, mappings, and references in the project.
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Set
import json

# External dependency patterns
EXTERNAL_PATTERNS = {
    'registry': [
        r'https?://(?:registry|npmjs|pypi|maven)\.io',
        r'https?://(?:www\.)?github\.com/[^/]+/[^/]+',
        r'(?:npm|pip|pypi|maven)\s+install',
    ],
    'container_registry': [
        r'(?:docker|ghcr|quay|k8s\.gcr|gcr)\.io/[^\s]+',
        r'registry:\s*["\']?(?:docker|ghcr|quay|k8s\.gcr|gcr)\.io',
    ],
    'cdn': [
        r'(?:cdnjs|jsdelivr|unpkg)\.cloudflare\.com',
        r'(?:ajax\.googleapis\.com)',
    ],
    'api_endpoint': [
        r'https?://api\.',
        r'https?://[a-z]+\.api\.',
    ],
    'package_manager': [
        r'(?:pip install|npm install|yarn add|maven)',
        r'(?:requirements\.txt|package\.json|pom\.xml)',
    ],
    'cloud_services': [
        r'(?:aws\.amazon|azure|cloud\.google)\.com',
        r'(?:s3|ec2|rds)\.amazonaws\.com',
        r'(?:storage\.googleapis|blob\.core\.windows)\.net',
    ],
    'monitoring': [
        r'(?:prometheus|grafana|datadog)\.io',
        r'(?:newrelic|splunkd)\.com',
    ],
    'documentation': [
        r'(?:docs\.[a-z]+\.com|readthedocs\.io)',
    ],
}

class DependencyAnalyzer:
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.dependencies = {
            'files': [],
            'by_type': {},
            'by_file': {}
        }
    
    def analyze_file(self, file_path: Path) -> Dict:
        """Analyze a single file for external dependencies."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            dependencies = {
                'file': str(file_path.relative_to(self.root_dir)),
                'file_type': file_path.suffix,
                'dependencies': []
            }
            
            for dep_type, patterns in EXTERNAL_PATTERNS.items():
                for pattern in patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        dependency = {
                            'type': dep_type,
                            'pattern': match.group(),
                            'line': content[:match.start()].count('\n') + 1,
                            'start': match.start(),
                            'end': match.end()
                        }
                        dependencies['dependencies'].append(dependency)
            
            return dependencies
            
        except Exception as e:
            return {
                'file': str(file_path.relative_to(self.root_dir)),
                'error': str(e),
                'dependencies': []
            }
    
    def scan_directory(self) -> Dict:
        """Scan all files in the directory."""
        file_extensions = {'.md', '.yaml', '.yml', '.json', '.py', '.js', '.ts', '.sh', '.txt'}
        
        for file_path in self.root_dir.rglob('*'):
            if file_path.is_file() and file_path.suffix in file_extensions:
                file_deps = self.analyze_file(file_path)
                
                if file_deps['dependencies']:
                    self.dependencies['files'].append(file_deps)
                    self.dependencies['by_file'][str(file_deps['file'])] = file_deps
                    
                    for dep in file_deps['dependencies']:
                        dep_type = dep['type']
                        if dep_type not in self.dependencies['by_type']:
                            self.dependencies['by_type'][dep_type] = []
                        self.dependencies['by_type'][dep_type].append({
                            'file': file_deps['file'],
                            'pattern': dep['pattern'],
                            'line': dep['line']
                        })
        
        return self.dependencies
    
    def generate_report(self) -> str:
        """Generate a comprehensive dependency report."""
        report = []
        
        report.append("=" * 80)
        report.append("EXTERNAL DEPENDENCY ANALYSIS REPORT")
        report.append("=" * 80)
        report.append("")
        
        # Summary
        report.append("## SUMMARY")
        report.append(f"Total files scanned: {len(list(self.root_dir.rglob('*')))}")
        report.append(f"Files with dependencies: {len(self.dependencies['files'])}")
        report.append(f"Total dependencies found: {sum(len(f['dependencies']) for f in self.dependencies['files'])}")
        report.append("")
        
        # By type
        report.append("## DEPENDENCIES BY TYPE")
        for dep_type, deps in self.dependencies['by_type'].items():
            report.append(f"\n### {dep_type.upper()}")
            report.append(f"Count: {len(deps)}")
            
            # Show first 10 examples
            for dep in deps[:10]:
                report.append(f"  - {dep['file']}:{dep['line']} - {dep['pattern'][:100]}")
            
            if len(deps) > 10:
                report.append(f"  ... and {len(deps) - 10} more")
        
        # Detailed file list
        report.append("\n## DETAILED FILE LIST")
        for file_data in self.dependencies['files']:
            report.append(f"\n### {file_data['file']}")
            report.append(f"File type: {file_data['file_type']}")
            report.append(f"Dependencies: {len(file_data['dependencies'])}")
            
            for dep in file_data['dependencies'][:5]:
                report.append(f"  Line {dep['line']}: [{dep['type']}] {dep['pattern'][:100]}")
            
            if len(file_data['dependencies']) > 5:
                report.append(f"  ... and {len(file_data['dependencies']) - 5} more")
        
        return "\n".join(report)

def main():
    """Main function."""
    root_dir = "/workspace/machine-native-ops"
    
    analyzer = DependencyAnalyzer(root_dir)
    dependencies = analyzer.scan_directory()
    
    # Generate report
    report = analyzer.generate_report()
    
    # Save report
    report_file = Path(root_dir) / "external_dependencies_analysis_report.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # Save JSON data
    json_file = Path(root_dir) / "external_dependencies_analysis.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(dependencies, f, indent=2)
    
    print(f"Analysis complete!")
    print(f"Report saved to: {report_file}")
    print(f"JSON data saved to: {json_file}")
    print(f"\nTotal dependencies found: {len(dependencies['files'])}")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""GL File Scanner for Governance Alignment Analysis"""
import os
import re
from pathlib import Path
from collections import defaultdict
import json

class GLFileScanner:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.results = {
            'total_files': 0,
            'by_type': defaultdict(int),
            'by_gl_compliance': defaultdict(int),
            'files_needing_adjustment': [],
            'compliance_stats': {
                'with_governed_marker': 0,
                'with_layer_marker': 0,
                'with_semantic_marker': 0,
                'with_audit_trail': 0,
                'fully_compliant': 0
            }
        }
    
    def scan_file(self, file_path):
        """Scan a single file for GL compliance"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except:
            return None
        
        # Check for GL markers
        has_governed = '@GL-governed' in content
        has_layer = '@GL-layer:' in content
        has_semantic = '@GL-semantic:' in content
        has_audit_trail = '@GL-audit-trail:' in content
        
        rel_path = str(file_path.relative_to(self.base_path))
        
        file_info = {
            'path': rel_path,
            'size': os.path.getsize(file_path),
            'has_governed_marker': has_governed,
            'has_layer_marker': has_layer,
            'has_semantic_marker': has_semantic,
            'has_audit_trail': has_audit_trail,
            'fully_compliant': all([has_governed, has_layer, has_semantic, has_audit_trail])
        }
        
        return file_info
    
    def scan_all(self):
        """Scan all relevant files"""
        file_patterns = ['*.py', '*.js', '*.ts', '*.yaml', '*.yml', '*.json', '*.md']
        exclude_dirs = ['node_modules', '.git', 'archives', '__pycache__']
        
        for pattern in file_patterns:
            for file_path in self.base_path.rglob(pattern):
                # Skip excluded directories
                if any(exclude_dir in file_path.parts for exclude_dir in exclude_dirs):
                    continue
                
                # Scan file
                file_info = self.scan_file(file_path)
                if not file_info:
                    continue
                
                self.results['total_files'] += 1
                self.results['by_type'][file_path.suffix] += 1
                
                # Update compliance stats
                if file_info['has_governed_marker']:
                    self.results['compliance_stats']['with_governed_marker'] += 1
                if file_info['has_layer_marker']:
                    self.results['compliance_stats']['with_layer_marker'] += 1
                if file_info['has_semantic_marker']:
                    self.results['compliance_stats']['with_semantic_marker'] += 1
                if file_info['has_audit_trail']:
                    self.results['compliance_stats']['with_audit_trail'] += 1
                if file_info['fully_compliant']:
                    self.results['compliance_stats']['fully_compliant'] += 1
                    self.results['by_gl_compliance']['fully_compliant'] += 1
                else:
                    self.results['files_needing_adjustment'].append(file_info)
                    self.results['by_gl_compliance']['needs_adjustment'] += 1
        
        return self.results
    
    def infer_gl_layer_from_path(self, path_str):
        """Infer GL layer from file path"""
        if 'semantic_engine' in path_str or 'governance' in path_str or '.governance' in path_str:
            return 'GL90-99'
        elif 'engine' in path_str and 'semantic' not in path_str:
            return 'GL30-49'
        elif 'algorithm' in path_str:
            return 'GL40-49'
        elif 'data' in path_str or 'etl' in path_str:
            return 'GL20-29'
        else:
            return 'GL00-09'
    
    def infer_semantic_type(self, path_str):
        """Infer semantic type from file path"""
        if 'semantic_engine' in path_str:
            return 'semantic-engine'
        elif 'test' in path_str:
            return 'test'
        elif 'naming' in path_str:
            return 'naming-governance'
        elif 'governance' in path_str:
            return 'governance-core'
        elif 'script' in path_str:
            return 'execution-script'
        else:
            return 'general-component'
    
    def generate_adjustment_suggestions(self):
        """Generate adjustment suggestions for non-compliant files"""
        suggestions = []
        
        for file_info in self.results['files_needing_adjustment']:
            path_str = file_info['path']
            path_obj = Path(path_str)
            suffix = path_obj.suffix
            
            # Infer GL layer and semantic
            gl_layer = self.infer_gl_layer_from_path(path_str)
            semantic_type = self.infer_semantic_type(path_str)
            
            # Generate suggested name
            base_name = path_obj.stem
            if suffix == '.py':
                # Python files
                suggested_name = f"{gl_layer}-{semantic_type}-{base_name}.py"
            elif suffix in ['.yaml', '.yml']:
                # YAML files
                suggested_name = f"{gl_layer}-{semantic_type}-{base_name}.yaml"
            elif suffix == '.json':
                # JSON files
                suggested_name = f"{gl_layer}-{semantic_type}-{base_name}.json"
            elif suffix == '.md':
                # Markdown files
                suggested_name = f"{gl_layer}-{semantic_type}-{base_name}.md"
            else:
                suggested_name = path_obj.name
            
            suggestion = {
                'current_path': file_info['path'],
                'suggested_name': suggested_name,
                'gl_layer': gl_layer,
                'semantic_type': semantic_type,
                'compliance_issues': [],
                'required_markers': [
                    '@GL-governed',
                    f'@GL-layer: {gl_layer}',
                    f'@GL-semantic: {semantic_type}',
                    '@GL-audit-trail: [audit_path]'
                ]
            }
            
            # Identify compliance issues
            if not file_info['has_governed_marker']:
                suggestion['compliance_issues'].append('Missing @GL-governed marker')
            if not file_info['has_layer_marker']:
                suggestion['compliance_issues'].append('Missing @GL-layer marker')
            if not file_info['has_semantic_marker']:
                suggestion['compliance_issues'].append('Missing @GL-semantic marker')
            if not file_info['has_audit_trail']:
                suggestion['compliance_issues'].append('Missing @GL-audit-trail marker')
            
            suggestions.append(suggestion)
        
        return suggestions

def main():
    base_path = Path('/workspace/machine-native-ops')
    scanner = GLFileScanner(base_path)
    
    print("=== GL File Scanner Starting ===")
    print(f"Base path: {base_path}")
    print()
    
    # Scan all files
    results = scanner.scan_all()
    
    # Generate suggestions
    suggestions = scanner.generate_adjustment_suggestions()
    
    # Save results
    output = {
        'scan_summary': {
            'total_files': results['total_files'],
            'files_needing_adjustment': len(results['files_needing_adjustment']),
            'compliance_rate': f"{(results['compliance_stats']['fully_compliant'] / results['total_files'] * 100):.2f}%"
        },
        'compliance_stats': results['compliance_stats'],
        'files_by_type': dict(results['by_type']),
        'adjustment_suggestions': suggestions[:1000]  # Limit to first 1000 for performance
    }
    
    with open('/workspace/scan_results.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Scan complete:")
    print(f"  Total files: {results['total_files']}")
    print(f"  Fully compliant: {results['compliance_stats']['fully_compliant']}")
    print(f"  Needs adjustment: {len(results['files_needing_adjustment'])}")
    print(f"  Compliance rate: {(results['compliance_stats']['fully_compliant'] / results['total_files'] * 100):.2f}%")
    print(f"\nResults saved to: /workspace/scan_results.json")

if __name__ == '__main__':
    main()

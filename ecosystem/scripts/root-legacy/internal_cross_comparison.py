import os
import yaml
import json
import re
from pathlib import Path
from collections import defaultdict

def load_yaml_file(filepath):
    """Load YAML file content"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

def analyze_directory_patterns(root_path):
    """Analyze directory naming patterns"""
    patterns = defaultdict(list)
    
    for root, dirs, files in os.walk(root_path):
        for dir_name in dirs:
            # Check if it follows GL naming conventions
            if dir_name.startswith('gl-'):
                pattern = re.match(r'gl-([a-z]+)-([a-z]+)-?(platform|service|module|app)?', dir_name)
                if pattern:
                    domain = pattern.group(1)
                    capability = pattern.group(2)
                    resource_type = pattern.group(3) or 'unknown'
                    patterns[f"{domain}-{capability}-{resource_type}"].append(dir_name)
    
    return patterns

def analyze_naming_conventions(naming_file):
    """Analyze naming conventions from file"""
    conventions = load_yaml_file(naming_file)
    if not conventions:
        return {}
    
    analysis = {
        'total_conventions': len(conventions.get('spec', {}).get('conventions', {})),
        'convention_types': list(conventions.get('spec', {}).get('conventions', {}).keys()),
        'enforcement_level': conventions.get('metadata', {}).get('enforcement'),
        'governance_level': conventions.get('metadata', {}).get('governance_level')
    }
    
    return analysis

def analyze_governance_files(root_path):
    """Find and analyze all governance files"""
    governance_files = []
    
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith('.yaml') and ('governance' in root or 'naming' in root):
                filepath = os.path.join(root, file)
                governance_files.append({
                    'path': filepath,
                    'size': os.path.getsize(filepath)
                })
    
    return governance_files

def identify_inconsistencies():
    """Identify naming inconsistencies across the repository"""
    inconsistencies = []
    
    # Check for naming violations
    for root, dirs, files in os.walk('/workspace/machine-native-ops'):
        for dir_name in dirs:
            # Check GL naming violations
            if (dir_name.startswith('gl-') or dir_name.startswith('GL_')) and \
               ('_' in dir_name or ' ' in dir_name):
                inconsistencies.append({
                    'type': 'naming_violation',
                    'path': os.path.join(root, dir_name),
                    'issue': 'Invalid characters in GL-named directory'
                })
    
    return inconsistencies

def extract_governance_patterns():
    """Extract governance patterns from architecture files"""
    patterns = []
    
    governance_dirs = [
        '/workspace/machine-native-ops/.github/governance',
        '/workspace/machine-native-ops/gl-platform/governance'
    ]
    
    for gov_dir in governance_dirs:
        if os.path.exists(gov_dir):
            for root, dirs, files in os.walk(gov_dir):
                for file in files:
                    if file.endswith('.yaml'):
                        filepath = os.path.join(root, file)
                        content = load_yaml_file(filepath)
                        if content:
                            patterns.append({
                                'file': file,
                                'path': filepath,
                                'kind': content.get('kind', 'unknown'),
                                'api_version': content.get('apiVersion', 'unknown')
                            })
    
    return patterns

def generate_internal_report():
    """Generate comprehensive internal comparison report"""
    report = {
        'timestamp': '2026-01-31T00:00:00Z',
        'analysis_phase': 'internal_repository_cross_comparison',
        'findings': {}
    }
    
    # 1. Directory pattern analysis
    print("Analyzing directory patterns...")
    patterns = analyze_directory_patterns('/workspace/machine-native-ops')
    report['findings']['directory_patterns'] = {
        'total_patterns_found': len(patterns),
        'sample_patterns': dict(list(patterns.items())[:10])
    }
    
    # 2. Naming conventions analysis
    print("Analyzing naming conventions...")
    naming_file = '/workspace/machine-native-ops/gl-platform/governance/naming-governance/contracts/naming-conventions.yaml'
    conventions = analyze_naming_conventions(naming_file)
    report['findings']['naming_conventions'] = conventions
    
    # 3. Governance files analysis
    print("Analyzing governance files...")
    gov_files = analyze_governance_files('/workspace/machine-native-ops')
    report['findings']['governance_files'] = {
        'total_files': len(gov_files),
        'sample_files': gov_files[:20]
    }
    
    # 4. Inconsistency detection
    print("Detecting inconsistencies...")
    inconsistencies = identify_inconsistencies()
    report['findings']['inconsistencies'] = inconsistencies
    
    # 5. Governance patterns extraction
    print("Extracting governance patterns...")
    gov_patterns = extract_governance_patterns()
    report['findings']['governance_patterns'] = gov_patterns
    
    # 6. Statistics
    print("Calculating statistics...")
    report['findings']['statistics'] = {
        'gl_prefixed_directories': len([d for r, dirs, files in os.walk('/workspace/machine-native-ops') 
                                       for d in dirs if d.startswith('gl-')]),
        'governance_yaml_files': len([f for r, d, files in os.walk('/workspace/machine-native-ops/.github/governance') 
                                      for f in files if f.endswith('.yaml')]),
        'platform_directories': len([d for r, dirs, files in os.walk('/workspace/machine-native-ops')
                                    for d in dirs if d.endswith('-platform')])
    }
    
    return report

if __name__ == '__main__':
    report = generate_internal_report()
    
    # Save report
    with open('/workspace/internal_cross_comparison_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*80)
    print("INTERNAL CROSS-COMPARISON REPORT GENERATED")
    print("="*80)
    print(f"\nReport saved to: /workspace/internal_cross_comparison_report.json")
    print(f"\nKey Findings:")
    print(f"  - Directory patterns found: {report['findings']['directory_patterns']['total_patterns_found']}")
    print(f"  - Naming conventions analyzed: {report['findings']['naming_conventions'].get('total_conventions', 0)}")
    print(f"  - Governance files found: {report['findings']['governance_files']['total_files']}")
    print(f"  - Inconsistencies detected: {len(report['findings']['inconsistencies'])}")
    print(f"  - Governance patterns extracted: {len(report['findings']['governance_patterns'])}")
    print(f"\nStatistics:")
    print(f"  - GL-prefixed directories: {report['findings']['statistics']['gl_prefixed_directories']}")
    print(f"  - Governance YAML files: {report['findings']['statistics']['governance_yaml_files']}")
    print(f"  - Platform directories: {report['findings']['statistics']['platform_directories']}")
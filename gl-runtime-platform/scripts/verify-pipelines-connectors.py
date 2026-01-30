#!/usr/bin/env python3
"""
Verify all pipelines and connectors in the GL Runtime Platform
"""
@GL-governed
import os
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Define pipelines to verify
PIPELINES = {
    'src/infinite-continuum-server.ts': {
        'type': 'server',
        'description': 'Infinite Continuum Server',
        'required_imports': ['express']
    },
    'src/infinite-continuum/index.ts': {
        'type': 'continuum',
        'description': 'Infinite Learning Continuum',
        'required_exports': ['KnowledgeAccretion', 'SemanticReformation', 'AlgorithmicEvolution', 'InfiniteComposition', 'FabricExpansion', 'ContinuumMemory']
    }
}

# Define connectors to verify
CONNECTORS = {
    'src/connectors/git-connector.ts': {
        'type': 'git',
        'description': 'Git Connector',
        'required_classes': ['GitConnector']
    }
}

def verify_file_exists(filepath: Path) -> bool:
    """Check if file exists"""
    return filepath.exists() and filepath.is_file()

def verify_file_readable(filepath: Path) -> bool:
    """Check if file is readable"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            f.read()
        return True
    except Exception:
        return False

def verify_typescript_imports(filepath: Path, imports: List[str]) -> Tuple[bool, List[str]]:
    """Verify TypeScript imports"""
    missing = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        for imp in imports:
            if imp not in content:
                missing.append(imp)
        return (len(missing) == 0, missing)
    except Exception as e:
        return (False, [f"Error reading file: {e}"])

def verify_typescript_exports(filepath: Path, exports: List[str]) -> Tuple[bool, List[str]]:
    """Verify TypeScript exports"""
    missing = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        for exp in exports:
            if exp not in content:
                missing.append(exp)
        return (len(missing) == 0, missing)
    except Exception as e:
        return (False, [f"Error reading file: {e}"])

def verify_python_classes(filepath: Path, classes: List[str]) -> Tuple[bool, List[str]]:
    """Verify Python classes"""
    missing = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        for cls in classes:
            if f'class {cls}' not in content:
                missing.append(cls)
        return (len(missing) == 0, missing)
    except Exception as e:
        return (False, [f"Error reading file: {e}"])

def verify_pipeline(filepath: Path, config: Dict) -> Dict:
    """Verify a single pipeline"""
    result = {
        'file': str(filepath.relative_to(BASE_DIR)),
        'description': config['description'],
        'exists': False,
        'readable': False,
        'verified': False,
        'issues': []
    }
    
    # Check file exists
    if not verify_file_exists(filepath):
        result['issues'].append('File does not exist')
        return result
    
    result['exists'] = True
    
    # Check file readable
    if not verify_file_readable(filepath):
        result['issues'].append('File is not readable')
        return result
    
    result['readable'] = True
    
    # Verify based on type
    if filepath.suffix == '.ts':
        if 'required_imports' in config:
            verified, missing = verify_typescript_imports(filepath, config['required_imports'])
            if not verified:
                result['issues'].append(f'Missing imports: {", ".join(missing)}')
        
        if 'required_exports' in config:
            verified, missing = verify_typescript_exports(filepath, config['required_exports'])
            if not verified:
                result['issues'].append(f'Missing exports: {", ".join(missing)}')
    
    elif filepath.suffix == '.py':
        if 'required_classes' in config:
            verified, missing = verify_python_classes(filepath, config['required_classes'])
            if not verified:
                result['issues'].append(f'Missing classes: {", ".join(missing)}')
    
    result['verified'] = len(result['issues']) == 0
    return result

def verify_connector(filepath: Path, config: Dict) -> Dict:
    """Verify a single connector"""
    return verify_pipeline(filepath, config)

def main():
    print("🔍 Verifying Pipelines and Connectors...\n")
    
    all_results = []
    
    # Verify pipelines
    print("📦 Verifying Pipelines:")
    pipeline_results = []
    for rel_path, config in PIPELINES.items():
        filepath = BASE_DIR / rel_path
        result = verify_pipeline(filepath, config)
        pipeline_results.append(result)
        all_results.append(result)
        
        status = "✅" if result['verified'] else "❌"
        print(f"  {status} {result['description']}")
        if result['issues']:
            for issue in result['issues']:
                print(f"      - {issue}")
    
    # Verify connectors
    print("\n🔌 Verifying Connectors:")
    connector_results = []
    for rel_path, config in CONNECTORS.items():
        filepath = BASE_DIR / rel_path
        result = verify_connector(filepath, config)
        connector_results.append(result)
        all_results.append(result)
        
        status = "✅" if result['verified'] else "❌"
        print(f"  {status} {result['description']}")
        if result['issues']:
            for issue in result['issues']:
                print(f"      - {issue}")
    
    # Summary
    print("\n📊 Summary:")
    total = len(all_results)
    verified = sum(1 for r in all_results if r['verified'])
    print(f"  Total Components: {total}")
    print(f"  Verified: {verified}")
    print(f"  Failed: {total - verified}")
    print(f"  Pass Rate: {(verified/total*100):.1f}%")
    
    # Generate report
    report = {
        'timestamp': str(Path(__file__).stat().st_mtime),
        'total_components': total,
        'verified_components': verified,
        'failed_components': total - verified,
        'pass_rate': verified/total,
        'pipelines': pipeline_results,
        'connectors': connector_results
    }
    
    # Save report
    report_path = BASE_DIR / 'test-reports' / 'pipelines-connectors-verification.json'
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Report saved to: {report_path.relative_to(BASE_DIR)}")
    
    # Exit code
    if verified == total:
        print("\n✅ All pipelines and connectors verified successfully!")
        return 0
    else:
        print(f"\n❌ {total - verified} component(s) failed verification")
        return 1

if __name__ == '__main__':
    sys.exit(main())
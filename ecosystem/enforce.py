#!/usr/bin/env python3
# @GL-semantic: org.mnga.enforce@1.0.0
# @GL-audit-trail: enabled
"""
MNGA Governance Enforcement Script

This script provides comprehensive governance enforcement for the MachineNativeOps
ecosystem, including validation, refresh, and reverse architecture analysis.
"""

import sys
import os
import importlib.util
from datetime import datetime

# Load modules directly from file paths
def load_module_from_file(module_name, file_path):
    """Load a Python module from a file path"""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load engines
validation_engine_path = os.path.join(script_dir, 'governance', 'engines', 'validation', 'validation_engine.py')
refresh_engine_path = os.path.join(script_dir, 'governance', 'engines', 'refresh', 'refresh_engine.py')
reverse_arch_engine_path = os.path.join(script_dir, 'governance', 'engines', 'reverse-architecture', 'reverse_architecture_engine.py')

ValidationEngine = load_module_from_file('validation_engine', validation_engine_path).ValidationEngine
RefreshEngine = load_module_from_file('refresh_engine', refresh_engine_path).RefreshEngine
ReverseArchitectureEngine = load_module_from_file('reverse_architecture_engine', reverse_arch_engine_path).ReverseArchitectureEngine


def print_header(title: str) -> None:
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def print_section(title: str) -> None:
    """Print a formatted section header"""
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print(f"{'─' * 60}\n")


def main():
    """Main entry point for governance enforcement"""
    # Get the parent directory of ecosystem (the actual workspace root)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(script_dir)
    
    print_header("MNGA Governance Enforcement")
    print(f"Workspace: {workspace_root}")
    print(f"Timestamp: {datetime.utcnow().isoformat() + 'Z'}")
    
    # Parse command line arguments
    command = sys.argv[1] if len(sys.argv) > 1 else "all"
    
    success = True
    
    if command in ["all", "validate"]:
        print_section("Running Validation Engine")
        validator = ValidationEngine(workspace_root=workspace_root)
        validation_result = validator.validate_all()
        
        if not validation_result.success:
            success = False
            print("\n⚠️  Validation failed with errors")
        else:
            print("\n✓ Validation passed")
    
    if command in ["all", "refresh"]:
        print_section("Running Refresh Engine")
        refresher = RefreshEngine(workspace_root=workspace_root)
        refresh_result = refresher.refresh_all()
        
        if not refresh_result.success:
            success = False
            print("\n⚠️  Refresh completed with errors")
        else:
            print("\n✓ Refresh completed successfully")
    
    if command in ["all", "analyze"]:
        print_section("Running Reverse Architecture Engine")
        analyzer = ReverseArchitectureEngine(workspace_root=workspace_root)
        analysis_result = analyzer.analyze()
        
        print("\n✓ Architecture analysis completed")
        print(f"  Components: {len(analysis_result.components)}")
        print(f"  Layers: {len(analysis_result.layers)}")
    
    # Final summary
    print_header("Enforcement Summary")
    if success:
        print("✓ All enforcement operations completed successfully")
        return 0
    else:
        print("✗ Enforcement completed with errors")
        return 1


if __name__ == "__main__":
    exit(main())
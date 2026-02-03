#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: shared-utilities
# @GL-audit-trail: ./governance/GL_SEMANTIC_ANCHOR.json
#
"""
Shared Utilities
================
GL Layer: GL90-99 Meta-Specification Layer

Common utility functions shared across the ecosystem.

Features:
- Base path detection
- Common path utilities
- Project structure helpers
"""

from pathlib import Path
from typing import Optional


def detect_project_root(start_path: Optional[Path] = None) -> str:
    """
    Auto-detect project root by looking for key marker files.
    
    Searches upward from the start_path for:
    1. governance-manifest.yaml (primary marker)
    2. ecosystem/enforce.py (secondary marker)
    
    Args:
        start_path: Starting path for search (defaults to current file's parent)
        
    Returns:
        String path to project root
    """
    if start_path is None:
        start_path = Path(__file__).parent
    
    current = start_path if isinstance(start_path, Path) else Path(start_path)
    
    while current != current.parent:
        # Check for primary marker
        if (current / "governance-manifest.yaml").exists():
            return str(current)
        
        # Check for secondary marker
        if (current / "ecosystem").exists() and (current / "ecosystem" / "enforce.py").exists():
            return str(current)
        
        current = current.parent
    
    # Fallback to parent of ecosystem directory
    # Assuming this file is at ecosystem/utils/path_utils.py
    return str(Path(__file__).parent.parent.parent)


def get_ecosystem_root(project_root: Optional[str] = None) -> Path:
    """
    Get the ecosystem directory path.
    
    Args:
        project_root: Optional project root path
        
    Returns:
        Path to ecosystem directory
    """
    if project_root is None:
        project_root = detect_project_root()
    
    return Path(project_root) / "ecosystem"


def get_logs_dir(project_root: Optional[str] = None) -> Path:
    """
    Get the logs directory path, creating it if necessary.
    
    Args:
        project_root: Optional project root path
        
    Returns:
        Path to logs directory
    """
    ecosystem_root = get_ecosystem_root(project_root)
    logs_dir = ecosystem_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    return logs_dir


def get_audit_logs_dir(project_root: Optional[str] = None) -> Path:
    """
    Get the audit logs directory path, creating it if necessary.
    
    Args:
        project_root: Optional project root path
        
    Returns:
        Path to audit logs directory
    """
    logs_dir = get_logs_dir(project_root)
    audit_logs_dir = logs_dir / "audit-logs"
    audit_logs_dir.mkdir(parents=True, exist_ok=True)
    return audit_logs_dir


def get_contracts_dir(project_root: Optional[str] = None) -> Path:
    """
    Get the contracts directory path.
    
    Args:
        project_root: Optional project root path
        
    Returns:
        Path to contracts directory
    """
    ecosystem_root = get_ecosystem_root(project_root)
    return ecosystem_root / "contracts"


def get_governance_dir(project_root: Optional[str] = None) -> Path:
    """
    Get the governance directory path.
    
    Args:
        project_root: Optional project root path
        
    Returns:
        Path to governance directory
    """
    ecosystem_root = get_ecosystem_root(project_root)
    return ecosystem_root / "governance"


# Aliases for backward compatibility
def get_base_path(start_path: Optional[Path] = None) -> str:
    """Alias for detect_project_root for backward compatibility."""
    return detect_project_root(start_path)


if __name__ == "__main__":
    # Demo usage
    print("Path Utilities Demo")
    print("=" * 50)
    
    project_root = detect_project_root()
    print(f"Project Root: {project_root}")
    print(f"Ecosystem Root: {get_ecosystem_root()}")
    print(f"Logs Dir: {get_logs_dir()}")
    print(f"Audit Logs Dir: {get_audit_logs_dir()}")
    print(f"Contracts Dir: {get_contracts_dir()}")
    print(f"Governance Dir: {get_governance_dir()}")

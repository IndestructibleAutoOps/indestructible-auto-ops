# Ecosystem Utils Package
# GL Layer: GL90-99 Meta-Specification Layer

from .path_utils import (
    detect_project_root,
    get_ecosystem_root,
    get_logs_dir,
    get_audit_logs_dir,
    get_contracts_dir,
    get_governance_dir,
    get_base_path
)

__all__ = [
    "detect_project_root",
    "get_ecosystem_root",
    "get_logs_dir",
    "get_audit_logs_dir",
    "get_contracts_dir",
    "get_governance_dir",
    "get_base_path"
]

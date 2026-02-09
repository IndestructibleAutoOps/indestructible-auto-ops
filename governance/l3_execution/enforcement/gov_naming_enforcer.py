#!/usr/bin/env python3
"""
命名規範執行器
Naming Convention Enforcer
"""

import re
from pathlib import Path
from typing import List, Optional


class GovNamingEnforcer:
    FILE_PATTERN = r"^([a-z][a-z0-9_]*\.(py|yaml|json|md|txt)|README\.md|__init__\.py)$"
    DIR_PATTERN = r"^[a-z][a-z0-9_-]*$"
    FORBIDDEN_PREFIXES = ["ng_", "gl_"]
    ALLOWED_PREFIXES = ["gov_", "gov_naming_"]
    ALLOWED_DIR_PREFIXES = ["gov_", "gov_naming_", "l0_", "l1_", "l2_", "l3_", "l4_", "l5_", "l6_", "l7_", "l8_", "l9_"]
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)

    def scan_project(self) -> List[dict]:
        violations = []
        for path in self.project_root.rglob("*"):
            # Skip hidden files, .git, and __pycache__ directories
            if ".git" in str(path) or path.name.startswith(".") or "__pycache__" in str(path):
                continue
            
            if path.is_file():
                v = self.check_file_naming(path)
                if v:
                    violations.append(v)
            elif path.is_dir():
                v = self.check_directory_naming(path)
                if v:
                    violations.append(v)
        return violations

    def check_file_naming(self, file_path: Path) -> Optional[dict]:
        # Check for deprecated prefixes
        for prefix in self.FORBIDDEN_PREFIXES:
            if file_path.name.startswith(prefix):
                return {
                    "asset_id": str(file_path.relative_to(self.project_root)),
                    "violation_id": "NAMING-DEPRECATED-001",
                    "severity": "BLOCKER",
                    "description": f"使用已棄用前綴: {prefix}",
                }
        
        # Check if file matches pattern
        if not re.match(self.FILE_PATTERN, file_path.name):
            return {
                "asset_id": str(file_path.relative_to(self.project_root)),
                "violation_id": "NAMING-001",
                "severity": "CRITICAL",
                "description": "檔案命名不符合規範",
            }
        
        # Check if file has required prefix (only for governance root files)
        rel_path = file_path.relative_to(self.project_root)
        if len(rel_path.parts) >= 2 and rel_path.parts[0] == "governance":
            # Only enforce prefix for files directly in governance subdirectories
            has_allowed_prefix = any(file_path.name.startswith(prefix) for prefix in self.ALLOWED_PREFIXES)
            if not has_allowed_prefix and file_path.name not in ["README.md", ".gitkeep"]:
                return {
                    "asset_id": str(file_path.relative_to(self.project_root)),
                    "violation_id": "NAMING-PREFIX-001",
                    "severity": "CRITICAL",
                    "description": f"治理檔案缺少必要前綴 (gov_ 或 gov_naming_)",
                }
        
        return None
    
    def check_directory_naming(self, dir_path: Path) -> Optional[dict]:
        # Check for deprecated prefixes
        for prefix in self.FORBIDDEN_PREFIXES:
            if dir_path.name.startswith(prefix):
                return {
                    "asset_id": str(dir_path.relative_to(self.project_root)),
                    "violation_id": "NAMING-DEPRECATED-002",
                    "severity": "BLOCKER",
                    "description": f"目錄使用已棄用前綴: {prefix}",
                }
        
        # Check if directory matches pattern
        if not re.match(self.DIR_PATTERN, dir_path.name):
            return {
                "asset_id": str(dir_path.relative_to(self.project_root)),
                "violation_id": "NAMING-002",
                "severity": "CRITICAL",
                "description": "目錄命名不符合規範",
            }
        
        # Check if directory has allowed prefix (only for L0-L4 directories directly under governance/)
        rel_path = dir_path.relative_to(self.project_root)
        if len(rel_path.parts) == 2 and rel_path.parts[0] == "governance":
            # Only enforce for directories directly under governance/
            has_allowed_prefix = any(dir_path.name.startswith(prefix) for prefix in self.ALLOWED_DIR_PREFIXES)
            if not has_allowed_prefix:
                return {
                    "asset_id": str(dir_path.relative_to(self.project_root)),
                    "violation_id": "NAMING-PREFIX-002",
                    "severity": "CRITICAL",
                    "description": f"治理目錄缺少必要前綴",
                }
        
        return None


if __name__ == "__main__":
    import sys
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    enforcer = GovNamingEnforcer(root)
    violations = enforcer.scan_project()
    print(f"發現 {len(violations)} 個違規")
    for v in violations[:10]:
        print(f"  [{v['severity']}] {v['asset_id']}: {v['description']}")

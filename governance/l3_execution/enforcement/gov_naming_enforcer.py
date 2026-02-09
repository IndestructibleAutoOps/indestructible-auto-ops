#!/usr/bin/env python3
"""
命名規範執行器
Naming Convention Enforcer
"""

import os
import re
from pathlib import Path
from typing import List
from datetime import datetime
import json


class GovNamingEnforcer:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.FILE_PATTERN = r"^[a-z][a-z0-9_]*\.(py|yaml|json|md|txt)$"
        self.DIR_PATTERN = r"^[a-z][a-z0-9_-]*$"
        self.FORBIDDEN_PREFIXES = ["ng_", "gl_"]

    def scan_project(self) -> List[dict]:
        violations = []
        for file_path in self.project_root.rglob("*"):
            if not file_path.is_file():
                continue
            if ".git" in str(file_path) or file_path.name.startswith("."):
                continue
            v = self.check_file_naming(file_path)
            if v:
                violations.append(v)
        return violations

    def check_file_naming(self, file_path: Path) -> dict:
        for prefix in self.FORBIDDEN_PREFIXES:
            if file_path.name.startswith(prefix):
                return {
                    "asset_id": str(file_path.relative_to(self.project_root)),
                    "violation_id": "NAMING-DEPRECATED-001",
                    "severity": "BLOCKER",
                    "description": f"使用已棄用前綴: {prefix}",
                }
        if not re.match(self.FILE_PATTERN, file_path.name):
            return {
                "asset_id": str(file_path.relative_to(self.project_root)),
                "violation_id": "NAMING-001",
                "severity": "CRITICAL",
                "description": "檔案命名不符合規範",
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

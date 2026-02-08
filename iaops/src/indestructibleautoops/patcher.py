from __future__ import annotations

from pathlib import Path
from typing import Any

from .io import ensure_dir, write_text


# Internal templates for common files
INTERNAL_TEMPLATES = {
    "ci.yml": """\
# Auto-generated CI workflow
name: ci
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "Add your build and test steps here"
""",
    "pyproject.toml": """\
# Auto-generated pyproject.toml
[project]
name = "project"
version = "0.1.0"
description = "A Python project"
requires-python = ">=3.11"
""",
}


class Patcher:
    def __init__(self, project_root: Path, allow_writes: bool):
        self.root = project_root
        self.allow_writes = allow_writes

    def _get_template_content(self, action: dict[str, Any]) -> str:
        """Get content for an action, using templateRef if available.
        
        Args:
            action: Action dictionary that may contain a templateRef.
            
        Returns:
            Template content if templateRef is "internal:<name>", 
            otherwise a placeholder comment.
        """
        template_ref = action.get("templateRef", "")
        if template_ref.startswith("internal:"):
            template_name = template_ref.split(":", 1)[1]
            if template_name in INTERNAL_TEMPLATES:
                return INTERNAL_TEMPLATES[template_name]
        
        # Fallback to placeholder
        rel = action.get("path", "unknown")
        return f"# generated placeholder: {rel}\n"

    def apply(self, plan: dict[str, Any]) -> dict[str, Any]:
        actions = plan.get("actions", [])
        applied: list[dict[str, Any]] = []
        skipped: list[dict[str, Any]] = []
        for a in actions:
            kind = a.get("kind")
            if kind == "write_file_if_missing":
                rel = a["path"]
                p = self.root / rel
                if p.exists():
                    skipped.append({"action": a, "reason": "exists"})
                    continue
                if not self.allow_writes:
                    skipped.append({"action": a, "reason": "writes_disabled"})
                    continue
                
                # Get content from templateRef if available
                content = self._get_template_content(a)
                ensure_dir(p.parent)
                write_text(p, content)
                applied.append({"action": a})
                continue
            if kind == "mkdir":
                rel = a["path"]
                p = self.root / rel
                if p.exists():
                    skipped.append({"action": a, "reason": "exists"})
                    continue
                if not self.allow_writes:
                    skipped.append({"action": a, "reason": "writes_disabled"})
                    continue
                ensure_dir(p)
                applied.append({"action": a})
                continue
            skipped.append({"action": a, "reason": "unsupported"})
        return {
            "ok": True,
            "allowWrites": self.allow_writes,
            "applied": applied,
            "skipped": skipped,
        }

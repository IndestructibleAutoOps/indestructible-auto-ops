from __future__ import annotations

from pathlib import Path
from typing import Any

from .io import ensure_dir, write_text

# Internal templates for common files
INTERNAL_TEMPLATES = {
    "ci.yml": """name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: echo "Add your test commands here"
""",
    "pyproject.toml": """[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "project"
version = "0.1.0"
description = "Generated project"
""",
}


class Patcher:
    def __init__(self, project_root: Path, allow_writes: bool):
        self.root = project_root
        self.allow_writes = allow_writes

    def _get_template_content(self, template_ref: str | None) -> str:
        """Get template content from templateRef.

        Supports 'internal:<name>' for built-in templates.
        Returns placeholder comment if templateRef is None or unsupported.
        """
        if not template_ref:
            return "# generated placeholder\n"

        if template_ref.startswith("internal:"):
            template_name = template_ref[9:]  # strip 'internal:' prefix
            if template_name in INTERNAL_TEMPLATES:
                return INTERNAL_TEMPLATES[template_name]

        # Unsupported template reference
        return f"# generated placeholder (template: {template_ref})\n"

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
                ensure_dir(p.parent)
                # Use templateRef to generate proper content
                template_ref = a.get("templateRef")
                content = self._get_template_content(template_ref)
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

#!/usr/bin/env python3
"""
Shim entrypoint to run the canonical MNGA enforcement script.

Bindings:
- Delegates execution to responsibility-namespace-governance-boundary/implementation/ecosystem/enforce.py
- Preserves exit codes from the upstream script so pipelines can keep existing behavior.
"""

from pathlib import Path
import runpy
import sys


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    target = (
        repo_root
        / "governance"
        / "l3_execution"
        / "boundaries"
        / "namespace-governance-boundary"
        / "implementation"
        / "ecosystem"
        / "enforce.py"
    )

    if not target.exists():
        sys.stderr.write(f"Missing upstream enforcement script: {target}\n")
        return 1

    try:
        runpy.run_path(str(target), run_name="__main__")
    except SystemExit as exc:  # propagate exit code from upstream main
        return int(exc.code) if exc.code is not None else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())

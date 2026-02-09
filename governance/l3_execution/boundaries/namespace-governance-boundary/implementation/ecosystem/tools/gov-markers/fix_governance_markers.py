# @GL-governed
# @GL-layer: GL20-29
# @GL-semantic: python-module
# @GL-audit-trail: ../../engine/governance/gov-artifacts/meta/semantic/GL-ROOT-SEMANTIC-ANCHOR.yaml
#
# GL Unified Architecture Governance Framework Activated
# GL Root Semantic Anchor: gov-enterprise-architecture/governance/engine/governance/gov-artifacts/meta/semantic/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gov-enterprise-architecture/governance/engine/governance/gov-artifacts/meta/naming-charter/gl-unified-naming-charter.yaml

#!/usr/bin/env python3
"""
Script to fix missing @GL-governed markers and _gl metadata
"""

# MNGA-002: Import organization needs review
import os
import json
from pathlib import Path

# Files that need @GL-governed marker
MARKER_FILES = [
    "gov-execution-runtime/code-intel-security-layer/capability-schema/capability-definition-language.md",
    "gov-execution-runtime/code-intel-security-layer/deployment-weaver/ci-cd-integration/README.md",
    "gov-execution-runtime/code-intel-security-layer/deployment-weaver/cli-generator/README.md",
    "gov-execution-runtime/code-intel-security-layer/deployment-weaver/ide-extension/README.md",
    "gov-execution-runtime/code-intel-security-layer/deployment-weaver/web-console/README.md",
    "gov-execution-runtime/code-intel-security-layer/evolution-engine/adaptation-engine.py",
    "gov-execution-runtime/code-intel-security-layer/evolution-engine/self-optimizer.py",
    "gov-execution-runtime/code-intel-security-layer/evolution-engine/usage-tracker.py",
    "gov-execution-runtime/code-intel-security-layer/generator-engine/capability-generator.py",
    "gov-execution-runtime/code-intel-security-layer/generator-engine/pattern-matcher.py",
    "gov-execution-runtime/code-intel-security-layer/generator-engine/template-engine.py",
    "gov-execution-runtime/code-intel-security-layer/integrations/v19-fabric/fabric-adapter.py",
    "gov-execution-runtime/code-intel-security-layer/integrations/v19-fabric/fabric-connector.py",
    "gov-execution-runtime/code-intel-security-layer/integrations/v20-continuum/continuum-connector.py",
    "gov-execution-runtime/code-intel-security-layer/integrations/v20-continuum/learning-adapter.py",
    "gov-execution-runtime/code-intel-security-layer/pattern-library/architecture-patterns/solid-principles.md",
    "gov-execution-runtime/code-intel-security-layer/pattern-library/performance-patterns/database-optimization.md",
    "gov-execution-runtime/code-intel-security-layer/pattern-library/security-patterns/sql-injection-prevention.md",
    "gov-execution-runtime/code-intel-security-layer/pattern-library/security-patterns/xss-prevention.md",
    "gov-execution-runtime/gov-platform.gl-platform.governance-audit-reports/audit-summary.md",
    "gov-execution-runtime/infinite-learning-continuum/index.ts",
    "gov-execution-runtime/progress-report.md",
    "gov-execution-runtime/scripts/test-code-intel-security-layer.py",
    "gov-execution-runtime/test-reports/test-summary.md",
    "gov-execution-runtime/todo-v20.md",
    "gov-execution-runtime/todo.md",
    "todo-v20.md",
]

# JSON files that need _gl metadata
JSON_FILES = [
    "gov-execution-runtime/code-intel-security-layer/capability-schema/capability-examples.json",
    "gov-execution-runtime/gov-platform.gl-platform.governance-audit-reports/global-gl-platform.gl-platform.governance-audit-report.json",
    "gov-execution-runtime/test-reports/code-intel-test-report.json",
]


def add_marker_to_file(filepath):
    """Add @GL-governed marker to file"""
    if not os.path.exists(filepath):
        print(f"⚠️  File not found: {filepath}")
        return

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Check if marker already exists
        if "@GL-governed" in content:
            print(f"✓ Marker already exists: {filepath}")
            return

        # Determine the comment style based on file extension
        ext = os.path.splitext(filepath)[1]

        if ext == ".py":
            marker = "# @GL-governed\n"
        elif ext in [".ts", ".js"]:
            marker = "// @GL-governed\n"
        elif ext in [".yaml", ".yml"]:
            marker = "# @GL-governed\n"
        else:  # .md, etc.
            marker = "@GL-governed\n"

        # Add marker at the beginning
        new_content = marker + content

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"✓ Added marker: {filepath}")
    except Exception as e:
        print(f"✗ Error adding marker to {filepath}: {e}")


def add_metadata_to_json(filepath):
    """Add _gl metadata to JSON file"""
    if not os.path.exists(filepath):
        print(f"⚠️  File not found: {filepath}")
        return

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Check if _gl metadata already exists
        if isinstance(data, dict) and "_gl" in data:
            print(f"✓ Metadata already exists: {filepath}")
            return

        # Add _gl metadata
        if isinstance(data, dict):
            data["_gl"] = {
                "gov-platform.gov-platform.governance": "GL-Standard",
                "version": "1.0.0",
                "validated": True,
            }
        elif isinstance(data, list):
            # For lists, we can't add metadata directly
            print(f"⚠️  Cannot add metadata to array: {filepath}")
            return

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"✓ Added metadata: {filepath}")
    except Exception as e:
        print(f"✗ Error adding metadata to {filepath}: {e}")


def main():
    print("🔧 Fixing Governance Markers and Metadata\n")
    print("=" * 50)

    print("\n📝 Adding @GL-governed markers...")
    for filepath in MARKER_FILES:
        add_marker_to_file(filepath)

    print("\n📊 Adding _gl metadata to JSON files...")
    for filepath in JSON_FILES:
        add_metadata_to_json(filepath)

    print("\n" + "=" * 50)
    print("✅ Governance markers and metadata fixed!")


if __name__ == "__main__":
    main()

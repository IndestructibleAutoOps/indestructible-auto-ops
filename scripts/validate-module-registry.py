#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL30-49
# @GL-semantic: validate-module-registry
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
"""
Module Registry Validator
Validates module registry structure and dependencies
"""
import yaml
import sys
from pathlib import Path


def main():
    # Load registry
    registry_path = Path("controlplane/baseline/modules/REGISTRY.yaml")
    if not registry_path.exists():
        print(f"❌ Registry file not found: {registry_path}")
        sys.exit(1)
    with open(registry_path, 'r') as f:
        registry = yaml.safe_load(f)
    print("📋 Module Registry Validation")
    print("=" * 50)
    if 'modules' not in registry:
        print("❌ Registry missing 'modules' section")
        sys.exit(1)

    modules = registry['modules']
    module_ids = {m['module_id'] for m in modules if 'module_id' in m}

    print(f"✅ Found {len(modules)} modules")
    # Check each module
    has_errors = False
    for module in modules:
        module_id = module.get('module_id', 'unknown')
        print(f"\n📦 Module: {module_id}")
        # Check required fields
        required_fields = ['module_id', 'status', 'autonomy_level']
        for field in required_fields:
            if field not in module:
                print(f"  ❌ Missing required field: {field}")
                has_errors = True
            else:
                print(f"  ✅ {field}: {module[field]}")
        # Validate dependencies
        if 'dependencies' in module:
            deps = module['dependencies']
            for dep in deps:
                if dep not in module_ids and dep != 'none':
                    print(f"  ⚠️  Unknown dependency: {dep}")

    print("\n" + "=" * 50)

    if has_errors:
        print("❌ Registry validation failed!")
        sys.exit(1)
    else:
        print("✅ Registry validation passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()

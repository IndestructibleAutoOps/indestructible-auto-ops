#!/bin/bash
# GL YAML 文件驗證 Pre-commit Hook
# 在提交前驗證所有 YAML 文件的語法和結構

set -e

echo "🔍 GL YAML Pre-commit Validation"
echo "=================================="

# 獲取即將提交的 YAML 文件
YAML_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(yaml|yml)$' || true)

if [ -z "$YAML_FILES" ]; then
    echo "✅ No YAML files to validate"
    exit 0
fi

echo "Found $(echo "$YAML_FILES" | wc -l) YAML file(s) to validate:"
echo "$YAML_FILES"
echo

VALIDATION_FAILED=0

# 檢查 Python yaml 模組是否可用
if ! python3 -c "import yaml" 2>/dev/null; then
    echo "⚠️  Warning: PyYAML not installed. Install with: pip install pyyaml"
    echo "Proceeding with basic syntax check only..."
fi

# 驗證每個 YAML 文件
for file in $YAML_FILES; do
    if [ ! -f "$file" ]; then
        continue
    fi
    
    echo "Validating: $file"
    
    # 基本語法檢查
    if ! python3 - "$file" <<'EOF' 2>/dev/null; then
import sys
import yaml

try:
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        yaml.safe_load(f)
except Exception:
    sys.exit(1)
EOF
        echo "❌ ERROR: Invalid YAML syntax in $file"
        VALIDATION_FAILED=1
        continue
    fi
    
    # GL 特定驗證
    if [[ "$file" == gl/*DEFINITION.yaml ]] || [[ "$file" == gl/*/*.yaml ]]; then
        echo "  → GL YAML file detected, performing additional checks..."
        
        # 檢查必需字段
        if ! python3 - "$file" <<'EOF'; then
import yaml
import sys

try:
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # 檢查基本結構
    if not isinstance(data, dict):
        print('  ❌ ERROR: Root must be a dictionary')
        sys.exit(1)
    
    # 檢查版本字段
    if 'version' in data:
        version = str(data['version'])
        if not version.replace('.', '').isdigit():
            print('  ⚠️  Warning: Version should be in semver format (e.g., 1.0.0)')
    
    # 檢查描述字段
    if 'description' in data and not isinstance(data['description'], str):
        print('  ❌ ERROR: description must be a string')
        sys.exit(1)
    
    print('  ✅ GL YAML structure valid')
except Exception as e:
    print(f'  ❌ ERROR: {e}')
    sys.exit(1)
EOF
            VALIDATION_FAILED=1
        fi
    else
        echo "  ✅ Valid YAML syntax"
    fi
    
    echo
done

if [ $VALIDATION_FAILED -eq 1 ]; then
    echo ""
    echo "❌ YAML validation failed!"
    echo "Please fix the errors above before committing."
    echo "You can bypass this check with: git commit --no-verify"
    exit 1
fi

echo "✅ All YAML files validated successfully!"
exit 0
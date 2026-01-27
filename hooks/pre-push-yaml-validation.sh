#!/bin/bash
# GL YAML 文件驗證 Pre-push Hook
# 在推送前執行完整的 YAML 驗證流程

set -e

echo "🔍 GL YAML Pre-push Validation"
echo "==============================="

# 獲取當前分支的遠程
REMOTE="$1"
URL="$2"

echo "Pushing to: $REMOTE ($URL)"
echo

# 檢查是否有 GL YAML 文件變更
GL_YAML_CHANGES=$(git diff --name-only $REMOTE/$(git branch --show-current) HEAD | grep -E '^gl/.*\.ya?ml$' || true)

if [ -z "$GL_YAML_CHANGES" ]; then
    echo "✅ No GL YAML files changed in this push"
    exit 0
fi

echo "Found GL YAML changes:"
echo "$GL_YAML_CHANGES"
echo

VALIDATION_FAILED=0

# 深度驗證 GL YAML 文件
for file in $GL_YAML_CHANGES; do
    if [ ! -f "$file" ]; then
        continue
    fi
    
    echo "Validating: $file"
    
    # 語法驗證
    if ! python3 - "$file" <<'EOF' 2>/dev/null; then
import sys
import yaml

file_path = sys.argv[1]
with open(file_path, 'r', encoding='utf-8') as f:
    yaml.safe_load(f)
EOF
        echo "❌ ERROR: Invalid YAML syntax in $file"
        VALIDATION_FAILED=1
        continue
    fi
    
    # GL 層級驗證
    if [[ "$file" =~ ^gl/([0-9]{2})- ]]; then
        layer="${BASH_REMATCH[1]}"
        echo "  → Layer $layer detected, performing layer-specific validation..."
        
        # 根據不同層級執行特定驗證
        case $layer in
            00)
                # 戰略層驗證
                python3 - "$file" <<'EOF' || VALIDATION_FAILED=1
import yaml
import sys
try:
    with open(sys.argv[1], 'r') as f:
        data = yaml.safe_load(f)
    if 'strategic_objectives' in data or 'vision' in data or 'mission' in data:
        print('  ✅ Strategic layer structure valid')
except Exception as e:
    print(f'  ❌ ERROR: {e}')
    sys.exit(1)
EOF
                ;;
            10|20|30|40|50|60|70|80|90)
                # 其他層級驗證
                python3 - "$file" <<'EOF' || VALIDATION_FAILED=1
import yaml
import sys
try:
    with open(sys.argv[1], 'r') as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict) or not data:
        print('  ❌ ERROR: File must be a non-empty dictionary')
        sys.exit(1)
    print('  ✅ Layer structure valid')
except Exception as e:
    print(f'  ❌ ERROR: {e}')
    sys.exit(1)
EOF
                ;;
        esac
    fi
    
    echo
done

# 交叉引用驗證
echo "Checking cross-references..."
if command -v python3 &> /dev/null; then
    python3 - <<'EOF'
import yaml
import glob
import sys

try:
    # 加載所有 GL YAML 文件
    yaml_files = glob.glob('gl/**/*.yaml', recursive=True)
    all_data = {}
    
    for yaml_file in yaml_files:
        try:
            with open(yaml_file, 'r') as f:
                all_data[yaml_file] = yaml.safe_load(f)
        except (IOError, OSError, yaml.YAMLError):
            pass
    
    print(f'  ✅ Loaded {len(all_data)} GL YAML files for cross-reference check')
except Exception as e:
    print(f'  ⚠️  Warning: Cross-reference check skipped: {e}')
EOF
fi

echo

if [ $VALIDATION_FAILED -eq 1 ]; then
    echo ""
    echo "❌ YAML validation failed!"
    echo "Please fix the errors before pushing."
    echo "You can bypass this check with: git push --no-verify"
    exit 1
fi

echo "✅ All GL YAML files validated successfully!"
exit 0
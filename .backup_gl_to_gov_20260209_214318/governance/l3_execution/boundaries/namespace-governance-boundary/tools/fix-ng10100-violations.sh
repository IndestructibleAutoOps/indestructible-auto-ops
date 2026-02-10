#!/bin/bash

# NG10100 自动修复脚本
# 修复所有目录命名违规，转换为 kebab-case 格式
# 生成时间：$(date -u +"%Y-%m-%dT%H:%M:%SZ")

set -e

WORKSPACE="/workspace"
cd "$WORKSPACE"

echo "开始修复 NG10100 目录命名违规..."
echo "======================================"

# 统计变量
TOTAL_RENAMED=0
TOTAL_FILES_UPDATED=0

# 函数：将目录名转换为 kebab-case
convert_to_kebab_case() {
    local dir_name="$1"
    
    # 将下划线替换为连字符
    local converted="${dir_name//_/-}"
    # 转换为小写
    converted="${converted,,}"
    
    echo "$converted"
}

# 函数：重命名目录
rename_directory() {
    local old_path="$1"
    local new_name="$2"
    
    local dir_path=$(dirname "$old_path")
    local new_path="$dir_path/$new_name"
    
    if [ "$old_path" != "$new_path" ] && [ -d "$old_path" ]; then
        echo "重命名: $old_path -> $new_path"
        mv "$old_path" "$new_path"
        ((TOTAL_RENAMED++))
        return 0
    fi
    return 1
}

# 函数：更新文件中的路径引用
update_path_references() {
    local old_name="$1"
    local new_name="$2"
    
    # 跳过特殊目录（node_modules, .git等）
    if [[ "$old_name" =~ ^(\.git|node_modules|__pycache__|\.venv|venv)$ ]]; then
        return 0
    fi
    
    # 查找所有可能包含路径引用的文件
    local file_types=("*.py" "*.js" "*.ts" "*.json" "*.yaml" "*.yml" "*.md" "*.txt" "*.sh" "*.toml" "*.cfg" "*.ini")
    
    for ext in "${file_types[@]}"; do
        # 使用 find 和 grep 定位包含旧路径的文件
        while IFS= read -r -d '' file; do
            if [ -f "$file" ]; then
                # 更新各种格式的路径引用
                # 1. Unix路径格式
                if grep -q "$old_name" "$file" 2>/dev/null; then
                    # 创建临时文件
                    local temp_file="${file}.tmp"
                    
                    # 执行替换（处理各种路径格式）
                    sed -e "s|/$old_name/|/$new_name/|g" \
                        -e "s|/$old_name&quot;|/$new_name&quot;|g" \
                        -e "s|/$old_name'|/$new_name'|g" \
                        -e "s|/$old_name}|/$new_name}|g" \
                        -e "s|/$old_name$|/$new_name|g" \
                        -e "s|$old_name/|$new_name/|g" \
                        -e "s|\\$old_name/|$new_name/|g" \
                        -e "s|\\$old_name&quot;|$new_name&quot;|g" \
                        -e "s|\\$old_name'|$new_name'|g" \
                        -e "s|\\$old_name}|$new_name}|g" \
                        -e "s|\\$old_name$|$new_name|g" \
                        "$file" > "$temp_file" && mv "$temp_file" "$file"
                    
                    ((TOTAL_FILES_UPDATED++))
                fi
            fi
        done < <(find "$WORKSPACE" -type f -name "$ext" -print0 2>/dev/null | head -1000)
    done
}

# 需要修复的目录列表（按照从深层到浅层的顺序排列）
declare -a directories=(
    # 最深层目录优先
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-003"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-086"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-2a5"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-2c8"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-2d4"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-388"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-61c"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-9a2"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-9ad"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-a15"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-bfe"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-2025-12-22-d09"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/naming-governance-v1-0-0-extended/monitoring"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/naming-governance-v1-0-0-extended/governance/naming"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/naming-governance-v1-0-0-extended/automation/scripts"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/quantum-naming-v4-0-0/monitoring"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/quantum-naming-v4-0-0/scripts"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/quantum-naming-v4-0-0/workflows"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/quantum-naming-v4-0-0/docs"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/quantum-naming-v4-0-0/deployment"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/quantum-naming-v4-0-0/config"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/naming-governance-v1-0-0-extended"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/quantum-naming-v4-0-0"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/naming-governance-v1-0-0/scripts/validation"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/naming-governance-v1-0-0/scripts/generation"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/naming-governance-v1-0-0/scripts/audit"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/naming-governance-v1-0-0/monitoring/prometheus"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/naming-governance-v1-0-0/monitoring/grafana"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/naming-governance-v1-0-0/training/modules"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/naming-governance-v1-0-0/ci-cd/workflows"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/naming-governance-v1-0-0/docs/best-practices"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/naming-governance-v1-0-0"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-d36"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-2c8"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-9ad"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-388"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-a15"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-61c"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-9a2"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-2a5"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-086"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-2d4"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-bfe"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-2025-12-22-d09"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/standards"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/policies/change-management"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/policies/gatekeeper"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/policies/validation"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/policies/migration"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/policies/security"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/policies/naming"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/policies/observability"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/policies/exception"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/policies"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-d36"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-2c8"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-9ad"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-388"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-a15"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-61c"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-9a2"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-2a5"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-086"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-2d4"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-bfe"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-2025-12-22-d09"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-d36"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-2c8"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-9ad"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-388"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-a15"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-61c"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-9a2"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-2a5"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-086"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-2d4"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-trace-2025-12-22-bfe"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming/trace-2025-12-22-d09"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence/incoming"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/evidence"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/standards"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/policies/change-management"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/policies/gatekeeper"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/policies/validation"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/policies/migration"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/policies/security"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/policies/naming"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/policies/observability"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/policies/exception"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/policies"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/tests/performance"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/tests/unit"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/tests/e2e"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/tests"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/rollback/points"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/rollback"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/security"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/compliance"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy/reports"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy/governance-legacy"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived/legacy"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/archived"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance/gl90-99-semantic-engine"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer/governance"
    "gov-governance-architecture-platform/gl90-99-meta-specification-layer"
    # 测试目录
    "tests/gl/autonomy-boundary/external-api-unavailable"
    "ecosystem/tests/semantic-defense/test-complement-missing"
    "ecosystem/tests/semantic-defense/test-yaml-failure"
    "ecosystem/tests/semantic-defense/test-semantic-corruption"
    "ecosystem/tests/semantic-defense/test-hash-divergence"
    "ecosystem/tests/semantic-defense/test-layered-sorting"
    "ecosystem/tests/semantic-defense/test-canonicalization-invariant"
    "ecosystem/tests/semantic-defense/test-tool-registry"
    "ecosystem/tests/semantic-defense/test-pipeline-interrupted"
    "ecosystem/tests/semantic-defense/test-event-missing-field"
    "ecosystem/tests/semantic-defense"
    # 证据目录
    "ecosystem/.evidence/semantic-tokens"
    "ecosystem/.evidence/autonomy-boundary/era-seals"
    "ecosystem/.evidence/autonomy-boundary/replayability-reports"
    "ecosystem/.evidence/autonomy-boundary/hash-boundaries"
    "ecosystem/.evidence/autonomy-boundary/wagb/append-only-events"
    "ecosystem/.evidence/autonomy-boundary/wagb"
    "ecosystem/.evidence/autonomy-boundary"
    # 治理目录
    "ecosystem/governance/hash-spec"
    "ecosystem/governance/gov-semantic-anchors"
    "ecosystem/governance/templates/artifact-schemas"
    "ecosystem/governance/templates/tool-stubs"
    "ecosystem/governance/templates/event-schemas"
    "ecosystem/governance/templates"
    # 推理目录
    "ecosystem/reasoning/dual-path"
    # NG 治理目录
    "ng-namespace-governance"
    # 机器原生操作
    "machine-native-ops/ecosystem/reasoning/dual-path"
    # 文档目录
    "docs/runbooks"
    "docs/training"
    "docs/migration"
    # 平台目录
    "platforms/gov-platform-ide"
    "platforms/gov-platform-assistant"
    # 运行时引擎
    "gov-runtime-execution-platform/engine/tools-legacy/path-tools"
    "gov-runtime-execution-platform/engine/aep-engine-app/app/tabs"
    "gov-runtime-execution-platform/engine/aep-engine-app/app"
    "gov-runtime-execution-platform/engine/aep-engine-app"
    "gov-runtime-execution-platform/engine/tools-legacy"
    "gov-runtime-execution-platform/engine"
    "gov-runtime-engine-platform/tools-legacy/path-tools"
    "gov-runtime-engine-platform/aep-engine-app/app/tabs"
    "gov-runtime-engine-platform/aep-engine-app/app"
    "gov-runtime-engine-platform/aep-engine-app"
    "gov-runtime-engine-platform/tools-legacy"
    # Indestructible AutoOps 治理
    "indestructible-autoops-governance/auto-task-project"
    "indestructible-autoops-governance/tests/gl/autonomy-boundary/external-api-unavailable"
    "indestructible-autoops-governance/ecosystem/tests/semantic-defense/test-semantic-corruption"
    "indestructible-autoops-governance/ecosystem/tests/semantic-defense/test-hash-divergence"
    "indestructible-autoops-governance/ecosystem/tests/semantic-defense"
    "indestructible-autoops-governance/ecosystem/.evidence/semantic-tokens"
    "indestructible-autoops-governance/ecosystem/.evidence/autonomy-boundary/era-seals"
    "indestructible-autoops-governance/ecosystem/.evidence/autonomy-boundary/replayability-reports"
    "indestructible-autoops-governance/ecosystem/.evidence/autonomy-boundary/hash-boundaries"
    "indestructible-autoops-governance/ecosystem/.evidence/autonomy-boundary/wagb/append-only-events"
    "indestructible-autoops-governance/ecosystem/.evidence/autonomy-boundary/wagb"
    "indestructible-autoops-governance/ecosystem/.evidence/autonomy-boundary"
    "indestructible-autoops-governance/ecosystem/governance/hash-spec"
    "indestructible-autoops-governance/ecosystem/governance/gov-semantic-anchors"
    "indestructible-autoops-governance/ecosystem/reasoning/dual-path"
    "indestructible-autoops-governance/docs/runbooks"
    "indestructible-autoops-governance/docs/training"
    "indestructible-autoops-governance/docs/migration"
    "indestructible-autoops-governance/platforms/gov-platform-ide"
    "indestructible-autoops-governance/platforms/gov-platform-assistant"
    "indestructible-autoops-governance/gov-runtime-execution-platform/engine/tools-legacy/path-tools"
    "indestructible-autoops-governance/gov-runtime-execution-platform/engine/aep-engine-app/app/tabs"
    "indestructible-autoops-governance/gov-runtime-execution-platform/engine/aep-engine-app/app"
    "indestructible-autoops-governance/gov-runtime-execution-platform/engine/aep-engine-app"
    "indestructible-autoops-governance/gov-runtime-execution-platform/engine/tools-legacy"
    "indestructible-autoops-governance/gov-runtime-execution-platform/engine"
    "indestructible-autoops-governance/gov-runtime-engine-platform/tools-legacy/path-tools"
    "indestructible-autoops-governance/gov-runtime-engine-platform/aep-engine-app/app/tabs"
    "indestructible-autoops-governance/gov-runtime-engine-platform/aep-engine-app/app"
    "indestructible-autoops-governance/gov-runtime-engine-platform/aep-engine-app"
    "indestructible-autoops-governance/gov-runtime-engine-platform/tools-legacy"
    # 根目录
    "summarized_conversations"
)

# 第一阶段：重命名目录（从深层到浅层）
echo ""
echo "第一阶段：重命名目录..."
echo "======================================"

for dir_path in "${directories[@]}"; do
    if [ -d "$WORKSPACE/$dir_path" ]; then
        old_name=$(basename "$dir_path")
        new_name=$(convert_to_kebab_case "$old_name")
        
        if [ "$old_name" != "$new_name" ]; then
            rename_directory "$WORKSPACE/$dir_path" "$new_name"
        fi
    fi
done

# 第二阶段：更新所有文件中的路径引用
echo ""
echo "第二阶段：更新文件中的路径引用..."
echo "======================================"

for dir_path in "${directories[@]}"; do
    old_name=$(basename "$dir_path")
    new_name=$(convert_to_kebab_case "$old_name")
    
    if [ "$old_name" != "$new_name" ]; then
        update_path_references "$old_name" "$new_name"
    fi
done

# 验证修复结果
echo ""
echo "验证修复结果..."
echo "======================================"

# 重新运行验证器
if [ -f "$WORKSPACE/ng-namespace-governance/tools/ng-namespace-validator.py" ]; then
    python3 "$WORKSPACE/ng-namespace-governance/tools/ng-namespace-validator.py" > /tmp/ng10100-validation-after.json
    echo "验证完成，结果已保存到 /tmp/ng10100-validation-after.json"
else
    echo "警告：验证器脚本不存在，跳过验证步骤"
fi

# 输出总结
echo ""
echo "======================================"
echo "修复完成！"
echo "======================================"
echo "重命名目录数：$TOTAL_RENAMED"
echo "更新文件数：$TOTAL_FILES_UPDATED"
echo ""
echo "请查看 /tmp/ng10100-validation-after.json 获取详细的验证结果"
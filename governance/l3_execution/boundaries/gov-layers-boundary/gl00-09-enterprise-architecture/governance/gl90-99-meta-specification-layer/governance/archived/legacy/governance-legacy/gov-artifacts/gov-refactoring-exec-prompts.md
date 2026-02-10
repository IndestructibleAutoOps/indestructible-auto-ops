# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: documentation
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Architecture Governance Framework Activated
# GL 目錄重構 - 高執行權重提示詞

## 執行指令 1: 重命名 extensions → gov-extended
```bash
cd workspace/governance/gov-architecture
git mv extensions gov-extended
```

## 執行指令 2: 更新所有檔案中的路徑引用
```bash
# 更新 INDEX.yaml
sed -i 's|extensions/|gov-extended/|g' workspace/governance/gov-architecture/INDEX.yaml

# 更新 README.md
sed -i 's|extensions/|gov-extended/|g' workspace/governance/gov-architecture/README.md

# 更新 governance-manifest.yaml
sed -i 's|extensions/|gov-extended/|g' governance-manifest.yaml

# 更新所有 integration YAML 檔案
find workspace/governance/gov-architecture/integrations/ -name "*.yaml" -exec sed -i 's|extensions/|gov-extended/|g' {} \;
```

## 執行指令 3: 驗證重構完整性
```python
import os
import yaml

def verify_gl_refactoring():
    base_path = "workspace/governance/gov-architecture"
    
    # 檢查 gov-extended 目錄存在
    assert os.path.exists(f"{base_path}/gov-extended"), "gov-extended directory must exist"
    
    # 檢查 extensions 目錄不存在
    assert not os.path.exists(f"{base_path}/extensions"), "extensions directory should not exist"
    
    # 驗證所有 GL 層級目錄
    layers = [
        "GL00-09-strategic",
        "GL10-29-operational",
        "GL30-49-execution",
        "GL50-59-observability",
        "GL60-80-advanced",
        "GL81-83-extended",
        "GL90-99-meta"
    ]
    
    for layer in layers:
        layer_path = f"{base_path}/gov-extended/{layer}"
        assert os.path.exists(layer_path), f"{layer} must exist in gov-extended/"
        assert os.path.exists(f"{layer_path}/DEFINITION.yaml"), f"{layer}/DEFINITION.yaml must exist"
        assert os.path.exists(f"{layer_path}/EXEC_PROMPTS.md"), f"{layer}/EXEC_PROMPTS.md must exist"
        assert os.path.exists(f"{layer_path}/README.md"), f"{layer}/README.md must exist"
    
    print("✅ GL 重構驗證完成")
    return True

verify_gl_refactoring()
```

## 執行指令 4: 更新 git 提交
```bash
git add -A
git commit -m "Refactor: Rename extensions/ to gov-extended/ for semantic clarity"
git push origin <branch-name>
```

## 執行指令 5: 部署更新後的配置
```bash
# 應用新的目錄命名規範
kubectl apply -f workspace/governance/gov-architecture/GL_DIRECTORY_NAMING_SPEC.yaml

# 應用 filesystem 映射
kubectl apply -f workspace/governance/gov-architecture/GL_FILESYSTEM_MAPPING.yaml

# 驗證部署
kubectl get glspecifications -n governance
```

## 執行指令 6: 生成重構報告
```bash
python scripts/governance/generate_refactoring_report.py \
  --before "extensions" \
  --after "gov-extended" \
  --output "reports/gov-refactoring-2026-01-18.md"
```

## 執行指令 7: 通知所有集成系統
```python
from governance_integration import notify_integrations

notify_integrations({
    "event": "gov-directory-refactored",
    "changes": {
        "old_path": "workspace/governance/gov-architecture/extensions",
        "new_path": "workspace/governance/gov-architecture/gov-extended"
    },
    "affected_layers": ["GL00-09", "GL10-29", "GL30-49", "GL50-59", "GL60-80", "GL81-83", "GL90-99"],
    "migration_guide": "workspace/governance/gov-architecture/GL_DIRECTORY_NAMING_SPEC.yaml"
})
```

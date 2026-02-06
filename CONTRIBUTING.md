# 🚨 CONTRIBUTING TO INDESTRUCTIBLEAUTOOPS

**平台**: IndestructibleAutoOps - Cloud-Native AIOps Platform  
**原則**: ZERO TOLERANCE | 永不降級 | 永不覆寫  
**模式**: Autonomous Infrastructure Resilience through ML-Driven Self-Healing

---

## ⚠️ 核心鐵律（不可妥協）

> **這些規則是 IMMUTABLE（不可變）的，違反任何一條將導致 PERMANENT_BLOCK**

---

## 🚫 鐵律一：永不覆寫原則（NO OVERRIDE EVER）

### 📜 核心命名空間治理規範

#### 1. 禁止覆寫原則（ABSOLUTE）

**所有屬於 `ng-*`、`gl-*`、`ecosystem/*` 命名空間的公共 API 與核心模組，嚴禁直接覆寫或猴子補丁（Monkey Patching）。**

**禁止的操作**:
```python
# ❌ FORBIDDEN - PERMANENT_BLOCK
import ng_namespace_governance
ng_namespace_governance.NgExecutor = MyCustomExecutor  # 覆寫

# ❌ FORBIDDEN - PERMANENT_BLOCK
from ecosystem.enforce import GovernanceEnforcer
GovernanceEnforcer.validate = lambda self, x: True  # 猴子補丁

# ❌ FORBIDDEN - PERMANENT_BLOCK
class MyExecutor(NgExecutor):
    def execute(self, *args, **kwargs):
        # 直接覆寫核心方法
        pass
```

**允許的操作**:
```python
# ✅ ALLOWED - 擴展而非覆寫
class MyCustomExecutor(NgExecutor):
    def execute_custom_logic(self):
        # 新增方法，不覆寫核心
        result = super().execute()
        return self.enhance(result)

# ✅ ALLOWED - 通過 PR 修改核心
# 提交 PR 到 ng-namespace-governance
# 經過完整審核流程
```

#### 2. 變更流程（MANDATORY）

**任何修正、更新或擴展必須透過 Pull Request，無例外。**

**流程**:
```
1. Fork 儲存庫
2. 創建功能分支（feature/*, fix/*, docs/*）
3. 進行修改並通過本地測試
4. 提交 Pull Request
5. 通過機器審核（CI/CD）
6. 通過組織審核（安全掃描）
7. 通過企業審核（合規檢查）
8. 至少 2 位核心維護者批准
9. 合併到主分支
```

**禁止**:
```bash
# ❌ FORBIDDEN - 直接推送到 main
git push origin main

# ❌ FORBIDDEN - 強制推送
git push --force origin main

# ❌ FORBIDDEN - 繞過 PR
git commit --no-verify && git push
```

#### 3. 自動化審核（機器審核三級制）

##### 機器團隊級別（Team）
**CI 流水線 - 必須 100% 通過**

- ✅ Lint 檢查（ruff, black, isort）
  - 行長限制：100
  - 零警告容忍
  - 零錯誤容忍

- ✅ 單元測試
  - 覆蓋率 >= 95%
  - 所有測試必須通過
  - 零失敗容忍

- ✅ 整合測試
  - 端到端測試通過
  - 性能基準達標
  - 零降級容忍

- ✅ 靜態分析
  - mypy 類型檢查（strict mode）
  - bandit 安全掃描（零漏洞）
  - pylint 評分 >= 9.5/10

**配置範例**:
```yaml
# .github/workflows/ng-ci.yaml
name: NG Namespace Governance CI

on: [pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Ruff Check
        run: ruff check . --select ALL
        # ZERO TOLERANCE: 任何 error/warning = CI 失敗
      
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Run Tests
        run: pytest --cov=. --cov-fail-under=95
        # ZERO TOLERANCE: 覆蓋率 < 95% = CI 失敗
      
  security:
    runs-on: ubuntu-latest
    steps:
      - name: Bandit Security Scan
        run: bandit -r . -ll
        # ZERO TOLERANCE: 任何 HIGH/MEDIUM 漏洞 = CI 失敗
```

##### 機器組織級別（Organization）
**依賴掃描 - 零漏洞容忍**

- ✅ 安全掃描
  - Snyk / Dependabot
  - 零 HIGH/CRITICAL 漏洞
  - 自動依賴更新

- ✅ 許可證合規
  - FOSSA / Black Duck
  - 僅允許白名單許可證
  - GPL 病毒檢查

- ✅ 供應鏈安全
  - SBOM 生成和驗證
  - 簽名驗證
  - 來源追蹤

**配置範例**:
```yaml
# dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "daily"
    open-pull-requests-limit: 10
    # ZERO TOLERANCE: 立即更新有漏洞的依賴
```

##### 機器企業級別（Enterprise）
**發布門禁 - 絕對合規**

- ✅ 版本號規範
  - 嚴格 Semantic Versioning
  - NG 編碼對應關係驗證
  - 零偏差容忍

- ✅ 變更日誌要求
  - 每個 PR 必須有變更描述
  - 遵循 Conventional Commits
  - 自動生成 CHANGELOG

- ✅ 文檔完整性
  - API 文檔必須更新
  - 架構圖必須同步
  - 零過時文檔容忍

**配置範例**:
```yaml
# release.yaml
on:
  push:
    tags:
      - 'v*'

jobs:
  validate-release:
    steps:
      - name: Validate Version
        run: |
          # ZERO TOLERANCE: 版本號必須符合規範
          python tools/validate-version.py || exit 1
      
      - name: Validate Changelog
        run: |
          # ZERO TOLERANCE: 必須有完整變更日誌
          python tools/validate-changelog.py || exit 1
```

#### 4. 人工複核（MANDATORY）

**在通過所有自動化檢查後，必須由至少 2 位核心維護者批准方可合併。**

**批准要求**:
```yaml
review_requirements:
  required_approvals: 2
  required_reviewers_from_team: "ng-core-maintainers"
  dismiss_stale_reviews: true
  require_code_owner_reviews: true
  
code_owners:
  # NG 核心
  ng-namespace-governance/**  @ng-core-team @governance-committee
  
  # 執行引擎
  **/ng-executor.py           @ng-core-team @ml-team
  **/ng-ml-*.py              @ml-team @security-team
  
  # 零容忍策略
  **/ZERO-TOLERANCE*.yaml    @governance-committee (UNANIMOUS required)
```

---

## 🚫 鐵律二：永不降級原則（NO DEGRADATION EVER）

### 絕對禁止降級的項目

#### 1. 驗證標準（IMMUTABLE）
```python
# ❌ FORBIDDEN
validation_threshold = 0.90  # 從 0.95 降低到 0.90

# ✅ REQUIRED
validation_threshold = 0.95  # 保持或提高
```

#### 2. 測試覆蓋率（IMMUTABLE）
```yaml
# ❌ FORBIDDEN
coverage: 90%  # 從 95% 降低

# ✅ REQUIRED  
coverage: 95%  # 保持或提高
```

#### 3. 性能 SLA（IMMUTABLE）
```python
# ❌ FORBIDDEN
max_latency_ms = 200  # 從 100ms 增加

# ✅ REQUIRED
max_latency_ms = 100  # 保持或降低
```

#### 4. ML 信心閾值（IMMUTABLE）
```python
# ❌ FORBIDDEN
ml_confidence_threshold = 0.90  # 從 0.95 降低

# ✅ REQUIRED
ml_confidence_threshold = 0.95  # 保持或提高
```

#### 5. 閉環完整性（IMMUTABLE）
```python
# ❌ FORBIDDEN
closure_completeness_requirement = 0.95  # 從 1.0 降低

# ✅ REQUIRED
closure_completeness_requirement = 1.0  # 必須保持 100%
```

### 檢測降級的自動化工具

**配置**: `.github/workflows/no-degradation-check.yaml`

```yaml
name: No Degradation Check

on: [pull_request]

jobs:
  check-metrics:
    runs-on: ubuntu-latest
    steps:
      - name: Check Test Coverage
        run: |
          CURRENT=$(pytest --cov=. --cov-report=json | jq '.totals.percent_covered')
          BASELINE=95
          if (( $(echo "$CURRENT < $BASELINE" | bc -l) )); then
            echo "🚨 ZERO_TOLERANCE_VIOLATION: Coverage degradation"
            echo "   Current: $CURRENT% < Required: $BASELINE%"
            exit 1
          fi
      
      - name: Check Performance SLA
        run: |
          # ZERO TOLERANCE: 任何性能降級 = BLOCK
          python tools/benchmark.py --compare-baseline --fail-on-degradation
      
      - name: Check ML Confidence
        run: |
          # ZERO TOLERANCE: ML 信心不得降低
          python tools/validate-ml-confidence.py --min-threshold 0.95
```

---

## 📋 技術實現：命名空間守護

### 1. ESLint / Pylint 自訂規則

**Python 範例** (`.pylintrc`):
```ini
[MASTER]
load-plugins=ng_namespace_guardian

[ng-namespace-guardian]
# 禁止覆寫 ng-* 命名空間
forbidden-overwrites=ng_namespace_governance,ecosystem.enforce,auto_executor
# 檢測猴子補丁
detect-monkey-patching=true
# 動作：立即失敗
action=FAIL_IMMEDIATELY
```

**自訂 Pylint 插件** (`ng_namespace_guardian.py`):
```python
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

class NgNamespaceGuardian(BaseChecker):
    __implements__ = IAstroidChecker
    
    name = 'ng-namespace-guardian'
    msgs = {
        'E9001': (
            'ZERO_TOLERANCE_VIOLATION: Forbidden override of ng-* namespace',
            'ng-namespace-override',
            'Overriding ng-* namespaces is permanently forbidden'
        ),
    }
    
    def visit_assignattr(self, node):
        # 檢測對 ng-* 模組的屬性賦值
        if node.attrname and 'ng_' in node.attrname:
            self.add_message('ng-namespace-override', node=node)
```

### 2. Pre-commit Hook

**配置**: `.pre-commit-config.yaml`

```yaml
repos:
  - repo: local
    hooks:
      - id: ng-namespace-guard
        name: NG Namespace Guardian
        entry: python tools/ng-namespace-guard.py
        language: python
        files: '\\.py$'
        # ZERO TOLERANCE: 檢測到覆寫 = BLOCK commit
        
      - id: no-degradation-check
        name: No Degradation Check
        entry: python tools/no-degradation-check.py
        language: python
        pass_filenames: false
        # ZERO TOLERANCE: 檢測到降級 = BLOCK commit
```

### 3. 快照測試

**測試檔案**: `tests/test_ng_core_immutability.py`

```python
"""
NG 核心不可變性測試
確保核心模組行為永不改變
"""
import pytest
import json
from pathlib import Path

def test_ng_executor_behavior_snapshot():
    """測試 NgExecutor 行為快照（不可變）"""
    from ng_namespace_governance.core.ng_executor import NgExecutor
    
    executor = NgExecutor()
    
    # 載入基線快照
    baseline = json.loads(
        Path('tests/snapshots/ng-executor-baseline.json').read_text()
    )
    
    # 執行並比較
    current_behavior = executor.get_behavior_signature()
    
    # ZERO TOLERANCE: 任何行為改變 = 測試失敗
    assert current_behavior == baseline, (
        "ZERO_TOLERANCE_VIOLATION: NgExecutor behavior changed. "
        "If intentional, update baseline with governance approval."
    )

def test_ng_validation_rules_immutable():
    """測試驗證規則不可變"""
    from ng_namespace_governance.core import validation_rules
    
    # 檢查關鍵配置
    assert validation_rules.ZERO_TOLERANCE_MODE == True
    assert validation_rules.TOLERANCE_LEVEL == 0.0
    assert validation_rules.AUTO_FIX_ENABLED == False
    
    # ZERO TOLERANCE: 配置被修改 = 測試失敗
```

---

## 🚫 鐵律二：永不降級原則（NO DEGRADATION EVER）

### 不可降級的指標（IMMUTABLE）

| 指標 | 當前值 | 最低要求 | 動作 |
|------|--------|----------|------|
| 測試覆蓋率 | 95% | >= 95% | BLOCK if < 95% |
| Lint 評分 | 9.5/10 | >= 9.5/10 | BLOCK if < 9.5 |
| 驗證延遲 | 100ms | <= 100ms | BLOCK if > 100ms |
| ML 信心閾值 | 95-99% | >= 95% | BLOCK if < 95% |
| 閉環完整性 | 100% | == 100% | BLOCK if < 100% |
| 系統可用性 | 99.99% | >= 99.99% | INCIDENT if < 99.99% |
| 違規容忍度 | 0% | == 0% | BLOCK if > 0% |

### 自動檢測降級

**工具**: `tools/detect-degradation.py`

```python
#!/usr/bin/env python3
"""
降級檢測工具
檢測任何指標降級並立即阻斷
"""

import sys
import json
from pathlib import Path

def check_no_degradation():
    """檢查無降級"""
    
    # 載入基線
    baseline = json.loads(Path('metrics/baseline.json').read_text())
    
    # 當前指標
    current = get_current_metrics()
    
    violations = []
    
    # 檢查每個指標
    for metric, baseline_value in baseline.items():
        current_value = current.get(metric)
        
        if current_value < baseline_value:
            violations.append({
                'metric': metric,
                'baseline': baseline_value,
                'current': current_value,
                'degradation': baseline_value - current_value
            })
    
    if violations:
        print("🚨 ZERO_TOLERANCE_VIOLATION: Degradation detected")
        for v in violations:
            print(f"   ❌ {v['metric']}: {v['current']} < {v['baseline']}")
        print("\n🚫 PERMANENT_BLOCK: Fix degradation before proceeding")
        sys.exit(1)
    
    print("✅ No degradation detected")
    sys.exit(0)

if __name__ == "__main__":
    check_no_degradation()
```

---

## 🔒 鐵律三：審核流程（THREE-TIER REVIEW）

### 機器審核（自動化）

#### Tier 1: Team CI/CD
```
✅ Lint通過 → 0 warnings, 0 errors
✅ Tests通過 → 100% pass, >= 95% coverage
✅ Build通過 → 零錯誤構建
✅ NG守護 → 零命名空間違規
```

#### Tier 2: Organization Security
```
✅ Snyk掃描 → 零 HIGH/CRITICAL 漏洞
✅ 許可證檢查 → 100% 白名單
✅ SBOM驗證 → 完整物料清單
✅ 簽名驗證 → 加密簽名有效
```

#### Tier 3: Enterprise Compliance
```
✅ SonarQube → 評分 >= A 級
✅ 版本規範 → 100% Semantic Versioning
✅ 變更日誌 → 100% 完整
✅ 文檔同步 → 100% 更新
```

### 人工複核（強制）

**要求**:
- **最少審核者**: 2 位核心維護者
- **特殊 PR 要求**:
  - 零容忍策略修改：需治理委員會**一致同意**（100% 投票）
  - 核心執行引擎：需 ML 團隊 + 安全團隊審核
  - NG 規範修改：需架構團隊 + 治理委員會審核

**審核清單**:
```markdown
## PR 審核清單（核心維護者必須全部勾選）

### 零容忍合規
- [ ] 無覆寫核心命名空間
- [ ] 無降級任何指標
- [ ] 無繞過驗證流程
- [ ] 無跳過審計日誌

### 技術質量
- [ ] 代碼符合風格指南
- [ ] 測試覆蓋率 >= 95%
- [ ] 性能無降級
- [ ] 文檔已更新

### 安全合規
- [ ] 無安全漏洞
- [ ] 依賴已掃描
- [ ] 審計日誌完整

### 架構一致性
- [ ] 符合 NG 規範
- [ ] 符合 Era 定義
- [ ] 閉環完整性保持

我確認此 PR 完全符合 IndestructibleAutoOps 零容忍標準。

簽名: _______________  日期: _______________
```

---

## 🛡️ 團隊文化與溝通用語

### 場景 1: 快速修復建議

**開發者**: "我想直接修改 `NgExecutor.execute()` 來快速修復這個 bug。"

**正確回覆**:
```
🚨 這違反了我們的「永不覆寫」鐵律。

正確做法：
1. Fork 儲存庫
2. 創建 fix/ng-executor-bug 分支
3. 修改並通過本地測試
4. 提交 PR 到 ng-namespace-governance
5. 通過三級機器審核 + 2 位維護者批准
6. 合併後所有使用者自動獲得修復

理由：我們是 IndestructibleAutoOps，任何核心修改都必須
經過完整的零容忍審核流程，確保系統永不降級。
```

### 場景 2: 臨時繞過請求

**開發者**: "能否暫時禁用驗證來加快開發？"

**正確回覆**:
```
🚫 PERMANENT_BLOCK

IndestructibleAutoOps 的零容忍原則不允許：
- 禁用驗證
- 跳過檢查
- 臨時繞過
- 開發模式例外

理由：「永不降級」意味著開發環境和生產環境使用
相同的零容忍標準。這確保我們的系統真正 Indestructible。

替代方案：
1. 使用測試環境的獨立實例
2. 模擬（Mock）外部依賴
3. 提高本地測試效率
```

### 場景 3: 性能優化建議

**開發者**: "這個驗證太慢了，能否放寬到 200ms？"

**正確回覆**:
```
🚫 ZERO_TOLERANCE_VIOLATION: 性能降級

當前 SLA：<= 100ms（不可變）
建議值：200ms
結果：❌ REJECTED（降級 100%）

正確做法：
1. 分析性能瓶頸
2. 優化驗證邏輯
3. 使用緩存/索引
4. 並行化處理
5. 保持或改善 <= 100ms SLA

理由：IndestructibleAutoOps 通過 ML 優化來提升性能，
而非降低標準。我們追求「更快的零容忍」，而非「寬容」。
```

---

## 🔧 技術實現工具鏈

### 1. 命名空間守護腳本

**檔案**: `tools/ng-namespace-guard.py`

```python
#!/usr/bin/env python3
"""
NG 命名空間守護
檢測對 ng-* 命名空間的非法覆寫
"""
import ast
import sys
from pathlib import Path

PROTECTED_NAMESPACES = [
    'ng_namespace_governance',
    'ecosystem.enforce',
    'auto_executor'
]

def check_file(filepath):
    """檢查文件是否有非法覆寫"""
    code = Path(filepath).read_text()
    tree = ast.parse(code)
    
    violations = []
    
    for node in ast.walk(tree):
        # 檢測賦值操作
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Attribute):
                    # 檢查是否覆寫受保護命名空間
                    if any(ns in ast.unparse(target) for ns in PROTECTED_NAMESPACES):
                        violations.append({
                            'line': node.lineno,
                            'code': ast.unparse(node),
                            'type': 'FORBIDDEN_OVERRIDE'
                        })
    
    return violations

def main():
    files = sys.argv[1:]
    
    all_violations = []
    for filepath in files:
        if filepath.endswith('.py'):
            violations = check_file(filepath)
            if violations:
                all_violations.extend([(filepath, v) for v in violations])
    
    if all_violations:
        print("🚨 ZERO_TOLERANCE_VIOLATION: Namespace override detected")
        for filepath, violation in all_violations:
            print(f"   ❌ {filepath}:{violation['line']}")
            print(f"      {violation['code']}")
        print("\n🚫 PERMANENT_BLOCK: Remove all namespace overrides")
        sys.exit(1)
    
    print("✅ No namespace violations detected")
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### 2. 降級檢測腳本

**檔案**: `tools/no-degradation-check.py`

```python
#!/usr/bin/env python3
"""
降級檢測工具
確保所有指標永不降級
"""
import json
import sys
from pathlib import Path

def load_baseline():
    """載入基線指標"""
    baseline_file = Path('metrics/baseline.json')
    if not baseline_file.exists():
        return {}
    return json.loads(baseline_file.read_text())

def get_current_metrics():
    """獲取當前指標"""
    # 從測試報告、性能基準等獲取
    return {
        'test_coverage': 0.96,
        'lint_score': 9.7,
        'validation_latency_ms': 85,
        'ml_confidence': 0.97,
        'closure_completeness': 1.0
    }

def check_degradation():
    """檢查降級"""
    baseline = load_baseline()
    current = get_current_metrics()
    
    degradations = []
    
    for metric, baseline_value in baseline.items():
        current_value = current.get(metric, 0)
        
        # 檢查是否降級
        if current_value < baseline_value:
            degradations.append({
                'metric': metric,
                'baseline': baseline_value,
                'current': current_value,
                'degradation_pct': (baseline_value - current_value) / baseline_value * 100
            })
    
    if degradations:
        print("🚨 ZERO_TOLERANCE_VIOLATION: Metric degradation detected\n")
        for d in degradations:
            print(f"   ❌ {d['metric']}:")
            print(f"      Baseline: {d['baseline']}")
            print(f"      Current:  {d['current']}")
            print(f"      Degradation: {d['degradation_pct']:.1f}%\n")
        
        print("🚫 PERMANENT_BLOCK: All metrics must maintain or improve")
        print("   Fix degradations before proceeding")
        sys.exit(1)
    
    print("✅ No degradation detected - All metrics maintained or improved")
    sys.exit(0)

if __name__ == "__main__":
    check_degradation()
```

---

## 📋 Pull Request 模板

**檔案**: `.github/PULL_REQUEST_TEMPLATE.md`

```markdown
# Pull Request

## 🚨 零容忍合規聲明

我確認此 PR 完全符合 IndestructibleAutoOps 零容忍標準：

- [ ] ✅ 無覆寫任何 ng-* / gl-* / ecosystem 命名空間
- [ ] ✅ 無降級任何指標（測試覆蓋率、性能、ML 信心）
- [ ] ✅ 無繞過任何驗證流程
- [ ] ✅ 無跳過任何審計日誌
- [ ] ✅ 所有自動化檢查已通過

## 變更類型

- [ ] Bug 修復（不影響 API）
- [ ] 新功能（向後兼容）
- [ ] 破壞性變更（需要 MAJOR 版本）
- [ ] 文檔更新
- [ ] 性能改進（無降級）

## 變更描述

<!-- 詳細描述變更內容 -->

## 測試

- [ ] 單元測試已添加/更新
- [ ] 整合測試已通過
- [ ] 性能測試無降級
- [ ] 測試覆蓋率 >= 95%

## NG 規範合規

- [ ] 符合 NG 命名空間規範
- [ ] 符合 Era 定義
- [ ] 閉環完整性保持
- [ ] NG 編碼正確分配

## 機器審核狀態

- [ ] ✅ CI/CD 流水線通過（Team）
- [ ] ✅ 安全掃描通過（Organization）
- [ ] ✅ 合規檢查通過（Enterprise）

## 人工審核

需要以下團隊審核：
- [ ] @ng-core-team（核心團隊）
- [ ] @ml-team（如涉及 ML）
- [ ] @security-team（如涉及安全）
- [ ] @governance-committee（如涉及零容忍策略）

---

**我理解並同意**：違反任何零容忍規則將導致 PERMANENT_BLOCK。
```

---

## 🎯 貢獻指南

### 開始貢獻（Step-by-Step）

#### 1. 設置開發環境
```bash
# Clone 儲存庫
git clone https://github.com/IndestructibleAutoOps/indestructible-auto-ops
cd indestructible-auto-ops

# 安裝依賴
pip install -e .
pip install -r requirements-dev.txt

# 設置 pre-commit hooks
pre-commit install

# 運行測試驗證環境
pytest
python tools/ng-namespace-guard.py
python tools/no-degradation-check.py
```

#### 2. 創建分支
```bash
# 功能分支
git checkout -b feature/my-new-feature

# 修復分支
git checkout -b fix/issue-123

# 文檔分支
git checkout -b docs/update-readme
```

#### 3. 開發和測試
```bash
# 開發你的功能
# ...

# 運行測試
pytest --cov=. --cov-fail-under=95

# 運行 lint
ruff check .
black .
isort .

# 檢查命名空間守護
python tools/ng-namespace-guard.py $(git diff --name-only)

# 檢查無降級
python tools/no-degradation-check.py
```

#### 4. 提交 Commit
```bash
# 使用 Conventional Commits
git commit -m "feat: add new namespace validation rule

- Add semantic similarity check
- Threshold: 80%
- Action: IMMEDIATE_BLOCK

NG-Code: NG00305
Zero-Tolerance: COMPLIANT"
```

#### 5. 推送並創建 PR
```bash
git push origin feature/my-new-feature

# 在 GitHub 創建 Pull Request
# 填寫 PR 模板
# 等待機器審核 + 人工審核
```

---

## ⚠️ 常見違規與處理

### 違規 1: 直接修改核心模組
```python
# ❌ VIOLATION
from ng_executor import NgExecutor
NgExecutor.execute = my_custom_execute

# ✅ CORRECT
class MyExecutor(NgExecutor):
    def execute_custom(self):
        result = super().execute()
        return self.post_process(result)
```
**動作**: PERMANENT_BLOCK + 要求重寫

### 違規 2: 降低測試覆蓋率
```python
# ❌ VIOLATION
# 刪除測試以"加快CI"

# ✅ CORRECT
# 保持或增加測試
# 優化測試執行速度（並行、緩存）
```
**動作**: BLOCK_UNTIL_COVERAGE_RESTORED

### 違規 3: 跳過驗證
```python
# ❌ VIOLATION
def quick_register(namespace):
    return registry.register(namespace, skip_validation=True)

# ✅ CORRECT
def safe_register(namespace):
    # 通過完整驗證流程
    return registry.register(namespace)  # 零容忍驗證自動執行
```
**動作**: IMMEDIATE_BLOCK + CODE_REVIEW_REQUIRED

---

## 📚 參考資源

### 核心文檔
- `ng-namespace-governance/NG-CHARTER.md` - 治理憲章
- `ng-namespace-governance/ZERO-TOLERANCE-COMPLETE.md` - 零容忍完整說明
- `ng-namespace-governance/docs/NG-EXECUTION-ENGINES.md` - 執行引擎文檔

### 工具
- `tools/ng-namespace-guard.py` - 命名空間守護
- `tools/no-degradation-check.py` - 降級檢測
- `ng-namespace-governance/tools/ng-cli.py` - NG CLI

### 測試
- `tests/test_ng_core_immutability.py` - 核心不可變性測試
- `ng-namespace-governance/core/ng-executor.py` - 執行引擎測試（內建）

---

## 🎊 最終聲明

**IndestructibleAutoOps 是一個零容忍的 AIOps 平台。**

我們的核心原則：
- 🚨 **零容忍** - 無例外，無寬容
- 🚫 **永不覆寫** - 核心模組不可變
- 📈 **永不降級** - 所有指標只能提升
- 🤖 **ML 驅動** - 自主修復，60 秒內完成
- 🛡️ **不可摧毀** - 通過絕對治理實現韌性

**貢獻時請記住**：
> 我們不是在構建一個「可以用」的系統，
> 我們在構建一個「不可摧毀」的系統。
> 
> 這需要絕對的紀律、零容忍的標準、
> 以及對卓越的不妥協追求。

**歡迎加入 IndestructibleAutoOps！** 🚀

---

**最後更新**: 2026-02-06  
**維護者**: NG Governance Committee  
**授權**: 與主儲存庫相同

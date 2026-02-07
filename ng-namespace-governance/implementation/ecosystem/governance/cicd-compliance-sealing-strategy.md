# CI/CD Compliance Sealing Strategy

## 📋 概述

**版本**: 1.0.0
**Era**: 1 (Evidence-Native Bootstrap)
**Layer**: Operational
**日期**: 2026-02-04

本文檔定義了 CI/CD 管道中的合規性封存策略，包括封存條件、合規性閾值（Score Gate）和執行流程。

---

## 🎯 核心原則

### 原則 1: Score Gate - 合規性閾值
**定義**: 所有治理指標必須達到指定閾值才能通過 CI/CD

### 原則 2: Hash Sealing - 雜湊封存
**定義**: 所有通過 CI/CD 的 artifact 必須生成 SHA256 hash 並記錄

### 原則 3: Evidence Chain - 證據鏈
**定義**: 每次構建必須生成完整的證據鏈（事件流 + artifact + hash）

### 原則 4: Fail-Fast - 快速失敗
**定義**: 任何合規性檢查失敗立即終止 CI/CD 管道

---

## 🔢 合規性閾值定義

### 閾值結構

```yaml
compliance_thresholds:
  # 核心治理合規性 (40%)
  core_governance:
    minimum: 100.0
    description: "所有核心治理檢查必須通過"
    checks:
      - gl_compliance
      - naming_conventions
      - security_check
      - evidence_chain
  
  # 語義合規性 (25%)
  semantic_compliance:
    minimum: 85.0
    description: "報告語義合規性必須達到 85/100"
    validator: semantic_validator.py
  
  # 實作完成率 (20%)
  implementation_completion:
    minimum: 80.0
    description: "實作項目完成率必須達到 80%"
    executor: semantic_driven_executor.py
  
  # 驗證通過率 (15%)
  verification_pass_rate:
    minimum: 75.0
    description: "補件驗證通過率必須達到 75%"
    verifier: semantic_driven_executor.py

# 整體閾值
overall_threshold: 85.0
```

### 閾值等級

| 等級 | 閾值範圍 | CI/CD 行為 |
|------|----------|-----------|
| **PASS** | ≥ 85.0 | ✅ 允許合併和部署 |
| **WARNING** | 75.0 - 84.9 | ⚠️ 允許合併，需要手動審查 |
| **FAIL** | < 75.0 | ❌ 阻擋合併和部署 |

---

## 🔐 封存條件

### 條件 1: 核心治理檢查
```yaml
core_governance_check:
  tool: ecosystem/enforce.py
  command: --audit
  required_pass: true
  allowed_failures: 0
```

**規則**:
- ✅ 18/18 檢查必須通過
- ❌ 任何失敗立即阻止 CI/CD

### 條件 2: 語義驗證
```yaml
semantic_validation:
  tool: ecosystem/tools/semantic_validator.py
  command: --report <report_file>
  minimum_score: 85.0
  critical_violations: 0
```

**規則**:
- ✅ 合規性分數 ≥ 85.0
- ❌ 0 個 CRITICAL 違規
- ⚠️ 最多 3 個 HIGH 違規

### 條件 3: 實作清單驗證
```yaml
implementation_checklist:
  tool: ecosystem/tools/semantic_driven_executor.py
  command: --verify-implementation
  minimum_completion: 80.0
  minimum_verification: 75.0
```

**規則**:
- ✅ 實作完成率 ≥ 80.0%
- ✅ 驗證通過率 ≥ 75.0%
- ❌ 無 CRITICAL 級別未完成項目

### 條件 4: 證據鏈驗證
```yaml
evidence_chain_verification:
  tool: ecosystem/tools/auto_verify_report.py
  command: --verify-evidence
  required_artifacts:
    - .governance/event-stream.jsonl
    - .evidence/step-*.json
  required_hashes: true
```

**規則**:
- ✅ 所有 10 個 step artifact 存在
- ✅ 所有 artifact 包含 SHA256 hash
- ✅ 事件流記錄完整

---

## 🚀 CI/CD 管道集成

### Stage 1: 預檢查

```yaml
pre-check:
  - name: 檢查 Git 狀態
    run: git status
    
  - name: 檢查代碼風格
    run: ecosystem/tools/linter.py
    
  - name: 檢查命名約定
    run: python ecosystem/enforce.py --naming-only
```

### Stage 2: 核心治理檢查

```yaml
core-governance:
  - name: 執行 MNGA 治理檢查
    run: python ecosystem/enforce.py --audit
    on_failure: BLOCK_PIPELINE
    
  - name: 檢查結果驗證
    run: |
      if [ $? -ne 0 ]; then
        echo "❌ 核心治理檢查失敗"
        exit 1
      fi
```

### Stage 3: 語義驗證

```yaml
semantic-validation:
  - name: 語義驗證器檢查
    run: |
      python ecosystem/tools/semantic_validator.py \
        --directory reports/ \
        --output semantic-validation.json
    
  - name: 語義合規性評分
    run: |
      score=$(jq '.compliance_score' semantic-validation.json)
      critical=$(jq '.critical_violations' semantic-validation.json)
      
      if (( $(echo "$score < 85.0" | bc -l) )); then
        echo "❌ 語義合規性 $score 低於閾值 85.0"
        exit 1
      fi
      
      if [ "$critical" -gt 0 ]; then
        echo "❌ 發現 $critical 個 CRITICAL 違規"
        exit 1
      fi
```

### Stage 4: 實作驗證

```yaml
implementation-verification:
  - name: 生成實作清單
    run: |
      python ecosystem/tools/semantic_entity_task_converter.py \
        --directory reports/ \
        --output tasks.json
      
      python ecosystem/tools/semantic_driven_executor.py \
        --violations violations.json \
        --tasks tasks.json \
        --generate-checklist \
        --output implementation-checklist.json
    
  - name: 驗證實作補件
    run: |
      python ecosystem/tools/semantic_driven_executor.py \
        --checklist implementation-checklist.json \
        --verify-implementation \
        --output verification-report.json
    
  - name: 實作合規性評分
    run: |
      completion=$(jq '.completion_rate' verification-report.json)
      verification=$(jq '.verification_rate' verification-report.json)
      
      if (( $(echo "$completion < 80.0" | bc -l) )); then
        echo "❌ 實作完成率 $completion 低於閾值 80.0"
        exit 1
      fi
      
      if (( $(echo "$verification < 75.0" | bc -l) )); then
        echo "❌ 驗證通過率 $verification 低於閾值 75.0"
        exit 1
      fi
```

### Stage 5: 證據鏈驗證

```yaml
evidence-verification:
  - name: 執行 10 步閉環
    run: python ecosystem/enforce.rules.py
    
  - name: 驗證事件流
    run: |
      if [ ! -f .governance/event-stream.jsonl ]; then
        echo "❌ 事件流文件不存在"
        exit 1
      fi
      
      events=$(wc -l < .governance/event-stream.jsonl)
      if [ "$events" -lt 10 ]; then
        echo "❌ 事件流記錄不足 ($events < 10)"
        exit 1
      fi
    
  - name: 驗證 Artifacts
    run: |
      for step in {1..10}; do
        if [ ! -f .evidence/step-$step.json ]; then
          echo "❌ Artifact step-$step.json 不存在"
          exit 1
        fi
        
        hash=$(jq -r '.artifact_hash' .evidence/step-$step.json)
        if [ -z "$hash" ] || [ "$hash" == "null" ]; then
          echo "❌ Artifact step-$step.json 缺少 hash"
          exit 1
        fi
      done
```

### Stage 6: 封存

```yaml
sealing:
  - name: 生成 Core Hash
    run: |
      python ecosystem/tools/generate_core_hash.py \
        --artifacts .evidence/*.json \
        --output .governance/core-hash.json
    
  - name: 記錄到事件流
    run: |
      echo '{"event_type": "CORE_HASH_SEALED", "timestamp": "'$(date -Iseconds)'"}' \
        >> .governance/event-stream.jsonl
    
  - name: 提交封存文件
    run: |
      git add .governance/core-hash.json
      git add .governance/event-stream.jsonl
      git commit -m "chore: Seal core artifacts [ci-skip]"
```

---

## 📊 合規性評分計算

### 評分公式

```python
# 整體合規性分數
overall_score = (
    (core_governance_score * 0.40) +
    (semantic_compliance_score * 0.25) +
    (implementation_completion_rate * 0.20) +
    (verification_pass_rate * 0.15)
)
```

### 分數組件詳細說明

#### 1. Core Governance Score (40%)
```python
core_governance_score = (
    (passed_checks / total_checks) * 100
)

# 要求: 必須 = 100.0
```

#### 2. Semantic Compliance Score (25%)
```python
semantic_compliance_score = (
    semantic_validator.score
)

# 要求: ≥ 85.0
```

#### 3. Implementation Completion Rate (20%)
```python
implementation_completion_rate = (
    completed_items / total_items * 100
)

# 要求: ≥ 80.0
```

#### 4. Verification Pass Rate (15%)
```python
verification_pass_rate = (
    verified_items / total_items * 100
)

# 要求: ≥ 75.0
```

---

## 🔄 違規處理策略

### CRITICAL 違規處理
```yaml
critical_violations:
  action: BLOCK_PIPELINE
  notification: true
  required_fix: before_merge
  auto_assignee: governance_team
```

### HIGH 違規處理
```yaml
high_violations:
  action: WARNING
  max_allowed: 3
  notification: true
  required_fix: before_merge
```

### MEDIUM 違規處理
```yaml
medium_violations:
  action: ALLOW
  max_allowed: 10
  notification: false
  required_fix: within_sprint
```

### LOW 違規處理
```yaml
low_violations:
  action: ALLOW
  max_allowed: unlimited
  notification: false
  required_fix: backlog
```

---

## 🚨 閘門規則

### Gate 1: Pull Request 閘門
```yaml
pr_gate:
  conditions:
    - overall_score >= 85.0
    - core_governance_score == 100.0
    - critical_violations == 0
    - high_violations <= 3
  
  on_fail:
    - "❌ 無法合併 PR"
    - "📧 發送通知給提交者"
    - "📋 創建 GitHub Issue 追蹤修復"
```

### Gate 2: 合併閘門
```yaml
merge_gate:
  conditions:
    - overall_score >= 85.0
    - implementation_completion_rate >= 80.0
    - verification_pass_rate >= 75.0
  
  on_fail:
    - "❌ 無法合併到 main"
    - "📧 發送通知給團隊"
    - "🔄 觸發自動修復流程"
```

### Gate 3: 部署閘門
```yaml
deployment_gate:
  conditions:
    - overall_score >= 90.0
    - all_artifacts_sealed: true
    - evidence_chain_complete: true
  
  on_fail:
    - "❌ 無法部署到生產環境"
    - "📧 發送緊急通知"
    - "👥 要求人工審批"
```

---

## 📝 報告生成

### CI/CD 報告格式

```yaml
cicd_compliance_report:
  pipeline_id: "ci-20260204-123456"
  timestamp: "2026-02-04T12:00:00Z"
  status: "PASS"  # PASS, WARNING, FAIL
  
  # 核心指標
  core_governance_score: 100.0
  semantic_compliance_score: 87.5
  implementation_completion_rate: 85.0
  verification_pass_rate: 80.0
  overall_score: 88.0
  
  # 違規統計
  violations:
    critical: 0
    high: 2
    medium: 5
    low: 8
  
  # 封存狀態
  sealing:
    core_hash: "abc123..."
    artifacts_sealed: 10
    evidence_chain_complete: true
  
  # 閘門狀態
  gates:
    pr_gate: PASS
    merge_gate: PASS
    deployment_gate: WARNING
  
  # 動作
  actions:
    - "✅ 允許合併到 main"
    - "⚠️ 需要人工審查才能部署到生產"
```

---

## 🛠️ 工具整合

### 工具調用順序

```bash
# 1. 核心治理檢查
python ecosystem/enforce.py --audit
# 輸出: reports/audit_report_*.json

# 2. 語義驗證
python ecosystem/tools/semantic_validator.py --directory reports/
# 輸出: semantic-validation.json

# 3. 任務生成
python ecosystem/tools/semantic_entity_task_converter.py \
  --from-validator semantic-validation.json
# 輸出: tasks.json

# 4. 實作清單生成
python ecosystem/tools/semantic_driven_executor.py \
  --violations violations.json \
  --tasks tasks.json \
  --generate-checklist
# 輸出: implementation-checklist.json

# 5. 實作驗證
python ecosystem/tools/semantic_driven_executor.py \
  --checklist implementation-checklist.json \
  --verify-implementation
# 輸出: verification-report.json

# 6. 證據鏈生成
python ecosystem/enforce.rules.py
# 輸出: .evidence/step-*.json, .governance/event-stream.jsonl

# 7. 封存
python ecosystem/tools/generate_core_hash.py
# 輸出: .governance/core-hash.json
```

---

## ✅ Era-1 特殊規則

### 規則 1: 部分封存
- ✅ 允許部分 artifact 封存
- ⏸️ 不要求完整 core hash 封存

### 規則 2: 非阻擋性警告
- ✅ MEDIUM 和 LOW 違規不阻止 CI/CD
- ⚠️ 只發送警告通知

### 規則 3: 柔性閾值
- ✅ 可以臨時降低閾值進行緊急修復
- 📝 需要記錄降低原因和期限

---

## 🎯 成功標準

### CI/CD 通過標準
```
✅ Core Governance Score = 100.0 (18/18 checks PASS)
✅ Semantic Compliance Score ≥ 85.0
✅ Implementation Completion Rate ≥ 80.0
✅ Verification Pass Rate ≥ 75.0
✅ Overall Score ≥ 85.0
✅ 0 CRITICAL violations
✅ ≤ 3 HIGH violations
✅ All artifacts generated with SHA256 hashes
✅ Event stream complete
✅ Evidence chain intact
```

### PR 合併標準
```
✅ All CI/CD checks pass
✅ Code review approved
✅ At least 1 approval required
✅ No unresolved conversations
```

### 部署標準
```
✅ Overall Score ≥ 90.0 (higher threshold)
✅ All critical issues resolved
✅ Manual approval required
✅ Deployment checklist completed
```

---

## 📈 合規性趨勢追蹤

### 趨勢指標
- 每次提交的合規性分數
- 違規數量趨勢
- 實作完成率趨勢
- 驗證通過率趨勢

### 目標
- 每週提高合規性分數 2-3%
- 每月減少 CRITICAL 違規 20%
- 每月提高實作完成率 5%

---

## 🔗 相關文檔

- `ecosystem/governance/enforcement.rules.yaml` - 強制執行規則
- `ecosystem/governance/reporting-governance-spec.md` - 報告治理規範
- `ecosystem/tools/semantic_validator.py` - 語義驗證器
- `ecosystem/tools/semantic_entity_task_converter.py` - 任務轉換器
- `ecosystem/tools/semantic_driven_executor.py` - 執行引擎
- `ecosystem/tools/auto_verify_report.py` - 自動驗證工具

---

**文檔版本**: 1.0.0
**最後更新**: 2026-02-04
**維護者**: Governance Layer
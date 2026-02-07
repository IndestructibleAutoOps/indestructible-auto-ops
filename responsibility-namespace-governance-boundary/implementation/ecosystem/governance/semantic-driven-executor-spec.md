# Semantic-Driven Governance Executor Specification

## 📋 概述

語義驅動治理實作引擎（Semantic-Driven Governance Executor）將傳統的「驗證器」升級為「實作引擎」，不僅檢測問題，還自動生成解決方案並驗證實作完整性。

## 🎯 核心能力

### 1. 檢測層 (Detection Layer)
- **來源**: `semantic_validator.py`
- **功能**: 
  - 語義違規檢測
  - 合規性評分 (0-100)
  - 違規分類 (CRITICAL, HIGH, MEDIUM, LOW)

### 2. 轉換層 (Transformation Layer)
- **來源**: `semantic_entity_task_converter.py`
- **功能**:
  - 違規 → 可執行任務轉換
  - 任務優先級分配
  - 工作量估算
  - 任務依賴分析

### 3. 實作清單生成層 (Implementation Checklist Generation Layer)
- **新功能**
- **功能**:
  - 根據違規類型生成補件清單
  - 定義每個補件的要求（文件類型、內容、證據）
  - 生成實作指南

### 4. 驗證層 (Verification Layer)
- **新功能**
- **功能**:
  - ✅ 文件存在性驗證 - 檢查補件文件是否存在
  - ✅ 事件流驗證 - 檢查 `.governance/event-stream.jsonl` 是否有相關記錄
  - ✅ Artifact 驗證 - 檢查 `.evidence/step-*.json` 是否存在
  - ✅ Hash 驗證 - 檢查 artifact 是否包含 SHA256 hash
  - ✅ 封存驗證 - 檢查是否在 core-hash.json 中記錄

### 5. 執行層 (Execution Layer)
- **新功能**
- **功能**:
  - 補件狀態追蹤 (pending, in_progress, completed, verified)
  - 合規性趨勢追蹤
  - 進度報告生成

## 🔧 核心組件

### 1. ImplementationItem
```python
@dataclass
class ImplementationItem:
    item_id: str
    name: str
    type: str  # 'tool', 'phase', 'terminology', 'artifact', 'document'
    required_artifacts: List[str]
    required_evidence: List[str]
    required_hash: bool
    required_sealing: bool
    status: str  # 'pending', 'in_progress', 'completed', 'verified'
    verification_results: Dict[str, bool]
    created_at: str
    updated_at: str
```

### 2. ImplementationChecklist
```python
@dataclass
class ImplementationChecklist:
    checklist_id: str
    report_file: str
    violations: List[Violation]
    tasks: List[Task]
    items: List[ImplementationItem]
    completion_rate: float
    verification_rate: float
    created_at: str
```

### 3. VerificationEngine
```python
class VerificationEngine:
    def verify_file_exists(self, path: str) -> bool
    def verify_event_stream(self, event_type: str) -> bool
    def verify_artifact(self, step: int) -> bool
    def verify_hash(self, artifact_path: str) -> bool
    def verify_sealing(self, item_id: str) -> bool
```

## 📊 驗證規則

### 文件存在性驗證
- **規則**: `pathlib.Path(file_path).exists()`
- **通過**: 文件存在
- **失敗**: 文件不存在

### 事件流驗證
- **規則**: 檢查 `.governance/event-stream.jsonl` 中是否有相關事件
- **通過**: 找到至少一個匹配的事件
- **失敗**: 沒有找到匹配的事件

### Artifact 驗證
- **規則**: 檢查 `.evidence/step-*.json` 是否存在
- **通過**: artifact 文件存在且格式正確
- **失敗**: artifact 文件不存在或格式錯誤

### Hash 驗證
- **規則**: artifact JSON 包含 `artifact_hash` 欄位（SHA256）
- **通過**: hash 欄位存在且格式正確
- **失敗**: hash 欄位不存在或格式錯誤

### 封存驗證
- **規則**: 檢查 `.governance/core-hash.json` 中是否有記錄
- **通過**: 找到封存記錄
- **失敗**: 沒有找到封存記錄（ Era-1 可以 PASS）

## 🎬 執行流程

```python
# 步驟 1: 檢測違規
violations = semantic_validator.validate_report(report_file)

# 步驟 2: 轉換為任務
tasks = setc.convert_violations_to_tasks(violations)

# 步驟 3: 生成實作清單
checklist = executor.generate_implementation_checklist(violations, tasks)

# 步驟 4: 驗證補件
for item in checklist.items:
    verification = verification_engine.verify_item(item)
    item.verification_results = verification

# 步驟 5: 計算完成率
checklist.completion_rate = calculate_completion_rate(checklist.items)
checklist.verification_rate = calculate_verification_rate(checklist.items)

# 步驟 6: 生成報告
report = executor.generate_report(checklist)
```

## 📈 輸出格式

### 1. 實作清單報告
```markdown
# Implementation Checklist Report

## Report: example-report.md
- Violations: 15
- Tasks: 20
- Implementation Items: 25
- Completion Rate: 40%
- Verification Rate: 20%

## Implementation Items

### ✅ ITEM-001: Register tool 'semantic_validator.py'
- Type: tool
- Status: completed
- File Exists: ✅
- Event Stream: ✅
- Artifact: ✅
- Hash: ✅
- Sealing: ⏸️ (Era-1)

### ⏸️ ITEM-002: Define terminology '治理平台'
- Type: terminology
- Status: pending
- File Exists: ❌
- Event Stream: ❌
- Artifact: ❌
- Hash: ❌
- Sealing: ❌

[...]
```

### 2. 補件驗證矩陣
```markdown
## Verification Matrix

| Item ID | Type | Status | File | Events | Artifact | Hash | Sealing |
|---------|------|--------|------|--------|----------|------|---------|
| ITEM-001 | tool | ✅ | ✅ | ✅ | ✅ | ✅ | ⏸️ |
| ITEM-002 | terminology | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
[...]
```

## 🔄 合規性計算

### 整體合規性分數
```python
overall_score = (
    (semantic_compliance_score * 0.4) +  # 語義合規性
    (task_completion_rate * 0.3) +       # 任務完成率
    (verification_rate * 0.3)            # 驗證通過率
)
```

### 實作完成率
```python
completion_rate = (completed_items / total_items) * 100
```

### 驗證通過率
```python
verification_rate = (verified_items / total_items) * 100
```

## 🚀 使用方式

```bash
# 完整執行流程
python ecosystem/tools/semantic_driven_executor.py \
    --report reports/example.md \
    --generate-checklist \
    --verify-implementation \
    --output reports/implementation-checklist.md

# 只生成清單
python ecosystem/tools/semantic_driven_executor.py \
    --report reports/example.md \
    --generate-checklist \
    --output reports/implementation-checklist.md

# 只驗證現有實作
python ecosystem/tools/semantic_driven_executor.py \
    --checklist reports/implementation-checklist.md \
    --verify-implementation \
    --output reports/verification-report.md
```

## 📁 輸出文件

1. **Implementation Checklist** - `reports/implementation-checklist-{timestamp}.md`
2. **Verification Matrix** - `reports/verification-matrix-{timestamp}.md`
3. **Status Report** - `reports/implementation-status-{timestamp}.md`
4. **JSON Export** - `.governance/checklists/checklist-{id}.json`

## ✅ 驗證標準

### 通過標準
- 語義合規性 ≥ 80
- 實作完成率 ≥ 80
- 驗證通過率 ≥ 80
- 無 CRITICAL 級別未驗證項目

### Era-1 特殊規則
- Sealing 驗證可跳過（Era-1 不封存）
- Semantic Closure 必須為 NO
- Layer 必須為 Operational

## 🔗 整合點

1. **semantic_validator.py** - 違規檢測和合規性評分
2. **semantic_entity_task_converter.py** - 任務生成
3. **enforce.rules.py** - 事件流和 artifact 生成
4. **.governance/event-stream.jsonl** - 事件流驗證
5. **.evidence/step-*.json** - artifact 驗證
6. **.governance/core-hash.json** - 封存驗證
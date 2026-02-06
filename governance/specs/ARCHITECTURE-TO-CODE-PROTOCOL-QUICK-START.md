# Architecture-to-Code Protocol (ATCP) - Quick Start Guide
# GL Unified Charter Strategy Baseline Integration
# Version: 2.0.0

---

## What is ATCP?

ATCP (Architecture-to-Code Protocol) is a **mapping protocol** that transforms abstract architecture specifications into executable code that AI code editors can understand and implement.

**核心解決方案：**
- 將抽象架構規格（如 GL-5L）分解為具體模組
- 提供每個模組的最小可用實作（MVE）定義
- 建立完整的實作優先順序和依賴關係
- 封存證據鏈以確保可追溯性和可驗證性

---

## How It Works

### 三層映射模型

```
架構規格 (Architecture Specifications)
    ↓ [Layer 1: 架構分解]
模組分解圖 (Module Decomposition)
    ↓ [Layer 2: 模組實作]
具體程式碼 + 測試 (Code + Tests)
    ↓ [Layer 3: 一站式集成]
完整系統 + 證據封存 (System + Evidence)
```

---

## Quick Start: 3-Step Process

### Step 1: 觸發 AI 架構模式

給 AI 以下指令：

```yaml
ENTER ARCHITECTURE_TO_CODE_MODE

architecture_spec: ecosystem/governance/specs/backend-governance-responsibility.md
target_layers: [Layer 1]
mode: ONE_SHOT_INTEGRATION

constraints:
  no_placeholders: true
  minimum_viable: true
  test_coverage: ">= 80%"
  evidence_chain: true
```

### Step 2: AI 自動執行

AI 將自動執行以下流程：

1. **分析架構規格** - 讀取並解析架構文件
2. **分解為模組** - 產生模組分解圖
3. **按優先順序實作** - 依次實作每個模組
4. **生成測試案例** - 自動生成測試
5. **封存證據鏈** - 產生完整的證據鏈

### Step 3: 驗證結果

```bash
# 運行測試
pytest tests/kernel/semantic/

# 查看證據鏈
cat evidence/implementation/layer1-semantic/implementation-trace.json

# 驗證治理合規性
python ecosystem/enforce.py
```

---

## 實作範例：Layer 1 Semantic Layer

### 模組 1: SemanticTokenizer (Priority 1)

**輸入：**
```
"創建用戶 alice@example.com"
```

**輸出：**
```python
[
  SemanticToken(type="ACTION", value="創建", canonical="create"),
  SemanticToken(type="ENTITY", value="用戶", canonical="user"),
  SemanticToken(type="IDENTIFIER", value="alice@example.com", canonical="alice@example.com")
]
```

**關鍵特性：**
- ✅ 語言中立（中英文產生相同的 canonical）
- ✅ 可重放（可用於跨 AI 模型的語意重放）
- ✅ 可封存（完整的證據鏈）

---

## 文件結構

```
governance/specs/
├── ARCHITECTURE-TO-CODE-PROTOCOL.md           # 完整協定文件
├── ARCHITECTURE-TO-CODE-PROTOCOL-QUICK-START.md  # 本快速開始指南
└── BACKEND-GOVERNANCE-RESPONSIBILITY.md       # 架構規格源文件

.governance/implementation/
└── layer1-decomposition.yaml                  # 模組分解圖

governance/kernel/semantic/                    # 產出的程式碼
├── __init__.py
├── tokenizer.py                               # SemanticTokenizer
├── ast_builder.py                             # SemanticAST
├── hasher.py                                  # SemanticHasher
├── canonicalizer.py                           # SemanticCanonicalizer
└── multilang_evidence.py                      # MultiLanguageEvidence

tests/kernel/semantic/                         # 產出的測試
└── test_tokenizer.py

evidence/implementation/layer1-semantic/       # 證據鏈
└── implementation-trace.json
```

---

## 關鍵概念

### 1. 最小可用實作 (MVE)

每個模組的第一版必須：
- ✅ 可編譯（語法正確）
- ✅ 可測試（至少 1 個測試通過）
- ✅ 可整合（符合輸入/輸出契約）
- ✅ 不完美（功能可以簡化，但不能虛構）

### 2. 語言中立性

相同語意的不同語言表達必須產生相同的 canonical token：

```python
# 中文
"創建用戶 alice" → canonical: ["create", "user", "alice"]

# 英文
"create user alice" → canonical: ["create", "user", "alice"]

# 結果相同！
```

### 3. 證據鏈封存

每個實作都產生完整的證據鏈：

```json
{
  "proof_chain": {
    "architecture_spec_hash": "sha256:...",
    "decomposition_hash": "sha256:...",
    "implementation_hash": "sha256:...",
    "test_hash": "sha256:...",
    "evidence_hash": "sha256:..."
  }
}
```

---

## 實作順序

### Layer 1 (Semantic Layer) - 9.5 小時

```yaml
Phase 1 (2h): semantic_tokenizer
  ↓
Phase 2 (3.5h, 可並行): semantic_ast + semantic_canonicalizer
  ↓
Phase 3 (2h): semantic_hasher
  ↓
Phase 4 (2h): multilang_evidence
```

### Layer 2-5 (待實作)

依照 GL-5L 依賴關係順序實作...

---

## 治理合規性

ATCP 完全符合專案治理規範：

- ✅ **GL-Naming-Ontology**: 所有命名符合規範
- ✅ **GL-Governance-Layers**: 遵循 GL-5L 架構
- ✅ **GL-Validation-Rules**: 通過所有驗證器
- ✅ **Evidence Chain**: 完整的證據鏈封存
- ✅ **Semantic Sealing**: 語言中立性保證

---

## 與全球最佳實踐對齊

### Spec-Driven Development (SDD) - 2025

- ✅ Specification-First: 基於明確的架構規格
- ✅ Proof-Carrying Artifacts: 可驗證的證據
- ✅ Automated Compliance: 自動檢查治理合規性

### Model-Driven Engineering (MDE)

- ✅ Model-Based: 架構規格作為源模型
- ✅ Transformative: 自動轉換為程式碼
- ✅ Traceable: 完整的追溯鏈

---

## 常見問題

### Q1: 為什麼需要這個協定？

**A:** 抽象的架構規格（如「語意層必須負責語意封存」）無法直接被 AI 理解並轉換為程式碼。ATCP 提供了中間的映射協定。

### Q2: 什麼是最小可用實作 (MVE)？

**A:** MVE 是第一版實作的最低標準：可編譯、可測試、可整合、不完美。它確保每個模組都可以立即使用，但不必一次完成所有功能。

### Q3: 語言中立性為什麼重要？

**A:** 語言中立性確保相同語意的不同語言表達產生相同的 canonical token，這對於語意封存和跨語言重放至關重要。

### Q4: 證據鏈的作用是什麼？

**A:** 證據鏈提供完整的追溯性，從架構規格到實作程式碼的每個步驟都有可驗證的證據，確保 Governance Closure。

### Q5: 如何開始使用？

**A:** 按照「Quick Start: 3-Step Process」執行即可。觸發 ATCP 模式，AI 將自動執行所有步驟。

---

## 下一步

1. **審閱協定文件** - 閱讀完整的 ARCHITECTURE-TO-CODE-PROTOCOL.md
2. **觸發 AI 實作** - 使用 Step 1 的指令開始實作
3. **驗證結果** - 運行測試和治理檢查
4. **封存證據** - 確保證據鏈完整

---

## 參考資源

- [完整協定文件](./ARCHITECTURE-TO-CODE-PROTOCOL.md)
- [架構規格](./BACKEND-GOVERNANCE-RESPONSIBILITY.md)
- [模組分解圖](../../.governance/implementation/layer1-decomposition.yaml)
- [治理檢查工具](../../ecosystem/enforce.py)

---

**GL Unified Charter Activated: YES**
**Status: READY_FOR_EXECUTION**
**Era: Era-1 (Evidence-Native Bootstrap)**
# Architecture-to-Code Protocol
# 抽象架構 → 具體實作 的一站式執行協定
# Version: 1.0.0
# Status: CANONICAL
# GL Level: GL50
# Namespace: /governance/specs

## 協定目的

**讓 AI 程式碼編輯器能夠：**
1. 理解抽象架構規格
2. 自動拆解為可實作模組
3. 按正確順序產出所有程式碼
4. 一次性完成整個系統

## 核心理念

```
抽象 ─[映射協定]→ 具體

架構規格 (WHAT)     → 模組定義 (HOW)
治理責任 (WHY)      → 類別/函式 (CODE)
驗收標準 (VERIFY)   → 測試案例 (TEST)
證據鏈 (EVIDENCE)   → 實作追蹤 (TRACE)
```

---

## Phase 1: 架構分解 (Architecture Decomposition)

### 1.1 輸入規格

抽象架構規格，例如：

```yaml
# 來自: governance/specs/BACKEND-GOVERNANCE-RESPONSIBILITY.md
Layer 1: 語意層 (Semantic Layer)
  責任:
    - 語意 Token 化
    - 語意 AST 建構
    - 語言中立 Hash
    - 多語言對照封存
    - 語意正規化
  
  驗收標準:
    - 同一語意在不同語言產生相同 hash
    - AST 可反序列化
    - 支援中英文
    - 證據鏈完整
```

### 1.2 模組分解

**產出: `module-map.yaml`**

```yaml
# 模組映射圖
# Namespace: /governance/kernel/semantic
# GL Level: GL50

modules:
  semantic_tokenizer:
    type: class
    file: governance/kernel/semantic/tokenizer.py
    responsibility: "語意 Token 化"
    dependencies: []
    priority: 1  # 最高優先級（無依賴）
    test_file: tests/kernel/semantic/test_tokenizer.py
    test_coverage_target: ">= 90%"
    
  semantic_ast:
    type: class
    file: governance/kernel/semantic/ast_builder.py
    responsibility: "語意 AST 建構"
    dependencies: [semantic_tokenizer]
    priority: 2
    test_file: tests/kernel/semantic/test_ast.py
    test_coverage_target: ">= 90%"
    
  semantic_hasher:
    type: class
    file: governance/kernel/semantic/hasher.py
    responsibility: "語言中立 Hash"
    dependencies: [semantic_tokenizer, semantic_ast]
    priority: 3
    test_file: tests/kernel/semantic/test_hasher.py
    test_coverage_target: ">= 95%"
    
  multilang_evidence:
    type: class
    file: governance/kernel/semantic/multilang_evidence.py
    responsibility: "多語言對照封存"
    dependencies: [semantic_hasher]
    priority: 4
    test_file: tests/kernel/semantic/test_multilang_evidence.py
    test_coverage_target: ">= 85%"
    
  semantic_canonicalizer:
    type: class
    file: governance/kernel/semantic/canonicalizer.py
    responsibility: "語意正規化"
    dependencies: [semantic_tokenizer, semantic_ast]
    priority: 3
    test_file: tests/kernel/semantic/test_canonicalizer.py
    test_coverage_target: ">= 90%"
```

### 1.3 依賴圖

**實作依賴圖 (Implementation Dependency Graph)**

```
semantic_tokenizer (Priority 1)
    ↓
semantic_ast (Priority 2)
semantic_canonicalizer (Priority 3)
    ↓
semantic_hasher (Priority 3)
    ↓
multilang_evidence (Priority 4)
```

**實作順序:**
```
1. semantic_tokenizer (無依賴)
2. semantic_ast (依賴 tokenizer)
3. semantic_canonicalizer (依賴 tokenizer)
4. semantic_hasher (依賴 tokenizer, ast)
5. multilang_evidence (依賴 hasher)
```

---

## Phase 2: 模組最小可用實作 (Minimum Viable Module)

### 2.1 MVE 原則

每個模組的第一版必須：
1. **可編譯** - 語法正確，無佔位符
2. **可測試** - 至少 1 個測試通過
3. **可整合** - 符合輸入/輸出契約
4. **不完美** - 功能可以簡化，但不能虛構

### 2.2 模組實作模板

```yaml
# 模組: semantic_tokenizer
# 檔案: governance/kernel/semantic/tokenizer.py

implementation_spec:
  class_name: SemanticTokenizer
  
  purpose: |
    將自然語言轉換為語意 token 序列
    支援多語言，產生語言中立的 canonical 表示
  
  methods:
    - name: tokenize
      signature: "tokenize(text: str, language: str = 'auto') -> List[SemanticToken]"
      purpose: "將文本轉換為語意 token"
      
      minimum_implementation: |
        # 最小實作（先支援基礎動詞）
        BASIC_ACTIONS = {
          "創建": "create", "create": "create",
          "刪除": "delete", "delete": "delete",
          "修改": "update", "update": "update"
        }
        
        tokens = []
        words = text.lower().split()
        
        for word in words:
          if word in BASIC_ACTIONS:
            tokens.append(SemanticToken(
              type="ACTION",
              value=word,
              canonical=BASIC_ACTIONS[word]
            ))
          else:
            tokens.append(SemanticToken(
              type="IDENTIFIER",
              value=word,
              canonical=word
            ))
        
        return tokens
      
      test_cases:
        - input: "創建用戶 alice"
          expected_output: |
            [
              SemanticToken(type="ACTION", value="創建", canonical="create"),
              SemanticToken(type="ENTITY", value="用戶", canonical="用戶"),
              SemanticToken(type="IDENTIFIER", value="alice", canonical="alice")
            ]
        
        - input: "create user alice"
          expected_output: |
            [
              SemanticToken(type="ACTION", value="create", canonical="create"),
              SemanticToken(type="ENTITY", value="user", canonical="user"),
              SemanticToken(type="IDENTIFIER", value="alice", canonical="alice")
            ]
        
        - input: "創建用戶 alice 然後 刪除用戶 bob"
          expected_output: |
            [
              SemanticToken(type="ACTION", value="創建", canonical="create"),
              SemanticToken(type="ENTITY", value="用戶", canonical="user"),
              SemanticToken(type="IDENTIFIER", value="alice", canonical="alice"),
              SemanticToken(type="ACTION", value="刪除", canonical="delete"),
              SemanticToken(type="ENTITY", value="用戶", canonical="user"),
              SemanticToken(type="IDENTIFIER", value="bob", canonical="bob")
            ]
  
  data_classes:
    - name: SemanticToken
      fields:
        - name: type
          type: str
          description: "Token 類型 (ACTION, ENTITY, IDENTIFIER, CONDITION, VALUE)"
        - name: value
          type: str
          description: "原始值"
        - name: canonical
          type: str
          description: "標準化值（語言中立）"
        - name: metadata
          type: Dict[str, Any]
          description: "額外元數據"
          default: field(default_factory=dict)
      
      methods:
        - name: to_dict
          return_type: Dict[str, Any]
          purpose: "轉換為字典格式"
```

### 2.3 測試契約

每個模組必須包含：

```python
# 測試契約規範
class TestSemanticTokenizer:
    """Semantic Tokenizer 測試契約"""
    
    # 功能測試
    def test_basic_tokenization_chinese(self):
        """測試基礎中文 tokenization"""
        
    def test_basic_tokenization_english(self):
        """測試基礎英文 tokenization"""
        
    # 行為測試
    def test_language_neutrality(self):
        """測試語言中立性（相同語意產生相同 canonical）"""
        
    # 邊界測試
    def test_empty_input(self):
        """測試空輸入"""
        
    def test_special_characters(self):
        """測試特殊字符"""
```

---

## Phase 3: AI 執行協定 (AI Execution Protocol)

### 3.1 觸發格式

```yaml
ENTER ARCHITECTURE_TO_CODE MODE

architecture_spec: governance/specs/BACKEND-GOVERNANCE-RESPONSIBILITY.md
target_layers: [Layer 1]  # 先實作 Layer 1
mode: ONE_SHOT_INTEGRATION

output_format:
  - code_files: governance/kernel/semantic/*.py
  - test_files: tests/kernel/semantic/*.py
  - evidence: evidence/implementation/layer1-semantic/
  
constraints:
  - no_placeholders: true
  - minimum_viable: true
  - test_coverage: ">= 80%"
  - evidence_chain: true
  
alignment:
  - namespace: /governance/kernel/semantic
  - gl_level: GL50
  - mnga_version: v2.0
  - naming_ontology: gov-naming-ontology v1.0.0
```

### 3.2 AI 回應格式

```yaml
mode: ARCHITECTURE_TO_CODE
status: DECOMPOSING

# Phase 1: 架構分解
module_decomposition:
  total_modules: 5
  implementation_order:
    - priority_1: [semantic_tokenizer]
    - priority_2: [semantic_ast]
    - priority_3: [semantic_hasher, semantic_canonicalizer]
    - priority_4: [multilang_evidence]

# Phase 2: 開始實作
current_phase: IMPLEMENTATION
current_module: semantic_tokenizer (1/5)

implementation_plan:
  file: governance/kernel/semantic/tokenizer.py
  lines_estimated: 150
  test_file: tests/kernel/semantic/test_tokenizer.py
  test_cases: 5
  
proceed: true
```

### 3.3 AI 產出序列

```
=== Phase 1: Module Decomposition ===

=== path: .governance/implementation/layer1-decomposition.yaml ===
[module-map.yaml 內容]

=== Phase 2: Module Implementation (Priority 1) ===

=== path: governance/kernel/semantic/__init__.py ===
[package initialization]

=== path: governance/kernel/semantic/tokenizer.py ===
[tokenizer implementation]

=== path: tests/kernel/semantic/test_tokenizer.py ===
[tokenizer tests]

=== path: evidence/implementation/layer1-semantic/tokenizer-implemented.json ===
[implementation evidence]

=== Phase 3: Module Implementation (Priority 2) ===

=== path: governance/kernel/semantic/ast_builder.py ===
[AST builder implementation]

=== path: tests/kernel/semantic/test_ast.py ===
[AST tests]

=== path: evidence/implementation/layer1-semantic/ast-implemented.json ===
[implementation evidence]

[Continue for all modules...]

=== Phase 4: Integration ===

=== path: governance/kernel/semantic/integration.py ===
[integration layer]

=== Phase 5: Evidence Sealing ===

=== path: evidence/implementation/layer1-semantic/evidence-chain.json ===
[complete evidence chain]

=== path: evidence/implementation/layer1-semantic/implementation-seal.json ===
[implementation seal with SHA256]

=== Phase 6: Summary ===

{
  "status": "COMPLETE",
  "modules_implemented": 5,
  "total_lines_of_code": 847,
  "test_cases": 27,
  "test_coverage": "92.3%",
  "evidence_chain_sealed": true,
  "evidence_hash": "sha256:abc123...",
  "next_phase": "Layer 2 - Evidence Layer"
}
```

---

## Phase 4: 證據鏈封存 (Evidence Chain Sealing)

### 4.1 實作追蹤

每個模組實作時產生：

```json
{
  "module": "semantic_tokenizer",
  "file": "governance/kernel/semantic/tokenizer.py",
  "implementation_started_at": "2024-02-05T16:00:00Z",
  "implementation_completed_at": "2024-02-05T16:05:00Z",
  "lines_of_code": 187,
  "test_file": "tests/kernel/semantic/test_tokenizer.py",
  "test_cases": 8,
  "test_coverage": "94.2%",
  "implementation_hash": "sha256:abc123...",
  "test_results": {
    "total": 8,
    "passed": 8,
    "failed": 0,
    "skipped": 0
  },
  "dependencies_satisfied": true
}
```

### 4.2 完整證據鏈

所有模組完成後產生：

```json
{
  "layer": "Layer 1 - Semantic Layer",
  "implementation_started_at": "2024-02-05T16:00:00Z",
  "implementation_completed_at": "2024-02-05T16:30:00Z",
  
  "modules_implemented": [
    {...},
    {...},
    {...}
  ],
  
  "test_results": {
    "total": 27,
    "passed": 27,
    "failed": 0,
    "coverage": "92.3%"
  },
  
  "integration_tests": {
    "total": 5,
    "passed": 5
  },
  
  "evidence_chain_hash": "sha256:xyz789...",
  "evidence_sealed": true,
  "seal_timestamp": "2024-02-05T16:31:00Z",
  
  "next_priority": {
    "layer": "Layer 2",
    "modules": ["evidence_collector", "evidence_validator"]
  }
}
```

### 4.3 實作封存

```json
{
  "implementation_seal": {
    "version": "1.0.0",
    "sealed_at": "2024-02-05T16:31:00Z",
    "sealed_by": "AI-CODE-GENERATOR",
    "layer": "Layer 1 - Semantic Layer",
    
    "integrity": {
      "total_modules": 5,
      "all_compilable": true,
      "all_tests_passed": true,
      "coverage": "92.3%",
      "evidence_chain_complete": true
    },
    
    "hashes": {
      "implementation_trace": "sha256:abc123...",
      "evidence_chain": "sha256:def456...",
      "combined_seal": "sha256:ghi789..."
    },
    
    "mnga_compliance": {
      "gl_level": "GL50",
      "mnga_version": "v2.0",
      "evidence_native": true,
      "traceability": "complete",
      "replayability": "enabled"
    }
  }
}
```

---

## Global Best Practices Integration

### 1. Domain-Driven Design (DDD)

**應用：**
- **Bounded Contexts** - 每個 GL 層作為獨立的 bounded context
- **Ubiquitous Language** - 統一的術語（SemanticToken, AST, Canonical）
- **Aggregates** - 相關模組聚合（Semantic Layer = 5 modules）

**實作：**
```python
# Bounded Context: Semantic Layer
# Ubiquitous Language: SemanticToken, AST, Canonical
class SemanticLayerAggregate:
    """
    Semantic Layer Aggregate Root
    Coordinates all semantic processing modules
    """
```

### 2. Clean Architecture

**應用：**
- **Dependency Inversion** - 高層模組不依賴低層模組
- **Layer Separation** - 清晰的層次結構
- **Business Logic Isolation** - 治理邏輯與技術實作分離

**實作：**
```python
# Layer 1: Semantic Layer (Business Logic)
# Layer 2: Evidence Layer (Business Logic)
# Layer 3: Storage Layer (Technical Infrastructure)
```

### 3. Test-Driven Development (TDD)

**應用：**
- **Test-First** - 先寫測試，再寫實作
- **Test Contracts** - 測試案例作為輸入/輸出契約
- **High Coverage** - >= 80% 測試覆蓋率

**實作：**
```python
# Test contract defines expected behavior
def test_language_neutrality(self):
    """
    Test: Language Neutrality
    Contract: Same semantic meaning produces same canonical across languages
    """
    # Given
    text_zh = "創建用戶 alice"
    text_en = "create user alice"
    
    # When
    tokens_zh = self.tokenizer.tokenize(text_zh)
    tokens_en = self.tokenizer.tokenize(text_en)
    
    # Then
    canonical_zh = [t.canonical for t in tokens_zh]
    canonical_en = [t.canonical for t in tokens_en]
    assert canonical_zh == canonical_en
```

### 4. Behavior-Driven Development (BDD)

**應用：**
- **Behavior Specifications** - 從架構規格產生行為描述
- **Given-When-Then** - 標準化測試結構
- **Acceptance Criteria** - 架構驗收標準轉換為測試

**實作：**
```python
# Behavior from architecture spec:
# "同一語意在不同語言產生相同 hash"

def test_same_semantic_produces_same_hash(self):
    """
    GIVEN: Same semantic meaning in different languages
    WHEN: Hashed
    THEN: Produce identical hash values
    """
    # Given
    text_zh = "創建用戶 alice"
    text_en = "create user alice"
    
    # When
    hash_zh = self.hasher.hash(text_zh)
    hash_en = self.hasher.hash(text_en)
    
    # Then
    assert hash_zh == hash_en
```

### 5. Model-Driven Engineering (MDE)

**應用：**
- **Model-to-Code Transformation** - 架構模型 → 程式碼
- **Metamodel** - module-map.yaml 作為元模型
- **Transformation Rules** - 實作協定定義轉換規則

**實作：**
```yaml
# Model (Architecture)
Layer 1:
  - Semantic Tokenization
  
# Metamodel (Module Map)
modules:
  semantic_tokenizer:
    responsibility: "Semantic Tokenization"
    
# Transformation (Code)
class SemanticTokenizer:
    # Generated from model
```

### 6. Infrastructure as Code (IaC)

**應用：**
- **Declarative Specification** - YAML 聲明式定義
- **Version Control** - 所有規格可版本化
- **Reproducibility** - 一致的重現環境

**實作：**
```yaml
# Declarative specification of implementation
modules:
  semantic_tokenizer:
    file: governance/kernel/semantic/tokenizer.py
    dependencies: []
```

### 7. CI/CD Integration

**應用：**
- **Automated Validation** - 自動執行測試和驗證
- **Continuous Evidence** - 持續產生證據鏈
- **Deployment Gates** - 通過驗證才能部署

**實作：**
```yaml
# CI/CD pipeline
validation_steps:
  - compile_all_modules
  - run_all_tests
  - verify_coverage
  - validate_evidence_chain
  - seal_implementation
```

### 8. Evidence-Based Engineering

**應用：**
- **Complete Traceability** - 每個決策都有證據
- **Audit Trail** - 完整的審計日誌
- **Cryptographic Integrity** - SHA256 hash 驗證

**實作：**
```json
{
  "trace": {
    "module": "semantic_tokenizer",
    "implementation_hash": "sha256:abc123...",
    "test_hash": "sha256:def456...",
    "evidence_hash": "sha256:ghi789...",
    "audit_trail": [...]
  }
}
```

---

## 治理對齊 (Governance Alignment)

### MNGA Compliance

```yaml
mnga_compliance:
  gl_level: "GL50"
  mnga_version: "v2.0"
  
  requirements:
    - evidence_native: true
    - traceability: "complete"
    - replayability: "enabled"
    - cryptographic_integrity: "SHA256"
    - semantic_closure: "pending"
  
  validation:
    - all_modules_compilable: true
    - all_tests_passed: true
    - coverage: ">= 80%"
    - evidence_chain_complete: true
```

### GL-Naming-Ontology Alignment

```yaml
naming_conventions:
  modules:
    - pattern: "<layer>_<responsibility>"
    - example: "semantic_tokenizer"
  
  classes:
    - pattern: "<Module>PascalCase"
    - example: "SemanticTokenizer"
  
  files:
    - pattern: "<module>.py"
    - example: "tokenizer.py"
  
  tests:
    - pattern: "test_<module>.py"
    - example: "test_tokenizer.py"
```

---

## 執行範例 (Execution Example)

### Complete Workflow

```bash
# Step 1: AI 觸發架構分解
ENTER ARCHITECTURE_TO_CODE MODE
architecture_spec: BACKEND-GOVERNANCE-RESPONSIBILITY.md
target_layers: [Layer 1]

# Step 2: AI 產生模組映射
Generated: .governance/implementation/layer1-decomposition.yaml

# Step 3: AI 實作模組（按優先順序）
Implemented: semantic_tokenizer (Priority 1)
Implemented: semantic_ast (Priority 2)
Implemented: semantic_hasher (Priority 3)
Implemented: semantic_canonicalizer (Priority 3)
Implemented: multilang_evidence (Priority 4)

# Step 4: AI 執行測試
Test Results: 27/27 passed, Coverage: 92.3%

# Step 5: AI 整合模組
Integration Tests: 5/5 passed

# Step 6: AI 封存證據鏈
Evidence Chain Sealed: sha256:abc123...

# Step 7: AI 產生總結
Status: COMPLETE
Next Phase: Layer 2 - Evidence Layer
```

---

## 成功標準 (Success Criteria)

### 必須滿足 (Must)

- ✅ 所有模組編譯成功
- ✅ 所有測試通過
- ✅ 測試覆蓋率 >= 80%
- ✅ 端到端整合驗證通過
- ✅ 證據鏈完整且封存
- ✅ 一站式執行可能

### 應該滿足 (Should)

- ✅ 測試覆蓋率 >= 90%
- ✅ 程式碼符合 PEP 8
- ✅ 完整的文檔字串
- ✅ 類型提示 (type hints)

### 可以滿足 (Could)

- ✅ 效能優化
- ✅ 錯誤處理增強
- ✅ 日誌記錄
- ✅ 配置管理

---

## 參考文獻 (References)

1. **Domain-Driven Design** - Eric Evans
2. **Clean Architecture** - Robert C. Martin
3. **Test-Driven Development** - Kent Beck
4. **Behavior-Driven Development** - Dan North
5. **Model-Driven Engineering** - Object Management Group
6. **Infrastructure as Code** - Kief Morris
7. **Continuous Integration** - Martin Fowler
8. **Evidence-Based Engineering** - IEEE Standards

---

**Document Version:** 1.0.0  
**Status:** CANONICAL  
**GL Level:** GL50  
**Last Updated:** 2024-02-05
# Architecture-to-Code Protocol (ATCP)
# GL Unified Charter Strategy Baseline Integration
# 抽象架構 → 具體實作 的一站式執行協定
# Version: 2.0.0
# Status: CANONICAL
# GL Level: GL50 (Indestructible Kernel)
# GL Unified Charter Activated: YES

---

## Protocol Metadata

```yaml
protocol_name: Architecture-to-Code Protocol (ATCP)
version: "2.0.0"
status: CANONICAL
gl_level: GL50
charter_activated: true
created_at: 2025-02-05T12:00:00Z
last_updated: 2025-02-05T12:00:00Z
compliance:
  - gl-naming-ontology: v1.0.0
  - gl-governance-layers: v1.0.0
  - gl-validation-rules: v1.0.0
  - materialization-complement-spec: v2.0.0
```

---

## Executive Summary

**核心問題：** 抽象的治理架構規格（如 GL-5L）無法直接被 AI 程式碼編輯器理解並轉換為可執行程式碼。

**解決方案：** 建立三層映射協定，將架構規格分解為可執行的模組，並提供一次性完整實作的路徑。

**關鍵創新：**
1. **架構分解協定** - 將抽象層級拆解為具體模組和依賴圖
2. **模組實作協定 (MVE)** - 每個模組的最小可用實作定義
3. **一站式集成協定** - 端到端驗證與證據封存

**與全球最佳實踐對齊：**
- Spec-Driven Development (SDD) - 2025年工程趨勢
- Model-Driven Engineering (MDE) - DSL到程式碼的轉換
- Proof-Carrying Artifacts - PRISM啟發的可驗證補充

---

## Protocol Architecture

### 三層映射模型

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 3: 一站式集成協定 (One-Shot Integration)              │
│ - 端到端驗證                                                 │
│ - 證據鏈封存                                                │
│ - Governance Closure 驗證                                    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Layer 2: 模組實作協定 (Module Implementation)               │
│ - 最小可用實作 (MVE)                                         │
│ - 輸入/輸出契約                                             │
│ - 測試案例驅動                                             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Layer 1: 架構分解協定 (Architecture Decomposition)          │
│ - 模組定義                                                 │
│ - 依賴關係圖                                               │
│ - 實作優先順序                                             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ 架構規格輸入 (Architecture Specifications)                  │
│ - GL-5L 五層治理責任模型                                     │
│ - BACKEND-GOVERNANCE-RESPONSIBILITY.md                     │
│ - 其他治理規格文件                                          │
└─────────────────────────────────────────────────────────────┘
```

---

## Layer 1: 架構分解協定 (Architecture Decomposition)

### 1.1 輸入格式

架構規格必須遵循以下結構：

```yaml
# 來源：BACKEND-GOVERNANCE-RESPONSIBILITY.md
specification:
  name: "Backend Governance Responsibility"
  version: "2.0.0"
  gl_level: "GL50"
  
layers:
  - id: "L1"
    name: "Semantic Layer"
    name_zh: "語意層"
    responsibility: "語意封存（語言中立）"
    modules:
      - name: "semantic_tokenizer"
        description: "自然語言轉語意 token"
        status: "NOT_IMPLEMENTED"
        priority: "CRITICAL"
```

### 1.2 模組分解規則

**規則 1：單一責任原則**
- 每個模組必須只有一個明確的治理責任
- 模組名稱必須反映其責任

**規則 2：依賴方向**
- 上層依賴下層，下層不依賴上層
- 依賴必須顯式聲明

**規則 3：優先順序**
- 優先級：CRITICAL > HIGH > MEDIUM > LOW
- 無依賴的模組優先實作

### 1.3 模組映射輸出

```yaml
# 產出文件：.governance/implementation/module-decomposition.yaml

architecture_reference: "ecosystem/governance/specs/backend-governance-responsibility.md"
generated_at: "2025-02-05T12:00:00Z"
sha256: "..."

modules:
  semantic_tokenizer:
    type: "class"
    file: "governance/kernel/semantic/tokenizer.py"
    responsibility: "Semantic Tokenization"
    priority: 1
    dependencies: []
    status: "PENDING"
    gl_level: "GL50"
    
  semantic_ast:
    type: "class"
    file: "governance/kernel/semantic/ast_builder.py"
    responsibility: "Semantic AST Construction"
    priority: 2
    dependencies: ["semantic_tokenizer"]
    status: "PENDING"
    gl_level: "GL50"
    
  semantic_hasher:
    type: "class"
    file: "governance/kernel/semantic/hasher.py"
    responsibility: "Language-Neutral Hash"
    priority: 3
    dependencies: ["semantic_tokenizer", "semantic_ast"]
    status: "PENDING"
    gl_level: "GL50"

implementation_order:
  - phase: 1
    priority: "P1"
    modules: ["semantic_tokenizer"]
    can_parallel: false
    
  - phase: 2
    priority: "P2"
    modules: ["semantic_ast", "semantic_canonicalizer"]
    can_parallel: true
    
  - phase: 3
    priority: "P3"
    modules: ["semantic_hasher"]
    can_parallel: false
```

---

## Layer 2: 模組實作協定 (Module Implementation)

### 2.1 最小可用實作 (MVE) 原則

每個模組的第一版必須滿足：

**可編譯**
- 語法正確，無錯誤
- 符合 PEP 8 編碼規範
- 通過靜態分析工具檢查

**可測試**
- 至少 1 個測試案例通過
- 測試覆蓋率 >= 80%
- 測試案例包含邊界條件

**可整合**
- 符合輸入/輸出契約
- 與依賴模組兼容
- 產生規範化的輸出

**不完美**
- 功能可以簡化，但不能虛構
- 註明未完成的功能
- 提供擴充路徑

### 2.2 模組實作模板

```yaml
# 模組：semantic_tokenizer
# 檔案：governance/kernel/semantic/tokenizer.py

implementation_spec:
  class_name: "SemanticTokenizer"
  base_class: null
  gl_level: "GL50"
  
  dependencies:
    - module: "none"
      import: null
  
  methods:
    - name: "tokenize"
      signature: "tokenize(text: str, language: str = 'auto') -> List[SemanticToken]"
      responsibility: "將文本轉換為語意 token"
      minimum_implementation: |
        # 支援基礎動詞（創建/刪除/修改）
        # 支援中英文
        # 產生語意 token
      
      test_cases:
        - name: "test_basic_tokenization_chinese"
          input: "創建用戶 alice"
          expected_output: |
            [
              SemanticToken(type="ACTION", value="創建", canonical="create"),
              SemanticToken(type="ENTITY", value="用戶", canonical="user"),
              SemanticToken(type="IDENTIFIER", value="alice", canonical="alice")
            ]
          
        - name: "test_language_neutrality"
          description: "相同語意產生相同 canonical"
          input_zh: "創建用戶 alice"
          input_en: "create user alice"
          expected: "canonical tokens 必須相同"
  
  data_classes:
    - name: "SemanticToken"
      fields:
        - name: "type"
          type: "TokenType"
          required: true
        - name: "value"
          type: "str"
          required: true
        - name: "canonical"
          type: "str"
          required: true
        - name: "metadata"
          type: "Dict[str, Any]"
          required: false
          default: "field(default_factory=dict)"
```

### 2.3 實作產出示例

```python
# governance/kernel/semantic/tokenizer.py

"""
Semantic Tokenizer - Language-Neutral Token Extraction
Responsibility: 將自然語言轉換為語意 token 序列
GL Level: GL50 (Indestructible Kernel)
GL Unified Charter Activated: YES
Status: MINIMAL_VIABLE_IMPLEMENTATION (MVE)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from enum import Enum
import re

@dataclass
class SemanticToken:
    """
    語意 Token
    
    Governance Constraints:
    - Must be language-neutral through canonical field
    - Must be reproducible across different AI models
    - Must support semantic sealing
    """
    type: str           # ACTION, ENTITY, IDENTIFIER, CONDITION, VALUE
    value: str          # 原始值
    canonical: str      # 標準化值（語言中立）
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """轉換為字典（用於證據封存）"""
        return {
            "type": self.type,
            "value": self.value,
            "canonical": self.canonical,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SemanticToken':
        """從字典還原（用於證據重放）"""
        return cls(
            type=data["type"],
            value=data["value"],
            canonical=data["canonical"],
            metadata=data.get("metadata", {})
        )

class SemanticTokenizer:
    """
    語意 Tokenizer
    
    Minimum Viable Implementation (MVE):
    - 支援基礎動詞（創建/刪除/修改）
    - 支援中英文
    - 產生語意 token
    
    Governance Compliance:
    - GL50: Indestructible Kernel
    - Semantic sealing: Language-neutral canonical tokens
    - Evidence chain: Full traceability
    
    Future Enhancements:
    - More verbs
    - Entity recognition
    - Condition identification
    - Multi-language support (ja, ko, de, fr)
    """
    
    # 基礎動詞映射（中英文 → canonical）
    ACTION_MAP = {
        # 創建
        "創建": "create", "建立": "create", "新增": "create", "加入": "create",
        "create": "create", "add": "create", "insert": "create", "register": "create",
        
        # 刪除
        "刪除": "delete", "移除": "delete", "去除": "delete",
        "delete": "delete", "remove": "delete", "drop": "delete",
        
        # 修改
        "修改": "update", "更新": "update", "變更": "update",
        "update": "update", "modify": "update", "change": "update",
        
        # 查詢
        "查詢": "query", "搜尋": "query", "找": "query",
        "query": "query", "search": "query", "find": "query", "get": "query"
    }
    
    # 實體類型映射
    ENTITY_MAP = {
        "用戶": "user", "使用者": "user", "user": "user",
        "訂單": "order", "order": "order",
        "產品": "product", "商品": "product", "product": "product"
    }
    
    def tokenize(self, text: str, language: str = "auto") -> List[SemanticToken]:
        """
        將文本轉換為語意 token
        
        Args:
            text: 輸入文本
            language: 語言 (auto/zh/en)
        
        Returns:
            語意 token 列表
        
        Example:
            Input: "創建用戶 alice"
            Output: [
              SemanticToken(type="ACTION", value="創建", canonical="create"),
              SemanticToken(type="ENTITY", value="用戶", canonical="user"),
              SemanticToken(type="IDENTIFIER", value="alice", canonical="alice")
            ]
        """
        tokens = []
        
        # 簡單分詞（空格分割）
        words = text.strip().split()
        
        for word in words:
            word_lower = word.lower()
            
            # 檢查是否為動作
            if word in self.ACTION_MAP or word_lower in self.ACTION_MAP:
                canonical = self.ACTION_MAP.get(word, self.ACTION_MAP.get(word_lower))
                tokens.append(SemanticToken(
                    type="ACTION",
                    value=word,
                    canonical=canonical,
                    metadata={"language": self._detect_language(word)}
                ))
            
            # 檢查是否為實體
            elif word in self.ENTITY_MAP or word_lower in self.ENTITY_MAP:
                canonical = self.ENTITY_MAP.get(word, self.ENTITY_MAP.get(word_lower))
                tokens.append(SemanticToken(
                    type="ENTITY",
                    value=word,
                    canonical=canonical,
                    metadata={"language": self._detect_language(word)}
                ))
            
            # Email 格式
            elif '@' in word and '.' in word:
                tokens.append(SemanticToken(
                    type="IDENTIFIER",
                    value=word,
                    canonical=word.lower(),  # Email 統一小寫
                    metadata={"format": "email"}
                ))
            
            # 其他視為標識符
            else:
                tokens.append(SemanticToken(
                    type="IDENTIFIER",
                    value=word,
                    canonical=word.lower(),
                    metadata={}
                ))
        
        return tokens
    
    def detokenize(self, tokens: List[SemanticToken], target_language: str) -> str:
        """
        將語意 token 轉換回目標語言
        
        Args:
            tokens: 語意 token 列表
            target_language: 目標語言 (zh/en)
        
        Returns:
            目標語言文本
        """
        words = []
        
        # 反向映射（canonical → target language word）
        reverse_action_map = self._build_reverse_map(self.ACTION_MAP, target_language)
        reverse_entity_map = self._build_reverse_map(self.ENTITY_MAP, target_language)
        
        for token in tokens:
            if token.type == "ACTION":
                word = reverse_action_map.get(token.canonical, token.canonical)
            elif token.type == "ENTITY":
                word = reverse_entity_map.get(token.canonical, token.canonical)
            else:
                word = token.value  # 標識符保持不變
            
            words.append(word)
        
        return " ".join(words)
    
    def _detect_language(self, word: str) -> str:
        """檢測詞語語言"""
        # 簡單檢測：包含中文字元 → zh，否則 → en
        if re.search(r'[\u4e00-\u9fff]', word):
            return "zh"
        return "en"
    
    def _build_reverse_map(
        self,
        forward_map: Dict[str, str],
        target_language: str
    ) -> Dict[str, str]:
        """建立反向映射（canonical → target language word）"""
        reverse_map = {}
        
        for word, canonical in forward_map.items():
            # 只選擇目標語言的詞
            if target_language == "zh" and self._detect_language(word) == "zh":
                if canonical not in reverse_map:
                    reverse_map[canonical] = word
            elif target_language == "en" and self._detect_language(word) == "en":
                if canonical not in reverse_map:
                    reverse_map[canonical] = word
        
        return reverse_map
```

### 2.4 測試文件模板

```python
# tests/kernel/semantic/test_tokenizer.py

"""
Semantic Tokenizer Tests
GL Level: GL50
GL Unified Charter Activated: YES
"""

import pytest
from governance.kernel.semantic.tokenizer import SemanticTokenizer, SemanticToken

class TestSemanticTokenizer:
    """語意 Tokenizer 測試"""
    
    def setup_method(self):
        self.tokenizer = SemanticTokenizer()
    
    def test_basic_tokenization_chinese(self):
        """測試基礎中文 tokenization"""
        text = "創建用戶 alice"
        tokens = self.tokenizer.tokenize(text)
        
        assert len(tokens) == 3
        assert tokens[0].type == "ACTION"
        assert tokens[0].canonical == "create"
        assert tokens[1].type == "ENTITY"
        assert tokens[1].canonical == "user"
        assert tokens[2].type == "IDENTIFIER"
        assert tokens[2].canonical == "alice"
    
    def test_basic_tokenization_english(self):
        """測試基礎英文 tokenization"""
        text = "create user alice"
        tokens = self.tokenizer.tokenize(text)
        
        assert len(tokens) == 3
        assert tokens[0].canonical == "create"
        assert tokens[1].canonical == "user"
        assert tokens[2].canonical == "alice"
    
    def test_language_neutrality(self):
        """
        測試語言中立性（相同語意產生相同 canonical）
        
        Governance Requirement:
        - Same semantics in different languages must produce the same hash
        - This is critical for semantic sealing and cross-language replay
        """
        text_zh = "創建用戶 alice"
        text_en = "create user alice"
        
        tokens_zh = self.tokenizer.tokenize(text_zh)
        tokens_en = self.tokenizer.tokenize(text_en)
        
        # Canonical tokens 必須相同
        canonical_zh = [t.canonical for t in tokens_zh]
        canonical_en = [t.canonical for t in tokens_en]
        
        assert canonical_zh == canonical_en
        assert canonical_zh == ["create", "user", "alice"]
    
    def test_email_identification(self):
        """測試 Email 識別"""
        text = "創建用戶 alice@example.com"
        tokens = self.tokenizer.tokenize(text)
        
        email_token = tokens[2]
        assert email_token.type == "IDENTIFIER"
        assert email_token.canonical == "alice@example.com"
        assert email_token.metadata.get("format") == "email"
    
    def test_detokenization_chinese(self):
        """測試反向 tokenization（中文）"""
        tokens = [
            SemanticToken(type="ACTION", value="create", canonical="create"),
            SemanticToken(type="ENTITY", value="user", canonical="user"),
            SemanticToken(type="IDENTIFIER", value="alice", canonical="alice")
        ]
        
        text = self.tokenizer.detokenize(tokens, target_language="zh")
        
        # 應轉換為中文
        assert "創建" in text or "建立" in text
        assert "用戶" in text or "使用者" in text
        assert "alice" in text
    
    def test_detokenization_english(self):
        """測試反向 tokenization（英文）"""
        tokens = [
            SemanticToken(type="ACTION", value="創建", canonical="create"),
            SemanticToken(type="ENTITY", value="用戶", canonical="user"),
            SemanticToken(type="IDENTIFIER", value="alice", canonical="alice")
        ]
        
        text = self.tokenizer.detokenize(tokens, target_language="en")
        
        # 應轉換為英文
        assert "create" in text.lower()
        assert "user" in text.lower()
        assert "alice" in text.lower()
    
    def test_multiple_actions(self):
        """測試多個動作"""
        text = "創建用戶 alice 然後 刪除用戶 bob"
        tokens = self.tokenizer.tokenize(text)
        
        actions = [t for t in tokens if t.type == "ACTION"]
        assert len(actions) == 2
        assert actions[0].canonical == "create"
        assert actions[1].canonical == "delete"
    
    def test_semantic_token_serialization(self):
        """
        測試語意 token 序列化/反序列化
        
        Governance Requirement:
        - Tokens must be serializable for evidence sealing
        - Must support replay for decision replayability
        """
        original_token = SemanticToken(
            type="ACTION",
            value="創建",
            canonical="create",
            metadata={"language": "zh"}
        )
        
        # 序列化
        token_dict = original_token.to_dict()
        
        # 反序列化
        restored_token = SemanticToken.from_dict(token_dict)
        
        # 驗證
        assert restored_token.type == original_token.type
        assert restored_token.value == original_token.value
        assert restored_token.canonical == original_token.canonical
        assert restored_token.metadata == original_token.metadata
```

---

## Layer 3: 一站式集成協定 (One-Shot Integration)

### 3.1 AI 執行觸發格式

```yaml
ENTER ARCHITECTURE_TO_CODE_MODE

architecture_spec: "ecosystem/governance/specs/backend-governance-responsibility.md"
target_layers: ["Layer 1"]  # 先實作 Layer 1
mode: ONE_SHOT_INTEGRATION

output_format:
  code_files: "governance/kernel/semantic/*.py"
  test_files: "tests/kernel/semantic/*.py"
  evidence: "evidence/implementation/layer1-semantic/"
  
constraints:
  no_placeholders: true
  minimum_viable: true
  test_coverage: ">= 80%"
  evidence_chain: true
  gl_compliance: true

governance:
  gl_level: "GL50"
  charter_activated: true
  closure_required: false  # Era-1, not yet sealed
  evidence_native: true
```

### 3.2 AI 回應格式

```yaml
mode: ARCHITECTURE_TO_CODE
status: DECOMPOSING
timestamp: "2025-02-05T12:00:00Z"

# Phase 1: 架構分解
module_decomposition:
  total_modules: 5
  implementation_order:
    - priority_1: ["semantic_tokenizer"]
    - priority_2: ["semantic_ast"]
    - priority_3: ["semantic_hasher", "semantic_canonicalizer"]
    - priority_4: ["multilang_evidence"]

# Phase 2: 開始實作
current_phase: IMPLEMENTATION
current_module: semantic_tokenizer (1/5)

implementation_plan:
  file: "governance/kernel/semantic/tokenizer.py"
  lines_estimated: 120
  test_file: "tests/kernel/semantic/test_tokenizer.py"
  test_cases: 8
  
proceed: true
```

### 3.3 實作產出序列

```
=== Phase 1: Module Decomposition ===

=== path: .governance/implementation/layer1-decomposition.yaml ===
[module-decomposition.yaml 內容]

=== Phase 2: Module Implementation (Priority 1) ===

=== path: governance/kernel/semantic/__init__.py ===
"""
Semantic Layer - Language-Neutral Semantic Processing
GL Level: GL50 (Indestructible Kernel)
GL Unified Charter Activated: YES
"""

from .tokenizer import SemanticTokenizer, SemanticToken
from .ast_builder import SemanticAST, ASTNode
from .hasher import SemanticHasher
from .multilang_evidence import MultiLanguageEvidence
from .canonicalizer import SemanticCanonicalizer

__all__ = [
    'SemanticTokenizer',
    'SemanticToken',
    'SemanticAST',
    'ASTNode',
    'SemanticHasher',
    'MultiLanguageEvidence',
    'SemanticCanonicalizer'
]

[接續產出所有程式碼文件...]

=== Phase 3: Evidence Collection ===

=== path: evidence/implementation/layer1-semantic/implementation-trace.json ===
{
  "layer": "Layer 1 - Semantic Layer",
  "implementation_started_at": "2025-02-05T12:00:00Z",
  "implementation_completed_at": "2025-02-05T12:15:00Z",
  "gl_level": "GL50",
  "charter_activated": true,
  
  "modules_implemented": [
    {
      "module": "semantic_tokenizer",
      "file": "governance/kernel/semantic/tokenizer.py",
      "lines_of_code": 187,
      "test_file": "tests/kernel/semantic/test_tokenizer.py",
      "test_cases": 8,
      "test_coverage": "94.2%",
      "implementation_hash": "sha256:abc123def456..."
    }
  ],
  
  "test_results": {
    "total": 8,
    "passed": 8,
    "failed": 0,
    "skipped": 0,
    "coverage": "94.2%"
  },
  
  "governance_compliance": {
    "gl_naming": "PASS",
    "gl_structure": "PASS",
    "evidence_chain": "PASS",
    "semantic_sealing": "PASS"
  },
  
  "next_priority": {
    "priority": 2,
    "modules": ["semantic_ast"]
  }
}
```

---

## 實作優先順序策略

### GL-5L 實作順序

基於治理責任模型的依賴關係，推薦以下實作順序：

```yaml
layer_1_semantic:
  phase_1_critical:
    modules:
      - semantic_tokenizer
    rationale: "無依賴，是所有其他模組的基礎"
    estimated_time: "2 hours"
  
  phase_2_high:
    modules:
      - semantic_ast
      - semantic_canonicalizer
    rationale: "依賴 tokenizer，可並行實作"
    estimated_time: "3 hours"
    can_parallel: true
  
  phase_3_high:
    modules:
      - semantic_hasher
    rationale: "依賴 tokenizer 和 ast"
    estimated_time: "2 hours"
  
  phase_4_medium:
    modules:
      - multilang_evidence
    rationale: "依賴 hasher，用於跨語言證據"
    estimated_time: "2 hours"

layer_2_decision:
  # 待實作...
  
layer_3_evidence:
  # 待實作...
  
layer_4_governance:
  # 待實作...
  
layer_5_repository:
  # 待實作...
```

---

## 證據封存協定

### 證據鏈結構

每個實作必須產生完整的證據鏈：

```json
{
  "evidence_id": "EV-20250205-001",
  "evidence_type": "IMPLEMENTATION_TRACE",
  "layer": "Layer 1 - Semantic",
  "module": "semantic_tokenizer",
  "timestamp": "2025-02-05T12:00:00Z",
  
  "proof_chain": {
    "architecture_spec_hash": "sha256:...",
    "decomposition_hash": "sha256:...",
    "implementation_hash": "sha256:...",
    "test_hash": "sha256:...",
    "evidence_hash": "sha256:..."
  },
  
  "verification": {
    "automated": {
      "syntax_check": "PASS",
      "static_analysis": "PASS",
      "unit_tests": "PASS (8/8)",
      "coverage": "94.2%"
    },
    "governance": {
      "gl_naming": "PASS",
      "gl_structure": "PASS",
      "evidence_chain": "PASS",
      "semantic_sealing": "PASS"
    }
  },
  
  "artifacts": [
    "governance/kernel/semantic/tokenizer.py",
    "tests/kernel/semantic/test_tokenizer.py",
    ".governance/implementation/layer1-decomposition.yaml",
    "evidence/implementation/layer1-semantic/implementation-trace.json"
  ]
}
```

### Governance Closure 狀態

```yaml
closure_status:
  era: "Era-1"
  evidence_native: true
  semantic_closure: false  # 待 Era-2 完成
  governance_closure: false  # 待 Era-2 完成
  core_sealed: false  # 待 Era-2 完成
  
  completion_metrics:
    layer_1_semantic: 0%  # 當前任務完成後會更新
    layer_2_decision: 0%
    layer_3_evidence: 0%
    layer_4_governance: 0%
    layer_5_repository: 0%
```

---

## 最佳實踐參考

### Spec-Driven Development (SDD) 對齊

本協定與 2025 年 SDD 趨勢對齊：

1. **Specification-First**: 所有實作基於明確的架構規格
2. **Proof-Carrying Artifacts**: 每個實作都包含可驗證的證據
3. **Automated Compliance**: 自動檢查治理合規性
4. **Continuous Validation**: 持續驗證架構一致性

### Model-Driven Engineering (MDE) 對齊

本協定採用 MDE 原則：

1. **Model-Based**: 架構規格作為源模型
2. **Transformative**: 自動轉換為程式碼
3. **Traceable**: 完整的追溯鏈
4. **Executable**: 產出的程式碼可立即執行

---

## 附錄：AI 執行範例

### 完整對話流程

**用戶輸入：**
```
ENTER ARCHITECTURE_TO_CODE_MODE
architecture_spec: ecosystem/governance/specs/backend-governance-responsibility.md
target_layers: [Layer 1]
```

**AI 回應 1（分解階段）：**
```
Phase 1: Analyzing architecture specification...

Found 5 modules in Layer 1 (Semantic Layer):
1. semantic_tokenizer (Priority 1, No dependencies)
2. semantic_ast (Priority 2, Depends on: semantic_tokenizer)
3. semantic_canonicalizer (Priority 2, Depends on: semantic_tokenizer)
4. semantic_hasher (Priority 3, Depends on: semantic_tokenizer, semantic_ast)
5. multilang_evidence (Priority 4, Depends on: semantic_hasher)

Implementation order: P1 → P2 (parallel) → P3 → P4

Proceeding to Phase 2...
```

**AI 回應 2（實作階段 - P1）：**
```
Phase 2: Implementing Priority 1 modules...

Current module: semantic_tokenizer
File: governance/kernel/semantic/tokenizer.py
Estimated lines: 120

[Producing code...]

Test file: tests/kernel/semantic/test_tokenizer.py
Test cases: 8

Running tests...
✅ test_basic_tokenization_chinese: PASS
✅ test_basic_tokenization_english: PASS
✅ test_language_neutrality: PASS
✅ test_email_identification: PASS
✅ test_detokenization_chinese: PASS
✅ test_detokenization_english: PASS
✅ test_multiple_actions: PASS
✅ test_semantic_token_serialization: PASS

Test coverage: 94.2%

Generating evidence...
Evidence ID: EV-20250205-001
Proof chain: [architecture_spec] → [decomposition] → [implementation] → [tests]

Phase 1 Complete. Proceeding to Phase 2 (P2)...
```

**AI 回應 3（完成）：**
```
Phase 4: Integration complete!

Summary:
- Modules implemented: 1/5 (semantic_tokenizer)
- Test coverage: 94.2%
- Governance compliance: PASS
- Evidence sealed: YES

Next priority: P2 modules (semantic_ast, semantic_canonicalizer)
Can proceed in parallel: YES

Continue? (yes/no)
```

---

## 版本歷史

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-02-05 | Initial CANONICAL version with GL integration |
| 1.0.0 | 2024-01-01 | Draft version |

---

## 參考文獻

1. Thoughtworks - Spec-Driven Development (2025)
2. IEEE 1471 - Architecture Description
3. ISO/IEC 12207 - Systems and Software Engineering
4. Materialization Complement Specification v2.0
5. GL-5L Five-Layer Governance Responsibility Model

---

**GL Unified Charter Activated: YES**
**Status: CANONICAL**
**Ready for Execution: YES**
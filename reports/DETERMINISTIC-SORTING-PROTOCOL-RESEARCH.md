# 決定性排序協定深度研究與兼容性分析報告
# Deterministic Sorting Protocol Research & Compatibility Analysis Report

> **報告日期**: 2026-02-04  
> **Era**: 1 (Evidence-Native Bootstrap)  
> **目的**: 分析決定性排序協定與 Era-1 架構的兼容性，找出全球最佳實踐

---

## 📋 執行摘要

### 核心問題
> 架構會一直擴充，那我現在定義的排序規則，以後一定夠用嗎？

### 核心答案
**不需要「一次定義永遠夠用」**，而是需要一個「**永遠可擴充、不會破壞過去的排序協定**」。

### 全球最佳實踐
經過深度檢索，我們找到了兩個關鍵的全球最佳實踐：

1. **RFC 8785 - JSON Canonicalization Scheme (JCS)** ✅
   - 正式的 IETF RFC 標準
   - 已被廣泛實施和驗證
   - 提供後向穩定性和前向擴充性

2. **Git hash-function-transition (SHA-1 → SHA-256)** ✅
   - 成功的 hash 函數遷移案例
   - 使用雙向映射表實現兼容性
   - 支持 4 種漸進式遷移模式

---

## 🔍 深度檢索結果

### 1. RFC 8785 - JSON Canonicalization Scheme (JCS)

#### 基本信息
- **標準**: IETF RFC 8785 (Informational)
- **發布日期**: 2020 年 6 月
- **狀態**: 已被廣泛實施
- **實施**: JavaScript, Java, Go, Python, .NET

#### 關鍵規則

##### 3.2.1 Whitespace
- JSON tokens 之間不能有空格

##### 3.2.2 Serialization of Primitive Data Types
- Literals: `null`, `true`, `false` 必須嚴格序列化
- Strings:
  - ASCII 控制字符 (U+0000-U+001F): 使用 `\uXXXX` 除非是 `\b`, `\t`, `\n`, `\f`, `\r`
  - 其他字符: 保持原樣，除非是 `\` 或 `"`
  - 使用 UTF-16 碼單元處理
- Numbers: 使用 IEEE 754 double-precision，遵循 ECMA-262 規範
  - 不能使用 `NaN` 或 `Infinity`

##### 3.2.3 Sorting of Object Properties
- **遞歸排序**: JSON 對象的屬性必須遞歸排序
- **數組順序**: 數組元素的順序不能改變
- **排序基礎**: 使用屬性名稱的「原始」（未轉義）形式
- **編碼**: 使用 UTF-16 碼單元數組進行比較
- **比較方式**: 純值比較，不考慮 locale 設置

##### 示例排序結果
```json
{
  "\r": "Carriage Return",
  "1": "One",
  "\x80": "Control",
  "ö": "Latin Small Letter O With Diaeresis",
  "€": "Euro Sign",
  "😀": "Emoji: Grinning Face",
  "דּ": "Hebrew Letter Dalet With Dagesh"
}
```

##### 3.2.4 UTF-8 Generation
- 最終結果必須編碼為 UTF-8

#### 設計原則

1. **後向穩定性**: 
   - JCS 基於 ECMAScript 的序列化方法
   - 這些方法自 ECMA-262 第 6 版起是穩定的
   - 未來版本即使改變，開發者社群也會堅持此規範

2. **I-JSON 限制**:
   - 無重複屬性名稱
   - Unicode 字符串必須可表達
   - IEEE 754 double-precision 數字
   - 大數字使用字符串表示

3. **子類型處理**:
   - JSON 的字符串類型常用於保存子類型（如 BigInt, DateTime）
   - Stream- 和 schema-based 解析器必須將子類型視為「純」字符串類型
   - 實際轉換在後續步驟進行

#### 與我們架構的關係

✅ **完全兼容**:
- 我們的架構主要使用 JSON 格式（event-stream.jsonl, reports/*.json, artifacts/*.json）
- JCS 可以直接應用於所有 JSON 對象
- 已有成熟的 Python 實施（`rfc8785` PyPI 包）

⚠️ **需要注意**:
- YAML 文件沒有類似的正式標準
- YAML 需要先轉換為 JSON，然後應用 JCS

---

### 2. Git hash-function-transition (SHA-1 → SHA-256)

#### 基本信息
- **文檔**: Git hash-function-transition
- **目標**: 從 SHA-1 遷移到更強的 hash 函數
- **選擇**: SHA-256 (2018 年選定)
- **狀態**: 已實施並在 Git v2.40+ 可用

#### 核心設計原則

##### 遷移目標
1. **漸進式遷移**:
   - 可以一次遷移一個本地倉庫
   - 不需要其他方的行動
   - SHA-256 倉庫可以與 SHA-1 Git 服務器通信（push/fetch）
   - 用戶可以互換使用 SHA-1 和 SHA-256 標識符

2. **完全遷離 SHA-1**:
   - 可以移除 SHA-1 兼容性的本地元數據

3. **可維護性**:
   - 對象格式保持簡單一致
   - 創建通用的倉庫轉換工具

##### 關鍵設計：雙向映射表（Translation Table）

```
SHA-1 名稱 ←→ SHA-256 名稱
```

**工作原理**:
1. SHA-256 倉庫在 packfile 旁邊存儲雙向映射
2. 映射表在本地生成，可用 `git fsck` 驗證
3. 對象查找使用此映射，允許使用任一 hash 函數命名對象

**對象內容的區別**:
- SHA-1 內容: 對象使用 SHA-1 名稱引用其他對象
- SHA-256 內容: 對象使用 SHA-256 名稱引用其他對象
- Blob 對象: SHA-1 和 SHA-256 內容相同（不引用其他對象）

**對象名稱計算**:
- SHA-1: SHA-1(type + length + '\0' + SHA-1 content)
- SHA-256: SHA-256(type + length + '\0' + SHA-256 content)

##### 遷移模式

Git 設計了 4 種操作模式：

1. **Dark Launch** (暗啟動):
   - 用戶輸入視為 SHA-1
   - 輸出轉換為 SHA-1
   - 內部存儲使用 SHA-256
   - 用戶看不到行為變化

2. **Early Transition** (早期遷移):
   - 輸入允許 SHA-1 和 SHA-256
   - 輸出使用 SHA-1
   - 與未遷移的對方通信

3. **Late Transition** (晚期遷移):
   - 輸入允許 SHA-1 和 SHA-256
   - 輸出使用 SHA-256
   - 默認使用更安全的命名方法

4. **Post-Transition** (遷移後):
   - 輸入視為 SHA-256
   - 輸出使用 SHA-256
   - 最安全模式

##### Fetch 流程（從 SHA-1 服務器）

```
1. index-pack: 解壓每個對象，計算其 SHA-1
2. topological sort: 拓撲排序對象
3. convert to SHA-256: 轉換為 SHA-256 格式
4. sort: 重新排序條目
5. clean up: 清理
```

**關鍵洞察**:
- 步驟 2（topological sort）是必要的，因為轉換需要所有被引用的對象都在映射表中
- 步驟 4（sort）對於讀取性能是必要的

##### Push 流程（到 SHA-1 服務器）

**更簡單**，因為被推送對象引用的對象已經在映射表中。

##### 簽名處理

**Commits**:
- 新增 `gpgsig-sha256` 字段
- 允許三種簽名方式：
  1. 只使用 SHA-1
  2. 同時使用 SHA-1 和 SHA-256
  3. 只使用 SHA-256

**Tags**:
- 新增 `gpgsig` 和 `gpgsig-sha256` 字段
- 支持使用一個或兩個算法

#### 與我們架構的關係

✅ **高度相關**:
- Git 的設計展示了如何實現**後向穩定性**和**前向擴充性**
- 雙向映射表的概念可以直接應用於我們的 Era-1 → Era-2 遷移
- 4 種遷移模式提供了靈活的遷移策略

✅ **可借鑒的設計**:
1. **雙向映射表**: 
   - 我們可以為 Era-1 hash 和 Era-2 hash 創建映射表
   - 允許在遷移期間互換使用

2. **拓撲排序**:
   - 在轉換對象時，確保所有引用的對象都可用

3. **漸進式遷移**:
   - 一次一個倉庫
   - 不需要其他方協作
   - 支持跨版本通信

⚠️ **需要適應**:
- Git 的遷移是在同一倉庫內進行
- 我們的 Era-1 → Era-2 遷移可能涉及不同的存儲格式或架構

---

### 3. Merkle Tree 最佳實踐

#### 關鍵洞察

有一篇重要的文章：**"Why you should probably never sort your Merkle tree's leaves"**

**核心論點**:
1. **排序可能破壞某些用例**:
   - 某些應用依賴於葉節點的原始順序
   - 排序可能影響證明（proofs）的生成

2. **替代方案**:
   - 使用固定順序（如插入順序）
   - 使用索引而不是值來標識葉節點

#### 與我們架構的關係

⚠️ **需要謹慎**:
- 如果我們計劃使用 Merkle tree 來存儲語義聲明或實體
- 排序可能不是最佳選擇
- 需要考慮特定用例的需求

✅ **但是**:
- 如果我們只是需要決定性的 hash
- JCS 的排序方法（按屬性名稱）是安全且標準的

---

### 4. YAML Canonicalization

#### 現狀

- **沒有正式標準**: 不像 JCS，YAML 沒有官方的 canonicalization 標準
- **工具級別解決方案**: 主要是 IDE 插件和命令行工具
- **排序檢查器**: YAML sort checker 等工具

#### 與我們架構的關係

⚠️ **挑戰**:
- 我們的架構使用大量 YAML 文件（governance/*.yaml, tools-registry.yaml）
- 沒有標準的 canonicalization 方法

✅ **解決方案**:
- YAML 可以轉換為 JSON，然後應用 JCS
- PyYAML 或 ruamel.yaml 支持轉換為 JSON
- 在轉換時需要處理 YAML 特有的功能（anchors, tags 等）

---

## 🔎 兼容性分析

### 當前 Era-1 架構特徵

1. **Event Stream** (`event-stream.jsonl`):
   - JSON Lines 格式
   - 每行一個 JSON 對象
   - 包含事件元數據和 payload

2. **Artifacts** (`ecosystem/.evidence/step-*.json`):
   - JSON 格式
   - 包含證據和 metadata
   - 附帶 SHA256 hash

3. **Reports** (`reports/*.md`, `reports/*.json`):
   - Markdown 格式（人類可讀）
   - JSON 格式（機器可讀）

4. **Governance Files** (`ecosystem/governance/*.yaml`):
   - YAML 格式
   - 治理規則和定義

5. **Tools Registry** (`ecosystem/governance/tools-registry.yaml`):
   - YAML 格式
   - 工具定義和元數據

### 分層排序協定 vs Era-1 架構

#### 提議的分層排序協定

```
L1: 核心欄位（永遠不變）
  - 時間戳（如果存在）
  - UUID
  - 標識符

L2: 可選欄位（未來可新增）
  - 按字母序排序

L3: 擴充欄位（未來可無限擴充）
  - 按字母序排序
```

#### 兼容性評估

##### ✅ 完全兼容的部分

1. **JSON Artifacts**:
   - JCS 可以直接應用
   - 屬性排序提供決定性
   - 遞歸排序確保嵌套對象的一致性

2. **Event Stream**:
   - 每個 JSON 對象可以獨立 canonicalize
   - 排序不影響事件順序（timestamp 用於排序）

3. **Reports (JSON)**:
   - JCS 適用
   - 決定性的 hash 用於驗證

##### ⚠️ 需要適應的部分

1. **YAML Files**:
   - 需要先轉換為 JSON
   - 可能丟失 YAML 特有的語義（anchors, tags）
   - 需要定義轉換規則

2. **Markdown Files**:
   - 不適用 canonicalization
   - 主要用於人類閱讀
   - 可以附帶 hash 作為驗證

##### 🔍 需要進一步研究的部分

1. **分層排序 vs JCS**:
   - JCS 不使用分層排序，而是對所有屬性進行排序
   - 分層排序可能與 JCS 不兼容
   - 需要決定是否採用 JCS 或自定義分層協定

2. **Field Missing**:
   - JCS 不處理缺失欄位（因為它只是序列化現有內容）
   - 分層協定需要定義如何處理缺失欄位
   - Git 的方法：缺失欄位在轉換時補充

3. **欄位順序穩定性**:
   - JCS 的排序順序在未來是穩定的（基於 UTF-16）
   - 分層協定的 L1/L2/L3 順序需要確保穩定性
   - 需要定義如何識別 L1, L2, L3 欄位

---

## 💡 推薦的最佳實踐

### 方案 1: 完全採用 JCS（推薦）⭐⭐⭐⭐⭐

**優點**:
- ✅ 正式標準，經過驗證
- ✅ 已有成熟實施（Python 包 `rfc8785`）
- ✅ 後向穩定性（基於 ECMA-262）
- ✅ 廣泛支持和社區
- ✅ 與現有 JSON 工具兼容

**缺點**:
- ⚠️ 需要將 YAML 轉換為 JSON
- ⚠️ 不使用分層排序（可能不符合用戶的願望）

**實施建議**:
```python
from rfc8785 import canonicalize
import json

# Canonicalize JSON data
data = {"b": 2, "a": 1}
canonical_json = canonicalize(data)
hash = hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()
```

**適用範圍**:
- Event Stream (JSON Lines)
- Artifacts (JSON)
- Reports (JSON)

**不適用範圍**:
- Markdown 文件
- YAML 文件（需要先轉換）

---

### 方案 2: 自定義分層排序協定

**優點**:
- ✅ 完全控制排序邏輯
- ✅ 支持分層排序（L1/L2/L3）
- ✅ 可以針對特定用例優化

**缺點**:
- ⚠️ 不是標準，需要自己維護
- ⚠️ 需要確保後向穩定性
- ⚠️ 沒有社區支持
- ⚠️ 可能與現有工具不兼容

**實施建議**:
```python
def canonicalize_layered(data, layer_definitions):
    """
    Canonicalize data using layered sorting protocol.
    
    Args:
        data: Dict to canonicalize
        layer_definitions: Dict mapping field names to layers (1, 2, 3)
    
    Returns:
        Canonical JSON string
    """
    # Separate fields by layer
    l1_fields = {k: v for k, v in data.items() if layer_definitions.get(k) == 1}
    l2_fields = {k: v for k, v in data.items() if layer_definitions.get(k) == 2}
    l3_fields = {k: v for k, v in data.items() if layer_definitions.get(k) == 3}
    
    # Sort each layer alphabetically
    l1_sorted = dict(sorted(l1_fields.items()))
    l2_sorted = dict(sorted(l2_fields.items()))
    l3_sorted = dict(sorted(l3_fields.items()))
    
    # Merge layers in order
    canonical = {**l1_sorted, **l2_sorted, **l3_sorted}
    
    return json.dumps(canonical, separators=(',', ':'))
```

**挑戰**:
- 如何定義 `layer_definitions`？
  - 硬編碼？
  - 從 schema 推導？
  - 從約定推導？
- 如何處理未來新增的欄位？
  - 默認 L3？
  - 需要顯式聲明？

---

### 方案 3: 混合方案（推薦）⭐⭐⭐⭐

**核心思想**:
- 對於 JSON 數據：使用 JCS
- 對於特殊需求（如分層排序）：在應用層實施
- 使用 Git 的雙向映射表概念實現 Era-1 → Era-2 遷移

**實施建議**:

##### 1. Canonicalization 層
```python
from rfc8785 import canonicalize
import hashlib

def canonicalize_and_hash(data):
    """Canonicalize and hash JSON data using JCS."""
    canonical_json = canonicalize(data)
    return hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()
```

##### 2. 分層映射（可選）
```python
def apply_layer_mapping(data, layer_map=None):
    """
    Apply layer mapping for special use cases.
    
    This is optional and only used when layered semantics are required.
    """
    if layer_map is None:
        return data
    
    # Reorder fields based on layer map
    l1 = {k: v for k, v in data.items() if layer_map.get(k) == 1}
    l2 = {k: v for k, v in data.items() if layer_map.get(k) == 2}
    l3 = {k: v for k, v in data.items() if layer_map.get(k) == 3}
    
    return {**dict(sorted(l1.items())), 
            **dict(sorted(l2.items())), 
            **dict(sorted(l3.items()))}
```

##### 3. YAML 處理
```python
import yaml

def yaml_to_canonical_json(yaml_content):
    """Convert YAML to canonical JSON."""
    data = yaml.safe_load(yaml_content)
    return canonicalize(data)
```

##### 4. 雙向映射表（Git 風格）
```python
class HashTranslationTable:
    """
    Bidirectional hash translation table (Git-style).
    
    Supports Era-1 hash <-> Era-2 hash translation.
    """
    
    def __init__(self):
        self.era1_to_era2 = {}
        self.era2_to_era1 = {}
    
    def add_mapping(self, era1_hash, era2_hash):
        """Add a bidirectional mapping."""
        self.era1_to_era2[era1_hash] = era2_hash
        self.era2_to_era1[era2_hash] = era1_hash
    
    def get_era2(self, era1_hash):
        """Get Era-2 hash from Era-1 hash."""
        return self.era1_to_era2.get(era1_hash)
    
    def get_era1(self, era2_hash):
        """Get Era-1 hash from Era-2 hash."""
        return self.era2_to_era1.get(era2_hash)
```

**優點**:
- ✅ 使用標準的 JCS 進行 canonicalization
- ✅ 支持分層排序（可選）
- ✅ 支持雙向映射（Era-1 ↔ Era-2）
- ✅ 靈活且可擴充
- ✅ 與 Git 的遷移策略一致

**缺點**:
- ⚠️ 需要維護多個組件
- ⚠️ 分層映射是可選的，不是強制的

---

## 🚀 實施建議

### 階段 1: 採用 JCS（立即）⏱️

1. **安裝依賴**:
```bash
pip install rfc8785
```

2. **創建 canonicalization 工具**:
```python
# ecosystem/tools/canonicalize.py
from rfc8785 import canonicalize
import hashlib
import json

def canonicalize_json(data):
    """Canonicalize JSON data using RFC 8785."""
    return canonicalize(data)

def hash_canonical(data):
    """Compute hash of canonical JSON."""
    canonical = canonicalize_json(data)
    return hashlib.sha256(canonical.encode('utf-8')).hexdigest()
```

3. **集成到現有流程**:
   - 在 artifact 生成時使用 canonical hash
   - 在 event stream 寫入時使用 canonical hash
   - 在驗證時使用 canonical hash

### 階段 2: YAML 處理（短期）⏱️⏱️

1. **創建 YAML 到 JSON 的轉換工具**:
```python
# ecosystem/tools/yaml_to_json.py
import yaml
from rfc8785 import canonicalize

def yaml_to_canonical(yaml_content):
    """Convert YAML to canonical JSON."""
    data = yaml.safe_load(yaml_content)
    return canonicalize(data)
```

2. **處理 YAML 特有的功能**:
   - Anchors: 展開
   - Tags: 轉換為普通值
   - 多文檔: 處理每個文檔

### 階段 3: 雙向映射表（中期）⏱️⏱️⏱️

1. **創建 HashTranslationTable**:
```python
# ecosystem/core/hash_translation.py
class HashTranslationTable:
    """Bidirectional hash translation table."""
    
    def __init__(self, storage_path):
        self.era1_to_era2 = {}
        self.era2_to_era1 = {}
        self.storage_path = storage_path
        self.load()
    
    def add_mapping(self, era1_hash, era2_hash):
        """Add a bidirectional mapping."""
        self.era1_to_era2[era1_hash] = era2_hash
        self.era2_to_era1[era2_hash] = era1_hash
        self.save()
    
    def load(self):
        """Load from storage."""
        # Load from file
        pass
    
    def save(self):
        """Save to storage."""
        # Save to file
        pass
```

2. **集成到 Era-1 → Era-2 遷移**:
   - 在創建 Era-2 hash 時，自動創建 Era-1 → Era-2 映射
   - 在查找時，支持使用任一 hash 函數
   - 在封存時，記錄完整的映射表

### 階段 4: 分層排序（可選）⏱️⏱️⏱️⏱️

1. **定義 layer_map**:
```python
# ecosystem/core/layer_map.py
LAYER_MAP = {
    # L1: Core fields (never change)
    'uuid': 1,
    'timestamp': 1,
    'artifact_id': 1,
    
    # L2: Optional fields (can be added in future)
    'type': 2,
    'source': 2,
    'era': 2,
    
    # L3: Extension fields (can be infinitely expanded)
    # All other fields default to 3
}
```

2. **創建分層 canonicalization 工具**:
```python
def canonicalize_layered(data, layer_map=None):
    """Canonicalize using layered sorting protocol."""
    if layer_map is None:
        layer_map = LAYER_MAP
    
    l1 = {k: v for k, v in data.items() if layer_map.get(k, 3) == 1}
    l2 = {k: v for k, v in data.items() if layer_map.get(k, 3) == 2}
    l3 = {k: v for k, v in data.items() if layer_map.get(k, 3) == 3}
    
    canonical_data = {
        **dict(sorted(l1.items())),
        **dict(sorted(l2.items())),
        **dict(sorted(l3.items()))
    }
    
    return canonicalize_json(canonical_data)
```

---

## ⚠️ 潛在衝突與解決方案

### 衝突 1: 分層排序 vs JCS

**問題**:
- JCS 對所有屬性進行排序（不分層）
- 分層協定要求 L1 在 L2 前，L2 在 L3 前

**解決方案**:
- 採用混合方案
- 使用 JCS 進行 canonicalization
- 在應用層實施分層映射（可選）
- 分層映射是語義上的，不是格式上的

### 衝突 2: YAML 語義丟失

**問題**:
- YAML 有 JCS 不支持的特性（anchors, tags）
- 轉換為 JSON 可能丟失這些語義

**解決方案**:
- 定義 YAML → JSON 的轉換規則
- Anchors: 展開
- Tags: 轉換為普通值或特殊欄位
- 多文檔: 分別處理

### 衝突 3: Era-1 → Era-2 遷移的 hash 變化

**問題**:
- Era-1 使用某種 hash 方法
- Era-2 使用 JCS + SHA256
- hash 值不同

**解決方案**:
- 使用雙向映射表（Git 風格）
- 在 Era-1 → Era-2 遷移時記錄映射
- 支持在遷移期間使用任一 hash

### 衝突 4: 後向穩定性

**問題**:
- JCS 的排序順序在未來是否穩定？
- ECMA-262 未來版本是否會改變序列化方法？

**解決方案**:
- JCS 文檔明確說明：即使 ECMA-262 改變，開發者社群會堅持此規範
- 參考 JCS 社區的實施和測試
- 定期驗證 canonicalization 的結果

---

## 📊 總結與建議

### 核心結論

1. **RFC 8785 (JCS) 是最佳選擇** ⭐⭐⭐⭐⭐
   - 正式標準
   - 已驗證
   - 廣泛支持
   - 後向穩定

2. **Git 的雙向映射表是關鍵設計** ⭐⭐⭐⭐⭐
   - 支持遷移
   - 確保兼容性
   - 已成功實施

3. **分層排序是可選的增強** ⭐⭐⭐
   - 不是標準
   - 可以在應用層實施
   - 不與 JCS 衝突

### 推薦實施路徑

```
階段 1 (立即): 採用 JCS
    ↓
階段 2 (短期): YAML 處理
    ↓
階段 3 (中期): 雙向映射表
    ↓
階段 4 (可選): 分層排序
```

### 最終建議

**採用方案 3: 混合方案**

**理由**:
1. ✅ 使用標準的 JCS 進行 canonicalization
2. ✅ 支持雙向映射（Era-1 ↔ Era-2）
3. ✅ 靈活且可擴充
4. ✅ 與 Git 的遷移策略一致
5. ✅ 支持分層排序（可選）

**下一步**:
1. 安裝 `rfc8785` Python 包
2. 創建 canonicalization 工具
3. 集成到現有流程
4. 創建雙向映射表
5. 規劃 Era-1 → Era-2 遷移

---

**報告完成時間**: 2026-02-04  
**下次審查**: Era-1 → Era-2 遷移規劃時  
**聯繫人**: SuperNinja AI Agent
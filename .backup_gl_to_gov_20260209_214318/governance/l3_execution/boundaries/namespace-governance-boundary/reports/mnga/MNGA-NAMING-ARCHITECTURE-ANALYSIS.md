# MNGA 命名架構分析報告

**報告日期**: 2026-02-03  
**分析範圍**: machine-native-ops 儲存庫  
**分析目的**: 識別並解決命名規範衝突，建立最佳實踐

---

## 執行摘要

### 🔴 關鍵發現

當前 `ecosystem/enforce.py` 存在**根本性架構錯誤**：它期望使用 `dual-path` (kebab-case) 作為 Python 模組路徑，但這在 Python 中是**不可能的**。

```python
# ❌ 錯誤 - Python 無法解析
from ecosystem.reasoning.dual-path.arbitrator import Arbitrator
# Python 會將此解析為: ecosystem.reasoning.dual 減去 path.arbitrator

# ✅ 正確 - Python 可以解析
from ecosystem.reasoning.dual_path.arbitrator import Arbitrator
```

---

## 1. 命名規範衝突分析

### 1.1 Python 語言限制

| 規則 | 說明 | 範例 |
|------|------|------|
| **模組名稱** | 必須是有效的 Python 標識符 | `dual_path` ✓, `dual-path` ✗ |
| **包目錄** | 必須使用 snake_case 或無分隔符 | `my_package/` ✓, `my-package/` ✗ |
| **導入語句** | 連字符會被解析為減法運算符 | `import a-b` = `import a - b` |

### 1.2 當前狀態 vs 期望狀態

| 組件 | 當前狀態 | enforce.py 期望 | 正確做法 |
|------|---------|----------------|---------|
| 目錄 | `dual_path` | `dual-path` | `dual_path` ✓ |
| Python 導入 | `reasoning.dual_path.*` | `reasoning.dual-path.*` | `reasoning.dual_path.*` ✓ |
| 配置文件 | `dual-path-spec.yaml` | `dual-path-spec.yaml` | `dual-path-spec.yaml` ✓ |
| 文件系統路徑 | `ecosystem/reasoning/dual-path/` | `ecosystem/reasoning/dual-path/` | `ecosystem/reasoning/dual-path/` ✓ |

### 1.3 衝突根源

`enforce.py` 第 706-815 行包含錯誤的路徑引用：

```python
# 錯誤的目錄路徑檢查
"ecosystem/reasoning/dual-path/internal": {...}  # ❌ 目錄不存在
"ecosystem/reasoning/dual-path/external": {...}  # ❌ 目錄不存在

# 錯誤的 Python 模組導入
("ecosystem.reasoning.dual-path.arbitration.arbitrator", "Arbitrator")  # ❌ 無法導入
```

---

## 2. MNGA 命名規範最佳實踐

### 2.1 分層命名規則

```
MNGA 命名規範層級結構
├── Layer 0-1: 基礎設施層
│   ├── 目錄: kebab-case (非 Python 模組)
│   └── 配置: kebab-case.yaml
│
├── Layer 2-4: Python 模組層
│   ├── 目錄: snake_case (Python 包)
│   ├── 文件: snake_case.py
│   └── 類名: PascalCase
│
├── Layer 5-6: 治理層
│   ├── 契約: kebab-case.yaml
│   └── 規則: kebab-case.yaml
│
└── Layer 7: 監控層
    ├── 日誌: kebab-case.jsonl
    └── 報告: kebab-case.json
```

### 2.2 具體規則

| 類型 | 命名規範 | 範例 | 原因 |
|------|---------|------|------|
| **Python 包目錄** | snake_case | `dual-path/` | Python 語言限制 |
| **Python 文件** | snake_case | `rule_engine.py` | PEP 8 規範 |
| **Python 類** | PascalCase | `ArbitrationRuleEngine` | PEP 8 規範 |
| **Python 函數/變數** | snake_case | `process_request()` | PEP 8 規範 |
| **配置文件** | kebab-case | `dual-path-spec.yaml` | 可讀性 |
| **非 Python 目錄** | kebab-case | `gov-semantic-anchors/` | 一致性 |
| **GL 語義目錄** | GL00-99 格式 | `GL90-99-Meta/` | GL 規範 |

---

## 3. 需要修正的文件

### 3.1 高優先級 (阻塞性錯誤)

| 文件 | 問題 | 修正方案 |
|------|------|---------|
| `ecosystem/enforce.py` | 使用 `dual-path` 作為 Python 模組路徑 | 改為 `dual_path` |
| `apply_mnga_enforcement.py` | 包含錯誤的路徑映射 | 移除或修正 |

### 3.2 中優先級 (一致性問題)

| 文件 | 問題 | 修正方案 |
|------|------|---------|
| `platforms/gov-platform-assistant/api/reasoning.py` | 導入路徑正確 | 無需修改 |
| `platforms/gov-platform-assistant/orchestration/pipeline.py` | 導入路徑正確 | 無需修改 |

### 3.3 低優先級 (文檔更新)

| 文件 | 問題 | 修正方案 |
|------|------|---------|
| `ecosystem/governance/docs/architecture/architecture-summary.json` | 路徑引用 | 更新文檔 |

---

## 4. 修正計劃

### Phase 1: 修正 enforce.py (關鍵)

```python
# 修正前
"ecosystem/reasoning/dual-path/internal": {...}
("ecosystem.reasoning.dual-path.arbitration.arbitrator", "Arbitrator")

# 修正後
"ecosystem/reasoning/dual-path/internal": {...}
("ecosystem.reasoning.dual_path.arbitration.arbitrator", "Arbitrator")
```

### Phase 2: 驗證 Python 模組可導入性

```python
# 驗證腳本
import sys
sys.path.insert(0, 'ecosystem')

from reasoning.dual_path.internal.retrieval import InternalRetrievalEngine
from reasoning.dual_path.external.retrieval import ExternalRetrievalEngine
from reasoning.dual_path.arbitration.arbitrator import Arbitrator
from reasoning.dual_path.arbitration.rule_engine import ArbitrationRuleEngine

print("✓ 所有模組可正確導入")
```

### Phase 3: 運行 enforce.py 驗證

```bash
python ecosystem/enforce.py --audit
# 預期結果: 所有檢查通過
```

---

## 5. 命名規範決策矩陣

### 5.1 何時使用 snake_case

- ✅ Python 包目錄
- ✅ Python 模組文件 (.py)
- ✅ Python 函數和變數
- ✅ Python 模組導入路徑

### 5.2 何時使用 kebab-case

- ✅ 非 Python 目錄 (docs, configs, assets)
- ✅ YAML/JSON 配置文件
- ✅ Markdown 文檔
- ✅ Shell 腳本
- ✅ URL 路徑

### 5.3 何時使用 PascalCase

- ✅ Python 類名
- ✅ TypeScript/JavaScript 類名
- ✅ React 組件

### 5.4 特殊例外

- `.github/` - GitHub 標準目錄
- `PULL_REQUEST_TEMPLATE/` - GitHub 標準
- `GL00-99-*` - GL 語義層級目錄
- `(tabs)`, `(auth)` - Next.js/Expo 路由目錄

---

## 6. 結論與建議

### 6.1 立即行動

1. **修正 `ecosystem/enforce.py`** - 將所有 `dual-path` 改為 `dual_path`
2. **驗證模組導入** - 確保所有 Python 模組可正確導入
3. **運行完整測試** - 確保修正不破壞現有功能

### 6.2 長期建議

1. **建立 pre-commit hook** - 自動檢查命名規範
2. **更新 CI/CD** - 在 PR 階段阻擋命名違規
3. **文檔化規範** - 將命名規範加入開發者指南

### 6.3 架構原則

> **Python 模組目錄必須使用 snake_case，這是語言限制，不是風格選擇。**

---

## 附錄 A: 驗證命令

```bash
# 檢查目錄結構
ls -la ecosystem/reasoning/dual-path/

# 驗證 Python 導入
python3 -c "from ecosystem.reasoning.dual_path.arbitration.arbitrator import Arbitrator; print('OK')"

# 運行 enforce.py
python ecosystem/enforce.py --audit
```

## 附錄 B: 相關文件

- `ng-namespace-governance/specs/naming-conventions.yaml` - 命名規範定義
- `ng-namespace-governance/tools/naming-enforcer.py` - 命名檢查器
- `.github/workflows/naming-check.yaml` - CI 命名檢查

---

**報告生成者**: MNGA Governance System  
**版本**: 3.0.0  
**狀態**: 待執行修正
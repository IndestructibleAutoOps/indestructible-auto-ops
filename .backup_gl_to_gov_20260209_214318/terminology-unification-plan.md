# 架構規範術語統一計劃

## 基於專業架構標準的術語優化

**依據標準**:
- TOGAF (The Open Group Architecture Framework)
- Federal Enterprise Architecture Framework (FEAF)
- California Enterprise Architecture Glossary
- ISO/IEC/IEEE 42010 Architecture Description

---

## 問題識別

### 當前使用的非標準術語

| 當前術語 | 使用位置 | 問題分析 |
|---------|---------|---------|
| **框架** (Charter) | GL00-GL99-unified-charter.json, governance-framework-baseline.json | 非標準架構術語，企業架構領域不使用"框架" |
| **宇宙** (Universe) | gov-platform, 多個工具腳本 | 概念模糊，不符合專業架構命名規範 |

### 專業標準對照

根據 TOGAF、FEAF、ISO/IEC/IEEE 42010 等標準，架構治理領域的標準術語包括：

** Governance Layer 術語**:
- **Framework** - 治理框架（標準術語）
- **Specification** - 規格說明（標準術語）
- **Baseline** - 基線（標準術語）
- **Policy** - 政策（標準術語）
- **Standard** - 標準（標準術語）
- **Guideline** - 指導原則（標準術語）

** Platform/Environment 術語**:
- **Platform** - 平台（標準術語）
- **Environment** - 環境（標準術語）
- **Domain** - 域（標準術語）
- **Scope** - 範圍（標準術語）
- **Context** - 上下文（標準術語）

---

## 建議的術語替換

### 1. "框架" (Charter) → "Framework" (框架)

**替換理由**:
- TOGAF 使用 "Architecture Governance Framework"
- ISO/IEC/IEEE 42010 使用 "Architecture Framework"
- "Framework" 是架構治理領域的國際標準術語

**受影響文件**:
```
ecosystem/governance/gov-semantic-anchors/GL00-GL99-unified-charter.json
  → ecosystem/governance/gov-semantic-anchors/GL00-GL99-unified-framework.json

ecosystem/governance/gov-semantic-anchors/governance-framework-baseline.json
  (更新描述中的 "Charter" 為 "Framework")

ecosystem/governance/GL-SEMANTIC-ANCHOR.json
  (更新相關描述)
```

**新術語示例**:
```json
{
  "GL_UNIFIED_FRAMEWORK": {
    "version": "1.0.0",
    "description": "MNGA Governance Layer Unified Framework - 100 Semantic Anchors"
  }
}
```

### 2. "宇宙" (Universe) → "Platform" (平台)

**替換理由**:
- "Platform" 是技術架構領域的標準術語
- "Universe" 概念模糊，缺乏明確定義
- "Platform" 符合微服務和雲原生架構標準

**受影響文件**:
```
gov-platform → gl_platform (或 gov-machine-native-platform)

影響範圍：
- ecosystem/tools/gov-markers/*.py
- ecosystem/tools/code_scanning_analysis.py
- ecosystem/tools/fix_code_scanning_issues.py
- ecosystem/tools/audit/gov_audit_simple.py
- ecosystem/reasoning/auto_reasoner.py
- ecosystem/CODE-SCANNING-ECOSYSTEM-SUMMARY.md
```

**新術語示例**:
```python
# 舊
gov-platform.gl-platform.governance

# 新
gov-platform.governance  # 或 gov-machine-native-platform.governance
```

### 3. "統一框架" (Unified Architecture Governance Framework) → "統一架構治理框架" (Unified Architecture Governance Framework)

**完整術語對照**:

| 當前術語 | 建議術語 | 英文對應 |
|---------|---------|---------|
| GL 統一框架 | GL 統一架構治理框架 | GL Unified Architecture Governance Framework |
| 框架規範 | 框架規範 | Framework Specification |
| 框架基線 | 框架基線 | Framework Baseline |
| 平台宇宙 | 平台環境 | Platform Environment |
| 治理宇宙 | 治理域 | Governance Domain |

---

## 執行計劃

### Phase 1: 術語映射定義
- [ ] 創建完整的術語映射表
- [ ] 確定所有需要更新的文件列表
- [ ] 制定替換規則

### Phase 2: 核心治理文件更新
- [ ] 更新 `GL00-GL99-unified-charter.json` → `GL00-GL99-unified-framework.json`
- [ ] 更新 `governance-framework-baseline.json` 描述
- [ ] 更新 `GL-SEMANTIC-ANCHOR.json`
- [ ] 更新 `governance-monitor-config.yaml`

### Phase 3: 代碼庫批量替換
- [ ] 更新所有 `gov-platform` 引用
- [ ] 更新工具腳本中的術語
- [ ] 更新文檔中的描述

### Phase 4: 驗證與測試
- [ ] 運行 `ecosystem/enforce.py --audit`
- [ ] 檢查所有引用是否正確更新
- [ ] 驗證功能完整性

### Phase 5: 文檔更新
- [ ] 更新 README 文檔
- [ ] 更新架構文檔
- [ ] 更新變更日誌

---

## 專業性提升對比

### 替換前
```
"GL_UNIFIED_FRAMEWORK": "MNGA Governance Layer Unified Architecture Governance Framework"
gov-platform.gl-platform.governance
```
**問題**: 使用非標準術語 "Charter" 和 "Universe"

### 替換後
```
"GL_UNIFIED_FRAMEWORK": "MNGA Governance Layer Unified Architecture Governance Framework"
gov-platform.governance
```
**優點**: 符合 TOGAF、FEAF、ISO 等國際標準，專業度提升

---

## 參考標準

1. **TOGAF Standard, 10th Edition**
   - Architecture Governance Framework
   - Architecture Continuum
   - Standards Information Base

2. **ISO/IEC/IEEE 42010:2011**
   - Systems and software engineering — Architecture description
   - Architecture Framework 定義

3. **Federal Enterprise Architecture Framework (FEAF)**
   - Enterprise Architecture Framework
   - Architecture Governance

4. **California Enterprise Architecture Glossary**
   - Architecture Framework
   - Platform Architecture
   - Governance Domain

---

## 實施時間表

| 階段 | 任務 | 預計時間 | 優先級 |
|------|------|---------|--------|
| 1 | 術語映射定義 | 30 分鐘 | HIGH |
| 2 | 核心治理文件更新 | 1 小時 | HIGH |
| 3 | 代碼庫批量替換 | 2 小時 | HIGH |
| 4 | 驗證與測試 | 1 小時 | HIGH |
| 5 | 文檔更新 | 1 小時 | MEDIUM |
| **總計** | | **5.5 小時** | |

---

**結論**: 
將 "框架" 替換為 "Framework"，"宇宙" 替換為 "Platform"，將使整個架構規範符合國際標準，提升專業性和一致性。

**下一步**: 開始執行 Phase 1 - 術語映射定義
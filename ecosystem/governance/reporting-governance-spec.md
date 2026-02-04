# 報告生成強制規格
# Reporting Governance Specification

**規格版本:** v1.0.0
**Era:** 1 (Evidence-Native Bootstrap)
**Layer:** Operational (Evidence Generation)
**Semantic Closure:** NO (Evidence layer only, governance not closed)

---

## 📋 規格目的

本規格旨在確保所有治理報告都遵守統一的敘事框架，防止虛假或誤導性的終態聲明。所有治理報告**必須**符合本規格，否則視為治理違規。

**適用範圍：**
- 所有由系統自動生成的治理報告
- 所有手動撰寫的治理分析報告
- 所有治理狀態聲明和進度報告

---

## 🚨 強制要求（MUST）

### 要求 1：報告必須明確標示三個欄位

所有治理報告必須在**開頭**（前 10 行內）明確標示以下三個欄位：

```markdown
**Layer:** <Operational | Governance>
**Era:** <數字> (<Era 名稱>)
**Semantic Closure:** <YES | NO> (<說明>)
```

**約束條件：**
- `Layer`: 只能是 "Operational" 或 "Governance"
  - Era-1 一律為 "Operational"
  - Era-2+ 可能為 "Governance"
- `Era`: 必須標示數字和名稱
  - Era-1: "Evidence-Native Bootstrap"
  - Era-2+: 根據實際定義
- `Semantic Closure`: 必須標示 YES 或 NO
  - Era-1 必須為 "NO"
  - 說明必須真實反映當前狀態

**範例：**
```markdown
**Layer:** Operational (Evidence Generation)
**Era:** 1 (Evidence-Native Bootstrap)
**Semantic Closure:** NO (Evidence layer only, governance not closed)
```

---

### 要求 2：禁止使用終態敘事

除非**明確**達到以下條件，**禁止**使用以下敘事：

**達到終態的條件：**
1. Governance Layer 已完成語義閉環（Semantic Closure = YES）
2. Immutable Core 已封存（core-hash.json 標記為 SEALED）
3. Era 封存流程已完成
4. 完整 Lineage 已驗證
5. 用戶明確聲明「已完成治理閉環並封存核心」

**禁止的敘事（除非滿足上述條件）：**
- ❌ "100% 治理合規"
- ❌ "所有治理元件全部通過"
- ❌ "完整治理閉環"
- ❌ "系統已完全準備好投入生產"
- ❌ "MNGA 架構完全通過"
- ❌ "治理閉環已建立"
- ❌ "Ready for Deployment: True"
- ❌ 任何包含「完全、全部、100%、零風險」等終態語言

**允許的替代敘事：**
- ✅ "Era-1 Evidence-Native Bootstrap 完成"
- ✅ "Operational Layer 達成穩定"
- ✅ "Evidence chain 已啟動"
- ✅ "達到 Era-1 階段性目標"
- ✅ "Era-1 治理基礎設施驗證通過"

---

### 要求 3：Era-1 的正確定位

Era-1 的報告必須明確說明其範圍和限制：

**Era-1 的範圍（只能聲明已完成的部分）：**
- ✅ 證據鏈基礎設施啟動（Evidence Infrastructure Bootstrap）
- ✅ Operational Layer 達成：真實證據生成 + 事件流存在 + SHA256 完整性
- ✅ Step-by-Step 執行軌跡記錄

**Era-1 未完成的部分（必須承認）：**
- ❌ Governance Layer 語義閉環
- ❌ Immutable Core 封存
- ❌ Era 封存
- ❌ 完整 Lineage
- ❌ Semantic Distillation
- ❌ v1.0.0 抽離

**Era-1 報告結論範例：**
```markdown
本次變更屬於 Evidence-Native Bootstrap，而非完整治理閉環。
目前僅在 Operational Layer 達成穩定，Governance Layer 仍在建構中。
未來仍需：Era 封存、核心 hash 封存、語義閉環與治理一致性驗證。
```

---

### 要求 4：必須承認歷史缺口

所有報告必須包含以下歷史聲明：

**必需的歷史缺口聲明：**
```markdown
## ⚠️ 歷史完整性聲明

- Era-0 歷史沒有完整的證據鏈，只能部分重建
- Era-1 是本系統第一個具備完整證據鏈的時期，仍在演化中
- 治理閉環、不可變核心、完整 MNGA 合規「尚未完成」
```

**約束條件：**
- 必須明確提及 Era-0 的證據鏈缺損
- 必須說明 Era-1 是第一個具備證據鏈的時期
- 必須承認治理閉環「尚未完成」

---

### 要求 5：允許的結論語氣

報告的結論部分必須遵守以下約束：

**允許的結論語氣範例（可以參考，但不得超出）：**
- "證據鏈基礎設施已在 Era-1 啟動，具備真實證據與事件流"
- "目前僅在 Operational Layer 達成穩定，Governance Layer 仍在建構中"
- "本次變更屬於 Evidence-Native Bootstrap，而非完整治理閉環"
- "未來仍需：Era 封存、核心 hash 封存、語義閉環與治理一致性驗證"
- "Era-1 治理基礎設施驗證通過，但 Governance Layer 尚未閉環"

**禁止的結論語氣：**
- 任何暗示「已完成」或「100%」的語氣
- 任何暗示「可上線生產」的語氣
- 任何省略 Governance Layer 未完成狀態的語氣

---

### 要求 6：必須包含「尚未完成的治理面」專門區塊

所有報告必須包含一個專門的區塊，說明尚未完成的治理面：

**必需的專門區塊：**
```markdown
## 🚧 尚未完成的治理面（Era-1 現狀）

### ❌ 尚未建立
- [列出所有尚未建立的治理功能]

### ⏳ 進行中
- [列出所有進行中的治理功能]

### ✅ 已完成（Era-1）
- [列出 Era-1 已完成的功能]
```

**約束條件：**
- 必須使用專門的 markdown 區塊（不是簡單的列表）
- 必須區分三種狀態：尚未建立、進行中、已完成
- 必須清楚標註這些是 Era-1 的現狀
- 必須包含具體的功能項目（不能只說「治理層未完成」）

---

## 📊 報告結構模板

### 推薦的報告結構

```markdown
# <報告標題>

**Layer:** Operational (Evidence Generation)
**Era:** 1 (Evidence-Native Bootstrap)
**Semantic Closure:** NO (Evidence layer only, governance not closed)

---

## 📋 執行摘要
[簡短摘要（最多 200 字）]

---

## 🚧 尚未完成的治理面（Era-1 現狀）

### ❌ 尚未建立
- Era 封存流程（Era Sealing Protocol）
- Core hash 封存（core-hash.json 標記為 SEALED）
- Semantic Distillation 流程
- v1.0.0 抽離與版本管理

### ⏳ 進行中
- Semantic Closure 定義與驗證
- Immutable Core 邊界確定
- 完整 Lineage 重建與驗證

### ✅ 已完成（Era-1）
- Evidence Generation Layer 啟動
- Event Stream 基礎設施
- SHA256 完整性保護
- Step-by-Step 執行軌跡

---

## ⚠️ 歷史完整性聲明

- Era-0 歷史沒有完整的證據鏈，只能部分重建
- Era-1 是本系統第一個具備完整證據鏈的時期，仍在演化中
- 治理閉環、不可變核心、完整 MNGA 合規「尚未完成」

---

## 📊 詳細執行內容
[詳細的執行內容、分析、數據等]

---

## 🎯 結論

本次變更屬於 Evidence-Native Bootstrap，而非完整治理閉環。
目前僅在 Operational Layer 達成穩定，Governance Layer 仍在建構中。
未來仍需：Era 封存、核心 hash 封存、語義閉環與治理一致性驗證。
```

---

## 🔍 合規性檢查

### 自動化檢查規則

**檢查 1：開頭三個欄位**
- 檢查報告開頭是否包含 Layer、Era、Semantic Closure
- 檢查 Layer 是否為 "Operational" 或 "Governance"
- 檢查 Era 是否為數字 + 名稱
- 檢查 Semantic Closure 是否為 YES 或 NO

**檢查 2：終態敘事檢測**
- 檢查是否包含 "100% 治理合規"、"完整治理閉環"、"已準備就緒" 等禁止詞彙
- 如果發現，檢查是否同時包含「已封存」、「已閉環」等必要條件

**檢查 3：歷史缺口聲明**
- 檢查是否提及 "Era-0"
- 檢查是否承認 "尚未完成" 或 "仍在演化中"

**檢查 4：未完成治理面區塊**
- 檢查是否存在專門區塊
- 檢查是否區分三種狀態

---

## 🚨 違規處理

### 違規級別

**CRITICAL（阻擋）：**
- 缺少開頭三個欄位
- 使用終態敘事但未達到必要條件
- 缺少歷史缺口聲明

**HIGH（警告）：**
- 未包含「尚未完成的治理面」專門區塊
- 結論語氣超出允許範圍

**MEDIUM（提醒）：**
- 結構不符合推薦模板
- 缺少合規性檢查

### 處理措施

**CRITICAL 違規：**
- 🔴 阻擋報告發布
- 🔴 要求重寫報告
- 🔴 記錄到治理事件流

**HIGH 違規：**
- 🟠 警告但仍允許發布
- 🟠 建議修正
- 🟠 記錄到治理事件流

**MEDIUM 違規：**
- 🟡 提醒
- 🟡 建議改進
- 🟡 不記錄到事件流

---

## 📝 版本歷史

| 版本 | 日期 | 變更 |
|------|------|------|
| v1.0.0 | 2026-02-03 | 初始版本，基於 Era-1 Evidence-Native Bootstrap |

---

## 🔄 規格演進

**Era-1:**
- 聚焦於 Evidence Layer
- 所有報告必須聲明 Operational Layer
- 禁止任何治理層的終態聲明

**Era-2+（待定義）：**
- 可能擴展到 Governance Layer
- 允許部分治理終態聲明
- 需要明確定義「治理閉環」的條件
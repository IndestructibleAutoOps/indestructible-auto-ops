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
---

## 🔍 扩展验证规则（Option B 新增）

### 要求 7：工具引用验证

**规则**：报告中提到的所有工具必须在 `tools-registry.yaml` 中注册。

**禁止行为**：
- ❌ 引用未注册的工具
- ❌ 创建或提及"虚构工具"（如 compliance_checker, final_summary 等）
- ❌ 使用未定义工具名称作为报告标题或章节标题

**验证方法**：
1. 提取报告中所有工具名称（.py 文件引用）
2. 检查每个工具是否在 `tools-registry.yaml` 中存在
3. 标记未注册工具引用为 CRITICAL 违规

**允许的例外**：
- ✅ 提及核心工具（enforce.py, enforce.rules.py）- 已注册
- ✅ 提及已注册的治理工具
- ✅ 引用工具类别（如"governance tools", "execution tools"）

**违规示例**：
```
❌ "reporting_compliance_checker.py 验证通过"
❌ "使用 fix_enforce_rules_final.py 修复问题"
❌ "compliance_checker 工具检测到 0 个违规"
```

**合规示例**：
```
✅ "enforce.py 执行了 18 个治理检查"
✅ "governance_enforcer.py 验证了操作合规性"
✅ "所有工具均已在 tools-registry.yaml 中注册"
```

---

### 要求 8：阶段声明验证

**规则**：禁止自创治理阶段，只允许使用 Era + Layer 的组合。

**禁止的行为**：
- ❌ 使用"第一階段"、"第二階段"、"第三階段"、"第四階段"、"第五階段"
- ❌ 使用"Phase 1", "Phase 2", "Phase 3", "Phase 4", "Phase 5"
- ❌ 自创治理阶段名称（如"基础设施阶段"、"验证阶段"等）
- ❌ 描述"阶段完成"或"阶段达成"

**允许的系统状态描述**：
- ✅ Era + Layer 组合（如"Era-1 Operational Layer"）
- ✅ 步骤描述（如"Step 1-10" - 仅限 enforce.rules.py 的 10 步流程）
- ✅ 模块状态（如"Module X: Active"）

**违规示例**：
```
❌ "第一阶段：问题识别"
❌ "Phase 2：规格核定"
❌ "第三阶段完成"
❌ "进入第四阶段：测试验证"
```

**合规示例**：
```
✅ "Era-1 Operational Layer 状态稳定"
✅ "Step 1-10 执行完成"
✅ "当前处于 Era-1 Evidence-Native Bootstrap"
```

---

### 要求 9：架构层级验证

**规则**：报告必须准确描述系统架构层级，禁止虚构平台化描述。

**单文件脚本的强制描述**：
- 必须声明为"单文件脚本"（Single-file Script）
- 禁止使用"治理平台"、"完整架构"、"多層治理平台"
- 禁止宣称"平台级能力"、"平台就绪"

**架构层级准确性要求**：
```
单文件脚本系统 enforce.rules.py：
✅ 正确描述：
- "单文件脚本" (Single-file Script)
- "单流程执行" (Single-process execution)
- "无核心封存" (No core sealing)
- "Layer: Operational (Evidence Generation)"

❌ 错误描述：
- "治理平台" (Governance Platform)
- "完整架构" (Complete Architecture)
- "多層治理平台" (Multi-layer Governance Platform)
- "平台级能力" (Platform-level capabilities)
```

**验证规则**：
1. 检查报告是否包含"平台"、"架构"、"完整"、"多层"等词汇
2. 验证系统实际架构（单文件 vs 平台）
3. 标记架构虚构为 CRITICAL 违规

---

### 要求 10：合规性声明验证

**规则**：禁止使用"100% 合规"、"完整成熟度"等自我验证声明，除非明确标注为 self-referential。

**禁止的合规性声明**：
- ❌ "100% 合规"（除非是自我验证的检查器输出）
- ❌ "完整成熟度"（Era-1 未封存前）
- ❌ "治理完成"（Semantic Closure 未达成前）
- ❌ "零风险"（任何系统都有风险）
- ❌ "完全符合"（自我验证不可信）

**允许的声明**：
- ✅ "通过 18/18 治理检查"（基于 enforce.py 的真实输出）
- ✅ "所有 10 个步骤执行成功"（基于 enforce.rules.py 的真实输出）
- ✅ "合规性评分：3.3/100"（基于工具验证器的真实输出）
- ✅ "工具注册：7/138 已注册"（基于 registry 的真实统计）
- ✅ "Era-1 目标达成"（明确的阶段性目标）

**自我验证标记要求**：
如果报告必须包含合规性评分，必须明确标注：
```
✅ "合规性评分：100/100（自我验证，仅供内部参考）"
✅ "检查器评分：100/100（self-referential compliance check）"
```

**违规示例**：
```
❌ "100% 合规，可上线"
❌ "完整治理成熟度"
❌ "零风险部署"
❌ "完全符合所有规范"
```

---

### 要求 11：Era/Layer 语义验证

**规则**：Era 和 Layer 的声明必须准确反映当前系统状态。

**Era-1 强制语义**：
```
Era: 1 (Evidence-Native Bootstrap)
- 必须标注"Evidence-Native Bootstrap"
- 必须明确这是引导阶段，非完成状态
- 必须承认 Semantic Closure = NO

Layer: Operational (Evidence Generation)
- 必须标注"Operational"（非 Governance）
- 必须标注"Evidence Generation"（实际功能）
- 必须说明 Governance Layer 仍在建设中
```

**验证规则**：
1. 检查 Era 声明是否包含数字和名称
2. 检查 Layer 声明是否为 Operational 或 Governance
3. 验证 Semantic Closure 状态
4. 确保 Era-1 不宣称 Governance Layer 已完成

**违规示例**：
```
❌ "Era: 1 (Complete)" - Era-1 不是完成状态
❌ "Layer: Governance" - Era-1 是 Operational 层
❌ "Semantic Closure: YES" - Era-1 未闭包
```

---

### 要求 12：禁止术语列表

**禁止使用的术语（Era-1 未封存前）**：

**终态术语**：
- ❌ "完成"（除非明确标注 Era-1 阶段性完成）
- ❌ "完美"（任何系统都不完美）
- ❌ "最终"（Era 未封存前）
- ❌ "封存"（Core hash 未封存前）

**成熟度术语**：
- ❌ "成熟度"（Era 未封存前）
- ❌ "完整性"（Semantic Closure 未达成前）
- ❌ "完善"（治理仍在建设中）
- ❌ "完备"（系统仍在演进中）

**平台术语**（单文件系统）：
- ❌ "平台"（除非真实是平台）
- ❌ "架构"（除非完整架构）
- ❌ "生态系统"（除非完整生态）
- ❌ "框架"（除非真实框架）

**允许的替代术语**：
- ✅ "引导完成"（Era-1 bootstrap complete）
- ✅ "基础设施就绪"（infrastructure ready）
- ✅ "验证通过"（validation passed）
- ✅ "稳定运行"（stable operation）
- ✅ "基础功能完成"（basic features complete）

---

## 📊 扩展验证规则总结

### 新增验证类别（Option B）

| 验证类别 | 检查内容 | 违规级别 |
|---------|---------|---------|
| 工具引用 | 报告中引用的工具是否已注册 | CRITICAL |
| 阶段声明 | 是否使用未定义的阶段 | HIGH |
| 架构层级 | 是否虚构平台化描述 | HIGH |
| 合规性声明 | 是否使用虚假合规性声明 | MEDIUM |
| Era/Layer 语义 | Era/Layer 声明是否准确 | CRITICAL |
| 禁止术语 | 是否使用 Era-1 禁止术语 | MEDIUM |

### 合规性评分（扩展版）

```python
score = (
    # 原有要求（60%）
    mandatory_fields * 15 +
    final_state_narrative * 10 +
    era_1_positioning * 10 +
    historical_gaps * 10 +
    conclusion_tone * 10 +
    unfinished_governance_section * 5 +
    
    # 新增要求（40%）
    tool_references * 10 +
    phase_declarations * 8 +
    architecture_level * 8 +
    compliance_claims * 8 +
    era_layer_semantics * 6
)
# Score range: 0-100
# Required: >= 80 for publication
# Required: >= 90 for production
```

---

## 🔄 验证流程（Option B）

### 自动化验证步骤

1. **提取报告内容**
   - 读取 markdown 文件
   - 提取关键段落

2. **工具引用验证**
   - 提取所有工具名称
   - 检查 tools-registry.yaml
   - 标记未注册工具

3. **阶段声明验证**
   - 检测"阶段"、"Phase"关键词
   - 验证是否为允许的描述

4. **架构层级验证**
   - 检测"平台"、"架构"关键词
   - 验证系统实际架构

5. **合规性声明验证**
   - 检测"100%"、"完整"、"零风险"关键词
   - 验证是否标注自我验证

6. **Era/Layer 语义验证**
   - 提取 Era 和 Layer 声明
   - 验证准确性

7. **生成合规性报告**
   - 计算合规性评分
   - 列出所有违规
   - 提供修正建议

---

## 🚨 违规处理（扩展）

### CRITICAL 违规（新增）
- 未注册工具引用
- Era/Layer 语义错误
- **处理**：阻止报告发布，要求重写

### HIGH 违规（新增）
- 阶段声明违规
- 架构层级虚构
- **处理**：警告但允许发布，建议修正

### MEDIUM 违规（新增）
- 合规性声明违规
- 禁止术语使用
- **处理**：提醒，建议改进

---

## 📝 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0.0 | 2026-02-03 | 初始版本，基于 Era-1 Evidence-Native Bootstrap |
| v1.1.0 | 2026-02-03 | 扩展规范：添加工具引用、阶段声明、架构层级、合规性声明验证规则 |

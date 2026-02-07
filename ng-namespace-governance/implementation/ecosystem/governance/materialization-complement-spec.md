# 實體化補件規格
# Materialization Complement Specification

## 1. 核心原則

### 1.1 不降階原則
- **禁止**：移除或降級已聲明的語義層次
- **保留**：所有架構、階段、合規性、完整性等聲明
- **實現**：為聲明提供可驗證的具體實體

### 1.2 實體化原則
- **可見性**：每個語義聲明必須有對應的文件、代碼、測試或配置
- **可驗證性**：實體必須能被驗證（存在性、正確性、完整性）
- **可追溯性**：語義聲明 → 實體 → 驗證結果，形成完整鏈條

### 1.3 補件原則
- **自動生成**：根據語義聲明自動生成補件清單和模板
- **人工補充**：允許人工添加特定的補件項目
- **持續更新**：隨著語義演進，補件應同步更新

## 2. 語義聲明類型

### 2.1 架構層級聲明
**聲明示例**：
- "治理平台" (Governance Platform)
- "完整閉環" (Complete Closed Loop)
- "統一治理" (Unified Governance)

**實體化補件要求**：
1. 架構圖：系統架構圖、組件關係圖
2. API 文檔：所有公開接口的定義
3. 組件清單：所有組件的名稱、職責、依賴
4. 配置文件：平台配置、環境設置

### 2.2 階段聲明
**聲明示例**：
- "Phase 1: 基礎設施建設"
- "Phase 2: 語義層建立"
- "Phase 3: 治理閉環"

**實體化補件要求**：
1. 階段定義文檔：目標、範圍、交付物
2. 階段檢查清單：完成標準、驗收條件
3. 階段狀態文件：當前進度、完成度
4. 階段切換記錄：切換時間、決策人、理由

### 2.3 合規性聲明
**聲明示例**：
- "100% 合規" (100% Compliance)
- "完全符合規範" (Fully Compliant)
- "所有檢查通過" (All Checks Passed)

**實體化補件要求**：
1. 合規性報告：詳細檢查結果、得分、違規項
2. 證據清單：所有支持合規聲明的證據
3. 驗證腳本：可重複執行的驗證腳本
4. 趨勢圖表：合規性變化趨勢

### 2.4 完整性聲明
**聲明示例**：
- "完整性保證" (Integrity Guarantee)
- "無缺點" (No Defects)
- "完整覆蓋" (Full Coverage)

**實體化補件要求**：
1. 覆蓋率報告：代碼覆蓋、測試覆蓋、需求覆蓋
2. 完整性檢查清單：所有完整性指標
3. 缺陷追蹤：已知缺陷、修復計劃
4. 質量門檻：達到的質量指標

### 2.5 Era/Layer/Semantic Closure 聲明
**聲明示例**：
- "Era: 1 (Evidence-Native Bootstrap)"
- "Layer: Operational"
- "Semantic Closure: NO"

**實體化補件要求**：
1. Era 定義文檔：當前 Era 的定義、目標、限制
2. Layer 定義文檔：當前 Layer 的職責、範圍
3. Semantic Closure 文檔：當前語義封閉狀態、未封閉的原因
4. Era 遷移計劃：下一 Era 的準備工作

## 3. 實體類型

### 3.1 文檔實體
- Markdown 文檔 (`.md`)
- 圖表文件 (`.drawio`, `.png`, `.svg`)
- 配置文件 (`.yaml`, `.json`, `.toml`)

### 3.2 代碼實體
- Python 模組 (`.py`)
- 測試文件 (`test_*.py`, `*_test.py`)
- 腳本工具 (`tools/*.py`)

### 3.3 數據實體
- JSON 數據文件 (`.json`)
- YAML 數據文件 (`.yaml`)
- 事件流文件 (`.jsonl`)

### 3.4 證據實體
- 執行日誌 (`.log`)
- 測試報告 (`.xml`, `.html`)
- 審計記錄 (`.audit`)

## 4. 補件生成流程

### 4.1 掃描階段
1. 掃描所有報告文件 (`reports/*.md`)
2. 提取語義聲明（使用規則匹配）
3. 識別聲明類型（架構、階段、合規、完整、Era/Layer）

### 4.2 對比階段
1. 掃描現有文件和代碼
2. 對照語義聲明，識別缺失實體
3. 標記實體狀態（存在、缺失、不完整）

### 4.3 生成階段
1. 為每個缺失實體生成補件清單
2. 提供補件模板或生成腳本
3. 生成驗證方法

### 4.4 驗證階段
1. 驗證補件的完整性
2. 驗證補件的正確性
3. 生成補件報告

## 5. 補件模板

### 5.1 架構聲明補件模板
```yaml
architecture_complement:
  declaration: "治理平台"
  required_entities:
    - type: document
      name: "平台架構圖"
      location: "docs/architecture/platform-architecture.md"
      template: "architecture-diagram-template.md"
    - type: document
      name: "API 文檔"
      location: "docs/api/platform-api.md"
      template: "api-doc-template.md"
    - type: document
      name: "組件清單"
      location: "docs/architecture/component-list.md"
      template: "component-list-template.md"
    - type: config
      name: "平台配置"
      location: "config/platform.yaml"
      template: "platform-config-template.yaml"
  verification_methods:
    - "檢查文件是否存在"
    - "驗證架構圖一致性"
    - "驗證 API 文檔完整性"
```

### 5.2 階段聲明補件模板
```yaml
phase_complement:
  declaration: "Phase 1: 基礎設施建設"
  required_entities:
    - type: document
      name: "階段定義"
      location: "phases/phase-1/definition.md"
      template: "phase-definition-template.md"
    - type: document
      name: "階段檢查清單"
      location: "phases/phase-1/checklist.md"
      template: "phase-checklist-template.md"
    - type: data
      name: "階段狀態"
      location: "phases/phase-1/status.json"
      template: "phase-status-template.json"
    - type: data
      name: "階段切換記錄"
      location: "phases/phase-1/transitions.jsonl"
      template: "phase-transitions-template.jsonl"
  verification_methods:
    - "檢查階段定義完整性"
    - "驗證檢查清單覆蓋"
    - "驗證狀態文件格式"
```

### 5.3 合規性聲明補件模板
```yaml
compliance_complement:
  declaration: "100% 合規"
  required_entities:
    - type: document
      name: "合規性報告"
      location: "reports/compliance-report.md"
      template: "compliance-report-template.md"
    - type: document
      name: "證據清單"
      location: "reports/evidence-list.md"
      template: "evidence-list-template.md"
    - type: code
      name: "驗證腳本"
      location: "tools/verify_compliance.py"
      template: "verify-compliance-template.py"
    - type: data
      name: "合規性趨勢"
      location: "reports/compliance-trends.json"
      template: "compliance-trends-template.json"
  verification_methods:
    - "執行驗證腳本"
    - "檢查證據清單完整性"
    - "驗證趨勢數據連續性"
```

## 6. 驗證規則

### 6.1 文檔驗證規則
- 文件必須存在
- 文件必須有實質內容（不為空）
- 文件必須符合模板結構
- 文件必須與語義聲明一致

### 6.2 代碼驗證規則
- 代碼必須可執行
- 代碼必須有測試
- 測試必須通過
- 代碼必須符合風格規範

### 6.3 數據驗證規則
- 數據文件必須可解析
- 數據結構必須符合 schema
- 數據必須完整（無缺失字段）
- 數據必須一致（無矛盾）

## 7. 補件報告

### 7.1 報告結構
```markdown
# 實體化補件報告

## 執行摘要
- 總語義聲明數：N
- 缺失實體數：M
- 補件完成率：X%
- 合規性評分：Y/100

## 語義聲明分析
### 2.1 架構層級聲明
- 聲明數：N1
- 缺失實體：M1
- 合規性：Y1/100

### 2.2 階段聲明
- 聲明數：N2
- 缺失實體：M2
- 合規性：Y2/100

...

## 補件清單
### 補件 #1：平台架構圖
- 語義聲明："治理平台"
- 實體類型：文檔
- 位置：docs/architecture/platform-architecture.md
- 狀態：⏸️ 待生成
- 優先級：🔴 HIGH

...

## 驗證結果
### 驗證通過的實體：N
### 驗證失敗的實體：M
### 需要人工干預：K

## 下一步行動
- [ ] 生成補件模板
- [ ] 填充補件內容
- [ ] 執行驗證
- [ ] 更新報告
```

## 8. 工具接口

### 8.1 命令行接口
```bash
# 掃描並生成補件清單
python ecosystem/tools/materialization_complement_generator.py \
    --scan-reports /workspace/reports \
    --generate-complements \
    --output-dir /workspace/complements

# 驗證補件完整性
python ecosystem/tools/materialization_complement_generator.py \
    --verify-complements \
    --report-file /workspace/reports/complement-verification.md

# 生成特定類型的補件
python ecosystem/tools/materialization_complement_generator.py \
    --type architecture \
    --declaration "治理平台" \
    --generate-templates
```

### 8.2 輸出格式
- Markdown 報告 (`.md`)
- JSON 清單 (`.json`)
- YAML 配置 (`.yaml`)

## 9. Era-1 特殊規則

### 9.1 Era-1 限制
- Era-1 是 "Evidence-Native Bootstrap"
- 不強制要求完整語義封閉
- 允許部分實體缺失
- 要求提供缺失實體的計劃

### 9.2 Era-1 合規標準
- 語義聲明必須有意義（不虛構）
- 存在的實體必須可驗證
- 缺失的實體必須有計劃
- 補件進度必須可追蹤

## 10. 持續改進

### 10.1 反饋機制
- 收集補件生成錯誤
- 優化模板結構
- 改進驗證規則

### 10.2 自動化增強
- 自動生成簡單補件
- 自動驗證常見實體
- 自動更新補件清單

---

**版本**: v1.0.0  
**Era**: 1 (Evidence-Native Bootstrap)  
**創建日期**: 2026-02-04  
**狀態**: APPROVED
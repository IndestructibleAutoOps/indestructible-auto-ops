# 當前專案結構文檔

## 生成時間
2026-02-09 13:16:31

## 根層目錄概覽

### 統計數據
- **總目錄數**: 35 個
- **總文件數**: 4,604 個
- **主要語言**: Python, YAML, JSON, Markdown

### 目錄分類

#### 1. 核心系統（5個）
- `iaops/` - IAOPS 治理引擎
- `indestructibleautoops/` - Python 包
- `machinenativeops/` - 機器原生操作
- `IndestructibleAutoOps/` - 應用程序
- `governance/` - 治理系統

#### 2. 平台與部署（4個）
- `platforms/` - 平台系統
- `deployment/` - 部署配置
- `deployment-scripts/` - 部署腳本
- `monitoring/` - 監控系統

#### 3. 文檔與配置（4個）
- `docs/` - 文檔
- `config/` - 配置文件
- `scripts/` - 腳本
- `tests/` - 測試

#### 4. 責任邊界（18個）⚠️ 需要整合
- `responsibility-gap-boundary/`
- `responsibility-gates-boundary/`
- `responsibility-gateway-boundary/`
- `responsibility-gcp-boundary/`
- `responsibility-generation-boundary/`
- `responsibility-gov-layers-boundary/`
- `responsibility-global-policy-boundary/`
- `responsibility-governance-anchor-boundary/`
- `responsibility-governance-execution-boundary/`
- `responsibility-governance-sensing-boundary/`
- `responsibility-governance-specs-boundary/`
- `responsibility-group-boundary/`
- `responsibility-guardrails-boundary/`
- `responsibility-mnga-architecture-boundary/`
- `responsibility-mno-operations-boundary/`
- `responsibility-namespace-governance-boundary/`
- `responsibility-observability-grafana-boundary/`
- `responsibility-quantum-stack-boundary/`

#### 5. 企業與審計（2個）
- `enterprise-governance/` - 企業治理
- `audit-automation/` - 審計自動化

#### 6. 其他（2個）
- `archives/` - 歸檔
- `ecosystem/` - 生態系統

## 命名前綴分析

### gl- 前綴（120項）
主要用於治理相關的組件：
- gov-evolution-data
- gov-gate
- gov-artifacts
- gov-hooks
- gov-restructure
- gov-engine
- gov-core
- gov-governance
- gov-platform-assistant
- gov-platform-ide

### gl. 前綴（13項）
點號表示法的治理標識符：
- gl.platform-assistant
- gl.platform-ide
- gl.causal-reasoning-spec
- gl.execution.finalization-spec
- gl.evolution-metrics
- gl.cognitive-modes-spec
- gl.execution.analysis-report
- gl.flow.upgrade-log
- gl.execution.delta-report
- gl.verifiable-report-spec

### governance 前綴（52項）
治理相關的文件和目錄：
- governance（37項）
- governance-audit
- governance-legacy
- governance-enforcement-implementation-complete
- governance-enforcement-progress
- governance-enforcement-layer-todo
- governance-files-migration-complete
- governance-files-migration-plan
- governance-restructure-executor
- governance-event-stream（4項）

### gov_ 前綴（26項）
gov_ 前綴的治理組件：
- gov_policy
- gov_contract
- gov_evolution_engine
- gov_pre_commit（2項）
- gov_naming_check（2項）
- gov_consolidation_plan（2項）
- gov_integrator（2項）
- gov_executor（2項）
- gov_validator（2項）
- gov_reporter（2項）

### responsibility- 前綴（18項）
責任邊界目錄：
- responsibility-gap-boundary
- responsibility-gates-boundary
- responsibility-gateway-boundary
- responsibility-gcp-boundary
- responsibility-generation-boundary
- responsibility-gov-layers-boundary
- responsibility-global-policy-boundary
- responsibility-governance-anchor-boundary
- responsibility-governance-execution-boundary
- responsibility-governance-sensing-boundary
- responsibility-governance-specs-boundary
- responsibility-group-boundary
- responsibility-guardrails-boundary
- responsibility-mnga-architecture-boundary
- responsibility-mno-operations-boundary
- responsibility-namespace-governance-boundary
- responsibility-observability-grafana-boundary
- responsibility-quantum-stack-boundary

## 命名不一致問題

### 1. 混合命名約定
- kebab-case: `governance-enforcement-implementation-complete`
- camelCase: `IndestructibleAutoOps`
- snake_case: `gov_naming_check`

### 2. 重複前綴
- `deployment`: deployment, deployment-scripts
- `responsibility`: 18 個目錄共用同一前綴

### 3. 前綴不統一
- gl- vs gl. vs gl_ vs GL_
- governance vs gov_

## 文件分佈

### Python 文件
主要分佈在：
- `iaops/` - 治理引擎核心
- `indestructibleautoops/` - Python 包
- `scripts/` - 腳本和工具
- 根目錄 - 各種修復和分析腳本

### YAML 文件
主要分佈在：
- `config/` - 配置文件
- `.github/workflows/` - CI/CD 工作流
- `.governance/` - 治理配置

### JSON 文件
主要分佈在：
- `governance/` - 治理數據
- 根目錄 - 各種報告和數據文件

### Markdown 文件
主要分佈在：
- `docs/` - 文檔
- 根目錄 - 各種文檔和報告

## 關鍵發現

### 🔴 高優先級問題
1. **18 個 responsibility-* 目錄** 應該整合到單一目錄
2. **命名前綴不統一** 影響可維護性
3. **根層目錄過多**（35個）降低可讀性

### 🟡 中優先級問題
1. **混合命名約定** 降低一致性
2. **重複前綴** 導致混淆
3. **文檔分散** 難以查找

### 🟢 低優先級問題
1. **部分目錄空閒** 浪費空間
2. **臨時文件未清理** 影響整潔度

## 下一步行動

基於此結構分析，下一階段將：
1. 整合 18 個 responsibility-* 目錄
2. 統一命名前綴為 `gov-`
3. 建立 L0-L4 治理層級結構
4. 清理根層目錄

---

**文檔版本**: 1.0  
**最後更新**: 2026-02-09 13:16:31
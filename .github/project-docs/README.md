# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: documentation
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
# Project Documentation

本目錄包含 MachineNativeOps 專案的所有文檔、報告和工具腳本。

## 目錄結構

```
project-docs/
├── gl-governance/          # GL 治理層文檔
│   ├── reports/            # GL 執行報告和驗證文檔
│   ├── schemas/            # GL JSON schemas 和配置
│   └── semantic-terms/     # GL 語義術語定義
├── cicd/                   # CI/CD 相關文檔
│   ├── guides/             # CI/CD 操作指南
│   └── reports/            # CI/CD 修復報告
├── scripts/                # 工具腳本
├── analysis/               # 分析報告
└── archive/                # 歷史文件和備份
```

## GL 治理層 (`gl-governance/`)

### 報告 (`reports/`)
- **GL-AUTOMATION-ARCHITECTURE.md** - GL 自動化架構設計
- **GL-CICD-IMPLEMENTATION-SUMMARY.md** - GL CI/CD 實施摘要
- **GL-GOVERNANCE-AUDIT-COMPLETION-SUMMARY.md** - 治理審計完成摘要
- **GL10-TOP10-FINAL-SUMMARY.md** - GL10 Top 10 最終摘要
- **GL30-49-EXECUTION-LAYER-ANALYSIS-REPORT.md** - 執行層分析報告

### Schemas (`schemas/`)
- **GL99-unified-charter.json** - 統一章程配置
- **GL00-root-semantic-anchor.json** - 根語義錨點
- **GL01-risk-registry.json** - 風險登記表
- **GL02-success-metrics.json** - 成功指標

### 語義術語 (`semantic-terms/`)
- **GL17-GL20** - 語義術語定義 (process, standard, monitoring, resource)
- **GL21-GL24** - 功能定義 (optimization, scheduling, risk-control, supervision)

## CI/CD 文檔 (`cicd/`)

### 指南 (`guides/`)
- **CI_CD_SOP.md** - CI/CD 標準作業程序
- **CI_CD_QUICK_START.md** - CI/CD 快速入門
- **DEPLOYMENT_GUIDE.md** - 部署指南
- **PRODUCTION_BUG_FIX_GUIDE.md** - 生產環境錯誤修復指南

### 報告 (`reports/`)
- **FINAL_WORKFLOW_FIX_REPORT.md** - 工作流修復最終報告
- **DEEP_WORKFLOW_ANALYSIS_REPORT.md** - 深度工作流分析報告
- **BUG_FIX_COMPLETION_REPORT.md** - 錯誤修復完成報告

## 工具腳本 (`scripts/`)

| 腳本 | 用途 |
|------|------|
| `deep-workflow-analyzer.py` | 深度工作流分析工具 |
| `enhanced_yaml_parser.py` | 增強型 YAML 解析器 |
| `gl_governance_audit_engine.py` | GL 治理審計引擎 |
| `governance_executor.py` | 治理執行器 |
| `workflow-cleanup-fixer.py` | 工作流清理修復工具 |

## 分析報告 (`analysis/`)

- **conflict_analysis_report.json** - 衝突分析報告
- **consistency_analysis_results.json** - 一致性分析結果
- **system_integration_report.md** - 系統整合報告
- **PROJECT_STATUS.md** - 專案狀態

## 歷史文件 (`archive/`)

包含已完成階段的文檔和備份文件，供參考用途。

---

*最後更新: 2025-01-27*
# NG 命名空間治理體系

**版本**: 4.0.0  
**狀態**: Closed-Loop Complete  
**編碼範圍**: NG000~999  
**檔案數量**: 160+  
**閉環狀態**: v2 Adaptive Controlled Loop - 14/14 tests passing

## 概述

NG (Namespace Governance) 是一個完整的命名空間治理閉環體系，涵蓋從代碼層（Era-1）到微碼層（Era-2）再到無碼層（Era-3）的完整命名空間生命週期管理。

本目錄是**儲存庫中所有命名空間治理和命名規範相關內容的集中管理中心**，包括：
- NG 編碼體系規範（NG000-999）
- **閉環治理系統（v2 自適應受控迴圈）** - 完整的 SHA3 狀態鎖定、分層驗證、外部約束決策、實時成本評估、密碼學審計鏈
- 命名規範定義（GL 命名本體、26 層命名層級規範）
- 跨 Era 映射引擎和工具鏈
- 命名違規檢測、修復和驗證工具
- 合規性報告和分析數據
- CI/CD 工作流和監控儀表板

## 快速開始

### 註冊命名空間
```bash
python tools/ng-cli.py register \
  --namespace pkg.era1.platform.core \
  --owner platform-team \
  --description "平台核心包"
```

### 列出命名空間
```bash
python tools/ng-cli.py list --era era1
```

### 查看統計
```bash
python tools/ng-cli.py stats
```

## NG 編碼體系

```
NG{層級}{領域}{子類}{序列}
```

### 層級範圍

| 範圍 | Era | 描述 |
|------|-----|------|
| NG000-099 | Meta | 元框架和基礎規範 ✅ |
| NG100-299 | Era-1 | 代碼層命名空間 📋 |
| NG300-599 | Era-2 | 微碼層命名空間 📋 |
| NG600-899 | Era-3 | 無碼層命名空間 📋 |
| NG900-999 | Cross-Era | 跨層級治理 📋 |

### Era 定義

**Era-1: 代碼層**
- 靜態代碼結構
- 包、模組、類、函數
- 範圍: NG100-299

**Era-2: 微碼層**
- 動態服務和分佈式系統
- 服務、API、事件、數據流
- 範圍: NG300-599

**Era-3: 無碼層**
- 意圖驅動和語義理解
- 意圖、語義、神經網絡
- 範圍: NG600-899

## 核心規範（Batch 1 ✅）

### NG00000: 治理憲章
定義核心原則：唯一性、層級性、一致性、可追溯性、閉環性

### NG00101: 標識規範
統一的命名空間標識符格式和命名規範

### NG00201: 生命週期規範
從創建到歸檔的完整生命週期管理

### NG00301: 驗證規則
唯一性、格式、層級結構、Era 一致性驗證

### NG00401: 權限模型
4 級權限系統和角色基礎訪問控制

### NG00501: 版本控制
語義版本控制和兼容性管理

### NG00701: 審計追蹤
完整的審計事件和追蹤系統

### NG90101: 跨 Era 映射
Era 間命名空間映射和轉換規則

### NG90200: 閉環治理系統
v2 自適應受控迴圈 - 完整的狀態鎖定、驗證門、決策引擎、成本評估、審計追蹤

## 閉環治理系統（Closed-Loop Governance v2）

基於 `designs/closed-loop-integrity-analysis.md` 的分析實現的完整閉環系統：

```
【初始狀態鎖定 (SHA3-512)】
    |
【Layer 0: 假設驗證 (不可繞過)】
    |
【Layer 1-4: 分層驗證 (可配置)】
    |
【執行工作】
    |
【成本/收益記錄 (已實現 ROI)】
    |
【決策引擎 (外部約束優先)】
    +-- 目標達成 -> 終止 (成功)
    +-- 時間/資源耗盡 -> 終止 (約束)
    +-- 正常 -> 繼續 (標準/調整/降級)
    |
【密碼學審計鏈 (SHA3-256)】
    |
（下一輪 或 終止）
```

**組件**：`closed-loop/` 目錄
- `state_lock.py` - SHA3-512 不可變狀態鏈
- `verification_gates.py` - 分層驗證門（Layer 0 不可繞過）
- `decision_engine.py` - 外部約束驅動決策
- `cost_evaluator.py` - 實時已實現 ROI
- `audit_trail.py` - 密碼學審計鏈
- `cycle_orchestrator.py` - 完整生命週期編排
- `test_closed_loop.py` - 14 項整合測試（全通過）
- `closed-loop-config.yaml` - 配置 schema（含 SOC2/ISO27001/GDPR 映射）

## 目錄結構

```
ng-namespace-governance/
├── NG-CHARTER.md                        # 治理憲章
├── README.md                            # 本文件
│
├── core/                                # 核心規範 (NG000-099)
│   ├── NG00000-charter.yaml             #   治理憲章 YAML
│   ├── NG00101-identifier-standard.yaml #   標識規範
│   ├── NG00201-lifecycle-standard.yaml  #   生命週期規範
│   ├── NG00301-validation-rules.yaml    #   驗證規則
│   ├── NG00401-permission-model.yaml    #   權限模型
│   ├── NG00501-version-control.yaml     #   版本控制
│   ├── NG00701-audit-trail.yaml         #   審計追蹤
│   ├── ng-namespace-core.yaml           #   命名空間核心定義
│   ├── ng-namespace-access-policy.yaml  #   訪問策略
│   ├── ng-executor.py                   #   核心執行器
│   ├── ng-orchestrator.py               #   編排器
│   ├── ng-enforcer-strict.py            #   嚴格執行器
│   ├── ng-closure-engine.py             #   閉環引擎
│   ├── ng-batch-executor.py             #   批次執行器
│   └── ng-ml-self-healer.py             #   ML 自修復引擎
│
├── era-1/                               # Era-1 代碼層 (NG100-299)
│   └── ng-era1-namespace.yaml           #   Era-1 命名空間規範
│
├── era-2/                               # Era-2 微碼層 (NG300-599)
│   ├── ng-era2-namespace.yaml           #   Era-2 命名空間規範
│   ├── scripts/                         #   Era-2 執行腳本
│   │   ├── era2-activation.py           #     Era-2 啟動腳本
│   │   └── era2-upgrade-exec.py         #     Era-2 升級管線執行器
│   └── reports/                         #   Era-2 執行報告
│       ├── era2-activation-summary.md
│       └── era2-workflow-execution.json
│
├── era-3/                               # Era-3 無碼層 (NG600-899)
│   └── ng-era3-namespace.yaml           #   Era-3 命名空間規範
│
├── cross-era/                           # 跨 Era 規範 (NG900-999)
│   ├── NG90101-cross-era-mapping.yaml   #   跨 Era 映射規範
│   ├── era1-to-era2-mapping.yaml
│   ├── era2-to-era3-mapping.yaml
│   ├── ng-era1-era2-mapping.yaml
│   ├── ng-era2-era3-mapping.yaml
│   └── ng-era-comparison.md             #   跨 Era 比較文檔
│
├── closed-loop/                          # 閉環治理系統 (v2)
│   ├── state_lock.py                    #   SHA3-512 狀態鎖定鏈
│   ├── verification_gates.py            #   分層驗證門
│   ├── decision_engine.py               #   外部約束決策引擎
│   ├── cost_evaluator.py                #   實時 ROI 評估器
│   ├── audit_trail.py                   #   密碼學審計追蹤
│   ├── cycle_orchestrator.py            #   迴圈生命週期編排
│   ├── test_closed_loop.py              #   整合測試 (14/14)
│   └── closed-loop-config.yaml          #   配置 schema
│
├── specs/                               # 命名規範定義
│   ├── naming-conventions.yaml          #   命名規範（目錄/文件/代碼）
│   ├── naming-governance-directory-standards.yaml  # 目錄標準
│   ├── external-best-practices.yaml     #   外部最佳實踐
│   ├── global-aliases.yaml              #   全域別名
│   ├── gov-naming-layers/                #   GL 命名本體 26 層級規範
│   │   ├── gov-naming-ontology.yaml
│   │   ├── gov-naming-ontology-expanded.yaml
│   │   ├── gov-prefix-principles-engineering.md
│   │   └── gl-*-layer-specification.md  #   (26 個層級規範)
│   └── gov-naming-registry/              #   GL 命名契約註冊表
│       ├── gov-naming-contracts-registry.yaml
│       └── GL-NAMING-CONTRACTS-REGISTRY-SUMMARY.md
│
├── policies/                            # 治理策略
│   ├── naming-policy.rego               #   OPA Rego 命名策略
│   └── naming-filesystem-policy.yaml    #   文件系統命名策略
│
├── schemas/                             # JSON Schema
│   └── naming.schema.json               #   命名格式 Schema
│
├── tools/                               # 工具鏈（20+ 工具）
│   ├── ng-cli.py                        #   NG 命令行工具
│   ├── ng-mapper.py                     #   命名空間映射器
│   ├── ng-transformer.py                #   命名空間轉換器
│   ├── ng-namespace-guard.py            #   命名空間守護（零容忍）
│   ├── ng-namespace-validator.py        #   命名空間驗證器
│   ├── ng-namespace-pipeline.py         #   NG 管線（5 階段流）
│   ├── ng-era-mapping-engine.py         #   跨 Era 映射引擎
│   ├── gov-naming-validator.py           #   GL 命名驗證器
│   ├── naming-enforcer.py              #   命名規範強制執行器
│   ├── naming-consistency-alignment.py  #   命名一致性對齊
│   ├── naming-conventions-index.py      #   命名規範索引器
│   ├── naming-audit.sh                  #   命名審計腳本
│   ├── scan-naming-violations.py        #   命名違規掃描器
│   ├── fix-naming-violations.py         #   命名違規自動修復
│   ├── fix-namespace-violations.sh      #   命名空間違規修復
│   ├── apply-naming-alignment.py        #   命名對齊應用
│   ├── apply-file-naming-alignment.py   #   文件命名對齊
│   └── fix-ng10100-*.py/sh             #   NG10100 專項修復工具
│
├── analysis/                            # 分析數據
│   ├── ng-cross-era-matrix.json         #   跨 Era 映射矩陣
│   ├── actual-ng-validation-results.json
│   ├── evidence-chain-report.json       #   證據鏈報告
│   └── violation-catalog.json           #   違規目錄
│
├── reports/                             # 報告中心
│   ├── naming-conventions-index.json    #   命名規範索引
│   ├── scan-results.json                #   掃描結果
│   ├── naming-violations-report.json    #   命名違規報告
│   ├── naming-fix-map.json              #   修復映射
│   ├── ng10100-fix-*.json               #   NG10100 修復報告
│   ├── era2-*.md/json                   #   Era-2 升級報告
│   ├── governance-verification-beyond-era1.md
│   ├── naming/                          #   歷史命名對齊報告
│   └── mnga/                            #   MNGA 合規性報告
│
├── registry/                            # 命名空間註冊系統
│   ├── namespace-registry.py
│   └── namespaces.json
│
├── cicd/                                # CI/CD
│   └── ng-validation-workflow.yml       #   GitHub Actions 工作流
│
├── monitoring/                          # 監控
│   └── ng-compliance-dashboard.html     #   合規性儀表板
│
└── docs/                                # 文檔
    ├── NG-BATCH-1-IMPLEMENTATION-PLAN.md
    ├── NG-EXECUTION-ENGINES.md
    ├── LG-TO-NG-TRANSITION-PLAN.md
    ├── NG-Namespace-Governance-Whitepaper.md
    ├── ng-namespace-index.md            #   完整 NG000-999 索引
    ├── gov-naming-ontology-complete.md   #   GL 命名本體完成報告
    ├── gov-naming-ontology-gap-analysis.md  # 缺失分析
    ├── GL-NAMING-ONTOLOGY-EXPANDED-INTEGRATION.md
    ├── naming-governance-analysis-report.md
    ├── naming-governance-analysis-task.md
    ├── naming-governance-structure-definition.md
    ├── naming-examples.md               #   命名驗證工具使用範例
    └── professional-naming-restructure-proposal.md
```

## 使用範例

### Python API

```python
from registry.namespace_registry import (
    NgNamespaceRegistry,
    NamespaceSpec,
    Era
)

# 創建註冊系統
registry = NgNamespaceRegistry()

# 註冊命名空間
spec = NamespaceSpec(
    namespace_id="svc.era2.platform.api",
    namespace_type="service",
    era=Era.ERA_2,
    domain="platform",
    component="api",
    owner="platform-team",
    description="平台 API 服務"
)

ns_id = registry.register_namespace(spec)
print(f"註冊成功: {ns_id}")

# 查詢命名空間
record = registry.get_namespace(ns_id)
print(f"NG Code: {record.ng_code}")

# 統計
stats = registry.get_statistics()
print(f"總命名空間數: {stats['total']}")
```

### 命令行

```bash
# 註冊
python tools/ng-cli.py register \
  --namespace svc.era2.runtime.executor \
  --owner runtime-team \
  --description "運行時執行器服務"

# 列出 Era-2 的所有命名空間
python tools/ng-cli.py list --era era2

# 驗證命名空間
python tools/ng-cli.py validate --namespace svc.era2.runtime.executor

# 查看統計
python tools/ng-cli.py stats
```

## 與 GL 系統關係

### 共存模式
- NG 專注於命名空間治理
- GL 繼續處理整體治理（層級邊界、合規性檢查）
- 兩系統通過 NG90101 映射規範協作

### 語義替換
- GL Layer → NG Era
- GL Governance → NG Namespace Governance
- GL Compliance → NG Closure
- GL Boundary → NG Scope

## 批次實施狀態

| 批次 | 範圍 | 焦點 | 狀態 |
|------|------|------|------|
| 1 | NG000-099 | 元框架 | ✅ COMPLETE |
| 2 | NG100-299 | Era-1 代碼層 | 📋 READY |
| 3 | NG300-599 | Era-2 微碼層 | 📋 PLANNED |
| 4 | NG600-899 | Era-3 無碼層 | 📋 PLANNED |
| 5 | NG900-999 | 跨 Era 閉環 | 📋 PLANNED |

## 文檔資源

### 核心文檔
- **NG-CHARTER.md** - 治理憲章和核心原則
- **docs/NG-Namespace-Governance-Whitepaper.md** - NG 命名空間治理白皮書
- **docs/ng-namespace-index.md** - 完整 NG000-999 命名空間索引

### 規範和計劃
- **docs/NG-BATCH-1-IMPLEMENTATION-PLAN.md** - 批次 1 實施計劃
- **docs/LG-TO-NG-TRANSITION-PLAN.md** - LG→NG 轉型計劃
- **specs/naming-conventions.yaml** - 完整命名規範定義
- **specs/gov-naming-layers/** - GL 26 層命名本體規範

### 分析和報告
- **analysis/** - 驗證結果、證據鏈和違規目錄
- **reports/** - 執行報告、升級摘要、合規性報告
- **reports/mnga/** - MNGA 命名架構分析報告

### 工具
- **tools/** - 20+ 命名治理工具（驗證、修復、對齊、掃描）

## 貢獻指南

### 新增規範
1. 分配 NG 編碼（根據 Era 和領域）
2. 創建 YAML 規範文件
3. 更新相關註冊系統
4. 編寫測試用例
5. 更新文檔

### 報告問題
1. 使用 NG CLI 驗證命名空間
2. 查看審計日誌
3. 提交 issue 包含 NG Code

## 授權

NG 命名空間治理體系遵循與主儲存庫相同的授權條款。

---

**維護者**: NG Governance Committee  
**最後更新**: 2026-02-06  
**下一次審查**: 2027-02-06

# NG 命名空間治理體系

**版本**: 3.0.0  
**狀態**: Batch 1 Complete  
**編碼範圍**: NG000~999

## 概述

NG (Namespace Governance) 是一個完整的命名空間治理閉環體系，涵蓋從代碼層（Era-1）到微碼層（Era-2）再到無碼層（Era-3）的完整命名空間生命週期管理。

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

## 目錄結構

```
ng-namespace-governance/
├── NG-CHARTER.md                    # 治理憲章
├── README.md                        # 本文件
├── core/                            # 核心規範 (NG000-099)
│   ├── NG00000-charter.yaml
│   ├── NG00101-identifier-standard.yaml
│   ├── NG00201-lifecycle-standard.yaml
│   ├── NG00301-validation-rules.yaml
│   ├── NG00401-permission-model.yaml
│   ├── NG00501-version-control.yaml
│   ├── NG00701-audit-trail.yaml
│   ├── ng-namespace-core.yaml       # 命名空間核心定義
│   └── ng-namespace-access-policy.yaml  # 訪問策略
├── era-1/                           # Era-1 規範 (NG100-299)
│   └── ng-era1-namespace.yaml       # Era-1 命名空間規範
├── era-2/                           # Era-2 規範 (NG300-599)
│   └── ng-era2-namespace.yaml       # Era-2 命名空間規範
├── era-3/                           # Era-3 規範 (NG600-899)
│   └── ng-era3-namespace.yaml       # Era-3 命名空間規範
├── cross-era/                       # 跨 Era 規範 (NG900-999)
│   ├── NG90101-cross-era-mapping.yaml
│   ├── era1-to-era2-mapping.yaml
│   ├── era2-to-era3-mapping.yaml
│   ├── ng-era1-era2-mapping.yaml    # Era-1↔Era-2 映射
│   ├── ng-era2-era3-mapping.yaml    # Era-2↔Era-3 映射
│   └── ng-era-comparison.md         # 跨 Era 比較文檔
├── analysis/                        # 分析報告
│   ├── ng-cross-era-matrix.json     # 跨 Era 映射矩陣
│   ├── actual-ng-validation-results.json
│   ├── evidence-chain-report.json
│   └── violation-catalog.json
├── reports/                         # 執行報告
│   ├── era2-completion-report.md
│   ├── era2-compliance-verification.md
│   ├── era2-deployment-report.md
│   ├── era2-execution-summary.md
│   ├── era2-upgrade-execution-summary.md
│   ├── era2-upgrade-pipeline-report.json
│   ├── era2-upgrade-pipeline-todo.md
│   └── governance-verification-beyond-era1.md
├── registry/                        # 註冊系統
│   ├── namespace-registry.py
│   └── namespaces.json
├── tools/                           # 工具
│   ├── ng-cli.py                    # NG 命令行工具
│   ├── ng-mapper.py                 # 命名空間映射器
│   ├── ng-transformer.py            # 命名空間轉換器
│   ├── ng-namespace-guard.py        # 命名空間守護
│   ├── ng-namespace-validator.py    # 命名空間驗證器
│   ├── ng-era-mapping-engine.py     # 跨 Era 映射引擎
│   └── fix-namespace-violations.sh  # 違規修復腳本
├── cicd/                            # CI/CD
│   └── ng-validation-workflow.yml   # GitHub Actions 工作流
├── monitoring/                      # 監控
│   └── ng-compliance-dashboard.html # 合規性儀表板
└── docs/                            # 文檔
    ├── NG-BATCH-1-IMPLEMENTATION-PLAN.md
    ├── NG-EXECUTION-ENGINES.md
    ├── LG-TO-NG-TRANSITION-PLAN.md
    ├── NG-Namespace-Governance-Whitepaper.md  # 白皮書
    └── ng-namespace-index.md        # 命名空間索引 (NG000-999)
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

- **NG-CHARTER.md** - 治理憲章和核心原則
- **docs/NG-BATCH-1-IMPLEMENTATION-PLAN.md** - 批次 1 實施計劃
- **docs/LG-TO-NG-TRANSITION-PLAN.md** - LG→NG 轉型計劃
- **docs/NG-Namespace-Governance-Whitepaper.md** - NG 命名空間治理白皮書
- **docs/ng-namespace-index.md** - 完整 NG000-999 命名空間索引
- **Core Specs** - 核心規範 YAML 文件（`core/` 目錄）
- **analysis/** - 分析報告和證據鏈
- **reports/** - 執行報告和升級摘要

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

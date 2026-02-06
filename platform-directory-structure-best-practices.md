# 平台級統一巨型目錄樹結構最佳實踐報告

## 執行摘要

本報告基於對大型儲存庫（多平台並行）架構的深入研究，提供了在每個專業平台及子平台目錄中實作統一巨型目錄樹結構的全面指南。通過分析 Monorepo 與 Polyrepo 策略、目錄組織模式、狀態管理和工具鏈整合，本報告為構建可擴展、可維護的平台級架構提供了可操作的建議。

## 1\. 架構策略選擇

### 1.1 Monorepo vs Polyrepo 決策框架

#### Monorepo 優勢

-   **簡化依賴管理**: 內部依賴更易於管理，跨組件變更可在單一提交/PR中協調
-   **代碼可發現性與重構**: 更易於查找代碼、理解關係並執行大規模重構
-   **統一工具/CI**: 可在所有基礎設施代碼中實施一致的 Linting、測試和部署流水線
-   **協作增強**: 鼓勵共享所有權和可見性，打破團隊壁壘

#### Monorepo 挑戰

-   **CI/CD 瓶頸**: 克隆大型倉庫並在許多組件上運行 plan/apply 可能變得非常緩慢
-   **工具需求**: 需要複雜工具用於選擇性構建/測試、智能緩存和稀疏檢出
-   **爆炸半徑**: 主分支上的破壞性變更可能影響更大範圍
-   **訪問控制**: 管理細粒度權限更具挑戰性
-   **衛生管理**: 需要嚴格的分支策略和勤奮的依賴管理

#### Polyrepo 優勢

-   **明確所有權**: 邊界明確，特定團隊擁有每個倉庫
-   **獨立流水線**: 每個倉庫可有自己的定制 CI/CD 流水線
-   **細粒度訪問控制**: 可輕鬆管理基於倉庫的權限
-   **團隊自治**: 團隊有更多自由選擇工具並獨立演進其基礎設施代碼

#### Polyrepo 挑戰

-   **複雜依賴管理**: 管理倉庫間的依賴關係具有挑戰性
-   **代碼重複風險**: 樣板代碼高度重複的風險
-   **可發現性問題**: 難以獲得整個基礎設施的全景視圖
-   **工具開銷**: 需要投資於跨倉庫工具
-   **不一致標準**: 跨不同倉庫和團隊標準可能分歧

### 1.2 推薦策略：混合模式

對於大型多平台並行架構，推薦採用混合模式：

-   **核心平台基礎設施**: 使用 Monorepo 確保一致性
-   **業務邊界**: 在業務單位之間使用 Polyrepo 提供自治權
-   **共享模塊**: 維護集中的共享模塊倉庫

## 2\. 目錄結構組織模式

### 2.1 核心原則

1.  **模組化**: 設計和使用專注的、可重用的模塊作為主要構建塊
2.  **狀態管理優先**: 謹慎處理狀態文件，按環境、區域和組件隔離狀態
3.  **配置而非代碼重複**: 通過輸入變量、.tfvars 文件處理變異
4.  **結構反映架構與團隊**: 以邏輯方式組織目錄
5.  **自動化**: 實施強大的 CI/CD 流水線
6.  **迭代與重構**: 定期審查和重構代碼庫
7.  **投資工具**: 利用工具能力
8.  **一致性**: 遵守一致的命名約定、格式標準

### 2.2 推薦的目錄結構

#### 模式一：按環境優先，然後按組件

```
platform-monorepo/
├── .github/
│   ├── workflows/           # CI/CD 工作流
│   │   ├── pr-validation.yml
│   │   ├── deploy-dev.yml
│   │   ├── deploy-staging.yml
│   │   └── deploy-prod.yml
│   └── CODEOWNERS           # 代碼所有權定義
├── docs/                    # 文檔
│   ├── architecture/
│   ├── runbooks/
│   └── onboarding/
├── scripts/                 # 輔助腳本
├── tools/                   # 開發工具配置
│   ├── terraform/
│   ├── kubernetes/
│   └── make/
├── modules/                 # 可重用共享模塊
│   ├── networking/          # 網絡模塊
│   │   ├── vpc/
│   │   ├── subnet/
│   │   └── security-groups/
│   ├── compute/             # 計算模塊
│   │   ├── ec2/
│   │   ├── lambda/
│   │   └── eks/
│   ├── storage/             # 存儲模塊
│   │   ├── s3/
│   │   ├── rds/
│   │   └── dynamodb/
│   ├── security/            # 安全模塊
│   │   ├── iam/
│   │   └── kms/
│   └── monitoring/          # 監控模塊
│       ├── cloudwatch/
│       └── prometheus/
├── platforms/               # 平台級別配置
│   ├── shared/              # 共享平台服務
│   │   ├── dev/
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   ├── outputs.tf
│   │   │   └── terraform.tfvars
│   │   ├── staging/
│   │   └── prod/
│   │   └── modules/
│   │       └── versions.tf
│   ├── data-platform/       # 數據平台
│   │   ├── dev/
│   │   ├── staging/
│   │   ├── prod/
│   │   └── components/
│   │       ├── data-lake/
│   │       ├── data-warehouse/
│   │       └── etl-pipelines/
│   ├── application-platform/ # 應用平台
│   │   ├── dev/
│   │   ├── staging/
│   │   ├── prod/
│   │   └── components/
│   │       ├── api-gateway/
│   │       ├── microservices/
│   │       └── frontend/
│   └── ml-platform/         # 機器學習平台
│       ├── dev/
│       ├── staging/
│       ├── prod/
│       └── components/
│           ├── model-training/
│           ├── model-serving/
│           └── feature-store/
├── infrastructure/          # 基礎設施代碼
│   ├── global/              # 全局資源
│   │   ├── main.tf
│   │   └── state/
│   ├── regions/             # 區域特定
│   │   ├── us-east-1/
│   │   │   ├── networking/
│   │   │   ├── security/
│   │   │   └── shared-services/
│   │   ├── eu-west-1/
│   │   └── ap-southeast-1/
│   └── environments/        # 環境特定
│       ├── dev/
│       ├── staging/
│       └── prod/
├── services/                # 微服務
│   ├── auth-service/
│   ├── user-service/
│   ├── order-service/
│   └── payment-service/
├── libraries/               # 共享庫
│   ├── utils/
│   ├── api-clients/
│   └── middleware/
├── config/                  # 配置文件
│   ├── terraform/
│   ├── kubernetes/
│   └── docker/
├── tests/                   # 測試
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── deployments/             # 部署清單
│   ├── helm/
│   ├── kustomize/
│   └── docker-compose/
└── makefile                 # 統一入口點
```

#### 模式二：按組件優先，然後按環境

```
platform-monorepo/
├── components/             # 按組件組織
│   ├── networking/         # 網絡組件
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── environments/
│   │       ├── dev.tfvars
│   │       ├── staging.tfvars
│   │       └── prod.tfvars
│   ├── database/           # 數據庫組件
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── application/        # 應用組件
│   └── monitoring/         # 監控組件
├── environments/           # 環境配置
│   ├── dev/
│   ├── staging/
│   └── prod/
└── modules/                # 共享模塊
```

### 2.3 標準文件佈局

每個模塊或組件應遵循標準文件結構：

```
module-name/
├── main.tf              # 主要資源定義
├── variables.tf         # 輸入變量定義
├── outputs.tf          # 輸出值聲明
├── versions.tf         # Terraform 和提供者版本
├── providers.tf        # 提供者配置
├── terraform.tfvars    # 環境特定變量（可選）
├── readme.md           # 模塊文檔
└── tests/              # 模塊測試
    └── test.go
```

## 3\. 狀態管理策略

### 3.1 狀態隔離原則

-   **按環境隔離**: dev、staging、prod 各自獨立狀態
-   **按區域隔離**: 每個地理區域獨立狀態
-   **按組件隔離**: 邏輯上獨立的基礎設施部分分離狀態

### 3.2 狀態文件管理

```hcl
# 示例：遠程後端配置
terraform {
  backend "s3" {
    bucket         = "my-company-terraform-state"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
```

### 3.3 狀態分割策略

**按環境分割**:

```
state/
├── dev/
├── staging/
└── prod/
```

**按區域分割**:

```
state/
├── us-east-1/
├── eu-west-1/
└── ap-southeast-1/
```

**按組件分割**:

```
state/
├── networking/
├── security/
├── database/
└── application/
```

### 3.4 依賴管理

使用 `terraform_remote_state` 數據源：

```hcl
data "terraform_remote_state" "network" {
  backend = "s3"
  config = {
    bucket = "my-terraform-state"
    key    = "prod/us-east-1/network/terraform.tfstate"
    region = "us-east-1"
  }
}

resource "aws_instance" "app" {
  subnet_id = data.terraform_remote_state.network.outputs.private_subnet_ids
}
```

## 4\. CI/CD 優化

### 4.1 增量構建

```yaml
# GitHub Actions 示例
name: Terraform Plan
on:
  pull_request:
    paths:
      - 'platforms/**'

jobs:
  plan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
      - name: Terraform Plan
        run: |
          # 使用依賴圖確定需要重建的項目
          terragrunt run-all plan
```

### 4.2 依賴圖驅動構建

```bash
# 使用依賴圖確定受影響的模塊
terraform graph | dot -Tpng > graph.png
```

### 4.3 並行化構建

```yaml
strategy:
  matrix:
    component:
      - networking
      - database
      - application
```

## 5\. 工具鏈整合

### 5.1 推薦工具

**Monorepo 管理工具**:

-   **Nx**: TypeScript/JavaScript 項目
-   **Lerna**: JavaScript 項目
-   **Turborepo**: 高性能構建
-   **Bazel**: Google 的構建系統，用於大型項目
-   **Pants**: 基於 Python 的 Monorepo

**Terraform 編排工具**:

-   **Terragrunt**: 薄封裝器，用於管理多個模塊和分割狀態

### 5.2 Terragrunt 配置示例

```hcl
# 根級別通用配置
# /live/terragrunt.hcl
remote_state {
  backend = "s3"
  config = {
    bucket = "my-company-tfstate"
    key    = "${path_relative_to_include()}/terraform.tfstate"
    region = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}

# 葉模塊配置
# /live/prod/app/terragrunt.hcl
include "root" {
  path = find_in_parent_folders()
}

dependency "vpc" {
  config_path = "../vpc"
}

terraform {
  source = "git::github.com/my-company/modules.git//app?ref=v1.0.0"
}

inputs = {
  vpc_id          = dependency.vpc.outputs.vpc_id
  private_subnets = dependency.vpc.outputs.private_subnet_ids
  instance_count  = 5
}
```

## 6\. 命名約定

### 6.1 資源命名

-   使用下劃線分隔單詞（例如：`google_compute_instance`, `web_server_firewall`）
-   資源名稱使用單數形式
-   如果模塊中的主要資源，考慮命名為 `main` 以簡化

### 6.2 變量命名

-   使用反映用途或目的的描述性名稱
-   包含數值單位（例如：`ram_size_gb`, `disk_size_gb`）
-   布爾標誌使用肯定名稱（例如：`enable_monitoring` 而不是 `disable_monitoring`）

### 6.3 輸出命名

-   根據提供的值描述性地命名輸出

### 6.4 文件命名

-   將相關資源邏輯地分組到命名文件中（例如：`network.tf`, `database.tf`）

## 7\. 訪問控制與所有權

### 7.1 CODEOWNERS 文件

```github
# 全局所有者
* @platform-team

# 平台特定
/platforms/shared/* @shared-platform-team
/platforms/data-platform/* @data-platform-team

# 組件特定
/infrastructure/global/* @infrastructure-team
/infrastructure/regions/us-east-1/* @us-east-1-team

# 緊急情況
PLATFORM-CRITICAL @platform-team @sre-team
```

### 7.2 基於目錄的權限

```yaml
# 示例：訪問控制配置
permissions:
  - path: /platforms/production/
    teams:
      - platform-ops
      - sre-team
    restrictions:
      - require_approval: 2
      - restrict_changes: true
```

## 8\. 環境與多區域管理

### 8.1 環境管理技術

**Terraform Workspaces**:

-   適用於結構相同或非常相似的環境
-   差異主要通過輸入變量處理

**目錄分隔**:

-   每個環境的根模塊配置使用單獨目錄
-   提供最大隔離
-   允許完全不同的後端配置

### 8.2 多區域策略

**提供者別名**:

```hcl
provider "aws" {
  region = "us-east-1"
}

provider "aws" {
  alias  = "eu-west-1"
  region = "eu-west-1"
}
```

**區域差異結構化**:

-   通過輸入變量傳遞區域特定參數
-   基於區域變量使用條件邏輯
-   考慮為顯著區域差異創建單獨的區域特定模塊

### 8.3 全局和複製服務

-   全局服務（如 AWS IAM、Route 53）需要特殊處理
-   考慮在專用的 "global" 配置中管理

## 9\. 擴展策略

### 9.1 演變階段

**初創階段**:

-   單一 Monorepo
-   最小模組化
-   環境文件夾或工作空間用於基本分隔

**成長階段**:

-   大型單一狀態文件成為瓶頸
-   投資創建文檔齊全、可重用的內部模塊庫
-   積極按邏輯組件和環境/區域分割單調狀態文件
-   實施自動化測試和 Linting

**企業階段**:

-   多團隊貢獻 IaC
-   需要明確的所有權邊界、強大模組化
-   需要內部 Terraform/OpenTofu 模塊註冊表
-   需要專用平台/基礎設施團隊提供共享模塊和工具
-   Terragrunt 或自定義編排工具

### 9.2 性能優化

**分割狀態文件**:

-   減少 plan/apply 範圍
-   降低爆炸半徑

**條件刷新**:

-   在 CI/CD 流水線中使用 `terraform plan -refresh=false`

**優化複雜邏輯**:

-   簡化 for\_each 循環、locals 涉及的複雜邏輯

## 10\. 測量成功

### 10.1 DORA 指標

**部署頻率 (DF)**:

-   成功部署到生產環境的基礎設施變更頻率

**變更前置時間 (LTTC)**:

-   從提交 IaC 變更到成功部署的時間

**變更失敗率 (CFR)**:

-   導致需要恢復的基礎設施部署百分比

**平均恢復時間 (MTTR)**:

-   部署導致的失敗後恢復服務所需的時間

### 10.2 其他指標

-   **Plan/Apply 時間趨勢**: 監控執行時間
-   **上線難度**: 新團隊成員理解結構並進行安全變更的速度
-   **環境一致性/漂移**: 測量實際基礎設施狀態與代碼定義狀態的偏差頻率
-   **代碼審查速度**: PR 審查和合併的效率

## 11\. 實施檢查清單

### 11.1 結構設計

-   [ ]  選擇適當的倉庫策略（Monorepo、Polyrepo 或混合）
-   [ ]  定義清晰的目錄結構
-   [ ]  建立標準文件佈局
-   [ ]  實施一致的命名約定

### 11.2 狀態管理

-   [ ]  配置遠程後端
-   [ ]  實施狀態鎖定
-   [ ]  按環境、區域和組件分割狀態
-   [ ]  啟用狀態文件版本控制

### 11.3 CI/CD

-   [ ]  實施增量構建
-   [ ]  配置依賴圖驅動構建
-   [ ]  並行化構建
-   [ ]  實施自動化測試和驗證

### 11.4 訪問控制

-   [ ]  配置 CODEOWNERS
-   [ ]  實施基於目錄的權限
-   [ ]  配置審批工作流

### 11.5 工具鏈

-   [ ]  選擇適當的 Monorepo 管理工具
-   [ ]  配置 Terraform 編排工具（如需要）
-   [ ]  集成 CI/CD 平台
-   [ ]  配置監控和日誌記錄

### 11.6 文檔

-   [ ]  創建架構文檔
-   [ ]  編寫模塊 README
-   [ ]  創建操作手冊
-   [ ]  建立上線指南

## 12\. 結論

實施平台級統一巨型目錄樹結構需要系統性的方法和持續的改進。通過遵循以下核心原則，組織可以構建可擴展、可維護的平台級架構：

1.  **擁抱模組化**: 設計和使用專注的、可重用的模塊
2.  **優先考慮狀態管理**: 謹慎處理狀態文件並按環境、區域和組件隔離
3.  **配置而非代碼重複**: 通過輸入變量和配置文件處理變異
4.  **結構反映架構與團隊**: 以邏輯方式組織目錄以反映架構
5.  **自動化**: 實施強大的 CI/CD 流水線
6.  **迭代與重構**: 定期審查和改進結構
7.  **投資工具**: 利用工具能力管理複雜性
8.  **一致性**: 遵守一致的命名約定、格式標準

通過採用這些最佳實踐，組織可以從臨時基礎設施腳本轉向構建強大、可擴展和可維護的基礎設施即代碼系統，無論選擇何種特定工具或模式。

## 參考文獻

1.  Radiansys. "Mono Repos: Structure, Benefits & Best Practices"
2.  Scalr. "The Platform Engineer's Guide to Structuring Terraform and OpenTofu"
3.  Google Cloud. "Best practices for general style and structure"
4.  HashiCorp. "Terraform Modules Guide: Best Practices & Examples"
5.  Buildkite. "Monorepo vs Polyrepo: How to Choose Between Them"
6.  Spacelift. "Terraform Architecture Overview"
7.  DORA Metrics. "DevOps Research and Assessment"

* * *

_報告生成日期: 2025年_ _適用於: 大型多平台並行架構_
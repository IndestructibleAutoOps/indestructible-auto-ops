<!-- @GL-governed -->
<!-- @GL-layer: GL90-99 -->
<!-- @GL-semantic: governed-documentation -->
<!-- @GL-audit-trail: engine/governance/GL_SEMANTIC_ANCHOR.json -->

# GL Unified Charter Activated
# 可插拔 CI/CD 架構指南

## 概述

本架構設計為完全可插拔（pluggable）的 CI/CD 系統，允許客戶根據自身需求和可用資源靈活配置。即使沒有外部服務（如 AWS、Docker、Slack 等），核心 CI/CD 功能仍然可以正常運作。

## 核心設計原則

### 1. **零依賴默認配置**
- 所有核心功能（lint、test、build）無需任何外部服務
- 默認使用本地部署
- 無需配置任何 secrets 即可使用

### 2. **可選組件按需啟用**
- 每個功能模組都可以獨立啟用/禁用
- 未啟用的模組不會影響其他功能
- 配置失敗時自動降級到本地部署

### 3. **智能降級機制**
- 檢測到缺失的配置時自動降級
- 提供清晰的警告信息
- 確保核心流程不受影響

### 4. **模組化架構**
- 每個功能都是獨立的模組
- 模組之間通過標準接口通信
- 易於擴展和自定義

## 架構圖

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Actions                           │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Configuration Layer (config.yml)             │  │
│  │  - Feature Flags                                      │  │
│  │  - Deployment Targets                                 │  │
│  │  - Integration Settings                               │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Orchestration Layer (combined-ci.yml)         │  │
│  │  - Parse Configuration                               │  │
│  │  - Route to Modules                                   │  │
│  │  - Handle Failures                                    │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            Pluggable Modules                          │  │
│  │                                                       │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────┐    │  │
│  │  │ Lint Module  │  │ Test Module  │  │ Build    │    │  │
│  │  │ (Always ON)  │  │ (Always ON)  │  │ Module   │    │  │
│  │  └──────────────┘  └──────────────┘  └──────────┘    │  │
│  │                                                       │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────┐    │  │
│  │  │ Security     │  │ Deploy       │  │ Notify   │    │  │
│  │  │ (Optional)   │  │ (Optional)   │  │ (Optional)│   │  │
│  │  └──────────────┘  └──────────────┘  └──────────┘    │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Deployment Targets (Auto-selected)            │  │
│  │                                                       │  │
│  │  1. Local (Default - No deps)          ✓              │  │
│  │  2. SSH (Requires SSH keys)          ○              │  │
│  │  3. Docker (Requires registry)        ○              │  │
│  │  4. Kubernetes (Requires K8s config)  ○              │  │
│  │  5. AWS ECS (Requires AWS creds)      ○              │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 配置文件說明

### config.yml - 主配置文件

```yaml
# 功能開關 - 控制各個模組的啟用狀態
core:
  linting: true           # 核心功能，建議始終啟用
  testing: true           # 核心功能，建議始終啟用
  building: true          # 核心功能，建議始終啟用

# 可選功能 - 根據需求配置
optional:
  security:
    enabled: true         # 安全掃描
    sast_scan: true       # 靜態代碼分析（無需配置）
    dependency_scan: true # 依賴掃描（無需配置）
    container_scan: false # 容器掃描（需要 Docker）
    codeql_analysis: true # CodeQL 分析（無需配置）
    secret_scan: true     # 密鑰掃描（無需配置）
  
  deployment:
    enabled: true
    staging: true
    production: true
    blue_green: true      # 藍綠部署（需要雙台服務器）
  
  integrations:
    # 云服務提供商
    aws: false            # AWS（需要 AWS 憑證）
    gcp: false            # GCP（需要 GCP 憑證）
    azure: false          # Azure（需要 Azure 憑證）
    
    # 容器註冊表
    docker_registry: false # Docker（需要註冊表憑證）
    
    # 安全工具
    snyk: false          # Snyk（需要 Snyk token）
    trivy: true          # Trivy（內建，無需配置）
    
    # 通知渠道
    slack: false         # Slack（需要 webhook）
    email: false         # 郵件（需要 SMTP 配置）
    discord: false       # Discord（需要 webhook）
    
    # 監控工具
    datadog: false       # Datadog（需要 API key）
    prometheus: false    # Prometheus（需要 endpoint）
    sentry: false        # Sentry（需要 DSN）

# 部署目標配置
deployment_targets:
  local:
    enabled: true        # 本地部署（默認）
    description: "部署到本地文件系統"
  
  self_hosted:
    enabled: false       # SSH 部署（可選）
    description: "通過 SSH 部署到自託管服務器"
    requires: [SSH_PRIVATE_KEY, SERVER_HOST, SERVER_USER]
  
  docker:
    enabled: false       # Docker 部署（可選）
    description: "部署為 Docker 容器"
    requires: [DOCKER_REGISTRY, DOCKER_USERNAME, DOCKER_PASSWORD]
```

## 模組說明

### 1. Lint Module (lint-module.yml)

**狀態：始終啟用（核心功能）**

**功能：**
- ESLint（JavaScript/TypeScript）
- Pylint（Python）
- Markdown lint
- JSON/YAML lint

**依賴：** 無

**無配置情況：**
- 自動檢測配置文件
- 未找到配置時跳過相應檢查
- 不會導致流程失敗

### 2. Test Module (test-module.yml)

**狀態：始終啟用（核心功能）**

**功能：**
- 單元測試
- 集成測試
- 端到端測試
- 覆蓋率報告

**依賴：** 無

**無配置情況：**
- 自動檢測測試框架
- 未找到測試時跳過
- 可配置覆蓋率閾值

### 3. Build Module (build-module.yml)

**狀態：始終啟用（核心功能）**

**功能：**
- 應用構建
- 構建信息生成
- Docker 構建（可選）

**依賴：** 無

**無配置情況：**
- 自動檢測構建配置
- 未找到配置時創建佔位構建
- 生成構建信息文件

### 4. Security Module (security-module.yml)

**狀態：可選（默認啟用）**

**功能：**
- SAST 掃描
- 依賴掃描
- 容器掃描（需要 Docker）
- CodeQL 分析
- 密鑰掃描

**依賴：**
- SAST、依賴掃描、CodeQL、密鑰掃描：無需配置
- 容器掃描：需要 Docker
- Snyk：需要 Snyk token（可選）

**無配置情況：**
- 無需配置的掃描正常運行
- 需要配置的掃描自動跳過
- 生成完整的安全報告

### 5. Deploy Module (deploy-module.yml)

**狀態：可選（默認啟用）**

**功能：**
- 本地部署（默認）
- SSH 部署
- Docker 部署
- Kubernetes 部署
- AWS ECS 部署

**依賴：**
- 本地部署：無需配置
- SSH 部署：SSH_PRIVATE_KEY, SERVER_HOST, SERVER_USER
- Docker 部署：DOCKER_REGISTRY, DOCKER_USERNAME, DOCKER_PASSWORD
- Kubernetes 部署：KUBE_CONFIG, KUBE_NAMESPACE
- AWS ECS 部署：AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION

**智能降級：**
```yaml
# 檢測配置缺失時自動降級到本地部署
if [ -z "${{ secrets.SSH_PRIVATE_KEY }}" ]; then
  echo "⚠️  SSH 部署需要憑證"
  echo "⚠️  降級到本地部署..."
  deployment_target=local
fi
```

### 6. Notification Module (notification-module.yml)

**狀態：可選（默認禁用）**

**功能：**
- Slack 通知
- 郵件通知
- Discord 通知
- 控制台輸出（始終啟用）

**依賴：**
- 控制台輸出：無需配置
- Slack：SLACK_WEBHOOK
- 郵件：SMTP_SERVER, SMTP_USERNAME, SMTP_PASSWORD, EMAIL_TO
- Discord：DISCORD_WEBHOOK

**無配置情況：**
- 始終輸出到控制台
- 未配置的通知渠道自動跳過

## 使用場景

### 場景 1：最小化配置（無任何外部服務）

**配置：**
```yaml
# config.yml
core:
  linting: true
  testing: true
  building: true

optional:
  security:
    enabled: true
    sast_scan: true
    dependency_scan: true
    container_scan: false
    codeql_analysis: true
    secret_scan: true
  
  deployment:
    enabled: true
    staging: true
    production: true
    blue_green: false    # 禁用藍綠部署
```

**運行結果：**
- ✓ 代碼檢查
- ✓ 運行測試
- ✓ 構建應用
- ✓ 安全掃描（無需配置的）
- ✓ 部署到本地（模擬部署）
- ✓ 生成部署記錄

### 場景 2：自託管服務器部署

**配置：**
```yaml
# config.yml
deployment_targets:
  self_hosted:
    enabled: true
    type: "ssh"
    description: "通過 SSH 部署到自託管服務器"

# GitHub Secrets
SSH_PRIVATE_KEY: <your-private-key>
SERVER_HOST: your-server.com
SERVER_USER: deploy
DEPLOY_PATH: /var/www/app
```

**運行結果：**
- ✓ 所有核心功能
- ✓ 通過 SSH 部署到自託管服務器
- ✓ 健康檢查
- ✓ 部署記錄

### 場景 3：Docker + Kubernetes 部署

**配置：**
```yaml
# config.yml
deployment_targets:
  docker:
    enabled: true
    type: "docker"
  
  kubernetes:
    enabled: true
    type: "kubernetes"

# GitHub Secrets
DOCKER_REGISTRY: registry.example.com
DOCKER_USERNAME: your-username
DOCKER_PASSWORD: your-password
KUBE_CONFIG: <base64-encoded-kubeconfig>
KUBE_NAMESPACE: production
```

**運行結果：**
- ✓ 構建 Docker 鏡像
- ✓ 推送到註冊表
- ✓ 部署到 Kubernetes 集群
- ✓ 滾動更新

### 場景 4：完整功能啟用

**配置：**
```yaml
# config.yml
core:
  linting: true
  testing: true
  building: true

optional:
  security:
    enabled: true
    sast_scan: true
    dependency_scan: true
    container_scan: true    # 啟用容器掃描
    codeql_analysis: true
    secret_scan: true
    snyk_enabled: true     # 啟用 Snyk
  
  deployment:
    enabled: true
    staging: true
    production: true
    blue_green: true
  
  integrations:
    aws: true
    docker_registry: true
    snyk: true
    slack: true
    datadog: true

# GitHub Secrets
AWS_ACCESS_KEY_ID: <key>
AWS_SECRET_ACCESS_KEY: <secret>
AWS_REGION: us-east-1
SNYK_TOKEN: <token>
SLACK_WEBHOOK: <webhook-url>
DATADOG_API_KEY: <api-key>
```

**運行結果：**
- ✓ 所有核心功能
- ✓ 完整安全掃描
- ✓ Docker 容器掃描
- ✓ Snyk 依賴掃描
- ✓ AWS 雲服務部署
- ✓ 藍綠部署
- ✓ Slack 通知
- ✓ Datadog 監控

## 配置步驟

### 步驟 1：基礎設置（無需任何配置）

```bash
# 克隆倉庫
git clone [EXTERNAL_URL_REMOVED]
cd machine-native-ops

# 查看配置文件
cat .github/workflows/config.yml

# 推送到 GitHub
git add .
git commit -m "Add pluggable CI/CD architecture"
git push origin main
```

**結果：** CI/CD 流程自動運行，所有核心功能正常工作。

### 步驟 2：啟用可選功能（按需配置）

#### 啟用 SSH 部署：

```bash
# 在 GitHub 設置中添加 Secrets
Settings → Secrets and variables → Actions → New repository secret

# 添加以下 secrets：
- SSH_PRIVATE_KEY
- SERVER_HOST
- SERVER_USER
- DEPLOY_PATH
```

#### 啟用 Docker 部署：

```bash
# 添加 secrets：
- DOCKER_REGISTRY
- DOCKER_USERNAME
- DOCKER_PASSWORD
```

#### 啟用通知：

```bash
# 添加 secrets：
- SLACK_WEBHOOK
```

### 步驟 3：自定義配置

編輯 `.github/workflows/config.yml`：

```yaml
# 禁用不需要的功能
optional:
  security:
    container_scan: false    # 禁用容器掃描
    snyk_enabled: false     # 禁用 Snyk
  
  integrations:
    aws: false              # 禁用 AWS
  
  deployment:
    blue_green: false       # 禁用藍綠部署
```

## 故障排除

### 問題 1：部署失敗

**原因：** 配置缺失或目標不可用

**解決方案：**
```bash
# 檢查工作流日誌
gh run view --log

# 查看降級警告
# 會看到類似 "⚠️  SSH deployment requires credentials"
# 自動降級到本地部署
```

### 問題 2：安全掃描失敗

**原因：** 容器掃描需要 Docker

**解決方案：**
```yaml
# 禁用容器掃描
optional:
  security:
    container_scan: false
```

### 問題 3：通知未發送

**原因：** 未配置通知渠道

**解決方案：**
```yaml
# 檢查控制台輸出（始終可用）
# 或配置通知渠道
optional:
  integrations:
    slack: true
```

## 最佳實踐

### 1. 漸進式啟用

```yaml
# 階段 1：核心功能（無需配置）
core:
  linting: true
  testing: true
  building: true

# 階段 2：安全掃描（部分配置）
optional:
  security:
    enabled: true
    sast_scan: true
    dependency_scan: true

# 階段 3：部署（選擇目標）
deployment_targets:
  local:
    enabled: true

# 階段 4：集成（按需添加）
integrations:
  slack: true
```

### 2. 環境隔離

```yaml
environments:
  staging:
    enabled: true
    deployment_target: local
  
  production:
    enabled: true
    deployment_target: ssh  # 生產環境使用 SSH
    blue_green: true
```

### 3. 備份方案

```yaml
# 始終保留本地部署作為備份
deployment_targets:
  local:
    enabled: true
    always_available: true
```

## 總結

這個可插拔架構的關鍵優勢：

1. **零依賴起步** - 無需任何配置即可使用核心功能
2. **按需擴展** - 根據需求逐步啟用功能
3. **智能降級** - 配置缺失時自動降級，不影響核心流程
4. **模組化設計** - 每個功能獨立，易於維護
5. **清晰文檔** - 每個模組的依賴和配置都清楚標註

客戶可以從最小化配置開始，根實際需求逐步添加更多功能，而不需要一次性配置所有東西。
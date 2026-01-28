# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: documentation
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
# GL Unified Charter Activated
# 快速開始指南 - 可插拔 CI/CD 架構

## 🚀 5 分鐘快速開始

### 方式 1：零配置開始（推薦給新用戶）

無需任何配置，即可使用核心 CI/CD 功能！

```bash
# 1. 克隆倉庫
git clone https://github.com/MachineNativeOps/machine-native-ops.git
cd machine-native-ops

# 2. 查看默認配置
cat .github/workflows/config.yml

# 3. 推送到 GitHub
git add .
git commit -m "Setup CI/CD pipeline"
git push origin main
```

**✅ 完成！** CI/CD 流程將自動運行：
- ✓ 代碼檢查
- ✓ 運行測試
- ✓ 構建應用
- ✓ 安全掃描
- ✓ 本地部署（模擬）

---

## 📋 配置選項列表

### 可選配置（按需添加）

#### 🔐 部署相關

| 配置項 | 用途 | 必需的 Secrets |
|--------|------|----------------|
| SSH 部署 | 部署到自託管服務器 | `SSH_PRIVATE_KEY`, `SERVER_HOST`, `SERVER_USER` |
| Docker 部署 | 部署 Docker 容器 | `DOCKER_REGISTRY`, `DOCKER_USERNAME`, `DOCKER_PASSWORD` |
| Kubernetes 部署 | 部署到 K8s 集群 | `KUBE_CONFIG`, `KUBE_NAMESPACE` |
| AWS ECS 部署 | 部署到 AWS ECS | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION` |

#### 🔒 安全相關

| 配置項 | 用途 | 必需的 Secrets |
|--------|------|----------------|
| Snyk 掃描 | 依賴漏洞掃描 | `SNYK_TOKEN` |

#### 📢 通知相關

| 配置項 | 用途 | 必需的 Secrets |
|--------|------|----------------|
| Slack 通知 | 發送 Slack 消息 | `SLACK_WEBHOOK` |
| 郵件通知 | 發送郵件 | `SMTP_SERVER`, `SMTP_USERNAME`, `SMTP_PASSWORD`, `EMAIL_TO` |
| Discord 通知 | 發送 Discord 消息 | `DISCORD_WEBHOOK` |

#### 📊 監控相關

| 配置項 | 用途 | 必需的 Secrets |
|--------|------|----------------|
| Datadog 監控 | Datadog 集成 | `DATADOG_API_KEY` |
| Prometheus 監控 | Prometheus 集成 | `PROMETHEUS_ENDPOINT` |
| Sentry 錯誤追蹤 | Sentry 集成 | `SENTRY_DSN` |

---

## 🎯 常見使用場景

### 場景 1：個人項目（無需配置）

**適合：** 個人開發、小型項目

```yaml
# .github/workflows/config.yml
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
    blue_green: false
```

**結果：** 自動化的 CI/CD，無需任何外部服務。

---

### 場景 2：自託管服務器

**適合：** 有自己的服務器

**步驟 1：** 添加 GitHub Secrets

```bash
Settings → Secrets and variables → Actions
```

添加以下 Secrets：
- `SSH_PRIVATE_KEY` - 你的 SSH 私鑰
- `SERVER_HOST` - 服務器地址（如：example.com）
- `SERVER_USER` - SSH 用戶名（如：deploy）
- `DEPLOY_PATH` - 部署路徑（如：/var/www/app）
- `SERVER_URL` - 服務器 URL（如：https://example.com）
- `HEALTH_URL` - 健康檢查 URL（如：https://example.com/health）

**步驟 2：** 更新配置

```yaml
# .github/workflows/config.yml
deployment_targets:
  self_hosted:
    enabled: true
    type: "ssh"
    description: "通過 SSH 部署到自託管服務器"
```

**步驟 3：** 修改 combined-ci.yml 中的部署目標

```yaml
# .github/workflows/combined-ci.yml
deploy-staging:
  with:
    deployment_target: ssh  # 改為 ssh

deploy-production:
  with:
    deployment_target: ssh  # 改為 ssh
```

**結果：** 自動部署到你的服務器。

---

### 場景 3：Docker 部署

**適合：** 使用 Docker 的項目

**步驟 1：** 添加 GitHub Secrets

- `DOCKER_REGISTRY` - Docker 註冊表（如：registry.example.com）
- `DOCKER_USERNAME` - 用戶名
- `DOCKER_PASSWORD` - 密碼

**步驟 2：** 更新配置

```yaml
# .github/workflows/config.yml
deployment_targets:
  docker:
    enabled: true
    type: "docker"
```

**步驟 3：** 修改 combined-ci.yml

```yaml
build:
  with:
    docker_build: true  # 啟用 Docker 構建

deploy-staging:
  with:
    deployment_target: docker
```

**結果：** 自動構建並推送 Docker 鏡像。

---

### 場景 4：完整功能啟用

**適合：** 企業級項目，需要完整功能

**步驟 1：** 配置所有需要的 Secrets

參考上表的配置選項，添加所有需要的 Secrets。

**步驟 2：** 更新 config.yml

```yaml
# .github/workflows/config.yml
core:
  linting: true
  testing: true
  building: true

optional:
  security:
    enabled: true
    sast_scan: true
    dependency_scan: true
    container_scan: true
    codeql_analysis: true
    secret_scan: true
    snyk_enabled: true
  
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

deployment_targets:
  self_hosted:
    enabled: true
    type: "ssh"
```

**步驟 3：** 修改 combined-ci.yml

```yaml
build:
  with:
    docker_build: true

security:
  with:
    container_scan: true
    snyk_enabled: true

deploy-staging:
  with:
    deployment_target: ssh

deploy-production:
  with:
    deployment_target: ssh
    blue_green: true

notify-ci:
  with:
    enabled: true
    slack_enabled: true

notify-deployment:
  with:
    enabled: true
    slack_enabled: true
```

**結果：** 完整的企業級 CI/CD 流程。

---

## 🔧 故障排除

### 問題：部署失敗，顯示 "⚠️  SSH deployment requires credentials"

**原因：** 未配置 SSH 相關的 Secrets

**解決方案：**
1. 添加所需的 Secrets（見場景 2）
2. 或者保持 `deployment_target: local` 使用本地部署

---

### 問題：容器掃描失敗

**原因：** 未啟用 Docker 構建或沒有 Dockerfile

**解決方案：**
```yaml
# 禁用容器掃描
optional:
  security:
    container_scan: false
```

---

### 問題：通知未發送

**原因：** 未配置通知渠道的 Secrets

**解決方案：**
1. 檢查控制台輸出（始終可用）
2. 添加對應的 Secrets（見配置選項表）

---

## 📝 配置檢查清單

### 第一次使用

- [ ] 克隆倉庫
- [ ] 查看 config.yml
- [ ] 推送到 GitHub
- [ ] 檢查 CI/CD 流程是否運行

### 啟用 SSH 部署

- [ ] 添加 SSH_PRIVATE_KEY
- [ ] 添加 SERVER_HOST
- [ ] 添加 SERVER_USER
- [ ] 添加 DEPLOY_PATH
- [ ] 更新 config.yml
- [ ] 修改 deployment_target

### 啟用 Docker 部署

- [ ] 添加 DOCKER_REGISTRY
- [ ] 添加 DOCKER_USERNAME
- [ ] 添加 DOCKER_PASSWORD
- [ ] 更新 config.yml
- [ ] 啟用 docker_build
- [ ] 修改 deployment_target

### 啟用通知

- [ ] 添加 SLACK_WEBHOOK
- [ ] 啟用 notification module

### 啟用完整功能

- [ ] 配置所有需要的 Secrets
- [ ] 更新所有配置文件
- [ ] 測試所有功能

---

## 🆚 與傳統 CI/CD 的對比

| 特性 | 傳統 CI/CD | 可插拔 CI/CD |
|------|-----------|-------------|
| 初始配置 | 需要配置所有東西 | 零配置即可開始 |
| 靈活性 | 固定配置 | 按需啟用功能 |
| 部署方式 | 單一方式 | 多種方式可選 |
| 失敗處理 | 流程失敗 | 自動降級 |
| 學習曲線 | 陡峭 | 平緩 |
| 適合場景 | 企業級 | 所有場景 |

---

## 💡 提示

1. **從簡單開始** - 先使用默認配置，熟悉後再逐步添加功能
2. **逐步啟用** - 不要一次性配置所有功能
3. **查看日誌** - 所有配置缺失都會有清晰的警告
4. **保持靈活** - 可以隨時禁用不需要的功能
5. **備份配置** - 保存好你的 config.yml

---

## 📞 獲取幫助

如果遇到問題：

1. 查看 `docs/PLUGGABLE-ARCHITECTURE.md` 了解詳細架構
2. 查看 GitHub Actions 日誌
3. 檢查 config.yml 配置
4. 查看工作流輸出中的警告信息

---

## 🎉 開始使用

現在就開始使用可插拔 CI/CD 架構吧！

```bash
git clone https://github.com/MachineNativeOps/machine-native-ops.git
cd machine-native-ops
git push origin main
```

✨ 無需任何配置，CI/CD 自動運行！
# MachineNativeOps Official Actions Library

本目錄包含 MachineNativeOps 官方自建的 GitHub Actions 元件，完全替代第三方依賴，實現 CI/CD 流程的完全自主可控。

## 📦 可用 Actions 清單

### 核心 Actions

| Action | 替代 | 描述 |
|--------|------|------|
| `mn-checkout` | `actions/checkout@v4` | Git 倉庫檢出 |
| `mn-upload-artifact` | `actions/upload-artifact@v4` | 上傳構建產物 |
| `mn-download-artifact` | `actions/download-artifact@v4` | 下載構建產物 |
| `mn-setup-python` | `actions/setup-python@v5` | Python 環境設置 |
| `mn-setup-node` | `actions/setup-node@v4` | Node.js 環境設置 |
| `mn-github-script` | `actions/github-script@v7` | GitHub API 腳本執行 |
| `mn-cache` | `actions/cache@v4` | 依賴緩存 |

### 安全掃描 Actions

| Action | 替代 | 描述 |
|--------|------|------|
| `mn-codeql` | `github/codeql-action/*@v3` | CodeQL 安全分析 |
| `mn-trivy-scan` | `aquasecurity/trivy-action@master` | Trivy 漏洞掃描 |
| `mn-secret-scan` | `trufflesecurity/trufflehog@main`, `gitleaks/gitleaks-action@v2` | 密鑰洩漏檢測 |

### Docker/容器 Actions

| Action | 替代 | 描述 |
|--------|------|------|
| `mn-docker-build` | `docker/build-push-action@v5`, `docker/setup-buildx-action@v3`, `docker/metadata-action@v5` | Docker 構建推送 |

### 通知/報告 Actions

| Action | 替代 | 描述 |
|--------|------|------|
| `mn-slack-notify` | `8398a7/action-slack@v3` | Slack 通知 |

### PR/Issue 管理 Actions

| Action | 替代 | 描述 |
|--------|------|------|
| `mn-create-pr` | `peter-evans/create-pull-request@v6` | 創建/更新 PR |

### 工具類 Actions

| Action | 替代 | 描述 |
|--------|------|------|
| `mn-setup-opa` | `open-policy-agent/setup-opa@v2` | OPA 策略引擎設置 |
| `mn-super-linter` | `super-linter/super-linter/slim@v7` | 多語言代碼檢查 |

## 🚀 使用方式

### 基本用法

> **Bootstrap 注意事項**
> GitHub Actions 必須先使用 `actions/checkout@v4` 取得倉庫內容後，才能引用本地的 MN Actions。
> 這是 GitHub Actions 的限制，請在每個 job 的第一個 checkout 步驟使用官方 action，後續即可改用 MN Actions。

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      # 使用自建 checkout
      - uses: ./.github/actions/mn-checkout
        with:
          fetch-depth: 0
      
      # 使用自建 Node.js 設置
      - uses: ./.github/actions/mn-setup-node
        with:
          node-version: '20'
          cache: 'npm'
      
      # 使用自建 artifact 上傳
      - uses: ./.github/actions/mn-upload-artifact
        with:
          name: build-output
          path: dist/
```

### 安全掃描

```yaml
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: ./.github/actions/mn-checkout
      
      # CodeQL 分析
      - uses: ./.github/actions/mn-codeql
        with:
          mode: full
          languages: javascript,python
          upload-sarif: true
      
      # Trivy 漏洞掃描
      - uses: ./.github/actions/mn-trivy-scan
        with:
          scan-type: fs
          severity: HIGH,CRITICAL
          upload-sarif: true
      
      # 密鑰掃描
      - uses: ./.github/actions/mn-secret-scan
        with:
          fail-on-secrets: true
```

### Docker 構建

```yaml
jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - uses: ./.github/actions/mn-checkout
      
      - uses: ./.github/actions/mn-docker-build
        with:
          context: .
          push: true
          auto-tag: true
          image-name: ghcr.io/${{ github.repository }}
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
```

### 自動化 PR

```yaml
jobs:
  auto-pr:
    runs-on: ubuntu-latest
    steps:
      - uses: ./.github/actions/mn-checkout
      
      - name: Make changes
        run: |
          echo "Updated at $(date)" >> CHANGELOG.md
      
      - uses: ./.github/actions/mn-create-pr
        with:
          branch: auto-update
          title: 'chore: automated update'
          body: 'This PR was created automatically'
          labels: automated,maintenance
```

## 🔧 遷移指南

### 從第三方 Actions 遷移

1. **替換 uses 路徑**
   ```yaml
   # 之前
   - uses: actions/checkout@v4
   
   # 之後
   - uses: ./.github/actions/mn-checkout
   ```

2. **參數兼容性**
   - 大多數參數與原始 Actions 保持兼容
   - 查看各 Action 的 `action.yml` 了解完整參數列表

3. **批量替換**
   - 使用 `scripts/migrate-actions.sh` 腳本自動替換

### 自動遷移腳本

```bash
# 運行遷移腳本
./scripts/migrate-actions.sh

# 預覽變更（不實際修改）
./scripts/migrate-actions.sh --dry-run

# 只遷移特定 workflow
./scripts/migrate-actions.sh --file .github/workflows/ci.yml
```

## 📋 功能對照表

### mn-checkout vs actions/checkout

| 功能 | mn-checkout | actions/checkout |
|------|-------------|------------------|
| 基本檢出 | ✅ | ✅ |
| 淺克隆 | ✅ | ✅ |
| SSH 認證 | ✅ | ✅ |
| Token 認證 | ✅ | ✅ |
| 子模組 | ✅ | ✅ |
| LFS | ✅ | ✅ |
| 稀疏檢出 | ✅ | ✅ |

### mn-codeql vs github/codeql-action

| 功能 | mn-codeql | github/codeql-action |
|------|-----------|---------------------|
| 初始化 | ✅ | ✅ |
| 自動構建 | ✅ | ✅ |
| 分析 | ✅ | ✅ |
| SARIF 上傳 | ✅ | ✅ |
| 多語言 | ✅ | ✅ |
| 自定義查詢 | ✅ | ✅ |

## 🛡️ 安全優勢

1. **完全自主可控** - 無需依賴第三方維護者
2. **代碼透明** - 所有邏輯可審計
3. **版本穩定** - 不受上游破壞性變更影響
4. **合規性** - 滿足企業安全策略要求
5. **離線可用** - 無需外部網絡依賴

## 📝 開發指南

### 創建新 Action

1. 在 `.github/actions/` 下創建新目錄
2. 創建 `action.yml` 定義 Action
3. 使用 Composite Action 模式
4. 添加完整的輸入/輸出定義
5. 更新本 README

### Action 命名規範

- 前綴: `mn-` (MachineNativeOps)
- 使用小寫和連字符
- 名稱應反映功能

### 測試 Action

```yaml
# .github/workflows/test-actions.yml
name: Test Custom Actions
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: ./.github/actions/mn-checkout
      - name: Verify checkout
        run: ls -la
```

## 📄 授權

本 Actions 庫為 MachineNativeOps 專案的一部分，遵循專案授權條款。

## 🤝 貢獻

歡迎提交 Issue 和 PR 來改進這些 Actions。

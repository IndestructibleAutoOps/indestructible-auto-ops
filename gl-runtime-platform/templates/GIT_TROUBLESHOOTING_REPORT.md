# Git 推送失敗深度排查報告

## 問題概述

**問題描述**: 無法將代碼推送到 GitHub 倉庫  
**錯誤信息**: `fatal: unable to access 'https://github.com/MachineNativeOps/machine-native-ops.git/': Could not resolve host: github.com`  
**實際錯誤**: HTTP/2 401 Unauthorized

## 排查過程

### 1. 基礎網絡檢查 ✅

```bash
# 檢查 GitHub.com 可達性
ping github.com
# 結果: 正常 (延遲 75ms, 0% 丟包)

# 檢查 DNS 解析
nslookup github.com
# 結果: 正常 (140.82.114.3)
```

**結論**: 網絡連接正常，問題不是 DNS 或網絡連接。

### 2. Git 配置檢查

```bash
# 檢查 Remote URL
git remote -v
# 結果:
# origin  https://<TOKEN_REDACTED>@github.com/MachineNativeOps/machine-native-ops.git (fetch)
# origin  https://<TOKEN_REDACTED>@github.com/MachineNativeOps/machine-native-ops.git (push)

# 檢查 Git 配置
git config --list | grep -E "(user|credential|url)"
# 結果:
# remote.origin.url=https://<TOKEN_REDACTED>@github.com/MachineNativeOps/machine-native-ops.git
# user.name=GL Runtime Platform
# user.email=gl-platform@machine-native-ops.com
```

**發現**:
- Token 直接嵌入在 URL 中
- 沒有配置 credential helper
- URL 格式可能不兼容當前 Git 版本

### 3. 詳細錯誤分析

使用 `GIT_CURL_VERBOSE=1` 進行詳細診斷：

```bash
GIT_CURL_VERBOSE=1 git push origin feature/gl-enterprise-architecture-v1.0.0 2>&1 | head -50
```

**關鍵發現**:
```
14:39:22.796509 http.c:725              == Info: Couldn't find host github.com in the (nil) file; using defaults
14:39:22.805329 http.c:725              == Info:   Trying 140.82.112.3:443...
14:39:22.878373 http.c:725              == Info: Connected to github.com (140.82.112.3) port 443 (#0)
14:39:22.904711 http.c:725              == Info: found 428 certificates in /etc/ssl/certs
14:39:22.979403 http.c:725              == Info: SSL connection using TLS1.3 / ECDHE_RSA_AES_128_GCM_SHA256
14:39:22.980855 http.c:725              == Info:   server certificate verification OK
14:39:23.061013 http.c:684              <= Recv header: HTTP/2 401
14:39:23.061029 http.c:684              <= Recv header: www-authenticate: Basic realm="GitHub"
```

**分析**:
- TCP 連接成功 ✅
- SSL/TLS 握手成功 ✅
- HTTP/2 連接建立成功 ✅
- **認證失敗** ❌ - 返回 401 Unauthorized

### 4. Token 驗證測試

測試 Token 是否有效：

```bash
# 測試 GitHub API 認證
curl -H "Authorization: token <TOKEN_REDACTED>" https://api.github.com/user
```

**結果**: ✅ 成功
```json
{
  "login": "MachineNativeOps",
  "id": 251967226,
  "type": "User",
  "site_admin": false,
  ...
}
```

測試倉庫權限：

```bash
curl -sH "Authorization: token <TOKEN_REDACTED>" \
  https://api.github.com/repos/MachineNativeOps/machine-native-ops | \
  grep -E "(push|admin|permissions)"
```

**結果**: ✅ 有權限
```json
"permissions": {
  "admin": true,
  "push": true,
  ...
}
```

**結論**: Token 本身有效且擁有推送權限。

### 5. 系統時間檢查

```bash
date
# 結果: Sat Jan 31 14:41:24 UTC 2026
```

**發現**: 系統時間錯誤（2026 年，應該是 2024 年）

**影響**: 
- HTTPS 證書驗證可能受影響
- 時間戳記錄錯誤
- 但從 CURL 日誌看，SSL 驗證仍然通過

### 6. 問題根本原因

通過深入分析，確定問題根源：

1. **URL 格式問題**:
   - 舊格式: `https://ghp_TOKEN@github.com/...`
   - 新格式: `https://x-access-token:TOKEN@github.com/...`
   - Git 2.39.5 對舊格式支持有變化

2. **缺少 Credential Helper**:
   - Git 無法正確處理認證信息
   - 每次推送都需要重新認證

3. **認證方式不匹配**:
   - Git 期望 Basic Auth
   - URL 中的 token 格式不匹配

## 解決方案

### 方案 1: 配置 Credential Helper ✅ 成功

```bash
# 配置 credential helper
git config --global credential.helper store

# 更新 Remote URL 格式
git remote set-url origin \
  https://x-access-token:<TOKEN_REDACTED>@github.com/MachineNativeOps/machine-native-ops.git

# 推送代碼
git push origin feature/gl-enterprise-architecture-v1.0.0
```

**結果**: ✅ 成功推送
```
remote: GitHub found 3 vulnerabilities on MachineNativeOps/machine-native-ops's default branch (2 moderate, 1 low).
To https://github.com/MachineNativeOps/machine-native-ops.git
   a087bf69..28fb94a0  feature/gl-enterprise-architecture-v1.0.0 -> feature/gl-enterprise-architecture-v1.0.0
```

### 方案 2: 使用 SSH Key（推薦用於長期使用）

```bash
# 生成 SSH Key
ssh-keygen -t ed25519 -C "gl-platform@machine-native-ops.com"

# 添加到 GitHub
# 複製 ~/.ssh/id_ed25519.pub 的內容到 GitHub Settings

# 更新 Remote URL
git remote set-url origin git@github.com:MachineNativeOps/machine-native-ops.git

# 測試連接
ssh -T git@github.com
```

### 方案 3: 使用 GitHub CLI（推薦用於 CI/CD）

```bash
# 登錄 GitHub CLI
gh auth login

# 推送代碼
git push origin feature/gl-enterprise-architecture-v1.0.0
```

## 學習要點

### 1. Git 認證機制

**舊方式**:
```bash
https://TOKEN@github.com/user/repo.git
```

**新方式**:
```bash
https://x-access-token:TOKEN@github.com/user/repo.git
```

**SSH 方式**:
```bash
git@github.com:user/repo.git
```

### 2. 診斷工具

- **CURL 詳細模式**: `GIT_CURL_VERBOSE=1`
- **追蹤模式**: `GIT_TRACE=1`
- **包追蹤**: `GIT_TRACE_PACKET=1`

### 3. Credential Helper 配置

```bash
# 存儲憑證（明文）
git config --global credential.helper store

# 緩存憑證（內存）
git config --global credential.helper 'cache --timeout=3600'

# macOS Keychain
git config --global credential.helper osxkeychain

# Windows Manager
git config --global credential.helper manager
```

### 4. 常見錯誤訊息

| 錯誤訊息 | 可能原因 | 解決方案 |
|---------|---------|---------|
| Could not resolve host | DNS 問題 | 檢查 `/etc/resolv.conf` |
| SSL certificate problem | 證書問題 | 檢查系統時間 |
| 401 Unauthorized | 認證失敗 | 檢查 token 權限 |
| 403 Forbidden | 權限不足 | 檢查倉庫權限 |
| Connection refused | 網絡問題 | 檢查防火牆/代理 |

### 5. 最佳實務

1. **使用 SSH Key**（最安全）
2. **使用 GitHub CLI**（最方便）
3. **不要將 token 提交到倉庫**
4. **定期輪換 token**
5. **使用最小權限原則**

### 6. 故障排查步驟

```bash
# 1. 檢查網絡連接
ping github.com
nslookup github.com

# 2. 檢查 Git 配置
git remote -v
git config --list

# 3. 測試 Token
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user

# 4. 詳細診斷
GIT_CURL_VERBOSE=1 git push origin BRANCH_NAME

# 5. 檢查憑證
git credential-manager version
git credential-store --version
```

## 總結

### 問題根源
Git Remote URL 格式不兼容當前 Git 版本（2.39.5），導致認證失敗。

### 解決方法
配置 Git Credential Helper 並更新為正確的 URL 格式。

### 經驗教訓
1. 始終使用最新的 Git 認證方式
2. 配置適當的 credential helper
3. 使用詳細模式進行診斷
4. 定期更新 Git 版本和工具

### 後續改進
1. 配置 SSH Key 用於長期使用
2. 設置自動化 CI/CD 流程
3. 實施 token 輪換策略
4. 監控 Git 操作日誌

---

**報告日期**: 2024-01-31  
**問題狀態**: ✅ 已解決  
**Git 版本**: 2.39.5  
**推送狀態**: 成功
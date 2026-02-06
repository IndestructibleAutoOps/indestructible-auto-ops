# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: documentation
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Architecture Governance Framework Activated
# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: documentation
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Architecture Governance Framework Activated
# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: documentation
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Architecture Governance Framework Activated
# Git 分支系統快速參考

## 快速開始

### 使用分支管理腳本
```bash
# 建立功能分支
./scripts/branch-manager.sh feature user-authentication

# 建立修復分支
./scripts/branch-manager.sh fix login-validation

# 建立緊急修復分支
./scripts/branch-manager.sh hotfix security-issue

# 列出所有分支
./scripts/branch-manager.sh list

# 同步主要分支
./scripts/branch-manager.sh sync
```

### 手動建立分支
```bash
# 功能開發
git checkout develop
git pull origin develop
git checkout -b feature/awesome-feature

# 一般修復
git checkout develop
git pull origin develop
git checkout -b fix/bug-description

# 緊急修復
git checkout main
git pull origin main
git checkout -b hotfix/critical-issue

# 重構
git checkout develop
git pull origin develop
git checkout -b refactor/component-name
```

## 分支類型快速查詢

| 分支類型 | 用途 | 基礎分支 | 合併目標 |
|---------|------|----------|----------|
| `feature/*` | 新功能開發 | develop | develop |
| `fix/*` | 一般 bug 修復 | develop | develop |
| `hotfix/*` | 緊急問題修復 | main | main, develop |
| `refactor/*` | 程式碼重構 | develop | develop |
| `test/*` | 測試相關工作 | develop | develop |
| `integration/*` | 整合測試 | develop | develop |
| `docs/*` | 文件更新 | develop | develop, main |
| `release/*` | 發布準備 | develop | main, develop |
| `experiment/*` | 實驗性功能 | develop | develop |
| `research/*` | 研究專案 | develop | develop |

## 提交訊息格式

### 功能開發
```
feat: add user authentication system
```

### Bug 修復
```
fix: resolve login page validation issue
```

### 緊急修復
```
hotfix: patch critical security vulnerability
```

### 重構
```
refactor: optimize database query performance
```

### 文件
```
docs: update API documentation
```

### 測試
```
test: add integration tests for payment module
```

### 發布
```
release: prepare version 2.0.0
```

## 常用工作流程

### 功能開發完整流程
```bash
# 1. 建立功能分支
git checkout develop
git pull origin develop
git checkout -b feature/new-feature

# 2. 開發功能
# ... 開發工作 ...

# 3. 提交變更
git add .
git commit -m "feat: add new feature"

# 4. 推送到遠端
git push origin feature/new-feature

# 5. 建立 Pull Request
# 在 GitHub 上建立 PR 到 develop 分支

# 6. 等待 Code Review 和 CI/CD 檢查

# 7. 合併後清理
git checkout develop
git pull origin develop
git branch -d feature/new-feature
git push origin --delete feature/new-feature
```

### 緊急修復流程
```bash
# 1. 建立緊急修復分支
git checkout main
git pull origin main
git checkout -b hotfix/critical-bug

# 2. 修復問題
# ... 修復工作 ...

# 3. 提交變更
git add .
git commit -m "hotfix: resolve critical security issue"

# 4. 推送到遠端
git push origin hotfix/critical-bug

# 5. 建立 Pull Request 到 main 和 develop

# 6. 緊急合併後標記版本
git tag -a v1.0.1 -m "Emergency fix for security issue"
git push origin v1.0.1

# 7. 清理分支
git checkout main
git pull origin main
git branch -d hotfix/critical-bug
git push origin --delete hotfix/critical-bug
```

### 發布流程
```bash
# 1. 建立發布分支
git checkout develop
git pull origin develop
git checkout -b release/v2.0.0

# 2. 準備發布
# ... 版本準備工作 ...

# 3. 提交變更
git add .
git commit -m "chore: prepare release v2.0.0"

# 4. 推送到遠端
git push origin release/v2.0.0

# 5. 建立 Pull Request 到 main

# 6. 合併到 main 後標記版本
git checkout main
git pull origin main
git tag -a v2.0.0 -m "Release version 2.0.0"
git push origin v2.0.0

# 7. 合併回 develop
git checkout develop
git merge main
git push origin develop

# 8. 清理
git branch -d release/v2.0.0
git push origin --delete release/v2.0.0
```

## 分支保護規則建議

### main 分支
- ✅ 需要 Pull Request
- ✅ 需要至少 1 個審核者
- ✅ 需要狀態檢查通過
- ✅ 需要通過 CI/CD
- ✅ 需要通過 CodeQL 掃描
- ❌ 禁止直接推送

### develop 分支
- ✅ 需要 Pull Request
- ✅ 需要至少 1 個審核者
- ✅ 需要狀態檢查通過
- ✅ 需要通過 CI/CD
- ❌ 禁止直接推送

### staging 分支
- ✅ 需要Pull Request
- ✅ 需要至少 1 個審核者
- ✅ 需要狀態檢查通過
- ❌ 禁止直接推送

## 故障排除

### 解決合併衝突
```bash
# 1. 更新目標分支
git checkout develop
git pull origin develop

# 2. 切換回功能分支
git checkout feature/my-feature

# 3. 合併目標分支
git merge develop

# 4. 解決衝突
# ... 手動編輯衝突文件 ...

# 5. 標記衝突已解決
git add .

# 6. 完成合併
git commit -m "resolve merge conflicts"

# 7. 推送
git push origin feature/my-feature
```

### 恢復已刪除的分支
```bash
# 查找分支的 commit hash
git reflog | grep feature/my-feature

# 重新建立分支
git checkout -b feature/my-feature <commit-hash>
```

### 同步遠端分支
```bash
# 刪除本地不存在的遠端分支引用
git remote prune origin

# 刪除本地已刪除的遠端分支
git fetch -p
```

## 最佳實踐

### 分支命名
- 使用小寫字母和連字符
- 保持簡短且描述性
- 遵循語意化版本控制
- 避免使用特殊字符

### 提交頻率
- 頻繁提交，小步驟
- 清晰的提交訊息
- 避免大型提交
- 及時推送變更

### 分支生命週期
- 保持分支短暫（1-2 週）
- 完成後立即刪除
- 避免長期存在的分支
- 定期清理舊分支

### 協作規範
- 及時溝通分支狀態
- 主動 Code Review
- 尊重審核者意見
- 維護清晰的歷史記錄

---

**注意**：有關完整的分支策略和治理合規性要求，請參考 `BRANCH_STRATEGY.md` 文件。
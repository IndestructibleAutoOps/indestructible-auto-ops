<!-- @GL-governed -->
<!-- @GL-layer: GL90-99 -->
<!-- @GL-semantic: governed-documentation -->
<!-- @GL-audit-trail: engine/governance/GL_SEMANTIC_ANCHOR.json -->

# Git 分支策略指南

## 分支系統概覽

本專案採用 **Git Flow** 與 **Trunk-Based Development** 混合策略，確保程式碼品質、治理合規性和高效的開發流程。

### 主要分支

| 分支 | 用途 | 保護等級 | 合併策略 |
|------|------|----------|----------|
| `main` | 生產環境程式碼 | 🔒 最嚴格 | 僅接受 PR 合併 |
| `develop` | 開發整合分支 | 🔒 嚴格 | 僅接受 PR 合併 |
| `staging` | 預發布環境 | 🔒 嚴格 | 僅接受 PR 合併 |

### 功能分支

#### 功能開發分支
```
feature/<feature-name>
```
- **用途**：開發新功能
- **來源**：從 `develop` 分支建立
- **合併目標**：合併回 `develop`
- **生命週期**：開發完成後合併並刪除

#### 修復分支
```
fix/<issue-description>
hotfix/<critical-issue>
```
- **用途**：修復 bug 和緊急問題
- **來源**：從 `develop` 或 `main` 分支建立
- **合併目標**：合併回 `develop` 和 `main`
- **生命週期**：修復完成後合併並刪除

#### 重構分支
```
refactor/<component-name>
```
- **用途**：程式碼重構和優化
- **來源**：從 `develop` 分支建立
- **合併目標**：合併回 `develop`
- **生命週期**：重構完成後合併並刪除

#### 測試分支
```
test/<test-type>
integration/<integration-name>
```
- **用途**：測試和整合驗證
- **來源**：從 `develop` 分支建立
- **合併目標**：合併回 `develop`
- **生命週期**：測試完成後合併並刪除

#### 文件分支
```
docs/<documentation-type>
```
- **用途**：文件更新和文檔維護
- **來源**：從 `develop` 分支建立
- **合併目標**：合併回 `develop` 和 `main`
- **生命週期**：文件完成後合併並刪除

#### 發布分支
```
release/<version>
```
- **用途**：準備發布新版本
- **來源**：從 `develop` 分支建立
- **合併目標**：合併回 `develop` 和 `main`
- **生命週期**：發布完成後標記版本並刪除

#### 實驗性分支
```
experiment/<experiment-name>
research/<research-topic>
```
- **用途**：實驗性功能和研究方向
- **來源**：從 `develop` 分支建立
- **合併目標**：實驗成功後合併到 `develop`
- **生命週期**：實驗完成後合併或刪除

## 工作流程

### 1. 功能開發流程
```
1. git checkout develop
2. git pull origin develop
3. git checkout -b feature/awesome-feature
4. ... 開發功能 ...
5. git add .
6. git commit -m "feat: add awesome feature"
7. git push origin feature/awesome-feature
8. 建立 Pull Request 到 develop
9. Code Review 和 CI/CD 驗證
10. 合併到 develop
11. 刪除 feature 分支
```

### 2. 緊急修復流程
```
1. git checkout main
2. git pull origin main
3. git checkout -b hotfix/critical-bug
4. ... 修復 bug ...
5. git add .
6. git commit -m "fix: resolve critical security issue"
7. git push origin hotfix/critical-bug
8. 建立 Pull Request 到 main 和 develop
9. 緊急 Code Review 和驗證
10. 合併到 main 和 develop
11. 標記版本號
12. 刪除 hotfix 分支
```

### 3. 發布流程
```
1. git checkout develop
2. git pull origin develop
3. git checkout -b release/v1.2.0
4. ... 準備發布 ...
5. git add .
6. git commit -m "chore: prepare release v1.2.0"
7. git push origin release/v1.2.0
8. 建立 Pull Request 到 main
9. 最終測試和驗證
10. 合併到 main
11. 標記版本 v1.2.0
12. 合併回 develop
13. 刪除 release 分支
```

## 分支命名規範

### 格式
```
<type>/<short-description>
```

### 類型
- `feature` - 新功能
- `fix` - 一般修復
- `hotfix` - 緊急修復
- `refactor` - 重構
- `test` - 測試
- `docs` - 文件
- `release` - 發布
- `experiment` - 實驗
- `research` - 研究

### 範例
- `feature/user-authentication`
- `fix/login-page-validation`
- `hotfix/security-vulnerability`
- `refactor/api-performance`
- `test/integration-suite`
- `docs/api-documentation`
- `release/v2.0.0`
- `experiment/ai-model-optimization`
- `research/microservices-architecture`

## 合併策略

### 主要分支合併規則
1. **main 分支**：
   - 僅接受 Pull Request 合併
   - 需要至少 1 個審核者批准
   - 必須通過所有 CI/CD 檢查
   - 必須通過 CodeQL 掃描
   - 必須通過治理合規性檢查

2. **develop 分支**：
   - 僅接受 Pull Request 合併
   - 需要至少 1 個審核者批准
   - 必須通過所有 CI/CD 檢查
   - 建議通過治理合規性檢查

3. **staging 分支**：
   - 僅接受 Pull Request 合併
   - 需要至少 1 個審核者批准
   - 必須通過所有 CI/CD 檢查

### 合併方法優先順序
1. **Squash and Merge** - 功能分支（保持歷史乾淨）
2. **Merge Commit** - 發布分支（保留發布歷史）
3. **Rebase and Merge** - 實驗性分支（保持線性歷史）

## 治理合規性要求

### GL 系統合規性
所有分支必須遵守：
- **GL Semantic Boundaries** - 語義邊界約束
- **GL Artifacts Matrix** - 治理工件矩陣
- **GL Filesystem Mapping** - 檔案系統映射
- **GL DSL** - 領域特定語言
- **GL DAG** - 依賴圖拓扑
- **GL Parallelism** - 並行驗證模式

### 合規性檢查
- 程式碼掃描和靜態分析
- 安全漏洞檢測
- 治理約束驗證
- 文件完整性檢查

## 最佳實踐

### 開發者指南
1. **保持分支短暫** - 分支生命週期不應超過 1-2 週
2. **頻繁提交** - 小步驟、頻繁提交，便於追蹤和回溯
3. **明確訊息** - 使用清晰的 commit 訊息
4. **即時同步** - 定期從上游分支同步更新
5. **完整測試** - 確保所有測試通過後才提交

### 團隊協作
1. **Code Review** - 所有程式碼必須經過審核
2. **CI/CD** - 自動化測試和部署
3. **文檔更新** - 同步更新相關文檔
4. **溝通協調** - 及時溝通分支狀態和衝突解決

## 工具和自動化

### GitHub Actions 工作流程
- 自動化 CI/CD 流程
- 自動化測試執行
- 自動化程式碼掃描
- 自動化部署流程

### 分支保護規則
- 防止直接推送到主要分支
- 要求 PR 審核
- 要求狀態檢查通過
- 限制可以合併的人員

## 疑難排解

### 常見問題
1. **合併衝突** - 及時溝通和協作解決
2. **測試失敗** - 修復測試或排除問題
3. **合規性檢查失敗** - 遵守治理約束
4. **部署失敗** - 檢查配置和環境變數

---

**注意**：本策略應根據專案需求和團隊規模進行調整。定期審查和優化分支策略以確保持續改進。
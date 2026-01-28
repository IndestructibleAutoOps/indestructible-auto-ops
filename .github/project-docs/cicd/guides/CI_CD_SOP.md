# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: documentation
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
# CI/CD 流程標準操作程序 (SOP)
## 持續整合與交付標準化流程

---

## 📋 文件概述

**目的：** 建立 CI/CD 流程的標準操作程序，確保代碼質量、提升團隊協作效率、實現 CI 驗證全數通過且無隱藏錯誤

**適用範圍：** 所有使用 Git 版本控制並通過 Pull Request (PR) 進行代碼審查的團隊成員

**核心目標：**
- ✅ CI 驗證全數通過
- ✅ 無隱藏錯誤與假通過
- ✅ 所有 CI 評論具有高度輔助價值
- ✅ 阻斷性問題快速識別與解決

---

## 🔐 安全性要求（必讀）

### 環境變量配置
```bash
# 設置 GitHub Token（必需）
export GL_TOKEN=your_personal_access_token

# 設置日誌級別
export LOG_LEVEL=info

# 設置工作環境
export ENVIRONMENT=development
```

### ⚠️ 關鍵安全注意事項
- **絕不將 Token 提交到版本庫**
- **定期更換 Token（建議每 90 天）**
- **僅授予最小權限範圍**
- **使用 GitHub Secrets 存儲 CI/CD 密鑰**
- **在日誌中過濾敏感信息**

---

## 第一階段：PR 創建流程

### 步驟 1：代碼分支管理

#### 1.1 創建功能分支
```bash
# 標準分支命名格式
git checkout -b feature/功能描述-YYYYMMDD
git checkout -b fix/修復問題-YYYYMMDD
git checkout -b hotfix/緊急修復-YYYYMMDD

# 示例
git checkout -b feature/user-authentication-20240123
git checkout -b fix/login-timeout-20240123
```

**具體操作說明：**
1. 確保在最新的 main 分支上
2. 創建新分支並立即切換
3. 分支名稱必須清晰描述功能或修復內容
4. 包含日期以便追蹤

**注意事項：**
- ⚠️ 不要直接在 main 分支上開發
- ⚠️ 避免使用模糊的分支名稱（如 `test`、`update`）
- ⚠️ 分支名稱使用小寫字母和連字符
- ✅ 保持一個分支對應一個功能或修復

**常見問題：**
- **問題：** 忘記更新 main 分支
- **解決方案：** 在創建分支前執行 `git pull origin main`
- **問題：** 分支名稱過長
- **解決方案：** 使用簡短但清晰的縮寫

**最佳實踐：**
- 在分支名稱中包含 JIRA/issue 編號
- 使用一致的命名約定
- 定期清理舊分支

---

### 步驟 2：本地開發與測試

#### 2.1 本地測試檢查清單
```bash
# 1. 代碼格式化
npm run format  # 或 black src/ (Python)
npm run lint    # 或 flake8 src/ (Python)

# 2. 本地單元測試
npm test        # 或 pytest tests/ (Python)

# 3. 類型檢查
npm run typecheck  # 或 mypy src/ (Python)

# 4. 構建驗證
npm run build   # 確保構建成功
```

**具體操作說明：**
1. 在提交代碼前必須通過所有本地測試
2. 修復所有 linting 錯誤和警告
3. 確保代碼符合團隊編碼規範
4. 運行完整的測試套件

**注意事項：**
- ⚠️ 不要提交有 linting 錯誤的代碼
- ⚠️ 確保所有測試在本地通過後再推送
- ⚠️ 檢查是否有新增的測試覆蓋新功能
- ✅ 運行完整測試套件，不只是部分測試

**常見問題：**
- **問題：** 測試在本地通過但在 CI 失敗
- **解決方案：** 檢查環境差異、依賴版本、時區設置
- **問題：** Linting 規則不一致
- **解決方案：** 使用團隊統一的配置文件（如 `.eslintrc`、`prettierrc`）

**最佳實踐：**
- 使用 Git hooks 自動化預提交檢查
- 在 `.gitignore` 中排除構建產物
- 提交前運行 `git status` 檢查未追蹤文件

---

### 步驟 3：代碼提交與推送

#### 3.1 提交規範
```bash
# 提交信息格式
git commit -m "type(scope): description

詳細描述（可選）

Co-authored-by: 協作者姓名 <email@example.com>
"

# 示例
git commit -m "feat(auth): add user authentication feature

- Implement JWT token validation
- Add login/logout endpoints
- Update user model with auth fields

Closes #123"
```

**具體操作說明：**
1. 使用 Conventional Commits 規範
2. 提交信息必須清晰描述變更內容
3. 在單次提交中保持相關性
4. 引用相關的 issue 編號

**注意事項：**
- ⚠️ 避免模糊的提交信息（如 "update code"）
- ⚠️ 不要在單次提交中混合不相關的變更
- ⚠️ 提交前檢查 `git diff --staged`
- ✅ 提交信息應該能讓他人理解變更內容

**常見問題：**
- **問題：** 提交後發現遺漏文件
- **解決方案：** 使用 `git commit --amend`（尚未推送）或創建新提交
- **問題：** 提交信息格式錯誤
- **解決方案：** 使用 `git commit --amend -m "正確信息"` 修正

**最佳實踐：**
- 在提交前進行代碼審查（自我審查）
- 使用 `.gitmessage` 模板統一提交格式
- 保持提交歷史清晰可讀

---

#### 3.2 推送到遠程倉庫
```bash
# 推送當前分支
git push -u origin feature/功能描述-YYYYMMDD

# 推送到特定遠程
git push -u origin fix/修復問題-YYYYMMDD

# 如果分支已存在，強制推送（謹慎使用）
git push --force-with-lease origin feature/功能描述-YYYYMMDD
```

**具體操作說明：**
1. 使用 `-u` 參數設置上游分支追蹤
2. 確保推送前所有本地提交已通過測試
3. 避免使用 `--force` 除非絕對必要

**注意事項：**
- ⚠️ 強制推送會重寫歷史，可能影響他人
- ⚠️ 推送前確認目標分支正確
- ⚠️ 確保網絡連接穩定
- ✅ 推送後立即檢查 CI 狀態

**常見問題：**
- **問題：** 推送被拒絕（rejected）
- **解決方案：** 先拉取並合併遠程變更 `git pull --rebase origin main`
- **問題：** 推送失敗（網絡問題）
- **解決方案：** 檢查網絡連接，稍後重試

**最佳實踐：**
- 推送後立即創建 PR
- 在 PR 中關聯相關 issue
- 設置分支保護規則

---

### 步驟 4：創建 Pull Request

#### 4.1 使用 GitHub CLI 創建 PR
```bash
# 基本命令
gh pr create \
  --title "PR標題" \
  --body "PR描述內容" \
  --base main \
  --repo MachineNativeOps/machine-native-ops

# 完整示例
gh pr create \
  --title "feat(auth): add user authentication" \
  --body "## 變更描述

實現用戶身份驗證功能，包括：
- JWT token 驗證
- 登入/登出端點
- 用戶模型更新

## 測試
- ✅ 本地單元測試通過
- ✅ 集成測試通過
- ✅ 手動測試完成

## 相關 Issue
Closes #123

## 檢查清單
- [x] 代碼符合規範
- [x] 測試覆蓋完整
- [x] 文檔已更新" \
  --base main \
  --label feature,authentication \
  --reviewer @reviewer1,@reviewer2 \
  --assignee @developer1
```

**具體操作說明：**
1. PR 標題必須清晰簡潔
2. PR 描述應包含完整上下文
3. 添加適當的 labels 和 reviewers
4. 關聯相關 issues

**注意事項：**
- ⚠️ PR 標題應遵循提交信息規範
- ⚠️ 描述中必須包含變更說明和測試確認
- ⚠️ 不要創建空 PR 或信息不足的 PR
- ✅ 在 PR 創建後立即通知審查者

**常見問題：**
- **問題：** PR 標題格式錯誤
- **解決方案：** 使用 `gh pr edit` 修正標題
- **問題：** 忘記添加 reviewer
- **解決方案：** 在 PR 頁面手動添加或使用 `gh pr edit`

**最佳實踐：**
- 使用 PR 模板統一格式
- 在描述中包含視覺效果（截圖、錄像）
- 提供 PR 預覽或演示環境

---

#### 4.2 PR URL 的生成和分享

**自動生成的 URL 格式：**
```
https://github.com/MachineNativeOps/machine-native-ops/pull/[PR_NUMBER]
```

**獲取 PR URL 的方法：**
```bash
# 方法 1：創建後自動顯示
gh pr create --title "..." --body "..." --base main
# 輸出：https://github.com/MachineNativeOps/machine-native-ops/pull/123

# 方法 2：列出最近創建的 PR
gh pr list --head your-branch-name --json url --jq '.[0].url'

# 方法 3：打開 PR 頁面
gh pr view --web
```

**分享 PR 的最佳實踐：**

1. **在團隊溝通渠道分享：**
```bash
# Slack/Discord 示例
🔔 新 PR 待審查：[PR標題]
📋 URL: https://github.com/MachineNativeOps/machine-native-ops/pull/123
👤 作者: @author
🏷️ Labels: feature, high-priority
📊 CI 狀態: ⏳ 運行中
```

2. **在 issue 中引用：**
```markdown
此 PR 解決了當前 issue：
- [PR #123](https://github.com/MachineNativeOps/machine-native-ops/pull/123)
```

3. **使用 GitHub @提及：**
```markdown
@reviewer1 @reviewer2 請審查此 PR
```

**注意事項：**
- ✅ 在分享時包含 PR 上下文（標題、作者、優先級）
- ✅ 指定期望的審查時間框架
- ✅ 提醒審查者關注特定的代碼部分
- ⚠️ 避免在不相關的討論中隨意分享 PR 鏈接

**常見問題：**
- **問題：** PR URL 無法訪問（404）
- **解決方案：** 確認 PR 是否已創建，檢查權限設置
- **問題：** PR 編號混淆
- **解決方案：** 使用完整的 PR URL 而非僅編號

---

#### 4.3 PR 必要信息清單

**每個 PR 必須包含的信息：**

```markdown
## 變更類型
- [ ] 新功能 (feature)
- [ ] Bug 修復 (bugfix)
- [ ] 重構 (refactor)
- [ ] 文檔更新 (docs)
- [ ] 測試更新 (test)
- [ ] 性能優化 (performance)

## 變更描述
<!-- 詳細描述變更內容 -->

## 影響範圍
- [ ] 前端
- [ ] 後端
- [ ] 數據庫
- [ ] API
- [ ] 配置文件
- [ ] 文檔

## 測試
- [ ] 單元測試通過
- [ ] 集成測試通過
- [ ] 端到端測試通過
- [ ] 手動測試完成
- [ ] 測試覆蓋率: [__]%

## 向後兼容性
- [ ] 破壞性變更 (Breaking Change)
- [ ] 需要數據遷移
- [ ] 需要配置更新
- [ ] 需要文檔更新

## 相關 Issue
- Closes #[ISSUE_NUMBER]
- Fixes #[ISSUE_NUMBER]
- Relates to #[ISSUE_NUMBER]

## 審查者
- @reviewer1
- @reviewer2

## 預估審查時間
- 小型變更: < 30 分鐘
- 中型變更: 30-60 分鐘
- 大型變更: > 60 分鐘
```

**注意事項：**
- ⚠️ 缺少必要信息的 PR 應被拒絕或要求補充
- ⚠️ 向後兼容性必須明確聲明
- ✅ 提供充分的上下文幫助審查者理解變更

**最佳實踐：**
- 使用自動化工具檢查 PR 信息完整性
- 設置 PR 模板在倉庫中
- 在 PR 描述中包含視覺輔助（截圖、GIF）

---

## 第二階段：CI 評論管理

### 步驟 5：CI 評論質量標準

#### 5.1 有極大輔助能力的評論特徵

**✅ 高質量評論必須具備：**

1. **具體性（Specific）**
   - 指出具體的代碼行或文件
   - 提供清晰的問題描述
   - 避免模糊的批評

   **示例：**
   ```
   ❌ 錯誤：這段代碼有問題
   ✅ 正確：在 src/auth/jwt.js:45 行，token 驗證邏輯缺少過期檢查，可能導致安全風險
   ```

2. **可操作性（Actionable）**
   - 提供具體的修復建議
   - 包含代碼示例或偽代碼
   - 引用相關文檔或最佳實踐

   **示例：**
   ```
   ✅ 建議修改：

   // 當前代碼
   function validateToken(token) {
       return jwt.verify(token, SECRET);
   }

   // 建議修改
   function validateToken(token) {
       try {
           const decoded = jwt.verify(token, SECRET);
           if (decoded.exp < Date.now()) {
               throw new Error('Token expired');
           }
           return decoded;
       } catch (error) {
           return null;
       }
   }

   參考：https://github.com/auth0/node-jsonwebtoken#readme
   ```

3. **上下文相關性（Contextual）**
   - 說明問題的影響範圍
   - 提供背景信息
   - 解釋為什麼這是問題

   **示例：**
   ```
   ✅ 上下文說明：
   
   此問題影響所有使用 JWT 驗證的端點，可能導致：
   1. 未授權訪問
   2. 安全漏洞
   3. 數據洩漏風險
   
   需要立即修復以確保系統安全性。
   ```

4. **建設性（Constructive）**
   - 使用專業和尊重的語氣
   - 專注於改進代碼質量
   - 避免人身攻擊

   **示例：**
   ```
   ❌ 錯誤：你的代碼寫得很差
   ✅ 正確：建議重構此函數以提高可讀性和可維護性
   ```

5. **優先級明確（Priority）**
   - 標明問題的嚴重程度
   - 說明是否阻斷性問題
   - 提供修復的緊急程度

   **示例：**
   ```
   🔴 嚴重（阻斷）：必須在合併前修復
   🟡 警告：建議修復但不阻斷合併
   🟢 建議：可以延後處理的優化建議
   ```

#### 5.2 CI 評論分類標準

**必須包含的 CI 評論類型：**

1. **代碼質量評論**
   - 錯誤處理
   - 邊界條件
   - 性能問題
   - 安全漏洞

2. **測試覆蓋評論**
   - 缺失的測試用例
   - 測試質量問題
   - 測試覆蓋率不足

3. **文檔評論**
   - 缺少的文檔
   - 過時的文檔
   - 不清楚的 API 文檔

4. **最佳實踐評論**
   - 代碼風格違規
   - 設計模式建議
   - 架構改進建議

#### 5.3 評論質量檢查清單

```bash
# 檢查評論質量的腳本
cat << 'EOF' > scripts/check_ci_comments.py
#!/usr/bin/env python3
"""
CI 評論質量檢查工具
"""
import re

class CommentQualityChecker:
    def __init__(self):
        self.quality_score = 0
        self.issues = []
    
    def check_comment(self, comment: str) -> dict:
        """檢查評論質量"""
        self.quality_score = 0
        self.issues = []
        
        # 檢查具體性
        if self._check_specificity(comment):
            self.quality_score += 25
        else:
            self.issues.append("評論缺乏具體性")
        
        # 檢查可操作性
        if self._check_actionable(comment):
            self.quality_score += 25
        else:
            self.issues.append("評論缺乏可操作性")
        
        # 檢查上下文
        if self._check_context(comment):
            self.quality_score += 25
        else:
            self.issues.append("評論缺乏上下文")
        
        # 檢查建設性
        if self._check_constructive(comment):
            self.quality_score += 25
        else:
            self.issues.append("評論語氣不夠建設性")
        
        return {
            'score': self.quality_score,
            'passing': self.quality_score >= 75,
            'issues': self.issues
        }
    
    def _check_specificity(self, comment: str) -> bool:
        """檢查是否包含具體的文件和行號引用"""
        return bool(re.search(r'[\w/]+\.\w+:\d+', comment))
    
    def _check_actionable(self, comment: str) -> bool:
        """檢查是否提供修復建議"""
        actionable_keywords = ['建議', '應該', '建議修改', '可以', '改進']
        return any(keyword in comment for keyword in actionable_keywords)
    
    def _check_context(self, comment: str) -> bool:
        """檢查是否提供上下文說明"""
        context_keywords = ['影響', '因為', '由於', '導致', '背景']
        return any(keyword in comment for keyword in context_keywords)
    
    def _check_constructive(self, comment: str) -> bool:
        """檢查是否使用建設性語言"""
        negative_patterns = [
            r'你的.*很差',
            r'這是錯的',
            r'寫得很差',
            r'不應該這樣寫'
        ]
        return not any(re.search(pattern, comment) for pattern in negative_patterns)

if __name__ == "__main__":
    import sys
    
    comment = sys.stdin.read() if not sys.stdin.isatty() else "測試評論"
    
    checker = CommentQualityChecker()
    result = checker.check_comment(comment)
    
    print(f"評論質量分數: {result['score']}/100")
    print(f"是否通過: {'✅' if result['passing'] else '❌'}")
    if result['issues']:
        print("問題:")
        for issue in result['issues']:
            print(f"  - {issue}")
EOF
```

---

### 步驟 6：過濾和禁止無意義評論

#### 6.1 識別無意義評論的模式

**❌ 無意義評論的特徵：**

1. **過於泛化**
   ```
   ❌ 這段代碼看起來不錯
   ❌ LGTM (Looks Good To Me) - 沒有任何說明
   ❌ 同意
   ❌ OK
   ```

2. **重複信息**
   ```
   ❌ [CI] 測試通過（與 CI 狀態重複）
   ❌ 測試失敗（與 CI 報告重複）
   ```

3. **無明確目的**
   ```
   ❌ 看看
   ❌ 試試
   ❌ 也許
   ```

4. **機器生成且無價值**
   ```
   ❌ [自動] 代碼已更新（沒有說明變更內容）
   ❌ [CI] 構建完成（沒有結果摘要）
   ```

#### 6.2 實施評論過濾機制

**方法 1：CI 工具配置**

```yaml
# .github/workflows/pr-quality-check.yml
name: PR Quality Check

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  comment-quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Check comment quality
        run: |
          python scripts/check_ci_comments.py << 'COMMENT'
          ${{ github.event.comment.body }}
          COMMENT
          
      - name: Block low-quality comments
        if: failure()
        run: |
          echo "⚠️ CI 評論質量不足，請改進後再提交"
          exit 1
```

**方法 2：GitHub Actions 評論過濾**

```yaml
# .github/workflows/filter-ci-comments.yml
name: Filter CI Comments

on:
  pull_request_review:
    types: [submitted, edited]

jobs:
  filter-comments:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Check comment quality
        id: check
        run: |
          COMMENT="${{ github.event.review.body }}"
          
          # 檢查評論長度
          if [ ${#COMMENT} -lt 20 ]; then
            echo "評論太短，缺乏詳細信息"
            exit 1
          fi
          
          # 檢查是否包含具體引用
          if ! echo "$COMMENT" | grep -qE "[\w/]+\.\w+:\d+"; then
            echo "評論必須引用具體的代碼行"
            exit 1
          fi
          
          echo "✅ 評論質量檢查通過"
```

**方法 3：評論模板和指南**

```markdown
<!-- .github/PULL_REQUEST_TEMPLATE.md -->
## CI 評論指南

### 如何撰寫有價值的評論

1. **引用具體代碼**
   ```
   在 src/auth/login.js:45 行，建議添加錯誤處理
   ```

2. **提供修復建議**
   ```
   建議使用 try-catch 塊包裝異步操作
   ```

3. **解釋原因**
   ```
   這可以防止未捕獲的 Promise rejection
   ```

### 避免的評論

- ❌ 太短的評論（< 20 字符）
- ❌ 無具體引用的泛泛而談
- ❌ 與 CI 狀態重複的信息
- ❌ 機器生成的無內容評論
```

---

### 步驟 7：監控和管理 CI 評論

#### 7.1 CI 評論監控腳本

```bash
#!/bin/bash
# scripts/monitor_ci_comments.sh

PR_NUMBER=$1

if [ -z "$PR_NUMBER" ]; then
    echo "Usage: $0 <PR_NUMBER>"
    exit 1
fi

echo "=== 監控 PR #$PR_NUMBER 的 CI 評論 ==="
echo ""

# 獲取所有評論
gh api \
  repos/MachineNativeOps/machine-native-ops/pulls/$PR_NUMBER/comments \
  --jq '.[] | select(.body | contains("[CI]") or contains("[自動]")) | {user, body, created_at}'

echo ""
echo "=== 評論質量分析 ==="

# 統計評論類型
echo "總 CI 評論數: $(gh api repos/MachineNativeOps/machine-native-ops/pulls/$PR_NUMBER/comments --jq '. | length')"

# 檢查低質量評論
echo ""
echo "⚠️ 可能的無意義評論:"
gh api \
  repos/MachineNativeOps/machine-native-ops/pulls/$PR_NUMBER/comments \
  --jq '.[] | select(.body | length < 30) | {user, body}' \
  || echo "未發現無意義評論"
```

**使用方法：**
```bash
chmod +x scripts/monitor_ci_comments.sh
./scripts/monitor_ci_comments.sh 123
```

#### 7.2 自動化評論管理

```python
#!/usr/bin/env python3
# scripts/manage_ci_comments.py

import requests
import os

class CICommentManager:
    def __init__(self, repo, token):
        self.repo = repo
        self.token = token
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.api_base = f'https://api.github.com/repos/{repo}'
    
    def get_pr_comments(self, pr_number):
        """獲取 PR 的所有評論"""
        url = f'{self.api_base}/pulls/{pr_number}/comments'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def identify_low_quality_comments(self, comments):
        """識別低質量評論"""
        low_quality = []
        
        for comment in comments:
            body = comment['body']
            
            # 檢查評論長度
            if len(body) < 20:
                low_quality.append({
                    'id': comment['id'],
                    'reason': '評論太短',
                    'body': body
                })
                continue
            
            # 檢查是否包含具體引用
            if not any(c.isdigit() for c in body) and ':' not in body:
                low_quality.append({
                    'id': comment['id'],
                    'reason': '缺乏具體引用',
                    'body': body
                })
                continue
            
            # 檢查是否為機器生成且無價值
            if body.startswith('[自動]') and len(body) < 50:
                low_quality.append({
                    'id': comment['id'],
                    'reason': '機器生成且無價值',
                    'body': body
                })
        
        return low_quality
    
    def delete_comment(self, comment_id):
        """刪除評論"""
        url = f'{self.api_base}/pulls/comments/{comment_id}'
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()
        return response.status_code == 204
    
    def hide_comment(self, comment_id):
        """隱藏評論（不刪除）"""
        url = f'{self.api_base}/pulls/comments/{comment_id}'
        response = requests.patch(
            url,
            headers=self.headers,
            json={'body': '[此評論已被隱藏 - 質量不足]'}
        )
        response.raise_for_status()
        return response.status_code == 200
    
    def monitor_and_cleanup(self, pr_number, dry_run=True):
        """監控並清理低質量評論"""
        comments = self.get_pr_comments(pr_number)
        low_quality = self.identify_low_quality_comments(comments)
        
        print(f"找到 {len(low_quality)} 個低質量評論")
        
        for comment in low_quality:
            print(f"\n評論 ID: {comment['id']}")
            print(f"原因: {comment['reason']}")
            print(f"內容: {comment['body'][:100]}...")
            
            if not dry_run:
                # 可以選擇刪除或隱藏
                if comment['reason'] == '機器生成且無價值':
                    self.hide_comment(comment['id'])
                    print("✅ 已隱藏評論")
                else:
                    print("⚠️ 需要人工審查")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python manage_ci_comments.py <PR_NUMBER> [--dry-run]")
        sys.exit(1)
    
    pr_number = sys.argv[1]
    dry_run = '--dry-run' in sys.argv
    
    token = os.getenv('GL_TOKEN')
    if not token:
        print("錯誤: GL_TOKEN 環境變量未設置")
        sys.exit(1)
    
    manager = CICommentManager('MachineNativeOps/machine-native-ops', token)
    manager.monitor_and_cleanup(pr_number, dry_run=dry_run)
```

**使用方法：**
```bash
# 試運行（不實際刪除）
python scripts/manage_ci_comments.py 123 --dry-run

# 實際執行
python scripts/manage_ci_comments.py 123
```

---

## 第三階段：CI 驗證狀態監控

### 步驟 8：持續追蹤 CI 狀態

#### 8.1 實時監控 CI 狀態

```bash
#!/bin/bash
# scripts/monitor_ci_status.sh

PR_NUMBER=$1
CHECK_INTERVAL=${2:-30}  # 默認每 30 秒檢查一次

if [ -z "$PR_NUMBER" ]; then
    echo "Usage: $0 <PR_NUMBER> [CHECK_INTERVAL]"
    exit 1
fi

echo "=== 監控 PR #$PR_NUMBER 的 CI 狀態 ==="
echo "檢查間隔: $CHECK_INTERVAL 秒"
echo ""

while true; do
    # 獲取 PR 狀態
    STATUS=$(gh pr view $PR_NUMBER --json statusCheckRollup --jq '.statusCheckRollup | .[] | select(.conclusion != null) | {name, conclusion, status} | "\(.name): \(.conclusion) (\(.status))"' 2>/dev/null)
    
    if [ -z "$STATUS" ]; then
        echo "⏳ 等待 CI 開始..."
    else
        # 顯示當前狀態
        echo "[$(date '+%Y-%m-%d %H:%M:%S')]"
        echo "$STATUS"
        echo ""
        
        # 檢查是否有失敗的檢查
        FAILED=$(echo "$STATUS" | grep -i "failure\|cancelled" || true)
        if [ -n "$FAILED" ]; then
            echo "❌ 發現失敗的 CI 檢查:"
            echo "$FAILED"
            
            # 詢問是否繼續監控
            read -p "是否繼續監控? (y/n) " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                break
            fi
        fi
        
        # 檢查是否全部通過
        PENDING=$(echo "$STATUS" | grep -i "pending\|in_progress" || true)
        if [ -z "$PENDING" ] && [ -z "$FAILED" ]; then
            echo "✅ 所有 CI 檢查已通過！"
            break
        fi
    fi
    
    sleep $CHECK_INTERVAL
done
```

**使用方法：**
```bash
chmod +x scripts/monitor_ci_status.sh
./scripts/monitor_ci_status.sh 123 30
```

#### 8.2 CI 狀態儀表板

```python
#!/usr/bin/env python3
# scripts/ci_dashboard.py

import requests
import json
from datetime import datetime
from typing import Dict, List
import os

class CIDashboard:
    def __init__(self, repo: str, token: str):
        self.repo = repo
        self.token = token
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.api_base = f'https://api.github.com/repos/{repo}'
    
    def get_pr_status(self, pr_number: int) -> Dict:
        """獲取 PR 的 CI 狀態"""
        url = f'{self.api_base}/pulls/{pr_number}'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_check_runs(self, pr_number: int) -> List[Dict]:
        """獲取 PR 的檢查運行"""
        url = f'{self.api_base}/commits/{pr_number}/check-runs'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()['check_runs']
    
    def analyze_status(self, pr_number: int) -> Dict:
        """分析 CI 狀態"""
        pr_data = self.get_pr_status(pr_number)
        check_runs = self.get_check_runs(pr_number['head']['sha'])
        
        analysis = {
            'pr_number': pr_number,
            'title': pr_data['title'],
            'state': pr_data['state'],
            'total_checks': len(check_runs),
            'passed': 0,
            'failed': 0,
            'pending': 0,
            'cancelled': 0,
            'checks': []
        }
        
        for check in check_runs:
            status = check['conclusion'] or check['status']
            check_info = {
                'name': check['name'],
                'status': status,
                'started_at': check.get('started_at'),
                'completed_at': check.get('completed_at'),
                'details_url': check.get('details_url')
            }
            
            if status == 'success':
                analysis['passed'] += 1
            elif status == 'failure':
                analysis['failed'] += 1
            elif status in ['pending', 'queued', 'in_progress']:
                analysis['pending'] += 1
            elif status == 'cancelled':
                analysis['cancelled'] += 1
            
            analysis['checks'].append(check_info)
        
        return analysis
    
    def generate_report(self, pr_number: int) -> str:
        """生成 CI 狀態報告"""
        analysis = self.analyze_status(pr_number)
        
        report = f"""
# CI 狀態報告 - PR #{analysis['pr_number']}

**標題:** {analysis['title']}
**生成時間:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 總體狀態

- 總檢查數: {analysis['total_checks']}
- ✅ 通過: {analysis['passed']}
- ❌ 失敗: {analysis['failed']}
- ⏳ 進行中: {analysis['pending']}
- ⚠️ 取消: {analysis['cancelled']}

## 詳細檢查結果

"""
        
        for check in analysis['checks']:
            status_emoji = {
                'success': '✅',
                'failure': '❌',
                'pending': '⏳',
                'queued': '🔄',
                'in_progress': '🔄',
                'cancelled': '⚠️'
            }.get(check['status'], '❓')
            
            report += f"{status_emoji} **{check['name']}**\n"
            report += f"   狀態: {check['status']}\n"
            
            if check.get('completed_at'):
                report += f"   完成時間: {check['completed_at']}\n"
            elif check.get('started_at'):
                report += f"   開始時間: {check['started_at']}\n"
            
            if check.get('details_url'):
                report += f"   詳細: {check['details_url']}\n"
            
            report += "\n"
        
        return report
    
    def check_blocking_issues(self, pr_number: int) -> List[Dict]:
        """檢查阻斷性問題"""
        analysis = self.analyze_status(pr_number)
        blocking = []
        
        for check in analysis['checks']:
            if check['status'] == 'failure':
                blocking.append({
                    'check': check['name'],
                    'reason': '檢查失敗',
                    'severity': 'high',
                    'action': '必須修復後才能合併'
                })
            elif check['status'] == 'cancelled':
                blocking.append({
                    'check': check['name'],
                    'reason': '檢查被取消',
                    'severity': 'medium',
                    'action': '重新運行檢查'
                })
        
        return blocking

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python ci_dashboard.py <PR_NUMBER>")
        sys.exit(1)
    
    pr_number = int(sys.argv[1])
    token = os.getenv('GL_TOKEN')
    
    if not token:
        print("錯誤: GL_TOKEN 環境變量未設置")
        sys.exit(1)
    
    dashboard = CIDashboard('MachineNativeOps/machine-native-ops', token)
    
    # 生成報告
    report = dashboard.generate_report(pr_number)
    print(report)
    
    # 檢查阻斷性問題
    blocking = dashboard.check_blocking_issues(pr_number)
    if blocking:
        print("## ⚠️ 阻斷性問題\n")
        for issue in blocking:
            print(f"- **{issue['check']}**: {issue['reason']}")
            print(f"  嚴重性: {issue['severity']}")
            print(f"  行動: {issue['action']}\n")
```

**使用方法：**
```bash
python scripts/ci_dashboard.py 123
```

---

### 步驟 9：阻斷性問題處理流程

#### 9.1 阻斷性問題分類

**🔴 嚴重阻斷（必須立即處理）：**

1. **測試失敗**
   - 單元測試失敗
   - 集成測試失敗
   - 端到端測試失敗

2. **代碼質量檢查失敗**
   - Linting 錯誤
   - 類型檢查失敗
   - 安全漏洞檢測失敗

3. **構建失敗**
   - 編譯錯誤
   - 依賴解析失敗
   - 構建超時

**🟡 中等阻斷（應該儘快處理）：**

1. **測試覆蓋率不足**
   - 覆蓋率低於門檻
   - 關鍵路徑未測試

2. **性能問題**
   - 響應時間過長
   - 內存洩漏

3. **文檔問題**
   - API 文檔缺失
   - 變更日誌未更新

**🟢 輕微阻斷（可以延後處理）：**

1. **代碼風格警告**
   - 格式不一致
   - 命名約定違規

2. **優化建議**
   - 代碼重構建議
   - 性能優化機會

#### 9.2 阻斷性問題處理腳本

```bash
#!/bin/bash
# scripts/handle_blocking_issues.sh

PR_NUMBER=$1

if [ -z "$PR_NUMBER" ]; then
    echo "Usage: $0 <PR_NUMBER>"
    exit 1
fi

echo "=== 處理 PR #$PR_NUMBER 的阻斷性問題 ==="
echo ""

# 獲取失敗的檢查
FAILED_CHECKS=$(gh pr view $PR_NUMBER --json statusCheckRollup --jq '.statusCheckRollup | .[] | select(.conclusion == "failure" or .conclusion == "timed_out") | {name, conclusion, detailsUrl}' 2>/dev/null)

if [ -z "$FAILED_CHECKS" ]; then
    echo "✅ 未發現阻斷性問題"
    exit 0
fi

echo "❌ 發現阻斷性問題:"
echo "$FAILED_CHECKS"
echo ""

# 分析並提供建議
echo "=== 建議處理步驟 ==="

# 檢查測試失敗
if echo "$FAILED_CHECKS" | grep -qi "test"; then
    echo ""
    echo "📝 測試失敗處理:"
    echo "1. 查看失敗的測試日誌"
    echo "   gh run list --limit 1 --json databaseId | jq -r '.[0].databaseId'"
    echo "   gh run view RUN_ID --log-failed"
    echo ""
    echo "2. 本地重現問題"
    echo "   npm test -- --grep '失敗的測試名稱'"
    echo ""
    echo "3. 修復並重新運行測試"
    echo "   npm test"
fi

# 檢查 Linting 錯誤
if echo "$FAILED_CHECKS" | grep -qi "lint\|style\|format"; then
    echo ""
    echo "📝 Linting 錯誤處理:"
    echo "1. 自動修復（如果支持）"
    echo "   npm run lint:fix"
    echo ""
    echo "2. 手動修復錯誤"
    echo "   npm run lint"
fi

# 檢查構建失敗
if echo "$FAILED_CHECKS" | grep -qi "build\|compile"; then
    echo ""
    echo "📝 構建失敗處理:"
    echo "1. 查看構建日誌"
    echo "   gh run view RUN_ID --log"
    echo ""
    echo "2. 檢查依賴"
    echo "   npm audit"
    echo "   npm install"
fi

# 提供重新運行選項
echo ""
echo "=== 重新運行 CI 檢查 ==="
read -p "是否要重新運行失敗的檢查? (y/n) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "重新運行檢查..."
    gh run rerun --failed
    echo "✅ 檢查已重新運行"
fi

echo ""
echo "=== 監控 CI 狀態 ==="
read -p "是否要持續監控 CI 狀態? (y/n) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    ./scripts/monitor_ci_status.sh $PR_NUMBER 30
fi
```

**使用方法：**
```bash
chmod +x scripts/handle_blocking_issues.sh
./scripts/handle_blocking_issues.sh 123
```

---

### 步驟 10：關鍵指標監控

#### 10.1 CI 關鍵指標

**必須監控的指標：**

1. **測試通過率**
   ```bash
   # 計算測試通過率
   TOTAL_RUNS=$(gh run list --limit 100 --json conclusion --jq '. | length')
   PASSED_RUNS=$(gh run list --limit 100 --json conclusion --jq '.[] | select(.conclusion == "success")' | wc -l)
   PASS_RATE=$((PASSED_RUNS * 100 / TOTAL_RUNS))
   echo "測試通過率: ${PASS_RATE}%"
   ```

2. **平均構建時間**
   ```bash
   # 計算平均構建時間
   gh run list --limit 50 --json conclusion,updatedAt,createdAt | \
     jq -r '.[] | select(.conclusion == "success") | (.updatedAt | fromdateiso8601) - (.createdAt | fromdateiso8601)' | \
     awk '{sum+=$1; count++} END {print "平均構建時間:", sum/count, "秒"}'
   ```

3. **PR 到合併時間**
   ```bash
   # 計算平均 PR 到合併時間
   gh pr list --limit 50 --merged --json mergedAt,createdAt | \
     jq -r '.[] | (.mergedAt | fromdateiso8601) - (.createdAt | fromdateiso8601)' | \
     awk '{sum+=$1; count++} END {print "平均 PR 到合併時間:", sum/count/3600, "小時"}'
   ```

4. **CI 失敗率**
   ```bash
   # 計算 CI 失敗率
   TOTAL_RUNS=$(gh run list --limit 100 --json conclusion --jq '. | length')
   FAILED_RUNS=$(gh run list --limit 100 --json conclusion --jq '.[] | select(.conclusion == "failure")' | wc -l)
   FAILURE_RATE=$((FAILED_RUNS * 100 / TOTAL_RUNS))
   echo "CI 失敗率: ${FAILURE_RATE}%"
   ```

#### 10.2 指標監控儀表板

```python
#!/usr/bin/env python3
# scripts/ci_metrics.py

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List
import os

class CIMetrics:
    def __init__(self, repo: str, token: str):
        self.repo = repo
        self.token = token
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.api_base = f'https://api.github.com/repos/{repo}'
    
    def get_workflow_runs(self, days: int = 30) -> List[Dict]:
        """獲取最近 N 天的工作流運行"""
        since = (datetime.now() - timedelta(days=days)).isoformat()
        url = f'{self.api_base}/actions/runs?per_page=100&created={since}'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()['workflow_runs']
    
    def calculate_pass_rate(self, runs: List[Dict]) -> float:
        """計算通過率"""
        total = len(runs)
        if total == 0:
            return 0.0
        
        passed = len([r for r in runs if r['conclusion'] == 'success'])
        return (passed / total) * 100
    
    def calculate_avg_duration(self, runs: List[Dict]) -> float:
        """計算平均持續時間"""
        completed = [r for r in runs if r['conclusion'] is not None and r['updated_at']]
        if not completed:
            return 0.0
        
        durations = []
        for run in completed:
            start = datetime.fromisoformat(run['created_at'].replace('Z', '+00:00'))
            end = datetime.fromisoformat(run['updated_at'].replace('Z', '+00:00'))
            duration = (end - start).total_seconds()
            durations.append(duration)
        
        return sum(durations) / len(durations) if durations else 0.0
    
    def calculate_failure_rate(self, runs: List[Dict]) -> float:
        """計算失敗率"""
        total = len(runs)
        if total == 0:
            return 0.0
        
        failed = len([r for r in runs if r['conclusion'] == 'failure'])
        return (failed / total) * 100
    
    def generate_metrics_report(self, days: int = 30) -> str:
        """生成指標報告"""
        runs = self.get_workflow_runs(days)
        
        report = f"""
# CI 指標報告

**報告期間:** 最近 {days} 天
**生成時間:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**總運行次數:** {len(runs)}

## 關鍵指標

### 1. 測試通過率
- **數值:** {self.calculate_pass_rate(runs):.2f}%
- **目標:** ≥ 95%
- **狀態:** {'✅' if self.calculate_pass_rate(runs) >= 95 else '⚠️'}

### 2. 平均構建時間
- **數值:** {self.calculate_avg_duration(runs)/60:.2f} 分鐘
- **目標:** ≤ 10 分鐘
- **狀態:** {'✅' if self.calculate_avg_duration(runs) <= 600 else '⚠️'}

### 3. CI 失敗率
- **數值:** {self.calculate_failure_rate(runs):.2f}%
- **目標:** ≤ 5%
- **狀態:** {'✅' if self.calculate_failure_rate(runs) <= 5 else '⚠️'}

## 工作流運行統計

"""
        
        # 按工作流統計
        workflow_stats = {}
        for run in runs:
            name = run['name']
            if name not in workflow_stats:
                workflow_stats[name] = {
                    'total': 0,
                    'passed': 0,
                    'failed': 0
                }
            workflow_stats[name]['total'] += 1
            if run['conclusion'] == 'success':
                workflow_stats[name]['passed'] += 1
            elif run['conclusion'] == 'failure':
                workflow_stats[name]['failed'] += 1
        
        for workflow, stats in sorted(workflow_stats.items()):
            pass_rate = (stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0
            report += f"""
### {workflow}
- 總運行: {stats['total']}
- 通過: {stats['passed']}
- 失敗: {stats['failed']}
- 通過率: {pass_rate:.2f}%
"""
        
        return report

if __name__ == "__main__":
    import sys
    
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    token = os.getenv('GL_TOKEN')
    
    if not token:
        print("錯誤: GL_TOKEN 環境變量未設置")
        sys.exit(1)
    
    metrics = CIMetrics('MachineNativeOps/machine-native-ops', token)
    report = metrics.generate_metrics_report(days)
    print(report)
```

**使用方法：**
```bash
python scripts/ci_metrics.py 30
```

---

## 📊 總結檢查清單

### PR 創建階段檢查清單

- [ ] 分支命名符合規範
- [ ] 本地測試全部通過
- [ ] 代碼格式化和 linting 通過
- [ ] 提交信息符合 Conventional Commits
- [ ] 推送前確認 CI 配置正確
- [ ] PR 描述包含必要信息
- [ ] 添加適當的 labels 和 reviewers
- [ ] 關聯相關 issues
- [ ] PR URL 已分享給團隊
- [ ] 確認 CI 已開始運行

### CI 評論管理檢查清單

- [ ] 所有 CI 評論具有具體性
- [ ] 評論提供可操作的建議
- [ ] 評論包含相關上下文
- [ ] 評論語氣建設性且專業
- [ ] 過濾掉無意義的評論
- [ ] 機器生成評論有實際價值
- [ ] 評論質量分數 ≥ 75 分
- [ ] 定期審查和清理低質量評論
- [ ] 評論監控腳本已配置
- [ ] 評論模板已建立

### CI 驗證狀態監控檢查清單

- [ ] CI 狀態持續監控已啟動
- [ ] 阻斷性問題及時識別
- [ ] 失敗檢查立即通知
- [ ] 問題分類和優先級明確
- [ ] 修復流程已文檔化
- [ ] 關鍵指標定期追蹤
- [ ] 測試通過率 ≥ 95%
- [ ] 平均構建時間 ≤ 10 分鐘
- [ ] CI 失敗率 ≤ 5%
- [ ] 監控儀表板已配置

---

## 🔧 故障排除指南

### 常見問題和解決方案

#### 問題 1：CI 運行中但一直不完成
**可能原因：**
- 測試掛起
- 依賴下載失敗
- 資源不足

**解決方案：**
1. 檢查 CI 日誌查找掛起的測試
2. 重新運行 CI: `gh run rerun`
3. 增加超時時間
4. 檢查網絡連接和依賴可用性

#### 問題 2：測試本地通過但 CI 失敗
**可能原因：**
- 環境差異
- 依賴版本不一致
- 時區或配置差異

**解決方案：**
1. 檢查 CI 環境配置
2. 鎖定依賴版本（package-lock.json, requirements.txt）
3. 在本地模擬 CI 環境
4. 使用 Docker 容器確保一致性

#### 問題 3：CI 評論質量不足
**可能原因：**
- CI 配置不當
- 自動化工具配置錯誤
- 缺少評論模板

**解決方案：**
1. 配置評論質量檢查工具
2. 建立評論模板
3. 培訓團隊成員
4. 實施評論審查流程

#### 問題 4：假通過（False Positive）
**可能原因：**
- 測試覆蓋不足
- Mock 過度使用
- 測試未驗證關鍵路徑

**解決方案：**
1. 增加測試覆蓋率
2. 實施集成測試
3. 減少 Mock 使用
4. 添加端到端測試
5. 代碼審查時專注測試質量

---

## 📚 附錄

### A. 有用的 GitHub CLI 命令

```bash
# 查看 PR 狀態
gh pr view

# 查看 CI 運行
gh run list

# 查看 CI 日誌
gh run view RUN_ID --log

# 重新運行失敗的檢查
gh run rerun --failed

# 查看 PR 的所有評論
gh pr view --json comments --jq '.comments[]'

# 合併 PR
gh pr merge

# 添加 reviewer
gh pr edit --add-reviewer @username

# 添加 label
gh pr edit --add-label "label-name"
```

### B. CI 配置文件示例

```yaml
# .github/workflows/ci.yml
name: CI

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run linter
        run: npm run lint
      
      - name: Run tests
        run: npm test
      
      - name: Check coverage
        run: npm run test:coverage
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

---

## ✅ 最終目標驗證

為了確保達成「CI 驗證全數通過，沒有隱藏的錯誤與假通過」的最終目標，請執行以下驗證步驟：

### 驗證步驟 1：CI 狀態驗證
```bash
# 確認所有 CI 檢查通過
gh pr view --json statusCheckRollup --jq '.statusCheckRollup | .[] | select(.conclusion != "success")'

# 如果有輸出，說明有未通過的檢查
```

### 驗證步驟 2：測試覆蓋率驗證
```bash
# 檢查測試覆蓋率
npm run test:coverage

# 確認覆蓋率達到目標（建議 ≥ 80%）
```

### 驗證步驟 3：代碼質量驗證
```bash
# 運行所有質量檢查
npm run lint
npm run typecheck
npm run test

# 確認全部通過
```

### 驗證步驟 4：人工審查驗證
- [ ] 至少一位審查者已批准
- [ ] 所有 CI 評論已處理
- [ ] 阻斷性問題已解決
- [ ] 代碼變更已充分審查

### 驗證步驟 5：文檔驗證
- [ ] 變更日誌已更新
- [ ] API 文檔已更新（如需要）
- [ ] README 已更新（如需要）
- [ ] 技術文檔已更新（如需要）

通過以上所有驗證步驟後，即可安全地合併 PR 到主分支。

---

**文檔版本:** 1.0.0
**最後更新:** 2024-01-23
**維護者:** DevOps 團隊
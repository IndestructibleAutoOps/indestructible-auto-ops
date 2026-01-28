# CI/CD SOP 快速入門指南

## 📚 完整文檔
詳細的標準操作程序請參考：[CI_CD_SOP.md](CI_CD_SOP.md)

## 🚀 5 分鐘快速開始

### 1. 創建 Pull Request

```bash
# 創建功能分支
git checkout -b feature/your-feature-$(date +%Y%m%d)

# 進行開發和測試
npm run lint
npm test

# 提交代碼
git add .
git commit -m "feat: add your feature description"

# 推送並創建 PR
git push -u origin feature/your-feature-$(date +%Y%m%d)
gh pr create --title "feat: add your feature" \
            --body "描述您的變更..." \
            --base main
```

### 2. 監控 CI 狀態

```bash
# 監控特定 PR 的 CI 狀態
./scripts/monitor_ci_status.sh <PR_NUMBER>

# 示例
./scripts/monitor_ci_status.sh 123
```

### 3. 檢查評論質量

```bash
# 檢查評論質量
echo "在 src/auth.js:45 行，建議添加錯誤處理" | python scripts/check_ci_comments.py

# 或使用文件
python scripts/check_ci_comments.py < comment.txt
```

## ✅ 關鍵檢查清單

### PR 創建前
- [ ] 本地測試全部通過
- [ ] 代碼格式化和 linting 通過
- [ ] 提交信息符合規範
- [ ] 分支命名正確

### CI 評論標準
- [ ] 引用具體的文件和行號
- [ ] 提供可操作的建議
- [ ] 說明上下文和影響
- [ ] 使用建設性語氣
- [ ] 評論質量分數 ≥ 75

### CI 驗證監控
- [ ] 所有檢查通過
- [ ] 無阻斷性問題
- [ ] 測試覆蓋率達標
- [ ] 代碼質量檢查通過

## 🔧 有用的腳本

### 1. `monitor_ci_status.sh`
持續監控 PR 的 CI 狀態

```bash
./scripts/monitor_ci_status.sh <PR_NUMBER> [INTERVAL]
```

### 2. `check_ci_comments.py`
檢查 CI 評論質量

```bash
python scripts/check_ci_comments.py <評論內容>
```

## 📊 關鍵指標目標

- ✅ 測試通過率: ≥ 95%
- ✅ 平均構建時間: ≤ 10 分鐘
- ✅ CI 失敗率: ≤ 5%
- ✅ 測試覆蓋率: ≥ 80%

## ⚠️ 常見問題

### Q: CI 失敗怎麼辦？
A: 查看失敗日誌，本地重現問題，修復後重新推送。

### Q: 如何重新運行 CI？
A: `gh run rerun --failed`

### Q: 評論質量不達標怎麼辦？
A: 使用 `check_ci_comments.py` 檢查並根據建議改進。

## 🔗 相關資源

- [完整 SOP 文檔](CI_CD_SOP.md)
- [GitHub CLI 文檔](https://cli.github.com/)
- [CI/CD 最佳實踐](https://docs.github.com/en/actions)
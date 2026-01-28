# 自動化程式碼品質工具

本目錄包含自動化執行 PR #1 審查建議的工具和工作流程。

## 🎯 目的

將 PR-1-REVIEW-REPORT.md 中的手動檢查項目轉換為全自動化流程，包括：
- 自動掃描和報告品質問題
- 自動修復可修復的問題
- CI/CD 整合

## 📁 檔案結構

```
.
├── .github/workflows/
│   └── pr-quality-check.yml      # GitHub Actions 工作流程
├── scripts/
│   ├── auto-quality-check.py     # 自動品質檢查腳本
│   └── auto-fix-issues.py        # 自動修復腳本
└── AUTOMATION-README.md           # 本文件
```

## 🚀 快速開始

### 1. 本地執行自動品質檢查

```bash
# 執行完整的品質檢查
python scripts/auto-quality-check.py

# 查看生成的報告
cat AUTO-QUALITY-REPORT.md
cat auto-quality-report.json
```

### 2. 本地執行自動修復

```bash
# 預覽模式（不實際修改）
python scripts/auto-fix-issues.py --dry-run

# 實際執行修復
python scripts/auto-fix-issues.py
```

### 3. CI/CD 自動化

每次 Push 或 Pull Request 時，GitHub Actions 會自動：
1. 執行安全掃描
2. 檢查 Python 程式碼品質
3. 檢查 TypeScript 程式碼品質
4. 檢測程式碼重複
5. 檢查 Docstring 覆蓋率
6. 執行測試並生成覆蓋率報告
7. 執行自動化品質檢查腳本
8. 生成綜合報告並發布到 PR

## 📋 檢查項目

### 自動化品質檢查 (auto-quality-check.py)

| 檢查項目 | 說明 | 狀態標準 |
|---------|------|---------|
| **安全性** | 掃描硬編碼秘密 | 無秘密 = ✅ |
| **Python 品質** | 型別提示覆蓋率 | ≥90% = ✅ |
| **TypeScript 品質** | 檔案統計 | - |
| **程式碼重複** | 檢測重複模組 | 無重複 = ✅ |
| **Docstring 覆蓋率** | 文件字串覆蓋 | ≥85% = ✅ |
| **非 ASCII 檔名** | 跨平台相容性 | 無非 ASCII = ✅ |
| **Console.log** | 結構化日誌 | 無 console.log = ✅ |
| **eval() 使用** | 安全性檢查 | 無 eval() = ✅ |

### 自動修復 (auto-fix-issues.py)

| 修復項目 | 說明 |
|---------|------|
| **程式碼格式化** | 使用 Black 格式化 Python 程式碼 |
| **Import 排序** | 使用 isort 排序 imports |
| **.gitignore** | 確保環境變數檔案不被提交 |
| **.env.example** | 建立環境變數範本 |

## 📊 報告格式

### JSON 報告 (auto-quality-report.json)

```json
{
  "timestamp": "2026-01-16T08:00:00",
  "summary": {
    "total_checks": 8,
    "passed": 5,
    "warnings": 3,
    "pass_rate": "62.5%"
  },
  "details": {
    "security": { ... },
    "python_quality": { ... },
    ...
  }
}
```

### Markdown 報告 (AUTO-QUALITY-REPORT.md)

人類可讀的報告，包含：
- 總覽統計
- 詳細結果
- 建議行動

## 🔧 設定

### 安裝依賴

```bash
# Python 工具
pip install detect-secrets bandit black ruff mypy isort pytest pytest-cov interrogate

# Node.js 工具（如果需要）
npm install -D eslint @typescript-eslint/eslint-plugin
```

### GitHub Actions 設定

工作流程會在以下情況自動執行：
- Pull Request 開啟、更新或重新開啟時
- Push 到 `main` 或 `develop` 分支時

## 📈 使用範例

### 範例 1: 每日品質檢查

```bash
#!/bin/bash
# daily-quality-check.sh

echo "執行每日品質檢查..."
python scripts/auto-quality-check.py

# 檢查通過率
PASS_RATE=$(jq -r '.summary.pass_rate' auto-quality-report.json | tr -d '%')

if (( $(echo "$PASS_RATE < 80" | bc -l) )); then
    echo "⚠️  警告：品質通過率低於 80%"
    exit 1
else
    echo "✅ 品質檢查通過"
fi
```

### 範例 2: Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "執行程式碼品質檢查..."
python scripts/auto-quality-check.py

# 執行自動修復
python scripts/auto-fix-issues.py
```

### 範例 3: 整合到 Makefile

```makefile
# Makefile

.PHONY: quality-check quality-fix

quality-check:
	@echo "執行品質檢查..."
	python scripts/auto-quality-check.py

quality-fix:
	@echo "執行自動修復..."
	python scripts/auto-fix-issues.py
	
quality-report:
	@echo "生成品質報告..."
	python scripts/auto-quality-check.py
	@cat AUTO-QUALITY-REPORT.md
```

## 🎯 與原始審查報告的對應

| 原始報告 | 自動化工具 |
|---------|-----------|
| PR-1-REVIEW-REPORT.md | auto-quality-check.py |
| PR-1-CODE-EXAMPLES.md | 參考範例（手動實作） |
| PR-1-ACTION-PLAN.md | GitHub Actions workflow |
| PR-1-REVIEW-SUMMARY.md | AUTO-QUALITY-REPORT.md |

## 🔄 持續改進

### 第 1 階段（當前）
- ✅ 自動檢查
- ✅ 基本自動修復
- ✅ CI/CD 整合

### 第 2 階段（計劃中）
- [ ] 自動生成修復 PR
- [ ] 更智能的型別提示生成
- [ ] 自動重構程式碼重複

### 第 3 階段（未來）
- [ ] AI 輔助程式碼審查
- [ ] 自動化測試生成
- [ ] 效能分析整合

## 💡 最佳實踐

1. **定期執行**: 建議每天或每週執行品質檢查
2. **先預覽**: 使用 `--dry-run` 預覽自動修復
3. **審查報告**: 仔細審查生成的報告，不要盲目接受所有建議
4. **漸進改善**: 逐步提升品質標準，不要一次設定過高門檻
5. **團隊協作**: 將報告分享給團隊，共同改進

## 📝 注意事項

⚠️ **自動修復限制**:
- 只修復格式化、排序等機械性問題
- 不會修改業務邏輯
- 不會自動添加型別提示或 docstrings（需要人工判斷）

⚠️ **檢查準確性**:
- 簡單的模式匹配可能有誤報
- 建議人工審查所有警告
- 某些檢查需要額外工具支援

## 🔗 相關資源

- [PR-1-REVIEW-REPORT.md](../PR-1-REVIEW-REPORT.md) - 完整審查報告
- [PR-1-CODE-EXAMPLES.md](../PR-1-CODE-EXAMPLES.md) - 程式碼範例
- [PR-1-ACTION-PLAN.md](../PR-1-ACTION-PLAN.md) - 執行計劃
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## 🆘 故障排除

### 問題: 找不到 detect-secrets

```bash
pip install detect-secrets
```

### 問題: GitHub Actions 權限錯誤

確保在 Repository Settings > Actions > General 中啟用：
- Allow GitHub Actions to create and approve pull requests
- Read and write permissions

### 問題: 報告路徑錯誤

確認在倉庫根目錄執行腳本：
```bash
cd /home/runner/work/mno-repository-understanding-system/mno-repository-understanding-system
python scripts/auto-quality-check.py
```

## 📧 回饋

如有問題或建議，請：
1. 提交 Issue
2. 在團隊會議討論
3. 更新此文件

---

**版本**: 1.0.0  
**建立日期**: 2026-01-16  
**維護者**: DevOps 團隊

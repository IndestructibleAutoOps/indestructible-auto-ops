# 自動化品質檢查報告

**生成時間**: 2026-01-16T08:58:28.095229

## 📊 總覽

- 總檢查項目: 8
- ✅ 通過: 2
- ⚠️ 警告: 6
- 通過率: 25.0%

## 📋 詳細結果

### Security

**狀態**: ⚠️ WARNING

- **secrets_detected**: True
- **details**: 請審查包含敏感關鍵字的檔案

### Python Quality

**狀態**: ⚠️ WARNING

- **total_files**: 1328
- **files_with_type_hints**: 883
- **type_hint_coverage**: 66.5%
- **target**: 90%

### Typescript Quality

**狀態**: ✅ PASS

- **total_ts_files**: 1128
- **total_js_files**: 40

### Code Duplication

**狀態**: ⚠️ WARNING

- **duplicates_found**: 1
- **details**: [{'pattern': 'dependency-manager', 'locations': ['workspace/teams/holy-grail/agents/services/dependency-manager', 'workspace/teams/holy-grail/agents/ai-experts/dependency-manager', 'workspace/src/ai/agents/dependency-manager', 'workspace/src/services/agents/dependency-manager']}]

### Docstring Coverage

**狀態**: ✅ PASS

- **total_files**: 1328
- **files_with_docstrings**: 1284
- **coverage**: 96.7%
- **target**: 85%

### Non Ascii Filenames

**狀態**: ⚠️ WARNING

- **count**: 7
- **files**: 7 項 (僅顯示部分)

### Console Logs

**狀態**: ⚠️ WARNING

- **count**: 79
- **files**: 20 項 (僅顯示部分)

### Eval Usage

**狀態**: ⚠️ WARNING

- **count**: 27
- **files**: 27 項 (僅顯示部分)

## 🎯 建議行動

1. **高優先級**: 審查並移除硬編碼的秘密
2. **高優先級**: 提升 Python 型別提示覆蓋率至 90%+
3. **高優先級**: 移除重複的程式碼模組
4. **中優先級**: 重新命名非 ASCII 檔名
5. **中優先級**: 替換 console.log 為結構化日誌

詳細改進計劃請參考: [PR-1-ACTION-PLAN.md](./PR-1-ACTION-PLAN.md)

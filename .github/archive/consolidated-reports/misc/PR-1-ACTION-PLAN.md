# PR #1 改進行動計劃

本文件提供 Pull Request #1 改進工作的具體執行計劃，包含優先級、時間線和負責人分配。

---

## 📋 計劃概覽

**目標**: 提升 machine-native-ops 程式碼庫品質至生產就緒水準  
**時間範圍**: 4 週（分 3 個階段）  
**關鍵指標**:
- 程式碼重複率: 15-20% → < 5%
- Python 型別提示覆蓋率: 59% → 90%+
- Docstring 覆蓋率: 64% → 85%+
- 測試覆蓋率: 未知 → 70%+
- 安全漏洞: 待審查 → 0 個嚴重漏洞

---

## 🚀 第一階段：緊急修復（第 1 週）

### P0 - 嚴重問題

#### 1.1 安全審查與修復
**優先級**: 🔴 P0  
**預估時間**: 2-3 天  
**負責人**: 安全團隊 + 後端工程師

**任務清單**:
- [ ] 執行完整的秘密掃描
  ```bash
  # 使用 detect-secrets
  pip install detect-secrets
  detect-secrets scan > .secrets.baseline
  detect-secrets audit .secrets.baseline
  
  # 使用 gitleaks
  docker run -v $(pwd):/path zricethezav/gitleaks:latest detect --source="/path" -v
  ```

- [ ] 審查 55+ 個包含敏感關鍵字的檔案
  - 建立審查清單：`workspace/config/integrations/*.py`
  - 逐一審查每個檔案
  - 記錄發現的問題

- [ ] 修復所有硬編碼的敏感資訊
  - 移至環境變數
  - 建立 `.env.example` 範本
  - 更新 `.gitignore` 確保 `.env` 不被提交

- [ ] 建立秘密管理指南
  - 文件化最佳實踐
  - 提供程式碼範例
  - 設定 CI 檢查

**驗收標準**:
- ✅ 所有硬編碼秘密已移除
- ✅ `.env.example` 已建立
- ✅ detect-secrets baseline 已設定
- ✅ CI 檢查已啟用

---

#### 1.2 移除中文檔名
**優先級**: 🔴 P0  
**預估時間**: 1 天  
**負責人**: DevOps 工程師

**任務清單**:
- [ ] 找出所有非 ASCII 檔名
  ```bash
  find . -name "*[^[:ascii:]]*" -type f > non-ascii-files.txt
  ```

- [ ] 建立重新命名計劃
  - 為每個檔案選擇適當的英文名稱
  - 檢查是否有引用

- [ ] 執行重新命名
  ```bash
  # 範例
  git mv 儲存.py storage.py
  git mv 配置.py configuration.py
  ```

- [ ] 更新所有引用
  - 搜尋並替換 import 語句
  - 更新文件引用

**驗收標準**:
- ✅ 無非 ASCII 檔名
- ✅ 所有引用已更新
- ✅ CI 通過

---

#### 1.3 建立 Pre-commit Hooks
**優先級**: 🔴 P0  
**預估時間**: 1 天  
**負責人**: DevOps 工程師

**任務清單**:
- [ ] 安裝 pre-commit
  ```bash
  pip install pre-commit
  ```

- [ ] 建立 `.pre-commit-config.yaml`（參考 PR-1-CODE-EXAMPLES.md）

- [ ] 設定 hooks
  ```bash
  pre-commit install
  pre-commit run --all-files  # 初次執行
  ```

- [ ] 更新 CI 以執行 pre-commit
  ```yaml
  # .github/workflows/pre-commit.yml
  name: Pre-commit checks
  on: [push, pull_request]
  jobs:
    pre-commit:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - uses: actions/setup-python@v5
        - uses: pre-commit/action@v3.0.0
  ```

**驗收標準**:
- ✅ Pre-commit hooks 已設定
- ✅ CI 檢查已啟用
- ✅ 團隊成員已培訓

---

## 🔧 第二階段：品質提升（第 2-3 週）

### P1 - 高優先級

#### 2.1 程式碼去重
**優先級**: 🟡 P1  
**預估時間**: 3-5 天  
**負責人**: 架構師 + 資深工程師

**任務清單**:
- [ ] 分析程式碼重複
  ```bash
  # 使用 jscpd (JavaScript/TypeScript)
  npx jscpd workspace/src/
  
  # 使用 pylint 的重複檢測 (Python)
  pylint --disable=all --enable=duplicate-code workspace/src/
  ```

- [ ] 識別主要重複模組
  - `dependency-manager/` (3+ 個副本)
  - `drone_system/` (重複)
  - 測試檔案 (多處重複)

- [ ] 建立去重計劃
  - 確定每個模組的規範位置
  - 規劃遷移路徑
  - 評估破壞性影響

- [ ] 執行去重
  - 保留規範版本
  - 刪除重複版本
  - 更新所有引用

- [ ] 建立符號連結或模組引用（如適用）

**驗收標準**:
- ✅ 程式碼重複率 < 5%
- ✅ 所有測試通過
- ✅ 文件已更新

---

#### 2.2 Python 型別提示覆蓋率提升
**優先級**: 🟡 P1  
**預估時間**: 5-7 天  
**負責人**: Python 團隊

**任務清單**:
- [ ] 設定 MyPy 嚴格模式
  ```toml
  # pyproject.toml
  [tool.mypy]
  python_version = "3.11"
  strict = true
  warn_return_any = true
  warn_unused_configs = true
  ```

- [ ] 使用 monkeytype 自動生成型別提示
  ```bash
  # 對主要模組執行
  monkeytype run workspace/src/namespace_registry/registry_manager.py
  monkeytype apply workspace.src.namespace_registry.registry_manager
  ```

- [ ] 手動補充複雜型別
  - 公開 API 優先
  - 核心模組次之
  - 工具腳本最後

- [ ] 階段性啟用 MyPy 檢查
  ```yaml
  # .github/workflows/mypy.yml
  - name: Type check with MyPy
    run: mypy workspace/src/ --strict
  ```

**驗收標準**:
- ✅ 型別提示覆蓋率 > 90%
- ✅ MyPy 無錯誤
- ✅ CI 檢查已啟用

---

#### 2.3 統一 Docstring 風格
**優先級**: 🟡 P1  
**預估時間**: 4-5 天  
**負責人**: 文件團隊 + 工程師

**任務清單**:
- [ ] 選擇 Docstring 風格（建議：Google Style）

- [ ] 更新 Ruff 設定
  ```toml
  # pyproject.toml
  [tool.ruff.pydocstyle]
  convention = "google"
  ```

- [ ] 使用工具自動格式化
  ```bash
  pip install pydocstringformatter
  pydocstringformatter --style google workspace/src/
  ```

- [ ] 手動補充缺失的 docstrings
  - 所有公開函式
  - 所有類別
  - 所有模組

- [ ] 建立 docstring 範本和指南

**驗收標準**:
- ✅ Docstring 覆蓋率 > 85%
- ✅ 風格統一（Google Style）
- ✅ Ruff 檢查通過

---

#### 2.4 替換 Console.log 為結構化日誌
**優先級**: 🟡 P1  
**預估時間**: 3-4 天  
**負責人**: 前端/後端團隊

**任務清單**:
- [ ] 設定 Winston logger (TypeScript)
  ```bash
  npm install winston
  ```
  - 建立 `src/utils/logger.ts`（參考 PR-1-CODE-EXAMPLES.md）
  - 設定不同環境的日誌等級

- [ ] 設定 Python logging
  - 建立 `src/utils/logging_config.py`
  - 設定 JSON formatter
  - 設定 file 和 console handlers

- [ ] 逐步替換 console.log
  ```bash
  # 找出所有 console.log
  grep -r "console.log" workspace/src/ --include="*.ts" --include="*.js"
  ```

- [ ] 更新 ESLint 規則
  ```javascript
  rules: {
    'no-console': 'error',  // 從 warn 改為 error
  }
  ```

**驗收標準**:
- ✅ 無 console.log 在生產程式碼中
- ✅ 結構化日誌已實作
- ✅ ESLint 檢查通過

---

#### 2.5 審查並替換 eval() 使用
**優先級**: 🟡 P1  
**預估時間**: 2-3 天  
**負責人**: 安全團隊 + 資深工程師

**任務清單**:
- [ ] 找出所有 eval() 使用
  ```bash
  grep -r "eval(" workspace/src/ --include="*.py" --include="*.ts" --include="*.js"
  ```

- [ ] 審查每個使用情境
  - 記錄用途
  - 評估安全風險
  - 確定替代方案

- [ ] 實作安全替代方案
  - Python: 使用 `ast.literal_eval` 或 SafePolicyEvaluator（參考範例）
  - TypeScript: 使用解析器或安全沙箱

- [ ] 添加安全測試
  - 測試惡意輸入
  - 驗證沙箱限制

**驗收標準**:
- ✅ 所有 eval() 已審查
- ✅ 不安全使用已替換
- ✅ 安全測試已添加

---

## 📈 第三階段：持續改進（第 4 週）

### P2 - 中等優先級

#### 3.1 提升測試覆蓋率
**優先級**: 🟡 P2  
**預估時間**: 持續進行  
**負責人**: QA 團隊 + 工程師

**任務清單**:
- [ ] 設定 coverage 報告
  ```bash
  # Python
  pytest --cov=workspace/src --cov-report=html --cov-report=term
  
  # TypeScript
  npm test -- --coverage
  ```

- [ ] 識別低覆蓋率模組
  ```bash
  # 產生報告
  pytest --cov=workspace/src --cov-report=html
  # 檢視 htmlcov/index.html
  ```

- [ ] 為核心模組補充測試
  - `namespace_registry`
  - `governance_layer`
  - `policy_engine`

- [ ] 設定 CI 覆蓋率門檻
  ```yaml
  # .github/workflows/test.yml
  - name: Run tests with coverage
    run: pytest --cov=workspace/src --cov-fail-under=70
  ```

**驗收標準**:
- ✅ 整體覆蓋率 > 70%
- ✅ 核心模組覆蓋率 > 80%
- ✅ CI 檢查已啟用

---

#### 3.2 統一命名規範
**優先級**: 🟡 P2  
**預估時間**: 2-3 天  
**負責人**: 架構師

**任務清單**:
- [ ] 啟用 Ruff 命名檢查
  ```toml
  # pyproject.toml
  [tool.ruff]
  select = ["N"]  # 命名規則
  ```

- [ ] 找出不符合規範的命名
  ```bash
  ruff check --select N workspace/src/
  ```

- [ ] 建立重構計劃
  - 評估影響範圍
  - 規劃遷移路徑

- [ ] 執行自動重構（謹慎使用）
  ```bash
  ruff check --select N --fix workspace/src/
  ```

- [ ] 手動修正複雜情況

**驗收標準**:
- ✅ 命名符合 PEP 8 規範
- ✅ Ruff 檢查通過
- ✅ 所有測試通過

---

#### 3.3 TypeScript 回傳型別註解
**優先級**: 🟡 P2  
**預估時間**: 2-3 天  
**負責人**: 前端團隊

**任務清單**:
- [ ] 啟用 ESLint 規則
  ```javascript
  rules: {
    '@typescript-eslint/explicit-function-return-type': 'error',
  }
  ```

- [ ] 為所有公開函式添加回傳型別
  ```typescript
  // 重點關注
  // - src/services/
  // - src/api/
  // - src/utils/
  ```

- [ ] 修正 ESLint 錯誤
  ```bash
  npm run lint -- --fix
  ```

**驗收標準**:
- ✅ 所有公開函式有明確回傳型別
- ✅ ESLint 無錯誤
- ✅ TypeScript 編譯無警告

---

#### 3.4 整合重複文件
**優先級**: 🟢 P3  
**預估時間**: 2 天  
**負責人**: 文件團隊

**任務清單**:
- [ ] 找出重複文件
  ```bash
  find . -name "TODO.md" -o -name "README.md"
  ```

- [ ] 建立文件結構
  ```
  docs/
  ├── README.md (主要文件)
  ├── architecture/
  ├── guides/
  │   ├── development.md
  │   ├── deployment.md
  │   └── contributing.md
  ├── api/
  └── decisions/ (ADRs)
  ```

- [ ] 合併重複內容
  - 保留最新、最完整的版本
  - 移除過時資訊

- [ ] 建立文件索引

**驗收標準**:
- ✅ 無重複文件
- ✅ 文件結構清晰
- ✅ 索引已建立

---

## 📊 進度追蹤

### 第 1 週檢查點
- [ ] 安全審查完成
- [ ] 中文檔名移除
- [ ] Pre-commit hooks 設定

### 第 2 週檢查點
- [ ] 程式碼去重完成
- [ ] 型別提示 > 80%
- [ ] Console.log 替換 50%+

### 第 3 週檢查點
- [ ] Docstring 統一
- [ ] eval() 審查完成
- [ ] 測試覆蓋率 > 60%

### 第 4 週檢查點
- [ ] 測試覆蓋率 > 70%
- [ ] 命名規範統一
- [ ] 文件整合完成

---

## 🎯 成功指標

### 量化指標
| 指標 | 基線 | 目標 | 當前 |
|------|------|------|------|
| 程式碼重複率 | 15-20% | < 5% | - |
| Python 型別提示 | 59% | 90% | - |
| Docstring 覆蓋 | 64% | 85% | - |
| 測試覆蓋率 | 未知 | 70% | - |
| 安全漏洞 | 待審查 | 0 嚴重 | - |
| ESLint 錯誤 | 未知 | 0 | - |
| MyPy 錯誤 | 未知 | 0 | - |

### 質化指標
- [ ] 所有 CI 檢查通過
- [ ] 程式碼審查流程建立
- [ ] 團隊培訓完成
- [ ] 文件完整且最新
- [ ] 安全最佳實踐落實

---

## 🔄 持續改進流程

### 每週例會
- **時間**: 每週五 14:00-15:00
- **參與者**: 技術負責人、團隊代表
- **議程**:
  1. 回顧本週進度
  2. 討論遇到的問題
  3. 調整下週計劃

### 程式碼審查流程
1. 所有 PR 必須通過 CI 檢查
2. 至少 1 位資深工程師審查
3. 安全相關變更需安全團隊審查
4. 合併前執行完整測試

### 品質門檻
- ✅ Pre-commit hooks 通過
- ✅ ESLint/Ruff 無錯誤
- ✅ MyPy 型別檢查通過
- ✅ 測試覆蓋率不降低
- ✅ Security scan 無嚴重漏洞

---

## 📝 風險與緩解策略

### 風險 1: 大規模重構影響穩定性
**緩解策略**:
- 分階段執行，每次變更範圍小
- 每個階段都有完整測試
- 保留回滾計劃
- 在分支上驗證後再合併

### 風險 2: 時程延遲
**緩解策略**:
- 優先處理 P0 項目
- P2/P3 項目可延後
- 每週檢查進度，及時調整

### 風險 3: 團隊學習曲線
**緩解策略**:
- 提供充分培訓
- 建立詳細文件
- 配對程式設計
- 知識分享會議

---

## 📚 參考資源

### 內部文件
- [PR-1-REVIEW-REPORT.md](./PR-1-REVIEW-REPORT.md) - 詳細審查報告
- [PR-1-CODE-EXAMPLES.md](./PR-1-CODE-EXAMPLES.md) - 程式碼範例

### 外部資源
- [PEP 8 - Python 編碼規範](https://peps.python.org/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [TypeScript Deep Dive](https://basarat.gitbook.io/typescript/)
- [12 Factor App](https://12factor.net/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

### 工具文件
- [Black Documentation](https://black.readthedocs.io/)
- [Ruff Documentation](https://beta.ruff.rs/docs/)
- [MyPy Documentation](https://mypy.readthedocs.io/)
- [ESLint Rules](https://eslint.org/docs/rules/)
- [Winston Logger](https://github.com/winstonjs/winston)
- [Pytest Documentation](https://docs.pytest.org/)

---

## ✅ 完成檢查清單

### 第一階段完成標準
- [ ] 所有 P0 項目完成
- [ ] CI 基礎設施建立
- [ ] 無嚴重安全漏洞
- [ ] 團隊已接受培訓

### 第二階段完成標準
- [ ] 所有 P1 項目完成
- [ ] 程式碼品質指標達標 (80%)
- [ ] 文件完整性 > 80%

### 第三階段完成標準
- [ ] 所有 P2 項目完成
- [ ] 程式碼品質指標達標 (100%)
- [ ] 持續改進流程建立

### 專案完成標準
- [ ] 所有量化指標達成
- [ ] 所有質化指標達成
- [ ] 程式碼審查流程運作順暢
- [ ] 團隊對新流程熟悉

---

**計劃版本**: 1.0.0  
**建立日期**: 2026-01-16  
**負責人**: 技術負責人  
**狀態**: 📋 待執行

**下次更新**: 每週五

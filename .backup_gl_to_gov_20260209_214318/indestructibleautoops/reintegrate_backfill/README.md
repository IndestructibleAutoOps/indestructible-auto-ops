# IndestructibleAutoOps Reintegrate Backfill System

## 概述 (Overview)

此系統自動化處理舊分支的回填整合流程，確保所有更改都遵循最佳實踐的 Gate 檢查。

## 核心特性 (Core Features)

- ✅ **自動發現與排序**: 根據 merge-base 時間從最舊到最新排序分支
- ✅ **智能選擇**: 每個 family 自動選擇最佳候選分支
- ✅ **多維度評分**: CI 狀態、rebase 清潔度、測試通過率等
- ✅ **完整審計證據**: 所有操作都產生 JSON 報告和日誌
- ✅ **可回滾**: 支持未合併 PR 的清理和工作分支刪除

## 目錄結構 (Directory Structure)

```
indestructibleautoops/reintegrate_backfill/
├── README.md                          # 本文件
├── README.runbook.yaml                # 系統規格說明
├── config.yaml                        # 操作配置
├── PROMPT_FULL_MACHINE_ENGINEERING.txt # AI 提示詞
├── templates/
│   └── pr_body.txt                    # PR 內容模板
├── scripts/
│   ├── _lib.sh                        # 共用函數庫
│   ├── discover_rank_select.py        # 分支發現與排序
│   ├── preflight_main_latest.sh       # 預檢查腳本
│   ├── try_rebase_and_test.sh         # 測試候選分支
│   ├── backfill_execute.sh            # 主執行腳本
│   └── verify_post_merge.sh           # 合併後驗證
└── agent_prompt/
    └── IndestructibleAutoOps_Agents_Preflight_Backfill.prompt.txt
```

## 使用方式 (Usage)

### 前置需求 (Prerequisites)

1. **必要工具**:
   - `git` - Git 版本控制
   - `gh` - GitHub CLI
   - `python3` - Python 3.x
   - `PyYAML` - Python YAML 解析器

2. **Git 狀態**:
   - 工作樹必須乾淨 (no uncommitted changes)
   - main 分支必須是最新的

### 基本執行 (Basic Execution)

```bash
# 1. 執行 backfill 流程
bash indestructibleautoops/reintegrate_backfill/scripts/backfill_execute.sh

# 2. 驗證合併狀態
bash indestructibleautoops/reintegrate_backfill/scripts/verify_post_merge.sh
```

### 自訂配置 (Configuration)

編輯 `config.yaml` 來調整行為：

```yaml
# 分支發現規則
discovery:
  include_patterns:
    - "^cursor/.*"
    - "^feature/.*"
  exclude_patterns:
    - "^main$"
    - "^release/.*"

# 評分權重
selection:
  score_weights:
    ci_green: 60        # CI 通過的權重
    rebase_clean: 30    # Rebase 乾淨的權重
    conflicts: -120     # 衝突的懲罰
    staleness_days: -0.2 # 陳舊天數的懲罰

# 執行模式
execution:
  mode: rebase_then_merge_pr  # 或 squash_pr
  auto_merge: true
  test_command: ""  # 可選：例如 "make test"
```

## 輸出報告 (Output Reports)

所有執行證據都儲存在 `.evidence/reintegrate_backfill/`:

```
.evidence/reintegrate_backfill/
├── reports/
│   ├── discovery.json      # 發現的所有分支
│   ├── ranking.json        # 排序後的分支列表
│   ├── selection.json      # 選擇的候選分支
│   ├── result.json         # 執行結果
│   └── verify.json         # 驗證結果
└── logs/
    ├── commands.log        # 所有命令記錄
    ├── git.log            # Git 操作日誌
    └── gh.log             # GitHub CLI 日誌
```

## 工作流程 (Workflow)

```
1. Preflight Check
   ├─ 確保工作樹乾淨
   ├─ Fetch 所有遠端分支
   └─ 更新 main 到最新

2. Discovery & Ranking
   ├─ 掃描遠端分支
   ├─ 按 merge-base 時間排序
   ├─ 計算 diff 統計
   └─ 查詢 CI 狀態

3. Selection
   ├─ 依 family prefix 分組
   ├─ 每組選擇最高分候選
   └─ 過濾低於閾值的分支

4. Trial Execution
   ├─ 嘗試 rebase 到 main
   ├─ 可選：執行測試命令
   └─ 記錄結果

5. PR Creation
   ├─ 創建工作分支
   ├─ 推送到遠端
   ├─ 建立 PR
   └─ 可選：自動合併

6. Verification
   └─ 檢查 PR 狀態
```

## 評分系統 (Scoring System)

分支評分基於以下因素：

| 因素 | 權重 | 說明 |
|-----|------|------|
| ci_green | +60 | CI 所有檢查通過 |
| rebase_clean | +30 | Rebase 無衝突 |
| test_pass | +30 | 測試通過 |
| conflicts | -120 | 有合併衝突 |
| ahead_commits | +0.02 | 領先 main 的提交數 |
| changed_files | -0.05 | 變更的檔案數 |
| diffstat_lines | -0.001 | 變更的行數 |
| staleness_days | -0.2 | 分支陳舊天數 |

## 回滾操作 (Rollback)

如果需要撤銷操作：

```bash
# 關閉未合併的 PR 並刪除分支
gh pr close <PR_NUMBER> --delete-branch

# 刪除已推送的工作分支
git push origin :reintegrate-backfill/<branch-name>
```

## 故障排除 (Troubleshooting)

### 常見錯誤

1. **dirty_worktree**: 工作樹有未提交的更改
   ```bash
   git status
   git stash  # 或 git commit
   ```

2. **missing_binary**: 缺少必要工具
   ```bash
   # 安裝 GitHub CLI
   brew install gh  # macOS
   # 或參考: https://cli.github.com/
   ```

3. **rebase_conflict**: Rebase 衝突
   - 系統會自動跳過有衝突的分支
   - 檢查 logs/git.log 了解詳情

## 最佳實踐 (Best Practices)

1. **定期執行**: 建議每週或每兩週執行一次
2. **測試閘門**: 生產環境建議設定 `test_command`
3. **審查報告**: 執行後檢查 `.evidence/` 目錄的報告
4. **手動驗證**: 重要變更建議人工審查 PR 內容

## 支援 (Support)

如有問題或建議，請查閱：
- 配置文件: `config.yaml`
- 系統規格: `README.runbook.yaml`
- 日誌文件: `.evidence/reintegrate_backfill/logs/`

## 版本 (Version)

- **系統版本**: 1.0
- **最後更新**: 2026-02-07

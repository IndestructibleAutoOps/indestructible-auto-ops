# 深度研究：專案目錄與文檔合併計畫

## 目標
- 盤點並整合分散的目錄與文檔，建立單一權威工作空間。
- 消除重複/平行結構，降低維運成本並保持 GL 治理合規。
- 與既有計畫（如 `PLATFORM-CONSOLIDATION-PLAN.md`、`docs/plans/docs-reorganization-plan.md`、`config/environments/documentation-manifest.yaml`）對齊，避免重複發散。

## 現況洞察（重點目錄與文檔分佈）
- **活躍工作區**：`indestructibleautoops/`、`iaops/`、`machinenativeops/`（三套工作空間並存，需確立單一主幹並給出映射/歸檔策略）。
- **平台/年代分支**：`platforms/`、`ng-era1-platforms/`、`ng-era2-platforms/`、`ng-era3-platforms/`、`ng-cross-era-platforms/`（同一平台族群跨多代保留，須明確「現行 → 歸檔」路徑）。
- **命名差異目錄**：`IndestructibleAutoOps/`（大寫工單/補救檔案集） vs `indestructibleautoops/`（治理/回填工作流），需決定歸併方向與引用更新。
- **治理與執行**：`governance/`、`ecosystem/`（強制執行入口已集中到 namespace-governance-boundary）、`scripts/`、`tools/`（需保留單一入口並將舊路徑標記為受控遺留）。
- **文檔分散**：根目錄大量狀態/報告類 MD（`*_COMPLETE.md`, `*_REPORT.md`, `*_SUMMARY.md`），同時 `docs/` 已有 plans/analysis/reports 結構與文檔清單（`docs/plans/docs-reorganization-plan.md`）。需一次性收斂。

## 目錄映射表（初版）
| Source | Target | Action | Status |
| --- | --- | --- | --- |
| `IndestructibleAutoOps/` | `indestructibleautoops/` | 合併/歸檔，統一小寫入口 | Planned |
| `indestructibleautoops/` | `machinenativeops/` | 建立主幹映射（治理/回填同步） | Planned |
| `iaops/` | `machinenativeops/iaops/` (只讀) | 轉為受控遺留或文檔化接口 | Planned |
| `machinenativeops/` | `machinenativeops/` | 保持主幹（含 gov-runtime-engine） | In progress |
| `ng-era*-platforms/`、`ng-cross-era-platforms/` | `platforms/` (GL00-99 分層) | 按年代計畫收斂，遺留歸檔到 `archives/platforms/` | Planned |
| `governance/`、`ecosystem/` | 保留原位 | 唯一強制執行/治理入口 | Locked |

## 文檔搬遷映射（按優先級）
| Source (root) | Target | Rationale | Status |
| --- | --- | --- | --- |
| `PLATFORM-CONSOLIDATION-EXECUTION-REPORT.md` | `docs/reports/platform-consolidation-execution-report.md` | 平台整合報告應集中於 reports | Done |
| `ABSOLUTE-ZERO-TOLERANCE-ACHIEVED.md` | `docs/reports/absolute-zero-tolerance-achieved.md` | 減少根目錄雜訊並改善命名 | Done |
| `execution-plan.md` | `docs/plans/execution-plan.md` | 計畫類文檔集中於 plans | Pending |
| `radical-dependency-elimination-plan.md` | `docs/plans/radical-dependency-elimination-plan.md` | 跟隨重組計畫 | Pending |
| `PHASE*_COMPLETION_REPORT.md` | `docs/phases/` (保留原檔名或建立索引頁) | 階段報告集中化，後續更新索引 | Planned |

## 命名修正（批次切入點）
| Offending/legacy name | Target naming | Note |
| --- | --- | --- |
| `PLATFORM-CONSOLIDATION-EXECUTION-REPORT.md` | `platform-consolidation-execution-report.md` | 已搬至 `docs/reports/` |
| `ABSOLUTE-ZERO-TOLERANCE-ACHIEVED.md` | `absolute-zero-tolerance-achieved.md` | 已搬至 `docs/reports/` |
| `PHASE*_COMPLETION_REPORT.md` | `phase*-completion-report.md` (或索引聚合) | 後續批次處理，需更新引用 |

## 合併路線圖（階段化）
### Phase 1：盤點與護欄
- 以最新 `actual-tree-structure.txt`、`DIRECTORY-STRUCTURE-VERIFICATION.md` 為基準，補齊目錄 → 目標的映射表（含「保留/合併/歸檔」標記）。
- 用 `config/environments/documentation-manifest.yaml` 校對文檔索引，列出根目錄孤立/重複文檔。
- 鎖定強制執行入口：`python ecosystem/enforce.py`（已確認指向 `governance/l3_execution/boundaries/namespace-governance-boundary/implementation/ecosystem/enforce.py`）。

### Phase 2：目錄整併（優先序）
1. **命名一致性**：將 `IndestructibleAutoOps/` 內容對齊/合併到小寫主幹（或歸檔到 `archives/`），並更新引用。
2. **工作空間主幹**：選定 `machinenativeops/` 為主幹（含 gov-runtime-engine 平台)，將 `indestructibleautoops/`、`iaops/` 形成映射表（保留子模組或歸檔到 `archives/legacy-workspaces/`），保持 GL 邊界不變。
3. **平台代際收斂**：依 `PLATFORM-CONSOLIDATION-PLAN.md` 將 `ng-era*-platforms`、`ng-cross-era-platforms` 梳理到 `platforms/` 標準層級（GL00-99 分層），遺留版本移入 `archives/platforms/` 並保留只讀指標。
4. **治理與工具集中**：保留 `governance/` + `ecosystem/` 作為唯一強制執行/驗證入口；將平行腳本集中到 `scripts/` 或標記為遺留（`scripts-legacy/`），在說明文件中列出受控入口。

### Phase 3：文檔整合
- 依 `docs/plans/docs-reorganization-plan.md` 將根目錄報告/狀態類文檔移入 `docs/reports/`、`docs/plans/`、`docs/analysis/`，並同步更新 `documentation-manifest.yaml`。
- 合併重複主題報告（多個 *_COMPLETE/REPORT/SUMMARY），保留單一權威版本，其他移入 `docs/archive/`，在同一頁列出來源鏈接。
- 在 `GOVERNANCE-INDEX.md` / `ROOT-GOVERNANCE-MAP.md` 加入新索引鏈接，確保導航不依賴舊路徑。

### Phase 4：驗證與收尾
- 強制執行：`python ecosystem/enforce.py`；命名/路徑變更後再次運行。
- 目錄對齊：使用 `DIRECTORY-STRUCTURE-VERIFICATION.md` 和 `platform-directory-structure-best-practices.md` 的檢查清單做交叉驗證。
- 文檔對齊：更新 `config/environments/documentation-manifest.yaml`，確保所有移動後的檔案被索引；檢查死鏈。
- 產出最終報告：在 `docs/reports/` 保存合併完成報告（包含映射表與驗證結果）。

## 成功驗收標準
- 單一主幹工作空間明確（其餘目錄標記為受控遺留或歸檔），平台代際目錄完成搬遷。
- 根目錄僅保留核心/入口文檔；其他文檔均落在 `docs/` 既有結構並被 manifest 索引。
- 強制執行、目錄驗證、文檔索引檢查全部通過且無新的命名/路徑衝突。

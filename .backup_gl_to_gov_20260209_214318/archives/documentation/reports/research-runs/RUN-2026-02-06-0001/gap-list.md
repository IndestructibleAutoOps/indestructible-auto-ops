---
run_id: RUN-2026-02-06-0001
stage: A_INTERNAL_BASELINE
status: open
---

# Gap List（缺口清單）

## G0：本次 run 的關鍵缺口（阻擋命名映射與整合）
- **G0.1 草案正文缺失（Blocker）**
  - 需要：`docs/drafts/architecture-implement-draft.md`
  - 用途：抽取命名空間、規格、規則、依賴、路由訊號、目錄契約
  - 沒有它：無法做「名稱映射需要更改」的實質修正

- **G0.2 IndestructibleAutoOps 規範本體缺失（Blocker）**
  - 需要：你們專案定義的命名規範、rule registry、waiver schema、merge policy（repo 內路徑或貼文）
  - 沒有它：我無法“嚴格遵守專案所定義規範”而不自創規則

## G1：為了四階段流程可機器化，仍需補齊的材料
- **G1.1 Workflow 定義檔**
  - 需要：`governance/workflows/research-loop/workflow.yaml` 與 `gates.yaml`
  - 目的：讓 CI / hook 能強制「工作前必跑」

- **G1.2 離線引用基線（REF-Pack）**
  - 需要：`governance/references/registry.yaml`（至少先有 1~3 個 REF）
  - 目的：將“最佳實踐”具體化為可離線審核的引用

- **G1.3 命名映射格式定稿**
  - 需要：`governance/schemas/naming-map.schema.json`（若你們有既定 schema 更好）
  - 目的：讓 `outputs/naming-map.json` 可被工具驗證與套用

## G2：可選（若放寬外網）才需要的材料
- **G2.1 Egress 拓樸與隔離導入流程**
  - 需要：是「隔離區導入快照」或「封閉區受控代理」的明確選型
  - 目的：把外網結果導入 `references/snapshots/` 並產生 hash/provenance

- **G2.2 信源評分模型（離線）**
  - 需要：source scoring 規則（authority、recency、cross-check）
  - 目的：全球檢索的去偽存真可稽核

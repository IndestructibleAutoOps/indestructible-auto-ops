---
run_id: RUN-2026-02-06-0001
status: draft-skeleton
depends_on:
  - "docs/drafts/architecture-implement-draft.md"
  - "governance/* (policies, schemas, mapping, roles, router)"
---

# Architecture Plan（架構落地計畫 - 骨架）

## 目標
- 在零外網依賴下，建立「研究循環」作為工作前必跑流程，並把其產物對接到：
  - 自動白名單（waiver）治理
  - 命名映射修正（rename/canonical mapping）
  - 角色路由與 IDE 自適應編輯器層

## 交付物（MVP）
- `reports/research-runs/<run_id>/`：標準化 run 產物（intake/gap/synthesis/outputs）
- `governance/workflows/research-loop/`：workflow + gate + templates + schemas
- `tools/`：本機與 CI 可執行的：
  - run 初始化（init）
  - schema 驗證（validate）
  - 產物彙整（synthesize）
  - 產 PR 任務（emit-pr-plan）

## 實作分解（按四階段）
### A 內網啟動（必跑）
- 抽取來源：
  - repo docs（ADR/RFC/drafts）
  - governance policies/schemas/mapping
  - 近期 PR/commit metadata（若允許）
- 產出：
  - gap-list（缺口）
  - evidence/internal.jsonl（證據條目）
  - router inputs（供角色路由）

### B 外網深化（可選，需 gate）
- 僅允許「導入快照」策略：外部資料 → snapshots → registry → hash/provenance
- 產出：
  - evidence/external.jsonl（每條對應 REF-ID）

### C 全球拓展（可選，需更嚴 gate）
- 多信源交叉驗證，必須能落到 REF-ID
- 產出：
  - evidence/global.jsonl（每條對應 REF-ID + cross-check 指標）

### D 綜合推理（必跑）
- 產出：
  - synthesis.md（結論 + 決策）
  - naming-map.json（映射草案）
  - architecture-plan 更新（從骨架→定案）

## Gate 與稽核
- 所有出網必須留下：
  - gate 批准紀錄（meta/gates.json）
  - 導入 provenance（references/provenance）
  - hash（references/digests）
---
run_id: RUN-2026-02-06-0001
status: draft-skeleton
depends_on:
  - "docs/drafts/architecture-implement-draft.md"
  - "governance/* (policies, schemas, mapping, roles, router)"
---

# Architecture Plan（架構落地計畫 - 骨架）

## 目標
- 在零外網依賴下，建立「研究循環」作為工作前必跑流程，並把其產物對接到：
  - 自動白名單（waiver）治理
  - 命名映射修正（rename/canonical mapping）
  - 角色路由與 IDE 自適應編輯器層

## 交付物（MVP）
- `reports/research-runs/<run_id>/`：標準化 run 產物（intake/gap/synthesis/outputs）
- `governance/workflows/research-loop/`：workflow + gate + templates + schemas
- `tools/`：本機與 CI 可執行的：
  - run 初始化（init）
  - schema 驗證（validate）
  - 產物彙整（synthesize）
  - 產 PR 任務（emit-pr-plan）

## 實作分解（按四階段）
### A 內網啟動（必跑）
- 抽取來源：
  - repo docs（ADR/RFC/drafts）
  - governance policies/schemas/mapping
  - 近期 PR/commit metadata（若允許）
- 產出：
  - gap-list（缺口）
  - evidence/internal.jsonl（證據條目）
  - router inputs（供角色路由）

### B 外網深化（可選，需 gate）
- 僅允許「導入快照」策略：外部資料 → snapshots → registry → hash/provenance
- 產出：
  - evidence/external.jsonl（每條對應 REF-ID）

### C 全球拓展（可選，需更嚴 gate）
- 多信源交叉驗證，必須能落到 REF-ID
- 產出：
  - evidence/global.jsonl（每條對應 REF-ID + cross-check 指標）

### D 綜合推理（必跑）
- 產出：
  - synthesis.md（結論 + 決策）
  - naming-map.json（映射草案）
  - architecture-plan 更新（從骨架→定案）

## Gate 與稽核
- 所有出網必須留下：
  - gate 批准紀錄（meta/gates.json）
  - 導入 provenance（references/provenance）
  - hash（references/digests）

# 高級多代理研究系統 (Advanced Multi-Agent Research System)

本系統旨在升級現有的代理架構，支援 20 個並行任務的高強度研究、專業網站部署以及幻燈片生成。

## 核心架構

系統採用 **Wide Research (平行處理)** 模式，將複雜的研究主題拆解為多個子任務，並由不同的專業代理並行執行。

### 1. 代理角色定義

| 代理名稱 | 職責 | 工具 |
| :--- | :--- | :--- |
| **Research Coordinator** | 任務拆解、進度控管、結果彙整 | `parallel_processing`, `search` |
| **Domain Researcher** | 針對特定子主題進行深度研究 | `search`, `read`, `browse` |
| **Web Architect** | 負責專業網站的結構設計與部署 | `web_development`, `shell` |
| **Presentation Specialist** | 負責將研究成果轉化為高品質幻燈片 | `slides_content_writing`, `slides_generation` |
| **Quality Auditor** | 確保研究內容符合 GL Governance 標準 | `read`, `edit` |

### 2. 並行處理流程 (20 並行任務)

1. **拆解 (Decomposition)**: Coordinator 將主題拆解為 20 個獨立的研究維度。
2. **執行 (Execution)**: 20 個 Domain Researcher 實例並行運作，收集數據與事實。
3. **彙整 (Synthesis)**: Coordinator 整合所有研究結果，形成完整報告。
4. **產出 (Output)**:
   - **網站**: Web Architect 部署互動式研究報告網站。
   - **幻燈片**: Presentation Specialist 生成結構清晰的 PPT。

## 部署與整合

- **網站部署**: 使用 Vite + React + TailwindCSS 進行靜態或動態部署。
- **幻燈片**: 支援 HTML (Chart.js) 與 Image (Nano Banana) 模式。
- **治理**: 所有產出必須通過 `gl-governance` 代理的審核。

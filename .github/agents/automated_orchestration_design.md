# 全自動化代理調度系統設計 (Automated Agent Orchestration Design)

本設計旨在實現「任務驅動」的代理自動選擇與套用，消除人工干預。

## 核心組件

### 1. 代理路由 (Agent Router)
- **功能**：分析輸入的「研究主題」或「任務描述」。
- **邏輯**：提取關鍵詞（如：市場分析、技術架構、部署、PPT），並與代理定義中的 `description` 和 `tools` 進行語義匹配。

### 2. 動態配置器 (Dynamic Configurator)
- **功能**：根據路由結果，自動生成代理執行鏈。
- **範例**：若任務包含「部署」，則自動將 `Web Architect` 加入工作流。

### 3. 自動化執行引擎 (Auto-Execution Engine)
- **功能**：驅動 `Research Coordinator` 啟動 20 個並行任務，並在完成後自動觸發後續的網站部署與幻燈片生成。

## 工作流程

1. **觸發**：使用者提交一個 Issue 或在特定目錄建立 Markdown 檔案。
2. **分析**：`Agent Selector` 掃描任務內容。
3. **調度**：
   - 啟動 `Research Coordinator` 進行 20 路並行研究。
   - 研究完成後，自動將結果傳遞給 `Web Architect` 進行網站構建。
   - 同時傳遞給 `Presentation Specialist` 生成幻燈片。
4. **驗證**：`Quality Auditor` 自動審核所有產出。
5. **交付**：自動在 GitHub PR 或 Issue 中回覆結果連結。

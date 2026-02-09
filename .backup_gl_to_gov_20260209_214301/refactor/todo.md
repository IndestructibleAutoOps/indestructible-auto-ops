# 治理系統重構任務清單

## 階段 1: 基礎架構構建 ✅ 已完成
- [x] 創建 todo.md 任務追蹤
- [x] 備份與驗證
- [x] 工具準備（白名單管理器、重構執行器）
- [x] 文檔準備（當前結構、目標結構、遷移映射）
- [x] 創建 feature 分支：refactor/governance-standardization

## 階段 2: 根層目錄重構 ✅ 已完成
- [x] 整合 18 個 responsibility-* 目錄
- [x] 整合 enterprise-governance 目錄
- [x] 整合 .governance 目錄（白名單跳過）
- [x] 清理根層目錄

**成果**:
- 根層目錄從 35 減少到 17（減少 51%）
- 2,443 個文件成功重新組織
- L0-L4 治理層級結構建立完成

## 階段 3: 命名規範統一
- [ ] 實施 16 種命名規範
- [ ] 統一前綴為 gov-
- [ ] 創建自動修復工具

## 階段 4: L0-L4 治理架構構建
- [ ] 實現 L0 Semantic Root
- [ ] 實現 L1 Governance Core
- [ ] 實現 L2 Governance Domains
- [ ] 實現 L3 Governance Execution
- [ ] 實現 L4 Governance Evidence
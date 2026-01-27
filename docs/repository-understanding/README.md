# Repository Understanding System - 文檔中心

## 📚 概述

本目錄包含 Repository Understanding System 的完整文檔，該系統從 [superninja-repository-understanding-system](https://github.com/MachineNativeOps/superninja-repository-understanding-system) 整合而來。

## 📖 文檔索引

### 核心系統文檔

1. **[FINAL_SYSTEM_DOCUMENTATION.md](FINAL_SYSTEM_DOCUMENTATION.md)**
   - 完整的系統文檔
   - 系統架構和組件
   - 部署和管理指南
   - 性能指標和故障排除
   - **推薦首先閱讀**

2. **[AUTOMATED_REPOSITORY_UNDERSTANDING_SYSTEM.md](AUTOMATED_REPOSITORY_UNDERSTANDING_SYSTEM.md)**
   - 自動化系統指南（中文）
   - 四階段系統詳細說明
   - 使用方式和最佳實踐
   - 集成到工作流程的方法

### 系統狀態和報告

3. **[EVENT_DRIVEN_SYSTEM_STATUS.md](EVENT_DRIVEN_SYSTEM_STATUS.md)**
   - 事件驅動系統當前狀態
   - 系統健康監控
   - 運行時數據

4. **[PHASES_COMPLETION_SUMMARY.md](PHASES_COMPLETION_SUMMARY.md)**
   - 四階段完成總結
   - 系統開發進度
   - 功能驗證報告

### 階段報告

5. **[phase1_report.md](phase1_report.md)**
   - 第一階段：儲存庫掃描和知識庫建立
   - 掃描結果和統計

6. **[phase2_report.md](phase2_report.md)**
   - 第二階段：操作前的檢查機制
   - 檢查結果和風險評估

7. **[phase3_report.md](phase3_report.md)**
   - 第三階段：視覺化與查詢系統
   - 查詢功能和示例

8. **[phase4_report.md](phase4_report.md)**
   - 第四階段：持續學習機制
   - 學習結果和最佳實踐

### 計劃和設計文檔

9. **[DUPLICATE_PATHS_INTEGRATION_PLAN.md](DUPLICATE_PATHS_INTEGRATION_PLAN.md)**
   - 重複路徑整合與合併計劃
   - 目錄結構優化策略

10. **[solution_proposal.md](solution_proposal.md)**
    - 解決方案提案
    - 系統設計理念

11. **[repository_mapping_plan.md](repository_mapping_plan.md)**
    - 儲存庫映射計劃
    - 目錄結構設計

### 工作清單和待辦事項

12. **[operation_checklist.md](operation_checklist.md)**
    - 操作檢查清單
    - 必要的操作步驟

13. **[repo_understanding_todo.md](repo_understanding_todo.md)**
    - 儲存庫理解系統待辦事項
    - 未來改進計劃

14. **[todo.md](todo.md)**
    - 一般待辦事項
    - 系統增強計劃

## 🚀 快速開始

### 1. 閱讀順序建議

對於新用戶，建議按以下順序閱讀文檔：

1. **FINAL_SYSTEM_DOCUMENTATION.md** - 了解整體架構
2. **AUTOMATED_REPOSITORY_UNDERSTANDING_SYSTEM.md** - 了解使用方式
3. **phase1_report.md** 到 **phase4_report.md** - 了解各階段詳情
4. **EVENT_DRIVEN_SYSTEM_STATUS.md** - 了解系統狀態

### 2. 系統文件位置

- **Python 腳本**: `workspace/tools/repository-understanding/`
- **Shell 腳本**: `scripts/repository-understanding/`
- **Systemd 服務**: `etc/systemd/event-driven-system.service`
- **文檔**: `docs/repository-understanding/` (本目錄)

### 3. 基本使用

```bash
# 切換到工具目錄
cd workspace/tools/repository-understanding

# 執行第一階段掃描
python3 phase1_scanner.py

# 或使用一鍵腳本執行所有階段
bash ../../scripts/repository-understanding/run_all_phases.sh
```

## 📊 四階段系統概覽

### Phase 1: 儲存庫掃描和知識庫建立
- 自動掃描所有目錄和檔案
- 建立完整的知識庫
- 生成掃描報告

### Phase 2: 操作前的檢查機制
- 驗證操作安全性
- 評估風險等級
- 提供操作建議

### Phase 3: 視覺化與查詢系統
- 多維度查詢功能
- 檔案和目錄關係可視化
- 統計分析

### Phase 4: 持續學習機制
- 從操作中學習
- 自動更新知識庫
- 生成最佳實踐

## 🔄 事件驅動系統

### 自動化功能
- 持續監控檔案系統變化
- 自動觸發維護任務
- 自我修復能力
- 實時狀態報告

### 管理命令

```bash
# 啟動系統
bash scripts/repository-understanding/start_event_driven.sh

# 檢查狀態
bash scripts/repository-understanding/status_event_driven.sh

# 查看日誌
bash scripts/repository-understanding/logs_event_driven.sh

# 停止系統
bash scripts/repository-understanding/stop_event_driven.sh

# 重啟系統
bash scripts/repository-understanding/restart_event_driven.sh
```

## 🛠️ 生產環境部署

### Systemd 服務安裝

```bash
# 編輯服務文件，更新路徑和用戶
vim etc/systemd/event-driven-system.service

# 複製到系統目錄
sudo cp etc/systemd/event-driven-system.service /etc/systemd/system/

# 重新加載 systemd
sudo systemctl daemon-reload

# 啟用服務
sudo systemctl enable event-driven-system.service

# 啟動服務
sudo systemctl start event-driven-system.service

# 檢查狀態
sudo systemctl status event-driven-system.service
```

## 📈 系統性能

- **CPU 使用率**: 3-5%
- **記憶體使用**: ~50MB
- **磁碟使用**: ~20MB
- **事件處理延遲**: <1秒
- **正常運行時間**: 99.9%+

## 🔍 故障排除

### 常見問題

1. **無法找到知識庫**
   ```bash
   cd workspace/tools/repository-understanding
   python3 phase1_scanner.py
   ```

2. **腳本權限問題**
   ```bash
   chmod +x scripts/repository-understanding/*.sh
   ```

3. **Python 依賴缺失**
   ```bash
   cd workspace/tools/repository-understanding
   pip install -r requirements-test.txt
   ```

## 📞 獲取幫助

### 文檔資源
- 查看本目錄中的各個文檔文件
- 閱讀 `workspace/tools/repository-understanding/README.md`

### 系統檢查
```bash
# 運行基本測試
cd workspace/tools/repository-understanding
python3 phase1_scanner.py

# 檢查系統狀態
bash ../../scripts/repository-understanding/status_event_driven.sh
```

## 🔗 相關資源

### 原始儲存庫
- https://github.com/MachineNativeOps/superninja-repository-understanding-system

### 相關工具
- `workspace/tools/repository-understanding/` - Python 腳本
- `scripts/repository-understanding/` - Shell 腳本
- `etc/systemd/` - 系統服務配置

## 📝 版本歷史

### v1.0.0 (2025-01-16)
- ✅ 從 superninja-repository-understanding-system 整合完成
- ✅ 更新所有路徑以適應新的目錄結構
- ✅ 完善文檔和使用指南
- ✅ 系統測試和驗證

---

**文檔版本**: v1.0.0  
**最後更新**: 2025-01-16  
**維護者**: MachineNativeOps Team  
**狀態**: ✅ 已完成整合

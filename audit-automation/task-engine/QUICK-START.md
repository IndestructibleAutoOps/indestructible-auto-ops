# ⚡ Auto Task Project - 快速開始指南

## 🎯 3 步驟啟動（60 秒）

### 步驟 1: 安裝 (20秒)
```bash
cd auto_task_project
pip install -e .
```

### 步驟 2: 配置 (10秒)
```bash
cp .env.example .env
# 可選：編輯 .env 修改配置
```

### 步驟 3: 啟動 (30秒)
```bash
python main.py
```

✅ **完成！系統已啟動！**

---

## 📋 當前已載入任務（14個）

```
[P1] 每日備份             每天 2:00 AM
[P2] CPU監控              每 5 分鐘
[P2] 註冊表備份           每天 3:00 AM
[P3] 發送報表             每週一 9:00 AM
[P3] 服務註冊表管理       每小時
[P3] 語義驅動執行         每天 12:00 PM
[P4] 平台註冊表管理       每天 10:00 AM
[P4] 角色執行器           每 2 小時
[P4] 註冊表驗證           每天 8:00 AM
[P5] 數據目錄管理         每天 11:00 AM
[P5] 工具註冊表更新       每 6 小時
[P6] 命名規範註冊表       每天 9:00 AM
[P6] 註冊表同步           每 12 小時
[P8] 清理暫存             每小時
```

---

## ⚡ 常用操作

### 測試框架
```bash
python test_framework.py
```

### 驗證完整性
```bash
python verify_complete.py
```

### 查看日誌
```bash
tail -f logs/auto_task.log
```

### 查看註冊表
```bash
# 工具註冊表
cat tasks/registries/tools-registry.json | head -20

# 平台註冊表
cat tasks/registries/platform-registry.yaml | head -20
```

---

## 🆕 新增任務（3 分鐘）

### 範本

創建 `tasks/task_新功能.py`:

```python
from auto_executor import Task, executor
import logging

logger = logging.getLogger(__name__)


class MyNewTask(Task):
    """新功能描述"""
    
    name = "新功能任務"
    priority = 5  # 1=最高, 10=最低
    
    def execute(self):
        """執行邏輯"""
        logger.info("🎯 開始執行新功能...")
        
        # 你的代碼
        
        logger.info("✅ 新功能執行完成")


# 註冊任務
# 選項 1: Cron 排程
executor.register(MyNewTask, cron="0 10 * * *", priority=5)

# 選項 2: 間隔排程
# executor.register(MyNewTask, interval=3600, priority=5)

# 選項 3: 混合排程
# executor.register(MyNewTask, cron="0 2 * * *", interval=3600, priority=5)
```

重啟 `main.py` → 完成！

---

## 📞 快速參考

### Cron 表達式
```
分 時 日 月 週
*  *  *  *  *
```

常用:
- `0 2 * * *` - 每天 2 AM
- `0 9 * * MON` - 每週一 9 AM
- `*/5 * * * *` - 每 5 分鐘
- `0 */6 * * *` - 每 6 小時

### 優先級指南
- **1-2**: 關鍵業務（備份、監控）
- **3-4**: 重要操作（報表、驗證）
- **5-6**: 一般維護（更新、同步）
- **7-10**: 低優先級（清理、優化）

### 事件使用
```python
from event_bus import event_bus

# 觸發事件
event_bus.emit("my_event", data="value")

# 監聽事件
def my_handler(data):
    print(f"收到: {data}")

event_bus.on("my_event", my_handler)
```

---

## 🔧 故障排除

### 任務未執行？
```bash
# 1. 檢查是否已註冊
python test_framework.py

# 2. 查看日誌
grep "ERROR" logs/auto_task.log
```

### 註冊表錯誤？
```bash
# 1. 驗證格式
python -m json.tool tasks/registries/tools-registry.json

# 2. 運行驗證任務
python -c "
from tasks.task_註冊表驗證 import RegistryValidationTask
task = RegistryValidationTask()
task.execute()
"
```

### 查看系統狀態
```bash
# 檢查進程
ps aux | grep "python main.py"

# 檢查磁碟
du -sh logs/ backups/ tasks/registries/

# 查看最近日誌
tail -50 logs/auto_task.log
```

---

## 📚 完整文檔

- **README.md** - 詳細使用指南
- **TASKS-OVERVIEW.md** - 所有任務清單
- **DEPLOYMENT-GUIDE.md** - 生產部署
- **REGISTRY-MIGRATION-REPORT.md** - 技術細節
- **FINAL-SUMMARY.md** - 專案總結

---

## ✅ 驗證檢查清單

運行 `python verify_complete.py` 應該看到:

```
✅ 目錄結構
✅ 任務系統
✅ 註冊表數據
✅ 文檔系統
✅ 事件系統

🎉 所有驗證通過！專案完整無誤！
```

---

## 🎊 完成！

**你現在擁有一個完整的、生產級的、可擴展的自動任務執行框架！**

🚀 **開始使用**: `python main.py`  
📖 **查看文檔**: `cat README.md`  
🧪 **運行測試**: `python verify_complete.py`

**享受零痛點的擴展體驗！** ✨

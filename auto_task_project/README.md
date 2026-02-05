# Auto Task Project - 2026 工程標準

> **自動任務執行框架**：APScheduler + 事件系統 + 優先級 + 日誌旋轉

## ✨ 特性

- ✅ **自動任務發現**：只要在 `tasks/` 新增 `task_xxx.py` 即生效
- ✅ **優先級執行**：啟動時按優先級 1-10 依序執行
- ✅ **多種排程**：支援 cron 表達式 + 間隔秒數
- ✅ **事件系統**：任務間可透過 EventBus 通訊
- ✅ **日誌旋轉**：自動寫入 `logs/auto_task.log`（10MB 輪替）
- ✅ **2026 標準**：ruff + black + isort 配置完整

## 📦 安裝

```bash
# 1. 進入專案目錄
cd auto_task_project

# 2. 安裝依賴（可編輯模式）
pip install -e .

# 3. 複製配置檔案
cp .env.example .env
```

## 🚀 使用方式

### 啟動系統

```bash
python main.py
```

輸出範例：
```
2026-02-05 23:59:00 | INFO     | __main__ | 🔍 自動發現任務：tasks/
2026-02-05 23:59:00 | INFO     | __main__ | 🚀 開始執行 4 個任務...
2026-02-05 23:59:00 | INFO     | __main__ | ▶️  執行：每日備份 [優先級=1]
✅ 系統完全啟動（APScheduler + 事件 + 優先級 + 日誌寫檔案）
   Ctrl+C 結束
```

### 新增任務

1. 在 `tasks/` 創建 `task_新功能.py`：

```python
from auto_executor import Task, executor
import logging

logger = logging.getLogger(__name__)

class MyNewTask(Task):
    name = "新功能任務"
    priority = 5
    
    def execute(self):
        logger.info("執行新功能...")
        # 你的邏輯

# 註冊：每 30 分鐘執行
executor.register(MyNewTask, interval=1800, priority=5)
```

2. 重啟 `main.py` 即生效（零修改根目錄）

### 使用事件系統

```python
from event_bus import event_bus

# 任務 A 觸發事件
event_bus.emit("data_ready", data={"key": "value"})

# 任務 B 監聽事件
def on_data_ready(data):
    print(f"收到數據：{data}")

event_bus.on("data_ready", on_data_ready)
```

## 📁 目錄結構

```
auto_task_project/
├── pyproject.toml          # 依賴 + ruff/black 配置
├── main.py                 # 總入口（永遠不改）
├── auto_executor.py        # 核心執行器
├── scheduler.py            # APScheduler 排程
├── event_bus.py            # 事件系統
├── logger.py               # 日誌管理
├── config.py               # 配置管理
├── tasks/                  # ← 所有任務放這裡
│   ├── task_每日備份.py
│   ├── task_發送報表.py
│   ├── task_清理暫存.py
│   └── task_監控CPU警報.py
├── utils/                  # 工具函數
├── models/                 # 數據模型
├── api/                    # Webhook API（可選）
└── logs/                   # 日誌輸出
    └── auto_task.log
```

## 🔧 配置說明

### pyproject.toml

- **依賴管理**：apscheduler、python-dotenv
- **代碼規範**：ruff（行長 100）、black、isort

### .env

```env
BACKUP_PATH=./backup
REPORT_EMAIL=admin@example.com
LOG_LEVEL=INFO
```

## 📝 任務範例

### 1. Cron 排程（每天凌晨 2 點）

```python
executor.register(DailyBackupTask, cron="0 2 * * *", priority=1)
```

### 2. 間隔排程（每小時）

```python
executor.register(CleanTempTask, interval=3600, priority=8)
```

### 3. 混合排程

```python
executor.register(
    MyTask,
    interval=300,    # 每 5 分鐘
    cron="0 9 * * MON",  # 同時每週一 9 點
    priority=3
)
```

## 🎯 優先級說明

- **1-3**：高優先級（備份、監控、安全）
- **4-6**：中優先級（報表、通知）
- **7-10**：低優先級（清理、優化）

啟動時按優先級 1→10 依序執行一次，之後由 APScheduler 按排程執行。

## 🔍 進階功能

### 自定義事件處理

```python
# 在任務中觸發事件
from event_bus import event_bus

class MyTask(Task):
    def execute(self):
        result = do_something()
        event_bus.emit("task_complete", result=result)

# 在其他地方監聽
event_bus.on("task_complete", lambda r: print(f"完成：{r}"))
```

### 日誌查看

```bash
# 即時查看
tail -f logs/auto_task.log

# 查看最近錯誤
grep "ERROR" logs/auto_task.log
```

## 🛠️ 開發規範

### 代碼檢查

```bash
# 自動格式化
ruff check . --fix
black .

# 排序 import
isort .
```

### 新增依賴

編輯 `pyproject.toml`：

```toml
dependencies = [
    "apscheduler>=3.10",
    "python-dotenv>=1.0",
    "requests>=2.31",  # 新增
]
```

然後重新安裝：
```bash
pip install -e .
```

## 📊 性能優化

- 日誌自動旋轉（10MB × 5 份）
- 背景排程器（不阻塞主線程）
- 優先級隊列（啟動時依序執行）

## 🔒 最佳實踐

1. **任務命名**：`task_xxx.py` 格式
2. **優先級分配**：備份=1, 監控=2, 報表=3, 清理=8
3. **錯誤處理**：每個 task 內加 try-except
4. **日誌記錄**：使用 `logger.info/warning/error`
5. **配置外部化**：敏感信息放 `.env`

## 📄 授權

MIT License

---

**最終定讞版本 - 2026 工程標準**  
命名規範 ✓ | 模組拆分 ✓ | 擴展性 ✓

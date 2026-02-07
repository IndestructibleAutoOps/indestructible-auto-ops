# Auto Task Project - 部署指南

## 快速部署（3 步驟）

### 步驟 1: 安裝

```bash
cd auto_task_project
pip install -e .
```

安裝的依賴:
- `apscheduler>=3.10` - 任務排程
- `python-dotenv>=1.0` - 環境變數管理

### 步驟 2: 配置

```bash
# 複製環境變數範本
cp .env.example .env

# 編輯配置（可選）
nano .env
```

預設配置:
```env
BACKUP_PATH=./backup
REPORT_EMAIL=admin@example.com
LOG_LEVEL=INFO
```

### 步驟 3: 啟動

```bash
python main.py
```

預期輸出:
```
2026-02-06 00:10:00 | INFO | 🔍 自動發現任務：tasks/
2026-02-06 00:10:00 | INFO | ✅ 註冊任務：DailyBackupTask [優先級=1]
2026-02-06 00:10:00 | INFO | ✅ 註冊任務：CpuMonitorTask [優先級=2]
...
2026-02-06 00:10:00 | INFO | 🚀 開始執行 14 個任務...
✅ 系統完全啟動（APScheduler + 事件 + 優先級 + 日誌寫檔案）
   Ctrl+C 結束
```

## 生產環境部署

### 使用 systemd (推薦)

創建服務文件 `/etc/systemd/system/auto-task.service`:

```ini
[Unit]
Description=Auto Task Project - 自動任務執行框架
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/workspace/auto_task_project
ExecStart=/usr/bin/python3 main.py
Restart=always
RestartSec=10

Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target
```

啟用服務:
```bash
sudo systemctl daemon-reload
sudo systemctl enable auto-task
sudo systemctl start auto-task
sudo systemctl status auto-task
```

查看日誌:
```bash
sudo journalctl -u auto-task -f
```

### 使用 Docker

創建 `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml .
COPY . .

RUN pip install -e .

CMD ["python", "main.py"]
```

構建和運行:
```bash
docker build -t auto-task-project .
docker run -d --name auto-task \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/.env:/app/.env \
  auto-task-project
```

### 使用 Supervisor

創建配置文件 `/etc/supervisor/conf.d/auto-task.conf`:

```ini
[program:auto-task]
command=/usr/bin/python3 main.py
directory=/workspace/auto_task_project
user=ubuntu
autostart=true
autorestart=true
stderr_logfile=/var/log/auto-task.err.log
stdout_logfile=/var/log/auto-task.out.log
```

重載 supervisor:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start auto-task
```

## 監控和維護

### 查看日誌

```bash
# 即時查看
tail -f logs/auto_task.log

# 查看今天的日誌
grep "$(date +%Y-%m-%d)" logs/auto_task.log

# 查看錯誤
grep "ERROR" logs/auto_task.log

# 查看特定任務
grep "平台註冊表" logs/auto_task.log
```

### 檢查任務狀態

```bash
# 快速測試
python test_framework.py

# 手動執行單個任務
python -c "
from tasks.task_平台註冊表管理 import PlatformRegistryTask
task = PlatformRegistryTask()
task.execute()
"
```

### 備份管理

自動備份位置: `backups/registries/YYYYMMDD_HHMMSS/`

手動備份:
```bash
# 手動觸發備份任務
python -c "
from tasks.task_註冊表備份 import RegistryBackupTask
task = RegistryBackupTask()
task.execute()
"

# 查看備份
ls -lh backups/registries/
```

### 性能監控

```bash
# CPU 和記憶體使用
ps aux | grep "python main.py"

# 磁碟使用
du -sh logs/ backups/ tasks/registries/

# 任務執行統計（從日誌）
grep "✅ 完成" logs/auto_task.log | wc -l
```

## 常見問題

### Q1: 如何停止系統？

**方式 1**: Ctrl+C (前台運行)
**方式 2**: `sudo systemctl stop auto-task` (systemd)
**方式 3**: `docker stop auto-task` (Docker)

### Q2: 如何新增任務？

1. 在 `tasks/` 創建 `task_新功能.py`
2. 繼承 `Task` 類
3. 實作 `execute()` 方法
4. 最後一行註冊: `executor.register(YourTask, ...)`
5. 重啟系統

### Q3: 如何修改任務排程？

編輯任務文件最後的註冊行:
```python
# Cron 排程
executor.register(MyTask, cron="0 10 * * *", priority=5)

# 間隔排程
executor.register(MyTask, interval=3600, priority=5)

# 混合排程
executor.register(MyTask, cron="0 2 * * *", interval=3600, priority=5)
```

### Q4: 如何查看註冊表數據？

```bash
# JSON 註冊表
cat tasks/registries/tools-registry.json | jq .

# YAML 註冊表
cat tasks/registries/platform-registry.yaml

# 使用 Python
python -c "
import json
with open('tasks/registries/tools-registry.json') as f:
    data = json.load(f)
    print(f\"工具數: {len(data.get('tools', []))}\")
"
```

### Q5: 如何恢復備份？

```bash
# 查看可用備份
ls -lht backups/registries/

# 恢復最新備份
cp -r backups/registries/20260206_030000/* tasks/registries/

# 重啟系統
python main.py
```

## 故障排除

### 任務未執行

1. 檢查日誌: `grep "ERROR" logs/auto_task.log`
2. 驗證任務已註冊: `python test_framework.py`
3. 檢查排程配置: 查看任務文件最後的 `executor.register()`

### 註冊表載入失敗

1. 驗證 YAML/JSON 格式: `python -m json.tool file.json`
2. 檢查文件權限: `ls -la tasks/registries/`
3. 查看詳細錯誤: `tail -100 logs/auto_task.log`

### 記憶體使用過高

1. 調整日誌旋轉大小（logger.py）
2. 增加備份清理頻率（task_註冊表備份.py）
3. 減少任務執行頻率

## 效能優化

### 調整日誌設定

編輯 `logger.py`:
```python
file_handler = RotatingFileHandler(
    "logs/auto_task.log",
    maxBytes=5 * 1024 * 1024,  # 改為 5MB
    backupCount=3               # 只保留 3 份
)
```

### 調整任務優先級

優先級指南:
- **1-2**: 關鍵業務（備份、監控）
- **3-4**: 重要操作（報表、驗證）
- **5-6**: 一般維護（更新、同步）
- **7-10**: 低優先級（清理、優化）

### 調整排程頻率

根據實際需求調整:
```python
# 開發環境 - 更頻繁測試
executor.register(MyTask, interval=60, priority=5)  # 每分鐘

# 生產環境 - 降低頻率
executor.register(MyTask, interval=3600, priority=5)  # 每小時
```

## 安全建議

1. **敏感配置**: 使用 `.env` 文件，不要提交到 Git
2. **日誌權限**: 限制 logs/ 目錄訪問權限
3. **備份加密**: 考慮加密備份數據
4. **網路隔離**: 如使用 API 模組，配置防火牆
5. **定期審計**: 檢查 logs/ 中的異常活動

## 升級指南

### 升級依賴

```bash
# 查看當前版本
pip list | grep apscheduler

# 升級到最新版本
pip install --upgrade apscheduler python-dotenv

# 重新安裝專案
pip install -e .
```

### 升級任務

1. 備份當前配置: `cp -r tasks/ tasks.backup/`
2. 修改任務文件
3. 測試: `python test_framework.py`
4. 重啟系統

## 開發工作流

### 本地開發

```bash
# 1. Clone 專案
git clone <repo>
cd auto_task_project

# 2. 創建虛擬環境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. 安裝開發依賴
pip install -e .
pip install ruff black isort

# 4. 開發新任務
nano tasks/task_新功能.py

# 5. 測試
python test_framework.py

# 6. 運行
python main.py
```

### 代碼品質檢查

```bash
# 格式化代碼
black tasks/
isort tasks/

# Lint 檢查
ruff check tasks/

# 自動修復
ruff check tasks/ --fix
```

## 附錄

### Cron 表達式參考

```
* * * * *
│ │ │ │ │
│ │ │ │ └─ 星期幾 (0-7, 0和7都是週日)
│ │ │ └─── 月份 (1-12)
│ │ └───── 日期 (1-31)
│ └─────── 小時 (0-23)
└───────── 分鐘 (0-59)
```

常用範例:
- `0 2 * * *` - 每天 2:00 AM
- `0 */6 * * *` - 每 6 小時
- `0 9 * * MON` - 每週一 9:00 AM
- `*/5 * * * *` - 每 5 分鐘

### 優先級策略

根據業務重要性和時效性分配:

| 優先級 | 類型 | 範例 |
|--------|------|------|
| 1 | 關鍵備份 | 每日備份 |
| 2 | 即時監控 | CPU/記憶體監控、註冊表備份 |
| 3 | 重要業務 | 報表、服務管理、語義執行 |
| 4 | 日常維護 | 平台管理、驗證、角色執行 |
| 5 | 定期更新 | 工具更新、數據目錄 |
| 6 | 後台同步 | 命名檢查、數據同步 |
| 7-10 | 清理優化 | 暫存清理、日誌壓縮 |

---

**版本**: 1.0.0  
**最後更新**: 2026-02-06  
**維護者**: Auto Task Project Team

"""配置管理模組"""

import os
from dotenv import load_dotenv

load_dotenv()

BACKUP_PATH = os.getenv("BACKUP_PATH", "./backup")
REPORT_EMAIL = os.getenv("REPORT_EMAIL", "admin@example.com")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: documentation
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
# 安全與可觀測性 - 不可越界的邊界

## ⚠️ 禁止操作

### ❌ 禁止 1: 在程式碼中硬編碼敏感資訊

```python
# ❌ 不允許
API_KEY = "sk_prod_abc123"
PASSWORD = "admin123"

# ✅ 允許
from config import secrets_vault
API_KEY = secrets_vault.get("api-key")
```

### ❌ 禁止 2: 繞過安全檢查

```python
# ❌ 不允許：跳過 SLSA 驗證
artifact = load_artifact(path, skip_verification=True)

# ✅ 允許：始終驗證
artifact = load_artifact(path, verify=True)
```

### ❌ 禁止 3: 監控盲點

所有生產路徑必須有監控覆蓋。

### ❌ 禁止 4: 日誌中包含敏感資訊

```python
# ❌ 不允許
logger.info(f"User {username} password {password}")

# ✅ 允許
logger.info(f"User {username} authenticated")
```

## 🚫 安全紅線

1. **未授權訪問**：所有資源訪問必須經過授權
2. **資訊洩露**：敏感資訊不應出現在日誌或錯誤消息中
3. **完整性破壞**：所有構件必須簽名且可驗證

## 檢查清單

- [ ] 所有敏感資訊是否已隱藏？
- [ ] 是否啟用了 SLSA 驗證？
- [ ] 監控是否覆蓋所有關鍵路徑？
- [ ] 告警是否配置正確？
- [ ] 日誌是否可追蹤和不可篡改？

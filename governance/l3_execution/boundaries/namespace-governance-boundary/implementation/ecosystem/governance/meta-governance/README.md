# Meta-Governance Framework

元治理框架 - 驗證器規範的治理系統

**GL Governance Layer**: GL90-99 (Meta-Specification Layer)  
**Version**: 1.0.0  
**Status**: Active

---

## 📋 概述

Meta-Governance 框架提供了完整的治理規範系統，包括：

1. **版本管理** - 語義化版本控制
2. **變更流程** - 標準化變更管理
3. **審查機制** - 三層審查流程
4. **依賴管理** - 依賴關係追蹤和驗證
5. **生命周期** - 從設計到歸檔的完整管理
6. **責任界定** - RASCI 模型

---

## 🎯 核心概念

### 語義化版本（SemVer）

```
版本格式：MAJOR.MINOR.PATCH

MAJOR：破壞性變更（接口不兼容）
MINOR：向後兼容的功能新增
PATCH：向後兼容的缺陷修復

示例：v2.1.3
- 主版本：2（第二代架構）
- 次版本：1（新增1個功能）
- 修訂號：3（3個bug修復）
```

### 變更流程

```
變更提案 → 初步評估 → 影響分析 → 審查 → 實施 → 測試 → 發布
```

### 審查機制

三層審查：
1. **技術合規** - 開發團隊
2. **架構設計** - 架構委員會
3. **業務驗證** - 領域專家

### RASCI 責任模型

- **R** (Responsible) - 負責人
- **A** (Accountable) - 審批者
- **S** (Support) - 執行者
- **C** (Consult) - 顧問
- **I** (Inform) - 知會者

---

## 🚀 使用方式

### 版本管理

```python
from meta_governance import VersionManager

vm = VersionManager()

# 創建新版本
version = vm.create_version(
    component='validator-core',
    version_type='minor',  # major, minor, patch
    changes=['Added new validation rule'],
    breaking_changes=[]
)

# 驗證版本
result = vm.validate_version(version)
```

### 變更管理

```python
from meta_governance import ChangeManager

cm = ChangeManager()

# 提交變更提案
change_id = cm.submit_change(
    title='Add OAuth2 support',
    description='Implement OAuth2 authentication',
    impact_level='medium',  # low, medium, high, critical
    affected_components=['api-gateway', 'authenticator']
)

# 評估變更
assessment = cm.assess_change(change_id)

# 執行變更
cm.execute_change(change_id)
```

### 審查流程

```python
from meta_governance import ReviewManager

rm = ReviewManager()

# 創建審查
review_id = rm.create_review(
    change_id=change_id,
    reviewers=['tech-lead', 'architect', 'domain-expert']
)

# 提交審查意見
rm.submit_review(review_id, reviewer='tech-lead', approved=True)

# 檢查審查狀態
status = rm.get_review_status(review_id)
```

---

## 📚 治理規範

詳細規範請參閱：
- [版本管理規範](docs/VERSION_MANAGEMENT.md)
- [變更流程規範](docs/CHANGE_PROCESS.md)
- [審查機制規範](docs/REVIEW_MECHANISM.md)
- [依賴管理規範](docs/DEPENDENCY_MANAGEMENT.md)

---

**GL Compliance**: Yes  
**Layer**: GL90-99 (Meta-Specification)  
**Status**: Active

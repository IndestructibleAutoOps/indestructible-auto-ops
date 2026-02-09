# 文件路徑驗證報告

## 驗證日期
2025-01-20

## 驗證目標
驗證所有註冊表中的文件路徑是否正確，文件是否實際存在於指定位置。

---

## 驗證結果

### 1. ecosystem/registry/naming/gov-naming-contracts-registry.yaml

#### 註冊的契約路徑檢查

| 契約ID | 註冊路徑 | 實際存在 | 狀態 |
|--------|---------|---------|------|
| gov-naming-ontology | ecosystem/contracts/naming-governance/gov-naming-ontology.yaml | ❌ | 不存在 |
| gov-platforms | ecosystem/contracts/platforms/gov-platforms.yaml | ❌ | 不存在 |
| gov-platform-definition | ecosystem/registry/platforms/gov-platform-definition.yaml | ✅ | 存在 |
| gov-platform-index | ecosystem/registry/platforms/gov-platforms.index.yaml | ✅ | 存在 |
| gov-placement-rules | ecosystem/registry/platforms/gov-platforms.placement-rules.yaml | ✅ | 存在 |
| gov-platform-validator | ecosystem/registry/platforms/gov-platforms.validator.rego | ✅ | 存在 |
| gov-platform-lifecycle | ecosystem/registry/platforms/gov-platform-lifecycle-spec.yaml | ✅ | 存在 |
| gov-validation-rules | ecosystem/contracts/validation/gov-validation-rules.yaml | ❌ | 不存在 |
| gov-extension-points | ecosystem/contracts/extensions/gov-extension-points.yaml | ❌ | 不存在 |
| gov-governance-layers | ecosystem/contracts/governance/gov-governance-layers.yaml | ❌ | 不存在 |
| gov-generator-spec | ecosystem/contracts/generator/gov-generator-spec.yaml | ❌ | 不存在 |
| gov-reasoning-rules | ecosystem/contracts/reasoning/gov-reasoning-rules.yaml | ❌ | 不存在 |

#### 統計
- **總契約數**: 12
- **存在的契約**: 5 (41.7%)
- **不存在的契約**: 7 (58.3%)

---

## 問題分析

### 問題 1: 路徑不一致
**描述**: 註冊表中的路徑與實際文件位置不一致

**例子**:
- 註冊路徑: `ecosystem/contracts/naming-governance/gov-naming-ontology.yaml`
- 實際位置: 可能不存在或位置不同

### 問題 2: 缺失的契約文件
**描述**: 許多契約文件在註冊表中列出，但實際不存在

**缺失的文件**:
1. gov-naming-ontology.yaml
2. gov-platforms.yaml
3. gov-validation-rules.yaml
4. gov-extension-points.yaml
5. gov-governance-layers.yaml
6. gov-generator-spec.yaml
7. gov-reasoning-rules.yaml

---

## 建議的解決方案

### 方案 A: 創建缺失的契約文件
1. 在 `ecosystem/contracts/` 目錄下創建缺失的文件
2. 根據命名契約註冊表的定義填充內容
3. 確保所有路徑正確

### 方案 B: 更新註冊表路徑
1. 更新註冊表中的路徑，指向實際存在的文件
2. 確保所有註冊的路徑都有效
3. 重新驗證

### 方案 C: 移除不存在的契約
1. 從註冊表中移除不存在的契約
2. 更新依賴關係
3. 重新生成註冊表

---

## 當前存在的文件

### ecosystem/registry/platforms/
✅ gov-platform-definition.yaml  
✅ gov-platform-lifecycle-spec.yaml  
✅ gov-platforms.index.yaml  
✅ gov-platforms.placement-rules.yaml  
✅ gov-platforms.validator.rego  

### ecosystem/registry/naming/
✅ gov-naming-contracts-registry.yaml  

---

## 建議的目錄結構

```
ecosystem/
├── contracts/
│   ├── naming-governance/
│   │   └── gov-naming-ontology.yaml
│   ├── platforms/
│   │   └── gov-platforms.yaml
│   ├── validation/
│   │   └── gov-validation-rules.yaml
│   ├── extensions/
│   │   └── gov-extension-points.yaml
│   ├── governance/
│   │   └── gov-governance-layers.yaml
│   ├── generator/
│   │   └── gov-generator-spec.yaml
│   └── reasoning/
│       └── gov-reasoning-rules.yaml
└── registry/
    ├── naming/
    │   └── gov-naming-contracts-registry.yaml
    └── platforms/
        ├── gov-platform-definition.yaml
        ├── gov-platform-lifecycle-spec.yaml
        ├── gov-platforms.index.yaml
        ├── gov-platforms.placement-rules.yaml
        └── gov-platforms.validator.rego
```

---

## 下一步行動

1. **創建缺失的契約文件** (推薦)
   - 優先創建核心契約：gov-naming-ontology.yaml
   - 創建平台命名契約：gov-platforms.yaml
   - 創建驗證規則契約：gov-validation-rules.yaml

2. **驗證路徑正確性**
   - 檢查所有註冊的路徑
   - 確保文件存在於正確位置

3. **更新文檔**
   - 更新所有相關文檔
   - 確保一致性

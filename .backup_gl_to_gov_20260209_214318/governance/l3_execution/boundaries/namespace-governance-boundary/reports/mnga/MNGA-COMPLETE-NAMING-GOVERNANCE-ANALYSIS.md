# MNGA 完整命名治理體系分析報告

**報告日期**: 2026-02-03  
**分析範圍**: machine-native-ops 儲存庫  
**分析目的**: 識別命名治理規範與實際執行之間的差距

---

## 執行摘要

### 🔴 關鍵發現

**統一命名治理契約** (`unified-naming-governance-contract.yaml`) 定義了 **16 種命名規範**，但當前的 `enforce.py` **只實現了 2 種**（目錄命名和文件命名的基本檢查）。

| 狀態 | 數量 | 說明 |
|------|------|------|
| ✅ 已實現 | 2 | 目錄命名、文件命名（基本） |
| ❌ 未實現 | 14 | API、服務、端口、標籤、路徑等 |
| 📊 覆蓋率 | 12.5% | 嚴重不足 |

---

## 1. 命名治理規範完整清單

### 1.1 統一命名治理契約定義的 16 種命名類型

| # | 命名類型 | 格式 | enforce.py 狀態 |
|---|---------|------|----------------|
| 1 | Comment Naming | `gl:<domain>:<capability>:<tag>` | ❌ 未實現 |
| 2 | Mapping Naming | `gl-<domain>-<capability>-map` | ❌ 未實現 |
| 3 | Reference Naming | `gl.ref.<domain>.<capability>.<resource>` | ❌ 未實現 |
| 4 | Path Naming | `/gl/<domain>/<capability>/<resource>` | ❌ 未實現 |
| 5 | Port Naming | `<protocol>-<domain>-<capability>` | ❌ 未實現 |
| 6 | Service Naming | `gl-<domain>-<capability>-svc` | ❌ 未實現 |
| 7 | Dependency Naming | `gl.dep.<domain>.<capability>` | ❌ 未實現 |
| 8 | Short Naming | `gl.<abbr>` | ❌ 未實現 |
| 9 | Long Naming | `gl-<domain>-<capability>-<resource>` | ❌ 未實現 |
| 10 | Directory Naming | `gl-<domain>-<capability>-platform/` | ⚠️ 部分實現 |
| 11 | File Naming | `gl-<domain>-<capability>-<resource>.<ext>` | ⚠️ 部分實現 |
| 12 | Event Naming | `gl.event.<domain>.<capability>.<action>` | ❌ 未實現 |
| 13 | Variable Naming | `GL<DOMAIN><CAPABILITY>_<RESOURCE>` | ❌ 未實現 |
| 14 | Environment Variable | `GL_<DOMAIN>_<CAPABILITY>_<KEY>` | ❌ 未實現 |
| 15 | GitOps Naming | `gl-<env>-<domain>-<capability>` | ❌ 未實現 |
| 16 | Helm Release Naming | `gl-<domain>-<capability>-<env>` | ❌ 未實現 |

### 1.2 您提到的命名類型對應

| 您提到的類型 | 對應契約規範 | 狀態 |
|-------------|-------------|------|
| 平台命名 | Directory Naming (#10) | ⚠️ 部分 |
| API 命名 | Path Naming (#4) | ❌ |
| 元件命名 | Reference Naming (#3) | ❌ |
| 工具命名 | Long Naming (#9) | ❌ |
| 服務命名 | Service Naming (#6) | ❌ |
| 端口命名 | Port Naming (#5) | ❌ |
| 依賴命名 | Dependency Naming (#7) | ❌ |
| 目錄命名 | Directory Naming (#10) | ⚠️ 部分 |
| 檔案命名 | File Naming (#11) | ⚠️ 部分 |
| 註解命名 | Comment Naming (#1) | ❌ |
| 標籤命名 | K8s Labels (契約中定義) | ❌ |
| 路徑命名 | Path Naming (#4) | ❌ |
| 映射命名 | Mapping Naming (#2) | ❌ |
| 引用命名 | Reference Naming (#3) | ❌ |
| DNS 命名 | Service Naming + Ingress | ❌ |

---

## 2. 現有規範文件位置

### 2.1 核心契約文件

```
gov-governance-architecture-platform/
├── contracts/
│   ├── unified-naming-governance-contract.yaml  # 主契約 (16種命名)
│   ├── semantic-unification-spec.yaml           # 語義統一
│   ├── structural-unification-spec.yaml         # 結構統一
│   └── governance-unification-spec.yaml         # 治理統一
└── governance/
    └── naming-governance/
        └── contracts/
            └── naming-conventions.yaml          # 命名慣例
```

### 2.2 政策文件

```
gov-governance-architecture-platform/gl90-99-meta-specification-layer/
└── governance/archived/legacy/governance-legacy/policies/naming/
    ├── api-naming.yaml           # API 命名政策
    ├── k8s-deployment-naming.yaml # K8s 部署命名
    └── pipeline-naming.yaml      # Pipeline 命名
```

### 2.3 當前 ecosystem 中的命名規範

```
ecosystem/
├── governance/
│   └── naming-conventions.yaml   # 基本命名規範 (我之前創建的)
├── contracts/
│   └── naming-governance/
│       ├── gov-naming-ontology.yaml
│       └── gov-naming-ontology-expanded.yaml
└── enforcers/
    └── naming_enforcer.py        # 基本命名檢查器 (我之前創建的)
```

---

## 3. 差距分析

### 3.1 enforce.py 當前實現

```python
# 當前只檢查:
# 1. 目錄命名 - 是否使用 kebab-case
# 2. Python 文件命名 - 是否使用 snake_case
# 3. 配置文件命名 - 是否使用 kebab-case
```

### 3.2 缺失的檢查

| 檢查類型 | 應檢查內容 | 優先級 |
|---------|-----------|--------|
| API 路徑 | `/gl/<domain>/<capability>/*` 格式 | 🔴 高 |
| 服務名稱 | K8s Service 是否符合 `gl-*-svc` | 🔴 高 |
| 標籤命名 | K8s Labels 是否符合規範 | 🔴 高 |
| 端口命名 | 端口名稱是否符合 `<protocol>-<domain>-*` | 🟡 中 |
| 註解命名 | 代碼註解是否使用 `gl:*` 格式 | 🟡 中 |
| 環境變數 | 是否符合 `GL_*` 格式 | 🟡 中 |
| 事件命名 | 事件是否符合 `gl.event.*` 格式 | 🟢 低 |
| 映射命名 | 映射是否符合 `gl-*-map` 格式 | 🟢 低 |

---

## 4. 建議的實現計劃

### Phase 1: 高優先級 (立即)

1. **API 路徑命名檢查**
   - 掃描 OpenAPI/Swagger 文件
   - 驗證路徑是否以 `/gl/` 開頭

2. **K8s 資源命名檢查**
   - Service 名稱: `gl-<domain>-<capability>-svc`
   - Deployment 名稱: `gl-<domain>-<capability>-deploy`
   - ConfigMap 名稱: `gl-<domain>-<capability>-cm`

3. **標籤命名檢查**
   - 必須包含 `app.kubernetes.io/name`
   - 必須包含 `gl.machinenativeops.io/domain`

### Phase 2: 中優先級 (本週)

4. **端口命名檢查**
   - 格式: `<protocol>-<domain>-<capability>`

5. **環境變數命名檢查**
   - 格式: `GL_<DOMAIN>_<CAPABILITY>_<KEY>`

6. **註解命名檢查**
   - GL 標註: `@GL-governed`, `@GL-layer`, `@GL-semantic`

### Phase 3: 低優先級 (下週)

7. **事件命名檢查**
8. **映射命名檢查**
9. **引用命名檢查**

---

## 5. 命名規範速查表

### 5.1 目錄命名

| 類型 | 格式 | 範例 |
|------|------|------|
| 平台目錄 | `gl-<domain>-<capability>-platform/` | `gov-runtime-dag-platform/` |
| 服務目錄 | `gl-<domain>-<capability>-service/` | `gov-api-schema-service/` |
| Python 包 | `snake_case` | `dual-path/` |

### 5.2 文件命名

| 類型 | 格式 | 範例 |
|------|------|------|
| Python | `snake_case.py` | `rule_engine.py` |
| YAML/JSON | `kebab-case.yaml` | `api-naming.yaml` |
| GL 文件 | `gl-<domain>-<capability>-<resource>.<ext>` | `gov-api-schema-user.yaml` |

### 5.3 K8s 資源命名

| 資源類型 | 格式 | 範例 |
|---------|------|------|
| Service | `gl-<domain>-<capability>-svc` | `gov-runtime-dag-svc` |
| Deployment | `gl-<domain>-<capability>-deploy` | `gov-api-schema-deploy` |
| ConfigMap | `gl-<domain>-<capability>-cm` | `gov-agent-max-cm` |
| Secret | `gl-<domain>-<capability>-secret` | `gov-db-shard-secret` |

### 5.4 API 路徑命名

| 類型 | 格式 | 範例 |
|------|------|------|
| REST API | `/gl/<domain>/<capability>/<resource>` | `/gl/runtime/dag/submit` |
| 版本化 | `/api/v1/gl/<domain>/<capability>` | `/api/v1/gl/agent/max/execute` |

### 5.5 標籤命名

```yaml
labels:
  app.kubernetes.io/name: gov-runtime-dag
  app.kubernetes.io/component: executor
  app.kubernetes.io/part-of: gov-platform
  gl.machinenativeops.io/domain: runtime
  gl.machinenativeops.io/capability: dag
  gl.machinenativeops.io/version: v1.0.0
```

---

## 6. 結論

### 6.1 當前狀態

- ✅ 命名治理規範文件**已完整定義**
- ❌ `enforce.py` **未完整實現**這些規範
- ⚠️ 規範與執行之間存在**嚴重差距**

### 6.2 建議行動

1. **立即**: 將 `unified-naming-governance-contract.yaml` 整合到 `enforce.py`
2. **本週**: 實現 K8s 資源和 API 路徑的命名檢查
3. **持續**: 建立 CI/CD 門檻，阻擋不符合命名規範的 PR

### 6.3 預期成果

實現完整命名治理後：
- 命名規範覆蓋率: 12.5% → 100%
- 自動化檢查: 16 種命名類型
- 合規性報告: 完整的 SLA 指標

---

**報告生成者**: MNGA Governance System  
**版本**: 3.0.0  
**下一步**: 實現完整的命名治理檢查器
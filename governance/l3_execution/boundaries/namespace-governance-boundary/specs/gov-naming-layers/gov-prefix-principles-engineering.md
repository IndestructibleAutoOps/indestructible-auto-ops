# GL 前綴使用原則（工程版）

## 版本資訊
- **版本**: 1.0.0
- **日期**: 2026-02-01
- **狀態**: ACTIVE
- **適用範圍**: 所有 GL 命名實體和屬性

## gl 前綴使用原則表格

| 類型 | gl 前綴形式 | 範例 | 說明 |
|------|-------------|-------|------|
| 平台級命名 | gov-xxx | gov-runtime-platform | 用於平台目錄和服務命名 |
| 語意鍵命名 | gl.key.xxx | gl.key.api.schema | 用於鍵值對配置和元資料鍵 |
| 語意短名 | gl.xxx.yyy | gl.api.schema | 用於語意實體和命名空間 |
| API 路徑 | /gl/xxx/yyy | /gl/runtime/dag | 用於 API 端點路徑 |
| K8s / GitOps 標籤 | gl.xxx/yyy | gl.platform/runtime | 用於 Kubernetes 和 GitOps 標籤 |
| 程式語言命名 | glxxx 或 glXxx | glruntime_dag, glRuntimeDag | 用於程式語言中的變數和函式 |

---

## 1. 語意層（Semantic Layer）

**目的**：統一語意結構、語意鍵、語意映射、語意圖。

### 1.1 gl 語意節點（gl.semantic_node）

#### 命名規則
- **格式**: gl.semantic_node.{entity_name}
- **範例**: 
  - gl.semantic_node.user
  - gl.semantic_node.order
  - gl.semantic_node.product
- **約束**: 必須使用全小寫，單數形式，用下劃線分隔多個單詞

#### 類型分類
- **實體節點**（Entity Nodes）：代表業務實體
  - gl.semantic_node.user
  - gl.semantic_node.account
- **關係節點**（Relation Nodes）：代表實體間關係
  - gl.semantic_node.owns
  - gl.semantic_node.belongs_to
- **屬性節點**（Attribute Nodes）：代表實體屬性
  - gl.semantic_node.email
  - gl.semantic_node.phone
- **事件節點**（Event Nodes）：代表業務事件
  - gl.semantic_node.user_created
  - gl.semantic_node.order_placed

#### 屬性格式
```yaml
gl.semantic_node.user:
  type: entity
  properties:
    - name: email
      type: string
      format: gl.format.email
    - name: created_at
      type: timestamp
      format: gl.format.iso8601
```

#### 唯一識別規則
- 每個語意節點必須有全局唯一的 ID
- ID 格式：`{layer}.{entity_type}.{entity_name}`
- 範例：`semantic.entity.user`

#### 版本化規則
- 語意節點支持語意化版本控制
- 版本格式：`v{major}.{minor}.{patch}`
- 範例：`gl.semantic_node.user:v1.2.0`

### 1.2 gl 語意鍵（gl.key.xxx）

#### 命名格式
- **格式**: gl.key.{category}.{key_name}
- **範例**:
  - gl.key.api.schema
  - gl.key.config.timeout
  - gl.key.metadata.label
- **約束**: 
  - category 代表鍵的類別
  - key_name 代表具體的鍵名
  - 使用點分隔符號

#### 層級結構
```
gl.key
├── api
│   ├── schema
│   ├── endpoint
│   └── version
├── config
│   ├── timeout
│   ├── retry
│   └── rate_limit
├── metadata
│   ├── label
│   ├── tag
│   └── annotation
└── security
    ├── role
    ├── permission
    └── policy
```

#### 衝突處理
- 當鍵名衝突時，使用命名空間前綴
- 格式：`gl.key.{namespace}.{category}.{key_name}`
- 範例：`gl.key.user.config.timeout`

#### 作用域
- **全局作用域**: gl.key.global.xxx
- **平台作用域**: gl.key.platform.xxx
- **服務作用域**: gl.key.service.xxx
- **模組作用域**: gl.key.module.xxx

#### 映射規則
- 語意鍵到實際配置的映射
- 格式：`gl.key.{source} → {target}`
- 範例：`gl.key.config.timeout → config.request.timeout`

### 1.3 gl 語意映射（gl.semantic_mapping）

#### 來源格式
```yaml
gl.semantic_mapping.user_profile:
  source:
    type: database
    table: users
    schema: public
  target:
    type: api
    endpoint: /api/users
    format: json
```

#### 目標格式
```yaml
gl.semantic_mapping.user_profile:
  target:
    type: semantic
    entity: gl.semantic_node.user
    version: v1.0.0
```

#### 衝突處理
- 優先級：明確映射 > 隱含映射 > 默認映射
- 衝突解決：使用 `priority` 字段指定優先級
- 範例：
```yaml
gl.semantic_mapping.user_profile:
  priority: 100  # 數字越大優先級越高
```

#### 優先級
- **100**: 明確映射（顯式定義）
- **50**: 隱含映射（約束推斷）
- **10**: 默認映射（默認規則）

#### 驗證規則
```yaml
gl.semantic_mapping.user_profile:
  validation:
    - type: required_fields
      fields: [id, name, email]
    - type: type_check
      rules:
        id: uuid
        email: string
        created_at: timestamp
```

### 1.4 gl 語意圖（gl.semantic_graph）

#### 節點類型
- **實體節點**：代表業務實體
- **屬性節點**：代表實體屬性
- **關係節點**：代表實體間關係
- **事件節點**：代表業務事件

#### 邊類型
- **HAS_A**：擁有關係
- **BELONGS_TO**：歸屬關係
- **RELATES_TO**：關聯關係
- **DEPENDS_ON**：依賴關係

#### 邊命名規則
- **格式**: gl.semantic_edge.{source_type}.{target_type}
- **範例**:
  - gl.semantic_edge.user.address
  - gl.semantic_edge.order.product

#### 一致性檢查
```python
def check_semantic_consistency(graph):
    """
    檢查語意圖的一致性
    """
    rules = [
        'no_cycles',           # 無循環
        'type_consistency',    # 類型一致
        'required_edges',      # 必需邊
        'optional_edges'       # 可選邊
    ]
    
    for rule in rules:
        validate_rule(graph, rule)
```

#### 循環檢查
- 檢測圖中的循環依賴
- 使用深度優先搜索（DFS）算法
- 返回所有循環路徑

#### 快取規則
- **節點快取**: 快取節點屬性和關係
- **邊快取**: 快取節點間的連接關係
- **查詢快取**: 快取常見查詢結果
- **TTL**: 設定快取過期時間

### 1.5 gl 語意分類（gl.semantic_category）

#### 命名規則
- **格式**: gl.semantic_category.{category_name}
- **範例**:
  - gl.semantic_category.entity
  - gl.semantic_category.relation
  - gl.semantic_category.event

#### 層級結構
```
gl.semantic_category
├── entity
│   ├── user
│   ├── account
│   └── product
├── relation
│   ├── owns
│   ├── belongs_to
│   └── depends_on
└── event
    ├── created
    ├── updated
    └── deleted
```

#### 繼承規則
- 子類別繼承父類別的所有屬性和約束
- 格式：`gl.semantic_category.{parent}.{child}`
- 範例：
```yaml
gl.semantic_category.entity.user:
  inherits: gl.semantic_category.entity
  properties:
    - name
    - email
    - created_at
```

#### 衝突處理
- 當名稱衝突時，使用完全限定名
- 格式：`{parent}.{child}.{specific_name}`
- 範例：`entity.user.admin_user`

### 1.6 gl 語意屬性（gl.semantic_attribute）

#### 命名規則
- **格式**: gl.semantic_attribute.{entity}.{attribute_name}
- **範例**:
  - gl.semantic_attribute.user.email
  - gl.semantic_attribute.order.total
  - gl.semantic_attribute.product.price

#### 型別系統
```yaml
gl.semantic_attribute.user.email:
  type: string
  format: email
  validation:
    - required: true
    - pattern: '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

gl.semantic_attribute.user.created_at:
  type: timestamp
  format: iso8601
  validation:
    - required: true
    - default: 'now()'
```

#### 驗證規則
- **類型驗證**: 檢查值是否符合預期類型
- **格式驗證**: 檢查值是否符合預期格式
- **約束驗證**: 檢查值是否符合約束條件
- **自定義驗證**: 支持自定義驗證邏輯

#### 預設值
```yaml
gl.semantic_attribute.user.status:
  type: enum
  enum: [active, inactive, deleted]
  default: active

gl.semantic_attribute.order.created_at:
  type: timestamp
  default: 'now()'

gl.semantic_attribute.product.is_available:
  type: boolean
  default: true
```

---

## 2. 實現指南

### 2.1 程式語言實現

#### Python
```python
# 語意節點定義
class GLSemanticNode:
    def __init__(self, node_type: str, node_name: str):
        self.name = f"gl.semantic_node.{node_type}.{node_name}"
        self.type = node_type

# 使用範例
user_node = GLSemanticNode("entity", "user")
# user_node.name = "gl.semantic_node.entity.user"
```

#### Go
```go
// 語意鍵定義
const (
    KeyAPISchema    = "gl.key.api.schema"
    KeyConfigTimeout = "gl.key.config.timeout"
    KeyMetaLabel    = "gl.key.metadata.label"
)

// 使用範例
config := map[string]interface{}{
    KeyConfigTimeout: 30, // seconds
}
```

#### JavaScript/TypeScript
```typescript
// 語意映射定義
interface GLSemanticMapping {
    name: string;
    source: any;
    target: any;
    priority?: number;
}

// 使用範例
const userMapping: GLSemanticMapping = {
    name: 'gl.semantic_mapping.user_profile',
    source: { type: 'database', table: 'users' },
    target: { type: 'api', endpoint: '/api/users' },
    priority: 100
};
```

### 2.2 K8s 資源定義

#### Pod 標籤
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: gov-runtime-pod
  labels:
    gl.platform/runtime: "true"
    gl.service/type: "dag"
    gl.version: "v1.0.0"
spec:
  containers:
  - name: gov-runtime-container
    image: gov-runtime:v1.0.0
```

#### ConfigMap
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: gov-runtime-config
data:
  gl.key.api.timeout: "30"
  gl.key.api.retry: "3"
  gl.key.log.level: "info"
```

### 2.3 API 路徑設計

```yaml
# API 路徑規範
paths:
  /gl/runtime/dag:
    post:
      summary: 執行 DAG
      operationId: gl.runtime.dag.execute
  /gl/runtime/jobs:
    get:
      summary: 獲取任務列表
      operationId: gl.runtime.jobs.list
  /gl/api/schema:
    get:
      summary: 獲取 API Schema
      operationId: gl.api.schema.get
```

---

## 3. 驗證與合規

### 3.1 命名規則驗證
- 檢查 gl 前綴使用是否正確
- 驗證命名格式是否符合規範
- 檢查命名空間是否衝突

### 3.2 一致性檢查
- 驗證跨層級的命名一致性
- 檢查語意圖的一致性
- 驗證類型系統的一致性

### 3.3 自動化檢查
- 集成到 CI/CD pipeline
- 使用 pre-commit hooks
- 自動生成命名合規報告

---

## 4. 最佳實踐

### 4.1 命名約定
- 使用有意義的名稱
- 保持命名簡潔但表達清晰
- 避免縮寫（除非是通用縮寫）
- 使用單數形式表示實體

### 4.2 文檔化
- 為每個命名實體提供清晰的文檔
- 使用範例說明使用場景
- 提供錯誤處理指南

### 4.3 版本管理
- 對命名規範進行版本管理
- 使用語意化版本控制
- 維護變更日誌

---

## 5. 工具支持

### 5.1 CLI 工具
```bash
# 驗證命名規範
gov-naming validate --file ./config.yaml

# 生成命名模板
gov-naming generate --type semantic_node --name user

# 檢查命名衝突
gov-naming check-conflicts --layer semantic
```

### 5.2 IDE 插件
- 自動完成 gl 前綴命名
- 實時驗證命名規範
- 提供命名建議

### 5.3 Linter
- 靜態代碼分析
- 命名規範檢查
- 自動修復建議

---

## 附錄

### A. 完整命名範例
```yaml
# 語意節點
gl.semantic_node.user:
  type: entity
  properties:
    - gl.semantic_attribute.user.email
    - gl.semantic_attribute.user.name
    - gl.semantic_attribute.user.created_at

# 語意鍵
gl.key.api.schema: user_schema_v1
gl.key.config.timeout: 30
gl.key.metadata.label: user_service

# 語意映射
gl.semantic_mapping.user_profile:
  source:
    type: database
    table: users
  target:
    type: api
    endpoint: /api/users
  priority: 100

# 語意圖
gl.semantic_graph.user_system:
  nodes:
    - gl.semantic_node.user
    - gl.semantic_node.order
  edges:
    - gl.semantic_edge.user.order
```

### B. 遷移指南
1. 識別現有的命名實體
2. 應用 gl 前綴規則
3. 更新所有引用
4. 驗證一致性
5. 部署變更

### C. 參考資源
- GL 擴展命名本體 v3.0.0
- GL 平台命名契約
- GL 命名驗證規則

---

**文檔版本**: 1.0.0  
**最後更新**: 2026-02-01  
**維護者**: GL Governance Team  
**狀態**: ACTIVE
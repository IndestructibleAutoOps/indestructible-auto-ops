# GL 平台層（Platform Layer）規範

## 版本資訊
- **版本**: 1.0.0
- **日期**: 2026-02-01
- **狀態**: ACTIVE
- **適用範圍**: 所有 GL 平台、元件、服務、模組

---

## 3. 平台層（Platform Layer）

### 3.1 gl 平台（gov-platform）

#### 命名規則
- **格式**: gl.{domain}.{capability}-platform
- **範例**:
  - gl.runtime.execution-platform
  - gl.data.processing-platform
  - gl.ai.inference-platform

#### 約束
- 必須使用小寫字母
- 域和能力之間用點分隔
- 必須以 -platform 結尾
- 遵循 GL 平台命名契約

#### gov-platform ID
- **格式**: gl.{domain}.{capability}-platform
- **範例**: `gl.runtime.execution-platform`
- **約束**: 全局唯一，不可重複

#### gov-platform short name
- **格式**: {domain}-{capability}
- **範例**: runtime-execution, data-processing
- **約束**: 簡短名稱，不包含 gl- 和 -platform

#### gov-platform long name
- **格式**: GL {Domain} {Capability} Platform
- **範例**: GL Runtime Execution Platform
- **約束**: 完整名稱，大寫每個單詞首字母

#### 實現範例
```python
class GLPlatform:
    def __init__(
        self,
        domain: str,
        capability: str,
        short_name: str = None,
        long_name: str = None
    ):
        self.id = f"gl.{domain}.{capability}-platform"
        self.short_name = short_name or f"{domain}-{capability}"
        self.long_name = long_name or f"GL {domain.title()} {capability.title()} Platform"
        self.domain = domain
        self.capability = capability
    
    def validate(self) -> bool:
        """驗證平台命名"""
        import re
        pattern = r'^gl\.[a-z]+\.[a-z]+-platform$'
        return bool(re.match(pattern, self.id))

# 使用範例
platform = GLPlatform(
    domain='runtime',
    capability='execution'
)
print(f"Platform ID: {platform.id}")
print(f"Short Name: {platform.short_name}")
print(f"Long Name: {platform.long_name}")
print(f"Valid: {platform.validate()}")
```

### 3.2 gl 元件（gl.component）

#### 命名規則
- **格式**: gl.{domain}.{capability}.{component}
- **範例**:
  - gl.runtime.execution.dag-engine
  - gl.data.processing.bulk-indexer
  - gl.ai.inference.model-server

#### 分類
```yaml
component_categories:
  - engine: 執行引擎（如 dag-engine, query-engine）
  - processor: 處理器（如 bulk-processor, stream-processor）
  - service: 服務（如 api-service, auth-service）
  - client: 客戶端（如 http-client, grpc-client）
  - storage: 存儲（如 file-storage, database-storage）
  - cache: 緩存（如 memory-cache, redis-cache）
  - queue: 隊列（如 message-queue, task-queue）
  - monitor: 監控（如 metrics-monitor, log-monitor）
  - scheduler: 調度器（如 job-scheduler, cron-scheduler）
  - validator: 驗證器（如 data-validator, schema-validator）
```

#### 目錄結構
```
gl-{platform}/
├── components/
│   ├── {component_name}/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.yaml
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── tests/
│   │   └── docs/
│   └── ...
├── configs/
├── docs/
├── deployments/
└── governance/
```

#### 實現範例
```python
class GLComponent:
    CATEGORIES = ['engine', 'processor', 'service', 'client', 'storage', 
                  'cache', 'queue', 'monitor', 'scheduler', 'validator']
    
    def __init__(
        self,
        platform_id: str,
        component_type: str,
        component_name: str
    ):
        self.platform_id = platform_id
        self.type = component_type
        self.name = component_name
        self.id = f"{platform_id}.{component_name}"
        self.path = f"components/{component_name}"
    
    def validate(self) -> bool:
        """驗證元件命名"""
        # 驗證類別
        if self.type not in self.CATEGORIES:
            return False
        
        # 驗證命名格式
        import re
        pattern = r'^gl\.[a-z]+\.[a-z]+\.[a-z-]+$'
        return bool(re.match(pattern, self.id))

# 使用範例
component = GLComponent(
    platform_id='gl.runtime.execution-platform',
    component_type='engine',
    component_name='dag-engine'
)
print(f"Component ID: {component.id}")
print(f"Valid: {component.validate()}")
```

### 3.3 gl 服務（gl.service）

#### 命名規則
- **格式**: gl.{domain}.{service}.{service_name}
- **範例**:
  - gl.api.service.user-service
  - gl.runtime.service.job-service
  - gl.data.service.query-service

#### gl.service.endpoint 命名
- **格式**: /gl/{domain}/{service}/{action}
- **範例**:
  - /gl/api/users/list
  - /gl/runtime/jobs/create
  - /gl/data/query/execute

#### gl.service 版本
- **格式**: v{major}.{minor}.{patch}
- **範例**: v1.2.3
- **規則**: 遵循語意化版本控制

#### 實現範例
```python
class GLService:
    def __init__(
        self,
        service_id: str,
        version: str,
        endpoints: list = None
    ):
        self.id = service_id
        self.version = version
        self.endpoints = endpoints or []
    
    def add_endpoint(self, path: str, method: str, description: str = ""):
        """添加服務端點"""
        endpoint = {
            'path': path,
            'method': method,
            'description': description
        }
        self.endpoints.append(endpoint)
    
    def get_endpoint(self, path: str) -> dict:
        """獲取端點"""
        for endpoint in self.endpoints:
            if endpoint['path'] == path:
                return endpoint
        return None

# 使用範例
service = GLService(
    service_id='gl.api.service.user-service',
    version='1.0.0'
)

service.add_endpoint(
    path='/gl/api/users/list',
    method='GET',
    description='List all users'
)

service.add_endpoint(
    path='/gl/api/users/create',
    method='POST',
    description='Create a new user'
)

print(f"Service ID: {service.id}")
print(f"Version: {service.version}")
print(f"Endpoints: {len(service.endpoints)}")
```

### 3.4 gl 模組（gl.module）

#### 命名規則
- **格式**: gl.{domain}.{capability}.{module_name}
- **範例**:
  - gl.runtime.execution.dag-scheduler
  - gl.data.processing.etl-pipeline
  - gl.ai.inference.model-loader

#### 依賴規則
```yaml
dependency_rules:
  - rule: "只依賴 GL 內部模組"
    description: "模組只能依賴 GL 生態系統內的模組"
  
  - rule: "無循環依賴"
    description: "模組之間不能存在循環依賴"
  
  - rule: "依賴方向"
    description: "低層級模組可以依賴高層級模組"
  
  - rule: "顯式聲明"
    description: "所有依賴必須在 metadata 中顯式聲明"
```

#### 目錄結構
```
gl-{module}/
├── __init__.py
├── main.py
├── config.yaml
├── schemas/
│   ├── __init__.py
│   ├── models.py
│   └── requests.py
├── services/
│   ├── __init__.py
│   ├── service.py
│   └── handlers.py
├── utils/
│   ├── __init__.py
│   └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── test_services.py
└── docs/
    ├── README.md
    └── API.md
```

#### 實現範例
```python
class GLModule:
    DEPENDENCY_RULES = {
        'no_external': True,  # 只依賴 GL 內部
        'no_circular': True,  # 無循環依賴
        'directional': True,  # 方向性依賴
        'explicit': True      # 顯式聲明
    }
    
    def __init__(
        self,
        module_id: str,
        dependencies: list = None
    ):
        self.id = module_id
        self.dependencies = dependencies or []
        self.metadata = {
            'created_at': datetime.utcnow().isoformat(),
            'dependencies': self.dependencies
        }
    
    def add_dependency(self, dependency_id: str):
        """添加依賴"""
        if dependency_id not in self.dependencies:
            self.dependencies.append(dependency_id)
    
    def validate_dependencies(self, all_modules: dict) -> bool:
        """驗證依賴規則"""
        # 檢查循環依賴
        if self._has_circular_dependency(all_modules):
            return False
        
        # 檢查外部依賴
        for dep in self.dependencies:
            if dep not in all_modules:
                return False
        
        return True
    
    def _has_circular_dependency(self, all_modules: dict) -> bool:
        """檢查循環依賴"""
        visited = set()
        
        def dfs(module_id: str) -> bool:
            if module_id in visited:
                return True
            if module_id == self.id:
                return False
            visited.add(module_id)
            
            module = all_modules.get(module_id)
            if module:
                for dep in module.dependencies:
                    if dfs(dep):
                        return True
            return False
        
        for dep in self.dependencies:
            if dfs(dep):
                return True
        
        return False

# 使用範例
modules = {
    'gl.runtime.execution.dag-scheduler': GLModule('gl.runtime.execution.dag-scheduler'),
    'gl.data.processing.etl-pipeline': GLModule('gl.data.processing.etl-pipeline')
}

module = modules['gl.runtime.execution.dag-scheduler']
module.add_dependency('gl.data.processing.etl-pipeline')

print(f"Module ID: {module.id}")
print(f"Dependencies: {module.dependencies}")
print(f"Valid: {module.validate_dependencies(modules)}")
```

### 3.5 gl 套件（gl.package）

#### 命名規則
- **格式**: gl.{domain}.{package_name}
- **範例**:
  - gl.runtime.utils
  - gl.data.formats
  - gl.ai.models

#### 版本
- **格式**: v{major}.{minor}.{patch}
- **範例**: v1.0.0
- **規則**: 遵循語意化版本控制

#### 依賴
```yaml
package_dependencies:
  - type: "internal"
    description: "GL 內部套件依賴"
    format: gl.{domain}.{package_name}
  
  - type: "external"
    description: "外部套件依賴"
    format: {package_name}
  
  - type: "dev"
    description: "開發依賴"
    format: {package_name}
```

#### 實現範例
```python
class GLPackage:
    def __init__(
        self,
        package_id: str,
        version: str,
        dependencies: dict = None
    ):
        self.id = package_id
        self.version = version
        self.dependencies = dependencies or {
            'internal': [],
            'external': [],
            'dev': []
        }
    
    def add_dependency(self, dep_type: str, package_id: str):
        """添加依賴"""
        if dep_type in self.dependencies:
            if package_id not in self.dependencies[dep_type]:
                self.dependencies[dep_type].append(package_id)
    
    def get_dependency_graph(self) -> dict:
        """獲取依賴圖"""
        graph = {
            'internal': self.dependencies['internal'],
            'external': self.dependencies['external'],
            'dev': self.dependencies['dev']
        }
        return graph

# 使用範例
package = GLPackage(
    package_id='gl.runtime.utils',
    version='1.0.0'
)

package.add_dependency('internal', 'gl.data.formats')
package.add_dependency('external', 'requests')
package.add_dependency('dev', 'pytest')

print(f"Package ID: {package.id}")
print(f"Version: {package.version}")
print(f"Dependencies: {package.get_dependency_graph()}")
```

### 3.6 gl 資源（gl.resource）

#### 命名規則
- **格式**: gl.{resource_type}.{resource_name}
- **範例**:
  - gl.resource.config.timeout
  - gl.resource.secret.api_key
  - gl.resource.database.connection_string

#### 分類
```yaml
resource_categories:
  - config: 配置資源
  - secret: 機密資源
  - database: 數據庫資源
  - storage: 存儲資源
  - cache: 緩存資源
  - queue: 隊列資源
  - api: API 資源
  - file: 文件資源
```

#### 引用規則
```yaml
reference_rules:
  - rule: "使用完整路徑"
    format: "gl.{category}.{name}"
  
  - rule: "避免硬編碼"
    description: "資源引用應使用環境變量或配置"
  
  - rule: "作用域限制"
    description: "資源只能在其作用域內引用"
```

#### 實現範例
```python
class GLResource:
    CATEGORIES = ['config', 'secret', 'database', 'storage', 'cache', 'queue', 'api', 'file']
    
    def __init__(
        self,
        resource_type: str,
        resource_name: str,
        value: str = None
    ):
        self.type = resource_type
        self.name = resource_name
        self.id = f"gl.resource.{resource_type}.{resource_name}"
        self.value = value
        self.references = []
    
    def add_reference(self, resource_id: str):
        """添加引用"""
        if resource_id not in self.references:
            self.references.append(resource_id)
    
    def get_value(self, context: dict = None) -> str:
        """獲取資源值（支持變量替換）"""
        if self.value:
            import re
            value = self.value
            if context:
                for key, val in context.items():
                    value = value.replace(f"${{{key}}}", str(val))
            return value
        return None

# 使用範例
resource = GLResource(
    resource_type='config',
    resource_name='timeout',
    value='${default_timeout}'
)

print(f"Resource ID: {resource.id}")
print(f"Value: {resource.get_value({'default_timeout': '30s'})}")
```

### 3.7 gl 事件（gl.event）

#### 命名規則
- **格式**: gl.event.{domain}.{event_name}
- **範例**:
  - gl.event.api.request_received
  - gl.event.runtime.job_completed
  - gl.event.data.pipeline_finished

#### 分類
```yaml
event_categories:
  - system: 系統事件（啟動、停止、重啟）
  - user: 用戶事件（登錄、註冊、操作）
  - business: 業務事件（訂單創建、支付完成）
  - error: 錯誤事件（異常、失敗、超時）
  - audit: 審計事件（認證、授權、訪問）
  - metric: 指標事件（性能、資源、健康）
```

#### payload 格式
```yaml
event_payload:
  event_id: "evt-20260201-001"
  event_type: "gl.event.api.request_received"
  timestamp: "2026-02-01T10:00:00Z"
  source: "gl.api.service.user-service"
  data:
    method: "GET"
    path: "/gl/api/users/list"
    user_id: "user-123"
  metadata:
    request_id: "req-001"
    duration_ms: 125
    status_code: 200
```

#### 實現範例
```python
class GLEvent:
    def __init__(
        self,
        event_type: str,
        source: str,
        data: dict = None,
        metadata: dict = None
    ):
        self.id = self._generate_event_id()
        self.type = event_type
        self.source = source
        self.timestamp = datetime.utcnow().isoformat() + 'Z'
        self.data = data or {}
        self.metadata = metadata or {}
    
    def _generate_event_id(self) -> str:
        """生成事件 ID"""
        date_str = datetime.utcnow().strftime("%Y%m%d")
        uuid = str(hash(self.timestamp))[:3]
        return f"evt-{date_str}-{uuid}"
    
    def to_dict(self) -> dict:
        """轉換為字典"""
        return {
            'event_id': self.id,
            'event_type': self.type,
            'timestamp': self.timestamp,
            'source': self.source,
            'data': self.data,
            'metadata': self.metadata
        }

# 使用範例
event = GLEvent(
    event_type='gl.event.api.request_received',
    source='gl.api.service.user-service',
    data={
        'method': 'GET',
        'path': '/gl/api/users/list'
    },
    metadata={
        'request_id': 'req-001',
        'duration_ms': 125
    }
)

print(f"Event ID: {event.id}")
print(f"Event Type: {event.type}")
print(f"Event: {event.to_dict()}")
```

### 3.8 gl API（/gl/...）

#### /gl/api 路徑命名
- **格式**: /gl/{domain}/{service}/{action}
- **範例**:
  - /gl/api/users/list
  - /gl/runtime/jobs/create
  - /gl/data/query/execute

#### gl.api 方法命名
```yaml
api_methods:
  - GET: 獲取資源
  - POST: 創建資源
  - PUT: 更新資源
  - DELETE: 刪除資源
  - PATCH: 部分更新
  - HEAD: 獲取頭部
  - OPTIONS: 獲取選項
```

#### gl.api 參數命名
- **格式**: {parameter_name}
- **範例**:
  - user_id
  - page
  - limit
  - sort_by

#### gl.api 回應格式
```yaml
api_response:
  success: true
  data:
    # 回應數據
  metadata:
    total: 100
    page: 1
    limit: 10
  error:
    code: "GL-XXX-001"
    message: "Error message"
    details: {}
```

#### 實現範例
```python
class GLAPIEndpoint:
    def __init__(
        self,
        path: str,
        method: str,
        description: str = "",
        parameters: dict = None
    ):
        self.path = path
        self.method = method.upper()
        self.description = description
        self.parameters = parameters or {}
    
    def create_response(self, data: any = None, error: dict = None) -> dict:
        """創建 API 回應"""
        response = {
            'success': error is None,
            'data': data,
            'metadata': {}
        }
        
        if error:
            response['error'] = error
        else:
            if isinstance(data, list):
                response['metadata']['total'] = len(data)
        
        return response

# 使用範例
endpoint = GLAPIEndpoint(
    path='/gl/api/users/list',
    method='GET',
    description='List all users',
    parameters={
        'page': {'type': 'int', 'default': 1},
        'limit': {'type': 'int', 'default': 10}
    }
)

response = endpoint.create_response(
    data=[{'id': 1, 'name': 'User 1'}, {'id': 2, 'name': 'User 2'}]
)

print(f"Path: {endpoint.path}")
print(f"Method: {endpoint.method}")
print(f"Response: {response}")
```

### 3.9 gl ENV（gl.env.xxx）

#### 命名規則
- **格式**: gl.env.{category}.{variable_name}
- **範例**:
  - gl.env.api.timeout
  - gl.env.db.host
  - gl.env.secret.key

#### 分類
```yaml
env_categories:
  - api: API 配置
  - db: 數據庫配置
  - cache: 緩存配置
  - queue: 隊列配置
  - secret: 機密配置
  - storage: 存儲配置
  - monitoring: 監控配置
  - logging: 日誌配置
```

#### 安全規則
```yaml
security_rules:
  - rule: "敏感信息加密"
    description: "密碼、密鑰等敏感信息必須加密存儲"
  
  - rule: "最小權限原則"
    description: "環境變量應遵循最小權限原則"
  
  - rule: "定期輪換"
    description: "密鑰和密碼應定期輪換"
```

#### 實現範例
```python
class GLEnvironment:
    def __init__(self, category: str, variables: dict = None):
        self.category = category
        self.variables = variables or {}
        self.secrets = []
    
    def set_variable(self, name: str, value: str, is_secret: bool = False):
        """設置環境變量"""
        self.variables[name] = value
        if is_secret:
            self.secrets.append(name)
    
    def get_variable(self, name: str) -> str:
        """獲取環境變量"""
        return self.variables.get(name)
    
    def export(self) -> dict:
        """導出環境變量"""
        export_vars = {}
        for name, value in self.variables.items():
            key = f"gl.env.{self.category}.{name}"
            export_vars[key] = value
        return export_vars

# 使用範例
env = GLEnvironment('api')
env.set_variable('timeout', '30s')
env.set_variable('key', 'secret-value', is_secret=True)

print(f"Category: {env.category}")
print(f"Variables: {env.export()}")
print(f"Secrets: {env.secrets}")
```

### 3.10 gl Label（gl.label.xxx）

#### 命名規則
- **格式**: gl.label.{category}.{label_name}
- **範例**:
  - gl.label.platform.runtime
  - gl.label.service.users
  - gl.label.version.v1.0.0

#### 分類
```yaml
label_categories:
  - platform: 平台標籤
  - service: 服務標籤
  - component: 元件標籤
  - version: 版本標籤
  - environment: 環境標籤
  - tier: 層級標籤
  - owner: 所有者標籤
  - team: 團隊標籤
```

#### 作用域
```yaml
label_scopes:
  - global: 全局作用域
  - platform: 平台作用域
  - service: 服務作用域
  - component: 元件作用域
```

#### 實現範例
```python
class GLLabel:
    def __init__(
        self,
        category: str,
        label_name: str,
        scope: str = 'global'
    ):
        self.category = category
        self.name = label_name
        self.id = f"gl.label.{category}.{label_name}"
        self.scope = scope
        self.value = None
    
    def set_value(self, value: str):
        """設置標籤值"""
        self.value = value
    
    def to_dict(self) -> dict:
        """轉換為字典"""
        return {
            'id': self.id,
            'category': self.category,
            'name': self.name,
            'scope': self.scope,
            'value': self.value
        }

# 使用範例
label = GLLabel(
    category='platform',
    label_name='runtime',
    scope='platform'
)
label.set_value('true')

print(f"Label ID: {label.id}")
print(f"Label: {label.to_dict()}")
```

### 3.11 gl Comment（gl.comment.xxx）

#### 格式
- **格式**: # gl.{category}.{comment}
- **範例**:
  - # gl.api.endpoint.list_users
  - # gl.runtime.job.create_task

#### 分類
```yaml
comment_categories:
  - doc: 文檔註釋
  - todo: 待辦事項
  - fixme: 修復標記
  - hack: 臨時方案
  - note: 備註
  - warning: 警告
```

#### metadata
```yaml
comment_metadata:
  - author: 作者
  - date: 日期
  - line: 行號
  - file: 文件
  - context: 上下文
```

#### 實現範例
```python
class GLComment:
    CATEGORIES = ['doc', 'todo', 'fixme', 'hack', 'note', 'warning']
    
    def __init__(
        self,
        category: str,
        content: str,
        metadata: dict = None
    ):
        self.category = category
        self.content = content
        self.metadata = metadata or {}
        self.id = self._generate_id()
    
    def _generate_id(self) -> str:
        """生成註釋 ID"""
        import re
        text = re.sub(r'\s+', '-', self.content)[:30]
        date_str = datetime.utcnow().strftime("%Y%m%d")
        return f"gl.comment.{category}.{date_str}-{text}"
    
    def to_string(self) -> str:
        """轉換為字串格式"""
        return f"# gl.{self.category}.{self.content}"

# 使用範例
comment = GLComment(
    category='todo',
    content='implement user authentication',
    metadata={
        'author': 'developer-1',
        'date': '2026-02-01'
    }
)

print(f"Comment ID: {comment.id}")
print(f"Comment: {comment.to_string()}")
```

### 3.12 gl File / Directory / Path

#### gl.file 命名
- **格式**: {file_name}.{extension}
- **範例**:
  - dag_executor.py
  - user_service.py
  - data_processor.go

#### gl.dir 命名
- **格式**: {directory_name}
- **範例**:
  - components
  - services
  - configs
  - tests

#### gl.path 命名
- **格式**: {relative_path}
- **範例**:
  - gl/runtime/execution
  - gl/data/processing
  - gl/api/service

#### 實現範例
```python
import os
from pathlib import Path

class GLFileSystem:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
    
    def create_file(self, file_name: str, content: str = ""):
        """創建文件"""
        file_path = self.base_path / file_name
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
        return file_path
    
    def create_directory(self, dir_name: str):
        """創建目錄"""
        dir_path = self.base_path / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path
    
    def create_path(self, path_str: str):
        """創建路徑"""
        path = self.base_path / path_str
        if path.suffix:
            self.create_file(path_str)
        else:
            self.create_directory(path_str)
        return path

# 使用範例
fs = GLFileSystem('/tmp/gov-platform')

file = fs.create_file('components/dag_engine/main.py')
dir_ = fs.create_directory('services/user_service')
path = fs.create_path('configs/api_config.yaml')

print(f"File: {file}")
print(f"Directory: {dir_}")
print(f"Path: {path}")
```

---

## 實現指南

### 綜合使用範例

```python
from datetime import datetime
from pathlib import Path

# 創建平台
platform = GLPlatform(
    domain='runtime',
    capability='execution'
)

# 創建元件
component = GLComponent(
    platform_id=platform.id,
    component_type='engine',
    component_name='dag-engine'
)

# 創建服務
service = GLService(
    service_id='gl.api.service.user-service',
    version='1.0.0'
)
service.add_endpoint('/gl/api/users/list', 'GET', 'List all users')

# 創建模組
module = GLModule(
    module_id='gl.runtime.execution.dag-scheduler'
)
module.add_dependency('gl.data.processing.etl-pipeline')

# 創建事件
event = GLEvent(
    event_type='gl.event.api.request_received',
    source='gl.api.service.user-service',
    data={'method': 'GET', 'path': '/gl/api/users/list'}
)

# 創建環境變量
env = GLEnvironment('api')
env.set_variable('timeout', '30s')
env.set_variable('key', 'secret-value', is_secret=True)

# 創建文件系統
fs = GLFileSystem('/tmp/gov-platform')
fs.create_file('components/dag_engine/main.py')

print(f"Platform: {platform.id}")
print(f"Component: {component.id}")
print(f"Service: {service.id}")
print(f"Module: {module.id}")
print(f"Event: {event.id}")
print(f"Environment: {env.export()}")
```

## 集成示例

### K8s Deployment 示例

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
    env:
      - name: gl.env.api.timeout
        value: "30s"
      - name: gl.env.db.host
        value: "localhost"
    ports:
      - containerPort: 8080
```

## 最佳實踐

### 1. 命名一致性
- 使用統一的命名約定
- 遵循 GL 前綴規則
- 保持命名簡潔明了

### 2. 模塊化設計
- 每個模組職責單一
- 模組間低耦合
- 清晰的依賴關係

### 3. 文檔化
- 為每個實體提供文檔
- 使用清晰的註釋
- 提供使用範例

### 4. 安全性
- 敏感信息加密
- 遵循最小權限原則
- 定期輪換密鑰

---

**文檔版本**: 1.0.0  
**最後更新**: 2026-02-01  
**維護者**: GL Governance Team  
**狀態**: ACTIVE
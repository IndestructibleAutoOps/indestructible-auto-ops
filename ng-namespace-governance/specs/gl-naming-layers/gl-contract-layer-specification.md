# GL 契約層（Contract Layer）規範

## 版本資訊
- **版本**: 1.0.0
- **日期**: 2026-02-01
- **狀態**: ACTIVE
- **適用範圍**: 所有 GL 契約、規範、策略、驗證器

---

## 2. 契約層（Contract Layer）

### 2.1 gl 契約（gl.contract）

#### 命名規則
- **格式**: gl.contract.{contract_name}
- **範例**:
  - gl.contract.naming_ontology
  - gl.contract.platform_definition
  - gl.contract.validation_rules

#### 約束
- 契約名稱必須使用小寫字母
- 使用下劃線分隔多個單詞
- 必須具有全局唯一性

#### 實現範例
```yaml
gl.contract.naming_ontology:
  id: gl.contract.naming_ontology
  version: "1.0.0"
  type: core
  status: active
```

#### gl.contract ID
- **格式**: gl.contract.{contract_name}
- **約束**: 必須唯一，不可重複
- **範例**: `gl.contract.naming_ontology`

#### gl.contract 版本
- **格式**: v{major}.{minor}.{patch}
- **規則**: 遵循語意化版本控制（SemVer）
- **範例**: `v1.2.3`

#### gl.contract 分類
```yaml
categories:
  - core: 核心契約（如命名本體、治理層級）
  - platform: 平台契約（如平台定義、平台索引）
  - validation: 驗證契約（如驗證規則、驗證器）
  - governance: 治理契約（如治理層級、放置規則）
  - extension: 擴展契約（如擴展點定義）
  - generator: 生成器契約（如生成器規範）
  - reasoning: 推理契約（如推理規則）
```

### 2.2 gl 契約格式（gl.contract_format）

#### YAML/JSON 結構
```yaml
gl.contract_format.schema:
  apiVersion: contract.gl/v1
  kind: Contract
  metadata:
    name: {contract_name}
    version: "{version}"
    description: "{description}"
    category: {category}
  spec:
    # 契約具體規範
```

#### 必填欄位
```yaml
required_fields:
  - id: 契約唯一標識
  - version: 契約版本
  - type: 契約類型
  - status: 契約狀態
  - spec:約規範
```

#### 選填欄位
```yaml
optional_fields:
  - description: 契約描述
  - category: 契約分類
  - governance: 治理框架
  - dependencies: 依賴列表
  - validation_rules: 驗證規則
  - metadata: 元資料
```

#### gl.contract_format metadata
```yaml
gl.contract_format.metadata:
  created_at: "2026-02-01T00:00:00Z"
  updated_at: "2026-02-01T00:00:00Z"
  author: "GL Governance Team"
  license: "MIT"
  tags:
    - naming
    - governance
    - contract
  references:
    - type: documentation
      url: "https://docs.gl.com/naming"
```

### 2.3 gl 規範（gl.spec）

#### 結構
```yaml
gl.spec.contract:
  schema:
    type: object
    properties:
      layers:
        type: array
        items:
          type: string
      rules:
        type: object
      policies:
        type: array
```

#### 版本化
- **格式**: gl.spec.{contract_name}.v{version}
- **範例**: gl.spec.naming_ontology.v1.0.0
- **規則**:
  - 主版本號（major）：不兼容的 API 變更
  - 次版本號（minor）：向下兼容的功能性新增
  - 修訂號（patch）：向下兼容的問題修正

#### 引用方式
```yaml
# 直接引用
gl.spec.naming_ontology:
  $ref: "ecosystem/contracts/naming-governance/gl-naming-ontology.yaml"

# 版本引用
gl.spec.naming_ontology.v1.0.0:
  $ref: "ecosystem/contracts/naming-governance/gl-naming-ontology.yaml#v1.0.0"

# 命名空間引用
gl.spec.platform:
  namespace: gl.platform
  contract: gl.contract.platform_definition
```

### 2.4 gl 策略（gl.policy）

#### 命名規則
- **格式**: gl.policy.{domain}.{policy_name}
- **範例**:
  - gl.policy.naming.prefix_required
  - gl.policy.governance.no_circular_deps
  - gl.policy.security.api_authentication

#### 條件格式
```yaml
gl.policy.naming.prefix_required:
  conditions:
    - field: name
      operator: starts_with
      value: "gl."
    - field: type
      operator: equals
      value: "entity"
  
  actions:
    - type: validate
      severity: critical
      message: "All entities must have 'gl.' prefix"
```

#### 優先級
- **100**: Critical（關鍵策略，必須滿足）
- **80**: High（高優先級策略）
- **60**: Medium（中等優先級策略）
- **40**: Low（低優先級策略）
- **20**: Info（信息級策略）

#### 實現範例
```python
class GLPolicy:
    def __init__(self, name: str, priority: int = 80):
        self.name = name
        self.priority = priority
        self.conditions = []
        self.actions = []
    
    def add_condition(self, field: str, operator: str, value: str):
        self.conditions.append({
            'field': field,
            'operator': operator,
            'value': value
        })
    
    def add_action(self, type: str, severity: str, message: str):
        self.actions.append({
            'type': type,
            'severity': severity,
            'message': message
        })
    
    def evaluate(self, data: dict) -> bool:
        """評估策略是否滿足"""
        for condition in self.conditions:
            if not self._evaluate_condition(condition, data):
                return False
        return True

# 使用範例
policy = GLPolicy("gl.policy.naming.prefix_required", priority=100)
policy.add_condition("name", "starts_with", "gl.")
policy.add_action("validate", "critical", "All entities must have 'gl.' prefix")

# 評估
result = policy.evaluate({"name": "gl.user"})
# result = True
```

### 2.5 gl 驗證器（gl.validator）

#### 規則
```yaml
gl.validator.naming:
  rules:
    - id: GL-NO-001
      name: "語意一致性"
      level: CRITICAL
      pattern: "^gl\\.[a-z_]+\\.[a-z_]+$"
      message: "命名必須遵循 gl.{layer}.{entity} 格式"
    
    - id: GL-NO-002
      name: "層級關係驗證"
      level: HIGH
      pattern: "^gl\\.(semantic|contract|platform|format)\\."
      message: "必須使用定義的命名層級"
```

#### 錯誤格式
```yaml
gl.validator.error:
  code: "GL-NO-001"
  level: "CRITICAL"
  message: "命名格式錯誤"
  details:
    field: "name"
    expected: "gl.semantic.entity.user"
    actual: "user"
    location: "line 10, column 5"
  suggestions:
    - "使用 gl.semantic.entity.user"
    - "檢查命名前綴"
```

#### 流程
```python
def validate_contract(contract_data: dict) -> ValidationResult:
    """
    驗證契約數據
    
    1. 檢查必填欄位
    2. 驗證字段類型
    3. 檢查命名規範
    4. 驗證引用完整性
    5. 檢查版本兼容性
    """
    result = ValidationResult()
    
    # 步驟 1: 檢查必填欄位
    for field in REQUIRED_FIELDS:
        if field not in contract_data:
            result.add_error(f"Missing required field: {field}")
    
    # 步驟 2: 驗證字段類型
    for field, expected_type in FIELD_TYPES.items():
        if field in contract_data:
            if not isinstance(contract_data[field], expected_type):
                result.add_error(
                    f"Field '{field}' must be {expected_type}, "
                    f"got {type(contract_data[field])}"
                )
    
    # 步驟 3: 檢查命名規範
    validator = GLNamingValidator()
    if 'name' in contract_data:
        if not validator.validate(contract_data['name'], NamingType.SEMANTIC_SHORT):
            result.add_errors(validator.violations)
    
    # 步驟 4: 驗證引用完整性
    if 'dependencies' in contract_data:
        for dep in contract_data['dependencies']:
            if not validate_contract_exists(dep):
                result.add_error(f"Dependency not found: {dep}")
    
    # 步驟 5: 檢查版本兼容性
    if 'version' in contract_data:
        if not is_version_compatible(contract_data['version']):
            result.add_error(f"Incompatible version: {contract_data['version']}")
    
    return result
```

### 2.6 gl 例外（gl.exception）

#### 錯誤碼
- **格式**: GL-{CATEGORY}-{NUMBER}
- **範例**:
  - GL-NO-001: Naming Ontology Error
  - GL-CP-002: Contract Policy Error
  - GL-VD-003: Validation Error

#### 分類
```yaml
exception_categories:
  - NO: Naming Ontology（命名本體）
  - CP: Contract Policy（契約策略）
  - VD: Validation（驗證）
  - GO: Governance（治理）
  - PL: Platform（平台）
  - SE: Security（安全）
  - OP: Operation（操作）
```

#### 訊息格式
```yaml
gl.exception.message:
  code: "GL-NO-001"
  category: "NAMING_ONTOLOGY"
  severity: "CRITICAL"
  message: "命名格式錯誤"
  details:
    field: "name"
    expected: "gl.semantic.entity.user"
    actual: "user"
    location: {
      file: "user.py",
      line: 10,
      column: 5
    }
  suggestions: [
    "使用 gl.semantic.entity.user",
    "檢查命名前綴"
  ]
```

#### 實現範例
```python
class GLException(Exception):
    def __init__(self, code: str, message: str, details: dict = None):
        self.code = code
        self.message = message
        self.details = details or {}
        self.category = code.split('-')[1] if '-' in code else 'UNKNOWN'
        self.severity = self._extract_severity()
    
    def _extract_severity(self) -> str:
        """從錯誤碼提取嚴重等級"""
        severity_map = {
            '001': 'CRITICAL',
            '002': 'HIGH',
            '003': 'MEDIUM',
            '004': 'LOW'
        }
        number = self.code.split('-')[-1]
        return severity_map.get(number, 'MEDIUM')
    
    def to_dict(self) -> dict:
        """轉換為字典格式"""
        return {
            'code': self.code,
            'category': self.category,
            'severity': self.severity,
            'message': self.message,
            'details': self.details
        }
    
    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"

# 使用範例
try:
    if not name.startswith('gl.'):
        raise GLException(
            code='GL-NO-001',
            message='命名格式錯誤',
            details={
                'field': 'name',
                'expected': 'gl.semantic.entity.user',
                'actual': name
            }
        )
except GLException as e:
    print(f"Error: {e}")
    print(f"Severity: {e.severity}")
    print(f"Details: {e.to_dict()}")
```

### 2.7 gl 審計事件（gl.audit_event）

#### 命名規則
- **格式**: gl.audit_event.{event_type}.{action}
- **範例**:
  - gl.audit_event.contract.created
  - gl.audit_event.policy.updated
  - gl.audit_event.validator.executed

#### 分類
```yaml
event_categories:
  contract:
    - created: 契約創建
    - updated: 契約更新
    - deleted: 契約刪除
    - validated: 契約驗證
  
  policy:
    - created: 策略創建
    - updated: 策略更新
    - deleted: 策略刪除
    - evaluated: 策略評估
  
  validator:
    - executed: 驗證器執行
    - passed: 驗證通過
    - failed: 驗證失敗
  
  audit:
    - started: 審計開始
    - completed: 審計完成
    - failed: 審計失敗
```

#### Payload 格式
```yaml
gl.audit_event.payload:
  event_id: "evt-20260201-001"
  event_type: "contract.created"
  timestamp: "2026-02-01T10:00:00Z"
  actor:
    type: "user"
    id: "user-123"
    name: "admin"
  
  target:
    type: "contract"
    id: "gl.contract.naming_ontology"
    version: "1.0.0"
  
  changes:
    added:
      - field: "description"
        value: "Updated description"
    modified:
      - field: "version"
        from: "1.0.0"
        to: "1.1.0"
    deleted: []
  
  metadata:
    source: "cli"
    request_id: "req-001"
    duration_ms: 125
```

#### 實現範例
```python
import json
from datetime import datetime
from typing import Dict, Any

class GLAuditEvent:
    def __init__(self, event_type: str, action: str):
        self.name = f"gl.audit_event.{event_type}.{action}"
        self.timestamp = datetime.utcnow().isoformat() + 'Z'
        self.event_id = self._generate_event_id()
        self.payload: Dict[str, Any] = {
            'event_id': self.event_id,
            'event_type': self.name,
            'timestamp': self.timestamp,
            'actor': {},
            'target': {},
            'changes': {},
            'metadata': {}
        }
    
    def _generate_event_id(self) -> str:
        """生成事件 ID"""
        date_str = datetime.utcnow().strftime("%Y%m%d")
        uuid = str(hash(self.timestamp))[:3]
        return f"evt-{date_str}-{uuid}"
    
    def set_actor(self, actor_type: str, actor_id: str, name: str = None):
        """設置執行者"""
        self.payload['actor'] = {
            'type': actor_type,
            'id': actor_id,
            'name': name or actor_id
        }
        return self
    
    def set_target(self, target_type: str, target_id: str, version: str = None):
        """設置目標對象"""
        target = {
            'type': target_type,
            'id': target_id
        }
        if version:
            target['version'] = version
        self.payload['target'] = target
        return self
    
    def add_change(self, change_type: str, **kwargs):
        """添加變更"""
        if change_type not in self.payload['changes']:
            self.payload['changes'][change_type] = []
        self.payload['changes'][change_type].append(kwargs)
        return self
    
    def to_json(self) -> str:
        """轉換為 JSON"""
        return json.dumps(self.payload, indent=2)

# 使用範例
event = GLAuditEvent('contract', 'created')
event.set_actor('user', 'user-123', 'admin')
event.set_target('contract', 'gl.contract.naming_ontology', '1.0.0')
event.add_change('added', field='description', value='New contract description')
event.add_change('added', field='version', value='1.0.0')

print(event.to_json())
```

### 2.8 gl 品質門檻（gl.quality_gate）

#### 類型
```yaml
quality_gate_types:
  - naming: 命名規範門檻
  - validation: 驗證規則門檻
  - coverage: 代碼覆蓋率門檻
  - performance: 性能門檻
  - security: 安全門檻
  - governance: 治理門檻
```

#### 條件
```yaml
gl.quality_gate.naming:
  type: naming
  conditions:
    - metric: "naming_compliance"
      operator: "greater_than_or_equal"
      value: 100
      
    - metric: "naming_violations"
      operator: "less_than"
      value: 0
  
  exceptions:
    - condition: "legacy_code"
      allowed_violations: 10
      reason: "遺留代碼逐步重構"
```

#### 失敗處理
```yaml
gl.quality_gate.failure_handling:
  on_failure:
    - action: "block_commit"
      message: "命名規範檢查失敗，請修復後重試"
    
    - action: "create_issue"
      repository: "MachineNativeOps/machine-native-ops"
      title: "Naming Convention Violation"
      labels: ["naming", "quality-gate"]
      
    - action: "notify_team"
      channels: ["#governance"]
      message: "品質門檻檢查失敗"
  
  on_warning:
    - action: "warn_user"
      message: "命名規範有警告，建議修復"
    
    - action: "log_event"
      level: "warning"
```

#### 實現範例
```python
from typing import List, Dict, Any
from enum import Enum

class QualityGateStatus(Enum):
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    SKIPPED = "skipped"

class GLQualityGate:
    def __init__(self, name: str, gate_type: str):
        self.name = name
        self.type = gate_type
        self.conditions = []
        self.exceptions = []
        self.failure_handlers = []
    
    def add_condition(self, metric: str, operator: str, value: Any):
        """添加條件"""
        self.conditions.append({
            'metric': metric,
            'operator': operator,
            'value': value
        })
        return self
    
    def add_exception(self, condition: str, **kwargs):
        """添加例外"""
        self.exceptions.append({
            'condition': condition,
            **kwargs
        })
        return self
    
    def add_failure_handler(self, action: str, **kwargs):
        """添加失敗處理器"""
        self.failure_handlers.append({
            'action': action,
            **kwargs
        })
        return self
    
    def evaluate(self, metrics: Dict[str, Any]) -> QualityGateStatus:
        """評估品質門檻"""
        for condition in self.conditions:
            metric = condition['metric']
            operator = condition['operator']
            expected_value = condition['value']
            actual_value = metrics.get(metric)
            
            if not self._compare(actual_value, operator, expected_value):
                # 檢查是否有例外
                for exception in self.exceptions:
                    if exception['condition'] == metric:
                        return QualityGateStatus.WARNING
                
                return QualityGateStatus.FAILED
        
        return QualityGateStatus.PASSED
    
    def _compare(self, actual: Any, operator: str, expected: Any) -> bool:
        """比較值"""
        operators = {
            'equals': lambda a, b: a == b,
            'not_equals': lambda a, b: a != b,
            'greater_than': lambda a, b: a > b,
            'less_than': lambda a, b: a < b,
            'greater_than_or_equal': lambda a, b: a >= b,
            'less_than_or_equal': lambda a, b: a <= b,
        }
        return operators.get(operator, lambda a, b: False)(actual, expected)
    
    def handle_failure(self, status: QualityGateStatus):
        """處理失敗"""
        if status == QualityGateStatus.FAILED:
            for handler in self.failure_handlers:
                action = handler['action']
                if action == 'block_commit':
                    raise Exception(handler.get('message', 'Commit blocked'))
                elif action == 'create_issue':
                    # 創建 issue
                    pass
                elif action == 'notify_team':
                    # 通知團隊
                    pass

# 使用範例
gate = GLQualityGate('gl.quality_gate.naming', 'naming')
gate.add_condition('naming_compliance', 'greater_than_or_equal', 100)
gate.add_condition('naming_violations', 'less_than', 0)
gate.add_exception('legacy_code', allowed_violations=10, reason='遺留代碼')
gate.add_failure_handler('block_commit', message='命名規範檢查失敗')

# 評估
metrics = {
    'naming_compliance': 100,
    'naming_violations': 0
}

status = gate.evaluate(metrics)
if status != QualityGateStatus.PASSED:
    gate.handle_failure(status)
else:
    print("✅ Quality gate passed")
```

---

## 實現指南

### Python 實現範例

```python
# contracts/gl_contract.py
from typing import Dict, Any, Optional
from datetime import datetime
import json

class GLContract:
    """GL 契約基類"""
    
    def __init__(
        self,
        contract_id: str,
        version: str,
        contract_type: str,
        status: str = 'active'
    ):
        self.id = contract_id
        self.version = version
        self.type = contract_type
        self.status = status
        self.spec = {}
        self.metadata = {}
        self.dependencies = []
        self.validation_rules = []
        self.governance = []
    
    def to_dict(self) -> Dict[str, Any]:
        """轉換為字典"""
        return {
            'id': self.id,
            'version': self.version,
            'type': self.type,
            'status': self.status,
            'spec': self.spec,
            'metadata': self.metadata,
            'dependencies': self.dependencies,
            'validation_rules': self.validation_rules,
            'governance': self.governance
        }
    
    def to_yaml(self) -> str:
        """轉換為 YAML"""
        import yaml
        return yaml.dump(self.to_dict(), default_flow_style=False)
    
    def validate(self) -> ValidationResult:
        """驗證契約"""
        validator = GLContractValidator()
        return validator.validate(self)

# 使用範例
contract = GLContract(
    contract_id='gl.contract.naming_ontology',
    version='1.0.0',
    contract_type='core',
    status='active'
)

contract.spec = {
    'layers': ['semantic', 'contract', 'platform'],
    'rules': {'prefix_required': True}
}

result = contract.validate()
if result.is_valid():
    print("✅ Contract is valid")
else:
    print("❌ Contract validation failed:")
    for error in result.errors:
        print(f"  - {error}")
```

### 驗證器實現

```python
# validators/gl_contract_validator.py
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class ValidationError:
    """驗證錯誤"""
    code: str
    message: str
    field: str
    expected: Any
    actual: Any

class ValidationResult:
    """驗證結果"""
    
    def __init__(self):
        self.errors: List[ValidationError] = []
        self.warnings: List[str] = []
    
    def add_error(self, error: ValidationError):
        self.errors.append(error)
    
    def add_warning(self, warning: str):
        self.warnings.append(warning)
    
    def is_valid(self) -> bool:
        return len(self.errors) == 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'valid': self.is_valid(),
            'errors': [
                {
                    'code': e.code,
                    'message': e.message,
                    'field': e.field,
                    'expected': e.expected,
                    'actual': e.actual
                }
                for e in self.errors
            ],
            'warnings': self.warnings
        }

class GLContractValidator:
    """GL 契約驗證器"""
    
    REQUIRED_FIELDS = ['id', 'version', 'type', 'status']
    FIELD_TYPES = {
        'id': str,
        'version': str,
        'type': str,
        'status': str,
        'spec': dict,
        'metadata': dict
    }
    
    def __init__(self):
        self.policies = []
    
    def validate(self, contract: GLContract) -> ValidationResult:
        """驗證契約"""
        result = ValidationResult()
        
        # 檢查必填欄位
        for field in self.REQUIRED_FIELDS:
            if not hasattr(contract, field) or getattr(contract, field) is None:
                result.add_error(ValidationError(
                    code='GL-CP-001',
                    message=f'Missing required field: {field}',
                    field=field,
                    expected='present',
                    actual=None
                ))
        
        # 檢查字段類型
        contract_dict = contract.to_dict()
        for field, expected_type in self.FIELD_TYPES.items():
            if field in contract_dict:
                actual = contract_dict[field]
                if not isinstance(actual, expected_type):
                    result.add_error(ValidationError(
                        code='GL-CP-002',
                        message=f'Field type mismatch',
                        field=field,
                        expected=expected_type.__name__,
                        actual=type(actual).__name__
                    ))
        
        # 檢查命名規範
        if hasattr(contract, 'id'):
            if not contract.id.startswith('gl.contract.'):
                result.add_error(ValidationError(
                    code='GL-NO-001',
                    message='Contract ID must start with gl.contract.',
                    field='id',
                    expected='gl.contract.*',
                    actual=contract.id
                ))
        
        # 評估策略
        for policy in self.policies:
            if not policy.evaluate(contract_dict):
                result.add_warning(f"Policy {policy.name} not satisfied")
        
        return result
```

## 最佳實踐

### 1. 契約設計
- 保持契約簡潔明確
- 使用語意化的命名
- 提供清晰的文檔和範例
- 支持版本演進

### 2. 策略管理
- 使用清晰的優先級
- 提供詳細的錯誤訊息
- 支持策略組合
- 允許例外處理

### 3. 驗證實現
- 盡早驗證
- 提供有用的錯誤訊息
- 支持批量驗證
- 集成到 CI/CD

### 4. 品質門檻
- 設定合理的門檻值
- 支持漸進式採用
- 提供清晰的失敗處理
- 支持例外情況

## 集成示例

### CI/CD 集成

```yaml
# .github/workflows/quality-gate.yml
name: Quality Gate Validation

on: [push, pull_request]

jobs:
  validate-contracts:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Validate naming conventions
        run: |
          python3 gl-governance-compliance/scripts/naming/gl_naming_validator.py \
            semantic-node entity user
      
      - name: Check quality gates
        run: |
          python3 scripts/check_quality_gates.py
      
      - name: Create issue on failure
        if: failure()
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: 'Quality Gate Failed',
              body: 'Naming convention validation failed'
            })
```

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash

echo "Running GL quality gates..."

# 驗證命名規範
python3 gl-governance-compliance/scripts/naming/gl_naming_validator.py \
  semantic-node entity user

# 檢查品質門檻
python3 scripts/check_quality_gates.py

echo "Quality gate validation complete!"
```

---

**文檔版本**: 1.0.0  
**最後更新**: 2026-02-01  
**維護者**: GL Governance Team  
**狀態**: ACTIVE
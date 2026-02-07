# GL 格式層（Format Layer）規範

## 版本資訊
- **版本**: 1.0.0
- **日期**: 2026-02-01
- **狀態**: ACTIVE
- **適用範圍**: 所有 GL 格式文件（YAML、JSON、K8s、Helm、GitOps、Terraform、OpenAPI、Docker、Markdown、Rego）

---

## 4. 格式層（Format Layer）

### 4.1 gl YAML（gl.yaml.xxx）

#### gl.yaml.key 命名
- **格式**: gl.yaml.{category}.{key_name}
- **範例**:
  - gl.yaml.api.timeout
  - gl.yaml.db.connection_string
  - gl.yaml.secret.api_key

#### 層級結構
```yaml
gl.yaml.structure:
  version: "1.0"
  apiVersion: "config.gl/v1"
  kind: Config
  metadata:
    name: gl.config
    labels:
      gl.config.type: "runtime"
  spec:
    configuration:
      api:
        timeout: "30s"
        retry: 3
      database:
        host: "localhost"
        port: 5432
      secrets:
        api_key: "secret-value"
```

#### gl.yaml.anchor 規則
```yaml
# Anchor 定義
anchors:
  default_timeout: &default_timeout "30s"
  retry_policy: &retry_policy
    count: 3
    backoff: "exponential"

# Anchor 引用
api:
  timeout: *default_timeout
  retry: *retry_policy

data:
  timeout: *default_timeout
```

#### 實現範例
```python
class GLYAML:
    def __init__(self, yaml_content: str = None):
        self.content = yaml_content or ""
        self.data = {}
        self.anchors = {}
    
    def load(self, file_path: str):
        """加載 YAML 文件"""
        import yaml
        with open(file_path, 'r') as f:
            self.content = f.read()
        self.data = yaml.safe_load(self.content)
    
    def save(self, file_path: str):
        """保存 YAML 文件"""
        import yaml
        with open(file_path, 'w') as f:
            yaml.dump(self.data, f, default_flow_style=False)
    
    def set_key(self, key: str, value: any):
        """設置鍵值"""
        keys = key.split('.')
        data = self.data
        for k in keys[:-1]:
            if k not in data:
                data[k] = {}
            data = data[k]
        data[keys[-1]] = value
    
    def get_key(self, key: str) -> any:
        """獲取鍵值"""
        keys = key.split('.')
        data = self.data
        for k in keys:
            if isinstance(data, dict) and k in data:
                data = data[k]
            else:
                return None
        return data
```

### 4.2 gl JSON（gl.json.xxx）

#### gl.json.key 命名
- **格式**: gl.json.{category}.{key_name}
- **範例**:
  - gl.json.api.endpoint
  - gl.json.user.id
  - gl.json.order.total

#### gl.json.pointer
- **格式**: /{path}/{to}/{key}
- **範例**:
  - /api/users/0/id
  - /data/items/2/name
  - /config/timeout

#### gl.json.schema 命名
- **格式**: gl.json.schema.{schema_name}
- **範例**:
  - gl.json.schema.user
  - gl.json.schema.order
  - gl.json.schema.event

#### 實現範例
```python
class GLJSON:
    def __init__(self, json_content: str = None):
        self.content = json_content or ""
        self.data = {}
        self.schemas = {}
    
    def load(self, file_path: str):
        """加載 JSON 文件"""
        import json
        with open(file_path, 'r') as f:
            self.content = f.read()
        self.data = json.loads(self.content)
    
    def save(self, file_path: str):
        """保存 JSON 文件"""
        import json
        with open(file_path, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def get_pointer(self, pointer: str) -> any:
        """獲取 JSON Pointer 指向的值"""
        import jsonpointer
        return jsonpointer.resolve_pointer(self.data, pointer)
    
    def set_pointer(self, pointer: str, value: any):
        """設置 JSON Pointer 指向的值"""
        import jsonpointer
        jsonpointer.set_pointer(self.data, pointer, value)
    
    def add_schema(self, schema_name: str, schema: dict):
        """添加 JSON Schema"""
        self.schemas[schema_name] = schema
    
    def validate(self, schema_name: str) -> bool:
        """驗證 JSON Schema"""
        from jsonschema import validate
        if schema_name in self.schemas:
            try:
                validate(instance=self.data, schema=self.schemas[schema_name])
                return True
            except:
                return False
        return False
```

### 4.3 gl K8s（gl.k8s.xxx）

#### gl.k8s.metadata.name
- **格式**: gl-{platform}-{type}
- **範例**:
  - gl-runtime-pod
  - gl-data-deployment
  - gl-api-service

#### gl.k8s.label
- **格式**: gl.{category}.{name}
- **範例**:
  - gl.platform.runtime
  - gl.service.users
  - gl.version.v1.0.0

#### gl.k8s.annotation
- **格式**: gl.{category}.{annotation_name}
- **範例**:
  - gl.description.short
  - gl.owner.team
  - gl.deployment.date

#### gl.k8s.crd 命名
- **格式**: {plural}.{group}
- **範例**:
  - glplatforms.gl
  - glcomponents.gl
  - glservices.gl

#### 實現範例
```python
class GLK8s:
    def __init__(self):
        self.resources = []
    
    def create_pod(self, name: str, labels: dict = None, annotations: dict = None):
        """創建 Pod"""
        metadata = {
            'name': name,
            'labels': labels or {},
            'annotations': annotations or {}
        }
        
        # 添加 GL 標籤
        if 'labels' in metadata:
            metadata['labels'].update({
                'gl.platform.runtime': 'true',
                'gl.version': 'v1.0.0'
            })
        
        pod = {
            'apiVersion': 'v1',
            'kind': 'Pod',
            'metadata': metadata,
            'spec': {
                'containers': [{
                    'name': name,
                    'image': f'gl-{name}:v1.0.0',
                    'env': [
                        {
                            'name': 'gl.env.api.timeout',
                            'value': '30s'
                        }
                    ]
                }]
            }
        }
        
        self.resources.append(pod)
        return pod
    
    def create_deployment(self, name: str, replicas: int = 1):
        """創建 Deployment"""
        deployment = {
            'apiVersion': 'apps/v1',
            'kind': 'Deployment',
            'metadata': {
                'name': name,
                'labels': {
                    'gl.platform.runtime': 'true',
                    'gl.version': 'v1.0.0'
                }
            },
            'spec': {
                'replicas': replicas,
                'selector': {
                    'matchLabels': {
                        'app': name
                    }
                },
                'template': {
                    'metadata': {
                        'labels': {
                            'app': name,
                            'gl.platform.runtime': 'true'
                        }
                    },
                    'spec': {
                        'containers': [{
                            'name': name,
                            'image': f'gl-{name}:v1.0.0'
                        }]
                    }
                }
            }
        }
        
        self.resources.append(deployment)
        return deployment
    
    def save_yaml(self, file_path: str):
        """保存為 YAML"""
        import yaml
        with open(file_path, 'w') as f:
            for resource in self.resources:
                f.write('---\n')
                yaml.dump(resource, f, default_flow_style=False)
```

### 4.4 gl Helm（gl.helm.xxx）

#### gl.helm.chart 命名
- **格式**: gl-{platform}-{chart}
- **範例**:
  - gl-runtime-chart
  - gl-data-chart
  - gl-api-chart

#### gl.helm.release 命名
- **格式**: gl-{platform}-{env}
- **範例**:
  - gl-runtime-prod
  - gl-data-staging
  - gl-api-dev

#### gl.helm.values.key 命名
- **格式**: gl.{category}.{key_name}
- **範例**:
  - gl.image.tag
  - gl.service.port
  - gl.resources.cpu

#### 實現範例
```python
class GLHelm:
    def __init__(self, chart_name: str):
        self.chart_name = chart_name
        self.values = {}
        self.templates = []
    
    def create_chart(self, name: str, version: str = "1.0.0"):
        """創建 Helm Chart"""
        chart = {
            'apiVersion': 'v2',
            'name': name,
            'description': f'GL {name} Chart',
            'type': 'application',
            'version': version,
            'appVersion': version
        }
        return chart
    
    def set_value(self, key: str, value: any):
        """設置 Values"""
        keys = key.split('.')
        data = self.values
        for k in keys[:-1]:
            if k not in data:
                data[k] = {}
            data = data[k]
        data[keys[-1]] = value
    
    def get_value(self, key: str) -> any:
        """獲取 Value"""
        keys = key.split('.')
        data = self.values
        for k in keys:
            if isinstance(data, dict) and k in data:
                data = data[k]
            else:
                return None
        return data
    
    def add_template(self, template_name: str, content: str):
        """添加模板"""
        self.templates.append({
            'name': template_name,
            'content': content
        })
    
    def generate_release(self, release_name: str) -> dict:
        """生成 Release 配置"""
        return {
            'name': release_name,
            'chart': self.chart_name,
            'values': self.values
        }
```

### 4.5 gl GitOps（gl.gitops.xxx）

#### gl.gitops.application 命名
- **格式**: gl-{platform}-application
- **範例**:
  - gl-runtime-application
  - gl-data-application
  - gl-api-application

#### gl.gitops.sync_policy 命名
- **格式**: gl-{platform}-sync-policy
- **範例**:
  - gl-runtime-sync-policy
  - gl-data-sync-policy

#### gl.gitops.overlay 命名
- **格式**: gl-{platform}-{env}-overlay
- **範例**:
  - gl-runtime-prod-overlay
  - gl-data-staging-overlay

#### 實現範例
```python
class GLGitOps:
    def __init__(self):
        self.applications = []
        self.sync_policies = []
        self.overlays = []
    
    def create_application(self, name: str, repo_url: str):
        """創建 Application"""
        application = {
            'apiVersion': 'argoproj.io/v1alpha1',
            'kind': 'Application',
            'metadata': {
                'name': name,
                'labels': {
                    'gl.platform.runtime': 'true'
                }
            },
            'spec': {
                'project': 'gl-platforms',
                'source': {
                    'repoURL': repo_url,
                    'targetRevision': 'main'
                },
                'destination': {
                    'server': 'https://kubernetes.default.svc',
                    'namespace': name
                },
                'syncPolicy': {
                    'automated': {
                        'prune': True,
                        'selfHeal': True
                    }
                }
            }
        }
        
        self.applications.append(application)
        return application
    
    def create_sync_policy(self, name: str, applications: list):
        """創建 Sync Policy"""
        policy = {
            'apiVersion': 'argoproj.io/v1alpha1',
            'kind': 'ApplicationSet',
            'metadata': {
                'name': name
            },
            'spec': {
                'generators': [
                    {
                        'list': {
                            'elements': applications
                        }
                    }
                ],
                'template': {
                    'metadata': {
                        'name': '{{name}}',
                        'labels': {
                            'gl.platform.runtime': 'true'
                        }
                    }
                }
            }
        }
        
        self.sync_policies.append(policy)
        return policy
```

### 4.6 gl Terraform（gl.tf.xxx）

#### gl.tf.resource 命名
- **格式**: gl_{resource}_{type}
- **範例**:
  - gl_pod_compute
  - gl_deployment_web
  - gl_service_api

#### gl.tf.module 命名
- **格式**: gl-{platform}-module
- **範例**:
  - gl-runtime-module
  - gl-data-module
  - gl-api-module

#### gl.tf.variable 命名
- **格式**: gl_{category}_{variable_name}
- **範例**:
  - gl_cluster_name
  - gl_node_count
  - gl_disk_size

#### 實現範例
```python
class GLTerraform:
    def __init__(self):
        self.resources = []
        self.variables = {}
        self.outputs = {}
    
    def add_resource(self, resource_type: str, resource_name: str, config: dict):
        """添加 Terraform Resource"""
        resource = {
            'resource': {
                resource_type: {
                    resource_name: config
                }
            }
        }
        self.resources.append(resource)
        return resource
    
    def add_variable(self, name: str, default: any = None, description: str = ""):
        """添加 Variable"""
        variable = {
            'variable': {
                name: {
                    'default': default,
                    'description': description
                }
            }
        }
        self.variables[name] = variable
        return variable
    
    def add_output(self, name: str, value: str, description: str = ""):
        """添加 Output"""
        output = {
            'output': {
                name: {
                    'value': value,
                    'description': description
                }
            }
        }
        self.outputs[name] = output
        return output
    
    def generate_hcl(self) -> str:
        """生成 HCL 代碼"""
        hcl = []
        
        # Variables
        for var in self.variables.values():
            hcl.append('variable "{}" {{'.format(list(var['variable'].keys())[0]))
            hcl.append('  description = "{}"'.format(var['variable'][list(var['variable'].keys())[0]].get('description', '')))
            hcl.append('  default     = {}'.format(var['variable'][list(var['variable'].keys())[0]]['default'])))
            hcl.append('}\n')
        
        # Resources
        for resource in self.resources:
            hcl.append(str(resource))
        
        # Outputs
        for output in self.outputs.values():
            hcl.append(str(output))
        
        return '\n'.join(hcl)
```

### 4.7 gl OpenAPI（gl.oas.xxx）

#### gl.oas.path 命名
- **格式**: /gl/{domain}/{service}/{action}
- **範例**:
  - /gl/api/users/list
  - /gl/runtime/jobs/create
  - /gl/data/query/execute

#### gl.oas.schema 命名
- **格式**: gl.schema.{schema_name}
- **範例**:
  - gl.schema.user
  - gl.schema.order
  - gl.schema.event

#### gl.oas.parameter 命名
- **格式**: {parameter_name}
- **範例**:
  - user_id
  - page
  - limit
  - sort_by

#### 實現範例
```python
class GLOpenAPI:
    def __init__(self, title: str, version: str = "1.0.0"):
        self.spec = {
            'openapi': '3.0.0',
            'info': {
                'title': title,
                'version': version
            },
            'paths': {},
            'components': {
                'schemas': {}
            }
        }
    
    def add_path(self, path: str, method: str, description: str = ""):
        """添加 Path"""
        if path not in self.spec['paths']:
            self.spec['paths'][path] = {}
        
        operation = {
            'summary': description,
            'responses': {
                '200': {
                    'description': 'Success',
                    'content': {
                        'application/json': {
                            'schema': {
                                'type': 'object'
                            }
                        }
                    }
                }
            }
        }
        
        self.spec['paths'][path][method.lower()] = operation
        return operation
    
    def add_schema(self, schema_name: str, schema: dict):
        """添加 Schema"""
        self.spec['components']['schemas'][schema_name] = schema
    
    def generate_spec(self) -> dict:
        """生成 OpenAPI Spec"""
        return self.spec
```

### 4.8 gl Docker（gl.docker.xxx）

#### gl.docker.image 命名
- **格式**: gl-{platform}:{version}
- **範例**:
  - gl-runtime:v1.0.0
  - gl-data:v1.2.3
  - gl-api:latest

#### gl.docker.tag 命名
- **格式**: v{major}.{minor}.{patch}
- **範例**:
  - v1.0.0
  - v1.2.3
  - latest

#### gl.docker.container 命名
- **格式**: gl-{platform}-{type}
- **範例**:
  - gl-runtime-container
  - gl-data-container
  - gl-api-container

#### 實現範例
```python
class GLDocker:
    def __init__(self, platform_name: str):
        self.platform_name = platform_name
        self.image = f"gl-{platform_name}"
        self.tag = "v1.0.0"
        self.dockerfile = []
    
    def set_from(self, base_image: str):
        """設置 FROM"""
        self.dockerfile.append(f"FROM {base_image}")
    
    def add_run(self, command: str):
        """添加 RUN"""
        self.dockerfile.append(f"RUN {command}")
    
    def add_copy(self, source: str, dest: str):
        """添加 COPY"""
        self.dockerfile.append(f"COPY {source} {dest}")
    
    def add_cmd(self, command: str):
        """添加 CMD"""
        self.dockerfile.append(f'CMD ["{command}"]')
    
    def add_env(self, key: str, value: str):
        """添加 ENV"""
        self.dockerfile.append(f"ENV {key}={value}")
    
    def generate_dockerfile(self) -> str:
        """生成 Dockerfile"""
        return '\n'.join(self.dockerfile)
    
    def save_dockerfile(self, file_path: str):
        """保存 Dockerfile"""
        with open(file_path, 'w') as f:
            f.write(self.generate_dockerfile())
```

### 4.9 gl Markdown（gl.md.xxx）

#### gl.md.heading 命名
- **格式**: #{level} {heading}
- **範例**:
  - # GL API Reference
  - ## Platform Overview
  - ### Configuration Guide

#### gl.md.block 命名
- **格式**: ```{language}
- **範例**:
  - ```python
  - ```yaml
  - ```bash

#### 實現範例
```python
class GLMarkdown:
    def __init__(self):
        self.content = []
    
    def add_heading(self, level: int, text: str):
        """添加標題"""
        heading = f"{'#' * level} {text}"
        self.content.append(heading)
    
    def add_paragraph(self, text: str):
        """添加段落"""
        self.content.append(text)
    
    def add_code_block(self, language: str, code: str):
        """添加代碼塊"""
        self.content.append(f"```{language}")
        self.content.append(code)
        self.content.append("```")
    
    def add_list(self, items: list):
        """添加列表"""
        for item in items:
            self.content.append(f"- {item}")
    
    def generate_markdown(self) -> str:
        """生成 Markdown"""
        return '\n'.join(self.content)
    
    def save_markdown(self, file_path: str):
        """保存 Markdown 文件"""
        with open(file_path, 'w') as f:
            f.write(self.generate_markdown())
```

### 4.10 gl Rego（gl.rego.xxx）

#### gl.rego.policy 命名
- **格式**: gl_policy_{policy_name}
- **範例**:
  - gl_policy_prefix_required
  - gl_policy_no_circular_deps
  - gl_policy_api_authentication

#### gl.rego.rule 命名
- **格式**: gl_rule_{rule_name}
- **範例**:
  - gl_rule_check_prefix
  - gl_rule_validate_format
  - gl_rule_enforce_policy

#### 實現範例
```rego
# gl_policy_prefix_required.rego
package gl.policies.prefix

default allow = false

allow {
    input.name
    startswith(input.name, "gl.")
}

# gl_rule_check_prefix.rego
package gl.rules.prefix

check_prefix[name] {
    name := input.name
    startswith(name, "gl.")
}

# gl_policy_no_circular_deps.rego
package gl.policies.circular_deps

default allow = false

allow {
    not has_circular_dep(input.dependencies)
}

has_circular_dep(deps) {
    some dep in deps
    dep in input.dependencies
}

# gl_policy_api_authentication.rego
package gl.policies.api_auth

default allow = false

allow {
    input.authentication_required
    input.authenticated
}

deny[msg] {
    not input.authentication_required
    msg := "API authentication is required"
}

deny[msg] {
    input.authentication_required
    not input.authenticated
    msg := "User is not authenticated"
}
```

---

## 實現指南

### 綜合使用範例

```python
# 創建 YAML 配置
yaml_config = GLYAML()
yaml_config.set_key('gl.yaml.api.timeout', '30s')
yaml_config.set_key('gl.yaml.db.host', 'localhost')
yaml_config.save_yaml('/tmp/config.yaml')

# 創建 JSON 配置
json_config = GLJSON()
json_config.set_pointer('/api/endpoint', '/gl/api/users')
json_config.set_pointer('/data/items/0/id', 'user-001')
json_config.save_json('/tmp/config.json')

# 創建 K8s Pod
k8s = GLK8s()
pod = k8s.create_pod(
    name='gl-runtime-pod',
    labels={'gl.platform.runtime': 'true'},
    annotations={'gl.owner.team': 'devops'}
)
k8s.save_yaml('/tmp/pod.yaml')

# 創建 Helm Chart
helm = GLHelm('gl-runtime-chart')
helm.set_value('gl.image.tag', 'v1.0.0')
helm.set_value('gl.service.port', 8080)
chart = helm.create_chart('gl-runtime', version='1.0.0')

# 創建 GitOps Application
gitops = GLGitOps()
app = gitops.create_application(
    name='gl-runtime-application',
    repo_url='https://github.com/gl/runtime-platform.git'
)

# 創建 Terraform Resource
tf = GLTerraform()
tf.add_resource('kubernetes_pod', 'gl_pod_compute', {
    'metadata': {
        'name': 'gl-pod',
        'labels': {'gl.platform.runtime': 'true'}
    }
})

# 創建 OpenAPI Spec
oas = GLOpenAPI('GL API', version='1.0.0')
oas.add_path('/gl/api/users/list', 'get', 'List all users')
oas.add_schema('gl.schema.user', {
    'type': 'object',
    'properties': {
        'id': {'type': 'string'},
        'name': {'type': 'string'}
    }
})

# 創建 Docker Image
docker = GLDocker('runtime')
docker.set_from('python:3.11')
docker.add_copy('requirements.txt', '/app/')
docker.add_run('pip install -r requirements.txt')
dockerfile = docker.generate_dockerfile()
```

## 集成示例

### Docker Compose 示例

```yaml
version: "3.8"

services:
  gl-runtime:
    image: gl-runtime:v1.0.0
    environment:
      - gl.env.api.timeout=30s
      - gl.env.db.host=postgres
    labels:
      gl.platform.runtime: "true"
      gl.version: "v1.0.0"
    ports:
      - "8080:8080"
```

### Kubernetes Deployment 示例

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gl-runtime-deployment
  labels:
    gl.platform.runtime: "true"
    gl.version: "v1.0.0"
spec:
  replicas: 3
  selector:
    matchLabels:
      app: gl-runtime
      gl.platform.runtime: "true"
  template:
    metadata:
      labels:
        app: gl-runtime
        gl.platform.runtime: "true"
    spec:
      containers:
      - name: gl-runtime
        image: gl-runtime:v1.0.0
        env:
        - name: gl.env.api.timeout
          value: "30s"
        - name: gl.env.db.host
          value: "localhost"
```

## 最佳實踐

### 1. 命名一致性
- 所有格式使用統一的 gl 前綴
- 遵循各種格式的命名約定
- 保持命名簡潔明了

### 2. 模塊化設計
- 每個格式類職責單一
- 格式間低耦合
- 清晰的接口定義

### 3. 文檔化
- 為每個格式提供文檔
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
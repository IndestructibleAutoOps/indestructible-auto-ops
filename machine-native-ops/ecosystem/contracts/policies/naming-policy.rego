# @GL-governed
# @GL-layer: GQS-L2
# @GL-semantic: naming-policy
# @GL-audit-trail: ./governance/GL_SEMANTIC_ANCHOR.json

---
# Naming Policy - OPA Rego
# 命名政策 - OPA Rego 規則
#
# Purpose: 驗證資源命名是否符合治理規範
# Version: 1.0.0

package governance.naming

import input

# Default deny
default allow = false

# ============================================================================
# 命名模式定義
# ============================================================================

# 資源命名模式: ^(dev|staging|prod)-[a-z0-9-]+-(deploy|svc|ing|cm|secret)-v\d+.\d+.\d+(-[A-Za-z0-9]+)?$
# 示例: dev-myapp-svc-v1.0.0-release
resource_name_pattern = "^%s-%s-%s-v%s%s$" % {
  environment,
  resource_name,
  resource_type,
  version,
  optional_suffix
}

# 環境前綴
valid_environments = ["dev", "staging", "prod"]

# 資源類型
valid_resource_types = {
  "deploy": "deployment",
  "svc": "service",
  "ing": "ingress",
  "cm": "configmap",
  "secret": "secret"
}

# 版本模式 (vX.Y.Z)
version_pattern = "^v\\d+\\.\\d+\\.\\d+$"

# ============================================================================
# 允許條件
# ============================================================================

allow {
  # 檢查是否有規則明確拒絕
  not deny
}

# ============================================================================
# 拒絕條件
# ============================================================================

deny[msg] {
  # 檢查 Kubernetes 資源命名
  input.kind
  input.metadata.name
  
  # 無效的環境前綴
  not valid_environment_prefix
  
  msg := sprintf("Resource '%s' has invalid environment prefix. Must be one of: %v", [
    input.metadata.name,
    valid_environments
  ])
}

deny[msg] {
  # 檢查 Kubernetes 資源命名
  input.kind
  input.metadata.name
  
  # 無效的資源類型
  not valid_resource_type_suffix
  
  msg := sprintf("Resource '%s' has invalid resource type suffix. Must be one of: %v", [
    input.metadata.name,
    object.keys(valid_resource_types)
  ])
}

deny[msg] {
  # 檢查 Kubernetes 資源命名
  input.kind
  input.metadata.name
  
  # 無效的版本格式
  not valid_version_format
  
  msg := sprintf("Resource '%s' has invalid version format. Must match vX.Y.Z", [
    input.metadata.name
  ])
}

deny[msg] {
  # 檢查 Kubernetes 資源命名
  input.kind
  input.metadata.name
  
  # 名稱過長（超過 63 字符）
  count(input.metadata.name) > 63
  
  msg := sprintf("Resource '%s' name is too long. Maximum 63 characters", [
    input.metadata.name
  ])
}

deny[msg] {
  # 檢查 Kubernetes 資源命名
  input.kind
  input.metadata.name
  
  # 包含大寫字母
  is_upper_case(input.metadata.name)
  
  msg := sprintf("Resource '%s' contains uppercase letters. Names must be lowercase", [
    input.metadata.name
  ])
}

deny[msg] {
  # 檢查 Kubernetes 資源命名
  input.kind
  input.metadata.name
  
  # 包含無效字符
  invalid_chars(input.metadata.name)
  
  msg := sprintf("Resource '%s' contains invalid characters. Only lowercase letters, numbers, and hyphens are allowed", [
    input.metadata.name
  ])
}

# ============================================================================
# 驗證輔助函數
# ============================================================================

# 檢查環境前綴
valid_environment_prefix {
  some prefix
  prefix := input.metadata.name[0:count(prefix)]
  prefix in valid_environments
}

# 檢查資源類型後綴
valid_resource_type_suffix {
  some type_suffix
  type_suffix := input.metadata.name[-count(type_suffix):-1]
  type_suffix in object.keys(valid_resource_types)
}

# 檢查版本格式
valid_version_format {
  regex.match(version_pattern, input.metadata.name)
}

# 檢查是否包含大寫字母
is_upper_case(name) {
  some i
  i := count(split(name, "")) - 1
  i >= 0
  upper_case(split(name, "")[i])
}

# 檢查是否包含無效字符
invalid_chars(name) {
  some char
  char := split(name, "")[i]
  i := count(split(name, "")) - 1
  i >= 0
  not regex.match("^[a-z0-9-]$", char)
}

# ============================================================================
# 命名建議
# ============================================================================

# 生成正確的命名建議
suggest_name[msg] {
  input.kind
  input.metadata.name
  
  # 嘗試提取資源類型
  some type_suffix
  type_suffix := input.metadata.name[-count(type_suffix):-1]
  type_suffix in object.keys(valid_resource_types)
  
  # 建議的命名
  suggested := sprintf("%s-%s-%s-v1.0.0", [
    "dev",
    "myapp",
    type_suffix
  ])
  
  msg := sprintf("Consider using: %s (based on detected type: %s)", [
    suggested,
    valid_resource_types[type_suffix]
  ])
}

# ============================================================================
# 元數據
# ============================================================================

# 返回策略元數據
metadata := {
  "name": "naming-policy",
  "version": "1.0.0",
  "description": "Enforces resource naming conventions",
  "severity": "blocking",
  "category": "governance"
}
package naming_policy

# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: naming-policy-conftest
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json

import future.keywords.contains
import future.keywords.if

# Naming pattern validation
kubernetes_resource_pattern = "^(dev|staging|prod)-[a-z0-9-]+-(deploy|svc|ing|cm|secret)-v[0-9]+\\.[0-9]+\\.[0-9]+(-[A-Za-z0-9]+)?$"

deny[msg] if {
    input.kind
    name := input.metadata.name
    not regex.match(kubernetes_resource_pattern, name)
    msg := sprintf("Kubernetes resource name '%s' violates naming policy. Pattern: %s", [name, kubernetes_resource_pattern])
}

# Validate labels exist
deny[msg] if {
    input.kind
    not input.metadata.labels
    msg := "Missing required labels"
}

# Validate specific required labels
deny[msg] if {
    input.kind
    required_label := ["app", "version", "environment"]
    not required_label[_] == input.metadata.labels[_]
    msg := sprintf("Missing required label: %s", [required_label])
}

# Validate environment label value
deny[msg] if {
    input.kind
    input.metadata.labels.environment
    not input.metadata.labels.environment in ["dev", "staging", "prod"]
    msg := sprintf("Invalid environment label: %s (must be dev, staging, or prod)", [input.metadata.labels.environment])
}

# Validate namespace naming
deny[msg] if {
    input.kind == "Namespace"
    name := input.metadata.name
    not name in ["dev", "staging", "prod"]
    msg := sprintf("Namespace name '%s' must be one of: dev, staging, prod", [name])
}
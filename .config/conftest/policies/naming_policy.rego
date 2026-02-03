# OPA/Conftest Naming Policy
# Enforces naming conventions for Kubernetes resources and IaC

package naming

# deny if resource name doesn't match pattern
deny[msg] {
  input.kind == "Deployment"
  not re_match("^(dev|staging|prod)-[a-z0-9-]+-(deploy|svc|ing|cm|secret)-v\\d+\\.\\d+\\.\\d+(-[A-Za-z0-9]+)?$", input.metadata.name)
  msg := sprintf("Deployment name '%s' does not match naming pattern. Expected: ^(dev|staging|prod)-[a-z0-9-]+-(deploy|svc|ing|cm|secret)-v\\d+\\.\\d+\\.\\d+(-[A-Za-z0-9]+)?$", [input.metadata.name])
}

deny[msg] {
  input.kind == "Service"
  not re_match("^(dev|staging|prod)-[a-z0-9-]+-(deploy|svc|ing|cm|secret)-v\\d+\\.\\d+\\.\\d+(-[A-Za-z0-9]+)?$", input.metadata.name)
  msg := sprintf("Service name '%s' does not match naming pattern. Expected: ^(dev|staging|prod)-[a-z0-9-]+-(deploy|svc|ing|cm|secret)-v\\d+\\.\\d+\\.\\d+(-[A-Za-z0-9]+)?$", [input.metadata.name])
}

deny[msg] {
  input.kind == "Ingress"
  not re_match("^(dev|staging|prod)-[a-z0-9-]+-(deploy|svc|ing|cm|secret)-v\\d+\\.\\d+\\.\\d+(-[A-Za-z0-9]+)?$", input.metadata.name)
  msg := sprintf("Ingress name '%s' does not match naming pattern. Expected: ^(dev|staging|prod)-[a-z0-9-]+-(deploy|svc|ing|cm|secret)-v\\d+\\.\\d+\\.\\d+(-[A-Za-z0-9]+)?$", [input.metadata.name])
}

deny[msg] {
  input.kind == "ConfigMap"
  not re_match("^(dev|staging|prod)-[a-z0-9-]+-(deploy|svc|ing|cm|secret)-v\\d+\\.\\d+\\.\\d+(-[A-Za-z0-9]+)?$", input.metadata.name)
  msg := sprintf("ConfigMap name '%s' does not match naming pattern. Expected: ^(dev|staging|prod)-[a-z0-9-]+-(deploy|svc|ing|cm|secret)-v\\d+\\.\\d+\\.\\d+(-[A-Za-z0-9]+)?$", [input.metadata.name])
}

deny[msg] {
  input.kind == "Secret"
  not re_match("^(dev|staging|prod)-[a-z0-9-]+-(deploy|svc|ing|cm|secret)-v\\d+\\.\\d+\\.\\d+(-[A-Za-z0-9]+)?$", input.metadata.name)
  msg := sprintf("Secret name '%s' does not match naming pattern. Expected: ^(dev|staging|prod)-[a-z0-9-]+-(deploy|svc|ing|cm|secret)-v\\d+\\.\\d+\\.\\d+(-[A-Za-z0-9]+)?$", [input.metadata.name])
}

# deny if labels are missing
deny[msg] {
  input.kind
  not input.metadata.labels["app"]
  msg := sprintf("Resource '%s' missing required label 'app'", [input.metadata.name])
}

deny[msg] {
  input.kind
  not input.metadata.labels["environment"]
  msg := sprintf("Resource '%s' missing required label 'environment'", [input.metadata.name])
}

deny[msg] {
  input.kind
  not input.metadata.labels["version"]
  msg := sprintf("Resource '%s' missing required label 'version'", [input.metadata.name])
}

# deny if label values don't match allowed values
deny[msg] {
  input.metadata.labels["environment"]
  not input.metadata.labels["environment"] in ["dev", "staging", "prod"]
  msg := sprintf("Label 'environment' must be one of: dev, staging, prod. Got: %s", [input.metadata.labels["environment"]])
}
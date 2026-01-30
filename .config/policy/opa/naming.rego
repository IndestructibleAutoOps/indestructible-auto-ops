package naming

# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: naming-policy-opa
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json

default valid = true

# Naming pattern for Kubernetes resources
# Pattern: ^(dev|staging|prod)-[a-z0-9-]+-(deploy|svc|ing|cm|secret)-v\d+.\d+.\d+(-[A-Za-z0-9]+)?$
kubernetes_naming_pattern = "^(dev|staging|prod)-[a-z0-9-]+-(deploy|svc|ing|cm|secret)-v[0-9]+\\.[0-9]+\\.[0-9]+(-[A-Za-z0-9]+)?$"

# Naming pattern for Helm releases
helm_naming_pattern = "^[a-z0-9]+(-[a-z0-9]+)*$"

# Naming pattern for Docker images
docker_image_pattern = "^[a-z0-9]+(\\/[a-z0-9-]+)*(:[a-z0-9.-]+)?$"

# Validate Kubernetes resource names
valid_kubernetes_name[name] {
    matches(name, kubernetes_naming_pattern)
}

# Validate Helm release names
valid_helm_name[name] {
    matches(name, helm_naming_pattern)
}

# Validate Docker image names
valid_docker_image[image] {
    matches(image, docker_image_pattern)
}

deny[msg] {
    input.kind == "Deployment"
    name := input.metadata.name
    not valid_kubernetes_name(name)
    msg := sprintf("Deployment name '%s' does not follow naming pattern. Expected pattern: %s", [name, kubernetes_naming_pattern])
}

deny[msg] {
    input.kind == "Service"
    name := input.metadata.name
    not valid_kubernetes_name(name)
    msg := sprintf("Service name '%s' does not follow naming pattern. Expected pattern: %s", [name, kubernetes_naming_pattern])
}

deny[msg] {
    input.kind == "Ingress"
    name := input.metadata.name
    not valid_kubernetes_name(name)
    msg := sprintf("Ingress name '%s' does not follow naming pattern. Expected pattern: %s", [name, kubernetes_naming_pattern])
}

deny[msg] {
    input.kind == "ConfigMap"
    name := input.metadata.name
    not valid_kubernetes_name(name)
    msg := sprintf("ConfigMap name '%s' does not follow naming pattern. Expected pattern: %s", [name, kubernetes_naming_pattern])
}

deny[msg] {
    input.kind == "Secret"
    name := input.metadata.name
    not valid_kubernetes_name(name)
    msg := sprintf("Secret name '%s' does not follow naming pattern. Expected pattern: %s", [name, kubernetes_naming_pattern])
}

# Check for required labels
deny[msg] {
    input.kind
    not input.metadata.labels
    msg := sprintf("Resource of kind '%s' must have labels", [input.kind])
}

deny[msg] {
    input.kind
    required_label := {"app", "version", "environment"}
    not required_label[label]
    label := input.metadata.labels[label]
    msg := sprintf("Resource of kind '%s' is missing required label '%s'", [input.kind, label])
}

# Validate environment label values
deny[msg] {
    input.kind
    input.metadata.labels.environment
    not input.metadata.labels.environment in ["dev", "staging", "prod"]
    msg := sprintf("Environment label must be one of: dev, staging, prod. Got: %s", [input.metadata.labels.environment])
}
# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: naming-policy
#
# ═══════════════════════════════════════════════════════════════════════════════
#                    Machine Native Ops - Naming Policy
#                    GL Layer: GL10-29 Operational Layer
#                    Purpose: Enforce naming conventions via OPA/Rego
# ═══════════════════════════════════════════════════════════════════════════════
#
# Policy Rules:
# - Kubernetes deployment names must follow pattern: (dev|prod|staging)-[a-z0-9-]+-deploy-v[0-9]+
# - Service names must follow pattern: [a-z0-9-]+-svc
# - ConfigMap names must follow pattern: [a-z0-9-]+-config
# - Secret names must follow pattern: [a-z0-9-]+-secret

package main

import future.keywords.in

# ─────────────────────────────────────────────────────────────────────────────
# Deployment Naming Policy
# ─────────────────────────────────────────────────────────────────────────────

deny[msg] {
    input.kind == "Deployment"
    name := input.metadata.name
    not valid_deployment_name(name)
    msg := sprintf("Invalid deployment name '%v'. Must match pattern: (dev|prod|staging)-[a-z0-9-]+-deploy-v[0-9]+", [name])
}

valid_deployment_name(name) {
    regex.match(`^(dev|prod|staging)-[a-z0-9-]+-deploy-v\d+$`, name)
}

# ─────────────────────────────────────────────────────────────────────────────
# Service Naming Policy
# ─────────────────────────────────────────────────────────────────────────────

deny[msg] {
    input.kind == "Service"
    name := input.metadata.name
    not valid_service_name(name)
    msg := sprintf("Invalid service name '%v'. Must match pattern: [a-z0-9-]+-svc", [name])
}

valid_service_name(name) {
    regex.match(`^[a-z0-9-]+-svc$`, name)
}

# ─────────────────────────────────────────────────────────────────────────────
# ConfigMap Naming Policy
# ─────────────────────────────────────────────────────────────────────────────

deny[msg] {
    input.kind == "ConfigMap"
    name := input.metadata.name
    not valid_configmap_name(name)
    # Allow system ConfigMaps
    not startswith(name, "kube-")
    msg := sprintf("Invalid ConfigMap name '%v'. Must match pattern: [a-z0-9-]+-config", [name])
}

valid_configmap_name(name) {
    regex.match(`^[a-z0-9-]+-config$`, name)
}

# ─────────────────────────────────────────────────────────────────────────────
# Secret Naming Policy
# ─────────────────────────────────────────────────────────────────────────────

deny[msg] {
    input.kind == "Secret"
    name := input.metadata.name
    not valid_secret_name(name)
    # Allow system Secrets
    not startswith(name, "default-token-")
    msg := sprintf("Invalid Secret name '%v'. Must match pattern: [a-z0-9-]+-secret", [name])
}

valid_secret_name(name) {
    regex.match(`^[a-z0-9-]+-secret$`, name)
}

# ─────────────────────────────────────────────────────────────────────────────
# Namespace Naming Policy
# ─────────────────────────────────────────────────────────────────────────────

deny[msg] {
    input.kind == "Namespace"
    name := input.metadata.name
    not valid_namespace_name(name)
    # Allow system namespaces
    not name in ["default", "kube-system", "kube-public", "kube-node-lease"]
    msg := sprintf("Invalid namespace name '%v'. Must match pattern: [a-z0-9-]+ (3-63 chars)", [name])
}

valid_namespace_name(name) {
    regex.match(`^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$`, name)
}

# ─────────────────────────────────────────────────────────────────────────────
# Label Requirements
# ─────────────────────────────────────────────────────────────────────────────

required_labels := {"app.kubernetes.io/name", "app.kubernetes.io/version", "app.kubernetes.io/managed-by"}

deny[msg] {
    input.kind in ["Deployment", "Service", "StatefulSet", "DaemonSet"]
    labels := object.get(input.metadata, "labels", {})
    missing := required_labels - {label | labels[label]}
    count(missing) > 0
    msg := sprintf("Missing required labels on %v '%v': %v", [input.kind, input.metadata.name, missing])
}

# ─────────────────────────────────────────────────────────────────────────────
# Warning Rules (non-blocking)
# ─────────────────────────────────────────────────────────────────────────────

warn[msg] {
    input.kind == "Deployment"
    not input.spec.replicas
    msg := sprintf("Deployment '%v' does not specify replica count", [input.metadata.name])
}

warn[msg] {
    input.kind == "Deployment"
    input.spec.replicas < 2
    msg := sprintf("Deployment '%v' has less than 2 replicas (not HA)", [input.metadata.name])
}

warn[msg] {
    input.kind == "Pod"
    container := input.spec.containers[_]
    not container.resources.limits
    msg := sprintf("Container '%v' in Pod '%v' has no resource limits", [container.name, input.metadata.name])
}

# ─────────────────────────────────────────────────────────────────────────────
# Helper Functions
# ─────────────────────────────────────────────────────────────────────────────

# Check if string starts with prefix
startswith(str, prefix) {
    substring(str, 0, count(prefix)) == prefix
}

# Get nested object or default
object.get(obj, key, default) := value {
    value := obj[key]
} else := default

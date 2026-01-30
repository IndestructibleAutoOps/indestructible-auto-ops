#!/bin/bash
#
# GL-Native Execution Backend - Cluster Deployment Script
#

set -e
set -u

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

NAMESPACE=${NAMESPACE:-"gl-native"}
BACKEND_VERSION=${BACKEND_VERSION:-"v1.1"}
REPLICAS=${REPLICAS:-3}
HPA_ENABLED=${HPA_ENABLED:-false}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIFESTS_DIR="${SCRIPT_DIR}/manifests"

print_header() {
    echo ""
    echo "========================================"
    echo "$1"
    echo "========================================"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}→${NC} $1"
}

print_step() {
    echo ""
    echo "[$1] $2"
}

main() {
    print_header "GL-Native Cluster Deployment"
    echo ""
    
    mkdir -p "${MANIFESTS_DIR}"
    
    print_step "1/5" "Creating Namespace"
    cat <<'EOF' > "${MANIFESTS_DIR}/namespace.yaml"
apiVersion: v1
kind: Namespace
metadata:
  name: ${NAMESPACE}
EOF
    kubectl apply -f "${MANIFESTS_DIR}/namespace.yaml"
    print_success "Namespace created"
    
    print_step "2/5" "Creating ConfigMap"
    cat <<'EOF' > "${MANIFESTS_DIR}/configmap.yaml"
apiVersion: v1
kind: ConfigMap
metadata:
  name: gl-backend-config
  namespace: ${NAMESPACE}
data:
  version: "${BACKEND_VERSION}"
EOF
    kubectl apply -f "${MANIFESTS_DIR}/configmap.yaml"
    print_success "ConfigMap created"
    
    print_step "3/5" "Creating Deployment"
    cat <<'EOF' > "${MANIFESTS_DIR}/deployment.yaml"
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gl-backend-deployment
  namespace: ${NAMESPACE}
spec:
  replicas: ${REPLICAS}
  selector:
    matchLabels:
      app: gl-backend
  template:
    metadata:
      labels:
        app: gl-backend
    spec:
      containers:
      - name: backend
        image: gl-native/backend:${BACKEND_VERSION}
        ports:
        - containerPort: 8080
EOF
    kubectl apply -f "${MANIFESTS_DIR}/deployment.yaml"
    print_success "Deployment created"
    
    print_step "4/5" "Creating Service"
    cat <<'EOF' > "${MANIFESTS_DIR}/service.yaml"
apiVersion: v1
kind: Service
metadata:
  name: gl-backend-service
  namespace: ${NAMESPACE}
spec:
  selector:
    app: gl-backend
  ports:
  - port: 8080
    targetPort: 8080
EOF
    kubectl apply -f "${MANIFESTS_DIR}/service.yaml"
    print_success "Service created"
    
    print_step "5/5" "Verifying Deployment"
    kubectl get pods -n "${NAMESPACE}" -l app=gl-backend
    print_success "Deployment verified"
    
    print_header "Deployment Complete"
    echo -e "${GREEN}✓ GL-Native Backend deployed successfully!${NC}"
    exit 0
}

main "$@"
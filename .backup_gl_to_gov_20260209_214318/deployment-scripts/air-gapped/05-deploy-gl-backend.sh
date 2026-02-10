#!/bin/bash

###############################################################################
# GL-Native Execution Backend - 部署腳本 (離線環境)
#
# 用途：在離線環境的 k3s 叢集中部署 GL-Native Execution Backend
# 使用方式：./05_deploy_gl_backend.sh [選項]
###############################################################################

set -e
set -u

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

NAMESPACE=${NAMESPACE:-"gov-native"}
BACKEND_VERSION=${BACKEND_VERSION:-"v1.1"}
REGISTRY_URL=${REGISTRY_URL:-"http://localhost:5000"}
REPLICAS=${REPLICAS:-1}

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

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}→${NC} $1"
}

main() {
    print_header "GL-Native 離線環境部署腳本"
    echo ""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --namespace=*)
                NAMESPACE="${1#*=}"
                shift
                ;;
            --version=*)
                BACKEND_VERSION="${1#*=}"
                shift
                ;;
            --registry-url=*)
                REGISTRY_URL="${1#*=}"
                shift
                ;;
            --replicas=*)
                REPLICAS="${1#*=}"
                shift
                ;;
            --help|-h)
                echo "用法: $0 [選項]"
                exit 0
                ;;
        esac
    done
    
    # 檢查 kubectl
    if ! command -v kubectl > /dev/null 2>&1; then
        print_error "kubectl 未安裝"
        exit 1
    fi
    
    # 檢查 k3s 是否運行
    if ! kubectl get nodes > /dev/null 2>&1; then
        print_error "無法連接到 k3s 叢集"
        exit 1
    fi
    
    mkdir -p "${MANIFESTS_DIR}"
    
    # 創建 namespace
    print_info "創建 Namespace: ${NAMESPACE}"
    kubectl create namespace "${NAMESPACE}" --dry-run=client -o yaml > "${MANIFESTS_DIR}/namespace.yaml"
    kubectl apply -f "${MANIFESTS_DIR}/namespace.yaml"
    print_success "Namespace 創建完成"
    
    # 創建 registry secret
    print_info "創建 Registry Secret..."
    kubectl create secret docker-registry regcred \
        --docker-server=localhost:5000 \
        --docker-username=admin \
        --docker-password=admin123 \
        --docker-email=admin@example.com \
        --namespace="${NAMESPACE}" \
        --dry-run=client -o yaml > "${MANIFESTS_DIR}/secret.yaml"
    kubectl apply -f "${MANIFESTS_DIR}/secret.yaml"
    print_success "Registry Secret 創建完成"
    
    # 創建 configmap
    print_info "創建 ConfigMap..."
    cat > "${MANIFESTS_DIR}/configmap.yaml" <<EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: gov-backend-config
  namespace: ${NAMESPACE}
data:
  version: "${BACKEND_VERSION}"
  registry-url: "${REGISTRY_URL}"
EOF
    kubectl apply -f "${MANIFESTS_DIR}/configmap.yaml"
    print_success "ConfigMap 創建完成"
    
    # 創建 deployment
    print_info "創建 Deployment..."
    cat > "${MANIFESTS_DIR}/deployment.yaml" <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gov-backend-deployment
  namespace: ${NAMESPACE}
spec:
  replicas: ${REPLICAS}
  selector:
    matchLabels:
      app: gov-backend
  template:
    metadata:
      labels:
        app: gov-backend
    spec:
      imagePullSecrets:
      - name: regcred
      containers:
      - name: backend
        image: ${REGISTRY_URL}/gov-native/backend:${BACKEND_VERSION}
        ports:
        - containerPort: 8080
        env:
        - name: GL_BACKEND_VERSION
          value: "${BACKEND_VERSION}"
        - name: GL_REGISTRY_URL
          value: "${REGISTRY_URL}"
EOF
    kubectl apply -f "${MANIFESTS_DIR}/deployment.yaml"
    print_success "Deployment 創建完成"
    
    # 創建 service
    print_info "創建 Service..."
    cat > "${MANIFESTS_DIR}/service.yaml" <<EOF
apiVersion: v1
kind: Service
metadata:
  name: gov-backend-service
  namespace: ${NAMESPACE}
spec:
  selector:
    app: gov-backend
  ports:
  - port: 8080
    targetPort: 8080
EOF
    kubectl apply -f "${MANIFESTS_DIR}/service.yaml"
    print_success "Service 創建完成"
    
    # 等待部署完成
    print_info "等待部署完成..."
    kubectl wait --for=condition=ready pod \
        -l app=gov-backend \
        -n "${NAMESPACE}" \
        --timeout=300s
    
    # 驗證部署
    print_info "驗證部署..."
    kubectl get pods -n "${NAMESPACE}"
    kubectl get svc -n "${NAMESPACE}"
    
    print_header "部署完成"
    echo -e "${GREEN}✓ GL-Native Backend 部署成功！${NC}"
    echo ""
    echo "部署信息:"
    echo "  Namespace: ${NAMESPACE}"
    echo "  Version: ${BACKEND_VERSION}"
    echo "  Registry: ${REGISTRY_URL}"
    echo "  Replicas: ${REPLICAS}"
    echo ""
    exit 0
}

main "$@"
#!/bin/bash

###############################################################################
# GL-Native Execution Backend - 部署腳本 (單節點環境)
#
# 用途：在 k3s 叢集中部署 GL-Native Execution Backend
# 使用方式：./03_deploy_gl_backend.sh [--namespace NAMESPACE]
###############################################################################

set -e  # 遇到錯誤立即退出
set -u  # 使用未定義的變數時報錯

# 顏色輸出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 全局變數
NAMESPACE=${NAMESPACE:-"gl-native"}
BACKEND_VERSION=${BACKEND_VERSION:-"v1.1"}
REPO_PATH=${REPO_PATH:-"/workspace/gl-production-platform/execution-backend"}
STORAGE_PATH=${STORAGE_PATH:-"/opt/gl-native/data"}
REGISTRY=${REGISTRY:-"docker.io"}  # 使用公開 registry，實際部署時應使用私有 registry

# 容器配置
IMAGE_NAME="${REGISTRY}/gl-native/backend:${BACKEND_VERSION}"
CPU_REQUEST="500m"
CPU_LIMIT="2000m"
MEMORY_REQUEST="1Gi"
MEMORY_LIMIT="4Gi"
REPLICAS=1

# 配置檔案路徑
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="${SCRIPT_DIR}/configs"
MANIFESTS_DIR="${SCRIPT_DIR}/manifests"

###############################################################################
# 工具函數
###############################################################################

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

print_step() {
    echo ""
    echo "[$1] $2"
}

###############################################################################
# 前置檢查
###############################################################################

pre_deployment_check() {
    print_header "前置檢查"
    
    # 檢查 kubectl
    if ! command -v kubectl > /dev/null 2>&1; then
        print_error "kubectl 未安裝"
        exit 1
    fi
    
    # 檢查 k3s 是否運行
    if ! kubectl get nodes > /dev/null 2>&1; then
        print_error "無法連接到 k3s 叢集"
        print_info "請確保 k3s 已安裝並運行"
        exit 1
    fi
    
    print_success "k3s 叢集連接正常"
    
    # 檢查現有 namespace
    if kubectl get namespace "${NAMESPACE}" > /dev/null 2>&1; then
        print_warning "Namespace ${NAMESPACE} 已存在"
        read -p "是否要重新部署? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_error "取消部署"
            exit 0
        fi
    fi
    
    # 檢查源檔案
    if [ ! -d "${REPO_PATH}" ]; then
        print_warning "源代碼目錄不存在: ${REPO_PATH}"
        print_info "將使用容器化部署方式"
    else
        print_success "源代碼目錄存在"
    fi
}

###############################################################################
# 創建目錄結構
###############################################################################

create_directories() {
    print_step "1/8" "創建部署目錄結構"
    
    # 創建 manifests 目錄
    mkdir -p "${MANIFESTS_DIR}"
    
    # 創建 configs 目錄
    mkdir -p "${CONFIG_DIR}"
    
    # 創建本地存儲路徑
    mkdir -p "${STORAGE_PATH}"
    
    print_success "目錄結構創建完成"
}

###############################################################################
# 創建 Namespace
###############################################################################

create_namespace() {
    print_step "2/8" "創建 Namespace"
    
    cat > "${MANIFESTS_DIR}/namespace.yaml" <<EOF
apiVersion: v1
kind: Namespace
metadata:
  name: ${NAMESPACE}
  labels:
    name: ${NAMESPACE}
    app: gl-native-backend
    environment: production
    component: execution-backend
EOF
    
    kubectl apply -f "${MANIFESTS_DIR}/namespace.yaml"
    
    print_success "Namespace ${NAMESPACE} 創建完成"
}

###############################################################################
# 創建 ConfigMap
###############################################################################

create_configmap() {
    print_step "3/8" "創建 ConfigMap"
    
    # 如果有配置檔案，則從檔案創建 ConfigMap
    if [ -f "${REPO_PATH}/execution-backend-config.yaml" ]; then
        print_info "從執行後端配置檔案創建 ConfigMap..."
        kubectl create configmap gl-backend-config \
            --from-file="${REPO_PATH}/execution-backend-config.yaml" \
            --namespace="${NAMESPACE}" \
            --dry-run=client -o yaml > "${MANIFESTS_DIR}/configmap.yaml"
    else
        print_info "創建默認 ConfigMap..."
        cat > "${MANIFESTS_DIR}/configmap.yaml" <<EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: gl-backend-config
  namespace: ${NAMESPACE}
data:
  # 執行後端配置
  execution-backend.yaml: |
    version: "${BACKEND_VERSION}"
    
    # Runtime Core 配置
    runtime-core:
      event-buffer-size: 10000
      checkpoint-enabled: true
      checkpoint-interval: 300
      monitoring-enabled: true
    
    # Resource Manager 配置
    resource-manager:
      cpu-allocation: "share-based"
      memory-allocation: "request-based"
      cgroups-enabled: true
    
    # Isolation Engine 配置
    isolation-engine:
      namespaces-enabled: true
      overlayfs-enabled: true
      network-sandbox: "isolated"
    
    # Scheduler 配置
    scheduler:
      strategy: "priority"
      queue-size: 10000
      retry-policy: "exponential-backoff"
    
    # Verification Hooks 配置
    verification-hooks:
      enabled-hooks:
        - exit_code
        - test_results
        - behavior_diff
        - security_regression
        - structure_integrity
        - resource_compliance
    
    # Governance Hooks 配置
    governance-hooks:
      enabled: true
      v22-integration: true
      enforcement-mode: "strict"
    
    # Diagnostics 配置
    diagnostics:
      tracing-enabled: true
      metrics-enabled: true
      replay-enabled: true
      prometheus-port: 9090
      dashboard-port: 8080
EOF
    fi
    
    kubectl apply -f "${MANIFESTS_DIR}/configmap.yaml"
    
    print_success "ConfigMap 創建完成"
}

###############################################################################
# 創建 Secrets
###############################################################################

create_secrets() {
    print_step "4/8" "創建 Secrets"
    
    # 創建 TLS Secret (如果憑證文件存在)
    if [ -f "/etc/gl-native/tls.crt" ] && [ -f "/etc/gl-native/tls.key" ]; then
        print_info "創建 TLS Secret..."
        kubectl create secret tls gl-backend-tls \
            --cert=/etc/gl-native/tls.crt \
            --key=/etc/gl-native/tls.key \
            --namespace="${NAMESPACE}" \
            --dry-run=client -o yaml > "${MANIFESTS_DIR}/tls-secret.yaml"
        kubectl apply -f "${MANIFESTS_DIR}/tls-secret.yaml"
    else
        print_warning "TLS 憑證未找到，將生成自簽名憑證"
    fi
    
    # 創建 Governance Secret (模擬)
    cat > "${MANIFESTS_DIR}/secret.yaml" <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: gl-backend-secrets
  namespace: ${NAMESPACE}
type: Opaque
stringData:
  # Governance API Token
  governance-token: "gl-governance-v22-token"
  
  # Verification API Key
  verification-api-key: "gl-verification-key"
  
  # Metrics Token
  metrics-token: "gl-metrics-token"
EOF
    
    kubectl apply -f "${MANIFESTS_DIR}/secret.yaml"
    
    print_success "Secrets 創建完成"
}

###############################################################################
# 創建 Service Account
###############################################################################

create_service_account() {
    print_step "5/8" "創建 Service Account"
    
    cat > "${MANIFESTS_DIR}/service-account.yaml" <<EOF
apiVersion: v1
kind: ServiceAccount
metadata:
  name: gl-backend-sa
  namespace: ${NAMESPACE}
  labels:
    app: gl-backend
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: gl-backend-role
  namespace: ${NAMESPACE}
rules:
- apiGroups: [""]
  resources: ["configmaps", "secrets", "pods", "pods/log"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
- apiGroups: [""]
  resources: ["pods/exec"]
  verbs: ["create"]
- apiGroups: ["batch"]
  resources: ["jobs"]
  verbs: ["get", "list", "watch", "create", "delete"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: gl-backend-rolebinding
  namespace: ${NAMESPACE}
subjects:
- kind: ServiceAccount
  name: gl-backend-sa
  namespace: ${NAMESPACE}
roleRef:
  kind: Role
  name: gl-backend-role
  apiGroup: rbac.authorization.k8s.io
EOF
    
    kubectl apply -f "${MANIFESTS_DIR}/service-account.yaml"
    
    print_success "Service Account 創建完成"
}

###############################################################################
# 創建 Deployment
###############################################################################

create_deployment() {
    print_step "6/8" "創建 Deployment"
    
    cat > "${MANIFESTS_DIR}/deployment.yaml" <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gl-backend-deployment
  namespace: ${NAMESPACE}
  labels:
    app: gl-backend
    component: execution-backend
    version: "${BACKEND_VERSION}"
spec:
  replicas: ${REPLICAS}
  selector:
    matchLabels:
      app: gl-backend
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: gl-backend
        component: execution-backend
        version: "${BACKEND_VERSION}"
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "9090"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: gl-backend-sa
      securityContext:
        runAsNonRoot: false
        runAsUser: 0
        fsGroup: 0
      containers:
      - name: execution-engine
        image: ${IMAGE_NAME}
        imagePullPolicy: IfNotPresent
        ports:
        - name: api
          containerPort: 8080
          protocol: TCP
        - name: metrics
          containerPort: 9090
          protocol: TCP
        - name: diagnostics
          containerPort: 8081
          protocol: TCP
        
        env:
        - name: GL_BACKEND_VERSION
          value: "${BACKEND_VERSION}"
        - name: GL_NAMESPACE
          value: "${NAMESPACE}"
        - name: GL_STORAGE_PATH
          value: "/var/lib/gl-native/data"
        - name: GL_LOG_LEVEL
          value: "info"
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        - name: NODE_NAME
          valueFrom:
            fieldRef:
              fieldPath: spec.nodeName
        
        resources:
          requests:
            cpu: ${CPU_REQUEST}
            memory: ${MEMORY_REQUEST}
          limits:
            cpu: ${CPU_LIMIT}
            memory: ${MEMORY_LIMIT}
        
        volumeMounts:
        - name: config
          mountPath: /etc/gl-native/config
          readOnly: true
        - name: secrets
          mountPath: /etc/gl-native/secrets
          readOnly: true
        - name: storage
          mountPath: /var/lib/gl-native/data
        - name: logs
          mountPath: /var/log/gl-native
        
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
      
      volumes:
      - name: config
        configMap:
          name: gl-backend-config
      
      - name: secrets
        secret:
          secretName: gl-backend-secrets
          defaultMode: 0400
      
      - name: storage
        hostPath:
          path: ${STORAGE_PATH}
          type: DirectoryOrCreate
      
      - name: logs
        hostPath:
          path: /var/log/gl-native
          type: DirectoryOrCreate
      
      # 優先級調度
      priorityClassName: "high-priority"
      
      # 亲和性設置
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchLabels:
                app: gl-backend
            topologyKey: "kubernetes.io/hostname"
EOF
    
    # 創建 PriorityClass
    cat > "${MANIFESTS_DIR}/priorityclass.yaml" <<EOF
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000
globalDefault: false
description: "High priority class for GL-Native Execution Backend"
EOF
    
    kubectl apply -f "${MANIFESTS_DIR}/priorityclass.yaml"
    kubectl apply -f "${MANIFESTS_DIR}/deployment.yaml"
    
    print_success "Deployment 創建完成"
}

###############################################################################
# 創建 Service
###############################################################################

create_service() {
    print_step "7/8" "創建 Service"
    
    cat > "${MANIFESTS_DIR}/service.yaml" <<EOF
apiVersion: v1
kind: Service
metadata:
  name: gl-backend-service
  namespace: ${NAMESPACE}
  labels:
    app: gl-backend
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "9090"
spec:
  type: ClusterIP
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800
  ports:
  - name: api
    port: 8080
    targetPort: 8080
    protocol: TCP
  - name: metrics
    port: 9090
    targetPort: 9090
    protocol: TCP
  - name: diagnostics
    port: 8081
    targetPort: 8081
    protocol: TCP
  selector:
    app: gl-backend
---
apiVersion: v1
kind: Service
metadata:
  name: gl-backend-nodeport
  namespace: ${NAMESPACE}
  labels:
    app: gl-backend
spec:
  type: NodePort
  externalTrafficPolicy: Local
  ports:
  - name: api
    port: 8080
    targetPort: 8080
    nodePort: 30080
    protocol: TCP
  selector:
    app: gl-backend
EOF
    
    kubectl apply -f "${MANIFESTS_DIR}/service.yaml"
    
    print_success "Service 創建完成"
}

###############################################################################
# 創建 Ingress
###############################################################################

create_ingress() {
    print_step "8/8" "創建 Ingress"
    
    cat > "${MANIFESTS_DIR}/ingress.yaml" <<EOF
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: gl-backend-ingress
  namespace: ${NAMESPACE}
  labels:
    app: gl-backend
  annotations:
    ingress.kubernetes.io/ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "100m"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "300"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "300"
spec:
  ingressClassName: traefik
  tls:
  - hosts:
    - gl-backend.local
    secretName: gl-backend-tls
  rules:
  - host: gl-backend.local
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: gl-backend-service
            port:
              number: 8080
      - path: /metrics
        pathType: Prefix
        backend:
          service:
            name: gl-backend-service
            port:
              number: 9090
      - path: /diagnostics
        pathType: Prefix
        backend:
          service:
            name: gl-backend-service
            port:
              number: 8081
EOF
    
    kubectl apply -f "${MANIFESTS_DIR}/ingress.yaml"
    
    print_success "Ingress 創建完成"
}

###############################################################################
# 等待部署完成
###############################################################################

wait_for_deployment() {
    print_header "等待部署完成"
    
    print_info "等待 Pods 就緒..."
    kubectl wait --for=condition=ready pod \
        -l app=gl-backend \
        -n "${NAMESPACE}" \
        --timeout=300s
    
    print_success "所有 Pods 已就緒"
}

###############################################################################
# 驗證部署
###############################################################################

verify_deployment() {
    print_header "驗證部署"
    
    # 檢查 Pods
    print_info "檢查 Pods 狀態..."
    kubectl get pods -n "${NAMESPACE}" -l app=gl-backend
    
    # 檢查 Services
    print_info "檢查 Services..."
    kubectl get svc -n "${NAMESPACE}" -l app=gl-backend
    
    # 檢查 Ingress
    print_info "檢查 Ingress..."
    kubectl get ingress -n "${NAMESPACE}"
    
    # 檢查資源使用
    print_info "檢查資源使用..."
    kubectl top pods -n "${NAMESPACE}" -l app=gl-backend || echo "Metrics server not installed"
    
    # 獲取 Pod 日誌
    print_info "獲取 Pod 日誌..."
    local pod_name=$(kubectl get pods -n "${NAMESPACE}" -l app=gl-backend -o jsonpath='{.items[0].metadata.name}')
    if [ -n "$pod_name" ]; then
        echo "--- 最近 20 行日誌 ---"
        kubectl logs -n "${NAMESPACE}" "$pod_name" --tail=20
    fi
    
    print_success "部署驗證完成"
}

###############################################################################
# 部署完成總結
###############################################################################

print_summary() {
    print_header "部署完成"
    
    echo -e "${GREEN}✓ GL-Native Execution Backend 部署成功！${NC}"
    echo ""
    echo "部署信息:"
    echo "  Namespace: ${NAMESPACE}"
    echo "  Version: ${BACKEND_VERSION}"
    echo "  Replicas: ${REPLICAS}"
    echo "  Image: ${IMAGE_NAME}"
    echo ""
    echo "存取方式:"
    echo "  ClusterIP: kubectl port-forward -n ${NAMESPACE} svc/gl-backend-service 8080:8080"
    echo "  NodePort: http://<NODE_IP>:30080"
    echo "  Ingress: http://gl-backend.local (需要配置 DNS)"
    echo ""
    echo "API 端點:"
    echo "  主 API: http://localhost:8080/api"
    echo "  Metrics: http://localhost:9090/metrics"
    echo "  Diagnostics: http://localhost:8081/diagnostics"
    echo ""
    echo "常用命令:"
    echo "  kubectl get pods -n ${NAMESPACE}                    # 查看 Pods"
    echo "  kubectl get svc -n ${NAMESPACE}                     # 查看 Services"
    echo "  kubectl logs -n ${NAMESPACE} -l app=gl-backend      # 查看日誌"
    echo "  kubectl exec -n ${NAMESPACE} -it <pod-name> -- sh   # 進入容器"
    echo "  ./04_health_check.sh                                 # 健康檢查"
    echo ""
}

###############################################################################
# 主流程
###############################################################################

main() {
    print_header "GL-Native Execution Backend 部署腳本 (單節點環境)"
    echo ""
    
    # 解析參數
    for arg in "$@"; do
        case $arg in
            --namespace=*)
                NAMESPACE="${arg#*=}"
                shift
                ;;
            --version=*)
                BACKEND_VERSION="${arg#*=}"
                shift
                ;;
            --replicas=*)
                REPLICAS="${arg#*=}"
                shift
                ;;
            --help|-h)
                echo "用法: $0 [選項]"
                echo ""
                echo "選項:"
                echo "  --namespace=NAMESPACE  指定 Namespace (默認: gl-native)"
                echo "  --version=VERSION      指定後端版本 (默認: v1.1)"
                echo "  --replicas=N           指定副本數 (默認: 1)"
                echo "  --help, -h             顯示此幫助信息"
                echo ""
                echo "環境變數:"
                echo "  NAMESPACE              Namespace"
                echo "  BACKEND_VERSION        後端版本"
                echo "  STORAGE_PATH           存儲路徑 (默認: /opt/gl-native/data)"
                echo "  REGISTRY               Container Registry"
                exit 0
                ;;
        esac
    done
    
    # 執行部署步驟
    pre_deployment_check
    create_directories
    create_namespace
    create_configmap
    create_secrets
    create_service_account
    create_deployment
    create_service
    create_ingress
    wait_for_deployment
    verify_deployment
    print_summary
    
    exit 0
}

# 執行主函數
main "$@"
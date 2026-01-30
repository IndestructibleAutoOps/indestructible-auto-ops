#!/bin/bash

###############################################################################
# GL-Native Execution Backend - 健康檢查腳本 (單節點環境)
#
# 用途：檢查 k3s 叢集和 GL-Native Backend 的健康狀態
# 使用方式：./04_health_check.sh [--verbose] [--namespace NAMESPACE]
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
VERBOSE=${VERBOSE:-false}
CHECKS_PASSED=0
CHECKS_FAILED=0
CHECKS_WARNING=0

# 等待時間
WAIT_TIMEOUT=30
WAIT_INTERVAL=2

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
    ((CHECKS_PASSED++))
}

print_error() {
    echo -e "${RED}✗${NC} $1"
    ((CHECKS_FAILED++))
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((CHECKS_WARNING++))
}

print_info() {
    echo -e "${BLUE}→${NC} $1"
}

verbose_info() {
    if [ "$VERBOSE" = true ]; then
        echo "  [VERBOSE] $1"
    fi
}

###############################################################################
# k3s 健康檢查
###############################################################################

check_k3s_service() {
    print_header "檢查 1: k3s 服務狀態"
    
    if systemctl is-active --quiet k3s; then
        print_success "k3s 服務正在運行"
        
        local uptime=$(systemctl show k3s -p ActiveEnterTimestampMonotonic | cut -d= -f2)
        local uptime_sec=$((uptime / 1000000))
        local uptime_min=$((uptime_sec / 60))
        
        print_info "k3s 運行時間: ${uptime_min} 分鐘"
        return 0
    else
        print_error "k3s 服務未運行"
        print_info "啟動命令: sudo systemctl start k3s"
        return 1
    fi
}

check_k3s_version() {
    print_header "檢查 2: k3s 版本"
    
    if command -v k3s > /dev/null 2>&1; then
        local version=$(k3s --version 2>/dev/null | head -1)
        print_success "k3s 版本: $version"
        return 0
    else
        print_error "k3s 未安裝"
        return 1
    fi
}

check_k8s_api() {
    print_header "檢查 3: Kubernetes API"
    
    if kubectl get nodes > /dev/null 2>&1; then
        print_success "Kubernetes API 可訪問"
        return 0
    else
        print_error "無法訪問 Kubernetes API"
        return 1
    fi
}

check_node_status() {
    print_header "檢查 4: 節點狀態"
    
    local nodes=$(kubectl get nodes -o json)
    local node_count=$(echo "$nodes" | jq '.items | length')
    local ready_nodes=$(echo "$nodes" | jq '[.items[] | select(.status.conditions[] | select(.type=="Ready" and .status=="True"))] | length')
    
    print_info "總節點數: $node_count"
    print_info "Ready 節點數: $ready_nodes"
    
    if [ "$node_count" -gt 0 ] && [ "$ready_nodes" -eq "$node_count" ]; then
        print_success "所有節點狀態正常"
        
        if [ "$VERBOSE" = true ]; then
            print_info "節點詳情:"
            kubectl get nodes -o wide
        fi
        return 0
    else
        print_error "部分節點未就緒"
        return 1
    fi
}

check_system_pods() {
    print_header "檢查 5: 系統 Pods"
    
    local pods=$(kubectl get pods -n kube-system -o json)
    local pod_count=$(echo "$pods" | jq '.items | length')
    local running_pods=$(echo "$pods" | jq '[.items[] | select(.status.phase=="Running")] | length')
    
    print_info "總 Pod 數: $pod_count"
    print_info "Running Pods: $running_pods"
    
    local failed_pods=$(echo "$pods" | jq '[.items[] | select(.status.phase=="Failed")] | length')
    
    if [ "$failed_pods" -gt 0 ]; then
        print_warning "有 $failed_pods 個 Failed Pods"
        print_info "Failed Pods:"
        kubectl get pods -n kube-system --field-selector=status.phase=Failed
    fi
    
    if [ "$running_pods" -eq "$pod_count" ] || [ "$failed_pods" -eq 0 ]; then
        print_success "系統 Pods 狀態正常"
        return 0
    else
        print_error "部分系統 Pods 未正常運行"
        return 1
    fi
}

###############################################################################
# GL-Native Backend 健康檢查
###############################################################################

check_namespace() {
    print_header "檢查 6: Namespace"
    
    if kubectl get namespace "${NAMESPACE}" > /dev/null 2>&1; then
        print_success "Namespace ${NAMESPACE} 存在"
        
        if [ "$VERBOSE" = true ]; then
            kubectl describe namespace "${NAMESPACE}" | grep -A 5 "Labels"
        fi
        return 0
    else
        print_error "Namespace ${NAMESPACE} 不存在"
        return 1
    fi
}

check_backend_pods() {
    print_header "檢查 7: GL-Native Backend Pods"
    
    if ! kubectl get pods -n "${NAMESPACE}" -l app=gl-backend > /dev/null 2>&1; then
        print_warning "未找到 GL-Native Backend Pods"
        return 0
    fi
    
    local pods=$(kubectl get pods -n "${NAMESPACE}" -l app=gl-backend -o json)
    local pod_count=$(echo "$pods" | jq '.items | length')
    local ready_count=$(echo "$pods" | jq '[.items[] | select(.status.conditions[] | select(.type=="Ready" and .status=="True"))] | length')
    
    print_info "Backend Pods: $pod_count"
    print_info "Ready Pods: $ready_count"
    
    if [ "$pod_count" -eq 0 ]; then
        print_warning "沒有運行的 Backend Pods"
        return 0
    fi
    
    # 檢查每個 Pod 的詳細狀態
    local all_ready=true
    for pod in $(kubectl get pods -n "${NAMESPACE}" -l app=gl-backend -o name); do
        local pod_name=$(echo "$pod" | cut -d/ -f2)
        local phase=$(kubectl get pod -n "${NAMESPACE}" "$pod_name" -o jsonpath='{.status.phase}')
        local ready=$(kubectl get pod -n "${NAMESPACE}" "$pod_name" -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}')
        
        print_info "Pod $pod_name: Phase=$phase, Ready=$ready"
        
        if [ "$ready" != "True" ]; then
            all_ready=false
            print_error "Pod $pod_name 未就緒"
            
            # 顯示最近的事件
            if [ "$VERBOSE" = true ]; then
                print_info "Pod 事件:"
                kubectl describe pod -n "${NAMESPACE}" "$pod_name" | grep -A 10 "Events:"
            fi
        fi
    done
    
    if [ "$all_ready" = true ]; then
        print_success "所有 Backend Pods 狀態正常"
        return 0
    else
        print_error "部分 Backend Pods 未就緒"
        return 1
    fi
}

check_backend_services() {
    print_header "檢查 8: GL-Native Backend Services"
    
    if ! kubectl get svc -n "${NAMESPACE}" -l app=gl-backend > /dev/null 2>&1; then
        print_warning "未找到 GL-Native Backend Services"
        return 0
    fi
    
    local services=$(kubectl get svc -n "${NAMESPACE}" -l app=gl-backend -o json)
    local svc_count=$(echo "$services" | jq '.items | length')
    
    print_info "Services: $svc_count"
    
    if [ "$VERBOSE" = true ]; then
        print_info "Services 詳情:"
        kubectl get svc -n "${NAMESPACE}" -l app=gl-backend
    fi
    
    print_success "Services 狀態正常"
    return 0
}

check_backend_ingress() {
    print_header "檢查 9: GL-Native Backend Ingress"
    
    if ! kubectl get ingress -n "${NAMESPACE}" -l app=gl-backend > /dev/null 2>&1; then
        print_warning "未找到 GL-Native Backend Ingress"
        return 0
    fi
    
    local ingress=$(kubectl get ingress -n "${NAMESPACE}" -l app=gl-backend -o json)
    local ingress_count=$(echo "$ingress" | jq '.items | length')
    
    print_info "Ingress: $ingress_count"
    
    if [ "$VERBOSE" = true ]; then
        print_info "Ingress 詳情:"
        kubectl get ingress -n "${NAMESPACE}" -l app=gl-backend -o yaml
    fi
    
    print_success "Ingress 狀態正常"
    return 0
}

check_backend_api() {
    print_header "檢查 10: Backend API 可達性"
    
    # 獲取 Pod 名稱
    local pod_name=$(kubectl get pods -n "${NAMESPACE}" -l app=gl-backend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || echo "")
    
    if [ -z "$pod_name" ]; then
        print_warning "沒有可用的 Backend Pods"
        return 0
    fi
    
    # 檢查 Pod 是否運行
    local pod_status=$(kubectl get pod -n "${NAMESPACE}" "$pod_name" -o jsonpath='{.status.phase}')
    if [ "$pod_status" != "Running" ]; then
        print_warning "Pod $pod_name 未運行 (Status: $pod_status)"
        return 0
    fi
    
    # 檢查健康端點
    print_info "檢查健康端點..."
    local health_check=$(kubectl exec -n "${NAMESPACE}" "$pod_name" -- curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/health 2>/dev/null || echo "000")
    
    if [ "$health_check" = "200" ]; then
        print_success "Backend API 正常 (HTTP $health_check)"
        
        # 檢查就緒端點
        local ready_check=$(kubectl exec -n "${NAMESPACE}" "$pod_name" -- curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/ready 2>/dev/null || echo "000")
        if [ "$ready_check" = "200" ]; then
            print_success "Backend 就緒 (HTTP $ready_check)"
        else
            print_warning "Backend 未就緒 (HTTP $ready_check)"
        fi
        
        return 0
    else
        print_error "Backend API 無法訪問 (HTTP $health_check)"
        return 1
    fi
}

check_metrics_endpoint() {
    print_header "檢查 11: Metrics 端點"
    
    local pod_name=$(kubectl get pods -n "${NAMESPACE}" -l app=gl-backend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || echo "")
    
    if [ -z "$pod_name" ]; then
        print_warning "沒有可用的 Backend Pods"
        return 0
    fi
    
    print_info "檢查 metrics 端點..."
    local metrics_check=$(kubectl exec -n "${NAMESPACE}" "$pod_name" -- curl -s -o /dev/null -w "%{http_code}" http://localhost:9090/metrics 2>/dev/null || echo "000")
    
    if [ "$metrics_check" = "200" ]; then
        print_success "Metrics 端點正常 (HTTP $metrics_check)"
        
        if [ "$VERBOSE" = true ]; then
            print_info "Metrics 樣本:"
            kubectl exec -n "${NAMESPACE}" "$pod_name" -- curl -s http://localhost:9090/metrics | head -20
        fi
        return 0
    else
        print_warning "Metrics 端點無法訪問 (HTTP $metrics_check)"
        return 0
    fi
}

check_diagnostics_endpoint() {
    print_header "檢查 12: Diagnostics 端點"
    
    local pod_name=$(kubectl get pods -n "${NAMESPACE}" -l app=gl-backend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || echo "")
    
    if [ -z "$pod_name" ]; then
        print_warning "沒有可用的 Backend Pods"
        return 0
    fi
    
    print_info "檢查 diagnostics 端點..."
    local diagnostics_check=$(kubectl exec -n "${NAMESPACE}" "$pod_name" -- curl -s -o /dev/null -w "%{http_code}" http://localhost:8081/diagnostics 2>/dev/null || echo "000")
    
    if [ "$diagnostics_check" = "200" ]; then
        print_success "Diagnostics 端點正常 (HTTP $diagnostics_check)"
        return 0
    else
        print_warning "Diagnostics 端點無法訪問 (HTTP $diagnostics_check)"
        return 0
    fi
}

###############################################################################
# 資源使用檢查
###############################################################################

check_resource_usage() {
    print_header "檢查 13: 資源使用"
    
    # 檢查是否安裝了 metrics-server
    if ! kubectl top nodes > /dev/null 2>&1; then
        print_warning "Metrics server 未安裝，無法檢查資源使用"
        return 0
    fi
    
    print_info "節點資源使用:"
    kubectl top nodes
    echo ""
    
    if kubectl get pods -n "${NAMESPACE}" -l app=gl-backend > /dev/null 2>&1; then
        print_info "Backend Pods 資源使用:"
        kubectl top pods -n "${NAMESPACE}" -l app=gl-backend
        print_success "資源使用檢查完成"
    fi
    
    return 0
}

###############################################################################
# 日誌檢查
###############################################################################

check_recent_logs() {
    print_header "檢查 14: 最近日誌"
    
    local pod_name=$(kubectl get pods -n "${NAMESPACE}" -l app=gl-backend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || echo "")
    
    if [ -z "$pod_name" ]; then
        print_warning "沒有可用的 Backend Pods"
        return 0
    fi
    
    print_info "Pod $pod_name 最近 10 行日誌:"
    kubectl logs -n "${NAMESPACE}" "$pod_name" --tail=10
    
    # 檢查是否有錯誤日誌
    local error_count=$(kubectl logs -n "${NAMESPACE}" "$pod_name" --tail=100 2>/dev/null | grep -i error | wc -l)
    
    if [ "$error_count" -gt 0 ]; then
        print_warning "發現 $error_count 個錯誤"
    else
        print_success "沒有發現錯誤日誌"
    fi
    
    return 0
}

###############################################################################
# 配置檢查
###############################################################################

check_configuration() {
    print_header "檢查 15: 配置"
    
    # 檢查 ConfigMap
    if kubectl get configmap -n "${NAMESPACE}" gl-backend-config > /dev/null 2>&1; then
        print_success "ConfigMap gl-backend-config 存在"
        
        if [ "$VERBOSE" = true ]; then
            print_info "ConfigMap 內容:"
            kubectl get configmap -n "${NAMESPACE}" gl-backend-config -o yaml
        fi
    else
        print_error "ConfigMap gl-backend-config 不存在"
    fi
    
    # 檢查 Secrets
    if kubectl get secret -n "${NAMESPACE}" gl-backend-secrets > /dev/null 2>&1; then
        print_success "Secret gl-backend-secrets 存在"
    else
        print_error "Secret gl-backend-secrets 不存在"
    fi
    
    return 0
}

###############################################################################
# 主流程
###############################################################################

main() {
    print_header "GL-Native 健康檢查腳本 (單節點環境)"
    echo ""
    
    # 解析參數
    for arg in "$@"; do
        case $arg in
            --verbose|-v)
                VERBOSE=true
                shift
                ;;
            --namespace=*)
                NAMESPACE="${arg#*=}"
                shift
                ;;
            --help|-h)
                echo "用法: $0 [選項]"
                echo ""
                echo "選項:"
                echo "  --verbose, -v        顯示詳細輸出"
                echo "  --namespace=NS       指定 Namespace (默認: gl-native)"
                echo "  --help, -h           顯示此幫助信息"
                exit 0
                ;;
        esac
    done
    
    # 執行所有檢查
    check_k3s_service || true
    check_k3s_version || true
    check_k8s_api || true
    check_node_status || true
    check_system_pods || true
    check_namespace || true
    check_backend_pods || true
    check_backend_services || true
    check_backend_ingress || true
    check_backend_api || true
    check_metrics_endpoint || true
    check_diagnostics_endpoint || true
    check_resource_usage || true
    check_recent_logs || true
    check_configuration || true
    
    # 總結
    print_header "健康檢查總結"
    echo -e "${GREEN}通過:${NC} $CHECKS_PASSED"
    echo -e "${YELLOW}警告:${NC} $CHECKS_WARNING"
    echo -e "${RED}失敗:${NC} $CHECKS_FAILED"
    echo ""
    
    if [ "$CHECKS_FAILED" -eq 0 ]; then
        echo -e "${GREEN}✓ 所有關鍵檢查通過${NC}"
        echo ""
        echo "GL-Native Execution Backend 運行正常"
        exit 0
    else
        echo -e "${RED}✗ 部分檢查失敗${NC}"
        echo ""
        echo "請檢查上述失敗項目並修復"
        echo ""
        echo "常用故障排除命令:"
        echo "  kubectl get pods -n ${NAMESPACE}              # 查看 Pods"
        echo "  kubectl describe pod -n ${NAMESPACE} <pod>     # 查看 Pod 詳情"
        echo "  kubectl logs -n ${NAMESPACE} <pod>            # 查看 Pod 日誌"
        echo "  kubectl get events -n ${NAMESPACE}            # 查看事件"
        echo "  systemctl status k3s                         # 查看 k3s 狀態"
        echo "  journalctl -u k3s -n 50                      # 查看 k3s 日誌"
        exit 1
    fi
}

# 執行主函數
main "$@"
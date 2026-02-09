#!/bin/bash

###############################################################################
# GL-Native Execution Backend - 叢集健康檢查腳本
#
# 用途：檢查 k3s 叢集和 GL-Native Backend 的健康狀態
# 使用方式：./06_health_check.sh [--verbose]
###############################################################################

set -e
set -u

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

NAMESPACE=${NAMESPACE:-"gov-native"}
VERBOSE=${VERBOSE:-false}
CHECKS_PASSED=0
CHECKS_FAILED=0

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
}

print_info() {
    echo -e "${BLUE}→${NC} $1"
}

main() {
    print_header "GL-Native Cluster Health Check"
    echo ""
    
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
        esac
    done
    
    # Check k3s service
    print_header "Check 1: k3s Services"
    if systemctl is-active --quiet k3s; then
        print_success "k3s service running"
    else
        print_error "k3s service not running"
    fi
    
    if systemctl is-active --quiet k3s-agent 2>/dev/null; then
        print_success "k3s-agent service running"
    fi
    
    # Check k3s version
    print_header "Check 2: k3s Version"
    if command -v k3s > /dev/null 2>&1; then
        k3s --version
        print_success "k3s installed"
    fi
    
    # Check nodes
    print_header "Check 3: Node Status"
    kubectl get nodes -o wide
    
    # Check system pods
    print_header "Check 4: System Pods"
    kubectl get pods -n kube-system
    
    # Check GL Backend
    print_header "Check 5: GL-Native Backend"
    if kubectl get namespace "${NAMESPACE}" > /dev/null 2>&1; then
        kubectl get pods -n "${NAMESPACE}"
        kubectl get svc -n "${NAMESPACE}"
        print_success "GL-Native Backend namespace exists"
    else
        print_warning "GL-Native Backend namespace not found"
    fi
    
    # Summary
    print_header "Health Check Summary"
    echo -e "${GREEN}Passed:${NC} $CHECKS_PASSED"
    echo -e "${RED}Failed:${NC} $CHECKS_FAILED"
    echo ""
    
    if [ "$CHECKS_FAILED" -eq 0 ]; then
        echo -e "${GREEN}✓ All health checks passed${NC}"
        exit 0
    else
        echo -e "${RED}✗ Some health checks failed${NC}"
        exit 1
    fi
}

main "$@"
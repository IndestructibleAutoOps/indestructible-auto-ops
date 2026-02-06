#!/bin/bash

###############################################################################
# GL-Native Execution Backend - CNI 安裝腳本 (叢集環境)
#
# 用途：安裝和配置容器網路介面 (CNI)
# 使用方式：./04_install_cni.sh --plugin PLUGIN
###############################################################################

set -e
set -u

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

CNI_PLUGIN=${CNI_PLUGIN:-"calico"}
KUBECTL_CMD=${KUBECTL_CMD:-"kubectl"}

CALICO_VERSION=${CALICO_VERSION:-"v3.26.1"}
CILIUM_VERSION=${CILIUM_VERSION:-"v1.14.0"}
FLANNEL_VERSION=${FLANNEL_VERSION:-"v0.22.0"}

POD_CIDR=${POD_CIDR:-"10.42.0.0/16"}
SERVICE_CIDR=${SERVICE_CIDR:-"10.43.0.0/16"}

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
    print_header "GL-Native CNI 安裝腳本 (叢集環境)"
    echo ""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --plugin=*)
                CNI_PLUGIN="${1#*=}"
                shift
                ;;
            --help|-h)
                echo "用法: $0 [選項]"
                echo "  --plugin=PLUGIN    CNI 插件 (calico|cilium|flannel)"
                exit 0
                ;;
        esac
    done
    
    print_info "CNI 插件: $CNI_PLUGIN"
    print_info "Pod CIDR: $POD_CIDR"
    
    case "$CNI_PLUGIN" in
        calico)
            print_step "1/1" "安裝 Calico"
            curl -sfL https://raw.githubusercontent.com/projectcalico/calico/${CALICO_VERSION}/manifests/calico.yaml -o /tmp/calico.yaml
            sed -i "s|192.168.0.0/16|${POD_CIDR}|g" /tmp/calico.yaml
            kubectl apply -f /tmp/calico.yaml
            print_success "Calico 安裝完成"
            ;;
        cilium)
            print_step "1/1" "安裝 Cilium"
            curl -sfL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
            helm repo add cilium https://helm.cilium.io/
            helm repo update
            helm install cilium cilium/cilium --version ${CILIUM_VERSION} --namespace kube-system --set podCIDR="${POD_CIDR}"
            print_success "Cilium 安裝完成"
            ;;
        flannel)
            print_step "1/1" "安裝 Flannel"
            curl -sfL https://github.com/flannel-io/flannel/releases/download/${FLANNEL_VERSION}/kube-flannel.yml -o /tmp/flannel.yaml
            sed -i "s|10.244.0.0/16|${POD_CIDR}|g" /tmp/flannel.yaml
            kubectl apply -f /tmp/flannel.yaml
            print_success "Flannel 安裝完成"
            ;;
    esac
    
    print_header "CNI 安裝完成"
    echo -e "${GREEN}✓ CNI 插件 ${CNI_PLUGIN} 安裝成功！${NC}"
    exit 0
}

main "$@"
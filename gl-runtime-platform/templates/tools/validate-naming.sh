#!/bin/bash

# GL Runtime Platform Kubernetes 模板命名規範驗證腳本
# 版本: v1.0.0
# 用途: 驗證所有 Kubernetes 模板的命名規範合規性

set -e

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES_DIR="${SCRIPT_DIR}/../"
LOG_FILE="${SCRIPT_DIR}/validation-$(date +%Y%m%d-%H%M%S).log"
ERROR_COUNT=0
WARNING_COUNT=0
INFO_COUNT=0

# 日誌函數
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$LOG_FILE"
    ((INFO_COUNT++))
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
    ((WARNING_COUNT++))
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
    ((ERROR_COUNT++))
}

# 初始化
echo "==========================================" | tee "$LOG_FILE"
echo "GL Runtime Platform 命名規範驗證" | tee -a "$LOG_FILE"
echo "版本: v1.0.0" | tee -a "$LOG_FILE"
echo "時間: $(date)" | tee -a "$LOG_FILE"
echo "==========================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

log_info "開始驗證命名規範..."

# 檢查 YAML 文件
log_info "檢查 YAML 文件語法..."
find "$TEMPLATES_DIR" -name "*.yaml" -o -name "*.yml" | while read -r file; do
    if ! yamllint -d relaxed "$file" > /dev/null 2>&1; then
        log_warning "YAML 語法檢查失敗: $file"
    fi
done

log_success "YAML 語法檢查完成"

# 驗證命名空間命名規範
log_info "驗證命名空間命名規範..."
NAMING_PATTERN="^(team|dev|test|staging|prod|learn)-[a-z0-9-]+[a-z0-9]$"

find "$TEMPLATES_DIR" -name "namespace*.yaml" | while read -r file; do
    NS_NAME=$(grep -E "^  name: " "$file" | awk '{print $2}')
    
    if [[ -n "$NS_NAME" ]]; then
        # 檢查長度
        if [[ ${#NS_NAME} -gt 63 ]]; then
            log_error "命名空間名稱超過 63 字元: $NS_NAME in $file"
        fi
        
        # 檢查模式
        if ! [[ "$NS_NAME" =~ $NAMING_PATTERN ]]; then
            log_error "命名空間名稱不符合規範: $NS_NAME in $file"
        fi
        
        # 檢查禁用模式
        if [[ "$NS_NAME" =~ -- ]] || [[ "$NS_NAME" =~ ^- ]] || [[ "$NS_NAME" =~ -$ ]]; then
            log_error "命名空間名稱包含禁用模式: $NS_NAME in $file"
        fi
    fi
done

log_success "命名空間命名規範驗證完成"

# 驗證部署命名規範
log_info "驗證�部署命名規範..."
DEPLOYMENT_PATTERN="^[a-z0-9-]+-deploy-v[0-9]+$"

find "$TEMPLATES_DIR" -name "deployment*.yaml" | while read -r file; do
    DEPLOY_NAME=$(grep -E "^  name: " "$file" | awk '{print $2}')
    
    if [[ -n "$DEPLOY_NAME" ]]; then
        # 檢查長度
        if [[ ${#DEPLOY_NAME} -gt 63 ]]; then
            log_error "部署名稱超過 63 字元: $DEPLOY_NAME in $file"
        fi
        
        # 檢查模式
        if ! [[ "$DEPLOY_NAME" =~ $DEPLOYMENT_PATTERN ]]; then
            log_warning "部署名稱不符合建議模式: $DEPLOY_NAME in $file"
        fi
    fi
done

log_success "部署命名規範驗證完成"

# 驗證服務命名規範
log_info "驗證服務命名規範..."
SERVICE_PATTERN="^[a-z0-9-]+-svc$"

find "$TEMPLATES_DIR" -name "service*.yaml" | while read -r file; do
    SVC_NAME=$(grep -E "^  name: " "$file" | awk '{print $2}')
    
    if [[ -n "$SVC_NAME" ]]; then
        # 檢查長度
        if [[ ${#SVC_NAME} -gt 63 ]]; then
            log_error "服務名稱超過 63 字元: $SVC_NAME in $file"
        fi
        
        # 檢查模式
        if ! [[ "$SVC_NAME" =~ $SERVICE_PATTERN ]]; then
            log_warning "服務名稱不符合建議模式: $SVC_NAME in $file"
        fi
    fi
done

log_success "服務命名規範驗證完成"

# 驗證 ConfigMap 命名規範
log_info "驗證 ConfigMap 命名規範..."
CONFIGMAP_PATTERN="^[a-z0-9-]+-config$"

find "$TEMPLATES_DIR" -name "configmap*.yaml" | while read -r file; do
    CM_NAME=$(grep -E "^  name: " "$file" | awk '{print $2}')
    
    if [[ -n "$CM_NAME" ]]; then
        # 檢查長度
        if [[ ${#CM_NAME} -gt 63 ]]; then
            log_error "ConfigMap 名稱超過 63 字元: $CM_NAME in $file"
        fi
        
        # 檢查模式
        if ! [[ "$CM_NAME" =~ $CONFIGMAP_PATTERN ]]; then
            log_warning "ConfigMap 名稱不符合建議模式: $CM_NAME in $file"
        fi
    fi
done

log_success "ConfigMap 命名規範驗證完成"

# 驗證必要標籤
log_info "驗證必要標籤..."
REQUIRED_LABELS=(
    "app.kubernetes.io/name"
    "app.kubernetes.io/component"
    "app.kubernetes.io/part-of"
    "app.kubernetes.io/version"
    "app.kubernetes.io/managed-by"
    "tenant"
    "environment"
    "cost-center"
)

find "$TEMPLATES_DIR" -name "*.yaml" | while read -r file; do
    # 檢查是否包含 kind 定義
    if grep -q "^kind:" "$file"; then
        KIND=$(grep "^kind:" "$file" | awk '{print $2}')
        
        # 跳過 List 和特定資源類型
        if [[ "$KIND" != "List" ]] && [[ "$KIND" != "CustomResourceDefinition" ]]; then
            for label in "${REQUIRED_LABELS[@]}"; do
                if ! grep -q "$label:" "$file"; then
                    log_warning "缺少必要標籤 $label in $file ($KIND)"
                fi
            done
        fi
    fi
done

log_success "必要標籤驗證完成"

# 驗證資源限制
log_info "驗證資源限制..."
find "$TEMPLATES_DIR" -name "deployment*.yaml" | while read -r file; do
    if grep -q "resources:" "$file"; then
        if ! grep -q "requests:" "$file"; then
            log_warning "部署缺少資源請求: $file"
        fi
        if ! grep -q "limits:" "$file"; then
            log_warning "部署缺少資源限制: $file"
        fi
    else
        log_warning "部署未定義資源: $file"
    fi
done

log_success "資源限制驗證完成"

# 生成報告
echo "" | tee -a "$LOG_FILE"
echo "==========================================" | tee -a "$LOG_FILE"
echo "驗證報告" | tee -a "$LOG_FILE"
echo "==========================================" | tee -a "$LOG_FILE"
echo "信息: $INFO_COUNT" | tee -a "$LOG_FILE"
echo "警告: $WARNING_COUNT" | tee -a "$LOG_FILE"
echo "錯誤: $ERROR_COUNT" | tee -a "$LOG_FILE"
echo "==========================================" | tee -a "$LOG_FILE"

# 返回退出代碼
if [[ $ERROR_COUNT -gt 0 ]]; then
    log_error "驗證失敗：發現 $ERROR_COUNT 個錯誤"
    exit 1
elif [[ $WARNING_COUNT -gt 0 ]]; then
    log_warning "驗證完成但有警告：發現 $WARNING_COUNT 個警告"
    exit 0
else
    log_success "驗證成功：所有檢查通過"
    exit 0
fi
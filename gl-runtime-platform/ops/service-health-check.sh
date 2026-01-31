#!/bin/bash
# @GL-governed
# @GL-layer: GL10-29 Operational
# @GL-semantic: service-health-check
# @GL-charter-version: 1.0.0
#
# GL Runtime Platform 服務健康檢查腳本

set -euo pipefail

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 日誌函數
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 服務配置
SERVICES=(
    "3000:GL Runtime Platform:/health"
    "8080:REST API:/health"
    "5001:NLP Control Plane:/health"
    "9000:MinIO:/health"
    "6379:Redis:ping"
    "5432:PostgreSQL:pg_isready"
    "9090:Prometheus:/health"
    "3001:Health Check 1:/health"
    "3002:Health Check 2:/health"
)

# 檢查單個服務
check_service() {
    local port=$1
    local name=$2
    local endpoint=$3
    
    # 檢查端口是否開放
    if ! nc -z localhost $port 2>/dev/null; then
        log_error "$name (port $port) - 端口未開放"
        return 1
    fi
    
    # 檢查服務健康
    if [ "$endpoint" = "ping" ]; then
        if redis-cli ping > /dev/null 2>&1; then
            log_success "$name (port $port) - 健康檢查通過"
            return 0
        else
            log_error "$name (port $port) - 健康檢查失敗"
            return 1
        fi
    elif [ "$endpoint" = "pg_isready" ]; then
        if pg_isready -h localhost -p $port > /dev/null 2>&1; then
            log_success "$name (port $port) - 健康檢查通過"
            return 0
        else
            log_error "$name (port $port) - 健康檢查失敗"
            return 1
        fi
    else
        if curl -s -f "http://localhost:${port}${endpoint}" > /dev/null 2>&1; then
            log_success "$name (port $port) - 健康檢查通過"
            return 0
        else
            log_error "$name (port $port) - 健康檢查失敗"
            return 1
        fi
    fi
}

# 主函數
main() {
    log_info "╔══════════════════════════════════════════════════════════════╗"
    log_info "║         GL Runtime Platform 服務健康檢查                    ║"
    log_info "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    
    local healthy_count=0
    local total_count=${#SERVICES[@]}
    
    for service in "${SERVICES[@]}"; do
        local port="${service%%:*}"
        local remaining="${service#*:}"
        local name="${remaining%%:*}"
        local endpoint="${remaining##*:}"
        
        if check_service "$port" "$name" "$endpoint"; then
            ((healthy_count++))
        fi
    done
    
    echo ""
    log_info "╔══════════════════════════════════════════════════════════════╗"
    log_info "║                      健康檢查總結                           ║"
    log_info "╚══════════════════════════════════════════════════════════════╝"
    log_info "總服務數: $total_count"
    log_info "健康服務: $healthy_count"
    log_info "異常服務: $((total_count - healthy_count))"
    
    if [ $healthy_count -eq $total_count ]; then
        log_success "所有服務運行正常！"
        return 0
    else
        log_warning "部分服務運行異常，請檢查日誌"
        return 1
    fi
}

# 執行主函數
main "$@"
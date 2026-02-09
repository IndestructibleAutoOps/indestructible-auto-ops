# ═══════════════════════════════════════════════════════════════════════════════
#                    全機器自理 — Makefile
#                    Zero Human Intervention Governance
# ═══════════════════════════════════════════════════════════════════════════════

PYTHON := python3
REPO_ROOT := $(shell cd .. && pwd)

.PHONY: scan execute closed-loop all clean help

help: ## 顯示說明
	@echo "═══════════════════════════════════════════════════════════════"
	@echo "  全機器自理 — 自動化治理指令"
	@echo "═══════════════════════════════════════════════════════════════"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

scan: ## 執行全自主掃描
	@echo "🔍 啟動全自主掃描引擎..."
	cd $(REPO_ROOT) && $(PYTHON) scripts/autonomous_scanner.py

execute: ## 執行治理流水線
	@echo "⚙️ 啟動自主執行引擎..."
	cd $(REPO_ROOT) && $(PYTHON) scripts/autonomous_executor.py

closed-loop: ## 執行完整閉環循環
	@echo "🔄 啟動閉環編排器..."
	cd $(REPO_ROOT) && $(PYTHON) scripts/closed_loop_orchestrator.py

all: closed-loop ## 執行完整閉環（同 closed-loop）

clean: ## 清理暫存報告
	@echo "🧹 清理暫存報告..."
	rm -f $(REPO_ROOT)/responsibility-governance-sensing-boundary/report/scan-report-*.json
	rm -f $(REPO_ROOT)/responsibility-governance-execution-boundary/reports/execution-report-*.json
	rm -f $(REPO_ROOT)/.governance/closed-loop-reports/closed-loop-*.json

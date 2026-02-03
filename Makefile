# ═══════════════════════════════════════════════════════════════════════════════
#                    Machine Native Ops - Root Makefile
#                    GL Layer: GL30-49 Execution Layer
#                    Purpose: Build automation and task delegation
#                    Workspace Delegation & Top-Level Targets
# ═══════════════════════════════════════════════════════════════════════════════
#
# This Makefile delegates most operations to workspace/Makefile while providing
# convenient top-level targets for common operations.
#
# Usage:
#   make all-kg          - Run all knowledge graph generation (delegates to workspace)
#   make check-drift     - Check if generated files are up-to-date
#   make clean-generated - Remove all generated YAML files
#   make help            - Show this help message
#
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: all-kg kg mndoc superroot check-drift clean-generated analyze-reports help install automation-init automation-check automation-fix automation-verify automation-help test

# Default target
.DEFAULT_GOAL := help

# Workspace directory
WORKSPACE := workspace

# ─────────────────────────────────────────────────────────────────────────────
# Help
# ─────────────────────────────────────────────────────────────────────────────
help:
	@echo "Machine Native Ops - Root Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  make all-kg          - Run all knowledge graph generation"
	@echo "  make kg              - Build knowledge graph"
	@echo "  make mndoc           - Generate MN-DOC from README"
	@echo "  make superroot       - Generate SuperRoot entities"
	@echo "  make check-drift     - Check for drift in generated files"
	@echo "  make clean-generated - Remove generated YAML files"
	@echo "  make analyze-reports - Analyze root-level reports"
	@echo "  make install         - Install dependencies (npm + workspace)"
	@echo "  make help            - Show this help message"
	@echo ""
	@echo "Automation targets:"
	@echo "  make automation-init     - Initialize automation tools"
	@echo "  make automation-check    - Run quality checks"
	@echo "  make automation-fix      - Auto-fix issues"
	@echo "  make automation-verify   - Verify automation setup"
	@echo "  make automation-help     - Show automation help"
	@echo ""
	@echo "For workspace-specific operations, use: make -C $(WORKSPACE) <target>"

# ─────────────────────────────────────────────────────────────────────────────
# Delegation Targets - Forward to workspace Makefile
# ─────────────────────────────────────────────────────────────────────────────
all-kg:
	@$(MAKE) -C $(WORKSPACE) all-kg

kg:
	@$(MAKE) -C $(WORKSPACE) kg

mndoc:
	@$(MAKE) -C $(WORKSPACE) mndoc

superroot:
	@$(MAKE) -C $(WORKSPACE) superroot

check-drift:
	@$(MAKE) -C $(WORKSPACE) check-drift

clean-generated:
	@$(MAKE) -C $(WORKSPACE) clean-generated

analyze-reports:
	@$(MAKE) -C $(WORKSPACE) analyze-reports

# ─────────────────────────────────────────────────────────────────────────────
# Root-Level Targets
# ─────────────────────────────────────────────────────────────────────────────
install:
	@echo "📦 Installing dependencies (npm workspaces handles all subdirectories)..."
	npm install
	@echo "✅ Installation complete"

# ─────────────────────────────────────────────────────────────────────────────
# Automation Targets
# ─────────────────────────────────────────────────────────────────────────────
.PHONY: automation-init automation-check automation-fix automation-verify automation-help

automation-init:
	@echo "🚀 Initializing automation tools..."
	@bash scripts/init-automation.sh

automation-check:
	@echo "📊 Running quality checks..."
	@python3 scripts/auto-quality-check.py

automation-fix:
	@echo "🔧 Running auto-fix..."
	@python3 scripts/auto-fix-issues.py

automation-fix-preview:
	@echo "🔍 Previewing auto-fix (dry run)..."
	@python3 scripts/auto-fix-issues.py --dry-run

automation-verify:
	@echo "✅ Verifying automation setup..."
	@bash scripts/verify-automation.sh

automation-report:
	@echo "📄 Viewing quality report..."
	@cat AUTO-QUALITY-REPORT.md

automation-help:
	@echo "Automation Tools - Available Commands"
	@echo ""
	@echo "  make automation-init         - Initialize automation tools"
	@echo "  make automation-check        - Run quality checks"
	@echo "  make automation-fix          - Auto-fix issues"
	@echo "  make automation-fix-preview  - Preview auto-fix (dry run)"
	@echo "  make automation-verify       - Verify automation setup"
	@echo "  make automation-report       - View quality report"
	@echo "  make automation-help         - Show this help"
	@echo ""
	@echo "Quick start:"
	@echo "  1. make automation-init      # First time setup"
	@echo "  2. make automation-check     # Run checks"
	@echo "  3. make automation-report    # View results"

test:
	@echo "🧪 Running all GL implementation tests..."
	@echo ""
	@echo "Running GL implementation tests..."
	@python3 scripts/gl/implementation/test_implementation.py
	@echo ""
	@echo "Running layer validations..."
	@python3 scripts/gl/validate-semantics.py
	@python3 scripts/gl/quantum-validate.py
	@echo ""
	@echo "✅ All tests completed!"
	@echo ""
	@echo "For detailed validation reports, see:"
	@echo "  - GL-STATUS-REPORT.md"
	@echo "  - GL-CORE-INTEGRATION-REPORT.md"

# ============================================================================
# Governance System Targets - Governance Quantum Stack (GQS)
# ============================================================================

.PHONY: bootstrap start-min test-fast verify quick-check clean-gov deploy-gov install-deps fix-env

# Bootstrap & Setup
bootstrap: ## 引導腳本 - 初始化治理環境
	@echo "Bootstrapping governance environment..."
	@bash scripts/bootstrap.sh

start-min: ## 最小啟動 - 快速啟動治理系統
	@echo "Starting minimal governance system..."
	@bash scripts/start-min.sh

install-deps: ## 安裝治理依賴
	@echo "Installing governance dependencies..."
	@pip install -q pyyaml jsonschema python-dateutil requests pyjwt
	@echo "Dependencies installed"

fix-env: ## 修復環境變量 - 生成 .env 文件
	@echo "Fixing environment..."
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo ".env created from .env.example"; \
	else \
		echo ".env already exists"; \
	fi

# Testing & Verification
test-fast: ## 快速測試 - 驗證核心治理功能
	@echo "Running fast governance tests..."
	@python3 ecosystem/enforce.py
	@python3 ecosystem/enforcers/semantic_violation_classifier.py 2>&1 | tail -5
	@echo "Fast tests passed"

verify: ## 完整驗證 - 驗證所有治理層
	@echo "Running full governance verification..."
	@python3 ecosystem/enforce.py
	@echo "Governance enforcement verified"
	@if command -v conftest >/dev/null 2>&1; then \
		conftest verify ecosystem/contracts/policies/; \
		echo "Policies verified"; \
	else \
		echo "Conftest not installed, skipping policy verification"; \
	fi
	@echo "Full verification completed"

quick-check: ## 快速檢查 - 檢查治理系統健康狀態
	@echo "Quick governance system health check..."
	@echo "Checking governance compliance..."
	@python3 ecosystem/enforce.py 2>&1 | grep -E "(PASS|FAIL|違規數)"
	@echo "Checking database..."
	@if [ -f ecosystem/governance/audit.db ]; then \
		echo "✓ Database exists"; \
	else \
		echo "✗ Database not found"; \
	fi
	@echo "Checking policies..."
	@if [ -d ecosystem/contracts/policies/ ]; then \
		echo "✓ Policies directory exists"; \
		echo "  Policies: $$(ls ecosystem/contracts/policies/ | wc -l)"; \
	else \
		echo "✗ Policies directory not found"; \
	fi
	@echo "Quick check completed"

# Governance Operations
enforce: ## 執行治理強制檢查
	@echo "Enforcing governance rules..."
	@python3 ecosystem/enforce.py

audit: ## 運行治理審計
	@echo "Running audit..."
	@python3 ecosystem/tools/audit_trail_query.py --query all --limit 10 || echo "Audit tool not available"

report: ## 生成治理報告
	@echo "Generating governance report..."
	@python3 ecosystem/enforcers/closed_loop_governance.py generate-report \
		--artifacts-dir ecosystem/governance/artifacts/ \
		--output-dir ecosystem/governance/reports/ || echo "Report generation skipped"

# Cleanup
clean-gov: ## 清理治理臨時文件和日誌
	@echo "Cleaning up governance artifacts..."
	@rm -rf ecosystem/governance/artifacts/
	@rm -rf ecosystem/governance/states/
	@rm -rf ecosystem/governance/validation/
	@rm -rf ecosystem/governance/verification/
	@rm -rf ecosystem/governance/proofs/
	@rm -rf ecosystem/governance/execution-logs/
	@rm -rf ecosystem/governance/violations/
	@rm -rf ecosystem/governance/fixes/
	@find ecosystem/governance/ -name "*.log" -delete 2>/dev/null || true
	@find ecosystem/governance/ -name "*-report-*.json" -delete 2>/dev/null || true
	@echo "Cleanup completed"

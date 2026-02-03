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

.PHONY: all-kg kg mndoc superroot check-drift clean-generated analyze-reports help install automation-init automation-check automation-fix automation-verify automation-help test test-fast quick-verify bootstrap

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

# ─────────────────────────────────────────────────────────────────────────────
# Quick Test Target (fast local verification)
# ─────────────────────────────────────────────────────────────────────────────
.PHONY: test-fast quick-verify bootstrap

test-fast:
	@echo "⚡ Running quick tests (fast local verification)..."
	@echo ""
	@echo "Step 1: Quick environment verification..."
	@bash scripts/quick-verify.sh --json 2>/dev/null || bash scripts/quick-verify.sh
	@echo ""
	@echo "Step 2: Ecosystem enforcement check..."
	@python3 ecosystem/enforce.py 2>/dev/null || echo "⚠️  Ecosystem check had warnings (non-fatal)"
	@echo ""
	@echo "✅ Quick tests completed!"

quick-verify:
	@echo "🔍 Running quick verification..."
	@bash scripts/quick-verify.sh

bootstrap:
	@echo "🚀 Running bootstrap..."
	@bash scripts/bootstrap.sh

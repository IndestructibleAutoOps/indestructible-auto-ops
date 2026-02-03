# MNGA Makefile
# Convenient commands for MNGA system

.PHONY: help bootstrap start verify test clean lint enforce lint-fix

# Default target
help:
	@echo "MNGA - Machine Native Governance Architecture"
	@echo ""
	@echo "Available commands:"
	@echo "  make bootstrap     - Bootstrap the development environment"
	@echo "  make start        - Start the minimal system"
	@echo "  make verify       - Run quick verification tests"
	@echo "  make test         - Run all tests"
	@echo "  make enforce      - Run governance enforcement"
	@echo "  make lint         - Run code linting"
	@echo "  make lint-fix     - Fix linting issues automatically"
	@echo "  make clean        - Clean build artifacts and caches"
	@echo ""

# Bootstrap environment
bootstrap:
	@echo "Bootstrapping MNGA environment..."
	@./scripts/bootstrap.sh

# Start minimal system
start:
	@echo "Starting MNGA minimal system..."
	@./scripts/start-min.sh

# Quick verification
verify:
	@echo "Running verification tests..."
	@./scripts/quick-verify.sh

# Run tests
test:
	@echo "Running all tests..."
	@python3 -m pytest tests/ -v --cov=. --cov-report=html

# Run governance enforcement
enforce:
	@echo "Running governance enforcement..."
	@python3 ecosystem/enforce.py --audit --auto-fix

# Lint code
lint:
	@echo "Linting code..."
	@python3 -m flake8 ecosystem/ platforms/
	@python3 -m mypy ecosystem/ platforms/ --ignore-missing-imports
	@yamllint .config/ .github/workflows/

# Fix linting issues
lint-fix:
	@echo "Fixing linting issues..."
	@python3 -m black ecosystem/ platforms/
	@python3 -m isort ecosystem/ platforms/
	@yamllint -f parsable .config/ .github/workflows/ | while read file line; do \
		sed -i "$$line" "$$file"; \
	done

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name '*.pyc' -delete 2>/dev/null || true
	@find . -type f -name '*.pyo' -delete 2>/dev/null || true
	@rm -rf .pytest_cache
	@rm -rf htmlcov
	@rm -rf .coverage
	@rm -rf ecosystem/logs/*.log
	@rm -rf ecosystem/indexes/internal/*.db

# Run reasoning pipeline test
test-reasoning:
	@echo "Testing reasoning pipeline..."
	@python3 platforms/gl.platform-assistant/orchestration/pipeline.py

# Generate naming report
generate-naming-report:
	@echo "Generating naming compliance report..."
	@python3 ecosystem/scripts/naming/generate_naming_report.py \
		--output artifacts/reports/naming/compliance_report.json

# Run auto-fix pipeline
run-autofix:
	@echo "Running auto-fix pipeline..."
	@python3 ecosystem/enforce.py --audit --auto-fix

# Create feature branch
create-branch:
	@if [ -z "$(BRANCH_NAME)" ]; then \
		echo "Error: BRANCH_NAME not set"; \
		echo "Usage: make create-branch BRANCH_NAME=feature/my-feature"; \
		exit 1; \
	fi
	@echo "Creating branch: $(BRANCH_NAME)"
	@git checkout -b $(BRANCH_NAME)

# Push to remote
push:
	@if [ -z "$(BRANCH_NAME)" ]; then \
		git push origin main; \
	else \
		git push origin $(BRANCH_NAME); \
	fi

# Create PR
create-pr:
	@gh pr create --title "$(TITLE)" --body "$(BODY)" --base main

# Monitor system logs
logs:
	@echo "Monitoring system logs (Ctrl+C to exit)..."
	@tail -f ecosystem/logs/audit/*.jsonl 2>/dev/null || echo "No logs found"

# Generate SBOM
generate-sbom:
	@echo "Generating SBOM..."
	@syft . -o spdx-json > sbom.json
	@echo "SBOM generated: sbom.json"

# Security scan
security-scan:
	@echo "Running security scan..."
	@trivy fs --severity HIGH,CRITICAL . > security_report.txt
	@echo "Security report: security_report.txt"

# Install dependencies
install-deps:
	@echo "Installing dependencies..."
	@pip install -r requirements.txt

# Run development server
dev:
	@echo "Starting development server..."
	@python3 -m platforms.gl.platform-assistant.api.server

# Format code
format:
	@echo "Formatting code..."
	@python3 -m black ecosystem/ platforms/
	@python3 -m isort ecosystem/ platforms/

# Check code quality
quality:
	@echo "Checking code quality..."
	@python3 -m pylint ecosystem/ platforms/ --fail-under=8.0

# Generate documentation
docs:
	@echo "Generating documentation..."
	@mkdocs build

# Serve documentation
docs-serve:
	@echo "Serving documentation..."
	@mkdocs serve

# Run migrations
migrate:
	@echo "Running database migrations..."
	@python3 ecosystem/scripts/migrate.py

# Backup data
backup:
	@echo "Creating backup..."
	@tar -czf backup_$(shell date +%Y%m%d_%H%M%S).tar.gz \
		ecosystem/data/ \
		ecosystem/indexes/ \
		ecosystem/logs/

# Restore backup
restore:
	@if [ -z "$(BACKUP_FILE)" ]; then \
		echo "Error: BACKUP_FILE not set"; \
		echo "Usage: make restore BACKUP_FILE=backup_20240101_120000.tar.gz"; \
		exit 1; \
	fi
	@echo "Restoring from $(BACKUP_FILE)..."
	@tar -xzf $(BACKUP_FILE)

# Build Docker image
docker-build:
	@echo "Building Docker image..."
	@docker build -t mnga:latest .

# Run Docker container
docker-run:
	@echo "Running Docker container..."
	@docker run -p 8000:8000 mnga:latest

# Deploy to staging
deploy-staging:
	@echo "Deploying to staging..."
	@./scripts/deploy.sh staging

# Deploy to production
deploy-prod:
	@echo "Deploying to production..."
	@./scripts/deploy.sh production

# Rollback deployment
rollback:
	@echo "Rolling back deployment..."
	@./scripts/rollback.sh

# Monitor resources
monitor:
	@echo "Monitoring system resources..."
	@htop

# Check dependencies
check-deps:
	@echo "Checking for outdated dependencies..."
	@pip list --outdated

# Update dependencies
update-deps:
	@echo "Updating dependencies..."
	@pip install --upgrade -r requirements.txt
	@pip freeze > requirements.txt

# Run benchmarks
benchmark:
	@echo "Running benchmarks..."
	@python3 ecosystem/scripts/benchmark.py

# Generate metrics report
metrics:
	@echo "Generating metrics report..."
	@python3 ecosystem/scripts/generate_metrics.py \
		--output artifacts/reports/metrics/report.json

# Health check
health:
	@echo "Checking system health..."
	@python3 ecosystem/scripts/health_check.py

# Print system status
status:
	@echo "System Status:"
	@echo "================"
	@echo "Git branch: $$(git branch --show-current)"
	@echo "Python version: $$(python3 --version)"
	@echo "Virtual env: $$(if [ -d venv ]; then echo "Active"; else echo "Not active"; fi)"
	@echo "Last enforce: $$(ls -lt ecosystem/logs/audit/*.json 2>/dev/null | head -1 | awk '{print $$6, $$7, $$8}' || echo "Never")"
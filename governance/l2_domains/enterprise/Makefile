# Enterprise Governance Framework - Makefile
# Provides convenient commands for development, testing, and deployment

.PHONY: help install dev test test-fast test-integration lint lint-fix format format-check build run clean docker-build docker-up docker-down docker-logs audit security-check validate-prereqs quick-verify bootstrap start-min stop

# Default target
.DEFAULT_GOAL := help

# Variables
PYTHON := python3
VENV := .venv
ACTIVATE := $(VENV)/bin/activate
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest

# Colors
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[1;33m
NC := \033[0m

## ============================================
## Help
## ============================================

help: ## Show this help message
	@echo "$(BLUE)Enterprise Governance Framework - Available Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""

## ============================================
## Installation & Setup
## ============================================

install: ## Install all dependencies
	@echo "$(BLUE)Installing dependencies...$(NC)"
	@./scripts/install-deps.sh

bootstrap: ## Run complete bootstrap setup
	@echo "$(BLUE)Bootstrapping environment...$(NC)"
	@./scripts/bootstrap.sh

validate-prereqs: ## Validate all prerequisites
	@echo "$(BLUE)Validating prerequisites...$(NC)"
	@./scripts/validate-prereqs.sh

quick-verify: ## Run quick verification (<30 seconds)
	@echo "$(BLUE)Running quick verification...$(NC)"
	@./scripts/quick-verify.sh

## ============================================
## Development
## ============================================

dev: ## Start development server
	@echo "$(BLUE)Starting development server...$(NC)"
	@if [ -f $(ACTIVATE) ]; then \
		source $(ACTIVATE) && \
		python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload; \
	else \
		echo "$(YELLOW)Virtual environment not found. Run 'make install' first.$(NC)"; \
		exit 1; \
	fi

start-min: ## Start minimal services
	@echo "$(BLUE)Starting minimal services...$(NC)"
	@./scripts/start-min.sh

stop: ## Stop all running services
	@echo "$(BLUE)Stopping services...$(NC)"
	@for pidfile in *.pid; do \
		if [ -f "$$pidfile" ]; then \
			pid=$$(cat $$pidfile); \
			if kill -0 $$pid 2>/dev/null; then \
				kill $$pid && echo "Stopped PID $$pid"; \
			fi; \
			rm -f $$pidfile; \
		fi; \
	done 2>/dev/null || true

run: ## Run application (production mode)
	@echo "$(BLUE)Running application...$(NC)"
	@if [ -f $(ACTIVATE) ]; then \
		source $(ACTIVATE) && \
		uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4; \
	else \
		echo "$(YELLOW)Virtual environment not found. Run 'make install' first.$(NC)"; \
		exit 1; \
	fi

## ============================================
## Testing
## ============================================

test: ## Run all tests
	@echo "$(BLUE)Running full test suite...$(NC)"
	@if [ -f $(ACTIVATE) ]; then \
		source $(ACTIVATE) && \
		$(PYTEST) tests/ -v --cov=src --cov-report=html --cov-report=term; \
	else \
		echo "$(YELLOW)Virtual environment not found. Run 'make install' first.$(NC)"; \
		exit 1; \
	fi

test-fast: ## Run fast tests (<30 seconds)
	@echo "$(BLUE)Running fast tests...$(NC)"
	@if [ -f $(ACTIVATE) ]; then \
		source $(ACTIVATE) && \
		$(PYTEST) tests/test_fast.py -v --tb=short --maxfail=5; \
	else \
		echo "$(YELLOW)Virtual environment not found. Run 'make install' first.$(NC)"; \
		exit 1; \
	fi

test-integration: ## Run integration tests
	@echo "$(BLUE)Running integration tests...$(NC)"
	@if [ -f $(ACTIVATE) ]; then \
		source $(ACTIVATE) && \
		$(PYTEST) tests/integration/ -v --tb=short; \
	else \
		echo "$(YELLOW)Virtual environment not found. Run 'make install' first.$(NC)"; \
		exit 1; \
	fi

## ============================================
## Code Quality
## ============================================

lint: ## Run linters (black, ruff, mypy)
	@echo "$(BLUE)Running linters...$(NC)"
	@if [ -f $(ACTIVATE) ]; then \
		source $(ACTIVATE) && \
		echo "Checking with black..." && \
		black --check src/ tests/ && \
		echo "Checking with ruff..." && \
		ruff check src/ tests/ && \
		echo "Checking with mypy..." && \
		mypy src/ || true; \
	else \
		echo "$(YELLOW)Virtual environment not found. Run 'make install' first.$(NC)"; \
		exit 1; \
	fi

lint-fix: ## Fix linting issues automatically
	@echo "$(BLUE)Fixing linting issues...$(NC)"
	@if [ -f $(ACTIVATE) ]; then \
		source $(ACTIVATE) && \
		echo "Running black..." && \
		black src/ tests/ && \
		echo "Running ruff..." && \
		ruff check --fix src/ tests/; \
	else \
		echo "$(YELLOW)Virtual environment not found. Run 'make install' first.$(NC)"; \
		exit 1; \
	fi

format: ## Format code with black
	@echo "$(BLUE)Formatting code...$(NC)"
	@if [ -f $(ACTIVATE) ]; then \
		source $(ACTIVATE) && \
		black src/ tests/; \
	else \
		echo "$(YELLOW)Virtual environment not found. Run 'make install' first.$(NC)"; \
		exit 1; \
	fi

format-check: ## Check code formatting
	@echo "$(BLUE)Checking code formatting...$(NC)"
	@if [ -f $(ACTIVATE) ]; then \
		source $(ACTIVATE) && \
		black --check src/ tests/; \
	else \
		echo "$(YELLOW)Virtual environment not found. Run 'make install' first.$(NC)"; \
		exit 1; \
	fi

## ============================================
## Security & Audit
## ============================================

audit: ## Run security and compliance audit
	@echo "$(BLUE)Running security audit...$(NC)"
	@if [ -f $(ACTIVATE) ]; then \
		source $(ACTIVATE) && \
		echo "Running bandit..." && \
		bandit -r src/ -f json -o reports/bandit-report.json || true && \
		echo "Running safety check..." && \
		safety check --json --output reports/safety-report.json || true; \
	else \
		echo "$(YELLOW)Virtual environment not found. Run 'make install' first.$(NC)"; \
		exit 1; \
	fi

security-check: ## Run comprehensive security checks
	@echo "$(BLUE)Running security checks...$(NC)"
	@if [ -f $(ACTIVATE) ]; then \
		source $(ACTIVATE) && \
		bandit -r src/ && \
		safety check && \
		echo "$(GREEN)All security checks passed$(NC)"; \
	else \
		echo "$(YELLOW)Virtual environment not found. Run 'make install' first.$(NC)"; \
		exit 1; \
	fi

## ============================================
## Docker
## ============================================

docker-build: ## Build Docker images
	@echo "$(BLUE)Building Docker images...$(NC)"
	docker-compose build

docker-up: ## Start all Docker services
	@echo "$(BLUE)Starting Docker services...$(NC)"
	docker-compose up -d

docker-down: ## Stop all Docker services
	@echo "$(BLUE)Stopping Docker services...$(NC)"
	docker-compose down

docker-logs: ## Show Docker service logs
	docker-compose logs -f

docker-restart: ## Restart Docker services
	@echo "$(BLUE)Restarting Docker services...$(NC)"
	docker-compose restart

## ============================================
## Build & Cleanup
## ============================================

build: ## Build the project
	@echo "$(BLUE)Building project...$(NC)"
	@if [ -f $(ACTIVATE) ]; then \
		source $(ACTIVATE) && \
		python -m build; \
	else \
		echo "$(YELLOW)Virtual environment not found. Run 'make install' first.$(NC)"; \
		exit 1; \
	fi

clean: ## Clean temporary files and directories
	@echo "$(BLUE)Cleaning temporary files...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build dist .coverage htmlcov
	rm -rf reports/*.json reports/*.html
	rm -rf logs/*.log
	rm -f *.pid
	@echo "$(GREEN)Clean complete$(NC)"

clean-all: ## Clean everything including virtual environment
	@echo "$(BLUE)Deep clean...$(NC)"
	$(MAKE) clean
	rm -rf $(VENV)
	rm -rf data/evidence/* data/events/*
	@echo "$(GREEN)Deep clean complete$(NC)"

## ============================================
## Utilities
## ============================================

init-db: ## Initialize database
	@echo "$(BLUE)Initializing database...$(NC)"
	@if [ -f $(ACTIVATE) ]; then \
		source $(ACTIVATE) && \
		alembic upgrade head; \
	fi

migrate: ## Run database migrations
	@echo "$(BLUE)Running migrations...$(NC)"
	@if [ -f $(ACTIVATE) ]; then \
		source $(ACTIVATE) && \
		alembic upgrade head; \
	fi

reset-db: ## Reset database (WARNING: Deletes all data)
	@echo "$(YELLOW)WARNING: This will delete all data!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		source $(ACTIVATE) && \
		alembic downgrade base && \
		alembic upgrade head; \
	fi

shell: ## Open Python shell with environment loaded
	@if [ -f $(ACTIVATE) ]; then \
		source $(ACTIVATE) && \
		python -c "from src.audit.logger import get_audit_logger; print('Audit logger loaded')"; \
		python; \
	else \
		echo "$(YELLOW)Virtual environment not found. Run 'make install' first.$(NC)"; \
		exit 1; \
	fi

show-env: ## Show current environment configuration
	@echo "$(BLUE)Current environment:$(NC)"
	@if [ -f .env ]; then \
		grep -v "SECRET\|PASSWORD\|TOKEN" .env | sort; \
	else \
		echo "$(YELLOW).env file not found$(NC)"; \
	fi
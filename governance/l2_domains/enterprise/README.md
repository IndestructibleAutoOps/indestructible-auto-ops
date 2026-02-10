# Enterprise DevSecOps Governance Framework

> A comprehensive, enterprise-grade DevSecOps and supply chain governance framework with full auditability, compliance, and security capabilities.

## 🏗️ Overview

This framework provides a complete solution for enterprise engineering governance, including:

- **Audit Trail System**: Full operation logging with OpenTelemetry integration
- **Governance Enforcement**: 20 Forbidden Principles implementation
- **Supply Chain Security**: SBOM generation, vulnerability scanning, dependency management
- **Multi-Language Support**: Python, Node.js, Go, Java
- **Container Orchestration**: Docker, Kubernetes support
- **Monitoring & Observability**: Prometheus, Grafana, Jaeger integration
- **CI/CD Integration**: GitHub Actions, GitLab CI, Jenkins support
- **Compliance Ready**: SOC 2, ISO 27001, GDPR compliance features

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher (optional)
- Docker and Docker Compose (optional)
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/IndestructibleAutoOps/indestructibleautoops.git
cd indestructibleautoops/enterprise-governance

# 2. Run bootstrap script (installs all dependencies)
./scripts/bootstrap.sh

# 3. Configure environment
cp .env.example .env
./scripts/fix-env.sh

# 4. Verify installation
./scripts/quick-verify.sh

# 5. Start services
./scripts/start-min.sh
```

### Quick Verification

Run the fast test suite (<30 seconds):

```bash
make test-fast
```

Or use the verification script:

```bash
./scripts/quick-verify.sh
```

## 📁 Project Structure

```
enterprise-governance/
├── src/                      # Source code
│   ├── audit/               # Audit logging system
│   │   └── logger.py        # OpenTelemetry-enabled logger
│   ├── governance/          # Governance enforcement
│   │   └── enforcer.py      # 20 Forbidden Principles enforcer
│   ├── security/            # Security modules
│   ├── monitoring/          # Monitoring & metrics
│   ├── api/                 # API endpoints
│   └── utils/               # Utilities
├── tests/                   # Test suites
│   ├── test_fast.py         # Fast tests (<30s)
│   ├── unit/                # Unit tests
│   └── integration/         # Integration tests
├── scripts/                 # Automation scripts
│   ├── bootstrap.sh         # Complete setup
│   ├── start-min.sh         # Minimal service start
│   ├── quick-verify.sh      # Quick verification
│   ├── validate-prereqs.sh  # Prerequisites check
│   ├── install-deps.sh      # Dependency installation
│   └── fix-env.sh           # Environment fix
├── infrastructure/          # IaC configurations
│   ├── deployment/          # Deployment configs
│   ├── kubernetes/          # K8s manifests
│   ├── docker/              # Docker configs
│   └── monitoring/          # Monitoring stack
├── docs/                    # Documentation
│   ├── architecture/        # Architecture docs
│   ├── specifications/      # Technical specs
│   └── governance/          # Governance policies
├── specifications/          # Governance specs
│   ├── policies/            # Policy definitions
│   ├── schemas/             # Data schemas
│   └── workflows/           # Workflow definitions
├── configs/                 # Configuration files
│   ├── environments/        # Environment configs
│   ├── logging/             # Logging configs
│   └── security/            # Security configs
├── data/                    # Data directories
│   ├── evidence/            # Audit evidence
│   ├── events/              # Event logs
│   └── migrations/          # Database migrations
├── tools/                   # CLI tools and utilities
│   ├── cli/                 # Command-line interface
│   ├── scripts/             # Utility scripts
│   └── migrations/          # Migration tools
├── examples/                # Usage examples
│   ├── basic-usage/         # Basic examples
│   ├── advanced-scenarios/  # Advanced examples
│   └── integration/         # Integration examples
├── reports/                 # Generated reports
│   ├── coverage/            # Code coverage
│   ├── security/            # Security reports
│   ├── performance/         # Performance reports
│   └── compliance/          # Compliance reports
├── pyproject.toml           # Python project config
├── package.json             # Node.js project config
├── Dockerfile               # Docker image definition
├── docker-compose.yaml      # Docker orchestration
├── Makefile                 # Build commands
├── .env.example             # Environment template
└── README.md                # This file
```

## 🔧 Usage

### Using Make Commands

```bash
# Installation
make install              # Install all dependencies
make bootstrap            # Run complete setup
make validate-prereqs     # Validate prerequisites

# Development
make dev                  # Start development server
make start-min            # Start minimal services
make stop                 # Stop services

# Testing
make test                 # Run all tests
make test-fast            # Run fast tests (<30s)
make test-integration     # Run integration tests

# Code Quality
make lint                 # Run linters
make lint-fix             # Fix linting issues
make format               # Format code
make format-check         # Check formatting

# Security
make audit                # Run security audit
make security-check       # Comprehensive security checks

# Docker
make docker-build         # Build Docker images
make docker-up            # Start Docker services
make docker-down          # Stop Docker services
make docker-logs          # View logs

# Database
make init-db              # Initialize database
make migrate              # Run migrations
make reset-db             # Reset database (WARNING)

# Utilities
make clean                # Clean temporary files
make clean-all            # Clean everything
make shell                # Open Python shell
make show-env             # Show environment config
```

### Using Scripts

```bash
# Complete setup
./scripts/bootstrap.sh

# Quick verification
./scripts/quick-verify.sh

# Start minimal services
./scripts/start-min.sh

# Fix environment
./scripts/fix-env.sh

# Validate prerequisites
./scripts/validate-prereqs.sh
```

### Using Docker

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart services
docker-compose restart
```

## 🔐 Security & Compliance

### 20 Forbidden Principles

The framework enforces 20 forbidden principles across 5 categories:

1. **AI Control Boundary** (5 principles)
   - FP-001: AI directly triggers mode switching
   - FP-002: Semantic triggers as control signals
   - FP-003: AI as final decision source
   - FP-004: AI modifies own control parameters
   - FP-005: AI bypasses event verification

2. **Event Handling** (4 principles)
   - FP-006: Events without governance layer validation
   - FP-007: Non-deterministic event formats
   - FP-008: Events without time ordering guarantees
   - FP-009: Event loss without tracking

3. **Switcher** (4 principles)
   - FP-010: Non-deterministic switcher
   - FP-011: Switching without state snapshots
   - FP-012: Switching without isolation boundaries
   - FP-013: Switching without rollback mechanism

4. **Governance Layer** (4 principles)
   - FP-014: Governance layer bypass
   - FP-015: Governance rules without version control
   - FP-016: Governance decisions without causal chain
   - FP-017: Governance layer without health monitoring

5. **Audit & Reconstruction** (3 principles)
   - FP-018: Operations without complete audit trail
   - FP-019: System state cannot be reconstructed
   - FP-020: No independent verification mechanism

### Security Features

- **Audit Logging**: Complete operation logging with OpenTelemetry
- **SBOM Generation**: Software Bill of Materials for all artifacts
- **Vulnerability Scanning**: Automated dependency vulnerability detection
- **Secret Management**: Secure handling of sensitive data
- **RBAC**: Role-Based Access Control
- **SIEM Integration**: Integration with security information and event management systems

### Compliance Standards

- **SOC 2**: Service Organization Control Type 2
- **ISO 27001**: Information Security Management
- **GDPR**: General Data Protection Regulation
- **HIPAA**: Health Insurance Portability and Accountability Act

## 📊 Monitoring & Observability

### Metrics

- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and dashboards
- **Custom Metrics**: Business and operational metrics

### Logging

- **Structured Logging**: JSONL format with OpenTelemetry
- **Log Aggregation**: Centralized log collection
- **Log Retention**: Configurable retention policies

### Tracing

- **OpenTelemetry**: Distributed tracing
- **Jaeger**: Trace visualization and analysis
- **Span Context**: Complete request tracing

## 🔌 Integration

### CI/CD Integration

```yaml
# Example GitHub Actions workflow
name: Governance Check
on: [push, pull_request]
jobs:
  governance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Governance Checks
        run: |
          make test-fast
          make lint
          make security-check
```

### API Integration

```python
from src.audit.logger import get_audit_logger

# Get audit logger
logger = get_audit_logger()

# Log an event
record = logger.log(
    actor="user@example.com",
    action="create:resource",
    resource="resource://example/id",
    result="success",
    metadata={"key": "value"}
)
```

### Governance Enforcement

```python
from src.governance.enforcer import GovernanceEnforcer

# Create enforcer
enforcer = GovernanceEnforcer()

# Check codebase
violations = enforcer.check_directory("./src")

# Generate report
report = enforcer.generate_report()
```

## 📚 Documentation

- [Architecture](docs/architecture/README.md)
- [API Documentation](docs/api/README.md)
- [Governance Policies](docs/governance/policies.md)
- [Deployment Guide](docs/deployment/README.md)
- [Troubleshooting](docs/troubleshooting/README.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `make test`
5. Run linting: `make lint`
6. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/IndestructibleAutoOps/indestructibleautoops/issues)
- **Documentation**: [Project Docs](https://github.com/IndestructibleAutoOps/indestructibleautoops/tree/main/enterprise-governance/docs)
- **Email**: engineering@example.com

## 🎯 Roadmap

- [ ] Complete CI/CD pipeline templates
- [ ] Advanced threat detection
- [ ] Multi-cloud deployment support
- [ ] AI-powered governance recommendations
- [ ] Enhanced reporting dashboards
- [ ] Mobile app for monitoring

---

**Built with ❤️ by the Enterprise Governance Team**
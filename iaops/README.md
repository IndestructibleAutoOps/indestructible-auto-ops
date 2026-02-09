# IndestructibleAutoOps Skeleton-to-ClosedLoop

IAOPS Governance Framework - A production-ready governance engine with DAG validation, role-based access control, and evidence sealing.

## Features

- **DAG Dependency Validation** - Ensures task flows have no circular dependencies
- **Role-Based Access Control** - RBAC system for permission management
- **Evidence Chain Sealing** - Hash-manifest + seal manifest mechanism
- **Auto-Patch Verification** - Automated patching and verification workflows
- **Multi-language Support** - Python, Go, Node.js adapters

## Installation

```bash
# Install from iaops directory
cd iaops
python3 -m pip install -e .[dev]
```

## Usage

```bash
# Run in plan mode (dry-run)
python3 -m indestructibleautoops run --config configs/indestructibleautoops.pipeline.yaml --project . --mode plan

# Run in repair mode
python3 -m indestructibleautoops run --config configs/indestructibleautoops.pipeline.yaml --project . --mode repair
```

## Development

```bash
# Run linter
make lint

# Run tests
make test

# Or use pytest directly
python3 -m pytest tests/ -v
```

## CI/CD

The IAOPS CI workflow is located at the repository root in `.github/workflows/iaops-ci.yml`

This workflow runs automatically on:
- Pushes affecting `iaops/**` paths
- Pull requests affecting `iaops/**` paths

The workflow uses `working-directory: iaops` to execute tests in the correct context.

## Architecture

```
iaops/
├── src/indestructibleautoops/  # Core governance components
│   ├── engine.py              # Main governance engine
│   ├── planner.py             # Task planner
│   ├── graph.py               # DAG graph validation
│   ├── scanner.py             # File path scanner
│   ├── patcher.py             # Auto-patcher with template support
│   ├── verifier.py            # Verification engine
│   ├── sealing.py             # Evidence chain sealing
│   └── hashing.py             # Hash computation
├── configs/                   # Configuration system
├── schemas/                   # JSON Schema definitions
├── tests/                     # Comprehensive test suite
└── examples/                  # Example projects
```

## Governance Compliance

- ✅ No procedural theater - Substantive governance mechanisms
- ✅ Separation of duties - Clear role definitions
- ✅ Learning & adaptation - Built-in feedback loops
- ✅ Information transparency - Full observability
- ✅ Culture & process alignment - Governance documentation system

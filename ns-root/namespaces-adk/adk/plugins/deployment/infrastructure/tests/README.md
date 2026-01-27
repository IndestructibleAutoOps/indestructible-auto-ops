# Infrastructure Components Tests

This directory contains comprehensive unit and integration tests for all infrastructure components.

## Test Structure

```
tests/
├── __init__.py
├── pytest.ini
├── README.md
├── test_monitoring_manager.py
├── test_secrets_manager.py
├── test_container_orchestration.py
├── test_disaster_recovery.py
├── test_log_aggregation.py
├── test_performance_monitoring.py
└── test_integration.py
```

## Test Coverage

### Unit Tests

1. **Monitoring Stack Manager** (`test_monitoring_manager.py`)
   - Configuration tests
   - Alert rule management
   - Scrape configuration
   - Dashboard management
   - Deployment tests
   - Statistics and metrics

2. **Secrets Manager** (`test_secrets_manager.py`)
   - Configuration tests
   - Secret CRUD operations
   - Encryption/decryption
   - Rotation policies
   - Audit logging
   - Cache management

3. **Container Orchestration Manager** (`test_container_orchestration.py`)
   - Configuration tests
   - Container deployment
   - Service management
   - Scaling operations
   - Rollback functionality
   - Validation tests

4. **Disaster Recovery Manager** (`test_disaster_recovery.py`)
   - Configuration tests
   - Backup operations
   - Restore operations
   - Failover/failback
   - DR drills
   - Compliance reporting

5. **Log Aggregation Manager** (`test_log_aggregation.py`)
   - Configuration tests
   - ELK stack deployment
   - Log ingestion
   - Search and filtering
   - Statistics

6. **Performance Monitoring Manager** (`test_performance_monitoring.py`)
   - Configuration tests
   - Distributed tracing
   - Metrics recording
   - Performance baselines
   - Anomaly detection

### Integration Tests

- **Full Stack Integration** (`test_integration.py`)
  - Complete infrastructure deployment
  - Component interactions
  - End-to-end workflows
  - Lifecycle management

## Running Tests

### Run All Tests
```bash
cd ns-root/namespaces-adk/adk/plugins/deployment/infrastructure
python -m pytest tests/ -v
```

### Run Specific Test File
```bash
python -m pytest tests/test_monitoring_manager.py -v
```

### Run with Coverage
```bash
python -m pytest tests/ --cov=infrastructure --cov-report=html
```

### Run Specific Test Class
```bash
python -m pytest tests/test_monitoring_manager.py::TestMonitoringConfig -v
```

### Run Specific Test Function
```bash
python -m pytest tests/test_monitoring_manager.py::TestMonitoringStackManager::test_deploy_monitoring_stack -v
```

### Run Only Unit Tests
```bash
python -m pytest tests/ -m unit -v
```

### Run Only Integration Tests
```bash
python -m pytest tests/ -m integration -v
```

## Test Statistics

| Component | Test Classes | Test Methods | Estimated Coverage |
|-----------|--------------|--------------|-------------------|
| Monitoring Stack Manager | 5 | 25+ | 90%+ |
| Secrets Manager | 4 | 30+ | 90%+ |
| Container Orchestration | 6 | 35+ | 90%+ |
| Disaster Recovery | 4 | 25+ | 90%+ |
| Log Aggregation | 5 | 20+ | 90%+ |
| Performance Monitoring | 4 | 15+ | 90%+ |
| Integration | 1 | 6 | 85%+ |
| **Total** | **29** | **156+** | **90%+** |

## Test Categories

### Unit Tests
- Test individual classes and methods
- Mock external dependencies
- Fast execution (<1s per test)

### Integration Tests
- Test component interactions
- Test end-to-end workflows
- Slower execution (1-10s per test)

## Requirements

```bash
pip install pytest pytest-asyncio pytest-cov pytest-mock
```

## CI/CD Integration

These tests are designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run Tests
  run: |
    cd ns-root/namespaces-adk/adk/plugins/deployment/infrastructure
    python -m pytest tests/ --cov=infrastructure --cov-report=xml

- name: Upload Coverage
  uses: codecov/codecov-action@v3
  with:
    files: ./ns-root/namespaces-adk/adk/plugins/deployment/infrastructure/coverage.xml
```

## Best Practices

1. **Isolation**: Each test should be independent
2. **Speed**: Unit tests should be fast (<1s)
3. **Clarity**: Test names should describe what they test
4. **Coverage**: Aim for 90%+ coverage
5. **Documentation**: Add docstrings for complex tests

## Troubleshooting

### Import Errors
If you encounter import errors, ensure you're running from the correct directory:
```bash
cd /workspace/machine-native-ops
python -m pytest ns-root/namespaces-adk/adk/plugins/deployment/infrastructure/tests/
```

### Async Test Failures
Ensure pytest-asyncio is installed and tests use `@pytest.mark.asyncio`:
```bash
pip install pytest-asyncio
```

### Coverage Issues
For accurate coverage, run tests with the correct source path:
```bash
python -m pytest tests/ --cov=../../infrastructure
```

## Contributing

When adding new tests:

1. Follow the naming convention: `test_<component>_<feature>.py`
2. Use descriptive test names
3. Add appropriate markers (unit/integration)
4. Update this README with new test statistics
5. Ensure all tests pass before committing

## Test Status

- ✅ All unit tests implemented
- ✅ All integration tests implemented
- ✅ Coverage target: 90%+
- ✅ CI/CD ready
- ✅ Documentation complete
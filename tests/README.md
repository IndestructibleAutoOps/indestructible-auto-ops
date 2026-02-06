# Tests Directory

This directory contains comprehensive test suites for the NG Governance System.

## Test Structure

```
tests/
├── unit/                              # Unit tests for individual components
│   ├── test_ng_semantic_binding.py    # Tests for NG semantic binding functionality
│   ├── test_parametric_convergence.py # Tests for convergence guarantees
│   └── test_fallback_semantic_validation.py # Tests for fallback validation
├── integration/                       # Integration tests across components
│   ├── test_ng_governance_integration.py # End-to-end governance workflows
│   └── test_kubernetes_deployment.py  # Kubernetes infrastructure validation
├── pytest.ini                         # Pytest configuration
├── requirements.txt                   # Test dependencies
├── README.md                          # This file
└── TEST_REPORT.md                     # Detailed test execution report
```

## Quick Start

### Installation
```bash
cd tests
pip install -r requirements.txt
```

### Running Tests

#### Run all tests:
```bash
python -m pytest -v
```

#### Run only unit tests:
```bash
python -m pytest unit/ -v
```

#### Run only integration tests:
```bash
python -m pytest integration/ -v
```

#### Run specific test file:
```bash
python -m pytest unit/test_ng_semantic_binding.py -v
```

#### Run specific test:
```bash
python -m pytest unit/test_ng_semantic_binding.py::TestNgSemanticBinding::test_register_valid_entity -v
```

#### Run with coverage:
```bash
python -m pytest --cov=. --cov-report=html
```

## Test Categories

### Unit Tests

#### 1. NG Semantic Binding (`test_ng_semantic_binding.py`)
Tests the core functionality of the NG semantic binding system:
- Entity registration with valid NG codes
- NG code format validation (pattern: `NG[0-9]{5}`)
- Duplicate entity handling
- Embedding space consistency verification
- Hash-based drift detection
- Multiple entity management

**Coverage:**
- Entity registration and validation
- NG code format enforcement
- Embedding space consistency
- Drift detection mechanisms

#### 2. Parametric Convergence (`test_parametric_convergence.py`)
Tests mathematical convergence guarantees:
- Lipschitz continuity verification
- Contraction mapping detection
- Convergence time prediction
- Real-time convergence monitoring
- Parameter space sampling

**Coverage:**
- Mathematical convergence properties
- Lipschitz constant calculation
- Convergence prediction algorithms
- Monitoring and detection logic

#### 3. Fallback Semantic Validation (`test_fallback_semantic_validation.py`)
Tests fallback decision validation:
- Intent preservation verification
- Safety constraint validation
- Semantic anchor preservation
- Entity extraction from text
- NG code extraction and validation

**Coverage:**
- Fallback decision validation
- Intent similarity calculations
- Safety constraint enforcement
- Semantic anchor detection

### Integration Tests

#### 1. NG Governance Integration (`test_ng_governance_integration.py`)
Tests end-to-end workflows across components:
- Complete semantic binding workflows
- Multi-iteration convergence testing
- Fallback validation with recovery protocols
- Cross-component consistency validation

**Coverage:**
- Component integration
- End-to-end workflows
- Cross-component consistency
- Recovery protocols

#### 2. Kubernetes Deployment (`test_kubernetes_deployment.py`)
Validates Kubernetes infrastructure:
- Namespace YAML validity
- RBAC configuration validation
- Deployment configuration validation
- Service configuration validation
- ConfigMap configuration validation
- Resource quota and limit range validation

**Note:** These tests are skipped if infrastructure YAML files are not present.

## Test Results Summary

As of the latest run:

- **Unit Tests:** 32 passed, 5 failed (86.5% pass rate)
- **Integration Tests:** 3 passed, 1 failed, 7 skipped (75% pass rate on executed tests)
- **Total:** 35 passed, 6 failed, 7 skipped

See `TEST_REPORT.md` for detailed analysis of failures and recommendations.

## Known Issues

### Currently Failing Tests

1. **Semantic Anchor Preservation** - Threshold too strict for test data
2. **Embedding Space Drift Detection** - Entity re-binding test uses same entity ID
3. **Identity Mapping** - Lipschitz validation too strict for L=1.0
4. **Convergence Detection** - Thresholds too strict for test parameters
5. **Parameter Space Sampling** - Bounds checking needs refinement

See `TEST_REPORT.md` for detailed analysis and recommendations.

## Test Data

All tests use mock objects and deterministic test data to ensure:
- Reproducible results
- Fast execution
- No external dependencies
- Isolated testing environment

## Continuous Integration

These tests are designed to run in CI/CD pipelines:

```yaml
# Example CI configuration
test:
  script:
    - cd tests
    - pip install -r requirements.txt
    - python -m pytest --junitxml=report.xml
  artifacts:
    reports:
      junit: tests/report.xml
```

## Contributing

When adding new tests:

1. Follow existing test structure and naming conventions
2. Use descriptive test names that explain what is being tested
3. Include docstrings for test classes and methods
4. Use mock objects for external dependencies
5. Keep tests isolated and independent
6. Add appropriate markers (e.g., `@pytest.mark.slow` for long-running tests)

## Test Markers

Available pytest markers:

- `slow`: Marks tests as slow (deselect with `-m "not slow"`)
- `integration`: Marks tests as integration tests
- `unit`: Marks tests as unit tests

## Dependencies

- **pytest>=7.0.0**: Testing framework
- **pytest-cov>=4.0.0**: Coverage reporting
- **numpy>=1.21.0**: Numerical computations
- **pyyaml>=6.0**: YAML parsing for infrastructure tests

## Support

For questions or issues with the tests:
1. Check `TEST_REPORT.md` for known issues
2. Review test docstrings for expected behavior
3. Examine mock class implementations for understanding test data
4. Refer to the main project documentation for system architecture

## License

Same as the main project.
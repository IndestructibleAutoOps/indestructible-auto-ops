<!-- @GL-governed -->
<!-- @GL-layer: GL90-99 -->
<!-- @GL-semantic: governed-documentation -->
<!-- @GL-audit-trail: engine/governance/GL_SEMANTIC_ANCHOR.json -->

# GL Unified Charter Activated
# Test Suite Workflow

## Overview

The Test Suite workflow provides automated testing with visual test result dashboards using the TestForest Dashboard (powered by test-summary/action@v2.3).

## Features

- **Automated Testing**: Runs unit, integration, and e2e tests automatically
- **TestForest Dashboard**: Visual test result summaries in GitHub Actions
- **JUnit XML Reports**: Standard test output format for compatibility
- **Coverage Reporting**: Code coverage metrics and reports
- **Parallel Safe**: Tests run with proper isolation

## Workflow Triggers

The workflow runs on:
- **Pull Requests**: When opened, synchronized, or reopened
- **Push to Main/Develop**: On commits to main or develop branches
- **Manual Trigger**: Via workflow_dispatch

## Test Types

### Unit Tests
- Location: `tests/unit/`
- Fast, isolated tests
- Run with coverage tracking

### Integration Tests
- Location: `tests/integration/`
- Test component interactions
- Optional if no tests exist

### E2E Tests
- Location: `tests/e2e/`
- Full system workflow tests
- Optional if no tests exist

## TestForest Dashboard

The TestForest Dashboard step uses `test-summary/action@v2.3` to create visual test summaries:

```yaml
- name: TestForest Dashboard
  uses: test-summary/action@v2.3
  if: always()
  with:
    paths: "test-results/*.xml"
    show: "all"
```

### Features:
- **Visual Test Results**: See test outcomes at a glance
- **Failure Details**: Quickly identify failing tests
- **Always Runs**: Shows results even when tests fail
- **JUnit XML Support**: Works with pytest and other test frameworks

## Output Artifacts

The workflow generates several artifacts:

1. **Test Results** (`test-results/`)
   - JUnit XML files for each test type
   - Retention: 7 days

2. **Coverage Reports** (`coverage-reports/`)
   - XML coverage data
   - HTML coverage reports
   - Retention: 7 days

## GitHub Summary

After each run, the workflow generates a GitHub Step Summary showing:
- Test type status (Passed/Failed/Skipped)
- Coverage information
- Links to detailed reports

## Configuration

### Required Permissions

```yaml
permissions:
  contents: read
  checks: write
  pull-requests: write
```

### Python Version
- Python 3.11

### Test Dependencies
- pytest
- pytest-cov
- pytest-xdist
- pyyaml

## Usage Examples

### View Test Results
1. Navigate to the workflow run in GitHub Actions
2. Check the TestForest Dashboard step for visual summary
3. Download test-results artifacts for detailed analysis

### Local Testing
```bash
# Run all tests
pytest

# Run specific test type
pytest tests/unit/

# Generate coverage report
pytest --cov=workspace/src --cov-report=html

# Generate JUnit XML (same as CI)
pytest tests/unit/ --junitxml=test-results/unit-tests.xml
```

## Troubleshooting

### Tests Not Running
- Check that test files follow naming convention: `test_*.py` or `*_test.py`
- Ensure test dependencies are installed
- Verify Python path includes necessary modules

### TestForest Dashboard Not Showing
- Ensure JUnit XML files are generated in `test-results/` directory
- Check that the step runs with `if: always()`
- Verify permissions include `checks: write`

### Missing Coverage
- Coverage is only generated for unit tests
- Check that source code is in `workspace/src/`
- Verify pytest-cov is installed

## Related Documentation

- [Test Suite Documentation](../tests/README.md)
- [Pytest Configuration](../pytest.ini)
- [test-summary/action Documentation](https://github.com/test-summary/action)

## Maintenance

- Test results are retained for 7 days
- Coverage reports are retained for 7 days
- Workflow timeout: 20 minutes
- Concurrency: Cancels in-progress runs for same PR

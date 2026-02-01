@GL-governed
# CI/CD Integration

## Overview
Integrates Code Intelligence & Security Layer into CI/CD pipelines.

## Supported Platforms
1. **GitHub Actions**
2. **GitLab CI/CD**
3. **Jenkins**
4. **Azure DevOps**
5. **CircleCI**

## GitHub Actions Example
```yaml
name: Code Intelligence Scan
on: [push, pull_request]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: gl-platform/codeintel-action@v1
        with:
          source: ./src
          pattern: security
          fail-on-error: true
```

## GitLab CI Example
```yaml
code-intel-scan:
  stage: test
  image: gl-platform/codeintel:latest
  script:
    - gl-codeintel scan --source ./src --output report.json
  artifacts:
    reports:
      code_quality: report.json
```

## Features
- Automated security scanning
- Performance regression detection
- Architecture validation
- Test coverage analysis
- Customizable fail conditions
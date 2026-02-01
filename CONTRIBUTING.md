<!-- @GL-governed -->
<!-- @GL-layer: GL90-99 -->
<!-- @GL-semantic: governed-documentation -->
<!-- @GL-audit-trail: engine/governance/GL_SEMANTIC_ANCHOR.json -->

# Contributing to Machine Native Ops

Thank you for your interest in contributing to Machine Native Ops! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)
- [Testing Requirements](#testing-requirements)
- [GL Compliance Requirements](#gl-compliance-requirements)
- [Reporting Issues](#reporting-issues)

---

## Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [conduct@machinenativeops.com](mailto:conduct@machinenativeops.com) or by creating a GitHub issue with the `code-of-conduct` label.

---

## Getting Started

### Prerequisites

Before contributing, ensure you have:

- **Python 3.11 or higher** installed
- **Git** installed and configured
- **GitHub account** for pull requests and issues
- **Basic knowledge** of:
  - Python programming
  - Git workflow
  - YAML configuration
  - Markdown documentation
  - GL (Governance Layers) system concepts

### Setting Up Your Development Environment

1. **Fork the repository**
   ```bash
   # Click the "Fork" button on GitHub
   # Clone your fork locally
   git clone [EXTERNAL_URL_REMOVED]
   cd machine-native-ops
   ```

2. **Add upstream remote**
   ```bash
   git remote add upstream [EXTERNAL_URL_REMOVED]
   ```

3. **Install dependencies**
   ```bash
   # If requirements.txt exists
   pip install -r requirements.txt
   
   # Or initialize automation tools
   make automation-init
   ```

4. **Run quality checks**
   ```bash
   make automation-check
   ```

5. **Verify your setup**
   ```bash
   # Run GL implementation tests
   python scripts/gl/implementation/test_implementation.py
   ```

---

## Development Workflow

### Branch Naming Convention

Use descriptive branch names following this pattern:

```
<type>/<short-description>

Types:
- fix: Bug fixes
- feat: New features
- docs: Documentation changes
- refactor: Code refactoring
- test: Test additions or modifications
- chore: Maintenance tasks
- perf: Performance improvements
- gl: GL system changes (requires extra care)

Examples:
- fix/version-inconsistency
- feat/add-new-validator
- docs/update-readme
- refactor/simplify-validation
```

### Development Process

1. **Create a feature branch**
   ```bash
   git checkout -b feat/your-feature-name
   ```

2. **Make your changes**
   - Follow coding standards (see below)
   - Add tests for new functionality
   - Update documentation as needed
   - Ensure GL compliance

3. **Run validation**
   ```bash
   # Run GL validation
   python scripts/gl/validate-semantics.py
   
   # Run quantum validation
   python scripts/gl/quantum-validate.py
   
   # Run tests
   make test
   ```

4. **Commit your changes**
   - Follow commit message guidelines (see below)
   - Keep commits focused and atomic
   - Write clear, descriptive commit messages

5. **Push to your fork**
   ```bash
   git push origin feat/your-feature-name
   ```

6. **Create Pull Request**
   - Visit GitHub and create a PR
   - Fill out the PR template
   - Link related issues
   - Request review from maintainers

---

## Coding Standards

### Python Code Style

Follow these guidelines for Python code:

- **PEP 8** compliance (use `black` formatter)
- **Type hints** for function signatures
- **Docstrings** for all public functions and classes (Google style)
- **Line length**: maximum 100 characters
- **Imports**: organize in three groups (stdlib, third-party, local)
- **Naming conventions**:
  - Classes: `PascalCase`
  - Functions/variables: `snake_case`
  - Constants: `UPPER_SNAKE_CASE`
  - Private members: `_leading_underscore`

Example:
```python
"""
Module docstring describing the module's purpose.
"""

from typing import List, Optional
import sys

from gl.governance.base import GovernanceValidator


class MyValidator(GovernanceValidator):
    """A validator for GL compliance checking.
    
    Args:
        config_path: Path to the configuration file.
        strict_mode: Enable strict validation mode.
    """
    
    MAX_RETRIES = 3
    
    def __init__(self, config_path: str, strict_mode: bool = False) -> None:
        """Initialize the validator."""
        self.config_path = config_path
        self.strict_mode = strict_mode
        self._validation_results: List[dict] = []
    
    def validate(self, data: dict) -> bool:
        """Validate the provided data.
        
        Args:
            data: The data to validate.
            
        Returns:
            True if validation passes, False otherwise.
        """
        try:
            # Implementation here
            return True
        except Exception as e:
            self._handle_error(e)
            return False
```

### YAML Configuration Style

- **Indentation**: 2 spaces
- **Quoting**: prefer single quotes for strings
- **Comments**: use `#` for inline documentation
- **Alphabetical ordering** for list items where appropriate

Example:
```yaml
# GL Configuration File
version: "1.0.0"
name: "example-validator"

settings:
  strict_mode: true
  timeout: 30
  retries: 3

validators:
  - name: "semantic-validator"
    enabled: true
    priority: 1
    config:
      check_depth: true
      validate_references: true
```

### Markdown Documentation Style

- **Headings**: Use ATX style (`#`, `##`, etc.)
- **Lists**: Use `-` for unordered lists
- **Code blocks**: Specify language for syntax highlighting
- **Links**: Use descriptive link text
- **Tables**: Format with proper alignment

Example:
```markdown
# Heading

## Subheading

This is a paragraph with [a descriptive link]([EXTERNAL_URL_REMOVED]).

- Item 1
- Item 2

```python
# Code block with syntax highlighting
def example():
    return "Hello, World!"
```

| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |
```

---

## Commit Message Guidelines

### Format

Follow the [Conventional Commits]([EXTERNAL_URL_REMOVED]) specification:

```
<type>(<scope>): <short description>

[optional body]

[optional footer(s)]
```

### Types

- `fix`: Bug fix
- `feat`: New feature
- `docs`: Documentation only changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `gl`: GL governance system changes

### Scopes

Common scopes include:
- `readme`: README.md changes
- `docs`: Documentation changes
- `gl`: GL system changes
- `ci`: CI/CD changes
- `validation`: Validation system
- `implementation`: Implementation modules

### Examples

Good commit messages:
```
fix(readme): Correct version number from v2.0.0 to v1.0.0

- Update version to match CHANGELOG.md
- Ensure consistency across documentation

Closes #123
```

```
feat(gl): Add new quantum validation dimension

Implement the new 'reversibility' dimension for quantum validation.
This improves the overall validation accuracy by 2%.

Related to GL50-59 layer requirements.
```

```
docs(contributing): Add comprehensive contributing guidelines

Create detailed CONTRIBUTING.md with:
- Development workflow
- Coding standards
- Commit message guidelines
- PR process
- GL compliance requirements
```

Bad commit messages:
```
fixed bug
update stuff
wip
```

---

## Pull Request Process

### Before Submitting

1. **Ensure all tests pass**
   ```bash
   make test
   ```

2. **Run GL validation**
   ```bash
   python scripts/gl/validate-semantics.py
   python scripts/gl/quantum-validate.py
   ```

3. **Update documentation**
   - Update README.md if needed
   - Add/update inline documentation
   - Update CHANGELOG.md for significant changes

4. **Clean up commit history**
   - Squash related commits
   - Fix typos in commit messages
   - Ensure descriptive messages

### PR Template

Use this template when creating a PR:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issue
Fixes #123

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] GL validation passes
- [ ] Manual testing performed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review performed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added/updated
- [ ] All tests passing
- [ ] GL compliance verified
```

### PR Review Process

1. **Automated checks** must pass:
   - CI/CD pipeline
   - Code quality checks
   - GL validation

2. **Code review** by at least one maintainer

3. **Address review feedback** promptly

4. **Approval** required before merge

5. **Merge** typically via:
   - Squash and merge (for small PRs)
   - Merge commit (for significant features)

---

## Testing Requirements

### Unit Tests

- All new functions should have unit tests
- Aim for >80% code coverage
- Use descriptive test names
- Follow Arrange-Act-Assert pattern

Example:
```python
def test_semantic_validator_valid_input():
    """Test that semantic validator accepts valid input."""
    # Arrange
    validator = SemanticValidator()
    valid_data = {"name": "test", "type": "module"}
    
    # Act
    result = validator.validate(valid_data)
    
    # Assert
    assert result.is_valid is True
    assert result.errors == []
```

### Integration Tests

- Test module interactions
- Test GL governance flows
- Test CI/CD integration

### GL Validation Tests

- Run semantic validation: `python scripts/gl/validate-semantics.py`
- Run quantum validation: `python scripts/gl/quantum-validate.py`
- All GL layers must pass validation

---

## GL Compliance Requirements

### GL Semantic Boundaries

All changes must respect the GL governance layer boundaries (GL00-99):

- **GL00-09**: Strategic Layer - Vision, charter, objectives
- **GL10-29**: Operational Layer - Process policies, resource allocation
- **GL30-49**: Execution Layer - Deployment, project plans
- **GL50-59**: Observability Layer - Validation, metrics, alerts
- **GL60-80**: Feedback Layer - Reconciliation, innovation
- **GL81-83**: Extended Layer - External integration
- **GL90-99**: Meta Layer - Semantic root, governance standards

### Permitted Operations

✅ **Allowed**:
- Minimal operational fixes (bug fixes, typos, documentation)
- Non-breaking enhancements within existing semantic boundaries
- Test additions that respect GL validation framework
- Documentation improvements aligned with GL artifacts

❌ **Prohibited**:
- Semantic restructuring or layer redefinition
- Introduction of new governance concepts
- Modification of GL artifact relationships
- Changes to sealed governance components
- DAG topology alterations

### Validation Requirements

Before submitting a PR, ensure:

1. **Semantic validation passes**
   ```bash
   python scripts/gl/validate-semantics.py
   ```

2. **Quantum validation passes**
   ```bash
   python scripts/gl/quantum-validate.py
   ```

3. **No GL seal violations**
   - Check for unauthorized modifications
   - Verify artifact integrity

4. **DAG topology preserved**
   - No changes to dependency graph structure
   - Maintain existing parallelism patterns

---

## Reporting Issues

### Bug Reports

When reporting a bug, include:

1. **Clear title**
2. **Description**
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
3. **Environment**
   - OS and version
   - Python version
   - Git commit hash
4. **Screenshots/logs** (if applicable)
5. **Additional context**

### Feature Requests

When requesting a feature, include:

1. **Clear title**
2. **Problem statement**
   - What problem does this solve?
   - Why is this needed?
3. **Proposed solution**
   - Detailed description
   - Alternative solutions considered
4. **Additional context**
   - Use cases
   - Impact on GL system
   - Implementation ideas

### Documentation Issues

When reporting documentation issues:

1. **Location** (file and line number)
2. **Issue description**
3. **Suggested improvement**

---

## Getting Help

If you need help:

1. **Read the documentation**
   - [README.md](README.md)
   - [GL-STATUS-REPORT.md](GL-STATUS-REPORT.md)
   - [GL-CORE-INTEGRATION-REPORT.md](GL-CORE-INTEGRATION-REPORT.md)

2. **Search existing issues**
   - [GitHub Issues]([EXTERNAL_URL_REMOVED])

3. **Create a new issue**
   - Use appropriate labels
   - Provide detailed information

4. **Join the community**
   - Participate in discussions
   - Ask questions in issues
   - Help others

---

## Recognition

Contributors are recognized in:

- [CONTRIBUTORS.md](CONTRIBUTORS.md) (when created)
- Release notes
- Project documentation

Thank you for contributing to Machine Native Ops! 🎉

---

**Last Updated**: 2026-01-21  
**Maintained by**: MachineNativeOps Team
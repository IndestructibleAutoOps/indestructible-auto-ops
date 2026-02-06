<!-- @GL-governed -->
<!-- @GL-layer: GL90-99 -->
<!-- @GL-semantic: governed-documentation -->
<!-- @GL-audit-trail: engine/governance/GL_SEMANTIC_ANCHOR.json -->

# GitHub Copilot Instructions for Machine Native Ops

This document provides comprehensive instructions for GitHub Copilot coding agents working on the machine-native-ops project.

---

## ⚡ 開始前必讀 (MUST READ BEFORE STARTING)

**CRITICAL**: Before making ANY changes to this repository, you MUST:

### 1. Execute Ecosystem Enforcement

```bash
# Run the unified ecosystem enforcement checker
python ecosystem/enforce.py
```

**This check is MANDATORY**. If it fails:
- ❌ **DO NOT** proceed with code changes
- ❌ **DO NOT** bypass the checks
- ✅ **FIX** the reported issues first
- ✅ **RE-RUN** the checker until it passes

### 2. Understand Copilot's Limitations

GitHub Copilot:
- ✅ **DOES** read this instruction file
- ✅ **DOES** provide code suggestions based on context
- ❌ **DOES NOT** automatically execute Python scripts
- ❌ **DOES NOT** automatically run governance checks
- ❌ **DOES NOT** enforce ecosystem contracts

**You must explicitly run enforcement tools.**

### 3. Standard Workflow

```
任務請求 → 執行 ecosystem/enforce.py → 檢查通過? → 進行變更 → 再次檢查 → 提交
Task Request → Run ecosystem/enforce.py → Pass? → Make Changes → Check Again → Commit
            ↓                                ↓
       如果失敗                          如果失敗
       If Failed                        If Failed
            ↓                                ↓
       修復問題                          修復問題
       Fix Issues                       Fix Issues
```

### 4. Security Best Practices

**NEVER log sensitive data in plain text:**

```python
# ❌ BAD - Logs sensitive data
print(f"  - details: {result['details']}")  # May contain secrets

# ✅ GOOD - Use fixed safe message
print("  - security scan executed; see JSON report for non-sensitive summary.")

# ✅ GOOD - Redact sensitive fields
if key in ['secrets', 'tokens', 'passwords', 'keys', 'credentials']:
    print(f"  - {key}: [REDACTED FOR SECURITY]")
```

### 5. Common Mistakes to Avoid

- ❌ Skipping ecosystem enforcement checks
- ❌ Modifying GL semantic boundaries
- ❌ Logging sensitive information (see recent CodeQL fixes)
- ❌ Bypassing governance contracts
- ❌ Directly modifying controlplane/ directory

**Correct Approach:**
- ✅ Run `python ecosystem/enforce.py` first
- ✅ Follow GL layer architecture
- ✅ Use `[REDACTED FOR SECURITY]` for sensitive data
- ✅ Make changes in workspace/
- ✅ Re-run checks after each change

---

## 📚 Repository Overview

**MachineNativeOps** is a production-ready platform with an integrated **GL (Governance Layers) Global Governance System**. The platform combines machine-native architecture principles with advanced governance, validation, and automation capabilities.

### Key Features
- **7-layer GL governance framework** (GL00-99)
- **Instant execution engine** with second-level response times
- **AI-native infrastructure** (data, algorithms, GPU layers)
- **Comprehensive validation system** with 99.3% accuracy
- **Production-ready** with 100% GL compliance

### Tech Stack
- **Languages**: Python 3.11+, TypeScript 5.x, Node.js 18+
- **Architecture**: Modular, pipeline-based, declarative
- **Governance**: GL (Governance Layers) system with strict boundaries
- **CI/CD**: GitHub Actions with GL enforcement
- **Documentation**: Markdown, YAML, Mermaid diagrams

---

## 🏗️ GL Governance System

### Critical Constraints ⚠️

**IMPORTANT**: This project operates under **strict GL governance boundaries**. All changes must respect these constraints:

#### Immutable GL Constraints 🔒
- **GL Semantic Boundaries**: All changes must respect semantic layer boundaries (GL00-99)
- **GL Artifacts Matrix**: No modifications to governance artifact structure
- **GL Filesystem Mapping**: Directory structure follows strict FHS+GL compliance
- **GL DSL**: Domain-Specific Language remains unchanged
- **GL DAG**: Dependency graph topology is immutable
- **GL Sealing**: Governance seals prevent unauthorized modifications

#### GL Layer Hierarchy
- **GL00-09 (Strategic)**: Vision, charter, objectives
- **GL10-29 (Operational)**: Process policies, resource allocation
- **GL30-49 (Execution)**: Deployment records, project plans
- **GL50-59 (Observability)**: Quantum validation, metrics, alerts
- **GL60-80 (Feedback)**: Reconciliation mechanisms, innovation
- **GL81-83 (Extended)**: External integration
- **GL90-99 (Meta)**: Semantic root, governance standards

#### Permitted Operations ✅
- Minimal operational fixes (bug fixes, typos, documentation)
- Non-breaking enhancements within existing semantic boundaries
- Test additions that respect GL validation framework
- Documentation improvements aligned with GL artifacts

#### Prohibited Operations ⛔
- Semantic restructuring or layer redefinition
- Introduction of new governance concepts
- Modification of GL artifact relationships
- Changes to sealed governance components
- DAG topology alterations

---

## 🚀 Development Workflow

### Project Structure
```
machine-native-ops/
├── gl/                     # GL Governance System (GL00-99)
├── scripts/gl/             # GL validation scripts
├── workspace/              # Active development workspace
│   ├── src/               # Source code
│   └── docs/              # Documentation
├── controlplane/           # Governance control plane (read-only)
├── governance/             # Governance framework
└── .github/workflows/      # CI/CD workflows
```

### Build and Test Commands

#### Installation
```bash
# Install dependencies
npm install                    # Node.js dependencies
pip install -r requirements.txt  # Python dependencies (if exists)

# Initialize automation tools
make automation-init
```

#### Testing
```bash
# Run all tests
make test

# Run GL validation
python scripts/gl/validate-semantics.py
python scripts/gl/quantum-validate.py

# Run specific GL tests
python scripts/gl/implementation/test_implementation.py
python scripts/gl/validate-data-catalog.py
python scripts/gl/validate-metadata.py
```

#### Quality Checks
```bash
# Run quality checks
make automation-check

# Auto-fix issues
make automation-fix

# View quality report
cat AUTO-QUALITY-REPORT.md
```

#### Build Commands
```bash
# Build all workspaces
npm run build

# Lint code
npm run lint

# Validate GL compliance
npm run validate:gl
npm run check:gl-compliance
```

### Validation Before Committing

**Always run these commands before committing:**

1. **GL Semantic Validation**
   ```bash
   python scripts/gl/validate-semantics.py
   ```

2. **GL Quantum Validation**
   ```bash
   python scripts/gl/quantum-validate.py
   ```

3. **Run Tests**
   ```bash
   make test
   ```

4. **Check GL Compliance**
   ```bash
   npm run check:gl-compliance
   ```

---

## 📝 Code Style and Conventions

### Python Code Style

#### General Guidelines
- Follow **PEP 8** guidelines strictly
- Use **type hints** for all function signatures
- Use **f-strings** for string formatting
- Maximum line length: **100 characters**
- Use **docstrings** for all public functions/classes (Google style)
- Prefer descriptive variable names over comments

#### Import Order
```python
# 1. Standard library imports
import os
import sys
from typing import List, Dict, Optional

# 2. Third-party imports
import yaml
import requests

# 3. Local imports
from .config import settings
from .utils import helper_function
```

#### Example Code Structure
```python
"""Module docstring describing purpose."""

from typing import List, Optional


class ExampleValidator:
    """Brief class description.
    
    Attributes:
        config_path: Path to configuration file.
        strict_mode: Enable strict validation.
    """
    
    MAX_RETRIES = 3
    
    def __init__(self, config_path: str, strict_mode: bool = False) -> None:
        """Initialize the validator.
        
        Args:
            config_path: Path to the configuration file.
            strict_mode: Enable strict validation mode.
        """
        self.config_path = config_path
        self.strict_mode = strict_mode
    
    def validate(self, data: dict) -> bool:
        """Validate the provided data.
        
        Args:
            data: The data to validate.
            
        Returns:
            True if validation passes, False otherwise.
            
        Raises:
            ValueError: If data is malformed.
        """
        if not data:
            raise ValueError("Data cannot be empty")
        return True
```

### TypeScript/JavaScript Code Style

#### General Guidelines
- Use TypeScript for type safety
- Follow existing ESLint configuration (`.eslintrc.json`)
- Use `const` and `let`, avoid `var`
- Prefer arrow functions for callbacks
- Use async/await over raw promises

#### Example Code Structure
```typescript
/**
 * Brief class description.
 */
export class ExampleService {
    private readonly config: Config;
    
    constructor(config: Config) {
        this.config = config;
    }
    
    /**
     * Process data according to configuration.
     * 
     * @param data - The data to process
     * @returns Processed result
     * @throws Error if data is invalid
     */
    async processData(data: unknown): Promise<Result> {
        if (!this.isValid(data)) {
            throw new Error('Invalid data');
        }
        
        return await this.transform(data);
    }
}
```

### YAML Configuration Style
- **Indentation**: 2 spaces
- **Quoting**: Single quotes for strings
- **Comments**: Use `#` for inline documentation
- **GL Layer Tags**: Always include GL layer and purpose comments

```yaml
# GL Layer: GL30-49 Execution Layer
# Purpose: Configuration for execution pipeline
version: '1.0.0'
name: 'example-config'

settings:
  strict_mode: true
  timeout: 30
  retries: 3

validators:
  - name: 'semantic-validator'
    enabled: true
    priority: 1
```

### Markdown Documentation Style
- Use ATX-style headings (`#`, `##`, etc.)
- Use `-` for unordered lists
- Specify language for code blocks
- Use descriptive link text
- Include GL layer comments where appropriate

---

## 🎯 Common Patterns and Best Practices

### Security Patterns ✅

#### Avoid eval()
```python
# ❌ BAD - Security vulnerability
result = eval(user_input)

# ✅ GOOD - Safe alternative
import ast
result = ast.literal_eval(user_input)
```

#### Use Secure Hashing
```python
# ❌ BAD - MD5 is weak for security
import hashlib
hash = hashlib.md5(data).hexdigest()

# ✅ GOOD - SHA256 for security
import hashlib
hash = hashlib.sha256(data.encode()).hexdigest()
```

#### Input Validation
```python
# ✅ GOOD - Always validate input
def process_data(data: dict) -> Result:
    """Process validated data."""
    if not isinstance(data, dict):
        raise TypeError("Data must be a dictionary")
    
    if 'required_field' not in data:
        raise ValueError("Missing required field")
    
    # Process data...
    return result
```

### GL Governance Patterns

#### Reading Governance Manifest
```python
import yaml

# Read governance manifest
with open('governance-manifest.yaml', 'r') as f:
    manifest = yaml.safe_load(f)

# Access GL layer information
gl_layers = manifest['spec']['gl_layers']
```

#### Validating GL Compliance
```python
from scripts.gl.implementation.governance_loop import (
    create_governance_loop_executor
)

# Create executor
executor = create_governance_loop_executor()

# Execute validation cycle
input_data = {
    "tasks": [
        {"id": "T001", "type": "policy", "description": "Update policy"}
    ]
}

context = executor.execute_cycle(input_data)

# Check results
if context.loop_metrics['governance_closure_rate'] == 100:
    print("✅ Validation passed")
```

### Performance Patterns

#### Efficient Data Processing
```python
# ✅ GOOD - Use generators for large datasets
def process_large_file(filepath: str):
    """Process large file efficiently."""
    with open(filepath, 'r') as f:
        for line in f:
            yield process_line(line)

# ✅ GOOD - Use list comprehensions
results = [process(item) for item in items if is_valid(item)]

# ❌ BAD - Inefficient loop
results = []
for item in items:
    if is_valid(item):
        results.append(process(item))
```

#### Resource Management
```python
# ✅ GOOD - Use context managers
with open('file.txt', 'r') as f:
    data = f.read()

# ✅ GOOD - Clean up resources
try:
    connection = create_connection()
    result = connection.query()
finally:
    connection.close()
```

---

## 🧪 Testing Guidelines

### Test Structure
- Follow **AAA pattern**: Arrange, Act, Assert
- Use descriptive test names
- Test edge cases and error conditions
- Maintain test isolation

### Example Test
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
    assert result.overall_accuracy > 0.95
```

### GL Validation Tests
```bash
# Run all GL implementation tests
python scripts/gl/implementation/test_implementation.py

# Run specific layer validations
python scripts/gl/validate-data-catalog.py
python scripts/gl/validate-metadata.py
python scripts/gl/validate-model-registry.py
```

---

## 📖 Documentation Requirements

### Required Documentation

#### For New Functions/Classes
- **Docstring**: Google-style with description, args, returns, raises
- **Type hints**: All parameters and return types
- **Examples**: Usage examples in docstring for complex functionality

#### For New Features
- Update **readme.md** if it affects usage
- Update **CHANGELOG.md** for significant changes
- Add/update architecture docs in `docs/architecture/` if needed
- Update **governance-manifest.yaml** if it affects GL system

#### For Bug Fixes
- Reference issue number in commit message
- Document root cause if non-obvious
- Add regression test if applicable

---

## 🚨 Common Anti-Patterns to Avoid

### Code Anti-Patterns ❌

#### Hardcoded Values
```python
# ❌ BAD - Magic numbers
if count > 100:
    process()

# ✅ GOOD - Named constants
MAX_ITEMS = 100
if count > MAX_ITEMS:
    process()
```

#### Missing Error Handling
```python
# ❌ BAD - Silent failures
try:
    result = risky_operation()
except:
    pass

# ✅ GOOD - Proper error handling
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    raise
```

#### Broad Exception Catching
```python
# ❌ BAD - Too broad
try:
    process_data()
except Exception:
    pass

# ✅ GOOD - Specific exceptions
try:
    process_data()
except ValueError as e:
    handle_value_error(e)
except IOError as e:
    handle_io_error(e)
```

### GL Governance Anti-Patterns ❌

#### Violating Layer Boundaries
```python
# ❌ BAD - Strategic layer accessing execution layer directly
# GL00-09 should not directly import from GL30-49

# ✅ GOOD - Follow layer hierarchy
# Use proper governance loops and validation chains
```

#### Modifying Sealed Artifacts
```python
# ❌ BAD - Modifying sealed governance files
# Never modify files in controlplane/ or sealed GL artifacts

# ✅ GOOD - Create new artifacts or extend existing ones
# Follow proper change management process
```

---

# Code Review Instructions

When reviewing code for the machine-native-ops project, provide constructive, specific feedback based on the following criteria:

## Functionality ✅
- Verify code performs the intended functionality
- Check that edge cases are handled appropriately
- Ensure error handling is comprehensive and errors are not silently ignored
- Look for obvious bugs or logic errors
- Confirm requirements are met

## Code Quality 🎨
- Check adherence to PEP 8 guidelines for Python code
- Verify imports are properly ordered (standard → third-party → local)
- Ensure variable/function names are descriptive and follow conventions
- Assess code readability and maintainability
- Flag dead code or unnecessary commented-out code
- Check for consistent code style with rest of project

## Security 🔒
**Critical Security Checks:**
- **NO hardcoded credentials or sensitive data** - this is a critical security issue
- **NO use of eval() without proper justification** - flag any eval() usage
- **MD5 should only be used for non-security purposes** - flag if used for security
- Verify input validation is present where needed
- Check for SQL injection prevention (if using databases)
- Check for XSS prevention (if handling user input)
- Ensure sensitive data is properly handled in logging
- Verify dependencies are secure

## Performance ⚡
- Identify obvious performance bottlenecks
- Check for appropriate use of data structures
- Flag unnecessary computations or inefficient loops
- Verify efficient algorithms are used
- Check proper resource management (connections, files)

## Documentation 📚
- Verify public functions/classes have docstrings
- Check that complex logic has explanatory comments
- Ensure docstrings follow Google style guide
- Flag missing or outdated documentation

## Testing 🧪
- Check if unit tests are included for new functionality
- Verify tests cover critical paths and edge cases
- Ensure test names are descriptive
- Check if tests follow AAA pattern (Arrange, Act, Assert)
- Verify appropriate use of mocks

## Python-Specific Best Practices 🐍
- Check for type hints in function signatures
- Prefer f-strings over .format() or %
- Verify context managers are used for resources (with statements)
- Ensure exceptions are specific (not bare except)
- Check for appropriate use of list/dict comprehensions
- Verify __init__.py files are present in packages

## Project-Specific Guidelines 🏗️
- Check adherence to machine-native-ops architecture guidelines
- Verify existing utility functions are used when possible
- Ensure configuration files are updated if needed
- Consider backward compatibility
- Verify documentation follows project style

## Review Guidelines
1. **Be Constructive**: Focus on the code, not the person
2. **Explain Why**: Don't just say "change this", explain the reasoning
3. **Be Specific**: Reference exact line numbers and code snippets
4. **Prioritize**: Mark critical issues clearly (CRITICAL, HIGH, MEDIUM, LOW)
5. **Acknowledge Good Work**: Note positive aspects of the code
6. **Provide Examples**: When suggesting changes, show how to improve the code

## Common Issues to Flag 🚨

### Security (CRITICAL)
- Hardcoded passwords/keys
- SQL injection vulnerabilities
- eval() or exec() usage without justification
- Unsafe deserialization
- Insufficient input validation

### Performance (HIGH)
- N+1 query problems
- Inefficient loops
- Memory leaks
- Blocking I/O in async code

### Maintainability (MEDIUM)
- Magic numbers (suggest using constants)
- Deeply nested code
- Long functions (>50 lines)
- Duplicate code (DRY principle violations)
- Poor naming

### Testing (MEDIUM)
- Missing edge case tests
- Brittle tests
- No test isolation
- Missing assertions

## Review Approach
When reviewing code, focus on:
1. Start with a brief summary of the changes
2. Prioritize issues by severity (CRITICAL/HIGH/MEDIUM/LOW)
3. For each issue, be specific about file and line numbers
4. Explain why the issue matters and how to fix it
5. Acknowledge good practices when you see them

---

## 📚 Additional Resources

### Key Documentation Files
- **[readme.md](../readme.md)** - Project overview and quick start
- **[CONTRIBUTING.md](../CONTRIBUTING.md)** - Contribution guidelines
- **[governance-manifest.yaml](../governance-manifest.yaml)** - Central governance entry point
- **[GL-STATUS-REPORT.md](../GL-STATUS-REPORT.md)** - Overall GL system status
- **[GL-CORE-INTEGRATION-REPORT.md](../GL-CORE-INTEGRATION-REPORT.md)** - Core architecture integration

### Developer Documentation
- **[DEVELOPER_GUIDELINES.md](../docs/DEVELOPER_GUIDELINES.md)** - Detailed coding standards
- **[CI-CD-GUIDE.md](../docs/CI-CD-GUIDE.md)** - CI/CD workflow guide
- **[QUICKSTART.md](../docs/QUICKSTART.md)** - Quick start guide

### GL System Documentation
- **[GL Layer Architecture](../gl/)** - GL governance layers (GL00-99)
- **[GL Validation Scripts](../scripts/gl/)** - Validation and generation scripts
- **[GL Implementation](../scripts/gl/implementation/)** - Concrete implementations

### Agent Definitions
- **[Architect Agent](./agents/architect.agent.md)** - Architecture design agent
- **[GL Governance Agent](./agents/gl-governance.agent.md)** - GL governance specialist
- **[Security Reviewer Agent](./agents/security-reviewer.agent.md)** - Security review agent
- **[Test Specialist Agent](./agents/test-specialist.agent.md)** - Testing specialist

---

## 🎯 Quick Reference Card

### Before Making Changes
1. ✅ Read relevant documentation (README, CONTRIBUTING, GL-STATUS-REPORT)
2. ✅ Understand GL layer boundaries for affected code
3. ✅ Check existing patterns in similar code
4. ✅ Review governance manifest if touching GL system

### During Development
1. ✅ Follow code style guidelines (PEP 8 for Python, ESLint for TypeScript)
2. ✅ Add type hints and docstrings
3. ✅ Respect GL governance constraints
4. ✅ Write tests for new functionality
5. ✅ Update documentation as needed

### Before Committing
1. ✅ Run `python scripts/gl/validate-semantics.py`
2. ✅ Run `python scripts/gl/quantum-validate.py`
3. ✅ Run `make test`
4. ✅ Run `npm run check:gl-compliance`
5. ✅ Review your own changes (self-review)
6. ✅ Write descriptive commit message (Conventional Commits format)

### Commit Message Format
```
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

**Types**: `fix`, `feat`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `gl`

**Example**:
```
feat(gl): Add new quantum validation dimension

Implement the 'reversibility' dimension for quantum validation.
This improves validation accuracy by 2%.

Related to GL50-59 layer requirements.
```

---

## 🆘 Getting Help

### If You're Stuck
1. **Search existing issues**: Check if someone has already solved this problem
2. **Read documentation**: Start with readme.md and relevant docs
3. **Check governance manifest**: For GL system questions
4. **Review similar code**: Look for patterns in existing implementations
5. **Ask in PR comments**: Tag maintainers for guidance

### Common Questions

**Q: Can I modify files in the `controlplane/` directory?**  
A: No, controlplane is read-only. Make changes in `workspace/` instead.

**Q: Can I change the GL layer structure?**  
A: No, GL layer boundaries are immutable. Work within existing boundaries.

**Q: How do I add a new feature?**  
A: Follow the contribution workflow in CONTRIBUTING.md and ensure GL compliance.

**Q: What if a GL validation check fails?**  
A: Review the error message, check governance constraints, and fix the issue. Don't bypass validations.

**Q: Can I use `eval()` in Python code?**  
A: No, `eval()` is prohibited for security reasons. Use `ast.literal_eval()` or `json.loads()` instead.

---

**Last Updated**: 2026-01-27  
**Maintained by**: MachineNativeOps Team  
**Version**: 2.0.0

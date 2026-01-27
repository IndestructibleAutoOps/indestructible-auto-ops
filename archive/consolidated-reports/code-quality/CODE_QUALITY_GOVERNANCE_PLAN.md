# Code Quality Governance Plan

## Overview

This document outlines the three-phase approach to implementing code quality governance for the machine-native-ops project.

---

## Phase 1: Prevent New Issues (Immediate)

### 1.1 Set up Pre-commit Hooks

#### Install Pre-commit Framework
```bash
pip install pre-commit
pre-commit install
```

#### Create `.pre-commit-config.yaml`
```yaml
repos:
  # General hooks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: debug-statements

  # Python imports
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ["--profile", "black"]

  # Python formatting
  - repo: https://github.com/psf/black
    rev: 24.3.0
    hooks:
      - id: black
        language_version: python3.11

  # Python linting
  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: ["--max-line-length=100", "--extend-ignore=E203,W503"]

  # Security checks
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.6
    hooks:
      - id: bandit
        args: ["-r", "."]
        exclude: ^tests/
```

#### Enable Pre-commit
```bash
pre-commit install --hook-type commit-msg
```

### 1.2 Create Code Review Checklist

#### File: `.github/CODE_REVIEW_CHECKLIST.md`
```markdown
# Code Review Checklist

## Functionality
- [ ] Code performs the intended functionality
- [ ] Edge cases are handled
- [ ] Error handling is appropriate
- [ ] No obvious bugs or logic errors

## Code Quality
- [ ] Code follows PEP 8 guidelines
- [ ] Imports are properly ordered (standard → third-party → local)
- [ ] Variable/function names are descriptive
- [ ] Code is readable and maintainable

## Security
- [ ] No hardcoded credentials or sensitive data
- [ ] No use of eval() without proper justification
- [ ] MD5 is only used for non-security purposes
- [ ] Input validation is present
- [ ] SQL injection prevention (if applicable)

## Performance
- [ ] No obvious performance issues
- [ ] Appropriate use of data structures
- [ ] No unnecessary computations

## Documentation
- [ ] Public functions have docstrings
- [ ] Complex logic has comments
- [ ] README is updated if needed
- [ ] API documentation is accurate

## Testing
- [ ] Unit tests are included
- [ ] Tests cover critical paths
- [ ] Tests are passing
```

### 1.3 Update Developer Guidelines

#### File: `docs/DEVELOPER_GUIDELINES.md`
```markdown
# Developer Guidelines

## Code Quality Standards

### Python Code Style
- Follow PEP 8 guidelines
- Use isort for import ordering
- Use black for code formatting
- Maximum line length: 100 characters

### Import Order
```python
# 1. Standard library imports
import os
import sys
from typing import List, Dict, Optional

# 2. Third-party imports
import yaml
import requests
from fastapi import FastAPI

# 3. Local imports
from .config import settings
from .utils import helper_function
```

### Security Best Practices

#### Avoid eval() Usage
```python
# ❌ BAD
result = eval(user_input)

# ✅ GOOD
import ast
result = ast.literal_eval(user_input)
```

#### Use Secure Hashing
```python
# ❌ BAD (for security-sensitive applications)
import hashlib
hash = hashlib.md5(data).hexdigest()

# ✅ GOOD
import hashlib
hash = hashlib.sha256(data).hexdigest()
```

#### Avoid Hardcoded URLs
```python
# ❌ BAD
API_URL = "https://api.example.com/endpoint"

# ✅ GOOD
import os
API_URL = os.getenv("API_URL", "https://api.example.com/endpoint")
```

### Documentation Standards

#### Function Docstrings
```python
def process_data(data: str, options: Dict = None) -> Dict:
    """
    Process input data according to specified options.
    
    Args:
        data: Input string to process
        options: Optional dictionary of processing options
            - normalize: bool - Whether to normalize the data
            - validate: bool - Whether to validate the data format
            
    Returns:
        Dictionary containing:
            - success: bool - Whether processing succeeded
            - result: str - Processed data
            - errors: List[str] - Any errors encountered
            
    Raises:
        ValueError: If data format is invalid
    """
    pass
```

### Testing Guidelines

#### Unit Tests
- Write tests for all public functions
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)
- Mock external dependencies

#### Example
```python
def test_process_data_normalizes_input():
    """Test that process_data normalizes input when requested."""
    # Arrange
    input_data = "  TEST DATA  "
    options = {"normalize": True}
    
    # Act
    result = process_data(input_data, options)
    
    # Assert
    assert result["success"] is True
    assert result["result"] == "test data"
```

## Common Patterns

### Configuration Management
```python
import os
from typing import Optional

class Settings:
    """Application settings with environment variable support."""
    
    API_URL: str = os.getenv("API_URL", "http://localhost:8080")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    TIMEOUT: int = int(os.getenv("TIMEOUT", "30"))
    RETRY_COUNT: int = int(os.getenv("RETRY_COUNT", "3"))
    
    def __post_init__(self):
        """Validate settings after initialization."""
        if not self.API_URL:
            raise ValueError("API_URL is required")

settings = Settings()
```

### Error Handling
```python
import logging

logger = logging.getLogger(__name__)

def process_with_retry(func, max_retries: int = 3):
    """
    Execute function with retry logic.
    
    Args:
        func: Function to execute
        max_retries: Maximum number of retry attempts
        
    Returns:
        Function result or raises last exception
        
    Raises:
        Exception: Last exception if all retries fail
    """
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            last_exception = e
            logger.warning(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
    
    logger.error(f"All {max_retries} attempts failed")
    raise last_exception
```

### Logging Best Practices
```python
import logging
import structlog

logger = structlog.get_logger()

def process_transaction(transaction_id: str, amount: float):
    """Process a financial transaction."""
    logger.info(
        "Processing transaction",
        transaction_id=transaction_id,
        amount=amount
    )
    
    try:
        # Processing logic
        logger.info(
            "Transaction completed",
            transaction_id=transaction_id,
            status="success"
        )
    except Exception as e:
        logger.error(
            "Transaction failed",
            transaction_id=transaction_id,
            error=str(e),
            exc_info=True
        )
        raise
```

## Code Review Process

1. Self-Review
   - Run all tests locally
   - Check code style with pre-commit hooks
   - Verify documentation is complete

2. Peer Review
   - Use the code review checklist
   - Provide constructive feedback
   - Approve only when standards are met

3. CI/CD Checks
   - All tests must pass
   - Code quality checks must pass
   - Security scans must pass

## Continuous Improvement

- Regular code quality audits
- Update guidelines based on team feedback
- Share best practices in team meetings
- Review and improve checklists periodically
```

---

## Phase 2: Incremental Improvements (Optional)

### 2.1 Security Audit

#### Create Security Review Plan
```python
# tools/security_audit.py

import ast
import re
from pathlib import Path
from typing import List, Dict

class SecurityAuditor:
    """Audit code for security issues."""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.findings = []
    
    def check_md5_usage(self, file_path: Path) -> List[Dict]:
        """Check for MD5 hash usage."""
        with open(file_path, 'r') as f:
            content = f.read()
        
        if 'hashlib.md5' in content or 'md5(' in content:
            return [{
                'file': str(file_path),
                'issue': 'MD5 usage',
                'severity': 'medium',
                'recommendation': 'Replace with SHA256 for security-sensitive operations'
            }]
        return []
    
    def check_eval_usage(self, file_path: Path) -> List[Dict]:
        """Check for eval() usage."""
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Find eval() calls
        eval_pattern = r'eval\s*\('
        matches = re.finditer(eval_pattern, content)
        
        findings = []
        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            findings.append({
                'file': str(file_path),
                'line': line_num,
                'issue': 'eval() usage',
                'severity': 'high',
                'recommendation': 'Review if eval() is necessary, consider safer alternatives'
            })
        return findings
    
    def check_hardcoded_secrets(self, file_path: Path) -> List[Dict]:
        """Check for hardcoded secrets."""
        patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
        ]
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        findings = []
        for pattern in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                findings.append({
                    'file': str(file_path),
                    'line': line_num,
                    'issue': 'Potential hardcoded secret',
                    'severity': 'high',
                    'recommendation': 'Move to environment variables or secret management'
                })
        return findings
    
    def audit_project(self) -> Dict:
        """Run full security audit."""
        python_files = list(self.project_root.rglob('*.py'))
        
        for file_path in python_files:
            # Skip cache and test files
            if '__pycache__' in str(file_path) or 'tests' in str(file_path):
                continue
            
            self.findings.extend(self.check_md5_usage(file_path))
            self.findings.extend(self.check_eval_usage(file_path))
            self.findings.extend(self.check_hardcoded_secrets(file_path))
        
        return {
            'total_findings': len(self.findings),
            'findings': self.findings
        }

# Usage
if __name__ == "__main__":
    auditor = SecurityAuditor(Path.cwd())
    report = auditor.audit_project()
    
    print(f"Total findings: {report['total_findings']}")
    for finding in report['findings']:
        print(f"\n{finding['severity'].upper()}: {finding['issue']}")
        print(f"  File: {finding['file']}")
        if 'line' in finding:
            print(f"  Line: {finding['line']}")
        print(f"  Recommendation: {finding['recommendation']}")
```

### 2.2 Configuration Refactoring

#### Create Configuration Migration Guide
```markdown
# Configuration Migration Guide

## Step 1: Identify Hardcoded Values
- Search for hardcoded URLs, endpoints, and credentials
- Document their purpose and dependencies

## Step 2: Create Configuration Files
Create `.env.example`:
```bash
# API Configuration
API_URL=http://localhost:8080
API_TIMEOUT=30
API_RETRY_COUNT=3

# Database Configuration
DATABASE_URL=postgresql://user:pass@localhost/db
DATABASE_POOL_SIZE=10

# Security
SECRET_KEY=your-secret-key-here
HASH_ALGORITHM=sha256
```

## Step 3: Update Code
```python
# Before
API_URL = "http://localhost:8080"

# After
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    api_url: str = "http://localhost:8080"
    api_timeout: int = 30
    api_retry_count: int = 3
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

## Step 4: Update Documentation
- Document all configuration options
- Provide examples
- Update deployment guides
```

### 2.3 Documentation Enhancement

#### Template for Adding Docstrings
```python
"""[Brief one-line description].

[Detailed description if needed.

Args:
    arg1: Description
    arg2: Description

Returns:
    Description of return value

Raises:
    Exception: Description of when exception is raised

Examples:
    >>> function(arg1, arg2)
    expected_result
"""
```

---

## Phase 3: Automation (Future)

### 3.1 Automated Fixes for New Code

#### Create Automated PR Bot
```python
# tools/auto_fix_bot.py

import subprocess
import sys
from pathlib import Path

class AutoFixBot:
    """Automatically fix code quality issues in new PRs."""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
    
    def fix_imports(self, files: List[Path]):
        """Fix import order."""
        for file_path in files:
            subprocess.run(['isort', str(file_path)], check=True)
    
    def fix_formatting(self, files: List[Path]):
        """Fix code formatting."""
        for file_path in files:
            subprocess.run(['black', str(file_path)], check=True)
    
    def fix_style(self, files: List[Path]):
        """Fix code style issues."""
        for file_path in files:
            subprocess.run(['autopep8', '--in-place', str(file_path)], check=True)
    
    def fix_all(self, changed_files: List[Path]):
        """Apply all automated fixes."""
        print(f"Fixing {len(changed_files)} files...")
        self.fix_imports(changed_files)
        self.fix_formatting(changed_files)
        self.fix_style(changed_files)
        print("All fixes applied!")

# Integration with CI/CD
if __name__ == "__main__":
    # Get list of changed files from git
    result = subprocess.run(
        ['git', 'diff', '--name-only', 'HEAD~1', 'HEAD'],
        capture_output=True,
        text=True
    )
    
    changed_files = [
        Path(f) for f in result.stdout.split('\n')
        if f.endswith('.py')
    ]
    
    bot = AutoFixBot(Path.cwd())
    bot.fix_all(changed_files)
```

### 3.2 Gradual Refactoring Strategy

#### Priority-Based Refactoring
```python
# tools/refactoring_planner.py

from pathlib import Path
from typing import List, Dict

class RefactoringPlanner:
    """Plan and track gradual refactoring efforts."""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
    
    def prioritize_files(self, issue_report: Dict) -> List[Dict]:
        """Prioritize files based on issue impact."""
        priorities = []
        
        for issue in issue_report.get('findings', []):
            file_path = Path(issue['file'])
            
            # Calculate priority score
            score = 0
            
            # High impact files
            if 'src/' in str(file_path):
                score += 10
            if 'tests/' not in str(file_path):
                score += 5
            
            # Security issues
            if issue.get('severity') == 'high':
                score += 20
            
            # Number of issues
            score += issue.get('count', 1)
            
            priorities.append({
                'file': file_path,
                'score': score,
                'issues': [issue]
            })
        
        # Sort by priority score (descending)
        priorities.sort(key=lambda x: x['score'], reverse=True)
        
        return priorities
    
    def create_refactoring_plan(self, priorities: List[Dict]) -> Dict:
        """Create a phased refactoring plan."""
        total_files = len(priorities)
        
        return {
            'phase1': priorities[:total_files // 10],  # Top 10%
            'phase2': priorities[total_files // 10:total_files // 3],  # Next 23%
            'phase3': priorities[total_files // 3:]  # Remaining 67%
        }

# Usage
if __name__ == "__main__":
    planner = RefactoringPlanner(Path.cwd())
    priorities = planner.prioritize_files(issue_report)
    plan = planner.create_refactoring_plan(priorities)
    
    print("Refactoring Plan:")
    print(f"Phase 1 (Immediate): {len(plan['phase1'])} files")
    print(f"Phase 2 (Short-term): {len(plan['phase2'])} files")
    print(f"Phase 3 (Long-term): {len(plan['phase3'])} files")
```

### 3.3 CI/CD Integration

#### GitHub Actions Workflow
```yaml
# .github/workflows/code-quality.yml

name: Code Quality

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main, develop]

jobs:
  quality-checks:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install pre-commit
          pre-commit install
      
      - name: Run pre-commit
        run: pre-commit run --all-files
      
      - name: Run security scan
        run: |
          pip install bandit
          bandit -r . -f json -o bandit-report.json || true
      
      - name: Upload security report
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: bandit-report
          path: bandit-report.json
      
      - name: Comment PR with results
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            // Add comment with quality check results
```

---

## Implementation Timeline

### Week 1-2: Phase 1 Setup
- [ ] Install pre-commit framework
- [ ] Configure hooks
- [ ] Create code review checklist
- [ ] Write developer guidelines
- [ ] Team training

### Week 3-4: Phase 2 Execution (Optional)
- [ ] Run security audit
- [ ] Address high-priority security issues
- [ ] Refactor configuration for core modules
- [ ] Add docstrings to public APIs

### Month 2-3: Phase 3 Automation (Future)
- [ ] Set up automated fix bot
- [ ] Implement refactoring planner
- [ ] Configure CI/CD workflows
- [ ] Monitor and refine automation

---

## Success Metrics

### Phase 1 Success Criteria
- ✅ Pre-commit hooks installed and active
- ✅ 0% regression in new code quality issues
- ✅ Team adoption rate > 80%

### Phase 2 Success Criteria
- ✅ Security findings reduced by 50%
- ✅ Configuration externalization for core modules
- ✅ Documentation coverage > 90% for public APIs

### Phase 3 Success Criteria
- ✅ Automated fixes applied to all new code
- ✅ Technical debt reduced by 30%
- ✅ Quality metrics improved by 25%

---

## Conclusion

This three-phase approach ensures:
- **Immediate**: Prevent new issues from being introduced
- **Gradual**: Incrementally improve existing code
- **Sustainable**: Long-term automation and quality maintenance

The conservative approach minimizes risk while maximizing the long-term benefits of code quality governance.

---

*Document created: 2025-01-16*  
*Version: 1.0*  
*Status: Ready for Implementation*
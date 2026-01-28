# GL Unified Charter Activated
# Developer Guidelines

## Overview

This document provides guidelines for contributing to the machine-native-ops project. Following these standards ensures code quality, maintainability, and collaboration efficiency.

---

## Code Quality Standards

### Python Code Style

#### General Guidelines
- Follow **PEP 8** guidelines
- Use **isort** for import ordering
- Use **black** for code formatting
- Maximum line length: **100 characters**
- Use **type hints** for function signatures
- Use **f-strings** for string formatting (Python 3.6+)

#### Example Code Structure
```python
"""
Module docstring describing the purpose of this module.
"""

import os
import sys
from typing import List, Dict, Optional

import yaml
import requests
from fastapi import FastAPI

from .config import settings
from .utils import helper_function


class ExampleClass:
    """
    Brief description of the class.
    
    Longer description if needed.
    
    Attributes:
        attr1: Description of attribute
        attr2: Description of attribute
    """
    
    def __init__(self, param1: str, param2: Optional[int] = None):
        """Initialize the example class.
        
        Args:
            param1: Description of parameter
            param2: Optional parameter description
        """
        self.param1 = param1
        self.param2 = param2
    
    def method_name(self, data: List[str]) -> Dict[str, Any]:
        """Method description in imperative mood.
        
        Args:
            data: Description of data parameter
            
        Returns:
            Description of return value
            
        Raises:
            ValueError: If data is empty
        """
        if not data:
            raise ValueError("Data cannot be empty")
        
        # Implementation
        return {"result": "success"}


def standalone_function(x: int, y: int) -> int:
    """Brief function description.
    
    Args:
        x: First parameter
        y: Second parameter
        
    Returns:
        The sum of x and y
    """
    return x + y
```

### Import Order

Follow this order for imports:

```python
# 1. Standard library imports
import os
import sys
from datetime import datetime
from typing import List, Dict, Optional

# 2. Third-party imports
import yaml
import requests
from fastapi import FastAPI
from pydantic import BaseModel

# 3. Local imports
from .config import settings
from .utils import helper_function
from .models import DataModel
```

**Rules:**
- Separate each group with a blank line
- Sort alphabetically within each group
- Use `from module import name` for specific imports
- Avoid `from module import *`

---

## Security Best Practices

### 🔒 Avoid eval() Usage

```python
# ❌ BAD - Dangerous!
result = eval(user_input)

# ✅ GOOD - Safe
import ast
result = ast.literal_eval(user_input)

# ✅ BETTER - Use specific parsers
import json
result = json.loads(user_input)
```

### 🔒 Use Secure Hashing

```python
# ❌ BAD - MD5 is weak for security
import hashlib
hash = hashlib.md5(data).hexdigest()

# ✅ GOOD - SHA256 for security
import hashlib
hash = hashlib.sha256(data).hexdigest()

# ✅ BEST - Use secrets module for tokens
import secrets
token = secrets.token_hex(32)
```

### 🔒 Avoid Hardcoded Configuration

```python
# ❌ BAD - Hardcoded values
API_URL = "https://api.example.com/endpoint"
DATABASE_PASSWORD = "secret123"

# ✅ GOOD - Environment variables
import os
API_URL = os.getenv("API_URL", "https://api.example.com/endpoint")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

# ✅ BEST - Configuration class with validation
from pydantic import BaseSettings

class Settings(BaseSettings):
    api_url: str
    database_password: str
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### 🔒 Input Validation

```python
# ❌ BAD - No validation
def process_user_input(user_input: str):
    return eval(user_input)

# ✅ GOOD - Validate input
import re

def process_user_input(user_input: str) -> str:
    """Process user input safely."""
    # Validate input format
    if not re.match(r'^[a-zA-Z0-9_]+$', user_input):
        raise ValueError("Invalid input format")
    
    # Sanitize input
    return user_input.strip().lower()
```

### 🔒 Secure Random Generation

```python
# ❌ BAD - Not cryptographically secure
import random
token = random.randint(1, 1000000)

# ✅ GOOD - Cryptographically secure
import secrets
token = secrets.randbits(64)
```

### 🔒 SQL Injection Prevention

```python
# ❌ BAD - SQL injection vulnerability
query = f"SELECT * FROM users WHERE name = '{user_name}'"

# ✅ GOOD - Parameterized queries
import sqlite3

cursor.execute(
    "SELECT * FROM users WHERE name = ?",
    (user_name,)
)
```

### 🔒 Security Remediation Audit Trail

- For internal security tools that must use `eval()`/`exec()`, add a security header and inline warnings documenting trusted input assumptions.
- Capture remediation status in consolidated reports under `archive/consolidated-reports/` (for example, `archive/consolidated-reports/misc/REMAINING_ISSUES_ANALYSIS.md` and `archive/consolidated-reports/code-quality/EVAL_USAGE_COMPREHENSIVE_REPORT.md`).
- Prefer linking to consolidated reports instead of adding new root-level report files.

---

## Documentation Standards

### Function Docstrings

Use **Google style docstrings**:

```python
def process_data(
    data: str,
    options: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Process input data according to specified options.
    
    This function performs data processing with configurable options.
    It supports normalization, validation, and transformation.
    
    Args:
        data: Input string to process. Must be non-empty.
        options: Optional dictionary of processing options:
            - normalize (bool): Whether to normalize whitespace (default: True)
            - validate (bool): Whether to validate data format (default: True)
            - transform (str): Transformation to apply ('upper', 'lower', 'title')
            
    Returns:
        Dictionary containing processing results:
            - success (bool): Whether processing succeeded
            - result (str): Processed data
            - errors (List[str]): Any validation errors encountered
            - warnings (List[str]): Non-critical warnings
            
    Raises:
        ValueError: If data format is invalid or empty
        TypeError: If data is not a string
        
    Examples:
        >>> process_data("  HELLO  ", {"normalize": True})
        {'success': True, 'result': 'hello', 'errors': [], 'warnings': []}
        
        >>> process_data("", {})
        ValueError: Data cannot be empty
    """
    if not isinstance(data, str):
        raise TypeError("Data must be a string")
    
    if not data.strip():
        raise ValueError("Data cannot be empty")
    
    # Implementation
    return {"success": True, "result": data, "errors": [], "warnings": []}
```

### Class Docstrings

```python
class DataProcessor:
    """
    Handles data processing operations with configurable strategies.
    
    This class provides a flexible framework for processing various
    types of data with pluggable transformation strategies.
    
    Attributes:
        config: Configuration dictionary for processing
        validators: List of validation functions to apply
        transformers: List of transformation functions to apply
        
    Example:
        >>> processor = DataProcessor({"normalize": True})
        >>> result = processor.process("  TEST DATA  ")
        >>> print(result.result)
        'test data'
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the data processor.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.validators = []
        self.transformers = []
```

### Module Docstrings

```python
"""
Data Processing Module.

This module provides utilities for data processing, validation,
and transformation with support for pluggable strategies.

Key Components:
    - DataProcessor: Main class for data processing
    - ValidationStrategy: Interface for validation strategies
    - TransformationStrategy: Interface for transformation strategies

Usage:
    >>> from data_processing import DataProcessor
    >>> processor = DataProcessor(config)
    >>> result = processor.process(data)
"""

import os
from typing import Any, Dict, List, Optional
```

---

## Testing Guidelines

### Unit Tests

#### Structure
```python
import pytest
from unittest.mock import Mock, patch
from mymodule import DataProcessor


class TestDataProcessor:
    """Test suite for DataProcessor class."""
    
    @pytest.fixture
    def processor(self):
        """Fixture providing a DataProcessor instance."""
        return DataProcessor({"normalize": True})
    
    @pytest.fixture
    def sample_data(self):
        """Fixture providing sample test data."""
        return {
            "input": "  TEST DATA  ",
            "expected": "test data"
        }
    
    def test_process_normalizes_data(self, processor, sample_data):
        """Test that process normalizes input data.
        
        This test verifies that the processor correctly
        normalizes whitespace in input data.
        
        Given:
            A processor with normalization enabled
        When:
            Processing data with extra whitespace
        Then:
            The result should have normalized whitespace
        """
        # Arrange
        input_data = sample_data["input"]
        expected = sample_data["expected"]
        
        # Act
        result = processor.process(input_data)
        
        # Assert
        assert result.success is True
        assert result.result == expected
    
    def test_process_empty_data_raises_error(self, processor):
        """Test that processing empty data raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            processor.process("")
    
    @patch('mymodule.external_service')
    def test_process_with_external_service(self, mock_service, processor):
        """Test processing with mocked external service."""
        # Arrange
        mock_service.call.return_value = "mocked result"
        
        # Act
        result = processor.process_with_service("data")
        
        # Assert
        assert result.result == "mocked result"
        mock_service.call.assert_called_once_with("data")
```

#### Best Practices

1. **Descriptive Test Names**: Use `test_<function>_<scenario>` format
2. **AAA Pattern**: Arrange, Act, Assert structure
3. **One Assertion Per Test**: Keep tests focused
4. **Use Fixtures**: For common setup code
5. **Mock External Dependencies**: Isolate unit under test
6. **Test Edge Cases**: Empty inputs, None, boundaries
7. **Test Error Cases**: Verify proper error handling

### Integration Tests

```python
import pytest
from fastapi.testclient import TestClient
from myapp import app


class TestAPIEndpoints:
    """Integration tests for API endpoints."""
    
    @pytest.fixture
    def client(self):
        """Provide test client."""
        return TestClient(app)
    
    def test_create_resource(self, client):
        """Test resource creation endpoint."""
        response = client.post(
            "/api/resources",
            json={"name": "test", "value": 123}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "test"
        assert "id" in data
    
    def test_get_resource_not_found(self, client):
        """Test getting non-existent resource."""
        response = client.get("/api/resources/999")
        
        assert response.status_code == 404
```

---

## Common Patterns

### Configuration Management

```python
import os
from typing import Optional
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    """Application settings with validation."""
    
    # API Configuration
    api_url: str
    api_timeout: int = 30
    api_retry_count: int = 3
    
    # Database Configuration
    database_url: str
    database_pool_size: int = 10
    
    # Security
    secret_key: str
    hash_algorithm: str = "sha256"
    
    # Feature Flags
    debug_mode: bool = False
    enable_metrics: bool = True
    
    @validator('api_timeout', 'database_pool_size')
    def validate_positive(cls, v):
        """Validate that values are positive."""
        if v <= 0:
            raise ValueError('Value must be positive')
        return v
    
    @validator('secret_key')
    def validate_secret_key(cls, v):
        """Validate secret key length."""
        if len(v) < 32:
            raise ValueError('Secret key must be at least 32 characters')
        return v
    
    class Config:
        """Configuration loader settings."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Create global settings instance
settings = Settings()
```

### Error Handling

```python
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class ProcessingError(Exception):
    """Custom exception for processing errors."""
    pass


def process_with_retry(
    func,
    max_retries: int = 3,
    backoff_factor: float = 2.0
) -> Any:
    """
    Execute function with exponential backoff retry logic.
    
    Args:
        func: Function to execute
        max_retries: Maximum number of retry attempts
        backoff_factor: Multiplier for backoff delay
        
    Returns:
        Function result
        
    Raises:
        ProcessingError: If all retries fail
    """
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            last_exception = e
            logger.warning(
                f"Attempt {attempt + 1}/{max_retries} failed: {e}"
            )
            
            if attempt < max_retries - 1:
                # Calculate backoff delay
                delay = backoff_factor ** attempt
                logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
    
    logger.error(f"All {max_retries} attempts failed")
    raise ProcessingError(f"Operation failed after {max_retries} attempts") from last_exception


def safe_operation(data: str) -> Optional[str]:
    """Safely perform operation with comprehensive error handling.
    
    Args:
        data: Input data
        
    Returns:
        Processed result or None if error occurs
    """
    try:
        # Validate input
        if not data or not isinstance(data, str):
            logger.warning("Invalid input: data must be non-empty string")
            return None
        
        # Process data
        result = process_data(data)
        
        return result
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return None
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return None
```

### Logging Best Practices

```python
import logging
import structlog

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)


class TransactionProcessor:
    """Process transactions with comprehensive logging."""
    
    def process_transaction(
        self,
        transaction_id: str,
        amount: float,
        user_id: str
    ) -> bool:
        """
        Process a financial transaction.
        
        Args:
            transaction_id: Unique transaction identifier
            amount: Transaction amount
            user_id: User identifier
            
        Returns:
            True if successful, False otherwise
        """
        logger.info(
            "Processing transaction",
            transaction_id=transaction_id,
            amount=amount,
            user_id=user_id
        )
        
        try:
            # Validate transaction
            if amount <= 0:
                logger.warning(
                    "Invalid transaction amount",
                    transaction_id=transaction_id,
                    amount=amount
                )
                return False
            
            # Process transaction
            result = self._execute_transaction(transaction_id, amount, user_id)
            
            if result:
                logger.info(
                    "Transaction completed successfully",
                    transaction_id=transaction_id,
                    user_id=user_id,
                    final_balance=self._get_balance(user_id)
                )
                return True
            else:
                logger.error(
                    "Transaction processing failed",
                    transaction_id=transaction_id,
                    user_id=user_id
                )
                return False
                
        except Exception as e:
            logger.error(
                "Transaction error",
                transaction_id=transaction_id,
                error=str(e),
                exc_info=True
            )
            return False
```

### Context Managers

```python
from contextlib import contextmanager
import tempfile
from typing import Generator


@contextmanager
def temp_file(content: str) -> Generator[str, None, None]:
    """
    Context manager for temporary file handling.
    
    Args:
        content: Content to write to the file
        
    Yields:
        Path to the temporary file
    """
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        temp_path = f.name
        f.write(content)
    
    try:
        yield temp_path
    finally:
        # Clean up
        try:
            os.unlink(temp_path)
        except OSError:
            pass


# Usage
def process_with_temp_file():
    """Example of using the context manager."""
    with temp_file("test content") as temp_path:
        # Work with the file
        with open(temp_path, 'r') as f:
            data = f.read()
            process(data)
    # File is automatically cleaned up
```

---

## Code Review Process

### 1. Self-Review Checklist
Before submitting your code for review:
- [ ] Run all tests locally (`pytest`)
- [ ] Check code style with pre-commit hooks (`pre-commit run --all-files`)
- [ ] Verify documentation is complete
- [ ] Ensure all TODO comments are addressed or documented
- [ ] Check for debug print statements
- [ ] Verify no sensitive data is committed
- [ ] Update CHANGELOG if needed

### 2. Peer Review
When reviewing others' code:
- Use the [Code Review Checklist](../.github/CODE_REVIEW_CHECKLIST.md)
- Provide constructive, specific feedback
- Suggest improvements when possible
- Acknowledge good work
- Ask questions if something is unclear

### 3. CI/CD Checks
All automated checks must pass:
- Unit tests
- Integration tests
- Code quality checks (pre-commit)
- Security scans
- Type checking

---

## Continuous Improvement

### Regular Activities
- **Code Quality Audits**: Monthly review of code quality metrics
- **Guideline Updates**: Quarterly review and updates
- **Team Training**: Monthly best practices sharing
- **Tool Updates**: Keep development tools up to date

### Feedback Loop
- Collect feedback on guidelines
- Identify pain points
- Improve documentation
- Share success stories

---

## Additional Resources

### External References
- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [pytest Documentation](https://docs.pytest.org/)

### Internal Resources
- [Code Review Checklist](../.github/CODE_REVIEW_CHECKLIST.md)
- [Governance Plan](../CODE_QUALITY_GOVERNANCE_PLAN.md)
- [Project README](../README.md)

---

## Questions?

If you have questions about these guidelines:
1. Check existing code for examples
2. Consult the team lead
3. Propose improvements via pull requests

---

*Last updated: 2025-01-16*  
*Version: 1.0*  
*Maintained by: MachineNativeOps Team*

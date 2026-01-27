# Pull Request #1 程式碼改進範例

本文件提供具體的程式碼範例，展示如何修正 PR #1 審查中發現的問題。

---

## 1. 型別提示改進範例

### Python 型別提示

#### 範例 1: 非同步函式型別提示

**❌ 改進前**:
```python
async def generate_code(context):
    """Generate code based on context."""
    result = await process(context)
    return result
```

**✅ 改進後**:
```python
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class CodeGenerationResult:
    """Result of code generation."""
    code: str
    language: str
    metadata: Dict[str, Any]
    error: Optional[str] = None

async def generate_code(
    context: Dict[str, Any]
) -> CodeGenerationResult:
    """Generate code based on context.
    
    Args:
        context: Dictionary containing generation parameters.
            - prompt (str): The code generation prompt
            - language (str): Target programming language
            - options (Dict[str, Any]): Additional options
    
    Returns:
        CodeGenerationResult containing the generated code and metadata.
        
    Raises:
        ValueError: If required context parameters are missing.
        GenerationError: If code generation fails.
    
    Example:
        >>> context = {
        ...     "prompt": "Create a function to calculate fibonacci",
        ...     "language": "python",
        ...     "options": {"max_lines": 50}
        ... }
        >>> result = await generate_code(context)
        >>> print(result.code)
    """
    if not context.get("prompt"):
        raise ValueError("Context must contain 'prompt' key")
    
    result = await process(context)
    return CodeGenerationResult(
        code=result["code"],
        language=context["language"],
        metadata=result.get("metadata", {}),
    )
```

#### 範例 2: Registry Manager 型別提示

**❌ 改進前**:
```python
class RegistryManager:
    def __init__(self, config_path):
        self.config = self._load_config(config_path)
        self.cache = {}
    
    def get_namespace(self, namespace_id):
        if namespace_id in self.cache:
            return self.cache[namespace_id]
        return self._fetch_from_registry(namespace_id)
    
    def add_namespace(self, namespace_data):
        validated = self._validate(namespace_data)
        self._save_to_registry(validated)
        return validated["id"]
```

**✅ 改進後**:
```python
from typing import Dict, Any, Optional, TypedDict
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class NamespaceData(TypedDict):
    """Namespace data structure."""
    id: str
    name: str
    version: str
    metadata: Dict[str, Any]

class RegistryConfig(TypedDict):
    """Registry configuration structure."""
    registry_path: str
    cache_ttl: int
    validation_strict: bool

class RegistryManager:
    """Manager for namespace registry operations.
    
    This class handles CRUD operations for namespaces, including
    validation, caching, and persistence to the registry.
    
    Attributes:
        config: Registry configuration.
        cache: In-memory cache of namespace data.
    
    Example:
        >>> manager = RegistryManager(Path("config/registry.yaml"))
        >>> namespace_id = manager.add_namespace({
        ...     "name": "my-namespace",
        ...     "version": "1.0.0",
        ...     "metadata": {}
        ... })
    """
    
    def __init__(self, config_path: Path) -> None:
        """Initialize the registry manager.
        
        Args:
            config_path: Path to the registry configuration file.
            
        Raises:
            FileNotFoundError: If config file doesn't exist.
            ValueError: If config is invalid.
        """
        self.config: RegistryConfig = self._load_config(config_path)
        self.cache: Dict[str, NamespaceData] = {}
        logger.info(f"Initialized RegistryManager with config: {config_path}")
    
    def get_namespace(self, namespace_id: str) -> Optional[NamespaceData]:
        """Retrieve a namespace by ID.
        
        Args:
            namespace_id: The unique identifier of the namespace.
            
        Returns:
            NamespaceData if found, None otherwise.
            
        Example:
            >>> namespace = manager.get_namespace("my-namespace")
            >>> if namespace:
            ...     print(namespace["name"])
        """
        if namespace_id in self.cache:
            logger.debug(f"Cache hit for namespace: {namespace_id}")
            return self.cache[namespace_id]
        
        logger.debug(f"Cache miss for namespace: {namespace_id}, fetching from registry")
        return self._fetch_from_registry(namespace_id)
    
    def add_namespace(self, namespace_data: Dict[str, Any]) -> str:
        """Add a new namespace to the registry.
        
        Args:
            namespace_data: Dictionary containing namespace information.
                Must include 'name' and 'version' keys.
            
        Returns:
            The ID of the newly created namespace.
            
        Raises:
            ValidationError: If namespace_data is invalid.
            DuplicateError: If namespace already exists.
            
        Example:
            >>> namespace_id = manager.add_namespace({
            ...     "name": "test-namespace",
            ...     "version": "1.0.0",
            ...     "metadata": {"owner": "team-a"}
            ... })
        """
        validated: NamespaceData = self._validate(namespace_data)
        self._save_to_registry(validated)
        
        # Update cache
        self.cache[validated["id"]] = validated
        
        logger.info(f"Added namespace: {validated['id']}")
        return validated["id"]
    
    def _load_config(self, config_path: Path) -> RegistryConfig:
        """Load configuration from file."""
        # Implementation
        ...
    
    def _validate(self, data: Dict[str, Any]) -> NamespaceData:
        """Validate namespace data."""
        # Implementation
        ...
    
    def _fetch_from_registry(self, namespace_id: str) -> Optional[NamespaceData]:
        """Fetch namespace from registry."""
        # Implementation
        ...
    
    def _save_to_registry(self, namespace: NamespaceData) -> None:
        """Save namespace to registry."""
        # Implementation
        ...
```

---

## 2. 安全性改進範例

### 移除硬編碼秘密

#### 範例 1: API 金鑰管理

**❌ 改進前**:
```python
# config/integrations/jira-integration.py
class JiraIntegration:
    def __init__(self):
        self.api_key = "JIRA-API-KEY-1234567890"  # 硬編碼!
        self.base_url = "https://company.atlassian.net"
        self.username = "admin@company.com"
```

**✅ 改進後**:
```python
# config/integrations/jira-integration.py
import os
from typing import Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class JiraConfig:
    """Jira integration configuration."""
    api_key: str
    base_url: str
    username: str
    
    @classmethod
    def from_env(cls) -> "JiraConfig":
        """Load configuration from environment variables.
        
        Returns:
            JiraConfig instance with loaded values.
            
        Raises:
            ValueError: If required environment variables are missing.
        """
        api_key = os.environ.get("JIRA_API_KEY")
        base_url = os.environ.get("JIRA_BASE_URL")
        username = os.environ.get("JIRA_USERNAME")
        
        missing = []
        if not api_key:
            missing.append("JIRA_API_KEY")
        if not base_url:
            missing.append("JIRA_BASE_URL")
        if not username:
            missing.append("JIRA_USERNAME")
        
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}"
            )
        
        return cls(
            api_key=api_key,
            base_url=base_url,
            username=username,
        )

class JiraIntegration:
    """Integration with Jira API."""
    
    def __init__(self, config: Optional[JiraConfig] = None) -> None:
        """Initialize Jira integration.
        
        Args:
            config: Jira configuration. If None, loads from environment.
        """
        self.config = config or JiraConfig.from_env()
        logger.info(f"Initialized Jira integration for {self.config.base_url}")
    
    def create_issue(self, project_key: str, summary: str, description: str) -> str:
        """Create a new Jira issue."""
        # Implementation using self.config.api_key
        ...
```

**配置 .env 檔案** (不要提交到 Git):
```bash
# .env
JIRA_API_KEY=your-actual-api-key-here
JIRA_BASE_URL=https://company.atlassian.net
JIRA_USERNAME=admin@company.com
```

**更新 .gitignore**:
```
# .gitignore
.env
.env.local
.env.*.local
```

#### 範例 2: 資料庫連線安全

**❌ 改進前**:
```python
# database/connection.py
import psycopg2

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="production_db",
        user="admin",
        password="SuperSecret123!"  # 硬編碼密碼!
    )
```

**✅ 改進後**:
```python
# database/connection.py
import os
from typing import Optional
from contextlib import contextmanager
import psycopg2
from psycopg2.extensions import connection
import logging

logger = logging.getLogger(__name__)

class DatabaseConfig:
    """Database configuration from environment."""
    
    def __init__(self) -> None:
        """Initialize database configuration from environment variables."""
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = int(os.getenv("DB_PORT", "5432"))
        self.database = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        
        self._validate()
    
    def _validate(self) -> None:
        """Validate that required configuration is present."""
        required = {
            "DB_NAME": self.database,
            "DB_USER": self.user,
            "DB_PASSWORD": self.password,
        }
        
        missing = [key for key, value in required.items() if not value]
        if missing:
            raise ValueError(
                f"Missing required database environment variables: {', '.join(missing)}"
            )
    
    def get_connection_string(self) -> str:
        """Get database connection string (password masked in logs)."""
        return (
            f"postgresql://{self.user}:***@{self.host}:{self.port}/{self.database}"
        )

@contextmanager
def get_db_connection(config: Optional[DatabaseConfig] = None):
    """Get a database connection with automatic cleanup.
    
    Args:
        config: Database configuration. If None, loads from environment.
        
    Yields:
        Database connection object.
        
    Example:
        >>> with get_db_connection() as conn:
        ...     cursor = conn.cursor()
        ...     cursor.execute("SELECT * FROM users")
    """
    cfg = config or DatabaseConfig()
    conn: Optional[connection] = None
    
    try:
        logger.debug(f"Connecting to database: {cfg.get_connection_string()}")
        conn = psycopg2.connect(
            host=cfg.host,
            port=cfg.port,
            database=cfg.database,
            user=cfg.user,
            password=cfg.password,
        )
        yield conn
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        if conn:
            conn.close()
            logger.debug("Database connection closed")
```

---

## 3. 日誌系統改進範例

### 結構化日誌

#### 範例 1: TypeScript Winston Logger

**❌ 改進前**:
```typescript
// src/services/namespace-service.ts
export class NamespaceService {
  async createNamespace(data: NamespaceData): Promise<string> {
    console.log("Creating namespace:", data.name);
    
    try {
      const id = await this.repo.save(data);
      console.log("Namespace created successfully:", id);
      return id;
    } catch (error) {
      console.error("Failed to create namespace:", error);
      throw error;
    }
  }
}
```

**✅ 改進後**:
```typescript
// src/utils/logger.ts
import winston from 'winston';

const logFormat = winston.format.combine(
  winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
  winston.format.errors({ stack: true }),
  winston.format.json()
);

const consoleFormat = winston.format.combine(
  winston.format.colorize(),
  winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
  winston.format.printf(({ timestamp, level, message, ...metadata }) => {
    let msg = `${timestamp} [${level}] ${message}`;
    if (Object.keys(metadata).length > 0) {
      msg += ` ${JSON.stringify(metadata)}`;
    }
    return msg;
  })
);

export const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: logFormat,
  defaultMeta: { service: 'machine-native-ops' },
  transports: [
    // Write all logs to combined.log
    new winston.transports.File({ 
      filename: 'logs/combined.log',
      maxsize: 10485760, // 10MB
      maxFiles: 5,
    }),
    // Write errors to error.log
    new winston.transports.File({ 
      filename: 'logs/error.log', 
      level: 'error',
      maxsize: 10485760,
      maxFiles: 5,
    })
  ]
});

// Add console transport in development
if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: consoleFormat
  }));
}

// Export helper functions for common operations
export const logError = (
  message: string, 
  error: Error, 
  metadata?: Record<string, unknown>
) => {
  logger.error(message, {
    error: error.message,
    stack: error.stack,
    ...metadata
  });
};

export const logInfo = (
  message: string, 
  metadata?: Record<string, unknown>
) => {
  logger.info(message, metadata);
};

export const logDebug = (
  message: string, 
  metadata?: Record<string, unknown>
) => {
  logger.debug(message, metadata);
};
```

```typescript
// src/services/namespace-service.ts
import { logger, logError, logInfo } from '../utils/logger';

export class NamespaceService {
  async createNamespace(data: NamespaceData): Promise<string> {
    logInfo('Creating namespace', {
      namespaceName: data.name,
      version: data.version,
      owner: data.metadata?.owner
    });
    
    try {
      const id = await this.repo.save(data);
      
      logInfo('Namespace created successfully', {
        namespaceId: id,
        namespaceName: data.name,
        duration: performance.now() // or use actual timing
      });
      
      return id;
    } catch (error) {
      logError('Failed to create namespace', error as Error, {
        namespaceName: data.name,
        attemptedData: data
      });
      throw error;
    }
  }
}
```

#### 範例 2: Python Structured Logging

**❌ 改進前**:
```python
# src/services/registry_service.py
class RegistryService:
    def register_namespace(self, namespace_data):
        print(f"Registering namespace: {namespace_data['name']}")
        
        try:
            result = self._validate_and_save(namespace_data)
            print(f"Registration successful: {result['id']}")
            return result
        except Exception as e:
            print(f"Registration failed: {e}")
            raise
```

**✅ 改進後**:
```python
# src/utils/logging_config.py
import logging
import json
from typing import Dict, Any
from datetime import datetime
import sys

class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields
        if hasattr(record, "extra_data"):
            log_data["data"] = record.extra_data
        
        return json.dumps(log_data)

def setup_logging(
    level: str = "INFO",
    log_file: str = "logs/app.log"
) -> None:
    """Setup application logging configuration.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_file: Path to log file.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Console handler (formatted for humans)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_format)
    
    # File handler (JSON formatted)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    file_handler.setFormatter(JSONFormatter())
    
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

class LoggerAdapter(logging.LoggerAdapter):
    """Logger adapter for adding context to logs."""
    
    def process(self, msg: str, kwargs: Dict[str, Any]) -> tuple:
        """Add extra context to log record."""
        extra = kwargs.get("extra", {})
        if self.extra:
            extra.update(self.extra)
        kwargs["extra"] = {"extra_data": extra}
        return msg, kwargs

# Helper function to get logger with context
def get_logger(name: str, **context) -> LoggerAdapter:
    """Get a logger with context.
    
    Args:
        name: Logger name (usually __name__).
        **context: Additional context to add to all log messages.
        
    Returns:
        LoggerAdapter with context.
    """
    logger = logging.getLogger(name)
    return LoggerAdapter(logger, context)
```

```python
# src/services/registry_service.py
from typing import Dict, Any
from src.utils.logging_config import get_logger

logger = get_logger(__name__, service="registry")

class RegistryService:
    """Service for namespace registration."""
    
    def register_namespace(self, namespace_data: Dict[str, Any]) -> Dict[str, Any]:
        """Register a new namespace.
        
        Args:
            namespace_data: Namespace information to register.
            
        Returns:
            Registration result with namespace ID.
            
        Raises:
            ValidationError: If namespace data is invalid.
            RegistrationError: If registration fails.
        """
        logger.info(
            "Registering namespace",
            extra={
                "namespace_name": namespace_data.get("name"),
                "version": namespace_data.get("version"),
            }
        )
        
        try:
            result = self._validate_and_save(namespace_data)
            
            logger.info(
                "Registration successful",
                extra={
                    "namespace_id": result["id"],
                    "namespace_name": namespace_data["name"],
                }
            )
            
            return result
            
        except Exception as e:
            logger.error(
                "Registration failed",
                extra={
                    "namespace_name": namespace_data.get("name"),
                    "error_type": type(e).__name__,
                },
                exc_info=True
            )
            raise
```

---

## 4. Docstring 統一範例

### Google Style Docstrings

**❌ 改進前**:
```python
def process_namespace(namespace_id, config):
    # Process the namespace
    result = validate(namespace_id)
    return apply_config(result, config)
```

**✅ 改進後**:
```python
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class ProcessResult:
    """Result of namespace processing.
    
    Attributes:
        namespace_id: The namespace identifier.
        status: Processing status (success, failed, pending).
        data: Processed namespace data.
        errors: List of errors if any occurred.
    """
    namespace_id: str
    status: str
    data: Dict[str, Any]
    errors: List[str]

def process_namespace(
    namespace_id: str, 
    config: Dict[str, Any]
) -> ProcessResult:
    """Process a namespace with the given configuration.
    
    This function validates the namespace and applies the provided
    configuration settings. It performs the following steps:
    1. Validate the namespace ID format
    2. Check namespace exists in registry
    3. Apply configuration transformations
    4. Persist changes
    
    Args:
        namespace_id: The unique identifier for the namespace.
            Must be in format 'ns-{uuid}'.
        config: Configuration dictionary containing processing parameters.
            Required keys:
                - mode (str): Processing mode ('strict' or 'lenient')
                - options (Dict[str, Any]): Additional options
            Optional keys:
                - timeout (int): Timeout in seconds (default: 30)
        
    Returns:
        ProcessResult object containing the processing status and data.
        The 'data' field contains the transformed namespace configuration.
        
    Raises:
        ValueError: If the namespace_id format is invalid.
        NamespaceNotFoundError: If the namespace doesn't exist.
        ConfigError: If the configuration is malformed.
        ProcessingError: If processing fails for any other reason.
    
    Example:
        >>> config = {
        ...     "mode": "strict",
        ...     "options": {"validate_schema": True},
        ...     "timeout": 60
        ... }
        >>> result = process_namespace("ns-123e4567-e89b", config)
        >>> if result.status == "success":
        ...     print(f"Processed namespace: {result.namespace_id}")
        
    Note:
        This function requires the namespace to be in an unlocked state.
        Locked namespaces will raise a NamespaceLockedError.
        
    See Also:
        validate_namespace: For standalone validation
        apply_namespace_config: For applying config without validation
    """
    result = validate(namespace_id)
    processed_data = apply_config(result, config)
    
    return ProcessResult(
        namespace_id=namespace_id,
        status="success",
        data=processed_data,
        errors=[]
    )
```

---

## 5. eval() 安全替代方案

### 使用 AST 和受限執行

**❌ 不安全的做法**:
```python
def execute_policy(policy_code: str, context: dict) -> bool:
    """Execute a policy rule."""
    # 危險! 可以執行任意程式碼
    return eval(policy_code, {"context": context})
```

**✅ 安全的做法**:
```python
import ast
from typing import Any, Dict, Set
import operator
from dataclasses import dataclass

# 定義允許的操作符
ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
    ast.And: operator.and_,
    ast.Or: operator.or_,
    ast.Not: operator.not_,
}

@dataclass
class PolicyEvaluationError(Exception):
    """Raised when policy evaluation fails."""
    message: str
    policy_code: str

class SafePolicyEvaluator:
    """Safe evaluator for policy expressions.
    
    This evaluator uses AST parsing to safely evaluate policy expressions
    without using eval() or exec(). Only specific operations are allowed.
    """
    
    def __init__(self, allowed_names: Set[str]) -> None:
        """Initialize the evaluator.
        
        Args:
            allowed_names: Set of allowed variable names in expressions.
        """
        self.allowed_names = allowed_names
    
    def evaluate(self, expression: str, context: Dict[str, Any]) -> Any:
        """Safely evaluate a policy expression.
        
        Args:
            expression: The expression to evaluate (e.g., "age > 18").
            context: Dictionary of variables available in the expression.
            
        Returns:
            The result of the expression evaluation.
            
        Raises:
            PolicyEvaluationError: If the expression is invalid or unsafe.
            
        Example:
            >>> evaluator = SafePolicyEvaluator({"age", "country"})
            >>> context = {"age": 25, "country": "US"}
            >>> result = evaluator.evaluate("age > 18 and country == 'US'", context)
            >>> print(result)  # True
        """
        try:
            tree = ast.parse(expression, mode='eval')
            return self._eval_node(tree.body, context)
        except Exception as e:
            raise PolicyEvaluationError(
                message=f"Failed to evaluate policy: {e}",
                policy_code=expression
            )
    
    def _eval_node(self, node: ast.AST, context: Dict[str, Any]) -> Any:
        """Recursively evaluate an AST node."""
        if isinstance(node, ast.Constant):
            # Python 3.8+ - literal values
            return node.value
        
        elif isinstance(node, ast.Name):
            # Variable reference
            if node.id not in self.allowed_names:
                raise ValueError(f"Variable '{node.id}' is not allowed")
            return context.get(node.id)
        
        elif isinstance(node, ast.BinOp):
            # Binary operation (e.g., a + b)
            op_type = type(node.op)
            if op_type not in ALLOWED_OPERATORS:
                raise ValueError(f"Operator {op_type} is not allowed")
            
            left = self._eval_node(node.left, context)
            right = self._eval_node(node.right, context)
            return ALLOWED_OPERATORS[op_type](left, right)
        
        elif isinstance(node, ast.Compare):
            # Comparison (e.g., a > b)
            left = self._eval_node(node.left, context)
            
            for op, comparator in zip(node.ops, node.comparators):
                op_type = type(op)
                if op_type not in ALLOWED_OPERATORS:
                    raise ValueError(f"Operator {op_type} is not allowed")
                
                right = self._eval_node(comparator, context)
                if not ALLOWED_OPERATORS[op_type](left, right):
                    return False
                left = right
            return True
        
        elif isinstance(node, ast.BoolOp):
            # Boolean operation (and, or)
            op_type = type(node.op)
            if op_type not in ALLOWED_OPERATORS:
                raise ValueError(f"Operator {op_type} is not allowed")
            
            values = [self._eval_node(v, context) for v in node.values]
            
            if isinstance(node.op, ast.And):
                return all(values)
            elif isinstance(node.op, ast.Or):
                return any(values)
        
        elif isinstance(node, ast.UnaryOp):
            # Unary operation (e.g., not)
            op_type = type(node.op)
            if op_type not in ALLOWED_OPERATORS:
                raise ValueError(f"Operator {op_type} is not allowed")
            
            operand = self._eval_node(node.operand, context)
            return ALLOWED_OPERATORS[op_type](operand)
        
        else:
            raise ValueError(f"Node type {type(node)} is not allowed")

# 使用範例
def execute_policy(policy_code: str, context: Dict[str, Any]) -> bool:
    """Execute a policy rule safely.
    
    Args:
        policy_code: The policy expression to evaluate.
        context: Dictionary of variables for the policy.
        
    Returns:
        Boolean result of policy evaluation.
        
    Example:
        >>> policy = "user.age >= 18 and user.verified == True"
        >>> context = {"user": {"age": 25, "verified": True}}
        >>> result = execute_policy(policy, context)
    """
    # 定義允許的變數名
    allowed_names = {"user", "resource", "action", "context"}
    
    evaluator = SafePolicyEvaluator(allowed_names)
    return bool(evaluator.evaluate(policy_code, context))
```

---

## 6. 測試範例

### Pytest 測試範例

```python
# tests/test_registry_service.py
import pytest
from unittest.mock import Mock, patch
from typing import Dict, Any

from src.services.registry_service import RegistryService
from src.exceptions import ValidationError, NamespaceNotFoundError

@pytest.fixture
def registry_service() -> RegistryService:
    """Create a RegistryService instance for testing."""
    return RegistryService()

@pytest.fixture
def valid_namespace_data() -> Dict[str, Any]:
    """Create valid namespace data for testing."""
    return {
        "name": "test-namespace",
        "version": "1.0.0",
        "metadata": {
            "owner": "test-team",
            "description": "Test namespace"
        }
    }

class TestRegistryService:
    """Tests for RegistryService."""
    
    def test_register_namespace_success(
        self, 
        registry_service: RegistryService,
        valid_namespace_data: Dict[str, Any]
    ) -> None:
        """Test successful namespace registration."""
        # Act
        result = registry_service.register_namespace(valid_namespace_data)
        
        # Assert
        assert result["id"] is not None
        assert result["name"] == valid_namespace_data["name"]
        assert result["version"] == valid_namespace_data["version"]
    
    def test_register_namespace_invalid_data(
        self, 
        registry_service: RegistryService
    ) -> None:
        """Test registration with invalid data raises ValidationError."""
        # Arrange
        invalid_data = {"name": ""}  # Missing required fields
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            registry_service.register_namespace(invalid_data)
        
        assert "name" in str(exc_info.value)
    
    @patch('src.services.registry_service.logger')
    def test_register_namespace_logs_info(
        self,
        mock_logger: Mock,
        registry_service: RegistryService,
        valid_namespace_data: Dict[str, Any]
    ) -> None:
        """Test that registration logs appropriate info messages."""
        # Act
        registry_service.register_namespace(valid_namespace_data)
        
        # Assert
        assert mock_logger.info.call_count == 2  # Start and success messages
        first_call_args = mock_logger.info.call_args_list[0]
        assert "Registering namespace" in first_call_args[0][0]
    
    def test_get_namespace_found(
        self,
        registry_service: RegistryService,
        valid_namespace_data: Dict[str, Any]
    ) -> None:
        """Test retrieving an existing namespace."""
        # Arrange
        result = registry_service.register_namespace(valid_namespace_data)
        namespace_id = result["id"]
        
        # Act
        namespace = registry_service.get_namespace(namespace_id)
        
        # Assert
        assert namespace is not None
        assert namespace["id"] == namespace_id
        assert namespace["name"] == valid_namespace_data["name"]
    
    def test_get_namespace_not_found(
        self,
        registry_service: RegistryService
    ) -> None:
        """Test retrieving a non-existent namespace."""
        # Act & Assert
        with pytest.raises(NamespaceNotFoundError):
            registry_service.get_namespace("non-existent-id")
    
    @pytest.mark.parametrize("invalid_id", [
        "",
        None,
        123,  # Should be string
        "invalid format",
    ])
    def test_get_namespace_invalid_id(
        self,
        registry_service: RegistryService,
        invalid_id: Any
    ) -> None:
        """Test that invalid namespace IDs raise ValidationError."""
        # Act & Assert
        with pytest.raises(ValidationError):
            registry_service.get_namespace(invalid_id)
```

---

## 7. Pre-commit 設定範例

```yaml
# .pre-commit-config.yaml
repos:
  # 通用 hooks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=1000']
      - id: check-json
      - id: check-toml
      - id: check-merge-conflict
      - id: detect-private-key
      
  # Python - Black formatter
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.11
        args: ['--line-length=100']
        
  # Python - isort
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ['--profile=black', '--line-length=100']
        
  # Python - Ruff
  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
        
  # Python - MyPy
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: 
          - types-PyYAML
          - types-requests
        args: [--strict, --ignore-missing-imports]
        
  # Python - Security check
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.6
    hooks:
      - id: bandit
        args: [-r, src/, -ll]
        
  # TypeScript/JavaScript - ESLint
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.56.0
    hooks:
      - id: eslint
        files: \.[jt]sx?$
        types: [file]
        additional_dependencies:
          - eslint@8.56.0
          - '@typescript-eslint/eslint-plugin'
          - '@typescript-eslint/parser'
          
  # TypeScript/JavaScript - Prettier
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.1.0
    hooks:
      - id: prettier
        types_or: [javascript, jsx, ts, tsx, json, yaml]
        
  # Secrets detection
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
```

---

**文件版本**: 1.0.0  
**最後更新**: 2026-01-16  
**相關文件**: PR-1-REVIEW-REPORT.md

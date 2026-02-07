# GL User-Facing Layer Specification

## 9. 使用者層（User-Facing Layer）

### 9.1 Layer Overview

The User-Facing Layer defines naming conventions for user-facing resources including UI components, CLI commands, documentation, error codes, messages, and templates. This layer ensures consistent and intuitive naming for all user-interaction points across the platform.

### 9.2 UI Component Naming

**Pattern**: `gl.ui.component`

**Format**: `gl.{platform}.{element}-component`

**Naming Rules**:
- Must use component identifier: `-component`
- Platform identifies the platform component
- Element identifies UI element type: `button|input|modal|dropdown|table|card|header|sidebar|footer`

**Examples**:
```yaml
# Valid
gl.runtime.submit-button-component
gl.api.dropdown-component
gl.data.table-component

# Invalid
button-component
submit-btn
component
```

**Purpose**: Reusable UI components across platforms

### 9.3 UI State Naming

**Pattern**: `gl.ui.state`

**Format**: `gl.{platform}.{scope}-state`

**Naming Rules**:
- Must use state identifier: `-state`
- Platform identifies the platform component
- Scope identifies state scope: `global|local|session|form`

**Examples**:
```yaml
# Valid
gl.runtime.global-state
gl.api.session-state
gl.data.form-state

# Invalid
state
global-state
user-state
```

**Purpose**: State management for UI components

### 9.4 CLI Command Naming

**Pattern**: `gl.cli.command`

**Format**: `gl.{platform}.{action}-command`

**Naming Rules**:
- Must use command identifier: `-command`
- Platform identifies the platform component
- Action identifies command action: `create|delete|update|list|get|run|deploy|stop|start`

**Examples**:
```yaml
# Valid
gl.runtime.create-command
gl.api.list-command
gl.data.deploy-command

# Invalid
command
create
cli-command
```

**Purpose**: Top-level CLI commands

### 9.5 CLI Subcommand Naming

**Pattern**: `gl.cli.subcommand`

**Format**: `gl.{platform}.{resource}-subcommand`

**Naming Rules**:
- Must use subcommand identifier: `-subcommand`
- Platform identifies the platform component
- Resource identifies subcommand resource

**Examples**:
```yaml
# Valid
gl.runtime.pod-subcommand
gl.api.service-subcommand
gl.data.deployment-subcommand

# Invalid
subcommand
pod
service
```

**Purpose**: CLI subcommands for specific resources

### 9.6 CLI Flag Naming

**Pattern**: `gl.cli.flag`

**Format**: `gl.{platform}.{option}-flag`

**Naming Rules**:
- Must use flag identifier: `-flag`
- Platform identifies the platform component
- Option identifies flag option: `output|format|config|verbose|quiet|force|dry-run`

**Examples**:
```yaml
# Valid
gl.runtime.output-flag
gl.api.format-flag
gl.data.config-flag

# Invalid
flag
output
--output
```

**Purpose**: CLI command flags and options

### 9.7 Documentation Naming

**Pattern**: `gl.doc`

**Format**: `gl.{type}.{topic}-doc`

**Naming Rules**:
- Must use doc identifier: `-doc`
- Type identifies documentation type: `guide|reference|api|tutorial|troubleshooting|faq`
- Topic identifies documentation topic

**Examples**:
```yaml
# Valid
gl.guide.setup-doc
gl.api.reference-doc
gl.tutorial.quickstart-doc

# Invalid
doc
setup
guide
```

**Purpose**: Documentation files and guides

### 9.8 Error Code Naming

**Pattern**: `gl.error_code`

**Format**: `gl.{domain}.{type}-error`

**Naming Rules**:
- Must use error identifier: `-error`
- Domain identifies error domain
- Type identifies error type: `validation|authentication|authorization|not-found|internal|network|timeout`

**Examples**:
```yaml
# Valid
gl.runtime.validation-error
gl.api.authentication-error
gl.data.network-error

# Invalid
error
validation-error
code-error
```

**Purpose**: System error codes and messages

### 9.9 Message Naming

**Pattern**: `gl.message`

**Format**: `gl.{scope}.{type}-message`

**Naming Rules**:
- Must use message identifier: `-message`
- Scope identifies message scope
- Type identifies message type: `success|info|warning|error|debug`

**Examples**:
```yaml
# Valid
gl.runtime.success-message
gl.api.info-message
gl.data.warning-message

# Invalid
message
success
warning
```

**Purpose**: User-facing messages and notifications

### 9.10 Template Naming

**Pattern**: `gl.template`

**Format**: `gl.{platform}.{type}-template`

**Naming Rules**:
- Must use template identifier: `-template`
- Platform identifies the platform component
- Type identifies template type: `deployment|config|email|report|notification`

**Examples**:
```yaml
# Valid
gl.runtime.deployment-template
gl.api.config-template
gl.data.email-template

# Invalid
template
deployment
config
```

**Purpose**: Reusable templates for various purposes

### 9.11 User-Facing Layer Integration

### 9.11.1 Layer Dependencies
- Depends on: All layers (provides user interface)
- Provides: User interaction capabilities
- Works with: Documentation for user guides

### 9.11.2 Naming Hierarchy
```
gl.user-facing/
├── ui/
│   ├── gl.ui.component
│   └── gl.ui.state
├── cli/
│   ├── gl.cli.command
│   ├── gl.cli.subcommand
│   └── gl.cli.flag
├── docs/
│   └── gl.doc
├── communication/
│   ├── gl.error_code
│   ├── gl.message
│   └── gl.template
```

### 9.11.3 Cross-Layer Integration
- **User-Facing → Platform**: Platform user interfaces
- **User-Facing → Deployment**: Deployment user controls
- **User-Facing → Security**: Security UI components
- **User-Facing → Observability**: Monitoring dashboards

## 9.12 Best Practices

### 9.12.1 Component Reusability
```yaml
# Reusable UI components
gl.ui.button-component
gl.ui.input-component
gl.ui.modal-component
gl.ui.dropdown-component
```

### 9.12.2 Command Structure
```yaml
# CLI command hierarchy
gl.cli.command: gl.runtime
gl.cli.subcommand: pod, service, deployment
gl.cli.flag: --output, --format, --config

# Example usage
gl.runtime create command
  --output json
  --config gl.runtime.config-template
```

### 9.12.3 Error Handling
```yaml
# Error codes with context
gl.runtime.validation-error
  - gl.runtime.invalid-input-message
  - gl.runtime.field-required-message

gl.api.authentication-error
  - gl.api.credentials-invalid-message
  - gl.api.token-expired-message
```

### 9.12.4 Documentation Organization
```yaml
# Structured documentation
gl.guide.setup-doc
gl.guide.configuration-doc
gl.api.reference-doc
gl.tutorial.quickstart-doc
gl.troubleshooting.common-issues-doc
gl.faq.frequent-questions-doc
```

## 9.13 Validation Rules

### Rule UL-001: Component Identifier
- **Severity**: CRITICAL
- **Check**: UI components must end with `-component` identifier
- **Pattern**: `^gl\..+\.button|input|modal|dropdown|table|card|header|sidebar|footer-component$`

### Rule UL-002: Command Action Validation
- **Severity**: CRITICAL
- **Check**: CLI commands must use valid action verbs
- **Valid Actions**: create|delete|update|list|get|run|deploy|stop|start

### Rule UL-003: Flag Format
- **Severity**: HIGH
- **Check**: CLI flags must follow kebab-case format
- **Pattern**: `^[a-z]+(-[a-z]+)*-flag$`

### Rule UL-004: Error Code Uniqueness
- **Severity**: CRITICAL
- **Check**: Error codes must be unique across the system
- **Enforcement**: Central error code registry

### Rule UL-005: Message Localization
- **Severity**: MEDIUM
- **Check**: Messages must support localization
- **Required**: Message ID and default text

### Rule UL-006: Template Variables
- **Severity**: HIGH
- **Check**: Templates must define variable schemas
- **Required**: Variable list and validation rules

## 9.14 Usage Examples

### Example 1: Complete UI Component System
```yaml
# UI Components
apiVersion: ui.gl.io/v1
kind: Component
metadata:
  name: gl.runtime.submit-button-component
spec:
  type: button
  label: Submit
  onClick: gl.runtime.submit-action
  state: gl.runtime.form-state
---
apiVersion: ui.gl.io/v1
kind: State
metadata:
  name: gl.runtime.form-state
spec:
  scope: local
  initial: {
    username: "",
    password: "",
    submitting: false
  }
```

### Example 2: CLI Command Structure
```yaml
# CLI Command
apiVersion: cli.gl.io/v1
kind: Command
metadata:
  name: gl.runtime.create-command
spec:
  action: create
  help: Create a new resource
  subcommands:
  - gl.runtime.pod-subcommand
  - gl.runtime.service-subcommand
  flags:
  - gl.runtime.output-flag
  - gl.runtime.format-flag
---
# CLI Subcommand
apiVersion: cli.gl.io/v1
kind: Subcommand
metadata:
  name: gl.runtime.pod-subcommand
spec:
  resource: pod
  help: Create a pod
  flags:
  - gl.runtime.config-flag
---
# CLI Flag
apiVersion: cli.gl.io/v1
kind: Flag
metadata:
  name: gl.runtime.output-flag
spec:
  name: --output
  type: string
  default: json
  help: Output format (json, yaml, table)
```

### Example 3: Error Handling System
```yaml
# Error Code
apiVersion: error.gl.io/v1
kind: ErrorCode
metadata:
  name: gl.runtime.validation-error
spec:
  code: GL_RUNTIME_001
  severity: error
  message: gl.runtime.invalid-input-message
  documentation: gl.troubleshooting.validation-error-doc
---
# Message
apiVersion: message.gl.io/v1
kind: Message
metadata:
  name: gl.runtime.invalid-input-message
spec:
  type: error
  default: "Invalid input: {field} is required"
  localization:
    zh-TW: "輸入無效：{field} 是必填的"
    zh-CN: "输入无效：{field} 是必填的"
---
# Documentation
apiVersion: doc.gl.io/v1
kind: Doc
metadata:
  name: gl.troubleshooting.validation-error-doc
spec:
  type: troubleshooting
  content: |
    # Validation Error
    This error occurs when required fields are missing.
    
    ## Common Causes
    - Missing required fields
    - Invalid data format
    - Data validation failed
```

### Example 4: Template System
```yaml
# Template
apiVersion: template.gl.io/v1
kind: Template
metadata:
  name: gl.runtime.deployment-template
spec:
  type: deployment
  version: 1.0.0
  variables:
  - name: image
    type: string
    required: true
  - name: replicas
    type: integer
    default: 3
  content: |
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: gl.runtime.core-deployment
    spec:
      replicas: {{ replicas }}
      selector:
        matchLabels:
          app: gl.runtime.core-pod
      template:
        metadata:
          labels:
            app: gl.runtime.core-pod
        spec:
          containers:
          - name: core
            image: {{ image }}
```

### Example 5: Documentation System
```yaml
# Documentation Files
apiVersion: doc.gl.io/v1
kind: Doc
metadata:
  name: gl.guide.setup-doc
spec:
  type: guide
  title: Setup Guide
  order: 1
  content: |
    # Platform Setup Guide
    
    ## Prerequisites
    - Kubernetes cluster
    - gl.runtime platform
    
    ## Installation
    Follow these steps to install the platform.
---
apiVersion: doc.gl.io/v1
kind: Doc
metadata:
  name: gl.api.reference-doc
spec:
  type: reference
  title: API Reference
  content: |
    # API Reference
    
    ## Endpoints
    - GET /api/v1/pods
    - POST /api/v1/pods
    - PUT /api/v1/pods/:id
---
apiVersion: doc.gl.io/v1
kind: Doc
metadata:
  name: gl.tutorial.quickstart-doc
spec:
  type: tutorial
  title: Quickstart Tutorial
  content: |
    # Quickstart Tutorial
    
    ## Step 1: Create Pod
    ```
    gl.runtime create pod --name my-pod
    ```
    
    ## Step 2: List Pods
    ```
    gl.runtime list pods
    ```
```

## 9.15 Compliance Checklist

- [x] UI component naming follows `gl.{platform}.{element}-component` pattern
- [x] UI state naming includes `-state` identifier
- [x] CLI command naming includes `-command` identifier with valid action
- [x] CLI subcommand naming includes `-subcommand` identifier
- [x] CLI flag naming includes `-flag` identifier
- [x] Documentation naming includes `-doc` identifier
- [x] Error code naming includes `-error` identifier
- [x] Message naming includes `-message` identifier
- [x] Template naming includes `-template` identifier
- [x] Error codes are unique across system
- [x] Messages support localization
- [x] Templates define variable schemas
- [x] CLI flags use kebab-case format

## 9.16 Tool Integration

### 9.16.1 Component Library
```typescript
// TypeScript UI component
export const SubmitButton: React.FC = () => {
  const state = useGLState('gl.runtime.form-state');
  
  return (
    <button 
      className="gl.runtime.submit-button-component"
      onClick={() => handleSubmit()}
    >
      Submit
    </button>
  );
};
```

### 9.16.2 CLI Framework
```python
# Python CLI command
@click.command()
@click.option('--output', type=click.Choice(['json', 'yaml', 'table']))
@click.option('--config', type=click.Path(exists=True))
def create(output, config):
    """Create a new resource"""
    # Implementation
```

### 9.16.3 Error Handling
```python
# Python error handling
class GLValidationError(Exception):
    def __init__(self, field):
        self.code = "gl.runtime.validation-error"
        self.message = f"Invalid input: {field} is required"
```

### 9.16.4 Pre-commit Hooks
```bash
#!/bin/bash
# Validate user-facing naming conventions
for file in $(git diff --name-only --cached | grep -E '\.(ts|tsx|py|yaml|yml)$'); do
  # Check component naming
  if grep -E "export.*Component" "$file" | grep -vE "gl\..+\.component"; then
    echo "ERROR: Invalid component naming in $file"
    exit 1
  fi
  
  # Check command naming
  if grep -E "@click.command|click.Group" "$file" | grep -vE "gl\..+\.command"; then
    echo "ERROR: Invalid command naming in $file"
    exit 1
  fi
done
```

## 9.17 References

- UI/UX Best Practices: https://design-system.microsoft.com/
- CLI Design: https://clig.dev/
- Error Handling: https://tools.ietf.org/html/rfc7807
- Documentation Standards: https://www.writethedocs.org/
- Naming Convention Principles: gl-prefix-principles-engineering.md
- Platform Layer: gl-platform-layer-specification.md
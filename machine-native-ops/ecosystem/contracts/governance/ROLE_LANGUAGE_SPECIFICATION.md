# MNGA Role Language Specification
## Version: 1.0.0
## Layer: MNGA-L0 (Language Layer)

---

## Overview

The Role Language Specification defines the formal syntax and semantics for invoking roles within the MNGA Role Execution Layer (L5.5). This specification enables declarative role invocation with structured parameters, ensuring all role interactions are governable, traceable, and auditable.

---

## 1. Syntax Definition

### 1.1 Basic Invocation Syntax

```
@role <role-id> <input> [options]
```

**Components:**
- `@role`: Role invocation keyword (MNGA-L0 syntax)
- `<role-id>`: Fully qualified role identifier (format: `namespace.role-name`)
- `<input>`: Target artifact or input for the role
- `[options]`: Optional parameters and flags

### 1.2 Formal Grammar (BNF)

```
<role_invocation> ::= "@" "role" <role_id> <input> [ <options> ]
<role_id> ::= <namespace> "." <role_name>
<namespace> ::= <identifier>
<role_name> ::= <identifier>
<input> ::= <path> | <artifact_id> | <string>
<options> ::= <option> [ <options> ]
<option> ::= <flag> | <parameter>
<flag> ::= "--" <identifier>
<parameter> ::= "--" <identifier> "=" <value>
<value> ::= <string> | <number> | <boolean> | <array>
<identifier> ::= [a-z] [a-z0-9-]*
```

### 1.3 Examples

```bash
# Basic invocation
@role ecosystem.runner ecosystem/

# With parameters
@role ecosystem.architect analyze platform-cloud/ --depth=full

# Multiple options
@role ecosystem.analyst detect-drift contracts/ --severity=CRITICAL --baseline=v1.2.0

# Complex invocation
@role ecosystem.semantic-checker verify src/ --depth=contextual --anchors=MNGA-L2,MNGA-L3
```

---

## 2. Parameter Types

### 2.1 String Parameters

```bash
@role ecosystem.validator validate contract.yaml --schema_version="1.0.0"
```

### 2.2 Numeric Parameters

```bash
@role ecosystem.runner scan src/ --scan_depth=10 --timeout=300
```

### 2.3 Boolean Flags

```bash
@role ecosystem.validator validate schema.json --strict_mode=true
@role ecosystem.analyst analyze / --include_dependencies
```

### 2.4 Array Parameters

```bash
@role ecosystem.runner scan / --include_patterns=["*.py","*.yaml"] --exclude_patterns=["test_*"]
```

---

## 3. Role Command Categories

### 3.1 Execution Commands (L5)

Commands that execute actions and produce results:

```bash
@role ecosystem.run <target> [options]
@role ecosystem.execute <target> [options]
@role ecosystem.process <target> [options]
```

### 3.2 Analysis Commands (L6)

Commands that perform analysis and reasoning:

```bash
@role ecosystem.architect analyze <target> [options]
@role ecosystem.analyst detect <target> [options]
@role ecosystem.semantic-checker verify <target> [options]
```

### 3.3 Validation Commands (L5)

Commands that validate and enforce rules:

```bash
@role ecosystem.validator validate <target> [options]
@role ecosystem.validator check <target> [options]
@role ecosystem.validator enforce <target> [options]
```

---

## 4. Input/Output Contract

### 4.1 Input Format

All role invocations MUST provide:
- **Target**: Path, artifact ID, or string input
- **Parameters**: Optional key-value pairs
- **Context**: Optional context metadata

### 4.2 Output Format

All role executions MUST return:

```json
{
  "role_id": "ecosystem.runner",
  "invocation_id": "uuid-v4",
  "status": "success|warning|failed",
  "timestamp": "2025-01-01T00:00:00Z",
  "duration_ms": 1500,
  "result": {
    // Role-specific output
  },
  "metadata": {
    "evidence_links": [],
    "audit_id": "uuid-v4",
    "correlation_id": "uuid-v4"
  }
}
```

---

## 5. Semantic Layer Mapping

### 5.1 MNGA-L0: Language Layer
- Defines the syntax (`@role`, `--parameter`)
- Defines grammar and parsing rules
- Defines token structure

### 5.2 MNGA-L1: Format Layer
- Defines input/output format (JSON)
- Defines parameter serialization
- Defines error response format

### 5.3 MNGA-L2: Semantic Layer
- Defines role semantics (what a role "means")
- Defines parameter semantics
- Defines result semantics

### 5.4 MNGA-L3: Index Layer
- Provides role registry lookup
- Provides role metadata query
- Provides capability search

### 5.5 MNGA-L5: Enforcement Layer
- Executes role logic
- Enforces governance rules
- Generates evidence

### 5.6 MNGA-L6: Reasoning Layer
- Performs semantic analysis
- Performs reasoning tasks
- Provides recommendations

---

## 6. Governance Enforcement

### 6.1 Pre-Invocation Validation

Before any role invocation:
1. **Role Lookup**: Verify role exists in registry
2. **Permission Check**: Verify caller has required permissions
3. **Parameter Validation**: Validate parameters against role schema
4. **Context Validation**: Validate context against governance rules

### 6.2 Post-Invocation Validation

After any role execution:
1. **Result Validation**: Validate result matches output schema
2. **Evidence Collection**: Collect evidence chain
3. **Audit Logging**: Log to audit trail
4. **Compliance Check**: Verify compliance with governance rules

---

## 7. Error Handling

### 7.1 Error Codes

| Code | Severity | Description |
|------|----------|-------------|
| R001 | CRITICAL | Role not found in registry |
| R002 | HIGH | Permission denied |
| R003 | HIGH | Invalid parameter format |
| R004 | MEDIUM | Validation failed |
| R005 | CRITICAL | Execution timeout |
| R006 | HIGH | Evidence generation failed |

### 7.2 Error Response Format

```json
{
  "error": {
    "code": "R001",
    "severity": "CRITICAL",
    "message": "Role not found: ecosystem.invalid",
    "timestamp": "2025-01-01T00:00:00Z",
    "suggestion": "Available roles: ecosystem.runner, ecosystem.architect, ..."
  }
}
```

---

## 8. Best Practices

### 8.1 Naming Conventions
- Role IDs: `namespace.role-name` (kebab-case)
- Parameters: `snake_case`
- Values: Follow language-specific conventions

### 8.2 Security
- Never pass secrets as parameters (use environment variables)
- Validate all inputs before role execution
- Audit all role invocations

### 8.3 Performance
- Use asynchronous execution for long-running tasks
- Implement proper timeouts
- Cache role definitions

---

## 9. Examples

### 9.1 Complete Workflow

```bash
# 1. Scan directory
@role ecosystem.scan ecosystem/ --depth=10 --output=index.json

# 2. Validate results
@role ecosystem.validator validate index.json --strict=true

# 3. Analyze architecture
@role ecosystem.architect analyze ecosystem/ --analysis_type=["consistency","topology"]

# 4. Detect drift
@role ecosystem.analyst detect-drift ecosystem/ --baseline=main

# 5. Verify semantics
@role ecosystem.semantic-checker verify ecosystem/ --depth=contextual
```

### 9.2 Pipeline Integration

```yaml
# CI/CD Pipeline
steps:
  - name: "Run governance checks"
    run: "@role ecosystem.runner scan . --include_patterns=['*.yaml']"
  
  - name: "Validate contracts"
    run: "@role ecosystem.validator validate contracts/ --strict=true"
  
  - name: "Analyze architecture"
    run: "@role ecosystem.architect analyze ecosystem/ --depth=deep"
```

---

## 10. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-01-01 | Initial specification |

---

## Appendix A: Role Registry

Current registered roles:
- `ecosystem.runner` - Directory scanner and index builder
- `ecosystem.architect` - Architecture analyzer
- `ecosystem.analyst` - Drift and inconsistency detector
- `ecosystem.validator` - Contract and schema validator
- `ecosystem.semantic-checker` - Semantic analyzer

---

## Appendix B: Implementation Status

- ✅ Schema definition complete
- ✅ Role registry complete
- ✅ Language specification complete
- ⏳ Parser implementation pending
- ⏳ Runtime executor pending
- ⏳ Governance enforcement integration pending
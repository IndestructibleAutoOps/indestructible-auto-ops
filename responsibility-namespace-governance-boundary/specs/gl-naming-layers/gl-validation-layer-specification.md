# GL Validation Layer Specification

## Validation Layer - 驗證層

### Layer Overview

The Validation Layer defines naming conventions for validation resources including schema validations, data validations, compliance validations, and quality checks. This layer ensures consistent validation management across the platform, enabling effective data quality, compliance, and error prevention.

### 1. Schema Validation Naming

**Pattern**: `gl.validation.schema`

**Format**: `gl.{resource}.{type}-schema-validation`

**Naming Rules**:
- Must use schema validation identifier: `-schema-validation`
- Resource identifies the validated resource
- Type identifies the validation type: `json|xml|yaml|protobuf|avro`

**Examples**:
```yaml
# Valid
gl.runtime.json-schema-validation
gl.data.xml-schema-validation
gl.security.yaml-schema-validation

# Invalid
json-schema-validation
runtime-schema-validation
schema-validation
```

**Purpose**: Schema validation definitions

### 2. Data Validation Naming

**Pattern**: `gl.validation.data`

**Format**: `gl.{entity}.{field}-data-validation`

**Naming Rules**:
- Must use data validation identifier: `-data-validation`
- Entity identifies the validated entity
- Field identifies the validated field

**Examples**:
```yaml
# Valid
gl.runtime.email-data-validation
gl.data.phone-data-validation
gl.security.ssn-data-validation

# Invalid
email-data-validation
runtime-data-validation
data-validation
```

**Purpose**: Data validation definitions

### 3. Compliance Validation Naming

**Pattern**: `gl.validation.compliance`

**Format**: `gl.{standard}.{control}-compliance-validation`

**Naming Rules**:
- Must use compliance validation identifier: `-compliance-validation`
- Standard identifies the compliance standard
- Control identifies the compliance control

**Examples**:
```yaml
# Valid
gl.security.gdpr-compliance-validation
gl.data.hipaa-compliance-validation
gl.runtime.pci-compliance-validation

# Invalid
gdpr-compliance-validation
runtime-compliance-validation
compliance-validation
```

**Purpose**: Compliance validation definitions

### 4. Quality Check Naming

**Pattern**: `gl.validation.quality-check`

**Format**: `gl.{component}.{metric}-quality-check`

**Naming Rules**:
- Must use quality check identifier: `-quality-check`
- Component identifies the checked component
- Metric identifies the quality metric

**Examples**:
```yaml
# Valid
gl.runtime.code-quality-check
gl.data.data-quality-check
gl.security.security-quality-check

# Invalid
code-quality-check
runtime-quality-check
quality-check
```

**Purpose**: Quality check definitions

### 5. Constraint Validation Naming

**Pattern**: `gl.validation.constraint`

**Format**: `gl.{entity}.{type}-constraint-validation`

**Naming Rules**:
- Must use constraint validation identifier: `-constraint-validation`
- Entity identifies the constrained entity
- Type identifies the constraint type: `unique|foreign-key|check|not-null`

**Examples**:
```yaml
# Valid
gl.runtime.unique-constraint-validation
gl.data.foreign-key-constraint-validation
gl.security.check-constraint-validation

# Invalid
unique-constraint-validation
runtime-constraint-validation
constraint-validation
```

**Purpose**: Constraint validation definitions

### 6. Format Validation Naming

**Pattern**: `gl.validation.format`

**Format**: `gl.{field}.{type}-format-validation`

**Naming Rules**:
- Must use format validation identifier: `-format-validation`
- Field identifies the validated field
- Type identifies the format type: `email|phone|url|date|credit-card`

**Examples**:
```yaml
# Valid
gl.runtime.email-format-validation
gl.data.phone-format-validation
gl.security.url-format-validation

# Invalid
email-format-validation
runtime-format-validation
format-validation
```

**Purpose**: Format validation definitions

### 7. Range Validation Naming

**Pattern**: `gl.validation.range`

**Format**: `gl.{field}.{type}-range-validation`

**Naming Rules**:
- Must use range validation identifier: `-range-validation`
- Field identifies the validated field
- Type identifies the range type: `numeric|date|length`

**Examples**:
```yaml
# Valid
gl.runtime.numeric-range-validation
gl.data.date-range-validation
gl.security.length-range-validation

# Invalid
numeric-range-validation
runtime-range-validation
range-validation
```

**Purpose**: Range validation definitions

### 8. Business Rule Validation Naming

**Pattern**: `gl.validation.business-rule`

**Format**: `gl.{domain}.{rule}-business-rule-validation`

**Naming Rules**:
- Must use business rule validation identifier: `-business-rule-validation`
- Domain identifies the business domain
- Rule identifies the business rule

**Examples**:
```yaml
# Valid
gl.runtime.age-business-rule-validation
gl.data.inventory-business-rule-validation
gl.security.credit-business-rule-validation

# Invalid
age-business-rule-validation
runtime-business-rule-validation
business-rule-validation
```

**Purpose**: Business rule validation definitions

### 9. Security Validation Naming

**Pattern**: `gl.validation.security`

**Format**: `gl.{vulnerability}.{type}-security-validation`

**Naming Rules**:
- Must use security validation identifier: `-security-validation`
- Vulnerability identifies the security vulnerability
- Type identifies the security validation type

**Examples**:
```yaml
# Valid
gl.security.xss-security-validation
gl.runtime.sql-injection-security-validation
gl.data.csrf-security-validation

# Invalid
xss-security-validation
runtime-security-validation
security-validation
```

**Purpose**: Security validation definitions

### 10. Validation Layer Integration

### Cross-Layer Dependencies
- **Depends on**: All layers (validation applies to all resources)
- **Provides**: Validation conventions
- **Works with**: Security Layer for security validation
- **Works with**: Testing Layer for validation testing

### Naming Hierarchy
```
gl.validation/
├── schema/
│   └── gl.validation.schema
├── data/
│   ├── gl.validation.data
│   ├── gl.validation.constraint
│   ├── gl.validation.format
│   └── gl.validation.range
├── compliance/
│   └── gl.validation.compliance
├── quality/
│   └── gl.validation.quality-check
├── business/
│   └── gl.validation.business-rule
└── security/
    └── gl.validation.security
```

### Validation Rules

### Rule VL-001: Schema Validation Convention
- **Severity**: CRITICAL
- **Check**: Schema validations must follow `gl.{resource}.{type}-schema-validation` pattern
- **Pattern**: `^gl\..+\.json|xml|yaml|protobuf|avro-schema-validation$`

### Rule VL-002: Data Type Consistency
- **Severity**: HIGH
- **Check**: Data validations must match data types
- **Required**: Type matching between schema and data

### Rule VL-003: Compliance Standard Alignment
- **Severity**: CRITICAL
- **Check**: Compliance validations must reference valid standards
- **Valid Standards**: GDPR, HIPAA, PCI-DSS, SOC2, ISO27001

### Rule VL-004: Quality Thresholds
- **Severity**: MEDIUM
- **Check**: Quality checks must have thresholds
- **Required**: Minimum quality score and threshold

### Rule VL-005: Constraint Enforcement
- **Severity**: HIGH
- **Check**: Constraint validations must be enforced
- **Required**: Enforcement action and error handling

### Rule VL-006: Security Validation Coverage
- **Severity**: HIGH
- **Check**: Security validations must cover OWASP Top 10
- **Required**: Coverage of common vulnerabilities

### Usage Examples

### Example 1: Complete Validation Stack
```yaml
# Schema Validation
apiVersion: gl.io/v1
kind: SchemaValidation
metadata:
  name: gl.runtime.json-schema-validation
spec:
  type: json-schema-validation
  resource: user
  schema: |
    {
      "$schema": "http://json-schema.org/draft-07/schema#",
      "type": "object",
      "properties": {
        "name": {"type": "string"},
        "email": {"type": "string", "format": "email"}
      },
      "required": ["name", "email"]
    }

# Data Validation
apiVersion: gl.io/v1
kind: DataValidation
metadata:
  name: gl.runtime.email-data-validation
spec:
  entity: user
  field: email
  type: string
  format: email
  regex: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"

# Compliance Validation
apiVersion: gl.io/v1
kind: ComplianceValidation
metadata:
  name: gl.security.gdpr-compliance-validation
spec:
  standard: GDPR
  control: data-portability
  scope: gl.runtime
  checks:
  - user-data-export
  - data-format-validation
  complianceThreshold: 100%
```

### Example 2: Quality and Constraint Validation
```yaml
# Quality Check
apiVersion: gl.io/v1
kind: QualityCheck
metadata:
  name: gl.runtime.code-quality-check
spec:
  component: gl.runtime
  metric: code
  checks:
  - cyclomatic-complexity
  - code-coverage
  - duplication
  thresholds:
    cyclomatic-complexity: 10
    code-coverage: 80
    duplication: 5

# Constraint Validation
apiVersion: gl.io/v1
kind: ConstraintValidation
metadata:
  name: gl.runtime.unique-constraint-validation
spec:
  entity: user
  type: unique
  field: email
  enforcement: strict
  errorHandling: reject
```

### Example 3: Security and Format Validation
```yaml
# Security Validation
apiVersion: gl.io/v1
kind: SecurityValidation
metadata:
  name: gl.security.xss-security-validation
spec:
  vulnerability: xss
  type: security
  scope: gl.runtime
  checks:
  - input-sanitization
  - output-encoding
  - content-security-policy
  severity: HIGH
  remediation: "Implement input validation and output encoding"

# Format Validation
apiVersion: gl.io/v1
kind: FormatValidation
metadata:
  name: gl.runtime.email-format-validation
spec:
  field: email
  type: email
  regex: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
  errorHandling: reject
  errorMessage: "Invalid email format"
```

### Best Practices

### Validation Organization
```yaml
# Hierarchical validation structure
validations:
  schema:
    - gl.runtime.json-schema-validation
    - gl.data.xml-schema-validation
  data:
    - gl.runtime.email-data-validation
    - gl.data.phone-data-validation
  compliance:
    - gl.security.gdpr-compliance-validation
    - gl.data.hipaa-compliance-validation
  security:
    - gl.security.xss-security-validation
    - gl.runtime.sql-injection-security-validation
```

### Quality Thresholds
```yaml
# Quality check thresholds
quality:
  code:
    - gl.runtime.code-quality-check: 80%
  data:
    - gl.data.data-quality-check: 90%
  security:
    - gl.security.security-quality-check: 95%
```

### Tool Integration

### Validation Execution
```bash
# Run schema validation
gl validation schema validate gl.runtime.json-schema-validation

# Run data validation
gl validation data validate gl.runtime.email-data-validation

# Run compliance validation
gl validation compliance validate gl.security.gdpr-compliance-validation
```

### Validation Enforcement
```python
# Python validation enforcement
def validate_data(data, validation):
    """Validate data against validation rules"""
    if validation.type == "schema":
        schema = load_schema(validation.schema)
        return validate(data, schema)
    elif validation.type == "data":
        if validation.regex:
            return re.match(validation.regex, data)
    return False
```

### Compliance Checklist

- [x] Schema validation naming follows `gl.{resource}.{type}-schema-validation` pattern
- [x] Data validation naming includes `-data-validation` identifier
- [x] Compliance validation naming includes `-compliance-validation` identifier
- [x] Quality check naming includes `-quality-check` identifier
- [x] Constraint validation naming includes `-constraint-validation` identifier
- [x] Format validation naming includes `-format-validation` identifier
- [x] Range validation naming includes `-range-validation` identifier
- [x] Business rule validation naming includes `-business-rule-validation` identifier
- [x] Security validation naming includes `-security-validation` identifier
- [x] All validations follow naming conventions
- [x] Data validations match data types
- [x] Compliance validations reference valid standards
- [x] Quality checks have thresholds
- [x] Constraint validations are enforced
- [x] Security validations cover OWASP Top 10

### References

- JSON Schema: https://json-schema.org/
- Data Validation: https://pydantic-docs.helpmanual.io/
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- Compliance Standards: GDPR, HIPAA, PCI-DSS, SOC2, ISO27001
- Naming Convention Principles: gl-prefix-principles-engineering.md
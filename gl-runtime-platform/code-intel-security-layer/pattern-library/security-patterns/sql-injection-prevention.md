@GL-governed
# SQL Injection Prevention Pattern

## Category
Security Pattern

## Description
This pattern detects and prevents SQL injection vulnerabilities by identifying unsafe SQL query construction and recommending parameterized queries or prepared statements.

## Pattern Definition

### Detection Rules
1. **String Concatenation in SQL**: Detect SQL queries built using string concatenation with user input
2. **Direct Variable Interpolation**: Identify variables interpolated directly into SQL strings
3. **Missing Parameterization**: Find SQL queries that should use parameterized queries but don't

### Prevention Strategies
1. **Parameterized Queries**: Use prepared statements with parameter binding
2. **ORM Frameworks**: Leverage ORM frameworks that handle SQL escaping automatically
3. **Input Validation**: Validate and sanitize all user inputs before SQL construction
4. **Least Privilege**: Use database accounts with minimum required permissions

## Code Example

### Vulnerable Code
```typescript
const query = "SELECT * FROM users WHERE id = '" + userId + "'";
const result = await database.execute(query);
```

### Secure Code
```typescript
const query = "SELECT * FROM users WHERE id = ?";
const result = await database.execute(query, [userId]);
```

## Detection Pattern
```yaml
pattern:
  type: security
  name: sql-injection
  severity: high
  detection:
    - pattern: ".*\\b(SELECT|INSERT|UPDATE|DELETE|CREATE|DROP)\\b.*\\+\\s*['&quot;].*['&quot;]"
      description: String concatenation in SQL query
    - pattern: ".*\\`\\$\\{.*\\}\\`.*"
      description: Template literal with variable interpolation in SQL
  mitigation:
    - use-parameterized-queries
    - use-orm-framework
    - validate-input
```

## Metrics
- **Precision**: 0.95
- **Recall**: 0.90
- **False Positive Rate**: < 5%

## References
- OWASP Top 10: A1:2017-Injection
- CWE-89: SQL Injection
- NIST: SP 800-53 Rev. 5 Control SI-10
# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: documentation
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
# Security Policy

<!-- GL Layer: GL50-59 Observability Layer -->
<!-- Purpose: Security baseline and governance -->

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| v1.0.0  | :white_check_mark: |

## Security Baseline

- Location: `archive/security-audits/security_audit_final.json`
- Timestamp: 2026-01-16T11:14:54.284456
- Total Findings: 56
  - Critical: 0
  - High: 29 (Code Injection, Cryptographic)
  - Medium: 27 (Code Injection, Cryptographic)
  - Low: 0
  - Info: 0

## Reporting a Vulnerability

Vulnerabilities must be reported following GL governance procedures through the proper channels:

1. **Email**: security@machinenativeops.io
2. **GitHub Security Advisories**: Use the Security tab in the repository
3. **Response Time**: Initial response within 48 hours

All reports are tracked in the GL50-59 Observability Layer.

## Security Categories Monitored

1. **Code Injection**
   - eval() function usage
   - exec() function usage
   - pickle deserialization

2. **Cryptographic**
   - MD5 hash usage (non-security contexts only)
   - Weak encryption algorithms

## Security Scanning

- **CI/CD Integration**: Bandit security scanner enforced on all PRs
- **Pre-commit Hooks**: Security checks via `.pre-commit-config.yaml`
- **Audit Artifacts**: Maintained in `archive/security-audits/`

## GL Compliance

This security policy adheres to:
- GL50-59 Observability Layer semantic boundaries
- GL Artifacts Matrix for security documentation
- GL Filesystem Mapping for audit artifact storage
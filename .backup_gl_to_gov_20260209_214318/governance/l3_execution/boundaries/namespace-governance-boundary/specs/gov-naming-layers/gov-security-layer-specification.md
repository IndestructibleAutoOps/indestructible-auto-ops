# GL Security Layer Specification

## 7. 安全層（Security Layer）

### 7.1 Layer Overview

The Security Layer defines naming conventions for security-related resources, ensuring consistent identification and management of security artifacts across the platform. This layer covers authentication, authorization, encryption, and security policy naming conventions.

### 7.2 Authentication Naming

**Pattern**: `gl.security.auth`

**Format**: `gl.{domain}.{method}-auth`

**Naming Rules**:
- Must use auth identifier: `-auth`
- Domain identifies the authentication scope
- Method identifies authentication type: `oauth|jwt|saml|basic|apikey`

**Examples**:
```yaml
# Valid
gl.security.oauth-auth
gl.api.jwt-auth
gl.runtime.saml-auth

# Invalid
auth
oauth-auth
login
```

**Purpose**: Authentication mechanisms and identity verification

### 7.3 Authorization Naming

**Pattern**: `gl.security.authorization`

**Format**: `gl.{domain}.{method}-authorization`

**Naming Rules**:
- Must use authorization identifier: `-authorization`
- Domain identifies the authorization scope
- Method identifies authorization type: `rbac|abac|pbac`

**Examples**:
```yaml
# Valid
gl.security.rbac-authorization
gl.api.abac-authorization
gl.runtime.pbac-authorization

# Invalid
authorization
rbac
access-control
```

**Purpose**: Access control and permission management

### 7.4 Policy Naming

**Pattern**: `gl.security.policy`

**Format**: `gl.{scope}.{type}-policy`

**Naming Rules**:
- Must use policy identifier: `-policy`
- Scope identifies policy domain
- Type identifies policy type: `network|data|access|encryption`

**Examples**:
```yaml
# Valid
gl.security.network-policy
gl.data.encryption-policy
gl.runtime.access-policy

# Invalid
policy
network-policy
security-policy
```

**Purpose**: Security policy definitions and enforcement rules

### 7.5 Certificate Naming

**Pattern**: `gl.security.certificate`

**Format**: `gl.{domain}.{purpose}-certificate`

**Naming Rules**:
- Must use certificate identifier: `-certificate`
- Domain identifies certificate scope
- Purpose identifies certificate use: `tls|ssl|client|server`

**Examples**:
```yaml
# Valid
gl.security.tls-certificate
gl.api.ssl-certificate
gl.runtime.client-certificate

# Invalid
certificate
tls-cert
cert
```

**Purpose**: SSL/TLS certificates for secure communication

### 7.6 Key Naming

**Pattern**: `gl.security.key`

**Format**: `gl.{domain}.{type}-key`

**Naming Rules**:
- Must use key identifier: `-key`
- Domain identifies key scope
- Type identifies key type: `private|public|signing|encryption`

**Examples**:
```yaml
# Valid
gl.security.private-key
gl.api.signing-key
gl.runtime.encryption-key

# Invalid
key
private-key
secret
```

**Purpose**: Cryptographic keys for encryption and signing

### 7.7 Token Naming

**Pattern**: `gl.security.token`

**Format**: `gl.{domain}.{purpose}-token`

**Naming Rules**:
- Must use token identifier: `-token`
- Domain identifies token scope
- Purpose identifies token use: `access|refresh|session|api`

**Examples**:
```yaml
# Valid
gl.security.access-token
gl.api.refresh-token
gl.runtime.session-token

# Invalid
token
access-token
jwt
```

**Purpose**: Security tokens for authentication and authorization

### 7.8 Secret Naming

**Pattern**: `gl.security.secret`

**Format**: `gl.{domain}.{type}-secret`

**Naming Rules**:
- Must use secret identifier: `-secret`
- Domain identifies secret scope
- Type identifies secret type: `credential|config|key|token`

**Examples**:
```yaml
# Valid
gl.security.credential-secret
gl.api.config-secret
gl.runtime.key-secret

# Invalid
secret
credential
password
```

**Purpose**: Secure storage of sensitive information

### 7.9 Firewall Naming

**Pattern**: `gl.security.firewall`

**Format**: `gl.{scope}.{type}-firewall`

**Naming Rules**:
- Must use firewall identifier: `-firewall`
- Scope identifies firewall boundary
- Type identifies firewall type: `network|application|database`

**Examples**:
```yaml
# Valid
gl.security.network-firewall
gl.api.application-firewall
gl.runtime.database-firewall

# Invalid
firewall
network-firewall
waf
```

**Purpose**: Network and application firewall configurations

### 7.10 Network Security Group Naming

**Pattern**: `gl.security.nsg`

**Format**: `gl.{scope}.{environment}-nsg`

**Naming Rules**:
- Must use NSG identifier: `-nsg`
- Scope identifies security group scope
- Environment identifies deployment environment

**Examples**:
```yaml
# Valid
gl.security.prod-nsg
gl.api.staging-nsg
gl.runtime.test-nsg

# Invalid
nsg
security-group
network-sg
```

**Purpose**: Network security group rules and policies

### 7.11 IAM Role Naming

**Pattern**: `gl.security.iam-role`

**Format**: `gl.{platform}.{function}-role`

**Naming Rules**:
- Must use role identifier: `-role`
- Platform identifies the platform component
- Function identifies the role purpose

**Examples**:
```yaml
# Valid
gl.security.admin-role
gl.api.executor-role
gl.runtime.operator-role

# Invalid
role
admin-role
access-role
```

**Purpose**: Identity and Access Management role definitions

### 7.12 IAM Policy Naming

**Pattern**: `gl.security.iam-policy`

**Format**: `gl.{platform}.{function}-iam-policy`

**Naming Rules**:
- Must use IAM policy identifier: `-iam-policy`
- Platform identifies the platform component
- Function identifies the policy scope

**Examples**:
```yaml
# Valid
gl.security.admin-iam-policy
gl.api.executor-iam-policy
gl.runtime.operator-iam-policy

# Invalid
iam-policy
policy
access-policy
```

**Purpose**: IAM policy definitions for permissions

### 7.13 Security Group Naming

**Pattern**: `gl.security.sg`

**Format**: `gl.{platform}.{type}-sg`

**Naming Rules**:
- Must use security group identifier: `-sg`
- Platform identifies the platform component
- Type identifies group type: `public|private|database`

**Examples**:
```yaml
# Valid
gl.security.public-sg
gl.api.private-sg
gl.runtime.database-sg

# Invalid
sg
security-group
group
```

**Purpose**: Security group configurations for resource isolation

### 7.14 WAF Naming

**Pattern**: `gl.security.waf`

**Format**: `gl.{platform}.{type}-waf`

**Naming Rules**:
- Must use WAF identifier: `-waf`
- Platform identifies the platform component
- Type identifies WAF type: `api|web|global`

**Examples**:
```yaml
# Valid
gl.security.api-waf
gl.api.web-waf
gl.runtime.global-waf

# Invalid
waf
web-firewall
firewall
```

**Purpose**: Web Application Firewall configurations

### 7.15 DLP Naming

**Pattern**: `gl.security.dlp`

**Format**: `gl.{platform}.{scope}-dlp`

**Naming Rules**:
- Must use DLP identifier: `-dlp`
- Platform identifies the platform component
- Scope identifies DLP scope: `data|document|email`

**Examples**:
```yaml
# Valid
gl.security.data-dlp
gl.api.document-dlp
gl.runtime.email-dlp

# Invalid
dlp
data-loss-prevention
protection
```

**Purpose**: Data Loss Prevention configurations

### 7.16 SIEM Naming

**Pattern**: `gl.security.siem`

**Format**: `gl.{platform}.{type}-siem`

**Naming Rules**:
- Must use SIEM identifier: `-siem`
- Platform identifies the platform component
- Type identifies SIEM type: `log|event|alert`

**Examples**:
```yaml
# Valid
gl.security.log-siem
gl.api.event-siem
gl.runtime.alert-siem

# Invalid
siem
security-monitoring
monitoring
```

**Purpose**: Security Information and Event Management

### 7.17 Threat Detection Naming

**Pattern**: `gl.security.threat-detection`

**Format**: `gl.{platform}.{type}-threat-detection`

**Naming Rules**:
- Must use threat detection identifier: `-threat-detection`
- Platform identifies the platform component
- Type identifies detection type: `anomaly|signature|behavior`

**Examples**:
```yaml
# Valid
gl.security.anomaly-threat-detection
gl.api.signature-threat-detection
gl.runtime.behavior-threat-detection

# Invalid
threat-detection
security-detection
threat
```

**Purpose**: Threat detection and monitoring systems

### 7.18 Compliance Naming

**Pattern**: `gl.security.compliance`

**Format**: `gl.{standard}.{control}-compliance`

**Naming Rules**:
- Must use compliance identifier: `-compliance`
- Standard identifies compliance standard: `gdpr|hipaa|pci|iso27001`
- Control identifies specific control

**Examples**:
```yaml
# Valid
gl.security.gdpr-compliance
gl.api.hipaa-compliance
gl.runtime.pci-compliance

# Invalid
compliance
gdpr-compliance
security-compliance
```

**Purpose**: Compliance and audit trail management

### 7.19 Audit Log Naming

**Pattern**: `gl.security.audit-log`

**Format**: `gl.{platform}.{type}-audit-log`

**Naming Rules**:
- Must use audit log identifier: `-audit-log`
- Platform identifies the platform component
- Type identifies log type: `access|change|system`

**Examples**:
```yaml
# Valid
gl.security.access-audit-log
gl.api.change-audit-log
gl.runtime.system-audit-log

# Invalid
audit-log
log
audit
```

**Purpose**: Security audit trail and logging

### 7.20 Security Layer Integration

### 7.20.1 Layer Dependencies
- Depends on: Deployment Layer (for security context)
- Provides: Security enforcement for all layers
- Works with: Policy Layer for security policies

### 7.20.2 Naming Hierarchy
```
gl.security/
├── authentication/
│   ├── gl.security.auth
│   └── gl.security.token
├── authorization/
│   ├── gl.security.authorization
│   ├── gl.security.iam-role
│   └── gl.security.iam-policy
├── encryption/
│   ├── gl.security.certificate
│   ├── gl.security.key
│   └── gl.security.secret
├── network-security/
│   ├── gl.security.firewall
│   ├── gl.security.nsg
│   └── gl.security.sg
├── application-security/
│   ├── gl.security.waf
│   └── gl.security.dlp
└── monitoring/
    ├── gl.security.siem
    ├── gl.security.threat-detection
    ├── gl.security.compliance
    └── gl.security.audit-log
```

### 7.20.3 Cross-Layer Integration
- **Security → Deployment**: Security policies applied to K8s deployments
- **Security → Platform**: Security controls for platform components
- **Security → Data**: Data encryption and DLP policies
- **Security → Contract**: Security contracts and SLAs

## 7.21 Best Practices

### 7.21.1 Principle of Least Privilege
```yaml
# IAM roles follow least privilege
gl.security.read-only-role
gl.security.executor-role
gl.security.admin-role

# Corresponding IAM policies
gl.security.read-only-iam-policy
gl.security.executor-iam-policy
gl.security.admin-iam-policy
```

### 7.21.2 Defense in Depth
```yaml
# Multiple security layers
gl.security.network-firewall
gl.security.api-waf
gl.security.data-dlp
gl.runtime.database-sg
```

### 7.21.3 Separation of Concerns
```yaml
# Authentication vs Authorization
gl.security.oauth-auth
gl.security.rbac-authorization

# Certificates vs Keys
gl.security.tls-certificate
gl.security.private-key

# Secrets vs Config
gl.security.credential-secret
gl.runtime.config-secret
```

### 7.21.4 Audit Trail
```yaml
# Comprehensive audit logging
gl.security.access-audit-log
gl.security.change-audit-log
gl.security.system-audit-log
gl.runtime.event-audit-log
```

## 7.22 Validation Rules

### Rule SL-001: Auth Identifier
- **Severity**: CRITICAL
- **Check**: Authentication resources must end with `-auth` identifier
- **Pattern**: `^gl\..+\.oauth|jwt|saml|basic|apikey-auth$`

### Rule SL-002: Policy Naming Convention
- **Severity**: CRITICAL
- **Check**: Policies must follow `gl.{scope}.{type}-policy` pattern
- **Pattern**: `^gl\..+\.network|data|access|encryption-policy$`

### Rule SL-003: Certificate Validity
- **Severity**: HIGH
- **Check**: Certificates must have validity period defined
- **Required**: `notBefore` and `notAfter` timestamps

### Rule SL-004: Key Rotation Policy
- **Severity**: MEDIUM
- **Check**: Keys must have rotation policy defined
- **Required**: Rotation period and notification settings

### Rule SL-005: Secret Encryption
- **Severity**: CRITICAL
- **Check**: Secrets must be encrypted at rest
- **Required**: Encryption mechanism specified

### Rule SL-006: IAM Role Least Privilege
- **Severity**: HIGH
- **Check**: IAM roles must follow least privilege principle
- **Enforcement**: Review role permissions

### Rule SL-007: Compliance Standard Alignment
- **Severity**: MEDIUM
- **Check**: Compliance must reference specific standard controls
- **Standards**: GDPR, HIPAA, PCI-DSS, ISO27001

## 7.23 Usage Examples

### Example 1: Complete Security Stack
```yaml
# Authentication
apiVersion: v1
kind: Secret
metadata:
  name: gl.security.credential-secret
type: Opaque
stringData:
  oauth-client-id: client-id
  oauth-client-secret: secret-value
---
apiVersion: security.gl.io/v1
kind: Authentication
metadata:
  name: gl.security.oauth-auth
spec:
  type: oauth
  provider: keycloak
---
# Authorization
apiVersion: security.gl.io/v1
kind: Authorization
metadata:
  name: gl.security.rbac-authorization
spec:
  type: rbac
  policies:
  - gl.security.read-only-iam-policy
  - gl.security.executor-iam-policy
---
# Network Security
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: gl.security.network-policy
spec:
  podSelector:
    matchLabels:
      app: gl.runtime.core-pod
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: gl.runtime.core-pod
---
apiVersion: v1
kind: Service
metadata:
  name: gl.security.firewall
spec:
  selector:
    app: gl.runtime.core-pod
  ports:
  - port: 8080
---
# Encryption
apiVersion: v1
kind: Secret
metadata:
  name: gl.security.tls-certificate
type: kubernetes.io/tls
data:
  tls.crt: <base64-cert>
  tls.key: <base64-key>
---
# Monitoring
apiVersion: monitoring.gl.io/v1
kind: SIEM
metadata:
  name: gl.security.log-siem
spec:
  type: log
  retention: 30d
  storage: 100Gi
---
apiVersion: security.gl.io/v1
kind: ThreatDetection
metadata:
  name: gl.security.anomaly-threat-detection
spec:
  type: anomaly
  threshold: 0.9
  action: alert
```

### Example 2: IAM Role and Policy
```yaml
# IAM Role
apiVersion: iam.aws/v1
kind: Role
metadata:
  name: gl.security.admin-role
rules:
- apiGroups:
  - ""
  resources:
  - pods
  - services
  verbs:
  - get
  - list
  - watch
  - create
  - update
  - patch
---
# IAM Policy
apiVersion: iam.aws/v1
kind: Policy
metadata:
  name: gl.security.admin-iam-policy
spec:
  policyDocument:
    Version: "2012-10-17"
    Statement:
    - Effect: Allow
      Action:
      - ec2:DescribeInstances
      - s3:GetObject
      Resource: "*"
```

### Example 3: Compliance and Audit
```yaml
# Compliance
apiVersion: compliance.gl.io/v1
kind: Compliance
metadata:
  name: gl.security.gdpr-compliance
spec:
  standard: GDPR
  version: "2018"
  controls:
  - data-portability
  - right-to-be-forgotten
  - consent-management
  auditLog: gl.security.access-audit-log
---
# Audit Log
apiVersion: logging.gl.io/v1
kind: Log
metadata:
  name: gl.security.access-audit-log
spec:
  type: access
  retention: 7y
  format: json
  fields:
  - timestamp
  - user
  - action
  - resource
  - result
```

### Example 4: Security Group and Firewall
```yaml
# Security Group
apiVersion: vpc.aws/v1
kind: SecurityGroup
metadata:
  name: gl.security.public-sg
spec:
  description: Public access security group
  ingressRules:
  - port: 443
    protocol: tcp
    cidr: 0.0.0.0/0
  egressRules:
  - port: 80
    protocol: tcp
    cidr: 10.0.0.0/8
---
# Firewall
apiVersion: network.gl.io/v1
kind: Firewall
metadata:
  name: gl.security.network-firewall
spec:
  type: network
  rules:
  - name: allow-https
    port: 443
    protocol: tcp
    action: allow
  - name: block-http
    port: 80
    protocol: tcp
    action: deny
```

## 7.24 Compliance Checklist

- [x] Authentication naming follows `gl.{domain}.{method}-auth` pattern
- [x] Authorization naming includes `-authorization` identifier
- [x] Policy naming follows `gl.{scope}.{type}-policy` pattern
- [x] Certificate naming includes `-certificate` identifier
- [x] Key naming includes `-key` identifier with type
- [x] Token naming includes `-token` identifier
- [x] Secret naming includes `-secret` identifier
- [x] Firewall naming includes `-firewall` identifier
- [x] NSG naming includes `-nsg` identifier
- [x] IAM role naming includes `-role` identifier
- [x] IAM policy naming includes `-iam-policy` identifier
- [x] Security group naming includes `-sg` identifier
- [x] WAF naming includes `-waf` identifier
- [x] DLP naming includes `-dlp` identifier
- [x] SIEM naming includes `-siem` identifier
- [x] Threat detection naming includes `-threat-detection` identifier
- [x] Compliance naming includes `-compliance` identifier
- [x] Audit log naming includes `-audit-log` identifier
- [x] All security resources follow least privilege principle
- [x] Proper encryption and key rotation policies defined

## 7.25 Tool Integration

### 7.25.1 Terraform Security
```terraform
# Security resources
resource "aws_iam_role" "admin" {
  name = "gl.security.admin-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_policy" "admin" {
  name = "gl.security.admin-iam-policy"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = ["*"]
      Resource = "*"
    }]
  })
}

resource "aws_security_group" "public" {
  name = "gl.security.public-sg"
  
  ingress {
    from_port = 443
    to_port = 443
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

### 7.25.2 Kubernetes Security
```bash
# Create security resources
kubectl apply -f auth-config.yaml
kubectl apply -f rbac-config.yaml
kubectl apply -f network-policy.yaml

# Verify security policies
kubectl get networkpolicies
kubectl get roles
kubectl get policies
```

### 7.25.3 Pre-commit Hooks
```bash
#!/bin/bash
# Validate security naming conventions
for file in $(git diff --name-only --cached | grep -E '\.(yaml|yml|tf)$'); do
  # Check for secret naming
  if grep -E "kind: Secret" "$file" | grep -vE "name: gl\..+-secret"; then
    echo "ERROR: Invalid secret naming in $file"
    exit 1
  fi
  
  # Check for policy naming
  if grep -E "kind: Policy" "$file" | grep -vE "name: gl\..+-policy"; then
    echo "ERROR: Invalid policy naming in $file"
    exit 1
  fi
done
```

### 7.25.4 Security Scanning
```bash
# Scan for security vulnerabilities
trivy image gl.runtime.core:latest

# Check for exposed secrets
git-secrets scan

# Validate IAM policies
iam-validator validate gl.security.admin-iam-policy.json
```

## 7.26 References

- Security Best Practices: NIST Cybersecurity Framework
- Kubernetes Security: https://kubernetes.io/docs/concepts/security/
- AWS Security: https://docs.aws.amazon.com/security/
- CIS Benchmarks: https://www.cisecurity.org/cis-benchmarks
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- Naming Convention Principles: gov-prefix-principles-engineering.md
- Deployment Layer: gov-deployment-layer-specification.md
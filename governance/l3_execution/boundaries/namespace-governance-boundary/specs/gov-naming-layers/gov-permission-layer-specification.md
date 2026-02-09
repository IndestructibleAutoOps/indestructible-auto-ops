# GL Permission Layer Specification

## Permission Layer - 權限層

### Layer Overview

The Permission Layer defines naming conventions for permission resources including roles, policies, permissions, and access controls. This layer ensures consistent permission management across the platform, enabling effective security, access control, and compliance.

### 1. Role Naming

**Pattern**: `gl.permission.role`

**Format**: `gl.{scope}.{function}-role`

**Naming Rules**:
- Must use role identifier: `-role`
- Scope identifies the role scope
- Function identifies the role function: `admin|editor|viewer|operator|auditor`

**Examples**:
```yaml
# Valid
gl.runtime.admin-role
gl.data.editor-role
gl.security.viewer-role

# Invalid
admin-role
runtime-role
role
```

**Purpose**: Role definitions for access control

### 2. Policy Naming

**Pattern**: `gl.permission.policy`

**Format**: `gl.{resource}.{type}-policy`

**Naming Rules**:
- Must use policy identifier: `-policy`
- Resource identifies the policy resource
- Type identifies the policy type: `access|data|network|security`

**Examples**:
```yaml
# Valid
gl.runtime.access-policy
gl.data.data-policy
gl.security.network-policy

# Invalid
access-policy
runtime-policy
policy
```

**Purpose**: Permission policy definitions

### 3. Permission Naming

**Pattern**: `gl.permission.permission`

**Format**: `gl.{resource}.{action}-permission`

**Naming Rules**:
- Must use permission identifier: `-permission`
- Resource identifies the permission resource
- Action identifies the permission action: `read|write|execute|delete|admin`

**Examples**:
```yaml
# Valid
gl.runtime.read-permission
gl.data.write-permission
gl.security.admin-permission

# Invalid
read-permission
runtime-permission
permission
```

**Purpose**: Individual permission definitions

### 4. Group Naming

**Pattern**: `gl.permission.group`

**Format**: `gl.{department}.{team}-group`

**Naming Rules**:
- Must use group identifier: `-group`
- Department identifies the group department
- Team identifies the group team

**Examples**:
```yaml
# Valid
gl.runtime.backend-group
gl.data.frontend-group
gl.security.devops-group

# Invalid
backend-group
runtime-group
group
```

**Purpose**: User group definitions

### 5. User Naming

**Pattern**: `gl.permission.user`

**Format**: `gl.{type}.{identifier}-user`

**Naming Rules**:
- Must use user identifier: `-user`
- Type identifies the user type
- Identifier identifies the user identifier

**Examples**:
```yaml
# Valid
gl.runtime.service-user
gl.data.human-user
gl.security.system-user

# Invalid
service-user
runtime-user
user
```

**Purpose**: User account definitions

### 6. Access Control Naming

**Pattern**: `gl.permission.access-control`

**Format**: `gl.{resource}.{type}-access-control`

**Naming Rules**:
- Must use access control identifier: `-access-control`
- Resource identifies the access control resource
- Type identifies the access control type: `rbac|abac|pbac`

**Examples**:
```yaml
# Valid
gl.runtime.rbac-access-control
gl.data.abac-access-control
gl.security.pbac-access-control

# Invalid
rbac-access-control
runtime-access-control
access-control
```

**Purpose**: Access control model definitions

### 7. Entitlement Naming

**Pattern**: `gl.permission.entitlement`

**Format**: `gl.{feature}.{level}-entitlement`

**Naming Rules**:
- Must use entitlement identifier: `-entitlement`
- Feature identifies the entitlement feature
- Level identifies the entitlement level

**Examples**:
```yaml
# Valid
gl.runtime.basic-entitlement
gl.data.premium-entitlement
gl.security.enterprise-entitlement

# Invalid
basic-entitlement
runtime-entitlement
entitlement
```

**Purpose**: Entitlement definitions

### 8. Grant Naming

**Pattern**: `gl.permission.grant`

**Format**: `gl.{principal}.{resource}-grant`

**Naming Rules**:
- Must use grant identifier: `-grant`
- Principal identifies the grant principal
- Resource identifies the granted resource

**Examples**:
```yaml
# Valid
gl.runtime.user-group-grant
gl.data.service-role-grant
gl.security.policy-grant

# Invalid
user-group-grant
runtime-grant
grant
```

**Purpose**: Permission grant definitions

### 9. Deny Naming

**Pattern**: `gl.permission.deny`

**Format**: `gl.{principal}.{resource}-deny`

**Naming Rules**:
- Must use deny identifier: `-deny`
- Principal identifies the denied principal
- Resource identifies the denied resource

**Examples**:
```yaml
# Valid
gl.runtime.user-group-deny
gl.data.service-role-deny
gl.security.policy-deny

# Invalid
user-group-deny
runtime-deny
deny
```

**Purpose**: Permission deny definitions

### 10. Permission Layer Integration

### Cross-Layer Dependencies
- **Depends on**: Security Layer (for permission security)
- **Provides**: Permission conventions
- **Works with**: Governance Layer for permission policies
- **Works with**: Deployment Layer for permission deployment

### Naming Hierarchy
```
gl.permission/
├── identities/
│   ├── gl.permission.role
│   ├── gl.permission.group
│   └── gl.permission.user
├── policies/
│   ├── gl.permission.policy
│   └── gl.permission.access-control
├── permissions/
│   ├── gl.permission.permission
│   ├── gl.permission.entitlement
│   ├── gl.permission.grant
│   └── gl.permission.deny
```

### Validation Rules

### Rule PL-001: Role Naming Convention
- **Severity**: CRITICAL
- **Check**: Roles must follow `gl.{scope}.{function}-role` pattern
- **Pattern**: `^gl\..+\.admin|editor|viewer|operator|auditor-role$`

### Rule PL-002: Least Privilege
- **Severity**: HIGH
- **Check**: Roles must follow least privilege principle
- **Required**: Minimal permissions for each role

### Rule PL-003: Separation of Duties
- **Severity**: HIGH
- **Check**: Critical operations require separation of duties
- **Required**: Multiple approvers for sensitive operations

### Rule PL-004: Permission Expiration
- **Severity**: MEDIUM
- **Check**: Temporary permissions must have expiration
- **Required**: Expiration date for temporary grants

### Rule PL-005: Access Review
- **Severity**: HIGH
- **Check**: Permissions must be reviewed periodically
- **Required**: Review schedule and owner

### Rule PL-006: Audit Trail
- **Severity**: CRITICAL
- **Check**: All permission changes must be audited
- **Required**: Timestamp, actor, action, resource

### Usage Examples

### Example 1: Complete Permission Stack
```yaml
# Role
apiVersion: gl.io/v1
kind: Role
metadata:
  name: gl.runtime.admin-role
spec:
  scope: gl.runtime
  function: admin
  permissions:
  - gl.runtime.read-permission
  - gl.runtime.write-permission
  - gl.runtime.admin-permission
  policies:
  - gl.runtime.access-policy

# Policy
apiVersion: gl.io/v1
kind: Policy
metadata:
  name: gl.runtime.access-policy
spec:
  type: access
  resource: gl.runtime
  rules:
  - allow: true
    actions:
    - read
    - write
    resources:
    - pods
    - services
  accessControl: gl.runtime.rbac-access-control

# Group
apiVersion: gl.io/v1
kind: Group
metadata:
  name: gl.runtime.backend-group
spec:
  department: gl.runtime
  team: backend
  members:
  - user1@example.com
  - user2@example.com
  roles:
  - gl.runtime.editor-role
```

### Example 2: Permissions and Grants
```yaml
# Permission
apiVersion: gl.io/v1
kind: Permission
metadata:
  name: gl.runtime.read-permission
spec:
  resource: pods
  action: read
  effect: allow
  conditions:
  - namespace: gl.runtime.prod-ns

# Grant
apiVersion: gl.io/v1
kind: Grant
metadata:
  name: gl.runtime.user-group-grant
spec:
  principal: gl.runtime.backend-group
  resource: gl.runtime
  permissions:
  - gl.runtime.read-permission
  - gl.runtime.write-permission
  expiration: "2024-12-31T23:59:59Z"
  grantedBy: admin@example.com
```

### Example 3: Access Control and Entitlements
```yaml
# Access Control
apiVersion: gl.io/v1
kind: AccessControl
metadata:
  name: gl.runtime.rbac-access-control
spec:
  type: rbac
  resource: gl.runtime
  rules:
  - role: gl.runtime.admin-role
    resources:
    - "*"
    actions:
    - "*"

# Entitlement
apiVersion: gl.io/v1
kind: Entitlement
metadata:
  name: gl.runtime.basic-entitlement
spec:
  feature: basic
  level: basic
  permissions:
  - gl.runtime.read-permission
  limits:
    maxResources: 100
    maxUsers: 10
```

### Best Practices

### Role Design
```yaml
# Follow least privilege principle
roles:
  admin:
    - gl.runtime.admin-role
  editor:
    - gl.runtime.editor-role
  viewer:
    - gl.runtime.viewer-role

# Each role has specific permissions
permissions:
  admin:
    - read
    - write
    - delete
    - admin
  editor:
    - read
    - write
  viewer:
    - read
```

### Access Control
```yaml
# Implement defense in depth
accessControls:
  rbac:
    - gl.runtime.rbac-access-control
  abac:
    - gl.data.abac-access-control
  pbac:
    - gl.security.pbac-access-control
```

### Tool Integration

### Permission Management
```bash
# Create role
gl permission role create gl.runtime.admin-role

# Assign permission
gl permission grant create gl.runtime.user-group-grant

# List permissions
gl permission permission list
```

### Access Control Enforcement
```python
# Python access control
def check_permission(user, resource, action):
    """Check user permission"""
    grants = get_user_grants(user)
    for grant in grants:
        if grant.resource == resource and grant.action == action:
            if not grant.expired():
                return True
    return False
```

### Compliance Checklist

- [x] Role naming follows `gl.{scope}.{function}-role` pattern
- [x] Policy naming includes `-policy` identifier
- [x] Permission naming includes `-permission` identifier
- [x] Group naming includes `-group` identifier
- [x] User naming includes `-user` identifier
- [x] Access control naming includes `-access-control` identifier
- [x] Entitlement naming includes `-entitlement` identifier
- [x] Grant naming includes `-grant` identifier
- [x] Deny naming includes `-deny` identifier
- [x] All roles follow naming conventions
- [x] Roles follow least privilege principle
- [x] Critical operations require separation of duties
- [x] Temporary permissions have expiration
- [x] Permissions are reviewed periodically
- [x] All permission changes are audited

### References

- RBAC Best Practices: https://kubernetes.io/docs/concepts/security/rbac-good-practices/
- ABAC vs RBAC: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_examples.html
- OWASP Access Control: https://owasp.org/www-community/Access_Control
- Naming Convention Principles: gov-prefix-principles-engineering.md
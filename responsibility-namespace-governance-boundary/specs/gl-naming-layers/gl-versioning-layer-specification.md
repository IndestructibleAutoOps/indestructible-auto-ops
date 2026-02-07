# GL Versioning Layer Specification

## Versioning Layer - 版本層

### Layer Overview

The Versioning Layer defines naming conventions for versioning resources including semantic versions, API versions, schema versions, and compatibility tracking. This layer ensures consistent version management across the platform, enabling effective release management, backward compatibility, and upgrade strategies.

### 1. Semantic Version Naming

**Pattern**: `gl.versioning.semantic`

**Format**: `gl.{component}.semantic-version`

**Naming Rules**:
- Must use semantic version identifier: `-semantic-version`
- Component identifies the versioned component
- Follows SemVer 2.0.0 format: MAJOR.MINOR.PATCH

**Examples**:
```yaml
# Valid
gl.runtime.semantic-version: "1.2.3"
gl.data.semantic-version: "2.0.0"
gl.security.semantic-version: "0.1.0-beta.1"

# Invalid
gl.runtime.version: "1.2.3"
runtime-version: "1.2.3"
semantic-version: "1.2.3"
```

**Purpose**: Semantic versioning following SemVer 2.0.0

### 2. API Version Naming

**Pattern**: `gl.versioning.api`

**Format**: `gl.{service}.api-version`

**Naming Rules**:
- Must use API version identifier: `-api-version`
- Service identifies the service name
- Uses date-based or numeric versioning

**Examples**:
```yaml
# Valid
gl.runtime.api-version: "v1"
gl.data.api-version: "v2"
gl.security.api-version: "2024-01-01"

# Invalid
gl.runtime.version: "v1"
runtime-api-version: "v1"
api-version: "v1"
```

**Purpose**: API version management

### 3. Schema Version Naming

**Pattern**: `gl.versioning.schema`

**Format**: `gl.{resource}.schema-version`

**Naming Rules**:
- Must use schema version identifier: `-schema-version`
- Resource identifies the schema resource
- Uses numeric or date-based versioning

**Examples**:
```yaml
# Valid
gl.runtime.user-schema-version: "1.0.0"
gl.data.product-schema-version: "2.0.0"
gl.security.auth-schema-version: "2024-01-01"

# Invalid
gl.runtime.version: "1.0.0"
runtime-schema-version: "1.0.0"
schema-version: "1.0.0"
```

**Purpose**: Schema version tracking

### 4. Contract Version Naming

**Pattern**: `gl.versioning.contract`

**Format**: `gl.{service}.contract-version`

**Naming Rules**:
- Must use contract version identifier: `-contract-version`
- Service identifies the contract service
- Uses semantic or numeric versioning

**Examples**:
```yaml
# Valid
gl.runtime.contract-version: "1.0.0"
gl.data.contract-version: "2.1.0"
gl.security.contract-version: "1.5.0"

# Invalid
gl.runtime.version: "1.0.0"
runtime-contract-version: "1.0.0"
contract-version: "1.0.0"
```

**Purpose**: Contract version management

### 5. Database Version Naming

**Pattern**: `gl.versioning.database`

**Format**: `gl.{database}.migration-version`

**Naming Rules**:
- Must use migration version identifier: `-migration-version`
- Database identifies the database
- Uses timestamp or sequential numbering

**Examples**:
```yaml
# Valid
gl.runtime.migration-version: "20240115103000"
gl.data.migration-version: "20240115103001"
gl.security.migration-version: "001"

# Invalid
gl.runtime.version: "20240115103000"
runtime-migration-version: "20240115103000"
migration-version: "20240115103000"
```

**Purpose**: Database migration versioning

### 6. Release Version Naming

**Pattern**: `gl.versioning.release`

**Format**: `gl.{platform}.release-version`

**Naming Rules**:
- Must use release version identifier: `-release-version`
- Platform identifies the release platform
- Uses semantic versioning with release metadata

**Examples**:
```yaml
# Valid
gl.runtime.release-version: "1.0.0"
gl.data.release-version: "2.0.0"
gl.security.release-version: "1.5.0"

# Invalid
gl.runtime.version: "1.0.0"
runtime-release-version: "1.0.0"
release-version: "1.0.0"
```

**Purpose**: Release version management

### 7. Build Version Naming

**Pattern**: `gl.versioning.build`

**Format**: `gl.{component}.build-version`

**Naming Rules**:
- Must use build version identifier: `-build-version`
- Component identifies the build component
- Uses timestamp or commit hash

**Examples**:
```yaml
# Valid
gl.runtime.build-version: "20240115-a1b2c3d"
gl.data.build-version: "20240115-123456"
gl.security.build-version: "a1b2c3d"

# Invalid
gl.runtime.version: "20240115-a1b2c3d"
runtime-build-version: "20240115-a1b2c3d"
build-version: "20240115-a1b2c3d"
```

**Purpose**: Build version tracking

### 8. Compatibility Version Naming

**Pattern**: `gl.versioning.compatibility`

**Format**: `gl.{resource}.compatibility-version`

**Naming Rules**:
- Must use compatibility version identifier: `-compatibility-version`
- Resource identifies the compatibility resource
- Uses semantic versioning for compatibility ranges

**Examples**:
```yaml
# Valid
gl.runtime.compatibility-version: ">=1.0.0,<2.0.0"
gl.data.compatibility-version: "^1.2.3"
gl.security.compatibility-version: "1.0.0 - 2.0.0"

# Invalid
gl.runtime.version: ">=1.0.0,<2.0.0"
runtime-compatibility-version: ">=1.0.0,<2.0.0"
compatibility-version: ">=1.0.0,<2.0.0"
```

**Purpose**: Compatibility version ranges

### 9. Deprecation Version Naming

**Pattern**: `gl.versioning.deprecation`

**Format**: `gl.{component}.deprecation-version`

**Naming Rules**:
- Must use deprecation version identifier: `-deprecation-version`
- Component identifies the deprecated component
- Includes deprecation date and version

**Examples**:
```yaml
# Valid
gl.runtime.deprecation-version: "1.0.0@2024-06-01"
gl.data.deprecation-version: "2.0.0@2024-12-01"
gl.security.deprecation-version: "1.5.0@2024-03-01"

# Invalid
gl.runtime.version: "1.0.0@2024-06-01"
runtime-deprecation-version: "1.0.0@2024-06-01"
deprecation-version: "1.0.0@2024-06-01"
```

**Purpose**: Deprecation version tracking

### 10. Versioning Layer Integration

### Cross-Layer Dependencies
- **Depends on**: All layers (version applies to all resources)
- **Provides**: Versioning conventions
- **Works with**: Interface Layer for API versioning
- **Works with**: Dependency Layer for version constraints

### Naming Hierarchy
```
gl.versioning/
├── semantic/
│   └── gl.versioning.semantic
├── interfaces/
│   ├── gl.versioning.api
│   ├── gl.versioning.schema
│   └── gl.versioning.contract
├── infrastructure/
│   ├── gl.versioning.database
│   └── gl.versioning.build
├── releases/
│   ├── gl.versioning.release
│   └── gl.versioning.deprecation
└── compatibility/
    └── gl.versioning.compatibility
```

### Validation Rules

### Rule VL-001: SemVer Compliance
- **Severity**: CRITICAL
- **Check**: Semantic versions must follow SemVer 2.0.0
- **Pattern**: `^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$`

### Rule VL-002: API Version Format
- **Severity**: CRITICAL
- **Check**: API versions must follow `v{number}` or `YYYY-MM-DD` format
- **Valid Formats**: v1, v2, 2024-01-01

### Rule VL-003: Database Migration Order
- **Severity**: HIGH
- **Check**: Database migrations must be sequential
- **Required**: Timestamp or sequential numbering

### Rule VL-004: Backward Compatibility
- **Severity**: CRITICAL
- **Check**: Breaking changes must increment MAJOR version
- **Enforcement**: SemVer compliance

### Rule VL-005: Deprecation Notice
- **Severity**: HIGH
- **Check**: Deprecated versions must have removal date
- **Required**: Deprecation date and replacement version

### Rule VL-006: Version Uniqueness
- **Severity**: CRITICAL
- **Check**: Version numbers must be unique per component
- **Enforcement**: Central version registry

### Usage Examples

### Example 1: Complete Versioning Stack
```yaml
# Semantic Versioning
apiVersion: gl.io/v1
kind: SemanticVersion
metadata:
  name: gl.runtime.semantic-version
spec:
  version: "1.2.3"
  major: 1
  minor: 2
  patch: 3
  prerelease: "beta.1"
  build: "20240115"

# API Versioning
apiVersion: gl.io/v1
kind: APIVersion
metadata:
  name: gl.runtime.api-version
spec:
  version: "v1"
  deprecated: false
  deprecationDate: null
  replacementVersion: "v2"

# Schema Versioning
apiVersion: gl.io/v1
kind: SchemaVersion
metadata:
  name: gl.runtime.user-schema-version
spec:
  version: "1.0.0"
  compatibility: ">=1.0.0,<2.0.0"
  breakingChanges: false

# Database Migration
apiVersion: gl.io/v1
kind: DatabaseVersion
metadata:
  name: gl.runtime.migration-version
spec:
  version: "20240115103000"
  type: migration
  description: "Add user table"
  checksum: "sha256:abc123..."
```

### Example 2: Release Management
```yaml
# Release Version
apiVersion: gl.io/v1
kind: ReleaseVersion
metadata:
  name: gl.runtime.release-version
spec:
  version: "1.0.0"
  components:
  - gl.runtime.semantic-version: "1.0.0"
  - gl.data.semantic-version: "1.0.0"
  - gl.security.semantic-version: "1.0.0"
  buildVersion: gl.runtime.build-version
  releaseDate: "2024-01-15T00:00:00Z"
  changelog: |
    - Initial release
    - Add user management
    - Add authentication

# Deprecation
apiVersion: gl.io/v1
kind: DeprecationVersion
metadata:
  name: gl.runtime.deprecation-version
spec:
  version: "1.0.0"
  deprecationDate: "2024-06-01T00:00:00Z"
  removalDate: "2024-12-01T00:00:00Z"
  replacementVersion: "2.0.0"
  reason: "New architecture"
  migrationGuide: "https://docs.gl.runtime/migration/1.0-to-2.0"
```

### Example 3: Compatibility Management
```yaml
# Compatibility Version
apiVersion: gl.io/v1
kind: CompatibilityVersion
metadata:
  name: gl.runtime.compatibility-version
spec:
  version: ">=1.0.0,<2.0.0"
  component: gl.runtime
  supportedVersions:
  - "1.0.0"
  - "1.1.0"
  - "1.2.0"
  deprecatedVersions:
  - "1.0.0"
  breakingChanges:
  - "2.0.0": "API endpoint changed"
```

### Best Practices

### Semantic Versioning
```yaml
# Follow SemVer 2.0.0
versions:
  - gl.runtime.semantic-version: "1.0.0"  # Initial release
  - gl.runtime.semantic-version: "1.1.0"  # New feature, backward compatible
  - gl.runtime.semantic-version: "1.2.3"  # Bug fix
  - gl.runtime.semantic-version: "2.0.0"  # Breaking change

# Pre-release versions
versions:
  - gl.runtime.semantic-version: "2.0.0-alpha.1"
  - gl.runtime.semantic-version: "2.0.0-beta.1"
  - gl.runtime.semantic-version: "2.0.0-rc.1"
  - gl.runtime.semantic-version: "2.0.0"
```

### API Versioning
```yaml
# URL-based versioning
apis:
  - gl.runtime.api-version: "v1"
    path: /api/v1
  - gl.runtime.api-version: "v2"
    path: /api/v2

# Header-based versioning
apis:
  - gl.runtime.api-version: "v1"
    header: "API-Version: v1"
```

### Tool Integration

### Version Management
```bash
# Bump version
npm version patch
npm version minor
npm version major

# Check version compatibility
semver check "^1.2.3" "1.2.4"

# Generate changelog
conventional-changelog -p angular -i CHANGELOG.md -s
```

### Migration Management
```python
# Python migration
def migrate(from_version, to_version):
    """Migrate database schema"""
    migrations = get_migrations(from_version, to_version)
    for migration in migrations:
        apply_migration(migration)
```

### Compliance Checklist

- [x] Semantic version naming follows SemVer 2.0.0
- [x] API version naming includes `-api-version` identifier
- [x] Schema version naming includes `-schema-version` identifier
- [x] Contract version naming includes `-contract-version` identifier
- [x] Database version naming includes `-migration-version` identifier
- [x] Release version naming includes `-release-version` identifier
- [x] Build version naming includes `-build-version` identifier
- [x] Compatibility version naming includes `-compatibility-version` identifier
- [x] Deprecation version naming includes `-deprecation-version` identifier
- [x] All versions follow SemVer 2.0.0
- [x] API versions follow standard formats
- [x] Database migrations are sequential
- [x] Breaking changes increment MAJOR version
- [x] Deprecated versions have removal dates
- [x] Version numbers are unique per component

### References

- SemVer 2.0.0: https://semver.org/
- API Versioning Best Practices: https://restfulapi.net/versioning/
- Database Migration: https://www.postgresql.org/docs/current/sql-createmigration.html
- Compatibility Semantics: https://github.com/npm/node-semver
- Naming Convention Principles: gl-prefix-principles-engineering.md
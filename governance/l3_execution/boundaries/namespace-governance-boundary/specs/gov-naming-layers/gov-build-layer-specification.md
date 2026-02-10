# GL Build Layer Specification

## Build Layer - 建置層

### Layer Overview

The Build Layer defines naming conventions for build resources including pipelines, stages, tasks, and artifacts. This layer ensures consistent build management across the platform, enabling effective build automation, artifact management, and build optimization.

### 1. Build Pipeline Naming

**Pattern**: `gl.build.pipeline`

**Format**: `gl.{project}.{type}-pipeline`

**Naming Rules**:
- Must use pipeline identifier: `-pipeline`
- Project identifies the build project
- Type identifies the pipeline type: `ci|cd|release|snapshot`

**Examples**:
```yaml
# Valid
gl.runtime.ci-pipeline
gl.data.cd-pipeline
gl.security.release-pipeline

# Invalid
ci-pipeline
runtime-pipeline
pipeline
```

**Purpose**: Build pipeline definitions

### 2. Build Stage Naming

**Pattern**: `gl.build.stage`

**Format**: `gl.{pipeline}.{phase}-stage`

**Naming Rules**:
- Must use stage identifier: `-stage`
- Pipeline identifies the build pipeline
- Phase identifies the build phase: `build|test|package|deploy`

**Examples**:
```yaml
# Valid
gl.runtime.build-stage
gl.data.test-stage
gl.security.deploy-stage

# Invalid
build-stage
runtime-stage
stage
```

**Purpose**: Build stage definitions

### 3. Build Task Naming

**Pattern**: `gl.build.task`

**Format**: `gl.{stage}.{action}-task`

**Naming Rules**:
- Must use task identifier: `-task`
- Stage identifies the build stage
- Action identifies the task action

**Examples**:
```yaml
# Valid
gl.runtime.compile-task
gl.data.unit-test-task
gl.security.package-task

# Invalid
compile-task
runtime-task
task
```

**Purpose**: Build task definitions

### 4. Build Artifact Naming

**Pattern**: `gl.build.artifact`

**Format**: `gl.{component}.{type}-artifact`

**Naming Rules**:
- Must use artifact identifier: `-artifact`
- Component identifies the built component
- Type identifies the artifact type: `binary|jar|war|docker|npm`

**Examples**:
```yaml
# Valid
gl.runtime.binary-artifact
gl.data.jar-artifact
gl.security.docker-artifact

# Invalid
binary-artifact
runtime-artifact
artifact
```

**Purpose**: Build artifact definitions

### 5. Build Configuration Naming

**Pattern**: `gl.build.config`

**Format**: `gl.{project}.{environment}-config`

**Naming Rules**:
- Must use config identifier: `-config`
- Project identifies the build project
- Environment identifies the build environment

**Examples**:
```yaml
# Valid
gl.runtime.prod-config
gl.data.staging-config
gl.security.dev-config

# Invalid
prod-config
runtime-config
config
```

**Purpose**: Build configuration definitions

### 6. Build Dependency Naming

**Pattern**: `gl.build.dependency`

**Format**: `gl.{component}.{type}-dependency`

**Naming Rules**:
- Must use dependency identifier: `-dependency`
- Component identifies the build component
- Type identifies the dependency type

**Examples**:
```yaml
# Valid
gl.runtime.library-dependency
gl.data.sdk-dependency
gl.security.tool-dependency

# Invalid
library-dependency
runtime-dependency
dependency
```

**Purpose**: Build dependency definitions

### 7. Build Cache Naming

**Pattern**: `gl.build.cache`

**Format**: `gl.{component}.{type}-cache`

**Naming Rules**:
- Must use cache identifier: `-cache`
- Component identifies the cached component
- Type identifies the cache type

**Examples**:
```yaml
# Valid
gl.runtime.maven-cache
gl.data.npm-cache
gl.security.docker-cache

# Invalid
maven-cache
runtime-cache
cache
```

**Purpose**: Build cache definitions

### 8. Build Environment Naming

**Pattern**: `gl.build.environment`

**Format**: `gl.{project}.{type}-environment`

**Naming Rules**:
- Must use environment identifier: `-environment`
- Project identifies the build project
- Type identifies the environment type

**Examples**:
```yaml
# Valid
gl.runtime.build-environment
gl.data.test-environment
gl.security.package-environment

# Invalid
build-environment
runtime-environment
environment
```

**Purpose**: Build environment definitions

### 9. Build Trigger Naming

**Pattern**: `gl.build.trigger`

**Format**: `gl.{pipeline}.{event}-trigger`

**Naming Rules**:
- Must use trigger identifier: `-trigger`
- Pipeline identifies the triggered pipeline
- Event identifies the trigger event

**Examples**:
```yaml
# Valid
gl.runtime.push-trigger
gl.data.pr-trigger
gl.security.schedule-trigger

# Invalid
push-trigger
runtime-trigger
trigger
```

**Purpose**: Build trigger definitions

### 10. Build Layer Integration

### Cross-Layer Dependencies
- **Depends on**: Testing Layer (for build tests)
- **Provides**: Build conventions
- **Works with**: CI/CD Layer for build automation
- **Works with**: Dependency Layer for build dependencies

### Naming Hierarchy
```
gl.build/
├── pipelines/
│   ├── gl.build.pipeline
│   └── gl.build.trigger
├── stages/
│   └── gl.build.stage
├── tasks/
│   └── gl.build.task
├── artifacts/
│   └── gl.build.artifact
├── configuration/
│   ├── gl.build.config
│   └── gl.build.dependency
├── caching/
│   └── gl.build.cache
└── environments/
    └── gl.build.environment
```

### Validation Rules

### Rule BL-001: Pipeline Naming Convention
- **Severity**: CRITICAL
- **Check**: Pipelines must follow `gl.{project}.{type}-pipeline` pattern
- **Pattern**: `^gl\..+\.ci|cd|release|snapshot-pipeline$`

### Rule BL-002: Stage Ordering
- **Severity**: HIGH
- **Check**: Build stages must be in correct order
- **Required**: build → test → package → deploy

### Rule BL-003: Artifact Versioning
- **Severity**: CRITICAL
- **Check**: Artifacts must be versioned
- **Required**: Version number in artifact name

### Rule BL-004: Cache Key Uniqueness
- **Severity**: HIGH
- **Check**: Cache keys must be unique
- **Required**: Component and type combination

### Rule BL-005: Environment Isolation
- **Severity**: HIGH
- **Check**: Build environments must be isolated
- **Required**: Separate containers or VMs

### Rule BL-006: Dependency Pinning
- **Severity**: MEDIUM
- **Check**: Build dependencies must be pinned
- **Required**: Exact version numbers

### Usage Examples

### Example 1: Complete Build Stack
```yaml
# Build Pipeline
apiVersion: gl.io/v1
kind: Pipeline
metadata:
  name: gl.runtime.ci-pipeline
spec:
  type: ci
  project: gl.runtime
  triggers:
  - gl.runtime.push-trigger
  - gl.runtime.pr-trigger
  stages:
  - gl.runtime.build-stage
  - gl.runtime.test-stage
  - gl.runtime.package-stage

# Build Stage
apiVersion: gl.io/v1
kind: Stage
metadata:
  name: gl.runtime.build-stage
spec:
  phase: build
  pipeline: gl.runtime.ci-pipeline
  tasks:
  - gl.runtime.compile-task
  - gl.runtime.lint-task
  cache:
  - gl.runtime.maven-cache

# Build Task
apiVersion: gl.io/v1
kind: Task
metadata:
  name: gl.runtime.compile-task
spec:
  action: compile
  stage: gl.runtime.build-stage
  script: |
    mvn clean compile
  timeout: 600s
  retries: 2
```

### Example 2: Artifacts and Configuration
```yaml
# Build Artifact
apiVersion: gl.io/v1
kind: Artifact
metadata:
  name: gl.runtime.binary-artifact
spec:
  type: binary
  component: gl.runtime
  version: "1.2.3"
  format: jar
  checksum: sha256:abc123...
  storage:
    type: s3
    path: s3://artifacts/gl/runtime/1.2.3/

# Build Configuration
apiVersion: gl.io/v1
kind: Config
metadata:
  name: gl.runtime.prod-config
spec:
  environment: prod
  project: gl.runtime
  variables:
    BUILD_NUMBER: "${BUILD_NUMBER}"
    DEPLOY_ENV: production
  secrets:
    - gl.runtime.creds-secret
```

### Example 3: Triggers and Dependencies
```yaml
# Build Trigger
apiVersion: gl.io/v1
kind: Trigger
metadata:
  name: gl.runtime.push-trigger
spec:
  event: push
  pipeline: gl.runtime.ci-pipeline
  branches:
  - main
  - develop
  filter: "**/*.java"

# Build Dependency
apiVersion: gl.io/v1
kind: Dependency
metadata:
  name: gl.runtime.library-dependency
spec:
  type: library
  component: gl.runtime
  name: spring-boot
  version: "2.7.0"
  scope: compile
  checksum: sha256:def456...
```

### Best Practices

### Pipeline Organization
```yaml
# Standard pipeline structure
pipelines:
  ci:
    - gl.runtime.ci-pipeline
    - gl.data.ci-pipeline
  cd:
    - gl.runtime.cd-pipeline
    - gl.data.cd-pipeline
  release:
    - gl.runtime.release-pipeline
    - gl.security.release-pipeline
```

### Build Stages
```yaml
# Typical build stages
stages:
  - gl.runtime.build-stage
  - gl.runtime.test-stage
  - gl.runtime.package-stage
  - gl.runtime.deploy-stage

# Each stage has multiple tasks
tasks:
  build-stage:
    - gl.runtime.compile-task
    - gl.runtime.lint-task
  test-stage:
    - gl.runtime.unit-test-task
    - gl.runtime.integration-test-task
```

### Tool Integration

### Build Execution
```bash
# Run pipeline
gl build pipeline gl.runtime.ci-pipeline

# Run specific stage
gl build stage gl.runtime.build-stage

# Run specific task
gl build task gl.runtime.compile-task
```

### Artifact Management
```python
# Python artifact management
def upload_artifact(artifact, storage):
    """Upload build artifact"""
    artifact_name = f"{artifact.component}-{artifact.version}.{artifact.format}"
    storage.upload(artifact_name, artifact.path)
    artifact.url = f"{storage.url}/{artifact_name}"
```

### Compliance Checklist

- [x] Pipeline naming follows `gl.{project}.{type}-pipeline` pattern
- [x] Stage naming includes `-stage` identifier
- [x] Task naming includes `-task` identifier
- [x] Artifact naming includes `-artifact` identifier
- [x] Config naming includes `-config` identifier
- [x] Dependency naming includes `-dependency` identifier
- [x] Cache naming includes `-cache` identifier
- [x] Environment naming includes `-environment` identifier
- [x] Trigger naming includes `-trigger` identifier
- [x] All pipelines follow naming conventions
- [x] Build stages are in correct order
- [x] Artifacts are versioned
- [x] Cache keys are unique
- [x] Build environments are isolated
- [x] Build dependencies are pinned

### References

- Build Best Practices: https://cloud.google.com/solutions/best-practices-for-continuous-deployment
- Artifact Management: https://docs.github.com/en/actions/guides/about-storing-artifacts
- Build Caching: https://docs.gradle.org/current/userguide/build_cache.html
- Naming Convention Principles: gov-prefix-principles-engineering.md
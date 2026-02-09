# GL Packaging Layer Specification

## Layer Overview

The GL Packaging Layer defines naming conventions for all packaging and distribution artifacts in a large-scale monorepo multi-platform architecture. This layer covers containers, archives, installers, and distribution packages across different platforms and environments.

**Layer ID**: L21-Packaging  
**Priority**: LOW  
**Scope**: Packaging artifacts, distributions, installers, and deployment units

---

## Resource Naming Patterns

### 1. Container Images

**Pattern**: `gl.pkg.image-{service}-{variant}-{version}`

**Examples**:
- `gl.pkg.image-user-service-alpine-1.0.0` - User service Alpine image
- `gl.pkg.image-api-gateway-debian-2.0.0` - API gateway Debian image
- `gl.pkg.image-auth-service-scratch-1.0.0` - Auth service scratch image

**Validation**:
- Service name must match actual service
- Variant must be valid (alpine, debian, scratch, slim)
- Version must follow semantic versioning
- Must include architecture metadata

### 2. Helm Charts

**Pattern**: `gl.pkg.chart-{component}-{version}`

**Examples**:
- `gl.pkg.chart-platform-core-1.0.0` - Platform core Helm chart
- `gl.pkg.chart-user-service-2.0.0` - User service Helm chart
- `gl.pkg.chart-auth-service-1.0.0` - Auth service Helm chart

**Validation**:
- Component name must match actual component
- Version must follow semantic versioning
- Must include values schema
- Must include README

### 3. Docker Compose Files

**Pattern**: `gl.pkg.compose-{environment}-{scope}-{version}`

**Examples**:
- `gl.pkg.compose-development-full-1.0.0` - Full development stack
- `gl.pkg.compose-staging-minimal-2.0.0` - Minimal staging stack
- `gl.pkg.compose-production-full-1.0.0` - Full production stack

**Validation**:
- Environment must be valid (development, staging, production)
- Scope must be valid (minimal, full, custom)
- Version must be tracked
- Must include service definitions

### 4. Kubernetes Manifests

**Pattern**: `gl.pkg.k8s-{component}-{type}-{version}`

**Examples**:
- `gl.pkg.k8s-platform-core-deployment-1.0.0` - Platform core deployment
- `gl.pkg.k8s-user-service-service-2.0.0` - User service service
- `gl.pkg.k8s-auth-service-configmap-1.0.0` - Auth service configmap

**Validation**:
- Component must be valid
- Type must be valid (deployment, service, configmap, ingress)
- Version must match application version
- Must include namespace

### 5. Terraform Modules

**Pattern**: `gl.pkg.terraform-{provider}-{module}-{version}`

**Examples**:
- `gl.pkg.terraform-aws-vpc-1.0.0` - AWS VPC module
- `gl.pkg.terraform-gcp-storage-2.0.0` - GCP storage module
- `gl.pkg.terraform-azure-network-1.0.0` - Azure network module

**Validation**:
- Provider must be valid (aws, gcp, azure, kubernetes)
- Module name must be descriptive
- Version must follow semantic versioning
- Must include outputs

### 6. Software Installers

**Pattern**: `gl.pkg.installer-{application}-{platform}-{version}`

**Examples**:
- `gl.pkg.installer-cli-tool-linux-1.0.0` - Linux CLI installer
- `gl.pkg.installer-desktop-app-macos-2.0.0` - macOS desktop installer
- `gl.pkg.installer-service-windows-1.0.0` - Windows service installer

**Validation**:
- Application name must be valid
- Platform must be valid (linux, macos, windows)
- Version must follow semantic versioning
- Must include checksum

### 7. Distribution Archives

**Pattern**: `gl.pkg.archive-{package}-{format}-{version}`

**Examples**:
- `gl.pkg.archive-platform-core-tar-1.0.0` - Platform core tarball
- `gl.pkg.archive-user-service-zip-2.0.0` - User service zip archive
- `gl.pkg.archive-auth-service-gz-1.0.0` - Auth service gz archive

**Validation**:
- Package name must match actual package
- Format must be valid (tar, zip, gz, bz2)
- Version must follow semantic versioning
- Must include manifest

### 8. Package Repositories

**Pattern**: `gl.pkg.repo-{type}-{channel}-{version}`

**Examples**:
- `gl.pkg.repo-npm-stable-1.0.0` - NPM stable repository
- `gl.pkg.repo-pypi-production-2.0.0` - PyPI production repository
- `gl.pkg.repo-maven-release-1.0.0` - Maven release repository

**Validation**:
- Type must be valid (npm, pypi, maven, docker, helm)
- Channel must be valid (stable, beta, alpha, production)
- Version must be tracked
- Must include repository metadata

### 9. Configuration Packages

**Pattern**: `gl.pkg.config-{service}-{environment}-{version}`

**Examples**:
- `gl.pkg.config-user-service-development-1.0.0` - Development config
- `gl.pkg.config-api-gateway-staging-2.0.0` - Staging config
- `gl.pkg.config-auth-service-production-1.0.0` - Production config

**Validation**:
- Service must be valid
- Environment must be valid
- Version must match application version
- Must include validation schema

### 10. Deployment Bundles

**Pattern**: `gl.pkg.bundle-{platform}-{scope}-{version}`

**Examples**:
- `gl.pkg.bundle-kubernetes-full-1.0.0` - Full K8s bundle
- `gl.pkg.bundle-docker-compose-minimal-2.0.0` - Minimal Docker Compose bundle
- `gl.pkg.bundle-terraform-production-1.0.0` - Production Terraform bundle

**Validation**:
- Platform must be valid (kubernetes, docker-compose, terraform)
- Scope must be valid (minimal, full, custom)
- Version must be consistent across components
- Must include deployment manifest

---

## Validation Rules

### GL-PKG-001: Container Image Standards
**Severity**: HIGH  
**Rule**: Container images must follow best practices  
**Implementation**:
```yaml
image_standards:
  base_images:
    - Prefer minimal base images
    - Use official base images
    - Pin base image versions
  security:
    - Scan images for vulnerabilities
    - Run as non-root user
    - Minimize attack surface
  metadata:
    - Include labels
    - Document entrypoints
    - Specify health checks
```

### GL-PKG-002: Helm Chart Structure
**Severity**: MEDIUM  
**Rule**: Helm charts must follow standardized structure  
**Implementation**:
```yaml
chart_structure:
  required_files:
    - Chart.yaml
    - values.yaml
    - README.md
    - templates/deployment.yaml
    - templates/service.yaml
  optional_files:
    - values.schema.json
    - templates/_helpers.tpl
    - templates/NOTES.txt
```

### GL-PKG-003: Kubernetes Manifest Standards
**Severity**: HIGH  
**Rule**: K8s manifests must follow conventions  
**Implementation**:
- Use resource limits
- Include liveness and readiness probes
- Use standard labels and annotations
- Specify security contexts

### GL-PKG-004: Terraform Module Standards
**Severity**: MEDIUM  
**Rule**: Terraform modules must be reusable and documented  
**Implementation**:
- Include README with examples
- Use consistent variable naming
- Define outputs
- Document dependencies

### GL-PKG-005: Package Versioning
**Severity**: HIGH  
**Rule**: All packages must use semantic versioning  
**Implementation**:
```yaml
versioning:
  scheme: semantic
  format: MAJOR.MINOR.PATCH
  pre_release: [alpha, beta, rc]
  build_metadata: supported
  compatibility:
    - Major breaking changes
    - Minor new features
    - Patch bug fixes
```

### GL-PKG-006: Package Security
**Severity**: CRITICAL  
**Rule**: All packages must be security-scanned  
**Implementation**:
- Scan containers for vulnerabilities
- Verify package signatures
- Check dependency licenses
- Validate configuration

### GL-PKG-007: Package Metadata
**Severity**: MEDIUM  
**Rule**: All packages must include comprehensive metadata  
**Implementation**:
- Description and purpose
- Dependencies and requirements
- Installation instructions
- Usage examples
- Changelog

---

## Usage Examples

### Complete Packaging Stack
```yaml
platform-core/
  packages/
    containers/
      gl.pkg.image-user-service-alpine-1.0.0.tar
      gl.pkg.image-api-gateway-debian-2.0.0.tar
    helm/
      gl.pkg.chart-platform-core-1.0.0.tgz
      gl.pkg.chart-user-service-2.0.0.tgz
    docker-compose/
      gl.pkg.compose-development-full-1.0.0.yml
      gl.pkg.compose-staging-minimal-2.0.0.yml
    kubernetes/
      gl.pkg.k8s-platform-core-deployment-1.0.0.yaml
      gl.pkg.k8s-user-service-service-2.0.0.yaml
    terraform/
      gl.pkg.terraform-aws-vpc-1.0.0.tf
      gl.pkg.terraform-gcp-storage-2.0.0.tf
    installers/
      gl.pkg.installer-cli-tool-linux-1.0.0.run
      gl.pkg.installer-desktop-app-macos-2.0.0.pkg
    archives/
      gl.pkg.archive-platform-core-tar-1.0.0.tar.gz
      gl.pkg.archive-user-service-zip-2.0.0.zip
    config/
      gl.pkg.config-user-service-development-1.0.0.yaml
      gl.pkg.config-api-gateway-staging-2.0.0.yaml
    bundles/
      gl.pkg.bundle-kubernetes-full-1.0.0.tar
      gl.pkg.bundle-docker-compose-minimal-2.0.0.tar
```

### Container Image Manifest
```dockerfile
# gl.pkg.image-user-service-alpine-1.0.0
FROM alpine:3.19

LABEL name="gl.pkg.image-user-service-alpine-1.0.0"
LABEL version="1.0.0"
LABEL description="User service for platform core"
LABEL maintainer="team@platform.com"

RUN apk add --no-cache python3

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/

WORKDIR /app

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

CMD ["python", "app.py"]
```

### Helm Chart Structure
```yaml
# gl.pkg.chart-user-service-2.0.0/Chart.yaml
apiVersion: v2
name: gl.pkg.chart-user-service-2.0.0
description: User service Helm chart
type: application
version: 2.0.0
appVersion: 2.0.0
maintainers:
  - name: Platform Team
    email: team@platform.com
```

---

## Best Practices

### 1. Multi-Stage Builds
- Use multi-stage Docker builds
- Minimize final image size
- Separate build and runtime dependencies
- Optimize layer caching

### 2. Immutable Tags
- Use immutable image tags
- Never use 'latest' tag
- Pin all dependency versions
- Document upgrade paths

### 3. Security First
- Scan all images before deployment
- Use minimal base images
- Run as non-root user
- Enable security features

### 4. Configuration Management
- Externalize configuration
- Use environment variables
- Provide default values
- Document configuration options

### 5. Reproducible Builds
- Use deterministic builds
- Pin base image digests
- Document build environment
- Verify reproducibility

---

## Tool Integration Examples

### Building Container Images
```bash
# Build container image
docker build \
  -t gl.pkg.image-user-service-alpine-1.0.0 \
  --build-arg VERSION=1.0.0 \
  --build-arg VARIANT=alpine \
  -f Dockerfile \
  .

# Tag and push
docker tag gl.pkg.image-user-service-alpine-1.0.0 \
  registry.example.com/gl.pkg.image-user-service-alpine-1.0.0

docker push registry.example.com/gl.pkg.image-user-service-alpine-1.0.0
```

### Packaging Helm Charts
```bash
# Package Helm chart
helm package \
  user-service/ \
  --version 2.0.0 \
  --app-version 2.0.0 \
  --destination dist/ \
  --dependency-update

# Output: gl.pkg.chart-user-service-2.0.0.tgz

# Push to registry
helm push gl.pkg.chart-user-service-2.0.0.tgz \
  oci://registry.example.com/charts
```

### Creating Deployment Bundles
```bash
# Create deployment bundle
tar -czf gl.pkg.bundle-kubernetes-full-1.0.0.tar \
  -C packages/kubernetes/ \
  gl.pkg.k8s-platform-core-deployment-1.0.0.yaml \
  gl.pkg.k8s-user-service-service-2.0.0.yaml \
  gl.pkg.k8s-auth-service-configmap-1.0.0.yaml

# Create manifest
cat > gl.pkg.bundle-kubernetes-full-1.0.0.manifest.yaml <<EOF
name: gl.pkg.bundle-kubernetes-full-1.0.0
version: 1.0.0
platform: kubernetes
scope: full
components:
  - gl.pkg.k8s-platform-core-deployment-1.0.0.yaml
  - gl.pkg.k8s-user-service-service-2.0.0.yaml
  - gl.pkg.k8s-auth-service-configmap-1.0.0.yaml
checksum: $(sha256sum gl.pkg.bundle-kubernetes-full-1.0.0.tar | cut -d' ' -f1)
EOF
```

### Scanning Images
```bash
# Scan with Trivy
trivy image \
  --severity HIGH,CRITICAL \
  --format json \
  --output gl.sc.vuln-user-service-trivy-20240120.json \
  gl.pkg.image-user-service-alpine-1.0.0

# Scan with Grype
grype gl.pkg.image-user-service-alpine-1.0.0 \
  --output json \
  --file gl.sc.vuln-user-service-grype-20240120.json
```

---

## Compliance Checklist

For each packaging artifact, verify:

- [ ] File name follows GL naming convention
- [ ] Version follows semantic versioning
- [ ] Security scan completed
- [ ] Documentation included
- [ ] Configuration externalized
- [ ] Metadata complete
- [ ] Checksums provided
- [ ] Installation tested
- [ ] Upgrade path documented
- [ ] Compatible with target platform

---

## References

- Docker Best Practices: https://docs.docker.com/develop/dev-best-practices/
- Helm Best Practices: https://helm.sh/docs/chart_best_practices/
- Kubernetes Conventions: https://kubernetes.io/docs/concepts/configuration/overview/
- Terraform Best Practices: https://www.terraform-best-practices.com/
- OCI Artifacts: https://opencontainers.org/

---

**Version**: 1.0.0  
**Last Updated**: 2024-01-20  
**Maintained By**: Packaging & Deployment Team
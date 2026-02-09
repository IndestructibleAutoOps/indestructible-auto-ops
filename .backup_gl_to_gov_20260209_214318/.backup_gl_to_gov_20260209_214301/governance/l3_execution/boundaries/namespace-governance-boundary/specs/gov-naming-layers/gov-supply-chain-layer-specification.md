# GL Supply Chain Layer Specification

## Layer Overview

The GL Supply Chain Layer defines naming conventions for software supply chain components, including artifacts, SBOMs (Software Bill of Materials), provenance records, and integrity verification. This layer is critical for security, compliance, and auditability in large-scale monorepo multi-platform architectures.

**Layer ID**: L20-SupplyChain  
**Priority**: LOW  
**Scope**: Supply chain artifacts, provenance, SBOMs, and security attestations

---

## Resource Naming Patterns

### 1. Software Bill of Materials (SBOM)

**Pattern**: `gl.sc.sbom-{component}-{format}-{version}`

**Examples**:
- `gl.sc.sbom-platform-core-spdx-1.0.0` - Platform core SBOM in SPDX format
- `gl.sc.sbom-user-service-cyclonedx-2.0.0` - User service SBOM in CycloneDX format
- `gl.sc.sbom-auth-library-spdx-1.0.0` - Auth library SBOM in SPDX format

**Validation**:
- Component name must match actual component
- Format must be valid (spdx, cyclonedx)
- Version must match component version
- Must include dependency tree

### 2. Build Attestations

**Pattern**: `gl.sc.attestation-{component}-{type}-{digest}`

**Examples**:
- `gl.sc.attestation-platform-core-build-sha256abc123` - Platform core build attestation
- `gl.sc.attestation-api-gateway-deploy-sha256def456` - API gateway deployment attestation
- `gl.sc.attestation-auth-service-release-sha256ghi789` - Auth service release attestation

**Validation**:
- Digest must be SHA256 or stronger
- Type must be valid (build, deploy, release)
- Must include signer information
- Must be verifiable

### 3. Provenance Records

**Pattern**: `gl.sc.provenance-{artifact}-{source}-{timestamp}`

**Examples**:
- `gl.sc.provenance-platform-core-git-20240120` - Platform core Git provenance
- `gl.sc.provenance-user-service-registry-20240120` - User service registry provenance
- `gl.sc.provenance-auth-library-vcs-20240120` - Auth library VCS provenance

**Validation**:
- Timestamp must be ISO 8601 format
- Source must be valid (git, registry, vcs)
- Must include commit SHA
- Must include build environment

### 4. Vulnerability Reports

**Pattern**: `gl.sc.vuln-{component}-{scanner}-{date}`

**Examples**:
- `gl.sc.vuln-platform-core-trivy-20240120` - Trivy vulnerability report
- `gl.sc.vuln-user-service-snyk-20240120` - Snyk vulnerability report
- `gl.sc.vuln-auth-library-grype-20240120` - Grype vulnerability report

**Validation**:
- Date must be YYYYMMDD format
- Scanner must be valid (trivy, snyk, grype)
- Must include severity levels
- Must include CVE references

### 5. Dependency Source Locks

**Pattern**: `gl.sc.lock-{package-manager}-{component}-{version}`

**Examples**:
- `gl.sc.lock-npm-platform-core-1.0.0` - NPM lock file
- `gl.sc.lock-pip-user-service-2.0.0` - Python lock file
- `gl.sc.lock-go-mod-auth-library-1.0.0` - Go module lock file

**Validation**:
- Package manager must be valid
- Component name must match
- Version must be consistent
- Must include checksums

### 6. Container Image Signatures

**Pattern**: `gl.sc.signature-{image}-{signer}-{digest}`

**Examples**:
- `gl.sc.signature-platform-core-cosign-sha256abc123` - Cosign signature
- `gl.sc.signature-user-service-fulcio-sha256def456` - Fulcio signature
- `gl.sc.signature-auth-service-notary-sha256ghi789` - Notary signature

**Validation**:
- Signer must be valid (cosign, fulcio, notary)
- Digest must match image digest
- Signature must be verifiable
- Must include certificate chain

### 7. License Inventory

**Pattern**: `gl.sc.license-{component}-{scope}-{date}`

**Examples**:
- `gl.sc.license-platform-core-transitive-20240120` - Transitive license inventory
- `gl.sc.license-user-service-direct-20240120` - Direct license inventory
- `gl.sc.license-auth-library-all-20240120` - Complete license inventory

**Validation**:
- Scope must be valid (direct, transitive, all)
- Must include license types
- Must include compliance status
- Must include policy violations if any

### 8. Supply Chain Policy

**Pattern**: `gl.sc.policy-{domain}-{name}-{version}`

**Examples**:
- `gl.sc.policy-security-slsa-v1.0` - SLSA security policy
- `gl.sc.policy-compliance-cis-v1.1` - CIS compliance policy
- `gl.sc.policy-approval-gate-v1.0` - Approval gate policy

**Validation**:
- Domain must be valid (security, compliance, approval)
- Name must be descriptive
- Version must follow semantic versioning
- Must include policy rules

### 9. Artifact Metadata

**Pattern**: `gl.sc.metadata-{artifact}-{type}-{version}`

**Examples**:
- `gl.sc.metadata-platform-core-build-1.0.0` - Build metadata
- `gl.sc.metadata-user-service-deploy-2.0.0` - Deployment metadata
- `gl.sc.metadata-auth-library-package-1.0.0` - Package metadata

**Validation**:
- Type must be valid (build, deploy, package)
- Must include build environment
- Must include runtime requirements
- Must be immutable

### 10. Integrity Verification

**Pattern**: `gl.sc.verify-{component}-{check}-{status}`

**Examples**:
- `gl.sc.verify-platform-core-signature-passed` - Signature verification passed
- `gl.sc.verify-user-service-sbom-failed` - SBOM verification failed
- `gl.sc.verify-auth-service-provenance-passed` - Provenance verification passed

**Validation**:
- Check type must be valid (signature, sbom, provenance)
- Status must be valid (passed, failed, warning)
- Must include verification details
- Must be timestamped

---

## Validation Rules

### GL-SC-001: SBOM Completeness
**Severity**: CRITICAL  
**Rule**: All production artifacts must have complete SBOMs  
**Implementation**:
```yaml
sbom_requirements:
  - Direct dependencies
  - Transitive dependencies
  - Build tools and libraries
  - Runtime dependencies
  - License information
  - Vulnerability data
```

### GL-SC-002: Attestation Verification
**Severity**: CRITICAL  
**Rule**: All attestations must be verifiable and signed  
**Implementation**:
- Use cryptographically secure signatures
- Include signer identity
- Verify signature chain
- Check certificate validity

### GL-SC-003: Provenance Integrity
**Severity**: HIGH  
**Rule**: Provenance records must be immutable and traceable  
**Implementation**:
- Store in immutable storage
- Include complete build environment
- Record all materials and inputs
- Link to source commits

### GL-SC-004: Vulnerability Scanning
**Severity**: HIGH  
**Rule**: All artifacts must undergo vulnerability scanning  
**Implementation**:
- Scan before deployment
- Include dependency scanning
- Check CVE databases
- Generate severity reports

### GL-SC-005: License Compliance
**Severity**: HIGH  
**Rule**: All dependencies must have valid license information  
**Implementation**:
- Track all licenses
- Check policy compliance
- Flag license conflicts
- Maintain license inventory

### GL-SC-006: Supply Chain Policy Enforcement
**Severity**: CRITICAL  
**Rule**: Supply chain policies must be enforced at gates  
**Implementation**:
```yaml
gates:
  - build: Require SBOM and attestation
  - deploy: Require signature verification
  - release: Require vulnerability scan
  - promotion: Require policy approval
```

### GL-SC-007: Integrity Verification
**Severity**: HIGH  
**Rule**: All artifacts must undergo integrity verification  
**Implementation**:
- Verify cryptographic signatures
- Check checksums
- Validate provenance
- Confirm artifact authenticity

---

## Usage Examples

### Complete Supply Chain Stack
```yaml
platform-core/
  supply-chain/
    sboms/
      gl.sc.sbom-platform-core-spdx-1.0.0.json
      gl.sc.sbom-platform-core-cyclonedx-1.0.0.json
    attestations/
      gl.sc.attestation-platform-core-build-sha256abc123.sig
      gl.sc.attestation-platform-core-deploy-sha256def456.sig
    provenance/
      gl.sc.provenance-platform-core-git-20240120.json
    vulnerabilities/
      gl.sc.vuln-platform-core-trivy-20240120.json
    locks/
      gl.sc.lock-npm-platform-core-1.0.0.json
      gl.sc.lock-pip-platform-core-1.0.0.txt
    signatures/
      gl.sc.signature-platform-core-cosign-sha256abc123.sig
    licenses/
      gl.sc.license-platform-core-transitive-20240120.csv
    policies/
      gl.sc.policy-security-slsa-v1.0.yaml
    metadata/
      gl.sc.metadata-platform-core-build-1.0.0.json
    verification/
      gl.sc.verify-platform-core-signature-passed.json
```

### Individual SBOM File
```json
{
  "bomFormat": "SPDX",
  "specVersion": "2.3",
  "name": "gl.sc.sbom-platform-core-spdx-1.0.0",
  "version": "1.0.0",
  "components": [
    {
      "name": "platform-core",
      "version": "1.0.0",
      "licenses": [{
        "license": {"id": "Apache-2.0"}
      }],
      "externalReferences": [
        {
          "type": "purl",
          "url": "pkg:docker/platform-core@1.0.0"
        }
      ]
    }
  ]
}
```

---

## Best Practices

### 1. Generate SBOMs Automatically
- Integrate SBOM generation into build pipeline
- Use multiple formats (SPDX, CycloneDX)
- Store SBOMs with artifacts
- Make SBOMs publicly available when possible

### 2. Sign All Artifacts
- Use code signing for all release artifacts
- Include signature verification in deployment
- Use trusted signing infrastructure
- Rotate signing keys regularly

### 3. Track Provenance
- Record complete build environment
- Link to source code commits
- Document build parameters
- Maintain immutable provenance records

### 4. Scan for Vulnerabilities
- Scan at multiple stages (build, test, deploy)
- Use multiple scanners for coverage
- Automate vulnerability response
- Maintain vulnerability inventory

### 5. Enforce Policies
- Define clear supply chain policies
- Implement policy as code
- Block non-compliant artifacts
- Audit policy violations

---

## Tool Integration Examples

### SBOM Generation
```bash
# Generate SPDX SBOM
syft platform-core:1.0.0 \
  --output spdx-json \
  --file gl.sc.sbom-platform-core-spdx-1.0.0.json

# Generate CycloneDX SBOM
cyclonedx-bom \
  --input-type docker \
  --input platform-core:1.0.0 \
  --output-file gl.sc.sbom-platform-core-cyclonedx-1.0.0.json
```

### Artifact Signing
```bash
# Sign container image with Cosign
cosign sign \
  platform-core:1.0.0 \
  --output-signature gl.sc.signature-platform-core-cosign-sha256abc123.sig

# Verify signature
cosign verify \
  platform-core:1.0.0 \
  --signature gl.sc.signature-platform-core-cosign-sha256abc123.sig
```

### Vulnerability Scanning
```bash
# Scan with Trivy
trivy image \
  --format json \
  --output gl.sc.vuln-platform-core-trivy-20240120.json \
  platform-core:1.0.0

# Scan with Grype
grype platform-core:1.0.0 \
  --output json \
  --file gl.sc.vuln-platform-core-grype-20240120.json
```

### Provenance Generation
```bash
# Generate SLSA provenance
slsa-provenance generate \
  --source-uri github.com/org/platform-core \
  --builder-image ghcr.io/slsa-framework/slsa-github-generator-generators \
  --output gl.sc.provenance-platform-core-git-20240120.json
```

---

## Compliance Checklist

For each supply chain artifact, verify:

- [ ] File name follows GL naming convention
- [ ] SBOM is complete and accurate
- [ ] Artifact is cryptographically signed
- [ ] Signature is verifiable
- [ ] Provenance is recorded
- [ ] Vulnerability scan completed
- [ ] License inventory maintained
- [ ] Policy compliance verified
- [ ] Integrity check passed
- [ ] Stored in immutable storage

---

## References

- SPDX: https://spdx.dev/
- CycloneDX: https://cyclonedx.org/
- SLSA: https://slsa.dev/
- Cosign: https://github.com/sigstore/cosign
- Trivy: https://github.com/aquasecurity/trivy
- Syft: https://github.com/anchore/syft
- Grype: https://github.com/anchore/grype

---

**Version**: 1.0.0  
**Last Updated**: 2024-01-20  
**Maintained By**: Security & Supply Chain Team
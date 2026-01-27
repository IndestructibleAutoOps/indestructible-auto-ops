# Supply Chain Security Implementation Guide

## Overview

This document describes the supply chain security implementation for MachineNativeOps, including SBOM generation, SLSA provenance, artifact signing, and vulnerability scanning.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Supply Chain Pipeline                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   Code Commit   │
                    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  SBOM Generation│  (syft)
                    │  (SPDX/CycloneDX)│
                    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Provenance     │  (SLSA Level 3)
                    │  Generation     │  (slsa-github-generator)
                    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Artifact       │  (Cosign + OIDC)
                    │  Signing        │
                    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Rekor Upload   │  (Transparency Log)
                    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Vulnerability  │  (Trivy)
                    │  Scanning       │
                    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Compliance     │
                    │  Verification   │
                    └─────────────────┘
```

## Components

### 1. SBOM Generation (syft)

**Purpose:** Generate Software Bill of Materials for all artifacts

**Formats:**
- SPDX JSON
- CycloneDX JSON
- SPDX Tag-Value

**Usage:**
```bash
workspace/tools/generate-sbom.sh
```

**Output:**
- `workspace/artifacts/sbom/sbom-spdx.json`
- `workspace/artifacts/sbom/sbom-cyclonedx.json`
- `workspace/artifacts/sbom/sbom-spdx.txt`

### 2. SLSA Provenance (slsa-github-generator)

**Purpose:** Generate SLSA Level 3 provenance attestations

**Level:** SLSA Level 3

**Information Captured:**
- Build inputs (source code, dependencies)
- Build environment
- Build parameters
- Builder identity

**Usage:**
```bash
generator \
  --artifact-path workspace/artifacts/ \
  --output-path workspace/artifacts/provenance/ \
  --digest sha256 \
  --context github
```

**Output:**
- `workspace/artifacts/provenance/provenance.json`

### 3. Artifact Signing (Cosign)

**Purpose:** Sign artifacts with OIDC-based identity

**Features:**
- Keyless signing (no private keys to manage)
- OIDC identity verification
- Certificate generation
- Signature generation

**Usage:**
```bash
cosign sign-blob \
  --yes \
  --output-certificate workspace/artifacts/signatures/sbom-cert.pem \
  --output-signature workspace/artifacts/signatures/sbom-sig.sig \
  workspace/artifacts/sbom/sbom-spdx.json
```

**Output:**
- `workspace/artifacts/signatures/sbom-cert.pem`
- `workspace/artifacts/signatures/sbom-sig.sig`

### 4. Rekor Transparency Log

**Purpose:** Upload signatures to immutable transparency log

**Benefits:**
- Immutable record of signatures
- Auditable signature history
- Public verification

**Usage:**
```bash
cosign upload-tlog \
  --bundle workspace/artifacts/rekor/sbom-bundle.json \
  workspace/artifacts/signatures/sbom-cert.pem
```

**Output:**
- `workspace/artifacts/rekor/sbom-bundle.json`

### 5. Vulnerability Scanning (Trivy)

**Purpose:** Scan artifacts for security vulnerabilities

**Capabilities:**
- OS package scanning
- Library dependency scanning
- Container image scanning
- SBOM-based scanning

**Usage:**
```bash
workspace/tools/scan-vulnerabilities.sh
```

**Output:**
- `workspace/artifacts/security/vulnerability-scan.json`
- `workspace/artifacts/security/vulnerability-report.txt`

## CI/CD Integration

### GitHub Actions Workflow

The supply chain security pipeline is integrated into `.github/workflows/supply-chain-security.yml` with the following jobs:

1. **sbom-generation** - Generate SBOM with syft
2. **provenance-generation** - Generate SLSA provenance
3. **artifact-signing** - Sign artifacts with Cosign
4. **rekor-upload** - Upload to Rekor transparency log
5. **vulnerability-scanning** - Scan for vulnerabilities
6. **compliance-check** - Verify compliance and generate reports

### Workflow Triggers

- Push to main/develop branches
- Pull requests to main branch
- Manual workflow dispatch

## Setup Instructions

### 1. Install Tools

Run the setup script:
```bash
./scripts/supply-chain-tools-setup.sh
```

This will install:
- syft (SBOM generation)
- trivy (vulnerability scanning)
- cosign (artifact signing)
- opa (policy engine)

### 2. Verify Installation

Test all tools:
```bash
workspace/tools/test-supply-chain.sh
```

### 3. Configure GitHub Secrets

Configure the following repository secrets:

- `COSIGN_EXPERIMENTAL` - Set to `1` for keyless signing
- `SLSA_GENERATOR_VERSION` - Specify generator version (optional)

### 4. Enable Workflow Permissions

Ensure the workflow has the following permissions:
```yaml
permissions:
  contents: read
  security-events: write
  id-token: write
```

## Usage Examples

### Generate SBOM

```bash
# Generate SBOM for current directory
workspace/tools/generate-sbom.sh

# Generate SBOM for specific directory
syft /path/to/code -o spdx-json > sbom.json
```

### Scan for Vulnerabilities

```bash
# Scan SBOM
workspace/tools/scan-vulnerabilities.sh

# Scan container image
trivy image my-image:latest

# Scan filesystem
trivy fs /path/to/code
```

### Sign Artifacts

```bash
# Sign SBOM
workspace/tools/sign-artifacts.sh

# Sign specific file
cosign sign-blob --yes my-file.json
```

### Verify Signatures

```bash
# Verify SBOM signature
cosign verify-blob \
  --certificate workspace/artifacts/signatures/sbom-cert.pem \
  --signature workspace/artifacts/signatures/sbom-sig.sig \
  workspace/artifacts/sbom/sbom-spdx.json

# Verify against transparency log
cosign verify-blob \
  --certificate-identity "https://github.com/MachineNativeOps/machine-native-ops/.github/workflows/supply-chain-security.yml@refs/heads/main" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
  workspace/artifacts/sbom/sbom-spdx.json
```

## Compliance Standards

### SLSA (Supply-chain Levels for Software Artifacts)

**Level:** 3

**Requirements Met:**
- ✅ Source control provenance
- ✅ Build environment provenance
- ✅ Dependency provenance
- ✅ Isolated build environment
- ✅ Hermetic builds

### SBOM Standards

**Formats:**
- ✅ SPDX 2.3
- ✅ CycloneDX 1.4

**Fields Included:**
- Package name and version
- License information
- Supplier information
- Dependency relationships
- Hashes and identifiers

### Artifact Signing

**Method:** Cosign (OIDC-based)

**Features:**
- ✅ Keyless signing
- ✅ Certificate-based identity
- ✅ Transparency log integration
- ✅ Timestamp verification

## Security Best Practices

### 1. Regular Scanning

- Scan on every commit
- Scan on pull requests
- Schedule periodic scans

### 2. Vulnerability Management

- Review and remediate critical vulnerabilities within 24 hours
- Review and remediate high vulnerabilities within 7 days
- Track vulnerability remediation in issue tracker

### 3. Artifact Verification

- Verify signatures before deployment
- Check provenance before deployment
- Validate SBOM completeness

### 4. Transparency

- Upload all signatures to Rekor
- Maintain public transparency log
- Enable public verification

## Troubleshooting

### Common Issues

**Issue:** SBOM generation fails
- **Solution:** Check file permissions and disk space

**Issue:** Vulnerability scan fails
- **Solution:** Ensure SBOM exists and is valid JSON

**Issue:** Cosign signing fails
- **Solution:** Verify OIDC identity and permissions

**Issue:** Rekor upload fails
- **Solution:** Check network connectivity and Rekor service status

### Debug Mode

Enable debug output:
```bash
export COSIGN_LOG_LEVEL=debug
export TRIVY_LOG_LEVEL=debug
export SYFT_LOG_LEVEL=debug
```

## Monitoring and Metrics

### Key Metrics

- SBOM generation success rate
- Vulnerability scan duration
- Signature verification success rate
- Compliance pass rate
- False positive rate

### Alerts

Configure alerts for:
- Critical vulnerabilities
- SBOM generation failures
- Signature verification failures
- Compliance violations

## Future Enhancements

### Planned Features

- [ ] Integration with dependency update automation
- [ ] Automated vulnerability remediation suggestions
- [ ] SBOM dependency graph visualization
- [ ] Real-time compliance monitoring
- [ ] Integration with security advisory databases

### Roadmap

**Q1 2025:**
- Enhanced vulnerability scanning
- Dependency risk scoring
- Automated SBOM updates

**Q2 2025:**
- Real-time compliance dashboard
- Integration with security advisory feeds
- Automated remediation workflows

## References

- [SLSA Specification](https://slsa.dev/)
- [SPDX Specification](https://spdx.dev/)
- [CycloneDX Specification](https://cyclonedx.org/)
- [Cosign Documentation](https://docs.sigstore.dev/cosign/)
- [Syft Documentation](https://github.com/anchore/syft)
- [Trivy Documentation](https://aquasecurity.github.io/trivy/)

## Support

For issues or questions:
- Review this documentation
- Check GitHub Issues
- Contact the MachineNativeOps team
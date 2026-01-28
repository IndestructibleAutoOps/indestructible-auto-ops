# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: federation-signing-keys-documentation
# @GL-charter-version: 2.0.0

# Federation Signing Keys Documentation

## Overview

This document describes the signing key management for the GL Federation Layer. All governance operations across organizations require cryptographic signing to ensure authenticity, integrity, and non-repudiation.

## Key Types

### 1. Primary Signing Keys

Primary signing keys are used for the most critical operations:
- Patch signing
- Deployment signing
- PR signing
- Cross-organization approvals

**Format**: ECDSA P-256  
**Storage**: Hardware Security Module (HSM) or KMS  
**Rotation**: Every 90 days

### 2. Backup Signing Keys

Backup keys provide redundancy and disaster recovery:
- Secondary verification
- Emergency operations
- Key recovery

**Format**: ECDSA P-256  
**Storage**: Encrypted at rest in key vault  
**Rotation**: Every 180 days

### 3. Organization-Level Keys

Each organization has its own key pair:
- Internal operations signing
- Artifact verification
- Cross-org communication

**Format**: ECDSA P-256  
**Storage**: Organization's KMS  
**Rotation**: Every 120 days

## Key Management Process

### Key Generation

1. **Generate Key Pair**:
   ```bash
   openssl ecparam -name prime256v1 -genkey -noout -out private-key.pem
   openssl ec -in private-key.pem -pubout -out public-key.pem
   ```

2. **Derive Key ID**:
   ```bash
   sha256sum public-key.pem | cut -d' ' -f1
   ```

3. **Register Key**:
   - Store private key in HSM/KMS
   - Publish public key to federation registry
   - Update trust model configuration

### Key Distribution

Public keys are distributed through:
1. Federation registry (org-registry/organizations.yaml)
2. Git repository (in federation/trust/)
3. Key management service (KMS)

### Key Rotation

**Rotation Procedure**:
1. Generate new key pair
2. Publish new public key
3. Allow 7-day grace period for key adoption
4. Revoke old key
5. Update all references

**Rollback**: Keep old key in backup for 30 days

## Signing Operations

### Patch Signing

When generating a patch for GL fixes:
```typescript
const signature = signPatch(patchData, organizationPrivateKey);
const verified = verifyPatch(patchData, signature, organizationPublicKey);
```

### Deployment Signing

Before deploying to production:
```typescript
const deploymentManifest = {
  version: "5.0.0",
  artifacts: [...],
  timestamp: new Date().toISOString()
};
const signature = signDeployment(deploymentManifest, organizationPrivateKey);
```

### PR Signing

When creating pull requests:
```typescript
const prManifest = {
  prId: "123",
  changes: [...],
  approver: "governance-team"
};
const signature = signPR(prManifest, organizationPrivateKey);
```

## Verification Operations

### Patch Verification

Before applying a patch:
```typescript
const isValid = verifyPatch(
  patchData,
  signature,
  sourceOrganizationPublicKey
);
if (!isValid) {
  throw new Error("Invalid patch signature");
}
```

### Deployment Verification

Before accepting a deployment:
```typescript
const isValid = verifyDeployment(
  deploymentManifest,
  signature,
  deployingOrganizationPublicKey
);
```

## Security Best Practices

1. **Private Key Protection**:
   - Never expose private keys in logs
   - Use HSM or KMS for storage
   - Rotate keys regularly
   - Monitor key usage

2. **Public Key Distribution**:
   - Use secure channels for distribution
   - Verify public key fingerprints
   - Keep public keys up-to-date

3. **Signature Verification**:
   - Always verify signatures before applying changes
   - Use strict verification mode
   - Log all verification failures
   - Alert on verification failures

4. **Revocation Handling**:
   - Immediately revoke compromised keys
   - Notify all federation members
   - Update trust model configuration
   - Re-verify all signatures with old key

## Key Registry

### MachineNativeOps Keys

- **Primary**: `machinenativeops-primary` (SHA256: TBD)
- **Backup**: `machinenativeops-backup` (SHA256: TBD)
- **Status**: Active

### Enterprise A Keys

- **Primary**: `enterprise-a-primary` (SHA256: TBD)
- **Backup**: Not configured
- **Status**: Active

## Troubleshooting

### Signature Verification Fails

1. Check if public key is up-to-date
2. Verify key hasn't been revoked
3. Check signature algorithm matches
4. Verify data hasn't been tampered with

### Key Rotation Issues

1. Ensure grace period has elapsed
2. Check all services updated to new key
3. Verify old key is properly revoked
4. Check backup key availability

## Compliance

- **Audit Trail**: All signing operations are logged
- **Verification Required**: All operations must verify signatures
- **Key Rotation**: Automated rotation enforcement
- **Revocation**: Immediate revocation on compromise detection

## References

- Federation Trust Model: `federation/trust/trust-model.yaml`
- Organization Registry: `federation/org-registry/organizations.yaml`
- GL Unified Charter: Charter Version 2.0.0

---

**Last Updated**: 2026-01-28  
**Document Version**: 5.0.0  
**Governance Layer**: GL90-99
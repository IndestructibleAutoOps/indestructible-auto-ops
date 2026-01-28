# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: federation-signing-keys
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

# Federation Signing Keys Documentation

## Overview

This document describes the signing key management for the GL Federation platform. All operations within the federation require cryptographic signing to ensure authenticity, integrity, and non-repudiation.

## Key Management

### Federation Root Keys

The federation maintains root keys that are used to sign and verify operations across all organizations.

**Root Key Details:**
- Algorithm: ECDSA P-256
- Key ID: GL-FEDERATION-ROOT-2024
- Created: 2026-01-28T00:00:00Z
- Purpose: Federation-level signing and verification
- Storage: Hardware Security Module (HSM)

### Organization Keys

Each organization in the federation maintains its own signing keys:

#### MachineNativeOps (org-machinenativeops)
- Algorithm: ECDSA P-256
- Key ID: GL-ORG-MNO-2024
- Trust Level: High
- Capabilities: Auto-repair, auto-deploy, cross-org fixes
- Key Rotation: Quarterly

#### Enterprise A (org-enterprise-a)
- Algorithm: ECDSA P-256
- Key ID: GL-ORG-ENT-A-2024
- Trust Level: Medium
- Capabilities: Auto-repair, manual approval deploy
- Key Rotation: Biannually

## Signed Operations

The following operations must be signed:

### Patches
- All GL repair patches
- Cross-org fix patches
- Schema updates
- Governance marker additions

**Verification:**
- Verify signature before applying patch
- Check provenance chain
- Validate signer trust level

### Commits
- All commits to main branch
- Auto-generated commits
- Manual commits with GL markers

**Verification:**
- Verify commit signature
- Check signer authorization
- Validate against trust model

### Deployments
- Production deployments
- Staging deployments
- Cross-cluster deployments

**Verification:**
- Verify deployment signature
- Check deployment provenance
- Validate deployment authorization

### PR/MR Merges
- Automatic merges
- Manual merges with GL approval
- Cross-org PR merges

**Verification:**
- Verify merge signature
- Check merge authorization
- Validate compliance with trust model

## Key Rotation Policy

### Root Keys
- Rotation interval: Annually
- Overlap period: 30 days
- Notification: 7 days before rotation
- Storage: HSM with multi-party control

### Organization Keys
- Rotation interval: Quarterly (High Trust) / Biannually (Medium Trust)
- Overlap period: 14 days
- Notification: 3 days before rotation
- Storage: Secure key management service

### Emergency Key Rotation
- Trigger: Compromise detection
- Process: Immediate revocation, new key generation, re-signing of active operations
- Recovery: Federation coordinator approval required

## Key Verification Process

### Step 1: Retrieve Public Key
```bash
gl-federation-cli keys get-public --key-id <KEY_ID>
```

### Step 2: Verify Signature
```bash
gl-federation-cli verify --signature <SIG_FILE> --data <DATA_FILE> --public-key <PUB_KEY>
```

### Step 3: Check Trust Level
```bash
gl-federation-cli trust check --signer <ORG_ID> --operation <OPERATION>
```

### Step 4: Validate Provenance
```bash
gl-federation-cli provenance validate --provenance <PROVENANCE_FILE>
```

## Security Best Practices

1. **Never expose private keys**
   - Private keys must remain in secure storage
   - No key material in logs or debug output
   - Rotate keys immediately on compromise

2. **Use hardware security modules**
   - Store root keys in HSM
   - Use secure enclaves for organization keys
   - Implement multi-party approval for key access

3. **Regular key rotation**
   - Follow rotation schedule strictly
   - Maintain key overlap during rotation
   - Document all rotation events

4. **Audit key usage**
   - Log all signing operations
   - Monitor for anomalous signing patterns
   - Review audit logs regularly

5. **Implement key recovery**
   - Maintain secure key backup
   - Test recovery procedures regularly
   - Document recovery process

## Troubleshooting

### Signature Verification Failed
1. Check if public key is current
2. Verify key rotation hasn't occurred
3. Check signer trust level
4. Validate operation is permitted

### Key Not Found
1. Check key ID format
2. Verify key hasn't been revoked
3. Check organization is registered
4. Contact federation coordinator

### Provenance Validation Failed
1. Check SLSA format version
2. Verify all required fields present
3. Validate provenance chain
4. Check for tampering indicators

## Contact

For key management issues:
- Federation Coordinator: federation@machinenativeops.io
- Security Team: security@machinenativeops.io
- Emergency: +1-555-GL-FED-SEC

---

**Document Version:** 1.0.0
**Last Updated:** 2026-01-28T00:00:00Z
**Next Review:** 2026-04-28T00:00:00Z
**GL Governance:** Active
**GL Layer:** GL90-99
**Semantic:** federation-signing-keys
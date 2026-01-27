"""
Phase 20: SLSA L3 Provenance System

This module provides comprehensive SLSA (Supply-chain Levels for Software Artifacts)
Level 3 compliance including:
- Provenance generation
- Signature verification with Sigstore
- Build attestation
- Artifact verification

Key Components:
- ProvenanceGenerator: Generate SLSA-compliant provenance
- SignatureVerifier: Verify signatures using Sigstore
- AttestationManager: Manage build attestations
- ArtifactVerifier: Verify artifact integrity
"""

from .artifact_verifier import ArtifactMetadata, ArtifactVerifier, VerificationResult
from .attestation_manager import Attestation, AttestationManager, AttestationType
from .provenance_generator import (
    BuildDefinition,
    Provenance,
    ProvenanceGenerator,
    SLSALevel,
)
from .signature_verifier import (
    SignatureResult,
    SignatureType,
    SignatureVerifier,
    VerificationPolicy,
)

__all__ = [
    "ProvenanceGenerator",
    "Provenance",
    "BuildDefinition",
    "SLSALevel",
    "SignatureVerifier",
    "SignatureResult",
    "VerificationPolicy",
    "SignatureType",
    "AttestationManager",
    "Attestation",
    "AttestationType",
    "ArtifactVerifier",
    "VerificationResult",
    "ArtifactMetadata",
]

__version__ = "1.0.0"
__author__ = "SynergyMesh Team"

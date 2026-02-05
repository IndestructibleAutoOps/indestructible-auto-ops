"""
GL Core Sealing Engine
Implements blockchain-inspired immutable core sealing for GL architecture

Based on Research:
- Blockchain cryptographic sealing mechanisms
- Netflix immutable infrastructure patterns
- Google Borg cell immutability principles
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import hashlib
import json
import base64


@dataclass
class SealedCoreEntry:
    """Represents a sealed core entry in the hash chain"""
    hash: str
    previous_hash: str
    timestamp: str
    artifacts: Dict
    approvals: List[str]
    status: str
    seal_signature: Optional[str] = None
    merkle_root: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "hash": self.hash,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "artifacts": self.artifacts,
            "approvals": self.approvals,
            "status": self.status,
            "seal_signature": self.seal_signature,
            "merkle_root": self.merkle_root
        }


@dataclass
class CeremonyData:
    """Data for core sealing ceremony"""
    candidate_hash: str
    artifacts: Dict
    timestamp: str
    committee: List[str]
    ceremony_id: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "ceremony_id": self.ceremony_id,
            "candidate_hash": self.candidate_hash,
            "artifacts": self.artifacts,
            "timestamp": self.timestamp,
            "committee": self.committee
        }


@dataclass
class VerificationResult:
    """Result of core verification"""
    is_valid: bool
    verification_score: float
    violations: List[str]
    warnings: List[str]
    verified_at: datetime
    core_hash: str
    
    def add_violation(self, message: str):
        """Add violation to result"""
        self.violations.append(message)
        self.is_valid = False
    
    def add_warning(self, message: str):
        """Add warning to result"""
        self.warnings.append(message)


class GLCoreSealingEngine:
    """
    GL Core Sealing Engine
    Implements blockchain-inspired immutable core sealing
    """
    
    def __init__(self):
        self.sealed_core_registry: List[SealedCoreEntry] = []
        self.sealing_committee: List[str] = []
        self.sealing_witnesses: List[str] = []
        self.verification_history: List[Dict] = []
        self.current_core_hash: Optional[str] = None
    
    def set_sealing_committee(self, committee: List[str]):
        """Set the sealing committee for multi-party approval"""
        self.sealing_committee = committee
    
    def add_sealing_witness(self, witness: str):
        """Add a witness to the sealing ceremony"""
        if witness not in self.sealing_witnesses:
            self.sealing_witnesses.append(witness)
    
    def prepare_sealing(self, core_layers: List[str], artifacts: Dict) -> CeremonyData:
        """
        Prepare core layers for sealing
        Creates ceremony data for multi-party approval
        """
        # Validate core layers
        for layer in core_layers:
            if not self._is_core_layer(layer):
                raise ValueError(f"{layer} is not a core layer")
        
        # Prepare artifacts
        prepared_artifacts = {
            "layers": core_layers,
            "artifacts": artifacts,
            "timestamp": datetime.now().isoformat()
        }
        
        # Compute candidate core hash
        candidate_hash = self._compute_candidate_hash(prepared_artifacts)
        
        # Compute Merkle root
        merkle_root = self._compute_merkle_root(artifacts)
        
        # Prepare ceremony data
        ceremony_id = self._generate_ceremony_id()
        ceremony_data = CeremonyData(
            ceremony_id=ceremony_id,
            candidate_hash=candidate_hash,
            artifacts=prepared_artifacts,
            timestamp=datetime.now().isoformat(),
            committee=self.sealing_committee
        )
        
        return ceremony_data
    
    def execute_sealing(self, ceremony_data: CeremonyData, approvals: List[str]) -> str:
        """
        Execute core sealing ceremony
        Requires multi-party approval from committee
        """
        # Verify approvals
        if not self._verify_approvals(approvals):
            raise ValueError("Insufficient or invalid approvals for sealing")
        
        # Get previous sealed hash
        previous_hash = self._get_previous_sealed_hash()
        
        # Create seal signature
        seal_signature = self._sign_seal(ceremony_data, approvals)
        
        # Compute Merkle root
        merkle_root = self._compute_merkle_root(ceremony_data.artifacts.get("artifacts", {}))
        
        # Create sealed core entry
        sealed_core = SealedCoreEntry(
            hash=ceremony_data.candidate_hash,
            previous_hash=previous_hash,
            timestamp=ceremony_data.timestamp,
            artifacts=ceremony_data.artifacts,
            approvals=approvals,
            status="SEALED",
            seal_signature=seal_signature,
            merkle_root=merkle_root
        )
        
        # Add to sealed core registry
        self.sealed_core_registry.append(sealed_core)
        self.current_core_hash = sealed_core.hash
        
        # Log sealing event
        self._log_sealing_event(sealed_core)
        
        return sealed_core.hash
    
    def verify_seal(self, core_hash: str) -> bool:
        """
        Verify core seal integrity
        Checks hash chain, signatures, and artifact integrity
        """
        seal_entry = self._get_seal_entry(core_hash)
        
        if not seal_entry:
            return False
        
        # Verify hash chain
        if not self._verify_hash_chain(seal_entry):
            return False
        
        # Verify seal signature
        if not self._verify_seal_signature(seal_entry):
            return False
        
        # Verify artifact integrity
        if not self._verify_artifact_integrity(seal_entry):
            return False
        
        # Verify Merkle root
        if not self._verify_merkle_root(seal_entry):
            return False
        
        return True
    
    def verify_core_continuously(self) -> VerificationResult:
        """
        Continuously verify core integrity
        Runs comprehensive verification checks
        """
        result = VerificationResult(
            is_valid=True,
            verification_score=0.0,
            violations=[],
            warnings=[],
            verified_at=datetime.now(),
            core_hash=self.current_core_hash or ""
        )
        
        if not self.current_core_hash:
            result.add_warning("No sealed core exists")
            return result
        
        # Verify hash chain integrity
        if not self._verify_hash_chain_continuously():
            result.add_violation("Hash chain broken")
        
        # Verify seal signatures
        if not self._verify_signatures_continuously():
            result.add_violation("Invalid seal signatures detected")
        
        # Verify artifact integrity
        if not self._verify_artifacts_continuously():
            result.add_violation("Artifact corruption detected")
        
        # Verify Merkle root
        if not self._verify_merkle_root_continuously():
            result.add_violation("Merkle root mismatch")
        
        # Compute verification score
        result.verification_score = self._compute_verification_score(result)
        
        # Record verification
        self.verification_history.append({
            "timestamp": datetime.now().isoformat(),
            "result": {
                "is_valid": result.is_valid,
                "verification_score": result.verification_score,
                "violations": result.violations,
                "warnings": result.warnings
            },
            "core_hash": self.current_core_hash
        })
        
        return result
    
    def get_seal_status(self) -> Dict:
        """
        Get current seal status
        Returns information about sealed core
        """
        if not self.current_core_hash:
            return {
                "status": "UNSEALED",
                "core_hash": None,
                "sealed_at": None,
                "approvals": [],
                "verification_count": len(self.verification_history)
            }
        
        seal_entry = self._get_seal_entry(self.current_core_hash)
        
        return {
            "status": seal_entry.status,
            "core_hash": seal_entry.hash,
            "previous_hash": seal_entry.previous_hash,
            "sealed_at": seal_entry.timestamp,
            "approvals": seal_entry.approvals,
            "merkle_root": seal_entry.merkle_root,
            "verification_count": len(self.verification_history),
            "last_verification": self.verification_history[-1]["timestamp"] if self.verification_history else None
        }
    
    def get_core_merkle_root(self) -> Optional[str]:
        """
        Compute Merkle root of all core artifacts
        Enables efficient verification of GL core
        """
        if not self.current_core_hash:
            return None
        
        seal_entry = self._get_seal_entry(self.current_core_hash)
        if seal_entry:
            return seal_entry.merkle_root
        
        return None
    
    # Private methods
    
    def _is_core_layer(self, layer: str) -> bool:
        """Check if layer is a core layer"""
        # Core layers are L00-L09
        return layer.startswith("L0")
    
    def _compute_candidate_hash(self, artifacts: Dict) -> str:
        """Compute candidate hash for core sealing"""
        artifacts_json = json.dumps(artifacts, sort_keys=True)
        return hashlib.sha256(artifacts_json.encode()).hexdigest()
    
    def _compute_merkle_root(self, artifacts: Dict) -> str:
        """Compute Merkle root of artifacts"""
        # Serialize artifacts
        artifact_hashes = []
        for key, value in artifacts.items():
            if isinstance(value, dict):
                artifact_data = json.dumps(value, sort_keys=True)
            else:
                artifact_data = str(value)
            artifact_hash = hashlib.sha256(artifact_data.encode()).hexdigest()
            artifact_hashes.append(artifact_hash)
        
        # Build Merkle tree
        return self._build_merkle_tree(artifact_hashes)
    
    def _build_merkle_tree(self, hashes: List[str]) -> str:
        """Build Merkle tree from hash list"""
        if not hashes:
            return ""
        
        if len(hashes) == 1:
            return hashes[0]
        
        # Build next level
        next_level = []
        for i in range(0, len(hashes), 2):
            if i + 1 < len(hashes):
                combined = hashes[i] + hashes[i + 1]
            else:
                combined = hashes[i] + hashes[i]  # Duplicate last hash if odd number
            next_hash = hashlib.sha256(combined.encode()).hexdigest()
            next_level.append(next_hash)
        
        # Recursively build tree
        return self._build_merkle_tree(next_level)
    
    def _generate_ceremony_id(self) -> str:
        """Generate unique ceremony ID"""
        timestamp = datetime.now().isoformat()
        data = f"{timestamp}-{len(self.sealed_core_registry)}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def _verify_approvals(self, approvals: List[str]) -> bool:
        """Verify sealing approvals"""
        # Check if all committee members approved
        required = set(self.sealing_committee)
        provided = set(approvals)
        
        # Require at least 2/3 of committee approval
        min_approvals = len(self.sealing_committee) * 2 // 3
        if len(approvals) < min_approvals:
            return False
        
        # Check if approvals are from committee members
        return provided.issubset(required)
    
    def _sign_seal(self, ceremony_data: CeremonyData, approvals: List[str]) -> str:
        """Create seal signature"""
        # Combine ceremony data and approvals
        signature_data = {
            "ceremony_id": ceremony_data.ceremony_id,
            "candidate_hash": ceremony_data.candidate_hash,
            "approvals": sorted(approvals),
            "timestamp": ceremony_data.timestamp
        }
        signature_json = json.dumps(signature_data, sort_keys=True)
        signature_hash = hashlib.sha256(signature_json.encode()).hexdigest()
        
        # Encode as base64 for readability
        return base64.b64encode(signature_hash.encode()).decode()
    
    def _get_previous_sealed_hash(self) -> str:
        """Get previous sealed core hash"""
        if not self.sealed_core_registry:
            return "GENESIS"
        
        return self.sealed_core_registry[-1].hash
    
    def _get_seal_entry(self, core_hash: str) -> Optional[SealedCoreEntry]:
        """Get seal entry by hash"""
        for entry in self.sealed_core_registry:
            if entry.hash == core_hash:
                return entry
        return None
    
    def _verify_hash_chain(self, seal_entry: SealedCoreEntry) -> bool:
        """Verify hash chain continuity"""
        if seal_entry.previous_hash == "GENESIS":
            return True
        
        # Find previous entry
        for entry in self.sealed_core_registry:
            if entry.hash == seal_entry.previous_hash:
                return True
        
        return False
    
    def _verify_seal_signature(self, seal_entry: SealedCoreEntry) -> bool:
        """Verify seal signature"""
        if not seal_entry.seal_signature:
            return False
        
        try:
            # Decode signature
            signature_hash = base64.b64decode(seal_entry.seal_signature.encode()).decode()
            
            # Recompute signature
            signature_data = {
                "approvals": sorted(seal_entry.approvals),
                "timestamp": seal_entry.timestamp
            }
            signature_json = json.dumps(signature_data, sort_keys=True)
            computed_hash = hashlib.sha256(signature_json.encode()).hexdigest()
            
            return signature_hash == computed_hash
        except Exception:
            return False
    
    def _verify_artifact_integrity(self, seal_entry: SealedCoreEntry) -> bool:
        """Verify artifact integrity"""
        # Recompute artifact hash
        artifacts_json = json.dumps(seal_entry.artifacts, sort_keys=True)
        computed_hash = hashlib.sha256(artifacts_json.encode()).hexdigest()
        
        # Verify matches stored hash
        return computed_hash == seal_entry.hash
    
    def _verify_merkle_root(self, seal_entry: SealedCoreEntry) -> bool:
        """Verify Merkle root"""
        if not seal_entry.merkle_root:
            return True
        
        # Recompute Merkle root
        artifacts = seal_entry.artifacts.get("artifacts", {})
        computed_root = self._compute_merkle_root(artifacts)
        
        return computed_root == seal_entry.merkle_root
    
    def _verify_hash_chain_continuously(self) -> bool:
        """Verify entire hash chain"""
        for i in range(1, len(self.sealed_core_registry)):
            current = self.sealed_core_registry[i]
            previous = self.sealed_core_registry[i - 1]
            
            if current.previous_hash != previous.hash:
                return False
        
        return True
    
    def _verify_signatures_continuously(self) -> bool:
        """Verify all seal signatures"""
        for entry in self.sealed_core_registry:
            if not self._verify_seal_signature(entry):
                return False
        
        return True
    
    def _verify_artifacts_continuously(self) -> bool:
        """Verify all artifact integrity"""
        for entry in self.sealed_core_registry:
            if not self._verify_artifact_integrity(entry):
                return False
        
        return True
    
    def _verify_merkle_root_continuously(self) -> bool:
        """Verify all Merkle roots"""
        for entry in self.sealed_core_registry:
            if not self._verify_merkle_root(entry):
                return False
        
        return True
    
    def _compute_verification_score(self, result: VerificationResult) -> float:
        """Compute verification score"""
        if not self.current_core_hash:
            return 0.0
        
        total_checks = 4  # hash chain, signatures, artifacts, merkle root
        passed_checks = total_checks - len(result.violations)
        
        return passed_checks / total_checks
    
    def _log_sealing_event(self, sealed_core: SealedCoreEntry):
        """Log sealing event to verification history"""
        self.verification_history.append({
            "timestamp": datetime.now().isoformat(),
            "event_type": "SEALING",
            "core_hash": sealed_core.hash,
            "previous_hash": sealed_core.previous_hash,
            "approvals": sealed_core.approvals,
            "status": sealed_core.status
        })
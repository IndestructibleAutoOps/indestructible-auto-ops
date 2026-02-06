#!/usr/bin/env python3
"""
Migration Tests for Era-1 → Era-2
Tests bidirectional mapping, migration consistency, complement replay, and semantic consistency.
"""

import pytest
import json
import hashlib
import sys
from pathlib import Path
from datetime import datetime

# Add ecosystem to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tools"))

from hash_translation_engine import HashTranslationEngine, HTTEntry, CanonicalizationSpec


class TestHashTranslation:
    """Test Hash Translation Table functionality"""
    
    @pytest.fixture
    def hte(self):
        """Initialize Hash Translation Engine"""
        return HashTranslationEngine(workspace="/workspace")
    
    @pytest.fixture
    def htt_entries(self, hte):
        """Load HTT entries"""
        entries = hte.generate_htt(verify=False)
        return entries
    
    def test_htt_file_exists(self, hte):
        """Test that HTT file exists"""
        assert hte.htt_file.exists(), "HTT file should exist"
    
    def test_htt_metadata_exists(self, hte):
        """Test that HTT metadata exists"""
        meta_file = hte.migration_dir / "htt-metadata.json"
        assert meta_file.exists(), "HTT metadata file should exist"
    
    def test_htt_entries_count(self, htt_entries):
        """Test HTT has correct number of entries"""
        # Should have 12 entries (10 step artifacts + 2 closure artifacts)
        assert len(htt_entries) == 12, f"Expected 12 entries, got {len(htt_entries)}"
    
    def test_bidirectional_mapping(self, hte, htt_entries):
        """Test Era-1 ↔ Era-2 bidirectional mapping"""
        for entry in htt_entries:
            # Verify Era-1 hash is present
            assert entry.era1_hash is not None, f"Era-1 hash missing for {entry.source_path}"
            assert entry.era1_hash.startswith("sha256:"), f"Era-1 hash should have 'sha256:' prefix"
            
            # Verify Era-2 hash is present
            assert entry.era2_hash is not None, f"Era-2 hash missing for {entry.source_path}"
            assert entry.era2_hash.startswith("sha256:"), f"Era-2 hash should have 'sha256:' prefix"
            
            # Verify hashes are different (canonicalization changed)
            assert entry.era1_hash != entry.era2_hash, f"Era-1 and Era-2 hashes should differ"
    
    def test_mapping_consistency(self, htt_entries):
        """Test mapping consistency - no duplicates, no conflicts, no missing"""
        era1_hashes = [e.era1_hash for e in htt_entries]
        era2_hashes = [e.era2_hash for e in htt_entries]
        
        # Check for duplicate Era-1 hashes (should be unique)
        era1_duplicates = [h for h in era1_hashes if era1_hashes.count(h) > 1]
        assert len(era1_duplicates) == 0, f"Found duplicate Era-1 hashes: {era1_duplicates}"
        
        # Note: Era-2 hashes may have duplicates if artifacts have identical canonicalized forms
        # This is expected behavior in some cases (e.g., same content in different artifacts)
        # We only check for Era-1 uniqueness, not Era-2
        
        # Check for conflicts (one Era-1 hash mapping to multiple Era-2 hashes)
        era1_to_era2 = {}
        for entry in htt_entries:
            if entry.era1_hash in era1_to_era2:
                assert era1_to_era2[entry.era1_hash] == entry.era2_hash, \
                    f"Era-1 hash {entry.era1_hash} maps to multiple Era-2 hashes"
            else:
                era1_to_era2[entry.era1_hash] = entry.era2_hash
    
    def test_complement_replay(self, hte):
        """Test that Era-1 complements can be replayed in Era-2"""
        # Find complement artifacts
        complement_dir = hte.evidence_dir / "complements"
        
        # Note: Complements directory may not exist yet, so we skip if not found
        if not complement_dir.exists():
            pytest.skip("Complements directory not found")
        
        # Scan complements
        complements = list(complement_dir.glob("*.json"))
        if not complements:
            pytest.skip("No complement files found")
        
        # Verify each complement has hash translation
        for complement_file in complements:
            data = hte.load_json(complement_file)
            if data:
                era1_hash = hte.extract_era1_hash(data)
                assert era1_hash is not None, f"Complement {complement_file} has no Era-1 hash"
                
                # Verify Era-2 hash can be generated
                era2_hash = hte.generate_era2_hash(data)
                assert era2_hash is not None, f"Failed to generate Era-2 hash for {complement_file}"
    
    def test_semantic_consistency(self, hte, htt_entries):
        """Test Era-1 semantic declarations can be interpreted by Era-2"""
        for entry in htt_entries:
            # Verify semantic delta is present (as a direct field, not in metadata)
            assert hasattr(entry, "semantic_delta"), \
                f"Semantic delta missing for {entry.source_path}"
            
            # Verify semantic delta structure
            delta = entry.semantic_delta
            assert "fields_added" in delta, f"fields_added missing for {entry.source_path}"
            assert "fields_removed" in delta, f"fields_removed missing for {entry.source_path}"
            assert "fields_renamed" in delta, f"fields_renamed missing for {entry.source_path}"
            
            # Verify preserve_semantic flag is True
            assert entry.metadata.get("preserve_semantic", False), \
                f"preserve_semantic should be True for {entry.source_path}"
            
            # Verify translation method is appropriate
            assert entry.translation_method in ["canonical_rehash", "semantic_preserve", "multi_semantic"], \
                f"Invalid translation method: {entry.translation_method}"
    
    def test_chain_continuity(self, hte, htt_entries):
        """Test hash chain continuity across Era migration"""
        # Verify artifact chain is continuous
        for i, entry in enumerate(htt_entries):
            if i > 0:
                # Previous entry's hash should be in current entry's chain references
                prev_entry = htt_entries[i - 1]
                if entry.chain_references.get("parent"):
                    assert entry.chain_references["parent"] == prev_entry.era1_hash, \
                        f"Chain broken at entry {i}: parent hash mismatch"
    
    def test_canonicalization_versions(self, htt_entries):
        """Test canonicalization versions are correctly recorded"""
        for entry in htt_entries:
            # Verify Era-1 spec
            assert "canonicalization_v1" in entry.__dict__, "Era-1 canonicalization info missing"
            v1 = entry.canonicalization_v1
            assert v1["version"] == "1.0", f"Era-1 version should be 1.0, got {v1['version']}"
            assert v1["method"] == "JCS+LayeredSorting", f"Invalid Era-1 method"
            
            # Verify Era-2 spec
            assert "canonicalization_v2" in entry.__dict__, "Era-2 canonicalization info missing"
            v2 = entry.canonicalization_v2
            assert v2["version"] == "2.0", f"Era-2 version should be 2.0, got {v2['version']}"
            assert v2["method"] == "JCS+EnhancedLayeredSorting", f"Invalid Era-2 method"
    
    def test_htt_integrity(self, hte):
        """Test HTT file integrity"""
        # Load HTT metadata
        meta_file = hte.migration_dir / "htt-metadata.json"
        with open(meta_file, 'r') as f:
            metadata = json.load(f)
        
        # Verify HTT hash
        assert "htt_hash" in metadata, "HTT hash missing from metadata"
        assert metadata["htt_hash"].startswith("sha256:"), "Invalid HTT hash format"
        
        # Verify HTT version
        assert metadata["htt_version"] == "1.0", f"Invalid HTT version: {metadata['htt_version']}"
        
        # Verify total entries
        assert metadata["total_entries"] == 12, f"Expected 12 entries, got {metadata['total_entries']}"
    
    def test_verification_status(self, htt_entries):
        """Test all entries are verified"""
        for entry in htt_entries:
            assert entry.verification_status == "verified", \
                f"Entry {entry.source_path} not verified: {entry.verification_status}"


class TestMigrationConsistency:
    """Test migration consistency and completeness"""
    
    @pytest.fixture
    def hte(self):
        """Initialize Hash Translation Engine"""
        return HashTranslationEngine(workspace="/workspace")
    
    @pytest.fixture
    def migration_report(self, hte):
        """Load migration report"""
        report_file = hte.migration_dir / "migration-report.json"
        with open(report_file, 'r') as f:
            return json.load(f)
    
    def test_era1_artifacts_count(self, migration_report):
        """Test all Era-1 artifacts are migrated"""
        assert migration_report["era1_artifacts"] == 12, \
            f"Expected 12 artifacts, got {migration_report['era1_artifacts']}"
    
    def test_era1_hashes_count(self, migration_report):
        """Test all Era-1 hashes are recorded"""
        era1_hashes = migration_report["era1_hashes"]
        assert len(era1_hashes) == 12, f"Expected 12 Era-1 hashes, got {len(era1_hashes)}"
    
    def test_era2_hashes_count(self, migration_report):
        """Test all Era-2 hashes are generated"""
        era2_hashes = migration_report["era2_hashes"]
        assert len(era2_hashes) == 12, f"Expected 12 Era-2 hashes, got {len(era2_hashes)}"
    
    def test_chain_continuity(self, migration_report):
        """Test artifact chain is continuous"""
        assert migration_report["chain_continuity"] is True, "Chain continuity should be True"
    
    def test_translation_methods(self, migration_report):
        """Test translation methods are recorded"""
        methods = migration_report["translation_methods"]
        assert "canonical_rehash" in methods, "canonical_rehash method missing"
        assert methods["canonical_rehash"] == 12, \
            f"Expected 12 canonical_rehash entries, got {methods['canonical_rehash']}"


def test_migration_readiness():
    """Test overall migration readiness"""
    hte = HashTranslationEngine(workspace="/workspace")
    
    # Check HTT exists
    assert hte.htt_file.exists(), "HTT file should exist"
    
    # Check Era-2 spec exists
    era2_spec_file = Path("/workspace/ecosystem/governance/hash-spec/era-2.yaml")
    assert era2_spec_file.exists(), "Era-2 hash spec should exist"
    
    # Check migration directory exists
    assert hte.migration_dir.exists(), "Migration directory should exist"
    
    # Check HTT entries can be loaded
    hte.generate_htt(verify=False)
    assert len(hte.htt_entries) > 0, "HTT entries should be loaded"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
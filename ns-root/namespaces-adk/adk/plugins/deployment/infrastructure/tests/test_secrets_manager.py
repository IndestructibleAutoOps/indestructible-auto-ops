"""
Unit tests for Secrets Manager
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

import sys
sys.path.insert(0, '/workspace/machine-native-ops')

from adk.plugins.deployment.infrastructure.secrets_manager import (
    SecretsManager,
    SecretConfig,
    SecretProvider,
    SecretType,
    RotationPolicy,
    SecretMetadata,
    SecretValue,
    AuditLogEntry,
    SecretManagerResult
)


class TestSecretConfig:
    """Test SecretConfig dataclass"""
    
    def test_default_config(self):
        """Test default configuration values"""
        config = SecretConfig()
        
        assert config.provider == SecretProvider.KUBERNETES_SECRETS
        assert config.encryption_enabled is True
        assert config.auto_rotation_enabled is True
        assert config.default_rotation_policy == RotationPolicy.WEEKLY
        assert config.audit_logging_enabled is True
        assert config.versioning_enabled is True
        assert config.backup_enabled is True
        assert config.cache_enabled is True
    
    def test_custom_config(self):
        """Test custom configuration"""
        config = SecretConfig(
            provider=SecretProvider.AWS_SECRETS_MANAGER,
            encryption_enabled=False,
            auto_rotation_enabled=False,
            audit_logging_enabled=False,
            backup_retention_days=60
        )
        
        assert config.provider == SecretProvider.AWS_SECRETS_MANAGER
        assert config.encryption_enabled is False
        assert config.auto_rotation_enabled is False
        assert config.audit_logging_enabled is False
        assert config.backup_retention_days == 60


class TestSecretMetadata:
    """Test SecretMetadata class"""
    
    def test_secret_metadata_creation(self):
        """Test creating secret metadata"""
        metadata = SecretMetadata(
            name="test-secret",
            secret_type=SecretType.API_KEY,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            rotation_policy=RotationPolicy.DAILY,
            owner="devops-team"
        )
        
        assert metadata.name == "test-secret"
        assert metadata.secret_type == SecretType.API_KEY
        assert metadata.rotation_policy == RotationPolicy.DAILY
        assert metadata.owner == "devops-team"
        assert metadata.version == 1
    
    def test_secret_metadata_to_dict(self):
        """Test converting metadata to dictionary"""
        now = datetime.now()
        metadata = SecretMetadata(
            name="test-secret",
            secret_type=SecretType.STRING,
            created_at=now,
            updated_at=now,
            rotation_policy=RotationPolicy.MONTHLY
        )
        
        metadata_dict = metadata.to_dict()
        
        assert metadata_dict["name"] == "test-secret"
        assert metadata_dict["secret_type"] == "string"
        assert metadata_dict["rotation_policy"] == "monthly"
        assert metadata_dict["version"] == 1


class TestSecretsManager:
    """Test SecretsManager class"""
    
    @pytest.fixture
    def config(self):
        """Create test configuration"""
        return SecretConfig()
    
    @pytest.fixture
    def manager(self, config):
        """Create secrets manager instance"""
        return SecretsManager("kubernetes", config)
    
    def test_manager_initialization(self, manager):
        """Test manager initialization"""
        assert manager.provider == "kubernetes"
        assert manager.config is not None
        assert manager._secrets == {}
        assert manager._secrets_metadata == {}
        assert manager._audit_log == []
        assert manager._cache == {}
    
    @pytest.mark.asyncio
    async def test_create_secret(self, manager):
        """Test creating a secret"""
        result = await manager.create_secret(
            name="test-secret",
            value="secret-value",
            secret_type=SecretType.STRING,
            rotation_policy=RotationPolicy.DAILY
        )
        
        assert isinstance(result, SecretManagerResult)
        assert result.success is True
        assert "test-secret created successfully" in result.message
        assert result.data is not None
        assert result.data["name"] == "test-secret"
        assert result.data["version"] == 1
    
    @pytest.mark.asyncio
    async def test_create_duplicate_secret(self, manager):
        """Test creating duplicate secret"""
        # Create first secret
        await manager.create_secret(
            name="test-secret",
            value="value1",
            secret_type=SecretType.STRING
        )
        
        # Try to create duplicate
        result = await manager.create_secret(
            name="test-secret",
            value="value2",
            secret_type=SecretType.STRING
        )
        
        assert result.success is False
        assert len(result.errors) > 0
        assert "already exists" in result.errors[0].lower()
    
    @pytest.mark.asyncio
    async def test_get_secret(self, manager):
        """Test retrieving a secret"""
        # Create secret
        await manager.create_secret(
            name="test-secret",
            value="my-secret-value",
            secret_type=SecretType.API_KEY
        )
        
        # Get secret
        result = await manager.get_secret("test-secret")
        
        assert result.success is True
        assert result.data is not None
        assert result.data["value"] == "my-secret-value"
        assert result.data["version"] == 1
    
    @pytest.mark.asyncio
    async def test_get_nonexistent_secret(self, manager):
        """Test retrieving nonexistent secret"""
        result = await manager.get_secret("nonexistent-secret")
        
        assert result.success is False
        assert len(result.errors) > 0
        assert "not found" in result.errors[0].lower()
    
    @pytest.mark.asyncio
    async def test_update_secret(self, manager):
        """Test updating a secret"""
        # Create secret
        await manager.create_secret(
            name="test-secret",
            value="original-value",
            secret_type=SecretType.STRING
        )
        
        # Update secret
        result = await manager.update_secret(
            name="test-secret",
            value="updated-value"
        )
        
        assert result.success is True
        assert result.data["version"] == 2
        
        # Verify update
        get_result = await manager.get_secret("test-secret")
        assert get_result.data["value"] == "updated-value"
    
    @pytest.mark.asyncio
    async def test_delete_secret(self, manager):
        """Test deleting a secret"""
        # Create secret
        await manager.create_secret(
            name="test-secret",
            value="value-to-delete",
            secret_type=SecretType.STRING
        )
        
        # Delete secret
        result = await manager.delete_secret("test-secret")
        
        assert result.success is True
        assert "deleted successfully" in result.message
        
        # Verify deletion
        get_result = await manager.get_secret("test-secret")
        assert get_result.success is False
    
    @pytest.mark.asyncio
    async def test_rotate_secret(self, manager):
        """Test rotating a secret"""
        # Create secret
        await manager.create_secret(
            name="test-secret",
            value="original-value",
            secret_type=SecretType.API_KEY,
            rotation_policy=RotationPolicy.DAILY
        )
        
        # Rotate secret
        result = await manager.rotate_secret("test-secret")
        
        assert result.success is True
        assert "updated" in result.message or "rotated" in result.message
        assert result.data["version"] == 2
    
    @pytest.mark.asyncio
    async def test_rotate_with_custom_value(self, manager):
        """Test rotating with custom value"""
        # Create secret
        await manager.create_secret(
            name="test-secret",
            value="old-value",
            secret_type=SecretType.STRING
        )
        
        # Rotate with custom value
        result = await manager.rotate_secret(
            name="test-secret",
            new_value="new-rotated-value"
        )
        
        assert result.success is True
        
        # Verify new value
        get_result = await manager.get_secret("test-secret")
        assert get_result.data["value"] == "new-rotated-value"
    
    @pytest.mark.asyncio
    async def test_list_secrets(self, manager):
        """Test listing all secrets"""
        # Create multiple secrets
        await manager.create_secret("secret1", "value1", SecretType.STRING)
        await manager.create_secret("secret2", "value2", SecretType.API_KEY)
        await manager.create_secret("secret3", "value3", SecretType.DATABASE_URL)
        
        # List secrets
        result = await manager.list_secrets()
        
        assert result.success is True
        assert len(result.data["secrets"]) == 3
    
    @pytest.mark.asyncio
    async def test_list_secrets_with_filters(self, manager):
        """Test listing secrets with filters"""
        # Create secrets with different types
        await manager.create_secret("secret1", "value1", SecretType.API_KEY, tags={"team": "dev"})
        await manager.create_secret("secret2", "value2", SecretType.API_KEY, tags={"team": "ops"})
        await manager.create_secret("secret3", "value3", SecretType.STRING, tags={"team": "dev"})
        
        # Filter by type
        result = await manager.list_secrets(filter_type=SecretType.API_KEY)
        assert len(result.data["secrets"]) == 2
        
        # Filter by tags
        result = await manager.list_secrets(filter_tags={"team": "dev"})
        assert len(result.data["secrets"]) == 2
    
    @pytest.mark.asyncio
    async def test_rotate_all_secrets(self, manager):
        """Test rotating all secrets that need rotation"""
        now = datetime.now()
        
        # Create secrets with different rotation policies
        await manager.create_secret(
            "urgent-secret",
            "value1",
            SecretType.STRING,
            RotationPolicy.HOURLY
        )
        
        await manager.create_secret(
            "daily-secret",
            "value2",
            SecretType.STRING,
            RotationPolicy.DAILY
        )
        
        # Set last rotation to force rotation
        for metadata in manager._secrets_metadata.values():
            metadata.last_rotated_at = now - timedelta(days=2)
            metadata.next_rotation_at = now - timedelta(hours=1)
        
        # Rotate all
        result = await manager.rotate_all_secrets()
        
        assert result.success is True
        assert result.data["rotated_count"] == 2
        assert result.data["failed_count"] == 0
    
    @pytest.mark.asyncio
    async def test_get_audit_log(self, manager):
        """Test getting audit log"""
        # Perform some operations
        await manager.create_secret("secret1", "value1", SecretType.STRING)
        await manager.get_secret("secret1")
        await manager.update_secret("secret1", "new-value")
        
        # Get audit log
        result = await manager.get_audit_log()
        
        assert result.success is True
        assert len(result.data["entries"]) >= 3
        
        # Check log entries
        actions = [entry["action"] for entry in result.data["entries"]]
        assert "created" in actions
        assert "read" in actions
        assert "updated" in actions
    
    @pytest.mark.asyncio
    async def test_get_audit_log_filtered(self, manager):
        """Test getting audit log filtered by secret name"""
        # Create and modify secrets
        await manager.create_secret("secret1", "value1", SecretType.STRING)
        await manager.create_secret("secret2", "value2", SecretType.STRING)
        await manager.update_secret("secret1", "new-value")
        await manager.update_secret("secret2", "new-value")
        
        # Get audit log for secret1 only
        result = await manager.get_audit_log(secret_name="secret1")
        
        assert result.success is True
        
        # All entries should be for secret1
        for entry in result.data["entries"]:
            assert entry["secret_name"] == "secret1"
    
    @pytest.mark.asyncio
    async def test_get_statistics(self, manager):
        """Test getting statistics"""
        # Create some secrets
        await manager.create_secret("secret1", "value1", SecretType.STRING)
        await manager.create_secret("secret2", "value2", SecretType.API_KEY)
        
        # Perform some operations
        await manager.get_secret("secret1")
        await manager.update_secret("secret1", "new-value")
        
        # Get statistics
        stats = await manager.get_statistics()
        
        assert stats["total_secrets"] == 2
        assert stats["audit_log_entries"] > 0
        assert stats["encryption_enabled"] is True
        assert stats["auto_rotation_enabled"] is True
    
    def test_generate_secret_value(self, manager):
        """Test generating secret values"""
        # String type
        string_value = manager._generate_secret_value(SecretType.STRING)
        assert isinstance(string_value, str)
        assert len(string_value) > 0
        
        # API Key type
        api_key_value = manager._generate_secret_value(SecretType.API_KEY)
        assert api_key_value.startswith("sk-")
        assert len(api_key_value) > 10
        
        # Database URL type
        db_url = manager._generate_secret_value(SecretType.DATABASE_URL)
        assert "postgresql://" in db_url
        assert "localhost:5432" in db_url
    
    def test_calculate_checksum(self, manager):
        """Test calculating checksum"""
        checksum1 = manager._calculate_checksum("test-value")
        checksum2 = manager._calculate_checksum("test-value")
        checksum3 = manager._calculate_checksum("different-value")
        
        assert checksum1 == checksum2
        assert checksum1 != checksum3


class TestSecretsManagerEncryption:
    """Test encryption functionality"""
    
    @pytest.mark.asyncio
    async def test_encryption_enabled(self):
        """Test encryption is enabled by default"""
        config = SecretConfig(encryption_enabled=True)
        manager = SecretsManager("kubernetes", config)
        
        assert manager._encryption_key is not None
        assert manager._cipher is not None
    
    @pytest.mark.asyncio
    async def test_encryption_disabled(self):
        """Test encryption can be disabled"""
        config = SecretConfig(encryption_enabled=False)
        manager = SecretsManager("kubernetes", config)
        
        assert manager._encryption_key is None
    
    @pytest.mark.asyncio
    async def test_encrypt_decrypt_secret(self):
        """Test encrypting and decrypting secret"""
        config = SecretConfig(encryption_enabled=True)
        manager = SecretsManager("kubernetes", config)
        
        original_value = "my-secret-value"
        encrypted = manager._encrypt_secret(original_value)
        decrypted = manager._decrypt_secret(encrypted)
        
        assert encrypted != original_value
        assert decrypted == original_value
    
    @pytest.mark.asyncio
    async def test_encrypt_json_secret(self):
        """Test encrypting JSON secret"""
        config = SecretConfig(encryption_enabled=True)
        manager = SecretsManager("kubernetes", config)
        
        json_value = {"key": "value", "number": 123}
        import json
        json_string = json.dumps(json_value)
        encrypted = manager._encrypt_secret(json_string)
        decrypted = manager._decrypt_secret(encrypted)
        
        assert encrypted != json_string
        assert json.loads(decrypted) == json_value


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
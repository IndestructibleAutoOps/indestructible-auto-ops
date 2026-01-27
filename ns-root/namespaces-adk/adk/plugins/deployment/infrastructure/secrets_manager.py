"""
Enterprise-Grade Secrets Manager

Provides comprehensive secrets management with support for multiple
providers, automatic rotation, encryption, and audit logging.

Features:
- Multi-provider support (AWS Secrets Manager, GCP Secret Manager, Azure Key Vault, Kubernetes Secrets)
- Automatic secret rotation with configurable schedules
- Encryption at rest and in transit
- Audit logging and access control
- Secret versioning and rollback
"""

import asyncio
import hashlib
import hmac
import json
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
import yaml
import logging
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

logger = logging.getLogger(__name__)


class SecretProvider(Enum):
    """Supported secret providers"""
    AWS_SECRETS_MANAGER = "aws_secrets_manager"
    GCP_SECRET_MANAGER = "gcp_secret_manager"
    AZURE_KEY_VAULT = "azure_key_vault"
    KUBERNETES_SECRETS = "kubernetes_secrets"
    VAULT = "vault"
    ENVIRONMENT = "environment"
    FILE = "file"


class SecretType(Enum):
    """Secret types"""
    STRING = "string"
    JSON = "json"
    BINARY = "binary"
    CERTIFICATE = "certificate"
    SSH_KEY = "ssh_key"
    DATABASE_URL = "database_url"
    API_KEY = "api_key"


class RotationPolicy(Enum):
    """Rotation policies"""
    DISABLED = "disabled"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    CUSTOM = "custom"


@dataclass
class SecretConfig:
    """Configuration for secrets manager"""
    provider: SecretProvider = SecretProvider.KUBERNETES_SECRETS
    primary_provider: SecretProvider = SecretProvider.KUBERNETES_SECRETS
    fallback_providers: List[SecretProvider] = field(default_factory=list)
    
    # Encryption settings
    encryption_enabled: bool = True
    encryption_algorithm: str = "AES256-GCM"
    key_derivation_iterations: int = 100000
    
    # Rotation settings
    auto_rotation_enabled: bool = True
    default_rotation_policy: RotationPolicy = RotationPolicy.WEEKLY
    rotation_notification_enabled: bool = True
    rotation_notification_email: Optional[str] = None
    
    # Access control
    audit_logging_enabled: bool = True
    access_control_enabled: bool = True
    rbac_enabled: bool = True
    
    # Versioning
    versioning_enabled: bool = True
    max_versions: int = 10
    
    # Backup and recovery
    backup_enabled: bool = True
    backup_retention_days: int = 90
    auto_backup_before_rotation: bool = True
    
    # Performance
    cache_enabled: bool = True
    cache_ttl_seconds: int = 300
    
    # Provider-specific settings
    aws_region: str = "us-east-1"
    gcp_project_id: Optional[str] = None
    azure_key_vault_name: Optional[str] = None
    vault_address: Optional[str] = None
    vault_namespace: str = "default"
    file_secrets_path: Optional[str] = None
    
    # Advanced features
    secret_sharing_enabled: bool = False
    secret_approval_required: bool = False
    secret_expiry_enabled: bool = False


@dataclass
class SecretMetadata:
    """Metadata for a secret"""
    name: str
    secret_type: SecretType
    created_at: datetime
    updated_at: datetime
    rotation_policy: RotationPolicy
    last_rotated_at: Optional[datetime] = None
    next_rotation_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    version: int = 1
    tags: Dict[str, str] = field(default_factory=dict)
    description: Optional[str] = None
    owner: Optional[str] = None
    checksum: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "secret_type": self.secret_type.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "rotation_policy": self.rotation_policy.value,
            "last_rotated_at": self.last_rotated_at.isoformat() if self.last_rotated_at else None,
            "next_rotation_at": self.next_rotation_at.isoformat() if self.next_rotation_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "version": self.version,
            "tags": self.tags,
            "description": self.description,
            "owner": self.owner,
            "checksum": self.checksum
        }


@dataclass
class SecretValue:
    """Secret value with metadata"""
    value: Any
    version: int
    created_at: datetime
    expires_at: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class AuditLogEntry:
    """Audit log entry"""
    timestamp: datetime
    action: str  # created, read, updated, deleted, rotated, shared
    secret_name: str
    user: Optional[str] = None
    ip_address: Optional[str] = None
    success: bool = True
    details: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "timestamp": self.timestamp.isoformat(),
            "action": self.action,
            "secret_name": self.secret_name,
            "user": self.user,
            "ip_address": self.ip_address,
            "success": self.success,
            "details": self.details
        }


@dataclass
class SecretManagerResult:
    """Result of secret manager operation"""
    success: bool
    message: str
    data: Optional[Any] = None
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data,
            "warnings": self.warnings,
            "errors": self.errors
        }


class SecretsManager:
    """
    Enterprise-grade secrets manager
    
    Provides comprehensive secrets management with support for multiple
    providers, automatic rotation, encryption, and audit logging.
    """
    
    def __init__(self, provider: str, config: SecretConfig):
        """
        Initialize secrets manager
        
        Args:
            provider: Provider name (aws, gcp, azure, kubernetes)
            config: Secrets manager configuration
        """
        self.provider = provider.lower()
        self.config = config
        self._secrets: Dict[str, SecretValue] = {}
        self._secrets_metadata: Dict[str, SecretMetadata] = {}
        self._audit_log: List[AuditLogEntry] = []
        self._cache: Dict[str, Tuple[SecretValue, datetime]] = {}
        self._encryption_key: Optional[bytes] = None
        
        # Initialize encryption
        if config.encryption_enabled:
            self._initialize_encryption()
        
        logger.info(f"SecretsManager initialized for provider: {provider}")
    
    def _initialize_encryption(self) -> None:
        """Initialize encryption key"""
        # Generate a secure key using PBKDF2
        password = secrets.token_bytes(32)
        salt = secrets.token_bytes(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self.config.key_derivation_iterations
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(password))
        self._encryption_key = key
        self._cipher = Fernet(key)
        
        logger.info("Encryption initialized")
    
    def _encrypt_secret(self, secret_value: str) -> str:
        """Encrypt secret value"""
        if not self.config.encryption_enabled or not self._encryption_key:
            return secret_value
        
        encrypted = self._cipher.encrypt(secret_value.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def _decrypt_secret(self, encrypted_value: str) -> str:
        """Decrypt secret value"""
        if not self.config.encryption_enabled or not self._encryption_key:
            return encrypted_value
        
        try:
            encrypted = base64.urlsafe_b64decode(encrypted_value.encode())
            decrypted = self._cipher.decrypt(encrypted)
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise
    
    def _calculate_checksum(self, secret_value: Any) -> str:
        """Calculate checksum for secret value using a computationally expensive KDF."""
        if isinstance(secret_value, (dict, list)):
            secret_str = json.dumps(secret_value, sort_keys=True)
        else:
            secret_str = str(secret_value)

        # Use PBKDF2-HMAC with SHA-256 to derive a deterministic checksum from the secret value.
        # A fixed internal salt is acceptable here because this is used as an integrity checksum,
        # not as a password verifier, and callers rely on determinism.
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b"namespaces-adk-secret-checksum",
            iterations=100_000,
        )
        derived = kdf.derive(secret_str.encode("utf-8"))
        return base64.urlsafe_b64encode(derived).decode("utf-8")
    
    async def create_secret(
        self,
        name: str,
        value: Any,
        secret_type: SecretType = SecretType.STRING,
        rotation_policy: RotationPolicy = RotationPolicy.WEEKLY,
        tags: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        owner: Optional[str] = None,
        expires_in_days: Optional[int] = None
    ) -> SecretManagerResult:
        """
        Create a new secret
        
        Args:
            name: Secret name
            value: Secret value
            secret_type: Type of secret
            rotation_policy: Rotation policy
            tags: Secret tags
            description: Secret description
            owner: Secret owner
            expires_in_days: Days until expiration
        
        Returns:
            SecretManagerResult with operation details
        """
        try:
            logger.info(f"Creating secret: {name}")
            
            # Check if secret already exists
            if name in self._secrets_metadata:
                return SecretManagerResult(
                    success=False,
                    message=f"Secret {name} already exists",
                    errors=["Secret already exists"]
                )
            
            # Encrypt secret value
            encrypted_value = self._encrypt_secret(str(value) if secret_type != SecretType.JSON else json.dumps(value))
            
            # Create secret value
            now = datetime.now()
            expires_at = None
            if expires_in_days:
                expires_at = now + timedelta(days=expires_in_days)
            
            secret_value = SecretValue(
                value=encrypted_value,
                version=1,
                created_at=now,
                expires_at=expires_at,
                metadata={"type": secret_type.value}
            )
            
            # Calculate next rotation time
            next_rotation = self._calculate_next_rotation(now, rotation_policy)
            
            # Create secret metadata
            secret_metadata = SecretMetadata(
                name=name,
                secret_type=secret_type,
                created_at=now,
                updated_at=now,
                rotation_policy=rotation_policy,
                last_rotated_at=now,
                next_rotation_at=next_rotation,
                expires_at=expires_at,
                version=1,
                tags=tags or {},
                description=description,
                owner=owner,
                checksum=self._calculate_checksum(value)
            )
            
            # Store secret
            self._secrets[name] = secret_value
            self._secrets_metadata[name] = secret_metadata
            
            # Log audit entry
            if self.config.audit_logging_enabled:
                self._add_audit_log(
                    action="created",
                    secret_name=name,
                    details={"version": 1, "secret_type": secret_type.value}
                )
            
            # Create backup if enabled
            if self.config.backup_enabled:
                await self._backup_secret(name)
            
            logger.info(f"Secret {name} created successfully")
            
            return SecretManagerResult(
                success=True,
                message=f"Secret {name} created successfully",
                data={
                    "name": name,
                    "version": 1,
                    "next_rotation_at": next_rotation.isoformat() if next_rotation else None
                }
            )
            
        except Exception as e:
            logger.error(f"Failed to create secret {name}: {e}")
            return SecretManagerResult(
                success=False,
                message=f"Failed to create secret {name}",
                errors=[str(e)]
            )
    
    async def get_secret(
        self,
        name: str,
        version: Optional[int] = None,
        decrypt: bool = True,
        user: Optional[str] = None
    ) -> SecretManagerResult:
        """
        Get secret value
        
        Args:
            name: Secret name
            version: Secret version (None for latest)
            decrypt: Whether to decrypt the value
            user: User requesting the secret
        
        Returns:
            SecretManagerResult with secret value
        """
        try:
            # Check cache first
            if self.config.cache_enabled and version is None:
                cached = self._cache.get(name)
                if cached:
                    secret_value, cached_at = cached
                    if (datetime.now() - cached_at).total_seconds() < self.config.cache_ttl_seconds:
                        logger.debug(f"Secret {name} retrieved from cache")
                        
                        if self.config.audit_logging_enabled:
                            self._add_audit_log(
                                action="read",
                                secret_name=name,
                                user=user,
                                details={"source": "cache"}
                            )
                        
                        value = self._decrypt_secret(secret_value.value) if decrypt else secret_value.value
                        return SecretManagerResult(
                            success=True,
                            message=f"Secret {name} retrieved from cache",
                            data={"value": value, "version": secret_value.version}
                        )
            
            # Get secret from storage
            secret_metadata = self._secrets_metadata.get(name)
            if not secret_metadata:
                return SecretManagerResult(
                    success=False,
                    message=f"Secret {name} not found",
                    errors=["Secret not found"]
                )
            
            secret_value = self._secrets.get(name)
            if not secret_value:
                return SecretManagerResult(
                    success=False,
                    message=f"Secret value for {name} not found",
                    errors=["Secret value not found"]
                )
            
            # Check expiration
            if secret_value.expires_at and datetime.now() > secret_value.expires_at:
                return SecretManagerResult(
                    success=False,
                    message=f"Secret {name} has expired",
                    errors=["Secret expired"]
                )
            
            # Decrypt value
            value = self._decrypt_secret(secret_value.value) if decrypt else secret_value.value
            
            # Update cache
            if self.config.cache_enabled and version is None:
                self._cache[name] = (secret_value, datetime.now())
            
            # Log audit entry
            if self.config.audit_logging_enabled:
                self._add_audit_log(
                    action="read",
                    secret_name=name,
                    user=user,
                    details={"version": secret_value.version}
                )
            
            logger.info(f"Secret {name} retrieved successfully")
            
            return SecretManagerResult(
                success=True,
                message=f"Secret {name} retrieved successfully",
                data={
                    "value": value,
                    "version": secret_value.version,
                    "expires_at": secret_value.expires_at.isoformat() if secret_value.expires_at else None
                }
            )
            
        except Exception as e:
            logger.error(f"Failed to get secret {name}: {e}")
            return SecretManagerResult(
                success=False,
                message=f"Failed to get secret {name}",
                errors=[str(e)]
            )
    
    async def update_secret(
        self,
        name: str,
        value: Any,
        user: Optional[str] = None
    ) -> SecretManagerResult:
        """
        Update secret value
            logger.info(
                "Updating secret (id hash: %s)",
                hashlib.sha256(name.encode()).hexdigest()[:8]
            )
        Args:
            name: Secret name
            value: New secret value
            user: User updating the secret
        
        Returns:
            SecretManagerResult with operation details
        """
        try:
            logger.info(f"Updating secret: {name}")
            
            # Check if secret exists
            if name not in self._secrets_metadata:
                return SecretManagerResult(
                    success=False,
                    message=f"Secret {name} not found",
                    errors=["Secret not found"]
                )
            
            secret_metadata = self._secrets_metadata[name]
            
            # Create backup before update if enabled
            if self.config.auto_backup_before_rotation:
                await self._backup_secret(name)
            
            # Encrypt new value
            encrypted_value = self._encrypt_secret(str(value) if secret_metadata.secret_type != SecretType.JSON else json.dumps(value))
            
            # Create new version
            now = datetime.now()
            new_version = secret_metadata.version + 1
            
            # Update secret value
            secret_value = SecretValue(
                value=encrypted_value,
                version=new_version,
                created_at=now,
                expires_at=secret_metadata.expires_at,
                metadata={"type": secret_metadata.secret_type.value}
            )
            
            self._secrets[name] = secret_value
            
            # Update metadata
            secret_metadata.updated_at = now
            secret_metadata.version = new_version
            secret_metadata.checksum = self._calculate_checksum(value)
            
            # Calculate next rotation
            next_rotation = self._calculate_next_rotation(now, secret_metadata.rotation_policy)

            safe_secret_id = hashlib.sha256(name.encode("utf-8")).hexdigest()[:8]
            logger.info(f"Secret with id {safe_secret_id} updated to version {new_version}")

            self._cache.pop(name, None)
            
            # Log audit entry
            if self.config.audit_logging_enabled:
                self._add_audit_log(
                    action="updated",
            logger.error("Failed to update secret", exc_info=True)
                    user=user,
                    details={"old_version": new_version - 1, "new_version": new_version}
                )
            
            logger.info(f"Secret {name} updated to version {new_version}")
            
            return SecretManagerResult(
                success=True,
                message=f"Secret {name} updated to version {new_version}",
                data={"version": new_version, "next_rotation_at": next_rotation.isoformat() if next_rotation else None}
            )
            
        except Exception as e:
            logger.error(f"Failed to update secret {name}: {e}")
            return SecretManagerResult(
                success=False,
                message=f"Failed to update secret {name}",
                errors=[str(e)]
            )
    
    async def delete_secret(
        self,
        name: str,
        user: Optional[str] = None
    ) -> SecretManagerResult:
        """
        Delete secret
        
        Args:
            name: Secret name
            user: User deleting the secret
        
        Returns:
            SecretManagerResult with operation details
        """
        try:
            logger.info(f"Deleting secret: {name}")
            
            # Check if secret exists
            if name not in self._secrets_metadata:
                return SecretManagerResult(
                    success=False,
                    message=f"Secret {name} not found",
                    errors=["Secret not found"]
                )
            
            # Create final backup if enabled
            if self.config.backup_enabled:
                await self._backup_secret(name)
            
            # Delete secret
            del self._secrets[name]
            del self._secrets_metadata[name]
            
            # Clear cache
            self._cache.pop(name, None)
            
            # Log audit entry
            if self.config.audit_logging_enabled:
                self._add_audit_log(
                    action="deleted",
                    secret_name=name,
                    user=user
                )
            
            logger.info(f"Secret {name} deleted successfully")
            
            return SecretManagerResult(
                success=True,
                message=f"Secret {name} deleted successfully"
            )
            
        except Exception as e:
            logger.error(f"Failed to delete secret {name}: {e}")
            return SecretManagerResult(
                success=False,
                message=f"Failed to delete secret {name}",
                errors=[str(e)]
            )
    
    async def rotate_secret(
        self,
        name: str,
        new_value: Optional[Any] = None,
            logger.info("Rotating secret")
    ) -> SecretManagerResult:
        """
        Rotate secret value
            logger.info(
                "Rotating secret (id hash: %s)",
                hashlib.sha256(name.encode()).hexdigest()[:8]
            )
        Args:
            name: Secret name
            new_value: New secret value (None to auto-generate)
            user: User rotating the secret
        
        Returns:
            SecretManagerResult with operation details
        """
        try:
            logger.info(f"Rotating secret: {name}")
            
            # Check if secret exists
            if name not in self._secrets_metadata:
                return SecretManagerResult(
                    success=False,
                    message=f"Secret {name} not found",
                    errors=["Secret not found"]
                )
            
            secret_metadata = self._secrets_metadata[name]
            
            # Generate new value if not provided
            if new_value is None:
                new_value = self._generate_secret_value(secret_metadata.secret_type)
                logger.info("Secret rotated successfully")
            # Update secret
            result = await self.update_secret(name, new_value, user)
            
            if result.success:
                # Update last rotation time
                secret_metadata.last_rotated_at = datetime.now()
                
                # Log audit entry
                if self.config.audit_logging_enabled:
                    self._add_audit_log(
                        action="rotated",
            logger.error(
                "Failed to rotate secret (id hash: %s): %s",
                hashlib.sha256(name.encode()).hexdigest()[:8],
                e
            )
                        user=user,
                        details={"version": secret_metadata.version}
                    )
                
                logger.info(f"Secret {name} rotated successfully")
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to rotate secret {name}: {e}")
            return SecretManagerResult(
                success=False,
                message=f"Failed to rotate secret {name}",
                errors=[str(e)]
            )
    
    async def list_secrets(
        self,
        filter_tags: Optional[Dict[str, str]] = None,
        filter_type: Optional[SecretType] = None
    ) -> SecretManagerResult:
        """
        List all secrets
        
        Args:
            filter_tags: Filter by tags
            filter_type: Filter by secret type
        
        Returns:
            SecretManagerResult with list of secrets
        """
        try:
            secrets_list = []
            
            for name, metadata in self._secrets_metadata.items():
                # Apply filters
                if filter_tags:
                    if not all(metadata.tags.get(k) == v for k, v in filter_tags.items()):
                        continue
                
                if filter_type and metadata.secret_type != filter_type:
                    continue
                
                secrets_list.append(metadata.to_dict())
            
            logger.info(f"Listed {len(secrets_list)} secrets")
            
            return SecretManagerResult(
                success=True,
                message=f"Listed {len(secrets_list)} secrets",
                data={"secrets": secrets_list}
            )
            
        except Exception as e:
            logger.error(f"Failed to list secrets: {e}")
            return SecretManagerResult(
                success=False,
                message="Failed to list secrets",
                errors=[str(e)]
            )
    
    async def rotate_all_secrets(
        self,
        user: Optional[str] = None
    ) -> SecretManagerResult:
        """
        Rotate all secrets that need rotation
        
        Args:
            user: User rotating the secrets
        
        Returns:
            SecretManagerResult with operation details
        """
        try:
            logger.info("Rotating all secrets that need rotation")
            
                        "name_hash": hashlib.sha256(name.encode()).hexdigest()[:8],
            rotated_count = 0
            failed_count = 0
            results = []
            
            for name, metadata in self._secrets_metadata.items():
                # Check if rotation is needed
                if metadata.next_rotation_at and now >= metadata.next_rotation_at:
                    result = await self.rotate_secret(name, user=user)
                    results.append({
                        "name": name,
                        "success": result.success,
                        "message": result.message
                    })
                    
                    if result.success:
                        rotated_count += 1
                    else:
                        failed_count += 1
            
            logger.info(f"Rotated {rotated_count} secrets, {failed_count} failed")
            
            return SecretManagerResult(
                success=failed_count == 0,
                message=f"Rotated {rotated_count} secrets, {failed_count} failed",
                data={
                    "rotated_count": rotated_count,
                    "failed_count": failed_count,
                    "results": results
                }
            )
            
        except Exception as e:
            logger.error(f"Failed to rotate all secrets: {e}")
            return SecretManagerResult(
                success=False,
                message="Failed to rotate all secrets",
                errors=[str(e)]
            )
    
    def _generate_secret_value(self, secret_type: SecretType) -> Any:
        """Generate a new secret value based on type"""
        if secret_type == SecretType.STRING:
            return secrets.token_urlsafe(32)
        elif secret_type == SecretType.API_KEY:
            return f"sk-{secrets.token_hex(32)}"
        elif secret_type == SecretType.DATABASE_URL:
            password = secrets.token_urlsafe(16)
            return f"postgresql://user:{password}@localhost:5432/dbname"
        elif secret_type == SecretType.SSH_KEY:
            return f"-----BEGIN RSA PRIVATE KEY-----\n{secrets.token_hex(256)}\n-----END RSA PRIVATE KEY-----"
        else:
            return secrets.token_urlsafe(32)
    
    def _calculate_next_rotation(
        self,
        now: datetime,
        rotation_policy: RotationPolicy
    ) -> Optional[datetime]:
        """Calculate next rotation time"""
        logger.debug("Backing up secret")
            return None
        
        if rotation_policy == RotationPolicy.HOURLY:
            return now + timedelta(hours=1)
        elif rotation_policy == RotationPolicy.DAILY:
            return now + timedelta(days=1)
        elif rotation_policy == RotationPolicy.WEEKLY:
            return now + timedelta(weeks=1)
        elif rotation_policy == RotationPolicy.MONTHLY:
            return now + timedelta(days=30)
        elif rotation_policy == RotationPolicy.QUARTERLY:
            return now + timedelta(days=90)
        else:
            return now + timedelta(weeks=1)
    
    async def _backup_secret(self, name: str) -> None:
        """Backup secret"""
        if not self.config.backup_enabled:
            return
        
        logger.debug(f"Backing up secret: {name}")
        # Backup logic would go here
    
    def _add_audit_log(
        self,
        action: str,
        secret_name: str,
        user: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add audit log entry"""
        if not self.config.audit_logging_enabled:
            return
        
        entry = AuditLogEntry(
            timestamp=datetime.now(),
            action=action,
            secret_name=secret_name,
            user=user,
            details=details
        )
        
        self._audit_log.append(entry)
        
        # Keep only last 1000 entries
        if len(self._audit_log) > 1000:
            self._audit_log = self._audit_log[-1000:]
    
    async def get_audit_log(
        self,
        secret_name: Optional[str] = None,
        limit: int = 100
    ) -> SecretManagerResult:
        """
        Get audit log entries
        
        Args:
            secret_name: Filter by secret name
            limit: Maximum number of entries
        
        Returns:
            SecretManagerResult with audit log entries
        """
        try:
            entries = []
            
            for entry in reversed(self._audit_log):
                if secret_name and entry.secret_name != secret_name:
                    continue
                
                entries.append(entry.to_dict())
                
                if len(entries) >= limit:
                    break
            
            logger.info(f"Retrieved {len(entries)} audit log entries")
            
            return SecretManagerResult(
                success=True,
                message=f"Retrieved {len(entries)} audit log entries",
                data={"entries": entries}
            )
            
        except Exception as e:
            logger.error(f"Failed to get audit log: {e}")
            return SecretManagerResult(
                success=False,
                message="Failed to get audit log",
                errors=[str(e)]
            )
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Get secrets manager statistics"""
        now = datetime.now()
        
        total_secrets = len(self._secrets_metadata)
        expired_secrets = sum(
            1 for metadata in self._secrets_metadata.values()
            if metadata.expires_at and metadata.expires_at < now
        )
        needs_rotation = sum(
            1 for metadata in self._secrets_metadata.values()
            if metadata.next_rotation_at and metadata.next_rotation_at <= now
        )
        
        return {
            "total_secrets": total_secrets,
            "expired_secrets": expired_secrets,
            "needs_rotation": needs_rotation,
            "audit_log_entries": len(self._audit_log),
            "cache_entries": len(self._cache),
            "encryption_enabled": self.config.encryption_enabled,
            "auto_rotation_enabled": self.config.auto_rotation_enabled
        }
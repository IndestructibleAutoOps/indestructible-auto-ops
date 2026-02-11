"""Role and permission value objects for RBAC."""
from __future__ import annotations

from enum import Enum


class Permission(str, Enum):
    """System permissions."""
    # User
    USER_READ = "user:read"
    USER_WRITE = "user:write"
    USER_DELETE = "user:delete"
    USER_ADMIN = "user:admin"
    # Quantum
    QUANTUM_EXECUTE = "quantum:execute"
    QUANTUM_READ = "quantum:read"
    # AI
    AI_EXECUTE = "ai:execute"
    AI_READ = "ai:read"
    AI_MANAGE = "ai:manage"
    # Scientific
    SCIENTIFIC_EXECUTE = "scientific:execute"
    SCIENTIFIC_READ = "scientific:read"
    # Admin
    ADMIN_FULL = "admin:full"
    ADMIN_CONFIG = "admin:config"
    ADMIN_AUDIT = "admin:audit"
    # System
    SYSTEM_METRICS = "system:metrics"


class UserRole(str, Enum):
    """User roles with hierarchical permissions."""
    ADMIN = "admin"
    OPERATOR = "operator"
    SCIENTIST = "scientist"
    DEVELOPER = "developer"
    VIEWER = "viewer"


class RolePermissions:
    """Maps roles to their granted permissions."""

    _ROLE_MAP: dict[UserRole, set[Permission]] = {
        UserRole.VIEWER: {
            Permission.USER_READ,
            Permission.QUANTUM_READ,
            Permission.AI_READ,
            Permission.SCIENTIFIC_READ,
        },
        UserRole.DEVELOPER: {
            Permission.USER_READ,
            Permission.USER_WRITE,
            Permission.QUANTUM_READ,
            Permission.QUANTUM_EXECUTE,
            Permission.AI_READ,
            Permission.AI_EXECUTE,
            Permission.SCIENTIFIC_READ,
            Permission.SCIENTIFIC_EXECUTE,
        },
        UserRole.SCIENTIST: {
            Permission.USER_READ,
            Permission.USER_WRITE,
            Permission.QUANTUM_READ,
            Permission.QUANTUM_EXECUTE,
            Permission.AI_READ,
            Permission.AI_EXECUTE,
            Permission.AI_MANAGE,
            Permission.SCIENTIFIC_READ,
            Permission.SCIENTIFIC_EXECUTE,
        },
        UserRole.OPERATOR: {
            Permission.USER_READ,
            Permission.USER_WRITE,
            Permission.QUANTUM_READ,
            Permission.QUANTUM_EXECUTE,
            Permission.AI_READ,
            Permission.AI_EXECUTE,
            Permission.AI_MANAGE,
            Permission.SCIENTIFIC_READ,
            Permission.SCIENTIFIC_EXECUTE,
            Permission.SYSTEM_METRICS,
            Permission.ADMIN_AUDIT,
        },
        UserRole.ADMIN: set(Permission),
    }

    @classmethod
    def get_permissions(cls, role: UserRole) -> set[Permission]:
        return cls._ROLE_MAP.get(role, set())

    @classmethod
    def has_permission(cls, role: UserRole, permission: Permission) -> bool:
        return permission in cls.get_permissions(role)

    @classmethod
    def has_any_permission(cls, role: UserRole, permissions: set[Permission]) -> bool:
        return bool(cls.get_permissions(role) & permissions)
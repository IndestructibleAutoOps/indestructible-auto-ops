"""SQLAlchemy ORM models — infrastructure persistence layer."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Enum, Index, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.persistence.database import Base


class UserModel(Base):
    """User table — maps to domain User aggregate."""

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(254), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    role: Mapped[str] = mapped_column(
        Enum("admin", "operator", "scientist", "developer", "viewer", name="user_role_enum"),
        nullable=False,
        default="viewer",
        index=True,
    )
    status: Mapped[str] = mapped_column(
        Enum("active", "suspended", "deleted", "pending", name="user_status_enum"),
        nullable=False,
        default="active",
        index=True,
    )
    suspension_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    login_count: Mapped[int] = mapped_column(default=0)
    failed_login_count: Mapped[int] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    version: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        Index("ix_users_email_status", "email", "status"),
        Index("ix_users_role_status", "role", "status"),
    )

    def __repr__(self) -> str:
        return f"<UserModel id={self.id} username={self.username} role={self.role}>"


class QuantumJobModel(Base):
    """Quantum job execution record."""

    __tablename__ = "quantum_jobs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    algorithm: Mapped[str] = mapped_column(String(50), nullable=False)
    backend: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(
        Enum("submitted", "running", "completed", "failed", "cancelled", name="job_status_enum"),
        nullable=False,
        default="submitted",
        index=True,
    )
    parameters: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON
    result: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    execution_time_ms: Mapped[float | None] = mapped_column(nullable=True)
    num_qubits: Mapped[int] = mapped_column(default=0)
    shots: Mapped[int] = mapped_column(default=1024)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index("ix_quantum_jobs_user_status", "user_id", "status"),
    )

    def __repr__(self) -> str:
        return f"<QuantumJobModel id={self.id} algorithm={self.algorithm} status={self.status}>"


class AuditLogModel(Base):
    """Audit log for security-critical operations."""

    __tablename__ = "audit_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    action: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    resource_type: Mapped[str] = mapped_column(String(50), nullable=False)
    resource_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    details: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    __table_args__ = (
        Index("ix_audit_logs_user_action", "user_id", "action"),
        Index("ix_audit_logs_created", "created_at"),
    )
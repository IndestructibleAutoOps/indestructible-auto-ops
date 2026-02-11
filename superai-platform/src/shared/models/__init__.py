"""Shared data models — common structures used across layers."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PageRequest(BaseModel):
    """Standard pagination request."""
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=100)
    sort_by: str = Field(default="created_at")
    sort_order: str = Field(default="desc", pattern=r"^(asc|desc)$")


class PageResponse(BaseModel, Generic[T]):
    """Standard paginated response."""
    items: list[T]
    total: int
    skip: int
    limit: int
    has_next: bool = False
    total_pages: int = 1


class HealthStatus(BaseModel):
    """Service health check result."""
    status: str  # healthy | degraded | unhealthy
    timestamp: str
    version: str
    uptime_seconds: float
    checks: dict[str, Any] = Field(default_factory=dict)


class OperationResult(BaseModel):
    """Generic operation result wrapper."""
    success: bool
    message: str = ""
    data: Any = None
    errors: list[str] = Field(default_factory=list)

    @classmethod
    def ok(cls, data: Any = None, message: str = "Success") -> OperationResult:
        return cls(success=True, message=message, data=data)

    @classmethod
    def fail(cls, message: str, errors: list[str] | None = None) -> OperationResult:
        return cls(success=False, message=message, errors=errors or [])


class AuditEntry(BaseModel):
    """Audit log entry."""
    id: str
    user_id: str | None = None
    action: str
    resource_type: str
    resource_id: str | None = None
    details: dict[str, Any] = Field(default_factory=dict)
    ip_address: str | None = None
    timestamp: str


__all__ = ["PageRequest", "PageResponse", "HealthStatus", "OperationResult", "AuditEntry"]
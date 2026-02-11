"""Shared schemas — re-exports from presentation schemas for cross-layer use."""
from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any


class BaseResponse(BaseModel):
    """Standard API response wrapper."""
    success: bool = True
    data: Any = None
    message: str = ""


class ErrorSchema(BaseModel):
    """Standard error response."""
    code: str
    message: str
    details: list[dict[str, Any]] = Field(default_factory=list)


class BatchOperationResult(BaseModel):
    """Result of a batch operation."""
    total: int
    succeeded: int
    failed: int
    errors: list[dict[str, Any]] = Field(default_factory=list)


__all__ = ["BaseResponse", "ErrorSchema", "BatchOperationResult"]
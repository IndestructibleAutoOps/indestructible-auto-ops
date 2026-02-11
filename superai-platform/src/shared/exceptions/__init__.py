"""Shared exception hierarchy — re-exports domain exceptions for convenience."""
from __future__ import annotations

from src.domain.exceptions import (
    AuthenticationException,
    AuthorizationException,
    BusinessRuleViolation,
    ConcurrencyConflictException,
    DomainException,
    EntityAlreadyExistsException,
    EntityNotFoundException,
    EntityStateException,
    InvalidEmailError,
    InvalidTokenException,
    RateLimitExceededException,
    TokenExpiredException,
    WeakPasswordError,
)


class InfrastructureException(Exception):
    """Base exception for infrastructure failures."""

    def __init__(self, message: str, code: str = "INFRASTRUCTURE_ERROR") -> None:
        self.message = message
        self.code = code
        super().__init__(message)


class DatabaseConnectionError(InfrastructureException):
    def __init__(self, details: str = "") -> None:
        super().__init__(f"Database connection failed: {details}", "DB_CONNECTION_ERROR")


class CacheConnectionError(InfrastructureException):
    def __init__(self, details: str = "") -> None:
        super().__init__(f"Cache connection failed: {details}", "CACHE_CONNECTION_ERROR")


class ExternalServiceError(InfrastructureException):
    def __init__(self, service: str, details: str = "") -> None:
        super().__init__(f"External service '{service}' error: {details}", "EXTERNAL_SERVICE_ERROR")
        self.service = service


__all__ = [
    # Domain
    "DomainException",
    "EntityNotFoundException",
    "EntityAlreadyExistsException",
    "EntityStateException",
    "InvalidEmailError",
    "WeakPasswordError",
    "AuthenticationException",
    "AuthorizationException",
    "InvalidTokenException",
    "TokenExpiredException",
    "BusinessRuleViolation",
    "ConcurrencyConflictException",
    "RateLimitExceededException",
    # Infrastructure
    "InfrastructureException",
    "DatabaseConnectionError",
    "CacheConnectionError",
    "ExternalServiceError",
]
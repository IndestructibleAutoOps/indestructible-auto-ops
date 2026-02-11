"""Shared exception hierarchy for the entire platform."""
from __future__ import annotations
from typing import Any


class SuperAIBaseException(Exception):
    """Root exception for all platform errors."""
    def __init__(self, message: str = "An unexpected error occurred", code: str = "INTERNAL_ERROR", details: dict[str, Any] | None = None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)


# --- Domain Exceptions ---
class DomainException(SuperAIBaseException):
    """Base for all domain-layer errors."""
    pass

class EntityNotFoundException(DomainException):
    def __init__(self, entity: str, identifier: Any):
        super().__init__(f"{entity} with id '{identifier}' not found", "ENTITY_NOT_FOUND", {"entity": entity, "id": str(identifier)})

class DomainValidationError(DomainException):
    def __init__(self, field: str, reason: str):
        super().__init__(f"Validation failed for '{field}': {reason}", "VALIDATION_ERROR", {"field": field, "reason": reason})

class BusinessRuleViolation(DomainException):
    def __init__(self, rule: str, context: dict[str, Any] | None = None):
        super().__init__(f"Business rule violated: {rule}", "BUSINESS_RULE_VIOLATION", {"rule": rule, **(context or {})})

class ConcurrencyConflict(DomainException):
    def __init__(self, entity: str):
        super().__init__(f"Concurrency conflict on {entity}", "CONCURRENCY_CONFLICT", {"entity": entity})


# --- Application Exceptions ---
class ApplicationException(SuperAIBaseException):
    """Base for all application-layer errors."""
    pass

class UnauthorizedException(ApplicationException):
    def __init__(self, reason: str = "Authentication required"):
        super().__init__(reason, "UNAUTHORIZED")

class ForbiddenException(ApplicationException):
    def __init__(self, resource: str = "resource"):
        super().__init__(f"Access to {resource} is forbidden", "FORBIDDEN", {"resource": resource})

class RateLimitExceeded(ApplicationException):
    def __init__(self, limit: int, window: str):
        super().__init__(f"Rate limit of {limit}/{window} exceeded", "RATE_LIMIT_EXCEEDED", {"limit": limit, "window": window})


# --- Infrastructure Exceptions ---
class InfrastructureException(SuperAIBaseException):
    """Base for all infrastructure-layer errors."""
    pass

class DatabaseConnectionError(InfrastructureException):
    def __init__(self, detail: str = ""):
        super().__init__(f"Database connection failed: {detail}", "DB_CONNECTION_ERROR")

class CacheConnectionError(InfrastructureException):
    def __init__(self, detail: str = ""):
        super().__init__(f"Cache connection failed: {detail}", "CACHE_CONNECTION_ERROR")

class ExternalServiceError(InfrastructureException):
    def __init__(self, service: str, detail: str = ""):
        super().__init__(f"External service '{service}' error: {detail}", "EXTERNAL_SERVICE_ERROR", {"service": service})

class QueueConnectionError(InfrastructureException):
    def __init__(self, detail: str = ""):
        super().__init__(f"Message queue connection failed: {detail}", "QUEUE_CONNECTION_ERROR")


# --- Quantum Exceptions ---
class QuantumException(SuperAIBaseException):
    """Base for quantum computing errors."""
    pass

class QuantumCircuitError(QuantumException):
    def __init__(self, detail: str):
        super().__init__(f"Quantum circuit error: {detail}", "QUANTUM_CIRCUIT_ERROR")

class QuantumBackendError(QuantumException):
    def __init__(self, backend: str, detail: str):
        super().__init__(f"Quantum backend '{backend}' error: {detail}", "QUANTUM_BACKEND_ERROR", {"backend": backend})


# --- AI Exceptions ---
class AIException(SuperAIBaseException):
    """Base for AI/ML errors."""
    pass

class EmbeddingError(AIException):
    def __init__(self, detail: str):
        super().__init__(f"Embedding generation failed: {detail}", "EMBEDDING_ERROR")

class VectorDBError(AIException):
    def __init__(self, detail: str):
        super().__init__(f"Vector database error: {detail}", "VECTOR_DB_ERROR")

class LLMError(AIException):
    def __init__(self, model: str, detail: str):
        super().__init__(f"LLM '{model}' error: {detail}", "LLM_ERROR", {"model": model})
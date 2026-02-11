"""Global exception handlers for FastAPI."""
from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
import structlog

from src.shared.exceptions import (
    SuperAIBaseException, DomainException, ApplicationException,
    InfrastructureException, EntityNotFoundException, UnauthorizedException,
    ForbiddenException, RateLimitExceeded, DomainValidationError,
    QuantumException, AIException,
)

logger = structlog.get_logger(__name__)


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(EntityNotFoundException)
    async def entity_not_found_handler(request: Request, exc: EntityNotFoundException) -> ORJSONResponse:
        return ORJSONResponse(status_code=404, content={"error": exc.code, "message": exc.message, "details": exc.details})

    @app.exception_handler(DomainValidationError)
    async def validation_error_handler(request: Request, exc: DomainValidationError) -> ORJSONResponse:
        return ORJSONResponse(status_code=422, content={"error": exc.code, "message": exc.message, "details": exc.details})

    @app.exception_handler(UnauthorizedException)
    async def unauthorized_handler(request: Request, exc: UnauthorizedException) -> ORJSONResponse:
        return ORJSONResponse(status_code=401, content={"error": exc.code, "message": exc.message})

    @app.exception_handler(ForbiddenException)
    async def forbidden_handler(request: Request, exc: ForbiddenException) -> ORJSONResponse:
        return ORJSONResponse(status_code=403, content={"error": exc.code, "message": exc.message})

    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: RateLimitExceeded) -> ORJSONResponse:
        return ORJSONResponse(status_code=429, content={"error": exc.code, "message": exc.message, "details": exc.details})

    @app.exception_handler(DomainException)
    async def domain_handler(request: Request, exc: DomainException) -> ORJSONResponse:
        logger.warning("domain_error", error=exc.code, message=exc.message)
        return ORJSONResponse(status_code=400, content={"error": exc.code, "message": exc.message, "details": exc.details})

    @app.exception_handler(ApplicationException)
    async def application_handler(request: Request, exc: ApplicationException) -> ORJSONResponse:
        logger.warning("application_error", error=exc.code, message=exc.message)
        return ORJSONResponse(status_code=400, content={"error": exc.code, "message": exc.message})

    @app.exception_handler(QuantumException)
    async def quantum_handler(request: Request, exc: QuantumException) -> ORJSONResponse:
        logger.error("quantum_error", error=exc.code, message=exc.message)
        return ORJSONResponse(status_code=500, content={"error": exc.code, "message": exc.message, "details": exc.details})

    @app.exception_handler(AIException)
    async def ai_handler(request: Request, exc: AIException) -> ORJSONResponse:
        logger.error("ai_error", error=exc.code, message=exc.message)
        return ORJSONResponse(status_code=500, content={"error": exc.code, "message": exc.message, "details": exc.details})

    @app.exception_handler(InfrastructureException)
    async def infra_handler(request: Request, exc: InfrastructureException) -> ORJSONResponse:
        logger.error("infrastructure_error", error=exc.code, message=exc.message)
        return ORJSONResponse(status_code=503, content={"error": exc.code, "message": "Service temporarily unavailable"})

    @app.exception_handler(SuperAIBaseException)
    async def base_handler(request: Request, exc: SuperAIBaseException) -> ORJSONResponse:
        logger.error("unhandled_platform_error", error=exc.code, message=exc.message)
        return ORJSONResponse(status_code=500, content={"error": "INTERNAL_ERROR", "message": "An unexpected error occurred"})

    @app.exception_handler(Exception)
    async def global_handler(request: Request, exc: Exception) -> ORJSONResponse:
        logger.exception("unhandled_exception", error=str(exc))
        return ORJSONResponse(status_code=500, content={"error": "INTERNAL_ERROR", "message": "An unexpected error occurred"})
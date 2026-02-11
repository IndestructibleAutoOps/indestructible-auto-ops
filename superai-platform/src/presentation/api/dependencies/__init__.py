"""FastAPI dependency injection providers."""
from __future__ import annotations

from typing import Any, AsyncGenerator

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.domain.exceptions import (
    AuthenticationException,
    AuthorizationException,
    InvalidTokenException,
    TokenExpiredException,
)
from src.domain.repositories import UserRepository
from src.domain.value_objects.role import Permission
from src.infrastructure.config import get_settings
from src.infrastructure.config.settings import Settings

_bearer_scheme = HTTPBearer(auto_error=False)


async def get_db_session() -> AsyncGenerator:
    """Provide an async database session."""
    from src.infrastructure.persistence.database import async_session_factory
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_user_repository(session=Depends(get_db_session)) -> UserRepository:
    """Provide a UserRepository instance."""
    from src.infrastructure.persistence.repositories import SQLAlchemyUserRepository
    return SQLAlchemyUserRepository(session)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
) -> dict[str, Any]:
    """Extract and validate the current user from JWT token."""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "UNAUTHORIZED", "message": "Missing authentication token"},
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        from src.application.services import AuthService
        auth = AuthService()
        payload = auth.verify_access_token(credentials.credentials)
        return {
            "user_id": payload.get("user_id", ""),
            "username": payload.get("sub", ""),
            "role": payload.get("role", "viewer"),
        }
    except TokenExpiredException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "TOKEN_EXPIRED", "message": "Token has expired"},
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (InvalidTokenException, AuthenticationException):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "INVALID_TOKEN", "message": "Invalid or malformed token"},
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_permission(permission: Permission):
    """Dependency factory: require a specific permission."""

    async def _check(current_user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
        from src.infrastructure.security import RBACEnforcer
        try:
            RBACEnforcer.check_permission(current_user["role"], permission)
        except AuthorizationException as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": "FORBIDDEN", "message": e.message},
            )
        return current_user

    return _check


def require_admin():
    """Dependency: require admin role."""
    return require_permission(Permission.ADMIN_FULL)


def get_client_ip(request: Request) -> str:
    """Extract client IP from request, respecting X-Forwarded-For."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


__all__ = [
    "get_db_session",
    "get_user_repository",
    "get_current_user",
    "require_permission",
    "require_admin",
    "get_client_ip",
]
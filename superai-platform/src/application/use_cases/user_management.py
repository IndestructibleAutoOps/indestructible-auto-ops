"""User management use cases."""
from __future__ import annotations

from typing import Any

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CreateUserUseCase:
    async def execute(self, username: str, email: str, password: str, full_name: str, role: str) -> dict[str, Any]:
        from src.domain.entities.user import User, UserRole
        hashed = pwd_context.hash(password)
        user = User.create(username=username, email=email, hashed_password=hashed, full_name=full_name, role=UserRole(role))
        return {"id": user.id, "username": user.username, "email": user.email.value, "full_name": user.full_name, "role": user.role.value, "status": user.status.value, "created_at": user.created_at.isoformat()}


class AuthenticateUserUseCase:
    async def execute(self, username: str, password: str) -> dict[str, Any]:
        from datetime import datetime, timedelta, timezone
        from jose import jwt
        from src.infrastructure.config import get_settings
        settings = get_settings()
        access_token = jwt.encode({"sub": username, "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.jwt.expiration_minutes), "iss": settings.jwt.issuer}, settings.jwt.secret_key, algorithm=settings.jwt.algorithm)
        refresh_token = jwt.encode({"sub": username, "exp": datetime.now(timezone.utc) + timedelta(days=settings.jwt.refresh_expiration_days), "type": "refresh"}, settings.jwt.secret_key, algorithm=settings.jwt.algorithm)
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer", "expires_in": settings.jwt.expiration_minutes * 60}


class ListUsersUseCase:
    async def execute(self, skip: int, limit: int, search: str | None) -> dict[str, Any]:
        return {"items": [], "total": 0, "skip": skip, "limit": limit}


class GetUserUseCase:
    async def execute(self, user_id: str) -> dict[str, Any]:
        from src.shared.exceptions import EntityNotFoundException
        raise EntityNotFoundException("User", user_id)


class UpdateUserUseCase:
    async def execute(self, user_id: str, **kwargs: Any) -> dict[str, Any]:
        from src.shared.exceptions import EntityNotFoundException
        raise EntityNotFoundException("User", user_id)


class DeleteUserUseCase:
    async def execute(self, user_id: str) -> None:
        pass


class ActivateUserUseCase:
    async def execute(self, user_id: str) -> dict[str, Any]:
        from src.shared.exceptions import EntityNotFoundException
        raise EntityNotFoundException("User", user_id)


class SuspendUserUseCase:
    async def execute(self, user_id: str, reason: str = "") -> dict[str, Any]:
        from src.shared.exceptions import EntityNotFoundException
        raise EntityNotFoundException("User", user_id)
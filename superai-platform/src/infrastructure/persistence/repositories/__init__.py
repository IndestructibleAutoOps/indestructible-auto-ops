"""SQLAlchemy repository implementations — infrastructure adapters for domain ports."""
from __future__ import annotations

from typing import Any

from sqlalchemy import func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.user import User, UserRole, UserStatus
from src.domain.exceptions import EntityNotFoundException, EntityAlreadyExistsException
from src.domain.repositories import UserRepository
from src.domain.value_objects.email import Email
from src.domain.value_objects.password import HashedPassword
from src.infrastructure.persistence.models import UserModel


class SQLAlchemyUserRepository(UserRepository):
    """Concrete user repository backed by PostgreSQL via SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_id(self, entity_id: str) -> User | None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == entity_id, UserModel.status != "deleted")
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def find_by_username(self, username: str) -> User | None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.username == username, UserModel.status != "deleted")
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def find_by_email(self, email: str) -> User | None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.email == email.lower(), UserModel.status != "deleted")
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def save(self, entity: Any) -> User:
        existing = await self._session.get(UserModel, entity.id)
        if existing:
            raise EntityAlreadyExistsException("User", "id", entity.id)

        # Check unique constraints
        by_username = await self.find_by_username(entity.username)
        if by_username:
            raise EntityAlreadyExistsException("User", "username", entity.username)

        by_email = await self.find_by_email(entity.email.value if hasattr(entity.email, "value") else entity.email)
        if by_email:
            raise EntityAlreadyExistsException("User", "email", str(entity.email))

        model = self._to_model(entity)
        self._session.add(model)
        await self._session.flush()
        return entity

    async def update(self, entity: Any) -> User:
        email_str = entity.email.value if hasattr(entity.email, "value") else str(entity.email)
        role_str = entity.role.value if hasattr(entity.role, "value") else str(entity.role)
        status_str = entity.status.value if hasattr(entity.status, "value") else str(entity.status)

        await self._session.execute(
            update(UserModel)
            .where(UserModel.id == entity.id)
            .values(
                username=entity.username,
                email=email_str,
                hashed_password=entity.hashed_password.value if hasattr(entity.hashed_password, "value") else entity.hashed_password,
                full_name=entity.full_name,
                role=role_str,
                status=status_str,
                suspension_reason=getattr(entity, "suspension_reason", None),
                login_count=getattr(entity, "login_count", 0),
                failed_login_count=getattr(entity, "failed_login_count", 0),
                version=entity.version,
            )
        )
        await self._session.flush()
        return entity

    async def delete(self, entity_id: str) -> None:
        await self._session.execute(
            update(UserModel)
            .where(UserModel.id == entity_id)
            .values(status="deleted", is_active=False)
        )
        await self._session.flush()

    async def exists(self, entity_id: str) -> bool:
        result = await self._session.execute(
            select(func.count()).select_from(UserModel).where(
                UserModel.id == entity_id, UserModel.status != "deleted"
            )
        )
        return (result.scalar() or 0) > 0

    async def list_users(
        self, skip: int = 0, limit: int = 20, search: str | None = None
    ) -> tuple[list[User], int]:
        query = select(UserModel).where(UserModel.status != "deleted")
        count_query = select(func.count()).select_from(UserModel).where(UserModel.status != "deleted")

        if search:
            search_filter = or_(
                UserModel.username.ilike(f"%{search}%"),
                UserModel.email.ilike(f"%{search}%"),
                UserModel.full_name.ilike(f"%{search}%"),
            )
            query = query.where(search_filter)
            count_query = count_query.where(search_filter)

        total_result = await self._session.execute(count_query)
        total = total_result.scalar() or 0

        query = query.order_by(UserModel.created_at.desc()).offset(skip).limit(limit)
        result = await self._session.execute(query)
        models = result.scalars().all()

        return [self._to_entity(m) for m in models], total

    async def count(self) -> int:
        result = await self._session.execute(
            select(func.count()).select_from(UserModel).where(UserModel.status != "deleted")
        )
        return result.scalar() or 0

    # --- Mappers ---

    @staticmethod
    def _to_entity(model: UserModel) -> User:
        return User(
            id=model.id,
            username=model.username,
            email=Email(value=model.email),
            hashed_password=HashedPassword(value=model.hashed_password),
            full_name=model.full_name,
            role=UserRole(model.role),
            status=UserStatus(model.status),
            suspension_reason=model.suspension_reason,
            login_count=model.login_count,
            failed_login_count=model.failed_login_count,
            version=model.version,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _to_model(entity: User) -> UserModel:
        email_str = entity.email.value if hasattr(entity.email, "value") else str(entity.email)
        pwd_str = entity.hashed_password.value if hasattr(entity.hashed_password, "value") else str(entity.hashed_password)
        role_str = entity.role.value if hasattr(entity.role, "value") else str(entity.role)
        status_str = entity.status.value if hasattr(entity.status, "value") else str(entity.status)

        return UserModel(
            id=entity.id,
            username=entity.username,
            email=email_str,
            hashed_password=pwd_str,
            full_name=entity.full_name,
            role=role_str,
            status=status_str,
            suspension_reason=getattr(entity, "suspension_reason", None),
            login_count=getattr(entity, "login_count", 0),
            failed_login_count=getattr(entity, "failed_login_count", 0),
            is_active=status_str == "active",
            version=entity.version,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


__all__ = ["SQLAlchemyUserRepository"]
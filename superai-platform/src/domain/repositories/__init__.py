"""Repository interfaces (ports) for the domain layer."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from src.domain.entities.base import AggregateRoot

T = TypeVar("T", bound=AggregateRoot)


class Repository(ABC, Generic[T]):
    """Abstract repository interface."""

    @abstractmethod
    async def get_by_id(self, entity_id: str) -> T | None:
        ...

    @abstractmethod
    async def save(self, entity: T) -> T:
        ...

    @abstractmethod
    async def delete(self, entity_id: str) -> bool:
        ...

    @abstractmethod
    async def list_all(self, skip: int = 0, limit: int = 100) -> list[T]:
        ...

    @abstractmethod
    async def count(self) -> int:
        ...


class UserRepository(Repository):
    """User-specific repository interface."""

    @abstractmethod
    async def get_by_email(self, email: str) -> Any | None:
        ...

    @abstractmethod
    async def get_by_username(self, username: str) -> Any | None:
        ...

    @abstractmethod
    async def search(self, query: str, skip: int = 0, limit: int = 20) -> list[Any]:
        ...

    @abstractmethod
    async def get_active_users(self, skip: int = 0, limit: int = 100) -> list[Any]:
        ...


class UnitOfWork(ABC):
    """Unit of Work pattern for transaction management."""

    @abstractmethod
    async def __aenter__(self) -> "UnitOfWork":
        ...

    @abstractmethod
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        ...

    @abstractmethod
    async def commit(self) -> None:
        ...

    @abstractmethod
    async def rollback(self) -> None:
        ...

    @property
    @abstractmethod
    def users(self) -> UserRepository:
        ...
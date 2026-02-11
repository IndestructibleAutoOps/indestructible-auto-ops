"""Specification pattern for composable business rules."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class Specification(ABC, Generic[T]):
    """Base specification for composable domain rules."""

    @abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool:
        ...

    def and_(self, other: Specification[T]) -> AndSpecification[T]:
        return AndSpecification(self, other)

    def or_(self, other: Specification[T]) -> OrSpecification[T]:
        return OrSpecification(self, other)

    def not_(self) -> NotSpecification[T]:
        return NotSpecification(self)


class AndSpecification(Specification[T]):
    def __init__(self, left: Specification[T], right: Specification[T]):
        self._left = left
        self._right = right

    def is_satisfied_by(self, candidate: T) -> bool:
        return self._left.is_satisfied_by(candidate) and self._right.is_satisfied_by(candidate)


class OrSpecification(Specification[T]):
    def __init__(self, left: Specification[T], right: Specification[T]):
        self._left = left
        self._right = right

    def is_satisfied_by(self, candidate: T) -> bool:
        return self._left.is_satisfied_by(candidate) or self._right.is_satisfied_by(candidate)


class NotSpecification(Specification[T]):
    def __init__(self, spec: Specification[T]):
        self._spec = spec

    def is_satisfied_by(self, candidate: T) -> bool:
        return not self._spec.is_satisfied_by(candidate)


# --- Concrete User Specifications ---
class IsActiveUser(Specification):
    def is_satisfied_by(self, candidate: Any) -> bool:
        return getattr(candidate, "is_active", False)


class HasRole(Specification):
    def __init__(self, role: str):
        self._role = role

    def is_satisfied_by(self, candidate: Any) -> bool:
        return getattr(candidate, "role", None) == self._role or (hasattr(candidate, "role") and getattr(candidate.role, "value", None) == self._role)


class HasPermission(Specification):
    def __init__(self, permission: str):
        self._permission = permission

    def is_satisfied_by(self, candidate: Any) -> bool:
        return hasattr(candidate, "has_permission") and candidate.has_permission(self._permission)


class IsNotLocked(Specification):
    def is_satisfied_by(self, candidate: Any) -> bool:
        return not getattr(candidate, "is_locked", True)
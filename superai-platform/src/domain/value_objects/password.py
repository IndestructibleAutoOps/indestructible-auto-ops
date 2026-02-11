"""Password value object — stores only hashed representation."""
from __future__ import annotations

from src.domain.entities.base import ValueObject


class HashedPassword(ValueObject):
    """Bcrypt-hashed password. Never stores plaintext."""

    value: str

    @classmethod
    def from_plain(cls, plain: str) -> HashedPassword:
        cls._validate_strength(plain)
        from passlib.context import CryptContext
        ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return cls(value=ctx.hash(plain))

    @classmethod
    def from_hash(cls, hashed: str) -> HashedPassword:
        return cls(value=hashed)

    def verify(self, plain: str) -> bool:
        from passlib.context import CryptContext
        ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return ctx.verify(plain, self.value)

    @staticmethod
    def _validate_strength(plain: str) -> None:
        errors: list[str] = []
        if len(plain) < 8:
            errors.append("minimum 8 characters")
        if len(plain) > 128:
            errors.append("maximum 128 characters")
        if not any(c.isupper() for c in plain):
            errors.append("at least one uppercase letter")
        if not any(c.islower() for c in plain):
            errors.append("at least one lowercase letter")
        if not any(c.isdigit() for c in plain):
            errors.append("at least one digit")
        if errors:
            from src.domain.exceptions import WeakPasswordError
            raise WeakPasswordError(errors)

    def __str__(self) -> str:
        return "***HASHED***"

    def __repr__(self) -> str:
        return "HashedPassword(***)"
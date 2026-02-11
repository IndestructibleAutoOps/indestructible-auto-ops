"""Unit tests for domain entities."""
import pytest
from src.domain.entities.base import Entity, AggregateRoot, ValueObject, DomainEvent
from src.domain.entities.user import User, UserRole, UserStatus, Email, HashedPassword


class TestValueObject:
    def test_email_valid(self):
        email = Email(value="test@example.com")
        assert email.value == "test@example.com"

    def test_email_normalized(self):
        email = Email(value="Test@Example.COM")
        assert email.value == "test@example.com"

    def test_email_invalid(self):
        with pytest.raises(ValueError):
            Email(value="not-an-email")

    def test_email_equality(self):
        e1 = Email(value="a@b.com")
        e2 = Email(value="a@b.com")
        assert e1 == e2

    def test_email_immutable(self):
        email = Email(value="a@b.com")
        with pytest.raises(Exception):
            email.value = "b@c.com"


class TestUser:
    def _make_user(self, **kwargs):
        defaults = {"username": "testuser", "email": "test@example.com", "hashed_password": "$2b$12$abcdefghijklmnopqrstuv", "full_name": "Test User", "role": UserRole.DEVELOPER}
        defaults.update(kwargs)
        return User.create(**defaults)

    def test_create_user(self):
        user = self._make_user()
        assert user.username == "testuser"
        assert user.email.value == "test@example.com"
        assert user.role == UserRole.DEVELOPER
        assert user.status == UserStatus.PENDING_VERIFICATION

    def test_create_raises_event(self):
        user = self._make_user()
        events = user.collect_events()
        assert len(events) == 1
        assert events[0].event_type == "user.created"

    def test_activate_user(self):
        user = self._make_user()
        user.collect_events()
        user.activate()
        assert user.status == UserStatus.ACTIVE
        events = user.collect_events()
        assert len(events) == 1
        assert events[0].event_type == "user.activated"

    def test_suspend_user(self):
        user = self._make_user()
        user.collect_events()
        user.suspend(reason="policy violation")
        assert user.status == UserStatus.SUSPENDED

    def test_change_role(self):
        user = self._make_user()
        user.collect_events()
        user.change_role(UserRole.ADMIN)
        assert user.role == UserRole.ADMIN

    def test_permission_management(self):
        user = self._make_user()
        user.grant_permission("quantum:execute")
        assert user.has_permission("quantum:execute")
        user.revoke_permission("quantum:execute")
        assert not user.has_permission("quantum:execute")

    def test_admin_has_all_permissions(self):
        user = self._make_user(role=UserRole.ADMIN)
        assert user.has_permission("anything")

    def test_login_failure_lockout(self):
        user = self._make_user()
        for _ in range(5):
            user.record_login_failure(max_attempts=5)
        assert user.is_locked

    def test_login_success_resets(self):
        user = self._make_user()
        user.record_login_failure()
        user.record_login_success()
        assert user.failed_login_attempts == 0

    def test_version_increment(self):
        user = self._make_user()
        v0 = user.version
        user.activate()
        assert user.version == v0 + 1

    def test_invalid_username(self):
        with pytest.raises(ValueError):
            self._make_user(username="bad user!")


class TestSpecifications:
    def test_is_active_user(self):
        from src.domain.specifications import IsActiveUser
        user = User.create(username="test", email="t@t.com", hashed_password="$2b$12$abcdefghijklmnopqrstuv")
        spec = IsActiveUser()
        assert not spec.is_satisfied_by(user)
        user.activate()
        assert spec.is_satisfied_by(user)

    def test_has_role(self):
        from src.domain.specifications import HasRole
        user = User.create(username="test", email="t@t.com", hashed_password="$2b$12$abcdefghijklmnopqrstuv", role=UserRole.SCIENTIST)
        spec = HasRole("scientist")
        assert spec.is_satisfied_by(user)

    def test_composite_specification(self):
        from src.domain.specifications import IsActiveUser, HasRole
        user = User.create(username="test", email="t@t.com", hashed_password="$2b$12$abcdefghijklmnopqrstuv", role=UserRole.ADMIN)
        user.activate()
        spec = IsActiveUser().and_(HasRole("admin"))
        assert spec.is_satisfied_by(user)
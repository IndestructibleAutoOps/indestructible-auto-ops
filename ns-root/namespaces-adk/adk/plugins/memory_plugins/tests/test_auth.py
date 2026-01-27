"""
Unit tests for Auth (Authentication Manager).

Tests for authentication functionality including user management,
token generation, and verification.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import hashlib
import sys
from pathlib import Path

# Add the module to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

try:
    from adk.security.auth import AuthManager, User, Token, AuthMethod
except ImportError as e:
    pytest.skip(f"Could not import auth module: {e}", allow_module_level=True)


class TestAuthManager:
    """Test cases for AuthManager"""

    def setup_method(self):
        """Set up test fixtures"""
        # Use a mock user store
        self.mock_user_store = Mock()
        self.auth_manager = AuthManager(user_store=self.mock_user_store)

    def teardown_method(self):
        """Tear down test fixtures"""
        pass

    def test_initialization(self):
        """Test that AuthManager initializes correctly"""
        assert self.auth_manager is not None
        assert self.auth_manager.user_store == self.mock_user_store

    def test_authenticate_valid_credentials(self):
        """Test authentication with valid credentials"""
        # Mock user retrieval
        mock_user = User(
            username="testuser",
            password_hash=hashlib.sha256("password123".encode()).hexdigest(),
            is_active=True
        )
        self.mock_user_store.get_user.return_value = mock_user
        
        result = self.auth_manager.authenticate("testuser", "password123")
        
        assert result is not None
        assert result.username == "testuser"
        self.mock_user_store.get_user.assert_called_once_with("testuser")

    def test_authenticate_invalid_password(self):
        """Test authentication with invalid password"""
        # Mock user retrieval
        mock_user = User(
            username="testuser",
            password_hash=hashlib.sha256("correctpassword".encode()).hexdigest(),
            is_active=True
        )
        self.mock_user_store.get_user.return_value = mock_user
        
        with pytest.raises(Exception):
            self.auth_manager.authenticate("testuser", "wrongpassword")

    def test_authenticate_nonexistent_user(self):
        """Test authentication with non-existent user"""
        # Mock user retrieval to return None
        self.mock_user_store.get_user.return_value = None
        
        with pytest.raises(Exception):
            self.auth_manager.authenticate("nonexistent", "password")

    def test_authenticate_inactive_user(self):
        """Test authentication with inactive user"""
        # Mock user retrieval
        mock_user = User(
            username="testuser",
            password_hash=hashlib.sha256("password123".encode()).hexdigest(),
            is_active=False
        )
        self.mock_user_store.get_user.return_value = mock_user
        
        with pytest.raises(Exception):
            self.auth_manager.authenticate("testuser", "password123")

    def test_generate_token(self):
        """Test token generation"""
        mock_user = User(
            username="testuser",
            password_hash="hashed_password",
            is_active=True
        )
        
        token = self.auth_manager.generate_token(mock_user, expires_in_hours=1)
        
        assert token is not None
        assert hasattr(token, 'token_string')
        assert hasattr(token, 'expires_at')

    def test_verify_token_valid(self):
        """Test token verification with valid token"""
        # Mock token retrieval
        mock_token = Token(
            token_string="valid_token",
            user_id="user123",
            expires_at=(datetime.now() + timedelta(hours=1)).isoformat()
        )
        self.mock_user_store.get_token.return_value = mock_token
        
        result = self.auth_manager.verify_token("valid_token")
        
        assert result is not None
        assert result.token_string == "valid_token"

    def test_verify_token_expired(self):
        """Test token verification with expired token"""
        # Mock token retrieval with expired token
        mock_token = Token(
            token_string="expired_token",
            user_id="user123",
            expires_at=(datetime.now() - timedelta(hours=1)).isoformat()
        )
        self.mock_user_store.get_token.return_value = mock_token
        
        with pytest.raises(Exception):
            self.auth_manager.verify_token("expired_token")

    def test_verify_token_invalid(self):
        """Test token verification with invalid token"""
        # Mock token retrieval to return None
        self.mock_user_store.get_token.return_value = None
        
        with pytest.raises(Exception):
            self.auth_manager.verify_token("invalid_token")

    def test_create_user(self):
        """Test user creation"""
        # Mock user creation
        self.mock_user_store.create_user.return_value = User(
            username="newuser",
            password_hash="hashed_password",
            is_active=True
        )
        
        result = self.auth_manager.create_user(
            username="newuser",
            password="password123",
            email="newuser@example.com"
        )
        
        assert result is not None
        assert result.username == "newuser"
        self.mock_user_store.create_user.assert_called_once()

    def test_update_user(self):
        """Test user update"""
        # Mock user update
        mock_user = User(
            username="testuser",
            password_hash="hashed_password",
            is_active=True
        )
        self.mock_user_store.update_user.return_value = mock_user
        
        result = self.auth_manager.update_user(
            username="testuser",
            email="updated@example.com"
        )
        
        assert result is not None
        self.mock_user_store.update_user.assert_called_once()

    def test_delete_user(self):
        """Test user deletion"""
        # Mock user deletion
        self.mock_user_store.delete_user.return_value = True
        
        result = self.auth_manager.delete_user("testuser")
        
        assert result is True
        self.mock_user_store.delete_user.assert_called_once_with("testuser")

    def test_logout_user(self):
        """Test user logout (token invalidation)"""
        # Mock token deletion
        self.mock_user_store.delete_token.return_value = True
        
        result = self.auth_manager.logout("valid_token")
        
        assert result is True
        self.mock_user_store.delete_token.assert_called_once()

    def test_refresh_token(self):
        """Test token refresh"""
        # Mock token operations
        old_token = Token(
            token_string="old_token",
            user_id="user123",
            expires_at=(datetime.now() + timedelta(minutes=30)).isoformat()
        )
        new_token = Token(
            token_string="new_token",
            user_id="user123",
            expires_at=(datetime.now() + timedelta(hours=1)).isoformat()
        )
        
        self.mock_user_store.get_token.return_value = old_token
        self.mock_user_store.create_token.return_value = new_token
        
        result = self.auth_manager.refresh_token("old_token")
        
        assert result is not None
        assert result.token_string == "new_token"

    def test_change_password(self):
        """Test password change"""
        # Mock user retrieval and update
        mock_user = User(
            username="testuser",
            password_hash=hashlib.sha256("oldpassword".encode()).hexdigest(),
            is_active=True
        )
        self.mock_user_store.get_user.return_value = mock_user
        self.mock_user_store.update_user.return_value = mock_user
        
        result = self.auth_manager.change_password(
            username="testuser",
            old_password="oldpassword",
            new_password="newpassword"
        )
        
        assert result is True
        self.mock_user_store.update_user.assert_called_once()

    def test_get_user_info(self):
        """Test getting user information"""
        # Mock user retrieval
        mock_user = User(
            username="testuser",
            password_hash="hashed_password",
            is_active=True,
            email="testuser@example.com"
        )
        self.mock_user_store.get_user.return_value = mock_user
        
        result = self.auth_manager.get_user_info("testuser")
        
        assert result is not None
        assert result.username == "testuser"
        # Ensure password is not exposed
        assert "password" not in result or result.get("password_hash") is None


class TestUser:
    """Test cases for User class"""

    def test_user_creation(self):
        """Test creating a User object"""
        user = User(
            username="testuser",
            password_hash="hashed_password",
            is_active=True,
            email="test@example.com"
        )
        
        assert user.username == "testuser"
        assert user.password_hash == "hashed_password"
        assert user.is_active is True
        assert user.email == "test@example.com"

    def test_user_password_check(self):
        """Test password verification"""
        correct_hash = hashlib.sha256("password123".encode()).hexdigest()
        user = User(
            username="testuser",
            password_hash=correct_hash,
            is_active=True
        )
        
        assert user.check_password("password123") is True
        assert user.check_password("wrongpassword") is False


class TestToken:
    """Test cases for Token class"""

    def test_token_creation(self):
        """Test creating a Token object"""
        expires_at = (datetime.now() + timedelta(hours=1)).isoformat()
        token = Token(
            token_string="test_token",
            user_id="user123",
            expires_at=expires_at
        )
        
        assert token.token_string == "test_token"
        assert token.user_id == "user123"
        assert token.expires_at == expires_at

    def test_token_is_expired(self):
        """Test token expiration check"""
        expired_token = Token(
            token_string="expired",
            user_id="user123",
            expires_at=(datetime.now() - timedelta(hours=1)).isoformat()
        )
        
        valid_token = Token(
            token_string="valid",
            user_id="user123",
            expires_at=(datetime.now() + timedelta(hours=1)).isoformat()
        )
        
        assert expired_token.is_expired() is True
        assert valid_token.is_expired() is False


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
#!/usr/bin/env python3
"""
GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module ns-root/namespaces-mcp/level1/verification/tests
@gl-semantic-anchor GL-00-VERIFICA_TESTS_TESTVERIFICA
@gl-evidence-required false
GL Unified Charter Activated
"""

"""
Test suite for MCP Level 1 Verification System
"""

import os  # noqa: E402

# Import the verification system components
import sys  # noqa: E402
from unittest.mock import Mock, patch  # noqa: E402

import pytest  # noqa: E402
from dns_txt_verifier import DnsTxtVerifier  # noqa: E402
from github_oauth_verifier import GitHubOAuthVerifier  # noqa: E402
from http_well_known_verifier import HttpWellKnownVerifier  # noqa: E402
from verification_system import MCPVerificationSystem, VerificationMethod  # noqa: E402

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestMCPVerificationSystem:
    """Test the main verification system"""

    def setup_method(self):
        """Set up test fixtures"""
        self.verifier = MCPVerificationSystem()

    def test_determine_verification_method(self):
        """Test verification method determination"""
        # Test GitHub OAuth namespaces
        assert (
            self.verifier.determine_verification_method("io.github.username")
            == VerificationMethod.GITHUB_OAUTH
        )
        assert (
            self.verifier.determine_verification_method("io.github.organization")
            == VerificationMethod.GITHUB_OAUTH
        )

        # Test DNS/HTTP namespaces
        assert (
            self.verifier.determine_verification_method("com.company")
            == VerificationMethod.DNS_TXT
        )
        assert (
            self.verifier.determine_verification_method("org.organization")
            == VerificationMethod.DNS_TXT
        )
        assert (
            self.verifier.determine_verification_method("net.domain")
            == VerificationMethod.DNS_TXT
        )

        # Test invalid namespaces
        assert self.verifier.determine_verification_method("invalid.namespace") is None
        assert self.verifier.determine_verification_method("random-string") is None

    def test_verify_github_oauth_success(self):
        """Test successful GitHub OAuth verification"""
        with patch.object(
            self.verifier.github_verifier, "verify_namespace"
        ) as mock_verify:
            mock_result = Mock()
            mock_result.success = True
            mock_result.namespace = "io.github.testuser"
            mock_result.verification_method = "github-oauth"
            mock_result.verified_at = "2024-01-11T12:00:00Z"
            mock_result.expires_at = "2025-01-11T12:00:00Z"
            mock_result.verification_token = "test-token"
            mock_result.error_message = None
            mock_verify.return_value = mock_result

            result = self.verifier.verify_namespace(
                "io.github.testuser", oauth_token="test-token"
            )

            assert result.success is True
            assert result.namespace == "io.github.testuser"
            assert result.verification_method == "github-oauth"
            assert result.error_message is None

    def test_verify_github_oauth_missing_token(self):
        """Test GitHub OAuth verification without token"""
        result = self.verifier.verify_namespace("io.github.testuser")

        assert result.success is False
        assert "OAuth token required" in result.error_message

    def test_verify_unsupported_namespace(self):
        """Test verification of unsupported namespace"""
        result = self.verifier.verify_namespace("invalid.namespace")

        assert result.success is False
        assert "Unsupported namespace format" in result.error_message

    def test_generate_verification_setup(self):
        """Test verification setup generation"""
        setup = self.verifier.generate_verification_setup("io.github.testuser")

        assert setup["namespace"] == "io.github.testuser"
        assert setup["method"] == "github-oauth"
        assert "verification_token" in setup
        assert "instructions" in setup


class TestGitHubOAuthVerifier:
    """Test the GitHub OAuth verifier"""

    def setup_method(self):
        """Set up test fixtures"""
        self.verifier = GitHubOAuthVerifier()

    def test_generate_verification_token(self):
        """Test token generation"""
        token1 = self.verifier.generate_verification_token("test.namespace")
        token2 = self.verifier.generate_verification_token("test.namespace")

        # Tokens should be different (due to timestamp)
        assert token1 != token2
        assert len(token1) == 64  # SHA-256 hex length

    def test_verify_user_success(self):
        """Test successful user verification"""
        with patch("requests.get") as mock_get:
            # Mock successful GitHub API response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"login": "testuser", "active": True}
            mock_get.return_value = mock_response

            success, data = self.verifier.verify_github_user("testuser", "token")

            assert success is True
            assert data["login"] == "testuser"

    def test_verify_user_invalid_token(self):
        """Test user verification with invalid token"""
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 401
            mock_get.return_value = mock_response

            success, data = self.verifier.verify_github_user(
                "testuser", "invalid-token"
            )

            assert success is False
            assert "GitHub API error" in data["error"]


class TestDnsTxtVerifier:
    """Test the DNS TXT verifier"""

    def setup_method(self):
        """Set up test fixtures"""
        self.verifier = DnsTxtVerifier()

    def test_extract_domain_from_namespace(self):
        """Test domain extraction from namespace"""
        assert self.verifier.extract_domain_from_namespace("com.company") == "company"
        assert (
            self.verifier.extract_domain_from_namespace("org.organization")
            == "organization"
        )
        assert self.verifier.extract_domain_from_namespace("net.domain") == "domain"
        assert self.verifier.extract_domain_from_namespace("io.github.user") is None

    def test_generate_verification_token(self):
        """Test token generation"""
        token = self.verifier.generate_verification_token("example.com")

        assert len(token) == 64  # SHA-256 hex length
        assert isinstance(token, str)


class TestHttpWellKnownVerifier:
    """Test the HTTP well-known verifier"""

    def setup_method(self):
        """Set up test fixtures"""
        self.verifier = HttpWellKnownVerifier()

    def test_extract_domain_from_namespace(self):
        """Test domain extraction from namespace"""
        assert self.verifier.extract_domain_from_namespace("com.company") == "company"
        assert (
            self.verifier.extract_domain_from_namespace("org.organization")
            == "organization"
        )
        assert self.verifier.extract_domain_from_namespace("net.domain") == "domain"
        assert self.verifier.extract_domain_from_namespace("io.github.user") is None

    def test_build_endpoint_url(self):
        """Test endpoint URL construction"""
        https_url = self.verifier.build_endpoint_url("example.com", use_https=True)
        http_url = self.verifier.build_endpoint_url("example.com", use_https=False)

        assert https_url == "https://example.com/.well-known/mcp-registry-auth"
        assert http_url == "http://example.com/.well-known/mcp-registry-auth"

    def test_verify_token_in_response_json(self):
        """Test token verification in JSON response"""
        response_data = {"content": {"token": "expected-token"}}

        result = self.verifier.verify_token_in_response(response_data, "expected-token")
        assert result is True

        # Test with different token
        result = self.verifier.verify_token_in_response(response_data, "wrong-token")
        assert result is False

    def test_verify_token_in_response_text(self):
        """Test token verification in plain text response"""
        response_data = {"content": "expected-token"}

        result = self.verifier.verify_token_in_response(response_data, "expected-token")
        assert result is True


class TestIntegration:
    """Integration tests for the complete verification system"""

    def setup_method(self):
        """Set up test fixtures"""
        self.verifier = MCPVerificationSystem()

    def test_batch_verification(self):
        """Test batch verification of multiple namespaces"""
        namespaces = ["io.github.user1", "io.github.user2", "com.company"]

        with patch.object(self.verifier, "verify_namespace") as mock_verify:
            # Mock successful verifications
            mock_verify.side_effect = [
                Mock(success=True, namespace="io.github.user1"),
                Mock(success=True, namespace="io.github.user2"),
                Mock(
                    success=False,
                    namespace="com.company",
                    error_message="DNS verification failed",
                ),
            ]

            results = self.verifier.batch_verify(namespaces)

            assert len(results) == 3
            assert results[0].success is True
            assert results[1].success is True
            assert results[2].success is False

    @pytest.mark.parametrize(
        "namespace,expected_method",
        [
            ("io.github.user", "github-oauth"),
            ("com.company", "dns-txt"),
            ("org.nonprofit", "dns-txt"),
            ("net.domain", "dns-txt"),
        ],
    )
    def test_method_determination_parametrized(self, namespace, expected_method):
        """Parametrized test for method determination"""
        method = self.verifier.determine_verification_method(namespace)
        assert method.value == expected_method


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])

#!/usr/bin/env python3
"""
GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module ns-root/namespaces-mcp/level1/verification
@gl-semantic-anchor GL-00-LEVEL1_VERIFICA_GITHUBOAUTHV
@gl-evidence-required false
GL Unified Charter Activated
"""

"""
GitHub OAuth Verifier for MCP Level 1 Namespace Verification

Implements GitHub OAuth verification for io.github.* namespaces
as specified in the team identity registry.
"""

import hashlib  # noqa: E402
import secrets  # noqa: E402
import time  # noqa: E402
from dataclasses import dataclass  # noqa: E402
from datetime import datetime, timedelta  # noqa: E402
from typing import Dict, Optional, Tuple  # noqa: E402

import requests  # noqa: E402


@dataclass
class VerificationResult:
    """Result of namespace verification"""

    success: bool
    namespace: str
    verification_method: str
    verified_at: str
    expires_at: str
    verification_token: str
    error_message: Optional[str] = None


class GitHubOAuthVerifier:
    """GitHub OAuth verification system for MCP namespaces"""

    def __init__(self):
        self.github_api_base = "https://api.github.com"
        self.verification_timeout = 3600  # 1 hour
        self.validity_period = timedelta(days=365)  # 1 year

    def generate_verification_token(self, namespace: str) -> str:
        """Generate a unique verification token for the namespace"""
        timestamp = str(int(time.time()))
        data = f"{namespace}:{timestamp}:{secrets.token_hex(16)}"
        return hashlib.sha256(data.encode()).hexdigest()

    def verify_github_user(self, username: str, oauth_token: str) -> Tuple[bool, Dict]:
        """Verify GitHub user exists and token is valid"""
        headers = {
            "Authorization": f"token {oauth_token}",
            "Accept": "application/vnd.github.v3+json",
        }

        try:
            # Get user information
            response = requests.get(
                f"{self.github_api_base}/user", headers=headers, timeout=30
            )

            if response.status_code != 200:
                return False, {"error": f"GitHub API error: {response.status_code}"}

            user_data = response.json()

            # Verify username matches
            if user_data.get("login") != username:
                return False, {"error": "Username mismatch"}

            # Check if user is active
            if not user_data.get("active", True):
                return False, {"error": "User account is not active"}

            return True, user_data

        except requests.RequestException as e:
            return False, {"error": f"Request failed: {str(e)}"}

    def verify_github_organization(
        self, org_name: str, oauth_token: str
    ) -> Tuple[bool, Dict]:
        """Verify GitHub organization and user membership"""
        headers = {
            "Authorization": f"token {oauth_token}",
            "Accept": "application/vnd.github.v3+json",
        }

        try:
            # Get user information first
            user_response = requests.get(
                f"{self.github_api_base}/user", headers=headers, timeout=30
            )

            if user_response.status_code != 200:
                return False, {
                    "error": f"GitHub API error: {user_response.status_code}"
                }

            user_data = user_response.json()

            # Check organization membership
            org_response = requests.get(
                f"{self.github_api_base}/orgs/{org_name}/members/{user_data['login']}",
                headers=headers,
                timeout=30,
            )

            if org_response.status_code != 204:  # 204 = No Content = Member exists
                return False, {"error": "Not a member of the organization"}

            # Get organization details
            org_info_response = requests.get(
                f"{self.github_api_base}/orgs/{org_name}", headers=headers, timeout=30
            )

            if org_info_response.status_code != 200:
                return False, {"error": f"Organization not found: {org_name}"}

            org_data = org_info_response.json()

            return True, {
                "user": user_data,
                "organization": org_data,
                "role": "member",  # Could be enhanced to check admin role
            }

        except requests.RequestException as e:
            return False, {"error": f"Request failed: {str(e)}"}

    def verify_namespace(self, namespace: str, oauth_token: str) -> VerificationResult:
        """Verify a namespace using GitHub OAuth"""

        # Parse namespace
        if not namespace.startswith("io.github."):
            return VerificationResult(
                success=False,
                namespace=namespace,
                verification_method="github-oauth",
                verified_at="",
                expires_at="",
                verification_token="",
                error_message="Invalid namespace format for GitHub OAuth verification",
            )

        namespace_part = namespace[10:]  # Remove "io.github."

        # Generate verification token
        verification_token = self.generate_verification_token(namespace)

        # Determine if it's a user or organization namespace
        if "." in namespace_part:
            # Could be organization.subdomain, treat as organization
            org_name = namespace_part.split(".")[0]
            success, data = self.verify_github_organization(org_name, oauth_token)
        else:
            # User namespace
            username = namespace_part
            success, data = self.verify_github_user(username, oauth_token)

        if not success:
            return VerificationResult(
                success=False,
                namespace=namespace,
                verification_method="github-oauth",
                verified_at="",
                expires_at="",
                verification_token=verification_token,
                error_message=data.get("error", "Verification failed"),
            )

        # Create verification result
        now = datetime.utcnow()
        expires_at = now + self.validity_period

        return VerificationResult(
            success=True,
            namespace=namespace,
            verification_method="github-oauth",
            verified_at=now.isoformat() + "Z",
            expires_at=expires_at.isoformat() + "Z",
            verification_token=verification_token,
        )

    def verify_token_validity(self, verification_token: str, namespace: str) -> bool:
        """Verify if a verification token is still valid"""
        # In a real implementation, this would check against a database
        # For now, we'll implement basic token validation
        if not verification_token or len(verification_token) != 64:
            return False

        # Check if token matches expected format
        expected_pattern = hashlib.sha256(namespace.encode()).hexdigest()[:16]
        return verification_token.endswith(expected_pattern)


# CLI Interface for testing
if __name__ == "__main__":
    import sys  # noqa: E402

    if len(sys.argv) != 3:
        print("Usage: python github-oauth-verifier.py <namespace> <oauth-token>")
        sys.exit(1)

    namespace = sys.argv[1]
    oauth_token = sys.argv[2]

    verifier = GitHubOAuthVerifier()
    result = verifier.verify_namespace(namespace, oauth_token)

    print(f"Namespace: {result.namespace}")
    print(f"Success: {result.success}")
    print(f"Verification Method: {result.verification_method}")
    print(f"Verified At: {result.verified_at}")
    print(f"Expires At: {result.expires_at}")
    print(f"Verification Token: {result.verification_token}")

    if result.error_message:
        print(f"Error: {result.error_message}")

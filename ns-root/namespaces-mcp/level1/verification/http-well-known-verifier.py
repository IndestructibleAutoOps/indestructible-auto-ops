#!/usr/bin/env python3
"""
GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module ns-root/namespaces-mcp/level1/verification
@gl-semantic-anchor GL-00-LEVEL1_VERIFICA_HTTPWELLKNOW
@gl-evidence-required false
GL Unified Charter Activated
"""

"""
HTTP Well-Known Verifier for MCP Level 1 Namespace Verification

Implements HTTP well-known endpoint verification for domain namespaces
as specified in the team identity registry.
"""

import hashlib  # noqa: E402
import json  # noqa: E402
import secrets  # noqa: E402
import time  # noqa: E402
from dataclasses import dataclass  # noqa: E402
from datetime import datetime, timedelta  # noqa: E402
from typing import Dict, Optional, Tuple  # noqa: E402

import requests  # noqa: E402


@dataclass
class HTTPVerificationResult:
    """Result of HTTP namespace verification"""

    success: bool
    namespace: str
    domain: str
    verification_method: str
    verified_at: str
    expires_at: str
    verification_token: str
    endpoint_url: str
    http_status: int
    response_content: str
    error_message: Optional[str] = None


class HttpWellKnownVerifier:
    """HTTP well-known endpoint verification system for MCP namespaces"""

    def __init__(self):
        self.verification_timeout = 3600  # 1 hour
        self.validity_period = timedelta(days=365)  # 1 year
        self.well_known_path = "/.well-known/mcp-registry-auth"
        self.request_timeout = 30

    def extract_domain_from_namespace(self, namespace: str) -> Optional[str]:
        """Extract domain from namespace"""
        # Handle com.company, org.organization, net.domain formats
        if namespace.startswith("com."):
            return namespace[4:]  # Remove "com."
        elif namespace.startswith("org."):
            return namespace[4:]  # Remove "org."
        elif namespace.startswith("net."):
            return namespace[4:]  # Remove "net."
        return None

    def generate_verification_token(self, domain: str) -> str:
        """Generate a unique verification token for the domain"""
        timestamp = str(int(time.time()))
        data = f"{domain}:{timestamp}:{secrets.token_hex(16)}"
        return hashlib.sha256(data.encode()).hexdigest()

    def build_endpoint_url(self, domain: str, use_https: bool = True) -> str:
        """Build the well-known endpoint URL"""
        protocol = "https" if use_https else "http"
        return f"{protocol}://{domain}{self.well_known_path}"

    def fetch_verification_endpoint(
        self, domain: str
    ) -> Tuple[bool, Dict, Optional[str]]:
        """Fetch the verification endpoint content"""

        # Try HTTPS first, then HTTP
        urls_to_try = [
            self.build_endpoint_url(domain, use_https=True),
            self.build_endpoint_url(domain, use_https=False),
        ]

        user_agent = "MCP-Registry-Verifier/1.0"
        headers = {"User-Agent": user_agent, "Accept": "text/plain, application/json"}

        for url in urls_to_try:
            try:
                response = requests.get(
                    url,
                    headers=headers,
                    timeout=self.request_timeout,
                    allow_redirects=True,
                )

                if response.status_code == 200:
                    # Try to parse as JSON first
                    try:
                        content = response.json()
                        return (
                            True,
                            {
                                "url": url,
                                "status_code": response.status_code,
                                "content": content,
                                "content_type": response.headers.get(
                                    "content-type", ""
                                ),
                            },
                            None,
                        )
                    except json.JSONDecodeError:
                        # If not JSON, treat as plain text
                        return (
                            True,
                            {
                                "url": url,
                                "status_code": response.status_code,
                                "content": response.text.strip(),
                                "content_type": response.headers.get(
                                    "content-type", ""
                                ),
                            },
                            None,
                        )

            except requests.exceptions.Timeout:
                continue
            except requests.exceptions.ConnectionError:
                continue
            except requests.exceptions.RequestException:
                continue

        return (
            False,
            {},
            "Unable to fetch verification endpoint from either HTTP or HTTPS",
        )

    def verify_token_in_response(
        self, response_data: Dict, expected_token: str
    ) -> bool:
        """Verify the token exists in the response"""
        content = response_data.get("content", {})

        # If content is a dictionary, check multiple possible fields
        if isinstance(content, dict):
            return (
                content.get("token") == expected_token
                or content.get("verification_token") == expected_token
                or content.get("mcp_registry_token") == expected_token
                or content.get("auth_token") == expected_token
            )

        # If content is a string, check if it matches the token
        if isinstance(content, str):
            return content.strip() == expected_token

        return False

    def verify_namespace(
        self, namespace: str, verification_token: str
    ) -> HTTPVerificationResult:
        """Verify a namespace using HTTP well-known endpoint"""

        # Extract domain from namespace
        domain = self.extract_domain_from_namespace(namespace)
        if not domain:
            return HTTPVerificationResult(
                success=False,
                namespace=namespace,
                domain="",
                verification_method="http-well-known",
                verified_at="",
                expires_at="",
                verification_token=verification_token,
                endpoint_url="",
                http_status=0,
                response_content="",
                error_message="Invalid namespace format for HTTP verification",
            )

        # Fetch verification endpoint
        success, response_data, error = self.fetch_verification_endpoint(domain)

        if not success:
            return HTTPVerificationResult(
                success=False,
                namespace=namespace,
                domain=domain,
                verification_method="http-well-known",
                verified_at="",
                expires_at="",
                verification_token=verification_token,
                endpoint_url="",
                http_status=0,
                response_content="",
                error_message=error,
            )

        # Verify token in response
        token_valid = self.verify_token_in_response(response_data, verification_token)

        if not token_valid:
            return HTTPVerificationResult(
                success=False,
                namespace=namespace,
                domain=domain,
                verification_method="http-well-known",
                verified_at="",
                expires_at="",
                verification_token=verification_token,
                endpoint_url=response_data["url"],
                http_status=response_data["status_code"],
                response_content=str(
                    response_data["content"]),
                error_message=f"Verification token not found in response from {response_data['url']}",
            )

        # Create verification result
        now = datetime.utcnow()
        expires_at = now + self.validity_period

        return HTTPVerificationResult(
            success=True,
            namespace=namespace,
            domain=domain,
            verification_method="http-well-known",
            verified_at=now.isoformat() + "Z",
            expires_at=expires_at.isoformat() + "Z",
            verification_token=verification_token,
            endpoint_url=response_data["url"],
            http_status=response_data["status_code"],
            response_content=str(response_data["content"]),
        )

    def generate_verification_instructions(self, namespace: str) -> Dict:
        """Generate instructions for HTTP well-known verification"""
        domain = self.extract_domain_from_namespace(namespace)
        if not domain:
            return {"error": "Invalid namespace format"}

        verification_token = self.generate_verification_token(domain)
        endpoint_url = self.build_endpoint_url(domain)

        return {
            "namespace": namespace,
            "domain": domain,
            "verification_token": verification_token,
            "endpoint_url": endpoint_url,
            "instructions": {
                "step1": f"Create a file at: {domain}/.well-known/mcp-registry-auth",
                "step2": "Add the following content to the file:",
                "step3": "Content (JSON format):",
                "step4": "{",
                "step5": f'  "token": "{verification_token}",',
                "step6": f'  "namespace": "{namespace}",',
                "step7": f'  "created_at": "{datetime.utcnow().isoformat()}Z"',
                "step8": "}",
                "step9": f"Alternative (plain text): {verification_token}",
                "step10": "Ensure the file is accessible via HTTP and HTTPS",
                "step11": f"Run verification with: python http-well-known-verifier.py {namespace} {verification_token}",
            },
            "file_examples": {
                "json_example": {
                    "token": verification_token,
                    "namespace": namespace,
                    "created_at": datetime.utcnow().isoformat() + "Z",
                },
                "txt_example": verification_token,
            },
            "web_server_configs": {
                "nginx": f"location /.well-known/mcp-registry-auth {{ return 200 '{verification_token}'; add_header Content-Type text/plain; }}",
                "apache": f"<Location /.well-known/mcp-registry-auth>\n    Header set Content-Type &quot;text/plain&quot;\n    Require all granted\n</Location>\n# File content: {verification_token}",
                "express": f"app.get('/.well-known/mcp-registry-auth', (req, res) => res.send('{verification_token}'));",
                "python_flask": f"@app.route('/.well-known/mcp-registry-auth')\ndef verification():\n    return '{verification_token}', 200, {{'Content-Type': 'text/plain'}}",
            },
        }


# CLI Interface for testing
if __name__ == "__main__":
    import sys  # noqa: E402

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python http-well-known-verifier.py <namespace> <verification-token>")
        print("  python http-well-known-verifier.py <namespace> --instructions")
        sys.exit(1)

    namespace = sys.argv[1]

    if len(sys.argv) == 3 and sys.argv[2] == "--instructions":
        verifier = HttpWellKnownVerifier()
        instructions = verifier.generate_verification_instructions(namespace)
        print(json.dumps(instructions, indent=2))
    elif len(sys.argv) == 3:
        verification_token = sys.argv[2]
        verifier = HttpWellKnownVerifier()
        result = verifier.verify_namespace(namespace, verification_token)

        print(f"Namespace: {result.namespace}")
        print(f"Domain: {result.domain}")
        print(f"Success: {result.success}")
        print(f"Verification Method: {result.verification_method}")
        print(f"Verified At: {result.verified_at}")
        print(f"Expires At: {result.expires_at}")
        print(f"Verification Token: {result.verification_token}")
        print(f"Endpoint URL: {result.endpoint_url}")
        print(f"HTTP Status: {result.http_status}")
        print(f"Response Content: {result.response_content}")

        if result.error_message:
            print(f"Error: {result.error_message}")
    else:
        print("Invalid arguments")
        sys.exit(1)

#!/usr/bin/env python3
"""
GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module ns-root/namespaces-mcp/level1/verification
@gl-semantic-anchor GL-00-LEVEL1_VERIFICA_VERIFICATION
@gl-evidence-required false
GL Unified Charter Activated
"""

"""
MCP Level 1 Namespace Verification System

Integrates all verification methods (GitHub OAuth, DNS TXT, HTTP Well-Known)
as specified in the team identity registry.
"""

import json  # noqa: E402
from dataclasses import asdict, dataclass  # noqa: E402
from enum import Enum  # noqa: E402
from typing import Dict, List, Optional  # noqa: E402

from dns_txt_verifier import DnsTxtVerifier  # noqa: E402
from github_oauth_verifier import GitHubOAuthVerifier  # noqa: E402
from http_well_known_verifier import HttpWellKnownVerifier  # noqa: E402


class VerificationMethod(Enum):
    GITHUB_OAUTH = "github-oauth"
    DNS_TXT = "dns-txt"
    HTTP_WELL_KNOWN = "http-well-known"


@dataclass
class NamespaceVerification:
    """Complete namespace verification result"""

    namespace: str
    verification_method: str
    success: bool
    verified_at: str
    expires_at: str
    verification_token: str
    details: Dict
    error_message: Optional[str] = None


class MCPVerificationSystem:
    """Main verification system for MCP namespaces"""

    def __init__(self):
        self.github_verifier = GitHubOAuthVerifier()
        self.dns_verifier = DnsTxtVerifier()
        self.http_verifier = HttpWellKnownVerifier()

    def determine_verification_method(
        self, namespace: str
    ) -> Optional[VerificationMethod]:
        """Determine the appropriate verification method for a namespace"""
        if namespace.startswith("io.github."):
            return VerificationMethod.GITHUB_OAUTH
        elif namespace.startswith(("com.", "org.", "net.")):
            # Support both DNS TXT and HTTP for these domains
            return VerificationMethod.DNS_TXT  # Default to DNS, but can use HTTP too
        return None

    def verify_namespace(
        self, namespace: str, verification_token: str = None, oauth_token: str = None
    ) -> NamespaceVerification:
        """Verify a namespace using the appropriate method"""

        method = self.determine_verification_method(namespace)
        if not method:
            return NamespaceVerification(
                namespace=namespace,
                verification_method="none",
                success=False,
                verified_at="",
                expires_at="",
                verification_token="",
                details={},
                error_message="Unsupported namespace format",
            )

        try:
            if method == VerificationMethod.GITHUB_OAUTH:
                if not oauth_token:
                    return NamespaceVerification(
                        namespace=namespace,
                        verification_method=method.value,
                        success=False,
                        verified_at="",
                        expires_at="",
                        verification_token="",
                        details={},
                        error_message="OAuth token required for GitHub verification",
                    )

                result = self.github_verifier.verify_namespace(namespace, oauth_token)
                return NamespaceVerification(
                    namespace=result.namespace,
                    verification_method=result.verification_method,
                    success=result.success,
                    verified_at=result.verified_at,
                    expires_at=result.expires_at,
                    verification_token=result.verification_token,
                    details=asdict(result),
                    error_message=result.error_message,
                )

            elif method == VerificationMethod.DNS_TXT:
                if not verification_token:
                    return NamespaceVerification(
                        namespace=namespace,
                        verification_method=method.value,
                        success=False,
                        verified_at="",
                        expires_at="",
                        verification_token="",
                        details={},
                        error_message="Verification token required for DNS verification",
                    )

                result = self.dns_verifier.verify_namespace(
                    namespace, verification_token
                )
                return NamespaceVerification(
                    namespace=result.namespace,
                    verification_method=result.verification_method,
                    success=result.success,
                    verified_at=result.verified_at,
                    expires_at=result.expires_at,
                    verification_token=result.verification_token,
                    details=asdict(result),
                    error_message=result.error_message,
                )

            elif method == VerificationMethod.HTTP_WELL_KNOWN:
                if not verification_token:
                    return NamespaceVerification(
                        namespace=namespace,
                        verification_method=method.value,
                        success=False,
                        verified_at="",
                        expires_at="",
                        verification_token="",
                        details={},
                        error_message="Verification token required for HTTP verification",
                    )

                result = self.http_verifier.verify_namespace(
                    namespace, verification_token
                )
                return NamespaceVerification(
                    namespace=result.namespace,
                    verification_method=result.verification_method,
                    success=result.success,
                    verified_at=result.verified_at,
                    expires_at=result.expires_at,
                    verification_token=result.verification_token,
                    details=asdict(result),
                    error_message=result.error_message,
                )

        except Exception as e:
            return NamespaceVerification(
                namespace=namespace,
                verification_method=method.value,
                success=False,
                verified_at="",
                expires_at="",
                verification_token="",
                details={},
                error_message=f"Verification system error: {str(e)}",
            )

    def generate_verification_setup(self, namespace: str, method: str = None) -> Dict:
        """Generate verification setup instructions"""
        if not method:
            determined_method = self.determine_verification_method(namespace)
            if not determined_method:
                return {"error": "Unsupported namespace format"}
            method = determined_method.value

        if method == VerificationMethod.GITHUB_OAUTH.value:
            token = self.github_verifier.generate_verification_token(namespace)
            return {
                "namespace": namespace,
                "method": method,
                "verification_token": token,
                "instructions": {
                    "step1": "Use GitHub OAuth to verify ownership",
                    "step2": f"Run: python verification-system.py {namespace} --github-oauth",
                    "step3": "Provide your GitHub OAuth token when prompted",
                },
            }

        elif method == VerificationMethod.DNS_TXT.value:
            return self.dns_verifier.generate_verification_instructions(namespace)

        elif method == VerificationMethod.HTTP_WELL_KNOWN.value:
            return self.http_verifier.generate_verification_instructions(namespace)

        else:
            return {"error": "Unsupported verification method"}

    def batch_verify(
        self,
        namespaces: List[str],
        tokens: Dict[str, str] = None,
        oauth_token: str = None,
    ) -> List[NamespaceVerification]:
        """Verify multiple namespaces in batch"""
        results = []
        for namespace in namespaces:
            verification_token = tokens.get(namespace) if tokens else None
            result = self.verify_namespace(namespace, verification_token, oauth_token)
            results.append(result)
        return results

    def load_registry_namespaces(self, registry_file: str) -> List[str]:
        """Load namespaces from the team identity registry"""
        try:
            with open(registry_file, "r") as f:
                registry_data = yaml.safe_load(f)

            namespaces = []

            # Extract from namespace_example section
            if "namespace_example" in registry_data:
                for example in registry_data["namespace_example"]:
                    if "namespace" in example:
                        namespaces.append(example["namespace"])

            # Extract from semantic_boundary scopes
            if (
                "semantic_boundary" in registry_data
                and "scopes" in registry_data["semantic_boundary"]
            ):
                for scope_type, scope_data in registry_data["semantic_boundary"][
                    "scopes"
                ].items():
                    if "format" in scope_data:
                        # Extract example from format if available
                        format_str = scope_data["format"]
                        if "{username}" in format_str:
                            namespaces.append(
                                format_str.replace("{username}", "example-user")
                            )
                        elif "{orgname}" in format_str:
                            namespaces.append(
                                format_str.replace("{orgname}", "example-org")
                            )
                        elif "{company}" in format_str:
                            namespaces.append(
                                format_str.replace("{company}", "example-company")
                            )

            return list(set(namespaces))  # Remove duplicates

        except Exception as e:
            print(f"Error loading registry: {e}")
            return []


# CLI Interface
if __name__ == "__main__":
    import argparse  # noqa: E402

    import yaml  # noqa: E402

    parser = argparse.ArgumentParser(description="MCP Namespace Verification System")
    parser.add_argument("namespace", help="Namespace to verify")
    parser.add_argument("--token", help="Verification token (for DNS/HTTP)")
    parser.add_argument("--oauth-token", help="GitHub OAuth token (for GitHub)")
    parser.add_argument(
        "--method",
        choices=["github-oauth", "dns-txt", "http-well-known"],
        help="Verification method",
    )
    parser.add_argument(
        "--setup", action="store_true", help="Generate setup instructions"
    )
    parser.add_argument("--batch", help="Batch verify from registry file")

    args = parser.parse_args()

    verifier = MCPVerificationSystem()

    if args.batch:
        # Batch verification from registry
        namespaces = verifier.load_registry_namespaces(args.batch)
        print(f"Loaded {len(namespaces)} namespaces from registry")

        results = verifier.batch_verify(namespaces)

        for result in results:
            print(f"\n{result.namespace}: {'✅' if result.success else '❌'}")
            if result.error_message:
                print(f"  Error: {result.error_message}")

    elif args.setup:
        # Generate setup instructions
        instructions = verifier.generate_verification_setup(args.namespace, args.method)
        print(json.dumps(instructions, indent=2))

    else:
        # Single verification
        result = verifier.verify_namespace(args.namespace, args.token, args.oauth_token)

        print(f"Namespace: {result.namespace}")
        print(f"Method: {result.verification_method}")
        print(f"Success: {'✅' if result.success else '❌'}")
        print(f"Verified At: {result.verified_at}")
        print(f"Expires At: {result.expires_at}")
        print(f"Verification Token: {result.verification_token}")

        if result.error_message:
            print(f"Error: {result.error_message}")

        if result.success:
            print(f"\n🎉 Namespace {result.namespace} has been successfully verified!")
            print(f"Verification is valid until {result.expires_at}")

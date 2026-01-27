#!/usr/bin/env python3
"""
GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module ns-root/namespaces-mcp/level1/verification
@gl-semantic-anchor GL-00-LEVEL1_VERIFICA_DNSTXTVERIFI
@gl-evidence-required false
GL Unified Charter Activated
"""

"""
DNS TXT Verifier for MCP Level 1 Namespace Verification

Implements DNS TXT record verification for domain namespaces
as specified in the team identity registry.
"""

import hashlib  # noqa: E402
import json  # noqa: E402
import secrets  # noqa: E402
import time  # noqa: E402
from dataclasses import dataclass  # noqa: E402
from datetime import datetime, timedelta  # noqa: E402
from typing import Dict, List, Optional, Tuple  # noqa: E402

import dns.exception  # noqa: E402
import dns.resolver  # noqa: E402


@dataclass
class DNSVerificationResult:
    """Result of DNS namespace verification"""

    success: bool
    namespace: str
    domain: str
    verification_method: str
    verified_at: str
    expires_at: str
    verification_token: str
    txt_records: List[str]
    error_message: Optional[str] = None


class DnsTxtVerifier:
    """DNS TXT verification system for MCP namespaces"""

    def __init__(self):
        self.verification_timeout = 3600  # 1 hour
        self.validity_period = timedelta(days=365)  # 1 year
        self.txt_record_prefix = "mcp-registry-verification"

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

    def get_txt_records(self, domain: str) -> Tuple[bool, List[str], Optional[str]]:
        """Retrieve TXT records for a domain"""
        try:
            # Create resolver with custom timeout
            resolver = dns.resolver.Resolver()
            resolver.timeout = 10
            resolver.lifetime = 10

            # Query TXT records
            answers = resolver.resolve(domain, "TXT")
            txt_records = [str(rdata).strip('"') for rdata in answers]

            return True, txt_records, None

        except dns.resolver.NXDOMAIN:
            return False, [], f"Domain {domain} does not exist"
        except dns.resolver.NoAnswer:
            return False, [], f"No TXT records found for {domain}"
        except dns.exception.Timeout:
            return False, [], f"DNS query timeout for {domain}"
        except Exception as e:
            return False, [], f"DNS query failed: {str(e)}"

    def verify_txt_record(
        self, domain: str, expected_token: str
    ) -> Tuple[bool, List[str], Optional[str]]:
        """Verify that the domain has the expected TXT record"""
        success, txt_records, error = self.get_txt_records(domain)

        if not success:
            return False, [], error

        # Look for the verification record
        expected_record = f"{self.txt_record_prefix}={expected_token}"

        for record in txt_records:
            if record == expected_record or record.startswith(
                f"{self.txt_record_prefix}="
            ):
                # Extract token from record
                actual_token = record.split("=", 1)[1] if "=" in record else ""
                if actual_token == expected_token:
                    return True, txt_records, None

        return (
            False,
            txt_records,
            f"Verification TXT record not found. Expected: {expected_record}",
        )

    def verify_namespace(
        self, namespace: str, verification_token: str
    ) -> DNSVerificationResult:
        """Verify a namespace using DNS TXT record"""

        # Extract domain from namespace
        domain = self.extract_domain_from_namespace(namespace)
        if not domain:
            return DNSVerificationResult(
                success=False,
                namespace=namespace,
                domain="",
                verification_method="dns-txt",
                verified_at="",
                expires_at="",
                verification_token=verification_token,
                txt_records=[],
                error_message="Invalid namespace format for DNS TXT verification",
            )

        # First get existing TXT records
        success, txt_records, error = self.get_txt_records(domain)
        if not success:
            return DNSVerificationResult(
                success=False,
                namespace=namespace,
                domain=domain,
                verification_method="dns-txt",
                verified_at="",
                expires_at="",
                verification_token=verification_token,
                txt_records=[],
                error_message=error,
            )

        # Verify the specific token
        token_success, final_txt_records, token_error = self.verify_txt_record(
            domain, verification_token
        )

        if not token_success:
            return DNSVerificationResult(
                success=False,
                namespace=namespace,
                domain=domain,
                verification_method="dns-txt",
                verified_at="",
                expires_at="",
                verification_token=verification_token,
                txt_records=final_txt_records,
                error_message=token_error,
            )

        # Create verification result
        now = datetime.utcnow()
        expires_at = now + self.validity_period

        return DNSVerificationResult(
            success=True,
            namespace=namespace,
            domain=domain,
            verification_method="dns-txt",
            verified_at=now.isoformat() + "Z",
            expires_at=expires_at.isoformat() + "Z",
            verification_token=verification_token,
            txt_records=final_txt_records,
        )

    def generate_verification_instructions(self, namespace: str) -> Dict:
        """Generate instructions for DNS TXT verification"""
        domain = self.extract_domain_from_namespace(namespace)
        if not domain:
            return {"error": "Invalid namespace format"}

        verification_token = self.generate_verification_token(domain)
        txt_record = f"{self.txt_record_prefix}={verification_token}"

        return {
            "namespace": namespace,
            "domain": domain,
            "verification_token": verification_token,
            "txt_record": txt_record,
            "instructions": {
                "step1": f"Add the following TXT record to your domain {domain}:",
                "step2": "Record type: TXT",
                "step3": f"Record name: {domain}",
                "step4": f"Record value: {txt_record}",
                "step5": "Wait for DNS propagation (usually 5-60 minutes)",
                "step6": f"Run verification with: python dns-txt-verifier.py {namespace} {verification_token}",
            },
            "dns_commands": {
                "bind": f'TXT "{domain}" "{txt_record}"',
                "route53": "aws route53 change-resource-record-sets --hosted-zone-id YOUR_ZONE_ID --change-batch file://change.json",
                "cloudflare": "Use Cloudflare DNS management to add TXT record",
                "google": "Use Google Cloud DNS to add TXT record",
            },
        }


# CLI Interface for testing
if __name__ == "__main__":
    import sys  # noqa: E402

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python dns-txt-verifier.py <namespace> <verification-token>")
        print("  python dns-txt-verifier.py <namespace> --instructions")
        sys.exit(1)

    namespace = sys.argv[1]

    if len(sys.argv) == 3 and sys.argv[2] == "--instructions":
        verifier = DnsTxtVerifier()
        instructions = verifier.generate_verification_instructions(namespace)
        print(json.dumps(instructions, indent=2))
    elif len(sys.argv) == 3:
        verification_token = sys.argv[2]
        verifier = DnsTxtVerifier()
        result = verifier.verify_namespace(namespace, verification_token)

        print(f"Namespace: {result.namespace}")
        print(f"Domain: {result.domain}")
        print(f"Success: {result.success}")
        print(f"Verification Method: {result.verification_method}")
        print(f"Verified At: {result.verified_at}")
        print(f"Expires At: {result.expires_at}")
        print(f"Verification Token: {result.verification_token}")
        print(f"TXT Records Found: {len(result.txt_records)}")
        for record in result.txt_records:
            print(f"  - {record}")

        if result.error_message:
            print(f"Error: {result.error_message}")
    else:
        print("Invalid arguments")
        sys.exit(1)

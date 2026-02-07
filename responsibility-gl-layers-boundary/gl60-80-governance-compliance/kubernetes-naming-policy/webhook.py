#!/usr/bin/env python3
"""
Kubernetes ValidatingWebhook Server for Naming Policy Enforcement

GL Layer: GL60-80 Governance Compliance
Purpose: Kubernetes admission webhook for naming policy validation
Version: 1.0.0
Last Updated: 2026-02-07

This module implements a Flask-based webhook server that validates Kubernetes
resources against naming policies defined in core.py.
"""

import os
import sys
import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

# Import core validation logic
from core import build_standard_validator, ValidationResult

# Note: Flask is required for webhook server
# In production, install Flask: pip install Flask
try:
    from flask import Flask, request, jsonify
except ImportError:
    print("ERROR: Flask is required for webhook server", file=sys.stderr)
    print("Install with: pip install Flask", file=sys.stderr)
    sys.exit(1)


# ==============================================================================
# Configuration
# ==============================================================================

@dataclass
class WebhookConfig:
    """Configuration for webhook server."""
    tls_cert_file: str = os.getenv('TLS_CERT_FILE', '/etc/webhook/certs/tls.crt')
    tls_key_file: str = os.getenv('TLS_KEY_FILE', '/etc/webhook/certs/tls.key')
    webhook_port: int = int(os.getenv('WEBHOOK_PORT', '8443'))
    log_level: str = os.getenv('LOG_LEVEL', 'INFO')
    fail_mode: str = os.getenv('FAIL_MODE', 'closed')  # 'closed' or 'open'
    audit_enabled: bool = os.getenv('AUDIT_ENABLED', 'true').lower() == 'true'
    metrics_enabled: bool = os.getenv('METRICS_ENABLED', 'true').lower() == 'true'


# ==============================================================================
# Metrics
# ==============================================================================

class WebhookMetrics:
    """Simple in-memory metrics for Prometheus export."""

    def __init__(self):
        """Initialize metrics counters."""
        self.requests_total = 0
        self.requests_allowed = 0
        self.requests_denied = 0
        self.requests_errors = 0
        self.violations_by_field: Dict[str, int] = {}
        self.response_time_total_ms = 0.0
        self.hash_collisions = 0

    def record_request(self, allowed: bool, error: bool = False):
        """Record a webhook request."""
        self.requests_total += 1
        if error:
            self.requests_errors += 1
        elif allowed:
            self.requests_allowed += 1
        else:
            self.requests_denied += 1

    def record_violation(self, field: str):
        """Record a naming policy violation for a specific field."""
        if field not in self.violations_by_field:
            self.violations_by_field[field] = 0
        self.violations_by_field[field] += 1

    def record_response_time(self, time_ms: float):
        """Record response time in milliseconds."""
        self.response_time_total_ms += time_ms

    def to_prometheus(self) -> str:
        """
        Export metrics in Prometheus format.

        Returns:
            Prometheus-formatted metrics string
        """
        lines = []

        # Request metrics
        lines.append('# HELP webhook_requests_total Total webhook requests')
        lines.append('# TYPE webhook_requests_total counter')
        lines.append(f'webhook_requests_total{{status="allowed"}} {self.requests_allowed}')
        lines.append(f'webhook_requests_total{{status="denied"}} {self.requests_denied}')
        lines.append(f'webhook_requests_errors_total {self.requests_errors}')

        # Violation metrics
        lines.append('# HELP webhook_violations_by_field Naming policy violations by field')
        lines.append('# TYPE webhook_violations_by_field counter')
        for field, count in self.violations_by_field.items():
            lines.append(f'webhook_violations_by_field{{field="{field}"}} {count}')

        # Performance metrics
        lines.append('# HELP webhook_response_time_ms_total Total response time')
        lines.append('# TYPE webhook_response_time_ms_total counter')
        lines.append(f'webhook_response_time_ms_total {self.response_time_total_ms}')
        lines.append(f'webhook_response_time_ms_count {self.requests_total}')

        if self.requests_total > 0:
            avg_time = self.response_time_total_ms / self.requests_total
            lines.append(f'webhook_response_time_ms_avg {avg_time:.2f}')

        # Collision metrics
        lines.append('# HELP webhook_hash_collisions_detected Hash collisions detected')
        lines.append('# TYPE webhook_hash_collisions_detected counter')
        lines.append(f'webhook_hash_collisions_detected {self.hash_collisions}')

        return '\n'.join(lines) + '\n'


# ==============================================================================
# Audit Logger
# ==============================================================================

class AuditLogger:
    """Structured audit logging for compliance."""

    def __init__(self, enabled: bool = True):
        """
        Initialize audit logger.

        Args:
            enabled: Whether audit logging is enabled
        """
        self.enabled = enabled
        self.logger = logging.getLogger('naming_policy_audit')

    def log_decision(
        self,
        request_uid: str,
        operation: str,
        kind: str,
        namespace: str,
        name: str,
        allowed: bool,
        reason: str,
        violations: List[Dict],
        user_agent: Optional[str] = None,
        source_ip: Optional[str] = None
    ):
        """
        Log an admission decision for audit trail.

        Args:
            request_uid: Unique request ID
            operation: K8s operation (CREATE, UPDATE, etc.)
            kind: Resource kind (Pod, Service, etc.)
            namespace: Resource namespace
            name: Resource name
            allowed: Whether request was allowed
            reason: Reason for decision
            violations: List of violations
            user_agent: User agent string
            source_ip: Source IP address
        """
        if not self.enabled:
            return

        audit_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "request_uid": request_uid,
            "operation": operation,
            "kind": kind,
            "namespace": namespace,
            "name": name,
            "allowed": allowed,
            "reason": reason,
            "violations": violations,
            "user_agent": user_agent,
            "source_ip": source_ip
        }

        self.logger.info(json.dumps(audit_entry))


# ==============================================================================
# Webhook Handler
# ==============================================================================

class NamingPolicyWebhookHandler:
    """Handles admission review requests for naming policy validation."""

    def __init__(self, config: WebhookConfig):
        """
        Initialize webhook handler.

        Args:
            config: Webhook configuration
        """
        self.config = config
        self.validator = build_standard_validator()
        self.metrics = WebhookMetrics()
        self.audit = AuditLogger(enabled=config.audit_enabled)
        self.logger = logging.getLogger('naming_policy_webhook')

    def handle_admission_review(self, admission_review: Dict) -> Dict:
        """
        Process an AdmissionReview request.

        Args:
            admission_review: AdmissionReview request body

        Returns:
            AdmissionReview response
        """
        start_time = datetime.now()

        try:
            request_obj = admission_review.get('request', {})
            uid = request_obj.get('uid', 'unknown')
            operation = request_obj.get('operation', 'UNKNOWN')
            kind = request_obj.get('kind', {}).get('kind', 'Unknown')
            namespace = request_obj.get('namespace', 'default')
            name = request_obj.get('name', '')
            obj = request_obj.get('object', {})

            # Validate naming policy
            violations = self._validate_object(obj, kind)

            # Determine if request should be allowed
            allowed = len(violations) == 0

            # Build response
            response = self._build_response(
                uid=uid,
                allowed=allowed,
                violations=violations
            )

            # Record metrics
            self.metrics.record_request(allowed=allowed, error=False)
            for violation in violations:
                self.metrics.record_violation(violation['field'])

            # Audit log
            self.audit.log_decision(
                request_uid=uid,
                operation=operation,
                kind=kind,
                namespace=namespace,
                name=name,
                allowed=allowed,
                reason=response['response']['status'].get('message', 'OK'),
                violations=violations,
                user_agent=request_obj.get('userInfo', {}).get('username'),
                source_ip=None  # Not available in AdmissionReview
            )

            # Record response time
            elapsed_ms = (datetime.now() - start_time).total_seconds() * 1000
            self.metrics.record_response_time(elapsed_ms)

            return response

        except Exception as e:
            self.logger.error(f"Error processing admission review: {e}", exc_info=True)
            self.metrics.record_request(allowed=False, error=True)

            # Fail-closed: deny request on error
            if self.config.fail_mode == 'closed':
                return self._build_error_response(
                    uid=admission_review.get('request', {}).get('uid', 'unknown'),
                    error=str(e)
                )
            else:
                # Fail-open: allow request on error
                return self._build_response(
                    uid=admission_review.get('request', {}).get('uid', 'unknown'),
                    allowed=True,
                    violations=[]
                )

    def _validate_object(self, obj: Dict, kind: str) -> List[Dict]:
        """
        Validate a Kubernetes object against naming policies.

        Args:
            obj: Kubernetes object to validate
            kind: Resource kind

        Returns:
            List of violations
        """
        violations = []

        metadata = obj.get('metadata', {})
        spec = obj.get('spec', {})

        # Validate metadata.name
        name = metadata.get('name', '')
        if name:
            result = self.validator.process(
                name,
                'dns1123Label63',
                normalize=False,
                auto_truncate=False
            )
            if not result.passed:
                violations.append({
                    'field': 'metadata.name',
                    'input': name,
                    'reason': ', '.join(result.errors)
                })

        # Validate container names (for Pods, Deployments, etc.)
        if kind in ['Pod', 'Deployment', 'StatefulSet', 'DaemonSet', 'Job', 'CronJob']:
            containers = spec.get('containers', [])
            if kind in ['Deployment', 'StatefulSet', 'DaemonSet']:
                containers = spec.get('template', {}).get('spec', {}).get('containers', [])
            if kind in ['Job', 'CronJob']:
                containers = spec.get('jobTemplate', {}).get('spec', {}).get('template', {}).get('spec', {}).get('containers', [])

            for idx, container in enumerate(containers):
                container_name = container.get('name', '')
                if container_name:
                    result = self.validator.process(
                        container_name,
                        'dns1123Label63',
                        normalize=False,
                        auto_truncate=False
                    )
                    if not result.passed:
                        violations.append({
                            'field': f'spec.containers[{idx}].name',
                            'input': container_name,
                            'reason': ', '.join(result.errors)
                        })

                # Validate port names
                ports = container.get('ports', [])
                for port_idx, port in enumerate(ports):
                    port_name = port.get('name', '')
                    if port_name:
                        result = self.validator.process(
                            port_name,
                            'portName15',
                            normalize=False,
                            auto_truncate=False
                        )
                        if not result.passed:
                            violations.append({
                                'field': f'spec.containers[{idx}].ports[{port_idx}].name',
                                'input': port_name,
                                'reason': ', '.join(result.errors)
                            })

        # Validate labels
        labels = metadata.get('labels', {})
        for label_key, label_value in labels.items():
            result = self.validator.process(
                label_value,
                'k8sLabelValue63',
                normalize=False,
                auto_truncate=False
            )
            if not result.passed:
                violations.append({
                    'field': f'metadata.labels.{label_key}',
                    'input': label_value,
                    'reason': ', '.join(result.errors)
                })

        return violations

    def _build_response(self, uid: str, allowed: bool, violations: List[Dict]) -> Dict:
        """
        Build AdmissionReview response.

        Args:
            uid: Request UID
            allowed: Whether to allow the request
            violations: List of violations

        Returns:
            AdmissionReview response
        """
        response = {
            "apiVersion": "admission.k8s.io/v1",
            "kind": "AdmissionReview",
            "response": {
                "uid": uid,
                "allowed": allowed
            }
        }

        if not allowed:
            message = f"Naming policy violations ({len(violations)} error(s)):\n"
            for v in violations:
                message += f"  - {v['field']}: {v['reason']}\n"

            response["response"]["status"] = {
                "code": 403,
                "message": message.strip()
            }

        return response

    def _build_error_response(self, uid: str, error: str) -> Dict:
        """
        Build error response.

        Args:
            uid: Request UID
            error: Error message

        Returns:
            AdmissionReview error response
        """
        return {
            "apiVersion": "admission.k8s.io/v1",
            "kind": "AdmissionReview",
            "response": {
                "uid": uid,
                "allowed": False,
                "status": {
                    "code": 500,
                    "message": f"Internal webhook error: {error}"
                }
            }
        }


# ==============================================================================
# Flask Application
# ==============================================================================

def create_app(config: WebhookConfig) -> Flask:
    """
    Create Flask application with webhook endpoints.

    Args:
        config: Webhook configuration

    Returns:
        Flask application
    """
    app = Flask(__name__)
    handler = NamingPolicyWebhookHandler(config)

    @app.route('/validate', methods=['POST'])
    def validate():
        """Webhook endpoint for validation."""
        try:
            admission_review = request.get_json()
            response = handler.handle_admission_review(admission_review)
            return jsonify(response), 200
        except Exception as e:
            app.logger.error(f"Error in /validate endpoint: {e}", exc_info=True)
            return jsonify({
                "apiVersion": "admission.k8s.io/v1",
                "kind": "AdmissionReview",
                "response": {
                    "uid": "unknown",
                    "allowed": config.fail_mode == 'open',
                    "status": {
                        "code": 500,
                        "message": f"Internal error: {str(e)}"
                    }
                }
            }), 500

    @app.route('/health', methods=['GET'])
    def health():
        """Liveness probe endpoint."""
        return jsonify({"status": "healthy"}), 200

    @app.route('/ready', methods=['GET'])
    def ready():
        """Readiness probe endpoint."""
        # Check if validator is initialized
        if handler.validator is not None:
            return jsonify({"status": "ready"}), 200
        else:
            return jsonify({"status": "not ready"}), 503

    @app.route('/metrics', methods=['GET'])
    def metrics():
        """Prometheus metrics endpoint."""
        if config.metrics_enabled:
            return handler.metrics.to_prometheus(), 200, {'Content-Type': 'text/plain'}
        else:
            return "Metrics disabled", 404

    return app


# ==============================================================================
# Main
# ==============================================================================

def main():
    """Main entry point."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Load configuration
    config = WebhookConfig()

    logging.info(f"Starting naming policy webhook server")
    logging.info(f"  Port: {config.webhook_port}")
    logging.info(f"  Fail mode: {config.fail_mode}")
    logging.info(f"  Audit enabled: {config.audit_enabled}")
    logging.info(f"  Metrics enabled: {config.metrics_enabled}")

    # Create Flask app
    app = create_app(config)

    # Check if TLS files exist
    tls_cert_exists = Path(config.tls_cert_file).exists()
    tls_key_exists = Path(config.tls_key_file).exists()

    if tls_cert_exists and tls_key_exists:
        # Run with TLS
        logging.info(f"Starting HTTPS server with TLS")
        logging.info(f"  Cert: {config.tls_cert_file}")
        logging.info(f"  Key: {config.tls_key_file}")

        app.run(
            host='0.0.0.0',
            port=config.webhook_port,
            ssl_context=(config.tls_cert_file, config.tls_key_file)
        )
    else:
        # Run without TLS (for local testing only)
        logging.warning("TLS files not found, running HTTP server (LOCAL TESTING ONLY)")
        logging.warning("  For production, provide TLS_CERT_FILE and TLS_KEY_FILE")

        app.run(
            host='0.0.0.0',
            port=config.webhook_port
        )


if __name__ == '__main__':
    main()

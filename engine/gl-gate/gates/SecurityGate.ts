/**
 * @fileoverview GL-Gate:07 - Security Layer (PII Detection, Data Sanitization)
 * @module @machine-native-ops/gl-gate/gates/SecurityGate
 * @version 1.0.0
 * @since 2026-01-26
 * @author MachineNativeOps
 * @gl-governed true
 * @gl-layer GL-40-GOVERNANCE
 * @gl-gate gl-gate:07
 * 
 * gl-gate:07 — Security Layer (PII Detection, Data Sanitization)
 * gl-gate:07：安全層（PII 偵測、資料淨化）
 * 
 * 負責敏感資訊偵測、資料淨化、權限控管與安全策略執行，
 * 確保資料處理符合隱私與安全要求。
 * 
 * GL Unified Charter Activated
 */

import { BaseGate } from './BaseGate';
import {
  GateId,
  GateContext,
  GateResult,
  GateConfig,
  GateFinding,
  GateMetric
} from '../types';

/**
 * Security Gate Configuration
 */
export interface SecurityGateConfig extends GateConfig {
  /** PII patterns to detect */
  piiPatterns?: PIIPattern[];
  /** Sanitization rules */
  sanitizationRules?: SanitizationRule[];
  /** Security policy checks */
  policyChecks?: SecurityPolicyCheck[];
  /** Enable strict mode */
  strictMode?: boolean;
}

/**
 * PII Pattern definition
 */
export interface PIIPattern {
  name: string;
  pattern: RegExp;
  severity: 'critical' | 'high' | 'medium' | 'low';
  description: string;
}

/**
 * Sanitization Rule
 */
export interface SanitizationRule {
  name: string;
  field: string;
  action: 'mask' | 'hash' | 'remove' | 'encrypt';
}

/**
 * Security Policy Check
 */
export interface SecurityPolicyCheck {
  name: string;
  check: () => Promise<boolean>;
  severity: 'critical' | 'high' | 'medium' | 'low';
}

/**
 * Security scan result
 */
export interface SecurityScanResult {
  piiDetections: PIIDetection[];
  sanitizationStatus: SanitizationStatus[];
  policyViolations: PolicyViolation[];
  accessControlStatus: AccessControlStatus;
  auditLogIntegrity: boolean;
}

export interface PIIDetection {
  type: string;
  location: string;
  severity: string;
  masked: boolean;
}

export interface SanitizationStatus {
  field: string;
  sanitized: boolean;
  method: string;
}

export interface PolicyViolation {
  policy: string;
  description: string;
  severity: string;
}

export interface AccessControlStatus {
  rbacEnabled: boolean;
  leastPrivilegeEnforced: boolean;
  mfaEnabled: boolean;
  sessionManagement: boolean;
}

/**
 * GL-Gate:07 - Security Gate
 * 安全閘門
 * 
 * Validates security compliance including PII detection,
 * data sanitization, access control, and security policies.
 */
export class SecurityGate extends BaseGate {
  public readonly gateId: GateId = 'gl-gate:07';
  public readonly nameEN = 'Security Layer (PII Detection, Data Sanitization)';
  public readonly nameZH = '安全層（PII 偵測、資料淨化）';

  private defaultPIIPatterns: PIIPattern[] = [
    {
      name: 'Email',
      pattern: /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g,
      severity: 'high',
      description: 'Email address detected'
    },
    {
      name: 'Phone',
      pattern: /(\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}/g,
      severity: 'high',
      description: 'Phone number detected'
    },
    {
      name: 'SSN',
      pattern: /\b\d{3}[-]?\d{2}[-]?\d{4}\b/g,
      severity: 'critical',
      description: 'Social Security Number detected'
    },
    {
      name: 'CreditCard',
      pattern: /\b(?:\d{4}[-\s]?){3}\d{4}\b/g,
      severity: 'critical',
      description: 'Credit card number detected'
    },
    {
      name: 'IPAddress',
      pattern: /\b(?:\d{1,3}\.){3}\d{1,3}\b/g,
      severity: 'medium',
      description: 'IP address detected'
    },
    {
      name: 'APIKey',
      pattern: /(?:api[_-]?key|apikey|api_secret)[=:]\s*['"]?[\w-]{20,}['"]?/gi,
      severity: 'critical',
      description: 'API key or secret detected'
    },
    {
      name: 'JWT',
      pattern: /eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*/g,
      severity: 'critical',
      description: 'JWT token detected'
    }
  ];

  /**
   * Execute security gate validation
   */
  public async execute(context: GateContext, config?: SecurityGateConfig): Promise<GateResult> {
    const startTime = Date.now();
    const findings: GateFinding[] = [];
    const metrics: GateMetric[] = [];

    const piiPatterns = config?.piiPatterns ?? this.defaultPIIPatterns;
    const strictMode = config?.strictMode ?? false;

    try {
      // Perform security scan
      const scanResult = await this.performSecurityScan(context, piiPatterns);

      // Process PII detections
      metrics.push(this.createMetric(
        'pii_detections_count',
        scanResult.piiDetections.length,
        'count',
        { component: 'pii' }
      ));

      for (const detection of scanResult.piiDetections) {
        const severity = detection.severity as 'critical' | 'high' | 'medium' | 'low';
        findings.push(this.createFinding(
          severity === 'critical' || severity === 'high' ? 'violation' : 'warning',
          severity,
          `PII Detected: ${detection.type}`,
          `${detection.type} found at ${detection.location}`,
          {
            location: detection.location,
            remediation: detection.masked 
              ? 'PII has been masked but should be reviewed'
              : 'Implement data masking or remove sensitive data'
          }
        ));
      }

      // Process sanitization status
      const sanitizedCount = scanResult.sanitizationStatus.filter(s => s.sanitized).length;
      const totalFields = scanResult.sanitizationStatus.length;
      
      metrics.push(this.createMetric(
        'sanitization_coverage',
        totalFields > 0 ? sanitizedCount / totalFields : 1,
        'ratio',
        { component: 'sanitization' }
      ));

      for (const status of scanResult.sanitizationStatus) {
        if (!status.sanitized) {
          findings.push(this.createFinding(
            'warning',
            'medium',
            'Unsanitized Field',
            `Field "${status.field}" is not sanitized`,
            {
              remediation: `Apply ${status.method} sanitization to field "${status.field}"`
            }
          ));
        }
      }

      // Process policy violations
      metrics.push(this.createMetric(
        'policy_violations_count',
        scanResult.policyViolations.length,
        'count',
        { component: 'policy' }
      ));

      for (const violation of scanResult.policyViolations) {
        findings.push(this.createFinding(
          'violation',
          violation.severity as 'critical' | 'high' | 'medium' | 'low',
          `Policy Violation: ${violation.policy}`,
          violation.description,
          {
            remediation: `Review and remediate ${violation.policy} policy violation`
          }
        ));
      }

      // Check access control
      const accessControl = scanResult.accessControlStatus;
      
      metrics.push(this.createMetric(
        'rbac_enabled',
        accessControl.rbacEnabled ? 1 : 0,
        'boolean',
        { component: 'access_control' }
      ));

      metrics.push(this.createMetric(
        'least_privilege_enforced',
        accessControl.leastPrivilegeEnforced ? 1 : 0,
        'boolean',
        { component: 'access_control' }
      ));

      metrics.push(this.createMetric(
        'mfa_enabled',
        accessControl.mfaEnabled ? 1 : 0,
        'boolean',
        { component: 'access_control' }
      ));

      if (!accessControl.rbacEnabled) {
        findings.push(this.createFinding(
          strictMode ? 'violation' : 'warning',
          'high',
          'RBAC Not Enabled',
          'Role-Based Access Control is not enabled',
          {
            remediation: 'Implement RBAC for proper access control'
          }
        ));
      }

      if (!accessControl.leastPrivilegeEnforced) {
        findings.push(this.createFinding(
          'warning',
          'medium',
          'Least Privilege Not Enforced',
          'Least privilege principle is not fully enforced',
          {
            remediation: 'Review and restrict permissions to minimum required'
          }
        ));
      }

      // Check audit log integrity
      metrics.push(this.createMetric(
        'audit_log_integrity',
        scanResult.auditLogIntegrity ? 1 : 0,
        'boolean',
        { component: 'audit' }
      ));

      if (!scanResult.auditLogIntegrity) {
        findings.push(this.createFinding(
          'violation',
          'critical',
          'Audit Log Integrity Compromised',
          'Audit log integrity check failed',
          {
            remediation: 'Investigate audit log tampering and restore integrity'
          }
        ));
      }

      // Calculate security score
      const securityScore = this.calculateSecurityScore(scanResult, findings);
      metrics.push(this.createMetric(
        'security_score',
        securityScore,
        'score',
        { component: 'overall' }
      ));

      // Determine overall status
      const status = this.determineStatus(findings);
      const message = this.generateResultMessage(findings, securityScore);

      if (status === 'passed') {
        return this.createSuccessResult(context, message, findings, metrics, startTime);
      } else if (status === 'warning') {
        return this.createWarningResult(context, message, findings, metrics, startTime);
      } else {
        return this.createFailedResult(context, message, findings, metrics, startTime);
      }

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      findings.push(this.createFinding(
        'violation',
        'critical',
        'Security Gate Execution Error',
        `Failed to execute security gate: ${errorMessage}`
      ));
      return this.createFailedResult(context, `Security gate failed: ${errorMessage}`, findings, metrics, startTime);
    }
  }

  /**
   * Perform security scan
   */
  private async performSecurityScan(
    _context: GateContext,
    _piiPatterns: PIIPattern[]
  ): Promise<SecurityScanResult> {
    // Simulated scan - in production, integrate with security scanning tools
    // TODO: Replace with actual security scanning integration (e.g., SAST, DAST tools)
    return {
      piiDetections: [],
      sanitizationStatus: [
        { field: 'user.email', sanitized: true, method: 'mask' },
        { field: 'user.phone', sanitized: true, method: 'hash' },
        { field: 'payment.card', sanitized: true, method: 'encrypt' }
      ],
      policyViolations: [],
      accessControlStatus: {
        rbacEnabled: true,
        leastPrivilegeEnforced: true,
        mfaEnabled: true,
        sessionManagement: true
      },
      auditLogIntegrity: true
    };
  }

  /**
   * Calculate security score (0-100)
   */
  private calculateSecurityScore(result: SecurityScanResult, findings: GateFinding[]): number {
    let score = 100;

    // Deduct for PII detections
    score -= result.piiDetections.length * 5;

    // Deduct for policy violations
    score -= result.policyViolations.length * 10;

    // Deduct for access control issues
    if (!result.accessControlStatus.rbacEnabled) score -= 15;
    if (!result.accessControlStatus.leastPrivilegeEnforced) score -= 10;
    if (!result.accessControlStatus.mfaEnabled) score -= 10;

    // Deduct for audit log issues
    if (!result.auditLogIntegrity) score -= 20;

    // Deduct based on finding severity
    for (const finding of findings) {
      if (finding.severity === 'critical') score -= 15;
      else if (finding.severity === 'high') score -= 10;
      else if (finding.severity === 'medium') score -= 5;
      else if (finding.severity === 'low') score -= 2;
    }

    return Math.max(0, Math.min(100, score));
  }

  /**
   * Generate result message
   */
  private generateResultMessage(findings: GateFinding[], securityScore: number): string {
    const violations = findings.filter(f => f.type === 'violation').length;
    const warnings = findings.filter(f => f.type === 'warning').length;

    if (violations === 0 && warnings === 0) {
      return `Security gate passed. Security score: ${securityScore}/100`;
    }

    const parts: string[] = [];
    if (violations > 0) parts.push(`${violations} violation(s)`);
    if (warnings > 0) parts.push(`${warnings} warning(s)`);

    return `Security gate completed with ${parts.join(' and ')}. Security score: ${securityScore}/100`;
  }
}

// GL Unified Charter Activated
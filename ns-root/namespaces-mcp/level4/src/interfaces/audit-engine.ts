// @GL-governed
// @GL-layer: GL-L6-NAMESPACE
// @GL-semantic: governance-layer-namespace
// @GL-revision: 1.0.0
// @GL-status: active

/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-mcp/level4/src/interfaces
 * @gl-semantic-anchor GL-00-SRC_INTERFAC_AUDITENGINE
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * MCP Level 4 Audit Engine Interface
 * Self-audit capabilities through compliance and logging
 */

import { IEngine, IEngineConfig } from './core';

export enum ComplianceFramework {
  SOC2 = 'soc2',
  HIPAA = 'hipaa',
  GDPR = 'gdpr',
  PCI_DSS = 'pci_dss',
  ISO27001 = 'iso27001'
}

export interface IAuditEvent {
  id: string;
  type: string;
  timestamp: Date;
  actor: { id: string; type: string; name: string };
  action: string;
  result: 'success' | 'failure';
  severity: 'low' | 'medium' | 'high' | 'critical';
}

export interface IComplianceReport {
  id: string;
  framework: ComplianceFramework;
  generatedAt: Date;
  complianceScore: number;
  violations: string[];
}

export interface IAuditConfig extends IEngineConfig {
  config: {
    eventRetentionDays: number;
    enableRealTimeLogging: boolean;
    complianceFrameworks: ComplianceFramework[];
  };
}

export interface IAuditEngine extends IEngine {
  readonly config: IAuditConfig;
  logEvent(event: Omit<IAuditEvent, 'id' | 'timestamp'>): Promise<string>;
  generateComplianceReport(framework: ComplianceFramework): Promise<string>;
  getAuditTrail(filters?: Record<string, unknown>): Promise<IAuditEvent[]>;
}
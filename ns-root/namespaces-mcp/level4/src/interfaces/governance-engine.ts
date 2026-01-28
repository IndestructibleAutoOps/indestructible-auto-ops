// @GL-governed
// @GL-layer: GL-L6-NAMESPACE
// @GL-semantic: governance-layer-namespace
// @GL-revision: 1.0.0
// @GL-status: active

/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-mcp/level4/src/interfaces
 * @gl-semantic-anchor GL-00-SRC_INTERFAC_GOVERNANCEEN
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * MCP Level 4 Governance Engine Interface
 * Self-governance for policy management and autonomous decisions
 */

import { IEngine, IEngineConfig, AutonomyLevel } from './core';

export enum PolicyType {
  ACCESS_CONTROL = 'access_control',
  RESOURCE_QUOTA = 'resource_quota',
  SECURITY = 'security',
  COMPLIANCE = 'compliance'
}

export interface IGovernancePolicy {
  id: string;
  name: string;
  type: PolicyType;
  rules: Array<{ id: string; condition: string; action: string }>;
  enforcementMode: 'enforce' | 'audit' | 'warn';
}

export interface IGovernanceDecision {
  id: string;
  type: 'approval' | 'rejection' | 'escalation';
  timestamp: Date;
  outcome: 'approved' | 'rejected' | 'escalated';
  rationale: string;
  confidenceScore: number;
  autonomyLevel: AutonomyLevel;
}

export interface IGovernanceConfig extends IEngineConfig {
  config: {
    enableAutonomousDecisions: boolean;
    decisionAutonomyLevel: AutonomyLevel;
    decisionConfidenceThreshold: number;
    enablePolicyEnforcement: boolean;
  };
}

export interface IGovernanceEngine extends IEngine {
  readonly config: IGovernanceConfig;
  createPolicy(policy: Omit<IGovernancePolicy, 'id'>): Promise<string>;
  evaluatePolicies(context: unknown): Promise<{ allowed: boolean; appliedPolicies: string[] }>;
  makeDecision(request: unknown): Promise<string>;
  getDecision(decisionId: string): Promise<IGovernanceDecision | undefined>;
}
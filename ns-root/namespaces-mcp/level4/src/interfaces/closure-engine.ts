/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-mcp/level4/src/interfaces
 * @gl-semantic-anchor GL-00-SRC_INTERFAC_CLOSUREENGIN
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * MCP Level 4 Closure Engine Interface
 * Self-termination for safe lifecycle management
 */

import { IEngine, IEngineConfig } from './core';

export enum ClosureReason {
  PLANNED_MAINTENANCE = 'planned_maintenance',
  RESOURCE_OPTIMIZATION = 'resource_optimization',
  SECURITY_INCIDENT = 'security_incident'
}

export enum ShutdownMode {
  GRACEFUL = 'graceful',
  FORCED = 'forced',
  IMMEDIATE = 'immediate'
}

export interface IClosurePlan {
  id: string;
  reason: ClosureReason;
  shutdownMode: ShutdownMode;
  targets: string[];
  status: 'scheduled' | 'in_progress' | 'completed';
  scheduledAt?: Date;
}

export interface IClosureConfig extends IEngineConfig {
  config: {
    enableAutoClosure: boolean;
    defaultShutdownMode: ShutdownMode;
    enableStatePreservation: boolean;
  };
}

export interface IClosureEngine extends IEngine {
  readonly config: IClosureConfig;
  createClosurePlan(plan: Omit<IClosurePlan, 'id' | 'status'>): Promise<string>;
  executeClosurePlan(planId: string): Promise<string>;
  gracefulShutdown(targetId: string, timeoutSeconds: number): Promise<void>;
}
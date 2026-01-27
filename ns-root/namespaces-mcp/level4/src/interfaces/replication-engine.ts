/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-mcp/level4/src/interfaces
 * @gl-semantic-anchor GL-00-SRC_INTERFAC_REPLICATIONE
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * MCP Level 4 Replication Engine Interface
 * Self-replication for auto-scaling
 */

import { IEngine, IEngineConfig } from './core';

export enum ScalingPolicy {
  CPU_BASED = 'cpu_based',
  MEMORY_BASED = 'memory_based',
  REQUEST_BASED = 'request_based'
}

export interface IReplica {
  id: string;
  parentId: string;
  status: 'pending' | 'active' | 'terminating';
  health: 'healthy' | 'unhealthy';
  metrics: {
    cpuPercent: number;
    memoryPercent: number;
    requestsPerSecond: number;
  };
}

export interface IScalingRule {
  id: string;
  policy: ScalingPolicy;
  targetId: string;
  scaleUpThreshold: number;
  scaleDownThreshold: number;
  minReplicas: number;
  maxReplicas: number;
}

export interface IReplicationConfig extends IEngineConfig {
  config: {
    enableAutoScaling: boolean;
    defaultScalingPolicy: ScalingPolicy;
    minReplicas: number;
    maxReplicas: number;
  };
}

export interface IReplicationEngine extends IEngine {
  readonly config: IReplicationConfig;
  createReplica(parentId: string, configuration: unknown): Promise<string>;
  createScalingRule(rule: Omit<IScalingRule, 'id'>): Promise<string>;
  scale(targetId: string, replicaCount: number): Promise<string>;
}
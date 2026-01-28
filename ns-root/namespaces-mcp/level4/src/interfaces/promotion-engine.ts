// @GL-governed
// @GL-layer: GL-L6-NAMESPACE
// @GL-semantic: governance-layer-namespace
// @GL-revision: 1.0.0
// @GL-status: active

/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-mcp/level4/src/interfaces
 * @gl-semantic-anchor GL-00-SRC_INTERFAC_PROMOTIONENG
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * MCP Level 4 Promotion Engine Interface
 * Self-promotion through deployment automation
 */

import { IEngine, IEngineConfig } from './core';

export enum DeploymentEnvironment {
  DEVELOPMENT = 'development',
  STAGING = 'staging',
  PRODUCTION = 'production'
}

export enum DeploymentStrategy {
  BLUE_GREEN = 'blue_green',
  CANARY = 'canary',
  ROLLING = 'rolling'
}

export interface IPromotionRequest {
  id: string;
  artifactId: string;
  sourceEnvironment: DeploymentEnvironment;
  targetEnvironment: DeploymentEnvironment;
  strategy: DeploymentStrategy;
  status: 'pending' | 'approved' | 'in_progress' | 'completed' | 'failed';
}

export interface IPromotionConfig extends IEngineConfig {
  config: {
    enableAutoPromotion: boolean;
    defaultStrategy: DeploymentStrategy;
    validationChecks: string[];
  };
}

export interface IPromotionEngine extends IEngine {
  readonly config: IPromotionConfig;
  createPromotionRequest(request: Omit<IPromotionRequest, 'id' | 'status'>): Promise<string>;
  executePromotion(requestId: string): Promise<unknown>;
  rollbackPromotion(requestId: string): Promise<void>;
}
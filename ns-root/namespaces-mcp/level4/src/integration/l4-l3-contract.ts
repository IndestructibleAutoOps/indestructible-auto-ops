// @GL-governed
// @GL-layer: GL-L6-NAMESPACE
// @GL-semantic: governance-layer-namespace
// @GL-revision: 1.0.0
// @GL-status: active

/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-mcp/level4/src/integration
 * @gl-semantic-anchor GL-00-SRC_INTEGRAT_L4L3CONTRACT
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * MCP Level 4-Level 3 Integration Contract
 * 
 * Defines the contract between Level 4 autonomous engines and Level 3 engines.
 * 
 * @module l4-l3-contract
 * @version 1.0.0
 */

export enum L3EngineName {
  RAG = 'rag',
  DAG = 'dag',
  VALIDATION = 'validation',
  PROMOTION = 'promotion',
  GOVERNANCE = 'governance'
}

export interface IL3EngineMethod {
  engine: L3EngineName;
  method: string;
  parameters?: Record<string, any>;
  timeout?: number;
}

export interface IL3EngineResponse<T = unknown> {
  success: boolean;
  data?: T;
  error?: { code: string; message: string };
  metadata: {
    engine: L3EngineName;
    method: string;
    timestamp: Date;
    durationMs: number;
  };
}

export interface IL3Event {
  id: string;
  type: string;
  source: L3EngineName;
  timestamp: Date;
  data: Record<string, unknown>;
}

export interface IL4L3Contract {
  callL3Method<T = unknown>(method: IL3EngineMethod): Promise<IL3EngineResponse<T>>;
  subscribeL3Event(engine: L3EngineName, eventType: string, callback: (event: IL3Event) => void): Promise<string>;
  unsubscribeL3Event(subscriptionId: string): Promise<void>;
  getL3EngineStatus(engine: L3EngineName): Promise<{ status: string; metrics: unknown }>;
}
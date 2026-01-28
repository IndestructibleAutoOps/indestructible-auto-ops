// @GL-governed
// @GL-layer: GL-L0-UNCLASSIFIED
// @GL-semantic: governance-layer-unclassified
// @GL-revision: 1.0.0
// @GL-status: active

export type AgentSignal = 'info' | 'warn' | 'error';

export interface AgentContext {
  readonly requestId: string;
  readonly timestamp: Date;
  readonly payload?: Record<string, unknown>;
}

export interface AgentInsight {
  title: string;
  description: string;
  signal: AgentSignal;
  data?: Record<string, unknown>;
}

export interface AgentReport {
  agent: string;
  insights: AgentInsight[];
  generatedAt: Date;
}

export interface AgentModule {
  readonly name: string;
  run(context: AgentContext): Promise<AgentReport>;
}

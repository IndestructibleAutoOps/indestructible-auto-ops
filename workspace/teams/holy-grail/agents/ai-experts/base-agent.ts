// @GL-governed
// @GL-layer: GL-L0-UNCLASSIFIED
// @GL-semantic: governance-layer-unclassified
// @GL-revision: 1.0.0
// @GL-status: active

import { AgentContext, AgentInsight, AgentModule, AgentReport } from '../types.js';

export abstract class BaseAgent implements AgentModule {
  public abstract readonly name: string;

  public async run(context: AgentContext): Promise<AgentReport> {
    const insights = await this.evaluate(context);
    return {
      agent: this.name,
      insights,
      generatedAt: new Date()
    };
  }

  protected abstract evaluate(context: AgentContext): Promise<AgentInsight[]>;
}

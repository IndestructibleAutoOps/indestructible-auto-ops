// @GL-governed
// @GL-layer: GL-L0-UNCLASSIFIED
// @GL-semantic: governance-layer-unclassified
// @GL-revision: 1.0.0
// @GL-status: active

import { AgentContext, AgentInsight } from '../../types.js';

export class ProductFeedback {
  analyze(context: AgentContext): AgentInsight {
    const inputs = this.extractInputs(context);
    return {
      title: 'Feedback Analysis',
      description: `Processed ${inputs.length} feedback signals`,
      signal: 'info',
      data: { inputs },
    };
  }

  private extractInputs(context: AgentContext): string[] {
    const payload = context.payload ?? {};
    const inputs = payload['feedback'];
    if (Array.isArray(inputs)) {
      return inputs.filter((item): item is string => typeof item === 'string');
    }
    return [];
  }
}

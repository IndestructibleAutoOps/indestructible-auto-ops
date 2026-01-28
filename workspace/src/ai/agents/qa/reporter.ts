// @GL-governed
// @GL-layer: GL-L0-UNCLASSIFIED
// @GL-semantic: governance-layer-unclassified
// @GL-revision: 1.0.0
// @GL-status: active

import { AgentContext, AgentInsight } from '../../types.js';

export class QAReporter {
  report(context: AgentContext): AgentInsight {
    const duration = this.extractDuration(context);
    return {
      title: 'QA Report',
      description: `Total duration ${duration} minutes`,
      signal: duration > 60 ? 'warn' : 'info'
    };
  }

  private extractDuration(context: AgentContext): number {
    const payload = context.payload ?? {};
    const duration = payload['qaDurationMinutes'];
    if (typeof duration === 'number') {
      return Math.max(0, duration);
    }
    return 18;
  }
}

// @GL-governed
// @GL-layer: GL-L0-UNCLASSIFIED
// @GL-semantic: governance-layer-unclassified
// @GL-revision: 1.0.0
// @GL-status: active

import { AgentContext, AgentInsight } from '../../types.js';

export class ProductRoadmap {
  plan(context: AgentContext): AgentInsight {
    const horizon = this.resolveHorizon(context);
    return {
      title: 'Roadmap Plan',
      description: `Planning horizon ${horizon} quarters`,
      signal: horizon > 4 ? 'warn' : 'info',
    };
  }

  private resolveHorizon(context: AgentContext): number {
    const payload = context.payload ?? {};
    const horizon = payload['roadmapHorizon'];
    if (typeof horizon === 'number') {
      return Math.max(1, Math.min(8, horizon));
    }
    return 3;
  }
}

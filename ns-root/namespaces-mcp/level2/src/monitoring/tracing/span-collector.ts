// @GL-governed
// @GL-layer: GL-L6-NAMESPACE
// @GL-semantic: governance-layer-namespace
// @GL-revision: 1.0.0
// @GL-status: active

/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-mcp/level2/src/monitoring/tracing
 * @gl-semantic-anchor GL-00-MONITORI_TRACING_SPANCOLLECTO
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * Span Collector - Span Collection and Storage
 * 
 * @version 1.0.0
 */

import { EventEmitter } from 'events';
import { Span } from './trace-manager';

export class SpanCollector extends EventEmitter {
  private spans: Span[];
  private maxSpans: number;
  
  constructor(config?: { maxSpans?: number }) {
    super();
    this.spans = [];
    this.maxSpans = config?.maxSpans || 100000;
  }
  
  collect(span: Span): void {
    this.spans.push(span);
    
    if (this.spans.length > this.maxSpans) {
      this.spans.shift();
    }
    
    this.emit('span:collected', { span });
  }
  
  getSpans(traceId?: string): Span[] {
    if (traceId) {
      return this.spans.filter(s => s.traceId === traceId);
    }
    return [...this.spans];
  }
  
  clear(): void {
    this.spans = [];
  }
}

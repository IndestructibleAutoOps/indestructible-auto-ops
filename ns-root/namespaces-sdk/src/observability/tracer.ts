// @GL-governed
// @GL-layer: GL-L6-NAMESPACE
// @GL-semantic: governance-layer-namespace
// @GL-revision: 1.0.0
// @GL-status: active

/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-sdk/src/observability
 * @gl-semantic-anchor GL-00-SRC_OBSERVAB_TRACER
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * Distributed Tracing
 * 
 * Implements tracing for tool invocations and cross-service calls.
 */

import { randomUUID } from 'crypto';

/**
 * Span status
 */
export interface SpanStatus {
  /** Status code (0 = OK, 1 = ERROR) */
  code: number;
  
  /** Status message */
  message?: string;
}

/**
 * Span attributes
 */
export type SpanAttributes = Record<string, string | number | boolean>;

/**
 * Span interface
 */
export interface Span {
  /** Span ID */
  spanId: string;
  
  /** Trace ID */
  traceId: string;
  
  /** Parent span ID */
  parentSpanId?: string;
  
  /** Span name */
  name: string;
  
  /** Start timestamp */
  startTime: Date;
  
  /** End timestamp */
  endTime?: Date;
  
  /** Span attributes */
  attributes: SpanAttributes;
  
  /** Span status */
  status?: SpanStatus;
  
  /** Span events */
  events: SpanEvent[];
}

/**
 * Span event
 */
export interface SpanEvent {
  /** Event name */
  name: string;
  
  /** Event timestamp */
  timestamp: Date;
  
  /** Event attributes */
  attributes?: SpanAttributes;
}

/**
 * Tracer options
 */
export interface TracerOptions {
  /** Enable tracing */
  enabled?: boolean;
  
  /** Service name */
  serviceName?: string;
  
  /** Sampling rate (0-1) */
  samplingRate?: number;
  
  /** Custom span processor */
  processor?: (span: Span) => void;
}

/**
 * Tracer Class
 * 
 * Responsibilities:
 * - Generate trace spans for operations
 * - Propagate trace context across boundaries
 * - Support distributed tracing standards
 * - Export traces to monitoring systems
 */
export class Tracer {
  private options: Required<TracerOptions>;
  private activeSpans: Map<string, Span> = new Map();
  private completedSpans: Span[] = [];
  private currentTraceId?: string;

  constructor(options: TracerOptions = {}) {
    this.options = {
      enabled: options.enabled !== false,
      serviceName: options.serviceName || 'namespace-sdk',
      samplingRate: options.samplingRate || 1.0,
      processor: options.processor || this.defaultProcessor.bind(this)
    };
  }

  /**
   * Start a new span
   */
  startSpan(name: string, attributes?: SpanAttributes): Span {
    if (!this.options.enabled || !this.shouldSample()) {
      return this.createNoOpSpan(name);
    }

    const spanId = this.generateSpanId();
    const traceId = this.currentTraceId || this.generateTraceId();
    
    // Set current trace ID if not set
    if (!this.currentTraceId) {
      this.currentTraceId = traceId;
    }

    const span: Span = {
      spanId,
      traceId,
      name,
      startTime: new Date(),
      attributes: {
        'service.name': this.options.serviceName,
        ...attributes
      },
      events: [],
      end: () => {
        this.endSpan(span);
      }
    };

    this.activeSpans.set(spanId, span);

    return {
      ...span,
      setStatus: (status: SpanStatus) => {
        span.status = status;
      },
      setAttribute: (key: string, value: string | number | boolean) => {
        span.attributes[key] = value;
      },
      addEvent: (name: string, attributes?: SpanAttributes) => {
        span.events.push({
          name,
          timestamp: new Date(),
          attributes
        });
      },
      end: () => {
        this.endSpan(span);
      }
    } as any;
  }

  /**
   * Start a child span
   */
  startChildSpan(
    parentSpan: Span,
    name: string,
    attributes?: SpanAttributes
  ): Span {
    if (!this.options.enabled) {
      return this.createNoOpSpan(name);
    }

    const spanId = this.generateSpanId();
    
    const span: Span = {
      spanId,
      traceId: parentSpan.traceId,
      parentSpanId: parentSpan.spanId,
      name,
      startTime: new Date(),
      attributes: {
        'service.name': this.options.serviceName,
        ...attributes
      },
      events: [],
      end: () => {}
    }
    span.end = () => { this.endSpan(span); };

    this.activeSpans.set(spanId, span);

    return {
      ...span,
      setStatus: (status: SpanStatus) => {
        span.status = status;
      },
      setAttribute: (key: string, value: string | number | boolean) => {
        span.attributes[key] = value;
      },
      addEvent: (name: string, attributes?: SpanAttributes) => {
        span.events.push({
          name,
          timestamp: new Date(),
          attributes
        });
      },
      end: () => {
        this.endSpan(span);
      }
    } as any;
  }

  /**
   * End a span
   */
  private endSpan(span: Span): void {
    span.endTime = new Date();
    this.activeSpans.delete(span.spanId);
    this.completedSpans.push(span);
    
    // Process the span
    this.options.processor(span);
  }

  /**
   * Get current trace ID
   */
  getCurrentTraceId(): string | undefined {
    return this.currentTraceId;
  }

  /**
   * Set current trace ID
   */
  setCurrentTraceId(traceId: string): void {
    this.currentTraceId = traceId;
  }

  /**
   * Clear current trace ID
   */
  clearCurrentTraceId(): void {
    this.currentTraceId = undefined;
  }

  /**
   * Get active spans
   */
  getActiveSpans(): Span[] {
    return Array.from(this.activeSpans.values());
  }

  /**
   * Get completed spans
   */
  getCompletedSpans(): Span[] {
    return [...this.completedSpans];
  }

  /**
   * Clear completed spans
   */
  clearCompletedSpans(): void {
    this.completedSpans = [];
  }

  /**
   * Flush all spans
   */
  async flush(): Promise<void> {
    // End all active spans
    for (const span of this.activeSpans.values()) {
      this.endSpan(span);
    }

    // Clear completed spans
    this.completedSpans = [];
    this.currentTraceId = undefined;
  }

  /**
   * Enable or disable tracing
   */
  setEnabled(enabled: boolean): void {
    this.options.enabled = enabled;
  }

  /**
   * Check if tracing is enabled
   */
  isEnabled(): boolean {
    return this.options.enabled;
  }

  /**
   * Generate a span ID
   */
  private generateSpanId(): string {
    return randomUUID().replace(/-/g, '').substring(0, 16);
  }

  /**
   * Generate a trace ID
   */
  private generateTraceId(): string {
    return randomUUID().replace(/-/g, '');
  }

  /**
   * Check if span should be sampled
   */
  private shouldSample(): boolean {
    return Math.random() < this.options.samplingRate;
  }

  /**
   * Create a no-op span
   */
  private createNoOpSpan(name: string): Span {
    return {
      spanId: '',
      traceId: '',
      name,
      startTime: new Date(),
      attributes: {},
      events: [],
      setStatus: () => {},
      setAttribute: () => {},
      addEvent: () => {},
      end: () => {}
    } as any;
  }

  /**
   * Default span processor
   */
  private defaultProcessor(span: Span): void {
    // Default processor just logs the span
    // In production, this would export to a tracing backend
    if (this.options.enabled) {
      const duration = span.endTime
        ? span.endTime.getTime() - span.startTime.getTime()
        : 0;

      console.debug('[TRACE]', {
        traceId: span.traceId,
        spanId: span.spanId,
        name: span.name,
        duration: `${duration}ms`,
        status: span.status?.code === 0 ? 'OK' : 'ERROR'
      });
    }
  }
}

/**
 * Create a tracer instance
 */
export function createTracer(options?: TracerOptions): Tracer {
  return new Tracer(options);
}
/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-sdk/src/observability
 * @gl-semantic-anchor GL-00-SRC_OBSERVAB_METRICS
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * Metrics Collection
 * 
 * Collects and exports metrics on SDK usage, performance, and errors.
 */

/**
 * Metric type enumeration
 */
export enum MetricType {
  COUNTER = 'counter',
  GAUGE = 'gauge',
  HISTOGRAM = 'histogram'
}

/**
 * Metric labels
 */
export type MetricLabels = Record<string, string>;

/**
 * Metric value
 */
export interface MetricValue {
  /** Metric name */
  name: string;
  
  /** Metric type */
  type: MetricType;
  
  /** Metric value */
  value: number;
  
  /** Metric labels */
  labels: MetricLabels;
  
  /** Timestamp */
  timestamp: Date;
}

/**
 * Histogram bucket
 */
export interface HistogramBucket {
  /** Upper bound */
  le: number;
  
  /** Count */
  count: number;
}

/**
 * Histogram data
 */
export interface HistogramData {
  /** Sum of all values */
  sum: number;
  
  /** Count of all values */
  count: number;
  
  /** Buckets */
  buckets: HistogramBucket[];
}

/**
 * Metrics collector options
 */
export interface MetricsCollectorOptions {
  /** Enable metrics collection */
  enabled?: boolean;
  
  /** Metrics prefix */
  prefix?: string;
  
  /** Default labels */
  defaultLabels?: MetricLabels;
  
  /** Histogram buckets */
  histogramBuckets?: number[];
  
  /** Custom metrics handler */
  handler?: (metric: MetricValue) => void;
}

/**
 * Metrics Collector Class
 * 
 * Responsibilities:
 * - Track counters, gauges, and histograms
 * - Support metric labels for dimensions
 * - Export metrics to monitoring systems
 * - Minimize performance overhead
 */
export class MetricsCollector {
  private options: Required<MetricsCollectorOptions>;
  private counters: Map<string, number> = new Map();
  private gauges: Map<string, number> = new Map();
  private histograms: Map<string, HistogramData> = new Map();

  constructor(options: MetricsCollectorOptions = {}) {
    this.options = {
      enabled: options.enabled !== false,
      prefix: options.prefix || 'namespace_sdk',
      defaultLabels: options.defaultLabels || {},
      histogramBuckets: options.histogramBuckets || [
        0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10
      ],
      handler: options.handler || this.defaultHandler.bind(this)
    };
  }

  /**
   * Increment a counter
   */
  increment(name: string, labels?: MetricLabels, value: number = 1): void {
    if (!this.options.enabled) {
      return;
    }

    const key = this.getMetricKey(name, labels);
    const current = this.counters.get(key) || 0;
    this.counters.set(key, current + value);

    this.emitMetric({
      name: this.prefixName(name),
      type: MetricType.COUNTER,
      value: current + value,
      labels: this.mergeLabels(labels),
      timestamp: new Date()
    });
  }

  /**
   * Decrement a counter
   */
  decrement(name: string, labels?: MetricLabels, value: number = 1): void {
    this.increment(name, labels, -value);
  }

  /**
   * Set a gauge value
   */
  setGauge(name: string, value: number, labels?: MetricLabels): void {
    if (!this.options.enabled) {
      return;
    }

    const key = this.getMetricKey(name, labels);
    this.gauges.set(key, value);

    this.emitMetric({
      name: this.prefixName(name),
      type: MetricType.GAUGE,
      value,
      labels: this.mergeLabels(labels),
      timestamp: new Date()
    });
  }

  /**
   * Increment a gauge
   */
  incrementGauge(name: string, labels?: MetricLabels, value: number = 1): void {
    const key = this.getMetricKey(name, labels);
    const current = this.gauges.get(key) || 0;
    this.setGauge(name, current + value, labels);
  }

  /**
   * Decrement a gauge
   */
  decrementGauge(name: string, labels?: MetricLabels, value: number = 1): void {
    this.incrementGauge(name, labels, -value);
  }

  /**
   * Record a histogram value
   */
  recordHistogram(name: string, value: number, labels?: MetricLabels): void {
    if (!this.options.enabled) {
      return;
    }

    const key = this.getMetricKey(name, labels);
    let histogram = this.histograms.get(key);

    if (!histogram) {
      histogram = {
        sum: 0,
        count: 0,
        buckets: this.options.histogramBuckets.map(le => ({ le, count: 0 }))
      };
      this.histograms.set(key, histogram);
    }

    histogram.sum += value;
    histogram.count++;

    // Update buckets
    for (const bucket of histogram.buckets) {
      if (value <= bucket.le) {
        bucket.count++;
      }
    }

    this.emitMetric({
      name: this.prefixName(name),
      type: MetricType.HISTOGRAM,
      value,
      labels: this.mergeLabels(labels),
      timestamp: new Date()
    });
  }

  /**
   * Record a metric value
   *
   * This provides a generic interface used by callers such as the
   * instant-execution engine, and delegates to the appropriate
   * type-specific metric method.
   */
  recordMetric(name: string, type: MetricType, value: number, labels?: MetricLabels): void {
    switch (type) {
      case MetricType.COUNTER:
        this.increment(name, labels, value);
        break;
      case MetricType.GAUGE:
        this.setGauge(name, value, labels);
        break;
      case MetricType.HISTOGRAM:
        this.recordHistogram(name, value, labels);
        break;
      default:
        // Unknown metric type; ignore to preserve backwards compatibility
        break;
    }
  }

  /**
   * Get counter value
   */
  getCounter(name: string, labels?: MetricLabels): number {
    const key = this.getMetricKey(name, labels);
    return this.counters.get(key) || 0;
  }

  /**
   * Get gauge value
   */
  getGauge(name: string, labels?: MetricLabels): number {
    const key = this.getMetricKey(name, labels);
    return this.gauges.get(key) || 0;
  }

  /**
   * Get histogram data
   */
  getHistogram(name: string, labels?: MetricLabels): HistogramData | undefined {
    const key = this.getMetricKey(name, labels);
    return this.histograms.get(key);
  }

  /**
   * Get all metrics
   */
  getAllMetrics(): {
    counters: Map<string, number>;
    gauges: Map<string, number>;
    histograms: Map<string, HistogramData>;
  } {
    return {
      counters: new Map(this.counters),
      gauges: new Map(this.gauges),
      histograms: new Map(this.histograms)
    };
  }

  /**
   * Reset all metrics
   */
  reset(): void {
    this.counters.clear();
    this.gauges.clear();
    this.histograms.clear();
  }

  /**
   * Flush metrics
   */
  async flush(): Promise<void> {
    // Flush any buffered metrics
    // In production, this would export to a metrics backend
  }

  /**
   * Enable or disable metrics collection
   */
  setEnabled(enabled: boolean): void {
    this.options.enabled = enabled;
  }

  /**
   * Check if metrics collection is enabled
   */
  isEnabled(): boolean {
    return this.options.enabled;
  }

  /**
   * Export metrics in Prometheus format
   */
  exportPrometheus(): string {
    const lines: string[] = [];

    // Export counters
    for (const [key, value] of this.counters.entries()) {
      const { name, labels } = this.parseMetricKey(key);
      const labelsStr = this.formatLabels(labels);
      lines.push(`${name}${labelsStr} ${value}`);
    }

    // Export gauges
    for (const [key, value] of this.gauges.entries()) {
      const { name, labels } = this.parseMetricKey(key);
      const labelsStr = this.formatLabels(labels);
      lines.push(`${name}${labelsStr} ${value}`);
    }

    // Export histograms
    for (const [key, histogram] of this.histograms.entries()) {
      const { name, labels } = this.parseMetricKey(key);
      const labelsStr = this.formatLabels(labels);

      // Buckets
      for (const bucket of histogram.buckets) {
        const bucketLabels = { ...labels, le: bucket.le.toString() };
        const bucketLabelsStr = this.formatLabels(bucketLabels);
        lines.push(`${name}_bucket${bucketLabelsStr} ${bucket.count}`);
      }

      // Sum and count
      lines.push(`${name}_sum${labelsStr} ${histogram.sum}`);
      lines.push(`${name}_count${labelsStr} ${histogram.count}`);
    }

    return lines.join('\n');
  }

  /**
   * Get metric key
   */
  private getMetricKey(name: string, labels?: MetricLabels): string {
    const mergedLabels = this.mergeLabels(labels);
    const labelsStr = Object.entries(mergedLabels)
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([k, v]) => `${k}=${v}`)
      .join(',');
    
    return labelsStr ? `${name}{${labelsStr}}` : name;
  }

  /**
   * Parse metric key
   */
  private parseMetricKey(key: string): { name: string; labels: MetricLabels } {
    const match = key.match(/^([^{]+)(?:\{([^}]+)\})?$/);
    
    if (!match) {
      return { name: key, labels: {} };
    }

    const name = match[1];
    const labelsStr = match[2];
    const labels: MetricLabels = {};

    if (labelsStr) {
      for (const pair of labelsStr.split(',')) {
        const [k, v] = pair.split('=');
        labels[k] = v;
      }
    }

    return { name, labels };
  }

  /**
   * Prefix metric name
   */
  private prefixName(name: string): string {
    return this.options.prefix ? `${this.options.prefix}_${name}` : name;
  }

  /**
   * Merge labels with default labels
   */
  private mergeLabels(labels?: MetricLabels): MetricLabels {
    return {
      ...this.options.defaultLabels,
      ...labels
    };
  }

  /**
   * Format labels for Prometheus
   */
  private formatLabels(labels: MetricLabels): string {
    const entries = Object.entries(labels);
    
    if (entries.length === 0) {
      return '';
    }

    const labelsStr = entries
      .map(([k, v]) => `${k}="${v}"`)
      .join(',');
    
    return `{${labelsStr}}`;
  }

  /**
   * Emit a metric
   */
  private emitMetric(metric: MetricValue): void {
    this.options.handler(metric);
  }

  /**
   * Default metrics handler
   */
  private defaultHandler(metric: MetricValue): void {
    // Default handler does nothing
    // In production, this would export to a metrics backend
  }
}

/**
 * Metrics type alias for MetricsCollector
 */
export type Metrics = MetricsCollector;

/**
 * Create a metrics collector instance
 */
export function createMetricsCollector(
  options?: MetricsCollectorOptions
): MetricsCollector {
  return new MetricsCollector(options);
}
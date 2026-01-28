// @GL-governed
// @GL-layer: GL-L6-NAMESPACE
// @GL-semantic: governance-layer-namespace
// @GL-revision: 1.0.0
// @GL-status: active

/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-mcp/level2/src/monitoring/logging
 * @gl-semantic-anchor GL-00-MONITORI_LOGGING_LOGAGGREGATO
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * Log Aggregator - Centralized Log Aggregation System
 * 
 * @version 1.0.0
 */

import { EventEmitter } from 'events';
import { LogEntry } from './logger';

export class LogAggregator extends EventEmitter {
  private logs: Map<string, LogEntry[]>;
  private maxLogsPerSource: number;
  
  constructor(config?: { maxLogsPerSource?: number }) {
    super();
    this.logs = new Map();
    this.maxLogsPerSource = config?.maxLogsPerSource || 10000;
  }
  
  aggregate(source: string, entry: LogEntry): void {
    let sourceLogs = this.logs.get(source);
    
    if (!sourceLogs) {
      sourceLogs = [];
      this.logs.set(source, sourceLogs);
    }
    
    sourceLogs.push(entry);
    
    if (sourceLogs.length > this.maxLogsPerSource) {
      sourceLogs.shift();
    }
    
    this.emit('log:aggregated', { source, entry });
  }
  
  getLogs(source?: string): LogEntry[] {
    if (source) {
      return this.logs.get(source) || [];
    }
    
    return Array.from(this.logs.values()).flat();
  }
  
  getSources(): string[] {
    return Array.from(this.logs.keys());
  }
  
  clear(source?: string): void {
    if (source) {
      this.logs.delete(source);
    } else {
      this.logs.clear();
    }
  }
}

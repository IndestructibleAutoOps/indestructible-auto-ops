// @GL-governed
// @GL-layer: GL-L6-NAMESPACE
// @GL-semantic: governance-layer-namespace
// @GL-revision: 1.0.0
// @GL-status: active

/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-sdk/src/observability
 * @gl-semantic-anchor GL-00-SRC_OBSERVAB_AUDIT
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * Audit Trail Capture
 * 
 * Implements audit logging for all sensitive and governance-relevant operations.
 */

/**
 * Audit event
 */
export interface AuditEvent {
  /** Event ID */
  id: string;
  
  /** Event type */
  type: string;
  
  /** Event timestamp */
  timestamp: Date;
  
  /** Actor (user, service, etc.) */
  actor?: {
    id?: string;
    type?: string;
    name?: string;
  };
  
  /** Resource being accessed */
  resource?: {
    type?: string;
    id?: string;
    name?: string;
  };
  
  /** Action performed */
  action: string;
  
  /** Result of the action */
  result: 'success' | 'failure' | 'partial';
  
  /** Additional event data */
  data?: Record<string, any>;
  
  /** Request ID for correlation */
  requestId?: string;
  
  /** Session ID */
  sessionId?: string;
  
  /** IP address */
  ipAddress?: string;
  
  /** User agent */
  userAgent?: string;
}

/**
 * Audit logger options
 */
export interface AuditLoggerOptions {
  /** Enable audit logging */
  enabled?: boolean;
  
  /** Audit log format */
  format?: 'json' | 'text';
  
  /** Include sensitive data */
  includeSensitiveData?: boolean;
  
  /** Custom audit handler */
  handler?: (event: AuditEvent) => void;
  
  /** Retention period in days */
  retentionDays?: number;
}

/**
 * Audit Logger Class
 * 
 * Responsibilities:
 * - Record all sensitive operations
 * - Support tamper-evident storage
 * - Export audit trails for compliance
 * - Align with governance requirements
 */
export class AuditLogger {
  private options: Required<AuditLoggerOptions>;
  private events: AuditEvent[] = [];
  private eventCounter: number = 0;

  constructor(options: AuditLoggerOptions = {}) {
    this.options = {
      enabled: options.enabled !== false,
      format: options.format || 'json',
      includeSensitiveData: options.includeSensitiveData || false,
      handler: options.handler || this.defaultHandler.bind(this),
      retentionDays: options.retentionDays || 90
    };
  }

  /**
   * Log an audit event
   */
  log(
    type: string,
    data?: Record<string, any>,
    options?: {
      actor?: AuditEvent['actor'];
      resource?: AuditEvent['resource'];
      action?: string;
      result?: AuditEvent['result'];
      requestId?: string;
      sessionId?: string;
    }
  ): void {
    if (!this.options.enabled) {
      return;
    }

    const event: AuditEvent = {
      id: this.generateEventId(),
      type,
      timestamp: new Date(),
      actor: options?.actor,
      resource: options?.resource,
      action: options?.action || type,
      result: options?.result || 'success',
      data: this.sanitizeData(data),
      requestId: options?.requestId,
      sessionId: options?.sessionId
    };

    this.events.push(event);
    this.options.handler(event);
  }

  /**
   * Log a successful operation
   */
  logSuccess(
    type: string,
    data?: Record<string, any>,
    options?: Omit<Parameters<typeof this.log>[2], 'result'>
  ): void {
    this.log(type, data, { ...options, result: 'success' });
  }

  /**
   * Log a failed operation
   */
  logFailure(
    type: string,
    data?: Record<string, any>,
    options?: Omit<Parameters<typeof this.log>[2], 'result'>
  ): void {
    this.log(type, data, { ...options, result: 'failure' });
  }

  /**
   * Log credential access
   */
  logCredentialAccess(
    credentialKey: string,
    action: 'get' | 'set' | 'delete' | 'rotate',
    result: 'success' | 'failure',
    options?: {
      actor?: AuditEvent['actor'];
      requestId?: string;
    }
  ): void {
    this.log('credential.access', {
      credentialKey,
      action
    }, {
      ...options,
      resource: {
        type: 'credential',
        id: credentialKey
      },
      action,
      result
    });
  }

  /**
   * Log tool invocation
   */
  logToolInvocation(
    toolName: string,
    result: 'success' | 'failure',
    data?: Record<string, any>,
    options?: {
      actor?: AuditEvent['actor'];
      requestId?: string;
      duration?: number;
    }
  ): void {
    this.log('tool.invocation', {
      toolName,
      duration: options?.duration,
      ...data
    }, {
      ...options,
      resource: {
        type: 'tool',
        name: toolName
      },
      action: 'invoke',
      result
    });
  }

  /**
   * Log configuration change
   */
  logConfigChange(
    configKey: string,
    oldValue: unknown,
    newValue: unknown,
    options?: {
      actor?: AuditEvent['actor'];
      requestId?: string;
    }
  ): void {
    this.log('config.change', {
      configKey,
      oldValue: this.sanitizeValue(oldValue),
      newValue: this.sanitizeValue(newValue)
    }, {
      ...options,
      resource: {
        type: 'config',
        id: configKey
      },
      action: 'update',
      result: 'success'
    });
  }

  /**
   * Log authentication event
   */
  logAuthentication(
    result: 'success' | 'failure',
    data?: Record<string, any>,
    options?: {
      actor?: AuditEvent['actor'];
      requestId?: string;
    }
  ): void {
    this.log('auth.authentication', data, {
      ...options,
      action: 'authenticate',
      result
    });
  }

  /**
   * Log authorization event
   */
  logAuthorization(
    resource: string,
    action: string,
    result: 'success' | 'failure',
    options?: {
      actor?: AuditEvent['actor'];
      requestId?: string;
    }
  ): void {
    this.log('auth.authorization', {
      resource,
      action
    }, {
      ...options,
      resource: {
        type: 'resource',
        id: resource
      },
      action,
      result
    });
  }

  /**
   * Get all audit events
   */
  getEvents(): AuditEvent[] {
    return [...this.events];
  }

  /**
   * Get events by type
   */
  getEventsByType(type: string): AuditEvent[] {
    return this.events.filter(event => event.type === type);
  }

  /**
   * Get events by time range
   */
  getEventsByTimeRange(start: Date, end: Date): AuditEvent[] {
    return this.events.filter(
      event => event.timestamp >= start && event.timestamp <= end
    );
  }

  /**
   * Get events by actor
   */
  getEventsByActor(actorId: string): AuditEvent[] {
    return this.events.filter(event => event.actor?.id === actorId);
  }

  /**
   * Export audit trail
   */
  export(format: 'json' | 'csv' = 'json'): string {
    if (format === 'json') {
      return JSON.stringify(this.events, null, 2);
    } else {
      return this.exportCSV();
    }
  }

  /**
   * Clear old events based on retention policy
   */
  cleanup(): void {
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - this.options.retentionDays);

    const beforeCount = this.events.length;
    this.events = this.events.filter(event => event.timestamp >= cutoffDate);
    const afterCount = this.events.length;

    if (beforeCount !== afterCount) {
      console.log(`Audit cleanup: removed ${beforeCount - afterCount} old events`);
    }
  }

  /**
   * Flush audit events
   */
  async flush(): Promise<void> {
    // Flush any buffered events
    // In production, this would export to an audit backend
    this.events = [];
  }

  /**
   * Enable or disable audit logging
   */
  setEnabled(enabled: boolean): void {
    this.options.enabled = enabled;
  }

  /**
   * Check if audit logging is enabled
   */
  isEnabled(): boolean {
    return this.options.enabled;
  }

  /**
   * Generate event ID
   */
  private generateEventId(): string {
    this.eventCounter++;
    const timestamp = Date.now();
    return `audit_${timestamp}_${this.eventCounter}`;
  }

  /**
   * Sanitize data to remove sensitive information
   */
  private sanitizeData(data?: Record<string, any>): Record<string, any> | undefined {
    if (!data) {
      return undefined;
    }

    if (this.options.includeSensitiveData) {
      return data;
    }

    const sanitized: Record<string, any> = {};

    for (const [key, value] of Object.entries(data)) {
      sanitized[key] = this.sanitizeValue(value);
    }

    return sanitized;
  }

  /**
   * Sanitize a single value
   */
  private sanitizeValue(value: unknown): unknown {
    if (this.options.includeSensitiveData) {
      return value;
    }

    // Redact sensitive fields
    const sensitiveKeys = [
      'password',
      'token',
      'secret',
      'key',
      'credential',
      'apiKey',
      'api_key'
    ];

    if (typeof value === 'string') {
      // Check if this looks like a sensitive value
      if (value.length > 20 && /^[A-Za-z0-9+/=_-]+$/.test(value)) {
        return '[REDACTED]';
      }
    }

    if (typeof value === 'object' && value !== null) {
      const sanitized: Record<string, unknown> = Array.isArray(value) ? [] : {};

      for (const [k, v] of Object.entries(value)) {
        const lowerKey = k.toLowerCase();
        const isSensitive = sensitiveKeys.some(sk => lowerKey.includes(sk));

        if (isSensitive) {
          sanitized[k] = '[REDACTED]';
        } else {
          sanitized[k] = this.sanitizeValue(v);
        }
      }

      return sanitized;
    }

    return value;
  }

  /**
   * Export as CSV
   */
  private exportCSV(): string {
    const headers = [
      'id',
      'type',
      'timestamp',
      'actor',
      'resource',
      'action',
      'result',
      'requestId'
    ];

    const rows = this.events.map(event => [
      event.id,
      event.type,
      event.timestamp.toISOString(),
      event.actor?.id || '',
      event.resource?.id || '',
      event.action,
      event.result,
      event.requestId || ''
    ]);

    const lines = [
      headers.join(','),
      ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
    ];

    return lines.join('\n');
  }

  /**
   * Default audit handler
   */
  private defaultHandler(event: AuditEvent): void {
    // Default handler logs to console
    if (this.options.format === 'json') {
      console.log('[AUDIT]', JSON.stringify(event));
    } else {
      console.log(
        `[AUDIT] ${event.timestamp.toISOString()} ${event.type} ${event.action} ${event.result}`
      );
    }
  }
}

/**
 * Create an audit logger instance
 */
export function createAuditLogger(options?: AuditLoggerOptions): AuditLogger {
  return new AuditLogger(options);
}
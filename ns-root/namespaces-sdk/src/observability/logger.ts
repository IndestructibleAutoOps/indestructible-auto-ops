// @GL-governed
// @GL-layer: GL-L6-NAMESPACE
// @GL-semantic: governance-layer-namespace
// @GL-revision: 1.0.0
// @GL-status: active

/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-sdk/src/observability
 * @gl-semantic-anchor GL-00-SRC_OBSERVAB_LOGGER
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * Structured Logger
 * 
 * Provides structured, configurable logging for all SDK operations.
 */

/**
 * Log level enumeration
 */
export enum LogLevel {
  DEBUG = 0,
  INFO = 1,
  WARN = 2,
  ERROR = 3,
  FATAL = 4
}

/**
 * Log entry
 */
export interface LogEntry {
  /** Log level */
  level: LogLevel;
  
  /** Log message */
  message: string;
  
  /** Timestamp */
  timestamp: Date;
  
  /** Additional context */
  context?: Record<string, any>;
  
  /** Error object if applicable */
  error?: Error;
  
  /** Correlation ID for tracing */
  correlationId?: string;
}

/**
 * Logger options
 */
export interface LoggerOptions {
  /** Minimum log level */
  level?: LogLevel;
  
  /** Enable debug logging */
  debug?: boolean;
  
  /** Enable logging */
  enabled?: boolean;
  
  /** Log output format */
  format?: 'json' | 'text';
  
  /** Include timestamps */
  includeTimestamp?: boolean;
  
  /** Include stack traces for errors */
  includeStackTrace?: boolean;
  
  /** Custom log handler */
  handler?: (entry: LogEntry) => void;
}

/**
 * Logger Class
 * 
 * Responsibilities:
 * - Provide structured logging with multiple levels
 * - Support context and correlation IDs
 * - Format logs for different outputs
 * - Integrate with external logging systems
 */
export class Logger {
  private options: Required<LoggerOptions>;
  private buffer: LogEntry[] = [];

  constructor(options: LoggerOptions = {}) {
    this.options = {
      name: options.name || 'default',
      level: options.debug ? LogLevel.DEBUG : LogLevel.INFO,
      debug: options.debug || false,
      enabled: options.enabled !== false,
      format: options.format || 'json',
      includeTimestamp: options.includeTimestamp !== false,
      includeStackTrace: options.includeStackTrace !== false,
      handler: options.handler || this.defaultHandler.bind(this)
    };
  }

  /**
   * Log a debug message
   */
  debug(message: string, context?: Record<string, any>): void {
    this.log(LogLevel.DEBUG, message, context);
  }

  /**
   * Log an info message
   */
  info(message: string, context?: Record<string, any>): void {
    this.log(LogLevel.INFO, message, context);
  }

  /**
   * Log a warning message
   */
  warn(message: string, context?: Record<string, any>): void {
    this.log(LogLevel.WARN, message, context);
  }

  /**
   * Log an error message
   */
  error(message: string, error?: Error | any, context?: Record<string, any>): void {
    const errorObj = error instanceof Error ? error : undefined;
    const errorContext = error && !(error instanceof Error) ? error : undefined;
    
    this.log(LogLevel.ERROR, message, {
      ...context,
      ...errorContext
    }, errorObj);
  }

  /**
   * Log a fatal error message
   */
  fatal(message: string, error?: Error | any, context?: Record<string, any>): void {
    const errorObj = error instanceof Error ? error : undefined;
    const errorContext = error && !(error instanceof Error) ? error : undefined;
    
    this.log(LogLevel.FATAL, message, {
      ...context,
      ...errorContext
    }, errorObj);
  }

  /**
   * Create a child logger with additional context
   */
  child(context: Record<string, any>): Logger {
    const childLogger = new Logger(this.options);
    childLogger.options.handler = (entry: LogEntry) => {
      this.log(entry.level, entry.message, {
        ...context,
        ...entry.context
      }, entry.error);
    };
    return childLogger;
  }

  /**
   * Set log level
   */
  setLevel(level: LogLevel): void {
    this.options.level = level;
  }

  /**
   * Get current log level
   */
  getLevel(): LogLevel {
    return this.options.level;
  }

  /**
   * Enable or disable logging
   */
  setEnabled(enabled: boolean): void {
    this.options.enabled = enabled;
  }

  /**
   * Check if logging is enabled
   */
  isEnabled(): boolean {
    return this.options.enabled;
  }

  /**
   * Flush buffered logs
   */
  async flush(): Promise<void> {
    // Flush any buffered logs
    this.buffer = [];
  }

  /**
   * Core logging method
   */
  private log(
    level: LogLevel,
    message: string,
    context?: Record<string, any>,
    error?: Error
  ): void {
    if (!this.options.enabled || level < this.options.level) {
      return;
    }

    const entry: LogEntry = {
      level,
      message,
      timestamp: new Date(),
      context,
      error
    };

    this.options.handler(entry);
  }

  /**
   * Default log handler
   */
  private defaultHandler(entry: LogEntry): void {
    const formatted = this.format(entry);
    
    switch (entry.level) {
      case LogLevel.DEBUG:
      case LogLevel.INFO:
        console.log(formatted);
        break;
      case LogLevel.WARN:
        console.warn(formatted);
        break;
      case LogLevel.ERROR:
      case LogLevel.FATAL:
        console.error(formatted);
        break;
    }
  }

  /**
   * Format log entry
   */
  private format(entry: LogEntry): string {
    if (this.options.format === 'json') {
      return this.formatJSON(entry);
    } else {
      return this.formatText(entry);
    }
  }

  /**
   * Format as JSON
   */
  private formatJSON(entry: LogEntry): string {
    const obj: Record<string, unknown> = {
      level: LogLevel[entry.level],
      message: entry.message
    };

    if (this.options.includeTimestamp) {
      obj.timestamp = entry.timestamp.toISOString();
    }

    if (entry.context) {
      obj.context = entry.context;
    }

    if (entry.error) {
      obj.error = {
        name: entry.error.name,
        message: entry.error.message
      };

      if (this.options.includeStackTrace && entry.error.stack) {
        obj.error.stack = entry.error.stack;
      }
    }

    if (entry.correlationId) {
      obj.correlationId = entry.correlationId;
    }

    return JSON.stringify(obj);
  }

  /**
   * Format as text
   */
  private formatText(entry: LogEntry): string {
    const parts: string[] = [];

    if (this.options.includeTimestamp) {
      parts.push(`[${entry.timestamp.toISOString()}]`);
    }

    parts.push(`[${LogLevel[entry.level]}]`);
    parts.push(entry.message);

    if (entry.context && Object.keys(entry.context).length > 0) {
      parts.push(JSON.stringify(entry.context));
    }

    if (entry.error) {
      parts.push(`Error: ${entry.error.message}`);
      
      if (this.options.includeStackTrace && entry.error.stack) {
        parts.push(`\n${entry.error.stack}`);
      }
    }

    return parts.join(' ');
  }
}

/**
 * Create a logger instance
 */
export function createLogger(options?: LoggerOptions): Logger {
  return new Logger(options);
}
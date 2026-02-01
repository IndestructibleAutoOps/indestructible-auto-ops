// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: logger-utility
// @GL-charter-version: 2.0.0

import winston from 'winston';
import path from 'path';

export function createLogger(context: string): winston.Logger {
  const logFormat = winston.format.combine(
    winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
    winston.format.errors({ stack: true }),
    winston.format.splat(),
    winston.format.json()
  );

  const consoleFormat = winston.format.combine(
    winston.format.colorize(),
    winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
    winston.format.printf(({ timestamp, level, message, context: ctx, ...metadata }) => {
      let msg = `${timestamp} [${level}] [${ctx}] ${message}`;
      if (Object.keys(metadata).length > 0) {
        msg += ` ${JSON.stringify(metadata)}`;
      }
      return msg;
    })
  );

  const transports: winston.transport[] = [
    new winston.transports.Console({
      format: consoleFormat
    })
  ];

  // Add file transport if logs directory exists
  try {
    const logsPath = path.join(process.cwd(), 'storage', 'logs');
    require('fs').mkdirSync(logsPath, { recursive: true });
    
    transports.push(
      new winston.transports.File({
        filename: path.join(logsPath, 'combined.log'),
        format: logFormat
      }),
      new winston.transports.File({
        filename: path.join(logsPath, 'error.log'),
        level: 'error',
        format: logFormat
      })
    );
  } catch (error) {
    // Ignore error if we can't create log directory
  }

  return winston.createLogger({
    level: process.env.LOG_LEVEL || 'info',
    format: logFormat,
    defaultMeta: { context },
    transports
  });
}
/**
 * @module events_writer
 * @description Governance event stream writer
 * @gl-governed
 * GL Unified Charter Activated
 * @gl-layer GL-10-OPERATIONAL
 * @gl-module engine/governance
 * @gl-semantic-anchor GL-10-GOV-TS
 * @gl-evidence-required true
 * @version 1.0.0
 * @since 2026-01-24
 * @author MachineNativeOps Team
 */

import * as fs from 'fs';
import * as path from 'path';
import { GLEvent, EvidenceRecord } from '../interfaces.d';

/**
 * Events Writer
 * 
 * GL00-99: Unified Governance Framework
 * 
 * Writes governance events to stream for audit trail
 * and compliance requirements.
 */
export class EventsWriter {
  private evidence: EvidenceRecord[] = [];
  private readonly eventStream: GLEvent[] = [];
  private readonly outputPath?: string;
  private readonly enabled: boolean;

  constructor(options?: {
    outputPath?: string;
    enabled?: boolean;
  }) {
    this.outputPath = options?.outputPath;
    this.enabled = options?.enabled ?? true;
  }

  /**
   * Write events to stream
   */
  async write(events: GLEvent[]): Promise<void> {
    const startTime = Date.now();

    try {
      if (!this.enabled) {
        return;
      }

      // Add events to stream
      this.eventStream.push(...events);

      // Write to file if output path is specified
      if (this.outputPath) {
        await this.writeToFile();
      }

      // Generate evidence record
      this.evidence.push({
        timestamp: new Date().toISOString(),
        stage: 'governance',
        component: 'events_writer',
        action: 'write',
        status: 'success',
        input: { eventCount: events.length },
        output: {
          totalEvents: this.eventStream.length,
          written: !!this.outputPath
        },
        metrics: { duration: Date.now() - startTime }
      });
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);

      this.evidence.push({
        timestamp: new Date().toISOString(),
        stage: 'governance',
        component: 'events_writer',
        action: 'write',
        status: 'error',
        input: { eventCount: events.length },
        output: { error: errorMsg },
        metrics: { duration: Date.now() - startTime }
      });

      throw error;
    }
  }

  /**
   * Write events to file
   */
  private async writeToFile(): Promise<void> {
    if (!this.outputPath) {
      return;
    }

    // Ensure output directory exists
    const dir = path.dirname(this.outputPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    // Write events as JSON Lines
    const lines = this.eventStream.map(event => JSON.stringify(event));
    fs.writeFileSync(this.outputPath, lines.join('\n') + '\n', 'utf-8');
  }

  /**
   * Get event stream
   */
  getEvents(): GLEvent[] {
    return [...this.eventStream];
  }

  /**
   * Get events by type
   */
  getEventsByType(type: string): GLEvent[] {
    return this.eventStream.filter(event => event.type === type);
  }

  /**
   * Get events by stage
   */
  getEventsByStage(stage: string): GLEvent[] {
    return this.eventStream.filter(event => event.stage === stage);
  }

  /**
   * Get events by component
   */
  getEventsByComponent(component: string): GLEvent[] {
    return this.eventStream.filter(event => event.component === component);
  }

  /**
   * Get events by time range
   */
  getEventsByTimeRange(start: Date, end: Date): GLEvent[] {
    const startTime = start.getTime();
    const endTime = end.getTime();

    return this.eventStream.filter(event => {
      const eventTime = new Date(event.timestamp).getTime();
      return eventTime >= startTime && eventTime <= endTime;
    });
  }

  /**
   * Get event statistics
   */
  getStatistics(): {
    total: number;
    byType: Map<string, number>;
    byStage: Map<string, number>;
    byComponent: Map<string, number>;
  } {
    const byType = new Map<string, number>();
    const byStage = new Map<string, number>();
    const byComponent = new Map<string, number>();

    for (const event of this.eventStream) {
      byType.set(event.type, (byType.get(event.type) || 0) + 1);
      byStage.set(event.stage, (byStage.get(event.stage) || 0) + 1);
      byComponent.set(event.component, (byComponent.get(event.component) || 0) + 1);
    }

    return {
      total: this.eventStream.length,
      byType,
      byStage,
      byComponent
    };
  }

  /**
   * Clear event stream
   */
  clear(): void {
    this.eventStream.length = 0;
  }

  /**
   * Export events as JSON
   */
  exportJson(): string {
    return JSON.stringify(this.eventStream, null, 2);
  }

  /**
   * Export events as NDJSON
   */
  exportNdjson(): string {
    return this.eventStream.map(event => JSON.stringify(event)).join('\n');
  }

  /**
   * Get evidence records
   */
  getEvidence(): EvidenceRecord[] {
    return this.evidence;
  }
}
// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: event-stream-manager
// @GL-charter-version: 2.0.0

import fs from 'fs/promises';
import path from 'path';
import { createLogger } from '../utils/logger';

const logger = createLogger('EventStreamManager');

export interface GovernanceEvent {
  eventType: string;
  layer: string;
  semanticAnchor: string;
  timestamp: string;
  metadata: any;
}

export class EventStreamManager {
  private eventStreamPath: string;
  private events: GovernanceEvent[] = [];

  constructor() {
    this.eventStreamPath = path.join(process.cwd(), 'storage', 'gl-events-stream', 'events.jsonl');
  }

  public async logEvent(event: GovernanceEvent): Promise<void> {
    this.events.push(event);
    await this.persistEvent(event);
    logger.info(`Event logged: ${event.eventType}`);
  }

  private async persistEvent(event: GovernanceEvent): Promise<void> {
    try {
      const dir = path.dirname(this.eventStreamPath);
      await fs.mkdir(dir, { recursive: true });
      
      const eventLine = JSON.stringify(event) + '\n';
      await fs.appendFile(this.eventStreamPath, eventLine);
    } catch (error: any) {
      logger.error(`Failed to persist event: ${error.message}`);
      throw error;
    }
  }

  public async loadEvents(): Promise<GovernanceEvent[]> {
    try {
      const content = await fs.readFile(this.eventStreamPath, 'utf-8');
      const lines = content.trim().split('\n');
      this.events = lines.map(line => JSON.parse(line));
      return this.events;
    } catch (error: any) {
      if (error.code === 'ENOENT') {
        return [];
      }
      throw error;
    }
  }

  public async getEventsByType(eventType: string): Promise<GovernanceEvent[]> {
    const allEvents = await this.loadEvents();
    return allEvents.filter(event => event.eventType === eventType);
  }

  public async getEventsByLayer(layer: string): Promise<GovernanceEvent[]> {
    const allEvents = await this.loadEvents();
    return allEvents.filter(event => event.layer === layer);
  }

  public async getEventsByTimeRange(startTime: string, endTime: string): Promise<GovernanceEvent[]> {
    const allEvents = await this.loadEvents();
    return allEvents.filter(event => 
      event.timestamp >= startTime && event.timestamp <= endTime
    );
  }

  public getEventCount(): number {
    return this.events.length;
  }

  public clearEvents(): void {
    this.events = [];
  }
}
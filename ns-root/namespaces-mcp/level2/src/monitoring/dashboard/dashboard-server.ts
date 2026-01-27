/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-mcp/level2/src/monitoring/dashboard
 * @gl-semantic-anchor GL-00-MONITORI_DASHBOAR_DASHBOARDSER
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * Dashboard Server - Real-Time Monitoring Dashboard
 * 
 * @version 1.0.0
 */

import { EventEmitter } from 'events';

export interface DashboardConfig {
  port?: number;
  refreshInterval?: number;
  enableAuth?: boolean;
}

export class DashboardServer extends EventEmitter {
  private config: Required<DashboardConfig>;
  private clients: Set<any>;
  private running: boolean;
  
  constructor(config?: DashboardConfig) {
    super();
    
    this.config = {
      port: config?.port || 3000,
      refreshInterval: config?.refreshInterval || 5000,
      enableAuth: config?.enableAuth || false
    };
    
    this.clients = new Set();
    this.running = false;
  }
  
  async start(): Promise<void> {
    if (this.running) return;
    
    this.running = true;
    this.emit('server:started', { port: this.config.port });
  }
  
  async stop(): Promise<void> {
    if (!this.running) return;
    
    this.running = false;
    this.clients.clear();
    this.emit('server:stopped');
  }
  
  broadcast(data: Record<string, unknown>): void {
    for (const client of this.clients) {
      this.sendToClient(client, data);
    }
  }
  
  private sendToClient(client: unknown, data: Record<string, unknown>): void {
    this.emit('data:sent', { client, data });
  }
  
  isRunning(): boolean {
    return this.running;
  }
}

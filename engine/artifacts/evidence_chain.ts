/**
 * @module evidence_chain
 * @description Evidence chain generation for audit trail
 * @gl-governed
 * GL Unified Charter Activated
 * @gl-layer GL-30-EXECUTION
 * @gl-module engine/artifacts
 * @gl-semantic-anchor GL-30-EXEC-TS
 * @gl-evidence-required true
 * @version 1.0.0
 * @since 2026-01-24
 * @author MachineNativeOps Team
 */

import * as fs from 'fs';
import * as path from 'path';
import * as crypto from 'crypto';
import { EvidenceRecord } from '../interfaces.d';

/**
 * Evidence Chain Generator
 * 
 * GL90-99: Meta Layer - Evidence Chain Management
 * 
 * Generates complete evidence chains for all operations,
 * ensuring full auditability and compliance.
 */
export class EvidenceChain {
  private evidence: EvidenceRecord[] = [];
  private readonly outputDir: string;
  private readonly chain: Map<string, EvidenceRecord[]> = new Map();

  constructor(options?: {
    outputDir?: string;
  }) {
    this.outputDir = options?.outputDir || './artifacts/evidence';
    this.ensureDirectoryExists(this.outputDir);
  }

  /**
   * Add evidence record
   */
  add(record: EvidenceRecord): void {
    this.evidence.push(record);

    // Add to chain
    const stage = record.stage;
    if (!this.chain.has(stage)) {
      this.chain.set(stage, []);
    }
    this.chain.get(stage)!.push(record);
  }

  /**
   * Add multiple evidence records
   */
  addBatch(records: EvidenceRecord[]): void {
    for (const record of records) {
      this.add(record);
    }
  }

  /**
   * Generate complete evidence chain
   */
  generate(): {
    chainId: string;
    timestamp: string;
    evidence: EvidenceRecord[];
    byStage: Map<string, EvidenceRecord[]>;
    hash: string;
  } {
    const chainId = this.generateChainId();
    const timestamp = new Date().toISOString();

    // Generate hash of all evidence
    const hash = this.generateHash(this.evidence);

    return {
      chainId,
      timestamp,
      evidence: [...this.evidence],
      byStage: new Map(this.chain),
      hash
    };
  }

  /**
   * Save evidence chain to file
   */
  async save(chainId?: string): Promise<string> {
    const id = chainId || this.generateChainId();
    const chain = this.generate();
    const filePath = path.join(this.outputDir, `${id}.json`);

    const chainData = {
      ...chain,
      chainId: id,
      savedAt: new Date().toISOString()
    };

    fs.writeFileSync(filePath, JSON.stringify(chainData, null, 2), 'utf-8');

    return filePath;
  }

  /**
   * Get evidence by stage
   */
  getEvidenceByStage(stage: string): EvidenceRecord[] {
    return this.chain.get(stage) || [];
  }

  /**
   * Get evidence by component
   */
  getEvidenceByComponent(component: string): EvidenceRecord[] {
    return this.evidence.filter(record => record.component === component);
  }

  /**
   * Get evidence by action
   */
  getEvidenceByAction(action: string): EvidenceRecord[] {
    return this.evidence.filter(record => record.action === action);
  }

  /**
   * Get evidence by time range
   */
  getEvidenceByTimeRange(start: Date, end: Date): EvidenceRecord[] {
    const startTime = start.getTime();
    const endTime = end.getTime();

    return this.evidence.filter(record => {
      const recordTime = new Date(record.timestamp).getTime();
      return recordTime >= startTime && recordTime <= endTime;
    });
  }

  /**
   * Generate evidence summary
   */
  generateSummary(): {
    totalRecords: number;
    byStage: Map<string, number>;
    byComponent: Map<string, number>;
    byAction: Map<string, number>;
    byStatus: Map<string, number>;
    timeRange: {
      earliest: string | null;
      latest: string | null;
    };
  } {
    const byStage = new Map<string, number>();
    const byComponent = new Map<string, number>();
    const byAction = new Map<string, number>();
    const byStatus = new Map<string, number>();

    let earliest: string | null = null;
    let latest: string | null = null;

    for (const record of this.evidence) {
      // Count by stage
      byStage.set(record.stage, (byStage.get(record.stage) || 0) + 1);

      // Count by component
      byComponent.set(record.component, (byComponent.get(record.component) || 0) + 1);

      // Count by action
      byAction.set(record.action, (byAction.get(record.action) || 0) + 1);

      // Count by status
      byStatus.set(record.status, (byStatus.get(record.status) || 0) + 1);

      // Track time range
      if (!earliest || record.timestamp < earliest) {
        earliest = record.timestamp;
      }
      if (!latest || record.timestamp > latest) {
        latest = record.timestamp;
      }
    }

    return {
      totalRecords: this.evidence.length,
      byStage,
      byComponent,
      byAction,
      byStatus,
      timeRange: { earliest, latest }
    };
  }

  /**
   * Generate evidence report
   */
  generateReport(): string {
    const summary = this.generateSummary();
    const lines: string[] = [];

    lines.push('═'.repeat(80));
    lines.push('EVIDENCE CHAIN REPORT');
    lines.push('═'.repeat(80));
    lines.push('');
    lines.push(`Total Records: ${summary.totalRecords}`);
    lines.push(`Time Range: ${summary.timeRange.earliest} to ${summary.timeRange.latest}`);
    lines.push('');
    lines.push('─'.repeat(80));
    lines.push('By Stage:');
    lines.push('─'.repeat(80));

    for (const [stage, count] of summary.byStage.entries()) {
      lines.push(`  ${stage}: ${count} records`);
    }

    lines.push('');
    lines.push('─'.repeat(80));
    lines.push('By Status:');
    lines.push('─'.repeat(80));

    for (const [status, count] of summary.byStatus.entries()) {
      lines.push(`  ${status}: ${count} records`);
    }

    lines.push('');
    lines.push('─'.repeat(80));
    lines.push('Evidence Records:');
    lines.push('─'.repeat(80));

    for (const record of this.evidence) {
      const icon = record.status === 'success' ? '✅' : (record.status === 'error' ? '❌' : '⚠️');
      lines.push(`${icon} [${record.timestamp}] ${record.stage}/${record.component}/${record.action}`);
    }

    lines.push('');
    lines.push('═'.repeat(80));

    return lines.join('\n');
  }

  /**
   * Validate evidence chain integrity
   */
  validateIntegrity(expectedHash: string): {
    valid: boolean;
    actualHash: string;
  } {
    const actualHash = this.generateHash(this.evidence);

    return {
      valid: actualHash === expectedHash,
      actualHash
    };
  }

  /**
   * Generate chain ID
   */
  private generateChainId(): string {
    return `evidence_${Date.now()}_${crypto.randomBytes(8).toString('hex')}`;
  }

  /**
   * Generate hash
   */
  private generateHash(data: EvidenceRecord[]): string {
    return crypto.createHash('sha256').update(JSON.stringify(data)).digest('hex');
  }

  /**
   * Ensure directory exists
   */
  private ensureDirectoryExists(dirPath: string): void {
    if (!fs.existsSync(dirPath)) {
      fs.mkdirSync(dirPath, { recursive: true });
    }
  }

  /**
   * Get all evidence
   */
  getEvidence(): EvidenceRecord[] {
    return [...this.evidence];
  }

  /**
   * Clear evidence
   */
  clear(): void {
    this.evidence = [];
    this.chain.clear();
  }
}
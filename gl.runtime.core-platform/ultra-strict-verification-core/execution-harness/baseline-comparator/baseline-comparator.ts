# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: execution-harness-baseline-comparator
# @GL-charter-version: 2.0.0

/**
 * Execution-Grounded Reality Harness: Baseline Comparator
 * 
 * Core Philosophy: "所有報告 → 必須對照 baseline"
 * (All reports must be compared against baseline)
 * 
 * Purpose: Compare current behavior against established baselines
 * 
 * This module enforces:
 * - All metrics must be compared against baseline
 * - All behaviors must be compared against baseline
 * - All outputs must be compared against baseline
 * - All performance must be compared against baseline
 * - Any deviation must be justified
 */

import { 
  BaselineComparisonResult,
  VerificationSeverity,
  VerificationFinding 
} from '../../types';

export class BaselineComparator {
  private findings: VerificationFinding[] = [];
  private baselines: Map<string, any> = new Map();

  /**
   * Compare metrics against baseline
   */
  async compareBaseline(component: string, metrics: any): Promise<BaselineComparisonResult> {
    this.findings = [];
    
    // Load baseline for component
    const baseline = await this.loadBaseline(component);
    
    if (!baseline) {
      // No baseline exists - this is a finding
      this.findings.push({
        id: this.generateId(),
        type: 'INCONSISTENCY',
        severity: VerificationSeverity.MEDIUM,
        component,
        location: {
          module: component
        },
        title: 'No Baseline Found',
        description: `No baseline exists for component '${component}' - cannot compare metrics`,
        evidence: [{
          type: 'baseline',
          source: component,
          content: { metrics, baseline: null },
          timestamp: new Date(),
          verified: false
        }],
        timestamp: new Date(),
        verified: false,
        falsifiable: true
      });
      
      return {
        baselineMatched: false,
        differences: [{
          metric: 'baseline',
          baseline: null,
          current: metrics,
          delta: 'No baseline to compare',
          severity: VerificationSeverity.MEDIUM
        }]
      };
    }
    
    // Compare metrics against baseline
    await this.compareMetrics(component, baseline, metrics);
    
    return {
      baselineMatched: this.findings.length === 0,
      differences: this.extractDifferences()
    };
  }

  /**
   * Load baseline for component
   */
  private async loadBaseline(component: string): Promise<any | null> {
    // Check if baseline is already loaded
    if (this.baselines.has(component)) {
      return this.baselines.get(component);
    }
    
    // Try to load from file
    const baselinePath = this.getBaselinePath(component);
    
    try {
      const fs = require('fs').promises;
      const content = await fs.readFile(baselinePath, 'utf-8');
      const baseline = JSON.parse(content);
      
      this.baselines.set(component, baseline);
      return baseline;
    } catch (error) {
      return null;
    }
  }

  /**
   * Compare metrics against baseline
   */
  private async compareMetrics(component: string, baseline: any, metrics: any): Promise<void> {
    // Compare each metric
    for (const [key, baselineValue] of Object.entries(baseline)) {
      const currentValue = metrics[key];
      
      if (currentValue === undefined) {
        // Metric missing in current
        this.findings.push({
          id: this.generateId(),
          type: 'INCONSISTENCY',
          severity: VerificationSeverity.MEDIUM,
          component,
          location: {
            module: component
          },
          title: 'Metric Missing',
          description: `Metric '${key}' exists in baseline but missing in current`,
          evidence: [{
            type: 'baseline',
            source: component,
            content: { key, baseline: baselineValue, current: undefined },
            timestamp: new Date(),
            verified: false
          }],
          timestamp: new Date(),
          verified: false,
          falsifiable: true
        });
        
        continue;
      }
      
      // Compare values
      const difference = this.calculateDifference(baselineValue, currentValue);
      
      if (difference !== null && this.isSignificantDifference(baselineValue, currentValue, difference)) {
        this.findings.push({
          id: this.generateId(),
          type: 'PERFORMANCE_DEGRADATION',
          severity: this.getDifferenceSeverity(baselineValue, currentValue, difference),
          component,
          location: {
            module: component
          },
          title: 'Baseline Difference Detected',
          description: `Metric '${key}' differs from baseline: ${baselineValue} → ${currentValue} (delta: ${difference})`,
          evidence: [{
            type: 'baseline',
            source: component,
            content: { key, baseline: baselineValue, current: currentValue, delta: difference },
            timestamp: new Date(),
            verified: false
          }],
          timestamp: new Date(),
          verified: false,
          falsifiable: true
        });
      }
    }
    
    // Check for new metrics
    for (const [key, currentValue] of Object.entries(metrics)) {
      if (!(key in baseline)) {
        this.findings.push({
          id: this.generateId(),
          type: 'INCONSISTENCY',
          severity: VerificationSeverity.LOW,
          component,
          location: {
            module: component
          },
          title: 'New Metric Detected',
          description: `Metric '${key}' exists in current but missing from baseline`,
          evidence: [{
            type: 'baseline',
            source: component,
            content: { key, baseline: undefined, current: currentValue },
            timestamp: new Date(),
            verified: false
          }],
          timestamp: new Date(),
          verified: false,
          falsifiable: true
        });
      }
    }
  }

  /**
   * Calculate difference between baseline and current values
   */
  private calculateDifference(baseline: any, current: any): string | null {
    if (typeof baseline === 'number' && typeof current === 'number') {
      if (baseline === 0) {
        return current === 0 ? '0' : `${current}`;
      }
      const percentDiff = ((current - baseline) / Math.abs(baseline)) * 100;
      return `${current - baseline} (${percentDiff.toFixed(2)}%)`;
    }
    
    if (baseline === current) {
      return null;
    }
    
    return `${JSON.stringify(current)} (baseline: ${JSON.stringify(baseline)})`;
  }

  /**
   * Check if difference is significant
   */
  private isSignificantDifference(baseline: any, current: any, difference: string): boolean {
    if (typeof baseline === 'number' && typeof current === 'number') {
      // More than 5% difference is significant
      if (baseline === 0) {
        return current !== 0;
      }
      const percentDiff = Math.abs((current - baseline) / baseline) * 100;
      return percentDiff > 5;
    }
    
    return baseline !== current;
  }

  /**
   * Get severity based on difference
   */
  private getDifferenceSeverity(baseline: any, current: any, difference: string): VerificationSeverity {
    if (typeof baseline === 'number' && typeof current === 'number') {
      if (baseline === 0) {
        return current === 0 ? VerificationSeverity.LOW : VerificationSeverity.HIGH;
      }
      
      const percentDiff = Math.abs((current - baseline) / baseline) * 100;
      
      if (percentDiff > 50) {
        return VerificationSeverity.CRITICAL;
      } else if (percentDiff > 20) {
        return VerificationSeverity.HIGH;
      } else if (percentDiff > 10) {
        return VerificationSeverity.MEDIUM;
      }
      return VerificationSeverity.LOW;
    }
    
    return VerificationSeverity.MEDIUM;
  }

  /**
   * Extract differences from findings
   */
  private extractDifferences() {
    return this.findings.map(finding => ({
      metric: finding.title,
      baseline: finding.evidence[0]?.content?.baseline,
      current: finding.evidence[0]?.content?.current,
      delta: finding.evidence[0]?.content?.delta,
      severity: finding.severity
    }));
  }

  /**
   * Set baseline for component
   */
  setBaseline(component: string, baseline: any): void {
    this.baselines.set(component, baseline);
  }

  /**
   * Save baseline to file
   */
  async saveBaseline(component: string, baseline: any): Promise<void> {
    const baselinePath = this.getBaselinePath(component);
    const fs = require('fs').promises;
    
    await fs.writeFile(baselinePath, JSON.stringify(baseline, null, 2), 'utf-8');
    this.baselines.set(component, baseline);
  }

  /**
   * Get baseline path for component
   */
  private getBaselinePath(component: string): string {
    return `/workspace/gl-runtime-platform/.baselines/${component}.json`;
  }

  /**
   * Get findings
   */
  getFindings(): VerificationFinding[] {
    return this.findings;
  }

  /**
   * Clear findings
   */
  clearFindings(): void {
    this.findings = [];
  }

  // ============================================================================
  // Helper Methods
  // ============================================================================

  private generateId(): string {
    return `baseline-comparator-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
}
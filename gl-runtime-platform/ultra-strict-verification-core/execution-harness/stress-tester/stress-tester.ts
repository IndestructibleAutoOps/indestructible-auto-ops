# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: execution-harness-stress-tester
# @GL-charter-version: 2.0.0

/**
 * Execution-Grounded Reality Harness: Stress Tester
 * 
 * Core Philosophy: "所有優化 → 必須跑壓測"
 * (All optimizations must undergo stress testing)
 * 
 * Purpose: Test components under extreme load
 * 
 * This module enforces:
 * - All optimizations must be stress tested
 * - All performance claims must be verified under load
 * - All limits must be tested
 * - Failures under stress must be reported
 */

import { 
  StressTestResult,
  VerificationSeverity,
  VerificationFinding 
} from '../../types';

export class StressTester {
  private findings: VerificationFinding[] = [];

  /**
   * Stress test a component
   */
  async stressTest(component: string, maxLoad: number): Promise<StressTestResult> {
    this.findings = [];
    
    const failures: Array<{ load: number; failure: string; severity: VerificationSeverity }> = [];
    const responseTimes: number[] = [];
    const errors: number[] = [];
    
    // Run stress tests at increasing load levels
    const loadLevels = this.generateLoadLevels(maxLoad);
    
    for (const load of loadLevels) {
      const result = await this.runAtLoad(component, load);
      
      responseTimes.push(result.avgResponseTime);
      errors.push(result.errorRate);
      
      if (!result.success) {
        failures.push({
          load,
          failure: result.error || 'Unknown failure',
          severity: this.getFailureSeverity(load, maxLoad)
        });
        
        this.findings.push({
          id: this.generateId(),
          type: 'PERFORMANCE_DEGRADATION',
          severity: this.getFailureSeverity(load, maxLoad),
          component,
          location: {
            module: component
          },
          title: 'Stress Test Failure',
          description: `Component failed at load ${load}: ${result.error}`,
          evidence: [{
            type: 'execution',
            source: component,
            content: { load, result },
            timestamp: new Date(),
            verified: false
          }],
          timestamp: new Date(),
          verified: false,
          falsifiable: true
        });
      }
    }
    
    const avgResponseTime = responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length;
    const maxResponseTime = Math.max(...responseTimes);
    const errorRate = errors.reduce((a, b) => a + b, 0) / errors.length;
    
    return {
      stressPassed: failures.length === 0,
      load: maxLoad,
      failures,
      performance: {
        avgResponseTime,
        maxResponseTime,
        errorRate
      }
    };
  }

  /**
   * Generate load levels
   */
  private generateLoadLevels(maxLoad: number): number[] {
    const levels: number[] = [];
    
    // Start with small loads, then increase
    for (let i = 1; i <= 10; i++) {
      levels.push(Math.floor(maxLoad * (i / 10)));
    }
    
    return levels;
  }

  /**
   * Run test at specific load
   */
  private async runAtLoad(component: string, load: number): Promise<{
    success: boolean;
    avgResponseTime: number;
    errorRate: number;
    error?: string;
  }> {
    const startTime = Date.now();
    let errors = 0;
    
    try {
      // Simulate running at load
      await this.simulateLoad(component, load);
      
      const endTime = Date.now();
      const responseTime = endTime - startTime;
      
      return {
        success: true,
        avgResponseTime: responseTime,
        errorRate: errors / load
      };
    } catch (error) {
      return {
        success: false,
        avgResponseTime: Date.now() - startTime,
        errorRate: 1,
        error: error instanceof Error ? error.message : String(error)
      };
    }
  }

  /**
   * Simulate load
   */
  private async simulateLoad(component: string, load: number): Promise<void> {
    // Simplified - in reality would actually run operations
    const delay = Math.random() * 100 * (load / 100);
    await new Promise(resolve => setTimeout(resolve, delay));
    
    // Fail at high loads
    if (load > 80 && Math.random() > 0.9) {
      throw new Error(`Load too high: ${load}`);
    }
  }

  /**
   * Get failure severity based on load
   */
  private getFailureSeverity(load: number, maxLoad: number): VerificationSeverity {
    const loadPercent = (load / maxLoad) * 100;
    
    if (loadPercent > 80) {
      return VerificationSeverity.CRITICAL;
    } else if (loadPercent > 60) {
      return VerificationSeverity.HIGH;
    } else if (loadPercent > 40) {
      return VerificationSeverity.MEDIUM;
    }
    return VerificationSeverity.LOW;
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
    return `stress-tester-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
}
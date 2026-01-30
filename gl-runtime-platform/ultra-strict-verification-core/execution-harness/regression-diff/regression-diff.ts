# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: execution-harness-regression-diff
# @GL-charter-version: 2.0.0

/**
 * Execution-Grounded Reality Harness: Regression Diff
 * 
 * Core Philosophy: "所有重構 → 必須跑差分測試"
 * (All refactoring must undergo diff testing)
 * 
 * Purpose: Detect regressions between versions
 * 
 * This module enforces:
 * - All changes must be diff tested
 * - All regressions must be reported
 * - All behavior changes must be justified
 * - Performance regressions must be detected
 */

import { 
  RegressionDiffResult,
  VerificationSeverity,
  VerificationFinding 
} from '../../types';

export class RegressionDiff {
  private findings: VerificationFinding[] = [];
  private previousVersions: Map<string, any> = new Map();

  /**
   * Detect regressions between current and previous version
   */
  async detectRegression(component: string, previousVersion: string): Promise<RegressionDiffResult> {
    this.findings = [];
    
    // Load previous version
    const previousData = await this.loadPreviousVersion(component, previousVersion);
    
    if (!previousData) {
      this.findings.push({
        id: this.generateId(),
        type: 'INCONSISTENCY',
        severity: VerificationSeverity.MEDIUM,
        component,
        location: {
          module: component
        },
        title: 'Previous Version Not Found',
        description: `Previous version '${previousVersion}' not found - cannot detect regressions`,
        evidence: [{
          type: 'baseline',
          source: component,
          content: { previousVersion, status: 'not found' },
          timestamp: new Date(),
          verified: false
        }],
        timestamp: new Date(),
        verified: false,
        falsifiable: true
      });
      
      return {
        regressionDetected: false,
        regressions: []
      };
    }
    
    // Compare current version with previous
    await this.compareVersions(component, previousData);
    
    return {
      regressionDetected: this.findings.length > 0,
      regressions: this.extractRegressions()
    };
  }

  /**
   * Load previous version
   */
  private async loadPreviousVersion(component: string, version: string): Promise<any | null> {
    const key = `${component}:${version}`;
    
    // Check if already loaded
    if (this.previousVersions.has(key)) {
      return this.previousVersions.get(key);
    }
    
    // Try to load from file
    const versionPath = this.getVersionPath(component, version);
    
    try {
      const fs = require('fs').promises;
      const content = await fs.readFile(versionPath, 'utf-8');
      const data = JSON.parse(content);
      
      this.previousVersions.set(key, data);
      return data;
    } catch (error) {
      return null;
    }
  }

  /**
   * Compare current version with previous
   */
  private async compareVersions(component: string, previousData: any): Promise<void> {
    const componentPath = this.getComponentPath(component);
    
    // Get current version data
    const currentData = await this.getCurrentVersionData(component, componentPath);
    
    // Compare functions
    if (previousData.functions && currentData.functions) {
      await this.compareFunctions(component, previousData.functions, currentData.functions);
    }
    
    // Compare classes
    if (previousData.classes && currentData.classes) {
      await this.compareClasses(component, previousData.classes, currentData.classes);
    }
    
    // Compare metrics
    if (previousData.metrics && currentData.metrics) {
      await this.compareMetrics(component, previousData.metrics, currentData.metrics);
    }
  }

  /**
   * Get current version data
   */
  private async getCurrentVersionData(component: string, componentPath: string): Promise<any> {
    const files = await this.getTsFiles(componentPath);
    
    const data: any = {
      functions: {},
      classes: {},
      metrics: {}
    };
    
    for (const file of files) {
      const content = await this.readFileContent(file);
      
      // Extract functions
      const functionMatches = content.matchAll(
        /(?:function|const\s+\w+\s*=\s*|(?:async\s+)?\w+)\s*(\w+)\s*\(([^)]*)\)/g
      );
      
      for (const match of functionMatches) {
        const functionName = match[1];
        const params = match[2];
        
        if (!data.functions[functionName]) {
          data.functions[functionName] = {
            file,
            params: params.split(',').map(p => p.trim()),
            count: 0
          };
        }
        data.functions[functionName].count++;
      }
      
      // Extract classes
      const classMatches = content.matchAll(/class\s+(\w+)/g);
      for (const match of classMatches) {
        const className = match[1];
        
        if (!data.classes[className]) {
          data.classes[className] = {
            file,
            methods: []
          };
        }
      }
    }
    
    return data;
  }

  /**
   * Compare functions
   */
  private async compareFunctions(
    component: string,
    previous: any,
    current: any
  ): Promise<void> {
    // Check for removed functions
    for (const functionName of Object.keys(previous)) {
      if (!current[functionName]) {
        this.findings.push({
          id: this.generateId(),
          type: 'REGRESSION',
          severity: VerificationSeverity.HIGH,
          component,
          location: {
            module: component
          },
          title: 'Function Removed',
          description: `Function '${functionName}' was removed - this may break compatibility`,
          evidence: [{
            type: 'baseline',
            source: 'previous version',
            content: previous[functionName],
            timestamp: new Date(),
            verified: false
          }],
          timestamp: new Date(),
          verified: false,
          falsifiable: true
        });
      }
    }
    
    // Check for changed function signatures
    for (const functionName of Object.keys(current)) {
      if (previous[functionName]) {
        const prevFunc = previous[functionName];
        const currFunc = current[functionName];
        
        if (prevFunc.params.join(',') !== currFunc.params.join(',')) {
          this.findings.push({
            id: this.generateId(),
            type: 'REGRESSION',
            severity: VerificationSeverity.HIGH,
            component,
            location: {
              file: currFunc.file,
              module: component
            },
            title: 'Function Signature Changed',
            description: `Function '${functionName}' signature changed from (${prevFunc.params.join(',')}) to (${currFunc.params.join(',')})`,
            evidence: [
              {
                type: 'baseline',
                source: 'previous version',
                content: prevFunc,
                timestamp: new Date(),
                verified: false
              },
              {
                type: 'code',
                source: 'current version',
                content: currFunc,
                timestamp: new Date(),
                verified: true
              }
            ],
            timestamp: new Date(),
            verified: false,
            falsifiable: true
          });
        }
      }
    }
  }

  /**
   * Compare classes
   */
  private async compareClasses(
    component: string,
    previous: any,
    current: any
  ): Promise<void> {
    // Check for removed classes
    for (const className of Object.keys(previous)) {
      if (!current[className]) {
        this.findings.push({
          id: this.generateId(),
          type: 'REGRESSION',
          severity: VerificationSeverity.HIGH,
          component,
          location: {
            module: component
          },
          title: 'Class Removed',
          description: `Class '${className}' was removed - this may break compatibility`,
          evidence: [{
            type: 'baseline',
            source: 'previous version',
            content: previous[className],
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
   * Compare metrics
   */
  private async compareMetrics(
    component: string,
    previous: any,
    current: any
  ): Promise<void> {
    for (const metricName of Object.keys(previous)) {
      if (current[metricName]) {
        const prevValue = previous[metricName];
        const currValue = current[metricName];
        
        // Check for performance regression (values that got worse)
        const isWorse = this.isMetricWorse(metricName, prevValue, currValue);
        
        if (isWorse) {
          const percentChange = ((currValue - prevValue) / prevValue) * 100;
          
          this.findings.push({
            id: this.generateId(),
            type: 'PERFORMANCE_DEGRADATION',
            severity: Math.abs(percentChange) > 50 ? VerificationSeverity.HIGH : VerificationSeverity.MEDIUM,
            component,
            location: {
              module: component
            },
            title: 'Performance Regression Detected',
            description: `Metric '${metricName}' regressed from ${prevValue} to ${currValue} (${percentChange.toFixed(2)}% change)`,
            evidence: [
              {
                type: 'baseline',
                source: 'previous version',
                content: { metric: metricName, value: prevValue },
                timestamp: new Date(),
                verified: false
              },
              {
                type: 'execution',
                source: 'current version',
                content: { metric: metricName, value: currValue },
                timestamp: new Date(),
                verified: false
              }
            ],
            timestamp: new Date(),
            verified: false,
            falsifiable: true
          });
        }
      }
    }
  }

  /**
   * Check if metric got worse
   */
  private isMetricWorse(metricName: string, previous: number, current: number): boolean {
    // Lower is better metrics
    const lowerIsBetter = [
      'executionTime', 'responseTime', 'latency', 'memoryUsage', 'cpuTime',
      'errorRate', 'failureRate', 'loadTime', 'renderTime'
    ];
    
    if (lowerIsBetter.some(m => metricName.toLowerCase().includes(m))) {
      return current > previous;
    }
    
    // Higher is better metrics
    const higherIsBetter = [
      'throughput', 'qps', 'requestsPerSecond', 'successRate', 'availability',
      'efficiency', 'score', 'rating', 'accuracy'
    ];
    
    if (higherIsBetter.some(m => metricName.toLowerCase().includes(m))) {
      return current < previous;
    }
    
    return false;
  }

  /**
   * Extract regressions from findings
   */
  private extractRegressions() {
    return this.findings.map(finding => ({
      component: finding.component,
      change: finding.title,
      impact: finding.description,
      severity: finding.severity
    }));
  }

  /**
   * Save current version
   */
  async saveVersion(component: string, version: string, data: any): Promise<void> {
    const versionPath = this.getVersionPath(component, version);
    const fs = require('fs').promises;
    
    await fs.writeFile(versionPath, JSON.stringify(data, null, 2), 'utf-8');
    this.previousVersions.set(`${component}:${version}`, data);
  }

  /**
   * Get version path
   */
  private getVersionPath(component: string, version: string): string {
    return `/workspace/gl-runtime-platform/.versions/${component}/${version}.json`;
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

  private getComponentPath(component: string): string {
    return `/workspace/gl-runtime-platform/${component}`;
  }

  private async getTsFiles(path: string): Promise<string[]> {
    const { exec } = require('child_process');
    return new Promise((resolve, reject) => {
      exec(`find ${path} -type f -name "*.ts"`, (error, stdout) => {
        if (error) reject(error);
        else resolve(stdout.trim().split('\n').filter(f => f));
      });
    });
  }

  private async readFileContent(filePath: string): Promise<string> {
    const fs = require('fs').promises;
    return fs.readFile(filePath, 'utf-8');
  }

  private generateId(): string {
    return `regression-diff-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
}
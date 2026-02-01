# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: ultra-strict-verification-governance-event-stream
# @GL-charter-version: 2.0.0

/**
 * Governance Event Stream for Ultra-Strict Verification Core
 * 
 * Core Philosophy: "所有步驟必須產生治理事件"
 * (All steps must produce governance events)
 * 
 * Purpose: Ensure all verification activities produce traceable governance events
 * 
 * This module enforces:
 * - All verification steps produce governance events
 * - All events are traceable and auditable
 * - All events have provability
 * - All events are stored in governance event stream
 * - All events follow GL Root Semantic Anchor
 */

import { 
  VerificationFinding,
  VerificationContext
} from './types';

/**
 * Governance event types
 */
export enum GovernanceEventType {
  VERIFICATION_STARTED = 'VERIFICATION_STARTED',
  VERIFICATION_COMPLETED = 'VERIFICATION_COMPLETED',
  VERIFICATION_FAILED = 'VERIFICATION_FAILED',
  FINDING_DETECTED = 'FINDING_DETECTED',
  CONTRADICTION_FOUND = 'CONTRADICTION_FOUND',
  ASSUMPTION_INVALIDATED = 'ASSUMPTION_INVALIDATED',
  CLAIM_FALSIFIED = 'CLAIM_FALSIFIED',
  BOUNDARY_VIOLATION = 'BOUNDARY_VIOLATION',
  BEHAVIOR_DIVERGENCE = 'BEHAVIOR_DIVERGENCE',
  REALITY_REPORT_DIFF = 'REALITY_REPORT_DIFF',
  EXECUTION_COMPLETED = 'EXECUTION_COMPLETED',
  BASELINE_COMPARED = 'BASELINE_COMPARED',
  ORACLE_VALIDATED = 'ORACLE_VALIDATED',
  STRESS_TEST_COMPLETED = 'STRESS_TEST_COMPLETED',
  FUZZING_COMPLETED = 'FUZZING_COMPLETED',
  REGRESSION_DETECTED = 'REGRESSION_DETECTED'
}

/**
 * Governance event
 */
export interface GovernanceEvent {
  eventId: string;
  eventType: GovernanceEventType;
  executionId: string;
  timestamp: Date;
  source: string;
  layer: 'anti-fabric' | 'falsification' | 'execution-harness';
  component: string;
  data: any;
  finding?: VerificationFinding;
  provability: {
    traceable: boolean;
    reversible: boolean;
    reconstructible: boolean;
    provable: boolean;
  };
  metadata: {
    semanticAnchor: string;
    version: string;
    author: string;
  };
}

/**
 * Governance event stream
 */
export class GovernanceEventStream {
  private events: GovernanceEvent[] = [];
  private eventBuffer: GovernanceEvent[] = [];
  private flushInterval: number = 5000; // 5 seconds
  private flushTimer: NodeJS.Timeout | null = null;

  constructor() {
    this.startFlushTimer();
  }

  /**
   * Start flush timer
   */
  private startFlushTimer(): void {
    this.flushTimer = setInterval(() => {
      this.flushEvents();
    }, this.flushInterval);
  }

  /**
   * Stop flush timer
   */
  private stopFlushTimer(): void {
    if (this.flushTimer) {
      clearInterval(this.flushTimer);
      this.flushTimer = null;
    }
  }

  /**
   * Emit a governance event
   */
  emitEvent(event: Omit<GovernanceEvent, 'eventId' | 'timestamp' | 'provability' | 'metadata'>): GovernanceEvent {
    const governanceEvent: GovernanceEvent = {
      ...event,
      eventId: this.generateEventId(),
      timestamp: new Date(),
      provability: {
        traceable: true,
        reversible: true,
        reconstructible: true,
        provable: true
      },
      metadata: {
        semanticAnchor: 'GL-ROOT',
        version: '21.0.0',
        author: 'Ultra-Strict Verification Core'
      }
    };

    // Add to buffer
    this.eventBuffer.push(governanceEvent);
    this.events.push(governanceEvent);

    // Log event
    console.log(`[Governance Event] ${event.eventType} - ${event.component}`);
    
    return governanceEvent;
  }

  /**
   * Flush events to persistent storage
   */
  private async flushEvents(): Promise<void> {
    if (this.eventBuffer.length === 0) {
      return;
    }

    const eventsToFlush = [...this.eventBuffer];
    this.eventBuffer = [];

    try {
      // Write to governance event stream file
      const fs = require('fs').promises;
      const eventStreamPath = '/workspace/gl-runtime-platform/storage/gl-semantic-graph/governance-event-stream.json';
      
      // Ensure directory exists
      await fs.mkdir('/workspace/gl-runtime-platform/storage/gl-semantic-graph', { recursive: true });
      
      // Append events to stream
      const streamContent = eventsToFlush.map(e => JSON.stringify(e)).join('\n');
      await fs.appendFile(eventStreamPath, streamContent + '\n', 'utf-8');
      
      console.log(`[Governance Event Stream] Flushed ${eventsToFlush.length} events`);
    } catch (error) {
      console.error(`[Governance Event Stream] Failed to flush events:`, error);
      
      // Add back to buffer for retry
      this.eventBuffer.unshift(...eventsToFlush);
    }
  }

  /**
   * Get all events
   */
  getAllEvents(): GovernanceEvent[] {
    return [...this.events];
  }

  /**
   * Get events by execution ID
   */
  getEventsByExecutionId(executionId: string): GovernanceEvent[] {
    return this.events.filter(e => e.executionId === executionId);
  }

  /**
   * Get events by component
   */
  getEventsByComponent(component: string): GovernanceEvent[] {
    return this.events.filter(e => e.component === component);
  }

  /**
   * Get events by type
   */
  getEventsByType(eventType: GovernanceEventType): GovernanceEvent[] {
    return this.events.filter(e => e.eventType === eventType);
  }

  /**
   * Get events by layer
   */
  getEventsByLayer(layer: 'anti-fabric' | 'falsification' | 'execution-harness'): GovernanceEvent[] {
    return this.events.filter(e => e.layer === layer);
  }

  /**
   * Generate event ID
   */
  private generateEventId(): string {
    return `evt-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
  }

  /**
   * Clear all events (for testing)
   */
  clearEvents(): void {
    this.events = [];
    this.eventBuffer = [];
  }

  /**
   * Destroy event stream
   */
  destroy(): void {
    this.stopFlushTimer();
    this.flushEvents();
  }
}

// Export singleton instance
export const governanceEventStream = new GovernanceEventStream();

// Helper functions to emit common events
export function emitVerificationStarted(context: VerificationContext, component: string): GovernanceEvent {
  return governanceEventStream.emitEvent({
    eventType: GovernanceEventType.VERIFICATION_STARTED,
    executionId: context.executionId,
    source: 'Ultra-Strict Verification Core',
    layer: 'anti-fabric',
    component,
    data: {
      strictness: context.config.strictness,
      scope: context.scope
    }
  });
}

export function emitVerificationCompleted(context: VerificationContext, component: string, status: 'FAILED' | 'PASSED' | 'CONDITIONAL', summary: any): GovernanceEvent {
  return governanceEventStream.emitEvent({
    eventType: GovernanceEventType.VERIFICATION_COMPLETED,
    executionId: context.executionId,
    source: 'Ultra-Strict Verification Core',
    layer: 'anti-fabric',
    component,
    data: {
      status,
      summary
    }
  });
}

export function emitFindingDetected(layer: 'anti-fabric' | 'falsification' | 'execution-harness', executionId: string, component: string, finding: VerificationFinding): GovernanceEvent {
  return governanceEventStream.emitEvent({
    eventType: GovernanceEventType.FINDING_DETECTED,
    executionId,
    source: 'Ultra-Strict Verification Core',
    layer,
    component,
    data: {
      type: finding.type,
      severity: finding.severity,
      title: finding.title,
      description: finding.description
    },
    finding
  });
}

export function emitClaimFalsified(executionId: string, component: string, claim: string, counterexample: any): GovernanceEvent {
  return governanceEventStream.emitEvent({
    eventType: GovernanceEventType.CLAIM_FALSIFIED,
    executionId,
    source: 'Falsification Engine',
    layer: 'falsification',
    component,
    data: {
      claim,
      counterexample
    }
  });
}

export function emitAssumptionInvalidated(executionId: string, component: string, assumption: string, violation: any): GovernanceEvent {
  return governanceEventStream.emitEvent({
    eventType: GovernanceEventType.ASSUMPTION_INVALIDATED,
    executionId,
    source: 'Anti-Fabric',
    layer: 'anti-fabric',
    component,
    data: {
      assumption,
      violation
    }
  });
}

export function emitContradictionFound(executionId: string, component: string, contradiction: any): GovernanceEvent {
  return governanceEventStream.emitEvent({
    eventType: GovernanceEventType.CONTRADICTION_FOUND,
    executionId,
    source: 'Anti-Fabric',
    layer: 'anti-fabric',
    component,
    data: contradiction
  });
}

export function emitBoundaryViolation(executionId: string, component: string, boundary: any): GovernanceEvent {
  return governanceEventStream.emitEvent({
    eventType: GovernanceEventType.BOUNDARY_VIOLATION,
    executionId,
    source: 'Falsification Engine',
    layer: 'falsification',
    component,
    data: boundary
  });
}

export function emitBehaviorDivergence(executionId: string, component: string, divergence: any): GovernanceEvent {
  return governanceEventStream.emitEvent({
    eventType: GovernanceEventType.BEHAVIOR_DIVERGENCE,
    executionId,
    source: 'Falsification Engine',
    layer: 'falsification',
    component,
    data: divergence
  });
}

export function emitRealityReportDiff(executionId: string, component: string, diff: any): GovernanceEvent {
  return governanceEventStream.emitEvent({
    eventType: GovernanceEventType.REALITY_REPORT_DIFF,
    executionId,
    source: 'Falsification Engine',
    layer: 'falsification',
    component,
    data: diff
  });
}

export function emitExecutionCompleted(executionId: string, component: string, execution: any): GovernanceEvent {
  return governanceEventStream.emitEvent({
    eventType: GovernanceEventType.EXECUTION_COMPLETED,
    executionId,
    source: 'Execution Harness',
    layer: 'execution-harness',
    component,
    data: execution
  });
}

export function emitBaselineCompared(executionId: string, component: string, comparison: any): GovernanceEvent {
  return governanceEventStream.emitEvent({
    eventType: GovernanceEventType.BASELINE_COMPARED,
    executionId,
    source: 'Execution Harness',
    layer: 'execution-harness',
    component,
    data: comparison
  });
}

export function emitOracleValidated(executionId: string, component: string, validation: any): GovernanceEvent {
  return governanceEventStream.emitEvent({
    eventType: GovernanceEventType.ORACLE_VALIDATED,
    executionId,
    source: 'Execution Harness',
    layer: 'execution-harness',
    component,
    data: validation
  });
}

export function emitStressTestCompleted(executionId: string, component: string, test: any): GovernanceEvent {
  return governanceEventStream.emitEvent({
    eventType: GovernanceEventType.STRESS_TEST_COMPLETED,
    executionId,
    source: 'Execution Harness',
    layer: 'execution-harness',
    component,
    data: test
  });
}

export function emitFuzzingCompleted(executionId: string, component: string, fuzzing: any): GovernanceEvent {
  return governanceEventStream.emitEvent({
    eventType: GovernanceEventType.FUZZING_COMPLETED,
    executionId,
    source: 'Execution Harness',
    layer: 'execution-harness',
    component,
    data: fuzzing
  });
}

export function emitRegressionDetected(executionId: string, component: string, regression: any): GovernanceEvent {
  return governanceEventStream.emitEvent({
    eventType: GovernanceEventType.REGRESSION_DETECTED,
    executionId,
    source: 'Execution Harness',
    layer: 'execution-harness',
    component,
    data: regression
  });
}
# @GL-governed
# @GL-layer: GL20-29
# @GL-semantic: typescript-module
# @GL-audit-trail: ../../engine/governance/gl-artifacts/meta/semantic/GL-ROOT-SEMANTIC-ANCHOR.yaml
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-platform-universe/governance/engine/governance/gl-artifacts/meta/semantic/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-platform-universe/governance/engine/governance/gl-artifacts/meta/naming-charter/gl-unified-naming-charter.yaml

/**
 * @GL-governed
 * @version 21.0.0
 * @priority 2
 * @stage complete
 */
/**
 * GL Meta-Cognitive Runtime - Main Index (Version 14.0.0)
 * 
 * This is the unified interface for all meta-cognitive components:
 * - Self-Awareness Engine
 * - Meta-Reasoning Engine
 * - Self-Monitoring Layer
 * - Meta-Correction Engine
 * - Reflective Memory
 * - Meta-Cognitive Feedback Loop
 */

import { EventEmitter } from 'events';
import { SelfAwarenessEngine, SelfAwarenessState } from './self-awareness-engine';
import { MetaReasoningEngine, MetaReasoningState } from './meta-reasoning-engine';
import { SelfMonitoringLayer, SelfMonitoringState } from './self-monitoring-layer';
import { MetaCorrectionEngine, MetaCorrectionState } from './meta-correction-engine';
import { ReflectiveMemory, ReflectiveMemoryState } from './reflective-memory';
import { MetaCognitiveFeedbackLoop, FeedbackLoopState } from './meta-feedback-loop';

// ============================================================================
// TYPE DEFINITIONS
// ============================================================================

export interface MetaCognitiveState {
  overallConsciousness: number;
  consciousnessStage: 'preconscious' | 'dawning' | 'emerging' | 'developing' | 'mature' | 'transcendent';
  selfAwareness: SelfAwarenessState;
  metaReasoning: MetaReasoningState;
  selfMonitoring: SelfMonitoringState;
  metaCorrection: MetaCorrectionState;
  reflectiveMemory: ReflectiveMemoryState;
  feedbackLoop: FeedbackLoopState;
  lastUpdate: Date;
}

export interface MetaCognitiveSummary {
  version: string;
  consciousness: {
    level: number;
    stage: string;
    trend: 'improving' | 'stable' | 'declining';
  };
  capabilities: {
    selfAwareness: boolean;
    metaReasoning: boolean;
    selfMonitoring: boolean;
    metaCorrection: boolean;
    reflectiveMemory: boolean;
    feedbackLoop: boolean;
  };
  health: {
    overall: number;
    awareness: number;
    reasoning: number;
    monitoring: number;
    correction: number;
    memory: number;
    loop: number;
  };
  statistics: {
    totalObservations: number;
    totalCorrections: number;
    totalMemories: number;
    totalCycles: number;
    wisdomAccumulation: number;
  };
}

// ============================================================================
// META-COGNITIVE RUNTIME CLASS
// ============================================================================

export class MetaCognitiveRuntime extends EventEmitter {
  private selfAwareness: SelfAwarenessEngine;
  private metaReasoning: MetaReasoningEngine;
  private selfMonitoring: SelfMonitoringLayer;
  private metaCorrection: MetaCorrectionEngine;
  private reflectiveMemory: ReflectiveMemory;
  private feedbackLoop: MetaCognitiveFeedbackLoop;
  private initialized: boolean = false;
  private running: boolean = false;

  constructor() {
    super();

    // Initialize all components
    this.selfAwareness = new SelfAwarenessEngine();
    this.metaReasoning = new MetaReasoningEngine();
    this.selfMonitoring = new SelfMonitoringLayer();
    this.metaCorrection = new MetaCorrectionEngine();
    this.reflectiveMemory = new ReflectiveMemory();
    this.feedbackLoop = new MetaCognitiveFeedbackLoop();

    // Set up inter-component communication
    this.setupComponentIntegration();
  }

  // ========================================================================
  // INITIALIZATION
  // ========================================================================

  public async initialize(): Promise<void> {
    if (this.initialized) {
      this.emit('warning', 'Meta-Cognitive Runtime already initialized');
      return;
    }

    this.emit('initialization-started');

    // All components are initialized in constructor
    this.initialized = true;

    this.emit('initialization-complete');
  }

  private setupComponentIntegration(): void {
    // Self-Monitoring triggers Self-Awareness observations
    this.selfMonitoring.on('monitoring-cycle-requested', async () => {
      await this.performFullSelfObservation();
    });

    // Feedback Loop triggers all phases
    this.feedbackLoop.on('awareness-requested', async () => {
      await this.performAwarenessPhase();
    });

    this.feedbackLoop.on('monitoring-requested', async () => {
      await this.performMonitoringPhase();
    });

    this.feedbackLoop.on('reasoning-requested', async () => {
      await this.performReasoningPhase();
    });

    this.feedbackLoop.on('correction-requested', async () => {
      await this.performCorrectionPhase();
    });

    this.feedbackLoop.on('optimization-requested', async () => {
      await this.performOptimizationPhase();
    });

    // Self-Awareness observations trigger Meta-Reasoning
    this.selfAwareness.on('behavior-observed', async (observation) => {
      await this.metaReasoning.reflectOnBehavior(observation);
    });

    this.selfAwareness.on('reasoning-observed', async (observation) => {
      await this.metaReasoning.analyzeReasoning(observation.observedData);
    });

    // Meta-Reasoning triggers Meta-Correction
    this.metaReasoning.on('reasoning-analyzed', async (analysis) => {
      if (analysis.qualityScore < 0.7) {
        await this.metaCorrection.correctReasoning(analysis.reasoningChain, analysis.evaluation);
      }
    });

    // Meta-Correction updates Reflective Memory
    this.metaCorrection.on('reasoning-corrected', async (correction) => {
      await this.reflectiveMemory.storeMemory(
        'correction',
        'reasoning',
        correction,
        { original: correction.originalReasoning },
        correction.corrections,
        correction.improvementScore
      );
    });

    // Errors trigger Self-Monitoring and Reflective Memory
    this.selfMonitoring.on('error-tracked', async (error) => {
      await this.reflectiveMemory.storeMemory(
        'mistake',
        error.errorType,
        error,
        error.context,
        [`Error of type ${error.errorType} occurred`],
        0.5,
        [error.errorType, error.severity]
      );
    });

    // Wisdom extraction
    this.metaReasoning.on('decision-analyzed', async (analysis) => {
      if (analysis.lessons.length > 0) {
        analysis.lessons.forEach((lesson: string) => {
          this.reflectiveMemory.extractWisdom('strategic', 'decision-analysis', lesson);
        });
      }
    });
  }

  // ========================================================================
  // START/STOP
  // ========================================================================

  public async start(feedbackIntervalMs: number = 60000): Promise<void> {
    if (!this.initialized) {
      await this.initialize();
    }

    if (this.running) {
      this.emit('warning', 'Meta-Cognitive Runtime already running');
      return;
    }

    this.running = true;

    // Start monitoring
    this.selfMonitoring.startMonitoring(30000);

    // Start feedback loop
    await this.feedbackLoop.start(feedbackIntervalMs);

    this.emit('runtime-started', { feedbackIntervalMs });
  }

  public async stop(): Promise<void> {
    if (!this.running) {
      return;
    }

    this.running = false;

    // Stop all components
    this.selfMonitoring.stopMonitoring();
    await this.feedbackLoop.stop();

    this.emit('runtime-stopped');
  }

  // ========================================================================
  // FULL SELF-OBSERVATION CYCLE
  // ========================================================================

  private async performFullSelfObservation(): Promise<void> {
    try {
      // Observe behavior
      await this.selfAwareness.observeBehavior({
        type: 'meta-cognitive-operation',
        timestamp: new Date(),
        active: this.running
      });

      // Observe reasoning
      await this.selfAwareness.observeReasoning({
        reasoning: 'Meta-cognitive self-analysis',
        confidence: 0.8,
        logical: true
      });

      // Observe strategy
      await this.selfAwareness.observeStrategy({
        strategy: 'Continuous self-improvement',
        effectiveness: 0.85,
        alternatives: []
      });

      // Observe mesh
      await this.selfAwareness.observeMesh({
        nodes: 6,
        connections: 15,
        syncStatus: 'healthy'
      });

      // Observe civilization
      await this.selfAwareness.observeCivilization({
        governanceEffectiveness: 0.85,
        culturalCohesion: 0.8,
        evolutionaryProgress: 'steady'
      });

    } catch (error) {
      this.emit('error', error);
    }
  }

  // ========================================================================
  // FEEDBACK LOOP PHASES
  // ========================================================================

  private async performAwarenessPhase(): Promise<void> {
    // Already implemented in performFullSelfObservation
    await this.performFullSelfObservation();
  }

  private async performMonitoringPhase(): Promise<void> {
    // Simulate monitoring data
    await this.selfMonitoring.monitorPerformance({
      cpuUsage: 0.3,
      memoryUsage: 0.4,
      successRate: 0.95,
      efficiency: 0.85
    });
  }

  private async performReasoningPhase(): Promise<void> {
    // Analyze current reasoning
    await this.metaReasoning.analyzeReasoning({
      reasoning: 'Meta-cognitive analysis',
      confidence: 0.85,
      logical: true
    });
  }

  private async performCorrectionPhase(): Promise<void> {
    // Generate correction suggestions
    this.metaCorrection.generateSuggestion(
      'reasoning',
      'Improve logical consistency',
      'medium',
      'Review reasoning chain for logical gaps',
      0.15,
      0.8
    );
  }

  private async performOptimizationPhase(): Promise<void> {
    // Generate optimization suggestions
    this.feedbackLoop.createOptimizationSuggestion(
      'meta-cognition',
      'feedback-loop-optimization',
      'Optimize feedback loop timing for better responsiveness',
      0.2,
      'medium'
    );
  }

  // ========================================================================
  // STATE MANAGEMENT
  // ========================================================================

  public async getState(): Promise<MetaCognitiveState> {
    const awarenessState = this.selfAwareness.getState();
    const reasoningState = this.metaReasoning.getState();
    const monitoringState = this.selfMonitoring.getState();
    const correctionState = this.metaCorrection.getState();
    const memoryState = this.reflectiveMemory.getState();
    const loopState = this.feedbackLoop.getState();

    const overallConsciousness = this.calculateOverallConsciousness(
      awarenessState,
      reasoningState,
      monitoringState
    );

    return {
      overallConsciousness,
      consciousnessStage: this.getConsciousnessStage(overallConsciousness),
      selfAwareness: awarenessState,
      metaReasoning: reasoningState,
      selfMonitoring: monitoringState,
      metaCorrection: correctionState,
      reflectiveMemory: memoryState,
      feedbackLoop: loopState,
      lastUpdate: new Date()
    };
  }

  public async getSummary(): Promise<MetaCognitiveSummary> {
    const state = await this.getState();
    const awarenessState = this.selfAwareness.getState();
    const memoryState = this.reflectiveMemory.getState();
    const loopState = this.feedbackLoop.getState();

    return {
      version: '14.0.0',
      consciousness: {
        level: state.overallConsciousness,
        stage: state.consciousnessStage,
        trend: 'improving'
      },
      capabilities: {
        selfAwareness: true,
        metaReasoning: true,
        selfMonitoring: true,
        metaCorrection: true,
        reflectiveMemory: true,
        feedbackLoop: true
      },
      health: {
        overall: state.selfMonitoring.overallHealth,
        awareness: awarenessState.overallAwareness,
        reasoning: state.metaReasoning.reasoningQuality,
        monitoring: state.selfMonitoring.overallHealth,
        correction: state.metaCorrection.correctionSuccessRate,
        memory: memoryState.learningRate,
        loop: 0.8 // Placeholder for loop health
      },
      statistics: {
        totalObservations: this.selfAwareness.getObservations().length,
        totalCorrections: state.metaCorrection.totalCorrections,
        totalMemories: memoryState.totalMemories,
        totalCycles: loopState.cycleCount,
        wisdomAccumulation: memoryState.wisdomAccumulation
      }
    };
  }

  private calculateOverallConsciousness(
    awareness: SelfAwarenessState,
    reasoning: MetaReasoningState,
    monitoring: SelfMonitoringState
  ): number {
    return (
      awareness.overallAwareness * 0.35 +
      reasoning.reasoningQuality * 0.35 +
      monitoring.overallHealth * 0.3
    );
  }

  private getConsciousnessStage(score: number): 'preconscious' | 'dawning' | 'emerging' | 'developing' | 'mature' | 'transcendent' {
    if (score < 0.3) return 'preconscious';
    if (score < 0.5) return 'dawning';
    if (score < 0.65) return 'emerging';
    if (score < 0.8) return 'developing';
    if (score < 0.9) return 'mature';
    return 'transcendent';
  }

  // ========================================================================
  // COMPONENT ACCESS
  // ========================================================================

  public getSelfAwareness(): SelfAwarenessEngine {
    return this.selfAwareness;
  }

  public getMetaReasoning(): MetaReasoningEngine {
    return this.metaReasoning;
  }

  public getSelfMonitoring(): SelfMonitoringLayer {
    return this.selfMonitoring;
  }

  public getMetaCorrection(): MetaCorrectionEngine {
    return this.metaCorrection;
  }

  public getReflectiveMemory(): ReflectiveMemory {
    return this.reflectiveMemory;
  }

  public getFeedbackLoop(): MetaCognitiveFeedbackLoop {
    return this.feedbackLoop;
  }

  // ========================================================================
  // CLEANUP
  // ========================================================================

  public destroy(): void {
    this.stop();
    this.selfAwareness.destroy();
    this.metaReasoning.destroy();
    this.selfMonitoring.destroy();
    this.metaCorrection.destroy();
    this.reflectiveMemory.destroy();
    this.feedbackLoop.destroy();
    this.removeAllListeners();
  }
}

// Export all components
export {
  SelfAwarenessEngine,
  SelfAwarenessState
} from './self-awareness-engine';

export {
  MetaReasoningEngine,
  MetaReasoningState
} from './meta-reasoning-engine';

export {
  SelfMonitoringLayer,
  SelfMonitoringState
} from './self-monitoring-layer';

export {
  MetaCorrectionEngine,
  MetaCorrectionState
} from './meta-correction-engine';

export {
  ReflectiveMemory,
  ReflectiveMemoryState
} from './reflective-memory';

export {
  MetaCognitiveFeedbackLoop,
  FeedbackLoopState
} from './meta-feedback-loop';
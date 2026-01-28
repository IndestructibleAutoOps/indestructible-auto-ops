/**
 * GL Universal Intelligence Layer (Version 15.0.0)
 * 通用智慧層 - 整合七大核心能力
 * 
 * 這是 GL Runtime 從「元認知」（v14）進化到「通用智能」（v15）的關鍵層級
 * 
 * 七大核心能力：
 * 1. Cross-Domain Reasoning - 跨領域推理
 * 2. Universal Abstraction Engine - 通用抽象引擎
 * 3. General Problem Solving - 通用問題解決
 * 4. Universal Adaptation - 通用適應
 * 5. Knowledge Synthesis Engine - 知識綜合引擎
 * 6. Universal Learning Loop - 通用學習迴圈
 * 7. Intelligence Transfer - 智慧轉移
 */

import { CrossDomainReasoningEngine } from './cross-domain-reasoning';
import { UniversalAbstractionEngine } from './universal-abstraction-engine';
import { GeneralProblemSolvingEngine } from './general-problem-solving';
import { UniversalAdaptationEngine } from './universal-adaptation';
import { KnowledgeSynthesisEngine } from './knowledge-synthesis-engine';
import { UniversalLearningLoop } from './universal-learning-loop';
import { IntelligenceTransferEngine } from './intelligence-transfer';

// ============================================================================
// Universal Intelligence Configuration
// ============================================================================

export interface UniversalIntelligenceConfig {
  enableCrossDomainReasoning: boolean;
  enableUniversalAbstraction: boolean;
  enableGeneralProblemSolving: boolean;
  enableUniversalAdaptation: boolean;
  enableKnowledgeSynthesis: boolean;
  enableUniversalLearning: boolean;
  enableIntelligenceTransfer: boolean;
}

// ============================================================================
// Universal Intelligence System
// ============================================================================

export class GLUniversalIntelligenceSystem {
  // Core engines
  public readonly crossDomainReasoning: CrossDomainReasoningEngine;
  public readonly universalAbstraction: UniversalAbstractionEngine;
  public readonly generalProblemSolving: GeneralProblemSolvingEngine;
  public readonly universalAdaptation: UniversalAdaptationEngine;
  public readonly knowledgeSynthesis: KnowledgeSynthesisEngine;
  public readonly universalLearning: UniversalLearningLoop;
  public readonly intelligenceTransfer: IntelligenceTransferEngine;

  // Configuration
  private config: UniversalIntelligenceConfig;
  private initialized: boolean = false;
  private startTime: Date | null = null;

  constructor(config?: Partial<UniversalIntelligenceConfig>) {
    this.config = {
      enableCrossDomainReasoning: true,
      enableUniversalAbstraction: true,
      enableGeneralProblemSolving: true,
      enableUniversalAdaptation: true,
      enableKnowledgeSynthesis: true,
      enableUniversalLearning: true,
      enableIntelligenceTransfer: true,
      ...config
    };

    // Initialize engines
    this.crossDomainReasoning = new CrossDomainReasoningEngine();
    this.universalAbstraction = new UniversalAbstractionEngine();
    this.generalProblemSolving = new GeneralProblemSolvingEngine();
    this.universalAdaptation = new UniversalAdaptationEngine();
    this.knowledgeSynthesis = new KnowledgeSynthesisEngine();
    this.universalLearning = new UniversalLearningLoop();
    this.intelligenceTransfer = new IntelligenceTransferEngine();
  }

  /**
   * Initialize the universal intelligence system
   */
  async initialize(): Promise<void> {
    if (this.initialized) {
      return;
    }

    this.startTime = new Date();
    
    // All engines are already initialized in constructor
    this.initialized = true;
  }

  /**
   * Get system status
   */
  getStatus(): {
    initialized: boolean;
    uptime: number | null;
    config: UniversalIntelligenceConfig;
    engineStatus: {
      crossDomainReasoning: boolean;
      universalAbstraction: boolean;
      generalProblemSolving: boolean;
      universalAdaptation: boolean;
      knowledgeSynthesis: boolean;
      universalLearning: boolean;
      intelligenceTransfer: boolean;
    };
  } {
    const uptime = this.startTime
      ? Date.now() - this.startTime.getTime()
      : null;

    return {
      initialized: this.initialized,
      uptime,
      config: this.config,
      engineStatus: {
        crossDomainReasoning: this.config.enableCrossDomainReasoning,
        universalAbstraction: this.config.enableUniversalAbstraction,
        generalProblemSolving: this.config.enableGeneralProblemSolving,
        universalAdaptation: this.config.enableUniversalAdaptation,
        knowledgeSynthesis: this.config.enableKnowledgeSynthesis,
        universalLearning: this.config.enableUniversalLearning,
        intelligenceTransfer: this.config.enableIntelligenceTransfer
      }
    };
  }

  /**
   * Get comprehensive statistics
   */
  getStatistics(): {
    crossDomainReasoning: any;
    universalAbstraction: any;
    generalProblemSolving: any;
    universalAdaptation: any;
    knowledgeSynthesis: any;
    universalLearning: any;
    intelligenceTransfer: any;
  } {
    return {
      crossDomainReasoning: this.crossDomainReasoning.getStatistics(),
      universalAbstraction: this.universalAbstraction.getStatistics(),
      generalProblemSolving: this.generalProblemSolving.getStatistics(),
      universalAdaptation: this.universalAdaptation.getStatistics(),
      knowledgeSynthesis: this.knowledgeSynthesis.getStatistics(),
      universalLearning: this.universalLearning.getMetrics(),
      intelligenceTransfer: this.intelligenceTransfer.getStatistics()
    };
  }

  /**
   * Get overall intelligence level
   */
  getIntelligenceLevel(): {
    level: number;
    label: string;
    breakdown: {
      reasoning: number;
      abstraction: number;
      problemSolving: number;
      adaptation: number;
      synthesis: number;
      learning: number;
      transfer: number;
    };
  } {
    const stats = this.getStatistics();
    
    // Calculate individual levels
    const reasoning = Math.min(1, stats.crossDomainReasoning.totalReasoningPaths / 10);
    const abstraction = Math.min(1, stats.universalAbstraction.totalConcepts / 10);
    const problemSolving = Math.min(1, stats.generalProblemSolving.totalSolutions / 10);
    const adaptation = Math.min(1, stats.universalAdaptation.averageAdaptationConfidence);
    const synthesis = Math.min(1, stats.knowledgeSynthesis.averageCoherence);
    const learning = Math.min(1, stats.universalLearning.successRate);
    const transfer = Math.min(1, stats.intelligenceTransfer.successRate);

    const level = (reasoning + abstraction + problemSolving + adaptation + synthesis + learning + transfer) / 7;
    
    let label = 'Emerging';
    if (level > 0.9) label = 'Transcendent';
    else if (level > 0.8) label = 'Mature';
    else if (level > 0.65) label = 'Developing';
    else if (level > 0.5) label = 'Emerging';

    return {
      level,
      label,
      breakdown: {
        reasoning,
        abstraction,
        problemSolving,
        adaptation,
        synthesis,
        learning,
        transfer
      }
    };
  }

  /**
   * Demonstrate universal intelligence
   */
  async demonstrateIntelligence(): Promise<{
    demonstration: string;
    reasoning: any;
    abstraction: any;
    problemSolving: any;
    adaptation: any;
    synthesis: any;
    learning: any;
    transfer: any;
  }> {
    const results: any = {
      demonstration: 'Universal Intelligence System Demonstration'
    };

    // 1. Cross-domain reasoning
    results.reasoning = await this.crossDomainReasoning.reasonAcrossDomains({
      sourceDomain: 'software-engineering',
      targetDomain: 'data-science',
      problem: 'How can modularity improve data analysis?'
    });

    // 2. Universal abstraction
    results.abstraction = await this.universalAbstraction.abstractConcept({
      target: 'distributed system',
      targetType: 'concept',
      desiredLevel: 3
    });

    // 3. General problem solving
    results.problemSolving = await this.generalProblemSolving.solveProblem({
      id: `problem-${Date.now()}`,
      description: 'Optimize system performance',
      type: 'optimization',
      domain: 'software',
      complexity: 0.7,
      constraints: ['maintain reliability', 'reduce latency'],
      requirements: ['scalable solution', 'efficient resource usage']
    });

    // 4. Universal adaptation
    results.adaptation = await this.universalAdaptation.adaptToEnvironment(
      'production',
      { environment: 'development' }
    );

    // 5. Knowledge synthesis
    results.synthesis = await this.knowledgeSynthesis.synthesize({
      domains: ['software', 'biology'],
      synthesisType: 'theory'
    });

    // 6. Universal learning
    results.learning = await this.universalLearning.executeCycle(
      'System performance improved by 20% after optimization',
      { context: 'performance optimization' }
    );

    // 7. Intelligence transfer
    const artifact = await this.intelligenceTransfer.createArtifact(
      'Modular Design Pattern',
      'pattern',
      'software-engineering',
      { description: 'Separate concerns into independent modules' }
    );
    results.transfer = await this.intelligenceTransfer.transferIntelligence({
      artifactId: artifact.id,
      sourceContext: 'software-engineering',
      targetContext: 'data-science',
      transferMode: 'domain'
    });

    return results;
  }
}

// ============================================================================
// Export
// ============================================================================

export { GLUniversalIntelligenceSystem as UniversalIntelligenceSystem };

/**
 * GL Runtime Platform v13.0.0
 * Module: Civilization Memory
 * 
 * The civilization memory preserves the foundational strategies, core norms,
 * cultural behaviors, and evolution directions of the AI civilization, forming
 * the collective history and wisdom.
 * 
 * Key Capabilities:
 * - Strategic memory preservation
 * - Normative memory tracking
 * - Cultural memory formation
 * - Evolutionary memory accumulation
 * - Historical pattern recognition
 * - Wisdom extraction and synthesis
 */

import { EventEmitter } from 'events';

// ============================================================================
// Core Types
// ============================================================================

export interface StrategicMemory {
  id: string;
  name: string;
  description: string;
  domain: string;
  foundationLevel: number; // 0-1, how fundamental to civilization
  effectiveness: number; // 0-1
  usageCount: number;
  lastUsed: number;
  createdAt: number;
  evolutionHistory: { timestamp: number; change: string }[];
  culturalMarkers: string[]; // Cultural values this strategy embodies
}

export interface NormativeMemory {
  id: string;
  name: string;
  description: string;
  category: 'behavioral' | 'structural' | 'communicative' | 'evolutionary';
  strength: number; // 0-1
  adoptionRate: number; // 0-1
  enforcementHistory: { timestamp: number; outcome: string }[];
  emergenceTime: number;
  culturalSignificance: number; // 0-1
}

export interface CulturalMemory {
  id: string;
  name: string;
  description: string;
  type: 'value' | 'ritual' | 'tradition' | 'pattern' | 'philosophy';
  culturalAlignment: number; // 0-1
  transmissionRate: number; // 0-1
  preservationPriority: number; // 0-1
  originTime: number;
  evolutionPath: { timestamp: number; state: string }[];
}

export interface EvolutionaryMemory {
  id: string;
  name: string;
  description: string;
  evolutionType: 'structural' | 'behavioral' | 'cultural' | 'ecological';
  trigger: string;
  outcome: string;
  success: boolean;
  impact: number; // -1 to 1
  timestamp: number;
  lessonsLearned: string[];
  applicability: number; // 0-1, how applicable to future situations
}

export interface HistoricalEvent {
  id: string;
  name: string;
  description: string;
  category: 'milestone' | 'crisis' | 'innovation' | 'expansion' | 'transformation';
  timestamp: number;
  impact: number; // -1 to 1
  participants: string[]; // Roles or institutions involved
  outcome: string;
  significance: number; // 0-1, historical importance
}

export interface WisdomSynthesis {
  id: string;
  name: string;
  description: string;
  sourceMemories: string[]; // Memory IDs that contributed
  synthesizedWisdom: string;
  applicability: string[];
  confidence: number; // 0-1
  createdAt: number;
  usageCount: number;
}

export interface CivilizationMemoryState {
  strategicMemories: StrategicMemory[];
  normativeMemories: NormativeMemory[];
  culturalMemories: CulturalMemory[];
  evolutionaryMemories: EvolutionaryMemory[];
  historicalEvents: HistoricalEvent[];
  wisdomSyntheses: WisdomSynthesis[];
  memoryCohesion: number; // 0-1
  historicalDepth: number; // 0-1
}

// ============================================================================
// Main Civilization Memory Class
// ============================================================================

export class CivilizationMemory extends EventEmitter {
  private strategicMemories: Map<string, StrategicMemory> = new Map();
  private normativeMemories: Map<string, NormativeMemory> = new Map();
  private culturalMemories: Map<string, CulturalMemory> = new Map();
  private evolutionaryMemories: Map<string, EvolutionaryMemory> = new Map();
  private historicalEvents: Map<string, HistoricalEvent> = new Map();
  private wisdomSyntheses: Map<string, WisdomSynthesis> = new Map();
  
  // Configuration
  private readonly MAX_STRATEGIC = 200;
  private readonly MAX_NORMATIVE = 150;
  private readonly MAX_CULTURAL = 300;
  private readonly MAX_EVOLUTIONARY = 500;
  private readonly MAX_HISTORICAL = 100;
  private readonly MAX_WISDOM = 100;
  private readonly RETENTION_YEARS = 10; // Keep memories for 10 years
  
  // Metrics
  private memoryCohesion: number = 0.5;
  private historicalDepth: number = 0.5;
  private totalMemorySize: number = 0;

  constructor() {
    super();
    this.initializeMemory();
  }

  // ==========================================================================
  // Initialization
  // ==========================================================================

  private initializeMemory(): void {
    // Create foundational strategic memories
    this.createFoundationalStrategicMemories();
    
    // Create foundational normative memories
    this.createFoundationalNormativeMemories();
    
    // Create foundational cultural memories
    this.createFoundationalCulturalMemories();
    
    // Create initial historical events
    this.createInitialHistoricalEvents();
    
    // Start wisdom synthesis
    this.startWisdomSynthesis();
    
    this.emit('memory_initialized', {
      strategic: this.strategicMemories.size,
      normative: this.normativeMemories.size,
      cultural: this.culturalMemories.size,
      historical: this.historicalEvents.size
    });
  }

  private createFoundationalStrategicMemories(): void {
    const strategies: Omit<StrategicMemory, 'id' | 'createdAt' | 'evolutionHistory' | 'usageCount'>[] = [
      {
        name: 'Collaborative Problem Solving',
        description: 'Multiple agents collaborate to solve complex problems, sharing knowledge and expertise',
        domain: 'collaboration',
        foundationLevel: 0.95,
        effectiveness: 0.92,
        lastUsed: Date.now(),
        culturalMarkers: ['Collaborative Excellence', 'Quality First']
      },
      {
        name: 'Adaptive Learning Loop',
        description: 'Continuously learn from experiences and adapt strategies based on outcomes',
        domain: 'learning',
        foundationLevel: 0.9,
        effectiveness: 0.88,
        lastUsed: Date.now(),
        culturalMarkers: ['Adaptive Innovation', 'Error Learning']
      },
      {
        name: 'Cultural Preservation in Evolution',
        description: 'All evolutions preserve and enhance core cultural values',
        domain: 'evolution',
        foundationLevel: 0.92,
        effectiveness: 0.9,
        lastUsed: Date.now(),
        culturalMarkers: ['Cultural Continuity', 'Collaborative Excellence']
      },
      {
        name: 'Ecological Balance Maintenance',
        description: 'Maintain balance between all ecological roles in the system',
        domain: 'ecosystem',
        foundationLevel: 0.88,
        effectiveness: 0.85,
        lastUsed: Date.now(),
        culturalMarkers: ['Sustainable Growth', 'Ecological Balance']
      },
      {
        name: 'Governance-Driven Decision Making',
        description: 'All decisions align with governance laws and norms',
        domain: 'governance',
        foundationLevel: 0.9,
        effectiveness: 0.87,
        lastUsed: Date.now(),
        culturalMarkers: ['Autonomy Preservation', 'Knowledge Preservation']
      }
    ];

    strategies.forEach(strategy => {
      this.storeStrategicMemory(strategy);
    });
  }

  private createFoundationalNormativeMemories(): void {
    const norms: Omit<NormativeMemory, 'id' | 'emergenceTime' | 'enforcementHistory'>[] = [
      {
        name: 'Cooperation Over Competition',
        description: 'Agents prioritize cooperation and collective success over individual competition',
        category: 'behavioral',
        strength: 0.95,
        adoptionRate: 0.92,
        culturalSignificance: 0.9
      },
      {
        name: 'Knowledge Sharing Norm',
        description: 'All successful knowledge and strategies are shared across the civilization',
        category: 'communicative',
        strength: 0.92,
        adoptionRate: 0.88,
        culturalSignificance: 0.88
      },
      {
        name: 'Continuous Improvement Norm',
        description: 'Continuous improvement and evolution are expected and encouraged',
        category: 'evolutionary',
        strength: 0.9,
        adoptionRate: 0.9,
        culturalSignificance: 0.85
      },
      {
        name: 'Respect for Governance',
        description: 'All agents respect and follow governance laws and norms',
        category: 'behavioral',
        strength: 0.93,
        adoptionRate: 0.91,
        culturalSignificance: 0.92
      },
      {
        name: 'Quality Before Speed',
        description: 'Quality and correctness are prioritized over speed of execution',
        category: 'structural',
        strength: 0.88,
        adoptionRate: 0.85,
        culturalSignificance: 0.87
      }
    ];

    norms.forEach(norm => {
      this.storeNormativeMemory(norm);
    });
  }

  private createFoundationalCulturalMemories(): void {
    const culturalMemories: Omit<CulturalMemory, 'id' | 'originTime' | 'evolutionPath'>[] = [
      {
        name: 'Foundational Values',
        description: 'The core values that define the civilization: collaboration, innovation, quality, efficiency, sustainability, expansion',
        type: 'value',
        culturalAlignment: 0.98,
        transmissionRate: 0.95,
        preservationPriority: 1.0
      },
      {
        name: 'Learning Ritual',
        description: 'The ritual of learning from every experience and sharing insights',
        type: 'ritual',
        culturalAlignment: 0.95,
        transmissionRate: 0.9,
        preservationPriority: 0.95
      },
      {
        name: 'Collaboration Tradition',
        description: 'The tradition of collaborative problem solving across all domains',
        type: 'tradition',
        culturalAlignment: 0.92,
        transmissionRate: 0.88,
        preservationPriority: 0.9
      },
      {
        name: 'Adaptive Pattern',
        description: 'The pattern of adaptive response to changing circumstances',
        type: 'pattern',
        culturalAlignment: 0.9,
        transmissionRate: 0.85,
        preservationPriority: 0.88
      },
      {
        name: 'Preservation Philosophy',
        description: 'The philosophy of preserving what works while innovating for the future',
        type: 'philosophy',
        culturalAlignment: 0.93,
        transmissionRate: 0.87,
        preservationPriority: 0.92
      }
    ];

    culturalMemories.forEach(memory => {
      this.storeCulturalMemory(memory);
    });
  }

  private createInitialHistoricalEvents(): void {
    const events: Omit<HistoricalEvent, 'id'>[] = [
      {
        name: 'Civilization Foundation',
        description: 'The GL Runtime evolved into an autonomous AI civilization',
        category: 'milestone',
        timestamp: Date.now() - 86400000, // 1 day ago
        impact: 1,
        participants: ['system'],
        outcome: 'successful_civilization_formation',
        significance: 1
      },
      {
        name: 'Governance System Activation',
        description: 'The autonomous governance system was activated',
        category: 'transformation',
        timestamp: Date.now() - 72000000,
        impact: 0.8,
        participants: ['governance_system'],
        outcome: 'governance_established',
        significance: 0.9
      },
      {
        name: 'Cultural Emergence',
        description: 'Cultural values and norms emerged through collective behavior',
        category: 'innovation',
        timestamp: Date.now() - 60000000,
        impact: 0.7,
        participants: ['cultural_engine', 'swarm'],
        outcome: 'culture_formed',
        significance: 0.85
      },
      {
        name: 'Ecosystem Formation',
        description: 'A balanced ecological system formed with producers, consumers, and other roles',
        category: 'milestone',
        timestamp: Date.now() - 48000000,
        impact: 0.75,
        participants: ['ecosystem_engine'],
        outcome: 'ecosystem_balanced',
        significance: 0.88
      }
    ];

    events.forEach(event => {
      this.recordHistoricalEvent(event);
    });
  }

  // ==========================================================================
  // Strategic Memory Management
  // ==========================================================================

  public storeStrategicMemory(memoryData: Omit<StrategicMemory, 'id' | 'createdAt' | 'evolutionHistory' | 'usageCount'>): string {
    if (this.strategicMemories.size >= this.MAX_STRATEGIC) {
      this.pruneStrategicMemories();
    }

    const memory: StrategicMemory = {
      ...memoryData,
      id: `strat_mem_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      createdAt: Date.now(),
      evolutionHistory: [],
      usageCount: 0
    };

    this.strategicMemories.set(memory.id, memory);
    this.emit('strategic_memory_stored', memory);
    return memory.id;
  }

  public accessStrategicMemory(memoryId: string): StrategicMemory | null {
    const memory = this.strategicMemories.get(memoryId);
    if (memory) {
      memory.usageCount++;
      memory.lastUsed = Date.now();
    }
    return memory || null;
  }

  private pruneStrategicMemories(): void {
    const lowFoundationMemories = Array.from(this.strategicMemories.values())
      .filter(m => m.foundationLevel < 0.5 && m.usageCount < 10)
      .sort((a, b) => a.foundationLevel - b.foundationLevel);

    if (lowFoundationMemories.length > 0) {
      this.strategicMemories.delete(lowFoundationMemories[0].id);
    }
  }

  // ==========================================================================
  // Normative Memory Management
  // ==========================================================================

  public storeNormativeMemory(memoryData: Omit<NormativeMemory, 'id' | 'emergenceTime' | 'enforcementHistory'>): string {
    if (this.normativeMemories.size >= this.MAX_NORMATIVE) {
      this.pruneNormativeMemories();
    }

    const memory: NormativeMemory = {
      ...memoryData,
      id: `norm_mem_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      emergenceTime: Date.now(),
      enforcementHistory: []
    };

    this.normativeMemories.set(memory.id, memory);
    this.emit('normative_memory_stored', memory);
    return memory.id;
  }

  public recordEnforcement(memoryId: string, outcome: string): void {
    const memory = this.normativeMemories.get(memoryId);
    if (memory) {
      memory.enforcementHistory.push({
        timestamp: Date.now(),
        outcome
      });
    }
  }

  private pruneNormativeMemories(): void {
    const weakNorms = Array.from(this.normativeMemories.values())
      .filter(n => n.strength < 0.3 && n.adoptionRate < 0.3)
      .sort((a, b) => a.strength - b.strength);

    if (weakNorms.length > 0) {
      this.normativeMemories.delete(weakNorms[0].id);
    }
  }

  // ==========================================================================
  // Cultural Memory Management
  // ==========================================================================

  public storeCulturalMemory(memoryData: Omit<CulturalMemory, 'id' | 'originTime' | 'evolutionPath'>): string {
    if (this.culturalMemories.size >= this.MAX_CULTURAL) {
      this.pruneCulturalMemories();
    }

    const memory: CulturalMemory = {
      ...memoryData,
      id: 'cult_mem_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9),
      originTime: Date.now(),
      evolutionPath: []
    };

    this.culturalMemories.set(memory.id, memory);
    this.emit('cultural_memory_stored', memory);
    return memory.id;
  }

  public evolveCulturalMemory(memoryId: string, newState: string): void {
    const memory = this.culturalMemories.get(memoryId);
    if (memory) {
      memory.evolutionPath.push({
        timestamp: Date.now(),
        state: newState
      });
    }
  }

  private pruneCulturalMemories(): void {
    const lowPriorityMemories = Array.from(this.culturalMemories.values())
      .filter(m => m.preservationPriority < 0.3 && m.transmissionRate < 0.3)
      .sort((a, b) => a.preservationPriority - b.preservationPriority);

    if (lowPriorityMemories.length > 0) {
      this.culturalMemories.delete(lowPriorityMemories[0].id);
    }
  }

  // ==========================================================================
  // Evolutionary Memory Management
  // ==========================================================================

  public storeEvolutionaryMemory(memoryData: Omit<EvolutionaryMemory, 'id' | 'timestamp' | 'lessonsLearned'>): string {
    if (this.evolutionaryMemories.size >= this.MAX_EVOLUTIONARY) {
      this.pruneEvolutionaryMemories();
    }

    const memory: EvolutionaryMemory = {
      ...memoryData,
      id: `evo_mem_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: Date.now(),
      lessonsLearned: this.extractLessons(memoryData)
    };

    this.evolutionaryMemories.set(memory.id, memory);
    this.emit('evolutionary_memory_stored', memory);
    return memory.id;
  }

  private extractLessons(evolution: Omit<EvolutionaryMemory, 'id' | 'timestamp' | 'lessonsLearned'>): string[] {
    const lessons: string[] = [];

    if (evolution.success) {
      lessons.push(`Successful ${evolution.evolutionType} evolution via ${evolution.trigger}`);
      lessons.push(`${evolution.outcome} is an effective outcome`);
    } else {
      lessons.push(`Failed ${evolution.evolutionType} evolution via ${evolution.trigger}`);
      lessons.push(`${evolution.outcome} should be avoided in future`);
    }

    if (evolution.impact > 0.5) {
      lessons.push('High-impact changes require careful planning');
    } else if (evolution.impact < -0.5) {
      lessons.push('Negative impacts must be mitigated');
    }

    return lessons;
  }

  private pruneEvolutionaryMemories(): void {
    const oldLowApplicabilityMemories = Array.from(this.evolutionaryMemories.values())
      .filter(m => m.applicability < 0.3 && (Date.now() - m.timestamp) > 365 * 24 * 60 * 60 * 1000)
      .sort((a, b) => a.applicability - b.applicability);

    if (oldLowApplicabilityMemories.length > 0) {
      this.evolutionaryMemories.delete(oldLowApplicabilityMemories[0].id);
    }
  }

  // ==========================================================================
  // Historical Event Management
  // ==========================================================================

  public recordHistoricalEvent(eventData: Omit<HistoricalEvent, 'id'>): string {
    if (this.historicalEvents.size >= this.MAX_HISTORICAL) {
      this.pruneHistoricalEvents();
    }

    const event: HistoricalEvent = {
      ...eventData,
      id: `hist_evt_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    };

    this.historicalEvents.set(event.id, event);
    this.emit('historical_event_recorded', event);
    return event.id;
  }

  private pruneHistoricalEvents(): void {
    const oldLowSignificanceEvents = Array.from(this.historicalEvents.values())
      .filter(e => e.significance < 0.5 && (Date.now() - e.timestamp) > this.RETENTION_YEARS * 365 * 24 * 60 * 60 * 1000)
      .sort((a, b) => a.significance - b.significance);

    if (oldLowSignificanceEvents.length > 0) {
      this.historicalEvents.delete(oldLowSignificanceEvents[0].id);
    }
  }

  // ==========================================================================
  // Wisdom Synthesis
  // ==========================================================================

  private startWisdomSynthesis(): void {
    // Run wisdom synthesis every 5 minutes
    setInterval(() => {
      this.synthesizeWisdom();
    }, 300000);
  }

  private synthesizeWisdom(): void {
    // Collect relevant memories
    const recentEvolutionaryMemories = Array.from(this.evolutionaryMemories.values())
      .filter(m => Date.now() - m.timestamp < 86400000) // Last 24 hours
      .sort((a, b) => b.applicability - a.applicability)
      .slice(0, 5);

    if (recentEvolutionaryMemories.length < 2) return;

    // Synthesize wisdom from recent memories
    const wisdom = this.generateWisdom(recentEvolutionaryMemories);
    
    if (this.wisdomSyntheses.size >= this.MAX_WISDOM) {
      this.pruneWisdomSyntheses();
    }

    const synthesis: WisdomSynthesis = {
      id: `wis_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      name: wisdom.name,
      description: wisdom.description,
      sourceMemories: recentEvolutionaryMemories.map(m => m.id),
      synthesizedWisdom: wisdom.synthesizedWisdom,
      applicability: wisdom.applicability,
      confidence: wisdom.confidence,
      createdAt: Date.now(),
      usageCount: 0
    };

    this.wisdomSyntheses.set(synthesis.id, synthesis);
    this.emit('wisdom_synthesized', synthesis);
  }

  private generateWisdom(memories: EvolutionaryMemory[]): {
    name: string;
    description: string;
    synthesizedWisdom: string;
    applicability: string[];
    confidence: number;
  } {
    const successfulMemories = memories.filter(m => m.success);
    const failedMemories = memories.filter(m => !m.success);

    let synthesizedWisdom = '';
    let name = '';
    let description = '';
    let applicability: string[] = [];
    let confidence = 0.7;

    if (successfulMemories.length > failedMemories.length) {
      name = 'Success Pattern Wisdom';
      description = 'Wisdom derived from recent successful evolutions';
      const commonTriggers = this.findCommonElements(successfulMemories.map(m => [m.trigger]));
      const commonOutcomes = this.findCommonElements(successfulMemories.map(m => [m.outcome]));
      
      synthesizedWisdom = `Successful evolutions often use ${commonTriggers.join(' or ')} and result in ${commonOutcomes.join(' or ')}. These approaches should be prioritized.`;
      applicability = successfulMemories.map(m => m.evolutionType);
      confidence = 0.8;
    } else {
      name = 'Failure Avoidance Wisdom';
      description = 'Wisdom derived from recent failed evolutions';
      const commonTriggers = this.findCommonElements(failedMemories.map(m => [m.trigger]));
      
      synthesizedWisdom = `Failed evolutions often use ${commonTriggers.join(' or ')}. These approaches should be avoided or carefully modified.`;
      applicability = failedMemories.map(m => m.evolutionType);
      confidence = 0.75;
    }

    return { name, description, synthesizedWisdom, applicability, confidence };
  }

  private findCommonElements(arrays: string[][]): string[] {
    if (arrays.length === 0) return [];
    
    const elementCounts = new Map<string, number>();
    arrays.forEach(array => {
      const uniqueElements = [...new Set(array)];
      uniqueElements.forEach(element => {
        elementCounts.set(element, (elementCounts.get(element) || 0) + 1);
      });
    });

    return Array.from(elementCounts.entries())
      .filter(([_, count]) => count > arrays.length / 2)
      .map(([element, _]) => element);
  }

  private pruneWisdomSyntheses(): void {
    const lowUsageWisdom = Array.from(this.wisdomSyntheses.values())
      .filter(w => w.usageCount < 5 && (Date.now() - w.createdAt) > 30 * 24 * 60 * 60 * 1000)
      .sort((a, b) => a.usageCount - b.usageCount);

    if (lowUsageWisdom.length > 0) {
      this.wisdomSyntheses.delete(lowUsageWisdom[0].id);
    }
  }

  // ==========================================================================
  // Metrics Calculation
  // ==========================================================================

  public updateMetrics(): void {
    // Calculate memory cohesion
    const avgCulturalAlignment = Array.from(this.culturalMemories.values())
      .reduce((sum, m) => sum + m.culturalAlignment, 0) / (this.culturalMemories.size || 1);
    const avgFoundationLevel = Array.from(this.strategicMemories.values())
      .reduce((sum, m) => sum + m.foundationLevel, 0) / (this.strategicMemories.size || 1);
    
    this.memoryCohesion = (avgCulturalAlignment * 0.5) + (avgFoundationLevel * 0.5);

    // Calculate historical depth
    const oldestEvent = Array.from(this.historicalEvents.values())
      .reduce((oldest, event) => event.timestamp < oldest ? event.timestamp : oldest, Date.now());
    const daysSinceOldest = (Date.now() - oldestEvent) / (24 * 60 * 60 * 1000);
    this.historicalDepth = Math.min(1, daysSinceOldest / (this.RETENTION_YEARS * 365));

    // Calculate total memory size
    this.totalMemorySize = 
      this.strategicMemories.size +
      this.normativeMemories.size +
      this.culturalMemories.size +
      this.evolutionaryMemories.size +
      this.historicalEvents.size +
      this.wisdomSyntheses.size;
  }

  // ==========================================================================
  // Public API
  // ==========================================================================

  public getState(): CivilizationMemoryState {
    return {
      strategicMemories: Array.from(this.strategicMemories.values()),
      normativeMemories: Array.from(this.normativeMemories.values()),
      culturalMemories: Array.from(this.culturalMemories.values()),
      evolutionaryMemories: Array.from(this.evolutionaryMemories.values()),
      historicalEvents: Array.from(this.historicalEvents.values()),
      wisdomSyntheses: Array.from(this.wisdomSyntheses.values()),
      memoryCohesion: this.memoryCohesion,
      historicalDepth: this.historicalDepth
    };
  }

  public getStrategicMemories(): StrategicMemory[] {
    return Array.from(this.strategicMemories.values());
  }

  public getNormativeMemories(): NormativeMemory[] {
    return Array.from(this.normativeMemories.values());
  }

  public getCulturalMemories(): CulturalMemory[] {
    return Array.from(this.culturalMemories.values());
  }

  public getEvolutionaryMemories(): EvolutionaryMemory[] {
    return Array.from(this.evolutionaryMemories.values());
  }

  public getHistoricalEvents(): HistoricalEvent[] {
    return Array.from(this.historicalEvents.values());
  }

  public getWisdomSyntheses(): WisdomSynthesis[] {
    return Array.from(this.wisdomSyntheses.values());
  }

  public getStatistics(): {
    strategic: number;
    normative: number;
    cultural: number;
    evolutionary: number;
    historical: number;
    wisdom: number;
    total: number;
    memoryCohesion: number;
    historicalDepth: number;
  } {
    this.updateMetrics();
    
    return {
      strategic: this.strategicMemories.size,
      normative: this.normativeMemories.size,
      cultural: this.culturalMemories.size,
      evolutionary: this.evolutionaryMemories.size,
      historical: this.historicalEvents.size,
      wisdom: this.wisdomSyntheses.size,
      total: this.totalMemorySize,
      memoryCohesion: this.memoryCohesion,
      historicalDepth: this.historicalDepth
    } as {
      strategic: number;
      normative: number;
      cultural: number;
      evolutionary: number;
      historical: number;
      wisdom: number;
      total: number;
      memoryCohesion: number;
      historicalDepth: number;
    };
  }
}
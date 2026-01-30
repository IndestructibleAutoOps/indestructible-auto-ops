// @GL-governed
// @GL-layer: GL100-119
// @GL-semantic: runtime-algorithmic-evolution
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

/**
 * GL Infinite Learning Continuum - Perpetual Algorithmic Evolution
 * Version 20.0.0
 * 
 * 核心：演算法永續演化
 * - 演算法會自己突變、交叉、淘汰、生成、特化、跨領域遷移
 * - 演算法不再是「庫」，而是「生態」
 * - 演算法生態系統
 */

import { UnifiedIntelligenceFabric } from '../../unified-intelligence-fabric';

// ============================================================================
// Type Definitions
// ============================================================================

export interface AlgorithmicEvolutionConfig {
  evolutionInterval: number;      // milliseconds
  populationSize: number;
  mutationRate: number;           // 0-1
  crossoverRate: number;          // 0-1
  selectionPressure: number;      // 0-1
  enableAutoEvolution: boolean;
  enableSpecialization: boolean;
  enableCrossDomainMigration: boolean;
}

export interface AlgorithmEcosystem {
  id: string;
  algorithms: Map<string, EvolvingAlgorithm>;
  population: AlgorithmPopulation;
  evolutionHistory: EvolutionEvent[];
  lastEvolution: number;
  ecosystemMetrics: EcosystemMetrics;
}

export interface EvolvingAlgorithm {
  id: string;
  name: string;
  type: AlgorithmType;
  category: AlgorithmCategory;
  implementation: AlgorithmImplementation;
  genotype: AlgorithmGenotype;
  phenotype: AlgorithmPhenotype;
  fitness: number;
  generation: number;
  parentIds: string[];
  specialization?: AlgorithmSpecialization;
  crossDomainCapabilities: string[];
  temporalWeight: number;
}

export type AlgorithmType = 
  | 'transformation'
  | 'inference'
  | 'optimization'
  | 'search'
  | 'pattern_match'
  | 'reasoning'
  | 'learning'
  | 'evolution';

export type AlgorithmCategory = 
  | 'graph'
  | 'semantic'
  | 'statistical'
  | 'neural'
  | 'symbolic'
  | 'probabilistic'
  | 'quantum'
  | 'meta';

export interface AlgorithmGenotype {
  encoding: string;
  complexity: number;
  parameters: Map<string, number>;
  structure: AlgorithmStructure;
}

export interface AlgorithmStructure {
  layers: number;
  nodesPerLayer: number[];
  connections: Connection[];
}

export interface Connection {
  from: number;
  to: number;
  weight: number;
}

export interface AlgorithmPhenotype {
  performance: PerformanceMetrics;
  behavior: BehaviorProfile;
  characteristics: Characteristic[];
}

export interface PerformanceMetrics {
  accuracy: number;
  efficiency: number;
  speed: number;
  resourceUsage: number;
  generalization: number;
}

export interface BehaviorProfile {
  determinism: number;
  adaptability: number;
  creativity: number;
  robustness: number;
}

export interface Characteristic {
  name: string;
  value: number;
}

export interface AlgorithmImplementation {
  type: 'function' | 'flow' | 'pipeline' | 'composite';
  definition: any;
  dependencies: string[];
  computeRequirements: {
    cpuCores: number;
    memory: number;
    estimatedDuration: number;
  };
}

export interface AlgorithmSpecialization {
  domain: string;
  taskType: string;
  specializationLevel: number; // 0-1
  performanceInSpecialization: number;
}

export interface AlgorithmPopulation {
  size: number;
  generation: number;
  diversity: number;
  averageFitness: number;
  bestFitness: number;
  worstFitness: number;
}

export interface EcosystemMetrics {
  populationSize: number;
  algorithmicDiversity: number;
  evolutionaryVelocity: number;
  adaptationRate: number;
  extinctionRate: number;
  speciationRate: number;
}

export interface EvolutionEvent {
  id: string;
  timestamp: number;
  type: EvolutionEventType;
  description: string;
  algorithmIds: string[];
  impact: number;
  evolutionaryScore: number;
}

export type EvolutionEventType = 
  | 'mutation'
  | 'crossover'
  | 'selection'
  | 'extinction'
  | 'speciation'
  | 'specialization'
  | 'cross_domain_migration'
  | 'phenotypic_expression';

export interface AlgorithmicEvolutionStatistics {
  totalAlgorithms: number;
  totalGenerations: number;
  totalEvolutionEvents: number;
  averageFitness: number;
  bestFitness: number;
  algorithmicDiversity: number;
  evolutionaryVelocity: number;
  specializationCount: number;
  crossDomainMigrations: number;
  lastEvolution: number;
}

// ============================================================================
// Perpetual Algorithmic Evolution Class
// ============================================================================

export class PerpetualAlgorithmicEvolution {
  private fabric: UnifiedIntelligenceFabric;
  private config: AlgorithmicEvolutionConfig;
  private ecosystem: AlgorithmEcosystem;
  private evolutionTimer?: NodeJS.Timeout;
  private statistics: AlgorithmicEvolutionStatistics;
  private initialized: boolean;
  
  constructor(
    fabric: UnifiedIntelligenceFabric,
    config?: Partial<AlgorithmicEvolutionConfig>
  ) {
    this.fabric = fabric;
    this.config = {
      evolutionInterval: config?.evolutionInterval || 120000, // 2 minutes
      populationSize: config?.populationSize || 100,
      mutationRate: config?.mutationRate || 0.1,
      crossoverRate: config?.crossoverRate || 0.7,
      selectionPressure: config?.selectionPressure || 0.5,
      enableAutoEvolution: config?.enableAutoEvolution ?? true,
      enableSpecialization: config?.enableSpecialization ?? true,
      enableCrossDomainMigration: config?.enableCrossDomainMigration ?? true
    };
    
    this.ecosystem = {
      id: `ecosystem-${Date.now()}`,
      algorithms: new Map(),
      population: {
        size: 0,
        generation: 0,
        diversity: 0,
        averageFitness: 0,
        bestFitness: 0,
        worstFitness: 0
      },
      evolutionHistory: [],
      lastEvolution: Date.now(),
      ecosystemMetrics: {
        populationSize: 0,
        algorithmicDiversity: 0,
        evolutionaryVelocity: 0,
        adaptationRate: 0,
        extinctionRate: 0,
        speciationRate: 0
      }
    };
    
    this.statistics = {
      totalAlgorithms: 0,
      totalGenerations: 0,
      totalEvolutionEvents: 0,
      averageFitness: 0,
      bestFitness: 0,
      algorithmicDiversity: 0,
      evolutionaryVelocity: 0,
      specializationCount: 0,
      crossDomainMigrations: 0,
      lastEvolution: 0
    };
    this.initialized = false;
  }
  
  async initialize(): Promise<void> {
    console.log('[Perpetual Algorithmic Evolution] Initializing perpetual algorithmic evolution...');
    
    // 初始化演算法生態
    await this.initializeAlgorithmEcosystem();
    
    // 啟動持續演算法演化
    if (this.config.enableAutoEvolution) {
      await this.startPerpetualEvolution();
    }
    
    this.initialized = true;
    console.log('[Perpetual Algorithmic Evolution] Perpetual algorithmic evolution initialized');
  }
  
  // ========================================================================
  // Algorithm Ecosystem Management
  // ========================================================================
  
  private async initializeAlgorithmEcosystem(): Promise<void> {
    console.log('[Perpetual Algorithmic Evolution] Initializing algorithm ecosystem...');
    
    // 創建初始演算法種群
    await this.seedInitialPopulation();
    
    console.log(`[Perpetual Algorithmic Evolution] Initialized ${this.ecosystem.algorithms.size} algorithms`);
  }
  
  private async seedInitialPopulation(): Promise<void> {
    const initialAlgorithms = [
      {
        name: 'Base Transformation',
        type: 'transformation' as AlgorithmType,
        category: 'graph' as AlgorithmCategory
      },
      {
        name: 'Base Search',
        type: 'search' as AlgorithmType,
        category: 'graph' as AlgorithmCategory
      },
      {
        name: 'Base Pattern Match',
        type: 'pattern_match' as AlgorithmType,
        category: 'statistical' as AlgorithmCategory
      },
      {
        name: 'Base Reasoning',
        type: 'reasoning' as AlgorithmType,
        category: 'symbolic' as AlgorithmCategory
      },
      {
        name: 'Base Learning',
        type: 'learning' as AlgorithmType,
        category: 'neural' as AlgorithmCategory
      }
    ];
    
    for (const algo of initialAlgorithms) {
      await this.createAlgorithm(algo.name, algo.type, algo.category);
    }
  }
  
  async createAlgorithm(
    name: string,
    type: AlgorithmType,
    category: AlgorithmCategory
  ): Promise<string> {
    const algorithmId = `algorithm-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    
    const algorithm: EvolvingAlgorithm = {
      id: algorithmId,
      name,
      type,
      category,
      implementation: {
        type: 'function',
        definition: `function ${name}(input) { return input; }`,
        dependencies: [],
        computeRequirements: {
          cpuCores: 1,
          memory: 100,
          estimatedDuration: 100
        }
      },
      genotype: {
        encoding: this.generateGenotypeEncoding(),
        complexity: 1,
        parameters: new Map([
          ['learning_rate', 0.01],
          ['depth', 3],
          ['breadth', 10]
        ]),
        structure: {
          layers: 3,
          nodesPerLayer: [10, 20, 10],
          connections: this.generateRandomConnections(3, [10, 20, 10])
        }
      },
      phenotype: {
        performance: {
          accuracy: 0.5,
          efficiency: 0.5,
          speed: 0.5,
          resourceUsage: 0.5,
          generalization: 0.5
        },
        behavior: {
          determinism: 0.5,
          adaptability: 0.5,
          creativity: 0.5,
          robustness: 0.5
        },
        characteristics: []
      },
      fitness: 0.5,
      generation: 0,
      parentIds: [],
      crossDomainCapabilities: [],
      temporalWeight: 1.0
    };
    
    this.ecosystem.algorithms.set(algorithmId, algorithm);
    this.statistics.totalAlgorithms++;
    this.ecosystem.population.size++;
    
    // 註冊到 Fabric
    await this.fabric.registerAlgorithm({
      id: algorithmId,
      name,
      type,
      category,
      description: `Evolving ${type} algorithm in ${category} category`,
      implementation: algorithm.implementation,
      parameters: [
        {
          name: 'learning_rate',
          type: 'number',
          default: 0.01,
          range: [0.001, 0.1],
          description: 'Learning rate parameter',
          required: false
        }
      ],
      constraints: {},
      performance: {
        averageRuntime: 100,
        successRate: 0.5,
        accuracy: 0.5,
        resourceUsage: { cpu: 0.5, memory: 0.5 },
        lastExecuted: Date.now()
      },
      version: '1.0.0'
    });
    
    console.log(`[Perpetual Algorithmic Evolution] Created algorithm: ${name}`);
    
    return algorithmId;
  }
  
  private generateGenotypeEncoding(): string {
    return Math.random().toString(36).substring(2, 34);
  }
  
  private generateRandomConnections(layers: number, nodesPerLayer: number[]): Connection[] {
    const connections: Connection[] = [];
    
    for (let l = 0; l < layers - 1; l++) {
      for (let i = 0; i < nodesPerLayer[l]; i++) {
        for (let j = 0; j < nodesPerLayer[l + 1]; j++) {
          if (Math.random() > 0.5) {
            connections.push({
              from: l * 100 + i,
              to: (l + 1) * 100 + j,
              weight: Math.random() * 2 - 1
            });
          }
        }
      }
    }
    
    return connections;
  }
  
  // ========================================================================
  // Perpetual Algorithmic Evolution
  // ========================================================================
  
  private async startPerpetualEvolution(): Promise<void> {
    console.log(`[Perpetual Algorithmic Evolution] Starting perpetual evolution every ${this.config.evolutionInterval}ms`);
    
    this.evolutionTimer = setInterval(async () => {
      await this.performPerpetualEvolution();
    }, this.config.evolutionInterval);
  }
  
  private async performPerpetualEvolution(): Promise<void> {
    const startTime = Date.now();
    
    console.log('[Perpetual Algorithmic Evolution] Performing perpetual evolution cycle...');
    
    // 1. 評估適應度
    await this.evaluateFitness();
    
    // 2. 選擇
    await this.performSelection();
    
    // 3. 交叉
    await this.performCrossover();
    
    // 4. 突變
    await this.performMutation();
    
    // 5. 淘汰
    await this.performExtinction();
    
    // 6. 物種形成
    await this.performSpeciation();
    
    // 7. 特化
    if (this.config.enableSpecialization) {
      await this.performSpecialization();
    }
    
    // 8. 跨領域遷移
    if (this.config.enableCrossDomainMigration) {
      await this.performCrossDomainMigration();
    }
    
    // 9. 更新生態指標
    await this.updateEcosystemMetrics();
    
    this.ecosystem.lastEvolution = Date.now();
    this.ecosystem.population.generation++;
    this.statistics.lastEvolution = Date.now();
    
    const duration = Date.now() - startTime;
    console.log(`[Perpetual Algorithmic Evolution] Evolution cycle completed in ${duration}ms`);
  }
  
  private async evaluateFitness(): Promise<void> {
    console.log('[Perpetual Algorithmic Evolution] Evaluating fitness...');
    
    for (const [algorithmId, algorithm] of this.ecosystem.algorithms) {
      // 評估適應度（基於表現型）
      const performanceScore = (
        algorithm.phenotype.performance.accuracy +
        algorithm.phenotype.performance.efficiency +
        algorithm.phenotype.performance.speed +
        algorithm.phenotype.performance.generalization
      ) / 4;
      
      algorithm.fitness = performanceScore;
    }
  }
  
  private async performSelection(): Promise<void> {
    console.log('[Perpetual Algorithmic Evolution] Performing selection...');
    
    // 基於適應度選擇
    const algorithms = Array.from(this.ecosystem.algorithms.values());
    algorithms.sort((a, b) => b.fitness - a.fitness);
    
    // 保留適應度最高的演算法
    const selectionThreshold = this.config.selectionPressure;
    const selectedCount = Math.floor(this.ecosystem.algorithms.size * selectionThreshold);
    
    for (let i = selectedCount; i < algorithms.length; i++) {
      this.ecosystem.algorithms.delete(algorithms[i].id);
    }
    
    // 記錄事件
    await this.recordEvolutionEvent({
      id: `event-${Date.now()}`,
      timestamp: Date.now(),
      type: 'selection',
      description: `Selected top ${selectionThreshold * 100}% algorithms`,
      algorithmIds: algorithms.slice(0, selectedCount).map(a => a.id),
      impact: 2.0,
      evolutionaryScore: 10.0
    });
  }
  
  private async performCrossover(): Promise<void> {
    console.log('[Perpetual Algorithmic Evolution] Performing crossover...');
    
    const algorithms = Array.from(this.ecosystem.algorithms.values());
    
    // 隨機選擇父母進行交叉
    for (let i = 0; i < algorithms.length - 1; i += 2) {
      if (Math.random() < this.config.crossoverRate) {
        const parent1 = algorithms[i];
        const parent2 = algorithms[i + 1];
        
        const childGenotype = this.crossoverGenotypes(parent1.genotype, parent2.genotype);
        
        // 創建子代
        const childId = await this.createAlgorithm(
          `${parent1.name}x${parent2.name}`,
          parent1.type,
          parent1.category
        );
        
        const child = this.ecosystem.algorithms.get(childId);
        if (child) {
          child.genotype = childGenotype;
          child.parentIds = [parent1.id, parent2.id];
          child.generation = Math.max(parent1.generation, parent2.generation) + 1;
        }
        
        // 記錄事件
        await this.recordEvolutionEvent({
          id: `event-${Date.now()}`,
          timestamp: Date.now(),
          type: 'crossover',
          description: `Crossover between ${parent1.name} and ${parent2.name}`,
          algorithmIds: [parent1.id, parent2.id, childId],
          impact: 1.5,
          evolutionaryScore: 7.5
        });
      }
    }
  }
  
  private crossoverGenotypes(genotype1: AlgorithmGenotype, genotype2: AlgorithmGenotype): AlgorithmGenotype {
    // 基因型交叉
    const childGenotype: AlgorithmGenotype = {
      encoding: genotype1.encoding.substring(0, genotype1.encoding.length / 2) + 
                 genotype2.encoding.substring(genotype2.encoding.length / 2),
      complexity: (genotype1.complexity + genotype2.complexity) / 2,
      parameters: new Map(),
      structure: {
        layers: Math.max(genotype1.structure.layers, genotype2.structure.layers),
        nodesPerLayer: genotype1.structure.nodesPerLayer.map((n, i) => 
          Math.round((n + genotype2.structure.nodesPerLayer[i]) / 2)
        ),
        connections: this.crossoverConnections(genotype1.structure.connections, genotype2.structure.connections)
      }
    };
    
    // 參數交叉
    for (const [key, value] of genotype1.parameters) {
      const value2 = genotype2.parameters.get(key);
      if (value2 !== undefined) {
        childGenotype.parameters.set(key, (value + value2) / 2);
      }
    }
    
    return childGenotype;
  }
  
  private crossoverConnections(connections1: Connection[], connections2: Connection[]): Connection[] {
    // 連接交叉（簡化實作）
    const mergedConnections = [...connections1];
    
    for (const conn of connections2) {
      const exists = mergedConnections.some(c => 
        c.from === conn.from && c.to === conn.to
      );
      if (!exists) {
        mergedConnections.push(conn);
      }
    }
    
    return mergedConnections;
  }
  
  private async performMutation(): Promise<void> {
    console.log('[Perpetual Algorithmic Evolution] Performing mutation...');
    
    for (const [algorithmId, algorithm] of this.ecosystem.algorithms) {
      if (Math.random() < this.config.mutationRate) {
        await this.mutateAlgorithm(algorithmId);
      }
    }
  }
  
  private async mutateAlgorithm(algorithmId: string): Promise<void> {
    const algorithm = this.ecosystem.algorithms.get(algorithmId);
    if (!algorithm) return;
    
    // 突變基因型
    algorithm.genotype.encoding = this.mutateEncoding(algorithm.genotype.encoding);
    algorithm.genotype.complexity = Math.max(1, algorithm.genotype.complexity + (Math.random() - 0.5) * 0.5);
    
    // 突變參數
    for (const [key, value] of algorithm.genotype.parameters) {
      const mutation = value + (Math.random() - 0.5) * 0.2;
      algorithm.genotype.parameters.set(key, Math.max(0.001, Math.min(1.0, mutation)));
    }
    
    // 突變表現型
    algorithm.phenotype.performance.accuracy = Math.max(0, Math.min(1, 
      algorithm.phenotype.performance.accuracy + (Math.random() - 0.5) * 0.1
    ));
    
    algorithm.generation++;
    
    // 記錄事件
    await this.recordEvolutionEvent({
      id: `event-${Date.now()}`,
      timestamp: Date.now(),
      type: 'mutation',
      description: `Mutation in ${algorithm.name}`,
      algorithmIds: [algorithmId],
      impact: 1.0,
      evolutionaryScore: 5.0
    });
  }
  
  private mutateEncoding(encoding: string): string {
    const chars = encoding.split('');
    const mutationIndex = Math.floor(Math.random() * chars.length);
    chars[mutationIndex] = String.fromCharCode(97 + Math.floor(Math.random() * 26));
    return chars.join('');
  }
  
  private async performExtinction(): Promise<void> {
    console.log('[Perpetual Algorithmic Evolution] Performing extinction...');
    
    const extinctionThreshold = 0.1;
    const extinctAlgorithms: string[] = [];
    
    for (const [algorithmId, algorithm] of this.ecosystem.algorithms) {
      if (algorithm.fitness < extinctionThreshold) {
        extinctAlgorithms.push(algorithmId);
        this.ecosystem.algorithms.delete(algorithmId);
      }
    }
    
    if (extinctAlgorithms.length > 0) {
      // 記錄事件
      await this.recordEvolutionEvent({
        id: `event-${Date.now()}`,
        timestamp: Date.now(),
        type: 'extinction',
        description: `${extinctAlgorithms.length} algorithms went extinct`,
        algorithmIds: extinctAlgorithms,
        impact: extinctAlgorithms.length,
        evolutionaryScore: extinctAlgorithms.length * 2.5
      });
    }
  }
  
  private async performSpeciation(): Promise<void> {
    console.log('[Perpetual Algorithmic Evolution] Performing speciation...');
    
    // 物種形成（創建新類型的演算法）
    const existingTypes = new Set(Array.from(this.ecosystem.algorithms.values()).map(a => a.category));
    
    if (existingTypes.size < 8 && Math.random() > 0.7) {
      const newCategories = ['graph', 'semantic', 'statistical', 'neural', 'symbolic', 'probabilistic', 'quantum', 'meta'];
      const availableCategories = newCategories.filter(c => !existingTypes.has(c));
      
      if (availableCategories.length > 0) {
        const newCategory = availableCategories[Math.floor(Math.random() * availableCategories.length)];
        await this.createAlgorithm(
          `Speciated ${newCategory}`,
          'optimization',
          newCategory as AlgorithmCategory
        );
        
        this.statistics.totalEvolutionEvents++;
        
        // 記錄事件
        await this.recordEvolutionEvent({
          id: `event-${Date.now()}`,
          timestamp: Date.now(),
          type: 'speciation',
          description: `New species emerged: ${newCategory}`,
          algorithmIds: [],
          impact: 3.0,
          evolutionaryScore: 15.0
        });
      }
    }
  }
  
  private async performSpecialization(): Promise<void> {
    console.log('[Perpetual Algorithmic Evolution] Performing specialization...');
    
    const domains = ['software', 'data', 'systems', 'cognitive', 'governance', 'civilization'];
    
    for (const [algorithmId, algorithm] of this.ecosystem.algorithms) {
      if (!algorithm.specialization && Math.random() > 0.8) {
        const domain = domains[Math.floor(Math.random() * domains.length)];
        
        algorithm.specialization = {
          domain,
          taskType: algorithm.type,
          specializationLevel: Math.random(),
          performanceInSpecialization: algorithm.fitness * 1.2
        };
        
        this.statistics.specializationCount++;
        
        // 記錄事件
        await this.recordEvolutionEvent({
          id: `event-${Date.now()}`,
          timestamp: Date.now(),
          type: 'specialization',
          description: `${algorithm.name} specialized for ${domain}`,
          algorithmIds: [algorithmId],
          impact: 2.0,
          evolutionaryScore: 10.0
        });
      }
    }
  }
  
  private async performCrossDomainMigration(): Promise<void> {
    console.log('[Perpetual Algorithmic Evolution] Performing cross-domain migration...');
    
    const domains = ['software', 'data', 'systems', 'cognitive', 'governance', 'civilization', 'meta', 'universal'];
    
    for (const [algorithmId, algorithm] of this.ecosystem.algorithms) {
      if (algorithm.crossDomainCapabilities.length < 3 && Math.random() > 0.85) {
        const targetDomain = domains[Math.floor(Math.random() * domains.length)];
        
        if (!algorithm.crossDomainCapabilities.includes(targetDomain)) {
          algorithm.crossDomainCapabilities.push(targetDomain);
          this.statistics.crossDomainMigrations++;
          
          // 記錄事件
          await this.recordEvolutionEvent({
            id: `event-${Date.now()}`,
            timestamp: Date.now(),
            type: 'cross_domain_migration',
            description: `${algorithm.name} migrated to ${targetDomain}`,
            algorithmIds: [algorithmId],
            impact: 2.5,
            evolutionaryScore: 12.5
          });
        }
      }
    }
  }
  
  private async updateEcosystemMetrics(): Promise<void> {
    const algorithms = Array.from(this.ecosystem.algorithms.values());
    
    // 種群大小
    this.ecosystem.population.size = algorithms.length;
    this.ecosystem.ecosystemMetrics.populationSize = algorithms.length;
    
    // 種群指標
    if (algorithms.length > 0) {
      const fitnesses = algorithms.map(a => a.fitness);
      this.ecosystem.population.averageFitness = fitnesses.reduce((sum, f) => sum + f, 0) / fitnesses.length;
      this.ecosystem.population.bestFitness = Math.max(...fitnesses);
      this.ecosystem.population.worstFitness = Math.min(...fitnesses);
      
      // 多樣性
      const categories = new Set(algorithms.map(a => a.category));
      this.ecosystem.population.diversity = categories.size / 8;
      this.ecosystem.ecosystemMetrics.algorithmicDiversity = this.ecosystem.population.diversity;
      
      // 演化速度
      const recentGenerations = algorithms.filter(a => a.generation > this.ecosystem.population.generation - 5);
      this.ecosystem.ecosystemMetrics.evolutionaryVelocity = recentGenerations.length / algorithms.length;
    }
    
    this.statistics.totalGenerations = this.ecosystem.population.generation;
    this.statistics.averageFitness = this.ecosystem.population.averageFitness;
    this.statistics.bestFitness = this.ecosystem.population.bestFitness;
    this.statistics.algorithmicDiversity = this.ecosystem.population.diversity;
    this.statistics.evolutionaryVelocity = this.ecosystem.ecosystemMetrics.evolutionaryVelocity;
  }
  
  // ========================================================================
  // Statistics & Monitoring
  // ========================================================================
  
  async getStatistics(): Promise<AlgorithmicEvolutionStatistics> {
    return { ...this.statistics };
  }
  
  async getEcosystem(): Promise<AlgorithmEcosystem> {
    return {
      id: this.ecosystem.id,
      algorithms: new Map(this.ecosystem.algorithms),
      population: { ...this.ecosystem.population },
      evolutionHistory: [...this.ecosystem.evolutionHistory],
      lastEvolution: this.ecosystem.lastEvolution,
      ecosystemMetrics: { ...this.ecosystem.ecosystemMetrics }
    };
  }
  
  async getAlgorithm(algorithmId: string): Promise<EvolvingAlgorithm | undefined> {
    return this.ecosystem.algorithms.get(algorithmId);
  }
  
  async listAlgorithms(): Promise<EvolvingAlgorithm[]> {
    return Array.from(this.ecosystem.algorithms.values());
  }
  
  // ========================================================================
  // Event Recording
  // ========================================================================
  
  private async recordEvolutionEvent(event: EvolutionEvent): Promise<void> {
    this.evolutionHistory.push(event);
    this.statistics.totalEvolutionEvents++;
    
    // 限制歷史記錄大小
    const maxHistorySize = 10000;
    if (this.evolutionHistory.length > maxHistorySize) {
      this.evolutionHistory = this.evolutionHistory.slice(-maxHistorySize);
    }
  }
  
  async getEvolutionHistory(limit?: number): Promise<EvolutionEvent[]> {
    if (limit) {
      return this.evolutionHistory.slice(-limit);
    }
    return [...this.evolutionHistory];
  }
  
  // ========================================================================
  // Lifecycle Management
  // ========================================================================
  
  async shutdown(): Promise<void> {
    console.log('[Perpetual Algorithmic Evolution] Shutting down...');
    
    if (this.evolutionTimer) {
      clearInterval(this.evolutionTimer);
      this.evolutionTimer = undefined;
    }
    
    // 最後一次演化
    await this.performPerpetualEvolution();
    
    console.log('[Perpetual Algorithmic Evolution] Shutdown complete');
  }
  
  isInitialized(): boolean {
    return this.initialized;
  }
}
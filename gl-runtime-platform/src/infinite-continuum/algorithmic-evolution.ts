// @GL-governed
// @GL-layer: GL100-119
// @GL-semantic: runtime-infinite-continuum
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

/**
 * GL Infinite Learning Continuum - Algorithmic Evolution
 * Version 20.0.0
 * Self-improving algorithms through genetic evolution
 */

import {
  AlgorithmGenome,
  AlgorithmPerformance,
  EvolutionEvent
} from './types';
import { v4 as uuidv4 } from 'uuid';

export class PerpetualAlgorithmicEvolution {
  private population: Map<string, AlgorithmGenome>;
  private evolutionHistory: EvolutionEvent[];
  private config: {
    interval: number;
    populationSize: number;
    mutationRate: number;
    elitismRate: number;
    crossoverRate: number;
  };
  private evolutionInterval: NodeJS.Timeout | null = null;
  private generation: number = 0;

  constructor(config?: Partial<PerpetualAlgorithmicEvolution['config']>) {
    this.config = {
      interval: 180000, // 3 minutes
      populationSize: 50,
      mutationRate: 0.1,
      elitismRate: 0.2,
      crossoverRate: 0.7,
      ...config
    };

    this.population = new Map();
    this.evolutionHistory = [];
  }

  /**
   * Start continuous algorithmic evolution
   */
  public start(): void {
    if (this.evolutionInterval) {
      return;
    }

    this.evolutionInterval = setInterval(() => {
      this.performEvolution();
    }, this.config.interval);
  }

  /**
   * Stop algorithmic evolution
   */
  public stop(): void {
    if (this.evolutionInterval) {
      clearInterval(this.evolutionInterval);
      this.evolutionInterval = null;
    }
  }

  /**
   * Perform one generation of evolution
   */
  private performEvolution(): void {
    this.generation++;

    // Sort by fitness
    const sortedPopulation = this.sortByFitness();

    // Selection (Elitism)
    const eliteCount = Math.floor(this.config.populationSize * this.config.elitismRate);
    const elites = sortedPopulation.slice(0, eliteCount);

    // Crossover
    const offspring: AlgorithmGenome[] = [];
    while (offspring.length + eliteCount < this.config.populationSize) {
      const parent1 = this.selectParent(sortedPopulation);
      const parent2 = this.selectParent(sortedPopulation);

      if (Math.random() < this.config.crossoverRate) {
        const child = this.crossover(parent1, parent2);
        offspring.push(child);
      } else {
        offspring.push(this.clone(parent1));
      }
    }

    // Mutation
    const mutatedOffspring = offspring.map(child => this.mutate(child));

    // Replace population
    this.population.clear();
    for (const elite of elites) {
      elite.generation = this.generation;
      this.population.set(elite.id, elite);
    }
    for (const mutant of mutatedOffspring) {
      mutant.generation = this.generation;
      this.population.set(mutant.id, mutant);
    }

    // Record evolution event
    this.recordEvolutionEvent({
      id: uuidv4(),
      type: 'selection',
      timestamp: Date.now(),
      parentId: 'generation',
      childId: `gen_${this.generation}`,
      fitnessDelta: this.calculatePopulationFitnessDelta()
    });
  }

  /**
   * Sort population by fitness
   */
  private sortByFitness(): AlgorithmGenome[] {
    return Array.from(this.population.values())
      .sort((a, b) => {
        const fitnessA = this.calculateFitness(a);
        const fitnessB = this.calculateFitness(b);
        return fitnessB - fitnessA;
      });
  }

  /**
   * Calculate fitness of an algorithm genome
   */
  private calculateFitness(genome: AlgorithmGenome): number {
    const perf = genome.performance;
    return (perf.accuracy * 0.3) + 
           (perf.efficiency * 0.3) + 
           (perf.adaptability * 0.2) + 
           (perf.generalization * 0.2);
  }

  /**
   * Select parent using tournament selection
   */
  private selectParent(sortedPopulation: AlgorithmGenome[]): AlgorithmGenome {
    const tournamentSize = 3;
    const tournament: AlgorithmGenome[] = [];

    for (let i = 0; i < tournamentSize; i++) {
      const randomIndex = Math.floor(Math.random() * sortedPopulation.length);
      tournament.push(sortedPopulation[randomIndex]);
    }

    return tournament.reduce((best, current) => {
      const fitnessBest = this.calculateFitness(best);
      const fitnessCurrent = this.calculateFitness(current);
      return fitnessCurrent > fitnessBest ? current : best;
    });
  }

  /**
   * Crossover two parent genomes
   */
  private crossover(parent1: AlgorithmGenome, parent2: AlgorithmGenome): AlgorithmGenome {
    const childParams = new Map<string, any>();

    // Crossover parameters
    for (const [key, value] of parent1.parameters.entries()) {
      if (parent2.parameters.has(key)) {
        // Blend crossover for numeric values
        if (typeof value === 'number' && typeof parent2.parameters.get(key) === 'number') {
          const alpha = Math.random();
          childParams.set(key, value * alpha + parent2.parameters.get(key) * (1 - alpha));
        } else {
          // Uniform crossover for other types
          childParams.set(key, Math.random() < 0.5 ? value : parent2.parameters.get(key));
        }
      } else {
        childParams.set(key, value);
      }
    }

    // Add parameters from parent2 that parent1 doesn't have
    for (const [key, value] of parent2.parameters.entries()) {
      if (!childParams.has(key)) {
        childParams.set(key, value);
      }
    }

    const child: AlgorithmGenome = {
      id: uuidv4(),
      algorithmType: Math.random() < 0.5 ? parent1.algorithmType : parent2.algorithmType,
      parameters: childParams,
      performance: this.initializePerformance(),
      lineage: [...parent1.lineage, parent1.id],
      generation: this.generation
    };

    return child;
  }

  /**
   * Mutate an algorithm genome
   */
  private mutate(genome: AlgorithmGenome): AlgorithmGenome {
    const mutatedParams = new Map<string, any>();

    for (const [key, value] of genome.parameters.entries()) {
      if (Math.random() < this.config.mutationRate) {
        // Mutate parameter
        if (typeof value === 'number') {
          // Gaussian mutation for numeric values
          const mutation = (Math.random() - 0.5) * 0.2 * value;
          mutatedParams.set(key, Math.max(0, value + mutation));
        } else if (typeof value === 'boolean') {
          // Flip mutation for boolean values
          mutatedParams.set(key, !value);
        } else if (typeof value === 'string') {
          // Keep string values unchanged
          mutatedParams.set(key, value);
        } else if (Array.isArray(value)) {
          // Array mutation: add or remove element
          const mutatedArray = [...value];
          if (Math.random() < 0.5 && mutatedArray.length > 0) {
            mutatedArray.pop();
          } else {
            mutatedArray.push(0);
          }
          mutatedParams.set(key, mutatedArray);
        } else {
          mutatedParams.set(key, value);
        }
      } else {
        mutatedParams.set(key, value);
      }
    }

    // Occasionally add new parameter
    if (Math.random() < this.config.mutationRate * 0.5) {
      const newKey = `param_${Date.now()}`;
      mutatedParams.set(newKey, Math.random());
    }

    const mutated: AlgorithmGenome = {
      ...genome,
      id: uuidv4(),
      parameters: mutatedParams,
      lineage: [...genome.lineage]
    };

    return mutated;
  }

  /**
   * Clone a genome
   */
  private clone(genome: AlgorithmGenome): AlgorithmGenome {
    const cloned: AlgorithmGenome = {
      id: uuidv4(),
      algorithmType: genome.algorithmType,
      parameters: new Map(genome.parameters),
      performance: { ...genome.performance },
      lineage: [...genome.lineage],
      generation: genome.generation
    };

    return cloned;
  }

  /**
   * Initialize performance metrics
   */
  private initializePerformance(): AlgorithmPerformance {
    return {
      accuracy: 0.5,
      efficiency: 0.5,
      adaptability: 0.5,
      generalization: 0.5,
      lastUpdated: Date.now()
    };
  }

  /**
   * Calculate population fitness delta
   */
  private calculatePopulationFitnessDelta(): number {
    const currentFitness = this.calculateAverageFitness();
    
    // Simple delta calculation (in production, compare with historical data)
    const targetFitness = 0.7;
    return currentFitness - targetFitness;
  }

  /**
   * Calculate average population fitness
   */
  private calculateAverageFitness(): number {
    if (this.population.size === 0) {
      return 0;
    }

    const totalFitness = Array.from(this.population.values())
      .reduce((sum, genome) => sum + this.calculateFitness(genome), 0);

    return totalFitness / this.population.size;
  }

  /**
   * Record evolution event
   */
  private recordEvolutionEvent(event: EvolutionEvent): void {
    this.evolutionHistory.push(event);

    // Keep only last 1000 events
    if (this.evolutionHistory.length > 1000) {
      this.evolutionHistory = this.evolutionHistory.slice(-1000);
    }
  }

  /**
   * Add initial algorithm genome
   */
  public addInitialGenome(
    algorithmType: string,
    parameters: Record<string, any>
  ): string {
    const genome: AlgorithmGenome = {
      id: uuidv4(),
      algorithmType,
      parameters: new Map(Object.entries(parameters)),
      performance: this.initializePerformance(),
      lineage: [],
      generation: 0
    };

    this.population.set(genome.id, genome);
    return genome.id;
  }

  /**
   * Update algorithm performance
   */
  public updatePerformance(
    genomeId: string,
    performance: Partial<AlgorithmPerformance>
  ): void {
    const genome = this.population.get(genomeId);
    if (!genome) {
      return;
    }

    genome.performance = {
      ...genome.performance,
      ...performance,
      lastUpdated: Date.now()
    };
  }

  /**
   * Get best algorithm
   */
  public getBestAlgorithm(): AlgorithmGenome | null {
    const sorted = this.sortByFitness();
    return sorted.length > 0 ? sorted[0] : null;
  }

  /**
   * Get population
   */
  public getPopulation(): AlgorithmGenome[] {
    return Array.from(this.population.values());
  }

  /**
   * Get evolution history
   */
  public getEvolutionHistory(limit?: number): EvolutionEvent[] {
    if (limit) {
      return this.evolutionHistory.slice(-limit);
    }
    return this.evolutionHistory;
  }

  /**
   * Get current generation
   */
  public getGeneration(): number {
    return this.generation;
  }

  /**
   * Get population statistics
   */
  public getPopulationStats(): {
    size: number;
    generation: number;
    averageFitness: number;
    bestFitness: number;
    diversity: number;
  } {
    const population = Array.from(this.population.values());
    const fitnesses = population.map(g => this.calculateFitness(g));
    
    return {
      size: population.length,
      generation: this.generation,
      averageFitness: this.calculateAverageFitness(),
      bestFitness: Math.max(...fitnesses, 0),
      diversity: this.calculateDiversity(population)
    };
  }

  /**
   * Calculate population diversity
   */
  private calculateDiversity(population: AlgorithmGenome[]): number {
    if (population.length === 0) {
      return 0;
    }

    // Simplified diversity calculation based on algorithm type diversity
    const types = new Set(population.map(g => g.algorithmType));
    return types.size / population.length;
  }

  /**
   * Export population as JSON
   */
  public exportPopulation(): string {
    const population = Array.from(this.population.values()).map(genome => ({
      id: genome.id,
      algorithmType: genome.algorithmType,
      parameters: Object.fromEntries(genome.parameters),
      performance: genome.performance,
      lineage: genome.lineage,
      generation: genome.generation
    }));

    return JSON.stringify(population, null, 2);
  }

  /**
   * Import population from JSON
   */
  public importPopulation(json: string): void {
    try {
      const populationData = JSON.parse(json);
      this.population.clear();

      for (const data of populationData) {
        const genome: AlgorithmGenome = {
          id: data.id,
          algorithmType: data.algorithmType,
          parameters: new Map(Object.entries(data.parameters)),
          performance: data.performance,
          lineage: data.lineage,
          generation: data.generation
        };

        this.population.set(genome.id, genome);
      }
    } catch (error) {
      console.error('Failed to import population:', error);
    }
  }
}
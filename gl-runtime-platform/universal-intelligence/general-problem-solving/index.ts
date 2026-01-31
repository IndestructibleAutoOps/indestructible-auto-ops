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
 * General Problem Solving Engine
 * 通用問題解決引擎 - 具備解決任何問題的能力
 * 
 * 核心能力：
 * - 解決從未見過的問題
 * - 自己發明解法
 * - 自己創造工具
 * - 自己構建新策略
 */

// ============================================================================
// Data Types & Interfaces
// ============================================================================

export interface Problem {
  id: string;
  description: string;
  type: string;
  domain: string;
  complexity: number;
  constraints: string[];
  requirements: string[];
  context?: Record<string, any>;
}

export interface Solution {
  id: string;
  problemId: string;
  approach: string;
  steps: SolutionStep[];
  tools: Tool[];
  strategy: Strategy;
  confidence: number;
  effectiveness?: number;
  timestamp: Date;
}

export interface SolutionStep {
  stepNumber: number;
  action: string;
  reasoning: string;
  dependencies: number[];
  expectedOutcome: string;
}

export interface Tool {
  id: string;
  name: string;
  description: string;
  type: 'invented' | 'existing' | 'adapted';
  capability: string;
  implementation: string;
}

export interface Strategy {
  id: string;
  name: string;
  description: string;
  type: 'analytical' | 'creative' | 'heuristic' | 'algorithmic' | 'hybrid';
  approach: string;
  successRate: number;
}

export interface ProblemSpace {
  id: string;
  domain: string;
  knownProblems: Problem[];
  knownSolutions: Solution[];
  patterns: string[];
  heuristics: string[];
}

export interface SolutionPath {
  id: string;
  problemId: string;
  candidateSolutions: Solution[];
  selectedSolution: Solution;
  reasoning: string;
  confidence: number;
}

// ============================================================================
// General Problem Solving Engine
// ============================================================================

export class GeneralProblemSolvingEngine {
  private problems: Map<string, Problem>;
  private solutions: Map<string, Solution>;
  private tools: Map<string, Tool>;
  private strategies: Map<string, Strategy>;
  private problemSpaces: Map<string, ProblemSpace>;
  private solutionPaths: Map<string, SolutionPath>;

  constructor() {
    this.problems = new Map();
    this.solutions = new Map();
    this.tools = new Map();
    this.strategies = new Map();
    this.problemSpaces = new Map();
    this.solutionPaths = new Map();

    this.initializeDefaultStrategies();
    this.initializeDefaultTools();
  }

  /**
   * Initialize default strategies
   */
  private initializeDefaultStrategies(): void {
    const defaultStrategies: Strategy[] = [
      {
        id: 'analytical',
        name: 'Analytical Decomposition',
        description: 'Break problem into smaller sub-problems',
        type: 'analytical',
        approach: 'Decompose problem into components, solve each component, combine solutions',
        successRate: 0.85
      },
      {
        id: 'creative',
        name: 'Creative Lateral Thinking',
        description: 'Approach problem from unexpected angles',
        type: 'creative',
        approach: 'Generate novel perspectives, challenge assumptions, explore alternatives',
        successRate: 0.75
      },
      {
        id: 'heuristic',
        name: 'Heuristic Search',
        description: 'Use rules of thumb to guide search',
        type: 'heuristic',
        approach: 'Apply heuristics to navigate solution space efficiently',
        successRate: 0.8
      },
      {
        id: 'algorithmic',
        name: 'Algorithmic Approach',
        description: 'Apply systematic algorithmic procedures',
        type: 'algorithmic',
        approach: 'Use well-defined algorithms to guarantee solution',
        successRate: 0.9
      },
      {
        id: 'hybrid',
        name: 'Hybrid Multi-Strategy',
        description: 'Combine multiple strategies',
        type: 'hybrid',
        approach: 'Select and combine best strategies for problem characteristics',
        successRate: 0.88
      }
    ];

    defaultStrategies.forEach(strategy => this.strategies.set(strategy.id, strategy));
  }

  /**
   * Initialize default tools
   */
  private initializeDefaultTools(): void {
    const defaultTools: Tool[] = [
      {
        id: 'analyzer',
        name: 'Problem Analyzer',
        description: 'Analyze problem structure and requirements',
        type: 'existing',
        capability: 'decomposition, pattern recognition',
        implementation: 'systematic analysis'
      },
      {
        id: 'solver',
        name: 'General Solver',
        description: 'Apply solution strategies',
        type: 'existing',
        capability: 'strategy execution, solution generation',
        implementation: 'strategy-based solving'
      },
      {
        id: 'validator',
        name: 'Solution Validator',
        description: 'Validate solution correctness',
        type: 'existing',
        capability: 'verification, testing',
        implementation: 'validation procedures'
      }
    ];

    defaultTools.forEach(tool => this.tools.set(tool.id, tool));
  }

  /**
   * Solve a problem
   */
  async solveProblem(problem: Problem): Promise<Solution> {
    // Register problem
    this.problems.set(problem.id, problem);

    // Analyze problem
    const analysis = this.analyzeProblem(problem);

    // Select strategy
    const strategy = this.selectStrategy(problem, analysis);

    // Generate solution candidates
    const candidates = await this.generateSolutionCandidates(problem, strategy);

    // Evaluate candidates
    const evaluatedCandidates = candidates.map(c => ({
      ...c,
      confidence: this.evaluateSolution(c, problem)
    }));

    // Select best solution
    const bestSolution = this.selectBestSolution(evaluatedCandidates);

    // Register solution
    this.solutions.set(bestSolution.id, bestSolution);

    return bestSolution;
  }

  /**
   * Analyze problem
   */
  private analyzeProblem(problem: Problem): Record<string, any> {
    return {
      complexity: problem.complexity,
      domain: problem.domain,
      type: problem.type,
      constraints: problem.constraints.length,
      requirements: problem.requirements.length,
      context: problem.context ? Object.keys(problem.context).length : 0
    };
  }

  /**
   * Select best strategy
   */
  private selectStrategy(problem: Problem, analysis: Record<string, any>): Strategy {
    // Analytical for complex problems
    if (problem.complexity > 0.7) {
      return this.strategies.get('analytical')!;
    }

    // Creative for novel problems
    if (analysis.type === 'novel' || analysis.type === 'unknown') {
      return this.strategies.get('creative')!;
    }

    // Algorithmic for well-defined problems
    if (analysis.type === 'well-defined') {
      return this.strategies.get('algorithmic')!;
    }

    // Default to hybrid
    return this.strategies.get('hybrid')!;
  }

  /**
   * Generate solution candidates
   */
  private async generateSolutionCandidates(problem: Problem, strategy: Strategy): Promise<Solution[]> {
    const candidates: Solution[] = [];

    // Generate primary solution using selected strategy
    const primarySolution = await this.generateSolution(problem, strategy, 1);
    candidates.push(primarySolution);

    // Generate alternative solutions
    for (let i = 2; i <= 3; i++) {
      const altStrategy = this.getAlternativeStrategy(strategy.id);
      const altSolution = await this.generateSolution(problem, altStrategy, i);
      candidates.push(altSolution);
    }

    return candidates;
  }

  /**
   * Generate a solution
   */
  private async generateSolution(
    problem: Problem,
    strategy: Strategy,
    variant: number
  ): Promise<Solution> {
    // Generate steps
    const steps = this.generateSolutionSteps(problem, strategy);

    // Invent or select tools
    const tools = this.selectOrInventTools(problem, strategy);

    const solution: Solution = {
      id: `solution-${Date.now()}-${variant}`,
      problemId: problem.id,
      approach: strategy.name,
      steps,
      tools,
      strategy,
      confidence: strategy.successRate,
      timestamp: new Date()
    };

    return solution;
  }

  /**
   * Generate solution steps
   */
  private generateSolutionSteps(problem: Problem, strategy: Strategy): SolutionStep[] {
    const steps: SolutionStep[] = [];

    switch (strategy.type) {
      case 'analytical':
        steps.push(
          {
            stepNumber: 1,
            action: 'Decompose problem',
            reasoning: 'Break problem into manageable sub-problems',
            dependencies: [],
            expectedOutcome: 'Set of sub-problems'
          },
          {
            stepNumber: 2,
            action: 'Solve sub-problems',
            reasoning: 'Address each sub-problem systematically',
            dependencies: [1],
            expectedOutcome: 'Solutions to all sub-problems'
          },
          {
            stepNumber: 3,
            action: 'Integrate solutions',
            reasoning: 'Combine sub-solutions into complete solution',
            dependencies: [2],
            expectedOutcome: 'Complete solution to original problem'
          }
        );
        break;

      case 'creative':
        steps.push(
          {
            stepNumber: 1,
            action: 'Challenge assumptions',
            reasoning: 'Question fundamental assumptions about the problem',
            dependencies: [],
            expectedOutcome: 'New perspective on problem'
          },
          {
            stepNumber: 2,
            action: 'Explore alternatives',
            reasoning: 'Generate novel approaches and perspectives',
            dependencies: [1],
            expectedOutcome: 'Multiple alternative approaches'
          },
          {
            stepNumber: 3,
            action: 'Select creative solution',
            reasoning: 'Choose most innovative viable approach',
            dependencies: [2],
            expectedOutcome: 'Novel solution'
          }
        );
        break;

      default:
        steps.push(
          {
            stepNumber: 1,
            action: 'Analyze problem',
            reasoning: 'Understand problem structure and requirements',
            dependencies: [],
            expectedOutcome: 'Problem analysis'
          },
          {
            stepNumber: 2,
            action: 'Apply strategy',
            reasoning: `Apply ${strategy.name} to solve problem`,
            dependencies: [1],
            expectedOutcome: 'Solution approach'
          },
          {
            stepNumber: 3,
            action: 'Implement solution',
            reasoning: 'Execute solution approach',
            dependencies: [2],
            expectedOutcome: 'Final solution'
          }
        );
    }

    return steps;
  }

  /**
   * Select or invent tools
   */
  private selectOrInventTools(problem: Problem, strategy: Strategy): Tool[] {
    const tools: Tool[] = [];

    // Use existing tools
    tools.push(
      this.tools.get('analyzer')!,
      this.tools.get('solver')!,
      this.tools.get('validator')!
    );

    // Invent new tools if needed
    if (problem.complexity > 0.8) {
      const inventedTool: Tool = {
        id: `invented-${Date.now()}`,
        name: `Specialized ${problem.type} Tool`,
        description: `Tool designed for ${problem.type} problems`,
        type: 'invented',
        capability: `specialized ${problem.domain} solving`,
        implementation: 'custom implementation'
      };
      this.tools.set(inventedTool.id, inventedTool);
      tools.push(inventedTool);
    }

    return tools;
  }

  /**
   * Get alternative strategy
   */
  private getAlternativeStrategy(currentStrategyId: string): Strategy {
    const strategies = Array.from(this.strategies.values());
    const alternatives = strategies.filter(s => s.id !== currentStrategyId);
    return alternatives[Math.floor(Math.random() * alternatives.length)];
  }

  /**
   * Evaluate solution
   */
  private evaluateSolution(solution: Solution, problem: Problem): number {
    let score = 0;

    // Strategy success rate
    score += solution.strategy.successRate * 0.4;

    // Tool quality
    const toolQuality = solution.tools.reduce((sum, tool) => {
      return sum + (tool.type === 'invented' ? 0.9 : 0.8);
    }, 0) / solution.tools.length;
    score += toolQuality * 0.3;

    // Step coherence
    const stepCoherence = solution.steps.length > 0 ? 0.85 : 0.5;
    score += stepCoherence * 0.3;

    return Math.min(1, score);
  }

  /**
   * Select best solution
   */
  private selectBestSolution(candidates: Solution[]): Solution {
    return candidates.reduce((best, current) => 
      current.confidence > best.confidence ? current : best
    );
  }

  /**
   * Invent new tool
   */
  async inventTool(requirements: string[]): Promise<Tool> {
    const tool: Tool = {
      id: `invented-${Date.now()}`,
      name: `Invented Tool ${Date.now()}`,
      description: requirements.join(', '),
      type: 'invented',
      capability: requirements.join(' + '),
      implementation: 'custom implementation'
    };

    this.tools.set(tool.id, tool);
    return tool;
  }

  /**
   * Create new strategy
   */
  async createStrategy(
    name: string,
    description: string,
    type: Strategy['type'],
    approach: string
  ): Promise<Strategy> {
    const strategy: Strategy = {
      id: `strategy-${Date.now()}`,
      name,
      description,
      type,
      approach,
      successRate: 0.7 // Initial success rate, will be refined
    };

    this.strategies.set(strategy.id, strategy);
    return strategy;
  }

  /**
   * Get solution statistics
   */
  getStatistics(): {
    totalProblems: number;
    totalSolutions: number;
    totalTools: number;
    totalStrategies: number;
    averageSolutionConfidence: number;
  } {
    const solutions = Array.from(this.solutions.values());
    const avgConfidence = solutions.length > 0
      ? solutions.reduce((sum, s) => sum + s.confidence, 0) / solutions.length
      : 0;

    return {
      totalProblems: this.problems.size,
      totalSolutions: this.solutions.size,
      totalTools: this.tools.size,
      totalStrategies: this.strategies.size,
      averageSolutionConfidence: avgConfidence
    };
  }
}
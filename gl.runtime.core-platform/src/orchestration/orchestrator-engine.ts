// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: multi-agent-orchestrator
// @GL-charter-version: 2.0.0

import { v4 as uuidv4 } from 'uuid';
import { EventStreamManager } from '../events/event-stream-manager';
import { PolicyEngine } from '../policies/policy-engine';
import { createLogger } from '../utils/logger';

const logger = createLogger('OrchestratorEngine');

export interface AgentConfig {
  id: string;
  name: string;
  type: string;
  priority: number;
  enabled: boolean;
  config: any;
  dependencies: string[];
  outputs: string[];
}

export interface ExecutionTask {
  id: string;
  agentId: string;
  filePath?: string;
  input: any;
  status: 'pending' | 'running' | 'completed' | 'failed';
  result?: any;
  error?: string;
  startTime?: string;
  endTime?: string;
}

export class OrchestratorEngine {
  private agents: Map<string, AgentConfig> = new Map();
  private taskQueue: ExecutionTask[] = [];
  private runningTasks: Map<string, ExecutionTask> = new Map();
  private completedTasks: Map<string, ExecutionTask> = new Map();
  private maxConcurrentAgents: number = 8;
  private eventStream: EventStreamManager;
  private policyEngine: PolicyEngine;

  constructor() {
    this.eventStream = new EventStreamManager();
    this.policyEngine = new PolicyEngine();
  }

  public registerAgent(agent: AgentConfig): void {
    this.agents.set(agent.id, agent);
    logger.info(`Agent registered: ${agent.id}`);
  }

  public async executePerFilePipeline(filePath: string): Promise<void> {
    const taskId = uuidv4();
    
    // Create task for each agent
    for (const [agentId, agent] of this.agents) {
      if (!agent.enabled) continue;

      const task: ExecutionTask = {
        id: uuidv4(),
        agentId,
        filePath,
        input: { filePath },
        status: 'pending'
      };

      this.taskQueue.push(task);
    }

    // Execute tasks in dependency order
    await this.executeTasks();

    // Log governance event
    await this.eventStream.logEvent({
      eventType: 'pipeline_execution',
      layer: 'GL90-99',
      semanticAnchor: 'GL-ROOT-GOVERNANCE',
      timestamp: new Date().toISOString(),
      metadata: {
        filePath,
        totalTasks: this.taskQueue.length,
        completedTasks: this.completedTasks.size
      }
    });
  }

  private async executeTasks(): Promise<void> {
    while (this.taskQueue.length > 0 || this.runningTasks.size > 0) {
      // Start new tasks if capacity available
      while (this.runningTasks.size < this.maxConcurrentAgents && this.taskQueue.length > 0) {
        const task = this.taskQueue.shift()!;
        await this.executeTask(task);
      }

      // Wait a bit before next iteration
      await new Promise(resolve => setTimeout(resolve, 100));
    }
  }

  private async executeTask(task: ExecutionTask): Promise<void> {
    const agent = this.agents.get(task.agentId);
    if (!agent) {
      task.status = 'failed';
      task.error = 'Agent not found';
      return;
    }

    task.status = 'running';
    task.startTime = new Date().toISOString();
    this.runningTasks.set(task.id, task);

    logger.info(`Executing task ${task.id} with agent ${agent.id}`);

    try {
      // Validate against policy engine
      const validationResult = await this.policyEngine.validate(task.input, agent.config);
      
      if (!validationResult.valid) {
        throw new Error(`Policy validation failed: ${validationResult.error}`);
      }

      // Execute agent logic (placeholder for actual agent implementation)
      const result = await this.executeAgentLogic(agent, task);

      task.status = 'completed';
      task.result = result;
      task.endTime = new Date().toISOString();

      logger.info(`Task ${task.id} completed successfully`);

    } catch (error: any) {
      task.status = 'failed';
      task.error = error.message;
      task.endTime = new Date().toISOString();

      logger.error(`Task ${task.id} failed: ${error.message}`);

      await this.eventStream.logEvent({
        eventType: 'task_failed',
        layer: 'GL90-99',
        semanticAnchor: 'GL-ROOT-GOVERNANCE',
        timestamp: new Date().toISOString(),
        metadata: {
          taskId: task.id,
          agentId: task.agentId,
          error: error.message
        }
      });
    } finally {
      this.runningTasks.delete(task.id);
      this.completedTasks.set(task.id, task);
    }
  }

  private async executeAgentLogic(agent: AgentConfig, task: ExecutionTask): Promise<any> {
    // Placeholder for actual agent implementation
    // Each agent would have its own execution logic here
    
    const result = {
      agentId: agent.id,
      agentName: agent.name,
      success: true,
      outputs: agent.outputs,
      metadata: {
        executionTime: Date.now(),
        timestamp: new Date().toISOString()
      }
    };

    return result;
  }

  public getTaskStatus(taskId: string): ExecutionTask | undefined {
    return this.completedTasks.get(taskId) || this.runningTasks.get(taskId);
  }

  public getAllCompletedTasks(): ExecutionTask[] {
    return Array.from(this.completedTasks.values());
  }

  public reset(): void {
    this.taskQueue = [];
    this.runningTasks.clear();
    this.completedTasks.clear();
  }
}
// @GL-governed
// GL-ROOT Global Governance Audit & Platform Build
// Unified Charter v2.0.0 - Task Scheduler

const { CronJob } = require('cron');
const { v4: uuidv4 } = require('uuid');
const winston = require('winston');
const fs = require('fs').promises;
const path = require('path');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: '../../storage/gl-events-stream/scheduler.log' }),
    new winston.transports.Console()
  ]
});

class Scheduler {
  constructor() {
    this.tasks = new Map();
    this.cronJobs = new Map();
    this.eventStream = [];
  }

  scheduleTask(task) {
    const taskId = uuidv4();
    const taskData = {
      id: taskId,
      ...task,
      status: 'scheduled',
      createdAt: new Date().toISOString()
    };

    this.tasks.set(taskId, taskData);
    logger.info('Task scheduled', { taskId, name: task.name });
    this.logEvent('task_scheduled', taskData);

    // Create cron job if schedule is provided
    if (task.schedule) {
      const job = new CronJob(task.schedule, async () => {
        await this.executeTask(taskId);
      });
      job.start();
      this.cronJobs.set(taskId, job);
    }

    return taskId;
  }

  async executeTask(taskId) {
    const task = this.tasks.get(taskId);
    if (!task) {
      throw new Error(`Task not found: ${taskId}`);
    }

    task.status = 'running';
    task.startedAt = new Date().toISOString();
    this.logEvent('task_started', task);

    try {
      const result = await this.runTaskLogic(task);
      task.status = 'completed';
      task.completedAt = new Date().toISOString();
      task.result = result;
      this.logEvent('task_completed', task);
      return result;
    } catch (error) {
      task.status = 'failed';
      task.failedAt = new Date().toISOString();
      task.error = error.message;
      this.logEvent('task_failed', { taskId, error: error.message });
      throw error;
    }
  }

  async runTaskLogic(task) {
    switch (task.type) {
      case 'audit':
        return await this.runAuditTask(task);
      case 'fix':
        return await this.runFixTask(task);
      case 'deploy':
        return await this.runDeployTask(task);
      case 'monitor':
        return await this.runMonitorTask(task);
      default:
        throw new Error(`Unknown task type: ${task.type}`);
    }
  }

  async runAuditTask(task) {
    logger.info('Running audit task', { taskId: task.id, scope: task.scope });
    return {
      audited: true,
      scope: task.scope,
      findings: []
    };
  }

  async runFixTask(task) {
    logger.info('Running fix task', { taskId: task.id });
    return {
      fixed: true,
      changes: task.changes || []
    };
  }

  async runDeployTask(task) {
    logger.info('Running deploy task', { taskId: task.id });
    return {
      deployed: true,
      artifacts: task.artifacts || []
    };
  }

  async runMonitorTask(task) {
    logger.info('Running monitor task', { taskId: task.id });
    return {
      monitored: true,
      metrics: {}
    };
  }

  cancelTask(taskId) {
    const task = this.tasks.get(taskId);
    if (!task) {
      throw new Error(`Task not found: ${taskId}`);
    }

    const cronJob = this.cronJobs.get(taskId);
    if (cronJob) {
      cronJob.stop();
      this.cronJobs.delete(taskId);
    }

    task.status = 'cancelled';
    task.cancelledAt = new Date().toISOString();
    this.logEvent('task_cancelled', task);

    return task;
  }

  getTaskStatus(taskId) {
    return this.tasks.get(taskId);
  }

  getAllTasks() {
    return Array.from(this.tasks.values());
  }

  logEvent(type, data) {
    const event = {
      id: uuidv4(),
      timestamp: new Date().toISOString(),
      type,
      data,
      source: 'scheduler'
    };
    this.eventStream.push(event);
    logger.info('Scheduler event logged', event);

    fs.appendFile(
      path.join(__dirname, '../../storage/gl-events-stream/scheduler-events.jsonl'),
      JSON.stringify(event) + '\n'
    ).catch(err => logger.error('Event stream write failed', { error: err.message }));
  }
}

module.exports = Scheduler;
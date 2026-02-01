// @GL-governed
// @GL-layer: GL70-89
// @GL-semantic: connector-indexing
// @GL-charter-version: 2.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

// GL-ROOT Global Governance Audit & Platform Build
// Unified Charter v2.0.0 - GitHub CI Connector

const axios = require('axios');
const { v4: uuidv4 } = require('uuid');
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: '../../storage/gl-events-stream/github-connector.log' }),
    new winston.transports.Console()
  ]
});

class GitHubCIConnector {
  constructor(token, repoOwner, repoName) {
    this.token = token;
    this.baseURL = `https://api.github.com/repos/${repoOwner}/${repoName}`;
    this.eventStream = [];
  }

  async triggerWorkflow(workflowId, inputs) {
    const triggerId = uuidv4();
    logger.info('Workflow trigger started', { triggerId, workflowId });
    this.logEvent('workflow_trigger_started', { triggerId, workflowId });

    try {
      const response = await axios.post(
        `${this.baseURL}/actions/workflows/${workflowId}/dispatches`,
        {
          ref: 'main',
          inputs: inputs || {}
        },
        {
          headers: {
            'Authorization': `token ${this.token}`,
            'Accept': 'application/vnd.github.v3+json'
          }
        }
      );

      const result = {
        triggerId,
        workflowId,
        status: 'triggered',
        triggeredAt: new Date().toISOString()
      };

      this.logEvent('workflow_triggered', result);
      return result;
    } catch (error) {
      logger.error('Workflow trigger failed', { triggerId, error: error.message });
      this.logEvent('workflow_trigger_failed', { triggerId, error: error.message });
      throw error;
    }
  }

  async getWorkflowRun(runId) {
    try {
      const response = await axios.get(
        `${this.baseURL}/actions/runs/${runId}`,
        {
          headers: {
            'Authorization': `token ${this.token}`,
            'Accept': 'application/vnd.github.v3+json'
          }
        }
      );

      return response.data;
    } catch (error) {
      throw new Error(`Failed to get workflow run: ${error.message}`);
    }
  }

  async getWorkflowStatus(workflowId) {
    try {
      const response = await axios.get(
        `${this.baseURL}/actions/workflows/${workflowId}/runs`,
        {
          headers: {
            'Authorization': `token ${this.token}`,
            'Accept': 'application/vnd.github.v3+json'
          }
        }
      );

      return {
        workflowId,
        runs: response.data.workflow_runs,
        totalRuns: response.data.total_count
      };
    } catch (error) {
      throw new Error(`Failed to get workflow status: ${error.message}`);
    }
  }

  async createArtifact(name, files) {
    const artifactId = uuidv4();
    logger.info('Artifact creation started', { artifactId, name });
    this.logEvent('artifact_creation_started', { artifactId, name });

    // Note: Actual artifact upload would require more complex implementation
    // This is a minimal operational implementation
    
    const result = {
      artifactId,
      name,
      files: files.length,
      createdAt: new Date().toISOString()
    };

    this.logEvent('artifact_created', result);
    return result;
  }

  async listArtifacts(runId) {
    try {
      const response = await axios.get(
        `${this.baseURL}/actions/runs/${runId}/artifacts`,
        {
          headers: {
            'Authorization': `token ${this.token}`,
            'Accept': 'application/vnd.github.v3+json'
          }
        }
      );

      return response.data.artifacts;
    } catch (error) {
      throw new Error(`Failed to list artifacts: ${error.message}`);
    }
  }

  async getRepositoryStatus() {
    try {
      const response = await axios.get(
        this.baseURL,
        {
          headers: {
            'Authorization': `token ${this.token}`,
            'Accept': 'application/vnd.github.v3+json'
          }
        }
      );

      return {
        status: 'operational',
        repository: response.data
      };
    } catch (error) {
      return {
        status: 'error',
        error: error.message
      };
    }
  }

  logEvent(type, data) {
    const event = {
      id: uuidv4(),
      timestamp: new Date().toISOString(),
      type,
      data,
      source: 'github-ci-connector'
    };
    this.eventStream.push(event);
    logger.info('GitHub CI connector event logged', event);

    const fs = require('fs').promises;
    fs.appendFile(
      './storage/gl-events-stream/github-events.jsonl',
      JSON.stringify(event) + '\n'
    ).catch(err => logger.error('Event stream write failed', { error: err.message }));
  }
}

module.exports = GitHubCIConnector;
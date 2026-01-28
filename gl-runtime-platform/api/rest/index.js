// @GL-governed
// GL-ROOT Global Governance Audit & Platform Build
// Unified Charter v2.0.0 - REST API

const express = require('express');
const OrchestrationEngine = require('../../engine/orchestration-engine');
const SandboxRunner = require('../../engine/sandbox-runner');
const GLCore = require('../../governance/gl-core');
const GLPolicyEngine = require('../../governance/gl-policy-engine');
const GitConnector = require('../../connectors/connector-git');
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: '../../storage/gl-events-stream/rest-api.log' }),
    new winston.transports.Console()
  ]
});

class RestAPI {
  constructor() {
    this.app = express();
    this.engine = new OrchestrationEngine();
    this.sandbox = new SandboxRunner();
    this.glCore = new GLCore();
    this.policyEngine = new GLPolicyEngine();
    this.gitConnector = new GitConnector(process.cwd());
    
    this.setupMiddleware();
    this.setupRoutes();
  }

  setupMiddleware() {
    this.app.use(express.json());
    this.app.use((req, res, next) => {
      logger.info('API Request', { method: req.method, path: req.path });
      next();
    });
  }

  setupRoutes() {
    // Audit endpoints
    this.app.post('/api/v1/audit', this.handleAudit.bind(this));
    this.app.get('/api/v1/audit/:id', this.handleGetAudit.bind(this));
    
    // Fix endpoints
    this.app.post('/api/v1/fix', this.handleFix.bind(this));
    this.app.get('/api/v1/fix/:id', this.handleGetFix.bind(this));
    
    // Integrate endpoints
    this.app.post('/api/v1/integrate', this.handleIntegrate.bind(this));
    this.app.get('/api/v1/integrate/:id', this.handleGetIntegrate.bind(this));
    
    // Deploy endpoints
    this.app.post('/api/v1/deploy', this.handleDeploy.bind(this));
    this.app.get('/api/v1/deploy/:id', this.handleGetDeploy.bind(this));
    
    // Governance endpoints
    this.app.get('/api/v1/governance/status', this.handleGovernanceStatus.bind(this));
    this.app.get('/api/v1/governance/rules', this.handleGetRules.bind(this));
    this.app.get('/api/v1/governance/policies', this.handleGetPolicies.bind(this));
    
    // Sandbox endpoints
    this.app.post('/api/v1/sandbox/execute', this.handleSandboxExecute.bind(this));
    
    // Git endpoints
    this.app.get('/api/v1/git/status', this.handleGitStatus.bind(this));
    this.app.post('/api/v1/git/commit', this.handleGitCommit.bind(this));
    
    // Platform endpoints
    this.app.get('/api/v1/status', this.handleStatus.bind(this));
    this.app.get('/api/v1/events', this.handleEvents.bind(this));
  }

  async handleAudit(req, res) {
    try {
      const result = await this.engine.handleAudit(req, res);
    } catch (error) {
      logger.error('Audit error', { error: error.message });
      res.status(500).json({ error: error.message });
    }
  }

  async handleGetAudit(req, res) {
    try {
      const auditId = req.params.id;
      const result = await this.engine.getAuditResult(auditId);
      res.json({ success: true, result });
    } catch (error) {
      logger.error('Get audit error', { error: error.message });
      res.status(500).json({ error: error.message });
    }
  }

  async handleFix(req, res) {
    try {
      const result = await this.engine.handleFix(req, res);
    } catch (error) {
      logger.error('Fix error', { error: error.message });
      res.status(500).json({ error: error.message });
    }
  }

  async handleGetFix(req, res) {
    try {
      const fixId = req.params.id;
      const result = await this.engine.getFixResult(fixId);
      res.json({ success: true, result });
    } catch (error) {
      logger.error('Get fix error', { error: error.message });
      res.status(500).json({ error: error.message });
    }
  }

  async handleIntegrate(req, res) {
    try {
      const { components, context } = req.body;
      const integrateId = require('uuid').v4();
      
      logger.info('Integration started', { integrateId, components });
      
      // Integration logic
      const result = {
        integrateId,
        integrated: true,
        components,
        completedAt: new Date().toISOString()
      };
      
      res.json({ success: true, result });
    } catch (error) {
      logger.error('Integration error', { error: error.message });
      res.status(500).json({ error: error.message });
    }
  }

  async handleGetIntegrate(req, res) {
    try {
      const integrateId = req.params.id;
      res.json({ success: true, integrateId, status: 'completed' });
    } catch (error) {
      logger.error('Get integration error', { error: error.message });
      res.status(500).json({ error: error.message });
    }
  }

  async handleDeploy(req, res) {
    try {
      const result = await this.engine.handleDeploy(req, res);
    } catch (error) {
      logger.error('Deploy error', { error: error.message });
      res.status(500).json({ error: error.message });
    }
  }

  async handleGetDeploy(req, res) {
    try {
      const deployId = req.params.id;
      const result = await this.engine.getDeployResult(deployId);
      res.json({ success: true, result });
    } catch (error) {
      logger.error('Get deploy error', { error: error.message });
      res.status(500).json({ error: error.message });
    }
  }

  async handleGovernanceStatus(req, res) {
    try {
      const status = {
        semanticAnchor: this.glCore.getSemanticAnchor(),
        rules: this.glCore.getGovernanceRules().length,
        policies: this.policyEngine.getPolicies().length,
        schemas: this.policyEngine.getSchemas().length,
        status: 'operational'
      };
      res.json({ success: true, status });
    } catch (error) {
      logger.error('Governance status error', { error: error.message });
      res.status(500).json({ error: error.message });
    }
  }

  async handleGetRules(req, res) {
    try {
      const rules = this.glCore.getGovernanceRules();
      res.json({ success: true, rules });
    } catch (error) {
      logger.error('Get rules error', { error: error.message });
      res.status(500).json({ error: error.message });
    }
  }

  async handleGetPolicies(req, res) {
    try {
      const policies = this.policyEngine.getPolicies();
      res.json({ success: true, policies });
    } catch (error) {
      logger.error('Get policies error', { error: error.message });
      res.status(500).json({ error: error.message });
    }
  }

  async handleSandboxExecute(req, res) {
    try {
      const { file, operations } = req.body;
      const result = await this.sandbox.executeInSandbox(file, operations);
      res.json({ success: true, result });
    } catch (error) {
      logger.error('Sandbox execution error', { error: error.message });
      res.status(500).json({ error: error.message });
    }
  }

  async handleGitStatus(req, res) {
    try {
      const status = await this.gitConnector.getStatus();
      res.json({ success: true, status });
    } catch (error) {
      logger.error('Git status error', { error: error.message });
      res.status(500).json({ error: error.message });
    }
  }

  async handleGitCommit(req, res) {
    try {
      const { message, files } = req.body;
      const result = await this.gitConnector.commitChanges(message, files);
      res.json({ success: true, result });
    } catch (error) {
      logger.error('Git commit error', { error: error.message });
      res.status(500).json({ error: error.message });
    }
  }

  async handleStatus(req, res) {
    try {
      const status = await this.engine.handleStatus(req, res);
    } catch (error) {
      logger.error('Status error', { error: error.message });
      res.status(500).json({ error: error.message });
    }
  }

  async handleEvents(req, res) {
    try {
      const events = await this.engine.handleEvents(req, res);
    } catch (error) {
      logger.error('Events error', { error: error.message });
      res.status(500).json({ error: error.message });
    }
  }

  start(port = 8080) {
    this.app.listen(port, () => {
      logger.info(`REST API server started on port ${port}`);
    });
  }
}

module.exports = RestAPI;
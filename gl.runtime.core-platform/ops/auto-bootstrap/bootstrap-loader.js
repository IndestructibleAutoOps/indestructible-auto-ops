// @GL-governed
// @GL-layer: GL70-89
// @GL-semantic: runtime-behavior-implementation
// @GL-charter-version: 2.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

// GL-ROOT Global Governance Audit & Platform Build
// Unified Charter v2.0.0 - Bootstrap Loader

const fs = require('fs').promises;
const path = require('path');
const yaml = require('js-yaml');
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: '../../storage/gl-events-stream/bootstrap-loader.log' }),
    new winston.transports.Console()
  ]
});

class BootstrapLoader {
  constructor() {
    this.configDir = path.join(__dirname);
    this.autoStarters = new Map();
    this.status = 'idle';
  }

  async loadAll() {
    try {
      logger.info('Loading all auto-bootstrap configurations...');
      
      const files = await fs.readdir(this.configDir);
      const yamlFiles = files.filter(f => f.startsWith('auto-') && f.endsWith('.yaml'));
      
      logger.info(`Found ${yamlFiles.length} auto-bootstrap configuration files`);
      
      for (const file of yamlFiles) {
        await this.loadConfig(file);
      }
      
      this.status = 'loaded';
      logger.info(`Successfully loaded ${this.autoStarters.size} auto-starters`);
      
      return {
        success: true,
        loaded: this.autoStarters.size,
        starters: Array.from(this.autoStarters.keys())
      };
      
    } catch (error) {
      logger.error('Failed to load auto-bootstrap configurations', { error: error.message });
      throw error;
    }
  }

  async loadConfig(filename) {
    try {
      const filePath = path.join(this.configDir, filename);
      const content = await fs.readFile(filePath, 'utf8');
      const config = yaml.load(content);
      
      const starterName = filename.replace('.yaml', '');
      this.autoStarters.set(starterName, config);
      
      logger.info(`Loaded auto-starter: ${starterName}`, {
        kind: config.kind,
        enabled: config.spec?.enabled,
        version: config.metadata?.version
      });
      
      return config;
      
    } catch (error) {
      logger.error(`Failed to load configuration: ${filename}`, { error: error.message });
      throw error;
    }
  }

  async startAll() {
    try {
      logger.info('Starting all auto-starters...');
      
      const results = [];
      
      for (const [name, config] of this.autoStarters) {
        if (config.spec?.enabled !== false) {
          const result = await this.startStarter(name, config);
          results.push(result);
        }
      }
      
      this.status = 'running';
      logger.info(`Started ${results.filter(r => r.success).length} auto-starters`);
      
      return {
        success: true,
        started: results.filter(r => r.success).length,
        results
      };
      
    } catch (error) {
      logger.error('Failed to start auto-starters', { error: error.message });
      throw error;
    }
  }

  async startStarter(name, config) {
    try {
      logger.info(`Starting auto-starter: ${name}`);
      
      // Simulate starting the auto-starter
      // In production, this would actually trigger the orchestration engine
      
      const startTime = Date.now();
      
      // Log to event stream
      await this.logEvent('starter_started', {
        name,
        kind: config.kind,
        version: config.metadata?.version,
        layer: config.metadata?.layer
      });
      
      const duration = Date.now() - startTime;
      
      logger.info(`Successfully started auto-starter: ${name}`, { duration });
      
      return {
        success: true,
        name,
        duration,
        status: 'running'
      };
      
    } catch (error) {
      logger.error(`Failed to start auto-starter: ${name}`, { error: error.message });
      
      await this.logEvent('starter_failed', {
        name,
        error: error.message
      });
      
      return {
        success: false,
        name,
        error: error.message,
        status: 'failed'
      };
    }
  }

  async stopAll() {
    try {
      logger.info('Stopping all auto-starters...');
      
      for (const [name, config] of this.autoStarters) {
        await this.stopStarter(name);
      }
      
      this.status = 'stopped';
      logger.info('All auto-starters stopped');
      
      return {
        success: true,
        status: 'stopped'
      };
      
    } catch (error) {
      logger.error('Failed to stop auto-starters', { error: error.message });
      throw error;
    }
  }

  async stopStarter(name) {
    try {
      logger.info(`Stopping auto-starter: ${name}`);
      
      await this.logEvent('starter_stopped', { name });
      
      logger.info(`Successfully stopped auto-starter: ${name}`);
      
      return {
        success: true,
        name,
        status: 'stopped'
      };
      
    } catch (error) {
      logger.error(`Failed to stop auto-starter: ${name}`, { error: error.message });
      return {
        success: false,
        name,
        error: error.message,
        status: 'error'
      };
    }
  }

  async getStatus() {
    return {
      status: this.status,
      loaded: this.autoStarters.size,
      starters: Array.from(this.autoStarters.keys()).map(name => ({
        name,
        config: this.autoStarters.get(name),
        enabled: this.autoStarters.get(name).spec?.enabled !== false
      }))
    };
  }

  async logEvent(eventType, eventData) {
    try {
      const event = {
        id: `bootstrap-${Date.now()}`,
        type: eventType,
        timestamp: new Date().toISOString(),
        source: 'bootstrap-loader',
        data: eventData
      };
      
      const eventStreamPath = path.join(__dirname, '../../storage/gl-events-stream/bootstrap-events.jsonl');
      await fs.appendFile(eventStreamPath, JSON.stringify(event) + '\n');
      
    } catch (error) {
      logger.error('Failed to log event', { error: error.message });
    }
  }
}

// Export for use in other modules
module.exports = BootstrapLoader;

// If run directly, execute bootstrap loader
if (require.main === module) {
  const loader = new BootstrapLoader();
  
  loader.loadAll()
    .then(() => loader.startAll())
    .then(() => loader.getStatus())
    .then(status => {
      console.log('Bootstrap Loader Status:', JSON.stringify(status, null, 2));
      process.exit(0);
    })
    .catch(error => {
      console.error('Bootstrap Loader Error:', error);
      process.exit(1);
    });
}
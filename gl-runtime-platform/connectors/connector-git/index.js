// @GL-governed
// GL-ROOT Global Governance Audit & Platform Build
// Unified Charter v2.0.0 - Git Connector

const { exec } = require('child_process');
const { promisify } = require('util');
const fs = require('fs').promises;
const path = require('path');
const { v4: uuidv4 } = require('uuid');
const winston = require('winston');

const execAsync = promisify(exec);

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: '../../storage/gl-events-stream/git-connector.log' }),
    new winston.transports.Console()
  ]
});

class GitConnector {
  constructor(repoPath) {
    this.repoPath = repoPath;
    this.eventStream = [];
  }

  async scanRepository() {
    const scanId = uuidv4();
    logger.info('Repository scan started', { scanId, repoPath: this.repoPath });
    this.logEvent('repo_scan_started', { scanId, repoPath: this.repoPath });

    try {
      const files = await this.getAllFiles();
      const fileDetails = await Promise.all(
        files.map(file => this.getFileDetails(file))
      );

      const result = {
        scanId,
        repoPath: this.repoPath,
        filesScanned: files.length,
        fileDetails,
        completedAt: new Date().toISOString()
      };

      this.logEvent('repo_scan_completed', result);
      return result;
    } catch (error) {
      logger.error('Repository scan failed', { scanId, error: error.message });
      this.logEvent('repo_scan_failed', { scanId, error: error.message });
      throw error;
    }
  }

  async getAllFiles() {
    const { stdout } = await execAsync('find . -type f -not -path "./node_modules/*" -not -path "./.git/*"', {
      cwd: this.repoPath
    });
    
    return stdout.split('\n').filter(f => f.length > 0).map(f => f.replace(/^\.\//, ''));
  }

  async getFileDetails(filePath) {
    const fullPath = path.join(this.repoPath, filePath);
    const stats = await fs.stat(fullPath);
    
    try {
      const { stdout: logOutput } = await execAsync(`git log --oneline -n 1 "${filePath}"`, {
        cwd: this.repoPath
      });
      
      const { stdout: diffOutput } = await execAsync(`git diff HEAD "${filePath}"`, {
        cwd: this.repoPath
      });

      return {
        path: filePath,
        size: stats.size,
        modified: stats.mtime,
        lastCommit: logOutput.trim(),
        hasChanges: diffOutput.trim().length > 0
      };
    } catch (error) {
      return {
        path: filePath,
        size: stats.size,
        modified: stats.mtime,
        lastCommit: 'unknown',
        hasChanges: false,
        error: error.message
      };
    }
  }

  async getDiff(filePath) {
    try {
      const { stdout } = await execAsync(`git diff "${filePath}"`, {
        cwd: this.repoPath
      });
      
      return {
        path: filePath,
        diff: stdout,
        hasChanges: stdout.trim().length > 0
      };
    } catch (error) {
      throw new Error(`Failed to get diff for ${filePath}: ${error.message}`);
    }
  }

  async applyPatch(patchFile, filePath) {
    const patchId = uuidv4();
    logger.info('Patch application started', { patchId, patchFile, filePath });
    this.logEvent('patch_apply_started', { patchId, patchFile, filePath });

    try {
      await execAsync(`git apply "${patchFile}"`, {
        cwd: this.repoPath
      });

      const result = {
        patchId,
        patchFile,
        filePath,
        applied: true,
        appliedAt: new Date().toISOString()
      };

      this.logEvent('patch_applied', result);
      return result;
    } catch (error) {
      logger.error('Patch application failed', { patchId, error: error.message });
      this.logEvent('patch_apply_failed', { patchId, error: error.message });
      throw error;
    }
  }

  async commitChanges(message, files) {
    const commitId = uuidv4();
    logger.info('Commit started', { commitId, files });
    this.logEvent('commit_started', { commitId, files });

    try {
      // Stage files
      for (const file of files) {
        await execAsync(`git add "${file}"`, { cwd: this.repoPath });
      }

      // Commit
      const { stdout } = await execAsync(`git commit -m "${message}"`, {
        cwd: this.repoPath
      });

      const result = {
        commitId,
        message,
        files,
        commitHash: stdout.trim(),
        committedAt: new Date().toISOString()
      };

      this.logEvent('commit_completed', result);
      return result;
    } catch (error) {
      logger.error('Commit failed', { commitId, error: error.message });
      this.logEvent('commit_failed', { commitId, error: error.message });
      throw error;
    }
  }

  async pushChanges(branch = 'main') {
    const pushId = uuidv4();
    logger.info('Push started', { pushId, branch });
    this.logEvent('push_started', { pushId, branch });

    try {
      const { stdout } = await execAsync(`git push origin ${branch}`, {
        cwd: this.repoPath
      });

      const result = {
        pushId,
        branch,
        output: stdout,
        pushedAt: new Date().toISOString()
      };

      this.logEvent('push_completed', result);
      return result;
    } catch (error) {
      logger.error('Push failed', { pushId, error: error.message });
      this.logEvent('push_failed', { pushId, error: error.message });
      throw error;
    }
  }

  async getStatus() {
    try {
      const { stdout } = await execAsync('git status --porcelain', {
        cwd: this.repoPath
      });

      const files = stdout.split('\n').filter(f => f.length > 0).map(line => ({
        status: line.substring(0, 2),
        path: line.substring(3)
      }));

      return {
        status: 'success',
        files,
        hasChanges: files.length > 0
      };
    } catch (error) {
      return {
        status: 'error',
        error: error.message,
        files: [],
        hasChanges: false
      };
    }
  }

  logEvent(type, data) {
    const event = {
      id: uuidv4(),
      timestamp: new Date().toISOString(),
      type,
      data,
      source: 'git-connector'
    };
    this.eventStream.push(event);
    logger.info('Git connector event logged', event);

    fs.appendFile(
      path.join(__dirname, '../../storage/gl-events-stream/git-events.jsonl'),
      JSON.stringify(event) + '\n'
    ).catch(err => logger.error('Event stream write failed', { error: err.message }));
  }
}

module.exports = GitConnector;
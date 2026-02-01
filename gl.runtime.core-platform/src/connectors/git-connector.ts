// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: git-connector
// @GL-charter-version: 2.0.0

import simpleGit, { SimpleGit } from 'simple-git';
import path from 'path';
import fs from 'fs/promises';
import { createLogger } from '../utils/logger';
import { v4 as uuidv4 } from 'uuid';

const logger = createLogger('GitConnector');

export interface GitDiffResult {
  filePath: string;
  status: string;
  changes: string;
}

export interface GitPatch {
  id: string;
  filePath: string;
  originalContent: string;
  modifiedContent: string;
  patch: string;
}

export class GitConnector {
  private git: SimpleGit;
  private repoPath: string;

  constructor(repoPath?: string) {
    this.repoPath = repoPath || process.cwd();
    this.git = simpleGit(this.repoPath);
  }

  public async scanRepository(): Promise<string[]> {
    try {
      const status = await this.git.status();
      const files = [
        ...status.files.map((f: any) => f.path),
        ...status.staged,
        ...status.modified
      ];
      
      logger.info(`Scanned ${files.length} files in repository`);
      return Array.from(new Set(files));
    } catch (error: any) {
      logger.error(`Failed to scan repository: ${error.message}`);
      throw error;
    }
  }

  public async getDiff(filePath: string): Promise<GitDiffResult> {
    try {
      const diff = await this.git.diff([filePath]);
      
      const result: GitDiffResult = {
        filePath,
        status: 'modified',
        changes: diff
      };
      
      logger.info(`Generated diff for ${filePath}`);
      return result;
    } catch (error: any) {
      logger.error(`Failed to get diff for ${filePath}: ${error.message}`);
      throw error;
    }
  }

  public async createPatch(filePath: string, modifications: string): Promise<GitPatch> {
    try {
      const fullPath = path.join(this.repoPath, filePath);
      const originalContent = await fs.readFile(fullPath, 'utf-8');
      
      const patch: GitPatch = {
        id: uuidv4(),
        filePath,
        originalContent,
        modifiedContent: modifications,
        patch: this.generatePatchString(originalContent, modifications)
      };
      
      logger.info(`Created patch for ${filePath}`);
      return patch;
    } catch (error: any) {
      logger.error(`Failed to create patch for ${filePath}: ${error.message}`);
      throw error;
    }
  }

  private generatePatchString(original: string, modified: string): string {
    const originalLines = original.split('\n');
    const modifiedLines = modified.split('\n');
    
    let patch = `--- a/\n+++ b/\n`;
    
    // Simplified diff generation
    if (original !== modified) {
      patch += `@@ -1,${originalLines.length} +1,${modifiedLines.length} @@\n`;
      patch += originalLines.map(line => `- ${line}`).join('\n') + '\n';
      patch += modifiedLines.map(line => `+ ${line}`).join('\n');
    }
    
    return patch;
  }

  public async applyPatch(patch: GitPatch): Promise<void> {
    try {
      const fullPath = path.join(this.repoPath, patch.filePath);
      await fs.writeFile(fullPath, patch.modifiedContent, 'utf-8');
      
      logger.info(`Applied patch to ${patch.filePath}`);
    } catch (error: any) {
      logger.error(`Failed to apply patch: ${error.message}`);
      throw error;
    }
  }

  public async add(filePath: string): Promise<void> {
    try {
      await this.git.add(filePath);
      logger.info(`Staged file: ${filePath}`);
    } catch (error: any) {
      logger.error(`Failed to stage file ${filePath}: ${error.message}`);
      throw error;
    }
  }

  public async commit(message: string): Promise<string> {
    try {
      const result = await this.git.commit(message);
      logger.info(`Committed changes: ${result.commit}`);
      return result.commit;
    } catch (error: any) {
      logger.error(`Failed to commit: ${error.message}`);
      throw error;
    }
  }

  public async push(branch: string = 'main'): Promise<void> {
    try {
      await this.git.push('origin', branch);
      logger.info(`Pushed to origin/${branch}`);
    } catch (error: any) {
      logger.error(`Failed to push: ${error.message}`);
      throw error;
    }
  }

  public async createBranch(branchName: string): Promise<void> {
    try {
      await this.git.checkoutLocalBranch(branchName);
      logger.info(`Created branch: ${branchName}`);
    } catch (error: any) {
      logger.error(`Failed to create branch: ${error.message}`);
      throw error;
    }
  }

  public async getStatus(): Promise<any> {
    try {
      const status = await this.git.status();
      return status;
    } catch (error: any) {
      logger.error(`Failed to get status: ${error.message}`);
      throw error;
    }
  }
}
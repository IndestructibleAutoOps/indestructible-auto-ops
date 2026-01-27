/**
 * PR Bot - 自動處理 PR 的 CI 失敗分類
 */

import { CIFailAutoClassificationSystem } from './index.js';
import { PRDiff, CIFailure } from './types.js';
import * as https from 'https';

export interface GitHubAPIConfig {
  token: string;
  owner: string;
  repo: string;
}

interface GitHubPR {
  number: number;
  title: string;
  user: { login: string };
  base: { ref: string };
  head: { ref: string };
  created_at: string;
}

interface GitHubFile {
  filename: string;
  status: string;
  additions: number;
  deletions: number;
}

interface GitHubWorkflowRun {
  id: string;
  name: string;
  run_number: number;
  updated_at: string;
  conclusion: string | null;
}

export class PRBot {
  private apiConfig: GitHubAPIConfig;
  private classificationSystem: CIFailAutoClassificationSystem;

  constructor(apiConfig: GitHubAPIConfig) {
    this.apiConfig = apiConfig;
    this.classificationSystem = new CIFailAutoClassificationSystem({
      enableLLMJudgment: true,
      enableAutoRerun: true,
      enableAutoLabeling: true,
      enableAutoComment: true
    });
  }

  /**
   * 處理 PR 的 CI 失敗
   */
  public async handlePRCIFailure(prNumber: number, workflowRunId: string): Promise<void> {
    console.log(`Processing PR #${prNumber} CI failure...`);

    try {
      // 1. 獲取 PR 信息
      const prDiff = await this.getPRDiff(prNumber);

      // 2. 獲取 CI 失敗信息
      const ciFailure = await this.getCIFailure(workflowRunId);

      // 3. 執行分類
      const result = await this.classificationSystem.classify(prDiff, ciFailure);

      // 4. 發布評論
      if (this.classificationSystem.getConfig().enableAutoComment) {
        await this.postComment(prNumber, result.prComment);
      }

      // 5. 添加標籤
      if (this.classificationSystem.getConfig().enableAutoLabeling) {
        await this.addLabels(prNumber, result.labels);
      }

      // 6. 執行自動重跑（如果需要）
      if (result.rerunStrategy?.shouldRerun && this.classificationSystem.getConfig().enableAutoRerun) {
        await this.rerunWorkflow(workflowRunId);
      }

      console.log(`✅ Successfully processed PR #${prNumber}`);
    } catch (error) {
      console.error(`❌ Error processing PR #${prNumber}:`, error);
      throw error;
    }
  }

  /**
   * 獲取 PR Diff
   */
  private async getPRDiff(prNumber: number): Promise<PRDiff> {
    const url = `/repos/${this.apiConfig.owner}/${this.apiConfig.repo}/pulls/${prNumber}`;

    const response = await this.githubRequest(url);
    const pr = response as GitHubPR;

    // 獲取變更的文件
    const filesUrl = `/repos/${this.apiConfig.owner}/${this.apiConfig.repo}/pulls/${prNumber}/files`;
    const files = await this.githubRequest(filesUrl) as GitHubFile[];

    const changedFiles = files.map((f: GitHubFile) => f.filename);
    const changedModules = [...new Set(changedFiles.map((f: string) => f.split('/')[0]))];

    return {
      prNumber: pr.number,
      title: pr.title,
      author: pr.user.login,
      baseBranch: pr.base.ref,
      headBranch: pr.head.ref,
      changedFiles,
      changedLines: files.map((f: GitHubFile) => ({
        file: f.filename,
        added: typeof f.additions === 'number' ? f.additions : 0,
        removed: typeof f.deletions === 'number' ? f.deletions : 0
      })),
      changedModules,
      timestamp: new Date(pr.created_at).getTime()
    };
  }

  /**
   * 獲取 CI 失敗信息
   */
  private async getCIFailure(workflowRunId: string): Promise<CIFailure> {
    const url = `/repos/${this.apiConfig.owner}/${this.apiConfig.repo}/actions/runs/${workflowRunId}`;
    const workflowRun = await this.githubRequest(url) as GitHubWorkflowRun;

    return {
      workflowName: workflowRun.name,
      workflowId: workflowRun.id.toString(),
      jobName: 'unknown',  // 需要從 jobs API 獲取
      stepName: 'unknown',  // 需要從 logs 獲取
      failureMessage: workflowRun.conclusion || 'Workflow failed',
      failureLog: 'Check workflow logs for details',
      failedFiles: [],
      failedLines: [],
      timestamp: new Date(workflowRun.updated_at).getTime(),
      runNumber: workflowRun.run_number,
      runId: workflowRun.id.toString()
    };
  }

  /**
   * 發布評論
   */
  private async postComment(prNumber: number, comment: string): Promise<void> {
    const url = `/repos/${this.apiConfig.owner}/${this.apiConfig.repo}/issues/${prNumber}/comments`;

    await this.githubRequest(url, 'POST', {
      body: comment
    });

    console.log(`📝 Posted comment to PR #${prNumber}`);
  }

  /**
   * 添加標籤
   */
  private async addLabels(prNumber: number, labels: string[]): Promise<void> {
    if (labels.length === 0) return;

    const url = `/repos/${this.apiConfig.owner}/${this.apiConfig.repo}/issues/${prNumber}/labels`;

    await this.githubRequest(url, 'POST', {
      labels
    });

    console.log(`🏷️ Added labels to PR #${prNumber}: ${labels.join(', ')}`);
  }

  /**
   * 重跑 Workflow
   */
  private async rerunWorkflow(workflowRunId: string): Promise<void> {
    const url = `/repos/${this.apiConfig.owner}/${this.apiConfig.repo}/actions/runs/${workflowRunId}/rerun`;

    await this.githubRequest(url, 'POST');

    console.log(`🔄 Rerun workflow #${workflowRunId}`);
  }

  /**
   * GitHub API 請求
   */
  private async githubRequest(
    path: string,
    method: string = 'GET',
    body?: unknown
  ): Promise<unknown> {
    const options: https.RequestOptions = {
      hostname: 'api.github.com',
      path: path,
      method: method,
      headers: {
        'Authorization': `Bearer ${this.apiConfig.token}`,
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'CI-Fail-Classifier-Bot'
      }
    };

    return new Promise((resolve, reject) => {
      const req = https.request(options, (res) => {
        let data = '';

        res.on('data', (chunk) => {
          data += chunk;
        });

        res.on('end', () => {
          if (res.statusCode && res.statusCode >= 200 && res.statusCode < 300) {
            try {
              resolve(JSON.parse(data));
            } catch {
              resolve(data);
            }
          } else {
            reject(new Error(`GitHub API error: ${res.statusCode} - ${data}`));
          }
        });
      });

      req.on('error', reject);

      if (body) {
        req.write(JSON.stringify(body));
      }

      req.end();
    });
  }

  /**
   * 批量處理多個 PR
   */
  public async batchHandlePRs(prNumbers: number[], workflowRunId: string): Promise<void> {
    const results = await Promise.allSettled(
      prNumbers.map(prNumber => this.handlePRCIFailure(prNumber, workflowRunId))
    );

    const successful = results.filter(r => r.status === 'fulfilled').length;
    const failed = results.filter(r => r.status === 'rejected').length;

    console.log(`\n📊 Batch processing complete:`);
    console.log(`✅ Successful: ${successful}`);
    console.log(`❌ Failed: ${failed}`);
  }
}

/**
 * 創建 PR Bot 實例
 */
export function createPRBot(apiConfig: GitHubAPIConfig): PRBot {
  return new PRBot(apiConfig);
}
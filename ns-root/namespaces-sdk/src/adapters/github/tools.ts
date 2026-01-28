// @GL-governed
// @GL-layer: GL-L6-NAMESPACE
// @GL-semantic: governance-layer-namespace
// @GL-revision: 1.0.0
// @GL-status: active

/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-sdk/src/adapters/github
 * @gl-semantic-anchor GL-00-ADAPTERS_GITHUB_TOOLS
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * GitHub Tool Wrappers
 *
 * Implements individual tool wrappers for GitHub operations.
 */

import { Tool, ToolMetadata, ToolContext, ToolDescriptor } from '../../core/tool';
import { CredentialManager } from '../../credentials/manager';
import { GitHubAdapterConfig } from './index';

/**
 * Base GitHub tool class
 */
abstract class GitHubTool extends Tool {
  protected credentialManager: CredentialManager;
  protected config: GitHubAdapterConfig;

  constructor(
    metadata: ToolMetadata,
    credentialManager: CredentialManager,
    config: GitHubAdapterConfig
  ) {
    super(metadata);
    this.credentialManager = credentialManager;
    this.config = config;
  }

  /**
   * Get authenticated GitHub client
   */
  protected async getClient(): Promise<unknown> {
    const credential = await this.credentialManager.getCredential('github');
    // In real implementation, return Octokit client
    return { credential };
  }
}

/**
 * GitHub Create Issue Tool
 */
class GitHubCreateIssueTool extends GitHubTool {
  getInputSchema(): unknown {
    return {
      type: 'object',
      properties: {
        repository: { type: 'string', description: 'Repository name (owner/repo)' },
        title: { type: 'string', description: 'Issue title' },
        body: { type: 'string', description: 'Issue body' },
        labels: { type: 'array', items: { type: 'string' }, description: 'Issue labels' }
      },
      required: ['repository', 'title']
    };
  }

  override getOutputSchema(): unknown {
    return {
      type: 'object',
      properties: {
        issue_number: { type: 'number' },
        url: { type: 'string' }
      }
    };
  }

  async invoke(input: unknown, context: ToolContext): Promise<unknown> {
    await this.getClient();
    // Implementation would use GitHub API
    return {
      issue_number: 123,
      url: `https://github.com/${input.repository}/issues/123`
    };
  }
}

/**
 * GitHub List Repositories Tool
 */
class GitHubListReposTool extends GitHubTool {
  getInputSchema(): unknown {
    return {
      type: 'object',
      properties: {
        owner: { type: 'string', description: 'Repository owner' },
        limit: { type: 'number', description: 'Maximum number of repos to return' }
      },
      required: ['owner']
    };
  }

  override getOutputSchema(): unknown {
    return {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          name: { type: 'string' },
          full_name: { type: 'string' },
          url: { type: 'string' }
        }
      }
    };
  }

  async invoke(input: unknown, context: ToolContext): Promise<unknown> {
    await this.getClient();
    // Implementation would use GitHub API
    return [
      { name: 'repo1', full_name: 'owner/repo1', url: 'https://github.com/owner/repo1' }
    ];
  }
}

/**
 * GitHub Create Pull Request Tool
 */
class GitHubCreatePRTool extends GitHubTool {
  getInputSchema(): unknown {
    return {
      type: 'object',
      properties: {
        repository: { type: 'string', description: 'Repository name (owner/repo)' },
        title: { type: 'string', description: 'Pull request title' },
        body: { type: 'string', description: 'Pull request body' },
        head: { type: 'string', description: 'Head branch' },
        base: { type: 'string', description: 'Base branch' }
      },
      required: ['repository', 'title', 'head', 'base']
    };
  }

  override getOutputSchema(): unknown {
    return {
      type: 'object',
      properties: {
        number: { type: 'number' },
        url: { type: 'string' },
        state: { type: 'string' }
      }
    };
  }

  async invoke(input: unknown, context: ToolContext): Promise<unknown> {
    await this.getClient();
    // Implementation would use GitHub API
    return {
      number: 1,
      url: `https://github.com/${input.repository}/pull/1`,
      state: 'open'
    };
  }
}

/**
 * GitHub Get File Tool
 */
class GitHubGetFileTool extends GitHubTool {
  getInputSchema(): unknown {
    return {
      type: 'object',
      properties: {
        repository: { type: 'string', description: 'Repository name (owner/repo)' },
        path: { type: 'string', description: 'File path' },
        ref: { type: 'string', description: 'Git reference (branch, tag, or commit)' }
      },
      required: ['repository', 'path']
    };
  }

  override getOutputSchema(): unknown {
    return {
      type: 'object',
      properties: {
        content: { type: 'string' },
        encoding: { type: 'string' },
        sha: { type: 'string' }
      }
    };
  }

  async invoke(input: unknown, context: ToolContext): Promise<unknown> {
    await this.getClient();
    // Implementation would use GitHub API
    return {
      content: 'file content',
      encoding: 'utf-8',
      sha: 'abc123'
    };
  }
}

/**
 * GitHub Commit File Tool
 */
class GitHubCommitFileTool extends GitHubTool {
  getInputSchema(): unknown {
    return {
      type: 'object',
      properties: {
        repository: { type: 'string', description: 'Repository name (owner/repo)' },
        path: { type: 'string', description: 'File path' },
        content: { type: 'string', description: 'File content' },
        message: { type: 'string', description: 'Commit message' },
        branch: { type: 'string', description: 'Branch name' },
        sha: { type: 'string', description: 'File SHA for updates' }
      },
      required: ['repository', 'path', 'content', 'message', 'branch']
    };
  }

  override getOutputSchema(): unknown {
    return {
      type: 'object',
      properties: {
        content: { type: 'object' },
        commit: { type: 'object' }
      }
    };
  }

  async invoke(input: unknown, context: ToolContext): Promise<unknown> {
    await this.getClient();
    // Implementation would use GitHub API
    return {
      content: { sha: 'newsha123' },
      commit: { sha: 'commitsha123' }
    };
  }
}

/**
 * Tool descriptor factory functions
 */
export function createGitHubCreateIssueTool(
  credentialManager: CredentialManager,
  config: GitHubAdapterConfig
): ToolDescriptor {
  const metadata: ToolMetadata = {
    name: 'github_create_issue',
    title: 'GitHub Create Issue',
    description: 'Create a GitHub issue',
    version: '1.0.0'
  };
  
  const tool = new GitHubCreateIssueTool(metadata, credentialManager, config);
  
  return {
    metadata: tool.getMetadata(),
    factory: {
      createTool: () => new GitHubCreateIssueTool(metadata, credentialManager, config),
      getToolMetadata: () => metadata
    },
    inputSchema: tool.getInputSchema(),
    outputSchema: tool.getOutputSchema()
  };
}

export function createGitHubListReposTool(
  credentialManager: CredentialManager,
  config: GitHubAdapterConfig
): ToolDescriptor {
  const metadata: ToolMetadata = {
    name: 'github_list_repos',
    title: 'GitHub List Repositories',
    description: 'List GitHub repositories',
    version: '1.0.0'
  };
  
  const tool = new GitHubListReposTool(metadata, credentialManager, config);
  
  return {
    metadata: tool.getMetadata(),
    factory: {
      createTool: () => new GitHubListReposTool(metadata, credentialManager, config),
      getToolMetadata: () => metadata
    },
    inputSchema: tool.getInputSchema(),
    outputSchema: tool.getOutputSchema()
  };
}

export function createGitHubCreatePRTool(
  credentialManager: CredentialManager,
  config: GitHubAdapterConfig
): ToolDescriptor {
  const metadata: ToolMetadata = {
    name: 'github_create_pr',
    title: 'GitHub Create Pull Request',
    description: 'Create a GitHub pull request',
    version: '1.0.0'
  };
  
  const tool = new GitHubCreatePRTool(metadata, credentialManager, config);
  
  return {
    metadata: tool.getMetadata(),
    factory: {
      createTool: () => new GitHubCreatePRTool(metadata, credentialManager, config),
      getToolMetadata: () => metadata
    },
    inputSchema: tool.getInputSchema(),
    outputSchema: tool.getOutputSchema()
  };
}

export function createGitHubGetFileTool(
  credentialManager: CredentialManager,
  config: GitHubAdapterConfig
): ToolDescriptor {
  const metadata: ToolMetadata = {
    name: 'github_get_file',
    title: 'GitHub Get File',
    description: 'Get a file from GitHub repository',
    version: '1.0.0'
  };
  
  const tool = new GitHubGetFileTool(metadata, credentialManager, config);
  
  return {
    metadata: tool.getMetadata(),
    factory: {
      createTool: () => new GitHubGetFileTool(metadata, credentialManager, config),
      getToolMetadata: () => metadata
    },
    inputSchema: tool.getInputSchema(),
    outputSchema: tool.getOutputSchema()
  };
}

export function createGitHubCommitFileTool(
  credentialManager: CredentialManager,
  config: GitHubAdapterConfig
): ToolDescriptor {
  const metadata: ToolMetadata = {
    name: 'github_commit_file',
    title: 'GitHub Commit File',
    description: 'Commit a file to GitHub repository',
    version: '1.0.0'
  };
  
  const tool = new GitHubCommitFileTool(metadata, credentialManager, config);
  
  return {
    metadata: tool.getMetadata(),
    factory: {
      createTool: () => new GitHubCommitFileTool(metadata, credentialManager, config),
      getToolMetadata: () => metadata
    },
    inputSchema: tool.getInputSchema(),
    outputSchema: tool.getOutputSchema()
  };
}

/**
 * Export all tool factories
 */
export const githubTools = [
  createGitHubCreateIssueTool,
  createGitHubListReposTool,
  createGitHubCreatePRTool,
  createGitHubGetFileTool,
  createGitHubCommitFileTool
];

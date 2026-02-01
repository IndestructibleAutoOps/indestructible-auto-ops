// @GL-governed
// @GL-layer: GL100-119
// @GL-semantic: code-intelligence-deployment-weaver
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

/**
 * GL Code Intelligence & Security Layer - Deployment Weaver
 * Version 21.0.0
 * CLI/IDE/Web/CI/CD Integration - 部署編織器
 */

import { GeneratedCapability } from '../generator-engine';
import { EvaluationResult } from '../evaluation-engine';
import { v4 as uuidv4 } from 'uuid';

// ============================================================================
// Deployment Weaver Core Types
// ============================================================================

export interface DeploymentWeaverConfig {
  outputDirectory: string;
  generateCLI: boolean;
  generateIDEPlugins: boolean;
  generateWebConsole: boolean;
  generateCICDIntegrations: boolean;
  formats: DeploymentFormat[];
}

export type DeploymentFormat = 
  | 'cli'
  | 'vscode'
  | 'web'
  | 'cicd'
  | 'docker'
  | 'kubernetes';

export interface DeploymentRequest {
  id: string;
  generatedCapabilities: GeneratedCapability[];
  evaluationResults: Map<string, EvaluationResult>;
  deploymentTargets: DeploymentTarget[];
  options: DeploymentOptions;
  timestamp: number;
}

export interface DeploymentTarget {
  type: DeploymentFormat;
  config: Record<string, any>;
}

export interface DeploymentOptions {
  includeTests: boolean;
  includeDocs: boolean;
  minConfidenceScore: number;
  optimizeForProduction: boolean;
}

export interface DeploymentResult {
  id: string;
  requestId: string;
  success: boolean;
  deployedArtifacts: DeployedArtifact[];
  deploymentMetadata: DeploymentMetadata;
  errors: string[];
  warnings: string[];
  timestamp: number;
}

export interface DeployedArtifact {
  id: string;
  type: DeploymentFormat;
  path: string;
  content: string;
  metadata: Record<string, any>;
}

export interface DeploymentMetadata {
  deployedAt: number;
  capabilitiesDeployed: number;
  targetPlatforms: string[];
  version: string;
  checksums: Record<string, string>;
}

// ============================================================================
// Deployment Weaver Core
// ============================================================================

export class DeploymentWeaver {
  private config: DeploymentWeaverConfig;

  constructor(config?: Partial<DeploymentWeaverConfig>) {
    this.config = {
      outputDirectory: './deployed',
      generateCLI: true,
      generateIDEPlugins: true,
      generateWebConsole: true,
      generateCICDIntegrations: true,
      formats: ['cli', 'vscode', 'web', 'cicd'],
      ...config
    };
  }

  /**
   * Deploy capabilities to all specified targets
   */
  public async deploy(request: DeploymentRequest): Promise<DeploymentResult> {
    const startTime = Date.now();
    const artifacts: DeployedArtifact[] = [];
    const errors: string[] = [];
    const warnings: string[] = [];

    // Validate request
    if (!this.validateRequest(request, errors, warnings)) {
      return {
        id: uuidv4(),
        requestId: request.id,
        success: false,
        deployedArtifacts: [],
        deploymentMetadata: this.createDeploymentMetadata(artifacts),
        errors,
        warnings,
        timestamp: Date.now()
      };
    }

    // Deploy to each target
    for (const target of request.deploymentTargets) {
      try {
        const targetArtifacts = await this.deployToTarget(
          target,
          request.generatedCapabilities,
          request.evaluationResults,
          request.options
        );
        artifacts.push(...targetArtifacts);
      } catch (error: any) {
        errors.push(`Failed to deploy to ${target.type}: ${error.message}`);
      }
    }

    const deploymentTime = Date.now() - startTime;

    return {
      id: uuidv4(),
      requestId: request.id,
      success: errors.length === 0,
      deployedArtifacts: artifacts,
      deploymentMetadata: this.createDeploymentMetadata(artifacts, deploymentTime),
      errors,
      warnings,
      timestamp: Date.now()
    };
  }

  /**
   * Deploy to specific target
   */
  private async deployToTarget(
    target: DeploymentTarget,
    capabilities: GeneratedCapability[],
    evaluationResults: Map<string, EvaluationResult>,
    options: DeploymentOptions
  ): Promise<DeployedArtifact[]> {
    const artifacts: DeployedArtifact[] = [];

    switch (target.type) {
      case 'cli':
        artifacts.push(...await this.generateCLI(target, capabilities, options));
        break;

      case 'vscode':
        artifacts.push(...await this.generateVSCodePlugin(target, capabilities, options));
        break;

      case 'web':
        artifacts.push(...await this.generateWebConsole(target, capabilities, options));
        break;

      case 'cicd':
        artifacts.push(...await this.generateCICDIntegration(target, capabilities, options));
        break;

      case 'docker':
        artifacts.push(...await this.generateDockerConfig(target, capabilities, options));
        break;

      case 'kubernetes':
        artifacts.push(...await this.generateKubernetesConfig(target, capabilities, options));
        break;

      default:
        throw new Error(`Unsupported deployment target: ${target.type}`);
    }

    return artifacts;
  }

  /**
   * Generate CLI deployment
   */
  private async generateCLI(
    target: DeploymentTarget,
    capabilities: GeneratedCapability[],
    options: DeploymentOptions
  ): Promise<DeployedArtifact[]> {
    const artifacts: DeployedArtifact[] = [];

    // Generate main CLI entry point
    const cliCode = this.generateCLICode(capabilities);
    artifacts.push({
      id: uuidv4(),
      type: 'cli',
      path: 'cli/index.js',
      content: cliCode,
      metadata: { name: 'CLI Entry Point' }
    });

    // Generate package.json
    const packageJson = this.generateCLIPackageJson(capabilities);
    artifacts.push({
      id: uuidv4(),
      type: 'cli',
      path: 'cli/package.json',
      content: JSON.stringify(packageJson, null, 2),
      metadata: { name: 'CLI Package Configuration' }
    });

    // Generate README
    const readme = this.generateCLIReadme(capabilities);
    artifacts.push({
      id: uuidv4(),
      type: 'cli',
      path: 'cli/README.md',
      content: readme,
      metadata: { name: 'CLI Documentation' }
    });

    return artifacts;
  }

  /**
   * Generate CLI code
   */
  private generateCLICode(capabilities: GeneratedCapability[]): string {
    return `#!/usr/bin/env node

/**
 * GL Code Intelligence CLI
 * Auto-generated by Deployment Weaver
 */

const { program } = require('commander');
const path = require('path');

program
  .name('gl-code-intel')
  .description('GL Code Intelligence & Security CLI')
  .version('21.0.0');

${capabilities.map(cap => this.generateCLICommand(cap)).join('\n')}

program.parse(process.argv);
`;
  }

  /**
   * Generate CLI command
   */
  private generateCLICommand(capability: GeneratedCapability): string {
    return `
program
  .command('${capability.type}')
  .description('Execute ${capability.type}')
  .option('-i, --input <path>', 'Input file or directory')
  .option('-o, --output <path>', 'Output directory')
  .option('-f, --format <format>', 'Output format (json|yaml|sarif)')
  .action(async (options) => {
    const handler = require('./handlers/${capability.type}');
    await handler.execute(options);
  });
`;
  }

  /**
   * Generate CLI package.json
   */
  private generateCLIPackageJson(capabilities: GeneratedCapability[]): any {
    return {
      name: 'gl-code-intel-cli',
      version: '21.0.0',
      description: 'GL Code Intelligence & Security CLI',
      main: 'index.js',
      bin: {
        'gl-code-intel': './index.js'
      },
      scripts: {
        test: 'jest',
        lint: 'eslint .'
      },
      dependencies: {
        commander: '^11.0.0',
        chalk: '^4.1.2',
        ora: '^5.4.1'
      },
      devDependencies: {
        '@types/node': '^20.0.0',
        typescript: '^5.0.0',
        jest: '^29.0.0',
        eslint: '^8.0.0'
      }
    };
  }

  /**
   * Generate CLI README
   */
  private generateCLIReadme(capabilities: GeneratedCapability[]): string {
    return `# GL Code Intelligence CLI

Auto-generated CLI for GL Code Intelligence & Security capabilities.

## Installation

\`\`\`bash
npm install -g gl-code-intel-cli
\`\`\`

## Available Commands

${capabilities.map(cap => {
  return `
### ${cap.type}

\`\`\`bash
gl-code-intel ${cap.type} [options]
\`\`\`

**Options:**
- \`-i, --input <path>\`: Input file or directory
- \`-o, --output <path>\`: Output directory
- \`-f, --format <format>\`: Output format (json|yaml|sarif)
`;
}).join('\n')}

## Examples

\`\`\`bash
# Analyze code deeply
gl-code-intel deep-code-understanding -i ./src -o ./output

# Harden security
gl-code-intel security-hardening -i ./src -o ./hardened

# Optimize performance
gl-code-intel performance-optimization -i ./src -o ./optimized
\`\`\`
`;
  }

  /**
   * Generate VSCode plugin
   */
  private async generateVSCodePlugin(
    target: DeploymentTarget,
    capabilities: GeneratedCapability[],
    options: DeploymentOptions
  ): Promise<DeployedArtifact[]> {
    const artifacts: DeployedArtifact[] = [];

    // Generate extension manifest
    const manifest = this.generateVSCodeManifest(capabilities);
    artifacts.push({
      id: uuidv4(),
      type: 'vscode',
      path: 'vscode/package.json',
      content: JSON.stringify(manifest, null, 2),
      metadata: { name: 'VSCode Extension Manifest' }
    });

    // Generate extension code
    const extensionCode = this.generateVSCodeExtensionCode(capabilities);
    artifacts.push({
      id: uuidv4(),
      type: 'vscode',
      path: 'vscode/extension.ts',
      content: extensionCode,
      metadata: { name: 'VSCode Extension Code' }
    });

    // Generate README
    const readme = this.generateVSCodeReadme(capabilities);
    artifacts.push({
      id: uuidv4(),
      type: 'vscode',
      path: 'vscode/README.md',
      content: readme,
      metadata: { name: 'VSCode Extension Documentation' }
    });

    return artifacts;
  }

  /**
   * Generate VSCode manifest
   */
  private generateVSCodeManifest(capabilities: GeneratedCapability[]): any {
    return {
      name: 'gl-code-intel-vscode',
      displayName: 'GL Code Intelligence',
      description: 'GL Code Intelligence & Security capabilities in VSCode',
      version: '21.0.0',
      publisher: 'gl-intelligence',
      engines: {
        vscode: '^1.80.0'
      },
      categories: ['Linters', 'Formatters', 'Other'],
      activationEvents: [
        'onLanguage:typescript',
        'onLanguage:javascript',
        'onLanguage:python'
      ],
      contributes: {
        commands: capabilities.map(cap => ({
          command: `glCodeIntel.${cap.type}`,
          title: `GL Code Intel: ${cap.type}`
        })),
        keybindings: capabilities.map(cap => ({
          command: `glCodeIntel.${cap.type}`,
          key: 'ctrl+shift+g',
          mac: 'cmd+shift+g'
        }))
      },
      main: './out/extension.js',
      scripts: {
        compile: 'tsc -p ./',
        watch: 'tsc -watch -p ./'
      },
      devDependencies: {
        '@types/vscode': '^1.80.0',
        'typescript': '^5.0.0'
      }
    };
  }

  /**
   * Generate VSCode extension code
   */
  private generateVSCodeExtensionCode(capabilities: GeneratedCapability[]): string {
    return `import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
  console.log('GL Code Intelligence extension is now active');

  ${capabilities.map(cap => this.generateVSCodeCommand(cap)).join('\n\n')}
}

export function deactivate() {
  console.log('GL Code Intelligence extension is now deactivated');
}

${capabilities.map(cap => this.generateVSCodeCommandHandler(cap)).join('\n\n')}
`;
  }

  /**
   * Generate VSCode command
   */
  private generateVSCodeCommand(capability: GeneratedCapability): string {
    return `
const ${capability.type}Command = vscode.commands.registerCommand(
  'glCodeIntel.${capability.type}',
  async () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showErrorMessage('No active editor found');
      return;
    }

    const document = editor.document;
    const selection = editor.selection;
    const code = document.getText(selection) || document.getText();

    vscode.window.withProgress({
      location: vscode.ProgressLocation.Notification,
      title: \`Running ${capability.type}...\`,
      cancellable: false
    }, async (progress) => {
      try {
        // Execute capability
        progress.report({ increment: 50, message: 'Processing...' });
        
        // TODO: Integrate with actual capability execution
        const result = await execute${capability.type.charAt(0).toUpperCase() + capability.type.slice(1)}(code);
        
        progress.report({ increment: 50, message: 'Complete!' });
        
        // Show results
        vscode.window.showInformationMessage(\`${capability.type} completed successfully\`);
      } catch (error: any) {
        vscode.window.showErrorMessage(\`${capability.type} failed: \${error.message}\`);
      }
    });
  }
);

context.subscriptions.push(${capability.type}Command);
`;
  }

  /**
   * Generate VSCode command handler
   */
  private generateVSCodeCommandHandler(capability: GeneratedCapability): string {
    return `
async function execute${capability.type.charAt(0).toUpperCase() + capability.type.slice(1)}(code: string): Promise<any> {
  // TODO: Implement actual capability execution
  // This would integrate with the Generator Engine and Evaluation Engine
  
  return {
    success: true,
    result: {}
  };
}
`;
  }

  /**
   * Generate VSCode README
   */
  private generateVSCodeReadme(capabilities: GeneratedCapability[]): string {
    return `# GL Code Intelligence VSCode Extension

Auto-generated VSCode extension for GL Code Intelligence & Security capabilities.

## Features

${capabilities.map(cap => `- **${cap.type}**: Execute ${cap.description}`).join('\n')}

## Installation

1. Open VSCode
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "GL Code Intelligence"
4. Click Install

## Usage

### Commands

Open the Command Palette (Ctrl+Shift+P / Cmd+Shift+P) and search for:

${capabilities.map(cap => `- \`GL Code Intel: ${cap.type}\`: Execute ${cap.type}`).join('\n')}

### Keyboard Shortcuts

- \`Ctrl+Shift+G\` (Windows/Linux) / \`Cmd+Shift+G\` (Mac): Quick action

## Development

\`\`\`bash
npm install
npm run compile
\`\`\`
`;
  }

  /**
   * Generate Web console
   */
  private async generateWebConsole(
    target: DeploymentTarget,
    capabilities: GeneratedCapability[],
    options: DeploymentOptions
  ): Promise<DeployedArtifact[]> {
    const artifacts: DeployedArtifact[] = [];

    // Generate HTML
    const html = this.generateWebHTML(capabilities);
    artifacts.push({
      id: uuidv4(),
      type: 'web',
      path: 'web/index.html',
      content: html,
      metadata: { name: 'Web Console HTML' }
    });

    // Generate CSS
    const css = this.generateWebCSS();
    artifacts.push({
      id: uuidv4(),
      type: 'web',
      path: 'web/styles.css',
      content: css,
      metadata: { name: 'Web Console Styles' }
    });

    // Generate JavaScript
    const js = this.generateWebJavaScript(capabilities);
    artifacts.push({
      id: uuidv4(),
      type: 'web',
      path: 'web/app.js',
      content: js,
      metadata: { name: 'Web Console Application' }
    });

    return artifacts;
  }

  /**
   * Generate Web HTML
   */
  private generateWebHTML(capabilities: GeneratedCapability[]): string {
    return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GL Code Intelligence Console</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div class="container">
    <header>
      <h1>GL Code Intelligence Console</h1>
      <p class="subtitle">Auto-generated by Deployment Weaver</p>
    </header>

    <main>
      <section class="capabilities">
        <h2>Available Capabilities</h2>
        <div class="capability-grid">
${capabilities.map(cap => `
          <div class="capability-card" data-type="${cap.type}">
            <h3>${cap.type}</h3>
            <p>${cap.type.replace(/-/g, ' ').replace(/\\b\\w/g, l => l.toUpperCase())}</p>
            <button class="btn-execute" onclick="executeCapability('${cap.type}')">Execute</button>
          </div>
`).join('')}
        </div>
      </section>

      <section class="results">
        <h2>Results</h2>
        <div id="results-container">
          <p class="placeholder">Select a capability to see results</p>
        </div>
      </section>
    </main>

    <footer>
      <p>GL Code Intelligence & Security Layer v21.0.0</p>
    </footer>
  </div>

  <script src="app.js"></script>
</body>
</html>
`;
  }

  /**
   * Generate Web CSS
   */
  private generateWebCSS(): string {
    return `
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #333;
  min-height: 100vh;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

header {
  text-align: center;
  color: white;
  margin-bottom: 40px;
}

header h1 {
  font-size: 2.5em;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 1.1em;
  opacity: 0.9;
}

.capabilities {
  background: white;
  border-radius: 12px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.capability-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.capability-card {
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 20px;
  transition: all 0.3s ease;
}

.capability-card:hover {
  border-color: #667eea;
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.capability-card h3 {
  color: #667eea;
  margin-bottom: 10px;
}

.capability-card p {
  color: #666;
  margin-bottom: 15px;
}

.btn-execute {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: opacity 0.3s ease;
}

.btn-execute:hover {
  opacity: 0.9;
}

.results {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.results h2 {
  margin-bottom: 20px;
}

#results-container {
  min-height: 200px;
  padding: 20px;
  background: #f5f5f5;
  border-radius: 8px;
}

.placeholder {
  color: #999;
  text-align: center;
  padding: 40px;
}

footer {
  text-align: center;
  color: white;
  margin-top: 40px;
  opacity: 0.9;
}
`;
  }

  /**
   * Generate Web JavaScript
   */
  private generateWebJavaScript(capabilities: GeneratedCapability[]): string {
    const capabilitiesArray = JSON.stringify(capabilities.map(c => ({
      type: c.type,
      description: c.type.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
    })));

    return `
const capabilities = ${capabilitiesArray};

async function executeCapability(type) {
  const resultsContainer = document.getElementById('results-container');
  resultsContainer.innerHTML = '<div class="loading">Executing...</div>';

  try {
    // TODO: Integrate with actual capability execution
    // This would call the Generator Engine API
    const result = await fetch('/api/execute', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ type, input: '' })
    });

    const data = await result.json();
    
    displayResults(data);
  } catch (error) {
    resultsContainer.innerHTML = \`<div class="error">Error: \${error.message}</div>\`;
  }
}

function displayResults(data) {
  const resultsContainer = document.getElementById('results-container');
  
  if (data.success) {
    resultsContainer.innerHTML = \`
      <div class="success">
        <h3>Execution Successful</h3>
        <pre>\${JSON.stringify(data.result, null, 2)}</pre>
      </div>
    \`;
  } else {
    resultsContainer.innerHTML = \`
      <div class="error">
        <h3>Execution Failed</h3>
        <p>\${data.error}</p>
      </div>
    \`;
  }
}

// Initialize capability cards
document.addEventListener('DOMContentLoaded', () => {
  console.log('GL Code Intelligence Console loaded');
});
`;
  }

  /**
   * Generate CI/CD integration
   */
  private async generateCICDIntegration(
    target: DeploymentTarget,
    capabilities: GeneratedCapability[],
    options: DeploymentOptions
  ): Promise<DeployedArtifact[]> {
    const artifacts: DeployedArtifact[] = [];

    // Generate GitHub Actions workflow
    const githubActions = this.generateGitHubActions(capabilities);
    artifacts.push({
      id: uuidv4(),
      type: 'cicd',
      path: 'cicd/github-actions.yml',
      content: githubActions,
      metadata: { name: 'GitHub Actions Workflow' }
    });

    // Generate GitLab CI configuration
    const gitlabCI = this.generateGitLabCI(capabilities);
    artifacts.push({
      id: uuidv4(),
      type: 'cicd',
      path: 'cicd/gitlab-ci.yml',
      content: gitlabCI,
      metadata: { name: 'GitLab CI Configuration' }
    });

    // Generate Jenkinsfile
    const jenkinsfile = this.generateJenkinsfile(capabilities);
    artifacts.push({
      id: uuidv4(),
      type: 'cicd',
      path: 'cicd/Jenkinsfile',
      content: jenkinsfile,
      metadata: { name: 'Jenkins Pipeline' }
    });

    return artifacts;
  }

  /**
   * Generate GitHub Actions workflow
   */
  private generateGitHubActions(capabilities: GeneratedCapability[]): string {
    return `name: GL Code Intelligence

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  gl-code-intel:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
      
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '20'
        
    - name: Install dependencies
      run: npm ci
      
${capabilities.map(cap => `
    - name: Execute ${cap.type}
      run: npx gl-code-intel ${cap.type} -i . -o ./output
      continue-on-error: true
`).join('')}
      
    - name: Upload results
      uses: actions/upload-artifact@v3
      with:
        name: gl-code-intel-results
        path: ./output
        
    - name: Generate report
      run: |
        echo "# GL Code Intelligence Report" > report.md
        echo "Generated at: $(date)" >> report.md
        echo "" >> report.md
        echo "## Capabilities Executed" >> report.md
${capabilities.map(cap => `        echo "- ${cap.type}" >> report.md`).join('\n')}
        
    - name: Upload report
      uses: actions/upload-artifact@v3
      with:
        name: gl-code-intel-report
        path: report.md
`;
  }

  /**
   * Generate GitLab CI configuration
   */
  private generateGitLabCI(capabilities: GeneratedCapability[]): string {
    return `stages:
  - gl-code-intel

gl-code-intel:
  stage: gl-code-intel
  image: node:20
  script:
    - npm ci
${capabilities.map(cap => `    - npx gl-code-intel ${cap.type} -i . -o ./output`).join('\n')}
  artifacts:
    paths:
      - ./output
      - report.md
    expire_in: 1 week
  only:
    - main
    - develop
    - merge_requests
`;
  }

  /**
   * Generate Jenkinsfile
   */
  private generateJenkinsfile(capabilities: GeneratedCapability[]): string {
    return `pipeline {
  agent any
  
  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }
    
    stage('Setup') {
      steps {
        sh 'npm ci'
      }
    }
${capabilities.map((cap, index) => `
    stage('${cap.type.replace(/-/g, ' ').replace(/\\b\\w/g, l => l.toUpperCase())}') {
      steps {
        sh "npx gl-code-intel ${cap.type} -i . -o ./output"
      }
    }
`).join('')}
  }
  
  post {
    always {
      archiveArtifacts artifacts: '**/output/**', 'report.md'
    }
  }
}
`;
  }

  /**
   * Generate Docker configuration
   */
  private async generateDockerConfig(
    target: DeploymentTarget,
    capabilities: GeneratedCapability[],
    options: DeploymentOptions
  ): Promise<DeployedArtifact[]> {
    const artifacts: DeployedArtifact[] = [];

    // Generate Dockerfile
    const dockerfile = this.generateDockerfile(capabilities);
    artifacts.push({
      id: uuidv4(),
      type: 'docker',
      path: 'docker/Dockerfile',
      content: dockerfile,
      metadata: { name: 'Dockerfile' }
    });

    // Generate docker-compose.yml
    const dockerCompose = this.generateDockerCompose(capabilities);
    artifacts.push({
      id: uuidv4(),
      type: 'docker',
      path: 'docker/docker-compose.yml',
      content: dockerCompose,
      metadata: { name: 'Docker Compose' }
    });

    return artifacts;
  }

  /**
   * Generate Dockerfile
   */
  private generateDockerfile(capabilities: GeneratedCapability[]): string {
    return `FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

# Install GL Code Intelligence CLI
RUN npm install -g gl-code-intel-cli

EXPOSE 3000

CMD ["node", "index.js"]
`;
  }

  /**
   * Generate Docker Compose
   */
  private generateDockerCompose(capabilities: GeneratedCapability[]): string {
    return `version: '3.8'

services:
  gl-code-intel:
    build: .
    ports:
      - "3000:3000"
    volumes:
      - ./src:/app/src
      - ./output:/app/output
    environment:
      - NODE_ENV=production
    command: npm start

  gl-code-intel-cli:
    build: .
    volumes:
      - ./src:/app/src
      - ./output:/app/output
    working_dir: /app
    command: gl-code-intel --help
`;
  }

  /**
   * Generate Kubernetes configuration
   */
  private async generateKubernetesConfig(
    target: DeploymentTarget,
    capabilities: GeneratedCapability[],
    options: DeploymentOptions
  ): Promise<DeployedArtifact[]> {
    const artifacts: DeployedArtifact[] = [];

    // Generate deployment manifest
    const deployment = this.generateKubernetesDeployment(capabilities);
    artifacts.push({
      id: uuidv4(),
      type: 'kubernetes',
      path: 'kubernetes/deployment.yaml',
      content: deployment,
      metadata: { name: 'Kubernetes Deployment' }
    });

    // Generate service manifest
    const service = this.generateKubernetesService(capabilities);
    artifacts.push({
      id: uuidv4(),
      type: 'kubernetes',
      path: 'kubernetes/service.yaml',
      content: service,
      metadata: { name: 'Kubernetes Service' }
    });

    // Generate config map
    const configMap = this.generateKubernetesConfigMap(capabilities);
    artifacts.push({
      id: uuidv4(),
      type: 'kubernetes',
      path: 'kubernetes/configmap.yaml',
      content: configMap,
      metadata: { name: 'Kubernetes ConfigMap' }
    });

    return artifacts;
  }

  /**
   * Generate Kubernetes deployment
   */
  private generateKubernetesDeployment(capabilities: GeneratedCapability[]): string {
    return `apiVersion: apps/v1
kind: Deployment
metadata:
  name: gl-code-intel
  labels:
    app: gl-code-intel
spec:
  replicas: 3
  selector:
    matchLabels:
      app: gl-code-intel
  template:
    metadata:
      labels:
        app: gl-code-intel
    spec:
      containers:
      - name: gl-code-intel
        image: gl-code-intel:21.0.0
        ports:
        - containerPort: 3000
        env:
        - name: NODE_ENV
          value: "production"
        - name: CAPABILITIES
          value: "${capabilities.map(c => c.type).join(',')}"
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 10
          periodSeconds: 5
`;
  }

  /**
   * Generate Kubernetes service
   */
  private generateKubernetesService(capabilities: GeneratedCapability[]): string {
    return `apiVersion: v1
kind: Service
metadata:
  name: gl-code-intel-service
spec:
  selector:
    app: gl-code-intel
  ports:
  - protocol: TCP
    port: 80
    targetPort: 3000
  type: LoadBalancer
`;
  }

  /**
   * Generate Kubernetes config map
   */
  private generateKubernetesConfigMap(capabilities: GeneratedCapability[]): string {
    return `apiVersion: v1
kind: ConfigMap
metadata:
  name: gl-code-intel-config
data:
  capabilities.json: |
${JSON.stringify(capabilities.map(c => ({
  type: c.type,
  config: c.configuration
})), null, 2).split('\n').map(line => '    ' + line).join('\n')}
`;
  }

  /**
   * Validate deployment request
   */
  private validateRequest(
    request: DeploymentRequest,
    errors: string[],
    warnings: string[]
  ): boolean {
    if (request.generatedCapabilities.length === 0) {
      errors.push('No capabilities to deploy');
      return false;
    }

    if (request.deploymentTargets.length === 0) {
      errors.push('No deployment targets specified');
      return false;
    }

    // Check confidence scores
    for (const capability of request.generatedCapabilities) {
      if (capability.metadata.confidenceScore < request.options.minConfidenceScore) {
        warnings.push(`Capability ${capability.type} has low confidence score: ${capability.metadata.confidenceScore}`);
      }
    }

    return true;
  }

  /**
   * Create deployment metadata
   */
  private createDeploymentMetadata(artifacts: DeployedArtifact[], duration?: number): DeploymentMetadata {
    const checksums: Record<string, string> = {};
    
    for (const artifact of artifacts) {
      // Simple checksum (in production, use proper hash)
      checksums[artifact.path] = Buffer.from(artifact.content).toString('base64').slice(0, 16);
    }

    return {
      deployedAt: Date.now(),
      capabilitiesDeployed: artifacts.length,
      targetPlatforms: [...new Set(artifacts.map(a => a.type))],
      version: '21.0.0',
      checksums,
      deploymentDuration: duration
    };
  }

  /**
   * Get deployment statistics
   */
  public getStatistics(): {
    totalDeployments: number;
    averageArtifactsPerDeployment: number;
    successRate: number;
  } {
    // In production, track actual statistics
    return {
      totalDeployments: 0,
      averageArtifactsPerDeployment: 0,
      successRate: 0
    };
  }
}
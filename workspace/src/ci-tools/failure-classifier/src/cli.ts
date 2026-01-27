#!/usr/bin/env node

/**
 * CLI 工具 - 命令行界面
 */

import { CIFailAutoClassificationSystem } from './index.js';
import { ClassificationResult } from './types.js';
import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';

interface CLIOptions {
  config?: string;
  output?: string;
  format?: 'json' | 'markdown' | 'table';
  verbose?: boolean;
}

export class CLI {
  private classificationSystem: CIFailAutoClassificationSystem;
  private options: CLIOptions;

  constructor(options: CLIOptions = {}) {
    this.options = options;
    this.classificationSystem = new CIFailAutoClassificationSystem();
  }

  /**
   * 執行分類
   */
  public async classify(prDiffFile: string, ciFailureFile: string): Promise<void> {
    try {
      // 讀取輸入文件
      const prDiff = JSON.parse(fs.readFileSync(prDiffFile, 'utf-8'));
      const ciFailure = JSON.parse(fs.readFileSync(ciFailureFile, 'utf-8'));

      if (this.options.verbose) {
        console.log('📋 PR Diff:', JSON.stringify(prDiff, null, 2));
        console.log('❌ CI Failure:', JSON.stringify(ciFailure, null, 2));
      }

      // 執行分類
      console.log('🔍 Starting classification...');
      const result = await this.classificationSystem.classify(prDiff, ciFailure);

      // 輸出結果
      this.outputResult(result);

      console.log('✅ Classification complete!');
    } catch (error) {
      console.error('❌ Error:', error);
      process.exit(1);
    }
  }

  /**
   * 輸出結果
   */
  private outputResult(result: {
    classificationResult: ClassificationResult;
    report: string;
    [key: string]: unknown;
  }): void {
    const format = this.options.format || 'markdown';
    const output = this.options.output;

    let content: string;

    switch (format) {
      case 'json':
        content = JSON.stringify(result, null, 2);
        break;
      case 'markdown':
        content = result.report;
        break;
      case 'table':
        content = this.generateTable(result);
        break;
      default:
        content = result.report;
    }

    if (output) {
      fs.writeFileSync(output, content, 'utf-8');
      console.log(`📄 Results saved to: ${output}`);
    } else {
      console.log('\n' + content);
    }
  }

  /**
   * 生成表格
   */
  private generateTable(result: {
    classificationResult: ClassificationResult;
    [key: string]: unknown;
  }): string {
    const lines: string[] = [];

    lines.push('+------------------+------------+------------+----------------------+');
    lines.push('| Type             | Severity   | Confidence | Suggested Action    |');
    lines.push('+------------------+------------+------------+----------------------+');

    const classificationResult = result.classificationResult;
    lines.push(
      `| ${classificationResult.errorType.padEnd(16)} | ` +
      `${classificationResult.severity.padEnd(10)} | ` +
      `${classificationResult.confidence.toString().padEnd(10)} | ` +
      `${classificationResult.suggestedAction.padEnd(20)} |`
    );

    lines.push('+------------------+------------+------------+----------------------+');

    return lines.join('\n');
  }

  /**
   * 健康度檢查
   */
  public async healthCheck(workflowName: string): Promise<void> {
    try {
      console.log('🏥 Checking CI health...');

      const report = await this.classificationSystem.getCIHealthReport(workflowName);

      console.log('\n📊 Health Report:');
      console.log(`Status: ${report.healthStatus}`);
      console.log(`Failure Rate: ${(report.metrics.failureRate * 100).toFixed(1)}%`);
      console.log(`Recent Failures (7d): ${report.metrics.last7DaysFailures}`);
      console.log(`Flaky Tests: ${report.metrics.flakyTests.length}`);
      console.log(`Trend: ${report.trendAnalysis}`);

      console.log('\n💡 Recommendations:');
      for (const recommendation of report.recommendations) {
        console.log(`  - ${recommendation}`);
      }

      console.log('\n✅ Health check complete!');
    } catch (error) {
      console.error('❌ Error:', error);
      process.exit(1);
    }
  }

  /**
   * 統計信息
   */
  public async statistics(): Promise<void> {
    try {
      console.log('📈 Gathering statistics...');

      const stats = this.classificationSystem.getStatistics();

      console.log('\n📊 System Statistics:');
      console.log(`Workflows: ${stats.workflows.length}`);
      console.log(`Rerun Stats:`, JSON.stringify(stats.rerunStats, null, 2));

      console.log('\n✅ Statistics complete!');
    } catch (error) {
      console.error('❌ Error:', error);
      process.exit(1);
    }
  }

  /**
   * 顯示幫助
   */
  public static showHelp(): void {
    console.log(`
🤖 CI Fail Auto Classification System - CLI

Usage:
  ci-fail-classifier classify <pr-diff.json> <ci-failure.json> [options]
  ci-fail-classifier health <workflow-name>
  ci-fail-classifier stats

Options:
  -c, --config <file>     Load configuration from file
  -o, --output <file>     Save output to file
  -f, --format <format>   Output format (json|markdown|table)
  -v, --verbose           Show verbose output
  -h, --help              Show this help message

Examples:
  # Classify a CI failure
  ci-fail-classifier classify pr-diff.json ci-failure.json

  # Save results to file
  ci-fail-classifier classify pr-diff.json ci-failure.json -o report.md

  # Output as JSON
  ci-fail-classifier classify pr-diff.json ci-failure.json -f json -o result.json

  # Check CI health
  ci-fail-classifier health ci.yml

  # View statistics
  ci-fail-classifier stats

For more information, visit: https://github.com/MachineNativeOps/machine-native-ops
    `);
  }
}

/**
 * 主函數
 */
async function main() {
  const args = process.argv.slice(2);
  const cli = new CLI();

  if (args.length === 0 || args.includes('-h') || args.includes('--help')) {
    CLI.showHelp();
    return;
  }

  const command = args[0];

  switch (command) {
    case 'classify':
      if (args.length < 3) {
        console.error('❌ Error: classify command requires PR diff and CI failure files');
        process.exit(1);
      }
      await cli.classify(args[1], args[2]);
      break;

    case 'health':
      if (args.length < 2) {
        console.error('❌ Error: health command requires workflow name');
        process.exit(1);
      }
      await cli.healthCheck(args[1]);
      break;

    case 'stats':
      await cli.statistics();
      break;

    default:
      console.error(`❌ Unknown command: ${command}`);
      CLI.showHelp();
      process.exit(1);
  }
}

// 運行 CLI
const isMainModule = process.argv[1] === fileURLToPath(import.meta.url);
if (isMainModule) {
  main().catch(error => {
    console.error('❌ Fatal error:', error);
    process.exit(1);
  });
}
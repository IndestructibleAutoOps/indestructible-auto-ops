# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: documentation
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: documentation
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
# GL Unified Charter Activated
# CI/CD Comprehensive Guide

**Last Updated**: 2026-01-19  
**Status**: Active  
**Purpose**: Consolidated CI/CD documentation and error analysis

## Quick Reference

### AI PR Reviewer & Summarizer
- **Workflow**: `.github/workflows/ai-pr-reviewer.yml`
- **Action**: `coderabbitai/ai-pr-reviewer@1.16.2`
- **Purpose**: AI-powered code review with chat capabilities

### Key Features
- AI-driven code review and analysis
- Automated PR summaries
- Interactive chat capabilities for code discussions
- Context-aware suggestions and improvements
- Continuous review on PR updates

### CI Error Analyzer
- **Workflow**: `.github/workflows/ci-error-analyzer.yml`
- **Script**: `scripts/ci-error-analyzer.py`
- **Module**: `workspace/src/core/ci_error_handler/`

### Profile Readme Development Stats
- **Workflow**: `.github/workflows/profile-readme-stats.yml`
- **Action**: `anmol098/waka-readme-stats@v5`
- **Purpose**: Automatically update README with development statistics from WakaTime

### Key Features
- Automatic workflow failure analysis
- Structured error extraction and categorization
- PR comments with actionable insights
- GitHub issue creation for persistent tracking
- Auto-fix detection and suggestions

## Architecture

### AI PR Reviewer Flow

The AI PR Reviewer automatically analyzes pull requests and provides intelligent feedback:

```
PR Event (opened/synchronize/reopened)
  → AI PR Reviewer Triggered
  → CodeRabbit AI Analysis
  → Code Review & Suggestions
  → PR Summary Generation
  → Interactive Chat Enabled
```

### CI/CD Error Analyzer Flow

The CI/CD Error Analyzer automatically analyzes workflow failures and provides actionable insights:

```
CI Workflow Execution (failure) 
  → CI Error Analyzer Triggered
  → Download Workflow Logs
  → Run Error Analysis (scripts/ci-error-analyzer.py)
  → Generate Structured Results
  → Post PR Comment + Create GitHub Issue
```

### Error Categorization
- **Critical**: Security vulnerabilities, build failures
- **High**: Test failures, quality gate failures
- **Medium**: Warnings, deprecations
- **Low**: Informational, suggestions

### Auto-Fix Detection
The analyzer identifies errors that can be automatically fixed:
- Code formatting issues
- Import sorting
- Simple syntax errors
- Configuration updates

## Implementation Status

### Completed (2026-01-19)
- ✅ AI-based PR Reviewer & Summarizer with Chat Capabilities
- ✅ CodeRabbit AI integration for automated code reviews
- ✅ Interactive chat support for PR discussions

### Completed (2026-01-18)
- ✅ Security Scan converted to non-blocking mode (PR #2)
- ✅ Enhanced PR quality check workflow with parallel execution
- ✅ Intelligent caching and error handling
- ✅ Comprehensive monitoring and alerting
- ✅ Complete documentation system

### Core Improvements
1. **Parallel Execution**: Security, quality, and test checks run concurrently
2. **Smart Caching**: Dependencies cached for faster builds
3. **Error Handling**: Enhanced error reporting with actionable insights
4. **Monitoring**: Health checks and failure notifications

## Usage

### AI PR Reviewer & Summarizer
The AI PR Reviewer runs automatically on pull request events:
- **Triggers**: PR opened, synchronized, or reopened
- **Chat**: Responds to review comments for interactive discussions
- **Review**: Provides AI-driven code analysis and suggestions

#### Prerequisites
To use the AI PR Reviewer, ensure the repository has:
- `OPENAI_API_KEY` configured in GitHub Secrets
- `GITHUB_TOKEN` is automatically provided by GitHub Actions

#### Interacting with the AI Reviewer
- The AI will automatically review new PRs and updates
- Comment on the PR to ask questions or request clarifications
- The AI responds to review comments for iterative discussions

### Running CI Error Analyzer
The analyzer runs automatically on workflow failures. Manual execution:

```bash
python scripts/ci-error-analyzer.py --workflow-run-id <run-id>
```

### Viewing Analysis Results
- Check PR comments for inline analysis
- Review GitHub issues for detailed reports
- Access JSON reports in workflow artifacts

## Configuration

### AI PR Reviewer Configuration
Location: `.github/workflows/ai-pr-reviewer.yml`

Key settings:
- **Triggers**: 
  - `pull_request`: opened, synchronize, reopened
  - `pull_request_review_comment`: created (for chat)
- **Permissions**: 
  - `contents: read`
  - `pull-requests: write`
  - `issues: write`
- **Environment Variables**:
  - `GITHUB_TOKEN`: Automatically provided
  - `OPENAI_API_KEY`: Must be configured in repository secrets

Options configured:
- `debug: false` - Disable debug mode for production
- `review_simple_changes: false` - Skip trivial changes
- `review_comment_lgtm: false` - Don't comment LGTM on every approval

### Workflow Configuration
Location: `.github/workflows/pr-quality-check.yml`

Key settings:
- Parallel job execution
- Dependency caching (pip, npm)
- Conditional execution based on file changes
- Comprehensive quality reports

### Error Patterns
Defined in: `workspace/src/core/ci_error_handler/error_patterns.py`

Custom patterns can be added to match project-specific errors.

## Monitoring and Alerts

### Health Checks
- Workflow success rate tracking
- Build time monitoring
- Quality metric trends

### Failure Notifications
- PR comments with detailed analysis
- GitHub issues for tracking
- Slack/email notifications (configurable)

## Profile Readme Development Stats

### Overview
The Profile Readme Development Stats workflow automatically updates the repository's README.md with coding statistics from WakaTime.

### Configuration
- **Schedule**: Runs daily at 00:00 UTC
- **Manual Trigger**: Can be triggered via workflow_dispatch
- **Permissions**: Requires `contents: write` to update README

### Features Enabled
- ✅ Lines of Code tracking
- ✅ Commit statistics
- ✅ Days of week analysis
- ✅ Language usage breakdown
- ✅ Operating system metrics
- ✅ Editor statistics
- ✅ Language per repository
- ✅ Short info summary
- ✅ Lines of code charts

### Setup Requirements

To enable this workflow, you need to:

1. **Create a WakaTime Account**: Sign up at [wakatime.com](https://wakatime.com)
2. **Get API Key**: Find your API key in WakaTime settings
3. **Add Secret**: Add `WAKATIME_API_KEY` to repository secrets
   - Go to repository Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `WAKATIME_API_KEY`
   - Value: Your WakaTime API key

**Note**: The workflow uses the default `GITHUB_TOKEN` for committing README updates. If you encounter permission issues in a protected branch scenario, you may need to configure branch protection rules or use a Personal Access Token (PAT) instead.

### README Markers
The workflow updates content between these markers in README.md:
```markdown
<!--START_SECTION:waka-->
<!--END_SECTION:waka-->
```

### Monitoring
- Check workflow runs in the Actions tab
- Review daily updates to the Development Stats section
- Stats update automatically every 24 hours

## Best Practices

1. **Review PR Comments**: Check automated analysis before merging
2. **Track Issues**: Use created GitHub issues for persistent tracking
3. **Update Patterns**: Add new error patterns as encountered
4. **Monitor Trends**: Review quality metrics regularly

## Troubleshooting

### Common Issues

**Security Scan Failures**
- Cause: Bandit detecting security issues in existing code
- Solution: Security scan runs in non-blocking mode
- Action: Review and remediate flagged issues incrementally

**Dependency Installation Failures**
- Cause: Cache corruption or version conflicts
- Solution: Clear cache and reinstall
- Action: Check `requirements.txt` versions

**Test Failures**
- Cause: Code changes breaking existing tests
- Solution: Review test output in PR comments
- Action: Fix failing tests or update test expectations

## References

### Archived Documentation
Historical CI analysis reports available in:
- `archive/ci-documentation/ci-analysis-complete-summary.md`
- `archive/ci-documentation/ci-final-analysis-report.md`
- `archive/ci-documentation/ci-improvement-analysis.md`
- `archive/ci-documentation/ci-implementation-guide.md`

### Related Documentation
- Security: `SECURITY.md`
- Quality Gates: `docs/DEVELOPER_GUIDELINES.md`
- Architecture: `workspace/ARCHITECTURE.md`

---

**Maintenance**: This guide consolidates multiple CI documentation files for single source of truth.  
**Audit Trail**: All historical reports preserved in `archive/ci-documentation/` with full git history.

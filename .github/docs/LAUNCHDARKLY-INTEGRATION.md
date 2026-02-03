# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: documentation
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
# GL Unified Charter Activated
# LaunchDarkly Code References Integration

**Last Updated**: 2026-01-19  
**Status**: Active  
**Workflow**: `.github/workflows/launchdarkly-code-references.yml`

## Overview

This repository uses the LaunchDarkly Code References GitHub Action to automatically discover and report feature flag references in the codebase. This integration helps track where feature flags are used and supports code cleanup efforts.

## Configuration

### Required Secrets

To enable the LaunchDarkly Code References workflow, configure the following repository secrets:

1. **LD_ACCESS_TOKEN**
   - A LaunchDarkly access token with write permissions
   - Create this token in your LaunchDarkly dashboard under Account Settings → Authorization
   - Store it as a repository secret named `LD_ACCESS_TOKEN`

2. **LD_PROJECT_KEY**
   - Your LaunchDarkly project key
   - Find this in Account Settings → Projects in the LaunchDarkly dashboard
   - Store it as a repository secret named `LD_PROJECT_KEY`

### Adding Repository Secrets

1. Navigate to your GitHub repository
2. Go to Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add `LD_ACCESS_TOKEN` with your LaunchDarkly access token
5. Add `LD_PROJECT_KEY` with your LaunchDarkly project key

## How It Works

The workflow runs automatically on:
- Pushes to the `main` branch
- Manual workflow dispatch via GitHub Actions UI

The action:
1. Checks out the repository code
2. Scans for feature flag references
3. Sends the references to LaunchDarkly
4. Updates the LaunchDarkly dashboard with code reference data

## Configuration Options

### Basic Configuration
The workflow uses sensible defaults:
- Fetches the last 11 commits (allows the lookback feature to analyze the previous 10 commits for flag usage changes)
- Includes 2 lines of context around each reference

### Advanced Configuration
For advanced configuration (monorepo support, custom aliases, etc.), create a configuration file at `.launchdarkly/coderefs.yml`. 

See [LaunchDarkly Configuration Documentation]([EXTERNAL_URL_REMOVED]) for details.

## Troubleshooting

### Workflow Not Running
- Ensure you're pushing to the `main` branch
- Check that the workflow file is valid YAML
- Verify repository permissions allow Actions to run

### Authentication Errors
- Verify `LD_ACCESS_TOKEN` secret is set correctly
- Ensure the access token has write permissions
- Check that the token hasn't expired

### Project Not Found
- Verify `LD_PROJECT_KEY` matches your LaunchDarkly project key exactly
- Check for typos in the secret value

## Related Documentation
- [LaunchDarkly Code References Action]([EXTERNAL_URL_REMOVED])
- [LaunchDarkly Documentation]([EXTERNAL_URL_REMOVED])
- [CI/CD Comprehensive Guide](./CI_COMPREHENSIVE_GUIDE.md)

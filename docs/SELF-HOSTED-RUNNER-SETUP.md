# Self-Hosted GitHub Actions Runner Setup Guide

## Overview
This guide provides instructions for setting up a self-hosted GitHub Actions runner for the MachineNativeOps/machine-native-ops repository.

## Prerequisites
- Linux ARM64 machine (e.g., Mac M1/M2, Raspberry Pi, ARM64 Linux server)
- GitHub account with repository access
- Sudo or root access on the target machine

## Setup Instructions

### 1. Create a Folder for the Runner

```bash
mkdir actions-runner && cd actions-runner
```

### 2. Download the Latest Runner Package

For ARM64 architecture:

```bash
curl -o actions-runner-linux-arm64-2.331.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.331.0/actions-runner-linux-arm64-2.331.0.tar.gz
```

**Note:** Check for the latest version at: https://github.com/actions/runner/releases

### 3. Optional: Validate the Hash

```bash
echo "f5863a211241436186723159a111f352f25d5d22711639761ea24c98caef1a9a  actions-runner-linux-arm64-2.331.0.tar.gz" | shasum -a 256 -c
```

### 4. Extract the Installer

```bash
tar xzf ./actions-runner-linux-arm64-2.331.0.tar.gz
```

### 5. Configure the Runner

You'll need a registration token from GitHub. Get it by:
1. Go to: https://github.com/MachineNativeOps/machine-native-ops/settings/actions/runners
2. Click "New self-hosted runner"
3. Copy the registration token

Then run:

```bash
./config.sh --url https://github.com/MachineNativeOps/machine-native-ops --token <YOUR_REGISTRATION_TOKEN>
```

### 6. Install and Run the Runner

**Option A: Run as a service (recommended for production):**

```bash
./svc.sh install
./svc.sh start
```

**Option B: Run interactively (for testing):**

```bash
./run.sh
```

### 7. Verify Runner Status

Check that the runner is active at:
https://github.com/MachineNativeOps/machine-native-ops/settings/actions/runners

## Runner Configuration Options

### Labels
Add labels to categorize your runner:

```bash
./config.sh --url <url> --token <token> --labels arm64,self-hosted,linux
```

### Runner Group
Assign to a specific runner group:

```bash
./config.sh --url <url> --token <token> --runnergroup <group-name>
```

## Managing the Runner

### Stop the Runner
```bash
./svc.sh stop
```

### Start the Runner
```bash
./svc.sh start
```

### Restart the Runner
```bash
./svc.sh restart
```

### Remove the Runner
```bash
./svc.sh uninstall
```

### Update the Runner
```bash
./svc.sh stop
curl -o actions-runner-linux-arm64-2.331.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.331.0/actions-runner-linux-arm64-2.331.0.tar.gz
tar xzf ./actions-runner-linux-arm64-2.331.0.tar.gz --overwrite
./svc.sh start
```

## Troubleshooting

### Runner Not Showing Up
- Check the runner logs: `./svc.sh status`
- Verify network connectivity
- Ensure the registration token is valid

### Permission Errors
- Ensure the runner user has proper permissions
- Check file ownership: `ls -la actions-runner`

### Runner Stalls
- Check system resources (CPU, memory)
- Review runner logs for errors
- Restart the service: `./svc.sh restart`

## GL_TOKEN Configuration

The `GL_TOKEN` is a GitHub Personal Access Token (PAT) or GitHub App token that replaces the default `GITHUB_TOKEN` across 19 workflows in this repository. It requires elevated permissions to perform various operations including creating PRs, publishing packages, and deploying to registries.

### Required Token Permissions/Scopes

When creating the GL_TOKEN, ensure it has the following minimum required scopes:

#### For Personal Access Token (Classic)
- `repo` (Full control of private repositories)
  - Includes: `repo:status`, `repo_deployment`, `public_repo`, `repo:invite`, `security_events`
  - **Required for**: Checking out code, creating/updating PRs, pushing commits, accessing repository content
- `write:packages` (Upload packages to GitHub Package Registry)
  - **Required for**: Publishing npm packages to GitHub Packages
- `read:packages` (Download packages from GitHub Package Registry)
  - **Required for**: Installing dependencies from GitHub Packages
- `workflow` (Update GitHub Action workflows)
  - **Required for**: Workflows that trigger other workflows or update workflow files

#### For Fine-Grained Personal Access Token
- **Repository permissions:**
  - Contents: `Read and write`
  - Issues: `Read and write`
  - Pull requests: `Read and write`
  - Workflows: `Read and write`
  - Metadata: `Read-only` (automatically included)
- **Account permissions:**
  - Packages: `Read and write` (if publishing to GitHub Packages)

### Token Usage in Workflows

The GL_TOKEN is used for the following operations:
1. **Repository Operations**: Checkout, commit, push, create PRs
2. **Package Publishing**: Publishing to GitHub Packages (npm registry)
3. **Container Registry**: Pushing images to GitHub Container Registry (ghcr.io)
4. **Issue/PR Management**: Creating and updating issues and pull requests
5. **Workflow Automation**: Triggering workflows and updating workflow files
6. **Semantic Release**: Automated version management and releases

### Setting Up GL_TOKEN

1. **Create the token**:
   - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token (classic)"
   - Add a descriptive note: "GL_TOKEN for machine-native-ops workflows"
   - Select the required scopes listed above
   - Set an appropriate expiration date (recommend: 90 days with calendar reminder for renewal)
   - Click "Generate token" and copy the token immediately

2. **Add to repository secrets**:
   - Go to: https://github.com/MachineNativeOps/machine-native-ops/settings/secrets/actions
   - Click "New repository secret"
   - Name: `GL_TOKEN`
   - Value: Paste the token you generated
   - Click "Add secret"

3. **Verify the token**:
   - Trigger a workflow that uses GL_TOKEN (e.g., manually trigger a workflow)
   - Check the workflow logs to ensure authentication succeeds
   - Monitor for any permission-related errors

### Security Best Practices for GL_TOKEN

1. **Scope Minimization**: Only grant the minimum required permissions
2. **Regular Rotation**: Rotate the token every 90 days or when team members with access leave
3. **Audit Trail**: Regularly review workflow runs to monitor token usage
4. **Access Control**: Limit who can view/modify repository secrets
5. **Expiration**: Set token expiration dates and use calendar reminders for renewal
6. **Monitoring**: Watch for unauthorized usage or permission errors in workflow logs

### Troubleshooting GL_TOKEN Issues

**403 Forbidden errors**:
- Verify the token has all required scopes
- Check if the token has expired
- Ensure the token has access to the repository

**Package publishing failures**:
- Confirm `write:packages` scope is enabled
- Verify the package name matches the repository owner/org

**PR creation failures**:
- Ensure `repo` scope is enabled (for classic tokens)
- For fine-grained tokens, verify `Pull requests: Read and write` permission

## Security Considerations

1. **Isolation**: Consider running the runner in a container or VM for isolation
2. **Permissions**: Use minimal required permissions
3. **Secrets**: Store sensitive data in GitHub secrets, not in workflow files
4. **Updates**: Keep the runner updated with the latest version

## Additional Resources

- [GitHub Actions Runner Documentation](https://docs.github.com/en/actions/hosting-your-own-runners)
- [Runner Releases](https://github.com/actions/runner/releases)
- [Troubleshooting Self-Hosted Runners](https://docs.github.com/en/actions/hosting-your-own-runners/troubleshooting-self-hosted-runners)

## Notes

- This guide uses ARM64 architecture (v2.331.0)
- For x86_64 architecture, download the appropriate package
- Always check for the latest runner version before installation
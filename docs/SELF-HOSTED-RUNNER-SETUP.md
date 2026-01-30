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

### Overview
This repository uses a custom `GL_TOKEN` secret instead of the default `GITHUB_TOKEN` for enhanced capabilities across 19+ workflows. The GL_TOKEN requires specific permissions to support all automated operations.

### Required Token Permissions

The GL_TOKEN must be a **Personal Access Token (Classic)** or **Fine-Grained Personal Access Token** with the following scopes:

#### For Classic Personal Access Token:
- **`repo`** (Full control of private repositories)
  - Includes: `repo:status`, `repo_deployment`, `public_repo`, `repo:invite`, `security_events`
  - Required for: Checkout with token, creating PRs, pushing commits, triggering workflows
- **`write:packages`** (Upload packages to GitHub Package Registry)
  - Includes: `read:packages`
  - Required for: Publishing NPM packages and Docker images to GitHub Container Registry
- **`workflow`** (Update GitHub Action workflows)
  - Required for: Workflows that trigger other workflows or modify workflow files

#### For Fine-Grained Personal Access Token:
- **Repository permissions**:
  - **Contents**: Read and write
  - **Pull requests**: Read and write
  - **Issues**: Read and write
  - **Metadata**: Read-only (automatically included)
  - **Workflows**: Read and write
  - **Actions**: Read and write
  - **Security events**: Read and write
- **Account permissions**:
  - **Packages**: Read and write

### Token Use Cases by Workflow

The GL_TOKEN is used for the following operations:

1. **Repository Operations**
   - Checking out code with extended permissions
   - Creating and updating pull requests
   - Pushing commits and tags
   - Triggering workflow runs

2. **Package Publishing**
   - Publishing NPM packages to GitHub Packages (`@machinenativeops/*`, `@machine-native-ops/*`)
   - Building and pushing Docker images to GitHub Container Registry (ghcr.io)
   - Authenticating to package registries

3. **Issue & PR Management**
   - Creating and updating issues
   - Adding comments and labels
   - Managing stale issues and PRs
   - Running AI-based PR reviews

4. **Release Management**
   - Creating releases via semantic-release
   - Generating release notes
   - Publishing release artifacts

5. **Security & Quality**
   - Running CodeQL security scans
   - Uploading security scan results
   - Running super-linter and other quality tools

### Creating the GL_TOKEN

1. **Generate a Personal Access Token**:
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token" → "Generate new token (classic)" or "Fine-grained token"
   - Set a descriptive name (e.g., "MachineNativeOps GL_TOKEN")
   - Set expiration (recommended: 90 days for security, up to 365 days for convenience)
   - Select the required scopes (see above)
   - Click "Generate token" and copy the token immediately

2. **Add to Repository Secrets**:
   - Go to your repository Settings → Secrets and variables → Actions
   - Or navigate to: `https://github.com/<YOUR_ORG>/<YOUR_REPO>/settings/secrets/actions`
   - Click "New repository secret"
   - Name: `GL_TOKEN`
   - Value: Paste the token you generated
   - Click "Add secret"

### Security Best Practices

1. **Token Rotation**: Rotate the GL_TOKEN regularly (recommended: every 90 days for production)
2. **Least Privilege**: Only grant the minimum required permissions
3. **Monitoring**: Regularly audit token usage in workflow logs
4. **Revocation**: Immediately revoke tokens if compromised
5. **Fine-Grained Tokens**: Prefer fine-grained tokens over classic tokens when possible
6. **Expiration**: Set an expiration date based on your security requirements (90 days for high security, up to 365 days for lower-risk environments)

### Troubleshooting Token Issues

**Symptom**: Workflow fails with "Resource not accessible by integration" or "Bad credentials"
- **Solution**: Verify GL_TOKEN is set correctly in repository secrets and has required permissions

**Symptom**: Package publishing fails with 403 Forbidden
- **Solution**: Ensure GL_TOKEN has `write:packages` permission and the token owner has write access to the repository

**Symptom**: Cannot trigger workflows
- **Solution**: Add the `workflow` scope to GL_TOKEN

**Symptom**: CodeQL scan fails to upload results
- **Solution**: Ensure GL_TOKEN has `security_events` scope (included in `repo` for classic tokens)

## Security Considerations

1. **Isolation**: Consider running the runner in a container or VM for isolation
2. **Permissions**: Use minimal required permissions
3. **Secrets**: Store sensitive data in GitHub secrets, not in workflow files
4. **Updates**: Keep the runner updated with the latest version
5. **Token Security**: Follow GL_TOKEN security best practices (see GL_TOKEN Configuration section)

## Additional Resources

- [GitHub Actions Runner Documentation](https://docs.github.com/en/actions/hosting-your-own-runners)
- [Runner Releases](https://github.com/actions/runner/releases)
- [Troubleshooting Self-Hosted Runners](https://docs.github.com/en/actions/hosting-your-own-runners/troubleshooting-self-hosted-runners)

## Notes

- This guide uses ARM64 architecture (v2.331.0)
- For x86_64 architecture, download the appropriate package
- Always check for the latest runner version before installation
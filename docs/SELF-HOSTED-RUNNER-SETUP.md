<!-- @GL-governed -->
<!-- @GL-layer: GL90-99 -->
<!-- @GL-semantic: governed-documentation -->
<!-- @GL-audit-trail: ../engine/governance/GL_SEMANTIC_ANCHOR.json -->
<!-- @GL-audit-trail: engine/governance/GL_SEMANTIC_ANCHOR.json -->

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
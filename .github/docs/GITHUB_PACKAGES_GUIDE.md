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
# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: documentation
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
# GL Unified Charter Activated
# Publishing npm Packages to GitHub Packages

This repository is configured to publish npm packages to GitHub Packages, GitHub's package registry.

## Overview

GitHub Packages allows you to host and manage packages alongside your code. This repository contains multiple npm packages that can be published to the GitHub Packages npm registry.

## Packages

The following packages are configured for publication to GitHub Packages:

- `@machinenativeops/mcp-servers` - Enterprise-grade MCP servers
- `@machinenativeops/advisory-database` - Professional advisory database service
- `@machine-native-ops/taxonomy-core` - Core taxonomy system
- `@machine-native-ops/namespaces-mcp` - Enterprise-grade MCP platform
- `@machine-native-ops/namespaces-sdk` - Machine-Native Platform Integration Layer

## Authentication

### For Publishing (CI/CD)

Publishing is handled automatically by GitHub Actions using the `GITHUB_TOKEN` secret. The workflow is triggered on:

- Release publication
- Manual workflow dispatch

### For Installing Packages

To install packages from GitHub Packages, you need to authenticate with a Personal Access Token (classic) that has `read:packages` scope.

#### Using .npmrc File

Add the following to your `~/.npmrc` file:

```shell
@machinenativeops:registry=https://npm.pkg.github.com
@machine-native-ops:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=YOUR_PERSONAL_ACCESS_TOKEN
```

Replace `YOUR_PERSONAL_ACCESS_TOKEN` with your GitHub Personal Access Token.

#### Using npm login

For npm CLI version 9 or higher, use the `--auth-type=legacy` option:

```shell
npm login --scope=@machinenativeops --auth-type=legacy --registry=https://npm.pkg.github.com
```

When prompted:
- **Username**: Your GitHub username
- **Password**: Your Personal Access Token
- **Email**: Your GitHub email address

## Publishing Packages

### Automated Publishing via GitHub Actions

1. **Create a Release**: Publishing is automatically triggered when you create a new release on GitHub.

2. **Manual Publish**: You can manually trigger the publish workflow from the Actions tab.

### Manual Publishing

If you need to publish manually:

1. Authenticate with GitHub Packages (see Authentication section above)

2. Navigate to the package directory:
   ```shell
   cd workspace/src/mcp-servers
   ```

3. Ensure the package is built (if applicable):
   ```shell
   npm run build
   ```

4. Publish the package:
   ```shell
   npm publish
   ```

## Installing Packages

After configuring authentication, install packages using npm:

```shell
npm install @machinenativeops/mcp-servers
npm install @machine-native-ops/taxonomy-core
```

## Package Configuration

All publishable packages in this repository are configured with:

1. **Scoped Names**: All packages use organization scopes (`@machinenativeops` or `@machine-native-ops`)
2. **publishConfig**: Set to use GitHub Packages registry
3. **repository**: Linked to the GitHub repository

Example `package.json` configuration:

```json
{
  "name": "@machinenativeops/mcp-servers",
  "version": "1.0.0",
  "publishConfig": {
    "registry": "https://npm.pkg.github.com"
  },
  "repository": {
    "type": "git",
    "url": "git+https://github.com/MachineNativeOps/machine-native-ops.git",
    "directory": "workspace/src/mcp-servers"
  }
}
```

## Using Packages in GitHub Actions

To use these packages in GitHub Actions workflows:

1. Authenticate using `GITHUB_TOKEN`:

```yaml
- name: Setup Node.js
  uses: actions/setup-node@v4
  with:
    node-version: '18'
    registry-url: 'https://npm.pkg.github.com'

- name: Configure npm
  run: |
    echo "@machinenativeops:registry=https://npm.pkg.github.com" >> .npmrc
    echo "//npm.pkg.github.com/:_authToken=${{ secrets.GITHUB_TOKEN }}" >> .npmrc

- name: Install dependencies
  run: npm install
```

## Installing from Multiple Organizations

If you need to install packages from both GitHub Packages and npmjs.org:

```shell
# In your .npmrc
@machinenativeops:registry=https://npm.pkg.github.com
@machine-native-ops:registry=https://npm.pkg.github.com
registry=https://registry.npmjs.org/
```

This configuration routes scoped packages to GitHub Packages while other packages come from npmjs.org.

## Troubleshooting

### Permission Denied

If you get permission errors:
- Verify your Personal Access Token has the `read:packages` scope (for installing) or `write:packages` scope (for publishing)
- Check that you're authenticated with the correct account
- Ensure you have access to the `MachineNativeOps` organization

### Package Not Found

If a package is not found:
- Verify the package has been published by checking the Packages tab in the repository
- Ensure your `.npmrc` is configured correctly with the registry URL
- Check that you're using the correct package name with the scope

### Build Errors

If publishing fails due to build errors:
- Ensure all dependencies are installed (`npm install`)
- Run the build script locally first (`npm run build`)
- Check that all required build tools are available

## References

- [GitHub Packages Documentation](https://docs.github.com/en/packages)
- [Configuring npm for use with GitHub Packages](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-npm-registry)
- [Publishing and installing a package with GitHub Actions](https://docs.github.com/en/packages/managing-github-packages-using-github-actions-workflows/publishing-and-installing-a-package-with-github-actions)

## Support

For issues related to:
- Package publishing: Check the GitHub Actions workflow logs
- Package installation: Verify authentication and `.npmrc` configuration
- Package access: Ensure you have the necessary permissions in the MachineNativeOps organization

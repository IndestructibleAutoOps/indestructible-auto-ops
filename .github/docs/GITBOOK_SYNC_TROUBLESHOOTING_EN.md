# GL Unified Charter Activated
# GitBook Sync Troubleshooting Guide

## GitBook Sync Failures

This guide provides solutions for common issues when synchronizing GitBook with GitHub.

---

## 📋 Table of Contents

- [README File Management](#readme-file-management)
- [Repository Configuration Requirements](#repository-configuration-requirements)
- [Documentation Folder Configuration](#documentation-folder-configuration)
- [New File Sync Issues](#new-file-sync-issues)
- [Redirect Configuration](#redirect-configuration)
- [Repository Permission Issues](#repository-permission-issues)
- [GitHub Preview Issues](#github-preview-issues)
- [Duplicate Account Issues](#duplicate-account-issues)

---

## README File Management

### 🚫 I'm Encountering GitHub Sync Errors

**Ensure You Only Create README Files in Your Repository**

When enabling Git Sync, be careful not to create README files through the GitBook UI. Creating README files through GitBook UI will:

- ❌ Create duplicate README files in your repository
- ❌ Cause rendering conflicts between GitBook and GitHub
- ❌ Potentially break build and deployment processes
- ❌ Lead to unpredictable file prioritization

⚠️ **Note**: This includes files named `README.md`, `readme.md`, `Readme.md`, and `README` without an extension.

✅ **Best Practice**: Always manage your README files directly in your git repository.

---

## Repository Configuration Requirements

### 🔧 Still Encountering Errors?

Please ensure:

#### 1. README.md File Location

Your repository **has a `README.md` file in the root directory** (or in the folder specified in `.gitbook.yaml`) created directly in your git repository.

- This file is **required** and serves as the homepage of your documentation
- For more details, see our [.gitbook.yaml content configuration](https://docs.gitbook.com/integrations/git-sync/content-configuration)

#### 2. YAML Frontmatter Validation

If your Markdown files contain YAML frontmatter, use a [YAML checker](https://yamlchecker.com/) to ensure they are valid.

**Example YAML Frontmatter:**

```markdown
---
title: My Document Title
description: Document description
---

# Document content starts here
```

---

## Documentation Folder Configuration

### 📁 GitBook Is Not Using My docs Folder

By default, GitBook uses the repository root directory as the starting point. You can specify a specific directory to scope Markdown files.

**Configuration Method:**

Create or edit a `.gitbook.yaml` file in the repository root:

```yaml
root: ./docs/

structure:
  readme: README.md
  summary: SUMMARY.md
```

For more information, see the [GitBook content configuration documentation](https://docs.gitbook.com/integrations/git-sync/content-configuration).

---

## New File Sync Issues

### 🔄 GitBook Shows No Response After Adding New Files to My Repository

This section specifically addresses issues **when a `SUMMARY.md` file already exists**.

#### About SUMMARY.md

If your repository doesn't contain a `SUMMARY.md` file, GitBook will automatically create one during the first sync. This means if you've edited content on GitBook at least once after setting up Git Sync, GitBook should have already created this file.

#### Troubleshooting Steps

If after updating your repository by adding or modifying Markdown files, you don't see updates on GitBook, and the sidebar shows no errors during sync:

1. **Check SUMMARY.md**: Your modified files may not be listed in your `SUMMARY.md` file
2. **Understand SUMMARY.md's Role**:
   - The file's content mirrors your **Table of Contents** on GitBook
   - Used during the Git to GitBook import phase to rebuild your table of contents
   - Realigns incoming updates from the repository with existing content on GitBook

**Example SUMMARY.md:**

```markdown
# Table of Contents

* [Introduction](README.md)
* [Quick Start](docs/quickstart.md)
* [Configuration Guide](docs/configuration.md)
  * [Basic Configuration](docs/configuration/basic.md)
  * [Advanced Configuration](docs/configuration/advanced.md)
```

#### Still Not Resolved?

If GitBook still shows no response after confirming all files are included in the `SUMMARY.md` file, feel free to [contact support](https://www.gitbook.com/support) for assistance.

---

## Redirect Configuration

### 🔀 Redirects Are Not Working Properly

YAML files need to be properly formatted for redirects to work. Issues like indentation or spacing errors can cause redirects to fail.

#### Key Points for Redirect Configuration

1. **Validate YAML Format**: Using a [YAML validator](https://yamlchecker.com/) ensures redirects work smoothly
2. **Don't Add Leading Slashes**:
   - ❌ Wrong: `./misc/support.md`
   - ✅ Correct: `misc/support.md`

#### Redirect Priority Rules

⚠️ **Important**: As long as a page exists at a given path, GitBook won't look for possible redirects.

Therefore, if you set up a redirect from an old page to a new page, you need to **delete the old page** for the redirect to take effect.

**Example Redirect Configuration (.gitbook.yaml):**

```yaml
redirects:
  old-page: new-page.md
  guides/old-guide: guides/new-guide.md
```

---

## Repository Permission Issues

### 🔒 My Repository Is Not Listed

#### For GitHub Repositories

Ensure you've installed the GitBook GitHub app to the correct location:

1. When installing the app, you can choose to:
   - Install to your personal GitHub account
   - Install to any organization you have permissions for
2. Ensure the app has been granted the correct repository permissions

**Steps to Check Installation:**

1. Visit [GitHub Apps Settings](https://github.com/settings/installations)
2. Find the GitBook app
3. Verify repository access permissions

#### For GitLab Repositories

Ensure your access token is configured with the following permissions:

- ✅ `api`
- ✅ `read_repository`
- ✅ `write_repository`

**Creating a GitLab Access Token:**

1. Visit GitLab → Settings → Access Tokens
2. Create a new token and select the three permissions above
3. Copy the token to your GitBook integration settings

---

## GitHub Preview Issues

### 👁️ GitHub Preview Not Displaying

If your GitHub preview isn't displaying, it may be because your GitSync integration was configured **before January 2022**.

GitSync versions configured before this date don't include the GitHub preview feature.

#### Solution

You should have received a notification asking you to accept updated permission requests to enable read-only access to PRs.

#### Manual Update Steps

If you didn't receive the notification, troubleshooting requires updating to the new version:

1. **Uninstall Old Version**: Uninstall the GitSync integration from your organization
2. **Reinstall New Version**: Reinstall the new version with updated permissions
3. **Reconfigure Spaces**: Uninstalling GitSync integration will require reconfiguring the integration on any previously connected spaces

⚠️ **Note**: This will affect all previously configured spaces, requiring reconfiguration one by one.

---

## Duplicate Account Issues

### 👥 Possible Duplicate Accounts When Logging In

This error typically occurs when the GitHub account used to set up sync is already associated with another GitBook user account.

#### Identifying the Associated Account

To identify which GitBook account the GitHub account is linked to:

1. **Log Out of Current Session**: Log out of your current GitBook user session (e.g., `name@email.com`)
2. **Log Out of GitHub**: Log out of any GitHub user sessions
3. **Log In with GitHub**:
   - Go to the [GitBook login page](https://app.gitbook.com/login)
   - Select the "Sign in with GitHub" option
   - Enter your GitHub credentials
4. **Check Account Settings**:
   - After logging in, go to account settings
   - Do one of the following:
     - Unlink the account in the "Third-party logins > GitHub" section (in personal settings)
     - If the account isn't needed, delete it entirely
5. **Re-login**:
   - Log out from that session
   - Log back in using your `name@email.com` GitBook account
   - Try setting up Git Sync again

---

## 📚 Related Resources

- [GitBook Official Documentation](https://docs.gitbook.com/)
- [Git Sync Guide](https://docs.gitbook.com/integrations/git-sync)
- [Content Configuration](https://docs.gitbook.com/integrations/git-sync/content-configuration)
- [GitBook Support Center](https://www.gitbook.com/support)

---

## 🆘 Need More Help?

If none of the above solutions resolve your issue:

1. Check the [GitBook Support Center](https://www.gitbook.com/support)
2. Visit the [GitBook Community Forum](https://github.com/GitbookIO/gitbook/discussions)
3. [Contact GitBook Support Team](https://www.gitbook.com/support)

---

**Last Updated**: 2026-01-21

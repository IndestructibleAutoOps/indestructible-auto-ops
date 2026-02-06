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
# GitBook 同步故障排除指南

## 与 GitBook 同步失败

本指南提供 GitBook 与 GitHub 同步时常见问题的解决方案。

---

## 📋 目录

- [README 文件管理](#readme-文件管理)
- [仓库配置要求](#仓库配置要求)
- [文档文件夹配置](#文档文件夹配置)
- [新文件同步问题](#新文件同步问题)
- [重定向配置](#重定向配置)
- [仓库权限问题](#仓库权限问题)
- [GitHub 预览问题](#github-预览问题)
- [账户重复问题](#账户重复问题)

---

## README 文件管理

### 🚫 我遇到了 GitHub 同步错误

**请确保只在你的仓库中创建 README 文件**

启用 Git 同步时，请注意不要通过 GitBook UI 创建 README 文件。通过 GitBook UI 创建 README 文件会：

- ❌ 在你的仓库中创建重复的 README 文件
- ❌ 导致 GitBook 与 GitHub 之间的渲染冲突
- ❌ 可能破坏构建和部署流程
- ❌ 导致不可预测的文件优先级

⚠️ **注意**：这包括名为 `readme.md`、`readme.md`、`Readme.md` 和不带扩展名的 `README` 的文件。

✅ **最佳实践**：请记得直接在你的 git 仓库中管理你的 README 文件。

---

## 仓库配置要求

### 🔧 仍然遇到错误？

请确保：

#### 1. readme.md 文件位置

你的仓库**在根目录有一个 `readme.md` 文件**（或在 `.gitbook.yaml` 中指定的文件夹）直接在你的 git 仓库中创建。

- 该文件是**必需的**，并用作文档的首页
- 更多细节请参阅我们的 [.gitbook.yaml 内容配置]([EXTERNAL_URL_REMOVED])

#### 2. YAML Frontmatter 验证

如果你的 Markdown 文件中有 YAML frontmatter，请使用 [YAML 检查器]([EXTERNAL_URL_REMOVED]) 以确保它们有效。

**示例 YAML Frontmatter：**

```markdown
---
title: 我的文档标题
description: 文档描述
---

# 文档内容开始于此
```

---

## 文档文件夹配置

### 📁 GitBook 没有使用我的 docs 文件夹

默认情况下，GitBook 使用仓库根目录作为起点。可以指定特定目录以限定 Markdown 文件。

**配置方法：**

在仓库根目录创建或编辑 `.gitbook.yaml` 文件：

```yaml
root: ./docs/

structure:
  readme: readme.md
  summary: SUMMARY.md
```

有关更多信息，请查看 [GitBook 内容配置文档]([EXTERNAL_URL_REMOVED])。

---

## 新文件同步问题

### 🔄 在将新文件添加到我的仓库后，GitBook 没有任何反应

本节特别针对以下情况的问题，**当一个 `SUMMARY.md` 文件已存在**。

#### 关于 SUMMARY.md

如果你的仓库不包含一个 `SUMMARY.md` 文件，GitBook 会在第一次同步时自动创建一个。这意味着如果在设置 Git 同步后你至少在 GitBook 上编辑过一次内容，GitBook 应该已经自动创建了该文件。

#### 问题排查步骤

如果在通过向仓库添加或修改 Markdown 文件更新仓库后，你没有在 GitBook 上看到更新，且侧边栏在同步期间未显示错误：

1. **检查 SUMMARY.md**：你修改的文件可能没有被列在你的 `SUMMARY.md` 文件中
2. **了解 SUMMARY.md 的作用**：
   - 该文件的内容镜像你在 GitBook 上的**目录（Table of Contents）**
   - 在同步的 Git 到 GitBook 导入阶段用于重建你的目录
   - 将仓库中即将到来的更新与 GitBook 上现有内容重新对齐

**SUMMARY.md 示例：**

```markdown
# 目录

* [简介](readme.md)
* [快速开始](docs/quickstart.md)
* [配置指南](docs/configuration.md)
  * [基础配置](docs/configuration/basic.md)
  * [高级配置](docs/configuration/advanced.md)
```

#### 仍然没有解决？

如果在确认所有文件都包含在 `SUMMARY.md` 文件中后，GitBook 仍然没有任何反应，请随时[联系支持]([EXTERNAL_URL_REMOVED])寻求帮助。

---

## 重定向配置

### 🔀 重定向无法正确工作

YAML 文件需要正确格式化，重定向才能生效。诸如缩进或空格错误可能导致重定向无法工作。

#### 重定向配置要点

1. **验证 YAML 格式**：使用 [YAML 验证器]([EXTERNAL_URL_REMOVED])可以确保重定向顺利工作
2. **不要添加前导斜杠**：
   - ❌ 错误：`./misc/support.md`
   - ✅ 正确：`misc/support.md`

#### 重定向优先级规则

⚠️ **重要**：只要某个路径对应的页面存在，GitBook 就不会去查找可能的重定向。

因此，如果你为旧页面设置重定向到新页面，需要**删除旧页面**，重定向才能生效。

**重定向配置示例（.gitbook.yaml）：**

```yaml
redirects:
  old-page: new-page.md
  guides/old-guide: guides/new-guide.md
```

---

## 仓库权限问题

### 🔒 我的仓库未列出

#### 针对 GitHub 仓库

请确保你已将 GitBook GitHub 应用安装到正确的位置：

1. 安装应用时，你可以选择：
   - 安装到个人 GitHub 账户
   - 安装到你有权限的任何组织
2. 确保已授予该应用正确的仓库权限

**检查安装步骤：**

1. 访问 [GitHub Apps 设置]([EXTERNAL_URL_REMOVED])
2. 找到 GitBook 应用
3. 验证仓库访问权限

#### 针对 GitLab 仓库

请确保你的访问令牌已配置以下访问权限：

- ✅ `api`
- ✅ `read_repository`
- ✅ `write_repository`

**创建 GitLab 访问令牌：**

1. 访问 GitLab → Settings → Access Tokens
2. 创建新令牌并选择上述三个权限
3. 将令牌复制到 GitBook 集成设置中

---

## GitHub 预览问题

### 👁️ GitHub 预览未显示

如果你的 GitHub 预览未显示，可能是因为你的 GitSync 集成是在 **2022 年 1 月之前**配置的。

该日期之前配置的 GitSync 版本不包含 GitHub 预览功能。

#### 解决方案

你应该已经收到一条通知，要求你接受更新后的权限请求以启用对 PR 的只读访问。

#### 手动更新步骤

如果你没有收到该通知，故障排除需要更新到新版本：

1. **卸载旧版本**：从你的组织中卸载 GitSync 集成
2. **重新安装新版本**：使用更新权限重新安装新版本
3. **重新配置空间**：卸载 GitSync 集成将需要在之前连接过的任何空间上重新配置该集成

⚠️ **注意**：这将影响所有之前配置的空间，需要逐一重新配置。

---

## 账户重复问题

### 👥 登录时可能出现重复账户

此错误通常发生在用于设置同步的 GitHub 账户已与另一个 GitBook 用户账户关联时。

#### 识别关联账户

识别该 GitHub 账户已链接到哪个 GitBook 账户的方法：

1. **登出当前会话**：登出你当前的 GitBook 用户会话（例如：`name@email.com`）
2. **登出 GitHub**：登出任何 GitHub 用户会话
3. **使用 GitHub 登录**：
   - 前往 [GitBook 登录页面]([EXTERNAL_URL_REMOVED])
   - 选择"使用 GitHub 登录"选项
   - 输入你的 GitHub 凭据
4. **检查账户设置**：
   - 登录后，前往账户设置
   - 执行以下操作之一：
     - 在"第三方登录 > GitHub"部分取消关联该账户（个人设置中）
     - 如果不需要该账户，则彻底删除该账户
5. **重新登录**：
   - 从该会话登出
   - 使用你的 `name@email.com` GitBook 账户重新登录
   - 尝试再次设置 Git 同步

---

## 📚 相关资源

- [GitBook 官方文档]([EXTERNAL_URL_REMOVED])
- [Git 同步指南]([EXTERNAL_URL_REMOVED])
- [内容配置]([EXTERNAL_URL_REMOVED])
- [GitBook 支持中心]([EXTERNAL_URL_REMOVED])

---

## 🆘 需要更多帮助？

如果以上解决方案都无法解决你的问题：

1. 查看 [GitBook 支持中心]([EXTERNAL_URL_REMOVED])
2. 访问 [GitBook 社区论坛]([EXTERNAL_URL_REMOVED])
3. [联系 GitBook 支持团队]([EXTERNAL_URL_REMOVED])

---

**最后更新**: 2026-01-21

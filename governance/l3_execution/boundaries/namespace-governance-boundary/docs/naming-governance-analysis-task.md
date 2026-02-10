# 命名治理分析任务

## 任务 1: 分析 gov-platform/governance/naming-governance 四层结构

### 目标
分析命名治理目录的四层结构，理解其组织架构和职责划分。

### 四层结构概览
```
gov-platform/governance/naming-governance/
├── contracts/          # 第1层：契约层
├── registry/           # 第2层：注册表层
├── policies/           # 第3层：策略层
└── validators/         # 第4层：验证器层
```

### 待分析内容
1. **第1层 - Contracts (契约层)**
   - naming-conventions.yaml
   
2. **第2层 - Registry (注册表层)**
   - abbreviation-registry.yaml
   - capability-registry.yaml
   - domain-registry.yaml
   - resource-registry.yaml
   
3. **第3层 - Policies (策略层)**
   - 分析所有策略文件
   
4. **第4层 - Validators (验证器层)**
   - 分析验证器实现

---

## 任务 2: 全仓库命名规范索引

### 目标
索引整个仓库中所有提及的命名规范和约定。

### 发现的命名相关文件
目前已识别的命名相关文件：

#### 1. GitHub 层级
- `.github/governance/policies/observability/naming-metrics-policy.yaml`
- `.github/governance/policies/migration/naming-migration-policy.yaml`
- `.github/governance/policies/naming/api-naming.yaml`
- `.github/governance/policies/naming/k8s-deployment-naming.yaml`
- `.github/governance/policies/naming/pipeline-naming.yaml`
- `.github/governance/architecture/gov-directory-naming-spec.yaml`
- `.github/workflows/conftest-naming.yaml`
- `.github/workflows/gov-naming-governance.yml`

#### 2. Engine 层级
- `engine/governance/gov-artifacts/meta/naming-charter/gov-unified-naming-charter.yaml`
- `engine/governance/gov-artifacts/meta/gov-naming-charter-analysis.md`
- `engine/scripts-legacy/hooks/gov-naming-check.py`
- `engine/templates/ci/github-actions-naming-check.yml`
- `engine/controlplane/specifications/root.specs.naming.yaml`
- `engine/controlplane/config/root.naming-policy.yaml`
- `engine/tools-legacy/governance/python/validate_naming.py`
- `engine/tools-legacy/governance/python/naming-migration.py`

#### 3. 平台层级
- `observability/alerts/prometheus-rules/naming-convention-alerts.yaml`
- `observability/dashboards/naming-compliance.json`
- `gov-platform/contracts/unified-naming-governance-contract.yaml`
- `gov-platform/governance/naming-governance/contracts/naming-conventions.yaml`

### 下一步行动
1. 读取并分析所有命名相关文件
2. 提取命名规范和约定
3. 建立命名规范索引
4. 生成命名治理分析报告

---

## 分析进度

### 阶段 1：四层结构分析
- [ ] 读取 contracts/naming-conventions.yaml
- [ ] 读取 registry 下所有文件
- [ ] 读取 policies 下所有文件
- [ ] 读取 validators 下所有文件

### 阶段 2：全仓库索引
- [ ] 扫描所有命名相关文件
- [ ] 提取命名规范
- [ ] 建立命名规范数据库
- [ ] 生成索引报告

### 阶段 3：综合分析
- [ ] 对比各层级命名规范
- [ ] 识别冲突和不一致
- [ ] 提出统一化建议
- [ ] 生成最终报告
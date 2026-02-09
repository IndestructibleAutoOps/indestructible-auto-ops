# NG 治理系统部署包

## 概述

本部署包包含完整的 NG 治理系统部署配置，包括 Kubernetes YAML、测试套件、监控仪表板和运维手册。

## 目录结构

```
deployment/
├── kubernetes/           # Kubernetes 部署配置
│   ├── 01-namespace.yaml
│   ├── 02-configmap.yaml
│   ├── 03-secret.yaml
│   ├── 10-validator-deployment.yaml
│   ├── 20-parametric-engine-deployment.yaml
│   ├── 21-vector-space-deployment.yaml
│   └── 30-servicemonitors.yaml
├── tests/               # 测试套件
│   ├── test_ng_semantic_binding.py
│   ├── test_parametric_convergence.py
│   ├── test_fallback_semantic_validation.py
│   ├── pytest.ini
│   └── requirements.txt
├── monitoring/          # 监控配置
│   └── grafana-dashboard.json
├── docs/               # 文档
│   └── operations-manual.md
└── README.md           # 本文件
```

## 快速开始

### 1. 前置要求

- Kubernetes 1.24+
- Helm 3.x
- kubectl 1.24+
- Prometheus Operator

### 2. 部署

```bash
# 设置环境变量
export GITHUB_TOKEN="your-github-token"
export POSTGRES_PASSWORD="your-postgres-password"
export REDIS_PASSWORD="your-redis-password"
export OPENAI_API_KEY="your-openai-api-key"

# 部署所有组件
kubectl apply -f deployment/kubernetes/

# 验证部署
kubectl get pods -n ng-governance
```

### 3. 运行测试

```bash
# 安装测试依赖
cd deployment/tests
pip install -r requirements.txt

# 运行测试
pytest -v --cov=. --cov-report=html
```

### 4. 导入 Grafana 仪表板

1. 打开 Grafana
2. 导航到 Dashboards -> Import
3. 上传 `monitoring/grafana-dashboard.json`

## 组件说明

### Kubernetes 配置

- **01-namespace.yaml**: 创建 ng-governance 命名空间
- **02-configmap.yaml**: 包含 NG 命名规范、参数优化、收敛性保证和故障回退配置
- **03-secret.yaml**: 存储敏感信息（GitHub token、数据库密码等）
- **10-validator-deployment.yaml**: NG 命名空间验证器部署
- **20-parametric-engine-deployment.yaml**: 参数化引擎部署
- **21-vector-space-deployment.yaml**: 向量空间管理器部署
- **30-servicemonitors.yaml**: Prometheus ServiceMonitor 和告警规则

### 测试套件

- **test_ng_semantic_binding.py**: 测试 NG 语义绑定层
- **test_parametric_convergence.py**: 测试参数化收敛性保证
- **test_fallback_semantic_validation.py**: 测试故障回退语义验证

### 监控配置

- **grafana-dashboard.json**: Grafana 仪表板配置，包含以下面板：
  - NG 违规总数
  - NG 违规率
  - 参数收敛率
  - 反馈回路稳定性
  - NG 验证耗时
  - 回退激活统计
  - NG 违规按代码分布

### 文档

- **operations-manual.md**: 完整的运维手册，包括：
  - 系统概述
  - 部署指南
  - 故障排查
  - 恢复程序
  - 性能优化
  - 安全最佳实践

## 监控和告警

### 关键指标

| 指标名 | 描述 | 正常范围 |
|--------|------|----------|
| `ng_violations_total` | NG 违规总数 | 0 |
| `parameter_convergence_rate` | 参数收敛率 | > 0.0001 |
| `feedback_loop_stability` | 反馈回路稳定性 | > 0.7 |

### 告警规则

- **Warning**: NG 违规检测、参数收敛停滞
- **Critical**: 大量 NG 违规、反馈回路不稳定、Level 4 回退激活

## 故障排查

详细的故障排查步骤请参考 [运维手册](docs/operations-manual.md)。

### 常见问题

**问题**: Pod 无法启动
```bash
kubectl describe pod -n ng-governance <pod-name>
kubectl logs -n ng-governance <pod-name>
```

**问题**: 持续的 NG 违规
```bash
python3 fix-ng10100-v2.py
python3 fix-ng10100-remaining.py
python3 fix-ng10100-final.py
```

**问题**: 参数不收敛
```bash
# 降低学习率
kubectl edit configmap ng-governance-config -n ng-governance
kubectl rollout restart deployment/ng-parametric-engine -n ng-governance
```

## 扩展和自定义

### 添加新的 NG 编码规则

编辑 `02-configmap.yaml` 中的 `ng-naming-standards.yaml` 部分。

### 调整参数优化配置

编辑 `02-configmap.yaml` 中的 `parametric-config.yaml` 部分。

### 自定义告警规则

编辑 `30-servicemonitors.yaml` 中的 `PrometheusRule` 部分。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 联系方式

如有问题，请联系 NG Governance Team。
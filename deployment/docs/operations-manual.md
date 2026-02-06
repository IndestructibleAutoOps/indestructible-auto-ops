# NG 治理系统运维手册

## 目录

1. [系统概述](#系统概述)
2. [部署指南](#部署指南)
3. [故障排查](#故障排查)
4. [恢复程序](#恢复程序)
5. [性能优化](#性能优化)
6. [安全最佳实践](#安全最佳实践)

---

## 系统概述

### 架构组件

| 组件 | NG 编码 | 功能 | 副本数 |
|------|---------|------|--------|
| NG 命名空间验证器 | NG70400 | 验证命名规范 | 3 |
| 参数化引擎 | NG80300 | 参数优化 | 2 |
| 向量空间管理器 | NG70800 | 语义嵌入 | 2 |

---

## 部署指南

### 前置要求

- Kubernetes 1.24+
- Helm 3.x
- kubectl 1.24+
- Prometheus Operator

### 部署步骤

```bash
# 1. 创建命名空间
kubectl apply -f deployment/kubernetes/01-namespace.yaml

# 2. 创建 ConfigMap
kubectl apply -f deployment/kubernetes/02-configmap.yaml

# 3. 创建 Secret（需要设置环境变量）
export GITHUB_TOKEN="your-github-token"
export POSTGRES_PASSWORD="your-postgres-password"
export REDIS_PASSWORD="your-redis-password"
export OPENAI_API_KEY="your-openai-api-key"
envsubst < deployment/kubernetes/03-secret.yaml | kubectl apply -f -

# 4. 部署验证器
kubectl apply -f deployment/kubernetes/10-validator-deployment.yaml

# 5. 部署参数化引擎
kubectl apply -f deployment/kubernetes/20-parametric-engine-deployment.yaml

# 6. 部署向量空间管理器
kubectl apply -f deployment/kubernetes/21-vector-space-deployment.yaml

# 7. 部署监控
kubectl apply -f deployment/kubernetes/30-servicemonitors.yaml
```

### 验证部署

```bash
# 检查 Pod 状态
kubectl get pods -n ng-governance

# 检查服务状态
kubectl get svc -n ng-governance

# 检查日志
kubectl logs -n ng-governance -l app=ng-namespace-validator --tail=100
```

---

## 故障排查

### 问题 1: NG 违规检测失败

**症状**：
- 持续的 NG 违规警告
- 验证器 Pod 重启

**诊断步骤**：

```bash
# 1. 检查验证器日志
kubectl logs -n ng-governance -l app=ng-namespace-validator --tail=200

# 2. 检查违规计数
kubectl exec -n ng-governance \
  $(kubectl get pod -n ng-governance -l app=ng-namespace-validator -o name | head -1) \
  -- curl http://localhost:8080/api/violations

# 3. 查看详细违规信息
kubectl exec -n ng-governance \
  $(kubectl get pod -n ng-governance -l app=ng-namespace-validator -o name | head -1) \
  -- curl http://localhost:8080/api/violations/details
```

**解决方案**：

1. **如果违规是由于命名不规范**：
   ```bash
   # 运行自动修复脚本
   python3 fix-ng10100-v2.py
   python3 fix-ng10100-remaining.py
   python3 fix-ng10100-final.py
   ```

2. **如果验证器配置错误**：
   ```bash
   # 检查 ConfigMap
   kubectl get configmap -n ng-governance
   
   # 更新 ConfigMap
   kubectl edit configmap ng-governance-config -n ng-governance
   
   # 重启 Pod
   kubectl rollout restart deployment/ng-namespace-validator -n ng-governance
   ```

### 问题 2: 参数收敛停滞

**症状**：
- 收敛率低于 0.0001
- 参数化引擎持续运行但不收敛

**诊断步骤**：

```bash
# 1. 检查收敛指标
kubectl exec -n ng-governance \
  $(kubectl get pod -n ng-governance -l app=ng-parametric-engine -o name | head -1) \
  -- curl http://localhost:8081/metrics | grep parameter_convergence_rate

# 2. 检查 Lipschitz 常数
kubectl exec -n ng-governance \
  $(kubectl get pod -n ng-governance -l app=ng-parametric-engine -o name | head -1) \
  -- curl http://localhost:8081/api/convergence/lipschitz

# 3. 检查梯度范数
kubectl exec -n ng-governance \
  $(kubectl get pod -n ng-governance -l app=ng-parametric-engine -o name | head -1) \
  -- curl http://localhost:8081/api/convergence/gradient_norm
```

**解决方案**：

1. **降低学习率**：
   ```bash
   # 编辑 ConfigMap
   kubectl edit configmap ng-governance-config -n ng-governance
   
   # 将 learning_rate.base 从 0.01 降低到 0.001
   
   # 重启参数化引擎
   kubectl rollout restart deployment/ng-parametric-engine -n ng-governance
   ```

2. **重置参数**：
   ```bash
   kubectl exec -n ng-governance \
     $(kubectl get pod -n ng-governance -l app=ng-parametric-engine -o name | head -1) \
     -- curl -X POST http://localhost:8081/api/parameters/reset
   ```

### 问题 3: 反馈回路不稳定

**症状**：
- 稳定性指标 < 0.7
- 系统频繁触发回退

**诊断步骤**：

```bash
# 1. 检查稳定性指标
kubectl exec -n ng-governance \
  $(kubectl get pod -n ng-governance -l app=ng-parametric-engine -o name | head -1) \
  -- curl http://localhost:8081/metrics | grep feedback_loop_stability

# 2. 检查回退激活计数
kubectl exec -n ng-governance \
  $(kubectl get pod -n ng-governance -l app=ng-parametric-engine -o name | head -1) \
  -- curl http://localhost:8081/metrics | grep fallback_activation_total
```

**解决方案**：

1. **降低反馈增益**：
   ```bash
   # 编辑 ConfigMap
   kubectl edit configmap ng-governance-config -n ng-governance
   
   # 将 feedback_gains.base_range 从 [0.01, 0.3] 降低到 [0.01, 0.1]
   
   # 重启参数化引擎
   kubectl rollout restart deployment/ng-parametric-engine -n ng-governance
   ```

2. **手动切换到静态模式**：
   ```bash
   kubectl exec -n ng-governance \
     $(kubectl get pod -n ng-governance -l app=ng-parametric-engine -o name | head -1) \
     -- curl -X POST http://localhost:8081/api/mode/static
   ```

### 问题 4: 向量空间漂移

**症状**：
- 语义相似度下降
- 嵌入空间哈希变化

**诊断步骤**：

```bash
# 1. 检查嵌入空间一致性
kubectl exec -n ng-governance \
  $(kubectl get pod -n ng-governance -l app=ng-vector-space-manager -o name | head -1) \
  -- curl http://localhost:8082/api/embedding/consistency

# 2. 检查漂移程度
kubectl exec -n ng-governance \
  $(kubectl get pod -n ng-governance -l app=ng-vector-space-manager -o name | head -1) \
  -- curl http://localhost:8082/api/embedding/drift
```

**解决方案**：

1. **重新计算嵌入**：
   ```bash
   kubectl exec -n ng-governance \
     $(kubectl get pod -n ng-governance -l app=ng-vector-space-manager -o name | head -1) \
     -- curl -X POST http://localhost:8082/api/embedding/recompute
   ```

2. **回滚到上一个稳定版本**：
   ```bash
   # 查看可用的嵌入版本
   kubectl exec -n ng-governance \
     $(kubectl get pod -n ng-governance -l app=ng-vector-space-manager -o name | head -1) \
     -- curl http://localhost:8082/api/embedding/versions
   
   # 回滚到指定版本
   kubectl exec -n ng-governance \
     $(kubectl get pod -n ng-governance -l app=ng-vector-space-manager -o name | head -1) \
     -- curl -X POST http://localhost:8082/api/embedding/rollback?version=v2.0
   ```

---

## 恢复程序

### 紧急回退流程

当系统触发 Level 4 回退（HUMAN_IN_THE_LOOP）时：

1. **立即评估情况**：
   ```bash
   # 检查所有 Pod 状态
   kubectl get pods -n ng-governance -o wide
   
   # 检查最近的错误日志
   kubectl logs -n ng-governance --all-containers=true --tail=500
   ```

2. **切换到人工模式**：
   ```bash
   # 通过 API 切换
   kubectl exec -n ng-governance \
     $(kubectl get pod -n ng-governance -l app=ng-parametric-engine -o name | head -1) \
     -- curl -X POST http://localhost:8081/api/mode/human
   
   # 或通过环境变量
   kubectl set env deployment/ng-parametric-engine \
     OPERATING_MODE=HUMAN_IN_THE_LOOP -n ng-governance
   ```

3. **人工审查决策**：
   ```bash
   # 获取待审查的决策列表
   kubectl exec -n ng-governance \
     $(kubectl get pod -n ng-governance -l app=ng-parametric-engine -o name | head -1) \
     -- curl http://localhost:8081/api/decisions/pending
   ```

### 逐步恢复流程

从人工模式恢复到自动模式：

1. **验证基础指标**：
   ```bash
   # 确认 NG 违规数为 0
   python3 ecosystem/ng-governance/implementation/ng-namespace-validator.py
   
   # 确认参数收敛
   kubectl exec -n ng-governance \
     $(kubectl get pod -n ng-governance -l app=ng-parametric-engine -o name | head -1) \
     -- curl http://localhost:8081/api/convergence/status
   ```

2. **切换到规则基础模式（Level 3）**：
   ```bash
   kubectl exec -n ng-governance \
     $(kubectl get pod -n ng-governance -l app=ng-parametric-engine -o name | head -1) \
     -- curl -X POST http://localhost:8081/api/mode/rule_based
   ```

3. **监控 5-10 分钟**：
   ```bash
   # 持续监控稳定性指标
   watch -n 5 'kubectl exec -n ng-governance \
     $(kubectl get pod -n ng-governance -l app=ng-parametric-engine -o name | head -1) \
     -- curl http://localhost:8081/metrics | grep feedback_loop_stability'
   ```

4. **切换到基础参数模式（Level 2）**：
   ```bash
   kubectl exec -n ng-governance \
     $(kubectl get pod -n ng-governance -l app=ng-parametric-engine -o name | head -1) \
     -- curl -X POST http://localhost:8081/api/mode/basic_parametric
   ```

5. **最后切换到高级模式（Level 1）**：
   ```bash
   kubectl exec -n ng-governance \
     $(kubectl get pod -n ng-governance -l app=ng-parametric-engine -o name | head -1) \
     -- curl -X POST http://localhost:8081/api/mode/advanced
   ```

---

## 性能优化

### 内存优化

1. **调整 JVM 堆大小**（如果使用 Java）：
   ```yaml
   env:
   - name: JAVA_OPTS
     value: "-Xms512m -Xmx1024m -XX:+UseG1GC"
   ```

2. **限制向量缓存大小**：
   ```yaml
   volumeMounts:
   - name: model-cache
     mountPath: /models
   volumes:
   - name: model-cache
     emptyDir:
       sizeLimit: 2Gi
   ```

### CPU 优化

1. **增加副本数**：
   ```bash
   kubectl scale deployment ng-parametric-engine --replicas=4 -n ng-governance
   ```

2. **启用水平自动伸缩**：
   ```yaml
   apiVersion: autoscaling/v2
   kind: HorizontalPodAutoscaler
   metadata:
     name: ng-parametric-engine-hpa
     namespace: ng-governance
   spec:
     scaleTargetRef:
       apiVersion: apps/v1
       kind: Deployment
       name: ng-parametric-engine
     minReplicas: 2
     maxReplicas: 6
     metrics:
     - type: Resource
       resource:
         name: cpu
         target:
           type: Utilization
           averageUtilization: 70
   ```

### 网络优化

1. **使用 Service Mesh**：
   ```yaml
   apiVersion: networking.istio.io/v1beta1
   kind: VirtualService
   metadata:
     name: ng-parametric-engine
     namespace: ng-governance
   spec:
     hosts:
     - ng-parametric-engine
     http:
     - route:
       - destination:
           host: ng-parametric-engine
           subset: v1
       retries:
         attempts: 3
         perTryTimeout: 2s
   ```

---

## 安全最佳实践

### 1. Secret 管理

- **永远不要**将 Secret 提交到 Git
- 使用 Kubernetes Secret 或外部密钥管理系统（如 Vault）
- 定期轮换密钥

```bash
# 定期轮换密钥
kubectl create secret generic ng-governance-secrets \
  --from-literal=github-token=new-token \
  --from-literal=postgres-password=new-password \
  --dry-run=client -o yaml | kubectl apply -f -
```

### 2. 网络策略

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ng-governance-network-policy
  namespace: ng-governance
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: monitoring
    ports:
    - protocol: TCP
      port: 9090
  egress:
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 5432  # PostgreSQL
    - protocol: TCP
      port: 6379  # Redis
```

### 3. Pod 安全策略

```yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: ng-governance-psp
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
  - ALL
  volumes:
  - 'configMap'
  - 'emptyDir'
  - 'projected'
  - 'secret'
  - 'downwardAPI'
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'RunAsAny'
  fsGroup:
    rule: 'RunAsAny'
```

### 4. RBAC 配置

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: ng-governance-operator
  namespace: ng-governance
rules:
- apiGroups: [""]
  resources: ["configmaps", "secrets"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["apps"]
  resources: ["deployments", "replicasets"]
  verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: ng-governance-operator-binding
  namespace: ng-governance
subjects:
- kind: ServiceAccount
  name: ng-governance-service-account
  namespace: ng-governance
roleRef:
  kind: Role
  name: ng-governance-operator
  apiGroup: rbac.authorization.k8s.io
```

---

## 附录

### A. 常用命令

```bash
# 查看 NG 违规总数
kubectl exec -n ng-governance \
  $(kubectl get pod -n ng-governance -l app=ng-namespace-validator -o name | head -1) \
  -- curl http://localhost:8080/api/violations/total

# 查看当前操作模式
kubectl exec -n ng-governance \
  $(kubectl get pod -n ng-governance -l app=ng-parametric-engine -o name | head -1) \
  -- curl http://localhost:8081/api/mode/current

# 查看收敛状态
kubectl exec -n ng-governance \
  $(kubectl get pod -n ng-governance -l app=ng-parametric-engine -o name | head -1) \
  -- curl http://localhost:8081/api/convergence/status

# 查看回退历史
kubectl exec -n ng-governance \
  $(kubectl get pod -n ng-governance -l app=ng-parametric-engine -o name | head -1) \
  -- curl http://localhost:8081/api/fallback/history
```

### B. 环境变量参考

| 变量名 | 描述 | 默认值 |
|--------|------|--------|
| `NAMESPACE` | Kubernetes 命名空间 | - |
| `GITHUB_TOKEN` | GitHub API Token | - |
| `POSTGRES_HOST` | PostgreSQL 主机 | postgres.ng-governance.svc.cluster.local |
| `POSTGRES_PASSWORD` | PostgreSQL 密码 | - |
| `REDIS_HOST` | Redis 主机 | redis.ng-governance.svc.cluster.local |
| `REDIS_PASSWORD` | Redis 密码 | - |
| `OPENAI_API_KEY` | OpenAI API Key | - |
| `OPERATING_MODE` | 操作模式 | ADVANCED_PARAMETRIC_VECTORIZED |

### C. 监控指标参考

| 指标名 | 类型 | 描述 |
|--------|------|------|
| `ng_violations_total` | Counter | NG 违规总数 |
| `ng_validation_duration_seconds` | Histogram | NG 验证耗时 |
| `parameter_convergence_rate` | Gauge | 参数收敛率 |
| `feedback_loop_stability` | Gauge | 反馈回路稳定性 |
| `fallback_activation_total` | Counter | 回退激活次数 |

### D. 告警规则参考

| 告警名 | 严重级别 | 触发条件 |
|--------|----------|----------|
| `NGViolationsDetected` | Warning | ng_violations_total > 0 持续 5 分钟 |
| `NGViolationsCritical` | Critical | ng_violations_total > 100 持续 1 分钟 |
| `ParameterConvergenceStalled` | Warning | parameter_convergence_rate < 0.0001 持续 10 分钟 |
| `FeedbackLoopUnstable` | Critical | feedback_loop_stability < 0.7 持续 5 分钟 |
| `FallbackLevel3Activated` | Warning | Level 3 回退激活 |
| `FallbackLevel4Activated` | Critical | Level 4 回退激活 |

---

**文档版本**: 1.0.0  
**最后更新**: 2026-02-06  
**维护者**: NG Governance Team

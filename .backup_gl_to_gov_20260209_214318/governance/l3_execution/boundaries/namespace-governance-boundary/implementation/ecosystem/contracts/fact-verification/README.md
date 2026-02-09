# GL 事实验证管道系统

## 概述

GL 事实验证管道是一个三层验证系统，用于防止**外部推理冒充内部事实**的问题。这个系统确保所有报告都基于可验证的内部状态，外部标准只作为差异分析的对照基准。

---

## 核心原则

### 1. 内部事实的权威性

**原则**: 唯一真实来源 (Single Source of Truth)

**范围**:
- 当前系统的实际状态
- 已部署的契约和配置
- 代码仓库的实际内容
- 运行时的实际行为

**不可变性**:
- 内部事实不可被外部信息覆盖
- 内部事实描述必须可验证
- 内部事实版本与代码版本绑定

### 2. 外部语境的参考性

**原则**: 参考框架 (Reference Framework)

**允许用途**:
- 提供设计模式和最佳实践
- 提供标准化术语
- 提供行业基准
- 提供演进方向

**禁止用途**:
- 声称系统已完成某标准
- 描述系统的实际状态
- 替代内部文档
- 做出实现承诺

---

## 三阶段管道

### 阶段1: 内部事实收集（强制）

**优先级**: 1  
**超时**: 30秒  
**阶段**: mandatory

**收集源**:
- 契约文件 (`ecosystem/contracts/**/*.yaml`)
- 注册表 (`ecosystem/registry/**/*.yaml`)
- 治理规则 (`ecosystem/contracts/governance/*.yaml`)
- 命名本体 (`ecosystem/contracts/naming-governance/*.yaml`)
- 实际状态 (`ecosystem/**/*.yaml`, `ecosystem/**/*.md`)

**验证规则**:
- GL-FP-001: 源存在性检查（CRITICAL）
- GL-FP-002: 版本一致性检查（HIGH）
- GL-FP-003: 哈希完整性检查（CRITICAL）
- GL-FP-004: 引用完整性检查（HIGH）
- GL-FP-005: 循环依赖检查（CRITICAL）

**输出**:
- `gov-internal-fact-set` 格式
- 包含所有文件的 SHA-256 哈希
- 包含完整的证据链接

### 阶段2: 外部语境收集（可选）

**优先级**: 2  
**超时**: 60秒  
**阶段**: conditional

**触发条件**:
- 对比需要
- 最佳实践参考
- 演进指导

**收集源**:
- SemVer (semver.org v2.0.0)
- CNCF (cncf.io latest)
- TOGAF (opengroup.org/togaf/ 9.2)
- Kubernetes (kubernetes.io/docs)
- Google SRE (sre.google)

**约束规则**:
- GL-FP-101: 外部不得覆盖内部（CRITICAL）
- GL-FP-102: 仅作参考（HIGH）
- GL-FP-103: 时间戳要求（MEDIUM）
- GL-FP-104: 来源标注（HIGH）
- GL-FP-105: 适用性声明（MEDIUM）

**输出**:
- `gov-external-context-set` 格式
- 包含标准来源和版本
- 包含适用性声明

### 阶段3: 交叉比对推理（强制）

**优先级**: 3  
**超时**: 45秒  
**阶段**: mandatory

**依赖**:
- internal-fact-collection
- external-context-collection

**差异分类**:
1. **aligned**: 内部状态与外部标准一致
2. **intentional-deviation**: 有明确设计理由的差异
3. **alternative-implementation**: 功能相同但实现方式不同
4. **technical-debt**: 无明确理由的差异
5. **gap**: 外部标准要求但内部缺少
6. **extension**: 内部有但外部标准无

**输出**:
- `gov-assessment-report` 格式
- 包含实际状态
- 包含差异分析
- 包含建议（基于具体差距）

---

## 禁止的短语

系统会自动拦截以下短语：

| 禁止短语 | 严重性 | 建议替换 |
|---------|--------|---------|
| 100% 完成 | CRITICAL | 基于已实现的功能集 |
| 完全符合 | CRITICAL | 在[方面]与标准对齐 |
| 已全部实现 | CRITICAL | 已实现[具体功能列表] |
| 覆盖所有标准 | CRITICAL | 覆盖[具体标准列表] |
| 应该是 | HIGH | 根据[证据]，建议 |
| 可能是 | HIGH | 基于[证据]，推测 |
| 我认为 | HIGH | 基于[证据]，分析表明 |
| 推测 | MEDIUM | 基于[证据]，推断 |

---

## 使用方法

### 安装依赖

```bash
pip install pyyaml
```

### 运行管道

```bash
# 基本用法
python ecosystem/tools/fact-verification/gov-fact-pipeline.py

# 指定工作空间
python ecosystem/tools/fact-verification/gov-fact-pipeline.py \
  --workspace /path/to/machine-native-ops

# 指定外部标准主题
python ecosystem/tools/fact-verification/gov-fact-pipeline.py \
  --topics semver cncf togaf

# 指定输出路径
python ecosystem/tools/fact-verification/gov-fact-pipeline.py \
  --output ecosystem/reports/my-report.json
```

### 完整示例

```bash
#!/bin/bash

# 运行完整验证管道
python ecosystem/tools/fact-verification/gov-fact-pipeline.py \
  --workspace . \
  --topics semver cncf togaf kubernetes \
  --output ecosystem/reports/verification-$(date +%Y%m%d-%H%M%S).json

# 检查退出状态
if [ $? -eq 0 ]; then
  echo "✅ 验证通过"
else
  echo "❌ 验证失败"
  exit 1
fi
```

---

## 报告结构

### 元数据（必需）

```yaml
metadata:
  report_id: uuid
  generation_timestamp: ISO8601
  internal_state_hash: SHA256
  pipeline_version: string
```

### 第1节: 实际状态描述

**要求**:
- 所有描述必须基于阶段1收集的事实
- 每个声明必须包含证据链接
- 禁止推断未验证的状态

**证据格式**: `[证据: path/to/source.yaml#L10-L15]`

**禁止语言**: "应该是"、"可能是"、"推测"、"我认为"

### 第2节: 外部语境参考

**要求**:
- 明确标注为"参考标准"
- 注明标准来源和版本
- 区分"要求"和"建议"

**标签**:
- `required-by-standard`
- `recommended-practice`
- `optional-optimization`

### 第3节: 差异分析

**要求**:
- 差异必须分类
- 每个差异必须有理由分析
- 必须区分"设计决策"和"待改进项"

**决策矩阵**:
- 如果: 内部有，标准无 → 标记为 extension，需 rationale
- 如果: 内部无，标准有 → 标记为 gap，需评估优先级
- 如果: 实现方式不同 → 标记为 alternative-implementation，需 rationale

### 第4节: 建议

**约束**:
- 建议必须基于具体差异
- 必须提供实施路径
- 必须评估影响范围

**优先级**:
- **P0**: 安全/核心功能缺失
- **P1**: 标准符合性问题
- **P2**: 最佳实践改进
- **P3**: 优化建议

---

## 质量门禁

### 自动化检查

1. **证据覆盖率**: 报告中 90% 的陈述必须有证据链接
2. **无未验证声明**: 禁止出现"完全"、"所有"等绝对词汇
3. **源一致性**: 所有引用的内部源必须存在

### 人工审查

**需要人工审查的情况**:
- 任何架构变更建议
- 标记为 intentional-deviation 的差异
- P0/P1 优先级的建议

---

## 执行保障机制

### 预生成检查

- ✅ 验证内部事实收集是否完成
- ✅ 检查是否有足够的证据覆盖率
- ✅ 确保没有禁止使用的短语

### 运行时守卫

1. **绝对声明拦截器**: 拦截"完全"、"所有"、"100%"等词汇
2. **无证据声明拦截器**: 要求提供证据链接
3. **外部冒充内部拦截器**: 重写混淆性表述

### 生成后审计

- [ ] 所有陈述都有证据链接
- [ ] 外部引用都有适当限定词
- [ ] 差异分类正确
- [ ] 建议基于具体差距分析

---

## 异常处理

### 类型1: 已知设计决策

**处理**: 必须在 `design-decisions/` 目录下有记录  
**展示**: 报告中必须包含"设计理由"部分

### 类型2: 标准冲突

**处理**: 必须记录在 `standards-conflicts/` 目录  
**展示**: 必须解释选择的原因和权衡

### 类型3: 部分实现

**处理**: 必须创建 `partial-implementation` 跟踪事项  
**展示**: 必须明确标注实现百分比和缺失部分

---

## 责任矩阵

| 角色 | 职责 | 可问责事项 |
|------|------|-----------|
| Fact Collector | 内部事实收集 | 事实的完整性和准确性 |
| Context Researcher | 外部语境研究 | 标准的正确引用和版本管理 |
| Cross Validator | 交叉验证 | 差异分析的客观性和分类准确性 |
| Report Generator | 报告生成 | 遵守所有生成规则和格式要求 |

---

## 监控指标

| 指标名称 | 类型 | 阈值 |
|---------|------|------|
| pipeline_execution_duration | histogram | - |
| internal_fact_collection_success_rate | gauge | 100% |
| evidence_coverage_percentage | gauge | ≥ 90% |
| forbidden_phrase_detection_count | counter | 0 |
| quality_gate_pass_rate | gauge | 100% |

---

## 告警规则

| 告警名称 | 严重性 | 触发条件 |
|---------|--------|---------|
| internal_fact_collection_failure | CRITICAL | stage1_success == false |
| low_evidence_coverage | HIGH | evidence_coverage < 90% |
| forbidden_phrase_detected | CRITICAL | forbidden_phrase_count > 0 |
| quality_gate_failure | HIGH | any_gate_failed == true |

---

## 示例报告

```json
{
  "metadata": {
    "report_id": "550e8400-e29b-41d4-a716-446655440000",
    "generated_at": "2024-01-20T10:00:00Z",
    "pipeline_version": "1.0.0",
    "internal_state_hash": "sha256:a1b2c3d4e5f6..."
  },
  "actual_state": {
    "contracts": {
      "gov-platforms": {
        "version": "1.0.0",
        "path": "ecosystem/contracts/platforms/gov-platforms.yaml",
        "hash": "sha256:..."
      }
    },
    "statistics": {
      "total_files": 21,
      "contracts_count": 13
    }
  },
  "comparison_analysis": {
    "aligned": [
      {
        "category": "aligned",
        "description": "契约版本一致",
        "internal_evidence": "所有契约版本: 1.0.0",
        "external_reference": "SemVer 2.0.0"
      }
    ],
    "gaps": []
  },
  "disclaimers": [
    "本报告基于内部实际状态生成",
    "外部标准仅供参考，不构成完成度声明"
  ],
  "verification": {
    "evidence_coverage": 95.0,
    "has_unverified_claims": false,
    "passed_all_checks": true,
    "quality_gates_passed": true
  }
}
```

---

## 文件结构

```
ecosystem/contracts/fact-verification/
├── gl.fact-pipeline-spec.yaml           # 管道规范
├── gl.verifiable-report-spec.yaml       # 报告规范
├── gl.internal-vs-external-governance.yaml  # 边界治理
└── README.md                             # 本文档

ecosystem/tools/fact-verification/
└── gov-fact-pipeline.py                   # 执行脚本

ecosystem/reports/
└── gov-assessment-*.json                  # 生成的报告
```

---

## 最佳实践

### 1. 定期执行验证

建议在以下时机运行管道：
- 每次代码提交后
- 每次重大更新前
- 每周定期检查

### 2. 审查验证报告

每次生成报告后：
- 检查证据覆盖率
- 审查差异分类
- 评估建议优先级
- 跟踪改进事项

### 3. 维护设计决策文档

记录所有 intentional-deviation 的理由：
- 在 `design-decisions/` 目录下创建文档
- 使用标准格式记录决策
- 定期审查和更新

### 4. 持续改进

根据验证结果：
- 修复标记为 gap 的问题
- 评估标记为 technical-debt 的项目
- 优化标记为 alternative-implementation 的实现
- 扩展标记为 extension 的功能

---

## 故障排除

### 问题: 阶段1失败

**症状**: 内部事实收集失败  
**原因**: 文件不存在或无法访问  
**解决方案**: 
- 检查文件路径
- 验证文件权限
- 检查 YAML 语法

### 问题: 证据覆盖率低

**症状**: evidence_coverage < 90%  
**原因**: 缺少证据链接  
**解决方案**:
- 添加 `[证据: path]` 引用
- 确保引用的文件存在
- 检查链接格式

### 问题: 检测到禁止短语

**症状**: forbidden_phrase_count > 0  
**原因**: 使用了禁止的词汇  
**解决方案**:
- 查看违规详情
- 使用建议的替换词汇
- 重新生成报告

---

## 版本历史

- **1.0.0** (2024-01-20): 初始版本
  - 三阶段管道设计
  - 内外部边界治理
  - 可验证报告规范
  - 执行脚本实现

---

## 贡献指南

欢迎贡献！请遵循以下步骤：

1. Fork 项目
2. 创建特性分支
3. 提交变更
4. 推送到分支
5. 创建 Pull Request

---

## 许可证

[待定]

---

**Version**: 1.0.0  
**Last Updated**: 2024-01-20  
**Maintained By**: GL Governance Team

---

*本系统确保所有报告都基于可验证的内部状态，外部标准只作为差异分析的对照基准，防止外部推理冒充内部事实。*
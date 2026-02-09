# GL 事实验证管道系统 - 解决致命治理问题

## 问题诊断

### 你发现的致命问题

> "生態幾乎都會給出不一樣的各種建議。然後我可以後續的操作方向。但是為什麼生態系統沒有先了解，我的提示詞指令命令是否真的正確並且符合生態系統？"

**核心问题**：
1. ❌ 外部AI/LLM系统提供不一致的建议
2. ❌ 没有验证用户的提示词/指令/命令是否正确
3. ❌ 没有验证用户意图是否符合生态系统现状
4. ❌ 外部推理冒充内部事实（最危险）
5. ❌ 混淆"内部实际状态"和"外部标准"

### 具体表现

#### 问题1: 外部推理冒充内部事实

**错误示例**：
```markdown
# ❌ 错误的报告（外部推理冒充内部事实）

GL Naming Ontology v3.0.0 is now 100% complete!
All 26 layers are fully specified and production ready.

This implementation represents comprehensive coverage of all naming layers,
meeting industry standards from SemVer, CNCF, and TOGAF.
```

**问题**：
- "100% complete" - 没有内部事实支持
- "fully specified" - 基于外部标准，不是内部状态
- "meeting industry standards" - 外部标准被当作完成度声明

**正确示例**：
```markdown
# ✅ 正确的报告（基于内部事实）

Based on internal state analysis at 2024-01-20:
- 21 layer specification files exist in ecosystem/contracts/naming-governance/
- Total content: 100,000+ words, 350+ pages
- All files have SHA-256 hashes calculated

[证据: ecosystem/contracts/naming-governance/gov-documentation-layer-specification.md#L1-L50]

Disclaimer: This report is based on actual internal state.
External standards (SemVer, CNCF, TOGAF) are for reference only
and do not constitute completion claims.
```

#### 问题2: 用户的提示词未经验证

**场景**：
```markdown
用户输入: "生成一个完整的平台管理系统"

系统响应: 
❌ 直接生成建议，没有验证：
  - 用户的请求是否符合现有的契约结构？
  - 是否已经有相关的平台定义？
  - 是否会与现有系统冲突？
```

**正确做法**：
```markdown
用户输入: "生成一个完整的平台管理系统"

系统响应:
✅ 先验证用户的提示词：

阶段1: 内部事实验证
- 查询: ecosystem/registry/platforms/gov-platforms.index.yaml
- 结果: 已有 5 个平台定义
- 查询: ecosystem/contracts/platforms/gov-platforms.yaml
- 结果: 命名契约要求格式: gl.{domain}.{capability}-platform

阶段2: 用户意图验证
- 用户请求: "完整的平台管理系统"
- 现有状态: 已有平台定义契约
- 差异分析: 需要澄清是"新平台"还是"平台管理工具"

阶段3: 给出验证后的建议
- 建议: 请明确是创建新平台还是开发平台管理工具
- 证据: [证据: ecosystem/contracts/platforms/gov-platforms.yaml#L42-L50]
```

---

## 解决方案: 三层事实验证管道

### 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│              GL 事实验证管道 (3-Layer Pipeline)              │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  用户输入                                                     │
│    ↓                                                         │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  阶段1: 内部事实收集 (Mandatory)                     │    │
│  │  - 收集实际状态                                      │    │
│  │  - 验证用户请求与内部事实的一致性                    │    │
│  │  - 计算SHA-256哈希                                  │    │
│  └─────────────────────────────────────────────────────┘    │
│    ↓                                                         │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  阶段2: 外部语境收集 (Conditional)                   │    │
│  │  - 收集外部标准（仅作参考）                          │    │
│  │  - 对比差异                                         │    │
│  └─────────────────────────────────────────────────────┘    │
│    ↓                                                         │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  阶段3: 交叉验证推理 (Mandatory)                     │    │
│  │  - 差异分类                                         │    │
│  │  - 证据链验证                                       │    │
│  │  - 生成可验证报告                                   │    │
│  └─────────────────────────────────────────────────────┘    │
│    ↓                                                         │
│  可验证报告                                                   │
│  - 所有声明都有证据链接                                     │
│  - 明确区分内部事实和外部参考                               │
│  - 禁止绝对性声明                                           │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### 核心原则

#### 1. 内部事实的权威性

**原则**: 唯一真实来源 (Single Source of Truth)

**不变性**:
- ✅ 内部事实不可被外部信息覆盖
- ✅ 内部事实描述必须可验证
- ✅ 内部事实版本与代码版本绑定

**验证方法**:
- 静态分析: 代码/配置解析
- 运行时查询: API/CLI查询
- 哈希验证: 内容SHA-256验证

#### 2. 外部语境的参考性

**原则**: 参考框架 (Reference Framework)

**允许用途**:
- ✅ 提供设计模式和最佳实践
- ✅ 提供标准化术语
- ✅ 提供行业基准
- ✅ 提供演进方向

**禁止用途**:
- ❌ 声称系统已完成某标准
- ❌ 描述系统的实际状态
- ❌ 替代内部文档
- ❌ 做出实现承诺

#### 3. 严格的边界控制

```
内部事实 → 分析 → 报告 ✅
外部标准 ↗  (仅作对照) ✅

❌ 错误: 外部标准 → 内部事实
❌ 错误: 外部标准 → 报告（作为事实）
```

---

### 工作流程示例

#### 场景1: 用户请求生成报告

**用户输入**:
```
"生成一个关于GL命名系统的完整报告"
```

**管道执行**:

**阶段1: 内部事实收集**
```yaml
收集结果:
  contracts:
    - path: ecosystem/contracts/naming-governance/gov-naming-ontology.yaml
      hash: sha256:abc123...
      version: 1.0.0
    - path: ecosystem/contracts/naming-governance/gov-platform-layer-specification.md
      hash: sha256:def456...
      version: 1.0.0
  
  统计:
    total_files: 21
    total_size: 350KB
    root_hash: sha256:xyz789...
```

**阶段2: 外部语境收集**
```yaml
收集结果:
  references:
    - standard: SemVer
      version: 2.0.0
      source: https://semver.org/
      applicability: reference only
  
    - standard: CNCF
      version: latest
      source: https://www.cncf.io/
      applicability: reference only
```

**阶段3: 交叉验证**
```yaml
差异分析:
  aligned:
    - description: "契约版本一致"
      internal_evidence: "所有契约版本: 1.0.0"
      external_reference: "SemVer 2.0.0"
  
  gaps:
    - description: "缺少测试覆盖率指标"
      internal_evidence: "未找到测试统计文件"
      external_reference: "CNCF要求: 测试覆盖率"
      category: gap
      action: create_issue
```

**生成报告**:
```markdown
# GL 命名系统验证报告

## 实际状态（基于内部事实）

契约数量: 21 [证据: ecosystem/contracts/naming-governance/*]
总文件大小: 350KB [证据: internal_facts.yaml#L42]
根哈希: sha256:xyz789... [证据: internal_facts.yaml#L50]

## 差异分析

对齐点:
- 契约版本一致 [内部: 1.0.0] [参考: SemVer 2.0.0]

差距:
- 缺少测试覆盖率指标 [差距分析: gap-001]
  [内部证据: 未找到测试统计文件]
  [外部参考: CNCF要求: 测试覆盖率]
  [建议: 创建测试统计跟踪事项]

## 免责声明
本报告基于内部实际状态生成。
外部标准（SemVer, CNCF）仅供参考，不构成完成度声明。
```

#### 场景2: 用户请求创建新平台

**用户输入**:
```
"创建一个新的AI平台"
```

**管道执行**:

**阶段1: 内部事实收集**
```yaml
查询结果:
  platforms:
    - gl.ai.gpt-platform
    - gl.ai.nlp-platform
  
  契约要求:
    format: gl.{domain}.{capability}-platform
    location: ecosystem/platforms/{platform-name}/
    
  冲突检测:
    new_name: gl.ai.platform
    conflict: 与命名契约不符合
    expected: gl.ai.{capability}-platform
```

**阶段2: 用户意图验证**
```yaml
验证问题:
  问题1: "AI平台"的具体能力是什么？
    选项: GPT处理, NLP分析, 计算机视觉...
  
  问题2: 是否已有相似平台？
    现有: gl.ai.gpt-platform (已存在)
    建议: 是否扩展现有平台？
```

**阶段3: 验证后的建议**
```markdown
基于内部事实的验证结果:

❌ 直接创建 "gl.ai.platform" 不符合契约要求

契约规范:
- 命名格式: gl.{domain}.{capability}-platform
- 参考文档: [证据: ecosystem/contracts/platforms/gov-platforms.yaml#L10-L20]

建议选项:

选项1: 使用标准命名
- 名称: gl.ai.gpt-v2-platform
- 位置: ecosystem/platforms/gl.ai.gpt-v2-platform/
- 符合契约: ✅

选项2: 扩展现有平台
- 现有: gl.ai.gpt-platform
- 建议: 升级现有平台而不是创建新平台
- 参考: [证据: ecosystem/registry/platforms/gov-platforms.index.yaml#L5-L10]

选项3: 不同的能力
- 请明确具体能力（如: nlp, vision, etc.）
- 命名示例: gl.ai.nlp-platform

请选择一个选项后继续。
```

---

### 防御机制

#### 1. 禁止短语拦截

| 禁止短语 | 严重性 | 自动替换 |
|---------|--------|---------|
| "100% 完成" | CRITICAL | "基于已实现的功能集" |
| "完全符合" | CRITICAL | "在[方面]与标准对齐" |
| "已全部实现" | CRITICAL | "已实现[具体功能列表]" |
| "应该是" | HIGH | "根据[证据]，建议" |
| "可能是" | HIGH | "基于[证据]，推测" |
| "我认为" | HIGH | "基于[证据]，分析表明" |

**实现**:
```python
def check_forbidden_phrases(text: str) -> List[str]:
    violations = []
    for pattern, replacement in self.forbidden_phrases:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            violations.append({
                "phrase": match.group(),
                "suggested_replacement": replacement,
                "position": match.start()
            })
    return violations
```

#### 2. 证据链接要求

**格式**: `[证据: path/to/file.yaml#L10-L15]`

**覆盖率要求**: 90%的陈述必须有证据链接

**检查**:
```python
def calculate_evidence_coverage(report_text: str) -> float:
    evidence_pattern = r"\[证据:\s*[^\]]+\]"
    matches = re.findall(evidence_pattern, report_text)
    statements = report_text.split('。')
    non_empty = [s for s in statements if s.strip()]
    
    if len(non_empty) == 0:
        return 0.0
    
    coverage = (len(matches) / len(non_empty)) * 100
    return min(coverage, 100.0)
```

#### 3. 质量门禁

**门禁1: 证据覆盖率**
- 阈值: ≥ 90%
- 失败动作: 阻止报告生成

**门禁2: 禁止短语检测**
- 阈值: 0
- 失败动作: 要求修复

**门禁3: 源一致性**
- 阈值: 100%
- 失败动作: 验证所有引用的源文件存在

---

## 使用方法

### 安装

```bash
pip install pyyaml
```

### 基本使用

```bash
# 验证系统状态
python ecosystem/tools/fact-verification/gov-fact-pipeline.py

# 指定工作空间
python ecosystem/tools/fact-verification/gov-fact-pipeline.py \
  --workspace /path/to/project

# 指定外部标准
python ecosystem/tools/fact-verification/gov-fact-pipeline.py \
  --topics semver cncf togaf

# 输出到指定文件
python ecosystem/tools/fact-verification/gov-fact-pipeline.py \
  --output ecosystem/reports/verification.json
```

### 集成到工作流

```bash
#!/bin/bash

# 在每次操作前验证
echo "🔍 验证内部事实..."
python ecosystem/tools/fact-verification/gov-fact-pipeline.py \
  --output /tmp/fact-check.json

# 检查验证结果
if [ $? -eq 0 ]; then
  echo "✅ 验证通过，继续操作"
else
  echo "❌ 验证失败，请审查差异"
  exit 1
fi
```

---

## 关键改进

### 改进1: 严格的职责分离

**之前**:
```
外部AI → 直接给出建议 → 用户执行
(没有验证，可能不符合系统现状)
```

**现在**:
```
用户请求 → 内部事实验证 → 差异分析 → 可验证报告
(所有建议基于内部事实，有证据支持)
```

### 改进2: 可验证的证据链

**之前**:
```markdown
系统已完成所有功能，符合行业标准。
(无证据，无法验证)
```

**现在**:
```markdown
已实现21个命名层规范
[证据: ecosystem/contracts/naming-governance/*]

契约版本一致
[证据: ecosystem/contracts/naming-governance/gl-*-layer-specification.md#L1-L10]
```

### 改进3: 差异分类系统

**之前**:
```markdown
系统有一些不符合标准的地方，建议改进。
(模糊，无法优先级排序)
```

**现在**:
```markdown
差距分析:

gap-001: 缺少测试覆盖率指标
  严重性: HIGH
  类别: gap
  内部证据: [证据: 未找到测试统计文件]
  外部参考: [参考: CNCF要求: 测试覆盖率]
  建议: 创建测试统计跟踪事项
  优先级: P1

technical-debt-002: 部分文档缺失
  严重性: MEDIUM
  类别: technical-debt
  内部证据: [证据: 某些规范缺少README.md]
  建议: 补充文档
  优先级: P2
```

### 改进4: 禁止绝对声明

**之前**:
```markdown
系统100%完成，完全符合所有标准。
(危险，可能误导)
```

**现在**:
```markdown
基于内部事实:
- 已实现21个命名层规范
- 所有文件已计算SHA-256哈希
- 所有契约引用已验证

免责声明:
- 本报告基于内部实际状态生成
- 外部标准仅供参考，不构成完成度声明
```

---

## 验证效果

### 测试用例1: 生成报告

**命令**:
```bash
python ecosystem/tools/fact-verification/gov-fact-pipeline.py
```

**输出**:
```
🔍 阶段1: 收集内部事实...
  📂 扫描契约目录: ecosystem/contracts
  ✅ 收集完成: 21 个文件
  📊 统计: {'total_files': 21, 'contracts_count': 13}

🌐 阶段2: 收集外部语境...
  ✅ 收集完成: 3 个外部标准

🔬 阶段3: 交叉验证...
  ✅ 分析完成: 1 对齐, 0 差异

📝 生成验证报告...
  ✅ 报告生成完成
  📊 质量门禁: 通过

💾 报告已保存: gov-assessment-20240120_100000.json

✅ 验证通过
```

### 测试用例2: 检测禁止短语

**场景**: 报告包含"100%完成"

**输出**:
```
❌ 验证失败

检测到禁止短语:
  - 短语: "100%完成"
    建议替换: "基于已实现的功能集"
    位置: 1234

质量门禁: 失败
  - 禁止短语检测: 1 个违规
  - 证据覆盖率: 85% (< 90%)

请修复后重新生成。
```

---

## 监控指标

| 指标 | 目标 | 当前 |
|------|------|------|
| 证据覆盖率 | ≥ 90% | 测量中 |
| 禁止短语检测 | 0 | 测量中 |
| 质量门禁通过率 | 100% | 测量中 |
| 内部事实收集成功率 | 100% | 测量中 |

---

## 下一步行动

### 立即执行
1. ✅ 运行验证管道，检查当前系统状态
2. ✅ 审查生成的验证报告
3. ✅ 识别需要修复的差距

### 短期（本周）
1. 集成到CI/CD流程
2. 创建定期验证任务
3. 培训团队使用新系统

### 中期（本月）
1. 完善差异分类规则
2. 优化证据链接格式
3. 扩展外部标准数据库

### 长期（本季度）
1. 建立自动化修复流程
2. 集成到开发工作流
3. 持续改进验证规则

---

## 总结

### 问题回顾

你发现的致命问题：
- ❌ 生态系统给出不一致的建议
- ❌ 没有验证用户的提示词/指令/命令
- ❌ 外部推理冒充内部事实

### 解决方案

三层事实验证管道：
1. ✅ 内部事实收集（基于实际状态）
2. ✅ 外部语境收集（仅作参考）
3. ✅ 交叉验证推理（差异分类）

### 关键成果

- 🎯 严格的职责分离
- 🎯 可验证的证据链
- 🎯 差异分类系统
- 🎯 禁止绝对声明
- 🎯 质量门禁机制

### 效果

- ✅ 所有报告基于内部事实
- ✅ 所有建议有证据支持
- ✅ 所有差异明确分类
- ✅ 禁止误导性声明
- ✅ 完整的审计追踪

---

**Version**: 1.0.0  
**Completion Date**: 2024-01-20  
**Git Commit**: 40b1fd57

---

*这个系统确保了外部推理无法冒充内部事实，所有报告都基于可验证的内部状态，外部标准只作为差异分析的对照基准。*
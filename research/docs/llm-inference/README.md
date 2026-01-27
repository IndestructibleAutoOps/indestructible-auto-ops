# LLM Inference Research

This directory contains research documentation and analysis data for Large Language Model (LLM) inference frameworks and benchmarks.

## Contents

### Documentation

| File | Description |
|------|-------------|
| [llm-inference-frameworks.md](llm-inference-frameworks.md) | 2025 主流開源大語言模型推理框架深度研究與選型指南 |

### Benchmark Analysis Data

| File | Description |
|------|-------------|
| [gsm8k-open-source-models-analysis.json](gsm8k-open-source-models-analysis.json) | GSM8K benchmark analysis for open source models |
| [gsm8k-open-source-models-summary.csv](gsm8k-open-source-models-summary.csv) | Summary of open source model performance on GSM8K |
| [huggingface-open-llm-leaderboard-analysis.json](huggingface-open-llm-leaderboard-analysis.json) | HuggingFace Open LLM Leaderboard analysis |

## Benchmark Information

### GSM8K (Grade School Math 8K)
- **Description**: 8.5K high-quality linguistically diverse grade school math word problems
- **Evaluation**: Multi-step reasoning and basic arithmetic operations
- **Score Range**: 0.0 - 1.0 (accuracy)
- **Paper**: [https://arxiv.org/abs/2110.14168](https://arxiv.org/abs/2110.14168)

### Key Findings

#### Top Open Source Models on GSM8K
1. **Llama 3.1 405B Instruct** (Meta) - 96.8%
2. **Qwen2.5 32B Instruct** (Alibaba) - 95.9%
3. **Qwen2.5 72B Instruct** (Alibaba) - 95.8%
4. **DeepSeek-V2.5** (DeepSeek) - 95.1%

## Related Resources

- [Inference Framework Comparison](../comparison/inference-framework-comparison.md)
- [Open Source Inference Ecosystem Report](../../open-source-inference-ecosystem/open-source-inference-ecosystem-report.md)
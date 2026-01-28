<!-- @GL-governed -->
<!-- @GL-layer: GL90-99 -->
<!-- @GL-semantic: governed-documentation -->
<!-- @GL-audit-trail: engine/governance/GL_SEMANTIC_ANCHOR.json -->

# Threat Modeling Guide

## 框架

- STRIDE, PASTA, LINDDUN
- 結合 config/security-network-config.yml 與 governance/policies/

## 步驟

1. Asset & Data Flow：繪製資料流圖 (DFD)
2. Threat Enumeration：STRIDE 分析
3. Controls Mapping：零信任、IAM、SLSA
4. Residual Risk：計算 $Risk = Impact \times Likelihood$
5. Tracking：在 docs/KNOWLEDGE_HEALTH.md 記錄

## 工具

- Threat Dragon / IriusRisk
- OPA (Conftest) for policy gates

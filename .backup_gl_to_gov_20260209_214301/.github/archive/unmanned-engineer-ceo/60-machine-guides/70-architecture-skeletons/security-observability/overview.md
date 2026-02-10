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
# 安全與可觀測性骨架 / Security & Observability Skeleton

## 骨架簡介 / Overview

本骨架涵蓋系統安全機制（SLSA、Sigstore、零信任）、監控告警設置、分散式追蹤、日誌管理。AI 在設計安全策略、配置監控或實現可觀測性時應查詢此骨架。

## 使用場景 / Use Cases

- 🔒 安全機制設計（SLSA L3、Sigstore 簽名）
- 📊 監控告警設置（Prometheus、Grafana）
- 📝 日誌收集配置（ELK Stack）
- 🔍 分散式追蹤（Jaeger）
- 🐛 漏洞掃描與修復

## 關鍵原則 / Core Principles

- **零信任**：不信任任何人，驗證一切
- **深度防禦**：多層安全控制
- **可觀測性優先**：監控覆蓋所有關鍵路徑
- **自動化檢測**：使用工具自動掃描和修復

## 不負責的領域 / Not Responsible For

- ✅ 安全機制實現 ← 本骨架負責
- ❌ 身份認證 ← Identity & Tenancy 負責
- ❌ API 版本管理 ← API Governance 負責

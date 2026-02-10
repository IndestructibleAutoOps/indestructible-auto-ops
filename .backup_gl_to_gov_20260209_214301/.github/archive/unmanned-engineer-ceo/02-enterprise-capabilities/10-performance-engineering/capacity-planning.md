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
# Capacity Planning

## Inputs

- Traffic forecast（per service）
- Resource baseline（CPU, Memory, Storage）
- SLA/SLO targets

## Process

1. Demand forecasting（ARIMA/Prophet）。
2. Workload modeling（queueing theory, Little's Law）。
3. Scenario simulation（best/base/worst）。
4. Buffer allocation（20–30% headroom）。
5. Review with finance/ops；更新 docs/KNOWLEDGE_HEALTH.md。

## Tooling

- Grafana Capacity Planning plugin
- Spreadsheet templates
- automation/hyperautomation for auto-scaling

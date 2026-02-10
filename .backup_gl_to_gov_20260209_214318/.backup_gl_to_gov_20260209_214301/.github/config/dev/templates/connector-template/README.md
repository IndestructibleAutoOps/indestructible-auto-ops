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
# Connector Template

此目錄包含連接器模板，用於建立外部系統整合。

## 使用方式

```bash
cd .devcontainer/automation
ts-node code-generator.ts connector <名稱> [類型] [端點]
```

## 模板變數

- `name`: 連接器名稱
- `type`: 連接類型 (rest, graphql, grpc, websocket)
- `endpoint`: 目標端點 URL

## 生成的檔案

- `src/`: 主要程式碼
- `tests/`: 測試檔案
- `config/`: 配置檔案

## 範例

```bash
ts-node code-generator.ts connector payment-gateway rest [EXTERNAL_URL_REMOVED]
```

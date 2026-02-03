# MNGA 工程治理模組執行契約 - 完整落地計劃

## 1. 修復 Python 模組結構 [ ]
- [ ] 將 dual-path 重命名為 dual_path（Python 模組必須使用 snake_case）
- [ ] 添加所有必要的 __init__.py 文件
- [ ] 確保所有模組可正確導入

## 2. 重寫 enforce.py 核心框架 [ ]
- [ ] 實現真正的 MNGA 8 層架構檢查
- [ ] 整合雙路檢索系統
- [ ] 實現審計追蹤（actor/action/resource/result/hash/version）
- [ ] 支援 RFC3339 時間戳和 OpenTelemetry/JSONL 追蹤

## 3. 實現命名治理完整鏈路 [ ]
- [ ] OPA/Conftest 命名政策
- [ ] PrometheusRule 告警
- [ ] Grafana 儀表板
- [ ] 自動修復器
- [ ] 遷移 Playbook

## 4. 實現 CI Pipeline 第三階段 [ ]
- [ ] metadata/trigger/stages/artifacts/evidence_output
- [ ] 跨 Job Artifact 共享
- [ ] PR 註解和證據產出

## 5. 供應鏈安全 [ ]
- [ ] SBOM 生成
- [ ] Cosign 簽章
- [ ] SLSA Provenance

## 6. 驗證並推送 [ ]
- [ ] 運行完整測試
- [ ] 提交變更
- [ ] 推送到 GitHub

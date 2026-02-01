# GL Runtime Architecture

GL Runtime 全版本架構 (V1-V25)

## 版本概覽

| 階段 | 版本 | 功能 |
|------|------|------|
| 基礎執行 | V1-V6 | 任務執行、狀態管理、治理、修復、優化、協作 |
| 語義推理 | V7-V11 | DAG、語義圖、自我修復、多代理、網格認知 |
| 演化文明 | V12-V13 | 演化引擎、文明層 |
| 元認知 | V14-V18 | 元認知、通用智能、上下文、跨域、跨現實 |
| 統一織構 | V19-V20 | 統一織構、無限學習 |
| 程式智慧 | V21-V22 | 程式智慧、程式宇宙 |
| 元治理 | V23-V24 | 根本治理、元治理 |
| 平台整合 | V0Pro-V25 | 本地平台、生態整合 |

## 使用方式

```python
from gl.version_registry import VersionRegistry

registry = VersionRegistry()
print(registry.get_all_versions())
```

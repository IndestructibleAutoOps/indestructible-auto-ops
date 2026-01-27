#!/usr/bin/env python3
"""
GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module ns-root/namespaces-mcp/examples/example-project
@gl-semantic-anchor GL-00-EXAMPLES_EXAMPLEP_MAIN
@gl-evidence-required false
GL Unified Charter Activated
"""

"""
範例專案 - 用於演示 namespace-mcp 轉換效果
"""

from typing import Dict, List  # noqa: E402

# 外部依賴
import requests  # noqa: E402

# 內部導入


class DataProcessor:
    """數據處理器類"""

    MAX_SIZE = 1000

    def __init__(self):
        self.data = []

    def process_data(self, input_data: List[str]) -> Dict:
        """處理數據"""
        result = {"processed": len(input_data), "status": "success"}
        return result

    def fetch_remote_data(self, url: str) -> Dict:
        """獲取遠程數據"""
        response = requests.get(url)
        return response.json()


def main():
    """主函數"""
    processor = DataProcessor()
    data = ["item1", "item2", "item3"]
    result = processor.process_data(data)
    print(f"處理結果: {result}")


if __name__ == "__main__":
    main()

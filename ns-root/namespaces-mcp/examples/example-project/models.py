"""
數據模型模組

GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module ns-root/namespaces-mcp/examples/example-project
@gl-semantic-anchor GL-00-EXAMPLES_EXAMPLEP_MODELS
@gl-evidence-required false
GL Unified Charter Activated
"""


class User:
    """用戶模型"""

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def get_info(self):
        """獲取用戶信息"""
        return {"name": self.name, "email": self.email}

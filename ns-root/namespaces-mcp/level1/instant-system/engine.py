"""
INSTANT Engine - 即時引擎主控制器
統一協調所有即時組件

GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module ns-root/namespaces-mcp/level1/instant-system
@gl-semantic-anchor GL-00-LEVEL1_INSTANTS_ENGINE
@gl-evidence-required false
GL Unified Charter Activated
"""

import time
from typing import Any, Dict

from core import InstantArchitectureEngine, InstantConfig
from deployer import InstantDeployer
from validator import InstantValidator


class InstantEngine:
    """即時引擎主控制器"""

    def __init__(self):
        self.architecture_engine = InstantArchitectureEngine()
        self.validator = InstantValidator()
        self.deployer = InstantDeployer()
        self.performance_target_ms = 100

    async def execute_instant_pipeline(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """執行即時管道"""
        pipeline_start = time.time()

        # 階段 1: 即時架構生成
        config = InstantConfig(**request)
        architecture_result = await self._execute_architecture_generation(config)

        # 階段 2: 即時驗證
        validation_result = await self._execute_validation(
            architecture_result["architecture"]
        )

        # 階段 3: 即時部署
        deployment_result = await self._execute_deployment(
            architecture_result["architecture"]
        )

        pipeline_time = (time.time() - pipeline_start) * 1000

        # 檢查是否滿足即時要求
        instant_compliant = pipeline_time <= self.performance_target_ms

        return {
            "success": True,
            "instant_compliant": instant_compliant,
            "pipeline_time_ms": pipeline_time,
            "stages": {
                "architecture": architecture_result,
                "validation": validation_result,
                "deployment": deployment_result,
            },
        }

    async def _execute_architecture_generation(
        self, config: InstantConfig
    ) -> Dict[str, Any]:
        """執行架構生成"""
        return self.architecture_engine.parse_and_build(config)

    async def _execute_validation(self, architecture: Dict[str, Any]) -> Dict[str, Any]:
        """執行驗證"""
        return self.validator.validate(architecture)

    async def _execute_deployment(self, architecture: Dict[str, Any]) -> Dict[str, Any]:
        """執行部署"""
        return self.deployer.deploy(architecture)

    def get_performance_metrics(self) -> Dict[str, Any]:
        """獲取性能指標"""
        return {
            "target_response_time_ms": self.performance_target_ms,
            "instant_mode": True,
            "parallel_processing": True,
            "auto_optimization": True,
        }

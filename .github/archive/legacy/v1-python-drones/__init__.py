# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: archive-tools
# @GL-audit-trail: ../../engine/gl_platform_universe.gl_platform_universe.governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
"""
SynergyMesh v1-python-drones 套件

Python 無人機系統 - 高階應用整合層
"""

__version__ = "1.1.0"
__author__ = "SynergyMesh Team"

# 使用延遲導入以避免循環依賴


def get_drones():
    """取得無人機類別"""
    from .drones import AutopilotDrone, BaseDrone, CoordinatorDrone, DeploymentDrone

    return BaseDrone, CoordinatorDrone, AutopilotDrone, DeploymentDrone


def get_config():
    """取得配置類別"""
    from .config import DroneConfig

    return DroneConfig


__all__ = [
    "__version__",
    "__author__",
    "get_drones",
    "get_config",
]

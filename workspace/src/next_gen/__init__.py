"""
Next Generation Automation Platform Core
下一代智慧自動化平台核心模組

實現95%+自動化程度，AI驅動治理，企業級SaaS服務
"""

from .architecture import (
    EnterpriseSaaS,
    MultiLanguageSupport,
    UniversalCodeGenerator,
    VisualConfigInterface,
)
from .intelligence import AIAgentOrchestrator, AutonomousOptimizer, SmartDecisionEngine
from .services import BillingSystem, MCPService, MonitoringDashboard, SecurityFramework

__version__ = "2.0.0"
__author__ = "MachineNativeOps Next Gen Team"
__description__ = "Next Generation Intelligent Automation Platform"

# Platform Configuration
PLATFORM_CONFIG = {
    "automation_level": "95%+",
    "target_languages": 15,
    "saas_enabled": True,
    "enterprise_ready": True,
    "revenue_target": "$10M/month",
    "platform_compatibility": ["super.myninja.ai", "replit"],
}

# Export main components
__all__ = [
    "UniversalCodeGenerator",
    "MultiLanguageSupport",
    "VisualConfigInterface",
    "EnterpriseSaaS",
    "MCPService",
    "SecurityFramework",
    "MonitoringDashboard",
    "BillingSystem",
    "AIAgentOrchestrator",
    "SmartDecisionEngine",
    "AutonomousOptimizer",
]

# @GL-governed
# @GL-layer: GL30-49
# @GL-semantic: general-component
# @GL-audit-trail: gl-platform-universe/gl_platform_universegl_platform_universe.governance/audit-trails/GL30_49-audit.json
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-platform-universe/gl_platform_universegl_platform_universe.governance/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-platform-universe/gl_platform_universegl_platform_universe.governance/GL-UNIFIED-NAMING-CHARTER.yaml


"""V4 Auto Repair - 自動修復引擎"""
from typing import Dict, List, Optional
import time

class RepairEngine:
    def __init__(self):
        self.repair_strategies = {}
        self.repair_history = []
    
    def detect_fault(self, system_state: Dict) -> Optional[Dict]:
        anomalies = []
        for key, value in system_state.items():
            if self._is_anomaly(key, value):
                anomalies.append({"component": key, "state": value})
        return {"faults": anomalies} if anomalies else None
    
    def repair(self, fault: Dict) -> Dict:
        strategy = self._select_strategy(fault)
        result = self._execute_repair(strategy, fault)
        self.repair_history.append({
            "fault": fault, "strategy": strategy, 
            "result": result, "timestamp": time.time()
        })
        return result
    
    def register_strategy(self, fault_type: str, strategy: callable):
        self.repair_strategies[fault_type] = strategy
    
    def _is_anomaly(self, key: str, value: any) -> bool:
        return value is None or (isinstance(value, (int, float)) and value < 0)
    
    def _select_strategy(self, fault: Dict) -> str:
        return fault.get("type", "default_repair")
    
    def _execute_repair(self, strategy: str, fault: Dict) -> Dict:
        if strategy in self.repair_strategies:
            return self.repair_strategies[strategy](fault)
        return {"status": "repaired", "method": "default"}

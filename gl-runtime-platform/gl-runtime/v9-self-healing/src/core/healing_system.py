"""V9 Self Healing - 自我修復系統"""
from typing import Dict, List, Callable, Optional
import time
from enum import Enum

class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    RECOVERING = "recovering"

class SelfHealingSystem:
    def __init__(self):
        self.health_checks: Dict[str, Callable] = {}
        self.recovery_procedures: Dict[str, Callable] = {}
        self.status: Dict[str, HealthStatus] = {}
        self.healing_log = []
    
    def register_health_check(self, component: str, check_fn: Callable):
        self.health_checks[component] = check_fn
        self.status[component] = HealthStatus.HEALTHY
    
    def register_recovery(self, component: str, recovery_fn: Callable):
        self.recovery_procedures[component] = recovery_fn
    
    def monitor(self) -> Dict[str, HealthStatus]:
        for component, check_fn in self.health_checks.items():
            try:
                is_healthy = check_fn()
                self.status[component] = HealthStatus.HEALTHY if is_healthy else HealthStatus.DEGRADED
            except Exception as e:
                self.status[component] = HealthStatus.CRITICAL
        return self.status
    
    def heal(self, component: str) -> Dict:
        if component not in self.recovery_procedures:
            return {"status": "no_recovery_procedure"}
        
        self.status[component] = HealthStatus.RECOVERING
        try:
            result = self.recovery_procedures[component]()
            self.status[component] = HealthStatus.HEALTHY
            self.healing_log.append({
                "component": component, "result": "success", "timestamp": time.time()
            })
            return {"status": "healed", "result": result}
        except Exception as e:
            self.status[component] = HealthStatus.CRITICAL
            return {"status": "failed", "error": str(e)}
    
    def auto_heal(self) -> List[Dict]:
        results = []
        for component, status in self.status.items():
            if status in [HealthStatus.DEGRADED, HealthStatus.CRITICAL]:
                results.append(self.heal(component))
        return results

# GL Runtime Architecture - Version Registry
# @GL-governed
# @GL-layer: core
# @GL-semantic: version-registry

"""
GL Runtime 版本註冊表
管理 V1-V25 全版本的初始化順序與依賴關係
"""

from typing import Dict, List, Set, Optional, Callable, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class VersionPhase(Enum):
    FOUNDATION = "foundation"           # V1-V6
    GLOBAL_COLLABORATION = "global"     # V7-V11
    EVOLUTION = "evolution"             # V12-V13
    META_COGNITION = "meta_cognition"   # V14-V18
    UNIFIED_FABRIC = "unified_fabric"   # V19-V20
    CODE_INTELLIGENCE = "code_intel"    # V21-V22
    GOVERNANCE = "governance"           # V23-V24
    NATIVE_PLATFORM = "native_platform" # V0Pro-V25


@dataclass
class VersionSpec:
    """版本規格"""
    version: str
    name: str
    phase: VersionPhase
    core_modules: List[str]
    path: str
    direct_deps: List[str] = field(default_factory=list)
    governance_req: List[str] = field(default_factory=list)
    encryption_required: bool = False
    zero_residue: bool = True
    status: str = "active"


# GL Runtime 完整版本定義
GL_VERSIONS: Dict[str, VersionSpec] = {
    "V01": VersionSpec(
        version="V01",
        name="基礎執行層",
        phase=VersionPhase.FOUNDATION,
        core_modules=["task_executor", "state_manager", "io_handler"],
        path="/gl/v01/exec/",
        direct_deps=[],
        governance_req=[]
    ),
    "V02": VersionSpec(
        version="V02",
        name="基礎分析層",
        phase=VersionPhase.FOUNDATION,
        core_modules=["analyzer", "structure_parser"],
        path="/gl/v02/semantic/",
        direct_deps=["V01"]
    ),
    "V03": VersionSpec(
        version="V03",
        name="基礎治理層",
        phase=VersionPhase.FOUNDATION,
        core_modules=["audit", "result_checker"],
        path="/gl/v03/governance/",
        direct_deps=["V01", "V02"]
    ),
    "V04": VersionSpec(
        version="V04",
        name="自動修復層",
        phase=VersionPhase.FOUNDATION,
        core_modules=["patcher", "retry_manager"],
        path="/gl/v04/repair/",
        direct_deps=["V03"]
    ),
    "V05": VersionSpec(
        version="V05",
        name="自動優化層",
        phase=VersionPhase.FOUNDATION,
        core_modules=["perf_optimizer", "resource_tuner"],
        path="/gl/v05/optimize/",
        direct_deps=["V03", "V04"]
    ),
    "V06": VersionSpec(
        version="V06",
        name="多模組協作層",
        phase=VersionPhase.FOUNDATION,
        core_modules=["task_collaborator", "module_interactor"],
        path="/gl/v06/collaboration/",
        direct_deps=["V05"]
    ),
    "V07": VersionSpec(
        version="V07",
        name="全域DAG執行層",
        phase=VersionPhase.GLOBAL_COLLABORATION,
        core_modules=["dependency_graph", "scheduler"],
        path="/gl/v07/dag/",
        direct_deps=["V06"]
    ),
    "V08": VersionSpec(
        version="V08",
        name="語義資源圖(SRG)",
        phase=VersionPhase.GLOBAL_COLLABORATION,
        core_modules=["semantic_node", "semantic_edge", "semantic_reasoner"],
        path="/gl/v08/srg/",
        direct_deps=["V02", "V07"],
        encryption_required=True
    ),
    "V09": VersionSpec(
        version="V09",
        name="自我修復執行層(SHEL)",
        phase=VersionPhase.GLOBAL_COLLABORATION,
        core_modules=["self_healer", "self_adjuster"],
        path="/gl/v09/shel/",
        direct_deps=["V04", "V08"]
    ),
    "V10": VersionSpec(
        version="V10",
        name="多代理協作層(Swarm)",
        phase=VersionPhase.GLOBAL_COLLABORATION,
        core_modules=["agent_manager", "swarm_orchestrator"],
        path="/gl/v10/swarm/",
        direct_deps=["V06", "V07"]
    ),
    "V11": VersionSpec(
        version="V11",
        name="網格認知層(Mesh Cognition)",
        phase=VersionPhase.GLOBAL_COLLABORATION,
        core_modules=["mesh_cognition", "distributed_reasoner"],
        path="/gl/v11/mesh/",
        direct_deps=["V08", "V10"]
    ),
    "V12": VersionSpec(
        version="V12",
        name="演化引擎(Evolution Engine)",
        phase=VersionPhase.EVOLUTION,
        core_modules=["strategy_evolver", "model_evolver", "structure_evolver"],
        path="/gl/v12/evolution/",
        direct_deps=["V09", "V11"]
    ),
    "V13": VersionSpec(
        version="V13",
        name="文明層(Civilization Layer)",
        phase=VersionPhase.EVOLUTION,
        core_modules=["long_term_memory", "long_term_strategy", "long_term_evolution"],
        path="/gl/v13/civilization/",
        direct_deps=["V12"]
    ),
    "V14": VersionSpec(
        version="V14",
        name="元認知層(Meta-Cognition)",
        phase=VersionPhase.META_COGNITION,
        core_modules=["self_observer", "self_evaluator", "self_adjuster"],
        path="/gl/v14/meta_cognition/",
        direct_deps=["V13"]
    ),
    "V15": VersionSpec(
        version="V15",
        name="通用智慧(Universal Intelligence)",
        phase=VersionPhase.META_COGNITION,
        core_modules=["cross_domain_reasoner", "cross_module_reasoner"],
        path="/gl/v15/universal_intel/",
        direct_deps=["V14"]
    ),
    "V16": VersionSpec(
        version="V16",
        name="脈絡宇宙(Context Universe)",
        phase=VersionPhase.META_COGNITION,
        core_modules=["multi_context_reasoner", "context_fusion"],
        path="/gl/v16/context_universe/",
        direct_deps=["V15"]
    ),
    "V17": VersionSpec(
        version="V17",
        name="跨領域智慧(Cross-Domain)",
        phase=VersionPhase.META_COGNITION,
        core_modules=["cross_domain_mapper", "cross_domain_reasoner"],
        path="/gl/v17/cross_domain/",
        direct_deps=["V15", "V16"]
    ),
    "V18": VersionSpec(
        version="V18",
        name="跨現實智慧(Inter-Reality)",
        phase=VersionPhase.META_COGNITION,
        core_modules=["multi_reality_model", "multi_world_reasoner"],
        path="/gl/v18/inter_reality/",
        direct_deps=["V16", "V17"]
    ),
    "V19": VersionSpec(
        version="V19",
        name="統一智慧織網(Unified Fabric)",
        phase=VersionPhase.UNIFIED_FABRIC,
        core_modules=["unified_fabric", "intelligence_router"],
        path="/gl/v19/fabric/",
        direct_deps=["V01", "V02", "V03", "V04", "V05", "V06", "V07", "V08", 
                     "V09", "V10", "V11", "V12", "V13", "V14", "V15", "V16", "V17", "V18"]
    ),
    "V20": VersionSpec(
        version="V20",
        name="無限學習連續體(Infinite Learning)",
        phase=VersionPhase.UNIFIED_FABRIC,
        core_modules=["continuous_learner", "continuous_evolver", "continuous_restructurer"],
        path="/gl/v20/learning/",
        direct_deps=["V19"]
    ),
    "V21": VersionSpec(
        version="V21",
        name="程式智慧與安全層(Code Intelligence)",
        phase=VersionPhase.CODE_INTELLIGENCE,
        core_modules=["deep_analyzer", "auto_refactor", "auto_patcher", 
                      "security_enhancer", "perf_optimizer", "arch_evolver"],
        path="/gl/v21/code_intel/",
        direct_deps=["V14", "V19"],
        encryption_required=True
    ),
    "V22": VersionSpec(
        version="V22",
        name="程式宇宙層(Code Universe)",
        phase=VersionPhase.CODE_INTELLIGENCE,
        core_modules=["code_universe_modeler", "code_ecosystem_evolver"],
        path="/gl/v22/code_universe/",
        direct_deps=["V21"],
        status="reserved"
    ),
    "V23": VersionSpec(
        version="V23",
        name="根本治理層(Root Governance)",
        phase=VersionPhase.GOVERNANCE,
        core_modules=["anti_fabric", "falsification_engine", "execution_harness",
                      "governance_rules", "governance_auditor", "governance_enforcer", 
                      "governance_memory"],
        path="/gl/v23/root_governance/",
        direct_deps=["V20", "V21"],
        governance_req=["V01", "V02", "V03", "V04", "V05", "V06", "V07", "V08",
                        "V09", "V10", "V11", "V12", "V13", "V14", "V15", "V16",
                        "V17", "V18", "V19", "V20", "V21", "V22"],
        encryption_required=True
    ),
    "V24": VersionSpec(
        version="V24",
        name="元治理層(Meta-Governance)",
        phase=VersionPhase.GOVERNANCE,
        core_modules=["meta_rules", "meta_auditor", "meta_falsification",
                      "integrity_checker", "meta_enforcer", "meta_memory",
                      "success_criteria_auditor"],
        path="/gl/v24/meta_governance/",
        direct_deps=["V23"],
        governance_req=["V23"],
        encryption_required=True
    ),
    "V0Pro": VersionSpec(
        version="V0Pro",
        name="本地自主平台(GL-Native Platform)",
        phase=VersionPhase.NATIVE_PLATFORM,
        core_modules=["execution_engine", "storage_fabric", "compute_mesh",
                      "local_architecture", "zero_cloud"],
        path="/gl/v0pro/native_platform/",
        direct_deps=["V23", "V24"],
        encryption_required=True
    ),
    "V25": VersionSpec(
        version="V25",
        name="生態整合(Ecosystem Integration)",
        phase=VersionPhase.NATIVE_PLATFORM,
        core_modules=["p2p_federation", "local_marketplace", 
                      "resource_sharing", "community_governance"],
        path="/gl/v25/ecosystem/",
        direct_deps=["V0Pro"],
        status="reserved"
    )
}


def get_initialization_order() -> List[str]:
    """獲取正確的初始化順序"""
    return [
        "V01", "V02", "V03", "V04", "V05", "V06",  # Phase 1
        "V07", "V08", "V09", "V10", "V11",          # Phase 2
        "V12", "V13",                               # Phase 3
        "V14", "V15", "V16", "V17", "V18",          # Phase 4
        "V19", "V20",                               # Phase 5
        "V21", "V22",                               # Phase 6
        "V23", "V24",                               # Phase 7
        "V0Pro", "V25"                              # Phase 8
    ]


def get_version_dependencies(version: str) -> Set[str]:
    """獲取版本的所有依賴(包含間接依賴)"""
    if version not in GL_VERSIONS:
        return set()
    
    all_deps = set()
    to_process = list(GL_VERSIONS[version].direct_deps)
    
    while to_process:
        dep = to_process.pop(0)
        if dep not in all_deps:
            all_deps.add(dep)
            if dep in GL_VERSIONS:
                to_process.extend(GL_VERSIONS[dep].direct_deps)
    
    return all_deps


def validate_initialization(initialized: Set[str], target: str) -> bool:
    """驗證是否可以初始化目標版本"""
    if target not in GL_VERSIONS:
        return False
    
    deps = get_version_dependencies(target)
    return deps.issubset(initialized)

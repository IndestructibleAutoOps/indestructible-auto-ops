"""NG 命名空間治理任務

整合自: ng-namespace-governance/core/
用途: 在 auto_task_project 中執行 NG 命名空間治理操作
優先級: 最高（0級）- 因為這是治理的核心
"""
import logging
import sys
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
from auto_executor import Task, executor

logger = logging.getLogger(__name__)

# 添加 NG 系統到路徑
NG_ROOT = Path(__file__).resolve().parents[2] / "ng-namespace-governance"
sys.path.insert(0, str(NG_ROOT / "core"))


class NgGovernanceTask(Task):
    """NG 命名空間治理任務"""
    
    name = "NG命名空間治理"
    priority = 0  # 最高優先級（超越所有其他任務）
    
    def __init__(self):
        super().__init__()
        self.ng_executor = None
        self.closure_engine = None
        self._load_ng_engines()
    
    def _load_ng_engines(self):
        """載入 NG 執行引擎"""
        try:
            import importlib.util
            
            # 載入 ng-executor
            executor_path = NG_ROOT / "core" / "ng-executor.py"
            if executor_path.exists():
                spec = importlib.util.spec_from_file_location("ng_executor", executor_path)
                ng_executor_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(ng_executor_module)
                self.ng_executor = ng_executor_module.ng_executor
                logger.info("  ✓ NG executor 已載入")
            
            # 載入 closure-engine
            closure_path = NG_ROOT / "core" / "ng-closure-engine.py"
            if closure_path.exists():
                spec = importlib.util.spec_from_file_location("ng_closure_engine", closure_path)
                closure_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(closure_module)
                self.closure_engine = closure_module.ng_closure_engine
                logger.info("  ✓ NG closure engine 已載入")
                
        except Exception as e:
            logger.warning(f"⚠️  NG 引擎載入失敗: {e}")
            logger.info("  將使用簡化模式運行")
    
    def execute(self):
        """執行 NG 治理操作"""
        logger.info("👑 執行 NG 命名空間治理（最高權重）...")
        
        # 執行閉環檢查
        if self.ng_executor:
            try:
                closure_check = self.ng_executor.check_closure()
                
                logger.info(f"🔄 閉環狀態:")
                logger.info(f"  閉環完整: {'✅' if closure_check['closure_complete'] else '❌'}")
                logger.info(f"  待處理操作: {len(closure_check.get('pending_operations', []))}")
                
                if not closure_check['closure_complete']:
                    logger.warning(f"⚠️  發現治理缺口，需要修復")
                
                # 生成報告
                report = self.ng_executor.generate_execution_report()
                logger.info(f"\n{report}")
                
                # 保存日誌
                log_path = Path("../ng-namespace-governance/logs/ng-executor.json")
                log_path.parent.mkdir(parents=True, exist_ok=True)
                self.ng_executor.save_execution_log(str(log_path))
                
            except Exception as e:
                logger.error(f"❌ NG executor 執行失敗: {e}")
        
        # 執行閉環分析
        if self.closure_engine:
            try:
                # 從註冊表載入命名空間
                registry_path = NG_ROOT / "registry" / "namespaces.json"
                
                if registry_path.exists():
                    import json
                    with open(registry_path, 'r') as f:
                        registry_data = json.load(f)
                    
                    namespaces = list(registry_data.get('namespaces', {}).values())
                    
                    # 執行閉環分析
                    analysis = self.closure_engine.analyze_closure(namespaces)
                    
                    logger.info(f"🔍 閉環分析:")
                    logger.info(f"  總命名空間: {analysis['total_namespaces']}")
                    logger.info(f"  完整率: {analysis['closure_rate']:.1f}%")
                    
                    if analysis['closure_incomplete'] > 0:
                        logger.warning(
                            f"  ⚠️  不完整: {analysis['closure_incomplete']} 個命名空間"
                        )
                        
                        # 生成修復計劃
                        plan = self.closure_engine.generate_remediation_plan()
                        logger.info(f"  📋 修復計劃: {len(plan['remediation_actions'])} 個動作")
                
            except Exception as e:
                logger.error(f"❌ 閉環分析失敗: {e}")
        
        # 統計
        if self.ng_executor:
            stats = self.ng_executor.get_execution_statistics()
            logger.info(f"📊 NG 執行統計:")
            logger.info(f"  總操作數: {stats['total_operations']}")
            logger.info(f"  成功率: {stats['success_rate']:.1f}%")
        
        logger.info("✅ NG 命名空間治理完成")


# 註冊任務：每天凌晨 1 點執行（最高優先級，在所有其他任務之前）
executor.register(NgGovernanceTask, cron="0 1 * * *", priority=0)

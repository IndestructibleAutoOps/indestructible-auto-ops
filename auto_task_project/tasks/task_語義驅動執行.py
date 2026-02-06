"""語義驅動執行任務

整合自: ecosystem/tools/semantic_driven_executor.py
用途: 語義驅動的治理執行引擎
"""
import logging
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
from auto_executor import Task, executor

logger = logging.getLogger(__name__)


class SemanticDrivenExecutor:
    """語義驅動執行器"""
    
    def __init__(self, workspace_path: str = "."):
        """初始化執行器"""
        self.workspace_path = Path(workspace_path)
        self.execution_history = []
    
    def execute_semantic_validation(self, target_path: str) -> Dict[str, Any]:
        """執行語義驗證"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'target': target_path,
            'violations': [],
            'warnings': [],
            'suggestions': []
        }
        
        target = Path(target_path)
        
        if not target.exists():
            results['violations'].append(f"目標不存在: {target_path}")
            return results
        
        # 模擬語義驗證邏輯
        logger.info(f"🔍 執行語義驗證: {target_path}")
        
        # 檢查檔案命名
        if target.is_file():
            if not target.name.startswith('gl-') and 'gl' in target.name.lower():
                results['suggestions'].append(f"建議使用 'gl-' 前綴: {target.name}")
        
        # 檢查目錄結構
        if target.is_dir():
            py_files = list(target.glob("*.py"))
            if not py_files:
                results['warnings'].append(f"目錄中無 Python 文件: {target_path}")
        
        logger.info(f"  發現: {len(results['violations'])} 違規, {len(results['warnings'])} 警告")
        
        self.execution_history.append(results)
        return results
    
    def generate_execution_report(self) -> str:
        """生成執行報告"""
        report_lines = [
            "=" * 60,
            "語義驅動執行報告",
            "=" * 60,
            f"生成時間: {datetime.now().isoformat()}",
            f"執行次數: {len(self.execution_history)}",
            ""
        ]
        
        total_violations = sum(len(h['violations']) for h in self.execution_history)
        total_warnings = sum(len(h['warnings']) for h in self.execution_history)
        
        report_lines.append(f"總統計:")
        report_lines.append(f"  ❌ 違規: {total_violations}")
        report_lines.append(f"  ⚠️  警告: {total_warnings}")
        report_lines.append("")
        
        return "\n".join(report_lines)


class SemanticDrivenTask(Task):
    """語義驅動執行任務"""
    
    name = "語義驅動執行"
    priority = 3
    
    def __init__(self):
        super().__init__()
        self.executor_engine = SemanticDrivenExecutor()
    
    def execute(self):
        """執行語義驅動驗證"""
        logger.info("🧠 開始語義驅動執行...")
        
        # 驗證關鍵目錄
        targets = [
            "ecosystem/",
            "tasks/registries/",
            "docs/"
        ]
        
        for target in targets:
            if Path(target).exists():
                results = self.executor_engine.execute_semantic_validation(target)
                
                if results['violations']:
                    logger.error(f"❌ {target}: {len(results['violations'])} 違規")
                elif results['warnings']:
                    logger.warning(f"⚠️  {target}: {len(results['warnings'])} 警告")
                else:
                    logger.info(f"✅ {target}: 通過驗證")
        
        # 生成報告
        report = self.executor_engine.generate_execution_report()
        
        # 保存報告
        report_path = Path("logs/semantic-execution-report.txt")
        report_path.parent.mkdir(exist_ok=True)
        report_path.write_text(report)
        logger.info(f"📄 執行報告已保存: {report_path}")


# 註冊任務：每天執行一次
executor.register(SemanticDrivenTask, cron="0 12 * * *", priority=3)

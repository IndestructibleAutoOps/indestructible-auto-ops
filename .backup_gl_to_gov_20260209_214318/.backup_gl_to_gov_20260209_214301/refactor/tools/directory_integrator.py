#!/usr/bin/env python3
"""
目錄整合器 - 整合 18 個 responsibility-* 目錄
"""

import shutil
from pathlib import Path
from typing import List, Dict
import logging
from datetime import datetime

from refactor_executor import RefactorExecutor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)


class DirectoryIntegrator:
    """目錄整合器"""
    
    def __init__(self, workspace: Path, executor: RefactorExecutor):
        self.workspace = workspace
        self.executor = executor
        self.integration_log: List[Dict] = []
    
    def integrate_responsibility_directories(self):
        """整合所有 responsibility-* 目錄"""
        logger.info("🔄 開始整合 18 個 responsibility-* 目錄...")
        
        # 目標目錄
        target_base = self.workspace / "governance" / "l3_execution" / "boundaries"
        target_base.mkdir(parents=True, exist_ok=True)
        
        # 需要整合的目錄列表
        directories = [
            "responsibility-gap-boundary",
            "responsibility-gates-boundary",
            "responsibility-gateway-boundary",
            "responsibility-gcp-boundary",
            "responsibility-generation-boundary",
            "responsibility-gl-layers-boundary",
            "responsibility-global-policy-boundary",
            "responsibility-governance-anchor-boundary",
            "responsibility-governance-execution-boundary",
            "responsibility-governance-sensing-boundary",
            "responsibility-governance-specs-boundary",
            "responsibility-group-boundary",
            "responsibility-guardrails-boundary",
            "responsibility-mnga-architecture-boundary",
            "responsibility-mno-operations-boundary",
            "responsibility-namespace-governance-boundary",
            "responsibility-observability-grafana-boundary",
            "responsibility-quantum-stack-boundary",
        ]
        
        success_count = 0
        failed_count = 0
        
        for dir_name in directories:
            source = self.workspace / dir_name
            target_name = dir_name.replace("responsibility-", "")
            target = target_base / target_name
            
            logger.info(f"📁 處理: {dir_name} -> {target}")
            
            if not source.exists():
                logger.warning(f"⚠️  源目錄不存在: {dir_name}")
                failed_count += 1
                self._log_integration(dir_name, target_name, "failed", "源目錄不存在")
                continue
            
            # 執行移動
            success = self.executor.move_directory(dir_name, str(target.relative_to(self.workspace)), 
                                                   f"整合責任邊界到統一位置")
            
            if success:
                success_count += 1
                self._log_integration(dir_name, target_name, "success", "整合成功")
                logger.info(f"✅ 成功: {dir_name}")
            else:
                failed_count += 1
                self._log_integration(dir_name, target_name, "failed", "移動失敗")
                logger.error(f"❌ 失敗: {dir_name}")
        
        logger.info(f"\n📊 整合完成:")
        logger.info(f"  ✅ 成功: {success_count}/{len(directories)}")
        logger.info(f"  ❌ 失敗: {failed_count}/{len(directories)}")
        
        return success_count, failed_count
    
    def integrate_governance_directories(self):
        """整合 governance 相關目錄"""
        logger.info("🔄 開始整合 governance 相關目錄...")
        
        # 整合 enterprise-governance
        enterprise_dir = self.workspace / "enterprise-governance"
        if enterprise_dir.exists():
            target = "governance/l2_domains/enterprise"
            success = self.executor.move_directory("enterprise-governance", target, 
                                                   "整合企業治理到治理領域")
            if success:
                logger.info("✅ 整合 enterprise-governance 成功")
            else:
                logger.error("❌ 整合 enterprise-governance 失敗")
        
        # 整合 .governance
        hidden_governance = self.workspace / ".governance"
        if hidden_governance.exists():
            target = "governance/l1_governance_core/.internal"
            success = self.executor.move_directory(".governance", target, 
                                                   "整合 .governance 到治理核心")
            if success:
                logger.info("✅ 整合 .governance 成功")
            else:
                logger.error("❌ 整合 .governance 失敗")
    
    def verify_integration(self):
        """驗證整合結果"""
        logger.info("🔍 驗證整合結果...")
        
        # 檢查根層的 responsibility-* 目錄是否已移除
        remaining_resp_dirs = list(self.workspace.glob("responsibility-*-boundary"))
        
        if remaining_resp_dirs:
            logger.warning(f"⚠️  仍有 {len(remaining_resp_dirs)} 個 responsibility-* 目錄未移除")
            for dir_path in remaining_resp_dirs:
                logger.warning(f"    - {dir_path.name}")
        else:
            logger.info("✅ 所有 responsibility-* 目錄已成功移除")
        
        # 檢查目標目錄是否存在
        boundaries_dir = self.workspace / "governance" / "l3_execution" / "boundaries"
        if boundaries_dir.exists():
            boundary_dirs = [d for d in boundaries_dir.iterdir() if d.is_dir()]
            logger.info(f"✅ 邊界目錄已創建，包含 {len(boundary_dirs)} 個子目錄")
        else:
            logger.error("❌ 邊界目錄未創建")
        
        # 檢查根層目錄數量
        root_dirs = [d for d in self.workspace.iterdir() if d.is_dir() and not d.name.startswith('.')]
        logger.info(f"📊 根層目錄數量: {len(root_dirs)}")
        
        return len(remaining_resp_dirs) == 0, boundaries_dir.exists()
    
    def _log_integration(self, source: str, target: str, status: str, message: str):
        """記錄整合日誌"""
        self.integration_log.append({
            "timestamp": datetime.now().isoformat(),
            "source": source,
            "target": target,
            "status": status,
            "message": message
        })
    
    def save_integration_report(self):
        """保存整合報告"""
        report_path = self.workspace / "refactor" / "reports" / f"integration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_directories": len(self.integration_log),
            "successful": len([log for log in self.integration_log if log["status"] == "success"]),
            "failed": len([log for log in self.integration_log if log["status"] == "failed"]),
            "integrations": self.integration_log
        }
        
        with open(report_path, 'w', encoding='utf-8') as f:
            import json
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📄 整合報告已保存: {report_path}")


def main():
    """測試目錄整合器"""
    workspace = Path('/workspace/indestructibleautoops')
    whitelist_path = workspace / 'refactor' / 'tools' / 'whitelist.json'
    
    executor = RefactorExecutor(workspace, whitelist_path)
    integrator = DirectoryIntegrator(workspace, executor)
    
    # 執行整合
    integrator.integrate_responsibility_directories()
    integrator.integrate_governance_directories()
    
    # 驗證結果
    integrator.verify_integration()
    
    # 保存報告
    integrator.save_integration_report()


if __name__ == '__main__':
    main()
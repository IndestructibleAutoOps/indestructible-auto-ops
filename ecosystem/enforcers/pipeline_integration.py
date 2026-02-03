#!/usr/bin/env python3
"""
GL Pipeline Integrator
======================
Integrates governance with CI/CD pipelines and artifact flows.

Critical Features:
- Contract binding to pipelines
- Hook injection at pipeline stages
- Governance event emission
- Multi-platform support (GitHub Actions, GitLab CI, ArgoCD, Tekton)
- Multi-language support (YAML, JSON, DSL)
"""

# MNGA-002: Import organization needs review
import os
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class PipelineStage:
    """Pipeline stage definition"""
    name: str
    type: str  # "validation", "verification", "audit", "deployment"
    platforms: List[str]
    hooks: List[Dict]
    config: Dict

@dataclass
class GovernanceEvent:
    """Governance event for pipeline integration"""
    event_type: str
    contract_id: str
    stage: str
    payload: Dict
    timestamp: str

class PipelineIntegrator:
    """
    Pipeline integration engine that binds governance contracts to CI/CD pipelines.
    
    Key responsibilities:
    - Bind governance contracts to pipelines
    - Inject hooks at pipeline stages
    - Emit governance events
    - Support multiple platforms and languages
    """
    
    SUPPORTED_PLATFORMS = {
        "github_actions": "GitHub Actions",
        "gitlab_ci": "GitLab CI",
        "argocd": "ArgoCD",
        "tekton": "Tekton Pipelines"
    }
    
    SUPPORTED_LANGUAGES = ["yaml", "json", "dsl"]
    
    def __init__(self, base_path: str = "/workspace/machine-native-ops"):
        self.base_path = Path(base_path)
        self.contracts_dir = self.base_path / "ecosystem" / "contracts"
        self.bindings = {}
        self.hooks = {}
        self._initialize_default_stages()
    
    def _initialize_default_stages(self):
        """Initialize default pipeline stages"""
        self.stages = [
            PipelineStage(
                name="validation",
                type="validation",
                platforms=["github_actions", "gitlab_ci", "argocd", "tekton"],
                hooks=[
                    {
                        "name": "governance_validation",
                        "action": "validate_against_contract",
                        "platform": "all"
                    }
                ],
                config={
                    "fail_fast": True,
                    "timeout_minutes": 10
                }
            ),
            PipelineStage(
                name="verification",
                type="verification",
                platforms=["github_actions", "gitlab_ci", "argocd", "tekton"],
                hooks=[
                    {
                        "name": "evidence_collection",
                        "action": "collect_evidence",
                        "platform": "all"
                    },
                    {
                        "name": "proof_verification",
                        "action": "verify_proofs",
                        "platform": "all"
                    }
                ],
                config={
                    "evidence_threshold": 0.90,
                    "timeout_minutes": 15
                }
            ),
            PipelineStage(
                name="audit",
                type="audit",
                platforms=["github_actions", "gitlab_ci"],
                hooks=[
                    {
                        "name": "self_audit",
                        "action": "audit_operation",
                        "platform": "all"
                    }
                ],
                config={
                    "forbidden_phrase_check": True,
                    "quality_gate_check": True
                }
            ),
            PipelineStage(
                name="deployment",
                type="deployment",
                platforms=["argocd", "tekton"],
                hooks=[
                    {
                        "name": "pre_deployment_check",
                        "action": "validate_deployment_ready",
                        "platform": "all"
                    }
                ],
                config={
                    "require_manual_approval": False,
                    "rollback_on_failure": True
                }
            )
        ]
    
    def bind(self, contract: Dict) -> str:
        """
        Bind a governance contract to pipeline stages.
        
        Args:
            contract: Governance contract dictionary
        
        Returns:
            Binding ID
        """
        contract_id = contract.get("metadata", {}).get("name", "unknown")
        contract_version = contract.get("version", "1.0.0")
        
        # Create binding
        binding_id = f"{contract_id}_v{contract_version}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Determine applicable stages based on contract
        applicable_stages = self._determine_applicable_stages(contract)
        
        self.bindings[binding_id] = {
            "contract_id": contract_id,
            "contract_version": contract_version,
            "applicable_stages": applicable_stages,
            "bound_at": datetime.now().isoformat(),
            "contract": contract
        }
        
        # Inject hooks for applicable stages
        for stage_name in applicable_stages:
            self.inject_hooks(stage_name, contract)
        
        return binding_id
    
    def injectHooks(self, stage: str, platform: str = "all"):
        """
        Inject hooks into a pipeline stage for specific platform.
        
        Args:
            stage: Stage name (validation, verification, audit, deployment)
            platform: Platform name or "all"
        """
        # Find the stage
        stage_obj = next((s for s in self.stages if s.name == stage), None)
        if not stage_obj:
            raise ValueError(f"Stage {stage} not found")
        
        # Filter hooks by platform
        stage_hooks = stage_obj.hooks
        if platform != "all":
            stage_hooks = [h for h in stage_hooks if h.get("platform") == platform or h.get("platform") == "all"]
        
        # Store hooks for injection
        if stage not in self.hooks:
            self.hooks[stage] = {}
        
        if platform not in self.hooks[stage]:
            self.hooks[stage][platform] = []
        
        self.hooks[stage][platform].extend(stage_hooks)
    
    def inject_hooks(self, stage: str, contract: Dict):
        """
        Inject hooks into a pipeline stage based on contract.
        
        Args:
            stage: Stage name
            contract: Governance contract
        """
        if stage not in self.hooks:
            self.hooks[stage] = {}
        
        # Generate hook configuration from contract
        hook_config = self._generate_hook_config(contract, stage)
        
        self.hooks[stage]["all"] = self.hooks[stage].get("all", []) + [hook_config]
    
    def emit(self, event: GovernanceEvent):
        """
        Emit a governance event to pipeline integrations.
        
        Args:
            event: GovernanceEvent to emit
        """
        # Save event to log
        self._log_event(event)
        
        # Trigger downstream actions based on event type
        if event.event_type == "validation_failed":
            self._handle_validation_failure(event)
        elif event.event_type == "audit_failed":
            self._handle_audit_failure(event)
        elif event.event_type == "quality_gate_failed":
            self._handle_quality_gate_failure(event)
    
    def generate_github_actions_workflow(self, contract: Dict, workflow_name: str = "governance.yml") -> str:
        """
        Generate GitHub Actions workflow for governance.
        
        Args:
            contract: Governance contract
            workflow_name: Name of the workflow file
        
        Returns:
            YAML workflow configuration
        """
        workflow = {
            "name": "GL Governance Enforcement",
            "on": {
                "pull_request": None,
                "push": {
                    "branches": ["main", "develop"]
                }
            },
            "jobs": {
                "governance-validation": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {
                            "name": "Checkout code",
                            "uses": "actions/checkout@v3"
                        },
                        {
                            "name": "Set up Python",
                            "uses": "actions/setup-python@v4",
                            "with": {
                                "python-version": "3.11"
                            }
                        },
                        {
                            "name": "Install dependencies",
                            "run": "pip install pyyaml"
                        },
                        {
                            "name": "Run governance validation",
                            "run": "python ecosystem/enforce.py"
                        },
                        {
                            "name": "Upload governance report",
                            "uses": "actions/upload-artifact@v3",
                            "if": "always()",
                            "with": {
                                "name": "governance-report",
                                "path": "ecosystem/outputs/governance-report.json"
                            }
                        }
                    ]
                }
            }
        }
        
        return yaml.dump(workflow, default_flow_style=False, sort_keys=False)
    
    def generate_gitlab_ci_config(self, contract: Dict) -> str:
        """
        Generate GitLab CI configuration for governance.
        
        Args:
            contract: Governance contract
        
        Returns:
            YAML CI configuration
        """
        config = {
            "stages": ["validate", "verify", "audit", "deploy"],
            "governance:validate": {
                "stage": "validate",
                "script": [
                    "pip install pyyaml",
                    "python ecosystem/enforce.py"
                ],
                "artifacts": {
                    "paths": ["ecosystem/outputs/"],
                    "when": "always"
                }
            },
            "governance:verify": {
                "stage": "verify",
                "script": [
                    "python ecosystem/tools/collect-evidence.py"
                ],
                "dependencies": ["governance:validate"]
            },
            "governance:audit": {
                "stage": "audit",
                "script": [
                    "python ecosystem/enforcers/self_auditor.py"
                ],
                "dependencies": ["governance:verify"]
            }
        }
        
        return yaml.dump(config, default_flow_style=False, sort_keys=False)
    
    def _determine_applicable_stages(self, contract: Dict) -> List[str]:
        """Determine which stages a contract applies to"""
        stages = []
        
        # Check trigger conditions
        trigger_conditions = contract.get("trigger", {}).get("conditions", [])
        
        for condition in trigger_conditions:
            condition_type = condition.get("type")
            
            if condition_type in ["file_change", "ci_event"]:
                stages.append("validation")
                stages.append("verification")
            
            if condition_type == "report_generation":
                stages.append("audit")
            
            if condition_type == "manual":
                stages.append("deployment")
        
        # Remove duplicates while preserving order
        seen = set()
        result = []
        for stage in stages:
            if stage not in seen:
                seen.add(stage)
                result.append(stage)
        
        return result
    
    def _generate_hook_config(self, contract: Dict, stage: str) -> Dict:
        """Generate hook configuration from contract"""
        return {
            "name": f"gl_{stage}_hook",
            "action": f"execute_{stage}",
            "contract_id": contract.get("metadata", {}).get("name", "unknown"),
            "version": contract.get("version", "1.0.0"),
            "config": contract.get("trigger", {}).get("validation", {}),
            "fallback": contract.get("fallback", {})
        }
    
    def _log_event(self, event: GovernanceEvent):
        """Log governance event"""
        logs_dir = self.base_path / "ecosystem" / "logs" / "governance-events"
        logs_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = logs_dir / "events.log"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps({
                "event_type": event.event_type,
                "contract_id": event.contract_id,
                "stage": event.stage,
                "timestamp": event.timestamp,
                "payload": event.payload
            }) + "\n")
    
    def _handle_validation_failure(self, event: GovernanceEvent):
        """Handle validation failure event"""
        # Could trigger:
        # - Block PR merge
        # - Create issue
        # - Send notification
        pass
    
    def _handle_audit_failure(self, event: GovernanceEvent):
        """Handle audit failure event"""
        # Could trigger:
        # - Request evidence
        # - Mark operation as non-compliant
        # - Schedule re-audit
        pass
    
    def _handle_quality_gate_failure(self, event: GovernanceEvent):
        """Handle quality gate failure event"""
        # Could trigger:
        # - Block deployment
        # - Generate remediation guide
        # - Notify team
        pass
    
    def get_binding_info(self, binding_id: str) -> Optional[Dict]:
        """Get information about a contract binding"""
        return self.bindings.get(binding_id)
    
    def get_hooks_for_stage(self, stage: str, platform: str = "all") -> List[Dict]:
        """Get hooks for a specific stage and platform"""
        if stage not in self.hooks:
            return []
        
        if platform in self.hooks[stage]:
            return self.hooks[stage][platform]
        
        if "all" in self.hooks[stage]:
            return self.hooks[stage]["all"]
        
        return []
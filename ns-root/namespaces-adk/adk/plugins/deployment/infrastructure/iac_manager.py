"""
Infrastructure as Code Manager - Terraform configuration management
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class TerraformState:
    """Terraform state information"""
    workspace: str
    resources: List[Dict[str, Any]]
    outputs: Dict[str, Any]
    version: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'workspace': self.workspace,
            'resources': self.resources,
            'outputs': self.outputs,
            'version': self.version
        }


class IaCManager:
    """Infrastructure as Code manager using Terraform"""
    
    def __init__(self, provider: str, config: Dict[str, Any], terraform_dir: Optional[str] = None):
        """Initialize IaC manager"""
        self.provider = provider
        self.config = config
        self.terraform_dir = Path(terraform_dir) if terraform_dir else Path.cwd() / 'terraform'
        self.workspaces: Dict[str, TerraformState] = {}
        
        logger.info(f"IaCManager initialized for provider: {provider}, terraform_dir: {self.terraform_dir}")
    
    async def initialize_terraform(self) -> Dict[str, Any]:
        """Initialize Terraform working directory"""
        logger.info("Initializing Terraform...")
        
        try:
            self.terraform_dir.mkdir(parents=True, exist_ok=True)
            
            result = await self._run_terraform_command(['init'])
            
            if result['returncode'] == 0:
                logger.info("Terraform initialized successfully")
                return {'success': True, 'message': 'Terraform initialized successfully'}
            else:
                logger.error(f"Terraform init failed: {result['stderr']}")
                return {'success': False, 'error': result['stderr']}
                
        except Exception as e:
            logger.error(f"Terraform initialization error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def plan_infrastructure(self, var_file: Optional[str] = None) -> Dict[str, Any]:
        """Create Terraform plan"""
        logger.info("Creating Terraform plan...")
        
        try:
            cmd = ['plan']
            
            if var_file:
                cmd.extend(['-var-file', var_file])
            
            cmd.extend(['-out', 'terraform.plan'])
            
            result = await self._run_terraform_command(cmd)
            
            if result['returncode'] == 0:
                logger.info("Terraform plan created successfully")
                return {
                    'success': True,
                    'plan_file': 'terraform.plan',
                    'output': result['stdout']
                }
            else:
                logger.error(f"Terraform plan failed: {result['stderr']}")
                return {
                    'success': False,
                    'error': result['stderr']
                }
                
        except Exception as e:
            logger.error(f"Terraform plan error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def apply_infrastructure(self, plan_file: Optional[str] = None, auto_approve: bool = False) -> Dict[str, Any]:
        """Apply Terraform configuration"""
        logger.info("Applying Terraform configuration...")
        
        try:
            cmd = ['apply']
            
            if plan_file:
                cmd.append(plan_file)
            
            if auto_approve:
                cmd.append('-auto-approve')
            
            result = await self._run_terraform_command(cmd)
            
            if result['returncode'] == 0:
                logger.info("Terraform apply completed successfully")
                
                outputs = await self.get_outputs()
                
                return {
                    'success': True,
                    'output': result['stdout'],
                    'outputs': outputs
                }
            else:
                logger.error(f"Terraform apply failed: {result['stderr']}")
                return {
                    'success': False,
                    'error': result['stderr']
                }
                
        except Exception as e:
            logger.error(f"Terraform apply error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def destroy_infrastructure(self, auto_approve: bool = False) -> Dict[str, Any]:
        """Destroy Terraform-managed infrastructure"""
        logger.info("Destroying Terraform-managed infrastructure...")
        
        try:
            cmd = ['destroy']
            
            if auto_approve:
                cmd.append('-auto-approve')
            
            result = await self._run_terraform_command(cmd)
            
            if result['returncode'] == 0:
                logger.info("Terraform destroy completed successfully")
                return {
                    'success': True,
                    'output': result['stdout']
                }
            else:
                logger.error(f"Terraform destroy failed: {result['stderr']}")
                return {
                    'success': False,
                    'error': result['stderr']
                }
                
        except Exception as e:
            logger.error(f"Terraform destroy error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def get_outputs(self) -> Dict[str, Any]:
        """Get Terraform outputs"""
        try:
            result = await self._run_terraform_command(['output', '-json'])
            
            if result['returncode'] == 0:
                import json
                outputs = json.loads(result['stdout'])
                return outputs
            else:
                return {}
                
        except Exception as e:
            logger.error(f"Error getting outputs: {e}")
            return {}
    
    def _get_terraform_provider_type(self) -> str:
        """Map deployment provider to Terraform provider type"""
        if self.provider in ['aws', 'aws-eks']:
            return 'aws'
        elif self.provider in ['gcp', 'gcp-gke']:
            return 'gcp'
        elif self.provider in ['azure', 'azure-aks']:
            return 'azure'
        else:
            return 'aws'
    
    async def _run_terraform_command(self, args: List[str]) -> Dict[str, Any]:
        """Run Terraform command"""
        try:
            cmd = ['terraform'] + args
            
            result = subprocess.run(
                cmd,
                cwd=str(self.terraform_dir),
                capture_output=True,
                text=True,
                timeout=600
            )
            
            return {
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            
        except subprocess.TimeoutExpired:
            logger.error(f"Terraform command timed out: {' '.join(args)}")
            return {
                'returncode': -1,
                'stdout': '',
                'stderr': 'Command timed out'
            }
        except Exception as e:
            logger.error(f"Terraform command error: {e}")
            return {
                'returncode': -1,
                'stdout': '',
                'stderr': str(e)
            }
"""
Universal Deployment Manager - Enhanced orchestration with planning, validation, and rollback
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
import logging
import time
import asyncio

from ..adapters.provider_factory import ProviderAdapterFactory, ProviderAdapter
from ..detectors.environment_detector import EnvironmentDetector
from ..loaders.config_loader import ConfigLoader

logger = logging.getLogger(__name__)


@dataclass
class DeploymentResult:
    """Enhanced deployment result with detailed information"""
    success: bool
    provider: str
    environment: str
    resources: Dict[str, Any]
    errors: List[str]
    warnings: List[str]
    duration: float
    steps_completed: List[str] = field(default_factory=list)
    steps_failed: List[str] = field(default_factory=list)
    rollback_executed: bool = False
    rollback_success: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'success': self.success,
            'provider': self.provider,
            'environment': self.environment,
            'resources': self.resources,
            'errors': self.errors,
            'warnings': self.warnings,
            'duration': self.duration,
            'steps_completed': self.steps_completed,
            'steps_failed': self.steps_failed,
            'rollback_executed': self.rollback_executed,
            'rollback_success': self.rollback_success,
            'metadata': self.metadata
        }
    
    def has_errors(self) -> bool:
        """Check if deployment has errors"""
        return len(self.errors) > 0
    
    def has_warnings(self) -> bool:
        """Check if deployment has warnings"""
        return len(self.warnings) > 0


@dataclass
class DeploymentStep:
    """Individual deployment step"""
    name: str
    description: str
    action: Callable
    dependencies: List[str] = field(default_factory=list)
    rollback_action: Optional[Callable] = None
    timeout: int = 300
    retry_count: int = 0
    critical: bool = True  # If True, failure stops deployment
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'description': self.description,
            'dependencies': self.dependencies,
            'timeout': self.timeout,
            'retry_count': self.retry_count,
            'critical': self.critical
        }


@dataclass
class DeploymentPlan:
    """Deployment plan with steps and dependencies"""
    steps: List[DeploymentStep]
    dependencies: Dict[str, List[str]]
    rollback_steps: List[DeploymentStep]
    estimated_duration: float
    validation_rules: List[Callable] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'steps': [step.to_dict() for step in self.steps],
            'dependencies': self.dependencies,
            'rollback_steps': [step.to_dict() for step in self.rollback_steps],
            'estimated_duration': self.estimated_duration,
            'metadata': self.metadata
        }
    
    def get_step_names(self) -> List[str]:
        """Get list of step names"""
        return [step.name for step in self.steps]
    
    def get_rollback_step_names(self) -> List[str]:
        """Get list of rollback step names"""
        return [step.name for step in self.rollback_steps]


class DeploymentValidator:
    """Deployment configuration validator"""
    
    @staticmethod
    def validate_infrastructure_config(config: Dict[str, Any]) -> List[str]:
        """Validate infrastructure configuration"""
        errors = []
        
        # Check for required fields
        if 'infrastructure' not in config:
            errors.append("Missing 'infrastructure' section in configuration")
            return errors
        
        infra = config['infrastructure']
        
        # Validate VPC configuration if enabled
        if infra.get('vpc', {}).get('enabled'):
            vpc = infra['vpc']
            if 'cidr' not in vpc:
                errors.append("VPC enabled but missing CIDR")
            elif not DeploymentValidator._is_valid_cidr(vpc['cidr']):
                errors.append(f"Invalid VPC CIDR: {vpc['cidr']}")
        
        # Validate Kubernetes configuration if enabled
        if infra.get('kubernetes', {}).get('enabled'):
            k8s = infra['kubernetes']
            if 'version' not in k8s:
                errors.append("Kubernetes enabled but missing version")
        
        # Validate database configuration if enabled
        if infra.get('database', {}).get('enabled'):
            db = infra['database']
            if 'engine' not in db:
                errors.append("Database enabled but missing engine")
            if 'instance_class' not in db:
                errors.append("Database enabled but missing instance_class")
        
        return errors
    
    @staticmethod
    def _is_valid_cidr(cidr: str) -> bool:
        """Validate CIDR notation"""
        import ipaddress
        try:
            ipaddress.ip_network(cidr)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_resource_limits(config: Dict[str, Any]) -> List[str]:
        """Validate resource limits"""
        warnings = []
        
        # Check resource defaults
        resources = config.get('resources', {})
        
        if 'requests' in resources:
            requests = resources['requests']
            cpu = requests.get('cpu', '0')
            memory = requests.get('memory', '0')
            
            # Warn if too low
            if cpu == '0':
                warnings.append("CPU request is zero, may cause scheduling issues")
            if memory == '0':
                warnings.append("Memory request is zero, may cause OOM kills")
        
        return warnings


class UniversalDeploymentManager:
    """Enhanced universal deployment manager with planning and rollback support"""
    
    def __init__(
        self,
        provider: Optional[str] = None,
        environment: str = 'production',
        config_file: Optional[str] = None,
        auto_detect: bool = True,
        dry_run: bool = False,
        auto_rollback: bool = False,
        validate_before_deploy: bool = True,
        timeout: int = 3600
    ):
        """Initialize deployment manager"""
        self.environment = environment
        self.config_file = config_file
        self.auto_detect = auto_detect
        self.dry_run = dry_run
        self.auto_rollback = auto_rollback
        self.validate_before_deploy = validate_before_deploy
        self.timeout = timeout
        
        # Initialize components
        self.environment_detector = EnvironmentDetector()
        self.config_loader = ConfigLoader()
        self.validator = DeploymentValidator()
        
        # Detect or set provider
        if provider:
            self.provider = provider
        elif auto_detect:
            env_info = self.environment_detector.detect()
            self.provider = env_info.provider
            self.detected_environment = env_info
        else:
            raise ValueError("Provider must be specified or auto_detect must be enabled")
        
        # Load configuration
        self.config = self._load_configuration()
        
        # Create provider adapter
        self.adapter = self._create_adapter()
        
        # Deployment state
        self.deployment_steps = []
        self.rollback_steps = []
        self.errors = []
        self.warnings = []
        self.resources_created = []
        self.rollback_resources = []
        
        logger.info(f"Deployment manager initialized: provider={self.provider}, environment={self.environment}")
    
    def _load_configuration(self) -> Dict[str, Any]:
        """Load configuration"""
        logger.info(f"Loading configuration for provider: {self.provider}")
        
        config = self.config_loader.load_config(
            provider=self.provider,
            environment=self.environment,
            config_file=self.config_file,
            include_secrets=True
        )
        
        # Add provider and environment to config
        config['provider'] = self.provider
        config['environment'] = self.environment
        
        logger.info(f"Configuration loaded successfully")
        return config
    
    def _create_adapter(self) -> ProviderAdapter:
        """Create provider adapter"""
        logger.info(f"Creating adapter for provider: {self.provider}")
        
        try:
            adapter = ProviderAdapterFactory.get_adapter(self.provider, self.config)
            
            # Validate configuration
            if self.validate_before_deploy:
                if not adapter.validate_config(self.config):
                    raise ValueError(f"Configuration validation failed for provider: {self.provider}")
            
            logger.info(f"Adapter created and validated successfully")
            return adapter
            
        except Exception as e:
            logger.error(f"Failed to create adapter: {e}")
            raise
    
    async def create_deployment_plan(self) -> DeploymentPlan:
        """
        Create deployment plan with steps and dependencies
        
        Returns a detailed plan that can be reviewed before deployment
        """
        logger.info("Creating deployment plan...")
        
        steps = []
        rollback_steps = []
        dependencies = {}
        estimated_duration = 0.0
        
        # Analyze configuration to determine deployment steps
        infra = self.config.get('infrastructure', {})
        
        # Step 1: Deploy VPC (if enabled)
        if infra.get('vpc', {}).get('enabled'):
            step = DeploymentStep(
                name='deploy-vpc',
                description='Deploy VPC and network infrastructure',
                action=self._deploy_vpc,
                rollback_action=self._delete_vpc,
                timeout=600,
                retry_count=0,
                critical=True
            )
            steps.append(step)
            estimated_duration += 300
        
        # Step 2: Deploy Kubernetes cluster (if enabled)
        if infra.get('kubernetes', {}).get('enabled'):
            step = DeploymentStep(
                name='deploy-kubernetes',
                description='Deploy Kubernetes cluster',
                action=self._deploy_kubernetes_cluster,
                dependencies=['deploy-vpc'] if infra.get('vpc', {}).get('enabled') else [],
                rollback_action=self._delete_kubernetes_cluster,
                timeout=1800,
                retry_count=0,
                critical=True
            )
            steps.append(step)
            dependencies['deploy-kubernetes'] = step.dependencies
            estimated_duration += 900
        
        # Step 3: Deploy databases (if enabled)
        if infra.get('database', {}).get('enabled'):
            step = DeploymentStep(
                name='deploy-database',
                description='Deploy database instances',
                action=self._deploy_database,
                dependencies=['deploy-vpc'] if infra.get('vpc', {}).get('enabled') else [],
                rollback_action=self._delete_database,
                timeout=1200,
                retry_count=1,
                critical=True
            )
            steps.append(step)
            dependencies['deploy-database'] = step.dependencies
            estimated_duration += 600
        
        # Step 4: Deploy storage (if enabled)
        if infra.get('storage', {}).get('enabled'):
            step = DeploymentStep(
                name='deploy-storage',
                description='Deploy storage resources',
                action=self._deploy_storage,
                timeout=300,
                retry_count=2,
                critical=False
            )
            steps.append(step)
            estimated_duration += 150
        
        # Step 5: Deploy load balancers (if enabled)
        if infra.get('load_balancer', {}).get('enabled'):
            step = DeploymentStep(
                name='deploy-load-balancer',
                description='Deploy load balancer',
                action=self._deploy_load_balancer,
                dependencies=['deploy-vpc'] if infra.get('vpc', {}).get('enabled') else [],
                rollback_action=self._delete_load_balancer,
                timeout=300,
                retry_count=1,
                critical=False
            )
            steps.append(step)
            dependencies['deploy-load-balancer'] = step.dependencies
            estimated_duration += 150
        
        # Step 6: Deploy monitoring (if enabled)
        if self.config.get('monitoring', {}).get('enabled'):
            step = DeploymentStep(
                name='deploy-monitoring',
                description='Deploy monitoring and alerting',
                action=self._deploy_monitoring,
                timeout=600,
                retry_count=1,
                critical=False
            )
            steps.append(step)
            estimated_duration += 300
        
        # Create rollback steps (reverse order)
        for step in reversed(steps):
            if step.rollback_action:
                rollback_step = DeploymentStep(
                    name=f'rollback-{step.name}',
                    description=f'Rollback {step.description}',
                    action=step.rollback_action,
                    timeout=step.timeout,
                    critical=False
                )
                rollback_steps.append(rollback_step)
        
        plan = DeploymentPlan(
            steps=steps,
            dependencies=dependencies,
            rollback_steps=rollback_steps,
            estimated_duration=estimated_duration,
            metadata={
                'provider': self.provider,
                'environment': self.environment,
                'dry_run': self.dry_run,
                'created_at': time.time()
            }
        )
        
        logger.info(f"Deployment plan created with {len(steps)} steps, estimated duration: {estimated_duration}s")
        return plan
    
    async def validate_deployment_plan(self, plan: DeploymentPlan) -> List[str]:
        """Validate deployment plan before execution"""
        errors = []
        
        # Validate infrastructure configuration
        infra_errors = self.validator.validate_infrastructure_config(self.config)
        errors.extend(infra_errors)
        
        # Validate resource limits
        warnings = self.validator.validate_resource_limits(self.config)
        self.warnings.extend(warnings)
        
        # Check for circular dependencies
        if self._has_circular_dependencies(plan):
            errors.append("Deployment plan has circular dependencies")
        
        # Validate all steps have actions
        for step in plan.steps:
            if not step.action:
                errors.append(f"Step '{step.name}' has no action defined")
        
        return errors
    
    def _has_circular_dependencies(self, plan: DeploymentPlan) -> bool:
        """Check for circular dependencies in deployment plan"""
        # Simple cycle detection using DFS
        visited = set()
        recursion_stack = set()
        
        def has_cycle(node):
            visited.add(node)
            recursion_stack.add(node)
            
            for neighbor in plan.dependencies.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in recursion_stack:
                    return True
            
            recursion_stack.remove(node)
            return False
        
        for step_name in plan.get_step_names():
            if step_name not in visited:
                if has_cycle(step_name):
                    return True
        
        return False
    
    async def deploy(self) -> DeploymentResult:
        """
        Deploy infrastructure with automatic planning and validation
        
        Returns detailed deployment result
        """
        logger.info(f"Starting deployment to {self.provider} ({self.environment})...")
        
        start_time = time.time()
        steps_completed = []
        steps_failed = []
        resources_created = {}
        errors = []
        warnings = []
        rollback_executed = False
        rollback_success = False
        
        try:
            # Validate configuration
            if self.validate_before_deploy:
                logger.info("Validating configuration...")
                infra_errors = self.validator.validate_infrastructure_config(self.config)
                warnings.extend(self.validator.validate_resource_limits(self.config))
                
                if infra_errors:
                    errors.extend(infra_errors)
                    logger.error(f"Configuration validation failed: {infra_errors}")
                    return self._create_deployment_result(
                        success=False,
                        steps_completed=steps_completed,
                        steps_failed=steps_failed,
                        resources=resources_created,
                        errors=errors,
                        warnings=warnings,
                        rollback_executed=False,
                        rollback_success=False,
                        duration=time.time() - start_time
                    )
            
            # Create deployment plan
            logger.info("Creating deployment plan...")
            plan = await self.create_deployment_plan()
            
            # Validate deployment plan
            if self.validate_before_deploy:
                logger.info("Validating deployment plan...")
                plan_errors = await self.validate_deployment_plan(plan)
                if plan_errors:
                    errors.extend(plan_errors)
                    logger.error(f"Deployment plan validation failed: {plan_errors}")
                    return self._create_deployment_result(
                        success=False,
                        steps_completed=steps_completed,
                        steps_failed=steps_failed,
                        resources=resources_created,
                        errors=errors,
                        warnings=warnings,
                        rollback_executed=False,
                        rollback_success=False,
                        duration=time.time() - start_time
                    )
            
            # Print deployment plan
            logger.info(f"Deployment plan: {len(plan.steps)} steps, estimated {plan.estimated_duration:.0f}s")
            for step in plan.steps:
                logger.info(f"  - {step.name}: {step.description}")
            
            # Check dry run
            if self.dry_run:
                logger.info("DRY RUN MODE - No actual deployment will be performed")
                return self._create_deployment_result(
                    success=True,
                    steps_completed=[step.name for step in plan.steps],
                    steps_failed=[],
                    resources={},
                    errors=[],
                    warnings=warnings,
                    rollback_executed=False,
                    rollback_success=False,
                    duration=time.time() - start_time,
                    metadata={'dry_run': True}
                )
            
            # Execute deployment plan
            logger.info("Executing deployment plan...")
            for step in plan.steps:
                try:
                    logger.info(f"Executing step: {step.name}")
                    
                    # Check dependencies
                    for dep in step.dependencies:
                        if dep not in steps_completed:
                            errors.append(f"Dependency '{dep}' not completed for step '{step.name}'")
                            if step.critical:
                                raise RuntimeError(f"Dependency '{dep}' not completed")
                    
                    # Execute step with retry
                    step_result = await self._execute_step_with_retry(step)
                    
                    if step_result['success']:
                        steps_completed.append(step.name)
                        if step_result.get('resources'):
                            resources_created.update(step_result['resources'])
                        self.resources_created.extend(step_result.get('created', []))
                        logger.info(f"Step completed: {step.name}")
                    else:
                        error_msg = f"Step failed: {step.name} - {step_result.get('error', 'Unknown error')}"
                        errors.append(error_msg)
                        steps_failed.append(step.name)
                        logger.error(error_msg)
                        
                        if step.critical:
                            logger.error(f"Critical step failed, initiating rollback...")
                            if self.auto_rollback:
                                rollback_executed = True
                                rollback_success = await self._execute_rollback(plan, steps_completed)
                            break
                            
                except Exception as e:
                    error_msg = f"Step error: {step.name} - {str(e)}"
                    errors.append(error_msg)
                    steps_failed.append(step.name)
                    logger.error(error_msg, exc_info=True)
                    
                    if step.critical:
                        logger.error(f"Critical step error, initiating rollback...")
                        if self.auto_rollback:
                            rollback_executed = True
                            rollback_success = await self._execute_rollback(plan, steps_completed)
                        break
            
            # Determine success
            success = len(steps_failed) == 0
            
            logger.info(f"Deployment completed: {'SUCCESS' if success else 'FAILED'}")
            logger.info(f"Steps completed: {len(steps_completed)}/{len(plan.steps)}")
            logger.info(f"Duration: {time.time() - start_time:.2f}s")
            
            return self._create_deployment_result(
                success=success,
                steps_completed=steps_completed,
                steps_failed=steps_failed,
                resources=resources_created,
                errors=errors,
                warnings=warnings,
                rollback_executed=rollback_executed,
                rollback_success=rollback_success,
                duration=time.time() - start_time
            )
            
        except Exception as e:
            logger.error(f"Deployment error: {e}", exc_info=True)
            errors.append(str(e))
            
            # Attempt rollback if auto_rollback enabled
            if self.auto_rollback and steps_completed:
                rollback_executed = True
                rollback_success = await self._execute_rollback(plan if 'plan' in locals() else None, steps_completed)
            
            return self._create_deployment_result(
                success=False,
                steps_completed=steps_completed,
                steps_failed=steps_failed,
                resources=resources_created,
                errors=errors,
                warnings=warnings,
                rollback_executed=rollback_executed,
                rollback_success=rollback_success,
                duration=time.time() - start_time
            )
    
    async def _execute_step_with_retry(self, step: DeploymentStep) -> Dict[str, Any]:
        """Execute step with retry logic"""
        for attempt in range(step.retry_count + 1):
            try:
                result = await step.action()
                return {
                    'success': True,
                    'resources': result.get('resources', {}),
                    'created': result.get('created', [])
                }
            except Exception as e:
                if attempt < step.retry_count:
                    logger.warning(f"Step {step.name} failed (attempt {attempt + 1}/{step.retry_count + 1}), retrying...")
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                else:
                    return {
                        'success': False,
                        'error': str(e)
                    }
    
    async def _execute_rollback(self, plan: Optional[DeploymentPlan], completed_steps: List[str]) -> bool:
        """Execute rollback for completed steps"""
        if not plan:
            logger.warning("No deployment plan available for rollback")
            return False
        
        logger.info(f"Executing rollback for {len(completed_steps)} completed steps...")
        
        # Find rollback steps for completed steps (in reverse order)
        rollback_steps_to_execute = []
        for step_name in reversed(completed_steps):
            for rollback_step in plan.rollback_steps:
                if rollback_step.name == f'rollback-{step_name}':
                    rollback_steps_to_execute.append(rollback_step)
                    break
        
        # Execute rollback steps
        for rollback_step in rollback_steps_to_execute:
            try:
                logger.info(f"Executing rollback step: {rollback_step.name}")
                await rollback_step.action()
                logger.info(f"Rollback step completed: {rollback_step.name}")
            except Exception as e:
                logger.error(f"Rollback step failed: {rollback_step.name} - {e}")
        
        logger.info("Rollback completed")
        return True
    
    def _create_deployment_result(
        self,
        success: bool,
        steps_completed: List[str],
        steps_failed: List[str],
        resources: Dict[str, Any],
        errors: List[str],
        warnings: List[str],
        rollback_executed: bool,
        rollback_success: bool,
        duration: float,
        metadata: Optional[Dict[str, Any]] = None
    ) -> DeploymentResult:
        """Create deployment result"""
        return DeploymentResult(
            success=success,
            provider=self.provider,
            environment=self.environment,
            resources=resources,
            errors=errors,
            warnings=warnings,
            duration=duration,
            steps_completed=steps_completed,
            steps_failed=steps_failed,
            rollback_executed=rollback_executed,
            rollback_success=rollback_success,
            metadata=metadata or {}
        )
    
    # Deployment step actions (placeholder implementations)
    async def _deploy_vpc(self) -> Dict[str, Any]:
        """Deploy VPC"""
        logger.info("Deploying VPC...")
        # In real implementation, this would call the adapter
        return {'resources': {'vpc': 'vpc-12345'}, 'created': ['vpc-12345']}
    
    async def _delete_vpc(self):
        """Delete VPC (rollback)"""
        logger.info("Deleting VPC...")
    
    async def _deploy_kubernetes_cluster(self) -> Dict[str, Any]:
        """Deploy Kubernetes cluster"""
        logger.info("Deploying Kubernetes cluster...")
        return {'resources': {'cluster': 'my-cluster'}, 'created': ['my-cluster']}
    
    async def _delete_kubernetes_cluster(self):
        """Delete Kubernetes cluster (rollback)"""
        logger.info("Deleting Kubernetes cluster...")
    
    async def _deploy_database(self) -> Dict[str, Any]:
        """Deploy database"""
        logger.info("Deploying database...")
        return {'resources': {'database': 'my-db'}, 'created': ['my-db']}
    
    async def _delete_database(self):
        """Delete database (rollback)"""
        logger.info("Deleting database...")
    
    async def _deploy_storage(self) -> Dict[str, Any]:
        """Deploy storage"""
        logger.info("Deploying storage...")
        return {'resources': {'storage': 'my-storage'}, 'created': ['my-storage']}
    
    async def _deploy_load_balancer(self) -> Dict[str, Any]:
        """Deploy load balancer"""
        logger.info("Deploying load balancer...")
        return {'resources': {'load_balancer': 'my-lb'}, 'created': ['my-lb']}
    
    async def _delete_load_balancer(self):
        """Delete load balancer (rollback)"""
        logger.info("Deleting load balancer...")
    
    async def _deploy_monitoring(self) -> Dict[str, Any]:
        """Deploy monitoring"""
        logger.info("Deploying monitoring...")
        return {'resources': {'monitoring': 'my-monitoring'}, 'created': ['my-monitoring']}
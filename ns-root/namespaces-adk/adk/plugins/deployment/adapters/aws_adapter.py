"""
AWS Provider Adapter - Amazon Web Services Deployment
"""

import boto3
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class AWSConfig:
    """AWS configuration"""
    region: str
    profile: Optional[str] = None
    access_key: Optional[str] = None
    secret_key: Optional[str] = None
    session_token: Optional[str] = None


class AWSAdapter:
    """AWS cloud provider adapter implementation"""
    
    PROVIDER_NAME = "aws"
    PROVIDER_VERSION = "1.0.0"
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize AWS adapter"""
        if isinstance(config, AWSConfig):
            self.config = config
        else:
            self.config = AWSConfig(**config)
        
        # Initialize AWS clients
        self._init_clients()
    
    def _init_clients(self):
        """Initialize AWS clients"""
        session_kwargs = {}
        
        if self.config.profile:
            session_kwargs['profile_name'] = self.config.profile
        elif self.config.access_key and self.config.secret_key:
            session_kwargs['aws_access_key_id'] = self.config.access_key
            session_kwargs['aws_secret_access_key'] = self.config.secret_key
            if self.config.session_token:
                session_kwargs['aws_session_token'] = self.config.session_token
        
        try:
            self.session = boto3.Session(**session_kwargs, region_name=self.config.region)
            
            self.ec2 = self.session.client('ec2')
            self.eks = self.session.client('eks')
            self.rds = self.session.client('rds')
            self.s3 = self.session.client('s3')
            self.elb = self.session.client('elbv2')
            self.iam = self.session.client('iam')
            self.route53 = self.session.client('route53')
            self.cloudwatch = self.session.client('cloudwatch')
            self.secrets_manager = self.session.client('secretsmanager')
            self.lambda_client = self.session.client('lambda')
            
            logger.info(f"AWS clients initialized for region: {self.config.region}")
        except Exception as e:
            logger.error(f"Failed to initialize AWS clients: {e}")
            raise
    
    async def validate_config(self, config: dict) -> bool:
        """Validate AWS configuration"""
        required_fields = ['region']
        
        for field in required_fields:
            if field not in config:
                logger.error(f"Missing required configuration field: {field}")
                return False
        
        # Validate region
        valid_regions = [
            'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2',
            'eu-west-1', 'eu-west-2', 'eu-west-3',
            'ap-northeast-1', 'ap-northeast-2', 'ap-southeast-1', 'ap-southeast-2',
            'ca-central-1', 'sa-east-1'
        ]
        
        if config['region'] not in valid_regions:
            logger.warning(f"Region {config['region']} might not be valid")
        
        return True
    
    async def deploy_infrastructure(self, infra_config: dict) -> dict:
        """Deploy AWS infrastructure"""
        logger.info(f"Deploying AWS infrastructure in {self.config.region}")
        
        results = {}
        
        try:
            # Deploy VPC
            if 'vpc' in infra_config:
                results['vpc'] = await self._deploy_vpc(infra_config['vpc'])
            
            # Deploy EKS cluster
            if 'kubernetes' in infra_config:
                results['cluster'] = await self._deploy_eks_cluster(infra_config['kubernetes'])
            
            # Deploy databases
            if 'database' in infra_config:
                results['databases'] = await self._deploy_databases(infra_config['database'])
            
            # Deploy storage
            if 'storage' in infra_config:
                results['storage'] = await self._deploy_storage(infra_config['storage'])
            
            # Deploy load balancer
            if 'load_balancer' in infra_config:
                results['load_balancer'] = await self._deploy_load_balancer(infra_config['load_balancer'])
            
            logger.info("AWS infrastructure deployment completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"Failed to deploy AWS infrastructure: {e}")
            raise
    
    async def _deploy_vpc(self, vpc_config: dict) -> dict:
        """Deploy VPC and related resources"""
        logger.info("Deploying VPC")
        
        # Create VPC
        vpc_response = self.ec2.create_vpc(
            CidrBlock=vpc_config.get('cidr', '10.0.0.0/16'),
            AmazonProvidedIPv6CidrBlock=vpc_config.get('enable_ipv6', False),
            InstanceTenancy=vpc_config.get('tenancy', 'default')
        )
        vpc_id = vpc_response['Vpc']['VpcId']
        
        # Enable DNS support
        self.ec2.modify_vpc_attribute(
            VpcId=vpc_id,
            EnableDnsSupport={'Value': vpc_config.get('enable_dns_support', True)}
        )
        
        self.ec2.modify_vpc_attribute(
            VpcId=vpc_id,
            EnableDnsHostnames={'Value': vpc_config.get('enable_dns_hostnames', True)}
        )
        
        # Tag VPC
        self.ec2.create_tags(
            Resources=[vpc_id],
            Tags=[{'Key': 'Name', 'Value': vpc_config.get('name', 'main-vpc')}]
        )
        
        # Create subnets
        subnets = []
        for subnet_config in vpc_config.get('subnets', []):
            subnet = await self._create_subnet(vpc_id, subnet_config)
            subnets.append(subnet)
        
        # Create internet gateway
        igw_response = self.ec2.create_internet_gateway()
        igw_id = igw_response['InternetGateway']['InternetGatewayId']
        self.ec2.attach_internet_gateway(
            InternetGatewayId=igw_id,
            VpcId=vpc_id
        )
        
        # Create route tables
        await self._create_route_tables(vpc_id, subnets, igw_id)
        
        # Create security groups
        security_groups = []
        for sg_config in vpc_config.get('security_groups', []):
            sg = await self._create_security_group(vpc_id, sg_config)
            security_groups.append(sg)
        
        logger.info(f"VPC deployed: {vpc_id}")
        
        return {
            'vpc_id': vpc_id,
            'cidr': vpc_config.get('cidr'),
            'subnets': subnets,
            'internet_gateway': igw_id,
            'security_groups': security_groups
        }
    
    async def _create_subnet(self, vpc_id: str, subnet_config: dict) -> dict:
        """Create subnet"""
        response = self.ec2.create_subnet(
            VpcId=vpc_id,
            CidrBlock=subnet_config['cidr'],
            AvailabilityZone=subnet_config.get('availability_zone'),
            MapPublicIpOnLaunch=(subnet_config.get('type') == 'public')
        )
        
        subnet_id = response['Subnet']['SubnetId']
        
        # Tag subnet
        self.ec2.create_tags(
            Resources=[subnet_id],
            Tags=[{'Key': 'Name', 'Value': subnet_config['name']}]
        )
        
        # Auto-assign public IP for public subnets
        if subnet_config.get('type') == 'public':
            self.ec2.modify_subnet_attribute(
                SubnetId=subnet_id,
                MapPublicIpOnLaunch={'Value': True}
            )
        
        logger.info(f"Subnet created: {subnet_id} ({subnet_config['name']})")
        
        return {
            'subnet_id': subnet_id,
            'name': subnet_config['name'],
            'cidr': subnet_config['cidr'],
            'type': subnet_config.get('type', 'private')
        }
    
    async def _create_route_tables(self, vpc_id: str, subnets: List[dict], igw_id: str):
        """Create route tables and associate with subnets"""
        # Create main route table
        route_table_response = self.ec2.create_route_table(VpcId=vpc_id)
        route_table_id = route_table_response['RouteTable']['RouteTableId']
        
        # Add route to internet gateway for public subnets
        public_subnets = [s for s in subnets if s.get('type') == 'public']
        if public_subnets:
            try:
                self.ec2.create_route(
                    RouteTableId=route_table_id,
                    DestinationCidrBlock='0.0.0.0/0',
                    GatewayId=igw_id
                )
            except self.ec2.exceptions.RouteAlreadyExistsException as exc:
                # Route already exists; treat as idempotent and continue
                logger.debug(
                    "Route already exists for route table %s and internet gateway %s: %s",
                    route_table_id,
                    igw_id,
                    exc,
                )
        
        # Associate route tables with subnets
        for subnet in subnets:
            self.ec2.associate_route_table(
                RouteTableId=route_table_id,
                SubnetId=subnet['subnet_id']
            )
    
    async def _create_security_group(self, vpc_id: str, sg_config: dict) -> dict:
        """Create security group and rules"""
        response = self.ec2.create_security_group(
            GroupName=sg_config['name'],
            Description=sg_config.get('description', ''),
            VpcId=vpc_id
        )
        
        sg_id = response['GroupId']
        
        # Add ingress rules
        for rule in sg_config.get('rules', []):
            if rule.get('type') == 'ingress':
                try:
                    self.ec2.authorize_security_group_ingress(
                        GroupId=sg_id,
                        IpPermissions=[{
                            'IpProtocol': rule['protocol'],
                            'FromPort': int(rule['port']),
                            'ToPort': int(rule['port']),
                            'IpRanges': [{'CidrIp': rule['source']}]
                        }]
                    )
                except Exception as e:
                    logger.warning(f"Failed to add ingress rule: {e}")
        
        # Add egress rules
        for rule in sg_config.get('rules', []):
            if rule.get('type') == 'egress':
                try:
                    self.ec2.authorize_security_group_egress(
                        GroupId=sg_id,
                        IpPermissions=[{
                            'IpProtocol': rule['protocol'],
                            'FromPort': int(rule['port']),
                            'ToPort': int(rule['port']),
                            'IpRanges': [{'CidrIp': rule.get('destination', '0.0.0.0/0')}]
                        }]
                    )
                except Exception as e:
                    logger.warning(f"Failed to add egress rule: {e}")
        
        logger.info(f"Security group created: {sg_id}")
        
        return {
            'security_group_id': sg_id,
            'name': sg_config['name']
        }
    
    async def _deploy_eks_cluster(self, k8s_config: dict) -> dict:
        """Deploy EKS cluster"""
        logger.info(f"Deploying EKS cluster: {k8s_config.get('name')}")
        
        # Create IAM role for EKS
        role_name = f"{k8s_config['name']}-cluster-role"
        role_arn = await self._create_eks_cluster_role(role_name)
        
        # Create EKS cluster
        cluster_response = self.eks.create_cluster(
            name=k8s_config['name'],
            roleArn=role_arn,
            resourcesVpcConfig={
                'subnetIds': k8s_config.get('subnet_ids', []),
                'securityGroupIds': k8s_config.get('security_group_ids', []),
                'endpointPublicAccess': k8s_config.get('endpoint_public_access', True),
                'endpointPrivateAccess': k8s_config.get('endpoint_private_access', False)
            },
            version=k8s_config.get('version', '1.28'),
            logging=k8s_config.get('logging', {
                'clusterLogging': [{'types': ['api', 'audit', 'authenticator'], 'enabled': True}]
            })
        )
        
        cluster_name = cluster_response['cluster']['name']
        
        logger.info(f"EKS cluster created: {cluster_name}")
        
        # Create node groups
        node_groups = []
        for node_pool in k8s_config.get('node_pools', []):
            ng = await self._create_node_group(cluster_name, node_pool)
            node_groups.append(ng)
        
        return {
            'cluster_name': cluster_name,
            'cluster_arn': cluster_response['cluster']['arn'],
            'endpoint': cluster_response['cluster']['endpoint'],
            'certificate': cluster_response['cluster']['certificateAuthority']['data'],
            'role_arn': role_arn,
            'node_groups': node_groups
        }
    
    async def _create_eks_cluster_role(self, role_name: str) -> str:
        """Create IAM role for EKS cluster"""
        trust_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": "eks.amazonaws.com"},
                    "Action": "sts:AssumeRole"
                }
            ]
        }
        
        try:
            response = self.iam.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(trust_policy),
                Description=f"IAM role for EKS cluster {role_name}"
            )
            role_arn = response['Role']['Arn']
            
            # Attach cluster policy
            self.iam.attach_role_policy(
                RoleName=role_name,
                PolicyArn='arn:aws:iam::aws:policy/AmazonEKSClusterPolicy'
            )
            
            # Attach VPC resource controller policy
            self.iam.attach_role_policy(
                RoleName=role_name,
                PolicyArn='arn:aws:iam::aws:policy/AmazonEKSVPCResourceController'
            )
            
            logger.info(f"IAM role created: {role_name}")
            return role_arn
            
        except self.iam.exceptions.EntityAlreadyExistsException:
            # Role exists, get its ARN
            response = self.iam.get_role(RoleName=role_name)
            logger.info(f"IAM role already exists: {role_name}")
            return response['Role']['Arn']
    
    async def _create_node_group(self, cluster_name: str, node_pool: dict) -> dict:
        """Create EKS node group"""
        logger.info(f"Creating node group: {node_pool['name']}")
        
        # Create node IAM role
        node_role_name = f"{cluster_name}-{node_pool['name']}-node-role"
        node_role_arn = await self._create_node_role(node_role_name)
        
        # Create node group
        response = self.eks.create_nodegroup(
            clusterName=cluster_name,
            nodegroupName=node_pool['name'],
            scalingConfig={
                'minSize': node_pool.get('min_nodes', 1),
                'maxSize': node_pool.get('max_nodes', 5),
                'desiredSize': node_pool.get('desired_nodes', 1)
            },
            subnets=node_pool.get('subnet_ids', []),
            instanceTypes=[node_pool['instance_type']],
            nodeRole=node_role_arn,
            labels=node_pool.get('labels', {}),
            taints=node_pool.get('taints', []),
            capacityType=node_pool.get('capacity_type', 'ON_DEMAND'),
            diskSize=node_pool.get('disk_size', 20),
            amiType=node_pool.get('ami_type', 'AL2_x86_64')
        )
        
        logger.info(f"Node group created: {node_pool['name']}")
        
        return {
            'nodegroup_name': node_pool['name'],
            'nodegroup_arn': response['nodegroup']['nodegroupArn'],
            'role_arn': node_role_arn
        }
    
    async def _create_node_role(self, role_name: str) -> str:
        """Create IAM role for EKS nodes"""
        trust_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": "ec2.amazonaws.com"},
                    "Action": "sts:AssumeRole"
                }
            ]
        }
        
        try:
            response = self.iam.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(trust_policy),
                Description=f"IAM role for EKS node {role_name}"
            )
            role_arn = response['Role']['Arn']
            
            # Attach node policies
            policies = [
                'arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy',
                'arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy',
                'arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly'
            ]
            
            for policy_arn in policies:
                self.iam.attach_role_policy(
                    RoleName=role_name,
                    PolicyArn=policy_arn
                )
            
            logger.info(f"Node role created: {role_name}")
            return role_arn
            
        except self.iam.exceptions.EntityAlreadyExistsException:
            response = self.iam.get_role(RoleName=role_name)
            logger.info(f"Node role already exists: {role_name}")
            return response['Role']['Arn']
    
    async def _deploy_databases(self, db_config: dict) -> List[dict]:
        """Deploy RDS instances"""
        logger.info("Deploying RDS instances")
        
        databases = []
        for instance_config in db_config.get('instances', []):
            db = await self._create_rds_instance(instance_config)
            databases.append(db)
        
        return databases
    
    async def _create_rds_instance(self, db_config: dict) -> dict:
        """Create RDS instance"""
        logger.info(f"Creating RDS instance: {db_config['name']}")
        
        response = self.rds.create_db_instance(
            DBInstanceIdentifier=db_config['name'],
            DBInstanceClass=db_config['instance_class'],
            Engine=db_config['engine'],
            EngineVersion=db_config.get('engine_version'),
            AllocatedStorage=db_config['storage'],
            StorageType=db_config.get('storage_type', 'gp2'),
            MasterUsername=db_config['master_username'],
            MasterUserPassword=db_config['master_password'],
            VpcSecurityGroupIds=db_config.get('security_group_ids', []),
            DBSubnetGroupName=db_config.get('subnet_group_name'),
            MultiAZ=db_config.get('multi_az', False),
            BackupRetentionPeriod=db_config.get('backup_retention', 7),
            StorageEncrypted=db_config.get('encryption', True),
            PubliclyAccessible=False,
            DeletionProtection=db_config.get('deletion_protection', True)
        )
        
        logger.info(f"RDS instance created: {db_config['name']}")
        
        return {
            'db_instance_id': db_config['name'],
            'endpoint': response['DBInstance']['Endpoint']['Address'],
            'port': response['DBInstance']['Endpoint']['Port'],
            'engine': db_config['engine'],
            'instance_class': db_config['instance_class']
        }
    
    async def _deploy_storage(self, storage_config: dict) -> List[dict]:
        """Deploy S3 buckets"""
        logger.info("Deploying S3 buckets")
        
        buckets = []
        for bucket_config in storage_config.get('buckets', []):
            bucket = await self._create_s3_bucket(bucket_config)
            buckets.append(bucket)
        
        return buckets
    
    async def _create_s3_bucket(self, bucket_config: dict) -> dict:
        """Create S3 bucket"""
        logger.info(f"Creating S3 bucket: {bucket_config['name']}")
        
        bucket_args = {'Bucket': bucket_config['name']}
        
        # For regions other than us-east-1, specify LocationConstraint
        if self.config.region != 'us-east-1':
            bucket_args['CreateBucketConfiguration'] = {
                'LocationConstraint': self.config.region
            }
        
        try:
            self.s3.create_bucket(**bucket_args)
        except self.s3.exceptions.BucketAlreadyExists:
            logger.warning(f"Bucket already exists: {bucket_config['name']}")
        except self.s3.exceptions.BucketAlreadyOwnedByYou:
            logger.info(f"Bucket already owned: {bucket_config['name']}")
        
        # Enable versioning
        if bucket_config.get('versioning', False):
            self.s3.put_bucket_versioning(
                Bucket=bucket_config['name'],
                VersioningConfiguration={'Status': 'Enabled'}
            )
        
        # Set lifecycle configuration
        if bucket_config.get('lifecycle'):
            try:
                self.s3.put_bucket_lifecycle_configuration(
                    Bucket=bucket_config['name'],
                    LifecycleConfiguration=bucket_config['lifecycle']
                )
            except Exception as e:
                logger.warning(f"Failed to set lifecycle: {e}")
        
        # Set bucket policy
        if bucket_config.get('policy'):
            try:
                self.s3.put_bucket_policy(
                    Bucket=bucket_config['name'],
                    Policy=json.dumps(bucket_config['policy'])
                )
            except Exception as e:
                logger.warning(f"Failed to set bucket policy: {e}")
        
        logger.info(f"S3 bucket created: {bucket_config['name']}")
        
        return {
            'bucket_name': bucket_config['name'],
            'region': self.config.region
        }
    
    async def _deploy_load_balancer(self, lb_config: dict) -> dict:
        """Deploy Application Load Balancer"""
        logger.info("Deploying Load Balancer")
        
        # Create target group
        tg_response = self.elb.create_target_group(
            Name=lb_config['target_group_name'],
            Protocol=lb_config.get('protocol', 'HTTP'),
            Port=lb_config['port'],
            VpcId=lb_config['vpc_id'],
            HealthCheckProtocol=lb_config.get('health_check_protocol', 'HTTP'),
            HealthCheckPath=lb_config.get('health_check_path', '/'),
            HealthCheckIntervalSeconds=lb_config.get('health_check_interval', 30),
            HealthyThresholdCount=lb_config.get('healthy_threshold', 3),
            UnhealthyThresholdCount=lb_config.get('unhealthy_threshold', 3)
        )
        
        target_group_arn = tg_response['TargetGroups'][0]['TargetGroupArn']
        
        # Create load balancer
        lb_response = self.elb.create_load_balancer(
            Name=lb_config['name'],
            Subnets=lb_config['subnet_ids'],
            SecurityGroups=lb_config.get('security_group_ids', []),
            Scheme=lb_config.get('scheme', 'internet-facing'),
            Type='application',
            IpAddressType=lb_config.get('ip_address_type', 'ipv4')
        )
        
        load_balancer_arn = lb_response['LoadBalancers'][0]['LoadBalancerArn']
        dns_name = lb_response['LoadBalancers'][0]['DNSName']
        
        # Create listener
        self.elb.create_listener(
            LoadBalancerArn=load_balancer_arn,
            Protocol=lb_config.get('listener_protocol', 'HTTP'),
            Port=lb_config.get('listener_port', 80),
            DefaultActions=[{
                'Type': 'forward',
                'TargetGroupArn': target_group_arn
            }]
        )
        
        logger.info(f"Load balancer created: {lb_config['name']}")
        
        return {
            'load_balancer_arn': load_balancer_arn,
            'dns_name': dns_name,
            'target_group_arn': target_group_arn
        }
    
    async def get_resource(self, resource_id: str) -> dict:
        """Get resource details"""
        logger.info(f"Getting resource: {resource_id}")
        
        # This is a simplified implementation
        # In production, you'd need to determine resource type and call appropriate APIs
        
        return {
            'resource_id': resource_id,
            'status': 'available'
        }
    
    async def delete_resource(self, resource_id: str) -> bool:
        """Delete resource"""
        logger.info(f"Deleting resource: {resource_id}")
        
        # This is a simplified implementation
        # In production, you'd need to determine resource type and call appropriate delete APIs
        
        return True
    
    async def get_metrics(self, resource_id: str) -> dict:
        """Get resource metrics"""
        logger.info(f"Getting metrics for resource: {resource_id}")
        
        # Get metrics from CloudWatch
        # This is a simplified implementation
        
        return {
            'resource_id': resource_id,
            'metrics': {
                'cpu_utilization': 0.0,
                'memory_utilization': 0.0,
                'network_in': 0.0,
                'network_out': 0.0
            }
        }
    
    def get_provider_info(self) -> Dict[str, Any]:
        """Get provider information"""
        return {
            'provider_name': self.PROVIDER_NAME,
            'provider_version': self.PROVIDER_VERSION,
            'region': self.config.region,
            'available_services': [
                'ec2', 'eks', 'rds', 's3', 'elb', 'iam', 'route53',
                'cloudwatch', 'lambda', 'secrets-manager'
            ]
        }
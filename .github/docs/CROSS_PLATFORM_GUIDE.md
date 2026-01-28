# GL Unified Charter Activated
# Cross-Platform Deployment Guide

## Overview

This guide provides comprehensive instructions for deploying MachineNativeOps across multiple platforms and environments, ensuring maximum flexibility and compatibility.

---

## Supported Platforms

### Cloud Providers
- **AWS** (Amazon Web Services)
  - EKS (Elastic Kubernetes Service)
  - EC2 (Elastic Compute Cloud)
  - RDS, ElastiCache, S3, CloudWatch, etc.

- **GCP** (Google Cloud Platform)
  - GKE (Google Kubernetes Engine)
  - GCE (Google Compute Engine)
  - Cloud SQL, Memorystore, Cloud Storage, etc.

- **Azure** (Microsoft Azure)
  - AKS (Azure Kubernetes Service)
  - Azure VMs
  - Azure SQL, Redis Cache, Blob Storage, etc.

### On-Premise
- **Kubernetes** (Self-hosted)
- **Docker Compose**
- **Nomad**
- **Bare Metal / Systemd**

### Hybrid Cloud
- Multi-cloud deployments
- Hybrid cloud with on-prem integration
- Edge computing support

---

## Configuration Structure

### Platform-Agnostic Configuration Files

```
k8s/production/
├── platform-agnostic-config.yaml      # Multi-cloud provider support
├── universal-deployment.yaml          # Universal deployment options
├── cross-platform-monitoring.yaml     # Multi-platform monitoring
├── cross-platform-storage.yaml        # Multi-platform storage
└── cross-platform-networking.yaml     # Multi-platform networking
```

### Key Components

#### 1. Platform-Agnostic Configuration
- Cloud provider selection (AWS, GCP, Azure, On-prem)
- Service mapping for each provider
- Storage backends (S3, GCS, Azure Blob, MinIO)
- Database backends (PostgreSQL, MySQL, MongoDB, Redis)
- Message queues (SQS, Pub/Sub, Service Bus, Kafka)
- Monitoring backends (Prometheus, CloudWatch, Cloud Monitoring)
- Logging backends (CloudWatch Logs, Cloud Logging, Log Analytics)
- Secrets management (Secrets Manager, Parameter Store, Vault)

#### 2. Universal Deployment
- Kubernetes Deployment with comprehensive configuration
- Docker Compose for container orchestration
- Nomad Job specification for HashiCorp Nomad
- Systemd service for bare metal deployments
- Helm Chart for package management

#### 3. Cross-Platform Monitoring
- OpenTelemetry universal collectors
- Prometheus configuration
- CloudWatch integration
- Google Cloud Monitoring integration
- Azure Monitor integration
- Grafana dashboards

#### 4. Cross-Platform Storage
- Universal Storage Interface
- Object Storage (S3-compatible, GCS, Azure Blob)
- Database Storage (RDS, Cloud SQL, Azure SQL)
- Cache Storage (ElastiCache, Memorystore, Redis Cache)
- Backup Storage (Multi-region replication)

#### 5. Cross-Platform Networking
- Network topology configuration
- VPC/VNet configuration
- Service discovery (CoreDNS, Cloud Map, Consul)
- Load balancing (ALB/NLB, Cloud Load Balancing, Azure LB)

---

## Deployment Instructions

### AWS Deployment

#### Prerequisites
```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Install eksctl
curl --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin/
```

#### Environment Variables
```bash
export AWS_REGION=us-east-1
export CLUSTER_NAME=machine-native-ops-prod
export VPC_CIDR=10.0.0.0/16
export BUCKET_NAME=machine-native-ops-prod
export KMS_KEY_ID=arn:aws:kms:us-east-1:123456789012:key/abcd1234-5678-90ab-cdef-1234567890ab
export DATABASE_URL=postgresql://user:password@hostname:5432/dbname
export REDIS_URL=redis://hostname:6379
```

#### Deployment Steps
```bash
# 1. Create EKS cluster
eksctl create cluster \
  --name ${CLUSTER_NAME} \
  --region ${AWS_REGION} \
  --nodes 3 \
  --node-type t3.xlarge \
  --node-ami-family AmazonLinux2 \
  --managed

# 2. Configure kubectl
aws eks update-kubeconfig --name ${CLUSTER_NAME} --region ${AWS_REGION}

# 3. Create namespace
kubectl create namespace production

# 4. Apply configurations
kubectl apply -f k8s/production/platform-agnostic-config.yaml
kubectl apply -f k8s/production/universal-deployment.yaml
kubectl apply -f k8s/production/cross-platform-monitoring.yaml
kubectl apply -f k8s/production/cross-platform-storage.yaml
kubectl apply -f k8s/production/cross-platform-networking.yaml

# 5. Create secrets
kubectl create secret generic database-credentials \
  --from-literal=url=${DATABASE_URL}

kubectl create secret generic redis-credentials \
  --from-literal=url=${REDIS_URL}

# 6. Deploy application
kubectl apply -f k8s/production/deployment.yaml

# 7. Verify deployment
kubectl get pods -n production
kubectl get services -n production
```

---

### GCP Deployment

#### Prerequisites
```bash
# Install Google Cloud SDK
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init

# Install kubectl
gcloud components install kubectl
```

#### Environment Variables
```bash
export GCP_PROJECT=my-project
export GCP_REGION=us-central1
export GCP_ZONE=us-central1-a
export CLUSTER_NAME=machine-native-ops-prod
export GCS_BUCKET=machine-native-ops-prod
export DATABASE_URL=postgresql://user:password@hostname:5432/dbname
export REDIS_URL=redis://hostname:6379
```

#### Deployment Steps
```bash
# 1. Create GKE cluster
gcloud container clusters create ${CLUSTER_NAME} \
  --region ${GCP_REGION} \
  --num-nodes 3 \
  --machine-type e2-standard-4 \
  --enable-autoscaling \
  --min-nodes 3 \
  --max-nodes 10 \
  --enable-ip-alias \
  --enable-private-nodes

# 2. Configure kubectl
gcloud container clusters get-credentials ${CLUSTER_NAME} --region ${GCP_REGION}

# 3. Create namespace
kubectl create namespace production

# 4. Create service account
gcloud iam service-accounts create machine-native-ops \
  --project=${GCP_PROJECT}

gcloud projects add-iam-policy-binding ${GCP_PROJECT} \
  --member="serviceAccount:machine-native-ops@${GCP_PROJECT}.iam.gserviceaccount.com" \
  --role="roles/storage.objectAdmin"

gcloud iam service-accounts keys create key.json \
  --iam-account=machine-native-ops@${GCP_PROJECT}.iam.gserviceaccount.com

# 5. Apply configurations
kubectl apply -f k8s/production/platform-agnostic-config.yaml
kubectl apply -f k8s/production/universal-deployment.yaml
kubectl apply -f k8s/production/cross-platform-monitoring.yaml
kubectl apply -f k8s/production/cross-platform-storage.yaml
kubectl apply -f k8s/production/cross-platform-networking.yaml

# 6. Create secrets
kubectl create secret generic database-credentials \
  --from-literal=url=${DATABASE_URL}

kubectl create secret generic redis-credentials \
  --from-literal=url=${REDIS_URL}

kubectl create secret generic gcp-credentials \
  --from-file=key.json

# 7. Deploy application
kubectl apply -f k8s/production/deployment.yaml

# 8. Verify deployment
kubectl get pods -n production
kubectl get services -n production
```

---

### Azure Deployment

#### Prerequisites
```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Install kubectl
az aks install-cli
```

#### Environment Variables
```bash
export RESOURCE_GROUP=machine-native-ops-rg
export AZURE_LOCATION=EastUS
export CLUSTER_NAME=machine-native-ops-prod
export AZURE_STORAGE_ACCOUNT=machineopsstorage
export CONTAINER_NAME=machine-native-ops
export DATABASE_URL=postgresql://user:password@hostname:5432/dbname
export REDIS_URL=redis://hostname:6379
```

#### Deployment Steps
```bash
# 1. Create resource group
az group create --name ${RESOURCE_GROUP} --location ${AZURE_LOCATION}

# 2. Create AKS cluster
az aks create \
  --resource-group ${RESOURCE_GROUP} \
  --name ${CLUSTER_NAME} \
  --node-count 3 \
  --node-vm-size Standard_DS4_v2 \
  --enable-cluster-autoscaler \
  --min-count 3 \
  --max-count 10 \
  --enable-managed-identity \
  --network-plugin azure

# 3. Configure kubectl
az aks get-credentials --resource-group ${RESOURCE_GROUP} --name ${CLUSTER_NAME}

# 4. Create namespace
kubectl create namespace production

# 5. Apply configurations
kubectl apply -f k8s/production/platform-agnostic-config.yaml
kubectl apply -f k8s/production/universal-deployment.yaml
kubectl apply -f k8s/production/cross-platform-monitoring.yaml
kubectl apply -f k8s/production/cross-platform-storage.yaml
kubectl apply -f k8s/production/cross-platform-networking.yaml

# 6. Create secrets
kubectl create secret generic database-credentials \
  --from-literal=url=${DATABASE_URL}

kubectl create secret generic redis-credentials \
  --from-literal=url=${REDIS_URL}

# 7. Deploy application
kubectl apply -f k8s/production/deployment.yaml

# 8. Verify deployment
kubectl get pods -n production
kubectl get services -n production
```

---

### Docker Compose Deployment

#### Prerequisites
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### Environment Variables
```bash
export IMAGE_REGISTRY=docker.io
export VERSION=latest
export REPLICAS=3
export LOG_LEVEL=info
export DATABASE_URL=postgresql://user:password@localhost:5432/dbname
export REDIS_URL=redis://localhost:6379
export STORAGE_BACKEND=s3
export S3_BUCKET=machine-native-ops
export S3_REGION=us-east-1
export POSTGRES_DB=machine_native_ops
export POSTGRES_USER=machine_ops
export POSTGRES_PASSWORD=secure_password
```

#### Deployment Steps
```bash
# 1. Create .env file
cat > .env << EOF
IMAGE_REGISTRY=${IMAGE_REGISTRY}
VERSION=${VERSION}
REPLICAS=${REPLICAS}
LOG_LEVEL=${LOG_LEVEL}
DATABASE_URL=${DATABASE_URL}
REDIS_URL=${REDIS_URL}
STORAGE_BACKEND=${STORAGE_BACKEND}
S3_BUCKET=${S3_BUCKET}
S3_REGION=${S3_REGION}
POSTGRES_DB=${POSTGRES_DB}
POSTGRES_USER=${POSTGRES_USER}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
EOF

# 2. Extract Docker Compose configuration from universal-deployment.yaml
# (The YAML contains the docker-compose.yaml embedded)

# 3. Start services
docker-compose up -d

# 4. Verify services
docker-compose ps
docker-compose logs -f
```

---

### Nomad Deployment

#### Prerequisites
```bash
# Install Nomad
wget https://releases.hashicorp.com/nomad/1.5.0/nomad_1.5.0_linux_amd64.zip
unzip nomad_1.5.0_linux_amd64.zip
sudo mv nomad /usr/local/bin/
```

#### Environment Variables
```bash
export IMAGE_REGISTRY=docker.io
export VERSION=latest
export REPLICAS=3
export DATABASE_URL=postgresql://user:password@hostname:5432/dbname
export REDIS_URL=redis://hostname:6379
```

#### Deployment Steps
```bash
# 1. Extract Nomad job configuration from universal-deployment.yaml
# (The YAML contains the nomad.yaml embedded)

# 2. Validate job
nomad job validate nomad.yaml

# 3. Run job
nomad job run nomad.yaml

# 4. Verify job
nomad job status machine-native-ops
nomad alloc logs
```

---

### Bare Metal Deployment

#### Prerequisites
```bash
# Install systemd
sudo apt-get update
sudo apt-get install systemd -y

# Create user
sudo useradd -r -s /bin/false machine-native-ops
sudo mkdir -p /opt/machine-native-ops
sudo chown -R machine-native-ops:machine-native-ops /opt/machine-native-ops
```

#### Environment Variables
```bash
export LOG_LEVEL=info
export DATABASE_URL=postgresql://user:password@localhost:5432/dbname
export REDIS_URL=redis://localhost:6379
```

#### Deployment Steps
```bash
# 1. Extract systemd service configuration from universal-deployment.yaml
# (The YAML contains the systemd.yaml embedded)

# 2. Create service file
cat > /etc/systemd/system/machine-native-ops.service << 'EOF'
[Unit]
Description=MachineNativeOps Application
After=network.target postgresql.service redis.service
Requires=network.target

[Service]
Type=simple
User=machine-native-ops
Group=machine-native-ops
WorkingDirectory=/opt/machine-native-ops
ExecStart=/opt/machine-native-ops/bin/machine-native-ops \
  --config /etc/machine-native-ops/config.yaml \
  --log-level ${LOG_LEVEL:-info} \
  --port 8080 \
  --metrics-port 9090

Environment="ENVIRONMENT=production"
Environment="LOG_LEVEL=${LOG_LEVEL:-info}"
Environment="DATABASE_URL=${DATABASE_URL}"
Environment="REDIS_URL=${REDIS_URL}"

Restart=always
RestartSec=10
StartLimitInterval=60
StartLimitBurst=3

NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true

LimitNOFILE=65536
LimitNPROC=4096

StandardOutput=journal
StandardError=journal
SyslogIdentifier=machine-native-ops

[Install]
WantedBy=multi-user.target
EOF

# 3. Reload systemd
sudo systemctl daemon-reload

# 4. Enable and start service
sudo systemctl enable machine-native-ops
sudo systemctl start machine-native-ops

# 5. Verify service
sudo systemctl status machine-native-ops
sudo journalctl -u machine-native-ops -f
```

---

## Configuration Management

### Environment Variables

All configurations support environment variable substitution using the `${VARIABLE_NAME:-default}` syntax.

### Configuration Priority
1. Environment variables (highest priority)
2. Configuration files
3. Default values (lowest priority)

### Multi-Environment Support

```bash
# Development
export ENVIRONMENT=development
export LOG_LEVEL=debug
export REPLICAS=1

# Staging
export ENVIRONMENT=staging
export LOG_LEVEL=info
export REPLICAS=2

# Production
export ENVIRONMENT=production
export LOG_LEVEL=warn
export REPLICAS=3
```

---

## Monitoring and Logging

### Universal Monitoring

All platforms support:
- Prometheus metrics
- OpenTelemetry traces
- Structured logging
- Health checks

### Platform-Specific Monitoring

- **AWS**: CloudWatch metrics and logs
- **GCP**: Cloud Monitoring and Cloud Logging
- **Azure**: Monitor and Log Analytics

---

## Troubleshooting

### Common Issues

#### 1. Connectivity Issues
```bash
# Check pod status
kubectl get pods -n production

# Check pod logs
kubectl logs -n production <pod-name>

# Describe pod
kubectl describe pod -n production <pod-name>
```

#### 2. Storage Issues
```bash
# Check PVC status
kubectl get pvc -n production

# Check PV status
kubectl get pv

# Describe PVC
kubectl describe pvc <pvc-name> -n production
```

#### 3. Network Issues
```bash
# Check services
kubectl get svc -n production

# Check endpoints
kubectl get endpoints -n production

# Test connectivity
kubectl run -it --rm debug --image=busybox --restart=Never -- wget -O- http://service-name:port/health
```

---

## Best Practices

1. **Use GitOps**: Store configurations in Git and use tools like ArgoCD or FluxCD
2. **Secret Management**: Use proper secret management solutions (Vault, AWS Secrets Manager, etc.)
3. **Immutable Infrastructure**: Treat infrastructure as code
4. **Observability**: Implement comprehensive monitoring and logging
5. **Security**: Apply security best practices (network policies, RBAC, encryption)
6. **Disaster Recovery**: Implement backup and DR strategies
7. **Cost Optimization**: Monitor and optimize cloud costs

---

## Support

For issues or questions:
- GitHub Issues: https://github.com/MachineNativeOps/machine-native-ops/issues
- Documentation: https://docs.machine-native-ops.com
- Community: https://community.machine-native-ops.com
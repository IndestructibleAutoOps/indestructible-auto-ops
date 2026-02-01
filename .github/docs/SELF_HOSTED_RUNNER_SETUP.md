<!-- @GL-governed -->
<!-- @GL-layer: GL90-99 -->
<!-- @GL-semantic: governed-documentation -->
<!-- @GL-audit-trail: engine/governance/GL_SEMANTIC_ANCHOR.json -->

# GL Unified Charter Activated
# Self-Hosted Runner Setup Guide

This guide provides comprehensive instructions for setting up self-hosted GitHub Actions runners for the machine-native-ops CI/CD pipeline.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Server Requirements](#server-requirements)
3. [Runner Installation](#runner-installation)
4. [Runner Configuration](#runner-configuration)
5. [Security Hardening](#security-hardening)
6. [Monitoring & Maintenance](#monitoring--maintenance)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Hardware Requirements

| Environment | CPU | RAM | Storage | Network |
|-------------|-----|-----|---------|---------|
| Staging | 2+ cores | 4GB+ | 50GB SSD | 100Mbps+ |
| Production | 4+ cores | 8GB+ | 100GB SSD | 1Gbps+ |

### Software Requirements

- **Operating System**: Ubuntu 22.04 LTS (recommended) or Debian 11+
- **Docker**: 24.0+ with Docker Compose v2
- **Node.js**: 20.x LTS
- **Git**: 2.40+
- **PM2**: Latest (for process management)

---

## Server Requirements

### 1. System Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y \
    curl \
    wget \
    git \
    jq \
    unzip \
    build-essential \
    ca-certificates \
    gnupg \
    lsb-release \
    software-properties-common
```

### 2. Install Docker

```bash
# Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL [EXTERNAL_URL_REMOVED] | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] [EXTERNAL_URL_REMOVED] \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Add runner user to docker group
sudo usermod -aG docker $USER
```

### 3. Install Node.js

```bash
# Install Node.js 20.x
curl -fsSL [EXTERNAL_URL_REMOVED] | sudo -E bash -
sudo apt install -y nodejs

# Verify installation
node --version
npm --version

# Install PM2 globally
sudo npm install -g pm2
```

### 4. Create Runner User

```bash
# Create dedicated runner user
sudo useradd -m -s /bin/bash github-runner
sudo usermod -aG docker github-runner
sudo usermod -aG sudo github-runner

# Set up SSH access (optional)
sudo mkdir -p /home/github-runner/.ssh
sudo chmod 700 /home/github-runner/.ssh
```

---

## Runner Installation

### 1. Download GitHub Actions Runner

```bash
# Switch to runner user
sudo su - github-runner

# Create runner directory
mkdir -p ~/actions-runner && cd ~/actions-runner

# Determine architecture
ARCH=$(uname -m)
RUNNER_VERSION="2.331.0"

# Download runner based on architecture
if [ "$ARCH" = "x86_64" ]; then
    # For x64/AMD64 systems
    curl -o actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz -L \
        [EXTERNAL_URL_REMOVED]}/actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz
    
    # Validate hash (x64)
    echo "7e8e2095d2c30bbaa3d2ef03505622b883d9116a1b62d0a2050a1a8a4e37decd  actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz" | shasum -a 256 -c
    
    # Extract
    tar xzf ./actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz
    
elif [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
    # For ARM64 systems (e.g., AWS Graviton, Apple Silicon, Raspberry Pi 4)
    curl -o actions-runner-linux-arm64-${RUNNER_VERSION}.tar.gz -L \
        [EXTERNAL_URL_REMOVED]}/actions-runner-linux-arm64-${RUNNER_VERSION}.tar.gz
    
    # Validate hash (ARM64)
    echo "f5863a211241436186723159a111f352f25d5d22711639761ea24c98caef1a9a  actions-runner-linux-arm64-${RUNNER_VERSION}.tar.gz" | shasum -a 256 -c
    
    # Extract
    tar xzf ./actions-runner-linux-arm64-${RUNNER_VERSION}.tar.gz
else
    echo "Unsupported architecture: $ARCH"
    exit 1
fi
```

#### Quick Setup for ARM64 (Copy-Paste Ready)

```bash
# Create a folder
mkdir actions-runner && cd actions-runner

# Download the latest runner package for ARM64
curl -o actions-runner-linux-arm64-2.331.0.tar.gz -L [EXTERNAL_URL_REMOVED]

# Validate the hash
echo "f5863a211241436186723159a111f352f25d5d22711639761ea24c98caef1a9a  actions-runner-linux-arm64-2.331.0.tar.gz" | shasum -a 256 -c

# Extract the installer
tar xzf ./actions-runner-linux-arm64-2.331.0.tar.gz
```

### 2. Configure Runner

```bash
# Get registration token from GitHub
# Go to: Repository Settings > Actions > Runners > New self-hosted runner
# Copy the token

# Determine architecture label
ARCH=$(uname -m)
if [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
    ARCH_LABEL="arm64"
else
    ARCH_LABEL="x64"
fi

# Configure runner for STAGING
./config.sh \
    --url [EXTERNAL_URL_REMOVED] \
    --token YOUR_REGISTRATION_TOKEN \
    --name "staging-runner-01" \
    --labels "self-hosted,staging,linux,${ARCH_LABEL}" \
    --work "_work" \
    --runnergroup "Default"

# OR Configure runner for PRODUCTION
./config.sh \
    --url [EXTERNAL_URL_REMOVED] \
    --token YOUR_REGISTRATION_TOKEN \
    --name "production-runner-01" \
    --labels "self-hosted,production,linux,${ARCH_LABEL}" \
    --work "_work" \
    --runnergroup "Default"
```

#### ARM64 Specific Configuration

For ARM64 runners (AWS Graviton, Apple Silicon, etc.):

```bash
# Configure runner for STAGING (ARM64)
./config.sh \
    --url [EXTERNAL_URL_REMOVED] \
    --token YOUR_REGISTRATION_TOKEN \
    --name "staging-runner-arm64-01" \
    --labels "self-hosted,staging,linux,arm64" \
    --work "_work" \
    --runnergroup "Default"

# Configure runner for PRODUCTION (ARM64)
./config.sh \
    --url [EXTERNAL_URL_REMOVED] \
    --token YOUR_REGISTRATION_TOKEN \
    --name "production-runner-arm64-01" \
    --labels "self-hosted,production,linux,arm64" \
    --work "_work" \
    --runnergroup "Default"
```

### 3. Install as Service

```bash
# Install service
sudo ./svc.sh install github-runner

# Start service
sudo ./svc.sh start

# Check status
sudo ./svc.sh status

# Enable on boot
sudo systemctl enable actions.runner.MachineNativeOps-machine-native-ops.staging-runner-01.service
```

---

## Runner Configuration

### 1. Environment Variables

Create `/home/github-runner/.env`:

```bash
# Runner Environment Configuration
NODE_ENV=production
RUNNER_ENVIRONMENT=staging  # or production

# Deployment Directories
DEPLOY_DIR=/opt/deployments
BACKUP_DIR=/opt/deployments/backups
LOG_DIR=/var/log/deployments

# Blue-Green Configuration
BLUE_PORT=3001
GREEN_PORT=3002
BLUE_HOST=localhost
GREEN_HOST=localhost

# Docker Registry (optional)
DOCKER_REGISTRY=ghcr.io
DOCKER_IMAGE=machinenativeops/machine-native-ops
```

### 2. Directory Structure

```bash
# Create deployment directories
sudo mkdir -p /opt/deployments/{staging,production}/{blue,green}
sudo mkdir -p /opt/deployments/backups
sudo mkdir -p /var/log/deployments
sudo mkdir -p /var/lib/deployment

# Set permissions
sudo chown -R github-runner:github-runner /opt/deployments
sudo chown -R github-runner:github-runner /var/log/deployments
sudo chown -R github-runner:github-runner /var/lib/deployment
```

### 3. Load Balancer Configuration (Nginx)

Create `/etc/nginx/conf.d/app.conf`:

```nginx
# Upstream configuration for blue-green deployment
upstream app_backend {
    server localhost:3001 weight=100;  # Blue
    server localhost:3002 weight=0;    # Green
    keepalive 32;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass [EXTERNAL_URL_REMOVED]
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 90;
    }

    location /health {
        proxy_pass [EXTERNAL_URL_REMOVED]
        proxy_http_version 1.1;
    }

    # Blue environment direct access (internal)
    location /blue/ {
        internal;
        proxy_pass [EXTERNAL_URL_REMOVED]
    }

    # Green environment direct access (internal)
    location /green/ {
        internal;
        proxy_pass [EXTERNAL_URL_REMOVED]
    }
}
```

---

## Security Hardening

### 1. Firewall Configuration

```bash
# Install UFW
sudo apt install -y ufw

# Default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH
sudo ufw allow ssh

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow internal ports (only from localhost)
sudo ufw allow from 127.0.0.1 to any port 3001
sudo ufw allow from 127.0.0.1 to any port 3002

# Enable firewall
sudo ufw enable
```

### 2. Runner Security

```bash
# Limit runner permissions
sudo visudo

# Add line:
# github-runner ALL=(ALL) NOPASSWD: /usr/bin/docker, /usr/bin/systemctl, /usr/bin/nginx

# Secure runner directory
chmod 700 /home/github-runner/actions-runner
```

### 3. Secret Management

```bash
# Create secrets directory
sudo mkdir -p /etc/deployment-secrets
sudo chmod 700 /etc/deployment-secrets

# Store secrets (example)
echo "your-database-url" | sudo tee /etc/deployment-secrets/database_url
sudo chmod 600 /etc/deployment-secrets/*
```

---

## Monitoring & Maintenance

### 1. Log Rotation

Create `/etc/logrotate.d/deployments`:

```
/var/log/deployments/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 github-runner github-runner
    sharedscripts
    postrotate
        systemctl reload nginx > /dev/null 2>&1 || true
    endscript
}
```

### 2. Health Check Script

Create `/opt/scripts/runner-health-check.sh`:

```bash
#!/bin/bash
# Runner Health Check Script

check_service() {
    local service=$1
    if systemctl is-active --quiet "$service"; then
        echo "✅ $service: running"
        return 0
    else
        echo "❌ $service: not running"
        return 1
    fi
}

check_port() {
    local port=$1
    local name=$2
    if curl -sf "[EXTERNAL_URL_REMOVED] > /dev/null 2>&1; then
        echo "✅ $name (port $port): healthy"
        return 0
    else
        echo "⚠️ $name (port $port): not responding"
        return 1
    fi
}

echo "=== Runner Health Check ==="
echo "Date: $(date)"
echo ""

# Check services
check_service "actions.runner.*"
check_service "docker"
check_service "nginx"

echo ""

# Check applications
check_port 3001 "Blue Environment"
check_port 3002 "Green Environment"

echo ""

# System resources
echo "=== System Resources ==="
echo "CPU: $(top -bn1 | grep 'Cpu(s)' | awk '{print $2}')%"
echo "Memory: $(free -m | awk 'NR==2{printf "%.1f%%", $3*100/$2}')"
echo "Disk: $(df -h / | awk 'NR==2{print $5}')"
```

### 3. Automated Cleanup

Create cron job for cleanup:

```bash
# Edit crontab
crontab -e

# Add cleanup job (runs daily at 3 AM)
0 3 * * * /opt/scripts/cleanup-old-deployments.sh >> /var/log/deployments/cleanup.log 2>&1
```

---

## Troubleshooting

### Common Issues

#### 1. Runner Not Starting

```bash
# Check service status
sudo systemctl status actions.runner.*

# View logs
sudo journalctl -u actions.runner.* -f

# Restart runner
sudo ./svc.sh stop
sudo ./svc.sh start
```

#### 2. Docker Permission Denied

```bash
# Add user to docker group
sudo usermod -aG docker github-runner

# Restart runner service
sudo systemctl restart actions.runner.*
```

#### 3. Port Already in Use

```bash
# Find process using port
sudo lsof -i :3001

# Kill process
sudo kill -9 <PID>

# Or use fuser
sudo fuser -k 3001/tcp
```

#### 4. Deployment Failures

```bash
# Check deployment logs
tail -f /var/log/deployments/*.log

# Check application logs
pm2 logs
docker logs <container-name>
```

### Recovery Procedures

#### Quick Rollback

```bash
# Switch to previous environment
./scripts/switch-traffic.sh blue 100  # or green

# Full rollback
./scripts/rollback.sh previous production
```

#### Manual Recovery

```bash
# Stop all services
docker compose down
pm2 delete all

# Restore from backup
cp -r /opt/deployments/backups/latest/* /opt/deployments/production/blue/

# Restart
cd /opt/deployments/production/blue
docker compose up -d
```

---

## GitHub Secrets Configuration

Configure these secrets in your GitHub repository:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `GL_TOKEN` | GitHub Personal Access Token | `ghp_xxxx` |
| `STAGING_URL` | Staging environment URL | `[EXTERNAL_URL_REMOVED] |
| `PRODUCTION_URL` | Production environment URL | `[EXTERNAL_URL_REMOVED] |
| `PRODUCTION_BLUE_URL` | Blue environment URL | `[EXTERNAL_URL_REMOVED] |
| `PRODUCTION_GREEN_URL` | Green environment URL | `[EXTERNAL_URL_REMOVED] |
| `STAGING_DATABASE_URL` | Staging database connection | `postgresql://...` |
| `PRODUCTION_DATABASE_URL` | Production database connection | `postgresql://...` |
| `SLACK_WEBHOOK` | Slack notification webhook | `[EXTERNAL_URL_REMOVED] |

---

## Support

For issues or questions:
- Create an issue in the repository
- Check the [CI/CD SOP](../CI_CD_SOP.md)
- Review workflow logs in GitHub Actions

**GL Unified Charter Activated** ✅
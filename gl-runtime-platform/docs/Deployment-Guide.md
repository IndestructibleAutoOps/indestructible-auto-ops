# GL Runtime Platform Deployment Guide

**Version:** 21.0.0  
**Branch:** main  
**Last Updated:** 2026-01-29

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Enterprise Automation Architecture](#enterprise-automation-architecture)
5. [Deployment](#deployment)
6. [Monitoring](#monitoring)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

- **OS:** Linux (Ubuntu 20.04+ recommended)
- **Node.js:** v20.x or higher
- **npm:** v9.x or higher
- **Memory:** Minimum 4GB, Recommended 8GB+
- **CPU:** Minimum 2 cores, Recommended 4+ cores
- **Disk Space:** Minimum 10GB

### Required Tools

```bash
# Install Node.js 20
curl -fsSL [EXTERNAL_URL_REMOVED] | sudo -E bash -
sudo apt-get install -y nodejs

# Install Git
sudo apt-get install -y git

# Install Docker (optional, for containerized deployment)
curl -fsSL [EXTERNAL_URL_REMOVED] | sh
```

---

## Installation

### 1. Clone the Repository

```bash
git clone [EXTERNAL_URL_REMOVED]
cd machine-native-ops
```

### 2. Install Dependencies

```bash
cd gl-execution-runtime
npm install
```

### 3. Build the Project

```bash
npm run build
```

### 4. Run Tests

```bash
# Run integration tests
npx ts-node tests/integration-main/run-integration-tests-simple.ts

# Run all tests
npm test
```

---

## Configuration

### Environment Variables

Create a `.env` file in the `gl-execution-runtime` directory:

```env
# Node Environment
NODE_ENV=production

# Server Configuration
PORT=3000
HOST=0.0.0.0

# Fabric Configuration
FABRIC_ENDPOINT=fabric://v19-unified
FABRIC_TIMEOUT=30000

# Security Configuration
SECURITY_LEVEL=high
ENABLE_GOVERNANCE=true

# DAG Configuration
MAX_CONCURRENCY=100
DAG_TIMEOUT=300000

# Logging
LOG_LEVEL=info
LOG_FILE=/var/log/gl-execution-runtime.log
```

### Governance Configuration

Ensure governance markers are present in all files:

```typescript
/**
 * @GL-governed
 * @version 21.0.0
 * @priority 2
 * @stage complete
 */
```

---

## Enterprise Automation Architecture

The enterprise automation architecture is defined as machine-readable configuration in:

- `docs/architecture/Enterprise-Automation-Platform-Architecture.yaml`

This architecture specification captures the zero-residue execution model, internal-only event flow, and
production automation pipeline described in GL99.

### Zero-Residue Executor

The internal zero-residue executor is provided at:

- `ops/executors/zero-residue-executor.sh`

### Enterprise Deployment Configuration

Production deployment configuration for the enterprise automation platform is defined in:

- `deployment/enterprise-platform-deployment.yaml`

---

## Deployment

### Option 1: Direct Deployment

#### Start the Server

```bash
# Development mode
npm run dev

# Production mode
npm start
```

#### Using PM2 (Recommended for Production)

```bash
# Install PM2
npm install -g pm2

# Start the application
pm2 start dist/index.js --name gl-execution-runtime

# Configure PM2 to start on system boot
pm2 startup
pm2 save
```

### Option 2: Docker Deployment

#### Build Docker Image

```bash
docker build -t gl-execution-runtime:21.0.0 .
```

#### Run Docker Container

```bash
docker run -d \
  --name gl-execution-runtime \
  -p 3000:3000 \
  --env-file .env \
  gl-execution-runtime:21.0.0
```

#### Using Docker Compose

```bash
docker-compose up -d
```

### Option 3: Kubernetes Deployment

#### Apply Kubernetes Manifests

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

#### Verify Deployment

```bash
kubectl get pods
kubectl get services
```

---

## Monitoring

### Health Check

```bash
# Check health endpoint
curl [EXTERNAL_URL_REMOVED]

# Expected response
{
  "status": "healthy",
  "version": "21.0.0",
  "uptime": 3600
}
```

### Logs

```bash
# View application logs
pm2 logs gl-execution-runtime

# View Docker logs
docker logs -f gl-execution-runtime

# View Kubernetes logs
kubectl logs -f deployment/gl-execution-runtime
```

### Metrics

Monitor the following metrics:

- **Response Time:** < 100ms (average)
- **Error Rate:** < 0.1%
- **CPU Usage:** < 70%
- **Memory Usage:** < 80%
- **DAG Execution Time:** < 300s

---

## Troubleshooting

### Common Issues

#### 1. Build Fails

**Problem:** `npm run build` fails with compilation errors

**Solution:**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear TypeScript cache
rm -rf .tsbuildinfo
npm run build
```

#### 2. Tests Fail

**Problem:** Integration tests fail with missing components

**Solution:**
```bash
# Verify all components are present
ls -la fabric-storage/
ls -la code-intel-security-layer/
ls -la global-dag/

# Re-run tests
npx ts-node tests/integration-main/run-integration-tests-simple.ts
```

#### 3. Port Already in Use

**Problem:** `Error: listen EADDRINUSE: address already in use :::3000`

**Solution:**
```bash
# Find process using port 3000
lsof -i :3000

# Kill the process
kill -9 <PID>

# Or use a different port
PORT=3001 npm start
```

#### 4. Governance Validation Fails

**Problem:** Pre-commit validation fails with missing governance markers

**Solution:**
```bash
# Run governance fix script
python3 scripts/add-governance-tags-main.py

# Commit again
git add .
git commit -m "Add governance markers"
```

### Getting Help

1. Check the [GitHub Issues]([EXTERNAL_URL_REMOVED])
2. Review the [API Documentation](./API-Documentation.md)
3. Contact the engineering team

---

## Security Considerations

1. **Never expose tokens or secrets** in configuration files
2. **Use environment variables** for sensitive data
3. **Enable HTTPS** in production
4. **Implement rate limiting** on API endpoints
5. **Regular security audits** using the governance layer
6. **Keep dependencies updated** with `npm audit fix`

---

## Backup and Recovery

### Backup

```bash
# Backup configuration
tar -czf gl-execution-runtime-config-$(date +%Y%m%d).tar.gz .env

# Backup data
tar -czf gl-execution-runtime-data-$(date +%Y%m%d).tar.gz storage/
```

### Recovery

```bash
# Restore configuration
tar -xzf gl-execution-runtime-config-YYYYMMDD.tar.gz

# Restore data
tar -xzf gl-execution-runtime-data-YYYYMMDD.tar.gz
```

---

## Upgrades

### Upgrade Procedure

1. **Backup current version**
2. **Pull latest changes**
   ```bash
   git pull origin main
   ```
3. **Install new dependencies**
   ```bash
   npm install
   ```
4. **Build the project**
   ```bash
   npm run build
   ```
5. **Run tests**
   ```bash
   npm test
   ```
6. **Restart the application**
   ```bash
   pm2 restart gl-execution-runtime
   ```

---

**Generated by:** GL Runtime Platform v21.0.0  
**Governance Status:** ✅ Compliant  
**Last Tested:** 2026-01-29 (All tests passed)
